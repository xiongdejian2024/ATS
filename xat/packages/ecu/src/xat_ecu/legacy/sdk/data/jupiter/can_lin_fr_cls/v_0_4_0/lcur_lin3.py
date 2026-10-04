lin_scheduleTable = {'LCUR_LIN3_DiagSchedule01': [(0, 'DiagRequest4', 0.015), (1, 'DiagResponse4', 0.015)], 'LCUR_LIN3ScheduleSerlNrPartNr_LCUR_LIN3': [(0, 'ACCMLCUR_LIN3Fr01', 0.015), (1, 'ACCMLCUR_LIN3Fr02', 0.015), (2, 'AGMLCUR_LIN3Fr01', 0.015), (3, 'AGMLCUR_LIN3Fr02', 0.015), (4, 'HAVHLCUR_LIN3Fr01', 0.015), (5, 'HAVHLCUR_LIN3Fr02', 0.015), (6, 'HVCHLCUR_LIN3Fr01', 0.015), (7, 'HVCHLCUR_LIN3Fr02', 0.015)], 'LCUR_LIN3Schedule01_LCUR_LIN3': [(0, 'ACCMLCUR_LIN3Fr03', 0.015), (1, 'ACCMLCUR_LIN3Fr04', 0.015), (2, 'AGMLCUR_LIN3Fr03', 0.015), (3, 'HAVHLCUR_LIN3Fr03', 0.015), (4, 'HAVHLCUR_LIN3Fr04', 0.015), (5, 'HAVHLCUR_LIN3Fr05', 0.015), (6, 'HVCHLCUR_LIN3Fr03', 0.015), (7, 'HVCHLCUR_LIN3Fr04', 0.015), (8, 'LCURLCUR_LIN3Fr01', 0.015), (9, 'LCURLCUR_LIN3Fr02', 0.015), (10, 'LCURLCUR_LIN3Fr03', 0.015)]}


class AGMLCUR_LIN3Fr02:
    msg_name = "AGMLCUR_LIN3Fr02"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AGM"
    rx_nodes = ['LCUR']
    sig_group_dict = {'AGMSerNo': ['AGMSerNoNr1', 'AGMSerNoNr2', 'AGMSerNoNr3', 'AGMSerNoNr4']}
    sig_group_dataid_dict = {}

    class AGMSerNoNr4:
        sig_name = "AGMSerNoNr4"
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

    class AGMSerNoNr2:
        sig_name = "AGMSerNoNr2"
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

    class AGMSerNoNr3:
        sig_name = "AGMSerNoNr3"
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

    class AGMSerNoNr1:
        sig_name = "AGMSerNoNr1"
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


