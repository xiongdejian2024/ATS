class CCUMCUCDPublicCANFDFr03:
    msg_name = "CCUMCUCDPublicCANFDFr03"
    msg_id = 146
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['CCUMCUAD', 'LCUR', 'LCUL']
    sig_group_dict = {'PwrChRiTarSts': ['PwrChRiTarStsContnsPwrChRi1TarSts', 'PwrChRiTarStsContnsPwrChRi2TarSts', 'PwrChRiTarStsContnsPwrChRi3TarSts', 'PwrChRiTarStsContnsPwrChRi4TarSts', 'PwrChRiTarStsContnsPwrChRi5TarSts', 'PwrChRiTarStsSwilPwrChRi10TarSts', 'PwrChRiTarStsSwilPwrChRi11TarSts', 'PwrChRiTarStsSwilPwrChRi12TarSts', 'PwrChRiTarStsSwilPwrChRi13TarSts', 'PwrChRiTarStsSwilPwrChRi14TarSts', 'PwrChRiTarStsSwilPwrChRi15TarSts', 'PwrChRiTarStsSwilPwrChRi16TarSts', 'PwrChRiTarStsSwilPwrChRi17TarSts', 'PwrChRiTarStsSwilPwrChRi18TarSts', 'PwrChRiTarStsSwilPwrChRi19TarSts', 'PwrChRiTarStsSwilPwrChRi1TarSts', 'PwrChRiTarStsSwilPwrChRi20TarSts', 'PwrChRiTarStsSwilPwrChRi21TarSts', 'PwrChRiTarStsSwilPwrChRi22TarSts', 'PwrChRiTarStsSwilPwrChRi23TarSts', 'PwrChRiTarStsSwilPwrChRi24TarSts', 'PwrChRiTarStsSwilPwrChRi25TarSts', 'PwrChRiTarStsSwilPwrChRi26TarSts', 'PwrChRiTarStsSwilPwrChRi27TarSts', 'PwrChRiTarStsSwilPwrChRi28TarSts', 'PwrChRiTarStsSwilPwrChRi29TarSts', 'PwrChRiTarStsSwilPwrChRi2TarSts', 'PwrChRiTarStsSwilPwrChRi3TarSts', 'PwrChRiTarStsSwilPwrChRi4TarSts', 'PwrChRiTarStsSwilPwrChRi5TarSts', 'PwrChRiTarStsSwilPwrChRi6TarSts', 'PwrChRiTarStsSwilPwrChRi7TarSts', 'PwrChRiTarStsSwilPwrChRi8TarSts', 'PwrChRiTarStsSwilPwrChRi9TarSts'], 'VehSpd': ['VehSpdChks', 'VehSpdCntr', 'VehSpdQf', 'VehSpdSpd'], 'ADSSlaveADModeReqVmc': ['ADSSlaveADModeReqVmcAdActiveReq', 'ADSSlaveADModeReqVmcChks', 'ADSSlaveADModeReqVmcCntr'], 'ADSSlaveCtrlStsVmc': ['ADSSlaveCtrlStsVmcAdMode', 'ADSSlaveCtrlStsVmcChks', 'ADSSlaveCtrlStsVmcCntr', 'ADSSlaveCtrlStsVmcCtrlSts', 'ADSSlaveCtrlStsVmcQf', 'ADSSlaveCtrlStsVmcSts'], 'ADSSlaveCtrlSts': ['ADSSlaveCtrlStsAdMode', 'ADSSlaveCtrlStsChks', 'ADSSlaveCtrlStsCntr', 'ADSSlaveCtrlStsCtrlSts', 'ADSSlaveCtrlStsQf', 'ADSSlaveCtrlStsSts'], 'SecBrkEpbReq': ['SecBrkEpbReqAppRel', 'SecBrkEpbReqChks', 'SecBrkEpbReqCntr'], 'PwrChLeTarSts': ['PwrChLeTarStsContnsPwrChLe1TarSts', 'PwrChLeTarStsContnsPwrChLe2TarSts', 'PwrChLeTarStsContnsPwrChLe3TarSts', 'PwrChLeTarStsContnsPwrChLe4TarSts', 'PwrChLeTarStsContnsPwrChLe5TarSts', 'PwrChLeTarStsSwilPwrChLe10TarSts', 'PwrChLeTarStsSwilPwrChLe11TarSts', 'PwrChLeTarStsSwilPwrChLe12TarSts', 'PwrChLeTarStsSwilPwrChLe13TarSts', 'PwrChLeTarStsSwilPwrChLe14TarSts', 'PwrChLeTarStsSwilPwrChLe15TarSts', 'PwrChLeTarStsSwilPwrChLe16TarSts', 'PwrChLeTarStsSwilPwrChLe17TarSts', 'PwrChLeTarStsSwilPwrChLe18TarSts', 'PwrChLeTarStsSwilPwrChLe19TarSts', 'PwrChLeTarStsSwilPwrChLe1TarSts', 'PwrChLeTarStsSwilPwrChLe20TarSts', 'PwrChLeTarStsSwilPwrChLe21TarSts', 'PwrChLeTarStsSwilPwrChLe22TarSts', 'PwrChLeTarStsSwilPwrChLe23TarSts', 'PwrChLeTarStsSwilPwrChLe24TarSts', 'PwrChLeTarStsSwilPwrChLe25TarSts', 'PwrChLeTarStsSwilPwrChLe26TarSts', 'PwrChLeTarStsSwilPwrChLe27TarSts', 'PwrChLeTarStsSwilPwrChLe28TarSts', 'PwrChLeTarStsSwilPwrChLe29TarSts', 'PwrChLeTarStsSwilPwrChLe2TarSts', 'PwrChLeTarStsSwilPwrChLe3TarSts', 'PwrChLeTarStsSwilPwrChLe4TarSts', 'PwrChLeTarStsSwilPwrChLe5TarSts', 'PwrChLeTarStsSwilPwrChLe6TarSts', 'PwrChLeTarStsSwilPwrChLe7TarSts', 'PwrChLeTarStsSwilPwrChLe8TarSts', 'PwrChLeTarStsSwilPwrChLe9TarSts'], 'ADSSlaveSteerOvrdnAllwd': ['ADSSlaveSteerOvrdnAllwdChks', 'ADSSlaveSteerOvrdnAllwdCntr', 'ADSSlaveSteerOvrdnAllwdStrAllwdReq'], 'VehMovgDir': ['VehMovgDirChks', 'VehMovgDirCntr', 'VehMovgDirVehMovgDir'], 'ADSSlaveADModeReq': ['ADSSlaveADModeReqAdActiveReq', 'ADSSlaveADModeReqChks', 'ADSSlaveADModeReqCntr']}
    sig_group_dataid_dict = {'VehSpd': 1043}

    class PwrChRiTarStsSwilPwrChRi12TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi12TarSts"
        sig_start_bit = 251
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
        startbit = 251
        byte = 31
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADSSlaveCtrlStsVmcSts:
        sig_name = "ADSSlaveCtrlStsVmcSts"
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
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 73
        byte = 9
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADSSlaveCtrlStsAdMode:
        sig_name = "ADSSlaveCtrlStsAdMode"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 61
        byte = 7
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class PwrChRiTarStsSwilPwrChRi29TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi29TarSts"
        sig_start_bit = 295
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
        startbit = 295
        byte = 36
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChLeTarStsSwilPwrChLe20TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe20TarSts"
        sig_start_bit = 137
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
        startbit = 137
        byte = 17
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SecBrkEpbReqAppRel:
        sig_name = "SecBrkEpbReqAppRel"
        sig_start_bit = 187
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbSoftSwt_NoReq': 0, 'EpbSoftSwt_Apply': 1, 'EpbSoftSwt_Release': 2, 'EpbSoftSwt_Forbidden': 3, 'EpbSoftSwt_Unknown': 4, 'EpbSoftSwt_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 187
        byte = 23
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class PwrChRiTarStsSwilPwrChRi18TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi18TarSts"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChRiTarStsSwilPwrChRi2TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi2TarSts"
        sig_start_bit = 293
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
        startbit = 293
        byte = 36
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PwrChRiTarStsContnsPwrChRi1TarSts:
        sig_name = "PwrChRiTarStsContnsPwrChRi1TarSts"
        sig_start_bit = 233
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
        startbit = 233
        byte = 29
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PwrChRiTarSts_UB:
        sig_name = "PwrChRiTarSts_UB"
        sig_start_bit = 170
        update_id_bit = 170
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 170
        byte = 21
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChRiTarStsSwilPwrChRi13TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi13TarSts"
        sig_start_bit = 249
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
        startbit = 249
        byte = 31
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADSSlaveSteerOvrdnAllwdCntr:
        sig_name = "ADSSlaveSteerOvrdnAllwdCntr"
        sig_start_bit = 102
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
        startbit = 102
        byte = 12
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class PwrChLeTarStsSwilPwrChLe21TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe21TarSts"
        sig_start_bit = 123
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
        startbit = 123
        byte = 15
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VehMovgDirChks:
        sig_name = "VehMovgDirChks"
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

    class PwrChRiTarStsSwilPwrChRi1TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi1TarSts"
        sig_start_bit = 267
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
        startbit = 267
        byte = 33
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChLeTarStsSwilPwrChLe2TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe2TarSts"
        sig_start_bit = 135
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
        startbit = 135
        byte = 16
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChLeTarStsSwilPwrChLe26TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe26TarSts"
        sig_start_bit = 173
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
        startbit = 173
        byte = 21
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PwrChLeTarStsSwilPwrChLe17TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe17TarSts"
        sig_start_bit = 121
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
        startbit = 121
        byte = 15
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PwrChRiTarStsSwilPwrChRi4TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi4TarSts"
        sig_start_bit = 289
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
        startbit = 289
        byte = 36
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PwrChRiTarStsSwilPwrChRi20TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi20TarSts"
        sig_start_bit = 265
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
        startbit = 265
        byte = 33
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehSpdCntr:
        sig_name = "VehSpdCntr"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PwrChLeTarStsSwilPwrChLe9TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe9TarSts"
        sig_start_bit = 117
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
        startbit = 117
        byte = 14
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PwrChRiTarStsSwilPwrChRi3TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi3TarSts"
        sig_start_bit = 291
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
        startbit = 291
        byte = 36
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SecBrkEpbReqCntr:
        sig_name = "SecBrkEpbReqCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ADSSlaveSteerOvrdnAllwdStrAllwdReq:
        sig_name = "ADSSlaveSteerOvrdnAllwdStrAllwdReq"
        sig_start_bit = 103
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
        startbit = 103
        byte = 12
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChRiTarStsSwilPwrChRi15TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi15TarSts"
        sig_start_bit = 261
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
        startbit = 261
        byte = 32
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PwrChLeTarStsSwilPwrChLe28TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe28TarSts"
        sig_start_bit = 139
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
        startbit = 139
        byte = 17
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChRiTarStsSwilPwrChRi23TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi23TarSts"
        sig_start_bit = 275
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
        startbit = 275
        byte = 34
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChRiTarStsSwilPwrChRi24TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi24TarSts"
        sig_start_bit = 273
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
        startbit = 273
        byte = 34
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADSSlaveTakerOverStsVmc:
        sig_name = "ADSSlaveTakerOverStsVmc"
        sig_start_bit = 21
        update_id_bit = 96
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TakerOverSts_NoReq': 0, 'TakerOverSts_No': 1, 'TakerOverSts_Yes': 2, 'TakerOverSts_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ADSSlaveCtrlStsChks:
        sig_name = "ADSSlaveCtrlStsChks"
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

    class PwrChLeTarStsContnsPwrChLe5TarSts:
        sig_name = "PwrChLeTarStsContnsPwrChLe5TarSts"
        sig_start_bit = 163
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
        startbit = 163
        byte = 20
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChRiTarStsSwilPwrChRi17TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi17TarSts"
        sig_start_bit = 257
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
        startbit = 257
        byte = 32
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADSSlaveCtrlStsSts:
        sig_name = "ADSSlaveCtrlStsSts"
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

    class PwrChLeTarStsContnsPwrChLe4TarSts:
        sig_name = "PwrChLeTarStsContnsPwrChLe4TarSts"
        sig_start_bit = 129
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
        startbit = 129
        byte = 16
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PwrChLeTarStsSwilPwrChLe15TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe15TarSts"
        sig_start_bit = 141
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
        startbit = 141
        byte = 17
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RtrctrReqFromRestrntSys:
        sig_name = "RtrctrReqFromRestrntSys"
        sig_start_bit = 19
        update_id_bit = 169
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RtrctrReq_Invalid': 0, 'RtrctrReq_NoActvn': 1, 'RtrctrReq_LowForce': 2, 'RtrctrReq_HighForce': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADSSlaveCtrlStsVmcQf:
        sig_name = "ADSSlaveCtrlStsVmcQf"
        sig_start_bit = 75
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
        startbit = 75
        byte = 9
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChRiTarStsSwilPwrChRi5TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi5TarSts"
        sig_start_bit = 303
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
        startbit = 303
        byte = 37
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChRiTarStsSwilPwrChRi10TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi10TarSts"
        sig_start_bit = 255
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
        startbit = 255
        byte = 31
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChRiTarStsSwilPwrChRi26TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi26TarSts"
        sig_start_bit = 285
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
        startbit = 285
        byte = 35
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VehSpd_UB:
        sig_name = "VehSpd_UB"
        sig_start_bit = 200
        update_id_bit = 200
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 200
        byte = 25
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChLeTarStsSwilPwrChLe3TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe3TarSts"
        sig_start_bit = 159
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
        startbit = 159
        byte = 19
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChRiTarStsContnsPwrChRi5TarSts:
        sig_name = "PwrChRiTarStsContnsPwrChRi5TarSts"
        sig_start_bit = 241
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
        startbit = 241
        byte = 30
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PwrChLeTarStsSwilPwrChLe7TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe7TarSts"
        sig_start_bit = 147
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
        startbit = 147
        byte = 18
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChRiTarStsSwilPwrChRi14TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi14TarSts"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChRiTarStsSwilPwrChRi28TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi28TarSts"
        sig_start_bit = 281
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
        startbit = 281
        byte = 35
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADSSlaveADModeReqVmc_UB:
        sig_name = "ADSSlaveADModeReqVmc_UB"
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

    class PwrChRiTarStsSwilPwrChRi6TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi6TarSts"
        sig_start_bit = 301
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
        startbit = 301
        byte = 37
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ADSSlaveCtrlStsVmc_UB:
        sig_name = "ADSSlaveCtrlStsVmc_UB"
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

    class ADSSlavePscmTemporaryoff:
        sig_name = "ADSSlavePscmTemporaryoff"
        sig_start_bit = 57
        update_id_bit = 70
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
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChLeTarStsContnsPwrChLe3TarSts:
        sig_name = "PwrChLeTarStsContnsPwrChLe3TarSts"
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

    class ADSSlaveADModeReqCntr:
        sig_name = "ADSSlaveADModeReqCntr"
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

    class PwrChRiTarStsSwilPwrChRi16TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi16TarSts"
        sig_start_bit = 259
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
        startbit = 259
        byte = 32
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChLeTarStsSwilPwrChLe25TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe25TarSts"
        sig_start_bit = 131
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
        startbit = 131
        byte = 16
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChRiTarStsSwilPwrChRi21TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi21TarSts"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehSpdSpd:
        sig_name = "VehSpdSpd"
        sig_start_bit = 223
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
        startbit = 223
        bmuws_info = [(27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111110, 0b00000001, 7, 1)]

    class ADSSlaveTakerOverSts:
        sig_name = "ADSSlaveTakerOverSts"
        sig_start_bit = 23
        update_id_bit = 97
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TakerOverSts_NoReq': 0, 'TakerOverSts_No': 1, 'TakerOverSts_Yes': 2, 'TakerOverSts_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChLeTarStsSwilPwrChLe1TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe1TarSts"
        sig_start_bit = 149
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
        startbit = 149
        byte = 18
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ADSSlaveCtrlSts_UB:
        sig_name = "ADSSlaveCtrlSts_UB"
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

    class PwrChLeTarStsSwilPwrChLe10TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe10TarSts"
        sig_start_bit = 105
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
        startbit = 105
        byte = 13
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SecBrkEpbReqChks:
        sig_name = "SecBrkEpbReqChks"
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

    class PwrChLeTarStsSwilPwrChLe23TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe23TarSts"
        sig_start_bit = 109
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
        startbit = 109
        byte = 13
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PwrChRiTarStsSwilPwrChRi25TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi25TarSts"
        sig_start_bit = 287
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
        startbit = 287
        byte = 35
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSSlaveCtrlStsQf:
        sig_name = "ADSSlaveCtrlStsQf"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehSpdQf:
        sig_name = "VehSpdQf"
        sig_start_bit = 235
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
        startbit = 235
        byte = 29
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChLeTarStsSwilPwrChLe8TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe8TarSts"
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
        sig_value_table = {'OffOnNoCmd_NoCmd': 0, 'OffOnNoCmd_Off': 1, 'OffOnNoCmd_On': 2}
        compute_method = None
        length = 2
        startbit = 153
        byte = 19
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADSSlaveADModeReqVmcAdActiveReq:
        sig_name = "ADSSlaveADModeReqVmcAdActiveReq"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehMovgDirVehMovgDir:
        sig_name = "VehMovgDirVehMovgDir"
        sig_start_bit = 203
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
        startbit = 203
        byte = 25
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class PwrChLeTarStsSwilPwrChLe14TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe14TarSts"
        sig_start_bit = 175
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
        startbit = 175
        byte = 21
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChRiTarStsSwilPwrChRi27TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi27TarSts"
        sig_start_bit = 283
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
        startbit = 283
        byte = 35
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADSSlaveCtrlStsVmcCtrlSts:
        sig_name = "ADSSlaveCtrlStsVmcCtrlSts"
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
        sig_value_table = {'ADMasterTakeOverRequest_NoRequest': 0, 'ADMasterTakeOverRequest_Master': 1, 'ADMasterTakeOverRequest_SlaveTakeOver': 2, 'ADMasterTakeOverRequest_SlaveBrakeStop': 3}
        compute_method = None
        length = 2
        startbit = 69
        byte = 8
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PwrChLeTarStsContnsPwrChLe1TarSts:
        sig_name = "PwrChLeTarStsContnsPwrChLe1TarSts"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChLeTarStsSwilPwrChLe12TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe12TarSts"
        sig_start_bit = 165
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
        startbit = 165
        byte = 20
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SecBrkEpbReq_UB:
        sig_name = "SecBrkEpbReq_UB"
        sig_start_bit = 168
        update_id_bit = 168
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ADSSlaveADModeReqChks:
        sig_name = "ADSSlaveADModeReqChks"
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

    class PwrChRiTarStsSwilPwrChRi11TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi11TarSts"
        sig_start_bit = 253
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
        startbit = 253
        byte = 31
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ADSSlaveCtrlStsVmcChks:
        sig_name = "ADSSlaveCtrlStsVmcChks"
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

    class PwrChLeTarSts_UB:
        sig_name = "PwrChLeTarSts_UB"
        sig_start_bit = 171
        update_id_bit = 171
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChRiTarStsSwilPwrChRi7TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi7TarSts"
        sig_start_bit = 299
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
        startbit = 299
        byte = 37
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChLeTarStsSwilPwrChLe29TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe29TarSts"
        sig_start_bit = 143
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
        startbit = 143
        byte = 17
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehSpdChks:
        sig_name = "VehSpdChks"
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

    class PwrChLeTarStsSwilPwrChLe4TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe4TarSts"
        sig_start_bit = 133
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
        startbit = 133
        byte = 16
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PwrChLeTarStsSwilPwrChLe16TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe16TarSts"
        sig_start_bit = 113
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
        startbit = 113
        byte = 14
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PwrChLeTarStsSwilPwrChLe11TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe11TarSts"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChLeTarStsSwilPwrChLe5TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe5TarSts"
        sig_start_bit = 155
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
        startbit = 155
        byte = 19
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VehMovgDirCntr:
        sig_name = "VehMovgDirCntr"
        sig_start_bit = 207
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
        startbit = 207
        byte = 25
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PwrChRiTarStsSwilPwrChRi9TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi9TarSts"
        sig_start_bit = 311
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
        startbit = 311
        byte = 38
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSSlaveADModeReqVmcChks:
        sig_name = "ADSSlaveADModeReqVmcChks"
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

    class PwrChRiTarStsContnsPwrChRi2TarSts:
        sig_name = "PwrChRiTarStsContnsPwrChRi2TarSts"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChRiTarStsContnsPwrChRi3TarSts:
        sig_name = "PwrChRiTarStsContnsPwrChRi3TarSts"
        sig_start_bit = 245
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
        startbit = 245
        byte = 30
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ADSSlaveCtrlStsCntr:
        sig_name = "ADSSlaveCtrlStsCntr"
        sig_start_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class ADSSlaveSteerOvrdnAllwd_UB:
        sig_name = "ADSSlaveSteerOvrdnAllwd_UB"
        sig_start_bit = 98
        update_id_bit = 98
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 98
        byte = 12
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChLeTarStsContnsPwrChLe2TarSts:
        sig_name = "PwrChLeTarStsContnsPwrChLe2TarSts"
        sig_start_bit = 167
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
        startbit = 167
        byte = 20
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSSlaveCtrlStsVmcCntr:
        sig_name = "ADSSlaveCtrlStsVmcCntr"
        sig_start_bit = 67
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
        startbit = 67
        byte = 8
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PwrChRiTarStsSwilPwrChRi8TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi8TarSts"
        sig_start_bit = 297
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
        startbit = 297
        byte = 37
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADSSlaveCtrlStsCtrlSts:
        sig_name = "ADSSlaveCtrlStsCtrlSts"
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
        sig_value_table = {'ADMasterTakeOverRequest_NoRequest': 0, 'ADMasterTakeOverRequest_Master': 1, 'ADMasterTakeOverRequest_SlaveTakeOver': 2, 'ADMasterTakeOverRequest_SlaveBrakeStop': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PwrChRiTarStsContnsPwrChRi4TarSts:
        sig_name = "PwrChRiTarStsContnsPwrChRi4TarSts"
        sig_start_bit = 243
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
        startbit = 243
        byte = 30
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PwrChLeTarStsSwilPwrChLe18TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe18TarSts"
        sig_start_bit = 161
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
        startbit = 161
        byte = 20
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PwrChLeTarStsSwilPwrChLe22TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe22TarSts"
        sig_start_bit = 157
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
        startbit = 157
        byte = 19
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PwrChLeTarStsSwilPwrChLe19TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe19TarSts"
        sig_start_bit = 145
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
        startbit = 145
        byte = 18
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehMovgDir_UB:
        sig_name = "VehMovgDir_UB"
        sig_start_bit = 184
        update_id_bit = 184
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 184
        byte = 23
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChRiTarStsSwilPwrChRi22TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi22TarSts"
        sig_start_bit = 277
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
        startbit = 277
        byte = 34
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PwrChLeTarStsSwilPwrChLe13TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe13TarSts"
        sig_start_bit = 119
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
        startbit = 119
        byte = 14
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSSlaveCtrlStsVmcAdMode:
        sig_name = "ADSSlaveCtrlStsVmcAdMode"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ADSSlaveADModeReq_UB:
        sig_name = "ADSSlaveADModeReq_UB"
        sig_start_bit = 17
        update_id_bit = 17
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ADSSlaveADModeReqAdActiveReq:
        sig_name = "ADSSlaveADModeReqAdActiveReq"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PwrChRiTarStsSwilPwrChRi19TarSts:
        sig_name = "PwrChRiTarStsSwilPwrChRi19TarSts"
        sig_start_bit = 269
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
        startbit = 269
        byte = 33
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PwrChLeTarStsSwilPwrChLe6TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe6TarSts"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSSlaveADModeReqVmcCntr:
        sig_name = "ADSSlaveADModeReqVmcCntr"
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

    class PwrChLeTarStsSwilPwrChLe24TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe24TarSts"
        sig_start_bit = 125
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
        startbit = 125
        byte = 15
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PwrChLeTarStsSwilPwrChLe27TarSts:
        sig_name = "PwrChLeTarStsSwilPwrChLe27TarSts"
        sig_start_bit = 115
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
        startbit = 115
        byte = 14
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADSSlaveSteerOvrdnAllwdChks:
        sig_name = "ADSSlaveSteerOvrdnAllwdChks"
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


class CCUMCUADPublicCANFDFr05:
    msg_name = "CCUMCUADPublicCANFDFr05"
    msg_id = 400
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['VCU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VehSpdLim:
        sig_name = "VehSpdLim"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 1
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


class LCURPublicCANFDFr06:
    msg_name = "LCURPublicCANFDFr06"
    msg_id = 408
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['CCUMCUAD', 'CCUMCUCD']
    sig_group_dict = {'ReRiDoorRdrObj8': ['ReRiDoorRdrObj8RdrObjDstX', 'ReRiDoorRdrObj8RdrObjDstY', 'ReRiDoorRdrObj8RdrObjDstZ', 'ReRiDoorRdrObj8RdrObjV'], 'ReRiDoorRdrObj3': ['ReRiDoorRdrObj3RdrObjDstX', 'ReRiDoorRdrObj3RdrObjDstY', 'ReRiDoorRdrObj3RdrObjDstZ', 'ReRiDoorRdrObj3RdrObjV'], 'ReRiDoorRdrObj2': ['ReRiDoorRdrObj2RdrObjDstX', 'ReRiDoorRdrObj2RdrObjDstY', 'ReRiDoorRdrObj2RdrObjDstZ', 'ReRiDoorRdrObj2RdrObjV'], 'RRDoorPosnSts': ['RRDoorPosnStsDoorAngPosn', 'RRDoorPosnStsDoorPercPosn'], 'ReRiDoorRdrObj6': ['ReRiDoorRdrObj6RdrObjDstX', 'ReRiDoorRdrObj6RdrObjDstY', 'ReRiDoorRdrObj6RdrObjDstZ', 'ReRiDoorRdrObj6RdrObjV'], 'ReRiDoorRdrObj1': ['ReRiDoorRdrObj1RdrObjDstX', 'ReRiDoorRdrObj1RdrObjDstY', 'ReRiDoorRdrObj1RdrObjDstZ', 'ReRiDoorRdrObj1RdrObjV'], 'ReRiDoorRdrObj7': ['ReRiDoorRdrObj7RdrObjDstX', 'ReRiDoorRdrObj7RdrObjDstY', 'ReRiDoorRdrObj7RdrObjDstZ', 'ReRiDoorRdrObj7RdrObjV'], 'ReRiDoorRdrObj4': ['ReRiDoorRdrObj4RdrObjDstX', 'ReRiDoorRdrObj4RdrObjDstY', 'ReRiDoorRdrObj4RdrObjDstZ', 'ReRiDoorRdrObj4RdrObjV'], 'RRDoorAntiPnchFb': ['RRDoorAntiPnchFbCloseAntiPnchSts', 'RRDoorAntiPnchFbOPenAntiPnchSts'], 'ReRiDoorRdrObj5': ['ReRiDoorRdrObj5RdrObjDstX', 'ReRiDoorRdrObj5RdrObjDstY', 'ReRiDoorRdrObj5RdrObjDstZ', 'ReRiDoorRdrObj5RdrObjV']}
    sig_group_dataid_dict = {}

    class ReRiDoorRdrObj7RdrObjV:
        sig_name = "ReRiDoorRdrObj7RdrObjV"
        sig_start_bit = 251
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
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11111111, 0b00000000, 8, 0)]

    class ReRiDoorRdrObj4RdrObjV:
        sig_name = "ReRiDoorRdrObj4RdrObjV"
        sig_start_bit = 143
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
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj8_UB:
        sig_name = "ReRiDoorRdrObj8_UB"
        sig_start_bit = 395
        update_id_bit = 395
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 395
        byte = 49
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RRDoorAntiPnchFbCloseAntiPnchSts:
        sig_name = "RRDoorAntiPnchFbCloseAntiPnchSts"
        sig_start_bit = 377
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
        startbit = 377
        byte = 47
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RRIceBreakMotSts:
        sig_name = "RRIceBreakMotSts"
        sig_start_bit = 338
        update_id_bit = 405
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotSts_Inactive': 0, 'MotSts_Active': 1, 'MotSts_ResetActive': 2}
        compute_method = None
        length = 3
        startbit = 338
        byte = 42
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class RRDoorPosnStsDoorAngPosn:
        sig_name = "RRDoorPosnStsDoorAngPosn"
        sig_start_bit = 375
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
        startbit = 375
        byte = 46
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReRiDoorRdrObj6RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj6RdrObjDstZ"
        sig_start_bit = 213
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
        startbit = 213
        bmuws_info = [(26, 0b00111111, 0b11000000, 6, 0), (27, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj5RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj5RdrObjDstZ"
        sig_start_bit = 175
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
        startbit = 175
        bmuws_info = [(21, 0b11111111, 0b00000000, 8, 0), (22, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj3RdrObjV:
        sig_name = "ReRiDoorRdrObj3RdrObjV"
        sig_start_bit = 111
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
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj6RdrObjDstX:
        sig_name = "ReRiDoorRdrObj6RdrObjDstX"
        sig_start_bit = 245
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
        startbit = 245
        bmuws_info = [(30, 0b00111111, 0b11000000, 6, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj3_UB:
        sig_name = "ReRiDoorRdrObj3_UB"
        sig_start_bit = 384
        update_id_bit = 384
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 384
        byte = 48
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReRiDoorRdrObj2_UB:
        sig_name = "ReRiDoorRdrObj2_UB"
        sig_start_bit = 385
        update_id_bit = 385
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 385
        byte = 48
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ReRiDoorRdrObj8RdrObjDstX:
        sig_name = "ReRiDoorRdrObj8RdrObjDstX"
        sig_start_bit = 317
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
        startbit = 317
        bmuws_info = [(39, 0b00111111, 0b11000000, 6, 0), (40, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj8RdrObjDstY:
        sig_name = "ReRiDoorRdrObj8RdrObjDstY"
        sig_start_bit = 311
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
        startbit = 311
        bmuws_info = [(38, 0b11111111, 0b00000000, 8, 0), (39, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj6RdrObjV:
        sig_name = "ReRiDoorRdrObj6RdrObjV"
        sig_start_bit = 219
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
        startbit = 219
        bmuws_info = [(27, 0b00001111, 0b11110000, 4, 0), (28, 0b11111111, 0b00000000, 8, 0)]

    class RRRelsMotSts:
        sig_name = "RRRelsMotSts"
        sig_start_bit = 391
        update_id_bit = 402
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotSts_Inactive': 0, 'MotSts_Active': 1, 'MotSts_ResetActive': 2}
        compute_method = None
        length = 3
        startbit = 391
        byte = 48
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ReRiDoorRdrObj5RdrObjDstX:
        sig_name = "ReRiDoorRdrObj5RdrObjDstX"
        sig_start_bit = 187
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
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj1RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj1RdrObjDstZ"
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

    class ReRiDoorRdrObj1RdrObjDstY:
        sig_name = "ReRiDoorRdrObj1RdrObjDstY"
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

    class ReRiDoorRdrObj3RdrObjDstX:
        sig_name = "ReRiDoorRdrObj3RdrObjDstX"
        sig_start_bit = 89
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
        startbit = 89
        bmuws_info = [(11, 0b00000011, 0b11111100, 2, 0), (12, 0b11111111, 0b00000000, 8, 0)]

    class RRDoorPosnSts_UB:
        sig_name = "RRDoorPosnSts_UB"
        sig_start_bit = 407
        update_id_bit = 407
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 407
        byte = 50
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReRiDoorRdrObj2RdrObjDstX:
        sig_name = "ReRiDoorRdrObj2RdrObjDstX"
        sig_start_bit = 51
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
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrMod:
        sig_name = "ReRiDoorRdrMod"
        sig_start_bit = 340
        update_id_bit = 387
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
        startbit = 340
        byte = 42
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class ReRiDoorRdrObj6_UB:
        sig_name = "ReRiDoorRdrObj6_UB"
        sig_start_bit = 397
        update_id_bit = 397
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 397
        byte = 49
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj2RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj2RdrObjDstZ"
        sig_start_bit = 77
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
        startbit = 77
        bmuws_info = [(9, 0b00111111, 0b11000000, 6, 0), (10, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj2RdrObjV:
        sig_name = "ReRiDoorRdrObj2RdrObjV"
        sig_start_bit = 57
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
        startbit = 57
        bmuws_info = [(7, 0b00000011, 0b11111100, 2, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj4RdrObjDstX:
        sig_name = "ReRiDoorRdrObj4RdrObjDstX"
        sig_start_bit = 147
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
        startbit = 147
        bmuws_info = [(18, 0b00001111, 0b11110000, 4, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj3RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj3RdrObjDstZ"
        sig_start_bit = 83
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
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11111100, 0b00000011, 6, 2)]

    class RRDoorMtnSts:
        sig_name = "RRDoorMtnSts"
        sig_start_bit = 383
        update_id_bit = 392
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
        startbit = 383
        byte = 47
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ReRiDoorRdrFlt:
        sig_name = "ReRiDoorRdrFlt"
        sig_start_bit = 343
        update_id_bit = 388
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
        startbit = 343
        byte = 42
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ReRiDoorRdrObj4RdrObjDstY:
        sig_name = "ReRiDoorRdrObj4RdrObjDstY"
        sig_start_bit = 153
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
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class ReRiDoorRdrObj8RdrObjV:
        sig_name = "ReRiDoorRdrObj8RdrObjV"
        sig_start_bit = 323
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
        startbit = 323
        bmuws_info = [(40, 0b00001111, 0b11110000, 4, 0), (41, 0b11111111, 0b00000000, 8, 0)]

    class ReRiDoorRdrObj2RdrObjDstY:
        sig_name = "ReRiDoorRdrObj2RdrObjDstY"
        sig_start_bit = 45
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
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj1_UB:
        sig_name = "ReRiDoorRdrObj1_UB"
        sig_start_bit = 386
        update_id_bit = 386
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 386
        byte = 48
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReRiDoorRdrObj7RdrObjDstX:
        sig_name = "ReRiDoorRdrObj7RdrObjDstX"
        sig_start_bit = 283
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
        startbit = 283
        bmuws_info = [(35, 0b00001111, 0b11110000, 4, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj8RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj8RdrObjDstZ"
        sig_start_bit = 289
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
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111111, 0b00000000, 8, 0)]

    class ReRiDoorRdrObj4RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj4RdrObjDstZ"
        sig_start_bit = 121
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
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class ReRiDoorRdrObj3RdrObjDstY:
        sig_name = "ReRiDoorRdrObj3RdrObjDstY"
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

    class ReRiDoorRdrObj5RdrObjV:
        sig_name = "ReRiDoorRdrObj5RdrObjV"
        sig_start_bit = 193
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
        startbit = 193
        bmuws_info = [(24, 0b00000011, 0b11111100, 2, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj6RdrObjDstY:
        sig_name = "ReRiDoorRdrObj6RdrObjDstY"
        sig_start_bit = 239
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
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj7_UB:
        sig_name = "ReRiDoorRdrObj7_UB"
        sig_start_bit = 396
        update_id_bit = 396
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 396
        byte = 49
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReRiDoorRdrObj4_UB:
        sig_name = "ReRiDoorRdrObj4_UB"
        sig_start_bit = 399
        update_id_bit = 399
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 399
        byte = 49
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RRLtchRelsSts:
        sig_name = "RRLtchRelsSts"
        sig_start_bit = 368
        update_id_bit = 404
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
        startbit = 368
        byte = 46
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReRiDoorRdrObj5RdrObjDstY:
        sig_name = "ReRiDoorRdrObj5RdrObjDstY"
        sig_start_bit = 181
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
        startbit = 181
        bmuws_info = [(22, 0b00111111, 0b11000000, 6, 0), (23, 0b11110000, 0b00001111, 4, 4)]

    class RRDoorPosnStsDoorPercPosn:
        sig_name = "RRDoorPosnStsDoorPercPosn"
        sig_start_bit = 367
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
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RRDoorSpd:
        sig_name = "RRDoorSpd"
        sig_start_bit = 351
        update_id_bit = 406
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
        startbit = 351
        byte = 43
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

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

    class RRDoorLockStsResd:
        sig_name = "RRDoorLockStsResd"
        sig_start_bit = 379
        update_id_bit = 393
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
        startbit = 379
        byte = 47
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class RRDoorAntiPnchFbOPenAntiPnchSts:
        sig_name = "RRDoorAntiPnchFbOPenAntiPnchSts"
        sig_start_bit = 376
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
        startbit = 376
        byte = 47
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReRiDoorRdrObj1RdrObjDstX:
        sig_name = "ReRiDoorRdrObj1RdrObjDstX"
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

    class ReRiDoorRdrObj7RdrObjDstY:
        sig_name = "ReRiDoorRdrObj7RdrObjDstY"
        sig_start_bit = 271
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
        startbit = 271
        bmuws_info = [(33, 0b11111111, 0b00000000, 8, 0), (34, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj7RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj7RdrObjDstZ"
        sig_start_bit = 277
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
        startbit = 277
        bmuws_info = [(34, 0b00111111, 0b11000000, 6, 0), (35, 0b11110000, 0b00001111, 4, 4)]

    class RRDoorAntiPnchFb_UB:
        sig_name = "RRDoorAntiPnchFb_UB"
        sig_start_bit = 394
        update_id_bit = 394
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 394
        byte = 49
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReRiDoorRdrObj5_UB:
        sig_name = "ReRiDoorRdrObj5_UB"
        sig_start_bit = 398
        update_id_bit = 398
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 398
        byte = 49
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class CCUMCUCDPublicCANFDFr10:
    msg_name = "CCUMCUCDPublicCANFDFr10"
    msg_id = 305
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['LCUR', 'LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HAZBrkLiReq:
        sig_name = "HAZBrkLiReq"
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
        sig_value_table = {'HazBrkLight_NotInprogress': 0, 'HazBrkLight_InProgress': 1, 'HazBrkLight_InProgressSpdLow': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CCUMCUCDPublicCANFDFr05:
    msg_name = "CCUMCUCDPublicCANFDFr05"
    msg_id = 528
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {'ANPStatusCCU1': ['ANPStatusCCU1ANPFuncStatus', 'ANPStatusCCU1Chks', 'ANPStatusCCU1Cntr', 'ANPStatusCCU1Qf'], 'ADSSlavePrkingReq': ['ADSSlavePrkingReqChks', 'ADSSlavePrkingReqCntr', 'ADSSlavePrkingReqReq']}
    sig_group_dataid_dict = {}

    class ANPStatusCCU1Chks:
        sig_name = "ANPStatusCCU1Chks"
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

    class ANPStatusCCU1_UB:
        sig_name = "ANPStatusCCU1_UB"
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

    class ADSSlaveStandStillReq:
        sig_name = "ADSSlaveStandStillReq"
        sig_start_bit = 6
        update_id_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehStopReq1_NoReqOnVehStop': 0, 'VehStopReq1_ReqOnVehStopSoftToStandStill': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ADSSlavePrkingReqReq:
        sig_name = "ADSSlavePrkingReqReq"
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
        sig_value_table = {'PrkgBrkElectcCtrlReq_NoRequest': 0, 'PrkgBrkElectcCtrlReq_ReleaseRequest': 1, 'PrkgBrkElectcCtrlReq_ApplyRequest': 2, 'PrkgBrkElectcCtrlReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ANPStatusCCU1Qf:
        sig_name = "ANPStatusCCU1Qf"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSSlavePrkingReqCntr:
        sig_name = "ADSSlavePrkingReqCntr"
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

    class ANPStatusCCU1Cntr:
        sig_name = "ANPStatusCCU1Cntr"
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

    class ADSSlavePrkingReqChks:
        sig_name = "ADSSlavePrkingReqChks"
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

    class ADSSlaveDriveOffReq:
        sig_name = "ADSSlaveDriveOffReq"
        sig_start_bit = 7
        update_id_bit = 23
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehStopReq1_NoReqOnVehStop': 0, 'VehStopReq1_ReqOnVehStopSoftToStandStill': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ADSSlavePrkingReq_UB:
        sig_name = "ADSSlavePrkingReq_UB"
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

    class ANPStatusCCU1ANPFuncStatus:
        sig_name = "ANPStatusCCU1ANPFuncStatus"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 20
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ANPFuncStatus_Passive': 0, 'ANPFuncStatus_MPStandby': 1, 'ANPFuncStatus_MDStandby': 2, 'ANPFuncStatus_MPNormal': 3, 'ANPFuncStatus_MDNormal': 4, 'ANPFuncStatus_ACCNormal': 5, 'ANPFuncStatus_MPOverride': 6, 'ANPFuncStatus_MDOverride': 7, 'ANPFuncStatus_MPTakeover': 8, 'ANPFuncStatus_MDTakeover': 9, 'ANPFuncStatus_MPSafeStop': 10, 'ANPFuncStatus_MDSafeStop': 11, 'ANPFuncStatus_Fault': 12, 'ANPFuncStatus_MPTempPassive': 13, 'ANPFuncStatus_MDTempPassive': 14, 'ANPFuncStatus_ACCTakeOver': 15, 'ANPFuncStatus_ACCSafeStop': 16, 'ANPFuncStatus_BACUSafeStop': 17, 'ANPFuncStatus_Reserved1': 18, 'ANPFuncStatus_Reserved2': 19, 'ANPFuncStatus_Reserved3': 20}
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCULPublicCANFDFr08:
    msg_name = "LCULPublicCANFDFr08"
    msg_id = 661
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['CCUMCUCD', 'ETC']
    sig_group_dict = {'FLLtchErrFb': ['FLLtchErrFbCinchErrFb', 'FLLtchErrFbCinchMotThermErrFb', 'FLLtchErrFbHalfClsErrFb', 'FLLtchErrFbRelsgErrFb', 'FLLtchErrFbRelsMotThermErrFb'], 'HudSnsrErr': ['HudSnsrErrParChk', 'HudSnsrErrSnsrErr'], 'AmbIllmnFwdSts': ['AmbIllmnFwdStsAmbIllmn1', 'AmbIllmnFwdStsAmbIllmn2', 'AmbIllmnFwdStsChks', 'AmbIllmnFwdStsCntr'], 'RLLtchErrFb': ['RLLtchErrFbCinchErrFb', 'RLLtchErrFbCinchMotThermErrFb', 'RLLtchErrFbHalfClsErrFb', 'RLLtchErrFbRelsgErrFb', 'RLLtchErrFbRelsMotThermErrFb'], 'ChargeLidErrSts': ['ChargeLidErrStsElecErr', 'ChargeLidErrStsHallErr', 'ChargeLidErrStsTempErr', 'ChargeLidErrStsVoltErr']}
    sig_group_dataid_dict = {}

    class FLLtchErrFbHalfClsErrFb:
        sig_name = "FLLtchErrFbHalfClsErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FLLtchErrFb_UB:
        sig_name = "FLLtchErrFb_UB"
        sig_start_bit = 85
        update_id_bit = 85
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 85
        byte = 10
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HudSnsrErrParChk:
        sig_name = "HudSnsrErrParChk"
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
        sig_value_table = {'ParChk_Unevennrof': 0, 'ParChk_Evennrof': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HudSnsrErr_UB:
        sig_name = "HudSnsrErr_UB"
        sig_start_bit = 95
        update_id_bit = 95
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 95
        byte = 11
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RLLtchErrFbRelsMotThermErrFb:
        sig_name = "RLLtchErrFbRelsMotThermErrFb"
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

    class AmbIllmnFwdSts_UB:
        sig_name = "AmbIllmnFwdSts_UB"
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

    class HudSnsrErrSnsrErr:
        sig_name = "HudSnsrErrSnsrErr"
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
        sig_value_table = {'SnsrErr_FltStsTestPassd1': 0, 'SnsrErr_FltStsTestFaild2': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RLLtchErrFb_UB:
        sig_name = "RLLtchErrFb_UB"
        sig_start_bit = 80
        update_id_bit = 80
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 80
        byte = 10
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RLLtchErrFbCinchErrFb:
        sig_name = "RLLtchErrFbCinchErrFb"
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

    class SolarSnsrRiValue:
        sig_name = "SolarSnsrRiValue"
        sig_start_bit = 79
        update_id_bit = 92
        sig_length = 8
        sig_value_factor = 5
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

    class CmptFrntWindT:
        sig_name = "CmptFrntWindT"
        sig_start_bit = 39
        update_id_bit = 25
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 650
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11100000, 0b00011111, 3, 5)]

    class SolarSnsrLeValue:
        sig_name = "SolarSnsrLeValue"
        sig_start_bit = 71
        update_id_bit = 93
        sig_length = 8
        sig_value_factor = 5
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

    class CooltLvlRaw:
        sig_name = "CooltLvlRaw"
        sig_start_bit = 3
        update_id_bit = 24
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

    class CmptFrntWindDewT:
        sig_name = "CmptFrntWindDewT"
        sig_start_bit = 23
        update_id_bit = 26
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11100000, 0b00011111, 3, 5)]

    class RLLtchErrFbHalfClsErrFb:
        sig_name = "RLLtchErrFbHalfClsErrFb"
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

    class RelHumSnsrErr:
        sig_name = "RelHumSnsrErr"
        sig_start_bit = 86
        update_id_bit = 84
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 86
        byte = 10
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ChargeLidErrStsElecErr:
        sig_name = "ChargeLidErrStsElecErr"
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

    class ChargeLidErrStsHallErr:
        sig_name = "ChargeLidErrStsHallErr"
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

    class AmbIllmnFwdStsAmbIllmn2:
        sig_name = "AmbIllmnFwdStsAmbIllmn2"
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

    class FLLtchErrFbCinchMotThermErrFb:
        sig_name = "FLLtchErrFbCinchMotThermErrFb"
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

    class SolarSnsrErr:
        sig_name = "SolarSnsrErr"
        sig_start_bit = 87
        update_id_bit = 94
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 87
        byte = 10
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AmbIllmnFwdStsCntr:
        sig_name = "AmbIllmnFwdStsCntr"
        sig_start_bit = 91
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
        startbit = 91
        byte = 11
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RLLtchErrFbRelsgErrFb:
        sig_name = "RLLtchErrFbRelsgErrFb"
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

    class FLLtchErrFbRelsgErrFb:
        sig_name = "FLLtchErrFbRelsgErrFb"
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

    class FLLtchErrFbRelsMotThermErrFb:
        sig_name = "FLLtchErrFbRelsMotThermErrFb"
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

    class AmbIllmnFwdStsAmbIllmn1:
        sig_name = "AmbIllmnFwdStsAmbIllmn1"
        sig_start_bit = 119
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
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b10000000, 0b01111111, 1, 7)]

    class AmbIllmnFwdStsChks:
        sig_name = "AmbIllmnFwdStsChks"
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

    class RLLtchErrFbCinchMotThermErrFb:
        sig_name = "RLLtchErrFbCinchMotThermErrFb"
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

    class ChargeLidErrStsVoltErr:
        sig_name = "ChargeLidErrStsVoltErr"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RelHumSnsrRelHum:
        sig_name = "RelHumSnsrRelHum"
        sig_start_bit = 55
        update_id_bit = 83
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 200
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

    class ChargeLidErrSts_UB:
        sig_name = "ChargeLidErrSts_UB"
        sig_start_bit = 8
        update_id_bit = 8
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ChargeLidErrStsTempErr:
        sig_name = "ChargeLidErrStsTempErr"
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

    class FLLtchErrFbCinchErrFb:
        sig_name = "FLLtchErrFbCinchErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class CCUMCUADPublicCANFDFr03:
    msg_name = "CCUMCUADPublicCANFDFr03"
    msg_id = 145
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "CCUMCUAD"
    rx_nodes = ['VCU', 'CCUMCUCD', 'ETC']
    sig_group_dict = {'VmcGearShifReq': ['VmcGearShifReqChks', 'VmcGearShifReqCntr', 'VmcGearShifReqGearPrkgAssiReq1'], 'ADSMasterADModeReq': ['ADSMasterADModeReqAdActiveReq', 'ADSMasterADModeReqChks', 'ADSMasterADModeReqCntr'], 'GearAutoShiftReq': ['GearAutoShiftReqChks', 'GearAutoShiftReqCntr', 'GearAutoShiftReqGearAutoShiftReq'], 'GearAutoShiftReqSts': ['GearAutoShiftReqStsChks', 'GearAutoShiftReqStsCntr', 'GearAutoShiftReqStsSafe'], 'AdfPropCtrlReq': ['AdfPropCtrlReqChks', 'AdfPropCtrlReqCntr', 'AdfPropCtrlReqCtrlSts', 'AdfPropCtrlReqMode'], 'VmcAccrOvrdnAllwd': ['VmcAccrOvrdnAllwdChks', 'VmcAccrOvrdnAllwdCntr', 'VmcAccrOvrdnAllwdYesNo1'], 'VmcHoldType': ['VmcHoldTypeChks', 'VmcHoldTypeCntr', 'VmcHoldTypeStandstilMgrSts'], 'AdfPrimSysReq': ['AdfPrimSysReqActvReq', 'AdfPrimSysReqChks', 'AdfPrimSysReqCntr', 'AdfPrimSysReqDeActvReq'], 'AdfCtrlSts': ['AdfCtrlStsChks', 'AdfCtrlStsCntr', 'AdfCtrlStsColorSts', 'AdfCtrlStsCtrlSts', 'AdfCtrlStsDegraded', 'AdfCtrlStsMode'], 'VmcPropTqTotReq': ['VmcPropTqTotReqChks', 'VmcPropTqTotReqCntr', 'VmcPropTqTotReqGrdtNeg', 'VmcPropTqTotReqGrdtPos', 'VmcPropTqTotReqReq'], 'AdfPropReq': ['AdfPropReqActvReq', 'AdfPropReqChks', 'AdfPropReqCntr', 'AdfPropReqDeActvReq'], 'ADSMstCtrlSts': ['ADSMstCtrlStsAdMode', 'ADSMstCtrlStsChks', 'ADSMstCtrlStsCntr', 'ADSMstCtrlStsCtrlSts', 'ADSMstCtrlStsQf', 'ADSMstCtrlStsSts'], 'AdfPrimCtrlCts': ['AdfPrimCtrlCtsChks', 'AdfPrimCtrlCtsCntr', 'AdfPrimCtrlCtsCtrlSts', 'AdfPrimCtrlCtsMode']}
    sig_group_dataid_dict = {'GearAutoShiftReq': 1002, 'GearAutoShiftReqSts': 1003}

    class VmcGearShifReq_UB:
        sig_name = "VmcGearShifReq_UB"
        sig_start_bit = 197
        update_id_bit = 197
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 197
        byte = 24
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VmcPropTqTotReqChks:
        sig_name = "VmcPropTqTotReqChks"
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

    class AdfCtrlStsDegraded:
        sig_name = "AdfCtrlStsDegraded"
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

    class VmcPropTqTotReqCntr:
        sig_name = "VmcPropTqTotReqCntr"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AdfCtrlStsChks:
        sig_name = "AdfCtrlStsChks"
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

    class GearAutoShiftReqStsChks:
        sig_name = "GearAutoShiftReqStsChks"
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

    class ADSMasterADModeReq_UB:
        sig_name = "ADSMasterADModeReq_UB"
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

    class ADSMasterADModeReqAdActiveReq:
        sig_name = "ADSMasterADModeReqAdActiveReq"
        sig_start_bit = 111
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 111
        byte = 13
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AdfPrimCtrlCtsCntr:
        sig_name = "AdfPrimCtrlCtsCntr"
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

    class AdfPropReqChks:
        sig_name = "AdfPropReqChks"
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

    class AdfPrimSysReqChks:
        sig_name = "AdfPrimSysReqChks"
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

    class VmcAccrOvrdnAllwdCntr:
        sig_name = "VmcAccrOvrdnAllwdCntr"
        sig_start_bit = 139
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
        startbit = 139
        byte = 17
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class GearAutoShiftReq_UB:
        sig_name = "GearAutoShiftReq_UB"
        sig_start_bit = 212
        update_id_bit = 212
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 212
        byte = 26
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ADSMstCtrlStsCtrlSts:
        sig_name = "ADSMstCtrlStsCtrlSts"
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
        sig_value_table = {'ADMasterTakeOverRequest_NoRequest': 0, 'ADMasterTakeOverRequest_Master': 1, 'ADMasterTakeOverRequest_SlaveTakeOver': 2, 'ADMasterTakeOverRequest_SlaveBrakeStop': 3}
        compute_method = None
        length = 2
        startbit = 133
        byte = 16
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AdfPropCtrlReqCtrlSts:
        sig_name = "AdfPropCtrlReqCtrlSts"
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
        sig_value_table = {'CtrlSts_Primary': 0, 'CtrlSts_Secondary': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VmcGearShifReqGearPrkgAssiReq1:
        sig_name = "VmcGearShifReqGearPrkgAssiReq1"
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
        sig_value_table = {'GearPrkgAssiReq1_NoRequest': 0, 'GearPrkgAssiReq1_TargetgearP': 1, 'GearPrkgAssiReq1_TargetgearR': 2, 'GearPrkgAssiReq1_TargetgearD': 3}
        compute_method = None
        length = 2
        startbit = 163
        byte = 20
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class GearAutoShiftReqSts_UB:
        sig_name = "GearAutoShiftReqSts_UB"
        sig_start_bit = 228
        update_id_bit = 228
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 228
        byte = 28
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class GearAutoShiftReqCntr:
        sig_name = "GearAutoShiftReqCntr"
        sig_start_bit = 211
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
        startbit = 211
        byte = 26
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AdfPrimCtrlCtsMode:
        sig_name = "AdfPrimCtrlCtsMode"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AdfPropCtrlReq_UB:
        sig_name = "AdfPropCtrlReq_UB"
        sig_start_bit = 89
        update_id_bit = 89
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 89
        byte = 11
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VmcHoldTypeCntr:
        sig_name = "VmcHoldTypeCntr"
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

    class VmcPropTqTotReqGrdtPos:
        sig_name = "VmcPropTqTotReqGrdtPos"
        sig_start_bit = 262
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8192
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 262
        bmuws_info = [(32, 0b01111111, 0b10000000, 7, 0), (33, 0b11111100, 0b00000011, 6, 2)]

    class VmcGearShifReqChks:
        sig_name = "VmcGearShifReqChks"
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

    class GearAutoShiftReqChks:
        sig_name = "GearAutoShiftReqChks"
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

    class AdfPropReqDeActvReq:
        sig_name = "AdfPropReqDeActvReq"
        sig_start_bit = 91
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
        startbit = 91
        byte = 11
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VmcPropTqTotReqGrdtNeg:
        sig_name = "VmcPropTqTotReqGrdtNeg"
        sig_start_bit = 243
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8192
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 243
        bmuws_info = [(30, 0b00001111, 0b11110000, 4, 0), (31, 0b11111111, 0b00000000, 8, 0), (32, 0b10000000, 0b01111111, 1, 7)]

    class VmcAccrOvrdnAllwd_UB:
        sig_name = "VmcAccrOvrdnAllwd_UB"
        sig_start_bit = 198
        update_id_bit = 198
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 198
        byte = 24
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AdfPrimSysReqActvReq:
        sig_name = "AdfPrimSysReqActvReq"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AdfPropCtrlReqCntr:
        sig_name = "AdfPropCtrlReqCntr"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VmcHoldType_UB:
        sig_name = "VmcHoldType_UB"
        sig_start_bit = 196
        update_id_bit = 196
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 196
        byte = 24
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AdfPropCtrlReqMode:
        sig_name = "AdfPropCtrlReqMode"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AdfPrimSysReqCntr:
        sig_name = "AdfPrimSysReqCntr"
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

    class AdfCtrlStsCntr:
        sig_name = "AdfCtrlStsCntr"
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

    class VmcHoldTypeChks:
        sig_name = "VmcHoldTypeChks"
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

    class AdfPrimCtrlCtsCtrlSts:
        sig_name = "AdfPrimCtrlCtsCtrlSts"
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
        sig_value_table = {'CtrlSts_Primary': 0, 'CtrlSts_Secondary': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VmcPropTqTotReqReq:
        sig_name = "VmcPropTqTotReqReq"
        sig_start_bit = 279
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 279
        bmuws_info = [(34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0)]

    class GearAutoShiftReqStsSafe:
        sig_name = "GearAutoShiftReqStsSafe"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearAutoShiftReqSts_NoAction': 0, 'GearAutoShiftReqSts_GearReqEnable': 1, 'GearAutoShiftReqSts_GearReqComplete': 2, 'GearAutoShiftReqSts_GearReqInhibit': 3}
        compute_method = None
        length = 2
        startbit = 231
        byte = 28
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSMstCtrlStsChks:
        sig_name = "ADSMstCtrlStsChks"
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

    class VmcAccrOvrdnAllwdYesNo1:
        sig_name = "VmcAccrOvrdnAllwdYesNo1"
        sig_start_bit = 140
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
        startbit = 140
        byte = 17
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VmcPropTqTotReqEna:
        sig_name = "VmcPropTqTotReqEna"
        sig_start_bit = 295
        update_id_bit = 294
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 295
        byte = 36
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AdfPrimSysReq_UB:
        sig_name = "AdfPrimSysReq_UB"
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

    class VmcAccrOvrdnAllwdChks:
        sig_name = "VmcAccrOvrdnAllwdChks"
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

    class ADSMstCtrlStsAdMode:
        sig_name = "ADSMstCtrlStsAdMode"
        sig_start_bit = 123
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 123
        byte = 15
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ADSMstPscmTemporaryoff:
        sig_name = "ADSMstPscmTemporaryoff"
        sig_start_bit = 129
        update_id_bit = 160
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
        startbit = 129
        byte = 16
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AdfPrimCtrlCtsChks:
        sig_name = "AdfPrimCtrlCtsChks"
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

    class AdfCtrlSts_UB:
        sig_name = "AdfCtrlSts_UB"
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

    class VmcPropTqTotReq_UB:
        sig_name = "VmcPropTqTotReq_UB"
        sig_start_bit = 264
        update_id_bit = 264
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 264
        byte = 33
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AdfPropReq_UB:
        sig_name = "AdfPropReq_UB"
        sig_start_bit = 88
        update_id_bit = 88
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 88
        byte = 11
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ADSMasterADModeReqChks:
        sig_name = "ADSMasterADModeReqChks"
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

    class VmcGearShifReqCntr:
        sig_name = "VmcGearShifReqCntr"
        sig_start_bit = 167
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
        startbit = 167
        byte = 20
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AdfPrimSysReqDeActvReq:
        sig_name = "AdfPrimSysReqDeActvReq"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AdfCtrlStsMode:
        sig_name = "AdfCtrlStsMode"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VmcMonrSts:
        sig_name = "VmcMonrSts"
        sig_start_bit = 191
        update_id_bit = 195
        sig_length = 8
        sig_value_factor = None
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

    class ADSMstCtrlStsSts:
        sig_name = "ADSMstCtrlStsSts"
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
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 131
        byte = 16
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EpbRollerActv:
        sig_name = "EpbRollerActv"
        sig_start_bit = 128
        update_id_bit = 199
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
        startbit = 128
        byte = 16
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class GearAutoShiftReqStsCntr:
        sig_name = "GearAutoShiftReqStsCntr"
        sig_start_bit = 227
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
        startbit = 227
        byte = 28
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class GearAutoShiftReqGearAutoShiftReq:
        sig_name = "GearAutoShiftReqGearAutoShiftReq"
        sig_start_bit = 215
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
        startbit = 215
        byte = 26
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class AdfCtrlStsColorSts:
        sig_name = "AdfCtrlStsColorSts"
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
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADSMstCtrlStsCntr:
        sig_name = "ADSMstCtrlStsCntr"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ADSMstCtrlStsQf:
        sig_name = "ADSMstCtrlStsQf"
        sig_start_bit = 135
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
        startbit = 135
        byte = 16
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VmcHoldTypeStandstilMgrSts:
        sig_name = "VmcHoldTypeStandstilMgrSts"
        sig_start_bit = 179
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StandstilMgrSts_Val0': 0, 'StandstilMgrSts_Val1': 1, 'StandstilMgrSts_Val2': 2, 'StandstilMgrSts_Val3': 3, 'StandstilMgrSts_Val4': 4, 'StandstilMgrSts_Val5': 5, 'StandstilMgrSts_Val6': 6, 'StandstilMgrSts_Val7': 7}
        compute_method = None
        length = 3
        startbit = 179
        byte = 22
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class ADSMstTakeOverReq:
        sig_name = "ADSMstTakeOverReq"
        sig_start_bit = 143
        update_id_bit = 176
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ADMasterTakeOverRequest_NoRequest': 0, 'ADMasterTakeOverRequest_Master': 1, 'ADMasterTakeOverRequest_SlaveTakeOver': 2, 'ADMasterTakeOverRequest_SlaveBrakeStop': 3}
        compute_method = None
        length = 2
        startbit = 143
        byte = 17
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class AdfPropCtrlReqChks:
        sig_name = "AdfPropCtrlReqChks"
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

    class AdfPropReqCntr:
        sig_name = "AdfPropReqCntr"
        sig_start_bit = 75
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
        startbit = 75
        byte = 9
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AdfPropReqActvReq:
        sig_name = "AdfPropReqActvReq"
        sig_start_bit = 95
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 95
        byte = 11
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ADSMstCtrlSts_UB:
        sig_name = "ADSMstCtrlSts_UB"
        sig_start_bit = 161
        update_id_bit = 161
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 161
        byte = 20
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ADSMasterADModeReqCntr:
        sig_name = "ADSMasterADModeReqCntr"
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

    class AdfCtrlStsCtrlSts:
        sig_name = "AdfCtrlStsCtrlSts"
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
        sig_value_table = {'CtrlSts_Primary': 0, 'CtrlSts_Secondary': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AdfPrimCtrlCts_UB:
        sig_name = "AdfPrimCtrlCts_UB"
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


class VCUPublicCANFDFr04:
    msg_name = "VCUPublicCANFDFr04"
    msg_id = 258
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 16
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD', 'ETC']
    sig_group_dict = {'HVSysLimnIndcnDTCInfo': ['HVSysLimnIndcnDTCInfoBattDTCInfo1', 'HVSysLimnIndcnDTCInfoBattDTCInfo2', 'HVSysLimnIndcnDTCInfoChrgnAndCnvnDTCInfo1', 'HVSysLimnIndcnDTCInfoMotDTCInfo1', 'HVSysLimnIndcnDTCInfoPrpsnDTCInfo1', 'HVSysLimnIndcnDTCInfoPrpsnDTCInfo2']}
    sig_group_dataid_dict = {}

    class HVSysLimnIndcnDTCInfoBattDTCInfo1:
        sig_name = "HVSysLimnIndcnDTCInfoBattDTCInfo1"
        sig_start_bit = 47
        update_id_bit = None
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
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11000000, 0b00111111, 2, 6)]

    class PrpsnSysLimnIndcnFb:
        sig_name = "PrpsnSysLimnIndcnFb"
        sig_start_bit = 71
        update_id_bit = 58
        sig_length = 8
        sig_value_factor = None
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

    class HVSysLimnIndcnDTCInfoPrpsnDTCInfo1:
        sig_name = "HVSysLimnIndcnDTCInfoPrpsnDTCInfo1"
        sig_start_bit = 19
        update_id_bit = None
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
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class HVSysLimnIndcnDTCInfoBattDTCInfo2:
        sig_name = "HVSysLimnIndcnDTCInfoBattDTCInfo2"
        sig_start_bit = 7
        update_id_bit = None
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

    class HVSysLimnIndcnDTCInfoPrpsnDTCInfo2:
        sig_name = "HVSysLimnIndcnDTCInfoPrpsnDTCInfo2"
        sig_start_bit = 13
        update_id_bit = None
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
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class HVSysLimnIndcnDTCInfo_UB:
        sig_name = "HVSysLimnIndcnDTCInfo_UB"
        sig_start_bit = 59
        update_id_bit = 59
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HVSysLimnIndcnDTCInfoChrgnAndCnvnDTCInfo1:
        sig_name = "HVSysLimnIndcnDTCInfoChrgnAndCnvnDTCInfo1"
        sig_start_bit = 25
        update_id_bit = None
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
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class HVSysLimnIndcnDTCInfoMotDTCInfo1:
        sig_name = "HVSysLimnIndcnDTCInfoMotDTCInfo1"
        sig_start_bit = 53
        update_id_bit = None
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
        startbit = 53
        bmuws_info = [(6, 0b00111111, 0b11000000, 6, 0), (7, 0b11110000, 0b00001111, 4, 4)]


class CCUMCUCDPublicCANFDFr08:
    msg_name = "CCUMCUCDPublicCANFDFr08"
    msg_id = 659
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['LCUL', 'CCUMCUAD', 'LCUR', 'VCU']
    sig_group_dict = {'Vin': ['VinInfoBytePosn1', 'VinInfoBytePosn10', 'VinInfoBytePosn11', 'VinInfoBytePosn12', 'VinInfoBytePosn13', 'VinInfoBytePosn14', 'VinInfoBytePosn15', 'VinInfoBytePosn16', 'VinInfoBytePosn17', 'VinInfoBytePosn2', 'VinInfoBytePosn3', 'VinInfoBytePosn4', 'VinInfoBytePosn5', 'VinInfoBytePosn6', 'VinInfoBytePosn7', 'VinInfoBytePosn8', 'VinInfoBytePosn9'], 'NodeListInfo': ['NodeListInfo1', 'NodeListInfo2', 'NodeListInfo3', 'NodeListInfo4', 'NodeListInfo5', 'NodeListInfo6', 'NodeListInfo7', 'NodeListInfo8']}
    sig_group_dataid_dict = {}

    class Vin_UB:
        sig_name = "Vin_UB"
        sig_start_bit = 398
        update_id_bit = 398
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 398
        byte = 49
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class NodeListInfo5:
        sig_name = "NodeListInfo5"
        sig_start_bit = 231
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
        startbit = 231
        bmuws_info = [(28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11111111, 0b00000000, 8, 0)]

    class VinInfoBytePosn9:
        sig_name = "VinInfoBytePosn9"
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

    class NodeListInfo1:
        sig_name = "NodeListInfo1"
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

    class NodeListInfo_UB:
        sig_name = "NodeListInfo_UB"
        sig_start_bit = 399
        update_id_bit = 399
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 399
        byte = 49
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VinInfoBytePosn1:
        sig_name = "VinInfoBytePosn1"
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

    class NodeListInfo2:
        sig_name = "NodeListInfo2"
        sig_start_bit = 167
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
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b11111111, 0b00000000, 8, 0)]

    class VinInfoBytePosn2:
        sig_name = "VinInfoBytePosn2"
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

    class VinInfoBytePosn8:
        sig_name = "VinInfoBytePosn8"
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

    class VinInfoBytePosn5:
        sig_name = "VinInfoBytePosn5"
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

    class VinInfoBytePosn15:
        sig_name = "VinInfoBytePosn15"
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

    class NodeListInfo7:
        sig_name = "NodeListInfo7"
        sig_start_bit = 71
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
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111111, 0b00000000, 8, 0)]

    class NodeListInfo4:
        sig_name = "NodeListInfo4"
        sig_start_bit = 103
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
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0), (14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0)]

    class VinInfoBytePosn7:
        sig_name = "VinInfoBytePosn7"
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

    class VinInfoBytePosn17:
        sig_name = "VinInfoBytePosn17"
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

    class VinInfoBytePosn3:
        sig_name = "VinInfoBytePosn3"
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

    class VinInfoBytePosn4:
        sig_name = "VinInfoBytePosn4"
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

    class NodeListInfo6:
        sig_name = "NodeListInfo6"
        sig_start_bit = 135
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
        startbit = 135
        bmuws_info = [(16, 0b11111111, 0b00000000, 8, 0), (17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0)]

    class VinInfoBytePosn16:
        sig_name = "VinInfoBytePosn16"
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

    class VinInfoBytePosn13:
        sig_name = "VinInfoBytePosn13"
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

    class VinInfoBytePosn14:
        sig_name = "VinInfoBytePosn14"
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

    class VinInfoBytePosn11:
        sig_name = "VinInfoBytePosn11"
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

    class VinInfoBytePosn12:
        sig_name = "VinInfoBytePosn12"
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

    class NodeListInfo8:
        sig_name = "NodeListInfo8"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class VinInfoBytePosn10:
        sig_name = "VinInfoBytePosn10"
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

    class VinInfoBytePosn6:
        sig_name = "VinInfoBytePosn6"
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

    class NodeListInfo3:
        sig_name = "NodeListInfo3"
        sig_start_bit = 199
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
        startbit = 199
        bmuws_info = [(24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0)]


class LCURPublicCANFDFr03:
    msg_name = "LCURPublicCANFDFr03"
    msg_id = 307
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['LCUL', 'CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FRDoorCinchHomeSwt:
        sig_name = "FRDoorCinchHomeSwt"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CinMotPosn_HomePosn': 0, 'CinMotPosn_NotHomePosn': 1}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

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

    class RRDoorCinchHomeSwt:
        sig_name = "RRDoorCinchHomeSwt"
        sig_start_bit = 3
        update_id_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CinMotPosn_HomePosn': 0, 'CinMotPosn_NotHomePosn': 1}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

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


class CCUMCUADPublicCANFDNmFr:
    msg_name = "CCUMCUADPublicCANFDNmFr"
    msg_id = 1282
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['VCU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VCUPublicCANFDFr03:
    msg_name = "VCUPublicCANFDFr03"
    msg_id = 257
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 16
    tx_node = "VCU"
    rx_nodes = ['ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HVFctPrio:
        sig_name = "HVFctPrio"
        sig_start_bit = 5
        update_id_bit = 1
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVFctPrio_Standby': 0, 'HVFctPrio_Dischrgning': 1, 'HVFctPrio_Chrgning': 2, 'HVFctPrio_Thermal': 3, 'HVFctPrio_Climate': 4, 'HVFctPrio_RemoteClimate': 5, 'HVFctPrio_Resd1': 6, 'HVFctPrio_Resd2': 7}
        compute_method = None
        length = 3
        startbit = 5
        byte = 0
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class HVActvReqForEgy:
        sig_name = "HVActvReqForEgy"
        sig_start_bit = 7
        update_id_bit = 2
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


class LCURPublicCANFDFr10:
    msg_name = "LCURPublicCANFDFr10"
    msg_id = 773
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['VCU', 'CCUMCUCD']
    sig_group_dict = {'CmprFb': ['CmprFbCmprI', 'CmprFbCmprIPha', 'CmprFbCmprSpd', 'CmprFbCmprSts1', 'CmprFbCmprSts2', 'CmprFbCmprT1', 'CmprFbCmprT2', 'CmprFbCmprU']}
    sig_group_dataid_dict = {}

    class CmprFbCmprT1:
        sig_name = "CmprFbCmprT1"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 254
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

    class CmprFbCmprIPha:
        sig_name = "CmprFbCmprIPha"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.5
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

    class CmprSpdIncReq:
        sig_name = "CmprSpdIncReq"
        sig_start_bit = 87
        update_id_bit = 90
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
        startbit = 87
        byte = 10
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CmprInCurrOverCurrStat:
        sig_name = "CmprInCurrOverCurrStat"
        sig_start_bit = 57
        update_id_bit = 83
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
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CmprOverPowerStat:
        sig_name = "CmprOverPowerStat"
        sig_start_bit = 75
        update_id_bit = 94
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CompOverPowerStat_Normal': 0, 'CompOverPowerStat_SpeedDecreasedforOverPower': 1, 'CompOverPowerStat_SpeedDecreasedforOverCurrent': 2, 'CompOverPowerStat_InoperativeforOverPower': 3, 'CompOverPowerStat_InoperativeforOverCurrent': 4}
        compute_method = None
        length = 4
        startbit = 75
        byte = 9
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CmprFbCmprU:
        sig_name = "CmprFbCmprU"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11000000, 0b00111111, 2, 6)]

    class CmprFbCmprT2:
        sig_name = "CmprFbCmprT2"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 254
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

    class CmprFbCmprI:
        sig_name = "CmprFbCmprI"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class CmprFbCmprSts2:
        sig_name = "CmprFbCmprSts2"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CompStat_NormalOperation': 0, 'CompStat_DegradedOperation': 1, 'CompStat_Inoperative': 2}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CmprROMFlt:
        sig_name = "CmprROMFlt"
        sig_start_bit = 65
        update_id_bit = 92
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
        startbit = 65
        byte = 8
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CmprOverMotorCurrStat:
        sig_name = "CmprOverMotorCurrStat"
        sig_start_bit = 79
        update_id_bit = 95
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CompOverMotorCurrStat_Normal': 0, 'CompOverMotorCurrStat_ImmediatelyShutdown': 1, 'CompOverMotorCurrStat_SpeedIncreased': 2, 'CompOverMotorCurrStat_SpeedDecreased': 3, 'CompOverMotorCurrStat_Shutdown': 4}
        compute_method = None
        length = 4
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CmprFbCmprSts1:
        sig_name = "CmprFbCmprSts1"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmprSts_CmprOff': 0, 'CmprSts_CmprOn': 1, 'CmprSts_CmprPwrLimd': 2, 'CmprSts_CmprPreHeat': 3, 'CmprSts_Reserved1': 4, 'CmprSts_Reserved2': 5, 'CmprSts_Reserved3': 6, 'CmprSts_SigNotAvl': 7}
        compute_method = None
        length = 3
        startbit = 61
        byte = 7
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class CmprMotorCurrOverCurrStat:
        sig_name = "CmprMotorCurrOverCurrStat"
        sig_start_bit = 67
        update_id_bit = 80
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
        startbit = 67
        byte = 8
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CmprEEPROMFault:
        sig_name = "CmprEEPROMFault"
        sig_start_bit = 58
        update_id_bit = 86
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
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CmprFb_UB:
        sig_name = "CmprFb_UB"
        sig_start_bit = 85
        update_id_bit = 85
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 85
        byte = 10
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CmprRAMFlt:
        sig_name = "CmprRAMFlt"
        sig_start_bit = 66
        update_id_bit = 93
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
        startbit = 66
        byte = 8
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CmprFbCmprSpd:
        sig_name = "CmprFbCmprSpd"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 50
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 254
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

    class CmprLostCommStat:
        sig_name = "CmprLostCommStat"
        sig_start_bit = 68
        update_id_bit = 81
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
        startbit = 68
        byte = 8
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CmprHVoltResonanceStat:
        sig_name = "CmprHVoltResonanceStat"
        sig_start_bit = 71
        update_id_bit = 84
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AcHVoltResonanceStat_Normal': 0, 'AcHVoltResonanceStat_SpeedDecreased': 1, 'AcHVoltResonanceStat_Inoperative': 2, 'AcHVoltResonanceStat_Reserved': 3}
        compute_method = None
        length = 3
        startbit = 71
        byte = 8
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CmprLiquidSluggingStat:
        sig_name = "CmprLiquidSluggingStat"
        sig_start_bit = 56
        update_id_bit = 82
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
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CmprRotorLockSts:
        sig_name = "CmprRotorLockSts"
        sig_start_bit = 64
        update_id_bit = 91
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
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class LCULPublicCANFDFr03:
    msg_name = "LCULPublicCANFDFr03"
    msg_id = 306
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['CCUMCUAD', 'CCUMCUCD', 'LCUR', 'VCU']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class RLLtchPosn:
        sig_name = "RLLtchPosn"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FLDoorCinchHomeSwt:
        sig_name = "FLDoorCinchHomeSwt"
        sig_start_bit = 14
        update_id_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CinMotPosn_HomePosn': 0, 'CinMotPosn_NotHomePosn': 1}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class RLDoorCinchHomeSwt:
        sig_name = "RLDoorCinchHomeSwt"
        sig_start_bit = 5
        update_id_bit = 0
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CinMotPosn_HomePosn': 0, 'CinMotPosn_NotHomePosn': 1}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FLLtchPosn:
        sig_name = "FLLtchPosn"
        sig_start_bit = 7
        update_id_bit = 1
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


class CCUMCUADPublicCANFDFr02:
    msg_name = "CCUMCUADPublicCANFDFr02"
    msg_id = 1
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['LCUR', 'LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ReLeDoorRdrModReq:
        sig_name = "ReLeDoorRdrModReq"
        sig_start_bit = 3
        update_id_bit = 13
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
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ReRiDoorRdrModReq:
        sig_name = "ReRiDoorRdrModReq"
        sig_start_bit = 1
        update_id_bit = 12
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
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FrntRiDoorRdrModReq:
        sig_name = "FrntRiDoorRdrModReq"
        sig_start_bit = 5
        update_id_bit = 14
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
        update_id_bit = 15
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


class LCULPublicCANFDFr01:
    msg_name = "LCULPublicCANFDFr01"
    msg_id = 65
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['ETC']
    sig_group_dict = {'PwrChLeInhb': ['PwrChLeInhbContnsPwrChLe1Inhb', 'PwrChLeInhbContnsPwrChLe2Inhb', 'PwrChLeInhbContnsPwrChLe3Inhb', 'PwrChLeInhbContnsPwrChLe4Inhb', 'PwrChLeInhbContnsPwrChLe5Inhb', 'PwrChLeInhbSwilPwrChLe10Inhb', 'PwrChLeInhbSwilPwrChLe11Inhb', 'PwrChLeInhbSwilPwrChLe12Inhb', 'PwrChLeInhbSwilPwrChLe13Inhb', 'PwrChLeInhbSwilPwrChLe14Inhb', 'PwrChLeInhbSwilPwrChLe15Inhb', 'PwrChLeInhbSwilPwrChLe16Inhb', 'PwrChLeInhbSwilPwrChLe17Inhb', 'PwrChLeInhbSwilPwrChLe18Inhb', 'PwrChLeInhbSwilPwrChLe19Inhb', 'PwrChLeInhbSwilPwrChLe1Inhb', 'PwrChLeInhbSwilPwrChLe20Inhb', 'PwrChLeInhbSwilPwrChLe21Inhb', 'PwrChLeInhbSwilPwrChLe22Inhb', 'PwrChLeInhbSwilPwrChLe23Inhb', 'PwrChLeInhbSwilPwrChLe24Inhb', 'PwrChLeInhbSwilPwrChLe25Inhb', 'PwrChLeInhbSwilPwrChLe26Inhb', 'PwrChLeInhbSwilPwrChLe27Inhb', 'PwrChLeInhbSwilPwrChLe28Inhb', 'PwrChLeInhbSwilPwrChLe29Inhb', 'PwrChLeInhbSwilPwrChLe2Inhb', 'PwrChLeInhbSwilPwrChLe3Inhb', 'PwrChLeInhbSwilPwrChLe4Inhb', 'PwrChLeInhbSwilPwrChLe5Inhb', 'PwrChLeInhbSwilPwrChLe6Inhb', 'PwrChLeInhbSwilPwrChLe7Inhb', 'PwrChLeInhbSwilPwrChLe8Inhb', 'PwrChLeInhbSwilPwrChLe9Inhb'], 'PwrChLeCmd': ['PwrChLeCmdContnsPwrChLe1Cmd', 'PwrChLeCmdContnsPwrChLe2Cmd', 'PwrChLeCmdContnsPwrChLe3Cmd', 'PwrChLeCmdContnsPwrChLe4Cmd', 'PwrChLeCmdContnsPwrChLe5Cmd', 'PwrChLeCmdSwilPwrChLe10Cmd', 'PwrChLeCmdSwilPwrChLe11Cmd', 'PwrChLeCmdSwilPwrChLe12Cmd', 'PwrChLeCmdSwilPwrChLe13Cmd', 'PwrChLeCmdSwilPwrChLe14Cmd', 'PwrChLeCmdSwilPwrChLe15Cmd', 'PwrChLeCmdSwilPwrChLe16Cmd', 'PwrChLeCmdSwilPwrChLe17Cmd', 'PwrChLeCmdSwilPwrChLe18Cmd', 'PwrChLeCmdSwilPwrChLe19Cmd', 'PwrChLeCmdSwilPwrChLe1Cmd', 'PwrChLeCmdSwilPwrChLe20Cmd', 'PwrChLeCmdSwilPwrChLe21Cmd', 'PwrChLeCmdSwilPwrChLe22Cmd', 'PwrChLeCmdSwilPwrChLe23Cmd', 'PwrChLeCmdSwilPwrChLe24Cmd', 'PwrChLeCmdSwilPwrChLe25Cmd', 'PwrChLeCmdSwilPwrChLe26Cmd', 'PwrChLeCmdSwilPwrChLe27Cmd', 'PwrChLeCmdSwilPwrChLe28Cmd', 'PwrChLeCmdSwilPwrChLe29Cmd', 'PwrChLeCmdSwilPwrChLe2Cmd', 'PwrChLeCmdSwilPwrChLe3Cmd', 'PwrChLeCmdSwilPwrChLe4Cmd', 'PwrChLeCmdSwilPwrChLe5Cmd', 'PwrChLeCmdSwilPwrChLe6Cmd', 'PwrChLeCmdSwilPwrChLe7Cmd', 'PwrChLeCmdSwilPwrChLe8Cmd', 'PwrChLeCmdSwilPwrChLe9Cmd'], 'PwrChLeCurrVal': ['PwrChLeCurrValContnsPwrChLe1CurrVal', 'PwrChLeCurrValContnsPwrChLe2CurrVal', 'PwrChLeCurrValContnsPwrChLe3CurrVal', 'PwrChLeCurrValContnsPwrChLe4CurrVal', 'PwrChLeCurrValContnsPwrChLe5CurrVal', 'PwrChLeCurrValSwilPwrChLe10CurrVal', 'PwrChLeCurrValSwilPwrChLe11CurrVal', 'PwrChLeCurrValSwilPwrChLe12CurrVal', 'PwrChLeCurrValSwilPwrChLe13CurrVal', 'PwrChLeCurrValSwilPwrChLe14CurrVal', 'PwrChLeCurrValSwilPwrChLe15CurrVal', 'PwrChLeCurrValSwilPwrChLe16CurrVal', 'PwrChLeCurrValSwilPwrChLe17CurrVal', 'PwrChLeCurrValSwilPwrChLe18CurrVal', 'PwrChLeCurrValSwilPwrChLe19CurrVal', 'PwrChLeCurrValSwilPwrChLe1CurrVal', 'PwrChLeCurrValSwilPwrChLe20CurrVal', 'PwrChLeCurrValSwilPwrChLe21CurrVal', 'PwrChLeCurrValSwilPwrChLe22CurrVal', 'PwrChLeCurrValSwilPwrChLe23CurrVal', 'PwrChLeCurrValSwilPwrChLe24CurrVal', 'PwrChLeCurrValSwilPwrChLe25CurrVal', 'PwrChLeCurrValSwilPwrChLe26CurrVal', 'PwrChLeCurrValSwilPwrChLe27CurrVal', 'PwrChLeCurrValSwilPwrChLe28CurrVal', 'PwrChLeCurrValSwilPwrChLe29CurrVal', 'PwrChLeCurrValSwilPwrChLe2CurrVal', 'PwrChLeCurrValSwilPwrChLe3CurrVal', 'PwrChLeCurrValSwilPwrChLe4CurrVal', 'PwrChLeCurrValSwilPwrChLe5CurrVal', 'PwrChLeCurrValSwilPwrChLe6CurrVal', 'PwrChLeCurrValSwilPwrChLe7CurrVal', 'PwrChLeCurrValSwilPwrChLe8CurrVal', 'PwrChLeCurrValSwilPwrChLe9CurrVal']}
    sig_group_dataid_dict = {}

    class PwrChLeCmdSwilPwrChLe14Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe14Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChLeInhbSwilPwrChLe8Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe8Inhb"
        sig_start_bit = 460
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 460
        byte = 57
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChLeCurrValSwilPwrChLe26CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe26CurrVal"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 61
        bmuws_info = [(7, 0b00111111, 0b11000000, 6, 0), (8, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeCmdSwilPwrChLe24Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe24Cmd"
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

    class PwrChLeCurrValSwilPwrChLe7CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe7CurrVal"
        sig_start_bit = 349
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 349
        bmuws_info = [(43, 0b00111111, 0b11000000, 6, 0), (44, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeCmdSwilPwrChLe3Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe3Cmd"
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

    class PwrChLeInhbContnsPwrChLe5Inhb:
        sig_name = "PwrChLeInhbContnsPwrChLe5Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 479
        byte = 59
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChLeInhbSwilPwrChLe11Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe11Inhb"
        sig_start_bit = 452
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 452
        byte = 56
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChLeCurrValSwilPwrChLe27CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe27CurrVal"
        sig_start_bit = 229
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 229
        bmuws_info = [(28, 0b00111111, 0b11000000, 6, 0), (29, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeInhbSwilPwrChLe20Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe20Inhb"
        sig_start_bit = 466
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 466
        byte = 58
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChLeCurrValContnsPwrChLe2CurrVal:
        sig_name = "PwrChLeCurrValContnsPwrChLe2CurrVal"
        sig_start_bit = 89
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 89
        bmuws_info = [(11, 0b00000011, 0b11111100, 2, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeInhbSwilPwrChLe22Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe22Inhb"
        sig_start_bit = 459
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 459
        byte = 57
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChLeInhbSwilPwrChLe5Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe5Inhb"
        sig_start_bit = 477
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 477
        byte = 59
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChLeCurrValSwilPwrChLe14CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe14CurrVal"
        sig_start_bit = 181
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 181
        bmuws_info = [(22, 0b00111111, 0b11000000, 6, 0), (23, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeInhbSwilPwrChLe28Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe28Inhb"
        sig_start_bit = 462
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 462
        byte = 57
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChLeInhbContnsPwrChLe4Inhb:
        sig_name = "PwrChLeInhbContnsPwrChLe4Inhb"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 457
        byte = 57
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChLeInhbSwilPwrChLe2Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe2Inhb"
        sig_start_bit = 467
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 467
        byte = 58
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChLeCurrValSwilPwrChLe20CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe20CurrVal"
        sig_start_bit = 137
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 137
        bmuws_info = [(17, 0b00000011, 0b11111100, 2, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeInhbSwilPwrChLe14Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe14Inhb"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 454
        byte = 56
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChLeCmdSwilPwrChLe19Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe19Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChLeInhbSwilPwrChLe6Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe6Inhb"
        sig_start_bit = 475
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 475
        byte = 59
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChLeInhbContnsPwrChLe1Inhb:
        sig_name = "PwrChLeInhbContnsPwrChLe1Inhb"
        sig_start_bit = 451
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 451
        byte = 56
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChLeCurrValSwilPwrChLe17CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe17CurrVal"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeCurrValSwilPwrChLe6CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe6CurrVal"
        sig_start_bit = 185
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 185
        bmuws_info = [(23, 0b00000011, 0b11111100, 2, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeCmdSwilPwrChLe13Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe13Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChLeCmdSwilPwrChLe10Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe10Cmd"
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

    class PwrChLeCurrValSwilPwrChLe29CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe29CurrVal"
        sig_start_bit = 401
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 401
        bmuws_info = [(50, 0b00000011, 0b11111100, 2, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeInhbSwilPwrChLe16Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe16Inhb"
        sig_start_bit = 461
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 461
        byte = 57
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChLeInhbSwilPwrChLe29Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe29Inhb"
        sig_start_bit = 478
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 478
        byte = 59
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChLeInhbSwilPwrChLe18Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe18Inhb"
        sig_start_bit = 453
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 453
        byte = 56
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChLeCurrValSwilPwrChLe5CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe5CurrVal"
        sig_start_bit = 257
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 257
        bmuws_info = [(32, 0b00000011, 0b11111100, 2, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeCurrValSwilPwrChLe10CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe10CurrVal"
        sig_start_bit = 233
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 233
        bmuws_info = [(29, 0b00000011, 0b11111100, 2, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeCurrValSwilPwrChLe3CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe3CurrVal"
        sig_start_bit = 373
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 373
        bmuws_info = [(46, 0b00111111, 0b11000000, 6, 0), (47, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeHWProtRst:
        sig_name = "PwrChLeHWProtRst"
        sig_start_bit = 445
        update_id_bit = 472
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

    class PwrChLeInhbSwilPwrChLe19Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe19Inhb"
        sig_start_bit = 470
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 470
        byte = 58
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChLeInhbContnsPwrChLe2Inhb:
        sig_name = "PwrChLeInhbContnsPwrChLe2Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 440
        byte = 55
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChLeCmdSwilPwrChLe11Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe11Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChLeInhbSwilPwrChLe1Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe1Inhb"
        sig_start_bit = 450
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 450
        byte = 56
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChLeCurrValContnsPwrChLe4CurrVal:
        sig_name = "PwrChLeCurrValContnsPwrChLe4CurrVal"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeCurrValSwilPwrChLe28CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe28CurrVal"
        sig_start_bit = 305
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 305
        bmuws_info = [(38, 0b00000011, 0b11111100, 2, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeInhbSwilPwrChLe17Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe17Inhb"
        sig_start_bit = 449
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 449
        byte = 56
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChLeCurrValSwilPwrChLe13CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe13CurrVal"
        sig_start_bit = 85
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 85
        bmuws_info = [(10, 0b00111111, 0b11000000, 6, 0), (11, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeCurrValContnsPwrChLe5CurrVal:
        sig_name = "PwrChLeCurrValContnsPwrChLe5CurrVal"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 157
        bmuws_info = [(19, 0b00111111, 0b11000000, 6, 0), (20, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeInhbSwilPwrChLe3Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe3Inhb"
        sig_start_bit = 455
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 455
        byte = 56
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChLeInhbSwilPwrChLe26Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe26Inhb"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 465
        byte = 58
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChLeCmdSwilPwrChLe27Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe27Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChLeCmdSwilPwrChLe8Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe8Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChLeCurrValSwilPwrChLe11CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe11CurrVal"
        sig_start_bit = 277
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 277
        bmuws_info = [(34, 0b00111111, 0b11000000, 6, 0), (35, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeInhbSwilPwrChLe23Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe23Inhb"
        sig_start_bit = 458
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 458
        byte = 57
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChLeCurrValSwilPwrChLe24CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe24CurrVal"
        sig_start_bit = 325
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 325
        bmuws_info = [(40, 0b00111111, 0b11000000, 6, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeInhbSwilPwrChLe15Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe15Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 471
        byte = 58
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChLeCmdSwilPwrChLe18Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe18Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChLeCmdSwilPwrChLe16Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe16Cmd"
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

    class PwrChLeCmdSwilPwrChLe28Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe28Cmd"
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

    class PwrChLeCmdContnsPwrChLe1Cmd:
        sig_name = "PwrChLeCmdContnsPwrChLe1Cmd"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChLeCurrValSwilPwrChLe2CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe2CurrVal"
        sig_start_bit = 301
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 301
        bmuws_info = [(37, 0b00111111, 0b11000000, 6, 0), (38, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeInhbSwilPwrChLe21Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe21Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 444
        byte = 55
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChLeInhbSwilPwrChLe4Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe4Inhb"
        sig_start_bit = 468
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 468
        byte = 58
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChLeCurrValSwilPwrChLe8CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe8CurrVal"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 37
        bmuws_info = [(4, 0b00111111, 0b11000000, 6, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeCmdContnsPwrChLe3Cmd:
        sig_name = "PwrChLeCmdContnsPwrChLe3Cmd"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChLeCmdSwilPwrChLe17Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe17Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChLeCurrValSwilPwrChLe16CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe16CurrVal"
        sig_start_bit = 209
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 209
        bmuws_info = [(26, 0b00000011, 0b11111100, 2, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeInhbSwilPwrChLe12Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe12Inhb"
        sig_start_bit = 463
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 463
        byte = 57
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChLeCurrValSwilPwrChLe1CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe1CurrVal"
        sig_start_bit = 205
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 205
        bmuws_info = [(25, 0b00111111, 0b11000000, 6, 0), (26, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeCurrValSwilPwrChLe9CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe9CurrVal"
        sig_start_bit = 109
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 109
        bmuws_info = [(13, 0b00111111, 0b11000000, 6, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeCmdSwilPwrChLe7Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe7Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChLeCmdSwilPwrChLe25Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe25Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChLeCmdSwilPwrChLe2Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe2Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChLeCmdSwilPwrChLe20Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe20Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChLeInhbSwilPwrChLe24Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe24Inhb"
        sig_start_bit = 443
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 443
        byte = 55
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChLeCmdSwilPwrChLe12Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe12Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChLeCmdSwilPwrChLe1Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe1Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChLeInhb_UB:
        sig_name = "PwrChLeInhb_UB"
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

    class PwrChLeInhbSwilPwrChLe7Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe7Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 441
        byte = 55
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChLeCmdSwilPwrChLe29Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe29Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChLeCmdSwilPwrChLe9Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe9Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChLeCurrValContnsPwrChLe1CurrVal:
        sig_name = "PwrChLeCurrValContnsPwrChLe1CurrVal"
        sig_start_bit = 133
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 133
        bmuws_info = [(16, 0b00111111, 0b11000000, 6, 0), (17, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeCmdSwilPwrChLe23Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe23Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChLeCurrValSwilPwrChLe19CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe19CurrVal"
        sig_start_bit = 253
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 253
        bmuws_info = [(31, 0b00111111, 0b11000000, 6, 0), (32, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeInhbSwilPwrChLe27Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe27Inhb"
        sig_start_bit = 469
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 469
        byte = 58
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChLeCurrValSwilPwrChLe15CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe15CurrVal"
        sig_start_bit = 65
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 65
        bmuws_info = [(8, 0b00000011, 0b11111100, 2, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeInhbContnsPwrChLe3Inhb:
        sig_name = "PwrChLeInhbContnsPwrChLe3Inhb"
        sig_start_bit = 476
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 476
        byte = 59
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChLeCmdSwilPwrChLe4Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe4Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChLeInhbSwilPwrChLe10Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe10Inhb"
        sig_start_bit = 442
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 442
        byte = 55
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChLeCmd_UB:
        sig_name = "PwrChLeCmd_UB"
        sig_start_bit = 474
        update_id_bit = 474
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 474
        byte = 59
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChLeCmdContnsPwrChLe4Cmd:
        sig_name = "PwrChLeCmdContnsPwrChLe4Cmd"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChLeCurrValSwilPwrChLe22CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe22CurrVal"
        sig_start_bit = 377
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 377
        bmuws_info = [(47, 0b00000011, 0b11111100, 2, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeCurrValSwilPwrChLe25CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe25CurrVal"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeCmdSwilPwrChLe26Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe26Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChLeCurrValSwilPwrChLe12CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe12CurrVal"
        sig_start_bit = 353
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 353
        bmuws_info = [(44, 0b00000011, 0b11111100, 2, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeCurrValContnsPwrChLe3CurrVal:
        sig_name = "PwrChLeCurrValContnsPwrChLe3CurrVal"
        sig_start_bit = 397
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 397
        bmuws_info = [(49, 0b00111111, 0b11000000, 6, 0), (50, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeCmdContnsPwrChLe5Cmd:
        sig_name = "PwrChLeCmdContnsPwrChLe5Cmd"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChLeCmdContnsPwrChLe2Cmd:
        sig_name = "PwrChLeCmdContnsPwrChLe2Cmd"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChLeCurrValSwilPwrChLe23CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe23CurrVal"
        sig_start_bit = 421
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 421
        bmuws_info = [(52, 0b00111111, 0b11000000, 6, 0), (53, 0b11111100, 0b00000011, 6, 2)]

    class PwrChLeCurrValSwilPwrChLe4CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe4CurrVal"
        sig_start_bit = 281
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 281
        bmuws_info = [(35, 0b00000011, 0b11111100, 2, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeCurrValSwilPwrChLe21CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe21CurrVal"
        sig_start_bit = 161
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 161
        bmuws_info = [(20, 0b00000011, 0b11111100, 2, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeInhbSwilPwrChLe25Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe25Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 464
        byte = 58
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChLeCurrValSwilPwrChLe18CurrVal:
        sig_name = "PwrChLeCurrValSwilPwrChLe18CurrVal"
        sig_start_bit = 425
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 425
        bmuws_info = [(53, 0b00000011, 0b11111100, 2, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11000000, 0b00111111, 2, 6)]

    class PwrChLeCmdSwilPwrChLe5Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe5Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChLeCmdSwilPwrChLe22Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe22Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChLeCmdSwilPwrChLe15Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe15Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChLeCurrVal_UB:
        sig_name = "PwrChLeCurrVal_UB"
        sig_start_bit = 473
        update_id_bit = 473
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 473
        byte = 59
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChLeCmdSwilPwrChLe21Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe21Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChLeInhbSwilPwrChLe13Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe13Inhb"
        sig_start_bit = 456
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 456
        byte = 57
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChLeCmdSwilPwrChLe6Cmd:
        sig_name = "PwrChLeCmdSwilPwrChLe6Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChLeInhbSwilPwrChLe9Inhb:
        sig_name = "PwrChLeInhbSwilPwrChLe9Inhb"
        sig_start_bit = 448
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 448
        byte = 56
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class LCURPublicCANFDNmFr:
    msg_name = "LCURPublicCANFDNmFr"
    msg_id = 1284
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCURPublicCANFDFr11:
    msg_name = "LCURPublicCANFDFr11"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['LCUL', 'CCUMCUCD']
    sig_group_dict = {'DrvReqOfPositionLamp': ['DrvReqOfPositionLampLightID1', 'DrvReqOfPositionLampOffOnCmd', 'DrvReqOfPositionLampPerc']}
    sig_group_dataid_dict = {}

    class DrvReqOfPositionLampLightID1:
        sig_name = "DrvReqOfPositionLampLightID1"
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
        sig_value_table = {'LightID1_ALL': 0, 'LightID1_Front': 1, 'LightID1_Rear': 2, 'LightID1_LeftFrontLeftRearLeft': 3, 'LightID1_RightFrontRightRearRight': 4, 'LightID1_FrontLeft': 5, 'LightID1_FrontRight': 6, 'LightID1_RearLeft': 7, 'LightID1_FrontLeftRearRight': 8, 'LightID1_FrontRightRearLeft': 9, 'LightID1_ExceptFrontLeft': 10, 'LightID1_ExceptFrontRight': 11, 'LightID1_ExceptRearLeft': 12, 'LightID1_ExceptRearRight': 13, 'LightID1_Reserved1': 14, 'LightID1_Reserved2': 15}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DrvReqOfPositionLampPerc:
        sig_name = "DrvReqOfPositionLampPerc"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 7
        byte = 0
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class DrvReqOfPositionLampOffOnCmd:
        sig_name = "DrvReqOfPositionLampOffOnCmd"
        sig_start_bit = 11
        update_id_bit = None
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
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DrvReqOfPositionLamp_UB:
        sig_name = "DrvReqOfPositionLamp_UB"
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


class VCUPublicCANFDNmFr:
    msg_name = "VCUPublicCANFDNmFr"
    msg_id = 1285
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VCU"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUCDPublicCANFDFr02:
    msg_name = "CCUMCUCDPublicCANFDFr02"
    msg_id = 64
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['LCUL', 'CCUMCUAD', 'LCUR', 'VCU']
    sig_group_dict = {'VMMGlbSig': ['VMMGlbSigCarModSts', 'VMMGlbSigChks', 'VMMGlbSigCntr', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigLoBattModSts', 'VMMGlbSigUsgModSts'], 'EPBHpsReqSec': ['EPBHpsReqSecChks', 'EPBHpsReqSecCntr', 'EPBHpsReqSecHpsReq'], 'BrkSysStSecRdnt': ['BrkSysStSecRdntBrkSysSts', 'BrkSysStSecRdntChks', 'BrkSysStSecRdntCntr'], 'ADSSlaveAgCtrlTqLim': ['ADSSlaveAgCtrlTqLimChks', 'ADSSlaveAgCtrlTqLimCntr', 'ADSSlaveAgCtrlTqLimLowrLim', 'ADSSlaveAgCtrlTqLimUpperLim'], 'EpbCoornSec': ['EpbCoornSecChks', 'EpbCoornSecCntr', 'EpbCoornSecCommunicationAvl', 'EpbCoornSecHostAvailabilityFull', 'EpbCoornSecHostAvailabilityRelOnly', 'EpbCoornSecReserved1', 'EpbCoornSecReserved2', 'EpbCoornSecReserved3', 'EpbCoornSecReserved4', 'EpbCoornSecReserved5', 'EpbCoornSecReserved6', 'EpbCoornSecReserved7'], 'ADSSlavePinAgReq': ['ADSSlavePinAgReqAsyPinionAgReq', 'ADSSlavePinAgReqChks', 'ADSSlavePinAgReqCntr']}
    sig_group_dataid_dict = {'VMMGlbSig': 1074}

    class ADSSlaveAgCtrlTqLimCntr:
        sig_name = "ADSSlaveAgCtrlTqLimCntr"
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

    class EPBHpsReqSecHpsReq:
        sig_name = "EPBHpsReqSecHpsReq"
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
        sig_value_table = {'HpsReq_NoReq': 0, 'HpsReq_Normal': 1, 'HpsReq_Max': 2, 'HpsReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 179
        byte = 22
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VMMGlbSig_UB:
        sig_name = "VMMGlbSig_UB"
        sig_start_bit = 150
        update_id_bit = 150
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 150
        byte = 18
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BrkSysStSecRdntBrkSysSts:
        sig_name = "BrkSysStSecRdntBrkSysSts"
        sig_start_bit = 131
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotAvailable_Temporary': 0, 'NotAvailable_NotReleased': 1, 'NotAvailable_Permanent': 2, 'NotActivated_FullAvailable': 3, 'Activation_Preparation': 4, 'Activation_Pending': 5, 'Activation_PendingRedundancyLost': 6, 'Activation_PendingFailOperation': 7, 'Activated_FullAvailable': 8, 'Activated_FailOperation': 9, 'Activated_RedundancyLost': 10, 'Deactivation_Pending': 11}
        compute_method = None
        length = 4
        startbit = 131
        byte = 16
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EpbCoornSecHostAvailabilityRelOnly:
        sig_name = "EpbCoornSecHostAvailabilityRelOnly"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 167
        byte = 20
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VMMGlbSigCarModSts:
        sig_name = "VMMGlbSigCarModSts"
        sig_start_bit = 67
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
        startbit = 67
        byte = 8
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EPBHpsReqSec_UB:
        sig_name = "EPBHpsReqSec_UB"
        sig_start_bit = 113
        update_id_bit = 113
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 113
        byte = 14
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EpbCoornSecReserved4:
        sig_name = "EpbCoornSecReserved4"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 163
        byte = 20
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VMMGlbSigDrvgSubSts1:
        sig_name = "VMMGlbSigDrvgSubSts1"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EpbCoornSecReserved3:
        sig_name = "EpbCoornSecReserved3"
        sig_start_bit = 164
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 164
        byte = 20
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EpbCoornSecReserved1:
        sig_name = "EpbCoornSecReserved1"
        sig_start_bit = 166
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 166
        byte = 20
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VMMGlbSigLoBattModSts:
        sig_name = "VMMGlbSigLoBattModSts"
        sig_start_bit = 119
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
        startbit = 119
        byte = 14
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EPBHpsReqSecCntr:
        sig_name = "EPBHpsReqSecCntr"
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

    class ADSSlavePinAgReqChks:
        sig_name = "ADSSlavePinAgReqChks"
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

    class BrkSysStSecRdntCntr:
        sig_name = "BrkSysStSecRdntCntr"
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

    class EpbCoornSecHostAvailabilityFull:
        sig_name = "EpbCoornSecHostAvailabilityFull"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 148
        byte = 18
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class UsgModSts:
        sig_name = "UsgModSts"
        sig_start_bit = 71
        update_id_bit = 151
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
        startbit = 71
        byte = 8
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class BrkSysStSecRdnt_UB:
        sig_name = "BrkSysStSecRdnt_UB"
        sig_start_bit = 116
        update_id_bit = 116
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 116
        byte = 14
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EpbCoornSecReserved7:
        sig_name = "EpbCoornSecReserved7"
        sig_start_bit = 160
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 160
        byte = 20
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VMMGlbSigUsgModSts:
        sig_name = "VMMGlbSigUsgModSts"
        sig_start_bit = 87
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
        startbit = 87
        byte = 10
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CarModSts:
        sig_name = "CarModSts"
        sig_start_bit = 59
        update_id_bit = 115
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
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VMMGlbSigChks:
        sig_name = "VMMGlbSigChks"
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

    class EpbCoornSecCommunicationAvl:
        sig_name = "EpbCoornSecCommunicationAvl"
        sig_start_bit = 149
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 149
        byte = 18
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ADSSlaveAgCtrlTqLim_UB:
        sig_name = "ADSSlaveAgCtrlTqLim_UB"
        sig_start_bit = 118
        update_id_bit = 118
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 118
        byte = 14
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EPBHpsReqSecChks:
        sig_name = "EPBHpsReqSecChks"
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

    class EpbCoornSecReserved6:
        sig_name = "EpbCoornSecReserved6"
        sig_start_bit = 161
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 161
        byte = 20
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VMMGlbSigInactvSubSts1:
        sig_name = "VMMGlbSigInactvSubSts1"
        sig_start_bit = 95
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
        startbit = 95
        byte = 11
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EpbCoornSecReserved2:
        sig_name = "EpbCoornSecReserved2"
        sig_start_bit = 165
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 165
        byte = 20
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EpbCoornSecReserved5:
        sig_name = "EpbCoornSecReserved5"
        sig_start_bit = 162
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 162
        byte = 20
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class EpbCoornSec_UB:
        sig_name = "EpbCoornSec_UB"
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

    class ADSSlaveAgCtrlTqLimChks:
        sig_name = "ADSSlaveAgCtrlTqLimChks"
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

    class VMMGlbSigCnvincSubSts1:
        sig_name = "VMMGlbSigCnvincSubSts1"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EPBHpsTarPSec:
        sig_name = "EPBHpsTarPSec"
        sig_start_bit = 143
        update_id_bit = 112
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 220
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

    class ADSSlavePinAgReqAsyPinionAgReq:
        sig_name = "ADSSlavePinAgReqAsyPinionAgReq"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.0009765625
        sig_value_offset = -14.5
        sig_value_min = 0
        sig_value_max = 29696
        sig_byteorder = "Motorola"
        sig_value_init = 14848
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class EpbCoornSecCntr:
        sig_name = "EpbCoornSecCntr"
        sig_start_bit = 147
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
        startbit = 147
        byte = 18
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ADSSlaveAgCtrlTqLimLowrLim:
        sig_name = "ADSSlaveAgCtrlTqLimLowrLim"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.125
        sig_value_offset = -30.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 16
        bmuws_info = [(2, 0b00000001, 0b11111110, 1, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class ADSSlavePinAgReq_UB:
        sig_name = "ADSSlavePinAgReq_UB"
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

    class EpbCoornSecChks:
        sig_name = "EpbCoornSecChks"
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

    class VMMGlbSigCntr:
        sig_name = "VMMGlbSigCntr"
        sig_start_bit = 83
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
        startbit = 83
        byte = 10
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BrkSysStSecRdntChks:
        sig_name = "BrkSysStSecRdntChks"
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

    class ADSSlaveAgCtrlTqLimUpperLim:
        sig_name = "ADSSlaveAgCtrlTqLimUpperLim"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.125
        sig_value_offset = -30.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 480
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b10000000, 0b01111111, 1, 7)]

    class ADSSlavePinAgReqCntr:
        sig_name = "ADSSlavePinAgReqCntr"
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


class CCUMCUCDPublicCANFDFr06:
    msg_name = "CCUMCUCDPublicCANFDFr06"
    msg_id = 657
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['ETC']
    sig_group_dict = {'ClimateAirTempDecaySectn': ['ClimateAirTempDecaySectnFrntLe', 'ClimateAirTempDecaySectnFrntRi', 'ClimateAirTempDecaySectnReLe', 'ClimateAirTempDecaySectnReRi'], 'ClimateAirTempIniSuppsn': ['ClimateAirTempIniSuppsnFrntLe', 'ClimateAirTempIniSuppsnFrntRi', 'ClimateAirTempIniSuppsnReLe', 'ClimateAirTempIniSuppsnReRi'], 'ClimateAirTempTarCalcn': ['ClimateAirTempTarCalcnFrntLe', 'ClimateAirTempTarCalcnFrntRi', 'ClimateAirTempTarCalcnReLe', 'ClimateAirTempTarCalcnReRi'], 'ClimateAirFlwTarCalcn': ['ClimateAirFlwTarCalcnFrntLe', 'ClimateAirFlwTarCalcnFrntRi', 'ClimateAirFlwTarCalcnReLe', 'ClimateAirFlwTarCalcnReRi'], 'ClimateAirFlwDecayRat': ['ClimateAirFlwDecayRatFrntLe', 'ClimateAirFlwDecayRatFrntRi', 'ClimateAirFlwDecayRatReLe', 'ClimateAirFlwDecayRatReRi'], 'ClimateAirTempBascCalcn': ['ClimateAirTempBascCalcnFrntLe', 'ClimateAirTempBascCalcnFrntRi', 'ClimateAirTempBascCalcnReLe', 'ClimateAirTempBascCalcnReRi'], 'ClimateAirFlwIniSuppsn': ['ClimateAirFlwIniSuppsnFrntLe', 'ClimateAirFlwIniSuppsnFrntRi', 'ClimateAirFlwIniSuppsnReLe', 'ClimateAirFlwIniSuppsnReRi'], 'ClimateAirTempRealSuppsn': ['ClimateAirTempRealSuppsnFrntLe', 'ClimateAirTempRealSuppsnFrntRi', 'ClimateAirTempRealSuppsnReLe', 'ClimateAirTempRealSuppsnReRi'], 'ClimateAirTempDecayRat': ['ClimateAirTempDecayRatFrntLe', 'ClimateAirTempDecayRatFrntRi', 'ClimateAirTempDecayRatReLe', 'ClimateAirTempDecayRatReRi'], 'ClimateAirFlwRealSuppsn': ['ClimateAirFlwRealSuppsnFrntLe', 'ClimateAirFlwRealSuppsnFrntRi', 'ClimateAirFlwRealSuppsnReLe', 'ClimateAirFlwRealSuppsnReRi'], 'ClimateAirFlwBascCalcn': ['ClimateAirFlwBascCalcnFrntLe', 'ClimateAirFlwBascCalcnFrntRi', 'ClimateAirFlwBascCalcnReLe', 'ClimateAirFlwBascCalcnReRi'], 'ClimateAirFlwDecaySectn': ['ClimateAirFlwDecaySectnFrntLe', 'ClimateAirFlwDecaySectnFrntRi', 'ClimateAirFlwDecaySectnReLe', 'ClimateAirFlwDecaySectnReRi']}
    sig_group_dataid_dict = {}

    class ClimateAirTempDecaySectn_UB:
        sig_name = "ClimateAirTempDecaySectn_UB"
        sig_start_bit = 493
        update_id_bit = 493
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 493
        byte = 61
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ClimateAirTempBascCalcnReLe:
        sig_name = "ClimateAirTempBascCalcnReLe"
        sig_start_bit = 244
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
        startbit = 244
        bmuws_info = [(30, 0b00011111, 0b11100000, 5, 0), (31, 0b11111111, 0b00000000, 8, 0)]

    class ClimateAirTempTarCalcnFrntLe:
        sig_name = "ClimateAirTempTarCalcnFrntLe"
        sig_start_bit = 448
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
        startbit = 448
        bmuws_info = [(56, 0b00000001, 0b11111110, 1, 0), (57, 0b11111111, 0b00000000, 8, 0), (58, 0b11110000, 0b00001111, 4, 4)]

    class ClimateAirTempIniSuppsn_UB:
        sig_name = "ClimateAirTempIniSuppsn_UB"
        sig_start_bit = 492
        update_id_bit = 492
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 492
        byte = 61
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ClimateAirTempTarCalcnFrntRi:
        sig_name = "ClimateAirTempTarCalcnFrntRi"
        sig_start_bit = 467
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
        startbit = 467
        bmuws_info = [(58, 0b00001111, 0b11110000, 4, 0), (59, 0b11111111, 0b00000000, 8, 0), (60, 0b10000000, 0b01111111, 1, 7)]

    class ClimateAirTempDecayRatFrntLe:
        sig_name = "ClimateAirTempDecayRatFrntLe"
        sig_start_bit = 275
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 275
        bmuws_info = [(34, 0b00001111, 0b11110000, 4, 0), (35, 0b11100000, 0b00011111, 3, 5)]

    class ClimateAirTempTarCalcn_UB:
        sig_name = "ClimateAirTempTarCalcn_UB"
        sig_start_bit = 490
        update_id_bit = 490
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 490
        byte = 61
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ClimateAirFlwDecaySectnReLe:
        sig_name = "ClimateAirFlwDecaySectnReLe"
        sig_start_bit = 75
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 75
        bmuws_info = [(9, 0b00001111, 0b11110000, 4, 0), (10, 0b11100000, 0b00011111, 3, 5)]

    class ClimaEcoSts:
        sig_name = "ClimaEcoSts"
        sig_start_bit = 7
        update_id_bit = 486
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

    class ClimateAirTempRealSuppsnReLe:
        sig_name = "ClimateAirTempRealSuppsnReLe"
        sig_start_bit = 385
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
        startbit = 385
        bmuws_info = [(48, 0b00000011, 0b11111100, 2, 0), (49, 0b11111111, 0b00000000, 8, 0), (50, 0b11100000, 0b00011111, 3, 5)]

    class ClimateAirFlwDecayRatReRi:
        sig_name = "ClimateAirFlwDecayRatReRi"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 48
        bmuws_info = [(6, 0b00000001, 0b11111110, 1, 0), (7, 0b11111100, 0b00000011, 6, 2)]

    class ClimateAirTempDecayRatFrntRi:
        sig_name = "ClimateAirTempDecayRatFrntRi"
        sig_start_bit = 293
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 293
        bmuws_info = [(36, 0b00111111, 0b11000000, 6, 0), (37, 0b10000000, 0b01111111, 1, 7)]

    class ClimateAirFlwTarCalcn_UB:
        sig_name = "ClimateAirFlwTarCalcn_UB"
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

    class ClimateAirTempDecaySectnReRi:
        sig_name = "ClimateAirTempDecaySectnReRi"
        sig_start_bit = 311
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 311
        byte = 38
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ClimateAirFlwTarCalcnReRi:
        sig_name = "ClimateAirFlwTarCalcnReRi"
        sig_start_bit = 200
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
        startbit = 200
        bmuws_info = [(25, 0b00000001, 0b11111110, 1, 0), (26, 0b11111111, 0b00000000, 8, 0), (27, 0b10000000, 0b01111111, 1, 7)]

    class ClimateAirTempIniSuppsnReLe:
        sig_name = "ClimateAirTempIniSuppsnReLe"
        sig_start_bit = 322
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
        startbit = 322
        bmuws_info = [(40, 0b00000111, 0b11111000, 3, 0), (41, 0b11111111, 0b00000000, 8, 0), (42, 0b11000000, 0b00111111, 2, 6)]

    class ClimateAirFlwRealSuppsnReLe:
        sig_name = "ClimateAirFlwRealSuppsnReLe"
        sig_start_bit = 160
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
        startbit = 160
        bmuws_info = [(20, 0b00000001, 0b11111110, 1, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b10000000, 0b01111111, 1, 7)]

    class ClimateAirTempDecaySectnReLe:
        sig_name = "ClimateAirTempDecaySectnReLe"
        sig_start_bit = 313
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 313
        bmuws_info = [(39, 0b00000011, 0b11111100, 2, 0), (40, 0b11111000, 0b00000111, 5, 3)]

    class ClimateAirFlwDecayRatReLe:
        sig_name = "ClimateAirFlwDecayRatReLe"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 55
        byte = 6
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ClimateAirTempIniSuppsnFrntLe:
        sig_name = "ClimateAirTempIniSuppsnFrntLe"
        sig_start_bit = 344
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
        startbit = 344
        bmuws_info = [(43, 0b00000001, 0b11111110, 1, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11110000, 0b00001111, 4, 4)]

    class ClimateAirFlwRealSuppsnFrntLe:
        sig_name = "ClimateAirFlwRealSuppsnFrntLe"
        sig_start_bit = 154
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
        startbit = 154
        bmuws_info = [(19, 0b00000111, 0b11111000, 3, 0), (20, 0b11111110, 0b00000001, 7, 1)]

    class ClimateAirTempBascCalcnFrntRi:
        sig_name = "ClimateAirTempBascCalcnFrntRi"
        sig_start_bit = 225
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
        startbit = 225
        bmuws_info = [(28, 0b00000011, 0b11111100, 2, 0), (29, 0b11111111, 0b00000000, 8, 0), (30, 0b11100000, 0b00011111, 3, 5)]

    class ClimateAirTempDecayRatReLe:
        sig_name = "ClimateAirTempDecayRatReLe"
        sig_start_bit = 266
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 266
        bmuws_info = [(33, 0b00000111, 0b11111000, 3, 0), (34, 0b11110000, 0b00001111, 4, 4)]

    class ClimateAirTempDecaySectnFrntRi:
        sig_name = "ClimateAirTempDecaySectnFrntRi"
        sig_start_bit = 302
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 302
        byte = 37
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class ClimateAirFlwIniSuppsnFrntRi:
        sig_name = "ClimateAirFlwIniSuppsnFrntRi"
        sig_start_bit = 108
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
        startbit = 108
        bmuws_info = [(13, 0b00011111, 0b11100000, 5, 0), (14, 0b11111000, 0b00000111, 5, 3)]

    class ClimateAirTempDecayRatReRi:
        sig_name = "ClimateAirTempDecayRatReRi"
        sig_start_bit = 284
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 284
        bmuws_info = [(35, 0b00011111, 0b11100000, 5, 0), (36, 0b11000000, 0b00111111, 2, 6)]

    class ClimateAirFlwIniSuppsnFrntLe:
        sig_name = "ClimateAirFlwIniSuppsnFrntLe"
        sig_start_bit = 102
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
        startbit = 102
        bmuws_info = [(12, 0b01111111, 0b10000000, 7, 0), (13, 0b11100000, 0b00011111, 3, 5)]

    class ClimateAirFlwDecayRatFrntLe:
        sig_name = "ClimateAirFlwDecayRatFrntLe"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 57
        bmuws_info = [(7, 0b00000011, 0b11111100, 2, 0), (8, 0b11111000, 0b00000111, 5, 3)]

    class ClimateAirFlwDecayRat_UB:
        sig_name = "ClimateAirFlwDecayRat_UB"
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

    class ClimateAirTempDecaySectnFrntLe:
        sig_name = "ClimateAirTempDecaySectnFrntLe"
        sig_start_bit = 304
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 304
        bmuws_info = [(38, 0b00000001, 0b11111110, 1, 0), (39, 0b11111100, 0b00000011, 6, 2)]

    class ClimateAirTempIniSuppsnFrntRi:
        sig_name = "ClimateAirTempIniSuppsnFrntRi"
        sig_start_bit = 341
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
        startbit = 341
        bmuws_info = [(42, 0b00111111, 0b11000000, 6, 0), (43, 0b11111110, 0b00000001, 7, 1)]

    class ClimateAirFlwDecaySectnFrntLe:
        sig_name = "ClimateAirFlwDecaySectnFrntLe"
        sig_start_bit = 66
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 66
        bmuws_info = [(8, 0b00000111, 0b11111000, 3, 0), (9, 0b11110000, 0b00001111, 4, 4)]

    class ClimateAirTempBascCalcn_UB:
        sig_name = "ClimateAirTempBascCalcn_UB"
        sig_start_bit = 495
        update_id_bit = 495
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 495
        byte = 61
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ClimateAirFlwBascCalcnReLe:
        sig_name = "ClimateAirFlwBascCalcnReLe"
        sig_start_bit = 6
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
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class ClimateAirFlwBascCalcnFrntRi:
        sig_name = "ClimateAirFlwBascCalcnFrntRi"
        sig_start_bit = 12
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
        startbit = 12
        bmuws_info = [(1, 0b00011111, 0b11100000, 5, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class ClimateAirTempRealSuppsnFrntRi:
        sig_name = "ClimateAirTempRealSuppsnFrntRi"
        sig_start_bit = 382
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
        startbit = 382
        bmuws_info = [(47, 0b01111111, 0b10000000, 7, 0), (48, 0b11111100, 0b00000011, 6, 2)]

    class ClimateAirTempTarCalcnReRi:
        sig_name = "ClimateAirTempTarCalcnReRi"
        sig_start_bit = 445
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
        startbit = 445
        bmuws_info = [(55, 0b00111111, 0b11000000, 6, 0), (56, 0b11111110, 0b00000001, 7, 1)]

    class ClimateAirFlwIniSuppsn_UB:
        sig_name = "ClimateAirFlwIniSuppsn_UB"
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

    class ClimateAirFlwRealSuppsnReRi:
        sig_name = "ClimateAirFlwRealSuppsnReRi"
        sig_start_bit = 148
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
        startbit = 148
        bmuws_info = [(18, 0b00011111, 0b11100000, 5, 0), (19, 0b11111000, 0b00000111, 5, 3)]

    class ClimateAirFlwDecayRatFrntRi:
        sig_name = "ClimateAirFlwDecayRatFrntRi"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 46
        byte = 5
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class ClimateAirFlwRealSuppsnFrntRi:
        sig_name = "ClimateAirFlwRealSuppsnFrntRi"
        sig_start_bit = 142
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
        startbit = 142
        bmuws_info = [(17, 0b01111111, 0b10000000, 7, 0), (18, 0b11100000, 0b00011111, 3, 5)]

    class ClimateAirFlwIniSuppsnReLe:
        sig_name = "ClimateAirFlwIniSuppsnReLe"
        sig_start_bit = 120
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
        startbit = 120
        bmuws_info = [(15, 0b00000001, 0b11111110, 1, 0), (16, 0b11111111, 0b00000000, 8, 0), (17, 0b10000000, 0b01111111, 1, 7)]

    class ClimateAirTempBascCalcnFrntLe:
        sig_name = "ClimateAirTempBascCalcnFrntLe"
        sig_start_bit = 222
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
        startbit = 222
        bmuws_info = [(27, 0b01111111, 0b10000000, 7, 0), (28, 0b11111100, 0b00000011, 6, 2)]

    class ClimateAirTempRealSuppsn_UB:
        sig_name = "ClimateAirTempRealSuppsn_UB"
        sig_start_bit = 491
        update_id_bit = 491
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 491
        byte = 61
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ClimateAirFlwIniSuppsnReRi:
        sig_name = "ClimateAirFlwIniSuppsnReRi"
        sig_start_bit = 114
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
        startbit = 114
        bmuws_info = [(14, 0b00000111, 0b11111000, 3, 0), (15, 0b11111110, 0b00000001, 7, 1)]

    class ClimateAirFlwTarCalcnReLe:
        sig_name = "ClimateAirFlwTarCalcnReLe"
        sig_start_bit = 182
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
        startbit = 182
        bmuws_info = [(22, 0b01111111, 0b10000000, 7, 0), (23, 0b11100000, 0b00011111, 3, 5)]

    class ClimateAirTempIniSuppsnReRi:
        sig_name = "ClimateAirTempIniSuppsnReRi"
        sig_start_bit = 363
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
        startbit = 363
        bmuws_info = [(45, 0b00001111, 0b11110000, 4, 0), (46, 0b11111111, 0b00000000, 8, 0), (47, 0b10000000, 0b01111111, 1, 7)]

    class ClimateAirFlwTarCalcnFrntRi:
        sig_name = "ClimateAirFlwTarCalcnFrntRi"
        sig_start_bit = 194
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
        startbit = 194
        bmuws_info = [(24, 0b00000111, 0b11111000, 3, 0), (25, 0b11111110, 0b00000001, 7, 1)]

    class ClimateAirTempDecayRat_UB:
        sig_name = "ClimateAirTempDecayRat_UB"
        sig_start_bit = 494
        update_id_bit = 494
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 494
        byte = 61
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ClimateAirFlwBascCalcnFrntLe:
        sig_name = "ClimateAirFlwBascCalcnFrntLe"
        sig_start_bit = 18
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
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class ClimateAirTempRealSuppsnFrntLe:
        sig_name = "ClimateAirTempRealSuppsnFrntLe"
        sig_start_bit = 404
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
        startbit = 404
        bmuws_info = [(50, 0b00011111, 0b11100000, 5, 0), (51, 0b11111111, 0b00000000, 8, 0)]

    class ClimateAirTempRealSuppsnReRi:
        sig_name = "ClimateAirTempRealSuppsnReRi"
        sig_start_bit = 423
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
        startbit = 423
        bmuws_info = [(52, 0b11111111, 0b00000000, 8, 0), (53, 0b11111000, 0b00000111, 5, 3)]

    class ClimateAirTempTarCalcnReLe:
        sig_name = "ClimateAirTempTarCalcnReLe"
        sig_start_bit = 426
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
        startbit = 426
        bmuws_info = [(53, 0b00000111, 0b11111000, 3, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11000000, 0b00111111, 2, 6)]

    class ClimateAirFlwDecaySectnReRi:
        sig_name = "ClimateAirFlwDecaySectnReRi"
        sig_start_bit = 93
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 93
        bmuws_info = [(11, 0b00111111, 0b11000000, 6, 0), (12, 0b10000000, 0b01111111, 1, 7)]

    class ClimateAirTempBascCalcnReRi:
        sig_name = "ClimateAirTempBascCalcnReRi"
        sig_start_bit = 263
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
        startbit = 263
        bmuws_info = [(32, 0b11111111, 0b00000000, 8, 0), (33, 0b11111000, 0b00000111, 5, 3)]

    class ClimateAirFlwRealSuppsn_UB:
        sig_name = "ClimateAirFlwRealSuppsn_UB"
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

    class ClimateAirFlwTarCalcnFrntLe:
        sig_name = "ClimateAirFlwTarCalcnFrntLe"
        sig_start_bit = 188
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
        startbit = 188
        bmuws_info = [(23, 0b00011111, 0b11100000, 5, 0), (24, 0b11111000, 0b00000111, 5, 3)]

    class ClimateAirFlwBascCalcn_UB:
        sig_name = "ClimateAirFlwBascCalcn_UB"
        sig_start_bit = 485
        update_id_bit = 485
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 485
        byte = 60
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ClimateAirFlwBascCalcnReRi:
        sig_name = "ClimateAirFlwBascCalcnReRi"
        sig_start_bit = 24
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
        startbit = 24
        bmuws_info = [(3, 0b00000001, 0b11111110, 1, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b10000000, 0b01111111, 1, 7)]

    class ClimateAirFlwDecaySectnFrntRi:
        sig_name = "ClimateAirFlwDecaySectnFrntRi"
        sig_start_bit = 84
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 84
        bmuws_info = [(10, 0b00011111, 0b11100000, 5, 0), (11, 0b11000000, 0b00111111, 2, 6)]

    class ClimateAirFlwDecaySectn_UB:
        sig_name = "ClimateAirFlwDecaySectn_UB"
        sig_start_bit = 483
        update_id_bit = 483
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 483
        byte = 60
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class LCULPublicCANFDFr05:
    msg_name = "LCULPublicCANFDFr05"
    msg_id = 403
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['CCUMCUAD', 'CCUMCUCD']
    sig_group_dict = {'FrntLeDoorRdrObj13': ['FrntLeDoorRdrObj13RdrObjDstX', 'FrntLeDoorRdrObj13RdrObjDstY', 'FrntLeDoorRdrObj13RdrObjDstZ', 'FrntLeDoorRdrObj13RdrObjV'], 'FrntLeDoorRdrObj14': ['FrntLeDoorRdrObj14RdrObjDstX', 'FrntLeDoorRdrObj14RdrObjDstY', 'FrntLeDoorRdrObj14RdrObjDstZ', 'FrntLeDoorRdrObj14RdrObjV'], 'FrntLeDoorRdrObj15': ['FrntLeDoorRdrObj15RdrObjDstX', 'FrntLeDoorRdrObj15RdrObjDstY', 'FrntLeDoorRdrObj15RdrObjDstZ', 'FrntLeDoorRdrObj15RdrObjV'], 'FrntLeDoorRdrObj16': ['FrntLeDoorRdrObj16RdrObjDstX', 'FrntLeDoorRdrObj16RdrObjDstY', 'FrntLeDoorRdrObj16RdrObjDstZ', 'FrntLeDoorRdrObj16RdrObjV'], 'FrntLeDoorRdrObj9': ['FrntLeDoorRdrObj9RdrObjDstX', 'FrntLeDoorRdrObj9RdrObjDstY', 'FrntLeDoorRdrObj9RdrObjDstZ', 'FrntLeDoorRdrObj9RdrObjV'], 'FrntLeDoorRdrObj10': ['FrntLeDoorRdrObj10RdrObjDstX', 'FrntLeDoorRdrObj10RdrObjDstY', 'FrntLeDoorRdrObj10RdrObjDstZ', 'FrntLeDoorRdrObj10RdrObjV'], 'FrntLeDoorRdrObj11': ['FrntLeDoorRdrObj11RdrObjDstX', 'FrntLeDoorRdrObj11RdrObjDstY', 'FrntLeDoorRdrObj11RdrObjDstZ', 'FrntLeDoorRdrObj11RdrObjV'], 'FrntLeDoorRdrObj12': ['FrntLeDoorRdrObj12RdrObjDstX', 'FrntLeDoorRdrObj12RdrObjDstY', 'FrntLeDoorRdrObj12RdrObjDstZ', 'FrntLeDoorRdrObj12RdrObjV'], 'ChargeLidAntiPnchSts': ['ChargeLidAntiPnchStsCloseAntiPnchSts', 'ChargeLidAntiPnchStsOPenAntiPnchSts']}
    sig_group_dataid_dict = {}

    class FrntLeDoorRdrObj15RdrObjV:
        sig_name = "FrntLeDoorRdrObj15RdrObjV"
        sig_start_bit = 213
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
        startbit = 213
        bmuws_info = [(26, 0b00111111, 0b11000000, 6, 0), (27, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj13_UB:
        sig_name = "FrntLeDoorRdrObj13_UB"
        sig_start_bit = 355
        update_id_bit = 355
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 355
        byte = 44
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntLeDoorRdrObj14_UB:
        sig_name = "FrntLeDoorRdrObj14_UB"
        sig_start_bit = 354
        update_id_bit = 354
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 354
        byte = 44
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FrntLeDoorRdrObj15_UB:
        sig_name = "FrntLeDoorRdrObj15_UB"
        sig_start_bit = 353
        update_id_bit = 353
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 353
        byte = 44
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntLeDoorRdrObj16RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj16RdrObjDstX"
        sig_start_bit = 279
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
        startbit = 279
        bmuws_info = [(34, 0b11111111, 0b00000000, 8, 0), (35, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj11RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj11RdrObjDstZ"
        sig_start_bit = 49
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
        startbit = 49
        bmuws_info = [(6, 0b00000011, 0b11111100, 2, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj16_UB:
        sig_name = "FrntLeDoorRdrObj16_UB"
        sig_start_bit = 352
        update_id_bit = 352
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 352
        byte = 44
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntLeDoorRdrObj11RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj11RdrObjDstY"
        sig_start_bit = 71
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
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj14RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj14RdrObjDstY"
        sig_start_bit = 185
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
        startbit = 185
        bmuws_info = [(23, 0b00000011, 0b11111100, 2, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj15RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj15RdrObjDstX"
        sig_start_bit = 217
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
        startbit = 217
        bmuws_info = [(27, 0b00000011, 0b11111100, 2, 0), (28, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj16RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj16RdrObjDstY"
        sig_start_bit = 251
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
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj10RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj10RdrObjDstY"
        sig_start_bit = 17
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
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj13RdrObjV:
        sig_name = "FrntLeDoorRdrObj13RdrObjV"
        sig_start_bit = 143
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
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11110000, 0b00001111, 4, 4)]

    class FrntLeDoorRdrObj9_UB:
        sig_name = "FrntLeDoorRdrObj9_UB"
        sig_start_bit = 367
        update_id_bit = 367
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 367
        byte = 45
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntLeDoorRdrObj10_UB:
        sig_name = "FrntLeDoorRdrObj10_UB"
        sig_start_bit = 358
        update_id_bit = 358
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 358
        byte = 44
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntLeDoorRdrObj16RdrObjV:
        sig_name = "FrntLeDoorRdrObj16RdrObjV"
        sig_start_bit = 285
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
        startbit = 285
        bmuws_info = [(35, 0b00111111, 0b11000000, 6, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj11RdrObjV:
        sig_name = "FrntLeDoorRdrObj11RdrObjV"
        sig_start_bit = 45
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
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj12RdrObjV:
        sig_name = "FrntLeDoorRdrObj12RdrObjV"
        sig_start_bit = 117
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
        startbit = 117
        bmuws_info = [(14, 0b00111111, 0b11000000, 6, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj9RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj9RdrObjDstY"
        sig_start_bit = 311
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
        startbit = 311
        bmuws_info = [(38, 0b11111111, 0b00000000, 8, 0), (39, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj10RdrObjV:
        sig_name = "FrntLeDoorRdrObj10RdrObjV"
        sig_start_bit = 13
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
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj12RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj12RdrObjDstZ"
        sig_start_bit = 83
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
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj9RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj9RdrObjDstZ"
        sig_start_bit = 317
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
        startbit = 317
        bmuws_info = [(39, 0b00111111, 0b11000000, 6, 0), (40, 0b11110000, 0b00001111, 4, 4)]

    class FrntLeDoorRdrObj15RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj15RdrObjDstZ"
        sig_start_bit = 245
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
        startbit = 245
        bmuws_info = [(30, 0b00111111, 0b11000000, 6, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class FrntLeDoorRdrObj13RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj13RdrObjDstY"
        sig_start_bit = 147
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
        startbit = 147
        bmuws_info = [(18, 0b00001111, 0b11110000, 4, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj16RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj16RdrObjDstZ"
        sig_start_bit = 257
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
        startbit = 257
        bmuws_info = [(32, 0b00000011, 0b11111100, 2, 0), (33, 0b11111111, 0b00000000, 8, 0)]

    class FLIceBreakMotSts:
        sig_name = "FLIceBreakMotSts"
        sig_start_bit = 340
        update_id_bit = 345
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotSts_Inactive': 0, 'MotSts_Active': 1, 'MotSts_ResetActive': 2}
        compute_method = None
        length = 3
        startbit = 340
        byte = 42
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class FrntLeDoorRdrObj10RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj10RdrObjDstX"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj12RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj12RdrObjDstX"
        sig_start_bit = 111
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
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj14RdrObjV:
        sig_name = "FrntLeDoorRdrObj14RdrObjV"
        sig_start_bit = 175
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
        startbit = 175
        bmuws_info = [(21, 0b11111111, 0b00000000, 8, 0), (22, 0b11110000, 0b00001111, 4, 4)]

    class FrntLeDoorRdrObj11_UB:
        sig_name = "FrntLeDoorRdrObj11_UB"
        sig_start_bit = 357
        update_id_bit = 357
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 357
        byte = 44
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntLeDoorRdrObj14RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj14RdrObjDstX"
        sig_start_bit = 179
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
        startbit = 179
        bmuws_info = [(22, 0b00001111, 0b11110000, 4, 0), (23, 0b11111100, 0b00000011, 6, 2)]

    class ChargeLidAntiPnchStsCloseAntiPnchSts:
        sig_name = "ChargeLidAntiPnchStsCloseAntiPnchSts"
        sig_start_bit = 337
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
        startbit = 337
        byte = 42
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntLeDoorRdrObj12_UB:
        sig_name = "FrntLeDoorRdrObj12_UB"
        sig_start_bit = 356
        update_id_bit = 356
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 356
        byte = 44
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ChargeLidAntiPnchStsOPenAntiPnchSts:
        sig_name = "ChargeLidAntiPnchStsOPenAntiPnchSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 336
        byte = 42
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntLeDoorRdrObj14RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj14RdrObjDstZ"
        sig_start_bit = 207
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
        startbit = 207
        bmuws_info = [(25, 0b11111111, 0b00000000, 8, 0), (26, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj13RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj13RdrObjDstX"
        sig_start_bit = 121
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
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj12RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj12RdrObjDstY"
        sig_start_bit = 89
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
        startbit = 89
        bmuws_info = [(11, 0b00000011, 0b11111100, 2, 0), (12, 0b11111111, 0b00000000, 8, 0)]

    class FLRelsMotSts:
        sig_name = "FLRelsMotSts"
        sig_start_bit = 351
        update_id_bit = 359
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotSts_Inactive': 0, 'MotSts_Active': 1, 'MotSts_ResetActive': 2}
        compute_method = None
        length = 3
        startbit = 351
        byte = 43
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class FrntLeDoorRdrObj10RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj10RdrObjDstZ"
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

    class FrntLeDoorRdrObj15RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj15RdrObjDstY"
        sig_start_bit = 239
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
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11000000, 0b00111111, 2, 6)]

    class ChargeLidMoveSts:
        sig_name = "ChargeLidMoveSts"
        sig_start_bit = 343
        update_id_bit = 346
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
        startbit = 343
        byte = 42
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class FrntLeDoorRdrObj11RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj11RdrObjDstX"
        sig_start_bit = 77
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
        startbit = 77
        bmuws_info = [(9, 0b00111111, 0b11000000, 6, 0), (10, 0b11110000, 0b00001111, 4, 4)]

    class FLLtchRelsSts:
        sig_name = "FLLtchRelsSts"
        sig_start_bit = 348
        update_id_bit = 344
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
        startbit = 348
        byte = 43
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ChargeLidAntiPnchSts_UB:
        sig_name = "ChargeLidAntiPnchSts_UB"
        sig_start_bit = 347
        update_id_bit = 347
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 347
        byte = 43
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntLeDoorRdrObj9RdrObjV:
        sig_name = "FrntLeDoorRdrObj9RdrObjV"
        sig_start_bit = 323
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
        startbit = 323
        bmuws_info = [(40, 0b00001111, 0b11110000, 4, 0), (41, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj13RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj13RdrObjDstZ"
        sig_start_bit = 153
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
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FLDoorLockStsResd:
        sig_name = "FLDoorLockStsResd"
        sig_start_bit = 366
        update_id_bit = 364
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
        startbit = 366
        byte = 45
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class FrntLeDoorRdrObj9RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj9RdrObjDstX"
        sig_start_bit = 289
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
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111111, 0b00000000, 8, 0)]


class CCUMCUADPublicCANFDFr01:
    msg_name = "CCUMCUADPublicCANFDFr01"
    msg_id = 144
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "CCUMCUAD"
    rx_nodes = ['LCUL', 'CCUMCUCD', 'ETC', 'VCU']
    sig_group_dict = {'SteerWhlSnsr': ['SteerWhlSnsrAg', 'SteerWhlSnsrAgSpd', 'SteerWhlSnsrChks', 'SteerWhlSnsrCntr', 'SteerWhlSnsrQf'], 'VmcPropTqFrntReq': ['VmcPropTqFrntReqChks', 'VmcPropTqFrntReqCntr', 'VmcPropTqFrntReqGrdtNeg', 'VmcPropTqFrntReqGrdtPos', 'VmcPropTqFrntReqReq'], 'BrkMstCtrlModeReqRdnt': ['BrkMstCtrlModeReqRdntChks', 'BrkMstCtrlModeReqRdntCntr', 'BrkMstCtrlModeReqRdntReq'], 'EpbReqMst': ['EpbReqMstChks', 'EpbReqMstCntr', 'EpbReqMstEpbReq'], 'BrkSysStPrimRdnt': ['BrkSysStPrimRdntBrkSysSts', 'BrkSysStPrimRdntChks', 'BrkSysStPrimRdntCntr'], 'EpbCoornPrim': ['EpbCoornPrimApplyFunctionalitiesAvailable', 'EpbCoornPrimChks', 'EpbCoornPrimCntr', 'EpbCoornPrimDiagOperationMode', 'EpbCoornPrimDriveAwayIntention', 'EpbCoornPrimHostAvailabilityFull', 'EpbCoornPrimHostAvailabilityRelOnly', 'EpbCoornPrimPrimarySystemAvailable', 'EpbCoornPrimReserve1', 'EpbCoornPrimReserve2', 'EpbCoornPrimReserve3', 'EpbCoornPrimRollerTestBench'], 'VmcPropTqReReq': ['VmcPropTqReReqChks', 'VmcPropTqReReqCntr', 'VmcPropTqReReqGrdtNeg', 'VmcPropTqReReqGrdtPos', 'VmcPropTqReReqReq'], 'SteerInfoRef': ['SteerInfoRefChks', 'SteerInfoRefCntr', 'SteerInfoRefSteerPinionAgSpdVal', 'SteerInfoRefSteerPinionAgSpdValQf', 'SteerInfoRefSteerPinionAgVal', 'SteerInfoRefSteerPinionAgValQf', 'SteerInfoRefSteerTorqueValQf', 'SteerInfoRefSteerWhlTqVal']}
    sig_group_dataid_dict = {'SteerWhlSnsr': 1056, 'SteerInfoRef': 1037}

    class EpbCoornPrimReserve1:
        sig_name = "EpbCoornPrimReserve1"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SteerInfoRefSteerPinionAgValQf:
        sig_name = "SteerInfoRefSteerPinionAgValQf"
        sig_start_bit = 277
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
        startbit = 277
        byte = 34
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class VmcPropTqFrntReqReq:
        sig_name = "VmcPropTqFrntReqReq"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 151
        bmuws_info = [(18, 0b11111111, 0b00000000, 8, 0), (19, 0b11111111, 0b00000000, 8, 0)]

    class SteerInfoRefChks:
        sig_name = "SteerInfoRefChks"
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

    class BrkSysStPrimRdntCntr:
        sig_name = "BrkSysStPrimRdntCntr"
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

    class VseSlopAct:
        sig_name = "VseSlopAct"
        sig_start_bit = 247
        update_id_bit = 181
        sig_length = 8
        sig_value_factor = None
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

    class EpbCoornPrimReserve3:
        sig_name = "EpbCoornPrimReserve3"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VmcPropTqFrntReqCntr:
        sig_name = "VmcPropTqFrntReqCntr"
        sig_start_bit = 115
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
        startbit = 115
        byte = 14
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SteerInfoRefSteerPinionAgSpdVal:
        sig_name = "SteerInfoRefSteerPinionAgSpdVal"
        sig_start_bit = 287
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
        startbit = 287
        bmuws_info = [(35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class BrkSysStPrimRdntBrkSysSts:
        sig_name = "BrkSysStPrimRdntBrkSysSts"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotAvailable_Temporary': 0, 'NotAvailable_NotReleased': 1, 'NotAvailable_Permanent': 2, 'NotActivated_FullAvailable': 3, 'Activation_Preparation': 4, 'Activation_Pending': 5, 'Activation_PendingRedundancyLost': 6, 'Activation_PendingFailOperation': 7, 'Activated_FullAvailable': 8, 'Activated_FailOperation': 9, 'Activated_RedundancyLost': 10, 'Deactivation_Pending': 11}
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SteerWhlSnsr_UB:
        sig_name = "SteerWhlSnsr_UB"
        sig_start_bit = 168
        update_id_bit = 168
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SteerInfoRefSteerWhlTqVal:
        sig_name = "SteerInfoRefSteerWhlTqVal"
        sig_start_bit = 319
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
        startbit = 319
        bmuws_info = [(39, 0b11111111, 0b00000000, 8, 0), (40, 0b11111100, 0b00000011, 6, 2)]

    class EpbReqMstCntr:
        sig_name = "EpbReqMstCntr"
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

    class BrkMstCtrlModeReqRdntCntr:
        sig_name = "BrkMstCtrlModeReqRdntCntr"
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

    class SteerWhlSnsrAg:
        sig_name = "SteerWhlSnsrAg"
        sig_start_bit = 87
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
        startbit = 87
        bmuws_info = [(10, 0b11111111, 0b00000000, 8, 0), (11, 0b11111110, 0b00000001, 7, 1)]

    class VmcPropTqFrntReq_UB:
        sig_name = "VmcPropTqFrntReq_UB"
        sig_start_bit = 183
        update_id_bit = 183
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 183
        byte = 22
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BrkMstCtrlModeReqRdnt_UB:
        sig_name = "BrkMstCtrlModeReqRdnt_UB"
        sig_start_bit = 49
        update_id_bit = 49
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EpbReqMstEpbReq:
        sig_name = "EpbReqMstEpbReq"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbReq_Noreq': 0, 'EpbReq_RollerTestReq': 1, 'EpbReq_EmergencyApplyReq': 2, 'EpbReq_ApplyReq': 3, 'EpbReq_ReleaseReq': 4, 'EpbReq_DclBrkMechReq': 5, 'EpbReq_DARReq': 6, 'EpbReq_AAReq': 7, 'EpbReq_ApplyByExternal': 8, 'EpbReq_ReleaseByExternal': 9, 'EpbReq_BrkPadAdjust': 10, 'EpbReq_HappreparationReq': 11, 'EpbReq_EPbBackupReq': 12, 'EpbReq_ApplyByAVH': 13, 'EpbReq_ApplyByACB': 14, 'EpbReq_ReleaseBySoftSwt': 15}
        compute_method = None
        length = 4
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EpbReqMstChks:
        sig_name = "EpbReqMstChks"
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

    class SteerWhlSnsrAgSpd:
        sig_name = "SteerWhlSnsrAgSpd"
        sig_start_bit = 103
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
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111100, 0b00000011, 6, 2)]

    class SteerInfoRefSteerPinionAgSpdValQf:
        sig_name = "SteerInfoRefSteerPinionAgSpdValQf"
        sig_start_bit = 279
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
        startbit = 279
        byte = 34
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BrkSysStPrimRdntChks:
        sig_name = "BrkSysStPrimRdntChks"
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

    class EpbCoornPrimHostAvailabilityFull:
        sig_name = "EpbCoornPrimHostAvailabilityFull"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SteerWhlSnsrCntr:
        sig_name = "SteerWhlSnsrCntr"
        sig_start_bit = 119
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
        startbit = 119
        byte = 14
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VmcPropTqReReqGrdtNeg:
        sig_name = "VmcPropTqReReqGrdtNeg"
        sig_start_bit = 180
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8192
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 180
        bmuws_info = [(22, 0b00011111, 0b11100000, 5, 0), (23, 0b11111111, 0b00000000, 8, 0)]

    class EpbReqMst_UB:
        sig_name = "EpbReqMst_UB"
        sig_start_bit = 169
        update_id_bit = 169
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 169
        byte = 21
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class EpbCoornPrimApplyFunctionalitiesAvailable:
        sig_name = "EpbCoornPrimApplyFunctionalitiesAvailable"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VseVehMass:
        sig_name = "VseVehMass"
        sig_start_bit = 255
        update_id_bit = 235
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65536
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 255
        bmuws_info = [(31, 0b11111111, 0b00000000, 8, 0), (32, 0b11111111, 0b00000000, 8, 0)]

    class EpbCoornPrimReserve2:
        sig_name = "EpbCoornPrimReserve2"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EpbCoornPrimCntr:
        sig_name = "EpbCoornPrimCntr"
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

    class VmcPropTqReReqChks:
        sig_name = "VmcPropTqReReqChks"
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

    class BrkMstCtrlModeReqRdntReq:
        sig_name = "BrkMstCtrlModeReqRdntReq"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_ANP': 1, 'ModCfmd_AVP': 2, 'ModCfmd_ACC': 3, 'ModCfmd_Lcc': 4, 'ModCfmd_Reserved1': 5, 'ModCfmd_Reserved2': 6, 'ModCfmd_Reserved3': 7, 'ModCfmd_Reserved4': 8, 'ModCfmd_Reserved5': 9, 'ModCfmd_Reserved6': 10}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SteerWhlSnsrChks:
        sig_name = "SteerWhlSnsrChks"
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

    class EpbCoornPrimDiagOperationMode:
        sig_name = "EpbCoornPrimDiagOperationMode"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EpbCoornPrimChks:
        sig_name = "EpbCoornPrimChks"
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

    class VmcPropTqFrntReqChks:
        sig_name = "VmcPropTqFrntReqChks"
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

    class BrkSysStPrimRdnt_UB:
        sig_name = "BrkSysStPrimRdnt_UB"
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

    class VmcPropTqReReqCntr:
        sig_name = "VmcPropTqReReqCntr"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EpbCoornPrim_UB:
        sig_name = "EpbCoornPrim_UB"
        sig_start_bit = 170
        update_id_bit = 170
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 170
        byte = 21
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class SteerInfoRefSteerPinionAgVal:
        sig_name = "SteerInfoRefSteerPinionAgVal"
        sig_start_bit = 303
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
        startbit = 303
        bmuws_info = [(37, 0b11111111, 0b00000000, 8, 0), (38, 0b11111110, 0b00000001, 7, 1)]

    class EpbCoornPrimDriveAwayIntention:
        sig_name = "EpbCoornPrimDriveAwayIntention"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SteerInfoRefSteerTorqueValQf:
        sig_name = "SteerInfoRefSteerTorqueValQf"
        sig_start_bit = 289
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
        startbit = 289
        byte = 36
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VmcPropTqReReqReq:
        sig_name = "VmcPropTqReReqReq"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 215
        bmuws_info = [(26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0)]

    class VmcPropTqReReq_UB:
        sig_name = "VmcPropTqReReq_UB"
        sig_start_bit = 182
        update_id_bit = 182
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 182
        byte = 22
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SteerInfoRefCntr:
        sig_name = "SteerInfoRefCntr"
        sig_start_bit = 275
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
        startbit = 275
        byte = 34
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EpbCoornPrimHostAvailabilityRelOnly:
        sig_name = "EpbCoornPrimHostAvailabilityRelOnly"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BrkMstCtrlModeReqRdntChks:
        sig_name = "BrkMstCtrlModeReqRdntChks"
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

    class EpbCoornPrimPrimarySystemAvailable:
        sig_name = "EpbCoornPrimPrimarySystemAvailable"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SteerInfoRef_UB:
        sig_name = "SteerInfoRef_UB"
        sig_start_bit = 320
        update_id_bit = 320
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 320
        byte = 40
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VmcPropTqFrntReqGrdtPos:
        sig_name = "VmcPropTqFrntReqGrdtPos"
        sig_start_bit = 124
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8192
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 124
        bmuws_info = [(15, 0b00011111, 0b11100000, 5, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class VmcPropTqFrntReqGrdtNeg:
        sig_name = "VmcPropTqFrntReqGrdtNeg"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8192
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 167
        bmuws_info = [(20, 0b11111111, 0b00000000, 8, 0), (21, 0b11111000, 0b00000111, 5, 3)]

    class SteerWhlSnsrQf:
        sig_name = "SteerWhlSnsrQf"
        sig_start_bit = 105
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
        startbit = 105
        byte = 13
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VmcPropTqReReqGrdtPos:
        sig_name = "VmcPropTqReReqGrdtPos"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 4
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8192
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 199
        bmuws_info = [(24, 0b11111111, 0b00000000, 8, 0), (25, 0b11111000, 0b00000111, 5, 3)]

    class EpbCoornPrimRollerTestBench:
        sig_name = "EpbCoornPrimRollerTestBench"
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
        sig_value_table = {'CoornSt_Inactive': 0, 'CoornSt_Active': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class LCULPublicCANFDFr02:
    msg_name = "LCULPublicCANFDFr02"
    msg_id = 147
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['LCUR', 'CCUMCUCD']
    sig_group_dict = {'ReadingLiSwtSts': ['ReadingLiSwtStsFrntLeSwtSts', 'ReadingLiSwtStsFrntRiSwtSts', 'ReadingLiSwtStsSecLeSwtSts', 'ReadingLiSwtStsSecRiSwtSts', 'ReadingLiSwtStsThrdLeSwtSts', 'ReadingLiSwtStsThrdRiSwtSts']}
    sig_group_dataid_dict = {}

    class ReadingLiSwtStsThrdLeSwtSts:
        sig_name = "ReadingLiSwtStsThrdLeSwtSts"
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
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReadingLiSwtSts_UB:
        sig_name = "ReadingLiSwtSts_UB"
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

    class ReadingLiSwtStsSecRiSwtSts:
        sig_name = "ReadingLiSwtStsSecRiSwtSts"
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
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ReadingLiSwtStsThrdRiSwtSts:
        sig_name = "ReadingLiSwtStsThrdRiSwtSts"
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
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ReadingLiSwtStsFrntLeSwtSts:
        sig_name = "ReadingLiSwtStsFrntLeSwtSts"
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
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReadingLiSwtStsSecLeSwtSts:
        sig_name = "ReadingLiSwtStsSecLeSwtSts"
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
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HazardWarningSwitchSts:
        sig_name = "HazardWarningSwitchSts"
        sig_start_bit = 7
        update_id_bit = 0
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReadingLiSwtStsFrntRiSwtSts:
        sig_name = "ReadingLiSwtStsFrntRiSwtSts"
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
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class VCUPublicCANFDFr07:
    msg_name = "VCUPublicCANFDFr07"
    msg_id = 3
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class PrpsnDevelpSignalGroup4:
        sig_name = "PrpsnDevelpSignalGroup4"
        sig_start_bit = 31
        update_id_bit = 36
        sig_length = 8
        sig_value_factor = None
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

    class PrpsnDevelpSignalGroup3:
        sig_name = "PrpsnDevelpSignalGroup3"
        sig_start_bit = 23
        update_id_bit = 37
        sig_length = 8
        sig_value_factor = None
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

    class PrpsnDevelpSignalGroup2:
        sig_name = "PrpsnDevelpSignalGroup2"
        sig_start_bit = 15
        update_id_bit = 38
        sig_length = 8
        sig_value_factor = None
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

    class PrpsnDevelpSignalGroup1:
        sig_name = "PrpsnDevelpSignalGroup1"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 8
        sig_value_factor = None
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


class CCUMCUADPublicCANFDFr07:
    msg_name = "CCUMCUADPublicCANFDFr07"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.5
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['CCUMCUCD', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ADCoolgReq:
        sig_name = "ADCoolgReq"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ADActT:
        sig_name = "ADActT"
        sig_start_bit = 7
        update_id_bit = 14
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


class VCUPublicCANFDFr05:
    msg_name = "VCUPublicCANFDFr05"
    msg_id = 416
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 16
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HVBattChrgnPwrAvl:
        sig_name = "HVBattChrgnPwrAvl"
        sig_start_bit = 7
        update_id_bit = 10
        sig_length = 13
        sig_value_factor = 20
        sig_value_offset = 0
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

    class ThermMngtHVEgyCnsAllwd:
        sig_name = "ThermMngtHVEgyCnsAllwd"
        sig_start_bit = 25
        update_id_bit = 8
        sig_length = 10
        sig_value_factor = 50
        sig_value_offset = -1.0
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

    class ThermMngtHVPwrAllwd:
        sig_name = "ThermMngtHVPwrAllwd"
        sig_start_bit = 47
        update_id_bit = 26
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111000, 0b00000111, 5, 3)]

    class HvBattPackChrgnEgyCnsAllwd:
        sig_name = "HvBattPackChrgnEgyCnsAllwd"
        sig_start_bit = 23
        update_id_bit = 9
        sig_length = 13
        sig_value_factor = 20
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111000, 0b00000111, 5, 3)]


class LCURPublicCANFDFr02:
    msg_name = "LCURPublicCANFDFr02"
    msg_id = 148
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 24
    tx_node = "LCUR"
    rx_nodes = ['VCU', 'LCUL']
    sig_group_dict = {'ReadingLightThrdRowRiDrvReq': ['ReadingLightThrdRowRiDrvReqLightCmd', 'ReadingLightThrdRowRiDrvReqLiPerc', 'ReadingLightThrdRowRiDrvReqReadingLiDimsSpdCmd'], 'ReadingLightSecRowRiDrvReq': ['ReadingLightSecRowRiDrvReqLightCmd', 'ReadingLightSecRowRiDrvReqLiPerc', 'ReadingLightSecRowRiDrvReqReadingLiDimsSpdCmd'], 'ReadingLightFrntRiDrvReq': ['ReadingLightFrntRiDrvReqLightCmd', 'ReadingLightFrntRiDrvReqLiPerc', 'ReadingLightFrntRiDrvReqReadingLiDimsSpdCmd'], 'ReadingLightFrntLeDrvReq': ['ReadingLightFrntLeDrvReqLightCmd', 'ReadingLightFrntLeDrvReqLiPerc', 'ReadingLightFrntLeDrvReqReadingLiDimsSpdCmd'], 'ReadingLightThrdRowLeDrvReq': ['ReadingLightThrdRowLeDrvReqLightCmd', 'ReadingLightThrdRowLeDrvReqLiPerc', 'ReadingLightThrdRowLeDrvReqReadingLiDimsSpdCmd'], 'ReadingLightSecRowLeDrvReq': ['ReadingLightSecRowLeDrvReqLightCmd', 'ReadingLightSecRowLeDrvReqLiPerc', 'ReadingLightSecRowLeDrvReqReadingLiDimsSpdCmd']}
    sig_group_dataid_dict = {}

    class ReadingLightSecRowRiDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightSecRowRiDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 63
        byte = 7
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HoodSts:
        sig_name = "HoodSts"
        sig_start_bit = 100
        update_id_bit = 98
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
        startbit = 100
        byte = 12
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class ReadingLightThrdRowRiDrvReq_UB:
        sig_name = "ReadingLightThrdRowRiDrvReq_UB"
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

    class ReadingLightThrdRowLeDrvReqLiPerc:
        sig_name = "ReadingLightThrdRowLeDrvReqLiPerc"
        sig_start_bit = 71
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 71
        byte = 8
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLightFrntLeDrvReqLightCmd:
        sig_name = "ReadingLightFrntLeDrvReqLightCmd"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ReadingLightSecRowRiDrvReq_UB:
        sig_name = "ReadingLightSecRowRiDrvReq_UB"
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

    class ReadingLightFrntRiDrvReq_UB:
        sig_name = "ReadingLightFrntRiDrvReq_UB"
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

    class ReadingLightSecRowLeDrvReqLightCmd:
        sig_name = "ReadingLightSecRowLeDrvReqLightCmd"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ReadingLightFrntLeDrvReqLiPerc:
        sig_name = "ReadingLightFrntLeDrvReqLiPerc"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 7
        byte = 0
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLightThrdRowLeDrvReqLightCmd:
        sig_name = "ReadingLightThrdRowLeDrvReqLightCmd"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ReadingLightFrntRiDrvReqLightCmd:
        sig_name = "ReadingLightFrntRiDrvReqLightCmd"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ReadingLightFrntRiDrvReqLiPerc:
        sig_name = "ReadingLightFrntRiDrvReqLiPerc"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 31
        byte = 3
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLightThrdRowLeDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightThrdRowLeDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 75
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 75
        byte = 9
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class ReadingLightThrdRowRiDrvReqLiPerc:
        sig_name = "ReadingLightThrdRowRiDrvReqLiPerc"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 87
        byte = 10
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLightSecRowLeDrvReqLiPerc:
        sig_name = "ReadingLightSecRowLeDrvReqLiPerc"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 39
        byte = 4
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLightFrntRiDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightFrntRiDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 19
        byte = 2
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class ReadingLightFrntLeDrvReq_UB:
        sig_name = "ReadingLightFrntLeDrvReq_UB"
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

    class ReadingLightFrntLeDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightFrntLeDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 11
        byte = 1
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class ReadingLightThrdRowLeDrvReq_UB:
        sig_name = "ReadingLightThrdRowLeDrvReq_UB"
        sig_start_bit = 88
        update_id_bit = 88
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 88
        byte = 11
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReadingLightSecRowRiDrvReqLightCmd:
        sig_name = "ReadingLightSecRowRiDrvReqLightCmd"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 60
        byte = 7
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class ReadingLightThrdRowRiDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightThrdRowRiDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 91
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 91
        byte = 11
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class ReadingLightSecRowRiDrvReqLiPerc:
        sig_name = "ReadingLightSecRowRiDrvReqLiPerc"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 55
        byte = 6
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLightSecRowLeDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightSecRowLeDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 43
        byte = 5
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class ReadingLightThrdRowRiDrvReqLightCmd:
        sig_name = "ReadingLightThrdRowRiDrvReqLightCmd"
        sig_start_bit = 95
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 95
        byte = 11
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class TrSts:
        sig_name = "TrSts"
        sig_start_bit = 97
        update_id_bit = 111
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
        startbit = 97
        byte = 12
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ReadingLightSecRowLeDrvReq_UB:
        sig_name = "ReadingLightSecRowLeDrvReq_UB"
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


class CCUMCUCDPublicCANFDFr07:
    msg_name = "CCUMCUCDPublicCANFDFr07"
    msg_id = 658
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['LCUR', 'LCUL', 'ETC']
    sig_group_dict = {'ClimateTranProgsIndcr': ['ClimateTranProgsIndcrFrntLe', 'ClimateTranProgsIndcrFrntRi', 'ClimateTranProgsIndcrReLe', 'ClimateTranProgsIndcrReRi'], 'ClimateStrictAirTempSectn': ['ClimateStrictAirTempSectnFrntLe', 'ClimateStrictAirTempSectnFrntRi', 'ClimateStrictAirTempSectnReLe', 'ClimateStrictAirTempSectnReRi'], 'AntiColdFlowFlg': ['AntiColdFlowFlgFrnt', 'AntiColdFlowFlgRe'], 'ClimateBlwrActPwr': ['ClimateBlwrActPwrBoost', 'ClimateBlwrActPwrFrnt', 'ClimateBlwrActPwrRe'], 'ClimateHiAirFlwSectn': ['ClimateHiAirFlwSectnFrntLe', 'ClimateHiAirFlwSectnFrntRi', 'ClimateHiAirFlwSectnReLe', 'ClimateHiAirFlwSectnReRi'], 'SeatOccpSts': ['SeatOccpStsDrvrSeatSts', 'SeatOccpStsPassSeatSts', 'SeatOccpStsSecRowLeSeatSts', 'SeatOccpStsSecRowMidSeatSts', 'SeatOccpStsSecRowRiSeatSts', 'SeatOccpStsThrdRowLeSeatSts', 'SeatOccpStsThrdRowMidSeatSts', 'SeatOccpStsThrdRowRiSeatSts'], 'CoolAirActRat': ['CoolAirActRatFrntLe', 'CoolAirActRatFrntRi', 'CoolAirActRatReLe', 'CoolAirActRatReRi'], 'CoolAirTarRat': ['CoolAirTarRatFrntLe', 'CoolAirTarRatFrntRi', 'CoolAirTarRatReLe', 'CoolAirTarRatReRi'], 'ClimateTSoak': ['ClimateTSoakFrntLe', 'ClimateTSoakFrntRi', 'ClimateTSoakReLe', 'ClimateTSoakReRi']}
    sig_group_dataid_dict = {}

    class SeatOccpStsSecRowLeSeatSts:
        sig_name = "SeatOccpStsSecRowLeSeatSts"
        sig_start_bit = 317
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
        startbit = 317
        byte = 39
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ClimateTranProgsIndcr_UB:
        sig_name = "ClimateTranProgsIndcr_UB"
        sig_start_bit = 320
        update_id_bit = 320
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 320
        byte = 40
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ClimateTSoakReRi:
        sig_name = "ClimateTSoakReRi"
        sig_start_bit = 124
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
        startbit = 124
        bmuws_info = [(15, 0b00011111, 0b11100000, 5, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class ClimateHiAirFlwSectnReLe:
        sig_name = "ClimateHiAirFlwSectnReLe"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class ClimateStrictAirTempSectn_UB:
        sig_name = "ClimateStrictAirTempSectn_UB"
        sig_start_bit = 321
        update_id_bit = 321
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 321
        byte = 40
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ClimateTranProgsIndcrReLe:
        sig_name = "ClimateTranProgsIndcrReLe"
        sig_start_bit = 107
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 107
        bmuws_info = [(13, 0b00001111, 0b11110000, 4, 0), (14, 0b11100000, 0b00011111, 3, 5)]

    class ClimateTSoakFrntRi:
        sig_name = "ClimateTSoakFrntRi"
        sig_start_bit = 146
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
        startbit = 146
        bmuws_info = [(18, 0b00000111, 0b11111000, 3, 0), (19, 0b11111111, 0b00000000, 8, 0), (20, 0b11000000, 0b00111111, 2, 6)]

    class ClimateTranProgsIndcrFrntLe:
        sig_name = "ClimateTranProgsIndcrFrntLe"
        sig_start_bit = 89
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 89
        bmuws_info = [(11, 0b00000011, 0b11111100, 2, 0), (12, 0b11111000, 0b00000111, 5, 3)]

    class ThermSysCmptErrInd:
        sig_name = "ThermSysCmptErrInd"
        sig_start_bit = 271
        update_id_bit = 338
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
        startbit = 271
        bmuws_info = [(33, 0b11111111, 0b00000000, 8, 0), (34, 0b11111111, 0b00000000, 8, 0), (35, 0b11111111, 0b00000000, 8, 0), (36, 0b11111111, 0b00000000, 8, 0)]

    class CoolAirActRatFrntLe:
        sig_name = "CoolAirActRatFrntLe"
        sig_start_bit = 202
        update_id_bit = None
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
        startbit = 202
        bmuws_info = [(25, 0b00000111, 0b11111000, 3, 0), (26, 0b11111110, 0b00000001, 7, 1)]

    class ClimateTSoakFrntLe:
        sig_name = "ClimateTSoakFrntLe"
        sig_start_bit = 165
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
        startbit = 165
        bmuws_info = [(20, 0b00111111, 0b11000000, 6, 0), (21, 0b11111110, 0b00000001, 7, 1)]

    class SteerSysInin:
        sig_name = "SteerSysInin"
        sig_start_bit = 327
        update_id_bit = 341
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
        startbit = 327
        byte = 40
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DiagcComActv:
        sig_name = "DiagcComActv"
        sig_start_bit = 259
        update_id_bit = 331
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
        startbit = 259
        byte = 32
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ClimateStrictAirTempSectnReLe:
        sig_name = "ClimateStrictAirTempSectnReLe"
        sig_start_bit = 80
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 80
        bmuws_info = [(10, 0b00000001, 0b11111110, 1, 0), (11, 0b11111100, 0b00000011, 6, 2)]

    class FrntBlwrAftRunSts:
        sig_name = "FrntBlwrAftRunSts"
        sig_start_bit = 258
        update_id_bit = 328
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
        startbit = 258
        byte = 32
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ClimateStrictAirTempSectnReRi:
        sig_name = "ClimateStrictAirTempSectnReRi"
        sig_start_bit = 69
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 69
        bmuws_info = [(8, 0b00111111, 0b11000000, 6, 0), (9, 0b10000000, 0b01111111, 1, 7)]

    class ClimateHiAirFlwSectnFrntRi:
        sig_name = "ClimateHiAirFlwSectnFrntRi"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 42
        bmuws_info = [(5, 0b00000111, 0b11111000, 3, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class SeatOccpStsThrdRowRiSeatSts:
        sig_name = "SeatOccpStsThrdRowRiSeatSts"
        sig_start_bit = 312
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
        startbit = 312
        byte = 39
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AntiColdFlowFlg_UB:
        sig_name = "AntiColdFlowFlg_UB"
        sig_start_bit = 325
        update_id_bit = 325
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 325
        byte = 40
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SeatOccpStsPassSeatSts:
        sig_name = "SeatOccpStsPassSeatSts"
        sig_start_bit = 318
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
        startbit = 318
        byte = 39
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ClimateBlwrActPwr_UB:
        sig_name = "ClimateBlwrActPwr_UB"
        sig_start_bit = 323
        update_id_bit = 323
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 323
        byte = 40
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ClimateHiAirFlwSectn_UB:
        sig_name = "ClimateHiAirFlwSectn_UB"
        sig_start_bit = 322
        update_id_bit = 322
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 322
        byte = 40
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CoolAirTarRatFrntRi:
        sig_name = "CoolAirTarRatFrntRi"
        sig_start_bit = 230
        update_id_bit = None
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
        startbit = 230
        bmuws_info = [(28, 0b01111111, 0b10000000, 7, 0), (29, 0b11100000, 0b00011111, 3, 5)]

    class ClimateTSoakReLe:
        sig_name = "ClimateTSoakReLe"
        sig_start_bit = 143
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
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11111000, 0b00000111, 5, 3)]

    class ClimateTranProgsIndcrFrntRi:
        sig_name = "ClimateTranProgsIndcrFrntRi"
        sig_start_bit = 98
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 98
        bmuws_info = [(12, 0b00000111, 0b11111000, 3, 0), (13, 0b11110000, 0b00001111, 4, 4)]

    class DiagcExtCom:
        sig_name = "DiagcExtCom"
        sig_start_bit = 248
        update_id_bit = 330
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
        startbit = 248
        byte = 31
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SeatOccpStsThrdRowMidSeatSts:
        sig_name = "SeatOccpStsThrdRowMidSeatSts"
        sig_start_bit = 313
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
        startbit = 313
        byte = 39
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class SeatOccpSts_UB:
        sig_name = "SeatOccpSts_UB"
        sig_start_bit = 342
        update_id_bit = 342
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 342
        byte = 42
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ClimateBlwrActPwrRe:
        sig_name = "ClimateBlwrActPwrRe"
        sig_start_bit = 21
        update_id_bit = None
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
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class CoolAirActRatReLe:
        sig_name = "CoolAirActRatReLe"
        sig_start_bit = 190
        update_id_bit = None
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
        startbit = 190
        bmuws_info = [(23, 0b01111111, 0b10000000, 7, 0), (24, 0b11100000, 0b00011111, 3, 5)]

    class CoolAirTarRatReLe:
        sig_name = "CoolAirTarRatReLe"
        sig_start_bit = 242
        update_id_bit = None
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
        startbit = 242
        bmuws_info = [(30, 0b00000111, 0b11111000, 3, 0), (31, 0b11111110, 0b00000001, 7, 1)]

    class ClimateTranProgsIndcrReRi:
        sig_name = "ClimateTranProgsIndcrReRi"
        sig_start_bit = 116
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 116
        bmuws_info = [(14, 0b00011111, 0b11100000, 5, 0), (15, 0b11000000, 0b00111111, 2, 6)]

    class SeatOccpStsThrdRowLeSeatSts:
        sig_name = "SeatOccpStsThrdRowLeSeatSts"
        sig_start_bit = 314
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
        startbit = 314
        byte = 39
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ClimateStrictAirTempSectnFrntLe:
        sig_name = "ClimateStrictAirTempSectnFrntLe"
        sig_start_bit = 78
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 78
        byte = 9
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CoolAirTarRatReRi:
        sig_name = "CoolAirTarRatReRi"
        sig_start_bit = 208
        update_id_bit = None
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
        startbit = 208
        bmuws_info = [(26, 0b00000001, 0b11111110, 1, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b10000000, 0b01111111, 1, 7)]

    class ClimateTrfFlg:
        sig_name = "ClimateTrfFlg"
        sig_start_bit = 125
        update_id_bit = 335
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
        startbit = 125
        byte = 15
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DrvrInCarSts:
        sig_name = "DrvrInCarSts"
        sig_start_bit = 263
        update_id_bit = 329
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
        startbit = 263
        byte = 32
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AntiColdFlowFlgFrnt:
        sig_name = "AntiColdFlowFlgFrnt"
        sig_start_bit = 262
        update_id_bit = None
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
        startbit = 262
        byte = 32
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntBlwrLvlSts:
        sig_name = "FrntBlwrLvlSts"
        sig_start_bit = 307
        update_id_bit = 343
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
        startbit = 307
        byte = 38
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ClimateHiAirFlwSectnFrntLe:
        sig_name = "ClimateHiAirFlwSectnFrntLe"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 60
        bmuws_info = [(7, 0b00011111, 0b11100000, 5, 0), (8, 0b11000000, 0b00111111, 2, 6)]

    class ClimateBlwrActPwrBoost:
        sig_name = "ClimateBlwrActPwrBoost"
        sig_start_bit = 15
        update_id_bit = None
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
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11000000, 0b00111111, 2, 6)]

    class CoolAirActRat_UB:
        sig_name = "CoolAirActRat_UB"
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

    class SeatOccpStsDrvrSeatSts:
        sig_name = "SeatOccpStsDrvrSeatSts"
        sig_start_bit = 319
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
        startbit = 319
        byte = 39
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ThermSysProtnInd:
        sig_name = "ThermSysProtnInd"
        sig_start_bit = 351
        update_id_bit = 337
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
        startbit = 351
        bmuws_info = [(43, 0b11111111, 0b00000000, 8, 0), (44, 0b11111111, 0b00000000, 8, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11111111, 0b00000000, 8, 0)]

    class CoolAirTarRatFrntLe:
        sig_name = "CoolAirTarRatFrntLe"
        sig_start_bit = 236
        update_id_bit = None
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
        startbit = 236
        bmuws_info = [(29, 0b00011111, 0b11100000, 5, 0), (30, 0b11111000, 0b00000111, 5, 3)]

    class AntiFlashFogFlg:
        sig_name = "AntiFlashFogFlg"
        sig_start_bit = 260
        update_id_bit = 324
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
        startbit = 260
        byte = 32
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ThermFctReq:
        sig_name = "ThermFctReq"
        sig_start_bit = 326
        update_id_bit = 340
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
        startbit = 326
        byte = 40
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SeatOccpStsSecRowRiSeatSts:
        sig_name = "SeatOccpStsSecRowRiSeatSts"
        sig_start_bit = 315
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
        startbit = 315
        byte = 39
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CoolAirTarRat_UB:
        sig_name = "CoolAirTarRat_UB"
        sig_start_bit = 332
        update_id_bit = 332
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 332
        byte = 41
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WakeupADReq:
        sig_name = "WakeupADReq"
        sig_start_bit = 257
        update_id_bit = 336
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
        startbit = 257
        byte = 32
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CoolAirActRatReRi:
        sig_name = "CoolAirActRatReRi"
        sig_start_bit = 196
        update_id_bit = None
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
        startbit = 196
        bmuws_info = [(24, 0b00011111, 0b11100000, 5, 0), (25, 0b11111000, 0b00000111, 5, 3)]

    class ClimateBlwrActPwrFrnt:
        sig_name = "ClimateBlwrActPwrFrnt"
        sig_start_bit = 27
        update_id_bit = None
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
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11111100, 0b00000011, 6, 2)]

    class ThermMngtLVPwrCns:
        sig_name = "ThermMngtLVPwrCns"
        sig_start_bit = 303
        update_id_bit = 339
        sig_length = 12
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 3000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 303
        bmuws_info = [(37, 0b11111111, 0b00000000, 8, 0), (38, 0b11110000, 0b00001111, 4, 4)]

    class CoolAirActRatFrntRi:
        sig_name = "CoolAirActRatFrntRi"
        sig_start_bit = 168
        update_id_bit = None
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
        startbit = 168
        bmuws_info = [(21, 0b00000001, 0b11111110, 1, 0), (22, 0b11111111, 0b00000000, 8, 0), (23, 0b10000000, 0b01111111, 1, 7)]

    class ClimateTSoak_UB:
        sig_name = "ClimateTSoak_UB"
        sig_start_bit = 334
        update_id_bit = 334
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 334
        byte = 41
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SeatOccpStsSecRowMidSeatSts:
        sig_name = "SeatOccpStsSecRowMidSeatSts"
        sig_start_bit = 316
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
        startbit = 316
        byte = 39
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ClimateHiAirFlwSectnReRi:
        sig_name = "ClimateHiAirFlwSectnReRi"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11100000, 0b00011111, 3, 5)]

    class AntiColdFlowFlgRe:
        sig_name = "AntiColdFlowFlgRe"
        sig_start_bit = 261
        update_id_bit = None
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
        startbit = 261
        byte = 32
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ClimateStrictAirTempSectnFrntRi:
        sig_name = "ClimateStrictAirTempSectnFrntRi"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 87
        byte = 10
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1


class LCULPublicCANFDFr09:
    msg_name = "LCULPublicCANFDFr09"
    msg_id = 770
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DrvrSeatOccpSnsrRawSts:
        sig_name = "DrvrSeatOccpSnsrRawSts"
        sig_start_bit = 7
        update_id_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OccptSnsrOutpSts_Empty': 0, 'OccptSnsrOutpSts_L1': 1, 'OccptSnsrOutpSts_L2': 2, 'OccptSnsrOutpSts_L3': 3, 'OccptSnsrOutpSts_L4': 4, 'OccptSnsrOutpSts_Occupied': 5, 'OccptSnsrOutpSts_Unknown': 6}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DrvrSeatOccpSnsrOKSts:
        sig_name = "DrvrSeatOccpSnsrOKSts"
        sig_start_bit = 12
        update_id_bit = 28
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class LCURPublicCANFDFr08:
    msg_name = "LCURPublicCANFDFr08"
    msg_id = 662
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['VCU', 'CCUMCUCD']
    sig_group_dict = {'TrErrFb': ['TrErrFbCinchErrFb', 'TrErrFbCinchMotThermErrFb', 'TrErrFbHalfClsErrFb', 'TrErrFbRelsgErrFb', 'TrErrFbRelsMotThermErrFb', 'TrErrFbSpindleMotThermErrFb'], 'TERVSts': ['TERVStsExvBlkErr', 'TERVStsExvCalSts', 'TERVStsExvElecErr', 'TERVStsExvMoveSts', 'TERVStsExvOvrTempErr', 'TERVStsExvOvrTrvlErr', 'TERVStsExvPosnAct', 'TERVStsExvURangErr', 'TERVStsPreHeatgSts'], 'FRPwrDoorErrFb': ['FRPwrDoorErrFbBoolean', 'FRPwrDoorErrFbHallErrFb', 'FRPwrDoorErrFbMotThermErrFb', 'FRPwrDoorErrFbPosnUnknowFb', 'FRPwrDoorErrFbRollAngErrFb'], 'BEXVSts': ['BEXVStsExvBlkErr', 'BEXVStsExvCalSts', 'BEXVStsExvElecErr', 'BEXVStsExvMoveSts', 'BEXVStsExvOvrTempErr', 'BEXVStsExvOvrTrvlErr', 'BEXVStsExvPosnAct', 'BEXVStsExvURangErr', 'BEXVStsPreHeatgSts'], 'CERVSts': ['CERVStsExvBlkErr', 'CERVStsExvCalSts', 'CERVStsExvElecErr', 'CERVStsExvMoveSts', 'CERVStsExvOvrTempErr', 'CERVStsExvOvrTrvlErr', 'CERVStsExvPosnAct', 'CERVStsExvURangErr', 'CERVStsPreHeatgSts'], 'GrlShttrSts': ['GrlShttrStsShttrActrFlt', 'GrlShttrStsShttrBlkSts', 'GrlShttrStsShttrCalActv', 'GrlShttrStsShttrCalIndcd', 'GrlShttrStsShttrElecErr', 'GrlShttrStsShttrOvrTempErr', 'GrlShttrStsShttrPosnFb', 'GrlShttrStsShttrSnsrFlt', 'GrlShttrStsShttrULoErr'], 'RRPwrDoorErrFb': ['RRPwrDoorErrFbBoolean', 'RRPwrDoorErrFbHallErrFb', 'RRPwrDoorErrFbMotThermErrFb', 'RRPwrDoorErrFbPosnUnknowFb', 'RRPwrDoorErrFbRollAngErrFb'], 'FRLtchErrFb': ['FRLtchErrFbCinchErrFb', 'FRLtchErrFbCinchMotThermErrFb', 'FRLtchErrFbHalfClsErrFb', 'FRLtchErrFbRelsgErrFb', 'FRLtchErrFbRelsMotThermErrFb'], 'CmptmtAirFlwEstimd': ['CmptmtAirFlwEstimdFrnt', 'CmptmtAirFlwEstimdRe'], 'REXVSts': ['REXVStsExvBlkErr', 'REXVStsExvCalSts', 'REXVStsExvElecErr', 'REXVStsExvMoveSts', 'REXVStsExvOvrTempErr', 'REXVStsExvOvrTrvlErr', 'REXVStsExvPosnAct', 'REXVStsExvURangErr', 'REXVStsPreHeatgSts'], 'WERVSts': ['WERVStsExvBlkErr', 'WERVStsExvCalSts', 'WERVStsExvElecErr', 'WERVStsExvMoveSts', 'WERVStsExvOvrTempErr', 'WERVStsExvOvrTrvlErr', 'WERVStsExvPosnAct', 'WERVStsExvURangErr', 'WERVStsPreHeatgSts'], 'RRLtchErrFb': ['RRLtchErrFbCinchErrFb', 'RRLtchErrFbCinchMotThermErrFb', 'RRLtchErrFbHalfClsErrFb', 'RRLtchErrFbRelsgErrFb', 'RRLtchErrFbRelsMotThermErrFb'], 'EEXVSts': ['EEXVStsExvBlkErr', 'EEXVStsExvCalSts', 'EEXVStsExvElecErr', 'EEXVStsExvMoveSts', 'EEXVStsExvOvrTempErr', 'EEXVStsExvOvrTrvlErr', 'EEXVStsExvPosnAct', 'EEXVStsExvURangErr', 'EEXVStsPreHeatgSts']}
    sig_group_dataid_dict = {}

    class EEXVStsExvOvrTrvlErr:
        sig_name = "EEXVStsExvOvrTrvlErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 91
        byte = 11
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WERVStsExvPosnAct:
        sig_name = "WERVStsExvPosnAct"
        sig_start_bit = 215
        update_id_bit = None
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
        startbit = 215
        bmuws_info = [(26, 0b11111111, 0b00000000, 8, 0), (27, 0b11000000, 0b00111111, 2, 6)]

    class TrErrFb_UB:
        sig_name = "TrErrFb_UB"
        sig_start_bit = 236
        update_id_bit = 236
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 236
        byte = 29
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class TERVStsExvMoveSts:
        sig_name = "TERVStsExvMoveSts"
        sig_start_bit = 203
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 203
        byte = 25
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GrlShttrStsShttrCalIndcd:
        sig_name = "GrlShttrStsShttrCalIndcd"
        sig_start_bit = 269
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrCalIndcd_ShttrCalNotIndcd': 0, 'ShttrCalIndcd_ShttrCalIndcd': 1}
        compute_method = None
        length = 1
        startbit = 269
        byte = 33
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class TERVSts_UB:
        sig_name = "TERVSts_UB"
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

    class HVECmprPwrCns:
        sig_name = "HVECmprPwrCns"
        sig_start_bit = 233
        update_id_bit = 252
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 233
        bmuws_info = [(29, 0b00000011, 0b11111100, 2, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11100000, 0b00011111, 3, 5)]

    class REXVStsExvCalSts:
        sig_name = "REXVStsExvCalSts"
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
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 117
        byte = 14
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FRPwrDoorErrFb_UB:
        sig_name = "FRPwrDoorErrFb_UB"
        sig_start_bit = 251
        update_id_bit = 251
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 251
        byte = 31
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BEXVSts_UB:
        sig_name = "BEXVSts_UB"
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

    class RRPwrDoorErrFbHallErrFb:
        sig_name = "RRPwrDoorErrFbHallErrFb"
        sig_start_bit = 182
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
        startbit = 182
        byte = 22
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class REXVStsExvElecErr:
        sig_name = "REXVStsExvElecErr"
        sig_start_bit = 114
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 114
        byte = 14
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class CERVStsExvBlkErr:
        sig_name = "CERVStsExvBlkErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CERVSts_UB:
        sig_name = "CERVSts_UB"
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

    class WERVStsExvURangErr:
        sig_name = "WERVStsExvURangErr"
        sig_start_bit = 227
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 227
        byte = 28
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class REXVStsExvMoveSts:
        sig_name = "REXVStsExvMoveSts"
        sig_start_bit = 123
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 123
        byte = 15
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CERVStsExvPosnAct:
        sig_name = "CERVStsExvPosnAct"
        sig_start_bit = 39
        update_id_bit = None
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class TERVStsExvElecErr:
        sig_name = "TERVStsExvElecErr"
        sig_start_bit = 178
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 178
        byte = 22
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class RRPwrDoorErrFbPosnUnknowFb:
        sig_name = "RRPwrDoorErrFbPosnUnknowFb"
        sig_start_bit = 179
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
        startbit = 179
        byte = 22
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EEXVStsExvCalSts:
        sig_name = "EEXVStsExvCalSts"
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
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 95
        byte = 11
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TrErrFbRelsMotThermErrFb:
        sig_name = "TrErrFbRelsMotThermErrFb"
        sig_start_bit = 147
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
        startbit = 147
        byte = 18
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GrlShttrSts_UB:
        sig_name = "GrlShttrSts_UB"
        sig_start_bit = 275
        update_id_bit = 275
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 275
        byte = 34
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RRPwrDoorErrFb_UB:
        sig_name = "RRPwrDoorErrFb_UB"
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

    class GrlShttrStsShttrCalActv:
        sig_name = "GrlShttrStsShttrCalActv"
        sig_start_bit = 270
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrCalActv_NotActv': 0, 'ShttrCalActv_Actv': 1}
        compute_method = None
        length = 1
        startbit = 270
        byte = 33
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class TrErrFbHalfClsErrFb:
        sig_name = "TrErrFbHalfClsErrFb"
        sig_start_bit = 150
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
        startbit = 150
        byte = 18
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class GrlShttrStsShttrULoErr:
        sig_name = "GrlShttrStsShttrULoErr"
        sig_start_bit = 268
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 268
        byte = 33
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class FRLtchErrFb_UB:
        sig_name = "FRLtchErrFb_UB"
        sig_start_bit = 109
        update_id_bit = 109
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 109
        byte = 13
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CERVStsExvCalSts:
        sig_name = "CERVStsExvCalSts"
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
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WERVStsPreHeatgSts:
        sig_name = "WERVStsPreHeatgSts"
        sig_start_bit = 225
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
        startbit = 225
        byte = 28
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FRPwrDoorErrFbMotThermErrFb:
        sig_name = "FRPwrDoorErrFbMotThermErrFb"
        sig_start_bit = 75
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
        startbit = 75
        byte = 9
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TrErrFbRelsgErrFb:
        sig_name = "TrErrFbRelsgErrFb"
        sig_start_bit = 149
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
        startbit = 149
        byte = 18
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BEXVStsExvURangErr:
        sig_name = "BEXVStsExvURangErr"
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
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TERVStsPreHeatgSts:
        sig_name = "TERVStsPreHeatgSts"
        sig_start_bit = 202
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
        startbit = 202
        byte = 25
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RRLtchErrFbRelsMotThermErrFb:
        sig_name = "RRLtchErrFbRelsMotThermErrFb"
        sig_start_bit = 137
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
        startbit = 137
        byte = 17
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RRLtchErrFbCinchErrFb:
        sig_name = "RRLtchErrFbCinchErrFb"
        sig_start_bit = 140
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
        startbit = 140
        byte = 17
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RRLtchErrFbCinchMotThermErrFb:
        sig_name = "RRLtchErrFbCinchMotThermErrFb"
        sig_start_bit = 138
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
        startbit = 138
        byte = 17
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class REXVStsExvPosnAct:
        sig_name = "REXVStsExvPosnAct"
        sig_start_bit = 134
        update_id_bit = None
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
        startbit = 134
        bmuws_info = [(16, 0b01111111, 0b10000000, 7, 0), (17, 0b11100000, 0b00011111, 3, 5)]

    class BEXVStsExvBlkErr:
        sig_name = "BEXVStsExvBlkErr"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class RRDoorModSts:
        sig_name = "RRDoorModSts"
        sig_start_bit = 119
        update_id_bit = 224
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
        startbit = 119
        byte = 14
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TrErrFbCinchMotThermErrFb:
        sig_name = "TrErrFbCinchMotThermErrFb"
        sig_start_bit = 151
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
        startbit = 151
        byte = 18
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CERVStsExvElecErr:
        sig_name = "CERVStsExvElecErr"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 44
        byte = 5
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class EEXVStsExvOvrTempErr:
        sig_name = "EEXVStsExvOvrTempErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 83
        byte = 10
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class GrlShttrStsShttrOvrTempErr:
        sig_name = "GrlShttrStsShttrOvrTempErr"
        sig_start_bit = 259
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 259
        byte = 32
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CERVStsPreHeatgSts:
        sig_name = "CERVStsPreHeatgSts"
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

    class REXVStsExvOvrTempErr:
        sig_name = "REXVStsExvOvrTempErr"
        sig_start_bit = 122
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 122
        byte = 15
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class FRPwrDoorErrFbBoolean:
        sig_name = "FRPwrDoorErrFbBoolean"
        sig_start_bit = 77
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
        startbit = 77
        byte = 9
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BEXVStsExvMoveSts:
        sig_name = "BEXVStsExvMoveSts"
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
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CmptmtAirFlwEstimdFrnt:
        sig_name = "CmptmtAirFlwEstimdFrnt"
        sig_start_bit = 71
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
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11000000, 0b00111111, 2, 6)]

    class FRPwrDoorErrFbRollAngErrFb:
        sig_name = "FRPwrDoorErrFbRollAngErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 73
        byte = 9
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class WERVStsExvOvrTrvlErr:
        sig_name = "WERVStsExvOvrTrvlErr"
        sig_start_bit = 229
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 229
        byte = 28
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RRLtchErrFbHalfClsErrFb:
        sig_name = "RRLtchErrFbHalfClsErrFb"
        sig_start_bit = 136
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
        startbit = 136
        byte = 17
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class TrErrFbSpindleMotThermErrFb:
        sig_name = "TrErrFbSpindleMotThermErrFb"
        sig_start_bit = 146
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
        startbit = 146
        byte = 18
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CmptmtAirFlwEstimdRe:
        sig_name = "CmptmtAirFlwEstimdRe"
        sig_start_bit = 49
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
        startbit = 49
        bmuws_info = [(6, 0b00000011, 0b11111100, 2, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class TrErrFbCinchErrFb:
        sig_name = "TrErrFbCinchErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 148
        byte = 18
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BEXVStsExvElecErr:
        sig_name = "BEXVStsExvElecErr"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class BEXVStsExvCalSts:
        sig_name = "BEXVStsExvCalSts"
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
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class EEXVStsPreHeatgSts:
        sig_name = "EEXVStsPreHeatgSts"
        sig_start_bit = 72
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
        startbit = 72
        byte = 9
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class GrlShttrStsShttrBlkSts:
        sig_name = "GrlShttrStsShttrBlkSts"
        sig_start_bit = 271
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrBlkd_ShttrNotBlkd': 0, 'ShttrBlkd_ShttrBlkd': 1}
        compute_method = None
        length = 1
        startbit = 271
        byte = 33
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FRLtchErrFbCinchErrFb:
        sig_name = "FRLtchErrFbCinchErrFb"
        sig_start_bit = 105
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
        startbit = 105
        byte = 13
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class TERVStsExvCalSts:
        sig_name = "TERVStsExvCalSts"
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
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 195
        byte = 24
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WERVStsExvOvrTempErr:
        sig_name = "WERVStsExvOvrTempErr"
        sig_start_bit = 231
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 231
        byte = 28
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class GrlShttrStsShttrElecErr:
        sig_name = "GrlShttrStsShttrElecErr"
        sig_start_bit = 261
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 261
        byte = 32
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BEXVStsPreHeatgSts:
        sig_name = "BEXVStsPreHeatgSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CERVStsExvMoveSts:
        sig_name = "CERVStsExvMoveSts"
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
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EEXVStsExvURangErr:
        sig_name = "EEXVStsExvURangErr"
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
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 93
        byte = 11
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TERVStsExvPosnAct:
        sig_name = "TERVStsExvPosnAct"
        sig_start_bit = 191
        update_id_bit = None
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
        startbit = 191
        bmuws_info = [(23, 0b11111111, 0b00000000, 8, 0), (24, 0b11000000, 0b00111111, 2, 6)]

    class TERVStsExvBlkErr:
        sig_name = "TERVStsExvBlkErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 197
        byte = 24
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RRDoorMaxPosnSetFb:
        sig_name = "RRDoorMaxPosnSetFb"
        sig_start_bit = 175
        update_id_bit = 144
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

    class CmptmtAirFlwEstimd_UB:
        sig_name = "CmptmtAirFlwEstimd_UB"
        sig_start_bit = 111
        update_id_bit = 111
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 111
        byte = 13
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FRLtchErrFbRelsMotThermErrFb:
        sig_name = "FRLtchErrFbRelsMotThermErrFb"
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

    class RRLtchErrFbRelsgErrFb:
        sig_name = "RRLtchErrFbRelsgErrFb"
        sig_start_bit = 139
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
        startbit = 139
        byte = 17
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TERVStsExvURangErr:
        sig_name = "TERVStsExvURangErr"
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
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 205
        byte = 25
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WERVStsExvMoveSts:
        sig_name = "WERVStsExvMoveSts"
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
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 216
        byte = 27
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class GrlShttrStsShttrSnsrFlt:
        sig_name = "GrlShttrStsShttrSnsrFlt"
        sig_start_bit = 257
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 257
        byte = 32
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FRPwrDoorErrFbHallErrFb:
        sig_name = "FRPwrDoorErrFbHallErrFb"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 76
        byte = 9
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WERVStsExvCalSts:
        sig_name = "WERVStsExvCalSts"
        sig_start_bit = 221
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvCalibSts_NotInitialized': 0, 'ExvCalibSts_InitializationInProcess': 1, 'ExvCalibSts_Initialized': 2, 'ExvCalibSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 221
        byte = 27
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FRLtchErrFbCinchMotThermErrFb:
        sig_name = "FRLtchErrFbCinchMotThermErrFb"
        sig_start_bit = 106
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
        startbit = 106
        byte = 13
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class GrlShttrStsShttrActrFlt:
        sig_name = "GrlShttrStsShttrActrFlt"
        sig_start_bit = 263
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 263
        byte = 32
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class REXVStsExvBlkErr:
        sig_name = "REXVStsExvBlkErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 127
        byte = 15
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TERVStsExvOvrTempErr:
        sig_name = "TERVStsExvOvrTempErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 193
        byte = 24
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TrMaxPosnSetFB:
        sig_name = "TrMaxPosnSetFB"
        sig_start_bit = 159
        update_id_bit = 235
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
        startbit = 159
        byte = 19
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FRLtchErrFbRelsgErrFb:
        sig_name = "FRLtchErrFbRelsgErrFb"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GrlShttrStsShttrPosnFb:
        sig_name = "GrlShttrStsShttrPosnFb"
        sig_start_bit = 266
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 266
        bmuws_info = [(33, 0b00000111, 0b11111000, 3, 0), (34, 0b11110000, 0b00001111, 4, 4)]

    class BEXVStsExvOvrTrvlErr:
        sig_name = "BEXVStsExvOvrTrvlErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EEXVStsExvMoveSts:
        sig_name = "EEXVStsExvMoveSts"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvMovSts_NotMove': 0, 'ExvMovSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 87
        byte = 10
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BEXVStsExvPosnAct:
        sig_name = "BEXVStsExvPosnAct"
        sig_start_bit = 7
        update_id_bit = None
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class RRPwrDoorErrFbBoolean:
        sig_name = "RRPwrDoorErrFbBoolean"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CmprSpdAct:
        sig_name = "CmprSpdAct"
        sig_start_bit = 167
        update_id_bit = 50
        sig_length = 8
        sig_value_factor = 50
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

    class EEXVStsExvPosnAct:
        sig_name = "EEXVStsExvPosnAct"
        sig_start_bit = 89
        update_id_bit = None
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
        startbit = 89
        bmuws_info = [(11, 0b00000011, 0b11111100, 2, 0), (12, 0b11111111, 0b00000000, 8, 0)]

    class EEXVStsExvBlkErr:
        sig_name = "EEXVStsExvBlkErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 81
        byte = 10
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class REXVStsPreHeatgSts:
        sig_name = "REXVStsPreHeatgSts"
        sig_start_bit = 115
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
        startbit = 115
        byte = 14
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class REXVSts_UB:
        sig_name = "REXVSts_UB"
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

    class RRPwrDoorErrFbRollAngErrFb:
        sig_name = "RRPwrDoorErrFbRollAngErrFb"
        sig_start_bit = 180
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
        startbit = 180
        byte = 22
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FRPwrDoorErrFbPosnUnknowFb:
        sig_name = "FRPwrDoorErrFbPosnUnknowFb"
        sig_start_bit = 74
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
        startbit = 74
        byte = 9
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class WERVSts_UB:
        sig_name = "WERVSts_UB"
        sig_start_bit = 234
        update_id_bit = 234
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 234
        byte = 29
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CERVStsExvURangErr:
        sig_name = "CERVStsExvURangErr"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class CERVStsExvOvrTempErr:
        sig_name = "CERVStsExvOvrTempErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class EEXVStsExvElecErr:
        sig_name = "EEXVStsExvElecErr"
        sig_start_bit = 86
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 86
        byte = 10
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class REXVStsExvURangErr:
        sig_name = "REXVStsExvURangErr"
        sig_start_bit = 120
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvVoltgRangErr_NoErr': 0, 'ExvVoltgRangErr_UnderVoltageErr': 1, 'ExvVoltgRangErr_OverVoltageErr': 2, 'ExvVoltgRangErr_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 120
        bmuws_info = [(15, 0b00000001, 0b11111110, 1, 0), (16, 0b10000000, 0b01111111, 1, 7)]

    class WERVStsExvElecErr:
        sig_name = "WERVStsExvElecErr"
        sig_start_bit = 219
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ExvElecStsErr_NoError': 0, 'ExvElecStsErr_OpenCircuit': 1, 'ExvElecStsErr_ShortCircuit': 2, 'ExvElecStsErr_OverTemperatureShutdown': 3, 'ExvElecStsErr_IndeterminateElectricFault': 4, 'ExvElecStsErr_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 219
        byte = 27
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class WERVStsExvBlkErr:
        sig_name = "WERVStsExvBlkErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 201
        byte = 25
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class RRPwrDoorErrFbMotThermErrFb:
        sig_name = "RRPwrDoorErrFbMotThermErrFb"
        sig_start_bit = 181
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
        startbit = 181
        byte = 22
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FRLtchErrFbHalfClsErrFb:
        sig_name = "FRLtchErrFbHalfClsErrFb"
        sig_start_bit = 108
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
        startbit = 108
        byte = 13
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RRLtchErrFb_UB:
        sig_name = "RRLtchErrFb_UB"
        sig_start_bit = 239
        update_id_bit = 239
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 239
        byte = 29
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class REXVStsExvOvrTrvlErr:
        sig_name = "REXVStsExvOvrTrvlErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 125
        byte = 15
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BEXVStsExvOvrTempErr:
        sig_name = "BEXVStsExvOvrTempErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CERVStsExvOvrTrvlErr:
        sig_name = "CERVStsExvOvrTrvlErr"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class EEXVSts_UB:
        sig_name = "EEXVSts_UB"
        sig_start_bit = 110
        update_id_bit = 110
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 110
        byte = 13
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class TERVStsExvOvrTrvlErr:
        sig_name = "TERVStsExvOvrTrvlErr"
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
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 207
        byte = 25
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CCUMCUCDPublicCANFDFr11:
    msg_name = "CCUMCUCDPublicCANFDFr11"
    msg_id = 2
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class UsgModSwtInfo:
        sig_name = "UsgModSwtInfo"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = None
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


class LCURPublicCANFDFr04:
    msg_name = "LCURPublicCANFDFr04"
    msg_id = 406
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['CCUMCUAD', 'CCUMCUCD']
    sig_group_dict = {'DrvReqOfLighShow': ['DrvReqOfLighShowLightID1', 'DrvReqOfLighShowOffOnCmd', 'DrvReqOfLighShowPerc'], 'FrntRiDoorRdrObj6': ['FrntRiDoorRdrObj6RdrObjDstX', 'FrntRiDoorRdrObj6RdrObjDstY', 'FrntRiDoorRdrObj6RdrObjDstZ', 'FrntRiDoorRdrObj6RdrObjV'], 'FrntRiDoorRdrObj5': ['FrntRiDoorRdrObj5RdrObjDstX', 'FrntRiDoorRdrObj5RdrObjDstY', 'FrntRiDoorRdrObj5RdrObjDstZ', 'FrntRiDoorRdrObj5RdrObjV'], 'FrntRiDoorRdrObj7': ['FrntRiDoorRdrObj7RdrObjDstX', 'FrntRiDoorRdrObj7RdrObjDstY', 'FrntRiDoorRdrObj7RdrObjDstZ', 'FrntRiDoorRdrObj7RdrObjV'], 'FrntRiDoorRdrObj1': ['FrntRiDoorRdrObj1RdrObjDstX', 'FrntRiDoorRdrObj1RdrObjDstY', 'FrntRiDoorRdrObj1RdrObjDstZ', 'FrntRiDoorRdrObj1RdrObjV'], 'FrntRiDoorRdrObj4': ['FrntRiDoorRdrObj4RdrObjDstX', 'FrntRiDoorRdrObj4RdrObjDstY', 'FrntRiDoorRdrObj4RdrObjDstZ', 'FrntRiDoorRdrObj4RdrObjV'], 'FrntRiDoorRdrObj3': ['FrntRiDoorRdrObj3RdrObjDstX', 'FrntRiDoorRdrObj3RdrObjDstY', 'FrntRiDoorRdrObj3RdrObjDstZ', 'FrntRiDoorRdrObj3RdrObjV'], 'FrntRiDoorRdrObj8': ['FrntRiDoorRdrObj8RdrObjDstX', 'FrntRiDoorRdrObj8RdrObjDstY', 'FrntRiDoorRdrObj8RdrObjDstZ', 'FrntRiDoorRdrObj8RdrObjV'], 'FrntRiDoorRdrObj2': ['FrntRiDoorRdrObj2RdrObjDstX', 'FrntRiDoorRdrObj2RdrObjDstY', 'FrntRiDoorRdrObj2RdrObjDstZ', 'FrntRiDoorRdrObj2RdrObjV']}
    sig_group_dataid_dict = {}

    class DrvReqOfLighShow_UB:
        sig_name = "DrvReqOfLighShow_UB"
        sig_start_bit = 385
        update_id_bit = 385
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 385
        byte = 48
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FRDoorLockStsResd:
        sig_name = "FRDoorLockStsResd"
        sig_start_bit = 337
        update_id_bit = 344
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
        startbit = 337
        byte = 42
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FrntRiDoorRdrObj4RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj4RdrObjDstZ"
        sig_start_bit = 141
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
        startbit = 141
        bmuws_info = [(17, 0b00111111, 0b11000000, 6, 0), (18, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj7RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj7RdrObjDstX"
        sig_start_bit = 251
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
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11111100, 0b00000011, 6, 2)]

    class FRIceBreakMotSts:
        sig_name = "FRIceBreakMotSts"
        sig_start_bit = 340
        update_id_bit = 364
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotSts_Inactive': 0, 'MotSts_Active': 1, 'MotSts_ResetActive': 2}
        compute_method = None
        length = 3
        startbit = 340
        byte = 42
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class FrntRiDoorRdrObj6_UB:
        sig_name = "FrntRiDoorRdrObj6_UB"
        sig_start_bit = 371
        update_id_bit = 371
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 371
        byte = 46
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntRiDoorRdrObj8RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj8RdrObjDstX"
        sig_start_bit = 315
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
        startbit = 315
        bmuws_info = [(39, 0b00001111, 0b11110000, 4, 0), (40, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj6RdrObjV:
        sig_name = "FrntRiDoorRdrObj6RdrObjV"
        sig_start_bit = 213
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
        startbit = 213
        bmuws_info = [(26, 0b00111111, 0b11000000, 6, 0), (27, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj4RdrObjV:
        sig_name = "FrntRiDoorRdrObj4RdrObjV"
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

    class FrntRiDoorRdrObj6RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj6RdrObjDstY"
        sig_start_bit = 239
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
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj5_UB:
        sig_name = "FrntRiDoorRdrObj5_UB"
        sig_start_bit = 372
        update_id_bit = 372
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 372
        byte = 46
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRiDoorRdrObj7_UB:
        sig_name = "FrntRiDoorRdrObj7_UB"
        sig_start_bit = 370
        update_id_bit = 370
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 370
        byte = 46
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FrntRiDoorRdrObj2RdrObjV:
        sig_name = "FrntRiDoorRdrObj2RdrObjV"
        sig_start_bit = 51
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
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class FrntRiDoorRdrObj1_UB:
        sig_name = "FrntRiDoorRdrObj1_UB"
        sig_start_bit = 360
        update_id_bit = 360
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 360
        byte = 45
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DrvReqOfLighShowLightID1:
        sig_name = "DrvReqOfLighShowLightID1"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightID1_ALL': 0, 'LightID1_Front': 1, 'LightID1_Rear': 2, 'LightID1_LeftFrontLeftRearLeft': 3, 'LightID1_RightFrontRightRearRight': 4, 'LightID1_FrontLeft': 5, 'LightID1_FrontRight': 6, 'LightID1_RearLeft': 7, 'LightID1_FrontLeftRearRight': 8, 'LightID1_FrontRightRearLeft': 9, 'LightID1_ExceptFrontLeft': 10, 'LightID1_ExceptFrontRight': 11, 'LightID1_ExceptRearLeft': 12, 'LightID1_ExceptRearRight': 13, 'LightID1_Reserved1': 14, 'LightID1_Reserved2': 15}
        compute_method = None
        length = 4
        startbit = 391
        byte = 48
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntRiDoorRdrObj2RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj2RdrObjDstZ"
        sig_start_bit = 77
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
        startbit = 77
        bmuws_info = [(9, 0b00111111, 0b11000000, 6, 0), (10, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj4_UB:
        sig_name = "FrntRiDoorRdrObj4_UB"
        sig_start_bit = 373
        update_id_bit = 373
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 373
        byte = 46
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj5RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj5RdrObjDstX"
        sig_start_bit = 207
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
        startbit = 207
        bmuws_info = [(25, 0b11111111, 0b00000000, 8, 0), (26, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj2RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj2RdrObjDstY"
        sig_start_bit = 71
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
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj5RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj5RdrObjDstY"
        sig_start_bit = 181
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
        startbit = 181
        bmuws_info = [(22, 0b00111111, 0b11000000, 6, 0), (23, 0b11110000, 0b00001111, 4, 4)]

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

    class FrntRiDoorRdrObj3_UB:
        sig_name = "FrntRiDoorRdrObj3_UB"
        sig_start_bit = 374
        update_id_bit = 374
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 374
        byte = 46
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntRiDoorRdrObj3RdrObjV:
        sig_name = "FrntRiDoorRdrObj3RdrObjV"
        sig_start_bit = 89
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
        startbit = 89
        bmuws_info = [(11, 0b00000011, 0b11111100, 2, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj7RdrObjV:
        sig_name = "FrntRiDoorRdrObj7RdrObjV"
        sig_start_bit = 285
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
        startbit = 285
        bmuws_info = [(35, 0b00111111, 0b11000000, 6, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FRLtchRelsSts:
        sig_name = "FRLtchRelsSts"
        sig_start_bit = 346
        update_id_bit = 363
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
        startbit = 346
        byte = 43
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FrntRiDoorRdrObj6RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj6RdrObjDstZ"
        sig_start_bit = 245
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
        startbit = 245
        bmuws_info = [(30, 0b00111111, 0b11000000, 6, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrFlt:
        sig_name = "FrntRiDoorRdrFlt"
        sig_start_bit = 351
        update_id_bit = 362
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
        startbit = 351
        byte = 43
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class FrntRiDoorRdrObj7RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj7RdrObjDstZ"
        sig_start_bit = 257
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
        startbit = 257
        bmuws_info = [(32, 0b00000011, 0b11111100, 2, 0), (33, 0b11111111, 0b00000000, 8, 0)]

    class FrntRiDoorRdrObj1RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj1RdrObjDstX"
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

    class FRDoorInsdSwtSts:
        sig_name = "FRDoorInsdSwtSts"
        sig_start_bit = 343
        update_id_bit = 345
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtSts_IniVal': 0, 'SwtSts_Pressd': 1, 'SwtSts_NotPressd': 2, 'SwtSts_SWStuck': 3, 'SwtSts_Error': 4}
        compute_method = None
        length = 3
        startbit = 343
        byte = 42
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DrvReqOfLighShowOffOnCmd:
        sig_name = "DrvReqOfLighShowOffOnCmd"
        sig_start_bit = 387
        update_id_bit = None
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
        startbit = 387
        byte = 48
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class FrntRiDoorRdrObj4RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj4RdrObjDstX"
        sig_start_bit = 147
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
        startbit = 147
        bmuws_info = [(18, 0b00001111, 0b11110000, 4, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj7RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj7RdrObjDstY"
        sig_start_bit = 279
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
        startbit = 279
        bmuws_info = [(34, 0b11111111, 0b00000000, 8, 0), (35, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj8RdrObjV:
        sig_name = "FrntRiDoorRdrObj8RdrObjV"
        sig_start_bit = 289
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
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj4RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj4RdrObjDstY"
        sig_start_bit = 153
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
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntRiDoorRdrObj5RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj5RdrObjDstZ"
        sig_start_bit = 175
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
        startbit = 175
        bmuws_info = [(21, 0b11111111, 0b00000000, 8, 0), (22, 0b11000000, 0b00111111, 2, 6)]

    class DrvReqOfLighShowPerc:
        sig_name = "DrvReqOfLighShowPerc"
        sig_start_bit = 382
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 382
        byte = 47
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class FrntRiDoorRdrObj8_UB:
        sig_name = "FrntRiDoorRdrObj8_UB"
        sig_start_bit = 369
        update_id_bit = 369
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 369
        byte = 46
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntRiDoorRdrObj3RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj3RdrObjDstX"
        sig_start_bit = 83
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
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj5RdrObjV:
        sig_name = "FrntRiDoorRdrObj5RdrObjV"
        sig_start_bit = 187
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
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntRiDoorRdrObj6RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj6RdrObjDstX"
        sig_start_bit = 217
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
        startbit = 217
        bmuws_info = [(27, 0b00000011, 0b11111100, 2, 0), (28, 0b11111111, 0b00000000, 8, 0)]

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

    class FrntRiDoorRdrObj8RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj8RdrObjDstZ"
        sig_start_bit = 309
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
        startbit = 309
        bmuws_info = [(38, 0b00111111, 0b11000000, 6, 0), (39, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj2_UB:
        sig_name = "FrntRiDoorRdrObj2_UB"
        sig_start_bit = 375
        update_id_bit = 375
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 375
        byte = 46
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntRiDoorRdrObj1RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj1RdrObjDstY"
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

    class FrntRiDoorRdrObj1RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj1RdrObjDstZ"
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

    class FrntRiDoorRdrObj2RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj2RdrObjDstX"
        sig_start_bit = 45
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
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj8RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj8RdrObjDstY"
        sig_start_bit = 321
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
        startbit = 321
        bmuws_info = [(40, 0b00000011, 0b11111100, 2, 0), (41, 0b11111111, 0b00000000, 8, 0)]

    class FrntRiDoorRdrMod:
        sig_name = "FrntRiDoorRdrMod"
        sig_start_bit = 348
        update_id_bit = 361
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
        startbit = 348
        byte = 43
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class FRRelsMotSts:
        sig_name = "FRRelsMotSts"
        sig_start_bit = 367
        update_id_bit = 383
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotSts_Inactive': 0, 'MotSts_Active': 1, 'MotSts_ResetActive': 2}
        compute_method = None
        length = 3
        startbit = 367
        byte = 45
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

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


class LCULPublicCANFDFr04:
    msg_name = "LCULPublicCANFDFr04"
    msg_id = 402
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {'FrntLeDoorRdrObj2': ['FrntLeDoorRdrObj2RdrObjDstX', 'FrntLeDoorRdrObj2RdrObjDstY', 'FrntLeDoorRdrObj2RdrObjDstZ', 'FrntLeDoorRdrObj2RdrObjV'], 'FrntLeDoorRdrObj7': ['FrntLeDoorRdrObj7RdrObjDstX', 'FrntLeDoorRdrObj7RdrObjDstY', 'FrntLeDoorRdrObj7RdrObjDstZ', 'FrntLeDoorRdrObj7RdrObjV'], 'FrntLeDoorRdrObj3': ['FrntLeDoorRdrObj3RdrObjDstX', 'FrntLeDoorRdrObj3RdrObjDstY', 'FrntLeDoorRdrObj3RdrObjDstZ', 'FrntLeDoorRdrObj3RdrObjV'], 'FrntLeDoorRdrObj1': ['FrntLeDoorRdrObj1RdrObjDstX', 'FrntLeDoorRdrObj1RdrObjDstY', 'FrntLeDoorRdrObj1RdrObjDstZ', 'FrntLeDoorRdrObj1RdrObjV'], 'FrntLeDoorRdrObj8': ['FrntLeDoorRdrObj8RdrObjDstX', 'FrntLeDoorRdrObj8RdrObjDstY', 'FrntLeDoorRdrObj8RdrObjDstZ', 'FrntLeDoorRdrObj8RdrObjV'], 'FrntLeDoorRdrObj6': ['FrntLeDoorRdrObj6RdrObjDstX', 'FrntLeDoorRdrObj6RdrObjDstY', 'FrntLeDoorRdrObj6RdrObjDstZ', 'FrntLeDoorRdrObj6RdrObjV'], 'FrntLeDoorRdrObj4': ['FrntLeDoorRdrObj4RdrObjDstX', 'FrntLeDoorRdrObj4RdrObjDstY', 'FrntLeDoorRdrObj4RdrObjDstZ', 'FrntLeDoorRdrObj4RdrObjV'], 'FrntLeDoorRdrObj5': ['FrntLeDoorRdrObj5RdrObjDstX', 'FrntLeDoorRdrObj5RdrObjDstY', 'FrntLeDoorRdrObj5RdrObjDstZ', 'FrntLeDoorRdrObj5RdrObjV']}
    sig_group_dataid_dict = {}

    class FrntLeDoorRdrObj2_UB:
        sig_name = "FrntLeDoorRdrObj2_UB"
        sig_start_bit = 351
        update_id_bit = 351
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 351
        byte = 43
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntLeDoorRdrObj2RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj2RdrObjDstX"
        sig_start_bit = 45
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
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class FrntLeDoorRdrObj4RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj4RdrObjDstZ"
        sig_start_bit = 121
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
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj3RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj3RdrObjDstZ"
        sig_start_bit = 83
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
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj7RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj7RdrObjDstZ"
        sig_start_bit = 257
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
        startbit = 257
        bmuws_info = [(32, 0b00000011, 0b11111100, 2, 0), (33, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj1RdrObjV:
        sig_name = "FrntLeDoorRdrObj1RdrObjV"
        sig_start_bit = 13
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
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj7_UB:
        sig_name = "FrntLeDoorRdrObj7_UB"
        sig_start_bit = 346
        update_id_bit = 346
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 346
        byte = 43
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FrntLeDoorRdrObj3RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj3RdrObjDstX"
        sig_start_bit = 111
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
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj6RdrObjV:
        sig_name = "FrntLeDoorRdrObj6RdrObjV"
        sig_start_bit = 247
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
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class FrntLeDoorRdrObj6RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj6RdrObjDstY"
        sig_start_bit = 219
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
        startbit = 219
        bmuws_info = [(27, 0b00001111, 0b11110000, 4, 0), (28, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj2RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj2RdrObjDstZ"
        sig_start_bit = 51
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
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj2RdrObjV:
        sig_name = "FrntLeDoorRdrObj2RdrObjV"
        sig_start_bit = 57
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
        startbit = 57
        bmuws_info = [(7, 0b00000011, 0b11111100, 2, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj3RdrObjV:
        sig_name = "FrntLeDoorRdrObj3RdrObjV"
        sig_start_bit = 117
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
        startbit = 117
        bmuws_info = [(14, 0b00111111, 0b11000000, 6, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj8RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj8RdrObjDstZ"
        sig_start_bit = 321
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
        startbit = 321
        bmuws_info = [(40, 0b00000011, 0b11111100, 2, 0), (41, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj1RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj1RdrObjDstY"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj3_UB:
        sig_name = "FrntLeDoorRdrObj3_UB"
        sig_start_bit = 350
        update_id_bit = 350
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 350
        byte = 43
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntLeDoorRdrObj1_UB:
        sig_name = "FrntLeDoorRdrObj1_UB"
        sig_start_bit = 336
        update_id_bit = 336
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 336
        byte = 42
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntLeDoorRdrObj8_UB:
        sig_name = "FrntLeDoorRdrObj8_UB"
        sig_start_bit = 345
        update_id_bit = 345
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 345
        byte = 43
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntLeDoorRdrObj4RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj4RdrObjDstX"
        sig_start_bit = 143
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
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj5RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj5RdrObjDstY"
        sig_start_bit = 175
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
        startbit = 175
        bmuws_info = [(21, 0b11111111, 0b00000000, 8, 0), (22, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj7RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj7RdrObjDstX"
        sig_start_bit = 251
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
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11111100, 0b00000011, 6, 2)]

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
        sig_start_bit = 317
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
        startbit = 317
        bmuws_info = [(39, 0b00111111, 0b11000000, 6, 0), (40, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj5RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj5RdrObjDstZ"
        sig_start_bit = 181
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
        startbit = 181
        bmuws_info = [(22, 0b00111111, 0b11000000, 6, 0), (23, 0b11110000, 0b00001111, 4, 4)]

    class FrntLeDoorRdrFlt:
        sig_name = "FrntLeDoorRdrFlt"
        sig_start_bit = 343
        update_id_bit = 338
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
        startbit = 343
        byte = 42
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class FrntLeDoorRdrObj6_UB:
        sig_name = "FrntLeDoorRdrObj6_UB"
        sig_start_bit = 347
        update_id_bit = 347
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 347
        byte = 43
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntLeDoorRdrObj4_UB:
        sig_name = "FrntLeDoorRdrObj4_UB"
        sig_start_bit = 349
        update_id_bit = 349
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 349
        byte = 43
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntLeDoorRdrObj4RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj4RdrObjDstY"
        sig_start_bit = 153
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
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj5RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj5RdrObjDstX"
        sig_start_bit = 207
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
        startbit = 207
        bmuws_info = [(25, 0b11111111, 0b00000000, 8, 0), (26, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj6RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj6RdrObjDstZ"
        sig_start_bit = 225
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
        startbit = 225
        bmuws_info = [(28, 0b00000011, 0b11111100, 2, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj7RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj7RdrObjDstY"
        sig_start_bit = 283
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
        startbit = 283
        bmuws_info = [(35, 0b00001111, 0b11110000, 4, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj4RdrObjV:
        sig_name = "FrntLeDoorRdrObj4RdrObjV"
        sig_start_bit = 149
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
        startbit = 149
        bmuws_info = [(18, 0b00111111, 0b11000000, 6, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntLeDoorRdrObj1RdrObjDstZ:
        sig_name = "FrntLeDoorRdrObj1RdrObjDstZ"
        sig_start_bit = 17
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
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj2RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj2RdrObjDstY"
        sig_start_bit = 77
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
        startbit = 77
        bmuws_info = [(9, 0b00111111, 0b11000000, 6, 0), (10, 0b11110000, 0b00001111, 4, 4)]

    class FrntLeDoorRdrObj5_UB:
        sig_name = "FrntLeDoorRdrObj5_UB"
        sig_start_bit = 348
        update_id_bit = 348
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 348
        byte = 43
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntLeDoorRdrObj6RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj6RdrObjDstX"
        sig_start_bit = 213
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
        startbit = 213
        bmuws_info = [(26, 0b00111111, 0b11000000, 6, 0), (27, 0b11110000, 0b00001111, 4, 4)]

    class FrntLeDoorRdrMod:
        sig_name = "FrntLeDoorRdrMod"
        sig_start_bit = 340
        update_id_bit = 337
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
        startbit = 340
        byte = 42
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class FrntLeDoorRdrObj5RdrObjV:
        sig_name = "FrntLeDoorRdrObj5RdrObjV"
        sig_start_bit = 187
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
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj7RdrObjV:
        sig_name = "FrntLeDoorRdrObj7RdrObjV"
        sig_start_bit = 279
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
        startbit = 279
        bmuws_info = [(34, 0b11111111, 0b00000000, 8, 0), (35, 0b11110000, 0b00001111, 4, 4)]

    class FrntLeDoorRdrObj3RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj3RdrObjDstY"
        sig_start_bit = 89
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
        startbit = 89
        bmuws_info = [(11, 0b00000011, 0b11111100, 2, 0), (12, 0b11111111, 0b00000000, 8, 0)]

    class FrntLeDoorRdrObj8RdrObjDstX:
        sig_name = "FrntLeDoorRdrObj8RdrObjDstX"
        sig_start_bit = 311
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
        startbit = 311
        bmuws_info = [(38, 0b11111111, 0b00000000, 8, 0), (39, 0b11000000, 0b00111111, 2, 6)]

    class FrntLeDoorRdrObj8RdrObjDstY:
        sig_name = "FrntLeDoorRdrObj8RdrObjDstY"
        sig_start_bit = 289
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
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111111, 0b00000000, 8, 0)]


class LCURPublicCANFDFr01:
    msg_name = "LCURPublicCANFDFr01"
    msg_id = 66
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['ETC']
    sig_group_dict = {'PwrChRiInhb': ['PwrChRiInhbContnsPwrChRi1Inhb', 'PwrChRiInhbContnsPwrChRi2Inhb', 'PwrChRiInhbContnsPwrChRi3Inhb', 'PwrChRiInhbContnsPwrChRi4Inhb', 'PwrChRiInhbContnsPwrChRi5Inhb', 'PwrChRiInhbSwilPwrChRi10Inhb', 'PwrChRiInhbSwilPwrChRi11Inhb', 'PwrChRiInhbSwilPwrChRi12Inhb', 'PwrChRiInhbSwilPwrChRi13Inhb', 'PwrChRiInhbSwilPwrChRi14Inhb', 'PwrChRiInhbSwilPwrChRi15Inhb', 'PwrChRiInhbSwilPwrChRi16Inhb', 'PwrChRiInhbSwilPwrChRi17Inhb', 'PwrChRiInhbSwilPwrChRi18Inhb', 'PwrChRiInhbSwilPwrChRi19Inhb', 'PwrChRiInhbSwilPwrChRi1Inhb', 'PwrChRiInhbSwilPwrChRi20Inhb', 'PwrChRiInhbSwilPwrChRi21Inhb', 'PwrChRiInhbSwilPwrChRi22Inhb', 'PwrChRiInhbSwilPwrChRi23Inhb', 'PwrChRiInhbSwilPwrChRi24Inhb', 'PwrChRiInhbSwilPwrChRi25Inhb', 'PwrChRiInhbSwilPwrChRi26Inhb', 'PwrChRiInhbSwilPwrChRi27Inhb', 'PwrChRiInhbSwilPwrChRi28Inhb', 'PwrChRiInhbSwilPwrChRi29Inhb', 'PwrChRiInhbSwilPwrChRi2Inhb', 'PwrChRiInhbSwilPwrChRi3Inhb', 'PwrChRiInhbSwilPwrChRi4Inhb', 'PwrChRiInhbSwilPwrChRi5Inhb', 'PwrChRiInhbSwilPwrChRi6Inhb', 'PwrChRiInhbSwilPwrChRi7Inhb', 'PwrChRiInhbSwilPwrChRi8Inhb', 'PwrChRiInhbSwilPwrChRi9Inhb'], 'PwrChRiCmd': ['PwrChRiCmdContnsPwrChRi1Cmd', 'PwrChRiCmdContnsPwrChRi2Cmd', 'PwrChRiCmdContnsPwrChRi3Cmd', 'PwrChRiCmdContnsPwrChRi4Cmd', 'PwrChRiCmdContnsPwrChRi5Cmd', 'PwrChRiCmdSwilPwrChRi10Cmd', 'PwrChRiCmdSwilPwrChRi11Cmd', 'PwrChRiCmdSwilPwrChRi12Cmd', 'PwrChRiCmdSwilPwrChRi13Cmd', 'PwrChRiCmdSwilPwrChRi14Cmd', 'PwrChRiCmdSwilPwrChRi15Cmd', 'PwrChRiCmdSwilPwrChRi16Cmd', 'PwrChRiCmdSwilPwrChRi17Cmd', 'PwrChRiCmdSwilPwrChRi18Cmd', 'PwrChRiCmdSwilPwrChRi19Cmd', 'PwrChRiCmdSwilPwrChRi1Cmd', 'PwrChRiCmdSwilPwrChRi20Cmd', 'PwrChRiCmdSwilPwrChRi21Cmd', 'PwrChRiCmdSwilPwrChRi22Cmd', 'PwrChRiCmdSwilPwrChRi23Cmd', 'PwrChRiCmdSwilPwrChRi24Cmd', 'PwrChRiCmdSwilPwrChRi25Cmd', 'PwrChRiCmdSwilPwrChRi26Cmd', 'PwrChRiCmdSwilPwrChRi27Cmd', 'PwrChRiCmdSwilPwrChRi28Cmd', 'PwrChRiCmdSwilPwrChRi29Cmd', 'PwrChRiCmdSwilPwrChRi2Cmd', 'PwrChRiCmdSwilPwrChRi3Cmd', 'PwrChRiCmdSwilPwrChRi4Cmd', 'PwrChRiCmdSwilPwrChRi5Cmd', 'PwrChRiCmdSwilPwrChRi6Cmd', 'PwrChRiCmdSwilPwrChRi7Cmd', 'PwrChRiCmdSwilPwrChRi8Cmd', 'PwrChRiCmdSwilPwrChRi9Cmd'], 'PwrChRiCurrVal': ['PwrChRiCurrValContnsPwrChRi1CurrVal', 'PwrChRiCurrValContnsPwrChRi2CurrVal', 'PwrChRiCurrValContnsPwrChRi3CurrVal', 'PwrChRiCurrValContnsPwrChRi4CurrVal', 'PwrChRiCurrValContnsPwrChRi5CurrVal', 'PwrChRiCurrValSwilPwrChRi10CurrVal', 'PwrChRiCurrValSwilPwrChRi11CurrVal', 'PwrChRiCurrValSwilPwrChRi12CurrVal', 'PwrChRiCurrValSwilPwrChRi13CurrVal', 'PwrChRiCurrValSwilPwrChRi14CurrVal', 'PwrChRiCurrValSwilPwrChRi15CurrVal', 'PwrChRiCurrValSwilPwrChRi16CurrVal', 'PwrChRiCurrValSwilPwrChRi17CurrVal', 'PwrChRiCurrValSwilPwrChRi18CurrVal', 'PwrChRiCurrValSwilPwrChRi19CurrVal', 'PwrChRiCurrValSwilPwrChRi1CurrVal', 'PwrChRiCurrValSwilPwrChRi20CurrVal', 'PwrChRiCurrValSwilPwrChRi21CurrVal', 'PwrChRiCurrValSwilPwrChRi22CurrVal', 'PwrChRiCurrValSwilPwrChRi23CurrVal', 'PwrChRiCurrValSwilPwrChRi24CurrVal', 'PwrChRiCurrValSwilPwrChRi25CurrVal', 'PwrChRiCurrValSwilPwrChRi26CurrVal', 'PwrChRiCurrValSwilPwrChRi27CurrVal', 'PwrChRiCurrValSwilPwrChRi28CurrVal', 'PwrChRiCurrValSwilPwrChRi29CurrVal', 'PwrChRiCurrValSwilPwrChRi2CurrVal', 'PwrChRiCurrValSwilPwrChRi3CurrVal', 'PwrChRiCurrValSwilPwrChRi4CurrVal', 'PwrChRiCurrValSwilPwrChRi5CurrVal', 'PwrChRiCurrValSwilPwrChRi6CurrVal', 'PwrChRiCurrValSwilPwrChRi7CurrVal', 'PwrChRiCurrValSwilPwrChRi8CurrVal', 'PwrChRiCurrValSwilPwrChRi9CurrVal']}
    sig_group_dataid_dict = {}

    class PwrChRiCurrValSwilPwrChRi15CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi15CurrVal"
        sig_start_bit = 133
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 133
        bmuws_info = [(16, 0b00111111, 0b11000000, 6, 0), (17, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiInhbSwilPwrChRi17Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi17Inhb"
        sig_start_bit = 443
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 443
        byte = 55
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChRiCmdSwilPwrChRi16Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi16Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChRiCurrValSwilPwrChRi23CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi23CurrVal"
        sig_start_bit = 253
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 253
        bmuws_info = [(31, 0b00111111, 0b11000000, 6, 0), (32, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiCmdSwilPwrChRi9Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi9Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChRiCurrValSwilPwrChRi1CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi1CurrVal"
        sig_start_bit = 157
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 157
        bmuws_info = [(19, 0b00111111, 0b11000000, 6, 0), (20, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiInhbSwilPwrChRi19Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi19Inhb"
        sig_start_bit = 475
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 475
        byte = 59
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChRiCurrValSwilPwrChRi8CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi8CurrVal"
        sig_start_bit = 373
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 373
        bmuws_info = [(46, 0b00111111, 0b11000000, 6, 0), (47, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiCurrValSwilPwrChRi13CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi13CurrVal"
        sig_start_bit = 137
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 137
        bmuws_info = [(17, 0b00000011, 0b11111100, 2, 0), (18, 0b11111111, 0b00000000, 8, 0), (19, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiInhbSwilPwrChRi3Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi3Inhb"
        sig_start_bit = 478
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 478
        byte = 59
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChRiCmdSwilPwrChRi11Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi11Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChRiCmdContnsPwrChRi3Cmd:
        sig_name = "PwrChRiCmdContnsPwrChRi3Cmd"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChRiCmdContnsPwrChRi5Cmd:
        sig_name = "PwrChRiCmdContnsPwrChRi5Cmd"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChRiInhbSwilPwrChRi2Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi2Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 441
        byte = 55
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChRiInhbContnsPwrChRi5Inhb:
        sig_name = "PwrChRiInhbContnsPwrChRi5Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 444
        byte = 55
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChRiCurrValSwilPwrChRi7CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi7CurrVal"
        sig_start_bit = 277
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 277
        bmuws_info = [(34, 0b00111111, 0b11000000, 6, 0), (35, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiCurrValSwilPwrChRi11CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi11CurrVal"
        sig_start_bit = 65
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 65
        bmuws_info = [(8, 0b00000011, 0b11111100, 2, 0), (9, 0b11111111, 0b00000000, 8, 0), (10, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiCmdSwilPwrChRi3Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi3Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChRiCmdSwilPwrChRi12Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi12Cmd"
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

    class PwrChRiInhbSwilPwrChRi16Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi16Inhb"
        sig_start_bit = 457
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 457
        byte = 57
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChRiCurrValSwilPwrChRi26CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi26CurrVal"
        sig_start_bit = 161
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 161
        bmuws_info = [(20, 0b00000011, 0b11111100, 2, 0), (21, 0b11111111, 0b00000000, 8, 0), (22, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiCmdSwilPwrChRi25Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi25Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChRiCmdSwilPwrChRi2Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi2Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChRiCurrValSwilPwrChRi21CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi21CurrVal"
        sig_start_bit = 205
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 205
        bmuws_info = [(25, 0b00111111, 0b11000000, 6, 0), (26, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiCurrValSwilPwrChRi3CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi3CurrVal"
        sig_start_bit = 185
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 185
        bmuws_info = [(23, 0b00000011, 0b11111100, 2, 0), (24, 0b11111111, 0b00000000, 8, 0), (25, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiCmdSwilPwrChRi17Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi17Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChRiCurrValSwilPwrChRi25CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi25CurrVal"
        sig_start_bit = 113
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 113
        bmuws_info = [(14, 0b00000011, 0b11111100, 2, 0), (15, 0b11111111, 0b00000000, 8, 0), (16, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiCmdContnsPwrChRi2Cmd:
        sig_name = "PwrChRiCmdContnsPwrChRi2Cmd"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChRiCmdSwilPwrChRi29Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi29Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChRiHWProtRst:
        sig_name = "PwrChRiHWProtRst"
        sig_start_bit = 445
        update_id_bit = 472
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

    class PwrChRiInhbContnsPwrChRi3Inhb:
        sig_name = "PwrChRiInhbContnsPwrChRi3Inhb"
        sig_start_bit = 452
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 452
        byte = 56
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChRiCurrValSwilPwrChRi14CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi14CurrVal"
        sig_start_bit = 89
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 89
        bmuws_info = [(11, 0b00000011, 0b11111100, 2, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiCurrValContnsPwrChRi3CurrVal:
        sig_name = "PwrChRiCurrValContnsPwrChRi3CurrVal"
        sig_start_bit = 301
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 301
        bmuws_info = [(37, 0b00111111, 0b11000000, 6, 0), (38, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiCmdSwilPwrChRi10Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi10Cmd"
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

    class PwrChRiCmdSwilPwrChRi5Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi5Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChRiCmdSwilPwrChRi19Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi19Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChRiCmdContnsPwrChRi1Cmd:
        sig_name = "PwrChRiCmdContnsPwrChRi1Cmd"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChRiInhbSwilPwrChRi29Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi29Inhb"
        sig_start_bit = 461
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 461
        byte = 57
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChRiInhbSwilPwrChRi9Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi9Inhb"
        sig_start_bit = 463
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 463
        byte = 57
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChRiCurrValSwilPwrChRi20CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi20CurrVal"
        sig_start_bit = 233
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 233
        bmuws_info = [(29, 0b00000011, 0b11111100, 2, 0), (30, 0b11111111, 0b00000000, 8, 0), (31, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiCurrValSwilPwrChRi18CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi18CurrVal"
        sig_start_bit = 229
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 229
        bmuws_info = [(28, 0b00111111, 0b11000000, 6, 0), (29, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiCmdSwilPwrChRi7Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi7Cmd"
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

    class PwrChRiInhbSwilPwrChRi23Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi23Inhb"
        sig_start_bit = 460
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 460
        byte = 57
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChRiInhbSwilPwrChRi14Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi14Inhb"
        sig_start_bit = 451
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 451
        byte = 56
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChRiInhbSwilPwrChRi20Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi20Inhb"
        sig_start_bit = 470
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 470
        byte = 58
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChRiCmdSwilPwrChRi15Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi15Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChRiInhbSwilPwrChRi12Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi12Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 440
        byte = 55
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChRiCurrValSwilPwrChRi5CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi5CurrVal"
        sig_start_bit = 329
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 329
        bmuws_info = [(41, 0b00000011, 0b11111100, 2, 0), (42, 0b11111111, 0b00000000, 8, 0), (43, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiInhbContnsPwrChRi1Inhb:
        sig_name = "PwrChRiInhbContnsPwrChRi1Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 471
        byte = 58
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChRiCmdSwilPwrChRi26Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi26Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChRiCmdSwilPwrChRi18Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi18Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChRiCmdSwilPwrChRi24Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi24Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChRiCmdContnsPwrChRi4Cmd:
        sig_name = "PwrChRiCmdContnsPwrChRi4Cmd"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChRiCurrValSwilPwrChRi28CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi28CurrVal"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 61
        bmuws_info = [(7, 0b00111111, 0b11000000, 6, 0), (8, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiCmdSwilPwrChRi22Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi22Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChRiCurrValSwilPwrChRi24CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi24CurrVal"
        sig_start_bit = 305
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 305
        bmuws_info = [(38, 0b00000011, 0b11111100, 2, 0), (39, 0b11111111, 0b00000000, 8, 0), (40, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiCurrValSwilPwrChRi27CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi27CurrVal"
        sig_start_bit = 425
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 425
        bmuws_info = [(53, 0b00000011, 0b11111100, 2, 0), (54, 0b11111111, 0b00000000, 8, 0), (55, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiInhbSwilPwrChRi7Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi7Inhb"
        sig_start_bit = 442
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 442
        byte = 55
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChRiInhbSwilPwrChRi21Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi21Inhb"
        sig_start_bit = 469
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 469
        byte = 58
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChRiInhb_UB:
        sig_name = "PwrChRiInhb_UB"
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

    class PwrChRiCmdSwilPwrChRi14Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi14Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChRiCmdSwilPwrChRi8Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi8Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChRiCmd_UB:
        sig_name = "PwrChRiCmd_UB"
        sig_start_bit = 474
        update_id_bit = 474
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 474
        byte = 59
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChRiCurrValSwilPwrChRi29CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi29CurrVal"
        sig_start_bit = 353
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 353
        bmuws_info = [(44, 0b00000011, 0b11111100, 2, 0), (45, 0b11111111, 0b00000000, 8, 0), (46, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiCmdSwilPwrChRi21Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi21Cmd"
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

    class PwrChRiCurrValSwilPwrChRi4CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi4CurrVal"
        sig_start_bit = 209
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 209
        bmuws_info = [(26, 0b00000011, 0b11111100, 2, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiCurrValContnsPwrChRi1CurrVal:
        sig_name = "PwrChRiCurrValContnsPwrChRi1CurrVal"
        sig_start_bit = 421
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 421
        bmuws_info = [(52, 0b00111111, 0b11000000, 6, 0), (53, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiInhbSwilPwrChRi27Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi27Inhb"
        sig_start_bit = 476
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 476
        byte = 59
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChRiInhbSwilPwrChRi26Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi26Inhb"
        sig_start_bit = 467
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 467
        byte = 58
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChRiCurrValSwilPwrChRi9CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi9CurrVal"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiInhbSwilPwrChRi15Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi15Inhb"
        sig_start_bit = 454
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 454
        byte = 56
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChRiInhbSwilPwrChRi13Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi13Inhb"
        sig_start_bit = 456
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 456
        byte = 57
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChRiInhbSwilPwrChRi25Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi25Inhb"
        sig_start_bit = 455
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 455
        byte = 56
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChRiCurrValSwilPwrChRi17CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi17CurrVal"
        sig_start_bit = 85
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 85
        bmuws_info = [(10, 0b00111111, 0b11000000, 6, 0), (11, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiInhbSwilPwrChRi5Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi5Inhb"
        sig_start_bit = 458
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 458
        byte = 57
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChRiCmdSwilPwrChRi28Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi28Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChRiInhbSwilPwrChRi8Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi8Inhb"
        sig_start_bit = 453
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 453
        byte = 56
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChRiCmdSwilPwrChRi6Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi6Cmd"
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

    class PwrChRiInhbSwilPwrChRi1Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi1Inhb"
        sig_start_bit = 462
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 462
        byte = 57
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PwrChRiInhbSwilPwrChRi24Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi24Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 479
        byte = 59
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChRiInhbSwilPwrChRi4Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi4Inhb"
        sig_start_bit = 466
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 466
        byte = 58
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChRiCurrValContnsPwrChRi4CurrVal:
        sig_name = "PwrChRiCurrValContnsPwrChRi4CurrVal"
        sig_start_bit = 257
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 257
        bmuws_info = [(32, 0b00000011, 0b11111100, 2, 0), (33, 0b11111111, 0b00000000, 8, 0), (34, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiCmdSwilPwrChRi13Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi13Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChRiCurrValContnsPwrChRi5CurrVal:
        sig_name = "PwrChRiCurrValContnsPwrChRi5CurrVal"
        sig_start_bit = 281
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 281
        bmuws_info = [(35, 0b00000011, 0b11111100, 2, 0), (36, 0b11111111, 0b00000000, 8, 0), (37, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiInhbSwilPwrChRi11Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi11Inhb"
        sig_start_bit = 465
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 465
        byte = 58
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChRiCmdSwilPwrChRi20Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi20Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChRiCmdSwilPwrChRi23Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi23Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChRiCurrValSwilPwrChRi16CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi16CurrVal"
        sig_start_bit = 181
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 181
        bmuws_info = [(22, 0b00111111, 0b11000000, 6, 0), (23, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiInhbContnsPwrChRi4Inhb:
        sig_name = "PwrChRiInhbContnsPwrChRi4Inhb"
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
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 464
        byte = 58
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChRiInhbSwilPwrChRi6Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi6Inhb"
        sig_start_bit = 448
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 448
        byte = 56
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PwrChRiCmdSwilPwrChRi4Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi4Cmd"
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

    class PwrChRiCurrValSwilPwrChRi6CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi6CurrVal"
        sig_start_bit = 109
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 109
        bmuws_info = [(13, 0b00111111, 0b11000000, 6, 0), (14, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiCurrVal_UB:
        sig_name = "PwrChRiCurrVal_UB"
        sig_start_bit = 473
        update_id_bit = 473
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 473
        byte = 59
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChRiInhbSwilPwrChRi28Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi28Inhb"
        sig_start_bit = 459
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 459
        byte = 57
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PwrChRiCmdSwilPwrChRi1Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi1Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PwrChRiCurrValSwilPwrChRi22CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi22CurrVal"
        sig_start_bit = 377
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 377
        bmuws_info = [(47, 0b00000011, 0b11111100, 2, 0), (48, 0b11111111, 0b00000000, 8, 0), (49, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiCurrValSwilPwrChRi19CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi19CurrVal"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 37
        bmuws_info = [(4, 0b00111111, 0b11000000, 6, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiCurrValSwilPwrChRi2CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi2CurrVal"
        sig_start_bit = 397
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 397
        bmuws_info = [(49, 0b00111111, 0b11000000, 6, 0), (50, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiInhbSwilPwrChRi22Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi22Inhb"
        sig_start_bit = 450
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 450
        byte = 56
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PwrChRiInhbSwilPwrChRi10Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi10Inhb"
        sig_start_bit = 477
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 477
        byte = 59
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PwrChRiCurrValSwilPwrChRi10CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi10CurrVal"
        sig_start_bit = 401
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 401
        bmuws_info = [(50, 0b00000011, 0b11111100, 2, 0), (51, 0b11111111, 0b00000000, 8, 0), (52, 0b11000000, 0b00111111, 2, 6)]

    class PwrChRiInhbSwilPwrChRi18Inhb:
        sig_name = "PwrChRiInhbSwilPwrChRi18Inhb"
        sig_start_bit = 449
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 449
        byte = 56
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class PwrChRiInhbContnsPwrChRi2Inhb:
        sig_name = "PwrChRiInhbContnsPwrChRi2Inhb"
        sig_start_bit = 468
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 468
        byte = 58
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PwrChRiCurrValSwilPwrChRi12CurrVal:
        sig_name = "PwrChRiCurrValSwilPwrChRi12CurrVal"
        sig_start_bit = 349
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 349
        bmuws_info = [(43, 0b00111111, 0b11000000, 6, 0), (44, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiCurrValContnsPwrChRi2CurrVal:
        sig_name = "PwrChRiCurrValContnsPwrChRi2CurrVal"
        sig_start_bit = 325
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 325
        bmuws_info = [(40, 0b00111111, 0b11000000, 6, 0), (41, 0b11111100, 0b00000011, 6, 2)]

    class PwrChRiCmdSwilPwrChRi27Cmd:
        sig_name = "PwrChRiCmdSwilPwrChRi27Cmd"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class VCUPublicCANFDFr06:
    msg_name = "VCUPublicCANFDFr06"
    msg_id = 663
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "VCU"
    rx_nodes = ['ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HVClimaAllwd:
        sig_name = "HVClimaAllwd"
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
        sig_value_table = {'ThermAllwd_Init': 0, 'ThermAllwd_NOK': 1, 'ThermAllwd_OK': 2, 'ThermAllwd_HOLD': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CCUMCUCDPublicCANFDFr12:
    msg_name = "CCUMCUCDPublicCANFDFr12"
    msg_id = 660
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['LCUR', 'LCUL']
    sig_group_dict = {'VehCfgDataGrp': ['VehCfgDataGrpVehCfgData1BlkIDBytePosn1', 'VehCfgDataGrpVehCfgData1BytePosn10', 'VehCfgDataGrpVehCfgData1BytePosn11', 'VehCfgDataGrpVehCfgData1BytePosn12', 'VehCfgDataGrpVehCfgData1BytePosn13', 'VehCfgDataGrpVehCfgData1BytePosn14', 'VehCfgDataGrpVehCfgData1BytePosn15', 'VehCfgDataGrpVehCfgData1BytePosn16', 'VehCfgDataGrpVehCfgData1BytePosn17', 'VehCfgDataGrpVehCfgData1BytePosn18', 'VehCfgDataGrpVehCfgData1BytePosn19', 'VehCfgDataGrpVehCfgData1BytePosn2', 'VehCfgDataGrpVehCfgData1BytePosn20', 'VehCfgDataGrpVehCfgData1BytePosn21', 'VehCfgDataGrpVehCfgData1BytePosn22', 'VehCfgDataGrpVehCfgData1BytePosn23', 'VehCfgDataGrpVehCfgData1BytePosn24', 'VehCfgDataGrpVehCfgData1BytePosn25', 'VehCfgDataGrpVehCfgData1BytePosn26', 'VehCfgDataGrpVehCfgData1BytePosn27', 'VehCfgDataGrpVehCfgData1BytePosn28', 'VehCfgDataGrpVehCfgData1BytePosn29', 'VehCfgDataGrpVehCfgData1BytePosn3', 'VehCfgDataGrpVehCfgData1BytePosn30', 'VehCfgDataGrpVehCfgData1BytePosn31', 'VehCfgDataGrpVehCfgData1BytePosn32', 'VehCfgDataGrpVehCfgData1BytePosn33', 'VehCfgDataGrpVehCfgData1BytePosn34', 'VehCfgDataGrpVehCfgData1BytePosn35', 'VehCfgDataGrpVehCfgData1BytePosn36', 'VehCfgDataGrpVehCfgData1BytePosn37', 'VehCfgDataGrpVehCfgData1BytePosn38', 'VehCfgDataGrpVehCfgData1BytePosn39', 'VehCfgDataGrpVehCfgData1BytePosn4', 'VehCfgDataGrpVehCfgData1BytePosn40', 'VehCfgDataGrpVehCfgData1BytePosn41', 'VehCfgDataGrpVehCfgData1BytePosn42', 'VehCfgDataGrpVehCfgData1BytePosn43', 'VehCfgDataGrpVehCfgData1BytePosn44', 'VehCfgDataGrpVehCfgData1BytePosn45', 'VehCfgDataGrpVehCfgData1BytePosn46', 'VehCfgDataGrpVehCfgData1BytePosn47', 'VehCfgDataGrpVehCfgData1BytePosn48', 'VehCfgDataGrpVehCfgData1BytePosn49', 'VehCfgDataGrpVehCfgData1BytePosn5', 'VehCfgDataGrpVehCfgData1BytePosn50', 'VehCfgDataGrpVehCfgData1BytePosn51', 'VehCfgDataGrpVehCfgData1BytePosn52', 'VehCfgDataGrpVehCfgData1BytePosn53', 'VehCfgDataGrpVehCfgData1BytePosn54', 'VehCfgDataGrpVehCfgData1BytePosn55', 'VehCfgDataGrpVehCfgData1BytePosn56', 'VehCfgDataGrpVehCfgData1BytePosn57', 'VehCfgDataGrpVehCfgData1BytePosn58', 'VehCfgDataGrpVehCfgData1BytePosn59', 'VehCfgDataGrpVehCfgData1BytePosn6', 'VehCfgDataGrpVehCfgData1BytePosn60', 'VehCfgDataGrpVehCfgData1BytePosn61', 'VehCfgDataGrpVehCfgData1BytePosn62', 'VehCfgDataGrpVehCfgData1BytePosn63', 'VehCfgDataGrpVehCfgData1BytePosn64', 'VehCfgDataGrpVehCfgData1BytePosn7', 'VehCfgDataGrpVehCfgData1BytePosn8', 'VehCfgDataGrpVehCfgData1BytePosn9']}
    sig_group_dataid_dict = {}

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


class VCUPublicCANFDFr01:
    msg_name = "VCUPublicCANFDFr01"
    msg_id = 67
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 16
    tx_node = "VCU"
    rx_nodes = ['CCUMCUAD', 'ETC']
    sig_group_dict = {'ADASModInhbnFb': ['ADASModInhbnFbChks', 'ADASModInhbnFbCntr', 'ADASModInhbnFbInhbnFb']}
    sig_group_dataid_dict = {}

    class ADASModInhbnFbChks:
        sig_name = "ADASModInhbnFbChks"
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

    class ADASModInhbnFb_UB:
        sig_name = "ADASModInhbnFb_UB"
        sig_start_bit = 8
        update_id_bit = 8
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ADASModInhbnFbInhbnFb:
        sig_name = "ADASModInhbnFbInhbnFb"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class ADASModInhbnFbCntr:
        sig_name = "ADASModInhbnFbCntr"
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


class CCUMCUCDPublicCANFDFr09:
    msg_name = "CCUMCUCDPublicCANFDFr09"
    msg_id = 769
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CCUCoolgReq:
        sig_name = "CCUCoolgReq"
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

    class CCUCooltFlwReq:
        sig_name = "CCUCooltFlwReq"
        sig_start_bit = 7
        update_id_bit = 12
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 500
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b10000000, 0b01111111, 1, 7)]


class LCURPublicCANFDFr09:
    msg_name = "LCURPublicCANFDFr09"
    msg_id = 772
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.16
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['VCU', 'CCUMCUCD']
    sig_group_dict = {'HVHeatrCmptPwrCns': ['HVHeatrCmptPwrCnsHVAirHeatrPwrCns', 'HVHeatrCmptPwrCnsHVCooltHeatrPwrCns']}
    sig_group_dataid_dict = {}

    class HVHeatrCmptPwrCns_UB:
        sig_name = "HVHeatrCmptPwrCns_UB"
        sig_start_bit = 130
        update_id_bit = 130
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 130
        byte = 16
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BCTVPosnAct:
        sig_name = "BCTVPosnAct"
        sig_start_bit = 9
        update_id_bit = 12
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
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class CmprReqCmprPwrLim:
        sig_name = "CmprReqCmprPwrLim"
        sig_start_bit = 95
        update_id_bit = 85
        sig_length = 8
        sig_value_factor = 40
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

    class HVHeatrCmptPwrCnsHVAirHeatrPwrCns:
        sig_name = "HVHeatrCmptPwrCnsHVAirHeatrPwrCns"
        sig_start_bit = 108
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 108
        bmuws_info = [(13, 0b00011111, 0b11100000, 5, 0), (14, 0b11111111, 0b00000000, 8, 0)]

    class CmprReqCmprSpdReq:
        sig_name = "CmprReqCmprSpdReq"
        sig_start_bit = 103
        update_id_bit = 111
        sig_length = 8
        sig_value_factor = 50
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 254
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

    class ECTVPosnAct:
        sig_name = "ECTVPosnAct"
        sig_start_bit = 55
        update_id_bit = 37
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11000000, 0b00111111, 2, 6)]

    class CmprReqCmprRunReq:
        sig_name = "CmprReqCmprRunReq"
        sig_start_bit = 84
        update_id_bit = 82
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmprRunReq_CmprOff': 0, 'CmprRunReq_CmprOn': 1, 'CmprRunReq_Resd': 2, 'CmprRunReq_SigNotAvl': 3}
        compute_method = None
        length = 2
        startbit = 84
        byte = 10
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HVAirHeatrEna:
        sig_name = "HVAirHeatrEna"
        sig_start_bit = 81
        update_id_bit = 80
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
        startbit = 81
        byte = 10
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HvCooltHeatrEnad:
        sig_name = "HvCooltHeatrEnad"
        sig_start_bit = 110
        update_id_bit = 109
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
        startbit = 110
        byte = 13
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class LCTVPosnAct:
        sig_name = "LCTVPosnAct"
        sig_start_bit = 79
        update_id_bit = 35
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
        startbit = 79
        bmuws_info = [(9, 0b11111111, 0b00000000, 8, 0), (10, 0b11000000, 0b00111111, 2, 6)]

    class DCTVPosnAct:
        sig_name = "DCTVPosnAct"
        sig_start_bit = 33
        update_id_bit = 10
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
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class BCFVPosnAct:
        sig_name = "BCFVPosnAct"
        sig_start_bit = 7
        update_id_bit = 13
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class HVHeatrCmptPwrCnsHVCooltHeatrPwrCns:
        sig_name = "HVHeatrCmptPwrCnsHVCooltHeatrPwrCns"
        sig_start_bit = 127
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 127
        bmuws_info = [(15, 0b11111111, 0b00000000, 8, 0), (16, 0b11111000, 0b00000111, 5, 3)]

    class HCTVPosnAct:
        sig_name = "HCTVPosnAct"
        sig_start_bit = 57
        update_id_bit = 36
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
        startbit = 57
        bmuws_info = [(7, 0b00000011, 0b11111100, 2, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class CCTVPosnAct:
        sig_name = "CCTVPosnAct"
        sig_start_bit = 31
        update_id_bit = 11
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
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11000000, 0b00111111, 2, 6)]


class VCUPublicCANFDFr02:
    msg_name = "VCUPublicCANFDFr02"
    msg_id = 149
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 16
    tx_node = "VCU"
    rx_nodes = ['CCUMCUCD', 'ETC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class PrpsnEgyRgnLimCmpAllwd:
        sig_name = "PrpsnEgyRgnLimCmpAllwd"
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
        sig_value_table = {'AllwdorNot_Init': 0, 'AllwdorNot_NotAllwd': 1, 'AllwdorNot_Allwd': 2, 'AllwdorNot_Resd1': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class LCURPublicCANFDFr07:
    msg_name = "LCURPublicCANFDFr07"
    msg_id = 409
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['CCUMCUAD', 'CCUMCUCD']
    sig_group_dict = {'ReRiDoorRdrObj12': ['ReRiDoorRdrObj12RdrObjDstX', 'ReRiDoorRdrObj12RdrObjDstY', 'ReRiDoorRdrObj12RdrObjDstZ', 'ReRiDoorRdrObj12RdrObjV'], 'ReRiDoorRdrObj13': ['ReRiDoorRdrObj13RdrObjDstX', 'ReRiDoorRdrObj13RdrObjDstY', 'ReRiDoorRdrObj13RdrObjDstZ', 'ReRiDoorRdrObj13RdrObjV'], 'ReRiDoorRdrObj9': ['ReRiDoorRdrObj9RdrObjDstX', 'ReRiDoorRdrObj9RdrObjDstY', 'ReRiDoorRdrObj9RdrObjDstZ', 'ReRiDoorRdrObj9RdrObjV'], 'ReRiDoorRdrObj16': ['ReRiDoorRdrObj16RdrObjDstX', 'ReRiDoorRdrObj16RdrObjDstY', 'ReRiDoorRdrObj16RdrObjDstZ', 'ReRiDoorRdrObj16RdrObjV'], 'ReRiDoorRdrObj11': ['ReRiDoorRdrObj11RdrObjDstX', 'ReRiDoorRdrObj11RdrObjDstY', 'ReRiDoorRdrObj11RdrObjDstZ', 'ReRiDoorRdrObj11RdrObjV'], 'ReRiDoorRdrObj15': ['ReRiDoorRdrObj15RdrObjDstX', 'ReRiDoorRdrObj15RdrObjDstY', 'ReRiDoorRdrObj15RdrObjDstZ', 'ReRiDoorRdrObj15RdrObjV'], 'ReRiDoorRdrObj10': ['ReRiDoorRdrObj10RdrObjDstX', 'ReRiDoorRdrObj10RdrObjDstY', 'ReRiDoorRdrObj10RdrObjDstZ', 'ReRiDoorRdrObj10RdrObjV'], 'TrAntiPnchSts': ['TrAntiPnchStsCloseAntiPnchSts', 'TrAntiPnchStsOPenAntiPnchSts'], 'ReRiDoorRdrObj14': ['ReRiDoorRdrObj14RdrObjDstX', 'ReRiDoorRdrObj14RdrObjDstY', 'ReRiDoorRdrObj14RdrObjDstZ', 'ReRiDoorRdrObj14RdrObjV']}
    sig_group_dataid_dict = {}

    class TrAntiPnchStsOPenAntiPnchSts:
        sig_name = "TrAntiPnchStsOPenAntiPnchSts"
        sig_start_bit = 372
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
        startbit = 372
        byte = 46
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReRiDoorRdrObj10RdrObjV:
        sig_name = "ReRiDoorRdrObj10RdrObjV"
        sig_start_bit = 19
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
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class ReRiDoorRdrObj14RdrObjV:
        sig_name = "ReRiDoorRdrObj14RdrObjV"
        sig_start_bit = 193
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
        startbit = 193
        bmuws_info = [(24, 0b00000011, 0b11111100, 2, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj9RdrObjDstX:
        sig_name = "ReRiDoorRdrObj9RdrObjDstX"
        sig_start_bit = 321
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
        startbit = 321
        bmuws_info = [(40, 0b00000011, 0b11111100, 2, 0), (41, 0b11111111, 0b00000000, 8, 0)]

    class ReRiDoorRdrObj12_UB:
        sig_name = "ReRiDoorRdrObj12_UB"
        sig_start_bit = 370
        update_id_bit = 370
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 370
        byte = 46
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReRiDoorRdrObj12RdrObjV:
        sig_name = "ReRiDoorRdrObj12RdrObjV"
        sig_start_bit = 89
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
        startbit = 89
        bmuws_info = [(11, 0b00000011, 0b11111100, 2, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj16RdrObjV:
        sig_name = "ReRiDoorRdrObj16RdrObjV"
        sig_start_bit = 279
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
        startbit = 279
        bmuws_info = [(34, 0b11111111, 0b00000000, 8, 0), (35, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj14RdrObjDstX:
        sig_name = "ReRiDoorRdrObj14RdrObjDstX"
        sig_start_bit = 175
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
        startbit = 175
        bmuws_info = [(21, 0b11111111, 0b00000000, 8, 0), (22, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj13RdrObjDstY:
        sig_name = "ReRiDoorRdrObj13RdrObjDstY"
        sig_start_bit = 153
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
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class ReRiDoorRdrObj10RdrObjDstX:
        sig_name = "ReRiDoorRdrObj10RdrObjDstX"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj12RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj12RdrObjDstZ"
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

    class ReRiDoorRdrObj11RdrObjDstY:
        sig_name = "ReRiDoorRdrObj11RdrObjDstY"
        sig_start_bit = 77
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
        startbit = 77
        bmuws_info = [(9, 0b00111111, 0b11000000, 6, 0), (10, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj15RdrObjV:
        sig_name = "ReRiDoorRdrObj15RdrObjV"
        sig_start_bit = 213
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
        startbit = 213
        bmuws_info = [(26, 0b00111111, 0b11000000, 6, 0), (27, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj14RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj14RdrObjDstZ"
        sig_start_bit = 187
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
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj16RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj16RdrObjDstZ"
        sig_start_bit = 257
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
        startbit = 257
        bmuws_info = [(32, 0b00000011, 0b11111100, 2, 0), (33, 0b11111111, 0b00000000, 8, 0)]

    class TrunkCinchHomeSwt:
        sig_name = "TrunkCinchHomeSwt"
        sig_start_bit = 375
        update_id_bit = 390
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CinMotPosn_HomePosn': 0, 'CinMotPosn_NotHomePosn': 1}
        compute_method = None
        length = 2
        startbit = 375
        byte = 46
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ReRiDoorRdrObj13_UB:
        sig_name = "ReRiDoorRdrObj13_UB"
        sig_start_bit = 369
        update_id_bit = 369
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 369
        byte = 46
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ReRiDoorRdrObj9_UB:
        sig_name = "ReRiDoorRdrObj9_UB"
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

    class ReRiDoorRdrObj10RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj10RdrObjDstZ"
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

    class ReRiDoorRdrObj11RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj11RdrObjDstZ"
        sig_start_bit = 45
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
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj15RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj15RdrObjDstZ"
        sig_start_bit = 245
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
        startbit = 245
        bmuws_info = [(30, 0b00111111, 0b11000000, 6, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj15RdrObjDstX:
        sig_name = "ReRiDoorRdrObj15RdrObjDstX"
        sig_start_bit = 239
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
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj10RdrObjDstY:
        sig_name = "ReRiDoorRdrObj10RdrObjDstY"
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

    class ReRiDoorRdrObj14RdrObjDstY:
        sig_name = "ReRiDoorRdrObj14RdrObjDstY"
        sig_start_bit = 181
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
        startbit = 181
        bmuws_info = [(22, 0b00111111, 0b11000000, 6, 0), (23, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj16_UB:
        sig_name = "ReRiDoorRdrObj16_UB"
        sig_start_bit = 382
        update_id_bit = 382
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 382
        byte = 47
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReRiDoorRdrObj16RdrObjDstX:
        sig_name = "ReRiDoorRdrObj16RdrObjDstX"
        sig_start_bit = 251
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
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj11RdrObjV:
        sig_name = "ReRiDoorRdrObj11RdrObjV"
        sig_start_bit = 57
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
        startbit = 57
        bmuws_info = [(7, 0b00000011, 0b11111100, 2, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11000000, 0b00111111, 2, 6)]

    class ReRiDoorRdrObj16RdrObjDstY:
        sig_name = "ReRiDoorRdrObj16RdrObjDstY"
        sig_start_bit = 283
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
        startbit = 283
        bmuws_info = [(35, 0b00001111, 0b11110000, 4, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class TrAng:
        sig_name = "TrAng"
        sig_start_bit = 343
        update_id_bit = 380
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
        startbit = 343
        byte = 42
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReRiDoorRdrObj9RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj9RdrObjDstZ"
        sig_start_bit = 309
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
        startbit = 309
        bmuws_info = [(38, 0b00111111, 0b11000000, 6, 0), (39, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj9RdrObjDstY:
        sig_name = "ReRiDoorRdrObj9RdrObjDstY"
        sig_start_bit = 315
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
        startbit = 315
        bmuws_info = [(39, 0b00001111, 0b11110000, 4, 0), (40, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj11RdrObjDstX:
        sig_name = "ReRiDoorRdrObj11RdrObjDstX"
        sig_start_bit = 51
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
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj11_UB:
        sig_name = "ReRiDoorRdrObj11_UB"
        sig_start_bit = 371
        update_id_bit = 371
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 371
        byte = 46
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ReRiDoorRdrObj15RdrObjDstY:
        sig_name = "ReRiDoorRdrObj15RdrObjDstY"
        sig_start_bit = 217
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
        startbit = 217
        bmuws_info = [(27, 0b00000011, 0b11111100, 2, 0), (28, 0b11111111, 0b00000000, 8, 0)]

    class ReRiDoorRdrObj13RdrObjDstX:
        sig_name = "ReRiDoorRdrObj13RdrObjDstX"
        sig_start_bit = 147
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
        startbit = 147
        bmuws_info = [(18, 0b00001111, 0b11110000, 4, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class ReRiDoorRdrObj13RdrObjV:
        sig_name = "ReRiDoorRdrObj13RdrObjV"
        sig_start_bit = 143
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
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11110000, 0b00001111, 4, 4)]

    class ReRiDoorRdrObj9RdrObjV:
        sig_name = "ReRiDoorRdrObj9RdrObjV"
        sig_start_bit = 289
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
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111111, 0b00000000, 8, 0), (38, 0b11000000, 0b00111111, 2, 6)]

    class TrPosn:
        sig_name = "TrPosn"
        sig_start_bit = 367
        update_id_bit = 391
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
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TrMtnSts:
        sig_name = "TrMtnSts"
        sig_start_bit = 359
        update_id_bit = 377
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
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ReRiDoorRdrObj15_UB:
        sig_name = "ReRiDoorRdrObj15_UB"
        sig_start_bit = 383
        update_id_bit = 383
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 383
        byte = 47
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class TrOutdSwtSts:
        sig_name = "TrOutdSwtSts"
        sig_start_bit = 355
        update_id_bit = 376
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtSts_IniVal': 0, 'SwtSts_Pressd': 1, 'SwtSts_NotPressd': 2, 'SwtSts_SWStuck': 3, 'SwtSts_Error': 4}
        compute_method = None
        length = 3
        startbit = 355
        byte = 44
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class TrunkLtchOpenSwt:
        sig_name = "TrunkLtchOpenSwt"
        sig_start_bit = 352
        update_id_bit = 389
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
        startbit = 352
        byte = 44
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class TrLtchPosn:
        sig_name = "TrLtchPosn"
        sig_start_bit = 351
        update_id_bit = 378
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
        startbit = 351
        byte = 43
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TrAntiPnchStsCloseAntiPnchSts:
        sig_name = "TrAntiPnchStsCloseAntiPnchSts"
        sig_start_bit = 373
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
        startbit = 373
        byte = 46
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReRiDoorRdrObj13RdrObjDstZ:
        sig_name = "ReRiDoorRdrObj13RdrObjDstZ"
        sig_start_bit = 121
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
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class ReRiDoorRdrObj10_UB:
        sig_name = "ReRiDoorRdrObj10_UB"
        sig_start_bit = 336
        update_id_bit = 336
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 336
        byte = 42
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class TrAntiPnchSts_UB:
        sig_name = "TrAntiPnchSts_UB"
        sig_start_bit = 379
        update_id_bit = 379
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 379
        byte = 47
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ReRiDoorRdrObj12RdrObjDstY:
        sig_name = "ReRiDoorRdrObj12RdrObjDstY"
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

    class ReRiDoorRdrObj14_UB:
        sig_name = "ReRiDoorRdrObj14_UB"
        sig_start_bit = 368
        update_id_bit = 368
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 368
        byte = 46
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReRiDoorRdrObj12RdrObjDstX:
        sig_name = "ReRiDoorRdrObj12RdrObjDstX"
        sig_start_bit = 83
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
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11111100, 0b00000011, 6, 2)]


class LCULPublicCANFDNmFr:
    msg_name = "LCULPublicCANFDNmFr"
    msg_id = 1283
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUMCUADPublicCANFDFr04:
    msg_name = "CCUMCUADPublicCANFDFr04"
    msg_id = 304
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "CCUMCUAD"
    rx_nodes = ['LCUL', 'CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EPBHpsAck:
        sig_name = "EPBHpsAck"
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
        sig_value_table = {'NoYes3_No': 0, 'NoYes3_Yes': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EPBHpsAvl:
        sig_name = "EPBHpsAvl"
        sig_start_bit = 6
        update_id_bit = 3
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ScmLigtReq:
        sig_name = "ScmLigtReq"
        sig_start_bit = 5
        update_id_bit = 2
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


class CCUMCUCDPublicCANFDNmFr:
    msg_name = "CCUMCUCDPublicCANFDNmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCULPublicCANFDFr07:
    msg_name = "LCULPublicCANFDFr07"
    msg_id = 405
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['CCUMCUAD', 'CCUMCUCD']
    sig_group_dict = {'ReLeDoorRdrObj10': ['ReLeDoorRdrObj10RdrObjDstX', 'ReLeDoorRdrObj10RdrObjDstY', 'ReLeDoorRdrObj10RdrObjDstZ', 'ReLeDoorRdrObj10RdrObjV'], 'ReLeDoorRdrObj14': ['ReLeDoorRdrObj14RdrObjDstX', 'ReLeDoorRdrObj14RdrObjDstY', 'ReLeDoorRdrObj14RdrObjDstZ', 'ReLeDoorRdrObj14RdrObjV'], 'ReLeDoorRdrObj12': ['ReLeDoorRdrObj12RdrObjDstX', 'ReLeDoorRdrObj12RdrObjDstY', 'ReLeDoorRdrObj12RdrObjDstZ', 'ReLeDoorRdrObj12RdrObjV'], 'ReLeDoorRdrObj9': ['ReLeDoorRdrObj9RdrObjDstX', 'ReLeDoorRdrObj9RdrObjDstY', 'ReLeDoorRdrObj9RdrObjDstZ', 'ReLeDoorRdrObj9RdrObjV'], 'ReLeDoorRdrObj15': ['ReLeDoorRdrObj15RdrObjDstX', 'ReLeDoorRdrObj15RdrObjDstY', 'ReLeDoorRdrObj15RdrObjDstZ', 'ReLeDoorRdrObj15RdrObjV'], 'ReLeDoorRdrObj11': ['ReLeDoorRdrObj11RdrObjDstX', 'ReLeDoorRdrObj11RdrObjDstY', 'ReLeDoorRdrObj11RdrObjDstZ', 'ReLeDoorRdrObj11RdrObjV'], 'ReLeDoorRdrObj13': ['ReLeDoorRdrObj13RdrObjDstX', 'ReLeDoorRdrObj13RdrObjDstY', 'ReLeDoorRdrObj13RdrObjDstZ', 'ReLeDoorRdrObj13RdrObjV'], 'ReLeDoorRdrObj16': ['ReLeDoorRdrObj16RdrObjDstX', 'ReLeDoorRdrObj16RdrObjDstY', 'ReLeDoorRdrObj16RdrObjDstZ', 'ReLeDoorRdrObj16RdrObjV']}
    sig_group_dataid_dict = {}

    class ReLeDoorRdrObj15RdrObjDstY:
        sig_name = "ReLeDoorRdrObj15RdrObjDstY"
        sig_start_bit = 213
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
        startbit = 213
        bmuws_info = [(26, 0b00111111, 0b11000000, 6, 0), (27, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj9RdrObjDstX:
        sig_name = "ReLeDoorRdrObj9RdrObjDstX"
        sig_start_bit = 289
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
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj13RdrObjDstX:
        sig_name = "ReLeDoorRdrObj13RdrObjDstX"
        sig_start_bit = 121
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
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj10_UB:
        sig_name = "ReLeDoorRdrObj10_UB"
        sig_start_bit = 369
        update_id_bit = 369
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 369
        byte = 46
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ReLeDoorRdrObj12RdrObjDstX:
        sig_name = "ReLeDoorRdrObj12RdrObjDstX"
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

    class ReLeDoorRdrObj15RdrObjV:
        sig_name = "ReLeDoorRdrObj15RdrObjV"
        sig_start_bit = 247
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
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj11RdrObjDstX:
        sig_name = "ReLeDoorRdrObj11RdrObjDstX"
        sig_start_bit = 45
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
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj9RdrObjV:
        sig_name = "ReLeDoorRdrObj9RdrObjV"
        sig_start_bit = 323
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
        startbit = 323
        bmuws_info = [(40, 0b00001111, 0b11110000, 4, 0), (41, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj12RdrObjV:
        sig_name = "ReLeDoorRdrObj12RdrObjV"
        sig_start_bit = 83
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
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj10RdrObjDstY:
        sig_name = "ReLeDoorRdrObj10RdrObjDstY"
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

    class ReLeDoorRdrObj14_UB:
        sig_name = "ReLeDoorRdrObj14_UB"
        sig_start_bit = 389
        update_id_bit = 389
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 389
        byte = 48
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReLeDoorRdrObj11RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj11RdrObjDstZ"
        sig_start_bit = 51
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
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111100, 0b00000011, 6, 2)]

    class ReLeDoorRdrObj15RdrObjDstX:
        sig_name = "ReLeDoorRdrObj15RdrObjDstX"
        sig_start_bit = 225
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
        startbit = 225
        bmuws_info = [(28, 0b00000011, 0b11111100, 2, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj9RdrObjDstY:
        sig_name = "ReLeDoorRdrObj9RdrObjDstY"
        sig_start_bit = 311
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
        startbit = 311
        bmuws_info = [(38, 0b11111111, 0b00000000, 8, 0), (39, 0b11000000, 0b00111111, 2, 6)]

    class ReLeDoorRdrObj16RdrObjDstY:
        sig_name = "ReLeDoorRdrObj16RdrObjDstY"
        sig_start_bit = 271
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
        startbit = 271
        bmuws_info = [(33, 0b11111111, 0b00000000, 8, 0), (34, 0b11000000, 0b00111111, 2, 6)]

    class ReLeDoorRdrObj13RdrObjDstY:
        sig_name = "ReLeDoorRdrObj13RdrObjDstY"
        sig_start_bit = 143
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
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11000000, 0b00111111, 2, 6)]

    class ReLeDoorRdrObj12RdrObjDstY:
        sig_name = "ReLeDoorRdrObj12RdrObjDstY"
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

    class ReLeDoorRdrObj9RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj9RdrObjDstZ"
        sig_start_bit = 317
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
        startbit = 317
        bmuws_info = [(39, 0b00111111, 0b11000000, 6, 0), (40, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj13RdrObjV:
        sig_name = "ReLeDoorRdrObj13RdrObjV"
        sig_start_bit = 149
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
        startbit = 149
        bmuws_info = [(18, 0b00111111, 0b11000000, 6, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class ReLeDoorRdrObj12_UB:
        sig_name = "ReLeDoorRdrObj12_UB"
        sig_start_bit = 391
        update_id_bit = 391
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 391
        byte = 48
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReLeDoorRdrObj9_UB:
        sig_name = "ReLeDoorRdrObj9_UB"
        sig_start_bit = 386
        update_id_bit = 386
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 386
        byte = 48
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReLeDoorRdrObj14RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj14RdrObjDstZ"
        sig_start_bit = 175
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
        startbit = 175
        bmuws_info = [(21, 0b11111111, 0b00000000, 8, 0), (22, 0b11000000, 0b00111111, 2, 6)]

    class ReLeDoorRdrObj10RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj10RdrObjDstZ"
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

    class ReLeDoorRdrObj11RdrObjV:
        sig_name = "ReLeDoorRdrObj11RdrObjV"
        sig_start_bit = 79
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
        startbit = 79
        bmuws_info = [(9, 0b11111111, 0b00000000, 8, 0), (10, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj12RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj12RdrObjDstZ"
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

    class ReLeDoorRdrObj16RdrObjV:
        sig_name = "ReLeDoorRdrObj16RdrObjV"
        sig_start_bit = 251
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
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11111111, 0b00000000, 8, 0)]

    class RLRelsMotSts:
        sig_name = "RLRelsMotSts"
        sig_start_bit = 372
        update_id_bit = 393
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotSts_Inactive': 0, 'MotSts_Active': 1, 'MotSts_ResetActive': 2}
        compute_method = None
        length = 3
        startbit = 372
        byte = 46
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class ReLeDoorRdrObj15_UB:
        sig_name = "ReLeDoorRdrObj15_UB"
        sig_start_bit = 388
        update_id_bit = 388
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 388
        byte = 48
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReLeDoorRdrObj13RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj13RdrObjDstZ"
        sig_start_bit = 153
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
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj15RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj15RdrObjDstZ"
        sig_start_bit = 219
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
        startbit = 219
        bmuws_info = [(27, 0b00001111, 0b11110000, 4, 0), (28, 0b11111100, 0b00000011, 6, 2)]

    class ReLeDoorRdrObj11_UB:
        sig_name = "ReLeDoorRdrObj11_UB"
        sig_start_bit = 368
        update_id_bit = 368
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 368
        byte = 46
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReLeDoorRdrObj16RdrObjDstX:
        sig_name = "ReLeDoorRdrObj16RdrObjDstX"
        sig_start_bit = 283
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
        startbit = 283
        bmuws_info = [(35, 0b00001111, 0b11110000, 4, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class ReLeDoorRdrObj16RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj16RdrObjDstZ"
        sig_start_bit = 277
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
        startbit = 277
        bmuws_info = [(34, 0b00111111, 0b11000000, 6, 0), (35, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj13_UB:
        sig_name = "ReLeDoorRdrObj13_UB"
        sig_start_bit = 390
        update_id_bit = 390
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 390
        byte = 48
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ReLeDoorRdrObj14RdrObjDstY:
        sig_name = "ReLeDoorRdrObj14RdrObjDstY"
        sig_start_bit = 187
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
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111100, 0b00000011, 6, 2)]

    class ReLeDoorRdrObj11RdrObjDstY:
        sig_name = "ReLeDoorRdrObj11RdrObjDstY"
        sig_start_bit = 57
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
        startbit = 57
        bmuws_info = [(7, 0b00000011, 0b11111100, 2, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj14RdrObjDstX:
        sig_name = "ReLeDoorRdrObj14RdrObjDstX"
        sig_start_bit = 181
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
        startbit = 181
        bmuws_info = [(22, 0b00111111, 0b11000000, 6, 0), (23, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj14RdrObjV:
        sig_name = "ReLeDoorRdrObj14RdrObjV"
        sig_start_bit = 193
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
        startbit = 193
        bmuws_info = [(24, 0b00000011, 0b11111100, 2, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11000000, 0b00111111, 2, 6)]

    class ReLeDoorRdrObj10RdrObjV:
        sig_name = "ReLeDoorRdrObj10RdrObjV"
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

    class RLDoorLockStsResd:
        sig_name = "RLDoorLockStsResd"
        sig_start_bit = 365
        update_id_bit = 384
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
        startbit = 365
        byte = 45
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RLIceBreakMotSts:
        sig_name = "RLIceBreakMotSts"
        sig_start_bit = 375
        update_id_bit = 396
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MotSts_Inactive': 0, 'MotSts_Active': 1, 'MotSts_ResetActive': 2}
        compute_method = None
        length = 3
        startbit = 375
        byte = 46
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ReLeDoorRdrObj10RdrObjDstX:
        sig_name = "ReLeDoorRdrObj10RdrObjDstX"
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

    class ReLeDoorRdrObj16_UB:
        sig_name = "ReLeDoorRdrObj16_UB"
        sig_start_bit = 387
        update_id_bit = 387
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 387
        byte = 48
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RLLtchRelsSts:
        sig_name = "RLLtchRelsSts"
        sig_start_bit = 344
        update_id_bit = 395
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
        startbit = 344
        byte = 43
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class LCULPublicCANFDFr06:
    msg_name = "LCULPublicCANFDFr06"
    msg_id = 404
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "LCUL"
    rx_nodes = ['CCUMCUAD', 'LCUR']
    sig_group_dict = {'ReLeDoorRdrObj6': ['ReLeDoorRdrObj6RdrObjDstX', 'ReLeDoorRdrObj6RdrObjDstY', 'ReLeDoorRdrObj6RdrObjDstZ', 'ReLeDoorRdrObj6RdrObjV'], 'ReadingLiSecRowLeDrvSts': ['ReadingLiSecRowLeDrvStsLightErrorCode', 'ReadingLiSecRowLeDrvStsLightSts', 'ReadingLiSecRowLeDrvStsLiPerc'], 'ReLeDoorRdrObj7': ['ReLeDoorRdrObj7RdrObjDstX', 'ReLeDoorRdrObj7RdrObjDstY', 'ReLeDoorRdrObj7RdrObjDstZ', 'ReLeDoorRdrObj7RdrObjV'], 'ReLeDoorRdrObj1': ['ReLeDoorRdrObj1RdrObjDstX', 'ReLeDoorRdrObj1RdrObjDstY', 'ReLeDoorRdrObj1RdrObjDstZ', 'ReLeDoorRdrObj1RdrObjV'], 'ReLeDoorRdrObj4': ['ReLeDoorRdrObj4RdrObjDstX', 'ReLeDoorRdrObj4RdrObjDstY', 'ReLeDoorRdrObj4RdrObjDstZ', 'ReLeDoorRdrObj4RdrObjV'], 'ReadingLiSecRowRiDrvSts': ['ReadingLiSecRowRiDrvStsLightErrorCode', 'ReadingLiSecRowRiDrvStsLightSts', 'ReadingLiSecRowRiDrvStsLiPerc'], 'ReadingLiThrdRowLeDrvSts': ['ReadingLiThrdRowLeDrvStsLightErrorCode', 'ReadingLiThrdRowLeDrvStsLightSts', 'ReadingLiThrdRowLeDrvStsLiPerc'], 'ReLeDoorRdrObj2': ['ReLeDoorRdrObj2RdrObjDstX', 'ReLeDoorRdrObj2RdrObjDstY', 'ReLeDoorRdrObj2RdrObjDstZ', 'ReLeDoorRdrObj2RdrObjV'], 'ReadingLiFrntRiDrvSts': ['ReadingLiFrntRiDrvStsLightErrorCode', 'ReadingLiFrntRiDrvStsLightSts', 'ReadingLiFrntRiDrvStsLiPerc'], 'ReLeDoorRdrObj3': ['ReLeDoorRdrObj3RdrObjDstX', 'ReLeDoorRdrObj3RdrObjDstY', 'ReLeDoorRdrObj3RdrObjDstZ', 'ReLeDoorRdrObj3RdrObjV'], 'ReadingLiFrntLeDrvSts': ['ReadingLiFrntLeDrvStsLightErrorCode', 'ReadingLiFrntLeDrvStsLightSts', 'ReadingLiFrntLeDrvStsLiPerc'], 'ReLeDoorRdrObj5': ['ReLeDoorRdrObj5RdrObjDstX', 'ReLeDoorRdrObj5RdrObjDstY', 'ReLeDoorRdrObj5RdrObjDstZ', 'ReLeDoorRdrObj5RdrObjV'], 'ReLeDoorRdrObj8': ['ReLeDoorRdrObj8RdrObjDstX', 'ReLeDoorRdrObj8RdrObjDstY', 'ReLeDoorRdrObj8RdrObjDstZ', 'ReLeDoorRdrObj8RdrObjV'], 'ReadingLiThrdRowRiDrvSts': ['ReadingLiThrdRowRiDrvStsLightErrorCode', 'ReadingLiThrdRowRiDrvStsLightSts', 'ReadingLiThrdRowRiDrvStsLiPerc']}
    sig_group_dataid_dict = {}

    class ReLeDoorRdrObj1RdrObjDstX:
        sig_name = "ReLeDoorRdrObj1RdrObjDstX"
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

    class ReLeDoorRdrObj6_UB:
        sig_name = "ReLeDoorRdrObj6_UB"
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

    class ReadingLiSecRowLeDrvStsLightErrorCode:
        sig_name = "ReadingLiSecRowLeDrvStsLightErrorCode"
        sig_start_bit = 383
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 383
        byte = 47
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReLeDoorRdrObj5RdrObjDstY:
        sig_name = "ReLeDoorRdrObj5RdrObjDstY"
        sig_start_bit = 179
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
        startbit = 179
        bmuws_info = [(22, 0b00001111, 0b11110000, 4, 0), (23, 0b11111100, 0b00000011, 6, 2)]

    class ReLeDoorRdrObj5RdrObjDstX:
        sig_name = "ReLeDoorRdrObj5RdrObjDstX"
        sig_start_bit = 185
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
        startbit = 185
        bmuws_info = [(23, 0b00000011, 0b11111100, 2, 0), (24, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj1RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj1RdrObjDstZ"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class ReLeDoorRdrObj2RdrObjDstX:
        sig_name = "ReLeDoorRdrObj2RdrObjDstX"
        sig_start_bit = 45
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
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class ReadingLiSecRowLeDrvStsLiPerc:
        sig_name = "ReadingLiSecRowLeDrvStsLiPerc"
        sig_start_bit = 391
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 391
        byte = 48
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLiThrdRowLeDrvStsLiPerc:
        sig_name = "ReadingLiThrdRowLeDrvStsLiPerc"
        sig_start_bit = 431
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 431
        byte = 53
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLiFrntRiDrvStsLightSts:
        sig_name = "ReadingLiFrntRiDrvStsLightSts"
        sig_start_bit = 355
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 355
        byte = 44
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReLeDoorRdrObj3RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj3RdrObjDstZ"
        sig_start_bit = 83
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
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11111100, 0b00000011, 6, 2)]

    class ReadingLiFrntLeDrvStsLightErrorCode:
        sig_name = "ReadingLiFrntLeDrvStsLightErrorCode"
        sig_start_bit = 343
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 343
        byte = 42
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReadingLiThrdRowRiDrvStsLightSts:
        sig_name = "ReadingLiThrdRowRiDrvStsLightSts"
        sig_start_bit = 435
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 435
        byte = 54
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReLeDoorRdrObj3RdrObjDstX:
        sig_name = "ReLeDoorRdrObj3RdrObjDstX"
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

    class ReadingLiSecRowLeDrvSts_UB:
        sig_name = "ReadingLiSecRowLeDrvSts_UB"
        sig_start_bit = 448
        update_id_bit = 448
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 448
        byte = 56
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReLeDoorRdrObj4RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj4RdrObjDstZ"
        sig_start_bit = 121
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
        startbit = 121
        bmuws_info = [(15, 0b00000011, 0b11111100, 2, 0), (16, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj8RdrObjDstY:
        sig_name = "ReLeDoorRdrObj8RdrObjDstY"
        sig_start_bit = 289
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
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111111, 0b00000000, 8, 0)]

    class ReadingLiThrdRowLeDrvStsLightSts:
        sig_name = "ReadingLiThrdRowLeDrvStsLightSts"
        sig_start_bit = 439
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 439
        byte = 54
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ReLeDoorRdrObj6RdrObjV:
        sig_name = "ReLeDoorRdrObj6RdrObjV"
        sig_start_bit = 213
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
        startbit = 213
        bmuws_info = [(26, 0b00111111, 0b11000000, 6, 0), (27, 0b11111100, 0b00000011, 6, 2)]

    class ReLeDoorRdrObj3RdrObjDstY:
        sig_name = "ReLeDoorRdrObj3RdrObjDstY"
        sig_start_bit = 89
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
        startbit = 89
        bmuws_info = [(11, 0b00000011, 0b11111100, 2, 0), (12, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj1RdrObjDstY:
        sig_name = "ReLeDoorRdrObj1RdrObjDstY"
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

    class ReLeDoorRdrObj1RdrObjV:
        sig_name = "ReLeDoorRdrObj1RdrObjV"
        sig_start_bit = 19
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
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj7_UB:
        sig_name = "ReLeDoorRdrObj7_UB"
        sig_start_bit = 479
        update_id_bit = 479
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 479
        byte = 59
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReLeDoorRdrObj1_UB:
        sig_name = "ReLeDoorRdrObj1_UB"
        sig_start_bit = 469
        update_id_bit = 469
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 469
        byte = 58
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReLeDoorRdrObj4_UB:
        sig_name = "ReLeDoorRdrObj4_UB"
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

    class ReadingLiSecRowRiDrvSts_UB:
        sig_name = "ReadingLiSecRowRiDrvSts_UB"
        sig_start_bit = 458
        update_id_bit = 458
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 458
        byte = 57
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReadingLiThrdRowLeDrvSts_UB:
        sig_name = "ReadingLiThrdRowLeDrvSts_UB"
        sig_start_bit = 457
        update_id_bit = 457
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 457
        byte = 57
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ReadingLiThrdRowRiDrvStsLiPerc:
        sig_name = "ReadingLiThrdRowRiDrvStsLiPerc"
        sig_start_bit = 455
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 455
        byte = 56
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLiFrntLeDrvStsLiPerc:
        sig_name = "ReadingLiFrntLeDrvStsLiPerc"
        sig_start_bit = 351
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 351
        byte = 43
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReLeDoorRdrObj7RdrObjV:
        sig_name = "ReLeDoorRdrObj7RdrObjV"
        sig_start_bit = 279
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
        startbit = 279
        bmuws_info = [(34, 0b11111111, 0b00000000, 8, 0), (35, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj2_UB:
        sig_name = "ReLeDoorRdrObj2_UB"
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

    class ReadingLiSecRowRiDrvStsLightErrorCode:
        sig_name = "ReadingLiSecRowRiDrvStsLightErrorCode"
        sig_start_bit = 407
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 407
        byte = 50
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReadingLiSecRowLeDrvStsLightSts:
        sig_name = "ReadingLiSecRowLeDrvStsLightSts"
        sig_start_bit = 399
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 399
        byte = 49
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ReadingLiFrntRiDrvSts_UB:
        sig_name = "ReadingLiFrntRiDrvSts_UB"
        sig_start_bit = 408
        update_id_bit = 408
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 408
        byte = 51
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReLeDoorRdrObj7RdrObjDstY:
        sig_name = "ReLeDoorRdrObj7RdrObjDstY"
        sig_start_bit = 251
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
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11111100, 0b00000011, 6, 2)]

    class ReLeDoorRdrObj4RdrObjDstX:
        sig_name = "ReLeDoorRdrObj4RdrObjDstX"
        sig_start_bit = 147
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
        startbit = 147
        bmuws_info = [(18, 0b00001111, 0b11110000, 4, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class ReLeDoorRdrObj2RdrObjV:
        sig_name = "ReLeDoorRdrObj2RdrObjV"
        sig_start_bit = 51
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
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj3_UB:
        sig_name = "ReLeDoorRdrObj3_UB"
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

    class ReLeDoorRdrObj2RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj2RdrObjDstZ"
        sig_start_bit = 71
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
        startbit = 71
        bmuws_info = [(8, 0b11111111, 0b00000000, 8, 0), (9, 0b11000000, 0b00111111, 2, 6)]

    class ReLeDoorRdrObj4RdrObjDstY:
        sig_name = "ReLeDoorRdrObj4RdrObjDstY"
        sig_start_bit = 153
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
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj4RdrObjV:
        sig_name = "ReLeDoorRdrObj4RdrObjV"
        sig_start_bit = 143
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
        startbit = 143
        bmuws_info = [(17, 0b11111111, 0b00000000, 8, 0), (18, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj6RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj6RdrObjDstZ"
        sig_start_bit = 239
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
        startbit = 239
        bmuws_info = [(29, 0b11111111, 0b00000000, 8, 0), (30, 0b11000000, 0b00111111, 2, 6)]

    class ReLeDoorRdrObj8RdrObjDstX:
        sig_name = "ReLeDoorRdrObj8RdrObjDstX"
        sig_start_bit = 321
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
        startbit = 321
        bmuws_info = [(40, 0b00000011, 0b11111100, 2, 0), (41, 0b11111111, 0b00000000, 8, 0)]

    class ReadingLiFrntLeDrvStsLightSts:
        sig_name = "ReadingLiFrntLeDrvStsLightSts"
        sig_start_bit = 359
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 359
        byte = 44
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ReLeDoorRdrObj5RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj5RdrObjDstZ"
        sig_start_bit = 207
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
        startbit = 207
        bmuws_info = [(25, 0b11111111, 0b00000000, 8, 0), (26, 0b11000000, 0b00111111, 2, 6)]

    class ReadingLiFrntLeDrvSts_UB:
        sig_name = "ReadingLiFrntLeDrvSts_UB"
        sig_start_bit = 368
        update_id_bit = 368
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 368
        byte = 46
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReadingLiFrntRiDrvStsLiPerc:
        sig_name = "ReadingLiFrntRiDrvStsLiPerc"
        sig_start_bit = 375
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 375
        byte = 46
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLiThrdRowRiDrvStsLightErrorCode:
        sig_name = "ReadingLiThrdRowRiDrvStsLightErrorCode"
        sig_start_bit = 447
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 447
        byte = 55
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReLeDoorRdrObj7RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj7RdrObjDstZ"
        sig_start_bit = 257
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
        startbit = 257
        bmuws_info = [(32, 0b00000011, 0b11111100, 2, 0), (33, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj7RdrObjDstX:
        sig_name = "ReLeDoorRdrObj7RdrObjDstX"
        sig_start_bit = 283
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
        startbit = 283
        bmuws_info = [(35, 0b00001111, 0b11110000, 4, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class ReadingLiSecRowRiDrvStsLightSts:
        sig_name = "ReadingLiSecRowRiDrvStsLightSts"
        sig_start_bit = 395
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 395
        byte = 49
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReLeDoorRdrMod:
        sig_name = "ReLeDoorRdrMod"
        sig_start_bit = 460
        update_id_bit = 470
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
        startbit = 460
        byte = 57
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class ReadingLiFrntRiDrvStsLightErrorCode:
        sig_name = "ReadingLiFrntRiDrvStsLightErrorCode"
        sig_start_bit = 367
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 367
        byte = 45
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReadingLiSecRowRiDrvStsLiPerc:
        sig_name = "ReadingLiSecRowRiDrvStsLiPerc"
        sig_start_bit = 415
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 415
        byte = 51
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReLeDoorRdrObj5_UB:
        sig_name = "ReLeDoorRdrObj5_UB"
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

    class ReLeDoorRdrObj6RdrObjDstY:
        sig_name = "ReLeDoorRdrObj6RdrObjDstY"
        sig_start_bit = 217
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
        startbit = 217
        bmuws_info = [(27, 0b00000011, 0b11111100, 2, 0), (28, 0b11111111, 0b00000000, 8, 0)]

    class ReLeDoorRdrObj6RdrObjDstX:
        sig_name = "ReLeDoorRdrObj6RdrObjDstX"
        sig_start_bit = 245
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
        startbit = 245
        bmuws_info = [(30, 0b00111111, 0b11000000, 6, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj8RdrObjDstZ:
        sig_name = "ReLeDoorRdrObj8RdrObjDstZ"
        sig_start_bit = 311
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
        startbit = 311
        bmuws_info = [(38, 0b11111111, 0b00000000, 8, 0), (39, 0b11000000, 0b00111111, 2, 6)]

    class ReLeDoorRdrObj8RdrObjV:
        sig_name = "ReLeDoorRdrObj8RdrObjV"
        sig_start_bit = 317
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
        startbit = 317
        bmuws_info = [(39, 0b00111111, 0b11000000, 6, 0), (40, 0b11111100, 0b00000011, 6, 2)]

    class ReLeDoorRdrObj3RdrObjV:
        sig_name = "ReLeDoorRdrObj3RdrObjV"
        sig_start_bit = 111
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
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj5RdrObjV:
        sig_name = "ReLeDoorRdrObj5RdrObjV"
        sig_start_bit = 175
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
        startbit = 175
        bmuws_info = [(21, 0b11111111, 0b00000000, 8, 0), (22, 0b11110000, 0b00001111, 4, 4)]

    class ReLeDoorRdrObj8_UB:
        sig_name = "ReLeDoorRdrObj8_UB"
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

    class ReadingLiThrdRowLeDrvStsLightErrorCode:
        sig_name = "ReadingLiThrdRowLeDrvStsLightErrorCode"
        sig_start_bit = 423
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 423
        byte = 52
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReLeDoorRdrObj2RdrObjDstY:
        sig_name = "ReLeDoorRdrObj2RdrObjDstY"
        sig_start_bit = 77
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
        startbit = 77
        bmuws_info = [(9, 0b00111111, 0b11000000, 6, 0), (10, 0b11110000, 0b00001111, 4, 4)]

    class ReadingLiThrdRowRiDrvSts_UB:
        sig_name = "ReadingLiThrdRowRiDrvSts_UB"
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

    class ReLeDoorRdrFlt:
        sig_name = "ReLeDoorRdrFlt"
        sig_start_bit = 463
        update_id_bit = 471
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
        startbit = 463
        byte = 57
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CCUMCUCDPublicCANFDFr04:
    msg_name = "CCUMCUCDPublicCANFDFr04"
    msg_id = 401
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "CCUMCUCD"
    rx_nodes = ['LCUL', 'ETC', 'LCUR', 'VCU']
    sig_group_dict = {'DoorLockCmdResd': ['DoorLockCmdResdFLDoorLockCmd', 'DoorLockCmdResdFRDoorLockCmd', 'DoorLockCmdResdRLDoorLockCmd', 'DoorLockCmdResdRRDoorLockCmd'], 'FLPwrSideDoorCtrlReq': ['FLPwrSideDoorCtrlReqChks', 'FLPwrSideDoorCtrlReqCntr', 'FLPwrSideDoorCtrlReqPwrSideDoorCtrlReq', 'FLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc'], 'RRPwrSideDoorCtrlReq': ['RRPwrSideDoorCtrlReqChks', 'RRPwrSideDoorCtrlReqCntr', 'RRPwrSideDoorCtrlReqPwrSideDoorCtrlReq', 'RRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc'], 'FRPwrSideDoorCtrlReq': ['FRPwrSideDoorCtrlReqChks', 'FRPwrSideDoorCtrlReqCntr', 'FRPwrSideDoorCtrlReqPwrSideDoorCtrlReq', 'FRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc'], 'Odometer': ['OdometerValidity', 'OdometerValue'], 'RLPwrSideDoorCtrlReq': ['RLPwrSideDoorCtrlReqChks', 'RLPwrSideDoorCtrlReqCntr', 'RLPwrSideDoorCtrlReqPwrSideDoorCtrlReq', 'RLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc'], 'CentralLockSts': ['CentralLockStsCenLockSts', 'CentralLockStsTrigSrc', 'CentralLockStsTrigSrcType', 'CentralLockStsUpdateEvnt']}
    sig_group_dataid_dict = {}

    class RRLtchRelsReq:
        sig_name = "RRLtchRelsReq"
        sig_start_bit = 150
        update_id_bit = 246
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
        startbit = 150
        byte = 18
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FRRdrEnadCtrlReq:
        sig_name = "FRRdrEnadCtrlReq"
        sig_start_bit = 87
        update_id_bit = 177
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
        startbit = 87
        byte = 10
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FLLtchRelsReq:
        sig_name = "FLLtchRelsReq"
        sig_start_bit = 21
        update_id_bit = 148
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

    class RRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc:
        sig_name = "RRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc"
        sig_start_bit = 167
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
        startbit = 167
        byte = 20
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DoorLockCmdResd_UB:
        sig_name = "DoorLockCmdResd_UB"
        sig_start_bit = 128
        update_id_bit = 128
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 128
        byte = 16
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FLPwrSideDoorCtrlReq_UB:
        sig_name = "FLPwrSideDoorCtrlReq_UB"
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

    class DoorLockCmdResdFLDoorLockCmd:
        sig_name = "DoorLockCmdResdFLDoorLockCmd"
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
        sig_value_table = {'LockCmd_Idle': 0, 'LockCmd_LockCmd': 1, 'LockCmd_UnLockCmd': 2, 'LockCmd_CrashUnLockCmd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RRPwrSideDoorCtrlReqPwrSideDoorCtrlReq:
        sig_name = "RRPwrSideDoorCtrlReqPwrSideDoorCtrlReq"
        sig_start_bit = 146
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
        startbit = 146
        byte = 18
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DoorLockCmdResdRLDoorLockCmd:
        sig_name = "DoorLockCmdResdRLDoorLockCmd"
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
        sig_value_table = {'LockCmd_Idle': 0, 'LockCmd_LockCmd': 1, 'LockCmd_UnLockCmd': 2, 'LockCmd_CrashUnLockCmd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class TrPosnSet:
        sig_name = "TrPosnSet"
        sig_start_bit = 191
        update_id_bit = 241
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
        startbit = 191
        byte = 23
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CarLoctrAcoustReq:
        sig_name = "CarLoctrAcoustReq"
        sig_start_bit = 7
        update_id_bit = 32
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

    class CarLoctrActvnSts:
        sig_name = "CarLoctrActvnSts"
        sig_start_bit = 5
        update_id_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvnSts_Idle': 0, 'ActvnSts_Successful': 1, 'ActvnSts_Fail': 2, 'ActvnSts_Resvd': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RiElecPedlCtrlReq:
        sig_name = "RiElecPedlCtrlReq"
        sig_start_bit = 82
        update_id_bit = 203
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ElecPedlCtrlReq_Idle': 0, 'ElecPedlCtrlReq_Open': 1, 'ElecPedlCtrlReq_Close': 2, 'ElecPedlCtrlReq_Resd1': 3, 'ElecPedlCtrlReq_Resd2': 4, 'ElecPedlCtrlReq_Resd3': 5}
        compute_method = None
        length = 3
        startbit = 82
        byte = 10
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class RLLtchRelsReq:
        sig_name = "RLLtchRelsReq"
        sig_start_bit = 105
        update_id_bit = 202
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
        startbit = 105
        byte = 13
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FRPwrSideDoorCtrlReqPwrSideDoorCtrlReq:
        sig_name = "FRPwrSideDoorCtrlReqPwrSideDoorCtrlReq"
        sig_start_bit = 50
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
        startbit = 50
        byte = 6
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class FRPwrSideDoorCtrlReqChks:
        sig_name = "FRPwrSideDoorCtrlReqChks"
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

    class RRPwrSideDoorCtrlReqCntr:
        sig_name = "RRPwrSideDoorCtrlReqCntr"
        sig_start_bit = 163
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
        startbit = 163
        byte = 20
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FLRdrEnadCtrlReq:
        sig_name = "FLRdrEnadCtrlReq"
        sig_start_bit = 55
        update_id_bit = 181
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

    class VehBattU:
        sig_name = "VehBattU"
        sig_start_bit = 199
        update_id_bit = 255
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
        startbit = 199
        bmuws_info = [(24, 0b11111111, 0b00000000, 8, 0), (25, 0b11000000, 0b00111111, 2, 6)]

    class RLPwrSideDoorCtrlReqCntr:
        sig_name = "RLPwrSideDoorCtrlReqCntr"
        sig_start_bit = 115
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
        startbit = 115
        byte = 14
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CentralLockStsTrigSrc:
        sig_name = "CentralLockStsTrigSrc"
        sig_start_bit = 261
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
        startbit = 261
        byte = 32
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class FLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc:
        sig_name = "FLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ChrgLidCtrlReq:
        sig_name = "ChrgLidCtrlReq"
        sig_start_bit = 15
        update_id_bit = 104
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
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TrRelsReq:
        sig_name = "TrRelsReq"
        sig_start_bit = 149
        update_id_bit = 240
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
        startbit = 149
        byte = 18
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FLPwrSideDoorCtrlReqCntr:
        sig_name = "FLPwrSideDoorCtrlReqCntr"
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

    class RRPwrSideDoorCtrlReq_UB:
        sig_name = "RRPwrSideDoorCtrlReq_UB"
        sig_start_bit = 245
        update_id_bit = 245
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 245
        byte = 30
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VehTiGlb:
        sig_name = "VehTiGlb"
        sig_start_bit = 215
        update_id_bit = 254
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
        startbit = 215
        bmuws_info = [(26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0), (28, 0b11111111, 0b00000000, 8, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class RLPwrSideDoorCtrlReqPwrSideDoorCtrlReq:
        sig_name = "RLPwrSideDoorCtrlReqPwrSideDoorCtrlReq"
        sig_start_bit = 135
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
        startbit = 135
        byte = 16
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class FRPwrSideDoorCtrlReq_UB:
        sig_name = "FRPwrSideDoorCtrlReq_UB"
        sig_start_bit = 179
        update_id_bit = 179
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 179
        byte = 22
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HoodLtchRelsReq:
        sig_name = "HoodLtchRelsReq"
        sig_start_bit = 86
        update_id_bit = 176
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
        startbit = 86
        byte = 10
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CarLoctrHornLiSetActv:
        sig_name = "CarLoctrHornLiSetActv"
        sig_start_bit = 3
        update_id_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HornLiSetActv_NoReq': 0, 'HornLiSetActv_HornLiSetActv': 1, 'HornLiSetActv_HornSetActv': 2, 'HornLiSetActv_LiSetActv': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class RRRdrEnadCtrlReq:
        sig_name = "RRRdrEnadCtrlReq"
        sig_start_bit = 183
        update_id_bit = 243
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
        startbit = 183
        byte = 22
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class LeElecPedlCtrlReq:
        sig_name = "LeElecPedlCtrlReq"
        sig_start_bit = 85
        update_id_bit = 205
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ElecPedlCtrlReq_Idle': 0, 'ElecPedlCtrlReq_Open': 1, 'ElecPedlCtrlReq_Close': 2, 'ElecPedlCtrlReq_Resd1': 3, 'ElecPedlCtrlReq_Resd2': 4, 'ElecPedlCtrlReq_Resd3': 5}
        compute_method = None
        length = 3
        startbit = 85
        byte = 10
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class RRPwrSideDoorCtrlReqChks:
        sig_name = "RRPwrSideDoorCtrlReqChks"
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

    class DoorLockCmdResdFRDoorLockCmd:
        sig_name = "DoorLockCmdResdFRDoorLockCmd"
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
        sig_value_table = {'LockCmd_Idle': 0, 'LockCmd_LockCmd': 1, 'LockCmd_UnLockCmd': 2, 'LockCmd_CrashUnLockCmd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FRLtchRelsReq:
        sig_name = "FRLtchRelsReq"
        sig_start_bit = 54
        update_id_bit = 180
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

    class CentralLockStsUpdateEvnt:
        sig_name = "CentralLockStsUpdateEvnt"
        sig_start_bit = 256
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
        startbit = 256
        byte = 32
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CentralLockStsCenLockSts:
        sig_name = "CentralLockStsCenLockSts"
        sig_start_bit = 263
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
        startbit = 263
        byte = 32
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TrCtrlReq:
        sig_name = "TrCtrlReq"
        sig_start_bit = 132
        update_id_bit = 242
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
        startbit = 132
        byte = 16
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class CenLockExtrLiReq:
        sig_name = "CenLockExtrLiReq"
        sig_start_bit = 1
        update_id_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockExtLiReq_NoReq': 0, 'LockExtLiReq_UnlockExtrLiReq': 1, 'LockExtLiReq_LockExtrLiReq': 2}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorLockCmdResdRRDoorLockCmd:
        sig_name = "DoorLockCmdResdRRDoorLockCmd"
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
        sig_value_table = {'LockCmd_Idle': 0, 'LockCmd_LockCmd': 1, 'LockCmd_UnLockCmd': 2, 'LockCmd_CrashUnLockCmd': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class OdometerValue:
        sig_name = "OdometerValue"
        sig_start_bit = 95
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
        startbit = 95
        bmuws_info = [(11, 0b11111111, 0b00000000, 8, 0), (12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111000, 0b00000111, 5, 3)]

    class Odometer_UB:
        sig_name = "Odometer_UB"
        sig_start_bit = 204
        update_id_bit = 204
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 204
        byte = 25
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc:
        sig_name = "FRPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RLRdrEnadCtrlReq:
        sig_name = "RLRdrEnadCtrlReq"
        sig_start_bit = 151
        update_id_bit = 247
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
        startbit = 151
        byte = 18
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FLPwrSideDoorCtrlReqChks:
        sig_name = "FLPwrSideDoorCtrlReqChks"
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

    class FRPwrSideDoorCtrlReqCntr:
        sig_name = "FRPwrSideDoorCtrlReqCntr"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc:
        sig_name = "RLPwrSideDoorCtrlReqPwrSideDoorCtrlTrigSrc"
        sig_start_bit = 119
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
        startbit = 119
        byte = 14
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RLPwrSideDoorCtrlReq_UB:
        sig_name = "RLPwrSideDoorCtrlReq_UB"
        sig_start_bit = 201
        update_id_bit = 201
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 201
        byte = 25
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CentralLockSts_UB:
        sig_name = "CentralLockSts_UB"
        sig_start_bit = 269
        update_id_bit = 269
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 269
        byte = 33
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RLPwrSideDoorCtrlReqChks:
        sig_name = "RLPwrSideDoorCtrlReqChks"
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

    class CentralLockStsTrigSrcType:
        sig_name = "CentralLockStsTrigSrcType"
        sig_start_bit = 271
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
        startbit = 271
        byte = 33
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FLPwrSideDoorCtrlReqPwrSideDoorCtrlReq:
        sig_name = "FLPwrSideDoorCtrlReqPwrSideDoorCtrlReq"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class OdometerValidity:
        sig_name = "OdometerValidity"
        sig_start_bit = 106
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
        startbit = 106
        byte = 13
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class CCUMCUCDPublicCANFDFr01:
    msg_name = "CCUMCUCDPublicCANFDFr01"
    msg_id = 48
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.005
    msg_length = 16
    tx_node = "CCUMCUCD"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {'ADSSlaveALgtReq': ['ADSSlaveALgtReqChks', 'ADSSlaveALgtReqCntr', 'ADSSlaveALgtReqMax', 'ADSSlaveALgtReqMin'], 'ADSSlaveAccrOvrdnAllwd': ['ADSSlaveAccrOvrdnAllwdChks', 'ADSSlaveAccrOvrdnAllwdCntr', 'ADSSlaveAccrOvrdnAllwdYesNo1'], 'ADSSlaveGearShiftReq': ['ADSSlaveGearShiftReqChks', 'ADSSlaveGearShiftReqCntr', 'ADSSlaveGearShiftReqGearPrkgAssiReq1']}
    sig_group_dataid_dict = {}

    class ADSSlaveALgtReq_UB:
        sig_name = "ADSSlaveALgtReq_UB"
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

    class ADSSlaveGearShiftReqCntr:
        sig_name = "ADSSlaveGearShiftReqCntr"
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

    class ADSSlaveAccrOvrdnAllwdChks:
        sig_name = "ADSSlaveAccrOvrdnAllwdChks"
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

    class ADSSlaveAccrOvrdnAllwd_UB:
        sig_name = "ADSSlaveAccrOvrdnAllwd_UB"
        sig_start_bit = 10
        update_id_bit = 10
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ADSSlaveALgtReqMin:
        sig_name = "ADSSlaveALgtReqMin"
        sig_start_bit = 47
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
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class ADSSlaveALgtReqCntr:
        sig_name = "ADSSlaveALgtReqCntr"
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

    class ADSSlaveALgtReqChks:
        sig_name = "ADSSlaveALgtReqChks"
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

    class ADSSlaveALgtReqMax:
        sig_name = "ADSSlaveALgtReqMax"
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

    class ADSSlaveGearShiftReqChks:
        sig_name = "ADSSlaveGearShiftReqChks"
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

    class ADSSlaveGearShiftReqGearPrkgAssiReq1:
        sig_name = "ADSSlaveGearShiftReqGearPrkgAssiReq1"
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
        sig_value_table = {'GearPrkgAssiReq1_NoRequest': 0, 'GearPrkgAssiReq1_TargetgearP': 1, 'GearPrkgAssiReq1_TargetgearR': 2, 'GearPrkgAssiReq1_TargetgearD': 3}
        compute_method = None
        length = 2
        startbit = 71
        byte = 8
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ADSSlaveAccrOvrdnAllwdYesNo1:
        sig_name = "ADSSlaveAccrOvrdnAllwdYesNo1"
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
        sig_value_table = {'YesNo1_Yes': 0, 'YesNo1_No': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ADSSlaveGearShiftReq_UB:
        sig_name = "ADSSlaveGearShiftReq_UB"
        sig_start_bit = 8
        update_id_bit = 8
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ADSSlaveAccrOvrdnAllwdCntr:
        sig_name = "ADSSlaveAccrOvrdnAllwdCntr"
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


class LCURPublicCANFDFr05:
    msg_name = "LCURPublicCANFDFr05"
    msg_id = 407
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 64
    tx_node = "LCUR"
    rx_nodes = ['CCUMCUAD']
    sig_group_dict = {'FrntRiDoorRdrObj16': ['FrntRiDoorRdrObj16RdrObjDstX', 'FrntRiDoorRdrObj16RdrObjDstY', 'FrntRiDoorRdrObj16RdrObjDstZ', 'FrntRiDoorRdrObj16RdrObjV'], 'FrntRiDoorRdrObj10': ['FrntRiDoorRdrObj10RdrObjDstX', 'FrntRiDoorRdrObj10RdrObjDstY', 'FrntRiDoorRdrObj10RdrObjDstZ', 'FrntRiDoorRdrObj10RdrObjV'], 'FrntRiDoorRdrObj13': ['FrntRiDoorRdrObj13RdrObjDstX', 'FrntRiDoorRdrObj13RdrObjDstY', 'FrntRiDoorRdrObj13RdrObjDstZ', 'FrntRiDoorRdrObj13RdrObjV'], 'FrntRiDoorRdrObj12': ['FrntRiDoorRdrObj12RdrObjDstX', 'FrntRiDoorRdrObj12RdrObjDstY', 'FrntRiDoorRdrObj12RdrObjDstZ', 'FrntRiDoorRdrObj12RdrObjV'], 'FrntRiDoorRdrObj11': ['FrntRiDoorRdrObj11RdrObjDstX', 'FrntRiDoorRdrObj11RdrObjDstY', 'FrntRiDoorRdrObj11RdrObjDstZ', 'FrntRiDoorRdrObj11RdrObjV'], 'FrntRiDoorRdrObj15': ['FrntRiDoorRdrObj15RdrObjDstX', 'FrntRiDoorRdrObj15RdrObjDstY', 'FrntRiDoorRdrObj15RdrObjDstZ', 'FrntRiDoorRdrObj15RdrObjV'], 'FrntRiDoorRdrObj14': ['FrntRiDoorRdrObj14RdrObjDstX', 'FrntRiDoorRdrObj14RdrObjDstY', 'FrntRiDoorRdrObj14RdrObjDstZ', 'FrntRiDoorRdrObj14RdrObjV'], 'FrntRiDoorRdrObj9': ['FrntRiDoorRdrObj9RdrObjDstX', 'FrntRiDoorRdrObj9RdrObjDstY', 'FrntRiDoorRdrObj9RdrObjDstZ', 'FrntRiDoorRdrObj9RdrObjV']}
    sig_group_dataid_dict = {}

    class FrntRiDoorRdrObj14RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj14RdrObjDstZ"
        sig_start_bit = 181
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
        startbit = 181
        bmuws_info = [(22, 0b00111111, 0b11000000, 6, 0), (23, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj10RdrObjV:
        sig_name = "FrntRiDoorRdrObj10RdrObjV"
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

    class FrntRiDoorRdrObj9RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj9RdrObjDstY"
        sig_start_bit = 311
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
        startbit = 311
        bmuws_info = [(38, 0b11111111, 0b00000000, 8, 0), (39, 0b11000000, 0b00111111, 2, 6)]

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

    class FrntRiDoorRdrObj16_UB:
        sig_name = "FrntRiDoorRdrObj16_UB"
        sig_start_bit = 337
        update_id_bit = 337
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 337
        byte = 42
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntRiDoorRdrObj11RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj11RdrObjDstX"
        sig_start_bit = 51
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
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj10_UB:
        sig_name = "FrntRiDoorRdrObj10_UB"
        sig_start_bit = 343
        update_id_bit = 343
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 343
        byte = 42
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FrntRiDoorRdrObj14RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj14RdrObjDstY"
        sig_start_bit = 187
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
        startbit = 187
        bmuws_info = [(23, 0b00001111, 0b11110000, 4, 0), (24, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj16RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj16RdrObjDstZ"
        sig_start_bit = 257
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
        startbit = 257
        bmuws_info = [(32, 0b00000011, 0b11111100, 2, 0), (33, 0b11111111, 0b00000000, 8, 0)]

    class FrntRiDoorRdrObj13_UB:
        sig_name = "FrntRiDoorRdrObj13_UB"
        sig_start_bit = 340
        update_id_bit = 340
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 340
        byte = 42
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntRiDoorRdrObj12_UB:
        sig_name = "FrntRiDoorRdrObj12_UB"
        sig_start_bit = 341
        update_id_bit = 341
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 341
        byte = 42
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntRiDoorRdrObj11RdrObjV:
        sig_name = "FrntRiDoorRdrObj11RdrObjV"
        sig_start_bit = 57
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
        startbit = 57
        bmuws_info = [(7, 0b00000011, 0b11111100, 2, 0), (8, 0b11111111, 0b00000000, 8, 0), (9, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj11RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj11RdrObjDstZ"
        sig_start_bit = 77
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
        startbit = 77
        bmuws_info = [(9, 0b00111111, 0b11000000, 6, 0), (10, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj13RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj13RdrObjDstZ"
        sig_start_bit = 147
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
        startbit = 147
        bmuws_info = [(18, 0b00001111, 0b11110000, 4, 0), (19, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj16RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj16RdrObjDstX"
        sig_start_bit = 251
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
        startbit = 251
        bmuws_info = [(31, 0b00001111, 0b11110000, 4, 0), (32, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj16RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj16RdrObjDstY"
        sig_start_bit = 283
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
        startbit = 283
        bmuws_info = [(35, 0b00001111, 0b11110000, 4, 0), (36, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj16RdrObjV:
        sig_name = "FrntRiDoorRdrObj16RdrObjV"
        sig_start_bit = 279
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
        startbit = 279
        bmuws_info = [(34, 0b11111111, 0b00000000, 8, 0), (35, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj13RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj13RdrObjDstX"
        sig_start_bit = 153
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
        startbit = 153
        bmuws_info = [(19, 0b00000011, 0b11111100, 2, 0), (20, 0b11111111, 0b00000000, 8, 0)]

    class FrntRiDoorRdrObj13RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj13RdrObjDstY"
        sig_start_bit = 141
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
        startbit = 141
        bmuws_info = [(17, 0b00111111, 0b11000000, 6, 0), (18, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj11_UB:
        sig_name = "FrntRiDoorRdrObj11_UB"
        sig_start_bit = 342
        update_id_bit = 342
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 342
        byte = 42
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FrntRiDoorRdrObj10RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj10RdrObjDstY"
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

    class FrntRiDoorRdrObj11RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj11RdrObjDstY"
        sig_start_bit = 45
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
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj12RdrObjV:
        sig_name = "FrntRiDoorRdrObj12RdrObjV"
        sig_start_bit = 117
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
        startbit = 117
        bmuws_info = [(14, 0b00111111, 0b11000000, 6, 0), (15, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj15RdrObjV:
        sig_name = "FrntRiDoorRdrObj15RdrObjV"
        sig_start_bit = 247
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
        startbit = 247
        bmuws_info = [(30, 0b11111111, 0b00000000, 8, 0), (31, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj10RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj10RdrObjDstZ"
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

    class FrntRiDoorRdrObj9RdrObjV:
        sig_name = "FrntRiDoorRdrObj9RdrObjV"
        sig_start_bit = 323
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
        startbit = 323
        bmuws_info = [(40, 0b00001111, 0b11110000, 4, 0), (41, 0b11111111, 0b00000000, 8, 0)]

    class FrntRiDoorRdrObj14RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj14RdrObjDstX"
        sig_start_bit = 175
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
        startbit = 175
        bmuws_info = [(21, 0b11111111, 0b00000000, 8, 0), (22, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj12RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj12RdrObjDstX"
        sig_start_bit = 83
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
        startbit = 83
        bmuws_info = [(10, 0b00001111, 0b11110000, 4, 0), (11, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj15RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj15RdrObjDstX"
        sig_start_bit = 225
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
        startbit = 225
        bmuws_info = [(28, 0b00000011, 0b11111100, 2, 0), (29, 0b11111111, 0b00000000, 8, 0)]

    class FrntRiDoorRdrObj15RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj15RdrObjDstZ"
        sig_start_bit = 213
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
        startbit = 213
        bmuws_info = [(26, 0b00111111, 0b11000000, 6, 0), (27, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj15_UB:
        sig_name = "FrntRiDoorRdrObj15_UB"
        sig_start_bit = 338
        update_id_bit = 338
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 338
        byte = 42
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FrntRiDoorRdrObj14RdrObjV:
        sig_name = "FrntRiDoorRdrObj14RdrObjV"
        sig_start_bit = 193
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
        startbit = 193
        bmuws_info = [(24, 0b00000011, 0b11111100, 2, 0), (25, 0b11111111, 0b00000000, 8, 0), (26, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj10RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj10RdrObjDstX"
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

    class FrntRiDoorRdrObj12RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj12RdrObjDstY"
        sig_start_bit = 89
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
        startbit = 89
        bmuws_info = [(11, 0b00000011, 0b11111100, 2, 0), (12, 0b11111111, 0b00000000, 8, 0)]

    class FrntRiDoorRdrObj12RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj12RdrObjDstZ"
        sig_start_bit = 111
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
        startbit = 111
        bmuws_info = [(13, 0b11111111, 0b00000000, 8, 0), (14, 0b11000000, 0b00111111, 2, 6)]

    class FrntRiDoorRdrObj14_UB:
        sig_name = "FrntRiDoorRdrObj14_UB"
        sig_start_bit = 339
        update_id_bit = 339
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 339
        byte = 42
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntRiDoorRdrObj9RdrObjDstZ:
        sig_name = "FrntRiDoorRdrObj9RdrObjDstZ"
        sig_start_bit = 317
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
        startbit = 317
        bmuws_info = [(39, 0b00111111, 0b11000000, 6, 0), (40, 0b11110000, 0b00001111, 4, 4)]

    class FrntRiDoorRdrObj15RdrObjDstY:
        sig_name = "FrntRiDoorRdrObj15RdrObjDstY"
        sig_start_bit = 219
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
        startbit = 219
        bmuws_info = [(27, 0b00001111, 0b11110000, 4, 0), (28, 0b11111100, 0b00000011, 6, 2)]

    class FrntRiDoorRdrObj9RdrObjDstX:
        sig_name = "FrntRiDoorRdrObj9RdrObjDstX"
        sig_start_bit = 289
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
        startbit = 289
        bmuws_info = [(36, 0b00000011, 0b11111100, 2, 0), (37, 0b11111111, 0b00000000, 8, 0)]

    class FrntRiDoorRdrObj9_UB:
        sig_name = "FrntRiDoorRdrObj9_UB"
        sig_start_bit = 336
        update_id_bit = 336
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 336
        byte = 42
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


