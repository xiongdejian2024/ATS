class OhcCem_Lin3Fr05:
    msg_name = "OhcCem_Lin3Fr05"
    msg_id = 22
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 2
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class OHCPINFlt:
        sig_name = "OHCPINFlt"
        sig_start_bit = 0
        sig_length = 12
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]


class CemCem_Lin3Fr05:
    msg_name = "CemCem_Lin3Fr05"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class IntrLiRoofAUTOIndication:
        sig_name = "IntrLiRoofAUTOIndication"
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

    class IntrLiGen2RoofResetMemory:
        sig_name = "IntrLiGen2RoofResetMemory"
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

    class MoodLiAmbLightSettingTransitionTime:
        sig_name = "MoodLiAmbLightSettingTransitionTime"
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

    class MoodLiAmbLightSettingRed:
        sig_name = "MoodLiAmbLightSettingRed"
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

    class MoodLiAmbLightSettingGreen:
        sig_name = "MoodLiAmbLightSettingGreen"
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

    class IntrLiGen2RoofDimSpeed:
        sig_name = "IntrLiGen2RoofDimSpeed"
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

    class MoodLiAmbLightSettingIntensity:
        sig_name = "MoodLiAmbLightSettingIntensity"
        sig_start_bit = 3
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 3
        byte = 0
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class MoodLiAmbLightSettingBlue:
        sig_name = "MoodLiAmbLightSettingBlue"
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

    class MoodLiAmbLightSettingSynchDelay:
        sig_name = "MoodLiAmbLightSettingSynchDelay"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0


class SigCem_Lin3SerNrFr01:
    msg_name = "SigCem_Lin3SerNrFr01"
    msg_id = 46
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class SIGSerNoNr4:
        sig_name = "SIGSerNoNr4"
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

    class SIGSerNoNr2:
        sig_name = "SIGSerNoNr2"
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

    class SIGSerNoNr3:
        sig_name = "SIGSerNoNr3"
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

    class SIGSerNoNr1:
        sig_name = "SIGSerNoNr1"
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


class DiagRequest2:
    msg_name = "DiagRequest2"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']


class OhcCem_Lin3Fr04:
    msg_name = "OhcCem_Lin3Fr04"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 1
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class BtnStsOHCLiBtnReadingRi:
        sig_name = "BtnStsOHCLiBtnReadingRi"
        sig_start_bit = 3
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BtnStsSngTyp_Idle': 0, 'BtnStsSngTyp_BtnPsd': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BtnStsOHCIntrLiSwtAllOnSts:
        sig_name = "BtnStsOHCIntrLiSwtAllOnSts"
        sig_start_bit = 0
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BtnStsSngTyp_Idle': 0, 'BtnStsSngTyp_BtnPsd': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class IntrLiGen2RoofSwtAllOn:
        sig_name = "IntrLiGen2RoofSwtAllOn"
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

    class BtnStsOHCIntrLiSwtAutOnSts:
        sig_name = "BtnStsOHCIntrLiSwtAutOnSts"
        sig_start_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BtnStsSngTyp_Idle': 0, 'BtnStsSngTyp_BtnPsd': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BtnStsOHCLiBtnReadingLe:
        sig_name = "BtnStsOHCLiBtnReadingLe"
        sig_start_bit = 2
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BtnStsSngTyp_Idle': 0, 'BtnStsSngTyp_BtnPsd': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class IntrLiGen2RoofSwtAuto:
        sig_name = "IntrLiGen2RoofSwtAuto"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class SigCem_Lin3Fr01:
    msg_name = "SigCem_Lin3Fr01"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class ElecChromRoofFb_0_SigCem_Lin3SignalIPdu01:
        sig_name = "ElecChromRoofFb_0_SigCem_Lin3SignalIPdu01"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ElecChromFailr:
        sig_name = "ElecChromFailr"
        sig_start_bit = 8
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
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class SigCem_Lin3PartNrFr04:
    msg_name = "SigCem_Lin3PartNrFr04"
    msg_id = 44
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class SIGPartNo10CmplEndSgn3:
        sig_name = "SIGPartNo10CmplEndSgn3"
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

    class SIGPartNo10CmplNr3:
        sig_name = "SIGPartNo10CmplNr3"
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

    class SIGPartNo10CmplNr5:
        sig_name = "SIGPartNo10CmplNr5"
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

    class SIGPartNo10CmplNr1:
        sig_name = "SIGPartNo10CmplNr1"
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

    class SIGPartNo10CmplNr4:
        sig_name = "SIGPartNo10CmplNr4"
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

    class SIGPartNo10CmplEndSgn2:
        sig_name = "SIGPartNo10CmplEndSgn2"
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

    class SIGPartNo10CmplEndSgn1:
        sig_name = "SIGPartNo10CmplEndSgn1"
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

    class SIGPartNo10CmplNr2:
        sig_name = "SIGPartNo10CmplNr2"
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


