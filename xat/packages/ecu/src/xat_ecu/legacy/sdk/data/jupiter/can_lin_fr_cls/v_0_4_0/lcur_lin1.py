lin_scheduleTable = {'LCUR_LIN1Schedule01_LCUR_LIN1': [(0, 'BCFVLCUR_LIN1Fr03', 0.015), (1, 'BCTVLCUR_LIN1Fr03', 0.015), (2, 'CCTVLCUR_LIN1Fr03', 0.015), (3, 'DCTVLCUR_LIN1Fr03', 0.015), (4, 'ECTVLCUR_LIN1Fr03', 0.015), (5, 'HCTVLCUR_LIN1Fr03', 0.015), (6, 'LCTVLCUR_LIN1Fr03', 0.015), (7, 'LCURLCUR_LIN1Fr01', 0.015), (8, 'LCURLCUR_LIN1Fr02', 0.015)], 'LCUR_LIN1_DiagSchedule01': [(0, 'DiagRequest3', 0.015), (1, 'DiagResponse3', 0.015)], 'LCUR_LIN1ScheduleSerlNrPartNr_LCUR_LIN1': [(0, 'BCFVLCUR_LIN1Fr01', 0.015), (1, 'BCFVLCUR_LIN1Fr02', 0.015), (2, 'BCTVLCUR_LIN1Fr01', 0.015), (3, 'BCTVLCUR_LIN1Fr02', 0.015), (4, 'CCTVLCUR_LIN1Fr01', 0.015), (5, 'CCTVLCUR_LIN1Fr02', 0.015), (6, 'DCTVLCUR_LIN1Fr01', 0.015), (7, 'DCTVLCUR_LIN1Fr02', 0.015), (8, 'ECTVLCUR_LIN1Fr01', 0.015), (9, 'ECTVLCUR_LIN1Fr02', 0.015), (10, 'HCTVLCUR_LIN1Fr01', 0.015), (11, 'HCTVLCUR_LIN1Fr02', 0.015), (12, 'LCTVLCUR_LIN1Fr01', 0.015), (13, 'LCTVLCUR_LIN1Fr02', 0.015)]}


class ECTVLCUR_LIN1Fr01:
    msg_name = "ECTVLCUR_LIN1Fr01"
    msg_id = 12
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ECTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'ECTVPartNo': ['ECTVPartNoEndSgn1', 'ECTVPartNoEndSgn2', 'ECTVPartNoEndSgn3', 'ECTVPartNoNr1', 'ECTVPartNoNr2', 'ECTVPartNoNr3', 'ECTVPartNoNr4', 'ECTVPartNoNr5']}
    sig_group_dataid_dict = {}

    class ECTVPartNoNr1:
        sig_name = "ECTVPartNoNr1"
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

    class ECTVPartNoEndSgn3:
        sig_name = "ECTVPartNoEndSgn3"
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

    class ECTVPartNoEndSgn1:
        sig_name = "ECTVPartNoEndSgn1"
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

    class ECTVPartNoNr5:
        sig_name = "ECTVPartNoNr5"
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

    class ECTVPartNoNr2:
        sig_name = "ECTVPartNoNr2"
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

    class ECTVPartNoNr4:
        sig_name = "ECTVPartNoNr4"
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

    class ECTVPartNoEndSgn2:
        sig_name = "ECTVPartNoEndSgn2"
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

    class ECTVPartNoNr3:
        sig_name = "ECTVPartNoNr3"
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


