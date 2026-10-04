lin_scheduleTable = {'LCUL_LIN2Schedule01_LCUL_LIN2': [(0, 'IRMMLCUL_LIN2Fr01', 0.015), (1, 'LCULLCUL_LIN2Fr01', 0.015), (2, 'LCULLCUL_LIN2Fr02', 0.015), (3, 'LCULLCUL_LIN2Fr03', 0.015), (4, 'LCULLCUL_LIN2Fr04', 0.015), (5, 'LCULLCUL_LIN2Fr05', 0.015), (6, 'OHCLCUL_LIN2Fr03', 0.015), (7, 'OHCLCUL_LIN2Fr04', 0.015), (8, 'OHCLCUL_LIN2Fr05', 0.015), (9, 'SCMFLCUL_LIN2Fr01', 0.015), (10, 'SCMRLCUL_LIN2Fr01', 0.015)], 'LCUL_LIN2_DiagSchedule01': [(0, 'DiagRequest1', 0.015), (1, 'DiagResponse1', 0.015)], 'LCUL_LIN2ScheduleSerlNrPartNr_LCUL_LIN2': [(0, 'SCMRLCUL_LIN2Fr02', 0.015), (1, 'SCMRLCUL_LIN2Fr03', 0.015), (2, 'SCMFLCUL_LIN2Fr02', 0.015), (3, 'SCMFLCUL_LIN2Fr03', 0.015), (4, 'OHCLCUL_LIN2Fr01', 0.015), (5, 'OHCLCUL_LIN2Fr02', 0.015), (6, 'IRMMLCUL_LIN2Fr02', 0.015), (7, 'IRMMLCUL_LIN2Fr03', 0.015), (8, 'FCSILCUL_LIN2Fr01', 0.015), (9, 'FCSILCUL_LIN2Fr02', 0.015)]}


class SCMFLCUL_LIN2Fr02:
    msg_name = "SCMFLCUL_LIN2Fr02"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "SCMF"
    rx_nodes = ['LCUL']
    sig_group_dict = {'SCMFPartNo': ['SCMFPartNoEndSgn1', 'SCMFPartNoEndSgn2', 'SCMFPartNoEndSgn3', 'SCMFPartNoNr1', 'SCMFPartNoNr2', 'SCMFPartNoNr3', 'SCMFPartNoNr4', 'SCMFPartNoNr5']}
    sig_group_dataid_dict = {}

    class SCMFPartNoEndSgn1:
        sig_name = "SCMFPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMFPartNoEndSgn2:
        sig_name = "SCMFPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMFPartNoNr5:
        sig_name = "SCMFPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMFPartNoNr3:
        sig_name = "SCMFPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMFPartNoEndSgn3:
        sig_name = "SCMFPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMFPartNoNr4:
        sig_name = "SCMFPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMFPartNoNr2:
        sig_name = "SCMFPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMFPartNoNr1:
        sig_name = "SCMFPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class SCMFLCUL_LIN2Fr03:
    msg_name = "SCMFLCUL_LIN2Fr03"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "SCMF"
    rx_nodes = ['LCUL']
    sig_group_dict = {'SCMFSerNo': ['SCMFSerNoNr1', 'SCMFSerNoNr2', 'SCMFSerNoNr3', 'SCMFSerNoNr4']}
    sig_group_dataid_dict = {}

    class SCMFSerNoNr1:
        sig_name = "SCMFSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMFSerNoNr4:
        sig_name = "SCMFSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMFSerNoNr2:
        sig_name = "SCMFSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMFSerNoNr3:
        sig_name = "SCMFSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class SCMRLCUL_LIN2Fr03:
    msg_name = "SCMRLCUL_LIN2Fr03"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "SCMR"
    rx_nodes = ['LCUL']
    sig_group_dict = {'SCMRSerNo': ['SCMRSerNoNr1', 'SCMRSerNoNr2', 'SCMRSerNoNr3', 'SCMRSerNoNr4']}
    sig_group_dataid_dict = {}

    class SCMRSerNoNr1:
        sig_name = "SCMRSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMRSerNoNr2:
        sig_name = "SCMRSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMRSerNoNr3:
        sig_name = "SCMRSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMRSerNoNr4:
        sig_name = "SCMRSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class OHCLCUL_LIN2Fr03:
    msg_name = "OHCLCUL_LIN2Fr03"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "OHC"
    rx_nodes = ['LCUL']
    sig_group_dict = {'ReadingLiSecRowLeDrvSts': ['ReadingLiSecRowLeDrvStsLightErrorCode', 'ReadingLiSecRowLeDrvStsLightSts', 'ReadingLiSecRowLeDrvStsLiPerc'], 'ReadingLiFrntRiDrvSts': ['ReadingLiFrntRiDrvStsLightErrorCode', 'ReadingLiFrntRiDrvStsLightSts', 'ReadingLiFrntRiDrvStsLiPerc'], 'ReadingLiFrntLeDrvSts': ['ReadingLiFrntLeDrvStsLightErrorCode', 'ReadingLiFrntLeDrvStsLightSts', 'ReadingLiFrntLeDrvStsLiPerc']}
    sig_group_dataid_dict = {}

    class ReadingLiSecRowLeDrvStsLightErrorCode:
        sig_name = "ReadingLiSecRowLeDrvStsLightErrorCode"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReadingLiFrntLeDrvStsLiPerc:
        sig_name = "ReadingLiFrntLeDrvStsLiPerc"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 12
        bmuws_info = [(1, 0b11110000, 0b00001111, 4, 4), (2, 0b00000111, 0b11111000, 3, 0)]

    class ReadingLiSecRowLeDrvStsLightSts:
        sig_name = "ReadingLiSecRowLeDrvStsLightSts"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 48
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReadingLiFrntRiDrvStsLightErrorCode:
        sig_name = "ReadingLiFrntRiDrvStsLightErrorCode"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 21
        bmuws_info = [(2, 0b11100000, 0b00011111, 3, 5), (3, 0b00011111, 0b11100000, 5, 0)]

    class ReadingLiFrntLeDrvStsLightSts:
        sig_name = "ReadingLiFrntLeDrvStsLightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReadingLiFrntLeDrvStsLightErrorCode:
        sig_name = "ReadingLiFrntLeDrvStsLightErrorCode"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReadingLiFrntRiDrvStsLiPerc:
        sig_name = "ReadingLiFrntRiDrvStsLiPerc"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 33
        byte = 4
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLiSecRowLeDrvStsLiPerc:
        sig_name = "ReadingLiSecRowLeDrvStsLiPerc"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 52
        bmuws_info = [(6, 0b11110000, 0b00001111, 4, 4), (7, 0b00000111, 0b11111000, 3, 0)]

    class ReadingLiFrntRiDrvStsLightSts:
        sig_name = "ReadingLiFrntRiDrvStsLightSts"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 29
        bmuws_info = [(3, 0b11100000, 0b00011111, 3, 5), (4, 0b00000001, 0b11111110, 1, 0)]