class AGMLCUR_LIN3Fr03:
    msg_name = "AGMLCUR_LIN3Fr03"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AGM"
    rx_nodes = ['LCUR']
    sig_group_dict = {'GrlShttrSts': ['GrlShttrStsShttrActrFlt', 'GrlShttrStsShttrBlkSts', 'GrlShttrStsShttrCalActv', 'GrlShttrStsShttrCalIndcd', 'GrlShttrStsShttrElecErr', 'GrlShttrStsShttrOvrTempErr', 'GrlShttrStsShttrPosnFb', 'GrlShttrStsShttrSnsrFlt', 'GrlShttrStsShttrULoErr']}
    sig_group_dataid_dict = {}

    class GrlShttrStsShttrOvrTempErr:
        sig_name = "GrlShttrStsShttrOvrTempErr"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 15
        bmuws_info = [(1, 0b10000000, 0b01111111, 1, 7), (2, 0b00000001, 0b11111110, 1, 0)]

    class GrlShttrNVMFlt:
        sig_name = "GrlShttrNVMFlt"
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
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class GrlShttrHoldTrqActive:
        sig_name = "GrlShttrHoldTrqActive"
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

    class GrlShttrTqActive:
        sig_name = "GrlShttrTqActive"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TorqueBoost_TorqueMode0': 0, 'TorqueBoost_TorqueMode1': 1, 'TorqueBoost_BoostMode0': 2, 'TorqueBoost_BoostMode1': 3}
        compute_method = None
        length = 4
        startbit = 28
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class GrlShttrStsShttrElecErr:
        sig_name = "GrlShttrStsShttrElecErr"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class GrlShttrStsShttrSnsrFlt:
        sig_name = "GrlShttrStsShttrSnsrFlt"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class GrlShttrStsShttrCalActv:
        sig_name = "GrlShttrStsShttrCalActv"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrCalActv_NotActv': 0, 'ShttrCalActv_Actv': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GrlShttrOverVolt:
        sig_name = "GrlShttrOverVolt"
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
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class GrlShttrStsShttrULoErr:
        sig_name = "GrlShttrStsShttrULoErr"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class GrlShttrStsShttrActrFlt:
        sig_name = "GrlShttrStsShttrActrFlt"
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
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class GrlShttrStsShttrCalIndcd:
        sig_name = "GrlShttrStsShttrCalIndcd"
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
        sig_value_table = {'ShttrCalIndcd_ShttrCalNotIndcd': 0, 'ShttrCalIndcd_ShttrCalIndcd': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class GrlShttrOverTravelErr:
        sig_name = "GrlShttrOverTravelErr"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err_Initial': 0, 'Err_NoError': 1, 'Err_Error': 2, 'Err_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class GrlShttrStsShttrBlkSts:
        sig_name = "GrlShttrStsShttrBlkSts"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrBlkd_ShttrNotBlkd': 0, 'ShttrBlkd_ShttrBlkd': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class GrlShttrStsShttrPosnFb:
        sig_name = "GrlShttrStsShttrPosnFb"
        sig_start_bit = 17
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
        startbit = 17
        byte = 2
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class GrlShttrMoveActive:
        sig_name = "GrlShttrMoveActive"
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
        sig_value_table = {'VlvRunSts_NotMoving': 0, 'VlvRunSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class HAVHLCUR_LIN3Fr01:
    msg_name = "HAVHLCUR_LIN3Fr01"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HVAH"
    rx_nodes = ['LCUR']
    sig_group_dict = {'HVAHPartNo': ['HVAHPartNoEndSgn1', 'HVAHPartNoEndSgn2', 'HVAHPartNoEndSgn3', 'HVAHPartNoNr1', 'HVAHPartNoNr2', 'HVAHPartNoNr3', 'HVAHPartNoNr4', 'HVAHPartNoNr5']}
    sig_group_dataid_dict = {}

    class HVAHPartNoNr1:
        sig_name = "HVAHPartNoNr1"
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

    class HVAHPartNoEndSgn1:
        sig_name = "HVAHPartNoEndSgn1"
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

    class HVAHPartNoNr5:
        sig_name = "HVAHPartNoNr5"
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

    class HVAHPartNoNr3:
        sig_name = "HVAHPartNoNr3"
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

    class HVAHPartNoNr4:
        sig_name = "HVAHPartNoNr4"
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

    class HVAHPartNoEndSgn3:
        sig_name = "HVAHPartNoEndSgn3"
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

    class HVAHPartNoNr2:
        sig_name = "HVAHPartNoNr2"
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

    class HVAHPartNoEndSgn2:
        sig_name = "HVAHPartNoEndSgn2"
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


class LCURLCUR_LIN3Fr02:
    msg_name = "LCURLCUR_LIN3Fr02"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['HVAH', 'HVCH']
    sig_group_dict = {'HvCooltHeatrEnadWhE2E': ['HvCooltHeatrEnadWhE2EChks', 'HvCooltHeatrEnadWhE2ECntr', 'HvCooltHeatrEnadWhE2EHvchEnad'], 'HVAirHeatrE2E': ['HVAirHeatrE2EChks', 'HVAirHeatrE2ECntr', 'HVAirHeatrE2EHvahEnad']}
    sig_group_dataid_dict = {}

    class HvWtrHeatrWtrTDes:
        sig_name = "HvWtrHeatrWtrTDes"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVAirHeatrDutyReq:
        sig_name = "HVAirHeatrDutyReq"
        sig_start_bit = 57
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
        startbit = 57
        byte = 7
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class HvCooltHeatrEnadWhE2ECntr:
        sig_name = "HvCooltHeatrEnadWhE2ECntr"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HvCooltHeatrEnadWhE2EChks:
        sig_name = "HvCooltHeatrEnadWhE2EChks"
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

    class HVAirHeatrE2EHvahEnad:
        sig_name = "HVAirHeatrE2EHvahEnad"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvCooltHeatrEnadWhE2EHvchEnad:
        sig_name = "HvCooltHeatrEnadWhE2EHvchEnad"
        sig_start_bit = 56
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
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HVAirHeatrPwrAllwd:
        sig_name = "HVAirHeatrPwrAllwd"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00011111, 0b11100000, 5, 0)]

    class HVAirHeatrE2EChks:
        sig_name = "HVAirHeatrE2EChks"
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

    class HvWtrHeatrPwrCnsAllwd:
        sig_name = "HvWtrHeatrPwrCnsAllwd"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 40
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class HVAirHeatrE2ECntr:
        sig_name = "HVAirHeatrE2ECntr"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class HVCHLCUR_LIN3Fr01:
    msg_name = "HVCHLCUR_LIN3Fr01"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HVCH"
    rx_nodes = ['LCUR']
    sig_group_dict = {'HVCHPartNo10Cmpl': ['HVCHPartNo10CmplEndSgn1', 'HVCHPartNo10CmplEndSgn2', 'HVCHPartNo10CmplEndSgn3', 'HVCHPartNo10CmplNr1', 'HVCHPartNo10CmplNr2', 'HVCHPartNo10CmplNr3', 'HVCHPartNo10CmplNr4', 'HVCHPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class HVCHPartNo10CmplNr4:
        sig_name = "HVCHPartNo10CmplNr4"
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

    class HVCHPartNo10CmplNr2:
        sig_name = "HVCHPartNo10CmplNr2"
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

    class HVCHPartNo10CmplEndSgn3:
        sig_name = "HVCHPartNo10CmplEndSgn3"
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

    class HVCHPartNo10CmplNr1:
        sig_name = "HVCHPartNo10CmplNr1"
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

    class HVCHPartNo10CmplNr5:
        sig_name = "HVCHPartNo10CmplNr5"
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

    class HVCHPartNo10CmplEndSgn2:
        sig_name = "HVCHPartNo10CmplEndSgn2"
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

    class HVCHPartNo10CmplNr3:
        sig_name = "HVCHPartNo10CmplNr3"
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

    class HVCHPartNo10CmplEndSgn1:
        sig_name = "HVCHPartNo10CmplEndSgn1"
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


class LCURLCUR_LIN3Fr03:
    msg_name = "LCURLCUR_LIN3Fr03"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['AGM']
    sig_group_dict = {'AmbTEstimd': ['AmbTEstimdT', 'AmbTEstimdTQF']}
    sig_group_dataid_dict = {}

    class GrillShttrPosnReq:
        sig_name = "GrillShttrPosnReq"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class GrillShttrTqBoostReq:
        sig_name = "GrillShttrTqBoostReq"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TorqueBoost_TorqueMode0': 0, 'TorqueBoost_TorqueMode1': 1, 'TorqueBoost_BoostMode0': 2, 'TorqueBoost_BoostMode1': 3}
        compute_method = None
        length = 4
        startbit = 24
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class GrillShttrCalReq:
        sig_name = "GrillShttrCalReq"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AmbTEstimdTQF:
        sig_name = "AmbTEstimdTQF"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVACTempQf_SnsrDataNotOk': 0, 'HVACTempQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AmbTEstimdT:
        sig_name = "AmbTEstimdT"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -256
        sig_value_min = 0
        sig_value_max = 5119
        sig_byteorder = "Intel"
        sig_value_init = 2560
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00011111, 0b11100000, 5, 0)]

    class GrillShttrCalEna:
        sig_name = "GrillShttrCalEna"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisable4_NoCmd': 0, 'EnableDisable4_Disable': 1, 'EnableDisable4_Enable': 2}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class AGMLCUR_LIN3Fr01:
    msg_name = "AGMLCUR_LIN3Fr01"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "AGM"
    rx_nodes = ['LCUR']
    sig_group_dict = {'AGMPartNo': ['AGMPartNoEndSgn1', 'AGMPartNoEndSgn2', 'AGMPartNoEndSgn3', 'AGMPartNoNr1', 'AGMPartNoNr2', 'AGMPartNoNr3', 'AGMPartNoNr4', 'AGMPartNoNr5']}
    sig_group_dataid_dict = {}

    class AGMPartNoNr2:
        sig_name = "AGMPartNoNr2"
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

    class AGMPartNoNr5:
        sig_name = "AGMPartNoNr5"
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

    class AGMPartNoEndSgn1:
        sig_name = "AGMPartNoEndSgn1"
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

    class AGMPartNoEndSgn2:
        sig_name = "AGMPartNoEndSgn2"
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

    class AGMPartNoEndSgn3:
        sig_name = "AGMPartNoEndSgn3"
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

    class AGMPartNoNr1:
        sig_name = "AGMPartNoNr1"
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

    class AGMPartNoNr4:
        sig_name = "AGMPartNoNr4"
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

    class AGMPartNoNr3:
        sig_name = "AGMPartNoNr3"
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