class LCURLCUR_LIN1Fr02:
    msg_name = "LCURLCUR_LIN1Fr02"
    msg_id = 22
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['ECTV', 'HCTV', 'LCTV']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HCTVPosnSaveReq:
        sig_name = "HCTVPosnSaveReq"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActiveSaveReq_NoReq': 0, 'ActiveSaveReq_ActiveSave_Req': 1, 'ActiveSaveReq_Reserved': 2, 'ActiveSaveReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LCTVSpdLvlReq:
        sig_name = "LCTVSpdLvlReq"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpdLvlReq_Level0_Slow': 0, 'SpdLvlReq_Level1_Normal': 1, 'SpdLvlReq_Level2_Fast': 2, 'SpdLvlReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 38
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HCTVSpdLvlReq:
        sig_name = "HCTVSpdLvlReq"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpdLvlReq_Level0_Slow': 0, 'SpdLvlReq_Level1_Normal': 1, 'SpdLvlReq_Level2_Fast': 2, 'SpdLvlReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 32
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ECTVCalReq:
        sig_name = "ECTVCalReq"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RefDrvReq_NoReq': 0, 'RefDrvReq_REFDRV_Req': 1, 'RefDrvReq_Reserved': 2, 'RefDrvReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 7
        bmuws_info = [(0, 0b10000000, 0b01111111, 1, 7), (1, 0b00000001, 0b11111110, 1, 0)]

    class LCTVPosnSaveReq:
        sig_name = "LCTVPosnSaveReq"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActiveSaveReq_NoReq': 0, 'ActiveSaveReq_ActiveSave_Req': 1, 'ActiveSaveReq_Reserved': 2, 'ActiveSaveReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HCTVPosnSetReq:
        sig_name = "HCTVPosnSetReq"
        sig_start_bit = 9
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
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class LCTVCalReq:
        sig_name = "LCTVCalReq"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RefDrvReq_NoReq': 0, 'RefDrvReq_REFDRV_Req': 1, 'RefDrvReq_Reserved': 2, 'RefDrvReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ECTVPosnSaveReq:
        sig_name = "ECTVPosnSaveReq"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActiveSaveReq_NoReq': 0, 'ActiveSaveReq_ActiveSave_Req': 1, 'ActiveSaveReq_Reserved': 2, 'ActiveSaveReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ECTVSpdLvlReq:
        sig_name = "ECTVSpdLvlReq"
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
        sig_value_table = {'SpdLvlReq_Level0_Slow': 0, 'SpdLvlReq_Level1_Normal': 1, 'SpdLvlReq_Level2_Fast': 2, 'SpdLvlReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ECTVPosnSetReq:
        sig_name = "ECTVPosnSetReq"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class HCTVCalReq:
        sig_name = "HCTVCalReq"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RefDrvReq_NoReq': 0, 'RefDrvReq_REFDRV_Req': 1, 'RefDrvReq_Reserved': 2, 'RefDrvReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LCTVPosnSetReq:
        sig_name = "LCTVPosnSetReq"
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


class LCURLCUR_LIN1Fr01:
    msg_name = "LCURLCUR_LIN1Fr01"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCUR"
    rx_nodes = ['DCTV', 'BCFV', 'CCTV', 'BCTV']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BCTVPosnSetReq:
        sig_name = "BCTVPosnSetReq"
        sig_start_bit = 9
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
        startbit = 9
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class DCTVPosnSetReq:
        sig_name = "DCTVPosnSetReq"
        sig_start_bit = 25
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
        startbit = 25
        byte = 3
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class DCTVCalReq:
        sig_name = "DCTVCalReq"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RefDrvReq_NoReq': 0, 'RefDrvReq_REFDRV_Req': 1, 'RefDrvReq_Reserved': 2, 'RefDrvReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 46
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BCFVSpdLvlReq:
        sig_name = "BCFVSpdLvlReq"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpdLvlReq_Level0_Slow': 0, 'SpdLvlReq_Level1_Normal': 1, 'SpdLvlReq_Level2_Fast': 2, 'SpdLvlReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 32
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CCTVCalReq:
        sig_name = "CCTVCalReq"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RefDrvReq_NoReq': 0, 'RefDrvReq_REFDRV_Req': 1, 'RefDrvReq_Reserved': 2, 'RefDrvReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 40
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BCTVSpdLvlReq:
        sig_name = "BCTVSpdLvlReq"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpdLvlReq_Level0_Slow': 0, 'SpdLvlReq_Level1_Normal': 1, 'SpdLvlReq_Level2_Fast': 2, 'SpdLvlReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 38
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CCTVPosnSaveReq:
        sig_name = "CCTVPosnSaveReq"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActiveSaveReq_NoReq': 0, 'ActiveSaveReq_ActiveSave_Req': 1, 'ActiveSaveReq_Reserved': 2, 'ActiveSaveReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CCTVSpdLvlReq:
        sig_name = "CCTVSpdLvlReq"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpdLvlReq_Level0_Slow': 0, 'SpdLvlReq_Level1_Normal': 1, 'SpdLvlReq_Level2_Fast': 2, 'SpdLvlReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DCTVSpdLvlReq:
        sig_name = "DCTVSpdLvlReq"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpdLvlReq_Level0_Slow': 0, 'SpdLvlReq_Level1_Normal': 1, 'SpdLvlReq_Level2_Fast': 2, 'SpdLvlReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 50
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BCFVPosnSaveReq:
        sig_name = "BCFVPosnSaveReq"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActiveSaveReq_NoReq': 0, 'ActiveSaveReq_ActiveSave_Req': 1, 'ActiveSaveReq_Reserved': 2, 'ActiveSaveReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 23
        bmuws_info = [(2, 0b10000000, 0b01111111, 1, 7), (3, 0b00000001, 0b11111110, 1, 0)]

    class CCTVPosnSetReq:
        sig_name = "CCTVPosnSetReq"
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

    class BCTVCalReq:
        sig_name = "BCTVCalReq"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RefDrvReq_NoReq': 0, 'RefDrvReq_REFDRV_Req': 1, 'RefDrvReq_Reserved': 2, 'RefDrvReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BCTVPosnSaveReq:
        sig_name = "BCTVPosnSaveReq"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActiveSaveReq_NoReq': 0, 'ActiveSaveReq_ActiveSave_Req': 1, 'ActiveSaveReq_Reserved': 2, 'ActiveSaveReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BCFVPosnSetReq:
        sig_name = "BCFVPosnSetReq"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class BCFVCalReq:
        sig_name = "BCFVCalReq"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RefDrvReq_NoReq': 0, 'RefDrvReq_REFDRV_Req': 1, 'RefDrvReq_Reserved': 2, 'RefDrvReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 7
        bmuws_info = [(0, 0b10000000, 0b01111111, 1, 7), (1, 0b00000001, 0b11111110, 1, 0)]

    class DCTVPosnSaveReq:
        sig_name = "DCTVPosnSaveReq"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActiveSaveReq_NoReq': 0, 'ActiveSaveReq_ActiveSave_Req': 1, 'ActiveSaveReq_Reserved': 2, 'ActiveSaveReq_SNA': 3}
        compute_method = None
        length = 2
        startbit = 48
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class HCTVLCUR_LIN1Fr03:
    msg_name = "HCTVLCUR_LIN1Fr03"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HCTVFltSts:
        sig_name = "HCTVFltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaultSts_NoError': 0, 'FaultSts_PositionUnknown': 1, 'FaultSts_PCTR_Error': 2, 'FaultSts_Blocking_Err': 3, 'FaultSts_SetPoint_Err': 4, 'FaultSts_Learning_Err': 5, 'FaultSts_MotorCoilShort': 6, 'FaultSts_MotorCoilOpen': 7, 'FaultSts_MotorDrvOvertemperatureShutdown': 8, 'FaultSts_Indeterminate': 9, 'FaultSts_Reserved': 10, 'FaultSts_SNA': 15}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HCTVSpdLvl:
        sig_name = "HCTVSpdLvl"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpeedLvl_SpeedLevelLow': 0, 'SpeedLvl_SpeedLevelNormal': 1, 'SpeedLvl_SpeedLevelFast': 2, 'SpeedLvl_SNA': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HCTVVoltSts:
        sig_name = "HCTVVoltSts"
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
        sig_value_table = {'VoltSts_VoltageOK': 0, 'VoltSts_OverVoltage': 1, 'VoltSts_UnderVoltage': 2, 'VoltSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HCTVNVMFlt:
        sig_name = "HCTVNVMFlt"
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

    class HCTVPosnAct:
        sig_name = "HCTVPosnAct"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b00000011, 0b11111100, 2, 0)]

    class HCTVRunSts:
        sig_name = "HCTVRunSts"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HCTVMod:
        sig_name = "HCTVMod"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvMode_NormalOperation': 0, 'VlvMode_Mot_Off': 1, 'VlvMode_Learning': 2, 'VlvMode_Fail_Safe': 3, 'VlvMode_SNA': 15}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HCTVTempSts:
        sig_name = "HCTVTempSts"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempSts_Temperatureok': 0, 'TempSts_OvertemperatureWarning': 1, 'TempSts_PCBOvertemperature': 2, 'TempSts_LowTemperature': 3, 'TempSts_notused': 4, 'TempSts_SNA': 7}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CCTVLCUR_LIN1Fr02:
    msg_name = "CCTVLCUR_LIN1Fr02"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "CCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'CCTVSerNo': ['CCTVSerNoNr1', 'CCTVSerNoNr2', 'CCTVSerNoNr3', 'CCTVSerNoNr4']}
    sig_group_dataid_dict = {}

    class CCTVSerNoNr1:
        sig_name = "CCTVSerNoNr1"
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

    class CCTVSerNoNr3:
        sig_name = "CCTVSerNoNr3"
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

    class CCTVSerNoNr4:
        sig_name = "CCTVSerNoNr4"
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

    class CCTVSerNoNr2:
        sig_name = "CCTVSerNoNr2"
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


