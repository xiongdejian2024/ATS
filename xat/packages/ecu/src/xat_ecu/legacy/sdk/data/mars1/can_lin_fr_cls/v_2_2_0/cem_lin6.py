lin_scheduleTable = {'Cem_Lin6ScheduleSerNrPartNr_CEM_LIN6': [(0, 'AwmCem_Lin6Fr02', 0.015), (1, 'BmsCem_Lin6PartNrFr01', 0.01), (2, 'BmsCem_Lin6SerNrFr01', 0.01), (3, 'BmsCem_Lin6PartNrFr03', 0.01), (4, 'BmsCem_Lin6PartNrFr02', 0.01), (5, 'BmsCem_Lin6PartNrFr04', 0.01), (6, 'BmsCem_Lin6PartNrFr05', 0.015), (7, 'BmsCem_Lin6PartNrFr06', 0.015), (8, 'BmsCem_Lin6PartNrFr07', 0.015), (9, 'BmsCem_Lin6PartNrFr08', 0.015), (10, 'AwmCem_Lin6Fr01', 0.015)], 'Cem_Lin6_DiagRequestSchedule01': [(0, 'DiagRequest4', 0.015)], 'Cem_Lin6Schedule01_CEM_LIN6': [(0, 'AwmCem_Lin6Fr01', 0.015), (1, 'BgmCem_Lin6Fr01', 0.015), (2, 'BmsCem_Lin6Fr06', 0.01), (3, 'BmsCem_Lin6Fr02', 0.015), (4, 'BmsCem_Lin6Fr01', 0.015), (5, 'BmsCem_Lin6Fr03', 0.01), (6, 'BmsCem_Lin6Fr04', 0.01), (7, 'BmsCem_Lin6Fr05', 0.01), (8, 'BmsCem_Lin6Fr01', 0.015), (9, 'CemCem_Lin6Fr02', 0.015), (10, 'BmsCem_Lin6Fr05', 0.01), (11, 'BgmCem_Lin6Fr03', 0.015), (12, 'BmsCem_Lin6Fr07', 0.015)], 'Cem_Lin6_DiagResponseSchedule01': [(0, 'DiagResponse4', 0.015)]}


class AwmCem_Lin6Fr02:
    msg_name = "AwmCem_Lin6Fr02"
    msg_id = 33
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AWM"
    rx_nodes = ['BGM']
    sig_group_dict = {'AWMPartNo10Cmpl': ['AWMPartNo10CmplEndSgn1', 'AWMPartNo10CmplEndSgn2', 'AWMPartNo10CmplEndSgn3', 'AWMPartNo10CmplNr1', 'AWMPartNo10CmplNr2', 'AWMPartNo10CmplNr3', 'AWMPartNo10CmplNr4', 'AWMPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

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


class BmsCem_Lin6Fr02:
    msg_name = "BmsCem_Lin6Fr02"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

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


class BmsCem_Lin6Fr06:
    msg_name = "BmsCem_Lin6Fr06"
    msg_id = 40
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'EgyMeasIntl': ['EgyMeasIntlIntl1', 'EgyMeasIntlIntl2', 'EgyMeasIntlIntl3', 'EgyMeasIntlIntl4']}
    sig_group_dataid_dict = {}

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


class CemCem_Lin6Fr02:
    msg_name = "CemCem_Lin6Fr02"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 5
    tx_node = "BGM"
    rx_nodes = ['BMS']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

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


class BmsCem_Lin6SerNrFr01:
    msg_name = "BmsCem_Lin6SerNrFr01"
    msg_id = 35
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'NrSerlBMS': ['NrSerlBMSNr1', 'NrSerlBMSNr2', 'NrSerlBMSNr3', 'NrSerlBMSNr4']}
    sig_group_dataid_dict = {}

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


class BmsCem_Lin6Fr03:
    msg_name = "BmsCem_Lin6Fr03"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

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

    class BattTRaw:
        sig_name = "BattTRaw"
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

    class BattCpEstimdRaw:
        sig_name = "BattCpEstimdRaw"
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


class BgmCem_Lin6Fr01:
    msg_name = "BgmCem_Lin6Fr01"
    msg_id = 36
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['AWM']
    sig_group_dict = {'AmbTRawAtPassSide': ['AmbTRawAtPassSideAmbTVal', 'AmbTRawAtPassSideQly'], 'VehSpdLgt': ['VehSpdLgtA', 'VehSpdLgtChks', 'VehSpdLgtCntr', 'VehSpdLgtQf']}
    sig_group_dataid_dict = {'VehSpdLgt': 55}

    class VehSpdLgtCntr:
        sig_name = "VehSpdLgtCntr"
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

    class VehSpdLgtA:
        sig_name = "VehSpdLgtA"
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

    class VehSpdLgtQf:
        sig_name = "VehSpdLgtQf"
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

    class VehSpdLgtChks:
        sig_name = "VehSpdLgtChks"
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


