class BmsCem_Lin6PartNrFr02:
    msg_name = "BmsCem_Lin6PartNrFr02"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNoApplBMS': ['PartNoApplBMSEndSgn1', 'PartNoApplBMSEndSgn2', 'PartNoApplBMSEndSgn3', 'PartNoApplBMSNr1', 'PartNoApplBMSNr2', 'PartNoApplBMSNr3', 'PartNoApplBMSNr4']}
    sig_group_dataid_dict = {}

    class PartNoApplBMSEndSgn2:
        sig_name = "PartNoApplBMSEndSgn2"
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

    class PartNoApplBMSEndSgn3:
        sig_name = "PartNoApplBMSEndSgn3"
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

    class PartNoApplBMSNr2:
        sig_name = "PartNoApplBMSNr2"
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

    class PartNoApplBMSNr1:
        sig_name = "PartNoApplBMSNr1"
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

    class PartNoApplBMSNr4:
        sig_name = "PartNoApplBMSNr4"
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

    class PartNoApplBMSEndSgn1:
        sig_name = "PartNoApplBMSEndSgn1"
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

    class PartNoApplBMSNr3:
        sig_name = "PartNoApplBMSNr3"
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


class BmsCem_Lin6Fr06:
    msg_name = "BmsCem_Lin6Fr06"
    msg_id = 40
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'EgyMeasIntl': ['EgyMeasIntlIntl1', 'EgyMeasIntlIntl2', 'EgyMeasIntlIntl3', 'EgyMeasIntlIntl4']}
    sig_group_dataid_dict = {}

    class EgyMeasIntlIntl1:
        sig_name = "EgyMeasIntlIntl1"
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

    class EgyMeasIntlIntl2:
        sig_name = "EgyMeasIntlIntl2"
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

    class EgyMeasSec:
        sig_name = "EgyMeasSec"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EgyMeasIntlIntl3:
        sig_name = "EgyMeasIntlIntl3"
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

    class EgyMeas:
        sig_name = "EgyMeas"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.01
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00011111, 0b11100000, 5, 0)]

    class EgyMeasIntlIntl4:
        sig_name = "EgyMeasIntlIntl4"
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


class AwmCem_Lin6Fr01:
    msg_name = "AwmCem_Lin6Fr01"
    msg_id = 32
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "AWM"
    rx_nodes = ['BGM']
    sig_group_dict = {'ActvReSplrUFlt': ['ActvReSplrUFltHiVoltDetdFlt', 'ActvReSplrUFltLoVoltDetdFlt'], 'AWMSerNo': ['AWMSerNoNr1', 'AWMSerNoNr2', 'AWMSerNoNr3', 'AWMSerNoNr4'], 'ActvReSplrHallSnsrFlt': ['ActvReSplrHallSnsrFltHallAFlt', 'ActvReSplrHallSnsrFltHallBFlt', 'ActvReSplrHallSnsrFltHallOutpFlt'], 'ActvReSplrIntFlt': ['ActvReSplrIntFltActrFlt1', 'ActvReSplrIntFltActrFlt2', 'ActvReSplrIntFltActrFlt3', 'ActvReSplrIntFltActrFlt4', 'ActvReSplrIntFltActrFlt5', 'ActvReSplrIntFltTmrFlt']}
    sig_group_dataid_dict = {}

    class ActvReSplrIntFltActrFlt2:
        sig_name = "ActvReSplrIntFltActrFlt2"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ActvReSplrIntFltActrFlt3:
        sig_name = "ActvReSplrIntFltActrFlt3"
        sig_start_bit = 42
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
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ActvReSplrHallSnsrFltHallAFlt:
        sig_name = "ActvReSplrHallSnsrFltHallAFlt"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActvReSplrIntFltActrFlt1:
        sig_name = "ActvReSplrIntFltActrFlt1"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ActvReSplrIntFltActrFlt4:
        sig_name = "ActvReSplrIntFltActrFlt4"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AWMSerNoNr1:
        sig_name = "AWMSerNoNr1"
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

    class AWMSerNoNr4:
        sig_name = "AWMSerNoNr4"
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

    class CalStsAWM:
        sig_name = "CalStsAWM"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CalStsAWM_Nocal': 0, 'CalStsAWM_Calg': 1, 'CalStsAWM_Cald': 2, 'CalStsAWM_CalErr': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class ActvReSplrIntFltTmrFlt:
        sig_name = "ActvReSplrIntFltTmrFlt"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ActvReSplrIntFltActrFlt5:
        sig_name = "ActvReSplrIntFltActrFlt5"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ActvReSplrMotBlk:
        sig_name = "ActvReSplrMotBlk"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ActvReSplrPosn:
        sig_name = "ActvReSplrPosn"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvSplr_Ukwn': 0, 'ActvSplr_P0': 1, 'ActvSplr_P1': 2, 'ActvSplr_P2': 3, 'ActvSplr_P3': 4, 'ActvSplr_Shifting': 5, 'ActvSplr_Reserved': 6, 'Error': 7}
        compute_method = None
        length = 3
        startbit = 48
        byte = 6
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class ActvReSplrHallSnsrFltHallOutpFlt:
        sig_name = "ActvReSplrHallSnsrFltHallOutpFlt"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ActvReSplrIceBreakFaild:
        sig_name = "ActvReSplrIceBreakFaild"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ActvReSplrUFltHiVoltDetdFlt:
        sig_name = "ActvReSplrUFltHiVoltDetdFlt"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AWMSerNoNr2:
        sig_name = "AWMSerNoNr2"
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

    class ActvReSplrUFltLoVoltDetdFlt:
        sig_name = "ActvReSplrUFltLoVoltDetdFlt"
        sig_start_bit = 52
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
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ActvReSplrHallSnsrFltHallBFlt:
        sig_name = "ActvReSplrHallSnsrFltHallBFlt"
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
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AWMSerNoNr3:
        sig_name = "AWMSerNoNr3"
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


