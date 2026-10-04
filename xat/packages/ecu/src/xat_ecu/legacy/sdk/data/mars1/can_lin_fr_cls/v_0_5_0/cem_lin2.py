class FcsiEcm_Lin4Fr01:
    msg_name = "FcsiEcm_Lin4Fr01"
    msg_id = 32
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 3
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']


class FcsiEcm_Lin4SerNrFr01:
    msg_name = "FcsiEcm_Lin4SerNrFr01"
    msg_id = 35
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class FCSISerNoNr2:
        sig_name = "FCSISerNoNr2"
        sig_start_bit = 8
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

    class FCSISerNoNr1:
        sig_name = "FCSISerNoNr1"
        sig_start_bit = 0
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

    class FCSISerNoNr4:
        sig_name = "FCSISerNoNr4"
        sig_start_bit = 24
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

    class FCSISerNoNr3:
        sig_name = "FCSISerNoNr3"
        sig_start_bit = 16
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


class PrldCem_Lin2Fr02:
    msg_name = "PrldCem_Lin2Fr02"
    msg_id = 56
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class ChrgLidManvgDCorAcDcCalActvSts2:
        sig_name = "ChrgLidManvgDCorAcDcCalActvSts2"
        sig_start_bit = 14
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inact_Inactive': 0, 'Inact_Active': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ChrgLidManvgDCorAcDcActPosn2:
        sig_name = "ChrgLidManvgDCorAcDcActPosn2"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 126
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ChrgLidManvgDCorAcDcOverVoltFb:
        sig_name = "ChrgLidManvgDCorAcDcOverVoltFb"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ChrgLidManvgDCorAcDcMoveActvSts2:
        sig_name = "ChrgLidManvgDCorAcDcMoveActvSts2"
        sig_start_bit = 13
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inact_Inactive': 0, 'Inact_Active': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ChrgLidManvgDCorAcDcBlkFb:
        sig_name = "ChrgLidManvgDCorAcDcBlkFb"
        sig_start_bit = 17
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
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ChrgLidManvgDCorAcDcUnderVoltFb:
        sig_name = "ChrgLidManvgDCorAcDcUnderVoltFb"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ChrgLidManvgDCorAcDcCalRqrdFb:
        sig_name = "ChrgLidManvgDCorAcDcCalRqrdFb"
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

    class ChrgLidManvgDCorAcDcElecErrFb:
        sig_name = "ChrgLidManvgDCorAcDcElecErrFb"
        sig_start_bit = 18
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ChrgLidManvgDCorAcDcHldTqSts2:
        sig_name = "ChrgLidManvgDCorAcDcHldTqSts2"
        sig_start_bit = 12
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inact_Inactive': 0, 'Inact_Active': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ChrgLidManvgDCorAcDcOverTFb:
        sig_name = "ChrgLidManvgDCorAcDcOverTFb"
        sig_start_bit = 21
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
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ChrgLidManvgDCorAcDcOverTrvlFb:
        sig_name = "ChrgLidManvgDCorAcDcOverTrvlFb"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ChrgLidManvgDCorAcDcActTq2:
        sig_name = "ChrgLidManvgDCorAcDcActTq2"
        sig_start_bit = 8
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgLidManvgDCorAcDcActTq_NominalTorque': 0, 'ChrgLidManvgDCorAcDcActTq_reserved0': 1, 'ChrgLidManvgDCorAcDcActTq_LowTorque': 2, 'ChrgLidManvgDCorAcDcActTq_reserved1': 3}
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class CemCem_Lin2Fr06:
    msg_name = "CemCem_Lin2Fr06"
    msg_id = 40
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class ChrgLidManvgDCorAcDcCalReq2:
        sig_name = "ChrgLidManvgDCorAcDcCalReq2"
        sig_start_bit = 9
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inact_Inactive': 0, 'Inact_Active': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ChrgLidManvgDCorAcDcTqReq2:
        sig_name = "ChrgLidManvgDCorAcDcTqReq2"
        sig_start_bit = 10
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgLidManvgDCorAcDcActTq_NominalTorque': 0, 'ChrgLidManvgDCorAcDcActTq_reserved0': 1, 'ChrgLidManvgDCorAcDcActTq_LowTorque': 2, 'ChrgLidManvgDCorAcDcActTq_reserved1': 3}
        compute_method = None
        length = 4
        startbit = 10
        byte = 1
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class ChrgLidManvgDCorAcDcReq2:
        sig_name = "ChrgLidManvgDCorAcDcReq2"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 127
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class FcsiEcm_Lin4PartNrFr08:
    msg_name = "FcsiEcm_Lin4PartNrFr08"
    msg_id = 34
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class FCSIPartNoCmplEndSgn1:
        sig_name = "FCSIPartNoCmplEndSgn1"
        sig_start_bit = 32
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

    class FCSIPartNoCmplNr1:
        sig_name = "FCSIPartNoCmplNr1"
        sig_start_bit = 0
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

    class FCSIPartNoCmplNr3:
        sig_name = "FCSIPartNoCmplNr3"
        sig_start_bit = 16
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

    class FCSIPartNoCmplNr2:
        sig_name = "FCSIPartNoCmplNr2"
        sig_start_bit = 8
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

    class FCSIPartNoCmplEndSgn3:
        sig_name = "FCSIPartNoCmplEndSgn3"
        sig_start_bit = 48
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

    class FCSIPartNoCmplNr4:
        sig_name = "FCSIPartNoCmplNr4"
        sig_start_bit = 24
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

    class FCSIPartNoCmplEndSgn2:
        sig_name = "FCSIPartNoCmplEndSgn2"
        sig_start_bit = 40
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


