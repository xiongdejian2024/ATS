class AswmCem_Lin4Fr02:
    msg_name = "AswmCem_Lin4Fr02"
    msg_id = 26
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class SteerWhlPosnX:
        sig_name = "SteerWhlPosnX"
        sig_start_bit = 12
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = "-204.8"
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Intel"
        sig_value_init = 2048
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 12
        bmuws_info = [(1, 0b11110000, 0b00001111, 4, 4), (2, 0b11111111, 0b00000000, 8, 0)]

    class SteerWhlDownLdSts:
        sig_name = "SteerWhlDownLdSts"
        sig_start_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SteerWhlBtnPsd:
        sig_name = "SteerWhlBtnPsd"
        sig_start_bit = 28
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

    class SteerWhlPosnAng:
        sig_name = "SteerWhlPosnAng"
        sig_start_bit = 0
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = "-20.48"
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Intel"
        sig_value_init = 2048
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]

    class SteerWhlMemSts:
        sig_name = "SteerWhlMemSts"
        sig_start_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class CemCem_Lin4Fr06:
    msg_name = "CemCem_Lin4Fr06"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class SteerWhlPosnFromCldSteerWhlPosnX:
        sig_name = "SteerWhlPosnFromCldSteerWhlPosnX"
        sig_start_bit = 40
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = "-204.8"
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Intel"
        sig_value_init = 2048
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 40
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class AmbTIndcdWithUnitQF:
        sig_name = "AmbTIndcdWithUnitQF"
        sig_start_bit = 14
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
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlPosnFromCldSteerWhlPosnAng:
        sig_name = "SteerWhlPosnFromCldSteerWhlPosnAng"
        sig_start_bit = 28
        sig_length = 12
        sig_value_factor = 0.01
        sig_value_offset = "-20.48"
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Intel"
        sig_value_init = 2048
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 28
        bmuws_info = [(3, 0b11110000, 0b00001111, 4, 4), (4, 0b11111111, 0b00000000, 8, 0)]

    class SteerAdjSwtFwdSts:
        sig_name = "SteerAdjSwtFwdSts"
        sig_start_bit = 26
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

    class SteerAdjSwtDwnSts:
        sig_name = "SteerAdjSwtDwnSts"
        sig_start_bit = 25
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

    class AmbTIndcdWithUnitAmbTIndcd:
        sig_name = "AmbTIndcdWithUnitAmbTIndcd"
        sig_start_bit = 0
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = "-100.0"
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Intel"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]

    class SteerAdjSwtUpSts:
        sig_name = "SteerAdjSwtUpSts"
        sig_start_bit = 27
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

    class AmbTIndcdWithUnitAmbTIndcdUnit:
        sig_name = "AmbTIndcdWithUnitAmbTIndcdUnit"
        sig_start_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AmbTIndcdUnit_Celsius': 0, 'AmbTIndcdUnit_Fahrenheit': 1, 'AmbTIndcdUnit_UkwnUnit': 2}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerAdjSwtBackSts:
        sig_name = "SteerAdjSwtBackSts"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class DiagRequest3:
    msg_name = "DiagRequest3"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']