class OhcCem_Lin3Fr01:
    msg_name = "OhcCem_Lin3Fr01"
    msg_id = 32
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class ReadLiStsSecondRowRi:
        sig_name = "ReadLiStsSecondRowRi"
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

    class PassAirbLampStsRecPassAirbLampSts_0_OhcCem_Lin3SignalIPdu01:
        sig_name = "PassAirbLampStsRecPassAirbLampSts_0_OhcCem_Lin3SignalIPdu01"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PassAirbLampSts1_Resd1': 0, 'PassAirbLampSts1_LampStsOk': 1, 'PassAirbLampSts1_LampStsNotOk': 2, 'PassAirbLampSts1_Resd2': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SunRoofAndCurtBtnSts2Cntr:
        sig_name = "SunRoofAndCurtBtnSts2Cntr"
        sig_start_bit = 48
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
        startbit = 48
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SftyBltTelltlFlt:
        sig_name = "SftyBltTelltlFlt"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReadLiStsThirdRowLe:
        sig_name = "ReadLiStsThirdRowLe"
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

    class BtnStsOHCRLiBtnReadingLe:
        sig_name = "BtnStsOHCRLiBtnReadingLe"
        sig_start_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BtnStsSngTyp_Idle': 0, 'BtnStsSngTyp_BtnPsd': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BtnStsOHTRLiBtnReadingRi:
        sig_name = "BtnStsOHTRLiBtnReadingRi"
        sig_start_bit = 39
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BtnStsSngTyp_Idle': 0, 'BtnStsSngTyp_BtnPsd': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BtnStsOHCRLiBtnReadingRi:
        sig_name = "BtnStsOHCRLiBtnReadingRi"
        sig_start_bit = 47
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BtnStsSngTyp_Idle': 0, 'BtnStsSngTyp_BtnPsd': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class IntrLiCmdGroupIntrLiRoofDmdOff:
        sig_name = "IntrLiCmdGroupIntrLiRoofDmdOff"
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

    class ReadLiStsFirstRowRi:
        sig_name = "ReadLiStsFirstRowRi"
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

    class ReadLiStsSecondRowLe:
        sig_name = "ReadLiStsSecondRowLe"
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

    class ReadLiStsFirstRowLe:
        sig_name = "ReadLiStsFirstRowLe"
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

    class PassAirbLampStsRecPassAirbLampStsCntr_0_OhcCem_Lin3SignalIPdu01:
        sig_name = "PassAirbLampStsRecPassAirbLampStsCntr_0_OhcCem_Lin3SignalIPdu01"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SunRoofAndCurtBtnSts2Pos:
        sig_name = "SunRoofAndCurtBtnSts2Pos"
        sig_start_bit = 50
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SunRoofAndCurtBtnStsTyp2_Idle': 0, 'SunRoofAndCurtBtnStsTyp2_BackwStep1': 1, 'SunRoofAndCurtBtnStsTyp2_BackwStep2': 2, 'SunRoofAndCurtBtnStsTyp2_ForwStep1': 3, 'SunRoofAndCurtBtnStsTyp2_ForwStep2': 4, 'SunRoofAndCurtBtnStsTyp2_TiltUpStep1': 5, 'SunRoofAndCurtBtnStsTyp2_TiltDwnStep1': 6, 'SunRoofAndCurtBtnStsTyp2_Failr': 7}
        compute_method = None
        length = 3
        startbit = 50
        byte = 6
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class ReadLiStsThirdRowRi:
        sig_name = "ReadLiStsThirdRowRi"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class IntrLiCmdGroupIntrLiActvn:
        sig_name = "IntrLiCmdGroupIntrLiActvn"
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

    class PassAirbLampStsRecPassAirbLampStsChks_0_OhcCem_Lin3SignalIPdu01:
        sig_name = "PassAirbLampStsRecPassAirbLampStsChks_0_OhcCem_Lin3SignalIPdu01"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IntrLiCmdGroupIntrLiRoofDim:
        sig_name = "IntrLiCmdGroupIntrLiRoofDim"
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

    class BtnStsOHTRLiBtnReadingLe:
        sig_name = "BtnStsOHTRLiBtnReadingLe"
        sig_start_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BtnStsSngTyp_Idle': 0, 'BtnStsSngTyp_BtnPsd': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class CemCem_Lin3Fr03:
    msg_name = "CemCem_Lin3Fr03"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class IntrBriSts_2_CemCem_Lin3SignalIPdu03:
        sig_name = "IntrBriSts_2_CemCem_Lin3SignalIPdu03"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class ActvnOfRoofSwtIllmn:
        sig_name = "ActvnOfRoofSwtIllmn"
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

    class ReadLiOpenReqFrontLeft:
        sig_name = "ReadLiOpenReqFrontLeft"
        sig_start_bit = 0
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ReadLiOpenReqThirdRowLeft:
        sig_name = "ReadLiOpenReqThirdRowLeft"
        sig_start_bit = 8
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TwliBriSts_2_CemCem_Lin3SignalIPdu03:
        sig_name = "TwliBriSts_2_CemCem_Lin3SignalIPdu03"
        sig_start_bit = 18
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TwliBriSts1_Night': 0, 'TwliBriSts1_Day': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ReadLiOpenReqFrontRight:
        sig_name = "ReadLiOpenReqFrontRight"
        sig_start_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ReadLiOpenReqThirdRowRight:
        sig_name = "ReadLiOpenReqThirdRowRight"
        sig_start_bit = 10
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class RlyPwrDistbnCmd1WdIgnRlyCmd_1_CemCem_Lin3SignalIPdu03:
        sig_name = "RlyPwrDistbnCmd1WdIgnRlyCmd_1_CemCem_Lin3SignalIPdu03"
        sig_start_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReadLiOpenReqSecondRowRight:
        sig_name = "ReadLiOpenReqSecondRowRight"
        sig_start_bit = 6
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ReadLiOpenReqSecondRowLeft:
        sig_name = "ReadLiOpenReqSecondRowLeft"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class DiagResponse2:
    msg_name = "DiagResponse2"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']