class BCFVLCUR_LIN1Fr01:
    msg_name = "BCFVLCUR_LIN1Fr01"
    msg_id = 0
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BCFV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'BCFVPartNo': ['BCFVPartNoEndSgn1', 'BCFVPartNoEndSgn2', 'BCFVPartNoEndSgn3', 'BCFVPartNoNr1', 'BCFVPartNoNr2', 'BCFVPartNoNr3', 'BCFVPartNoNr4', 'BCFVPartNoNr5']}
    sig_group_dataid_dict = {}

    class BCFVPartNoEndSgn3:
        sig_name = "BCFVPartNoEndSgn3"
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

    class BCFVPartNoNr4:
        sig_name = "BCFVPartNoNr4"
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

    class BCFVPartNoNr2:
        sig_name = "BCFVPartNoNr2"
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

    class BCFVPartNoNr3:
        sig_name = "BCFVPartNoNr3"
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

    class BCFVPartNoEndSgn2:
        sig_name = "BCFVPartNoEndSgn2"
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

    class BCFVPartNoNr5:
        sig_name = "BCFVPartNoNr5"
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

    class BCFVPartNoEndSgn1:
        sig_name = "BCFVPartNoEndSgn1"
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

    class BCFVPartNoNr1:
        sig_name = "BCFVPartNoNr1"
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