class ACCMLCUR_LIN3Fr01:
    msg_name = "ACCMLCUR_LIN3Fr01"
    msg_id = 0
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ACCM"
    rx_nodes = ['LCUR']
    sig_group_dict = {'ACCMPartNo10Cmpl': ['ACCMPartNo10CmplEndSgn1', 'ACCMPartNo10CmplEndSgn2', 'ACCMPartNo10CmplEndSgn3', 'ACCMPartNo10CmplNr1', 'ACCMPartNo10CmplNr2', 'ACCMPartNo10CmplNr3', 'ACCMPartNo10CmplNr4', 'ACCMPartNo10CmplNr5']}
    sig_group_dataid_dict = {}

    class ACCMPartNo10CmplNr2:
        sig_name = "ACCMPartNo10CmplNr2"
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

    class ACCMPartNo10CmplEndSgn1:
        sig_name = "ACCMPartNo10CmplEndSgn1"
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

    class ACCMPartNo10CmplNr5:
        sig_name = "ACCMPartNo10CmplNr5"
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

    class ACCMPartNo10CmplEndSgn2:
        sig_name = "ACCMPartNo10CmplEndSgn2"
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

    class ACCMPartNo10CmplNr3:
        sig_name = "ACCMPartNo10CmplNr3"
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

    class ACCMPartNo10CmplNr1:
        sig_name = "ACCMPartNo10CmplNr1"
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

    class ACCMPartNo10CmplEndSgn3:
        sig_name = "ACCMPartNo10CmplEndSgn3"
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

    class ACCMPartNo10CmplNr4:
        sig_name = "ACCMPartNo10CmplNr4"
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