class SigCem_Lin3PartNrFr08:
    msg_name = "SigCem_Lin3PartNrFr08"
    msg_id = 45
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class SIGPartNoCmplNr3:
        sig_name = "SIGPartNoCmplNr3"
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

    class SIGPartNoCmplNr4:
        sig_name = "SIGPartNoCmplNr4"
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

    class SIGPartNoCmplEndSgn2:
        sig_name = "SIGPartNoCmplEndSgn2"
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

    class SIGPartNoCmplNr2:
        sig_name = "SIGPartNoCmplNr2"
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

    class SIGPartNoCmplNr1:
        sig_name = "SIGPartNoCmplNr1"
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

    class SIGPartNoCmplEndSgn3:
        sig_name = "SIGPartNoCmplEndSgn3"
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

    class SIGPartNoCmplEndSgn1:
        sig_name = "SIGPartNoCmplEndSgn1"
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


class CemCem_Lin3Fr01:
    msg_name = "CemCem_Lin3Fr01"
    msg_id = 0
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class PassAirbLampReqPassAirbLampDiReq_1_CemCem_Lin3SignalIPdu01:
        sig_name = "PassAirbLampReqPassAirbLampDiReq_1_CemCem_Lin3SignalIPdu01"
        sig_start_bit = 46
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PassAirbLampReq_LampNotCfgd': 0, 'PassAirbLampReq_LampOn': 1, 'PassAirbLampReq_LampOff': 2, 'PassAirbLampReq_Resd': 3}
        compute_method = None
        length = 2
        startbit = 46
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PassAirbLampReqPassAirbLampEnaReq_1_CemCem_Lin3SignalIPdu01:
        sig_name = "PassAirbLampReqPassAirbLampEnaReq_1_CemCem_Lin3SignalIPdu01"
        sig_start_bit = 44
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PassAirbLampReq_LampNotCfgd': 0, 'PassAirbLampReq_LampOn': 1, 'PassAirbLampReq_LampOff': 2, 'PassAirbLampReq_Resd': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LeSolarData_2_CemCem_Lin3SignalIPdu01:
        sig_name = "LeSolarData_2_CemCem_Lin3SignalIPdu01"
        sig_start_bit = 8
        sig_length = 8
        sig_value_factor = 5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 51
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BltRmnTelltl:
        sig_name = "BltRmnTelltl"
        sig_start_bit = 55
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Trig1_NoTrig': 0, 'Trig1_Trig': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PassAirbLampReqChgOfPassAirbSts_1_CemCem_Lin3SignalIPdu01:
        sig_name = "PassAirbLampReqChgOfPassAirbSts_1_CemCem_Lin3SignalIPdu01"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqForDisp_Idle': 0, 'ReqForDisp_IndcnReqd': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PassAirbLampReqChks_1_CemCem_Lin3SignalIPdu01:
        sig_name = "PassAirbLampReqChks_1_CemCem_Lin3SignalIPdu01"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RiSolarData_2_CemCem_Lin3SignalIPdu01:
        sig_name = "RiSolarData_2_CemCem_Lin3SignalIPdu01"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = 5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 51
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PassAirbLampReqCntr_1_CemCem_Lin3SignalIPdu01:
        sig_name = "PassAirbLampReqCntr_1_CemCem_Lin3SignalIPdu01"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class CemCem_Lin3Fr04:
    msg_name = "CemCem_Lin3Fr04"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class IntrLiGen2RoofParametersINtrlLiCourtesyLvl:
        sig_name = "IntrLiGen2RoofParametersINtrlLiCourtesyLvl"
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

    class IntrLiGen2RoofRequestIntrLiGen2RoofReqZon5:
        sig_name = "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon5"
        sig_start_bit = 56
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Unknow': 0, 'Welcome': 1, 'Courtesy': 2, 'Manual': 3, 'Polite': 4, 'ForceOn': 5, 'ForceOff': 6}
        compute_method = None
        length = 3
        startbit = 56
        byte = 7
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class IntrLiGen2RoofRequestIntrLiGen2RoofReqZon1:
        sig_name = "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon1"
        sig_start_bit = 42
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Unknow': 0, 'Welcome': 1, 'Courtesy': 2, 'Manual': 3, 'Polite': 4, 'ForceOn': 5, 'ForceOff': 6}
        compute_method = None
        length = 3
        startbit = 42
        byte = 5
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class IntrLiGen2RoofParametersIntrlLiPoliteLvl:
        sig_name = "IntrLiGen2RoofParametersIntrlLiPoliteLvl"
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

    class IntrLiGen2RoofRequestIntrLiGen2RoofReqZon4:
        sig_name = "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon4"
        sig_start_bit = 51
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Unknow': 0, 'Welcome': 1, 'Courtesy': 2, 'Manual': 3, 'Polite': 4, 'ForceOn': 5, 'ForceOff': 6}
        compute_method = None
        length = 3
        startbit = 51
        byte = 6
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class IntrLiGen2RoofParametersIntrLiWelcomeLvl:
        sig_name = "IntrLiGen2RoofParametersIntrLiWelcomeLvl"
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

    class IntrLiGen2RoofParametersIntrlLiAmbienceLvl:
        sig_name = "IntrLiGen2RoofParametersIntrlLiAmbienceLvl"
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

    class IntrLiGen2RoofRequestIntrLiGen2RoofReqZon6:
        sig_name = "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon6"
        sig_start_bit = 59
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Unknow': 0, 'Welcome': 1, 'Courtesy': 2, 'Manual': 3, 'Polite': 4, 'ForceOn': 5, 'ForceOff': 6}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class IntrLiGen2RoofRequestIntrLiGen2RoofReqZon2:
        sig_name = "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon2"
        sig_start_bit = 45
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Unknow': 0, 'Welcome': 1, 'Courtesy': 2, 'Manual': 3, 'Polite': 4, 'ForceOn': 5, 'ForceOff': 6}
        compute_method = None
        length = 3
        startbit = 45
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class IntrLiGen2RoofParametersIntrLiForceOnLvl:
        sig_name = "IntrLiGen2RoofParametersIntrLiForceOnLvl"
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

    class IntrLiGen2RoofRequestIntrLiGen2RoofReqZon3:
        sig_name = "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon3"
        sig_start_bit = 48
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Unknow': 0, 'Welcome': 1, 'Courtesy': 2, 'Manual': 3, 'Polite': 4, 'ForceOn': 5, 'ForceOff': 6}
        compute_method = None
        length = 3
        startbit = 48
        byte = 6
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class CemCem_Lin3Fr07:
    msg_name = "CemCem_Lin3Fr07"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class StoAmbLiStngGreen_1_CemCem_Lin3SignalIPdu07:
        sig_name = "StoAmbLiStngGreen_1_CemCem_Lin3SignalIPdu07"
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

    class ElecChromCmd:
        sig_name = "ElecChromCmd"
        sig_start_bit = 48
        sig_length = 8
        sig_value_factor = 0.39215686274509803
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 26
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class StoAmbLiStngIntensity_1_CemCem_Lin3SignalIPdu07:
        sig_name = "StoAmbLiStngIntensity_1_CemCem_Lin3SignalIPdu07"
        sig_start_bit = 3
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 3
        byte = 0
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class SunRoofDimEna:
        sig_name = "SunRoofDimEna"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SunRoofAndCurtEnaTyp_Di': 0, 'SunRoofAndCurtEnaTyp_LimdEna': 1, 'SunRoofAndCurtEnaTyp_FullEna': 2, 'SunRoofAndCurtEnaTyp_Resd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class StoAmbLiStngTransitionTime_1_CemCem_Lin3SignalIPdu07:
        sig_name = "StoAmbLiStngTransitionTime_1_CemCem_Lin3SignalIPdu07"
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

    class StoAmbLiStngRed_1_CemCem_Lin3SignalIPdu07:
        sig_name = "StoAmbLiStngRed_1_CemCem_Lin3SignalIPdu07"
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

    class StoAmbLiStngSynchDelay_1_CemCem_Lin3SignalIPdu07:
        sig_name = "StoAmbLiStngSynchDelay_1_CemCem_Lin3SignalIPdu07"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class StoAmbLiStngBlue_1_CemCem_Lin3SignalIPdu07:
        sig_name = "StoAmbLiStngBlue_1_CemCem_Lin3SignalIPdu07"
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