class ECTVLCUR_LIN1Fr02:
    msg_name = "ECTVLCUR_LIN1Fr02"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ECTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'ECTVSerNo': ['ECTVSerNoNr1', 'ECTVSerNoNr2', 'ECTVSerNoNr3', 'ECTVSerNoNr4']}
    sig_group_dataid_dict = {}

    class ECTVSerNoNr1:
        sig_name = "ECTVSerNoNr1"
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

    class ECTVSerNoNr2:
        sig_name = "ECTVSerNoNr2"
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

    class ECTVSerNoNr3:
        sig_name = "ECTVSerNoNr3"
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

    class ECTVSerNoNr4:
        sig_name = "ECTVSerNoNr4"
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


class BCTVLCUR_LIN1Fr01:
    msg_name = "BCTVLCUR_LIN1Fr01"
    msg_id = 3
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'BCTVPartNo': ['BCTVPartNoEndSgn1', 'BCTVPartNoEndSgn2', 'BCTVPartNoEndSgn3', 'BCTVPartNoNr1', 'BCTVPartNoNr2', 'BCTVPartNoNr3', 'BCTVPartNoNr4', 'BCTVPartNoNr5']}
    sig_group_dataid_dict = {}

    class BCTVPartNoNr5:
        sig_name = "BCTVPartNoNr5"
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

    class BCTVPartNoNr1:
        sig_name = "BCTVPartNoNr1"
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

    class BCTVPartNoEndSgn2:
        sig_name = "BCTVPartNoEndSgn2"
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

    class BCTVPartNoNr4:
        sig_name = "BCTVPartNoNr4"
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

    class BCTVPartNoNr2:
        sig_name = "BCTVPartNoNr2"
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

    class BCTVPartNoNr3:
        sig_name = "BCTVPartNoNr3"
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

    class BCTVPartNoEndSgn3:
        sig_name = "BCTVPartNoEndSgn3"
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

    class BCTVPartNoEndSgn1:
        sig_name = "BCTVPartNoEndSgn1"
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


class DiagRequest1:
    msg_name = "DiagRequest1"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "LCUR"
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
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DCTVLCUR_LIN1Fr02:
    msg_name = "DCTVLCUR_LIN1Fr02"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "DCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'DCTVSerNo': ['DCTVSerNoNr1', 'DCTVSerNoNr2', 'DCTVSerNoNr3', 'DCTVSerNoNr4']}
    sig_group_dataid_dict = {}

    class DCTVSerNoNr2:
        sig_name = "DCTVSerNoNr2"
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

    class DCTVSerNoNr3:
        sig_name = "DCTVSerNoNr3"
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

    class DCTVSerNoNr1:
        sig_name = "DCTVSerNoNr1"
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

    class DCTVSerNoNr4:
        sig_name = "DCTVSerNoNr4"
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


class LCTVLCUR_LIN1Fr03:
    msg_name = "LCTVLCUR_LIN1Fr03"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class LCTVMod:
        sig_name = "LCTVMod"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvMode_NormalOperation': 0, 'VlvMode_Mot_Off': 1, 'VlvMode_Learning': 2, 'VlvMode_Fail_Safe': 3, 'VlvMode_SNA': 15}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class LCTVSpdLvl:
        sig_name = "LCTVSpdLvl"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpeedLvl_SpeedLevelLow': 0, 'SpeedLvl_SpeedLevelNormal': 1, 'SpeedLvl_SpeedLevelFast': 2, 'SpeedLvl_SNA': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LCTVNVMFlt:
        sig_name = "LCTVNVMFlt"
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

    class LCTVPosnAct:
        sig_name = "LCTVPosnAct"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b00000011, 0b11111100, 2, 0)]

    class LCTVFltSts:
        sig_name = "LCTVFltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaultSts_NoError': 0, 'FaultSts_PositionUnknown': 1, 'FaultSts_PCTR_Error': 2, 'FaultSts_Blocking_Err': 3, 'FaultSts_SetPoint_Err': 4, 'FaultSts_Learning_Err': 5, 'FaultSts_MotorCoilShort': 6, 'FaultSts_MotorCoilOpen': 7, 'FaultSts_MotorDrvOvertemperatureShutdown': 8, 'FaultSts_Indeterminate': 9, 'FaultSts_Reserved': 10, 'FaultSts_SNA': 15}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class LCTVTempSts:
        sig_name = "LCTVTempSts"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempSts_Temperatureok': 0, 'TempSts_OvertemperatureWarning': 1, 'TempSts_PCBOvertemperature': 2, 'TempSts_LowTemperature': 3, 'TempSts_notused': 4, 'TempSts_SNA': 7}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class LCTVRunSts:
        sig_name = "LCTVRunSts"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class LCTVVoltSts:
        sig_name = "LCTVVoltSts"
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
        sig_value_table = {'VoltSts_VoltageOK': 0, 'VoltSts_OverVoltage': 1, 'VoltSts_UnderVoltage': 2, 'VoltSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class HCTVLCUR_LIN1Fr02:
    msg_name = "HCTVLCUR_LIN1Fr02"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'HCTVSerNo': ['HCTVSerNoNr1', 'HCTVSerNoNr2', 'HCTVSerNoNr3', 'HCTVSerNoNr4']}
    sig_group_dataid_dict = {}

    class HCTVSerNoNr3:
        sig_name = "HCTVSerNoNr3"
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

    class HCTVSerNoNr2:
        sig_name = "HCTVSerNoNr2"
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

    class HCTVSerNoNr4:
        sig_name = "HCTVSerNoNr4"
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

    class HCTVSerNoNr1:
        sig_name = "HCTVSerNoNr1"
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


