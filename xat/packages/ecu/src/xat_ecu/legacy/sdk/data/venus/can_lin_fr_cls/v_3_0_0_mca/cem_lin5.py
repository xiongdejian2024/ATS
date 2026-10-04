lin_scheduleTable = {'Cem_Lin5_DiagResponseSchedule01': [(0, 'Cem_Lin5LinTpDiagRespFrame', 0.015)], 'Cem_Lin5ScheduleTable01_CEM_LIN5': [(0, 'CemCem_Lin5Fr01', 0.015), (1, 'CemCem_Lin5Fr02', 0.015), (2, 'CemCem_Lin5Fr03', 0.015), (3, 'CemCem_Lin5Fr04', 0.015), (4, 'CemCem_Lin5Fr05', 0.015), (5, 'CemCem_Lin5Fr06', 0.015), (6, 'CemCem_Lin5Fr07', 0.015), (7, 'CemCem_Lin5Fr08', 0.015), (8, 'CemCem_Lin5Fr09', 0.015), (9, 'CemCem_Lin5Fr0A', 0.015), (10, 'CemCem_Lin5Fr0B', 0.015), (11, 'CemCem_Lin5Fr10', 0.015), (12, 'CemCem_Lin5Fr11', 0.015), (13, 'CemCem_Lin5Fr12', 0.015), (14, 'CemCem_Lin5Fr13', 0.015), (15, 'CemCem_Lin5Fr14', 0.015), (16, 'CemCem_Lin5Fr15', 0.015), (17, 'CemCem_Lin5Fr16', 0.015), (18, 'CemCem_Lin5Fr17', 0.015), (19, 'CemCem_Lin5Fr18', 0.015), (20, 'CemCem_Lin5Fr19', 0.015)], 'Cem_Lin5_DiagRequestSchedule01': [(0, 'Cem_Lin5LinTpDiagReqFrame', 0.015)]}


class CemCem_Lin5Fr15:
    msg_name = "CemCem_Lin5Fr15"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM6FailrSts': ['ALM6FailrStsLEDSts', 'ALM6FailrStsTmpSts', 'ALM6FailrStsVltSts']}
    sig_group_dataid_dict = {}

    class ALM6FailrStsLEDSts:
        sig_name = "ALM6FailrStsLEDSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ALM6FailrStsTmpSts:
        sig_name = "ALM6FailrStsTmpSts"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ALM6FailrStsVltSts:
        sig_name = "ALM6FailrStsVltSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class CemCem_Lin5Fr03:
    msg_name = "CemCem_Lin5Fr03"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightRearRight': ['OrdinaryAmbientLightRearRightBlue', 'OrdinaryAmbientLightRearRightBrightness', 'OrdinaryAmbientLightRearRightGreen', 'OrdinaryAmbientLightRearRightRed']}
    sig_group_dataid_dict = {}

    class OrdinaryAmbientLightRearRightGreen:
        sig_name = "OrdinaryAmbientLightRearRightGreen"
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

    class OrdinaryAmbientLightRearRightBrightness:
        sig_name = "OrdinaryAmbientLightRearRightBrightness"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class OrdinaryAmbientLightRearRightRed:
        sig_name = "OrdinaryAmbientLightRearRightRed"
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

    class OrdinaryAmbientLightRearRightBlue:
        sig_name = "OrdinaryAmbientLightRearRightBlue"
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


class CemCem_Lin5Fr06:
    msg_name = "CemCem_Lin5Fr06"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightCCLeft': ['OrdinaryAmbientLightCCLeftBlue', 'OrdinaryAmbientLightCCLeftBrightness', 'OrdinaryAmbientLightCCLeftGreen', 'OrdinaryAmbientLightCCLeftRed']}
    sig_group_dataid_dict = {}

    class OrdinaryAmbientLightCCLeftBlue:
        sig_name = "OrdinaryAmbientLightCCLeftBlue"
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

    class OrdinaryAmbientLightCCLeftBrightness:
        sig_name = "OrdinaryAmbientLightCCLeftBrightness"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class OrdinaryAmbientLightCCLeftGreen:
        sig_name = "OrdinaryAmbientLightCCLeftGreen"
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

    class OrdinaryAmbientLightCCLeftRed:
        sig_name = "OrdinaryAmbientLightCCLeftRed"
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


