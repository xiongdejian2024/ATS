lin_scheduleTable = {'Cem_Lin3_DiagResponseSchedule01': [(0, 'DiagResponse2', 0.015)], 'Cem_Lin3ScheduleSerNrPartNr_CEM_LIN3': [(0, 'OhcCem_Lin3PartNrFr04', 0.015), (1, 'OhcCem_Lin3SerNrFr01', 0.015), (2, 'DsglCem_Lin3PartNrFr01', 0.015), (3, 'DsglCem_Lin3SerNrFr01', 0.01), (4, 'PsglCem_Lin3PartNrFr01', 0.015), (5, 'PsglCem_Lin3SerNrFr01', 0.01)], 'Cem_Lin3_DiagRequestSchedule01': [(0, 'DiagRequest2', 0.015)], 'Cem_Lin3Schedule01_CEM_LIN3': [(0, 'OhcCem_Lin3Fr01', 0.01), (1, 'OhcCem_Lin3Fr04', 0.005), (2, 'OhcCem_Lin3Fr05', 0.01), (3, 'CemCem_Lin3Fr03', 0.015), (4, 'CemCem_Lin3Fr01', 0.01), (5, 'CemCem_Lin3Fr06', 0.01), (6, 'CemCem_Lin3Fr04', 0.015), (7, 'OhcCem_Lin3Fr01', 0.01), (8, 'CemCem_Lin3Fr05', 0.01), (9, 'OhcCem_Lin3Fr01', 0.01), (10, 'DsglCem_Lin3Fr01', 0.015), (11, 'PsglCem_Lin3Fr01', 0.015)]}


class CemCem_Lin3Fr03:
    msg_name = "CemCem_Lin3Fr03"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['DSGL', 'PSGL', 'OHC']
    sig_group_dict = {'ReadLiOpenReq': ['ReadLiOpenReqFrontLeft', 'ReadLiOpenReqFrontRight', 'ReadLiOpenReqSecondRowLeft', 'ReadLiOpenReqSecondRowRight', 'ReadLiOpenReqThirdRowLeft', 'ReadLiOpenReqThirdRowRight']}
    sig_group_dataid_dict = {}

    class ReadLiOpenReqFrontLeft:
        sig_name = "ReadLiOpenReqFrontLeft"
        sig_start_bit = 0
        update_id_bit = None
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

    class ReadLiOpenReqFrontRight:
        sig_name = "ReadLiOpenReqFrontRight"
        sig_start_bit = 2
        update_id_bit = None
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
        update_id_bit = None
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

    class ReadLiOpenReqThirdRowLeft:
        sig_name = "ReadLiOpenReqThirdRowLeft"
        sig_start_bit = 8
        update_id_bit = None
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

    class TwliBriSts:
        sig_name = "TwliBriSts"
        sig_start_bit = 18
        update_id_bit = None
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

    class ReadLiOpenReqSecondRowRight:
        sig_name = "ReadLiOpenReqSecondRowRight"
        sig_start_bit = 6
        update_id_bit = None
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

    class IntrBriSts:
        sig_name = "IntrBriSts"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class ReadLiOpenReqSecondRowLeft:
        sig_name = "ReadLiOpenReqSecondRowLeft"
        sig_start_bit = 4
        update_id_bit = None
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