class BCTVLCUR_LIN1Fr02:
    msg_name = "BCTVLCUR_LIN1Fr02"
    msg_id = 4
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'BCTVSerNo': ['BCTVSerNoNr1', 'BCTVSerNoNr2', 'BCTVSerNoNr3', 'BCTVSerNoNr4']}
    sig_group_dataid_dict = {}

    class BCTVSerNoNr3:
        sig_name = "BCTVSerNoNr3"
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

    class BCTVSerNoNr4:
        sig_name = "BCTVSerNoNr4"
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

    class BCTVSerNoNr1:
        sig_name = "BCTVSerNoNr1"
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

    class BCTVSerNoNr2:
        sig_name = "BCTVSerNoNr2"
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


class CCTVLCUR_LIN1Fr01:
    msg_name = "CCTVLCUR_LIN1Fr01"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "CCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'CCTVPartNo': ['CCTVPartNoEndSgn1', 'CCTVPartNoEndSgn2', 'CCTVPartNoEndSgn3', 'CCTVPartNoNr1', 'CCTVPartNoNr2', 'CCTVPartNoNr3', 'CCTVPartNoNr4', 'CCTVPartNoNr5']}
    sig_group_dataid_dict = {}

    class CCTVPartNoNr3:
        sig_name = "CCTVPartNoNr3"
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

    class CCTVPartNoNr4:
        sig_name = "CCTVPartNoNr4"
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

    class CCTVPartNoEndSgn3:
        sig_name = "CCTVPartNoEndSgn3"
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

    class CCTVPartNoEndSgn2:
        sig_name = "CCTVPartNoEndSgn2"
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

    class CCTVPartNoEndSgn1:
        sig_name = "CCTVPartNoEndSgn1"
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

    class CCTVPartNoNr5:
        sig_name = "CCTVPartNoNr5"
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

    class CCTVPartNoNr1:
        sig_name = "CCTVPartNoNr1"
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

    class CCTVPartNoNr2:
        sig_name = "CCTVPartNoNr2"
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