class CemCem_Lin5Fr19:
    msg_name = "CemCem_Lin5Fr19"
    msg_id = 25
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM10FailrSts': ['ALM10FailrStsLEDSts', 'ALM10FailrStsTmpSts', 'ALM10FailrStsVltSts']}
    sig_group_dataid_dict = {}

    class ALM10FailrStsVltSts:
        sig_name = "ALM10FailrStsVltSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ALM10FailrStsLEDSts:
        sig_name = "ALM10FailrStsLEDSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ALM10FailrStsTmpSts:
        sig_name = "ALM10FailrStsTmpSts"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class CemCem_Lin5Fr13:
    msg_name = "CemCem_Lin5Fr13"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM4FailrSts': ['ALM4FailrStsLEDSts', 'ALM4FailrStsTmpSts', 'ALM4FailrStsVltSts']}
    sig_group_dataid_dict = {}

    class ALM4FailrStsVltSts:
        sig_name = "ALM4FailrStsVltSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ALM4FailrStsTmpSts:
        sig_name = "ALM4FailrStsTmpSts"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ALM4FailrStsLEDSts:
        sig_name = "ALM4FailrStsLEDSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CemCem_Lin5Fr04:
    msg_name = "CemCem_Lin5Fr04"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightFrontRight': ['OrdinaryAmbientLightFrontRightBlue', 'OrdinaryAmbientLightFrontRightBrightness', 'OrdinaryAmbientLightFrontRightGreen', 'OrdinaryAmbientLightFrontRightRed']}
    sig_group_dataid_dict = {}

    class OrdinaryAmbientLightFrontRightGreen:
        sig_name = "OrdinaryAmbientLightFrontRightGreen"
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

    class OrdinaryAmbientLightFrontRightBlue:
        sig_name = "OrdinaryAmbientLightFrontRightBlue"
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

    class OrdinaryAmbientLightFrontRightRed:
        sig_name = "OrdinaryAmbientLightFrontRightRed"
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

    class OrdinaryAmbientLightFrontRightBrightness:
        sig_name = "OrdinaryAmbientLightFrontRightBrightness"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0


class CemCem_Lin5Fr17:
    msg_name = "CemCem_Lin5Fr17"
    msg_id = 23
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM8FailrSts': ['ALM8FailrStsLEDSts', 'ALM8FailrStsTmpSts', 'ALM8FailrStsVltSts']}
    sig_group_dataid_dict = {}

    class ALM8FailrStsLEDSts:
        sig_name = "ALM8FailrStsLEDSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ALM8FailrStsVltSts:
        sig_name = "ALM8FailrStsVltSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ALM8FailrStsTmpSts:
        sig_name = "ALM8FailrStsTmpSts"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class CemCem_Lin5Fr09:
    msg_name = "CemCem_Lin5Fr09"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightCCMiddleRight': ['OrdinaryAmbientLightCCMiddleRightBlue', 'OrdinaryAmbientLightCCMiddleRightBrightness', 'OrdinaryAmbientLightCCMiddleRightGreen', 'OrdinaryAmbientLightCCMiddleRightRed']}
    sig_group_dataid_dict = {}

    class OrdinaryAmbientLightCCMiddleRightRed:
        sig_name = "OrdinaryAmbientLightCCMiddleRightRed"
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

    class OrdinaryAmbientLightCCMiddleRightGreen:
        sig_name = "OrdinaryAmbientLightCCMiddleRightGreen"
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

    class OrdinaryAmbientLightCCMiddleRightBrightness:
        sig_name = "OrdinaryAmbientLightCCMiddleRightBrightness"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class OrdinaryAmbientLightCCMiddleRightBlue:
        sig_name = "OrdinaryAmbientLightCCMiddleRightBlue"
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


class CemCem_Lin5Fr16:
    msg_name = "CemCem_Lin5Fr16"
    msg_id = 22
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM7FailrSts': ['ALM7FailrStsLEDSts', 'ALM7FailrStsTmpSts', 'ALM7FailrStsVltSts']}
    sig_group_dataid_dict = {}

    class ALM7FailrStsTmpSts:
        sig_name = "ALM7FailrStsTmpSts"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ALM7FailrStsVltSts:
        sig_name = "ALM7FailrStsVltSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ALM7FailrStsLEDSts:
        sig_name = "ALM7FailrStsLEDSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CemCem_Lin5Fr08:
    msg_name = "CemCem_Lin5Fr08"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightTweeterLeft': ['OrdinaryAmbientLightTweeterLeftBlue', 'OrdinaryAmbientLightTweeterLeftBrightness', 'OrdinaryAmbientLightTweeterLeftGreen', 'OrdinaryAmbientLightTweeterLeftRed']}
    sig_group_dataid_dict = {}

    class OrdinaryAmbientLightTweeterLeftGreen:
        sig_name = "OrdinaryAmbientLightTweeterLeftGreen"
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

    class OrdinaryAmbientLightTweeterLeftBlue:
        sig_name = "OrdinaryAmbientLightTweeterLeftBlue"
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

    class OrdinaryAmbientLightTweeterLeftRed:
        sig_name = "OrdinaryAmbientLightTweeterLeftRed"
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

    class OrdinaryAmbientLightTweeterLeftBrightness:
        sig_name = "OrdinaryAmbientLightTweeterLeftBrightness"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0