class HVCHLCUR_LIN3Fr03:
    msg_name = "HVCHLCUR_LIN3Fr03"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HVCH"
    rx_nodes = ['LCUR']
    sig_group_dict = {'HvCooltHeatrSnsrFltSig': ['HvCooltHeatrSnsrFltSigCooltTInSnsrFlt', 'HvCooltHeatrSnsrFltSigCooltTOutSnsrFlt', 'HvCooltHeatrSnsrFltSigResdForSnsrFlt', 'HvCooltHeatrSnsrFltSigTInMtrlSnsrFlt'], 'HvCooltHeatrWarnSig': ['HvCooltHeatrWarnSigCooltTOutOfRng', 'HvCooltHeatrWarnSigFltInCom', 'HvCooltHeatrWarnSigFltPrsnt', 'HvCooltHeatrWarnSigFltPrsntResd', 'HvCooltHeatrWarnSigHvOutOfRng', 'HvCooltHeatrWarnSigULoOutOfRng'], 'HvCooltHeatrProtnOfSelfTmpSig': ['HvCooltHeatrProtnOfSelfTmpSigHwProtn', 'HvCooltHeatrProtnOfSelfTmpSigOvrheatg', 'HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmp', 'HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmpResd'], 'HvCooltHeatrSrvRqrdSig': ['HvCooltHeatrSrvRqrdSigCircForDrvrShoOrOpen', 'HvCooltHeatrSrvRqrdSigICnsOutOfRng', 'HvCooltHeatrSrvRqrdSigMemErr', 'HvCooltHeatrSrvRqrdSigSrvRqrd', 'HvCooltHeatrSrvRqrdSigSrvRqrdResd']}
    sig_group_dataid_dict = {}

    class HvCooltHeatrSrvRqrdSigSrvRqrdResd:
        sig_name = "HvCooltHeatrSrvRqrdSigSrvRqrdResd"
        sig_start_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvCooltHeatrSnsrFltSigResdForSnsrFlt:
        sig_name = "HvCooltHeatrSnsrFltSigResdForSnsrFlt"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvCooltHeatrWarnSigULoOutOfRng:
        sig_name = "HvCooltHeatrWarnSigULoOutOfRng"
        sig_start_bit = 61
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
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvCooltHeatrSrvRqrdSigCircForDrvrShoOrOpen:
        sig_name = "HvCooltHeatrSrvRqrdSigCircForDrvrShoOrOpen"
        sig_start_bit = 33
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
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HvCooltHeatrProtnOfSelfTmpSigHwProtn:
        sig_name = "HvCooltHeatrProtnOfSelfTmpSigHwProtn"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HvCooltHeatrWarnSigFltInCom:
        sig_name = "HvCooltHeatrWarnSigFltInCom"
        sig_start_bit = 57
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
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HVCooltHeatrCooltTIn:
        sig_name = "HVCooltHeatrCooltTIn"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvCooltHeatrWarnSigFltPrsntResd:
        sig_name = "HvCooltHeatrWarnSigFltPrsntResd"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HvCooltHeatrSrvRqrdSigMemErr:
        sig_name = "HvCooltHeatrSrvRqrdSigMemErr"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HvCooltHeatrWarnSigHvOutOfRng:
        sig_name = "HvCooltHeatrWarnSigHvOutOfRng"
        sig_start_bit = 60
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
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvCooltHeatrSplyUForCtrlUnitValSig:
        sig_name = "HvCooltHeatrSplyUForCtrlUnitValSig"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class HvCooltHeatrWarnSigFltPrsnt:
        sig_name = "HvCooltHeatrWarnSigFltPrsnt"
        sig_start_bit = 58
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
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HvCooltHeatrSnsrFltSigCooltTOutSnsrFlt:
        sig_name = "HvCooltHeatrSnsrFltSigCooltTOutSnsrFlt"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class HvCooltHeatrSnsrFltSigTInMtrlSnsrFlt:
        sig_name = "HvCooltHeatrSnsrFltSigTInMtrlSnsrFlt"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HvCooltHeatrInfoCompProtn:
        sig_name = "HvCooltHeatrInfoCompProtn"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HvCooltHeatrICnsSig:
        sig_name = "HvCooltHeatrICnsSig"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmpResd:
        sig_name = "HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmpResd"
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

    class HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmp:
        sig_name = "HvCooltHeatrProtnOfSelfTmpSigProtnOfSelfTmp"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HVCooltHeatrStsSig:
        sig_name = "HVCooltHeatrStsSig"
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
        sig_value_table = {'HvCooltHeatrSts_Off': 0, 'HvCooltHeatrSts_LockedUntilNextStart': 1, 'HvCooltHeatrSts_LockedUntilService': 2, 'HvCooltHeatrSts_LockedPermanent': 3, 'HvCooltHeatrSts_Operation': 4, 'HvCooltHeatrSts_Reserved1': 5, 'HvCooltHeatrSts_Reserved2': 6, 'HvCooltHeatrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 48
        byte = 6
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class HvCooltHeatrSnsrFltSigCooltTInSnsrFlt:
        sig_name = "HvCooltHeatrSnsrFltSigCooltTInSnsrFlt"
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

    class HVCooltHeatrCooltTOut:
        sig_name = "HVCooltHeatrCooltTOut"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvCooltHeatrSrvRqrdSigICnsOutOfRng:
        sig_name = "HvCooltHeatrSrvRqrdSigICnsOutOfRng"
        sig_start_bit = 34
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
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HvCooltHeatrSrvRqrdSigSrvRqrd:
        sig_name = "HvCooltHeatrSrvRqrdSigSrvRqrd"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvCooltHeatrProtnOfSelfTmpSigOvrheatg:
        sig_name = "HvCooltHeatrProtnOfSelfTmpSigOvrheatg"
        sig_start_bit = 26
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
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HvCooltHeatrWarnSigCooltTOutOfRng:
        sig_name = "HvCooltHeatrWarnSigCooltTOutOfRng"
        sig_start_bit = 56
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
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class HAVHLCUR_LIN3Fr02:
    msg_name = "HAVHLCUR_LIN3Fr02"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HVAH"
    rx_nodes = ['LCUR']
    sig_group_dict = {'HVAHSerNo': ['HVAHSerNoNr1', 'HVAHSerNoNr2', 'HVAHSerNoNr3', 'HVAHSerNoNr4']}
    sig_group_dataid_dict = {}

    class HVAHSerNoNr4:
        sig_name = "HVAHSerNoNr4"
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

    class HVAHSerNoNr1:
        sig_name = "HVAHSerNoNr1"
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

    class HVAHSerNoNr2:
        sig_name = "HVAHSerNoNr2"
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

    class HVAHSerNoNr3:
        sig_name = "HVAHSerNoNr3"
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


class DiagResponse4:
    msg_name = "DiagResponse4"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HAVHLCUR_LIN3Fr05:
    msg_name = "HAVHLCUR_LIN3Fr05"
    msg_id = 11
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HVAH"
    rx_nodes = ['LCUR']
    sig_group_dict = {'HVAirHeatrStsWhE2E': ['HVAirHeatrStsWhE2EChks', 'HVAirHeatrStsWhE2ECntr', 'HVAirHeatrStsWhE2EHvahSts']}
    sig_group_dataid_dict = {}

    class HVAirHeatrStsWhE2ECntr:
        sig_name = "HVAirHeatrStsWhE2ECntr"
        sig_start_bit = 8
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
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HVAirHeatrStsWhE2EHvahSts:
        sig_name = "HVAirHeatrStsWhE2EHvahSts"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCooltHeatrSts_Off': 0, 'HvCooltHeatrSts_LockedUntilNextStart': 1, 'HvCooltHeatrSts_LockedUntilService': 2, 'HvCooltHeatrSts_LockedPermanent': 3, 'HvCooltHeatrSts_Operation': 4, 'HvCooltHeatrSts_Reserved1': 5, 'HvCooltHeatrSts_Reserved2': 6, 'HvCooltHeatrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 12
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class HVAirHeatrStsWhE2EChks:
        sig_name = "HVAirHeatrStsWhE2EChks"
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


class DiagRequest4:
    msg_name = "DiagRequest4"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HVCHLCUR_LIN3Fr04:
    msg_name = "HVCHLCUR_LIN3Fr04"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HVCH"
    rx_nodes = ['LCUR']
    sig_group_dict = {'HvCooltHeatrStsWhE2E': ['HvCooltHeatrStsWhE2EChks', 'HvCooltHeatrStsWhE2ECntr', 'HvCooltHeatrStsWhE2EHvchSts']}
    sig_group_dataid_dict = {}

    class HvCooltHeatrStsWhE2EChks:
        sig_name = "HvCooltHeatrStsWhE2EChks"
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

    class HvCooltHeatrStsWhE2EHvchSts:
        sig_name = "HvCooltHeatrStsWhE2EHvchSts"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCooltHeatrSts_Off': 0, 'HvCooltHeatrSts_LockedUntilNextStart': 1, 'HvCooltHeatrSts_LockedUntilService': 2, 'HvCooltHeatrSts_LockedPermanent': 3, 'HvCooltHeatrSts_Operation': 4, 'HvCooltHeatrSts_Reserved1': 5, 'HvCooltHeatrSts_Reserved2': 6, 'HvCooltHeatrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 12
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class HvCooltHeatrStsWhE2ECntr:
        sig_name = "HvCooltHeatrStsWhE2ECntr"
        sig_start_bit = 8
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
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HvHeatrPwrCnsDes:
        sig_name = "HvHeatrPwrCnsDes"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 20
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 30
        bmuws_info = [(3, 0b11000000, 0b00111111, 2, 6), (4, 0b11111111, 0b00000000, 8, 0)]

    class HvHeatrPwrCns:
        sig_name = "HvHeatrPwrCns"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 20
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 16
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b00000011, 0b11111100, 2, 0)]