class CemCem_Lin3Fr06:
    msg_name = "CemCem_Lin3Fr06"
    msg_id = 29
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class MoodLiSwtIdPen:
        sig_name = "MoodLiSwtIdPen"
        sig_start_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AmbTRawQly_3_CemCem_Lin3SignalIPdu06:
        sig_name = "AmbTRawQly_3_CemCem_Lin3SignalIPdu06"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class AmbTRawAmbTVal_3_CemCem_Lin3SignalIPdu06:
        sig_name = "AmbTRawAmbTVal_3_CemCem_Lin3SignalIPdu06"
        sig_start_bit = 40
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-70.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Intel"
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 40
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class MoodLiSwtOnOff1:
        sig_name = "MoodLiSwtOnOff1"
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


class OhcCem_Lin3PartNrFr08:
    msg_name = "OhcCem_Lin3PartNrFr08"
    msg_id = 11
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class OHCPartNoCmplEndSgn3:
        sig_name = "OHCPartNoCmplEndSgn3"
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

    class OHCPartNoCmplNr4:
        sig_name = "OHCPartNoCmplNr4"
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

    class OHCPartNoCmplEndSgn2:
        sig_name = "OHCPartNoCmplEndSgn2"
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

    class OHCPartNoCmplNr2:
        sig_name = "OHCPartNoCmplNr2"
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

    class OHCPartNoCmplEndSgn1:
        sig_name = "OHCPartNoCmplEndSgn1"
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

    class OHCPartNoCmplNr3:
        sig_name = "OHCPartNoCmplNr3"
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

    class OHCPartNoCmplNr1:
        sig_name = "OHCPartNoCmplNr1"
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