class BmsCem_Lin6Fr07:
    msg_name = "BmsCem_Lin6Fr07"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BattSOHLAMRaw:
        sig_name = "BattSOHLAMRaw"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattSOHLAMRaw_Invalid': 255}
        compute_method = None
        length = 8
        startbit = 44
        bmuws_info = [(5, 0b11110000, 0b00001111, 4, 4), (6, 0b00001111, 0b11110000, 4, 0)]

    class BMSWakeUpTrgSrc:
        sig_name = "BMSWakeUpTrgSrc"
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
        sig_value_table = {'BMSWakeUpTrgSrc_NotReqd': 0, 'BMSWakeUpTrgSrc_LoSOC': 1, 'BMSWakeUpTrgSrc_LoVoltage': 2, 'BMSWakeUpTrgSrc_ChrgnCurrent': 3, 'BMSWakeUpTrgSrc_DisChrgnCurrent': 4, 'BMSWakeUpTrgSrc_Reserved1': 5, 'BMSWakeUpTrgSrc_Reserved2': 6, 'BMSWakeUpTrgSrc_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BattSOHCORRaw:
        sig_name = "BattSOHCORRaw"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattSOH_Invalid': 255}
        compute_method = None
        length = 8
        startbit = 34
        bmuws_info = [(4, 0b11111100, 0b00000011, 6, 2), (5, 0b00000011, 0b11111100, 2, 0)]

    class BattSOHCORSts:
        sig_name = "BattSOHCORSts"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOHSts_Not_Learned': 0, 'SOHSts_Learned': 1, 'SOHSts_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BattSOHLAMSts:
        sig_name = "BattSOHLAMSts"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOHSts_Not_Learned': 0, 'SOHSts_Learned': 1, 'SOHSts_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BattSOHSULRaw:
        sig_name = "BattSOHSULRaw"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattSOH_Invalid': 255}
        compute_method = None
        length = 8
        startbit = 54
        bmuws_info = [(6, 0b11000000, 0b00111111, 2, 6), (7, 0b00111111, 0b11000000, 6, 0)]

    class BattSocSts:
        sig_name = "BattSocSts"
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
        sig_value_table = {'BattSocSts_Larger15Per': 0, 'BattSocSts_LessOrEqual15Per': 1, 'BattSocSts_LessOrEqual10Per': 2, 'BattSocSts_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class BattSOHSULSts:
        sig_name = "BattSOHSULSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SOHSts_Not_Learned': 0, 'SOHSts_Learned': 1, 'SOHSts_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class BmsCem_Lin6PartNrFr03:
    msg_name = "BmsCem_Lin6PartNrFr03"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
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


class AwmCem_Lin6Fr01:
    msg_name = "AwmCem_Lin6Fr01"
    msg_id = 32
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AWM"
    rx_nodes = ['BGM']
    sig_group_dict = {'ActvReSplrHallSnsrFlt': ['ActvReSplrHallSnsrFltHallAFlt', 'ActvReSplrHallSnsrFltHallBFlt', 'ActvReSplrHallSnsrFltHallOutpFlt'], 'ActvReSplrUFlt': ['ActvReSplrUFltHiVoltDetdFlt', 'ActvReSplrUFltLoVoltDetdFlt'], 'ActvReSplrIntFlt': ['ActvReSplrIntFltActrFlt1', 'ActvReSplrIntFltActrFlt2', 'ActvReSplrIntFltActrFlt3', 'ActvReSplrIntFltActrFlt4', 'ActvReSplrIntFltActrFlt5', 'ActvReSplrIntFltTmrFlt'], 'AWMSerNo': ['AWMSerNoNr1', 'AWMSerNoNr2', 'AWMSerNoNr3', 'AWMSerNoNr4']}
    sig_group_dataid_dict = {}

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


class BgmCem_Lin6Fr03:
    msg_name = "BgmCem_Lin6Fr03"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BMSSocWakeUpEna:
        sig_name = "BMSSocWakeUpEna"
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
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BMSVolWakeUpThd:
        sig_name = "BMSVolWakeUpThd"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.02
        sig_value_offset = 9.0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BMSVolWakeUpThd': 255}
        compute_method = None
        length = 8
        startbit = 55
        bmuws_info = [(6, 0b10000000, 0b01111111, 1, 7), (7, 0b01111111, 0b10000000, 7, 0)]

    class BMSVolWakeUpEna:
        sig_name = "BMSVolWakeUpEna"
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
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BMSChrgnCurrWakeUpEna:
        sig_name = "BMSChrgnCurrWakeUpEna"
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
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BMSSocWakeUpThd:
        sig_name = "BMSSocWakeUpThd"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Intel"
        sig_value_init = 255
        sig_value_type = "SCALE_LINEAR_AND_TEXTTABLE"
        sig_value_table = {'BattSOH_Invalid': 255}
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BMSDisChrgnCurrWakeUpThd:
        sig_name = "BMSDisChrgnCurrWakeUpThd"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65520
        sig_byteorder = "Intel"
        sig_value_init = 65520
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class BMSDisChrgnCurrWakeUpEna:
        sig_name = "BMSDisChrgnCurrWakeUpEna"
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
        sig_value_table = {'EnableDisable_Enable': 0, 'EnableDisable_Disable': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BMSChrgnCurrWakeUpThd:
        sig_name = "BMSChrgnCurrWakeUpThd"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65520
        sig_byteorder = "Intel"
        sig_value_init = 65520
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class BmsCem_Lin6PartNrFr07:
    msg_name = "BmsCem_Lin6PartNrFr07"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNo10BMS': ['PartNo10BMSEndSgn1', 'PartNo10BMSEndSgn2', 'PartNo10BMSEndSgn3', 'PartNo10BMSNr1', 'PartNo10BMSNr2', 'PartNo10BMSNr3', 'PartNo10BMSNr4', 'PartNo10BMSNr5']}
    sig_group_dataid_dict = {}

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


class BmsCem_Lin6PartNrFr05:
    msg_name = "BmsCem_Lin6PartNrFr05"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNo10ApplBMS': ['PartNo10ApplBMSEndSgn1', 'PartNo10ApplBMSEndSgn2', 'PartNo10ApplBMSEndSgn3', 'PartNo10ApplBMSNr1', 'PartNo10ApplBMSNr2', 'PartNo10ApplBMSNr3', 'PartNo10ApplBMSNr4', 'PartNo10ApplBMSNr5']}
    sig_group_dataid_dict = {}

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


class BmsCem_Lin6PartNrFr08:
    msg_name = "BmsCem_Lin6PartNrFr08"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNo10HwBMS': ['PartNo10HwBMSEndSgn1', 'PartNo10HwBMSEndSgn2', 'PartNo10HwBMSEndSgn3', 'PartNo10HwBMSNr1', 'PartNo10HwBMSNr2', 'PartNo10HwBMSNr3', 'PartNo10HwBMSNr4', 'PartNo10HwBMSNr5']}
    sig_group_dataid_dict = {}

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


class BmsCem_Lin6PartNrFr01:
    msg_name = "BmsCem_Lin6PartNrFr01"
    msg_id = 34
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNoBMS': ['PartNoBMSEndSgn1', 'PartNoBMSEndSgn2', 'PartNoBMSEndSgn3', 'PartNoBMSNr1', 'PartNoBMSNr2', 'PartNoBMSNr3', 'PartNoBMSNr4']}
    sig_group_dataid_dict = {}

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


class BmsCem_Lin6PartNrFr02:
    msg_name = "BmsCem_Lin6PartNrFr02"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNoApplBMS': ['PartNoApplBMSEndSgn1', 'PartNoApplBMSEndSgn2', 'PartNoApplBMSEndSgn3', 'PartNoApplBMSNr1', 'PartNoApplBMSNr2', 'PartNoApplBMSNr3', 'PartNoApplBMSNr4']}
    sig_group_dataid_dict = {}

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


class BmsCem_Lin6PartNrFr04:
    msg_name = "BmsCem_Lin6PartNrFr04"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNoHwBMS': ['PartNoHwBMSEndSgn1', 'PartNoHwBMSEndSgn2', 'PartNoHwBMSEndSgn3', 'PartNoHwBMSNr1', 'PartNoHwBMSNr2', 'PartNoHwBMSNr3', 'PartNoHwBMSNr4']}
    sig_group_dataid_dict = {}

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


class BmsCem_Lin6Fr04:
    msg_name = "BmsCem_Lin6Fr04"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

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

    class BattRRaw:
        sig_name = "BattRRaw"
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

    class BattCircOpenU:
        sig_name = "BattCircOpenU"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 5
        sig_value_factor = 0.25
        sig_value_offset = 6
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


class BmsCem_Lin6PartNrFr06:
    msg_name = "BmsCem_Lin6PartNrFr06"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BMS"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNo10ApplDiagBMS': ['PartNo10ApplDiagBMSEndSgn1', 'PartNo10ApplDiagBMSEndSgn2', 'PartNo10ApplDiagBMSEndSgn3', 'PartNo10ApplDiagBMSNr1', 'PartNo10ApplDiagBMSNr2', 'PartNo10ApplDiagBMSNr3', 'PartNo10ApplDiagBMSNr4', 'PartNo10ApplDiagBMSNr5']}
    sig_group_dataid_dict = {}

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


class BmsCem_Lin6Fr05:
    msg_name = "BmsCem_Lin6Fr05"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
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

    class BattSnsrType:
        sig_name = "BattSnsrType"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BattSnsrType_AWC': 0, 'BattSnsrType_Reserved01': 1, 'BattSnsrType_Reserved02': 2, 'BattSnsrType_NAWC': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BattURaw:
        sig_name = "BattURaw"
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


class BmsCem_Lin6Fr01:
    msg_name = "BmsCem_Lin6Fr01"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
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

    class BattIRaw:
        sig_name = "BattIRaw"
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