class BCFVLCUR_LIN1Fr03:
    msg_name = "BCFVLCUR_LIN1Fr03"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BCFV"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BCFVSpdLvl:
        sig_name = "BCFVSpdLvl"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpeedLvl_SpeedLevelLow': 0, 'SpeedLvl_SpeedLevelNormal': 1, 'SpeedLvl_SpeedLevelFast': 2, 'SpeedLvl_SNA': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BCFVFltSts:
        sig_name = "BCFVFltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaultSts_NoError': 0, 'FaultSts_PositionUnknown': 1, 'FaultSts_PCTR_Error': 2, 'FaultSts_Blocking_Err': 3, 'FaultSts_SetPoint_Err': 4, 'FaultSts_Learning_Err': 5, 'FaultSts_MotorCoilShort': 6, 'FaultSts_MotorCoilOpen': 7, 'FaultSts_MotorDrvOvertemperatureShutdown': 8, 'FaultSts_Indeterminate': 9, 'FaultSts_Reserved': 10, 'FaultSts_SNA': 15}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BCFVMod:
        sig_name = "BCFVMod"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvMode_NormalOperation': 0, 'VlvMode_Mot_Off': 1, 'VlvMode_Learning': 2, 'VlvMode_Fail_Safe': 3, 'VlvMode_SNA': 15}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class BCFVRunSts:
        sig_name = "BCFVRunSts"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BCFVVoltSts:
        sig_name = "BCFVVoltSts"
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
        sig_value_table = {'VoltSts_VoltageOK': 0, 'VoltSts_OverVoltage': 1, 'VoltSts_UnderVoltage': 2, 'VoltSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BCFVPosnAct:
        sig_name = "BCFVPosnAct"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b00000011, 0b11111100, 2, 0)]

    class BCFVNVMFlt:
        sig_name = "BCFVNVMFlt"
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

    class BCFVTempSts:
        sig_name = "BCFVTempSts"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempSts_Temperatureok': 0, 'TempSts_OvertemperatureWarning': 1, 'TempSts_PCBOvertemperature': 2, 'TempSts_LowTemperature': 3, 'TempSts_notused': 4, 'TempSts_SNA': 7}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CCTVLCUR_LIN1Fr03:
    msg_name = "CCTVLCUR_LIN1Fr03"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "CCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CCTVNVMFlt:
        sig_name = "CCTVNVMFlt"
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

    class CCTVRunSts:
        sig_name = "CCTVRunSts"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CCTVFltSts:
        sig_name = "CCTVFltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaultSts_NoError': 0, 'FaultSts_PositionUnknown': 1, 'FaultSts_PCTR_Error': 2, 'FaultSts_Blocking_Err': 3, 'FaultSts_SetPoint_Err': 4, 'FaultSts_Learning_Err': 5, 'FaultSts_MotorCoilShort': 6, 'FaultSts_MotorCoilOpen': 7, 'FaultSts_MotorDrvOvertemperatureShutdown': 8, 'FaultSts_Indeterminate': 9, 'FaultSts_Reserved': 10, 'FaultSts_SNA': 15}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CCTVVoltSts:
        sig_name = "CCTVVoltSts"
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
        sig_value_table = {'VoltSts_VoltageOK': 0, 'VoltSts_OverVoltage': 1, 'VoltSts_UnderVoltage': 2, 'VoltSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CCTVMod:
        sig_name = "CCTVMod"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvMode_NormalOperation': 0, 'VlvMode_Mot_Off': 1, 'VlvMode_Learning': 2, 'VlvMode_Fail_Safe': 3, 'VlvMode_SNA': 15}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CCTVSpdLvl:
        sig_name = "CCTVSpdLvl"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpeedLvl_SpeedLevelLow': 0, 'SpeedLvl_SpeedLevelNormal': 1, 'SpeedLvl_SpeedLevelFast': 2, 'SpeedLvl_SNA': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CCTVTempSts:
        sig_name = "CCTVTempSts"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempSts_Temperatureok': 0, 'TempSts_OvertemperatureWarning': 1, 'TempSts_PCBOvertemperature': 2, 'TempSts_LowTemperature': 3, 'TempSts_notused': 4, 'TempSts_SNA': 7}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CCTVPosnAct:
        sig_name = "CCTVPosnAct"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b00000011, 0b11111100, 2, 0)]


class HCTVLCUR_LIN1Fr01:
    msg_name = "HCTVLCUR_LIN1Fr01"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "HCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'HCTVPartNo': ['HCTVPartNoEndSgn1', 'HCTVPartNoEndSgn2', 'HCTVPartNoEndSgn3', 'HCTVPartNoNr1', 'HCTVPartNoNr2', 'HCTVPartNoNr3', 'HCTVPartNoNr4', 'HCTVPartNoNr5']}
    sig_group_dataid_dict = {}

    class HCTVPartNoNr2:
        sig_name = "HCTVPartNoNr2"
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

    class HCTVPartNoEndSgn1:
        sig_name = "HCTVPartNoEndSgn1"
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

    class HCTVPartNoEndSgn2:
        sig_name = "HCTVPartNoEndSgn2"
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

    class HCTVPartNoEndSgn3:
        sig_name = "HCTVPartNoEndSgn3"
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

    class HCTVPartNoNr3:
        sig_name = "HCTVPartNoNr3"
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

    class HCTVPartNoNr1:
        sig_name = "HCTVPartNoNr1"
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

    class HCTVPartNoNr4:
        sig_name = "HCTVPartNoNr4"
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

    class HCTVPartNoNr5:
        sig_name = "HCTVPartNoNr5"
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


class BCFVLCUR_LIN1Fr02:
    msg_name = "BCFVLCUR_LIN1Fr02"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BCFV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'BCFVSerNo': ['BCFVSerNoNr1', 'BCFVSerNoNr2', 'BCFVSerNoNr3', 'BCFVSerNoNr4']}
    sig_group_dataid_dict = {}

    class BCFVSerNoNr4:
        sig_name = "BCFVSerNoNr4"
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

    class BCFVSerNoNr2:
        sig_name = "BCFVSerNoNr2"
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

    class BCFVSerNoNr1:
        sig_name = "BCFVSerNoNr1"
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

    class BCFVSerNoNr3:
        sig_name = "BCFVSerNoNr3"
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