class OhcCem_Lin3PartNrFr04:
    msg_name = "OhcCem_Lin3PartNrFr04"
    msg_id = 23
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class OHCPartNo10CmplNr3:
        sig_name = "OHCPartNo10CmplNr3"
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

    class OHCPartNo10CmplNr1:
        sig_name = "OHCPartNo10CmplNr1"
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

    class OHCPartNo10CmplEndSgn2:
        sig_name = "OHCPartNo10CmplEndSgn2"
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

    class OHCPartNo10CmplNr2:
        sig_name = "OHCPartNo10CmplNr2"
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

    class OHCPartNo10CmplEndSgn1:
        sig_name = "OHCPartNo10CmplEndSgn1"
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

    class OHCPartNo10CmplNr4:
        sig_name = "OHCPartNo10CmplNr4"
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

    class OHCPartNo10CmplEndSgn3:
        sig_name = "OHCPartNo10CmplEndSgn3"
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

    class OHCPartNo10CmplNr5:
        sig_name = "OHCPartNo10CmplNr5"
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


class OhcCem_Lin3SerNrFr01:
    msg_name = "OhcCem_Lin3SerNrFr01"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class OHCSerNoNr4:
        sig_name = "OHCSerNoNr4"
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

    class OHCSerNoNr3:
        sig_name = "OHCSerNoNr3"
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

    class OHCSerNoNr2:
        sig_name = "OHCSerNoNr2"
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

    class OHCSerNoNr1:
        sig_name = "OHCSerNoNr1"
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