class CemCem_Lin5Fr18:
    msg_name = "CemCem_Lin5Fr18"
    msg_id = 24
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM9FailrSts': ['ALM9FailrStsLEDSts', 'ALM9FailrStsTmpSts', 'ALM9FailrStsVltSts']}
    sig_group_dataid_dict = {}

    class ALM9FailrStsTmpSts:
        sig_name = "ALM9FailrStsTmpSts"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ALM9FailrStsVltSts:
        sig_name = "ALM9FailrStsVltSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ALM9FailrStsLEDSts:
        sig_name = "ALM9FailrStsLEDSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CemCem_Lin5Fr11:
    msg_name = "CemCem_Lin5Fr11"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM2FailrSts': ['ALM2FailrStsLEDSts', 'ALM2FailrStsTmpSts', 'ALM2FailrStsVltSts']}
    sig_group_dataid_dict = {}

    class ALM2FailrStsVltSts:
        sig_name = "ALM2FailrStsVltSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ALM2FailrStsTmpSts:
        sig_name = "ALM2FailrStsTmpSts"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ALM2FailrStsLEDSts:
        sig_name = "ALM2FailrStsLEDSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CemCem_Lin5Fr01:
    msg_name = "CemCem_Lin5Fr01"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightFrontLeft': ['OrdinaryAmbientLightFrontLeftBlue', 'OrdinaryAmbientLightFrontLeftBrightness', 'OrdinaryAmbientLightFrontLeftGreen', 'OrdinaryAmbientLightFrontLeftRed']}
    sig_group_dataid_dict = {}

    class OrdinaryAmbientLightFrontLeftGreen:
        sig_name = "OrdinaryAmbientLightFrontLeftGreen"
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

    class OrdinaryAmbientLightFrontLeftRed:
        sig_name = "OrdinaryAmbientLightFrontLeftRed"
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

    class OrdinaryAmbientLightFrontLeftBlue:
        sig_name = "OrdinaryAmbientLightFrontLeftBlue"
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

    class OrdinaryAmbientLightFrontLeftBrightness:
        sig_name = "OrdinaryAmbientLightFrontLeftBrightness"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0


class CemCem_Lin5Fr05:
    msg_name = "CemCem_Lin5Fr05"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightCCRight': ['OrdinaryAmbientLightCCRightBlue', 'OrdinaryAmbientLightCCRightBrightness', 'OrdinaryAmbientLightCCRightGreen', 'OrdinaryAmbientLightCCRightRed']}
    sig_group_dataid_dict = {}

    class OrdinaryAmbientLightCCRightRed:
        sig_name = "OrdinaryAmbientLightCCRightRed"
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

    class OrdinaryAmbientLightCCRightBrightness:
        sig_name = "OrdinaryAmbientLightCCRightBrightness"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class OrdinaryAmbientLightCCRightGreen:
        sig_name = "OrdinaryAmbientLightCCRightGreen"
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

    class OrdinaryAmbientLightCCRightBlue:
        sig_name = "OrdinaryAmbientLightCCRightBlue"
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


class Cem_Lin5LinTpDiagReqFrame:
    msg_name = "Cem_Lin5LinTpDiagReqFrame"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CemCem_Lin5Fr10:
    msg_name = "CemCem_Lin5Fr10"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM1FailrSts': ['ALM1FailrStsLEDSts', 'ALM1FailrStsTmpSts', 'ALM1FailrStsVltSts']}
    sig_group_dataid_dict = {}

    class ALM1FailrStsTmpSts:
        sig_name = "ALM1FailrStsTmpSts"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ALM1FailrStsVltSts:
        sig_name = "ALM1FailrStsVltSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ALM1FailrStsLEDSts:
        sig_name = "ALM1FailrStsLEDSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CemCem_Lin5Fr0A:
    msg_name = "CemCem_Lin5Fr0A"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightCCMiddleLeft': ['OrdinaryAmbientLightCCMiddleLeftBlue', 'OrdinaryAmbientLightCCMiddleLeftBrightness', 'OrdinaryAmbientLightCCMiddleLeftGreen', 'OrdinaryAmbientLightCCMiddleLeftRed']}
    sig_group_dataid_dict = {}

    class OrdinaryAmbientLightCCMiddleLeftRed:
        sig_name = "OrdinaryAmbientLightCCMiddleLeftRed"
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

    class OrdinaryAmbientLightCCMiddleLeftBrightness:
        sig_name = "OrdinaryAmbientLightCCMiddleLeftBrightness"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class OrdinaryAmbientLightCCMiddleLeftGreen:
        sig_name = "OrdinaryAmbientLightCCMiddleLeftGreen"
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

    class OrdinaryAmbientLightCCMiddleLeftBlue:
        sig_name = "OrdinaryAmbientLightCCMiddleLeftBlue"
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