class BCTVLCUR_LIN1Fr03:
    msg_name = "BCTVLCUR_LIN1Fr03"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BCTVRunSts:
        sig_name = "BCTVRunSts"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BCTVMod:
        sig_name = "BCTVMod"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvMode_NormalOperation': 0, 'VlvMode_Mot_Off': 1, 'VlvMode_Learning': 2, 'VlvMode_Fail_Safe': 3, 'VlvMode_SNA': 15}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class BCTVFltSts:
        sig_name = "BCTVFltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaultSts_NoError': 0, 'FaultSts_PositionUnknown': 1, 'FaultSts_PCTR_Error': 2, 'FaultSts_Blocking_Err': 3, 'FaultSts_SetPoint_Err': 4, 'FaultSts_Learning_Err': 5, 'FaultSts_MotorCoilShort': 6, 'FaultSts_MotorCoilOpen': 7, 'FaultSts_MotorDrvOvertemperatureShutdown': 8, 'FaultSts_Indeterminate': 9, 'FaultSts_Reserved': 10, 'FaultSts_SNA': 15}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BCTVSpdLvl:
        sig_name = "BCTVSpdLvl"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpeedLvl_SpeedLevelLow': 0, 'SpeedLvl_SpeedLevelNormal': 1, 'SpeedLvl_SpeedLevelFast': 2, 'SpeedLvl_SNA': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class BCTVTempSts:
        sig_name = "BCTVTempSts"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempSts_Temperatureok': 0, 'TempSts_OvertemperatureWarning': 1, 'TempSts_PCBOvertemperature': 2, 'TempSts_LowTemperature': 3, 'TempSts_notused': 4, 'TempSts_SNA': 7}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BCTVNVMFlt:
        sig_name = "BCTVNVMFlt"
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

    class BCTVVoltSts:
        sig_name = "BCTVVoltSts"
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
        sig_value_table = {'VoltSts_VoltageOK': 0, 'VoltSts_OverVoltage': 1, 'VoltSts_UnderVoltage': 2, 'VoltSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BCTVPosnAct:
        sig_name = "BCTVPosnAct"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b00000011, 0b11111100, 2, 0)]


class ECTVLCUR_LIN1Fr03:
    msg_name = "ECTVLCUR_LIN1Fr03"
    msg_id = 14
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "ECTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ECTVVoltSts:
        sig_name = "ECTVVoltSts"
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
        sig_value_table = {'VoltSts_VoltageOK': 0, 'VoltSts_OverVoltage': 1, 'VoltSts_UnderVoltage': 2, 'VoltSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ECTVFltSts:
        sig_name = "ECTVFltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaultSts_NoError': 0, 'FaultSts_PositionUnknown': 1, 'FaultSts_PCTR_Error': 2, 'FaultSts_Blocking_Err': 3, 'FaultSts_SetPoint_Err': 4, 'FaultSts_Learning_Err': 5, 'FaultSts_MotorCoilShort': 6, 'FaultSts_MotorCoilOpen': 7, 'FaultSts_MotorDrvOvertemperatureShutdown': 8, 'FaultSts_Indeterminate': 9, 'FaultSts_Reserved': 10, 'FaultSts_SNA': 15}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ECTVNVMFlt:
        sig_name = "ECTVNVMFlt"
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

    class ECTVPosnAct:
        sig_name = "ECTVPosnAct"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b00000011, 0b11111100, 2, 0)]

    class ECTVSpdLvl:
        sig_name = "ECTVSpdLvl"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpeedLvl_SpeedLevelLow': 0, 'SpeedLvl_SpeedLevelNormal': 1, 'SpeedLvl_SpeedLevelFast': 2, 'SpeedLvl_SNA': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ECTVMod:
        sig_name = "ECTVMod"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvMode_NormalOperation': 0, 'VlvMode_Mot_Off': 1, 'VlvMode_Learning': 2, 'VlvMode_Fail_Safe': 3, 'VlvMode_SNA': 15}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ECTVTempSts:
        sig_name = "ECTVTempSts"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempSts_Temperatureok': 0, 'TempSts_OvertemperatureWarning': 1, 'TempSts_PCBOvertemperature': 2, 'TempSts_LowTemperature': 3, 'TempSts_notused': 4, 'TempSts_SNA': 7}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ECTVRunSts:
        sig_name = "ECTVRunSts"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class LCTVLCUR_LIN1Fr01:
    msg_name = "LCTVLCUR_LIN1Fr01"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LCTVPartNo': ['LCTVPartNoEndSgn1', 'LCTVPartNoEndSgn2', 'LCTVPartNoEndSgn3', 'LCTVPartNoNr1', 'LCTVPartNoNr2', 'LCTVPartNoNr3', 'LCTVPartNoNr4', 'LCTVPartNoNr5']}
    sig_group_dataid_dict = {}

    class LCTVPartNoNr3:
        sig_name = "LCTVPartNoNr3"
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

    class LCTVPartNoEndSgn2:
        sig_name = "LCTVPartNoEndSgn2"
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

    class LCTVPartNoEndSgn3:
        sig_name = "LCTVPartNoEndSgn3"
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

    class LCTVPartNoNr2:
        sig_name = "LCTVPartNoNr2"
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

    class LCTVPartNoNr1:
        sig_name = "LCTVPartNoNr1"
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

    class LCTVPartNoEndSgn1:
        sig_name = "LCTVPartNoEndSgn1"
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

    class LCTVPartNoNr4:
        sig_name = "LCTVPartNoNr4"
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

    class LCTVPartNoNr5:
        sig_name = "LCTVPartNoNr5"
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