class DiagRequest2:
    msg_name = "DiagRequest2"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DiagResponse2:
    msg_name = "DiagResponse2"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class OhcCem_Lin3Fr04:
    msg_name = "OhcCem_Lin3Fr04"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "OHC"
    rx_nodes = ['BGM']
    sig_group_dict = {'BtnStsOHC': ['BtnStsOHCIntrLiSwtAllOnSts', 'BtnStsOHCIntrLiSwtAutOnSts', 'BtnStsOHCLiBtnReadingLe', 'BtnStsOHCLiBtnReadingRi']}
    sig_group_dataid_dict = {}

    class BtnStsOHCIntrLiSwtAutOnSts:
        sig_name = "BtnStsOHCIntrLiSwtAutOnSts"
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
        sig_value_table = {'BtnStsSngTyp_Idle': 0, 'BtnStsSngTyp_BtnPsd': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BtnStsOHCLiBtnReadingRi:
        sig_name = "BtnStsOHCLiBtnReadingRi"
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
        update_id_bit = None
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

    class BtnStsOHCLiBtnReadingLe:
        sig_name = "BtnStsOHCLiBtnReadingLe"
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
        sig_value_table = {'BtnStsSngTyp_Idle': 0, 'BtnStsSngTyp_BtnPsd': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class PsglCem_Lin3Fr01:
    msg_name = "PsglCem_Lin3Fr01"
    msg_id = 34
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "PSGL"
    rx_nodes = ['BGM']
    sig_group_dict = {'PSGLIntFlt': ['PSGLIntFltHiVoltDetdFlt', 'PSGLIntFltLEDsFlt', 'PSGLIntFltLoVoltDetdFlt', 'PSGLIntFltTpmFlt']}
    sig_group_dataid_dict = {}

    class PSGLIntFltTpmFlt:
        sig_name = "PSGLIntFltTpmFlt"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PSGLIntFltLEDsFlt:
        sig_name = "PSGLIntFltLEDsFlt"
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

    class PSGLIntFltLoVoltDetdFlt:
        sig_name = "PSGLIntFltLoVoltDetdFlt"
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

    class PSGLIntFltHiVoltDetdFlt:
        sig_name = "PSGLIntFltHiVoltDetdFlt"
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


class CemCem_Lin3Fr05:
    msg_name = "CemCem_Lin3Fr05"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['OHC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IntrLiGen2RoofDimSpeed:
        sig_name = "IntrLiGen2RoofDimSpeed"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class IntrLiGen2RoofResetMemory:
        sig_name = "IntrLiGen2RoofResetMemory"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class OhcCem_Lin3PartNrFr04:
    msg_name = "OhcCem_Lin3PartNrFr04"
    msg_id = 23
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "OHC"
    rx_nodes = ['BGM']
    sig_group_dict = {'OHCPartNo10Cmpl': ['OHCPartNo10CmplEndSgn1', 'OHCPartNo10CmplEndSgn2', 'OHCPartNo10CmplEndSgn3', 'OHCPartNo10CmplNr1', 'OHCPartNo10CmplNr2', 'OHCPartNo10CmplNr3', 'OHCPartNo10CmplNr4', 'OHCPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class OHCPartNo10CmplNr2:
        sig_name = "OHCPartNo10CmplNr2"
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

    class OHCPartNo10CmplEndSgn1:
        sig_name = "OHCPartNo10CmplEndSgn1"
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

    class OHCPartNo10CmplNr3:
        sig_name = "OHCPartNo10CmplNr3"
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

    class OHCPartNo10CmplNr5:
        sig_name = "OHCPartNo10CmplNr5"
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

    class OHCPartNo10CmplEndSgn2:
        sig_name = "OHCPartNo10CmplEndSgn2"
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

    class OHCPartNo10CmplNr1:
        sig_name = "OHCPartNo10CmplNr1"
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

    class OHCPartNo10CmplNr4:
        sig_name = "OHCPartNo10CmplNr4"
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

    class OHCPartNo10CmplEndSgn3:
        sig_name = "OHCPartNo10CmplEndSgn3"
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


class DsglCem_Lin3PartNrFr01:
    msg_name = "DsglCem_Lin3PartNrFr01"
    msg_id = 25
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "DSGL"
    rx_nodes = ['BGM']
    sig_group_dict = {'DSGLPartNo10Cmpl': ['DSGLPartNo10CmplEndSgn1', 'DSGLPartNo10CmplEndSgn2', 'DSGLPartNo10CmplEndSgn3', 'DSGLPartNo10CmplNr1', 'DSGLPartNo10CmplNr2', 'DSGLPartNo10CmplNr3', 'DSGLPartNo10CmplNr4', 'DSGLPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class DSGLPartNo10CmplNr5:
        sig_name = "DSGLPartNo10CmplNr5"
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

    class DSGLPartNo10CmplEndSgn2:
        sig_name = "DSGLPartNo10CmplEndSgn2"
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

    class DSGLPartNo10CmplNr3:
        sig_name = "DSGLPartNo10CmplNr3"
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

    class DSGLPartNo10CmplNr2:
        sig_name = "DSGLPartNo10CmplNr2"
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

    class DSGLPartNo10CmplEndSgn3:
        sig_name = "DSGLPartNo10CmplEndSgn3"
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

    class DSGLPartNo10CmplEndSgn1:
        sig_name = "DSGLPartNo10CmplEndSgn1"
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

    class DSGLPartNo10CmplNr4:
        sig_name = "DSGLPartNo10CmplNr4"
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

    class DSGLPartNo10CmplNr1:
        sig_name = "DSGLPartNo10CmplNr1"
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


class OhcCem_Lin3Fr05:
    msg_name = "OhcCem_Lin3Fr05"
    msg_id = 22
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 2
    tx_node = "OHC"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class OHCPINFlt:
        sig_name = "OHCPINFlt"
        sig_start_bit = 0
        update_id_bit = None
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
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00001111, 0b11110000, 4, 0)]


class OhcCem_Lin3Fr01:
    msg_name = "OhcCem_Lin3Fr01"
    msg_id = 32
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "OHC"
    rx_nodes = ['BGM']
    sig_group_dict = {'IntrLiCmdGroup': ['IntrLiCmdGroupIntrLiActvn', 'IntrLiCmdGroupIntrLiRoofDim', 'IntrLiCmdGroupIntrLiRoofDmdOff'], 'ReadLiSts': ['ReadLiStsFirstRowLe', 'ReadLiStsFirstRowRi', 'ReadLiStsSecondRowLe', 'ReadLiStsSecondRowRi', 'ReadLiStsThirdRowLe', 'ReadLiStsThirdRowRi'], 'BtnStsOHCR': ['BtnStsOHCRLiBtnReadingLe', 'BtnStsOHCRLiBtnReadingRi'], 'BtnStsOHTR': ['BtnStsOHTRLiBtnReadingLe', 'BtnStsOHTRLiBtnReadingRi']}
    sig_group_dataid_dict = {}

    class IntrLiCmdGroupIntrLiActvn:
        sig_name = "IntrLiCmdGroupIntrLiActvn"
        sig_start_bit = 45
        update_id_bit = None
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

    class ReadLiStsFirstRowLe:
        sig_name = "ReadLiStsFirstRowLe"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ReadLiStsFirstRowRi:
        sig_name = "ReadLiStsFirstRowRi"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class IntrLiCmdGroupIntrLiRoofDmdOff:
        sig_name = "IntrLiCmdGroupIntrLiRoofDmdOff"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BtnStsOHTRLiBtnReadingRi:
        sig_name = "BtnStsOHTRLiBtnReadingRi"
        sig_start_bit = 39
        update_id_bit = None
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

    class IntrLiCmdGroupIntrLiRoofDim:
        sig_name = "IntrLiCmdGroupIntrLiRoofDim"
        sig_start_bit = 43
        update_id_bit = None
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

    class ReadLiStsSecondRowRi:
        sig_name = "ReadLiStsSecondRowRi"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BtnStsOHTRLiBtnReadingLe:
        sig_name = "BtnStsOHTRLiBtnReadingLe"
        sig_start_bit = 38
        update_id_bit = None
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

    class ReadLiStsThirdRowLe:
        sig_name = "ReadLiStsThirdRowLe"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ReadLiStsSecondRowLe:
        sig_name = "ReadLiStsSecondRowLe"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BtnStsOHCRLiBtnReadingLe:
        sig_name = "BtnStsOHCRLiBtnReadingLe"
        sig_start_bit = 46
        update_id_bit = None
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

    class BtnStsOHCRLiBtnReadingRi:
        sig_name = "BtnStsOHCRLiBtnReadingRi"
        sig_start_bit = 47
        update_id_bit = None
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

    class ReadLiStsThirdRowRi:
        sig_name = "ReadLiStsThirdRowRi"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class PsglCem_Lin3SerNrFr01:
    msg_name = "PsglCem_Lin3SerNrFr01"
    msg_id = 26
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "PSGL"
    rx_nodes = ['BGM']
    sig_group_dict = {'PSGLSerNo': ['PSGLSerNoNr1', 'PSGLSerNoNr2', 'PSGLSerNoNr3', 'PSGLSerNoNr4']}
    sig_group_dataid_dict = {}

    class PSGLSerNoNr3:
        sig_name = "PSGLSerNoNr3"
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

    class PSGLSerNoNr1:
        sig_name = "PSGLSerNoNr1"
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

    class PSGLSerNoNr2:
        sig_name = "PSGLSerNoNr2"
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

    class PSGLSerNoNr4:
        sig_name = "PSGLSerNoNr4"
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


class CemCem_Lin3Fr04:
    msg_name = "CemCem_Lin3Fr04"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['OHC']
    sig_group_dict = {'IntrLiGen2RoofRequest': ['IntrLiGen2RoofRequestIntrLiGen2RoofReqZon1', 'IntrLiGen2RoofRequestIntrLiGen2RoofReqZon2', 'IntrLiGen2RoofRequestIntrLiGen2RoofReqZon3', 'IntrLiGen2RoofRequestIntrLiGen2RoofReqZon4', 'IntrLiGen2RoofRequestIntrLiGen2RoofReqZon5', 'IntrLiGen2RoofRequestIntrLiGen2RoofReqZon6'], 'IntrLiGen2RoofParameters': ['IntrLiGen2RoofParametersIntrLiForceOfflvl', 'IntrLiGen2RoofParametersIntrLiForceOnLvl', 'IntrLiGen2RoofParametersIntrlLiAmbienceLvl', 'IntrLiGen2RoofParametersINtrlLiCourtesyLvl', 'IntrLiGen2RoofParametersIntrlLiPoliteLvl']}
    sig_group_dataid_dict = {}

    class IntrLiGen2RoofParametersIntrlLiAmbienceLvl:
        sig_name = "IntrLiGen2RoofParametersIntrlLiAmbienceLvl"
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

    class IntrLiGen2RoofParametersIntrlLiPoliteLvl:
        sig_name = "IntrLiGen2RoofParametersIntrlLiPoliteLvl"
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

    class IntrLiGen2RoofRequestIntrLiGen2RoofReqZon2:
        sig_name = "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon2"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IntrLiGen2RoofReqTyp_Unknow': 0, 'IntrLiGen2RoofReqTyp_AllOff': 1, 'IntrLiGen2RoofReqTyp_Courtesy': 2, 'IntrLiGen2RoofReqTyp_Manual': 3, 'IntrLiGen2RoofReqTyp_Polite': 4, 'IntrLiGen2RoofReqTyp_ForceOn': 5, 'IntrLiGen2RoofReqTyp_ForceOff': 6}
        compute_method = None
        length = 3
        startbit = 45
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class IntrLiGen2RoofParametersINtrlLiCourtesyLvl:
        sig_name = "IntrLiGen2RoofParametersINtrlLiCourtesyLvl"
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

    class IntrLiGen2RoofParametersIntrLiForceOnLvl:
        sig_name = "IntrLiGen2RoofParametersIntrLiForceOnLvl"
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

    class IntrLiGen2RoofParametersIntrLiForceOfflvl:
        sig_name = "IntrLiGen2RoofParametersIntrLiForceOfflvl"
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

    class IntrLiGen2RoofRequestIntrLiGen2RoofReqZon4:
        sig_name = "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon4"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IntrLiGen2RoofReqTyp_Unknow': 0, 'IntrLiGen2RoofReqTyp_AllOff': 1, 'IntrLiGen2RoofReqTyp_Courtesy': 2, 'IntrLiGen2RoofReqTyp_Manual': 3, 'IntrLiGen2RoofReqTyp_Polite': 4, 'IntrLiGen2RoofReqTyp_ForceOn': 5, 'IntrLiGen2RoofReqTyp_ForceOff': 6}
        compute_method = None
        length = 3
        startbit = 51
        byte = 6
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class IntrLiGen2RoofRequestIntrLiGen2RoofReqZon6:
        sig_name = "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon6"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IntrLiGen2RoofReqTyp_Unknow': 0, 'IntrLiGen2RoofReqTyp_AllOff': 1, 'IntrLiGen2RoofReqTyp_Courtesy': 2, 'IntrLiGen2RoofReqTyp_Manual': 3, 'IntrLiGen2RoofReqTyp_Polite': 4, 'IntrLiGen2RoofReqTyp_ForceOn': 5, 'IntrLiGen2RoofReqTyp_ForceOff': 6}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class IntrLiGen2RoofRequestIntrLiGen2RoofReqZon5:
        sig_name = "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon5"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IntrLiGen2RoofReqTyp_Unknow': 0, 'IntrLiGen2RoofReqTyp_AllOff': 1, 'IntrLiGen2RoofReqTyp_Courtesy': 2, 'IntrLiGen2RoofReqTyp_Manual': 3, 'IntrLiGen2RoofReqTyp_Polite': 4, 'IntrLiGen2RoofReqTyp_ForceOn': 5, 'IntrLiGen2RoofReqTyp_ForceOff': 6}
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
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IntrLiGen2RoofReqTyp_Unknow': 0, 'IntrLiGen2RoofReqTyp_AllOff': 1, 'IntrLiGen2RoofReqTyp_Courtesy': 2, 'IntrLiGen2RoofReqTyp_Manual': 3, 'IntrLiGen2RoofReqTyp_Polite': 4, 'IntrLiGen2RoofReqTyp_ForceOn': 5, 'IntrLiGen2RoofReqTyp_ForceOff': 6}
        compute_method = None
        length = 3
        startbit = 42
        byte = 5
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class IntrLiGen2RoofRequestIntrLiGen2RoofReqZon3:
        sig_name = "IntrLiGen2RoofRequestIntrLiGen2RoofReqZon3"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IntrLiGen2RoofReqTyp_Unknow': 0, 'IntrLiGen2RoofReqTyp_AllOff': 1, 'IntrLiGen2RoofReqTyp_Courtesy': 2, 'IntrLiGen2RoofReqTyp_Manual': 3, 'IntrLiGen2RoofReqTyp_Polite': 4, 'IntrLiGen2RoofReqTyp_ForceOn': 5, 'IntrLiGen2RoofReqTyp_ForceOff': 6}
        compute_method = None
        length = 3
        startbit = 48
        byte = 6
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class PsglCem_Lin3PartNrFr01:
    msg_name = "PsglCem_Lin3PartNrFr01"
    msg_id = 24
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "PSGL"
    rx_nodes = ['BGM']
    sig_group_dict = {'PSGLPartNo10Cmpl': ['PSGLPartNo10CmplEndSgn1', 'PSGLPartNo10CmplEndSgn2', 'PSGLPartNo10CmplEndSgn3', 'PSGLPartNo10CmplNr1', 'PSGLPartNo10CmplNr2', 'PSGLPartNo10CmplNr3', 'PSGLPartNo10CmplNr4', 'PSGLPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class PSGLPartNo10CmplNr4:
        sig_name = "PSGLPartNo10CmplNr4"
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

    class PSGLPartNo10CmplNr2:
        sig_name = "PSGLPartNo10CmplNr2"
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

    class PSGLPartNo10CmplEndSgn2:
        sig_name = "PSGLPartNo10CmplEndSgn2"
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

    class PSGLPartNo10CmplEndSgn1:
        sig_name = "PSGLPartNo10CmplEndSgn1"
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

    class PSGLPartNo10CmplNr1:
        sig_name = "PSGLPartNo10CmplNr1"
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

    class PSGLPartNo10CmplNr3:
        sig_name = "PSGLPartNo10CmplNr3"
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

    class PSGLPartNo10CmplNr5:
        sig_name = "PSGLPartNo10CmplNr5"
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

    class PSGLPartNo10CmplEndSgn3:
        sig_name = "PSGLPartNo10CmplEndSgn3"
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


class CemCem_Lin3Fr06:
    msg_name = "CemCem_Lin3Fr06"
    msg_id = 29
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = []
    sig_group_dict = {'AmbTRaw': ['AmbTRawAmbTVal', 'AmbTRawQly']}
    sig_group_dataid_dict = {}

    class AmbTRawAmbTVal:
        sig_name = "AmbTRawAmbTVal"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -70.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Intel"
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 40
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b00000111, 0b11111000, 3, 0)]

    class AmbTRawQly:
        sig_name = "AmbTRawQly"
        sig_start_bit = 51
        update_id_bit = None
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


class DsglCem_Lin3Fr01:
    msg_name = "DsglCem_Lin3Fr01"
    msg_id = 33
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "DSGL"
    rx_nodes = ['BGM']
    sig_group_dict = {'DSGLIntFlt': ['DSGLIntFltHiVoltDetdFlt', 'DSGLIntFltLEDsFlt', 'DSGLIntFltLoVoltDetdFlt', 'DSGLIntFltTpmFlt']}
    sig_group_dataid_dict = {}

    class DSGLIntFltHiVoltDetdFlt:
        sig_name = "DSGLIntFltHiVoltDetdFlt"
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

    class DSGLIntFltLoVoltDetdFlt:
        sig_name = "DSGLIntFltLoVoltDetdFlt"
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

    class DSGLIntFltTpmFlt:
        sig_name = "DSGLIntFltTpmFlt"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DSGLIntFltLEDsFlt:
        sig_name = "DSGLIntFltLEDsFlt"
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


class OhcCem_Lin3SerNrFr01:
    msg_name = "OhcCem_Lin3SerNrFr01"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "OHC"
    rx_nodes = ['BGM']
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


class CemCem_Lin3Fr01:
    msg_name = "CemCem_Lin3Fr01"
    msg_id = 0
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['DSGL', 'PSGL']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class RiSolarData:
        sig_name = "RiSolarData"
        sig_start_bit = 16
        update_id_bit = None
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

    class ActvnOfFlGooseneckLamp:
        sig_name = "ActvnOfFlGooseneckLamp"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ActvnOfFrGooseneckLamp:
        sig_name = "ActvnOfFrGooseneckLamp"
        sig_start_bit = 30
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
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class LeSolarData:
        sig_name = "LeSolarData"
        sig_start_bit = 8
        update_id_bit = None
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


class DsglCem_Lin3SerNrFr01:
    msg_name = "DsglCem_Lin3SerNrFr01"
    msg_id = 27
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "DSGL"
    rx_nodes = ['BGM']
    sig_group_dict = {'DSGLSerNo': ['DSGLSerNoNr1', 'DSGLSerNoNr2', 'DSGLSerNoNr3', 'DSGLSerNoNr4']}
    sig_group_dataid_dict = {}

    class DSGLSerNoNr4:
        sig_name = "DSGLSerNoNr4"
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

    class DSGLSerNoNr1:
        sig_name = "DSGLSerNoNr1"
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

    class DSGLSerNoNr2:
        sig_name = "DSGLSerNoNr2"
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

    class DSGLSerNoNr3:
        sig_name = "DSGLSerNoNr3"
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