class CemCem_Lin5Fr07:
    msg_name = "CemCem_Lin5Fr07"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightTweeterRight': ['OrdinaryAmbientLightTweeterRightBlue', 'OrdinaryAmbientLightTweeterRightBrightness', 'OrdinaryAmbientLightTweeterRightGreen', 'OrdinaryAmbientLightTweeterRightRed']}
    sig_group_dataid_dict = {}

    class OrdinaryAmbientLightTweeterRightGreen:
        sig_name = "OrdinaryAmbientLightTweeterRightGreen"
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

    class OrdinaryAmbientLightTweeterRightBlue:
        sig_name = "OrdinaryAmbientLightTweeterRightBlue"
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

    class OrdinaryAmbientLightTweeterRightRed:
        sig_name = "OrdinaryAmbientLightTweeterRightRed"
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

    class OrdinaryAmbientLightTweeterRightBrightness:
        sig_name = "OrdinaryAmbientLightTweeterRightBrightness"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0


class CemCem_Lin5Fr14:
    msg_name = "CemCem_Lin5Fr14"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM5FailrSts': ['ALM5FailrStsLEDSts', 'ALM5FailrStsTmpSts', 'ALM5FailrStsVltSts']}
    sig_group_dataid_dict = {}

    class ALM5FailrStsTmpSts:
        sig_name = "ALM5FailrStsTmpSts"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ALM5FailrStsLEDSts:
        sig_name = "ALM5FailrStsLEDSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ALM5FailrStsVltSts:
        sig_name = "ALM5FailrStsVltSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class CemCem_Lin5Fr12:
    msg_name = "CemCem_Lin5Fr12"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM3FailrSts': ['ALM3FailrStsLEDSts', 'ALM3FailrStsTmpSts', 'ALM3FailrStsVltSts']}
    sig_group_dataid_dict = {}

    class ALM3FailrStsVltSts:
        sig_name = "ALM3FailrStsVltSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ALM3FailrStsLEDSts:
        sig_name = "ALM3FailrStsLEDSts"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ALM3FailrStsTmpSts:
        sig_name = "ALM3FailrStsTmpSts"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class Cem_Lin5LinTpDiagRespFrame:
    msg_name = "Cem_Lin5LinTpDiagRespFrame"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CemCem_Lin5Fr0B:
    msg_name = "CemCem_Lin5Fr0B"
    msg_id = 11
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightCCUnder': ['OrdinaryAmbientLightCCUnderBlue', 'OrdinaryAmbientLightCCUnderBrightness', 'OrdinaryAmbientLightCCUnderGreen', 'OrdinaryAmbientLightCCUnderRed']}
    sig_group_dataid_dict = {}

    class OrdinaryAmbientLightCCUnderBrightness:
        sig_name = "OrdinaryAmbientLightCCUnderBrightness"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class OrdinaryAmbientLightCCUnderGreen:
        sig_name = "OrdinaryAmbientLightCCUnderGreen"
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

    class OrdinaryAmbientLightCCUnderRed:
        sig_name = "OrdinaryAmbientLightCCUnderRed"
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

    class OrdinaryAmbientLightCCUnderBlue:
        sig_name = "OrdinaryAmbientLightCCUnderBlue"
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


class CemCem_Lin5Fr02:
    msg_name = "CemCem_Lin5Fr02"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightRearLeft': ['OrdinaryAmbientLightRearLeftBlue', 'OrdinaryAmbientLightRearLeftBrightness', 'OrdinaryAmbientLightRearLeftGreen', 'OrdinaryAmbientLightRearLeftRed']}
    sig_group_dataid_dict = {}

    class OrdinaryAmbientLightRearLeftRed:
        sig_name = "OrdinaryAmbientLightRearLeftRed"
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

    class OrdinaryAmbientLightRearLeftBrightness:
        sig_name = "OrdinaryAmbientLightRearLeftBrightness"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 8
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class OrdinaryAmbientLightRearLeftBlue:
        sig_name = "OrdinaryAmbientLightRearLeftBlue"
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

    class OrdinaryAmbientLightRearLeftGreen:
        sig_name = "OrdinaryAmbientLightRearLeftGreen"
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


