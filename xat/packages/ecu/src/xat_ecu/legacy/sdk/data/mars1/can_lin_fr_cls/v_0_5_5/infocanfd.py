class BgmInfoCanFdFr18:
    msg_name = "BgmInfoCanFdFr18"
    msg_id = 528
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC']

    class CarTiGlb_4_BgmInfoCanFdSignalIPdu18:
        sig_name = "CarTiGlb_4_BgmInfoCanFdSignalIPdu18"
        sig_start_bit = 39
        update_id_bit = 13
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class CdcInfoCANFDNmFr:
    msg_name = "CdcInfoCANFDNmFr"
    msg_id = 1282
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']


class BgmInfoCANFDNmFr:
    msg_name = "BgmInfoCANFDNmFr"
    msg_id = 1281
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC']


class BgmInfoCanFdFr19:
    msg_name = "BgmInfoCanFdFr19"
    msg_id = 789
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC']

    class VehTiAndDataSec1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataSec1_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 5
        byte = 0
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class VehTiAndDataYr1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataYr1_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 46
        byte = 5
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class VehTiAndDataMth1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataMth1_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehTiAndDataHr1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataHr1_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 20
        byte = 2
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class VehTiAndDataMins1_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataMins1_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 13
        byte = 1
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class VehTiAndDataDay_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataDay_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 28
        byte = 3
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class VehTiAndDataDataValid_3_BgmInfoCanFdSignalIPdu19:
        sig_name = "VehTiAndDataDataValid_3_BgmInfoCanFdSignalIPdu19"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class BgmInfoCanFdFr17:
    msg_name = "BgmInfoCanFdFr17"
    msg_id = 800
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['S2SReceiver', 'CDC']

    class WhlSpdCmpFac_1_BgmInfoCanFdSignalIPdu17:
        sig_name = "WhlSpdCmpFac_1_BgmInfoCanFdSignalIPdu17"
        sig_start_bit = 47
        update_id_bit = 50
        sig_length = 5
        sig_value_factor = 0.005
        sig_value_offset = 0.92
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Motorola"
        sig_value_init = 16
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 47
        byte = 5
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class IndirectLifeDetnAndCareLvl1Warn:
        sig_name = "IndirectLifeDetnAndCareLvl1Warn"
        sig_start_bit = 28
        update_id_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class IndirectLifeDetnAndCareDiWarn:
        sig_name = "IndirectLifeDetnAndCareDiWarn"
        sig_start_bit = 29
        update_id_bit = 55
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class CdcInfoCanFdFr04:
    msg_name = "CdcInfoCanFdFr04"
    msg_id = 256
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']

    class FaceIdnStsMsg:
        sig_name = "FaceIdnStsMsg"
        sig_start_bit = 2
        update_id_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaceIdnStsMsg_unavailable': 0, 'FaceIdnStsMsg_notDetected': 1, 'FaceIdnStsMsg_detectedButNotRecognized': 2, 'FaceIdnStsMsg_detectedAndRecognized': 3}
        compute_method = None
        length = 2
        startbit = 2
        byte = 0
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class AsySftyHWLReqBkp:
        sig_name = "AsySftyHWLReqBkp"
        sig_start_bit = 39
        update_id_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AsySftyHWLReq_NoRequest': 0, 'AsySftyHWLReq_TurnOn': 1, 'AsySftyHWLReq_TurnOff': 2, 'AsySftyHWLReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FaceIdnResForProfIdPen:
        sig_name = "FaceIdnResForProfIdPen"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class OutsidePrkOutReq_0_CdcInfoCanFdSignalIPdu04:
        sig_name = "OutsidePrkOutReq_0_CdcInfoCanFdSignalIPdu04"
        sig_start_bit = 23
        update_id_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FaceIdnResForProfYesNo:
        sig_name = "FaceIdnResForProfYesNo"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo2_No': 0, 'YesNo2_Yes': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class CdcInfoCanFdFr03:
    msg_name = "CdcInfoCanFdFr03"
    msg_id = 768
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['BGM']

    class MmedHdPwrMod:
        sig_name = "MmedHdPwrMod"
        sig_start_bit = 39
        update_id_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MmedMaiPwrMod_IHUStateSleep': 0, 'MmedMaiPwrMod_IHUStateStandby': 1, 'MmedMaiPwrMod_IHUStatePartial': 2, 'MmedMaiPwrMod_IHUStateOn': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BgmInfoCanFdFr20:
    msg_name = "BgmInfoCanFdFr20"
    msg_id = 821
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 32
    tx_node = "BGM"
    rx_nodes = ['CDC']

    class FrntLeOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntLeOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 27
        update_id_bit = 122
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ReRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 99
        update_id_bit = 147
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 99
        byte = 12
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FrntLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 31
        update_id_bit = 123
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AudWarnLvOfSnsrParkAssiRgt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiRgt_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 1
        update_id_bit = 112
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerReqUSS_BuzzerOFF': 0, 'BuzzerReqUSS_BuzzerON_Keep': 1, 'BuzzerReqUSS_BuzzerON_2Hz': 2, 'BuzzerReqUSS_BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AudWarnLvOfSnsrParkAssiLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 5
        update_id_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerReqUSS_BuzzerOFF': 0, 'BuzzerReqUSS_BuzzerON_Keep': 1, 'BuzzerReqUSS_BuzzerON_2Hz': 2, 'BuzzerReqUSS_BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class FrntRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntRiOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 39
        update_id_bit = 121
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class InsdLeOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdLeOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 43
        update_id_bit = 134
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class OutdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 87
        update_id_bit = 139
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 87
        byte = 10
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ReLeOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReLeOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 103
        update_id_bit = 148
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 103
        byte = 12
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SnsrFltReShoSideLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltReShoSideLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 116
        update_id_bit = 158
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 116
        byte = 14
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class AudWarnOfSnsrParkAssiLePosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiLePosn_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 12
        update_id_bit = 126
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'USSWarnPosn_NoRequest': 0, 'USSWarnPosn_Region1': 1, 'USSWarnPosn_Region2': 2, 'USSWarnPosn_Region3': 3, 'USSWarnPosn_Region4': 4, 'USSWarnPosn_Reserve': 5}
        compute_method = None
        length = 3
        startbit = 12
        byte = 1
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class SnsrFltFrntShoSideRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltFrntShoSideRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 105
        update_id_bit = 144
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 105
        byte = 13
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class OutdLeOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdLeOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 67
        update_id_bit = 142
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 67
        byte = 8
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SnsrFltReShoSideRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltReShoSideRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 114
        update_id_bit = 157
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 114
        byte = 14
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class AudWarnOfSnsrParkAssiFrntPosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiFrntPosn_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 15
        update_id_bit = 127
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'USSWarnPosn_NoRequest': 0, 'USSWarnPosn_Region1': 1, 'USSWarnPosn_Region2': 2, 'USSWarnPosn_Region3': 3, 'USSWarnPosn_Region4': 4, 'USSWarnPosn_Reserve': 5}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class InsdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 59
        update_id_bit = 129
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ReLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReLeOfSideDoor_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 91
        update_id_bit = 149
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 91
        byte = 11
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SnsrFltFrntShoSideLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltFrntShoSideLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 107
        update_id_bit = 145
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 107
        byte = 13
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ReRiOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "ReRiOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 111
        update_id_bit = 146
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 111
        byte = 13
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class OutdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 81
        update_id_bit = 136
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 81
        byte = 10
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PrkgDstCtrlSts_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "PrkgDstCtrlSts_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 95
        update_id_bit = 151
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgDstCtrlSysSts_Off': 0, 'PrkgDstCtrlSysSts_Standby': 1, 'PrkgDstCtrlSysSts_FrontRearActive': 2, 'PrkgDstCtrlSysSts_FrontActive': 3, 'PrkgDstCtrlSysSts_RearActive': 4, 'PrkgDstCtrlSysSts_SystemFailure': 5, 'PrkgDstCtrlSysSts_Inhibited': 6, 'PrkgDstCtrlSysSts_Initialize': 7, 'PrkgDstCtrlSysSts_Covered': 8, 'PrkgDstCtrlSysSts_FrontActiveTrailerMode': 9, 'PrkgDstCtrlSysSts_Reserved1': 10, 'PrkgDstCtrlSysSts_Reserved2': 11, 'PrkgDstCtrlSysSts_Reserved3': 12, 'PrkgDstCtrlSysSts_Reserved4': 13, 'PrkgDstCtrlSysSts_Reserved5': 14, 'PrkgDstCtrlSysSts_Reserved6': 15}
        compute_method = None
        length = 4
        startbit = 95
        byte = 11
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class OutdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltReShoLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 83
        update_id_bit = 137
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 83
        byte = 10
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class InsdLeOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdLeOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 47
        update_id_bit = 135
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class PrkgDstCtrlWarn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "PrkgDstCtrlWarn_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 9
        update_id_bit = 150
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WarningInd_NoWarning': 0, 'WarningInd_Warning': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntRiOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "FrntRiOfSnsrOfPrkgAssiSide_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 35
        update_id_bit = 120
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AudWarnOfSnsrParkAssiRgtPosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiRgtPosn_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 20
        update_id_bit = 124
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'USSWarnPosn_NoRequest': 0, 'USSWarnPosn_Region1': 1, 'USSWarnPosn_Region2': 2, 'USSWarnPosn_Region3': 3, 'USSWarnPosn_Region4': 4, 'USSWarnPosn_Reserve': 5}
        compute_method = None
        length = 3
        startbit = 20
        byte = 2
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class OutdLeOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdLeOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 71
        update_id_bit = 143
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 71
        byte = 8
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AudWarnOfSnsrParkAssiRePosn_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnOfSnsrParkAssiRePosn_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 23
        update_id_bit = 125
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'USSWarnPosn_NoRequest': 0, 'USSWarnPosn_Region1': 1, 'USSWarnPosn_Region2': 2, 'USSWarnPosn_Region3': 3, 'USSWarnPosn_Region4': 4, 'USSWarnPosn_Reserve': 5}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class InsdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltFrntShoLe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 63
        update_id_bit = 131
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class OutdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 85
        update_id_bit = 138
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 85
        byte = 10
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class InsdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltReShoRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 57
        update_id_bit = 128
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SnsrFltOfPrkgDstCtrl_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "SnsrFltOfPrkgDstCtrl_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 119
        update_id_bit = 159
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrFltOfPrkgDstCtrl2_NoFault': 0, 'SnsrFltOfPrkgDstCtrl2_Front_USS_Fault': 1, 'SnsrFltOfPrkgDstCtrl2_Rear_USS_Fault': 2, 'SnsrFltOfPrkgDstCtrl2_Front_and_Rear_USS_Fault': 3, 'SnsrFltOfPrkgDstCtrl2_Reserve1': 4, 'SnsrFltOfPrkgDstCtrl2_Reserve2': 5, 'SnsrFltOfPrkgDstCtrl2_Reserve3': 6, 'SnsrFltOfPrkgDstCtrl2_Reserve4': 7}
        compute_method = None
        length = 3
        startbit = 119
        byte = 14
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class InsdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdSnsrFltFrntShoRi_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 61
        update_id_bit = 130
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltAddCover_NoFault': 0, 'FltAddCover_Fault': 1, 'FltAddCover_Cover': 2}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class OutdRiOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdRiOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 75
        update_id_bit = 140
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 75
        byte = 9
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class InsdRiOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdRiOfSnsrPrkgAssiRe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 51
        update_id_bit = 132
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AudWarnLvOfSnsrParkAssiFrnt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiFrnt_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 7
        update_id_bit = 8
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerReqUSS_BuzzerOFF': 0, 'BuzzerReqUSS_BuzzerON_Keep': 1, 'BuzzerReqUSS_BuzzerON_2Hz': 2, 'BuzzerReqUSS_BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class OutdRiOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "OutdRiOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 79
        update_id_bit = 141
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AudWarnLvOfSnsrParkAssiRe_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "AudWarnLvOfSnsrParkAssiRe_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 3
        update_id_bit = 16
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BuzzerReqUSS_BuzzerOFF': 0, 'BuzzerReqUSS_BuzzerON_Keep': 1, 'BuzzerReqUSS_BuzzerON_2Hz': 2, 'BuzzerReqUSS_BuzzerON_4Hz': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class InsdRiOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20:
        sig_name = "InsdRiOfSnsrPrkgAssiFrnt_1_BgmInfoCanFdSignalIPdu20"
        sig_start_bit = 55
        update_id_bit = 133
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSnsrDstInsd_NoDistance': 0, 'PrkgAssiSnsrDstInsd_Range1': 1, 'PrkgAssiSnsrDstInsd_Range2': 2, 'PrkgAssiSnsrDstInsd_Range3': 3, 'PrkgAssiSnsrDstInsd_Range4': 4, 'PrkgAssiSnsrDstInsd_Range5': 5, 'PrkgAssiSnsrDstInsd_Range6': 6, 'PrkgAssiSnsrDstInsd_Range7': 7, 'PrkgAssiSnsrDstInsd_Range8': 8, 'PrkgAssiSnsrDstInsd_Range9': 9, 'PrkgAssiSnsrDstInsd_Range10': 10, 'PrkgAssiSnsrDstInsd_Range11': 11, 'PrkgAssiSnsrDstInsd_Range12': 12, 'PrkgAssiSnsrDstInsd_Range13': 13, 'PrkgAssiSnsrDstInsd_Reserve1': 14, 'PrkgAssiSnsrDstInsd_Reserve2': 15}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