class DCTVLCUR_LIN1Fr03:
    msg_name = "DCTVLCUR_LIN1Fr03"
    msg_id = 11
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "DCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DCTVVoltSts:
        sig_name = "DCTVVoltSts"
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
        sig_value_table = {'VoltSts_VoltageOK': 0, 'VoltSts_OverVoltage': 1, 'VoltSts_UnderVoltage': 2, 'VoltSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DCTVSpdLvl:
        sig_name = "DCTVSpdLvl"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SpeedLvl_SpeedLevelLow': 0, 'SpeedLvl_SpeedLevelNormal': 1, 'SpeedLvl_SpeedLevelFast': 2, 'SpeedLvl_SNA': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DCTVMod:
        sig_name = "DCTVMod"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvMode_NormalOperation': 0, 'VlvMode_Mot_Off': 1, 'VlvMode_Learning': 2, 'VlvMode_Fail_Safe': 3, 'VlvMode_SNA': 15}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DCTVFltSts:
        sig_name = "DCTVFltSts"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaultSts_NoError': 0, 'FaultSts_PositionUnknown': 1, 'FaultSts_PCTR_Error': 2, 'FaultSts_Blocking_Err': 3, 'FaultSts_SetPoint_Err': 4, 'FaultSts_Learning_Err': 5, 'FaultSts_MotorCoilShort': 6, 'FaultSts_MotorCoilOpen': 7, 'FaultSts_MotorDrvOvertemperatureShutdown': 8, 'FaultSts_Indeterminate': 9, 'FaultSts_Reserved': 10, 'FaultSts_SNA': 15}
        compute_method = None
        length = 4
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DCTVTempSts:
        sig_name = "DCTVTempSts"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempSts_Temperatureok': 0, 'TempSts_OvertemperatureWarning': 1, 'TempSts_PCBOvertemperature': 2, 'TempSts_LowTemperature': 3, 'TempSts_notused': 4, 'TempSts_SNA': 7}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DCTVPosnAct:
        sig_name = "DCTVPosnAct"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 8
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b00000011, 0b11111100, 2, 0)]

    class DCTVNVMFlt:
        sig_name = "DCTVNVMFlt"
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

    class DCTVRunSts:
        sig_name = "DCTVRunSts"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class LCTVLCUR_LIN1Fr02:
    msg_name = "LCTVLCUR_LIN1Fr02"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "LCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'LCTVSerNo': ['LCTVSerNoNr1', 'LCTVSerNoNr2', 'LCTVSerNoNr3', 'LCTVSerNoNr4']}
    sig_group_dataid_dict = {}

    class LCTVSerNoNr4:
        sig_name = "LCTVSerNoNr4"
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

    class LCTVSerNoNr3:
        sig_name = "LCTVSerNoNr3"
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

    class LCTVSerNoNr1:
        sig_name = "LCTVSerNoNr1"
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

    class LCTVSerNoNr2:
        sig_name = "LCTVSerNoNr2"
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


class DCTVLCUR_LIN1Fr01:
    msg_name = "DCTVLCUR_LIN1Fr01"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "DCTV"
    rx_nodes = ['LCUR']
    sig_group_dict = {'DCTVPartNo': ['DCTVPartNoEndSgn1', 'DCTVPartNoEndSgn2', 'DCTVPartNoEndSgn3', 'DCTVPartNoNr1', 'DCTVPartNoNr2', 'DCTVPartNoNr3', 'DCTVPartNoNr4', 'DCTVPartNoNr5']}
    sig_group_dataid_dict = {}

    class DCTVPartNoNr4:
        sig_name = "DCTVPartNoNr4"
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

    class DCTVPartNoNr3:
        sig_name = "DCTVPartNoNr3"
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

    class DCTVPartNoNr5:
        sig_name = "DCTVPartNoNr5"
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

    class DCTVPartNoNr1:
        sig_name = "DCTVPartNoNr1"
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

    class DCTVPartNoEndSgn2:
        sig_name = "DCTVPartNoEndSgn2"
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

    class DCTVPartNoEndSgn1:
        sig_name = "DCTVPartNoEndSgn1"
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

    class DCTVPartNoEndSgn3:
        sig_name = "DCTVPartNoEndSgn3"
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

    class DCTVPartNoNr2:
        sig_name = "DCTVPartNoNr2"
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