class SwmCem_Lin4Fr05:
    msg_name = "SwmCem_Lin4Fr05"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class SwtExtrLi2LiExtFctReq1:
        sig_name = "SwtExtrLi2LiExtFctReq1"
        sig_start_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LiExtFctReq1_Off': 0, 'LiExtFctReq1_Pos': 1, 'LiExtFctReq1_Lo': 2, 'LiExtFctReq1_AutLi': 3}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FrntWiprLvrCmd2FrntWiprLvrCmd1:
        sig_name = "FrntWiprLvrCmd2FrntWiprLvrCmd1"
        sig_start_bit = 8
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FrntWiprLvrCmd1_FrntWiprOff': 0, 'FrntWiprLvrCmd1_FrntWiprSngStk': 1, 'FrntWiprLvrCmd1_FrntWiprIntm': 2, 'FrntWiprLvrCmd1_FrntWiprContnsLoSpd': 3, 'FrntWiprLvrCmd1_FrntWiprContnsHiSpd': 4}
        compute_method = None
        length = 3
        startbit = 8
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class SwtExtrLi2LiExtFctCntr:
        sig_name = "SwtExtrLi2LiExtFctCntr"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FrntWiprLvrCmd2FrntWiprLvrQf:
        sig_name = "FrntWiprLvrCmd2FrntWiprLvrQf"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class FrntWiprLvrCmd2FrntWiprLvrCrc:
        sig_name = "FrntWiprLvrCmd2FrntWiprLvrCrc"
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

    class FrntWiprLvrCmd2FrntWiprLvrCntr:
        sig_name = "FrntWiprLvrCmd2FrntWiprLvrCntr"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class SwtExtrLi2LiExtFctCrc:
        sig_name = "SwtExtrLi2LiExtFctCrc"
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

    class SwtExtrLi2LiExtFctQf:
        sig_name = "SwtExtrLi2LiExtFctQf"
        sig_start_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class AswmCem_Lin4PartNrFr08:
    msg_name = "AswmCem_Lin4PartNrFr08"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class ASWMPartNoCmplEndSgn2:
        sig_name = "ASWMPartNoCmplEndSgn2"
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

    class ASWMPartNoCmplEndSgn1:
        sig_name = "ASWMPartNoCmplEndSgn1"
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

    class ASWMPartNoCmplNr2:
        sig_name = "ASWMPartNoCmplNr2"
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

    class ASWMPartNoCmplEndSgn3:
        sig_name = "ASWMPartNoCmplEndSgn3"
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

    class ASWMPartNoCmplNr4:
        sig_name = "ASWMPartNoCmplNr4"
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

    class ASWMPartNoCmplNr3:
        sig_name = "ASWMPartNoCmplNr3"
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

    class ASWMPartNoCmplNr1:
        sig_name = "ASWMPartNoCmplNr1"
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


class DiagResponse3:
    msg_name = "DiagResponse3"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']


class SwmCem_Lin4Fr02:
    msg_name = "SwmCem_Lin4Fr02"
    msg_id = 44
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class SwtBeamHi:
        sig_name = "SwtBeamHi"
        sig_start_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BeamHiFctReq1_Neut': 0, 'BeamHiFctReq1_Flash': 1, 'BeamHiFctReq1_HiBeam': 2, 'BeamHiFctReq1_LoBeam': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WinWshrLvrCmd:
        sig_name = "WinWshrLvrCmd"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinWshrLvrCmd1_WinWshrOff': 0, 'WinWshrLvrCmd1_FrntWshrCmd': 1, 'WinWshrLvrCmd1_ReWshrCmd': 2}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class SwtAhbcReq:
        sig_name = "SwtAhbcReq"
        sig_start_bit = 3
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RainSnsCmd:
        sig_name = "RainSnsCmd"
        sig_start_bit = 23
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RainSnsrCmd1_RainSnsrBtnNotPush': 0, 'RainSnsrCmd1_RainSnsrBtnPush': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WiprLvrDiagc:
        sig_name = "WiprLvrDiagc"
        sig_start_bit = 14
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WiprLvrDiagcTyp_WiprLvrNotConnect': 0, 'WiprLvrDiagcTyp_WiprLvrBtnStuck': 1, 'WiprLvrDiagcTyp_WiprLvrSwtundefd': 2, 'WiprLvrDiagcTyp_WiprLvrOk': 3}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SwtIntmIntlCmd:
        sig_name = "SwtIntmIntlCmd"
        sig_start_bit = 28
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 4
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgSpdIntlFromHmi_Posn0': 0, 'WipgSpdIntlFromHmi_Posn1': 1, 'WipgSpdIntlFromHmi_Posn2': 2, 'WipgSpdIntlFromHmi_Posn3': 3, 'WipgSpdIntlFromHmi_Posn4': 4, 'WipgSpdIntlFromHmi_Posn5': 5, 'WipgSpdIntlFromHmi_Posn6': 6, 'WipgSpdIntlFromHmi_Posn7': 7}
        compute_method = None
        length = 3
        startbit = 28
        byte = 3
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class ReWiprRotyCmd:
        sig_name = "ReWiprRotyCmd"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReWiprRotyCmd2_ReWiprRotyOff': 0, 'ReWiprRotyCmd2_ReWiprRotyResd': 1, 'ReWiprRotyCmd2_ReWiprRotyIntm': 2, 'ReWiprRotyCmd2_ReWiprRotyContns': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class CemCem_Lin4Fr02:
    msg_name = "CemCem_Lin4Fr02"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class LoadAndStoreReqErgoPosn:
        sig_name = "LoadAndStoreReqErgoPosn"
        sig_start_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MemPosn_ProfPosn': 0, 'MemPosn_MemBnk1': 1, 'MemPosn_MemBnk2': 2, 'MemPosn_MemBnk3': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadAndStoreReqInOutEasy:
        sig_name = "LoadAndStoreReqInOutEasy"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DisAdjMov:
        sig_name = "DisAdjMov"
        sig_start_bit = 29
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Inhb1_NotInhb': 0, 'Inhb1_Inhb': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class LoadAndStoreReqErgoSetgEve:
        sig_name = "LoadAndStoreReqErgoSetgEve"
        sig_start_bit = 21
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EveMemPosn_Idle': 0, 'EveMemPosn_Store': 1, 'EveMemPosn_Load': 2, 'EveMemPosn_Stop': 3, 'EveMemPosn_AutMovmt': 4, 'EveMemPosn_Upload': 5, 'EveMemPosn_Download': 6, 'EveMemPosn_Clear': 7}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class LoadAndStoreReqIdPen:
        sig_name = "LoadAndStoreReqIdPen"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RlyPwrDistbnCmd1WdPreBattSaveCmd:
        sig_name = "RlyPwrDistbnCmd1WdPreBattSaveCmd"
        sig_start_bit = 28
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
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SaveSetgToMemPrmnt:
        sig_name = "SaveSetgToMemPrmnt"
        sig_start_bit = 30
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnAut1_Off': 0, 'OffOnAut1_On': 1, 'OffOnAut1_Aut': 2}
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class AswmCem_Lin4SerNrFr01:
    msg_name = "AswmCem_Lin4SerNrFr01"
    msg_id = 33
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class ASWMSerNoNr4:
        sig_name = "ASWMSerNoNr4"
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

    class ASWMSerNoNr1:
        sig_name = "ASWMSerNoNr1"
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

    class ASWMSerNoNr2:
        sig_name = "ASWMSerNoNr2"
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

    class ASWMSerNoNr3:
        sig_name = "ASWMSerNoNr3"
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


