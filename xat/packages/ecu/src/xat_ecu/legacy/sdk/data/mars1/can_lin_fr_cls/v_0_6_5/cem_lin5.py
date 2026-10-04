class CemCem_Lin5Fr01:
    msg_name = "CemCem_Lin5Fr01"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightFrontLeft': ['OrdinaryAmbientLightFrontLeftBlue', 'OrdinaryAmbientLightFrontLeftBrightness', 'OrdinaryAmbientLightFrontLeftGreen', 'OrdinaryAmbientLightFrontLeftRed']}
    sig_group_dataid_dict = {}

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


class CemCem_Lin5Fr17:
    msg_name = "CemCem_Lin5Fr17"
    msg_id = 23
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
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


class CemCem_Lin5Fr15:
    msg_name = "CemCem_Lin5Fr15"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM6FailrSts': ['ALM6FailrStsLEDSts', 'ALM6FailrStsTmpSts', 'ALM6FailrStsVltSts']}
    sig_group_dataid_dict = {}

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


class CemCem_Lin5Fr03:
    msg_name = "CemCem_Lin5Fr03"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightRearRight': ['OrdinaryAmbientLightRearRightBlue', 'OrdinaryAmbientLightRearRightBrightness', 'OrdinaryAmbientLightRearRightGreen', 'OrdinaryAmbientLightRearRightRed']}
    sig_group_dataid_dict = {}

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


class CemCem_Lin5Fr10:
    msg_name = "CemCem_Lin5Fr10"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
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


class DiagResponse4:
    msg_name = "DiagResponse4"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CemCem_Lin5Fr02:
    msg_name = "CemCem_Lin5Fr02"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
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


class CemCem_Lin5Fr06:
    msg_name = "CemCem_Lin5Fr06"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
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


class CemCem_Lin5Fr07:
    msg_name = "CemCem_Lin5Fr07"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightTweeterRight': ['OrdinaryAmbientLightTweeterRightBlue', 'OrdinaryAmbientLightTweeterRightBrightness', 'OrdinaryAmbientLightTweeterRightGreen', 'OrdinaryAmbientLightTweeterRightRed']}
    sig_group_dataid_dict = {}

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


class CemCem_Lin5Fr08:
    msg_name = "CemCem_Lin5Fr08"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightTweeterLeft': ['OrdinaryAmbientLightTweeterLeftBlue', 'OrdinaryAmbientLightTweeterLeftBrightness', 'OrdinaryAmbientLightTweeterLeftGreen', 'OrdinaryAmbientLightTweeterLeftRed']}
    sig_group_dataid_dict = {}

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


class CemCem_Lin5Fr12:
    msg_name = "CemCem_Lin5Fr12"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
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


class CemCem_Lin5Fr13:
    msg_name = "CemCem_Lin5Fr13"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM4FailrSts': ['ALM4FailrStsLEDSts', 'ALM4FailrStsTmpSts', 'ALM4FailrStsVltSts']}
    sig_group_dataid_dict = {}

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


class AlmCem_SerNrLin1Fr01:
    msg_name = "AlmCem_SerNrLin1Fr01"
    msg_id = 33
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALMSerNo': ['ALMSerNoNr1', 'ALMSerNoNr2', 'ALMSerNoNr3', 'ALMSerNoNr4']}
    sig_group_dataid_dict = {}

    class ALMSerNoNr1:
        sig_name = "ALMSerNoNr1"
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

    class ALMSerNoNr2:
        sig_name = "ALMSerNoNr2"
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

    class ALMSerNoNr4:
        sig_name = "ALMSerNoNr4"
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

    class ALMSerNoNr3:
        sig_name = "ALMSerNoNr3"
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


class CemCem_Lin5Fr05:
    msg_name = "CemCem_Lin5Fr05"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ALM1']
    sig_group_dict = {'OrdinaryAmbientLightCCRight': ['OrdinaryAmbientLightCCRightBlue', 'OrdinaryAmbientLightCCRightBrightness', 'OrdinaryAmbientLightCCRightGreen', 'OrdinaryAmbientLightCCRightRed']}
    sig_group_dataid_dict = {}

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


class CemCem_Lin5Fr11:
    msg_name = "CemCem_Lin5Fr11"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM2FailrSts': ['ALM2FailrStsLEDSts', 'ALM2FailrStsTmpSts', 'ALM2FailrStsVltSts']}
    sig_group_dataid_dict = {}

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


class CemCem_Lin5Fr14:
    msg_name = "CemCem_Lin5Fr14"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
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


class DiagRequest4:
    msg_name = "DiagRequest4"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class AlmCem_Lin1PartNrFr01:
    msg_name = "AlmCem_Lin1PartNrFr01"
    msg_id = 32
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALMPartNo10Cmpl': ['ALMPartNo10CmplEndSgn1', 'ALMPartNo10CmplEndSgn2', 'ALMPartNo10CmplEndSgn3', 'ALMPartNo10CmplNr1', 'ALMPartNo10CmplNr2', 'ALMPartNo10CmplNr3', 'ALMPartNo10CmplNr4', 'ALMPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class ALMPartNo10CmplEndSgn2:
        sig_name = "ALMPartNo10CmplEndSgn2"
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

    class ALMPartNo10CmplNr5:
        sig_name = "ALMPartNo10CmplNr5"
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

    class ALMPartNo10CmplNr1:
        sig_name = "ALMPartNo10CmplNr1"
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

    class ALMPartNo10CmplEndSgn3:
        sig_name = "ALMPartNo10CmplEndSgn3"
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

    class ALMPartNo10CmplNr2:
        sig_name = "ALMPartNo10CmplNr2"
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

    class ALMPartNo10CmplNr3:
        sig_name = "ALMPartNo10CmplNr3"
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

    class ALMPartNo10CmplNr4:
        sig_name = "ALMPartNo10CmplNr4"
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

    class ALMPartNo10CmplEndSgn1:
        sig_name = "ALMPartNo10CmplEndSgn1"
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


class CemCem_Lin5Fr04:
    msg_name = "CemCem_Lin5Fr04"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
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


class CemCem_Lin5Fr16:
    msg_name = "CemCem_Lin5Fr16"
    msg_id = 22
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "ALM1"
    rx_nodes = ['BGM']
    sig_group_dict = {'ALM7FailrSts': ['ALM7FailrStsLEDSts', 'ALM7FailrStsTmpSts', 'ALM7FailrStsVltSts']}
    sig_group_dataid_dict = {}

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