class BmsCem_Lin6Fr04:
    msg_name = "BmsCem_Lin6Fr04"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BattRAtTNomRaw:
        sig_name = "BattRAtTNomRaw"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BattRRaw_0_BmsCem_Lin6SignalIPdu04:
        sig_name = "BattRRaw_0_BmsCem_Lin6SignalIPdu04"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BattCircOpenU:
        sig_name = "BattCircOpenU"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 0.25
        sig_value_offset = 6.0
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 27
        byte = 3
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class BattSnsrCalcnNotVldRaw:
        sig_name = "BattSnsrCalcnNotVldRaw"
        sig_start_bit = 25
        update_id_bit = None
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
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BattIQuiscFildShoRaw:
        sig_name = "BattIQuiscFildShoRaw"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 1.0
        sig_value_offset = -511.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Intel"
        sig_value_init = 511
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000001, 0b11111110, 1, 0)]

    class BattChrgnBalDurgDrvgRaw:
        sig_name = "BattChrgnBalDurgDrvgRaw"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.005
        sig_value_offset = -100.0
        sig_value_min = 0
        sig_value_max = 40000
        sig_byteorder = "Intel"
        sig_value_init = 20000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class BmsCem_Lin6Fr03:
    msg_name = "BmsCem_Lin6Fr03"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BattTiInSrvRaw:
        sig_name = "BattTiInSrvRaw"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00001111, 0b11110000, 4, 0)]

    class BattCpEstimdAtTNomRaw:
        sig_name = "BattCpEstimdAtTNomRaw"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class BattCpEstimdRaw_0_BmsCem_Lin6SignalIPdu03:
        sig_name = "BattCpEstimdRaw_0_BmsCem_Lin6SignalIPdu03"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 80
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 49
        byte = 6
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class BattTRaw_0_BmsCem_Lin6SignalIPdu03:
        sig_name = "BattTRaw_0_BmsCem_Lin6SignalIPdu03"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.5
        sig_value_offset = -128.0
        sig_value_min = 116
        sig_value_max = 506
        sig_byteorder = "Intel"
        sig_value_init = 256
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 15
        bmuws_info = [(1, 0b10000000, 0b01111111, 1, 7), (2, 0b11111111, 0b00000000, 8, 0)]

    class BattSnsrHwFltRaw:
        sig_name = "BattSnsrHwFltRaw"
        sig_start_bit = 12
        update_id_bit = None
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BattIQuiscAvgRaw:
        sig_name = "BattIQuiscAvgRaw"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 5.0
        sig_value_offset = -2555.0
        sig_value_min = 11
        sig_value_max = 511
        sig_byteorder = "Intel"
        sig_value_init = 511
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b00000001, 0b11111110, 1, 0)]

    class BattIQuiscFildLongRaw:
        sig_name = "BattIQuiscFildLongRaw"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 1.0
        sig_value_offset = -511.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Intel"
        sig_value_init = 511
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 40
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b00000001, 0b11111110, 1, 0)]