class FCSILCUL_LIN2Fr01:
    msg_name = "FCSILCUL_LIN2Fr01"
    msg_id = 0
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "FCSI"
    rx_nodes = ['LCUL']
    sig_group_dict = {'FCSIPartNo': ['FCSIPartNoEndSgn1', 'FCSIPartNoEndSgn2', 'FCSIPartNoEndSgn3', 'FCSIPartNoNr1', 'FCSIPartNoNr2', 'FCSIPartNoNr3', 'FCSIPartNoNr4', 'FCSIPartNoNr5']}
    sig_group_dataid_dict = {}

    class FCSIPartNoNr3:
        sig_name = "FCSIPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FCSIPartNoNr5:
        sig_name = "FCSIPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FCSIPartNoNr1:
        sig_name = "FCSIPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FCSIPartNoEndSgn2:
        sig_name = "FCSIPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FCSIPartNoNr4:
        sig_name = "FCSIPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FCSIPartNoNr2:
        sig_name = "FCSIPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FCSIPartNoEndSgn1:
        sig_name = "FCSIPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FCSIPartNoEndSgn3:
        sig_name = "FCSIPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class OHCLCUL_LIN2Fr05:
    msg_name = "OHCLCUL_LIN2Fr05"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "OHC"
    rx_nodes = ['LCUL']
    sig_group_dict = {'ReadingLiSwtSts': ['ReadingLiSwtStsFrntLeSwtSts', 'ReadingLiSwtStsFrntRiSwtSts', 'ReadingLiSwtStsSecLeSwtSts', 'ReadingLiSwtStsSecRiSwtSts', 'ReadingLiSwtStsThrdLeSwtSts', 'ReadingLiSwtStsThrdRiSwtSts']}
    sig_group_dataid_dict = {}

    class ReadingLiSwtStsSecRiSwtSts:
        sig_name = "ReadingLiSwtStsSecRiSwtSts"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class ReadingLiSwtStsFrntLeSwtSts:
        sig_name = "ReadingLiSwtStsFrntLeSwtSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReadingLiSwtStsSecLeSwtSts:
        sig_name = "ReadingLiSwtStsSecLeSwtSts"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class ReadingLiSwtStsThrdLeSwtSts:
        sig_name = "ReadingLiSwtStsThrdLeSwtSts"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class ReadingLiSwtStsThrdRiSwtSts:
        sig_name = "ReadingLiSwtStsThrdRiSwtSts"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class ReadingLiSwtStsFrntRiSwtSts:
        sig_name = "ReadingLiSwtStsFrntRiSwtSts"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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