class HVCHLCUR_LIN3Fr02:
    msg_name = "HVCHLCUR_LIN3Fr02"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HVCH"
    rx_nodes = ['LCUR']
    sig_group_dict = {'HVCHSerNo': ['HVCHSerNoNr1', 'HVCHSerNoNr2', 'HVCHSerNoNr3', 'HVCHSerNoNr4']}
    sig_group_dataid_dict = {}

    class HVCHSerNoNr1:
        sig_name = "HVCHSerNoNr1"
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

    class HVCHSerNoNr4:
        sig_name = "HVCHSerNoNr4"
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

    class HVCHSerNoNr2:
        sig_name = "HVCHSerNoNr2"
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

    class HVCHSerNoNr3:
        sig_name = "HVCHSerNoNr3"
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


class HAVHLCUR_LIN3Fr03:
    msg_name = "HAVHLCUR_LIN3Fr03"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HVAH"
    rx_nodes = ['LCUR']
    sig_group_dict = {'HvAirHeatrSts': ['HvAirHeatrStsHVCurrAct', 'HvAirHeatrStsHVPwrCns', 'HvAirHeatrStsHVVoltAct', 'HvAirHeatrStsIgbt1T', 'HvAirHeatrStsIgbt2T']}
    sig_group_dataid_dict = {}

    class HvAirHeatrStsHVPwrCns:
        sig_name = "HvAirHeatrStsHVPwrCns"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2046
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 40
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b00000111, 0b11111000, 3, 0)]

    class HVAirHeatrDutyFb:
        sig_name = "HVAirHeatrDutyFb"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 200
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

    class HvAirHeatrStsHVVoltAct:
        sig_name = "HvAirHeatrStsHVVoltAct"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class HvAirHeatrStsHVCurrAct:
        sig_name = "HvAirHeatrStsHVCurrAct"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 54
        bmuws_info = [(6, 0b11000000, 0b00111111, 2, 6), (7, 0b11111111, 0b00000000, 8, 0)]

    class HvAirHeatrStsIgbt1T:
        sig_name = "HvAirHeatrStsIgbt1T"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvAirHeatrStsIgbt2T:
        sig_name = "HvAirHeatrStsIgbt2T"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class LCURLCUR_LIN3Fr01:
    msg_name = "LCURLCUR_LIN3Fr01"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['ACCM', 'HVCH', 'HVAH']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CmprReqCmprPwrLim:
        sig_name = "CmprReqCmprPwrLim"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 40
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class HVAirHeatrCtrlMod:
        sig_name = "HVAirHeatrCtrlMod"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PTCCtrlMod_Default': 0, 'PTCCtrlMod_Duty': 1, 'PTCCtrlMod_Pwr': 2, 'PTCCtrlMod_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CmprReqCmprRunReq:
        sig_name = "CmprReqCmprRunReq"
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
        sig_value_table = {'CmprRunReq_CmprOff': 0, 'CmprRunReq_CmprOn': 1, 'CmprRunReq_Resd': 2, 'CmprRunReq_SigNotAvl': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HvCooltHeatrEnad:
        sig_name = "HvCooltHeatrEnad"
        sig_start_bit = 13
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
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HVAirHeatrEna:
        sig_name = "HVAirHeatrEna"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CmprReqCmprSpdReq:
        sig_name = "CmprReqCmprSpdReq"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 50
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CooltFlowInCmptmtCirc:
        sig_name = "CooltFlowInCmptmtCirc"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.05
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 24
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b00000011, 0b11111100, 2, 0)]