class BmsCem_Lin6Fr02:
    msg_name = "BmsCem_Lin6Fr02"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BattCycDchaCntrDurgDrvgRaw:
        sig_name = "BattCycDchaCntrDurgDrvgRaw"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 16000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 32
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b00111111, 0b11000000, 6, 0)]

    class BattCycChrgCntrRaw:
        sig_name = "BattCycChrgCntrRaw"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 16000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00111111, 0b11000000, 6, 0)]

    class BattCycDchaCntrDurgConvceRaw:
        sig_name = "BattCycDchaCntrDurgConvceRaw"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 16000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00111111, 0b11000000, 6, 0)]

    class BattCycDchaCntrDurgQuiscPhaRaw:
        sig_name = "BattCycDchaCntrDurgQuiscPhaRaw"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 0.015625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 16320
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 48
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b00111111, 0b11000000, 6, 0)]


class BmsCem_Lin6PartNrFr03:
    msg_name = "BmsCem_Lin6PartNrFr03"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNoApplDiagBMS': ['PartNoApplDiagBMSEndSgn1', 'PartNoApplDiagBMSEndSgn2', 'PartNoApplDiagBMSEndSgn3', 'PartNoApplDiagBMSNr1', 'PartNoApplDiagBMSNr2', 'PartNoApplDiagBMSNr3', 'PartNoApplDiagBMSNr4']}
    sig_group_dataid_dict = {}

    class PartNoApplDiagBMSEndSgn1:
        sig_name = "PartNoApplDiagBMSEndSgn1"
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

    class PartNoApplDiagBMSEndSgn3:
        sig_name = "PartNoApplDiagBMSEndSgn3"
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

    class PartNoApplDiagBMSNr1:
        sig_name = "PartNoApplDiagBMSNr1"
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

    class PartNoApplDiagBMSNr3:
        sig_name = "PartNoApplDiagBMSNr3"
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

    class PartNoApplDiagBMSNr2:
        sig_name = "PartNoApplDiagBMSNr2"
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

    class PartNoApplDiagBMSEndSgn2:
        sig_name = "PartNoApplDiagBMSEndSgn2"
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

    class PartNoApplDiagBMSNr4:
        sig_name = "PartNoApplDiagBMSNr4"
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


class BmsCem_Lin6PartNrFr08:
    msg_name = "BmsCem_Lin6PartNrFr08"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNo10HwBMS': ['PartNo10HwBMSEndSgn1', 'PartNo10HwBMSEndSgn2', 'PartNo10HwBMSEndSgn3', 'PartNo10HwBMSNr1', 'PartNo10HwBMSNr2', 'PartNo10HwBMSNr3', 'PartNo10HwBMSNr4', 'PartNo10HwBMSNr5']}
    sig_group_dataid_dict = {}

    class PartNo10HwBMSNr2:
        sig_name = "PartNo10HwBMSNr2"
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

    class PartNo10HwBMSEndSgn2:
        sig_name = "PartNo10HwBMSEndSgn2"
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

    class PartNo10HwBMSNr5:
        sig_name = "PartNo10HwBMSNr5"
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

    class PartNo10HwBMSNr4:
        sig_name = "PartNo10HwBMSNr4"
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

    class PartNo10HwBMSEndSgn3:
        sig_name = "PartNo10HwBMSEndSgn3"
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

    class PartNo10HwBMSNr3:
        sig_name = "PartNo10HwBMSNr3"
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

    class PartNo10HwBMSEndSgn1:
        sig_name = "PartNo10HwBMSEndSgn1"
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

    class PartNo10HwBMSNr1:
        sig_name = "PartNo10HwBMSNr1"
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


class BmsCem_Lin6Fr01:
    msg_name = "BmsCem_Lin6Fr01"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'BattSftySig': ['BattSftySigChks', 'BattSftySigCntr', 'BattSftySigSysSaftyBattI', 'BattSftySigSysSaftyBattU']}
    sig_group_dataid_dict = {'BattSftySig': 9}

    class BattSftySigCntr:
        sig_name = "BattSftySigCntr"
        sig_start_bit = 56
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
        startbit = 56
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BattIRaw_0_BmsCem_Lin6SignalIPdu01:
        sig_name = "BattIRaw_0_BmsCem_Lin6SignalIPdu01"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.015625
        sig_value_offset = -512.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Intel"
        sig_value_init = 32768
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class BattSftySigChks:
        sig_name = "BattSftySigChks"
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

    class BattUMinAvgDurgCrkRaw:
        sig_name = "BattUMinAvgDurgCrkRaw"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 6
        sig_value_factor = 0.2
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 16
        byte = 2
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class BattSftySigSysSaftyBattI:
        sig_name = "BattSftySigSysSaftyBattI"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.015625
        sig_value_offset = -512.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Intel"
        sig_value_init = 32768
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 32
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class BattSftySigSysSaftyBattU:
        sig_name = "BattSftySigSysSaftyBattU"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.025
        sig_value_offset = 5.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 23
        bmuws_info = [(2, 0b10000000, 0b01111111, 1, 7), (3, 0b11111111, 0b00000000, 8, 0)]