class HodDim_Lin1PartNrFr02:
    msg_name = "HodDim_Lin1PartNrFr02"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class HODPartNo10CmplEndSgn2:
        sig_name = "HODPartNo10CmplEndSgn2"
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

    class HODPartNo10CmplNr5:
        sig_name = "HODPartNo10CmplNr5"
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

    class HODPartNo10CmplNr3:
        sig_name = "HODPartNo10CmplNr3"
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

    class HODPartNo10CmplNr4:
        sig_name = "HODPartNo10CmplNr4"
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

    class HODPartNo10CmplEndSgn3:
        sig_name = "HODPartNo10CmplEndSgn3"
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

    class HODPartNo10CmplNr2:
        sig_name = "HODPartNo10CmplNr2"
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

    class HODPartNo10CmplEndSgn1:
        sig_name = "HODPartNo10CmplEndSgn1"
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

    class HODPartNo10CmplNr1:
        sig_name = "HODPartNo10CmplNr1"
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


class AswmCem_Lin4PartNrFr05:
    msg_name = "AswmCem_Lin4PartNrFr05"
    msg_id = 47
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class ASWMPartNo10CmplNr3:
        sig_name = "ASWMPartNo10CmplNr3"
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

    class ASWMPartNo10CmplEndSgn2:
        sig_name = "ASWMPartNo10CmplEndSgn2"
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

    class ASWMPartNo10CmplEndSgn1:
        sig_name = "ASWMPartNo10CmplEndSgn1"
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

    class ASWMPartNo10CmplNr1:
        sig_name = "ASWMPartNo10CmplNr1"
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

    class ASWMPartNo10CmplNr4:
        sig_name = "ASWMPartNo10CmplNr4"
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

    class ASWMPartNo10CmplEndSgn3:
        sig_name = "ASWMPartNo10CmplEndSgn3"
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

    class ASWMPartNo10CmplNr5:
        sig_name = "ASWMPartNo10CmplNr5"
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

    class ASWMPartNo10CmplNr2:
        sig_name = "ASWMPartNo10CmplNr2"
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