class EcmEcm_Lin4Fr02:
    msg_name = "EcmEcm_Lin4Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class FastChrgnLEDIndctn_1_EcmEcm_Lin4SignalIPdu02:
        sig_name = "FastChrgnLEDIndctn_1_EcmEcm_Lin4SignalIPdu02"
        sig_start_bit = 18
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FastChrgnLEDIndctn_Default': 0, 'FastChrgnLEDIndctn_Green1': 1, 'FastChrgnLEDIndctn_Green2': 2, 'FastChrgnLEDIndctn_Green3': 3, 'FastChrgnLEDIndctn_Green4': 4, 'FastChrgnLEDIndctn_Red': 5, 'FastChrgnLEDIndctn_Green5': 6, 'FastChrgnLEDIndctn_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 18
        byte = 2
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class ChrgLidRearSts_1_EcmEcm_Lin4SignalIPdu02:
        sig_name = "ChrgLidRearSts_1_EcmEcm_Lin4SignalIPdu02"
        sig_start_bit = 21
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
        startbit = 21
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5


class DiagResponse1:
    msg_name = "DiagResponse1"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']


class DiagRequest1:
    msg_name = "DiagRequest1"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']


class FcsiEcm_Lin4PartNrFr04:
    msg_name = "FcsiEcm_Lin4PartNrFr04"
    msg_id = 33
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class FCSIPartNo10CmplNr3:
        sig_name = "FCSIPartNo10CmplNr3"
        sig_start_bit = 16
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

    class FCSIPartNo10CmplNr1:
        sig_name = "FCSIPartNo10CmplNr1"
        sig_start_bit = 0
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

    class FCSIPartNo10CmplNr5:
        sig_name = "FCSIPartNo10CmplNr5"
        sig_start_bit = 32
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

    class FCSIPartNo10CmplNr2:
        sig_name = "FCSIPartNo10CmplNr2"
        sig_start_bit = 8
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

    class FCSIPartNo10CmplEndSgn2:
        sig_name = "FCSIPartNo10CmplEndSgn2"
        sig_start_bit = 48
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

    class FCSIPartNo10CmplEndSgn3:
        sig_name = "FCSIPartNo10CmplEndSgn3"
        sig_start_bit = 56
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

    class FCSIPartNo10CmplEndSgn1:
        sig_name = "FCSIPartNo10CmplEndSgn1"
        sig_start_bit = 40
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

    class FCSIPartNo10CmplNr4:
        sig_name = "FCSIPartNo10CmplNr4"
        sig_start_bit = 24
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