class BmsCem_Lin6PartNrFr06:
    msg_name = "BmsCem_Lin6PartNrFr06"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNo10ApplDiagBMS': ['PartNo10ApplDiagBMSEndSgn1', 'PartNo10ApplDiagBMSEndSgn2', 'PartNo10ApplDiagBMSEndSgn3', 'PartNo10ApplDiagBMSNr1', 'PartNo10ApplDiagBMSNr2', 'PartNo10ApplDiagBMSNr3', 'PartNo10ApplDiagBMSNr4', 'PartNo10ApplDiagBMSNr5']}
    sig_group_dataid_dict = {}

    class PartNo10ApplDiagBMSNr5:
        sig_name = "PartNo10ApplDiagBMSNr5"
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

    class PartNo10ApplDiagBMSNr1:
        sig_name = "PartNo10ApplDiagBMSNr1"
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

    class PartNo10ApplDiagBMSNr3:
        sig_name = "PartNo10ApplDiagBMSNr3"
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

    class PartNo10ApplDiagBMSNr4:
        sig_name = "PartNo10ApplDiagBMSNr4"
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

    class PartNo10ApplDiagBMSEndSgn1:
        sig_name = "PartNo10ApplDiagBMSEndSgn1"
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

    class PartNo10ApplDiagBMSEndSgn2:
        sig_name = "PartNo10ApplDiagBMSEndSgn2"
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

    class PartNo10ApplDiagBMSEndSgn3:
        sig_name = "PartNo10ApplDiagBMSEndSgn3"
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

    class PartNo10ApplDiagBMSNr2:
        sig_name = "PartNo10ApplDiagBMSNr2"
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


class DiagRequest5:
    msg_name = "DiagRequest5"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BmsCem_Lin6Fr05:
    msg_name = "BmsCem_Lin6Fr05"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BattSocRaw:
        sig_name = "BattSocRaw"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000011, 0b11111100, 2, 0)]

    class BattURaw_0_BmsCem_Lin6SignalIPdu05:
        sig_name = "BattURaw_0_BmsCem_Lin6SignalIPdu05"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 0.025
        sig_value_offset = 5.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 15
        bmuws_info = [(1, 0b10000000, 0b01111111, 1, 7), (2, 0b11111111, 0b00000000, 8, 0)]


class CemCem_Lin6Fr02:
    msg_name = "CemCem_Lin6Fr02"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 5
    tx_node = "BGM"
    rx_nodes = ['BMS']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EgyMeasSecRst:
        sig_name = "EgyMeasSecRst"
        sig_start_bit = 29
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
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class EgyMeasRst:
        sig_name = "EgyMeasRst"
        sig_start_bit = 28
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
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BattTyp:
        sig_name = "BattTyp"
        sig_start_bit = 11
        update_id_bit = None
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
        startbit = 11
        byte = 1
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class BattSnsrStReq:
        sig_name = "BattSnsrStReq"
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
        sig_value_table = {'BattSnsrSt_Off': 0, 'BattSnsrSt_Accessory': 1, 'BattSnsrSt_IgnistionONOrDriving': 2, 'BattSnsrSt_Cranking': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BattSnsrRstReq:
        sig_name = "BattSnsrRstReq"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class BmsCem_Lin6PartNrFr07:
    msg_name = "BmsCem_Lin6PartNrFr07"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNo10BMS': ['PartNo10BMSEndSgn1', 'PartNo10BMSEndSgn2', 'PartNo10BMSEndSgn3', 'PartNo10BMSNr1', 'PartNo10BMSNr2', 'PartNo10BMSNr3', 'PartNo10BMSNr4', 'PartNo10BMSNr5']}
    sig_group_dataid_dict = {}

    class PartNo10BMSNr3:
        sig_name = "PartNo10BMSNr3"
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

    class PartNo10BMSNr5:
        sig_name = "PartNo10BMSNr5"
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

    class PartNo10BMSEndSgn1:
        sig_name = "PartNo10BMSEndSgn1"
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

    class PartNo10BMSEndSgn2:
        sig_name = "PartNo10BMSEndSgn2"
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

    class PartNo10BMSNr4:
        sig_name = "PartNo10BMSNr4"
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

    class PartNo10BMSNr1:
        sig_name = "PartNo10BMSNr1"
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

    class PartNo10BMSEndSgn3:
        sig_name = "PartNo10BMSEndSgn3"
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

    class PartNo10BMSNr2:
        sig_name = "PartNo10BMSNr2"
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


class BmsCem_Lin6SerNrFr01:
    msg_name = "BmsCem_Lin6SerNrFr01"
    msg_id = 35
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'NrSerlBMS': ['NrSerlBMSNr1', 'NrSerlBMSNr2', 'NrSerlBMSNr3', 'NrSerlBMSNr4']}
    sig_group_dataid_dict = {}

    class NrSerlBMSNr2:
        sig_name = "NrSerlBMSNr2"
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

    class NrSerlBMSNr1:
        sig_name = "NrSerlBMSNr1"
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

    class NrSerlBMSNr3:
        sig_name = "NrSerlBMSNr3"
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

    class NrSerlBMSNr4:
        sig_name = "NrSerlBMSNr4"
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