class AswmCem_Lin4Fr01:
    msg_name = "AswmCem_Lin4Fr01"
    msg_id = 28
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class WhlFailrSts:
        sig_name = "WhlFailrSts"
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

    class SteerWhlInMovmt:
        sig_name = "SteerWhlInMovmt"
        sig_start_bit = 32
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


class HodDim_Lin1PartNrFr03:
    msg_name = "HodDim_Lin1PartNrFr03"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class HODPartNoCmplEndSgn2:
        sig_name = "HODPartNoCmplEndSgn2"
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

    class HODPartNoCmplEndSgn3:
        sig_name = "HODPartNoCmplEndSgn3"
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

    class HODPartNoCmplNr3:
        sig_name = "HODPartNoCmplNr3"
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

    class HODPartNoCmplNr1:
        sig_name = "HODPartNoCmplNr1"
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

    class HODPartNoCmplNr2:
        sig_name = "HODPartNoCmplNr2"
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

    class HODPartNoCmplNr4:
        sig_name = "HODPartNoCmplNr4"
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

    class HODPartNoCmplEndSgn1:
        sig_name = "HODPartNoCmplEndSgn1"
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


class HodDim_Lin1SerNrFr01:
    msg_name = "HodDim_Lin1SerNrFr01"
    msg_id = 22
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class HODSerNoNr4:
        sig_name = "HODSerNoNr4"
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

    class HODSerNoNr1:
        sig_name = "HODSerNoNr1"
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

    class HODSerNoNr2:
        sig_name = "HODSerNoNr2"
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

    class HODSerNoNr3:
        sig_name = "HODSerNoNr3"
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


class HodDim_Lin1Fr04:
    msg_name = "HodDim_Lin1Fr04"
    msg_id = 24
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class HandsOnDetectionHandsOnStatus_0_HodDim_Lin1Fr04:
        sig_name = "HandsOnDetectionHandsOnStatus_0_HodDim_Lin1Fr04"
        sig_start_bit = 6
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Init_Class': 0, 'Hands_ON': 1, 'Hands_OFF': 2, 'Undetermined_Class': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HandsOnDetectionErrorStatus_0_HodDim_Lin1Fr04:
        sig_name = "HandsOnDetectionErrorStatus_0_HodDim_Lin1Fr04"
        sig_start_bit = 9
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ErrorSts_Init_Diag': 0, 'ErrorSts_Reserved1': 1, 'ErrorSts_HOSWD_Ready': 2, 'ErrorSts_HOSWD_CUFault': 3, 'ErrorSts_HOSWD_SMFault': 4, 'ErrorSts_HOSWD_SVFault': 5, 'ErrorSts_Reserved2': 6, 'ErrorSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 9
        byte = 1
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class HandsOnDetectionCntr_0_HodDim_Lin1Fr04:
        sig_name = "HandsOnDetectionCntr_0_HodDim_Lin1Fr04"
        sig_start_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HandsOnDetectionChks_0_HodDim_Lin1Fr04:
        sig_name = "HandsOnDetectionChks_0_HodDim_Lin1Fr04"
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


class SwmCem_Lin4Fr01:
    msg_name = "SwmCem_Lin4Fr01"
    msg_id = 36
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 2
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class SwtIndcrIndcrTypExtReqToUpdQf_0_SwmCem_Lin4SignalIPdu01:
        sig_name = "SwtIndcrIndcrTypExtReqToUpdQf_0_SwmCem_Lin4SignalIPdu01"
        sig_start_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SwtIndcrIndcrTypExtReq_0_SwmCem_Lin4SignalIPdu01:
        sig_name = "SwtIndcrIndcrTypExtReq_0_SwmCem_Lin4SignalIPdu01"
        sig_start_bit = 8
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IndcrTypExt1_Off': 0, 'IndcrTypExt1_Le': 1, 'IndcrTypExt1_Ri': 2}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SwtIndcrIndcrTypExtReqCntr_0_SwmCem_Lin4SignalIPdu01:
        sig_name = "SwtIndcrIndcrTypExtReqCntr_0_SwmCem_Lin4SignalIPdu01"
        sig_start_bit = 10
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
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SwtIndcrIndcrTypExtReqChks_0_SwmCem_Lin4SignalIPdu01:
        sig_name = "SwtIndcrIndcrTypExtReqChks_0_SwmCem_Lin4SignalIPdu01"
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