class FCSILCUL_LIN2Fr02:
    msg_name = "FCSILCUL_LIN2Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "FCSI"
    rx_nodes = ['LCUL']
    sig_group_dict = {'FCSISerNo': ['FCSISerNoNr1', 'FCSISerNoNr2', 'FCSISerNoNr3', 'FCSISerNoNr4']}
    sig_group_dataid_dict = {}

    class FCSISerNoNr2:
        sig_name = "FCSISerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FCSISerNoNr3:
        sig_name = "FCSISerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FCSISerNoNr4:
        sig_name = "FCSISerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FCSISerNoNr1:
        sig_name = "FCSISerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class SCMRLCUL_LIN2Fr02:
    msg_name = "SCMRLCUL_LIN2Fr02"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "SCMR"
    rx_nodes = ['LCUL']
    sig_group_dict = {'SCMRPartNo': ['SCMRPartNoEndSgn1', 'SCMRPartNoEndSgn2', 'SCMRPartNoEndSgn3', 'SCMRPartNoNr1', 'SCMRPartNoNr2', 'SCMRPartNoNr3', 'SCMRPartNoNr4', 'SCMRPartNoNr5']}
    sig_group_dataid_dict = {}

    class SCMRPartNoNr5:
        sig_name = "SCMRPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMRPartNoEndSgn1:
        sig_name = "SCMRPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMRPartNoNr2:
        sig_name = "SCMRPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMRPartNoNr3:
        sig_name = "SCMRPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMRPartNoEndSgn2:
        sig_name = "SCMRPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMRPartNoEndSgn3:
        sig_name = "SCMRPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMRPartNoNr4:
        sig_name = "SCMRPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SCMRPartNoNr1:
        sig_name = "SCMRPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class IRMMLCUL_LIN2Fr01:
    msg_name = "IRMMLCUL_LIN2Fr01"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "IRMM"
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IntrReViewMirrDimPerc:
        sig_name = "IntrReViewMirrDimPerc"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 0
        byte = 0
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class IntrReViewMirrDimFailr:
        sig_name = "IntrReViewMirrDimFailr"
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
        sig_value_table = {'IntrReViewMirrDimFailr_NoFault': 0, 'IntrReViewMirrDimFailr_InternalFailure': 1, 'IntrReViewMirrDimFailr_Reserved1': 2, 'IntrReViewMirrDimFailr_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class LCULLCUL_LIN2Fr02:
    msg_name = "LCULLCUL_LIN2Fr02"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['OHC']
    sig_group_dict = {'ReadingLightThrdRowLeDrvReq': ['ReadingLightThrdRowLeDrvReqLightCmd', 'ReadingLightThrdRowLeDrvReqLiPerc', 'ReadingLightThrdRowLeDrvReqReadingLiDimsSpdCmd'], 'ReadingLightThrdRowRiDrvReq': ['ReadingLightThrdRowRiDrvReqLightCmd', 'ReadingLightThrdRowRiDrvReqLiPerc', 'ReadingLightThrdRowRiDrvReqReadingLiDimsSpdCmd'], 'ReadingLightSecRowLeDrvReq': ['ReadingLightSecRowLeDrvReqLightCmd', 'ReadingLightSecRowLeDrvReqLiPerc', 'ReadingLightSecRowLeDrvReqReadingLiDimsSpdCmd'], 'ReadingLightSecRowRiDrvReq': ['ReadingLightSecRowRiDrvReqLightCmd', 'ReadingLightSecRowRiDrvReqLiPerc', 'ReadingLightSecRowRiDrvReqReadingLiDimsSpdCmd']}
    sig_group_dataid_dict = {}

    class ReadingLightSecRowRiDrvReqLiPerc:
        sig_name = "ReadingLightSecRowRiDrvReqLiPerc"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 20
        bmuws_info = [(2, 0b11110000, 0b00001111, 4, 4), (3, 0b00000111, 0b11111000, 3, 0)]

    class ReadingLightSecRowRiDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightSecRowRiDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 27
        byte = 3
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class ReadingLightThrdRowLeDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightThrdRowLeDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 43
        byte = 5
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class ReadingLightThrdRowRiDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightThrdRowRiDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class ReadingLightSecRowRiDrvReqLightCmd:
        sig_name = "ReadingLightSecRowRiDrvReqLightCmd"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 16
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReadingLightSecRowLeDrvReqLiPerc:
        sig_name = "ReadingLightSecRowLeDrvReqLiPerc"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 4
        bmuws_info = [(0, 0b11110000, 0b00001111, 4, 4), (1, 0b00000111, 0b11111000, 3, 0)]

    class ReadingLightThrdRowLeDrvReqLightCmd:
        sig_name = "ReadingLightThrdRowLeDrvReqLightCmd"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 32
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReadingLightThrdRowRiDrvReqLightCmd:
        sig_name = "ReadingLightThrdRowRiDrvReqLightCmd"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 48
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReadingLightThrdRowRiDrvReqLiPerc:
        sig_name = "ReadingLightThrdRowRiDrvReqLiPerc"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 52
        bmuws_info = [(6, 0b11110000, 0b00001111, 4, 4), (7, 0b00000111, 0b11111000, 3, 0)]

    class ReadingLightThrdRowLeDrvReqLiPerc:
        sig_name = "ReadingLightThrdRowLeDrvReqLiPerc"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 36
        bmuws_info = [(4, 0b11110000, 0b00001111, 4, 4), (5, 0b00000111, 0b11111000, 3, 0)]

    class ReadingLightSecRowLeDrvReqLightCmd:
        sig_name = "ReadingLightSecRowLeDrvReqLightCmd"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReadingLightSecRowLeDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightSecRowLeDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 11
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3


class IRMMLCUL_LIN2Fr03:
    msg_name = "IRMMLCUL_LIN2Fr03"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "IRMM"
    rx_nodes = ['LCUL']
    sig_group_dict = {'IRMMSerNo': ['IRMMSerNoNr1', 'IRMMSerNoNr2', 'IRMMSerNoNr3', 'IRMMSerNoNr4']}
    sig_group_dataid_dict = {}

    class IRMMSerNoNr4:
        sig_name = "IRMMSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IRMMSerNoNr1:
        sig_name = "IRMMSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IRMMSerNoNr3:
        sig_name = "IRMMSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IRMMSerNoNr2:
        sig_name = "IRMMSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCULLCUL_LIN2Fr03:
    msg_name = "LCULLCUL_LIN2Fr03"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['SCMR', 'SCMF']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ReSunroofCurtlrnCmd:
        sig_name = "ReSunroofCurtlrnCmd"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LrnCmd_NoCmd': 0, 'LrnCmd_ClrCmd': 1, 'LrnCmd_LrngCmd': 2, 'LrnCmd_Resd': 3}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ReSunroofCurtPosnCmd:
        sig_name = "ReSunroofCurtPosnCmd"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 29
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PosnPercCmd_NoCmd': 0, 'PosnPercCmd_FullCls': 1, 'PosnPercCmd_Perc4': 2, 'PosnPercCmd_Perc8': 3, 'PosnPercCmd_Perc12': 4, 'PosnPercCmd_Perc16': 5, 'PosnPercCmd_Perc20': 6, 'PosnPercCmd_Perc24': 7, 'PosnPercCmd_Perc28': 8, 'PosnPercCmd_Perc32': 9, 'PosnPercCmd_Perc36': 10, 'PosnPercCmd_Perc40': 11, 'PosnPercCmd_Perc44': 12, 'PosnPercCmd_Perc48': 13, 'PosnPercCmd_Perc52': 14, 'PosnPercCmd_Perc56': 15, 'PosnPercCmd_Perc60': 16, 'PosnPercCmd_Perc64': 17, 'PosnPercCmd_Perc68': 18, 'PosnPercCmd_Perc72': 19, 'PosnPercCmd_Perc76': 20, 'PosnPercCmd_Perc80': 21, 'PosnPercCmd_Perc84': 22, 'PosnPercCmd_Perc88': 23, 'PosnPercCmd_Perc92': 24, 'PosnPercCmd_Perc96': 25, 'PosnPercCmd_FullOpen': 26, 'PosnPercCmd_Resd1': 27, 'PosnPercCmd_Resd2': 28, 'PosnPercCmd_Resd3': 29}
        compute_method = None
        length = 5
        startbit = 2
        byte = 0
        mask = 0b01111100
        unmask = 0b10000011
        shift = 2

    class FrntSunroofCurtPosnCmd:
        sig_name = "FrntSunroofCurtPosnCmd"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 29
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PosnPercCmd_NoCmd': 0, 'PosnPercCmd_FullCls': 1, 'PosnPercCmd_Perc4': 2, 'PosnPercCmd_Perc8': 3, 'PosnPercCmd_Perc12': 4, 'PosnPercCmd_Perc16': 5, 'PosnPercCmd_Perc20': 6, 'PosnPercCmd_Perc24': 7, 'PosnPercCmd_Perc28': 8, 'PosnPercCmd_Perc32': 9, 'PosnPercCmd_Perc36': 10, 'PosnPercCmd_Perc40': 11, 'PosnPercCmd_Perc44': 12, 'PosnPercCmd_Perc48': 13, 'PosnPercCmd_Perc52': 14, 'PosnPercCmd_Perc56': 15, 'PosnPercCmd_Perc60': 16, 'PosnPercCmd_Perc64': 17, 'PosnPercCmd_Perc68': 18, 'PosnPercCmd_Perc72': 19, 'PosnPercCmd_Perc76': 20, 'PosnPercCmd_Perc80': 21, 'PosnPercCmd_Perc84': 22, 'PosnPercCmd_Perc88': 23, 'PosnPercCmd_Perc92': 24, 'PosnPercCmd_Perc96': 25, 'PosnPercCmd_FullOpen': 26, 'PosnPercCmd_Resd1': 27, 'PosnPercCmd_Resd2': 28, 'PosnPercCmd_Resd3': 29}
        compute_method = None
        length = 5
        startbit = 10
        byte = 1
        mask = 0b01111100
        unmask = 0b10000011
        shift = 2

    class FrntSunroofCurtlrnCmd:
        sig_name = "FrntSunroofCurtlrnCmd"
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
        sig_value_table = {'LrnCmd_NoCmd': 0, 'LrnCmd_ClrCmd': 1, 'LrnCmd_LrngCmd': 2, 'LrnCmd_Resd': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class OHCLCUL_LIN2Fr01:
    msg_name = "OHCLCUL_LIN2Fr01"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "OHC"
    rx_nodes = ['LCUL']
    sig_group_dict = {'OHCPartNo': ['OHCPartNoEndSgn1', 'OHCPartNoEndSgn2', 'OHCPartNoEndSgn3', 'OHCPartNoNr1', 'OHCPartNoNr2', 'OHCPartNoNr3', 'OHCPartNoNr4', 'OHCPartNoNr5']}
    sig_group_dataid_dict = {}

    class OHCPartNoNr2:
        sig_name = "OHCPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OHCPartNoEndSgn3:
        sig_name = "OHCPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OHCPartNoNr5:
        sig_name = "OHCPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OHCPartNoEndSgn1:
        sig_name = "OHCPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OHCPartNoEndSgn2:
        sig_name = "OHCPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OHCPartNoNr1:
        sig_name = "OHCPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OHCPartNoNr4:
        sig_name = "OHCPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OHCPartNoNr3:
        sig_name = "OHCPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class OHCLCUL_LIN2Fr04:
    msg_name = "OHCLCUL_LIN2Fr04"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "OHC"
    rx_nodes = ['LCUL']
    sig_group_dict = {'ReadingLiSecRowRiDrvSts': ['ReadingLiSecRowRiDrvStsLightErrorCode', 'ReadingLiSecRowRiDrvStsLightSts', 'ReadingLiSecRowRiDrvStsLiPerc'], 'ReadingLiThrdRowRiDrvSts': ['ReadingLiThrdRowRiDrvStsLightErrorCode', 'ReadingLiThrdRowRiDrvStsLightSts', 'ReadingLiThrdRowRiDrvStsLiPerc'], 'ReadingLiThrdRowLeDrvSts': ['ReadingLiThrdRowLeDrvStsLightErrorCode', 'ReadingLiThrdRowLeDrvStsLightSts', 'ReadingLiThrdRowLeDrvStsLiPerc']}
    sig_group_dataid_dict = {}

    class ReadingLiThrdRowLeDrvStsLiPerc:
        sig_name = "ReadingLiThrdRowLeDrvStsLiPerc"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 33
        byte = 4
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ReadingLiSecRowRiDrvStsLiPerc:
        sig_name = "ReadingLiSecRowRiDrvStsLiPerc"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 12
        bmuws_info = [(1, 0b11110000, 0b00001111, 4, 4), (2, 0b00000111, 0b11111000, 3, 0)]

    class ReadingLiThrdRowLeDrvStsLightErrorCode:
        sig_name = "ReadingLiThrdRowLeDrvStsLightErrorCode"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 21
        bmuws_info = [(2, 0b11100000, 0b00011111, 3, 5), (3, 0b00011111, 0b11100000, 5, 0)]

    class ReadingLiSecRowRiDrvStsLightSts:
        sig_name = "ReadingLiSecRowRiDrvStsLightSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReadingLiThrdRowRiDrvStsLiPerc:
        sig_name = "ReadingLiThrdRowRiDrvStsLiPerc"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 52
        bmuws_info = [(6, 0b11110000, 0b00001111, 4, 4), (7, 0b00000111, 0b11111000, 3, 0)]

    class ReadingLiThrdRowRiDrvStsLightSts:
        sig_name = "ReadingLiThrdRowRiDrvStsLightSts"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 48
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReadingLiThrdRowLeDrvStsLightSts:
        sig_name = "ReadingLiThrdRowLeDrvStsLightSts"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightSts_Off': 0, 'LightSts_On': 1, 'LightSts_Error': 2, 'LightSts_Reserved': 3}
        compute_method = None
        length = 4
        startbit = 29
        bmuws_info = [(3, 0b11100000, 0b00011111, 3, 5), (4, 0b00000001, 0b11111110, 1, 0)]

    class ReadingLiThrdRowRiDrvStsLightErrorCode:
        sig_name = "ReadingLiThrdRowRiDrvStsLightErrorCode"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReadingLiSecRowRiDrvStsLightErrorCode:
        sig_name = "ReadingLiSecRowRiDrvStsLightErrorCode"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightErrorCode_ChipError': 0, 'LightErrorCode_ShortError': 1, 'LightErrorCode_OpenError': 2, 'LightErrorCode_NoneError': 255}
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class SCMFLCUL_LIN2Fr01:
    msg_name = "SCMFLCUL_LIN2Fr01"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "SCMF"
    rx_nodes = ['LCUL']
    sig_group_dict = {'FrntSunroofCurtFailrFb': ['FrntSunroofCurtFailrFbHallSnsrFailr', 'FrntSunroofCurtFailrFbHiVolt', 'FrntSunroofCurtFailrFbLoVolt', 'FrntSunroofCurtFailrFbMotOpenCirc', 'FrntSunroofCurtFailrFbMotShoCirc', 'FrntSunroofCurtFailrFbOverTmp']}
    sig_group_dataid_dict = {}

    class FrntSunroofCurtImpactFb:
        sig_name = "FrntSunroofCurtImpactFb"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PinchAndBlkFb_Idle': 0, 'PinchAndBlkFb_ClsPinch': 1, 'PinchAndBlkFb_ClsBlk': 2, 'PinchAndBlkFb_OpenPinch': 3, 'PinchAndBlkFb_OpenBlk': 4}
        compute_method = None
        length = 3
        startbit = 8
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class FrntSunroofCurtFailrFbMotShoCirc:
        sig_name = "FrntSunroofCurtFailrFbMotShoCirc"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FrntSunroofCurtFailrFbMotOpenCirc:
        sig_name = "FrntSunroofCurtFailrFbMotOpenCirc"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FrntSunroofCurtFailrFbLoVolt:
        sig_name = "FrntSunroofCurtFailrFbLoVolt"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FrntSunroofCurtlrnSts:
        sig_name = "FrntSunroofCurtlrnSts"
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
        sig_value_table = {'LrnSts_Idle': 0, 'LrnSts_lrnOk': 1, 'LrnSts_lrnInProgs': 2, 'LrnSts_lrnFail': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FrntSunroofCurtMvngSts:
        sig_name = "FrntSunroofCurtMvngSts"
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
        sig_value_table = {'MoveSts_Idle': 0, 'MoveSts_Stop': 1, 'MoveSts_Opening': 2, 'MoveSts_Closing': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FrntSunroofCurtFailrFbOverTmp:
        sig_name = "FrntSunroofCurtFailrFbOverTmp"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FrntSunroofCurtFailrFbHiVolt:
        sig_name = "FrntSunroofCurtFailrFbHiVolt"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntSunroofCurtFailrFbHallSnsrFailr:
        sig_name = "FrntSunroofCurtFailrFbHallSnsrFailr"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FrntSunroofCurtPosnPerc:
        sig_name = "FrntSunroofCurtPosnPerc"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 30
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PosnPerc_Idle': 0, 'PosnPerc_PosnPercUnknow': 1, 'PosnPerc_PosnPercFullCls': 2, 'PosnPerc_PosnPerc4': 3, 'PosnPerc_PosnPerc8': 4, 'PosnPerc_PosnPerc12': 5, 'PosnPerc_PosnPerc16': 6, 'PosnPerc_PosnPerc20': 7, 'PosnPerc_PosnPerc24': 8, 'PosnPerc_PosnPerc28': 9, 'PosnPerc_PosnPerc32': 10, 'PosnPerc_PosnPerc36': 11, 'PosnPerc_PosnPerc40': 12, 'PosnPerc_PosnPerc44': 13, 'PosnPerc_PosnPerc48': 14, 'PosnPerc_PosnPerc52': 15, 'PosnPerc_PosnPerc56': 16, 'PosnPerc_PosnPerc60': 17, 'PosnPerc_PosnPerc64': 18, 'PosnPerc_PosnPerc68': 19, 'PosnPerc_PosnPerc72': 20, 'PosnPerc_PosnPerc76': 21, 'PosnPerc_PosnPerc80': 22, 'PosnPerc_PosnPerc84': 23, 'PosnPerc_PosnPerc88': 24, 'PosnPerc_PosnPerc92': 25, 'PosnPerc_PosnPerc96': 26, 'PosnPerc_FullOpen': 27, 'PosnPerc_Reserved1': 28, 'PosnPerc_Reserved2': 29, 'PosnPerc_Reserved3': 30}
        compute_method = None
        length = 5
        startbit = 11
        byte = 1
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3


class SCMRLCUL_LIN2Fr01:
    msg_name = "SCMRLCUL_LIN2Fr01"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "SCMR"
    rx_nodes = ['LCUL']
    sig_group_dict = {'ReSunroofCurtFailrFb': ['ReSunroofCurtFailrFbHallSnsrFailr', 'ReSunroofCurtFailrFbHiVolt', 'ReSunroofCurtFailrFbLoVolt', 'ReSunroofCurtFailrFbMotOpenCirc', 'ReSunroofCurtFailrFbMotShoCirc', 'ReSunroofCurtFailrFbOverTmp']}
    sig_group_dataid_dict = {}

    class ReSunroofCurtFailrFbLoVolt:
        sig_name = "ReSunroofCurtFailrFbLoVolt"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReSunroofCurtFailrFbMotOpenCirc:
        sig_name = "ReSunroofCurtFailrFbMotOpenCirc"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ReSunroofCurtFailrFbHallSnsrFailr:
        sig_name = "ReSunroofCurtFailrFbHallSnsrFailr"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReSunroofCurtPosnPerc:
        sig_name = "ReSunroofCurtPosnPerc"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 30
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PosnPerc_Idle': 0, 'PosnPerc_PosnPercUnknow': 1, 'PosnPerc_PosnPercFullCls': 2, 'PosnPerc_PosnPerc4': 3, 'PosnPerc_PosnPerc8': 4, 'PosnPerc_PosnPerc12': 5, 'PosnPerc_PosnPerc16': 6, 'PosnPerc_PosnPerc20': 7, 'PosnPerc_PosnPerc24': 8, 'PosnPerc_PosnPerc28': 9, 'PosnPerc_PosnPerc32': 10, 'PosnPerc_PosnPerc36': 11, 'PosnPerc_PosnPerc40': 12, 'PosnPerc_PosnPerc44': 13, 'PosnPerc_PosnPerc48': 14, 'PosnPerc_PosnPerc52': 15, 'PosnPerc_PosnPerc56': 16, 'PosnPerc_PosnPerc60': 17, 'PosnPerc_PosnPerc64': 18, 'PosnPerc_PosnPerc68': 19, 'PosnPerc_PosnPerc72': 20, 'PosnPerc_PosnPerc76': 21, 'PosnPerc_PosnPerc80': 22, 'PosnPerc_PosnPerc84': 23, 'PosnPerc_PosnPerc88': 24, 'PosnPerc_PosnPerc92': 25, 'PosnPerc_PosnPerc96': 26, 'PosnPerc_FullOpen': 27, 'PosnPerc_Reserved1': 28, 'PosnPerc_Reserved2': 29, 'PosnPerc_Reserved3': 30}
        compute_method = None
        length = 5
        startbit = 11
        byte = 1
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class ReSunroofCurtlrnSts:
        sig_name = "ReSunroofCurtlrnSts"
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
        sig_value_table = {'LrnSts_Idle': 0, 'LrnSts_lrnOk': 1, 'LrnSts_lrnInProgs': 2, 'LrnSts_lrnFail': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ReSunroofCurtFailrFbHiVolt:
        sig_name = "ReSunroofCurtFailrFbHiVolt"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ReSunroofCurtMvngSts:
        sig_name = "ReSunroofCurtMvngSts"
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
        sig_value_table = {'MoveSts_Idle': 0, 'MoveSts_Stop': 1, 'MoveSts_Opening': 2, 'MoveSts_Closing': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ReSunroofCurtFailrFbMotShoCirc:
        sig_name = "ReSunroofCurtFailrFbMotShoCirc"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReSunroofCurtFailrFbOverTmp:
        sig_name = "ReSunroofCurtFailrFbOverTmp"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ReSunroofCurtImpactFb:
        sig_name = "ReSunroofCurtImpactFb"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PinchAndBlkFb_Idle': 0, 'PinchAndBlkFb_ClsPinch': 1, 'PinchAndBlkFb_ClsBlk': 2, 'PinchAndBlkFb_OpenPinch': 3, 'PinchAndBlkFb_OpenBlk': 4}
        compute_method = None
        length = 3
        startbit = 8
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class LCULLCUL_LIN2Fr04:
    msg_name = "LCULLCUL_LIN2Fr04"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['SCMR', 'SCMF']
    sig_group_dict = {'VMMGlbSig': ['VMMGlbSigCarModSts', 'VMMGlbSigChks', 'VMMGlbSigCntr', 'VMMGlbSigCnvincSubSts1', 'VMMGlbSigDrvgSubSts1', 'VMMGlbSigInactvSubSts1', 'VMMGlbSigLoBattModSts', 'VMMGlbSigUsgModSts']}
    sig_group_dataid_dict = {'VMMGlbSig': 1074}

    class VMMGlbSigDrvgSubSts1:
        sig_name = "VMMGlbSigDrvgSubSts1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvgSubSts_Invalid': 0, 'DrvgSubSts_Manual': 1, 'DrvgSubSts_Automatic': 2, 'DrvgSubSts_NoTorque': 3}
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigUsgModSts:
        sig_name = "VMMGlbSigUsgModSts"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 40
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VMMGlbSigCnvincSubSts1:
        sig_name = "VMMGlbSigCnvincSubSts1"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CnvincSubSts_Invalid': 0, 'CnvincSubSts_EnterExit': 1, 'CnvincSubSts_AllDoorClosed': 2}
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigCarModSts:
        sig_name = "VMMGlbSigCarModSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarModStsType_CarModNorm': 0, 'CarModStsType_CarModTrnsp': 1, 'CarModStsType_CarModFcy': 2, 'CarModStsType_CarModExhib': 3, 'CarModStsType_CarModCrash': 8}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VMMGlbSigInactvSubSts1:
        sig_name = "VMMGlbSigInactvSubSts1"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'InactvSubSts_Invalid': 0, 'InactvSubSts_Awake': 1, 'InactvSubSts_UserPresent': 2}
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigLoBattModSts:
        sig_name = "VMMGlbSigLoBattModSts"
        sig_start_bit = 44
        update_id_bit = None
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
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VMMGlbSigChks:
        sig_name = "VMMGlbSigChks"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VMMGlbSigCntr:
        sig_name = "VMMGlbSigCntr"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class IRMMLCUL_LIN2Fr02:
    msg_name = "IRMMLCUL_LIN2Fr02"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "IRMM"
    rx_nodes = ['LCUL']
    sig_group_dict = {'IRMMPartNo': ['IRMMPartNoEndSgn1', 'IRMMPartNoEndSgn2', 'IRMMPartNoEndSgn3', 'IRMMPartNoNr1', 'IRMMPartNoNr2', 'IRMMPartNoNr3', 'IRMMPartNoNr4', 'IRMMPartNoNr5']}
    sig_group_dataid_dict = {}

    class IRMMPartNoNr5:
        sig_name = "IRMMPartNoNr5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IRMMPartNoNr3:
        sig_name = "IRMMPartNoNr3"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IRMMPartNoEndSgn2:
        sig_name = "IRMMPartNoEndSgn2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IRMMPartNoEndSgn3:
        sig_name = "IRMMPartNoEndSgn3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IRMMPartNoEndSgn1:
        sig_name = "IRMMPartNoEndSgn1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IRMMPartNoNr2:
        sig_name = "IRMMPartNoNr2"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IRMMPartNoNr1:
        sig_name = "IRMMPartNoNr1"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IRMMPartNoNr4:
        sig_name = "IRMMPartNoNr4"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCULLCUL_LIN2Fr01:
    msg_name = "LCULLCUL_LIN2Fr01"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['SCMR', 'SCMF', 'IRMM']
    sig_group_dict = {'DualSunroofCurtPosnCmd': ['DualSunroofCurtPosnCmdFrntPosnPercCmd', 'DualSunroofCurtPosnCmdRearPosnPercCmd'], 'DualSunroofCurtlrnCmd': ['DualSunroofCurtlrnCmdFrntLrnCmd', 'DualSunroofCurtlrnCmdRearLrnCmd']}
    sig_group_dataid_dict = {}

    class DualSunroofCurtPosnCmdRearPosnPercCmd:
        sig_name = "DualSunroofCurtPosnCmdRearPosnPercCmd"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 29
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PosnPercCmd_NoCmd': 0, 'PosnPercCmd_FullCls': 1, 'PosnPercCmd_Perc4': 2, 'PosnPercCmd_Perc8': 3, 'PosnPercCmd_Perc12': 4, 'PosnPercCmd_Perc16': 5, 'PosnPercCmd_Perc20': 6, 'PosnPercCmd_Perc24': 7, 'PosnPercCmd_Perc28': 8, 'PosnPercCmd_Perc32': 9, 'PosnPercCmd_Perc36': 10, 'PosnPercCmd_Perc40': 11, 'PosnPercCmd_Perc44': 12, 'PosnPercCmd_Perc48': 13, 'PosnPercCmd_Perc52': 14, 'PosnPercCmd_Perc56': 15, 'PosnPercCmd_Perc60': 16, 'PosnPercCmd_Perc64': 17, 'PosnPercCmd_Perc68': 18, 'PosnPercCmd_Perc72': 19, 'PosnPercCmd_Perc76': 20, 'PosnPercCmd_Perc80': 21, 'PosnPercCmd_Perc84': 22, 'PosnPercCmd_Perc88': 23, 'PosnPercCmd_Perc92': 24, 'PosnPercCmd_Perc96': 25, 'PosnPercCmd_FullOpen': 26, 'PosnPercCmd_Resd1': 27, 'PosnPercCmd_Resd2': 28, 'PosnPercCmd_Resd3': 29}
        compute_method = None
        length = 5
        startbit = 13
        bmuws_info = [(1, 0b11100000, 0b00011111, 3, 5), (2, 0b00000011, 0b11111100, 2, 0)]

    class ReSunroofCurtSwtCmd:
        sig_name = "ReSunroofCurtSwtCmd"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SunroofCurtSwtSts_Idle': 0, 'SunroofCurtSwtSts_OpenMan': 1, 'SunroofCurtSwtSts_OpenAut': 2, 'SunroofCurtSwtSts_ClsMan1': 3, 'SunroofCurtSwtSts_ClsMan2': 4, 'SunroofCurtSwtSts_Stop': 5}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DualSunroofCurtlrnCmdFrntLrnCmd:
        sig_name = "DualSunroofCurtlrnCmdFrntLrnCmd"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LrnCmd_NoCmd': 0, 'LrnCmd_ClrCmd': 1, 'LrnCmd_LrngCmd': 2, 'LrnCmd_Resd': 3}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IntrReViewMirrDimCmd:
        sig_name = "IntrReViewMirrDimCmd"
        sig_start_bit = 4
        update_id_bit = None
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

    class FrntSunroofCurtSwtCmd:
        sig_name = "FrntSunroofCurtSwtCmd"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SunroofCurtSwtSts_Idle': 0, 'SunroofCurtSwtSts_OpenMan': 1, 'SunroofCurtSwtSts_OpenAut': 2, 'SunroofCurtSwtSts_ClsMan1': 3, 'SunroofCurtSwtSts_ClsMan2': 4, 'SunroofCurtSwtSts_Stop': 5}
        compute_method = None
        length = 3
        startbit = 18
        byte = 2
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class IntrReViewMirrInhbDimCmd:
        sig_name = "IntrReViewMirrInhbDimCmd"
        sig_start_bit = 7
        update_id_bit = None
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DualSunroofCurtPosnCmdFrntPosnPercCmd:
        sig_name = "DualSunroofCurtPosnCmdFrntPosnPercCmd"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 29
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PosnPercCmd_NoCmd': 0, 'PosnPercCmd_FullCls': 1, 'PosnPercCmd_Perc4': 2, 'PosnPercCmd_Perc8': 3, 'PosnPercCmd_Perc12': 4, 'PosnPercCmd_Perc16': 5, 'PosnPercCmd_Perc20': 6, 'PosnPercCmd_Perc24': 7, 'PosnPercCmd_Perc28': 8, 'PosnPercCmd_Perc32': 9, 'PosnPercCmd_Perc36': 10, 'PosnPercCmd_Perc40': 11, 'PosnPercCmd_Perc44': 12, 'PosnPercCmd_Perc48': 13, 'PosnPercCmd_Perc52': 14, 'PosnPercCmd_Perc56': 15, 'PosnPercCmd_Perc60': 16, 'PosnPercCmd_Perc64': 17, 'PosnPercCmd_Perc68': 18, 'PosnPercCmd_Perc72': 19, 'PosnPercCmd_Perc76': 20, 'PosnPercCmd_Perc80': 21, 'PosnPercCmd_Perc84': 22, 'PosnPercCmd_Perc88': 23, 'PosnPercCmd_Perc92': 24, 'PosnPercCmd_Perc96': 25, 'PosnPercCmd_FullOpen': 26, 'PosnPercCmd_Resd1': 27, 'PosnPercCmd_Resd2': 28, 'PosnPercCmd_Resd3': 29}
        compute_method = None
        length = 5
        startbit = 8
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class IntrReViewMirrDimSnvty:
        sig_name = "IntrReViewMirrDimSnvty"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IntrReViewMirrDimSnvty_Normal': 0, 'IntrReViewMirrDimSnvty_Dark': 1, 'IntrReViewMirrDimSnvty_Light': 2, 'IntrReViewMirrDimSnvty_Inhibit': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class DualSunroofCurtlrnCmdRearLrnCmd:
        sig_name = "DualSunroofCurtlrnCmdRearLrnCmd"
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
        sig_value_table = {'LrnCmd_NoCmd': 0, 'LrnCmd_ClrCmd': 1, 'LrnCmd_LrngCmd': 2, 'LrnCmd_Resd': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class DiagRequest1:
    msg_name = "DiagRequest1"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DiagResponse1:
    msg_name = "DiagResponse1"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['LCUL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class LCULLCUL_LIN2Fr05:
    msg_name = "LCULLCUL_LIN2Fr05"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUL"
    rx_nodes = ['OHC']
    sig_group_dict = {'ReadingLightFrntLeDrvReq': ['ReadingLightFrntLeDrvReqLightCmd', 'ReadingLightFrntLeDrvReqLiPerc', 'ReadingLightFrntLeDrvReqReadingLiDimsSpdCmd'], 'ReadingLightFrntRiDrvReq': ['ReadingLightFrntRiDrvReqLightCmd', 'ReadingLightFrntRiDrvReqLiPerc', 'ReadingLightFrntRiDrvReqReadingLiDimsSpdCmd']}
    sig_group_dataid_dict = {}

    class ReadingLightFrntRiDrvReqLightCmd:
        sig_name = "ReadingLightFrntRiDrvReqLightCmd"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 16
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReadingLightFrntRiDrvReqLiPerc:
        sig_name = "ReadingLightFrntRiDrvReqLiPerc"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 24
        byte = 3
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class ReadingLightFrntLeDrvReqLiPerc:
        sig_name = "ReadingLightFrntLeDrvReqLiPerc"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class ReadingLightFrntLeDrvReqLightCmd:
        sig_name = "ReadingLightFrntLeDrvReqLightCmd"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LightCmd_NoReq': 0, 'LightCmd_ON': 1, 'LightCmd_OFF': 2, 'LightCmd_TBD': 3}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReadingLightFrntLeDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightFrntLeDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class ReadingLightFrntRiDrvReqReadingLiDimsSpdCmd:
        sig_name = "ReadingLightFrntRiDrvReqReadingLiDimsSpdCmd"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReadingLiDimsSpdCmd_NoCmd': 0, 'ReadingLiDimsSpdCmd_400ms': 1, 'ReadingLiDimsSpdCmd_800ms': 2, 'ReadingLiDimsSpdCmd_1000ms': 3, 'ReadingLiDimsSpdCmd_2000ms': 4, 'ReadingLiDimsSpdCmd_Resverd': 5}
        compute_method = None
        length = 3
        startbit = 20
        byte = 2
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class OHCLCUL_LIN2Fr02:
    msg_name = "OHCLCUL_LIN2Fr02"
    msg_id = 11
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "OHC"
    rx_nodes = ['LCUL']
    sig_group_dict = {'OHCSerNo': ['OHCSerNoNr1', 'OHCSerNoNr2', 'OHCSerNoNr3', 'OHCSerNoNr4']}
    sig_group_dataid_dict = {}

    class OHCSerNoNr4:
        sig_name = "OHCSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OHCSerNoNr3:
        sig_name = "OHCSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OHCSerNoNr1:
        sig_name = "OHCSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OHCSerNoNr2:
        sig_name = "OHCSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