class AwmCem_Lin6Fr02:
    msg_name = "AwmCem_Lin6Fr02"
    msg_id = 33
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "AWM"
    rx_nodes = ['BGM']
    sig_group_dict = {'AWMPartNo10Cmpl': ['AWMPartNo10CmplEndSgn1', 'AWMPartNo10CmplEndSgn2', 'AWMPartNo10CmplEndSgn3', 'AWMPartNo10CmplNr1', 'AWMPartNo10CmplNr2', 'AWMPartNo10CmplNr3', 'AWMPartNo10CmplNr4', 'AWMPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class AWMPartNo10CmplNr4:
        sig_name = "AWMPartNo10CmplNr4"
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

    class AWMPartNo10CmplNr5:
        sig_name = "AWMPartNo10CmplNr5"
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

    class AWMPartNo10CmplNr1:
        sig_name = "AWMPartNo10CmplNr1"
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

    class AWMPartNo10CmplEndSgn2:
        sig_name = "AWMPartNo10CmplEndSgn2"
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

    class AWMPartNo10CmplNr2:
        sig_name = "AWMPartNo10CmplNr2"
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

    class AWMPartNo10CmplNr3:
        sig_name = "AWMPartNo10CmplNr3"
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

    class AWMPartNo10CmplEndSgn3:
        sig_name = "AWMPartNo10CmplEndSgn3"
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

    class AWMPartNo10CmplEndSgn1:
        sig_name = "AWMPartNo10CmplEndSgn1"
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


class BmsCem_Lin6PartNrFr04:
    msg_name = "BmsCem_Lin6PartNrFr04"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNoHwBMS': ['PartNoHwBMSEndSgn1', 'PartNoHwBMSEndSgn2', 'PartNoHwBMSEndSgn3', 'PartNoHwBMSNr1', 'PartNoHwBMSNr2', 'PartNoHwBMSNr3', 'PartNoHwBMSNr4']}
    sig_group_dataid_dict = {}

    class PartNoHwBMSNr2:
        sig_name = "PartNoHwBMSNr2"
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

    class PartNoHwBMSEndSgn1:
        sig_name = "PartNoHwBMSEndSgn1"
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

    class PartNoHwBMSNr3:
        sig_name = "PartNoHwBMSNr3"
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

    class PartNoHwBMSNr1:
        sig_name = "PartNoHwBMSNr1"
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

    class PartNoHwBMSNr4:
        sig_name = "PartNoHwBMSNr4"
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

    class PartNoHwBMSEndSgn2:
        sig_name = "PartNoHwBMSEndSgn2"
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

    class PartNoHwBMSEndSgn3:
        sig_name = "PartNoHwBMSEndSgn3"
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


class BmsCem_Lin6PartNrFr05:
    msg_name = "BmsCem_Lin6PartNrFr05"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNo10ApplBMS': ['PartNo10ApplBMSEndSgn1', 'PartNo10ApplBMSEndSgn2', 'PartNo10ApplBMSEndSgn3', 'PartNo10ApplBMSNr1', 'PartNo10ApplBMSNr2', 'PartNo10ApplBMSNr3', 'PartNo10ApplBMSNr4', 'PartNo10ApplBMSNr5']}
    sig_group_dataid_dict = {}

    class PartNo10ApplBMSEndSgn3:
        sig_name = "PartNo10ApplBMSEndSgn3"
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

    class PartNo10ApplBMSNr4:
        sig_name = "PartNo10ApplBMSNr4"
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

    class PartNo10ApplBMSNr2:
        sig_name = "PartNo10ApplBMSNr2"
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

    class PartNo10ApplBMSEndSgn1:
        sig_name = "PartNo10ApplBMSEndSgn1"
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

    class PartNo10ApplBMSEndSgn2:
        sig_name = "PartNo10ApplBMSEndSgn2"
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

    class PartNo10ApplBMSNr5:
        sig_name = "PartNo10ApplBMSNr5"
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

    class PartNo10ApplBMSNr1:
        sig_name = "PartNo10ApplBMSNr1"
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

    class PartNo10ApplBMSNr3:
        sig_name = "PartNo10ApplBMSNr3"
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


class BmsCem_Lin6PartNrFr01:
    msg_name = "BmsCem_Lin6PartNrFr01"
    msg_id = 34
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNoBMS': ['PartNoBMSEndSgn1', 'PartNoBMSEndSgn2', 'PartNoBMSEndSgn3', 'PartNoBMSNr1', 'PartNoBMSNr2', 'PartNoBMSNr3', 'PartNoBMSNr4']}
    sig_group_dataid_dict = {}

    class PartNoBMSNr4:
        sig_name = "PartNoBMSNr4"
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

    class PartNoBMSEndSgn1:
        sig_name = "PartNoBMSEndSgn1"
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

    class PartNoBMSEndSgn2:
        sig_name = "PartNoBMSEndSgn2"
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

    class PartNoBMSEndSgn3:
        sig_name = "PartNoBMSEndSgn3"
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

    class PartNoBMSNr2:
        sig_name = "PartNoBMSNr2"
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

    class PartNoBMSNr1:
        sig_name = "PartNoBMSNr1"
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

    class PartNoBMSNr3:
        sig_name = "PartNoBMSNr3"
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


class DiagResponse5:
    msg_name = "DiagResponse5"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmCem_Lin6Fr01:
    msg_name = "BgmCem_Lin6Fr01"
    msg_id = 36
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['AWM']
    sig_group_dict = {'VehSpdLgt_3_AcuFLRCANFDSignalIPdu01': ['VehSpdLgtA_3_AcuFLRCANFDSignalIPdu01', 'VehSpdLgtChks_3_AcuFLRCANFDSignalIPdu01', 'VehSpdLgtCntr_3_AcuFLRCANFDSignalIPdu01', 'VehSpdLgtQf_3_AcuFLRCANFDSignalIPdu01'], 'AmbTRawAtPassSide': ['AmbTRawAtPassSideAmbTVal', 'AmbTRawAtPassSideQly']}
    sig_group_dataid_dict = {'VehSpdLgt_3_AcuFLRCANFDSignalIPdu01': 55}

    class ActvReSplrPosnCmd:
        sig_name = "ActvReSplrPosnCmd"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvSplrCmd_NoCmd': 0, 'ActvSplrCmd_P0': 1, 'ActvSplrCmd_P1': 2, 'ActvSplrCmd_P2': 3, 'ActvSplrCmd_P3': 4, 'ActvSplrCmd_Reserved1': 5, 'ActvSplrCmd_Reserved2': 6, 'ActvSplrCmd_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class AmbTRawAtPassSideAmbTVal:
        sig_name = "AmbTRawAtPassSideAmbTVal"
        sig_start_bit = 0
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
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000111, 0b11111000, 3, 0)]

    class VehSpdLgtQf_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtQf_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 32
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AmbTRawAtPassSideQly:
        sig_name = "AmbTRawAtPassSideQly"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class VehSpdLgtCntr_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtCntr_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehSpdLgtA_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtA_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 40
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b01111111, 0b10000000, 7, 0)]

    class VehSpdLgtChks_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtChks_3_AcuFLRCANFDSignalIPdu01"
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

    class CalforAWMPosn:
        sig_name = "CalforAWMPosn"
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
        sig_value_table = {'CalForAWMPosn_NoCmd': 0, 'CalForAWMPosn_ClrCmd': 1, 'CalForAWMPosn_LrngCmd': 2, 'CalForAWMPosn_ReqCmd': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