class ACCMLCUR_LIN3Fr03:
    msg_name = "ACCMLCUR_LIN3Fr03"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ACCM"
    rx_nodes = ['LCUR']
    sig_group_dict = {'CmprFb': ['CmprFbCmprI', 'CmprFbCmprIPha', 'CmprFbCmprSpd', 'CmprFbCmprSts1', 'CmprFbCmprSts2', 'CmprFbCmprT1', 'CmprFbCmprT2', 'CmprFbCmprU']}
    sig_group_dataid_dict = {}

    class CmprFbCmprSts2:
        sig_name = "CmprFbCmprSts2"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CompStat_NormalOperation': 0, 'CompStat_DegradedOperation': 1, 'CompStat_Inoperative': 2}
        compute_method = None
        length = 4
        startbit = 12
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CmprFbCmprU:
        sig_name = "CmprFbCmprU"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 48
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b00000011, 0b11111100, 2, 0)]

    class CmprFbCmprIPha:
        sig_name = "CmprFbCmprIPha"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmprFbCmprI:
        sig_name = "CmprFbCmprI"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
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

    class CmprFbCmprT1:
        sig_name = "CmprFbCmprT1"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmprHVoltResonanceStat:
        sig_name = "CmprHVoltResonanceStat"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AcHVoltResonanceStat_Normal': 0, 'AcHVoltResonanceStat_SpeedDecreased': 1, 'AcHVoltResonanceStat_Inoperative': 2, 'AcHVoltResonanceStat_Reserved': 3}
        compute_method = None
        length = 3
        startbit = 61
        byte = 7
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CmprFbCmprT2:
        sig_name = "CmprFbCmprT2"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmprFbCmprSpd:
        sig_name = "CmprFbCmprSpd"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 50
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmprFbCmprSts1:
        sig_name = "CmprFbCmprSts1"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmprSts_CmprOff': 0, 'CmprSts_CmprOn': 1, 'CmprSts_CmprPwrLimd': 2, 'CmprSts_CmprPreHeat': 3, 'CmprSts_Reserved1': 4, 'CmprSts_Reserved2': 5, 'CmprSts_Reserved3': 6, 'CmprSts_SigNotAvl': 7}
        compute_method = None
        length = 3
        startbit = 58
        byte = 7
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2


class HAVHLCUR_LIN3Fr04:
    msg_name = "HAVHLCUR_LIN3Fr04"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HVAH"
    rx_nodes = ['LCUR']
    sig_group_dict = {'HVAirHeatrOCPSts': ['HVAirHeatrOCPStsOvrTempFlt', 'HVAirHeatrOCPStsTempActl', 'HVAirHeatrOCPStsTempSnsrFlt'], 'HVAirHeatrFltSts': ['HVAirHeatrFltStsCurrSnsrFlt', 'HVAirHeatrFltStsDrvrFlt', 'HVAirHeatrFltStsHVHighFlt', 'HVAirHeatrFltStsHVLowFlt', 'HVAirHeatrFltStsHVSnsrFlt', 'HVAirHeatrFltStsIgbt1OvrTempFlt', 'HVAirHeatrFltStsIgbt1TempSnsrFlt', 'HVAirHeatrFltStsIgbt2OvrTempFlt', 'HVAirHeatrFltStsIgbt2TempSnsrFlt', 'HVAirHeatrFltStsIgbtDrvrFlt', 'HVAirHeatrFltStsIgbtShrtFlt', 'HVAirHeatrFltStsLINTimeOutFlt', 'HVAirHeatrFltStsOvrCurrFlt'], 'HVAirHeatrPCBSts': ['HVAirHeatrPCBStsOvrTempFlt', 'HVAirHeatrPCBStsTempActl', 'HVAirHeatrPCBStsTempSnsrFlt']}
    sig_group_dataid_dict = {}

    class HVAirHeatrFltStsDrvrFlt:
        sig_name = "HVAirHeatrFltStsDrvrFlt"
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
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVAirHeatrFltStsLINTimeOutFlt:
        sig_name = "HVAirHeatrFltStsLINTimeOutFlt"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVAirHeatrPCBStsOvrTempFlt:
        sig_name = "HVAirHeatrPCBStsOvrTempFlt"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 48
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HVAirHeatrFltStsIgbt1OvrTempFlt:
        sig_name = "HVAirHeatrFltStsIgbt1OvrTempFlt"
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
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVAirHeatrFltStsHVSnsrFlt:
        sig_name = "HVAirHeatrFltStsHVSnsrFlt"
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
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HVAirHeatrOCPStsTempActl:
        sig_name = "HVAirHeatrOCPStsTempActl"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVAirHeatrPwrDerating:
        sig_name = "HVAirHeatrPwrDerating"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PTCPwrDerating_Reserved': 0, 'PTCPwrDerating_PCBovertempderatingpower1': 1, 'PTCPwrDerating_IGBTovertempderatingpower2': 2, 'PTCPwrDerating_COREovertempderatingpower3': 3, 'PTCPwrDerating_SHUNTovertempderatingpower4': 4}
        compute_method = None
        length = 3
        startbit = 52
        byte = 6
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class HVAirHeatrFltStsHVHighFlt:
        sig_name = "HVAirHeatrFltStsHVHighFlt"
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
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HVAirHeatrFltStsCurrSnsrFlt:
        sig_name = "HVAirHeatrFltStsCurrSnsrFlt"
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
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 0
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HVAirHeatrFltStsIgbt2OvrTempFlt:
        sig_name = "HVAirHeatrFltStsIgbt2OvrTempFlt"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVAirHeatrOCPStsOvrTempFlt:
        sig_name = "HVAirHeatrOCPStsOvrTempFlt"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HVAirHeatrFltStsIgbt1TempSnsrFlt:
        sig_name = "HVAirHeatrFltStsIgbt1TempSnsrFlt"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HVAirHeatrPCBStsTempActl:
        sig_name = "HVAirHeatrPCBStsTempActl"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVAirHeatrFltStsHVLowFlt:
        sig_name = "HVAirHeatrFltStsHVLowFlt"
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
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVAirHeatrOCPStsTempSnsrFlt:
        sig_name = "HVAirHeatrOCPStsTempSnsrFlt"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HVAirHeatrFltStsIgbtDrvrFlt:
        sig_name = "HVAirHeatrFltStsIgbtDrvrFlt"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVAirHeatrPCBStsTempSnsrFlt:
        sig_name = "HVAirHeatrPCBStsTempSnsrFlt"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 50
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HVAirHeatrFltStsIgbtShrtFlt:
        sig_name = "HVAirHeatrFltStsIgbtShrtFlt"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HVAirHeatrFltStsOvrCurrFlt:
        sig_name = "HVAirHeatrFltStsOvrCurrFlt"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HVAirHeatrFltStsIgbt2TempSnsrFlt:
        sig_name = "HVAirHeatrFltStsIgbt2TempSnsrFlt"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_Initial': 0, 'Flt_NoFault': 1, 'Flt_Fault': 2}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class ACCMLCUR_LIN3Fr04:
    msg_name = "ACCMLCUR_LIN3Fr04"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ACCM"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CmprLiquidSluggingStat:
        sig_name = "CmprLiquidSluggingStat"
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
        sig_value_table = {'Flt1_NoFault': 0, 'Flt1_Fault': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CmprROMFlt:
        sig_name = "CmprROMFlt"
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
        sig_value_table = {'Flt1_NoFault': 0, 'Flt1_Fault': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CmprOverMotorCurrStat:
        sig_name = "CmprOverMotorCurrStat"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CompOverMotorCurrStat_Normal': 0, 'CompOverMotorCurrStat_ImmediatelyShutdown': 1, 'CompOverMotorCurrStat_SpeedIncreased': 2, 'CompOverMotorCurrStat_SpeedDecreased': 3, 'CompOverMotorCurrStat_Shutdown': 4}
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CmprEEPROMFault:
        sig_name = "CmprEEPROMFault"
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
        sig_value_table = {'Flt1_NoFault': 0, 'Flt1_Fault': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CmprRAMFlt:
        sig_name = "CmprRAMFlt"
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
        sig_value_table = {'Flt1_NoFault': 0, 'Flt1_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CmprRotorLockSts:
        sig_name = "CmprRotorLockSts"
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
        sig_value_table = {'Flt1_NoFault': 0, 'Flt1_Fault': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CmprLostCommStat:
        sig_name = "CmprLostCommStat"
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
        sig_value_table = {'Flt1_NoFault': 0, 'Flt1_Fault': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CmprMotorCurrOverCurrStat:
        sig_name = "CmprMotorCurrOverCurrStat"
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
        sig_value_table = {'Flt1_NoFault': 0, 'Flt1_Fault': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CmprInCurrOverCurrStat:
        sig_name = "CmprInCurrOverCurrStat"
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
        sig_value_table = {'Flt1_NoFault': 0, 'Flt1_Fault': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CmprOverPowerStat:
        sig_name = "CmprOverPowerStat"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CompOverPowerStat_Normal': 0, 'CompOverPowerStat_SpeedDecreasedforOverPower': 1, 'CompOverPowerStat_SpeedDecreasedforOverCurrent': 2, 'CompOverPowerStat_InoperativeforOverPower': 3, 'CompOverPowerStat_InoperativeforOverCurrent': 4}
        compute_method = None
        length = 4
        startbit = 12
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CmprSpdIncReq:
        sig_name = "CmprSpdIncReq"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt1_NoFault': 0, 'Flt1_Fault': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class ACCMLCUR_LIN3Fr02:
    msg_name = "ACCMLCUR_LIN3Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ACCM"
    rx_nodes = ['LCUR']
    sig_group_dict = {'ACCMSerNo': ['ACCMSerNoNr1', 'ACCMSerNoNr2', 'ACCMSerNoNr3', 'ACCMSerNoNr4']}
    sig_group_dataid_dict = {}

    class ACCMSerNoNr3:
        sig_name = "ACCMSerNoNr3"
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

    class ACCMSerNoNr1:
        sig_name = "ACCMSerNoNr1"
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

    class ACCMSerNoNr2:
        sig_name = "ACCMSerNoNr2"
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

    class ACCMSerNoNr4:
        sig_name = "ACCMSerNoNr4"
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


