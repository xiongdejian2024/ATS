class IhuDhuInfoCanFr09:
    msg_name = "IhuDhuInfoCanFr09"
    msg_id = 1104
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD', 'CD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CarTiGlb:
        sig_name = "CarTiGlb"
        sig_start_bit = 7
        update_id_bit = 39
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class BkpOfDstTrvld:
        sig_name = "BkpOfDstTrvld"
        sig_start_bit = 36
        update_id_bit = 38
        sig_length = 21
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 21
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]


class IhuDhuInfoCanFr03:
    msg_name = "IhuDhuInfoCanFr03"
    msg_id = 336
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VehSpdLvl:
        sig_name = "VehSpdLvl"
        sig_start_bit = 31
        update_id_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehSpdLvl_Off': 0, 'VehSpdLvl_Low': 1, 'VehSpdLvl_Middle': 2, 'VehSpdLvl_High': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CdcPrivateInfoCANNmFr:
    msg_name = "CdcPrivateInfoCANNmFr"
    msg_id = 1339
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class AUDInfoCANFDFr11:
    msg_name = "AUDInfoCANFDFr11"
    msg_id = 560
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 32
    tx_node = "AUD"
    rx_nodes = ['CDC']
    sig_group_dict = {'FgrndChannelMappingSts': ['FgrndChannelMappingStsAudOutpCh1', 'FgrndChannelMappingStsAudOutpCh10', 'FgrndChannelMappingStsAudOutpCh11', 'FgrndChannelMappingStsAudOutpCh12', 'FgrndChannelMappingStsAudOutpCh13', 'FgrndChannelMappingStsAudOutpCh14', 'FgrndChannelMappingStsAudOutpCh15', 'FgrndChannelMappingStsAudOutpCh16', 'FgrndChannelMappingStsAudOutpCh2', 'FgrndChannelMappingStsAudOutpCh3', 'FgrndChannelMappingStsAudOutpCh4', 'FgrndChannelMappingStsAudOutpCh5', 'FgrndChannelMappingStsAudOutpCh6', 'FgrndChannelMappingStsAudOutpCh7', 'FgrndChannelMappingStsAudOutpCh8', 'FgrndChannelMappingStsAudOutpCh9'], 'AlarmsChannelMappingSts': ['AlarmsChannelMappingStsAudOutpCh1', 'AlarmsChannelMappingStsAudOutpCh10', 'AlarmsChannelMappingStsAudOutpCh11', 'AlarmsChannelMappingStsAudOutpCh12', 'AlarmsChannelMappingStsAudOutpCh13', 'AlarmsChannelMappingStsAudOutpCh14', 'AlarmsChannelMappingStsAudOutpCh15', 'AlarmsChannelMappingStsAudOutpCh16', 'AlarmsChannelMappingStsAudOutpCh2', 'AlarmsChannelMappingStsAudOutpCh3', 'AlarmsChannelMappingStsAudOutpCh4', 'AlarmsChannelMappingStsAudOutpCh5', 'AlarmsChannelMappingStsAudOutpCh6', 'AlarmsChannelMappingStsAudOutpCh7', 'AlarmsChannelMappingStsAudOutpCh8', 'AlarmsChannelMappingStsAudOutpCh9'], 'TtsChannelMappingSts': ['TtsChannelMappingStsAudOutpCh1', 'TtsChannelMappingStsAudOutpCh10', 'TtsChannelMappingStsAudOutpCh11', 'TtsChannelMappingStsAudOutpCh12', 'TtsChannelMappingStsAudOutpCh13', 'TtsChannelMappingStsAudOutpCh14', 'TtsChannelMappingStsAudOutpCh15', 'TtsChannelMappingStsAudOutpCh16', 'TtsChannelMappingStsAudOutpCh2', 'TtsChannelMappingStsAudOutpCh3', 'TtsChannelMappingStsAudOutpCh4', 'TtsChannelMappingStsAudOutpCh5', 'TtsChannelMappingStsAudOutpCh6', 'TtsChannelMappingStsAudOutpCh7', 'TtsChannelMappingStsAudOutpCh8', 'TtsChannelMappingStsAudOutpCh9'], 'BgrndChannelMappingSts': ['BgrndChannelMappingStsAudOutpCh1', 'BgrndChannelMappingStsAudOutpCh10', 'BgrndChannelMappingStsAudOutpCh11', 'BgrndChannelMappingStsAudOutpCh12', 'BgrndChannelMappingStsAudOutpCh13', 'BgrndChannelMappingStsAudOutpCh14', 'BgrndChannelMappingStsAudOutpCh15', 'BgrndChannelMappingStsAudOutpCh16', 'BgrndChannelMappingStsAudOutpCh2', 'BgrndChannelMappingStsAudOutpCh3', 'BgrndChannelMappingStsAudOutpCh4', 'BgrndChannelMappingStsAudOutpCh5', 'BgrndChannelMappingStsAudOutpCh6', 'BgrndChannelMappingStsAudOutpCh7', 'BgrndChannelMappingStsAudOutpCh8', 'BgrndChannelMappingStsAudOutpCh9']}
    sig_group_dataid_dict = {}

    class FgrndChannelMappingSts_UB:
        sig_name = "FgrndChannelMappingSts_UB"
        sig_start_bit = 64
        update_id_bit = 64
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SonarSoundSts2:
        sig_name = "SonarSoundSts2"
        sig_start_bit = 199
        update_id_bit = 192
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
        startbit = 199
        byte = 24
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class AlarmsChannelMappingStsAudOutpCh15:
        sig_name = "AlarmsChannelMappingStsAudOutpCh15"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AlarmsChannelMappingStsAudOutpCh9:
        sig_name = "AlarmsChannelMappingStsAudOutpCh9"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndChannelMappingStsAudOutpCh6:
        sig_name = "BgrndChannelMappingStsAudOutpCh6"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class EssOnOffSts:
        sig_name = "EssOnOffSts"
        sig_start_bit = 130
        update_id_bit = 169
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 130
        byte = 16
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AlarmsChannelMappingSts_UB:
        sig_name = "AlarmsChannelMappingSts_UB"
        sig_start_bit = 16
        update_id_bit = 16
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AlarmsChannelMappingStsAudOutpCh12:
        sig_name = "AlarmsChannelMappingStsAudOutpCh12"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class FgrndChannelMappingStsAudOutpCh1:
        sig_name = "FgrndChannelMappingStsAudOutpCh1"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BgrndEqFreq1Sts:
        sig_name = "BgrndEqFreq1Sts"
        sig_start_bit = 119
        update_id_bit = 144
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 119
        byte = 14
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class FgrndChannelMappingStsAudOutpCh9:
        sig_name = "FgrndChannelMappingStsAudOutpCh9"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class TtsChannelMappingSts_UB:
        sig_name = "TtsChannelMappingSts_UB"
        sig_start_bit = 88
        update_id_bit = 88
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 88
        byte = 11
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class TtsChannelMappingStsAudOutpCh4:
        sig_name = "TtsChannelMappingStsAudOutpCh4"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 76
        byte = 9
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BgrndEqFreq4Sts:
        sig_name = "BgrndEqFreq4Sts"
        sig_start_bit = 143
        update_id_bit = 175
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 143
        byte = 17
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class BgrndChannelMappingStsAudOutpCh2:
        sig_name = "BgrndChannelMappingStsAudOutpCh2"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class FgrndChannelMappingStsAudOutpCh7:
        sig_name = "FgrndChannelMappingStsAudOutpCh7"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AlarmsChannelMappingStsAudOutpCh6:
        sig_name = "AlarmsChannelMappingStsAudOutpCh6"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class FgrndChannelMappingStsAudOutpCh14:
        sig_name = "FgrndChannelMappingStsAudOutpCh14"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class FgrndChannelMappingStsAudOutpCh15:
        sig_name = "FgrndChannelMappingStsAudOutpCh15"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingStsAudOutpCh7:
        sig_name = "TtsChannelMappingStsAudOutpCh7"
        sig_start_bit = 73
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 73
        byte = 9
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class SurroundLvlFor3DSts:
        sig_name = "SurroundLvlFor3DSts"
        sig_start_bit = 154
        update_id_bit = 180
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SurroundLvl_low': 0, 'SurroundLvl_mid': 1, 'SurroundLvl_high': 2}
        compute_method = None
        length = 2
        startbit = 154
        byte = 19
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class AlarmsChannelMappingStsAudOutpCh7:
        sig_name = "AlarmsChannelMappingStsAudOutpCh7"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class AlarmsChannelMappingStsAudOutpCh13:
        sig_name = "AlarmsChannelMappingStsAudOutpCh13"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TtsChannelMappingStsAudOutpCh16:
        sig_name = "TtsChannelMappingStsAudOutpCh16"
        sig_start_bit = 80
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 80
        byte = 10
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class TtsChannelMappingStsAudOutpCh11:
        sig_name = "TtsChannelMappingStsAudOutpCh11"
        sig_start_bit = 85
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 85
        byte = 10
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FgrndChannelMappingStsAudOutpCh16:
        sig_name = "FgrndChannelMappingStsAudOutpCh16"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class SpkChErrSts:
        sig_name = "SpkChErrSts"
        sig_start_bit = 103
        update_id_bit = 89
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 103
        bmuws_info = [(12, 0b11111111, 0b00000000, 8, 0), (13, 0b11111111, 0b00000000, 8, 0)]

    class TtsChannelMappingStsAudOutpCh13:
        sig_name = "TtsChannelMappingStsAudOutpCh13"
        sig_start_bit = 83
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 83
        byte = 10
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BgrndChannelMappingStsAudOutpCh10:
        sig_name = "BgrndChannelMappingStsAudOutpCh10"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SurroundLvlFor2DSts:
        sig_name = "SurroundLvlFor2DSts"
        sig_start_bit = 146
        update_id_bit = 181
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SurroundLvl_low': 0, 'SurroundLvl_mid': 1, 'SurroundLvl_high': 2}
        compute_method = None
        length = 2
        startbit = 146
        byte = 18
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class BgrndChannelMappingSts_UB:
        sig_name = "BgrndChannelMappingSts_UB"
        sig_start_bit = 40
        update_id_bit = 40
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BgrndChannelMappingStsAudOutpCh12:
        sig_name = "BgrndChannelMappingStsAudOutpCh12"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndEqFreq2Sts:
        sig_name = "BgrndEqFreq2Sts"
        sig_start_bit = 127
        update_id_bit = 152
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 127
        byte = 15
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class A2BSts:
        sig_name = "A2BSts"
        sig_start_bit = 18
        update_id_bit = 17
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalStatus_Normal': 0, 'NormalStatus_Error': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BgrndChannelMappingStsAudOutpCh7:
        sig_name = "BgrndChannelMappingStsAudOutpCh7"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class AlarmsChannelMappingStsAudOutpCh1:
        sig_name = "AlarmsChannelMappingStsAudOutpCh1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FgrndChannelMappingStsAudOutpCh10:
        sig_name = "FgrndChannelMappingStsAudOutpCh10"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BgrndChannelMappingStsAudOutpCh16:
        sig_name = "BgrndChannelMappingStsAudOutpCh16"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndChannelMappingStsAudOutpCh1:
        sig_name = "BgrndChannelMappingStsAudOutpCh1"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingStsAudOutpCh8:
        sig_name = "TtsChannelMappingStsAudOutpCh8"
        sig_start_bit = 72
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 72
        byte = 9
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AlarmsChannelMappingStsAudOutpCh5:
        sig_name = "AlarmsChannelMappingStsAudOutpCh5"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SurroundTypeSts:
        sig_name = "SurroundTypeSts"
        sig_start_bit = 162
        update_id_bit = 179
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SurroundType_off': 0, 'SurroundType_2D_surround': 1, 'SurroundType_3D_surround': 2}
        compute_method = None
        length = 2
        startbit = 162
        byte = 20
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class AlarmsChannelMappingStsAudOutpCh2:
        sig_name = "AlarmsChannelMappingStsAudOutpCh2"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BgrndEqFreq3Sts:
        sig_name = "BgrndEqFreq3Sts"
        sig_start_bit = 135
        update_id_bit = 160
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 135
        byte = 16
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class ClearSoundSts:
        sig_name = "ClearSoundSts"
        sig_start_bit = 112
        update_id_bit = 171
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 112
        byte = 14
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FgrndChannelMappingStsAudOutpCh11:
        sig_name = "FgrndChannelMappingStsAudOutpCh11"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class SoundEffectSts:
        sig_name = "SoundEffectSts"
        sig_start_bit = 138
        update_id_bit = 183
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SoundEffect_beats': 0, 'SoundEffect_EQ1': 1, 'SoundEffect_EQ2': 2, 'SoundEffect_EQ3': 3, 'SoundEffect_customer': 4, 'SoundEffect_reserved1': 5, 'SoundEffect_reserved2': 6, 'SoundEffect_reserved3': 7}
        compute_method = None
        length = 3
        startbit = 138
        byte = 17
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class BgrndChannelMappingStsAudOutpCh13:
        sig_name = "BgrndChannelMappingStsAudOutpCh13"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndChannelMappingStsAudOutpCh5:
        sig_name = "BgrndChannelMappingStsAudOutpCh5"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class FgrndChannelMappingStsAudOutpCh2:
        sig_name = "FgrndChannelMappingStsAudOutpCh2"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AlarmsChannelMappingStsAudOutpCh8:
        sig_name = "AlarmsChannelMappingStsAudOutpCh8"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingStsAudOutpCh5:
        sig_name = "TtsChannelMappingStsAudOutpCh5"
        sig_start_bit = 75
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 75
        byte = 9
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AlarmsChannelMappingStsAudOutpCh4:
        sig_name = "AlarmsChannelMappingStsAudOutpCh4"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndEqFreq6Sts:
        sig_name = "BgrndEqFreq6Sts"
        sig_start_bit = 159
        update_id_bit = 173
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 159
        byte = 19
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class SoundFieldSts:
        sig_name = "SoundFieldSts"
        sig_start_bit = 129
        update_id_bit = 182
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SoundField_all': 0, 'SoundField_Front': 1, 'SoundField_Drive': 2}
        compute_method = None
        length = 2
        startbit = 129
        byte = 16
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AlarmsChannelMappingStsAudOutpCh10:
        sig_name = "AlarmsChannelMappingStsAudOutpCh10"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class TtsChannelMappingStsAudOutpCh6:
        sig_name = "TtsChannelMappingStsAudOutpCh6"
        sig_start_bit = 74
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 74
        byte = 9
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FgrndChannelMappingStsAudOutpCh13:
        sig_name = "FgrndChannelMappingStsAudOutpCh13"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingStsAudOutpCh2:
        sig_name = "TtsChannelMappingStsAudOutpCh2"
        sig_start_bit = 78
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 78
        byte = 9
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BgrndChannelMappingStsAudOutpCh11:
        sig_name = "BgrndChannelMappingStsAudOutpCh11"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingStsAudOutpCh14:
        sig_name = "TtsChannelMappingStsAudOutpCh14"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 82
        byte = 10
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AlarmsChannelMappingStsAudOutpCh14:
        sig_name = "AlarmsChannelMappingStsAudOutpCh14"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FgrndChannelMappingStsAudOutpCh6:
        sig_name = "FgrndChannelMappingStsAudOutpCh6"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FgrndChannelMappingStsAudOutpCh5:
        sig_name = "FgrndChannelMappingStsAudOutpCh5"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AlarmsChannelMappingStsAudOutpCh11:
        sig_name = "AlarmsChannelMappingStsAudOutpCh11"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingStsAudOutpCh3:
        sig_name = "TtsChannelMappingStsAudOutpCh3"
        sig_start_bit = 77
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 77
        byte = 9
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class TtsChannelMappingStsAudOutpCh15:
        sig_name = "TtsChannelMappingStsAudOutpCh15"
        sig_start_bit = 81
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 81
        byte = 10
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BgrndChannelMappingStsAudOutpCh3:
        sig_name = "BgrndChannelMappingStsAudOutpCh3"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingStsAudOutpCh10:
        sig_name = "TtsChannelMappingStsAudOutpCh10"
        sig_start_bit = 86
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 86
        byte = 10
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BgrndChannelMappingStsAudOutpCh8:
        sig_name = "BgrndChannelMappingStsAudOutpCh8"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class FgrndChannelMappingStsAudOutpCh3:
        sig_name = "FgrndChannelMappingStsAudOutpCh3"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BgrndChannelMappingStsAudOutpCh14:
        sig_name = "BgrndChannelMappingStsAudOutpCh14"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingStsAudOutpCh9:
        sig_name = "TtsChannelMappingStsAudOutpCh9"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 87
        byte = 10
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AlarmsChannelMappingStsAudOutpCh16:
        sig_name = "AlarmsChannelMappingStsAudOutpCh16"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AUDSts:
        sig_name = "AUDSts"
        sig_start_bit = 45
        update_id_bit = 41
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 45
        byte = 5
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class TtsChannelMappingStsAudOutpCh1:
        sig_name = "TtsChannelMappingStsAudOutpCh1"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 79
        byte = 9
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class FgrndChannelMappingStsAudOutpCh4:
        sig_name = "FgrndChannelMappingStsAudOutpCh4"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FgrndChannelMappingStsAudOutpCh12:
        sig_name = "FgrndChannelMappingStsAudOutpCh12"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class SonarSoundSts:
        sig_name = "SonarSoundSts"
        sig_start_bit = 167
        update_id_bit = 168
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
        startbit = 167
        byte = 20
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class BgrndChannelMappingStsAudOutpCh9:
        sig_name = "BgrndChannelMappingStsAudOutpCh9"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EssModeSts:
        sig_name = "EssModeSts"
        sig_start_bit = 122
        update_id_bit = 170
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerMod_Ukwn': 0, 'SteerMod_Mod1': 1, 'SteerMod_Mod2': 2, 'SteerMod_Mod3': 3, 'SteerMod_Mod4': 4, 'SteerMod_Resd5': 5, 'SteerMod_Resd6': 6, 'SteerMod_Resd7': 7}
        compute_method = None
        length = 3
        startbit = 122
        byte = 15
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class FgrndChannelMappingStsAudOutpCh8:
        sig_name = "FgrndChannelMappingStsAudOutpCh8"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BgrndChannelMappingStsAudOutpCh15:
        sig_name = "BgrndChannelMappingStsAudOutpCh15"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndChannelMappingStsAudOutpCh4:
        sig_name = "BgrndChannelMappingStsAudOutpCh4"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingStsAudOutpCh12:
        sig_name = "TtsChannelMappingStsAudOutpCh12"
        sig_start_bit = 84
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 84
        byte = 10
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BgrndEqFreq5Sts:
        sig_name = "BgrndEqFreq5Sts"
        sig_start_bit = 151
        update_id_bit = 174
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 151
        byte = 18
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class BgrndInputTypeSts:
        sig_name = "BgrndInputTypeSts"
        sig_start_bit = 178
        update_id_bit = 172
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BgrndInputType_2_0': 0, 'BgrndInputType_5_1': 1, 'BgrndInputType_7_1_2': 2, 'BgrndInputType_5_1_2': 3, 'BgrndInputType_7_1': 4, 'BgrndInputType_reserved1': 5, 'BgrndInputType_reserved2': 6, 'BgrndInputType_reserved3': 7}
        compute_method = None
        length = 3
        startbit = 178
        byte = 22
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class AlarmsChannelMappingStsAudOutpCh3:
        sig_name = "AlarmsChannelMappingStsAudOutpCh3"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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


class IhuDhuInfoCanFr25:
    msg_name = "IhuDhuInfoCanFr25"
    msg_id = 529
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD', 'CD']
    sig_group_dict = {'VehCfgPrm': ['VehCfgPrmBlkIDBytePosn1', 'VehCfgPrmCCPBytePosn2', 'VehCfgPrmCCPBytePosn3', 'VehCfgPrmCCPBytePosn4', 'VehCfgPrmCCPBytePosn5', 'VehCfgPrmCCPBytePosn6', 'VehCfgPrmCCPBytePosn7', 'VehCfgPrmCCPBytePosn8']}
    sig_group_dataid_dict = {}

    class VehCfgPrmCCPBytePosn8:
        sig_name = "VehCfgPrmCCPBytePosn8"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmBlkIDBytePosn1:
        sig_name = "VehCfgPrmBlkIDBytePosn1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn5:
        sig_name = "VehCfgPrmCCPBytePosn5"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn6:
        sig_name = "VehCfgPrmCCPBytePosn6"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn7:
        sig_name = "VehCfgPrmCCPBytePosn7"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn4:
        sig_name = "VehCfgPrmCCPBytePosn4"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn3:
        sig_name = "VehCfgPrmCCPBytePosn3"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmCCPBytePosn2:
        sig_name = "VehCfgPrmCCPBytePosn2"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CDPrivateInfoCANFDFr01:
    msg_name = "CDPrivateInfoCANFDFr01"
    msg_id = 576
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "CD"
    rx_nodes = ['CDC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DisplayAreaSts:
        sig_name = "DisplayAreaSts"
        sig_start_bit = 34
        update_id_bit = 70
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'All_Off': 0, 'All_On': 1, 'Only_Cluster_On': 2, 'Only_Entertainment_On': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class CDWorkSts:
        sig_name = "CDWorkSts"
        sig_start_bit = 39
        update_id_bit = 48
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CDWorkSts_Unknow': 0, 'CDWorkSts_Start_up': 1, 'CDWorkSts_Shut_down': 2, 'CDWorkSts_Work_On': 3, 'CDWorkSts_Reserve1': 4, 'CDWorkSts_Reserve2': 5, 'CDWorkSts_Reserve3': 6, 'CDWorkSts_Reserve4': 7}
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CDDispAbnormalSts:
        sig_name = "CDDispAbnormalSts"
        sig_start_bit = 119
        update_id_bit = 111
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 119
        bmuws_info = [(14, 0b11111111, 0b00000000, 8, 0), (15, 0b11111111, 0b00000000, 8, 0)]

    class GearDispFedBck:
        sig_name = "GearDispFedBck"
        sig_start_bit = 55
        update_id_bit = 66
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Gear_Display_Normally': 0, 'Display_P_Wrong': 1, 'Display_R_Wrong': 2, 'Display_D_Wrong': 3, 'Reserve1': 4, 'Reserve2': 5, 'Reserve3': 6, 'Reserve4': 7, 'Reserve5': 8, 'Reserve6': 9, 'Reserve7': 10, 'Reserve8': 11, 'Reserve9': 12, 'Reserve10': 13, 'Reserve11': 14, 'Reserve12': 15}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CDTemp:
        sig_name = "CDTemp"
        sig_start_bit = 15
        update_id_bit = 51
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 135
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDVoltage:
        sig_name = "CDVoltage"
        sig_start_bit = 31
        update_id_bit = 49
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LuminanceLevelFedBck:
        sig_name = "LuminanceLevelFedBck"
        sig_start_bit = 63
        update_id_bit = 65
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDFlickerSts:
        sig_name = "CDFlickerSts"
        sig_start_bit = 87
        update_id_bit = 88
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 87
        byte = 10
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDDisplayModeFedBck:
        sig_name = "CDDisplayModeFedBck"
        sig_start_bit = 1
        update_id_bit = 40
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CDCDisplayMode_Daymode': 0, 'CDCDisplayMode_Nightmode': 1, 'CDCDisplayMode_Nosetting': 2, 'CDCDisplayMode_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CDDispErrSts:
        sig_name = "CDDispErrSts"
        sig_start_bit = 103
        update_id_bit = 104
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CDDispErrSts_Not_occur': 0, 'CDDispErrSts_Occur': 1}
        compute_method = None
        length = 8
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CdcToAllInfoCanDiagReqFrame:
    msg_name = "CdcToAllInfoCanDiagReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD', 'CD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CDPrivateInfoCANFDFr03:
    msg_name = "CDPrivateInfoCANFDFr03"
    msg_id = 96
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 16
    tx_node = "CD"
    rx_nodes = ['CDC']
    sig_group_dict = {'DimSts': ['DimStsChks', 'DimStsCntr', 'DimStsDimSts'], 'ScreenSts': ['ScreenStsChks', 'ScreenStsCntr', 'ScreenStsScreenICSts']}
    sig_group_dataid_dict = {'DimSts': 8084, 'ScreenSts': 8083}

    class ScreenStsChks:
        sig_name = "ScreenStsChks"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ScreenStsScreenICSts:
        sig_name = "ScreenStsScreenICSts"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ScreenICSts_All_IC_Ok': 0, 'ScreenICSts_Fault1': 1, 'ScreenICSts_Fault2': 2, 'ScreenICSts_Fault3': 3, 'ScreenICSts_Fault4': 4, 'ScreenICSts_Fault5': 5, 'ScreenICSts_Fault6': 6, 'ScreenICSts_Fault7': 7, 'ScreenICSts_Fault8': 8, 'ScreenICSts_Fault9': 9, 'ScreenICSts_Fault10': 10, 'ScreenICSts_Fault11': 11, 'ScreenICSts_Fault12': 12, 'ScreenICSts_Fault13': 13, 'ScreenICSts_Fault14': 14, 'ScreenICSts_Fault15': 15, 'ScreenICSts_Fault16': 16, 'ScreenICSts_Fault17': 17, 'ScreenICSts_Fault18': 18, 'ScreenICSts_Fault19': 19, 'ScreenICSts_Fault20': 20, 'ScreenICSts_Fault21': 21, 'ScreenICSts_Fault22': 22, 'ScreenICSts_Fault23': 23, 'ScreenICSts_Fault24': 24, 'ScreenICSts_Fault25': 25, 'ScreenICSts_Fault26': 26, 'ScreenICSts_Fault27': 27, 'ScreenICSts_Fault28': 28, 'ScreenICSts_Fault29': 29, 'ScreenICSts_Fault30': 30, 'ScreenICSts_Fault31': 31, 'ScreenICSts_Fault32': 32, 'ScreenICSts_Fault33': 33, 'ScreenICSts_Fault34': 34, 'ScreenICSts_Fault35': 35, 'ScreenICSts_Fault36': 36, 'ScreenICSts_Fault37': 37, 'ScreenICSts_Fault38': 38, 'ScreenICSts_Fault39': 39, 'ScreenICSts_Fault40': 40, 'ScreenICSts_Fault41': 41, 'ScreenICSts_Fault42': 42, 'ScreenICSts_Fault43': 43, 'ScreenICSts_Fault44': 44, 'ScreenICSts_Fault45': 45, 'ScreenICSts_Fault46': 46, 'ScreenICSts_Fault47': 47, 'ScreenICSts_Fault48': 48, 'ScreenICSts_Fault49': 49, 'ScreenICSts_Fault50': 50, 'ScreenICSts_Fault51': 51, 'ScreenICSts_Fault52': 52, 'ScreenICSts_Fault53': 53, 'ScreenICSts_Fault54': 54, 'ScreenICSts_Fault55': 55, 'ScreenICSts_Fault56': 56, 'ScreenICSts_Fault57': 57, 'ScreenICSts_Fault58': 58, 'ScreenICSts_Fault59': 59, 'ScreenICSts_Fault60': 60, 'ScreenICSts_Fault61': 61, 'ScreenICSts_Fault62': 62, 'ScreenICSts_All_IC_Fault': 63}
        compute_method = None
        length = 6
        startbit = 55
        byte = 6
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DimStsCntr:
        sig_name = "DimStsCntr"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DimStsChks:
        sig_name = "DimStsChks"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ScreenStsCntr:
        sig_name = "ScreenStsCntr"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DimStsDimSts:
        sig_name = "DimStsDimSts"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DimmingSts_Off': 0, 'DimmingSts_Ready': 1, 'DimmingSts_Fault': 2, 'DimmingSts_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DimSts_UB:
        sig_name = "DimSts_UB"
        sig_start_bit = 24
        update_id_bit = 24
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ScreenSts_UB:
        sig_name = "ScreenSts_UB"
        sig_start_bit = 40
        update_id_bit = 40
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class IhuDhuInfoCanFr26:
    msg_name = "IhuDhuInfoCanFr26"
    msg_id = 570
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD', 'CD']
    sig_group_dict = {'VehCfgPrmExt': ['VehCfgPrmExtBlkIDBytePosn1', 'VehCfgPrmExtCCPBytePosn2', 'VehCfgPrmExtCCPBytePosn3', 'VehCfgPrmExtCCPBytePosn4', 'VehCfgPrmExtCCPBytePosn5', 'VehCfgPrmExtCCPBytePosn6', 'VehCfgPrmExtCCPBytePosn7', 'VehCfgPrmExtCCPBytePosn8']}
    sig_group_dataid_dict = {}

    class VehCfgPrmExtCCPBytePosn6:
        sig_name = "VehCfgPrmExtCCPBytePosn6"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn4:
        sig_name = "VehCfgPrmExtCCPBytePosn4"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn2:
        sig_name = "VehCfgPrmExtCCPBytePosn2"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn3:
        sig_name = "VehCfgPrmExtCCPBytePosn3"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn7:
        sig_name = "VehCfgPrmExtCCPBytePosn7"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn8:
        sig_name = "VehCfgPrmExtCCPBytePosn8"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtBlkIDBytePosn1:
        sig_name = "VehCfgPrmExtBlkIDBytePosn1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehCfgPrmExtCCPBytePosn5:
        sig_name = "VehCfgPrmExtCCPBytePosn5"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class IhuDhuInfoCanFr12:
    msg_name = "IhuDhuInfoCanFr12"
    msg_id = 11
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']
    sig_group_dict = {'AccrPedlRat': ['AccrPedlRatAccrPedlRat', 'AccrPedlRatChks', 'AccrPedlRatCntr']}
    sig_group_dataid_dict = {'AccrPedlRat': 868}

    class AccrPedlRatCntr:
        sig_name = "AccrPedlRatCntr"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AccrPedlRatAccrPedlRat:
        sig_name = "AccrPedlRatAccrPedlRat"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class AccrPedlRat_UB:
        sig_name = "AccrPedlRat_UB"
        sig_start_bit = 7
        update_id_bit = 7
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AccrPedlRatChks:
        sig_name = "AccrPedlRatChks"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CenterDisplayToCdcPrivateInfoCanDiagRespFrame:
    msg_name = "CenterDisplayToCdcPrivateInfoCanDiagRespFrame"
    msg_id = 1665
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CD"
    rx_nodes = ['CDC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class AudPrivateInfoCANNmFr:
    msg_name = "AudPrivateInfoCANNmFr"
    msg_id = 1281
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "AUD"
    rx_nodes = ['CD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IhuDhuInfoCanFr02:
    msg_name = "IhuDhuInfoCanFr02"
    msg_id = 913
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VolLvlBgrnd:
        sig_name = "VolLvlBgrnd"
        sig_start_bit = 23
        update_id_bit = 10
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 18
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class AUDInfoCanFr03:
    msg_name = "AUDInfoCanFr03"
    msg_id = 944
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "AUD"
    rx_nodes = ['CDC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BgrndForVolLvlSts:
        sig_name = "BgrndForVolLvlSts"
        sig_start_bit = 47
        update_id_bit = 30
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CDCPrivateInfoCANFDFr06:
    msg_name = "CDCPrivateInfoCANFDFr06"
    msg_id = 369
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 32
    tx_node = "CDC"
    rx_nodes = ['AUD']
    sig_group_dict = {'FgrndChannelMapping': ['FgrndChannelMappingAudOutpCh1', 'FgrndChannelMappingAudOutpCh10', 'FgrndChannelMappingAudOutpCh11', 'FgrndChannelMappingAudOutpCh12', 'FgrndChannelMappingAudOutpCh13', 'FgrndChannelMappingAudOutpCh14', 'FgrndChannelMappingAudOutpCh15', 'FgrndChannelMappingAudOutpCh16', 'FgrndChannelMappingAudOutpCh2', 'FgrndChannelMappingAudOutpCh3', 'FgrndChannelMappingAudOutpCh4', 'FgrndChannelMappingAudOutpCh5', 'FgrndChannelMappingAudOutpCh6', 'FgrndChannelMappingAudOutpCh7', 'FgrndChannelMappingAudOutpCh8', 'FgrndChannelMappingAudOutpCh9'], 'TtsChannelMapping': ['TtsChannelMappingAudOutpCh1', 'TtsChannelMappingAudOutpCh10', 'TtsChannelMappingAudOutpCh11', 'TtsChannelMappingAudOutpCh12', 'TtsChannelMappingAudOutpCh13', 'TtsChannelMappingAudOutpCh14', 'TtsChannelMappingAudOutpCh15', 'TtsChannelMappingAudOutpCh16', 'TtsChannelMappingAudOutpCh2', 'TtsChannelMappingAudOutpCh3', 'TtsChannelMappingAudOutpCh4', 'TtsChannelMappingAudOutpCh5', 'TtsChannelMappingAudOutpCh6', 'TtsChannelMappingAudOutpCh7', 'TtsChannelMappingAudOutpCh8', 'TtsChannelMappingAudOutpCh9'], 'BgrndChannelMapping': ['BgrndChannelMappingAudOutpCh1', 'BgrndChannelMappingAudOutpCh10', 'BgrndChannelMappingAudOutpCh11', 'BgrndChannelMappingAudOutpCh12', 'BgrndChannelMappingAudOutpCh13', 'BgrndChannelMappingAudOutpCh14', 'BgrndChannelMappingAudOutpCh15', 'BgrndChannelMappingAudOutpCh16', 'BgrndChannelMappingAudOutpCh2', 'BgrndChannelMappingAudOutpCh3', 'BgrndChannelMappingAudOutpCh4', 'BgrndChannelMappingAudOutpCh5', 'BgrndChannelMappingAudOutpCh6', 'BgrndChannelMappingAudOutpCh7', 'BgrndChannelMappingAudOutpCh8', 'BgrndChannelMappingAudOutpCh9'], 'AlarmsChannelMapping': ['AlarmsChannelMappingAudOutpCh1', 'AlarmsChannelMappingAudOutpCh10', 'AlarmsChannelMappingAudOutpCh11', 'AlarmsChannelMappingAudOutpCh12', 'AlarmsChannelMappingAudOutpCh13', 'AlarmsChannelMappingAudOutpCh14', 'AlarmsChannelMappingAudOutpCh15', 'AlarmsChannelMappingAudOutpCh16', 'AlarmsChannelMappingAudOutpCh2', 'AlarmsChannelMappingAudOutpCh3', 'AlarmsChannelMappingAudOutpCh4', 'AlarmsChannelMappingAudOutpCh5', 'AlarmsChannelMappingAudOutpCh6', 'AlarmsChannelMappingAudOutpCh7', 'AlarmsChannelMappingAudOutpCh8', 'AlarmsChannelMappingAudOutpCh9']}
    sig_group_dataid_dict = {}

    class FgrndChannelMappingAudOutpCh13:
        sig_name = "FgrndChannelMappingAudOutpCh13"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class SoundEffect:
        sig_name = "SoundEffect"
        sig_start_bit = 138
        update_id_bit = 183
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SoundEffect_beats': 0, 'SoundEffect_EQ1': 1, 'SoundEffect_EQ2': 2, 'SoundEffect_EQ3': 3, 'SoundEffect_customer': 4, 'SoundEffect_reserved1': 5, 'SoundEffect_reserved2': 6, 'SoundEffect_reserved3': 7}
        compute_method = None
        length = 3
        startbit = 138
        byte = 17
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class BgrndEqFreq4:
        sig_name = "BgrndEqFreq4"
        sig_start_bit = 143
        update_id_bit = 175
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 143
        byte = 17
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class TtsChannelMappingAudOutpCh16:
        sig_name = "TtsChannelMappingAudOutpCh16"
        sig_start_bit = 80
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 80
        byte = 10
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FgrndChannelMappingAudOutpCh16:
        sig_name = "FgrndChannelMappingAudOutpCh16"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndChannelMappingAudOutpCh7:
        sig_name = "BgrndChannelMappingAudOutpCh7"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class TtsChannelMappingAudOutpCh15:
        sig_name = "TtsChannelMappingAudOutpCh15"
        sig_start_bit = 81
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 81
        byte = 10
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class TtsChannelMappingAudOutpCh5:
        sig_name = "TtsChannelMappingAudOutpCh5"
        sig_start_bit = 75
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 75
        byte = 9
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AlarmsChannelMappingAudOutpCh15:
        sig_name = "AlarmsChannelMappingAudOutpCh15"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AlarmsChannelMappingAudOutpCh2:
        sig_name = "AlarmsChannelMappingAudOutpCh2"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AlarmsChannelMappingAudOutpCh13:
        sig_name = "AlarmsChannelMappingAudOutpCh13"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AlarmsChannelMappingAudOutpCh10:
        sig_name = "AlarmsChannelMappingAudOutpCh10"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FgrndChannelMappingAudOutpCh1:
        sig_name = "FgrndChannelMappingAudOutpCh1"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class TtsChannelMappingAudOutpCh2:
        sig_name = "TtsChannelMappingAudOutpCh2"
        sig_start_bit = 78
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 78
        byte = 9
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AlarmsChannelMappingAudOutpCh16:
        sig_name = "AlarmsChannelMappingAudOutpCh16"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FgrndChannelMapping_UB:
        sig_name = "FgrndChannelMapping_UB"
        sig_start_bit = 64
        update_id_bit = 64
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 64
        byte = 8
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BgrndChannelMappingAudOutpCh15:
        sig_name = "BgrndChannelMappingAudOutpCh15"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingAudOutpCh3:
        sig_name = "TtsChannelMappingAudOutpCh3"
        sig_start_bit = 77
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 77
        byte = 9
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AlarmsChannelMappingAudOutpCh1:
        sig_name = "AlarmsChannelMappingAudOutpCh1"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BgrndChannelMappingAudOutpCh1:
        sig_name = "BgrndChannelMappingAudOutpCh1"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SurroundLvlFor3D:
        sig_name = "SurroundLvlFor3D"
        sig_start_bit = 154
        update_id_bit = 180
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SurroundLvl_low': 0, 'SurroundLvl_mid': 1, 'SurroundLvl_high': 2}
        compute_method = None
        length = 2
        startbit = 154
        byte = 19
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class GearPosition:
        sig_name = "GearPosition"
        sig_start_bit = 207
        update_id_bit = 193
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn2_ParkIndcn': 0, 'GearLvrIndcn2_RvsIndcn': 1, 'GearLvrIndcn2_NeutIndcn': 2, 'GearLvrIndcn2_DrvIndcn': 3, 'GearLvrIndcn2_ManModeIndcn': 4, 'GearLvrIndcn2_Resd1': 5, 'GearLvrIndcn2_Resd2': 6, 'GearLvrIndcn2_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 207
        byte = 25
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class TtsChannelMappingAudOutpCh13:
        sig_name = "TtsChannelMappingAudOutpCh13"
        sig_start_bit = 83
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 83
        byte = 10
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BgrndInputType:
        sig_name = "BgrndInputType"
        sig_start_bit = 178
        update_id_bit = 172
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BgrndInputType_2_0': 0, 'BgrndInputType_5_1': 1, 'BgrndInputType_7_1_2': 2, 'BgrndInputType_5_1_2': 3, 'BgrndInputType_7_1': 4, 'BgrndInputType_reserved1': 5, 'BgrndInputType_reserved2': 6, 'BgrndInputType_reserved3': 7}
        compute_method = None
        length = 3
        startbit = 178
        byte = 22
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class TtsChannelMapping_UB:
        sig_name = "TtsChannelMapping_UB"
        sig_start_bit = 88
        update_id_bit = 88
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 88
        byte = 11
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BgrndChannelMappingAudOutpCh11:
        sig_name = "BgrndChannelMappingAudOutpCh11"
        sig_start_bit = 37
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingAudOutpCh7:
        sig_name = "TtsChannelMappingAudOutpCh7"
        sig_start_bit = 73
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 73
        byte = 9
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class TtsChannelMappingAudOutpCh10:
        sig_name = "TtsChannelMappingAudOutpCh10"
        sig_start_bit = 86
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 86
        byte = 10
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AlarmsChannelMappingAudOutpCh12:
        sig_name = "AlarmsChannelMappingAudOutpCh12"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndChannelMappingAudOutpCh5:
        sig_name = "BgrndChannelMappingAudOutpCh5"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BgrndChannelMappingAudOutpCh16:
        sig_name = "BgrndChannelMappingAudOutpCh16"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingAudOutpCh6:
        sig_name = "TtsChannelMappingAudOutpCh6"
        sig_start_bit = 74
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 74
        byte = 9
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BgrndEqFreq1:
        sig_name = "BgrndEqFreq1"
        sig_start_bit = 119
        update_id_bit = 144
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 119
        byte = 14
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class SonarSoundPosition2:
        sig_name = "SonarSoundPosition2"
        sig_start_bit = 103
        update_id_bit = 96
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
        startbit = 103
        byte = 12
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class AlarmsChannelMappingAudOutpCh3:
        sig_name = "AlarmsChannelMappingAudOutpCh3"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndEqFreq3:
        sig_name = "BgrndEqFreq3"
        sig_start_bit = 135
        update_id_bit = 160
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 135
        byte = 16
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class AlarmsChannelMappingAudOutpCh9:
        sig_name = "AlarmsChannelMappingAudOutpCh9"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndChannelMappingAudOutpCh9:
        sig_name = "BgrndChannelMappingAudOutpCh9"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AlarmsChannelMappingAudOutpCh4:
        sig_name = "AlarmsChannelMappingAudOutpCh4"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class SoundField:
        sig_name = "SoundField"
        sig_start_bit = 129
        update_id_bit = 182
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SoundField_all': 0, 'SoundField_Front': 1, 'SoundField_Drive': 2}
        compute_method = None
        length = 2
        startbit = 129
        byte = 16
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TtsChannelMappingAudOutpCh14:
        sig_name = "TtsChannelMappingAudOutpCh14"
        sig_start_bit = 82
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 82
        byte = 10
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FgrndChannelMappingAudOutpCh3:
        sig_name = "FgrndChannelMappingAudOutpCh3"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class FgrndChannelMappingAudOutpCh4:
        sig_name = "FgrndChannelMappingAudOutpCh4"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SonarSoundPosition:
        sig_name = "SonarSoundPosition"
        sig_start_bit = 167
        update_id_bit = 168
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
        startbit = 167
        byte = 20
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class BgrndChannelMappingAudOutpCh12:
        sig_name = "BgrndChannelMappingAudOutpCh12"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class AlarmsChannelMappingAudOutpCh8:
        sig_name = "AlarmsChannelMappingAudOutpCh8"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingAudOutpCh8:
        sig_name = "TtsChannelMappingAudOutpCh8"
        sig_start_bit = 72
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 72
        byte = 9
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FgrndChannelMappingAudOutpCh12:
        sig_name = "FgrndChannelMappingAudOutpCh12"
        sig_start_bit = 60
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class FgrndChannelMappingAudOutpCh8:
        sig_name = "FgrndChannelMappingAudOutpCh8"
        sig_start_bit = 48
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BgrndChannelMappingAudOutpCh4:
        sig_name = "BgrndChannelMappingAudOutpCh4"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BgrndChannelMappingAudOutpCh6:
        sig_name = "BgrndChannelMappingAudOutpCh6"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FgrndChannelMappingAudOutpCh15:
        sig_name = "FgrndChannelMappingAudOutpCh15"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndEqFreq5:
        sig_name = "BgrndEqFreq5"
        sig_start_bit = 151
        update_id_bit = 174
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 151
        byte = 18
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class FgrndChannelMappingAudOutpCh2:
        sig_name = "FgrndChannelMappingAudOutpCh2"
        sig_start_bit = 54
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class TtsChannelMappingAudOutpCh1:
        sig_name = "TtsChannelMappingAudOutpCh1"
        sig_start_bit = 79
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 79
        byte = 9
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EssOnOff:
        sig_name = "EssOnOff"
        sig_start_bit = 130
        update_id_bit = 169
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 130
        byte = 16
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FgrndChannelMappingAudOutpCh5:
        sig_name = "FgrndChannelMappingAudOutpCh5"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FgrndChannelMappingAudOutpCh14:
        sig_name = "FgrndChannelMappingAudOutpCh14"
        sig_start_bit = 58
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class FgrndChannelMappingAudOutpCh7:
        sig_name = "FgrndChannelMappingAudOutpCh7"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AlarmsChannelMappingAudOutpCh6:
        sig_name = "AlarmsChannelMappingAudOutpCh6"
        sig_start_bit = 2
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class FgrndChannelMappingAudOutpCh6:
        sig_name = "FgrndChannelMappingAudOutpCh6"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AlarmsChannelMappingAudOutpCh7:
        sig_name = "AlarmsChannelMappingAudOutpCh7"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class TtsChannelMappingAudOutpCh9:
        sig_name = "TtsChannelMappingAudOutpCh9"
        sig_start_bit = 87
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 87
        byte = 10
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class TtsChannelMappingAudOutpCh12:
        sig_name = "TtsChannelMappingAudOutpCh12"
        sig_start_bit = 84
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 84
        byte = 10
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BgrndChannelMappingAudOutpCh10:
        sig_name = "BgrndChannelMappingAudOutpCh10"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BgrndChannelMappingAudOutpCh3:
        sig_name = "BgrndChannelMappingAudOutpCh3"
        sig_start_bit = 29
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AlarmsChannelMappingAudOutpCh5:
        sig_name = "AlarmsChannelMappingAudOutpCh5"
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
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class FgrndChannelMappingAudOutpCh10:
        sig_name = "FgrndChannelMappingAudOutpCh10"
        sig_start_bit = 62
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class TtsChannelMappingAudOutpCh11:
        sig_name = "TtsChannelMappingAudOutpCh11"
        sig_start_bit = 85
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 85
        byte = 10
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BgrndChannelMappingAudOutpCh13:
        sig_name = "BgrndChannelMappingAudOutpCh13"
        sig_start_bit = 35
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndEqFreq6:
        sig_name = "BgrndEqFreq6"
        sig_start_bit = 159
        update_id_bit = 173
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 159
        byte = 19
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class AlarmsChannelMappingAudOutpCh14:
        sig_name = "AlarmsChannelMappingAudOutpCh14"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FgrndChannelMappingAudOutpCh11:
        sig_name = "FgrndChannelMappingAudOutpCh11"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class ClearSound:
        sig_name = "ClearSound"
        sig_start_bit = 112
        update_id_bit = 171
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 112
        byte = 14
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BgrndEqFreq2:
        sig_name = "BgrndEqFreq2"
        sig_start_bit = 127
        update_id_bit = 152
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 10
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 127
        byte = 15
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class BgrndChannelMappingAudOutpCh8:
        sig_name = "BgrndChannelMappingAudOutpCh8"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class EssModeStsReq:
        sig_name = "EssModeStsReq"
        sig_start_bit = 122
        update_id_bit = 170
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerMod_Ukwn': 0, 'SteerMod_Mod1': 1, 'SteerMod_Mod2': 2, 'SteerMod_Mod3': 3, 'SteerMod_Mod4': 4, 'SteerMod_Resd5': 5, 'SteerMod_Resd6': 6, 'SteerMod_Resd7': 7}
        compute_method = None
        length = 3
        startbit = 122
        byte = 15
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class BgrndChannelMapping_UB:
        sig_name = "BgrndChannelMapping_UB"
        sig_start_bit = 40
        update_id_bit = 40
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AlarmsChannelMappingAudOutpCh11:
        sig_name = "AlarmsChannelMappingAudOutpCh11"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class BgrndChannelMappingAudOutpCh14:
        sig_name = "BgrndChannelMappingAudOutpCh14"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class AlarmsChannelMapping_UB:
        sig_name = "AlarmsChannelMapping_UB"
        sig_start_bit = 16
        update_id_bit = 16
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SurroundLvlFor2D:
        sig_name = "SurroundLvlFor2D"
        sig_start_bit = 146
        update_id_bit = 181
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SurroundLvl_low': 0, 'SurroundLvl_mid': 1, 'SurroundLvl_high': 2}
        compute_method = None
        length = 2
        startbit = 146
        byte = 18
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class FgrndChannelMappingAudOutpCh9:
        sig_name = "FgrndChannelMappingAudOutpCh9"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BgrndChannelMappingAudOutpCh2:
        sig_name = "BgrndChannelMappingAudOutpCh2"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SurroundType:
        sig_name = "SurroundType"
        sig_start_bit = 162
        update_id_bit = 179
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SurroundType_off': 0, 'SurroundType_2D_surround': 1, 'SurroundType_3D_surround': 2}
        compute_method = None
        length = 2
        startbit = 162
        byte = 20
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class TtsChannelMappingAudOutpCh4:
        sig_name = "TtsChannelMappingAudOutpCh4"
        sig_start_bit = 76
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 76
        byte = 9
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class IhuDhuInfoCanFr13:
    msg_name = "IhuDhuInfoCanFr13"
    msg_id = 20
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']
    sig_group_dict = {'WhlMotSysTqEst': ['WhlMotSysTqEstChks', 'WhlMotSysTqEstCntr', 'WhlMotSysTqEstIsgTqAct', 'WhlMotSysTqEstQualityFactor']}
    sig_group_dataid_dict = {'WhlMotSysTqEst': 69}

    class WhlMotSysTqEstIsgTqAct:
        sig_name = "WhlMotSysTqEstIsgTqAct"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 14
        sig_value_factor = 1
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 8188
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111100, 0b00000011, 6, 2)]

    class WhlMotSysIdc:
        sig_name = "WhlMotSysIdc"
        sig_start_bit = 37
        update_id_bit = 38
        sig_length = 14
        sig_value_factor = 0.1
        sig_value_offset = -818.8
        sig_value_min = 0
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 8188
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 37
        bmuws_info = [(4, 0b00111111, 0b11000000, 6, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotSysTqEstChks:
        sig_name = "WhlMotSysTqEstChks"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMotSysTqEst_UB:
        sig_name = "WhlMotSysTqEst_UB"
        sig_start_bit = 27
        update_id_bit = 27
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class WhlMotSysTqEstCntr:
        sig_name = "WhlMotSysTqEstCntr"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WhlMotSysTqEstQualityFactor:
        sig_name = "WhlMotSysTqEstQualityFactor"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'QualityFactor_QfUndefd': 0, 'QualityFactor_QfInProgs': 1, 'QualityFactor_QfNotSpc': 2, 'QualityFactor_QfSnsrDataOk': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class CDCPrivateInfoCANFDFr02:
    msg_name = "CDCPrivateInfoCANFDFr02"
    msg_id = 528
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 32
    tx_node = "CDC"
    rx_nodes = ['CD']
    sig_group_dict = {'GearIndcn': ['GearIndcnChks', 'GearIndcnCntr', 'GearIndcnGearIndcn'], 'GearIndcnCheckSts': ['GearIndcnCheckStsChks', 'GearIndcnCheckStsCntr', 'GearIndcnCheckStsGearIndcnCheckSts'], 'GearIndcnQosSts': ['GearIndcnQosStsChks', 'GearIndcnQosStsCntr', 'GearIndcnQosStsGearIndcnQosSts']}
    sig_group_dataid_dict = {'GearIndcn': 8049, 'GearIndcnCheckSts': 8062, 'GearIndcnQosSts': 8073}

    class GearIndcnChks:
        sig_name = "GearIndcnChks"
        sig_start_bit = 135
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 135
        byte = 16
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GearIndcnCntr:
        sig_name = "GearIndcnCntr"
        sig_start_bit = 143
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 143
        byte = 17
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class GearIndcnQosStsGearIndcnQosSts:
        sig_name = "GearIndcnQosStsGearIndcnQosSts"
        sig_start_bit = 171
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OK': 0, 'Not_OK': 1}
        compute_method = None
        length = 1
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GearIndcnCheckStsCntr:
        sig_name = "GearIndcnCheckStsCntr"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 159
        byte = 19
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class GearIndcn_UB:
        sig_name = "GearIndcn_UB"
        sig_start_bit = 136
        update_id_bit = 136
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 136
        byte = 17
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class GearIndcnCheckStsChks:
        sig_name = "GearIndcnCheckStsChks"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GearIndcnCheckSts_UB:
        sig_name = "GearIndcnCheckSts_UB"
        sig_start_bit = 152
        update_id_bit = 152
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 152
        byte = 19
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class GearIndcnGearIndcn:
        sig_name = "GearIndcnGearIndcn"
        sig_start_bit = 139
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearIndcn_P': 0, 'GearIndcn_R': 1, 'GearIndcn_N': 2, 'GearIndcn_D': 3, 'GearIndcn_Reserve1': 4, 'GearIndcn_Reserve2': 5, 'GearIndcn_Reserve3': 6, 'GearIndcn_Invalid': 7}
        compute_method = None
        length = 3
        startbit = 139
        byte = 17
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class GearIndcnCheckStsGearIndcnCheckSts:
        sig_name = "GearIndcnCheckStsGearIndcnCheckSts"
        sig_start_bit = 155
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OK': 0, 'Not_OK': 1}
        compute_method = None
        length = 1
        startbit = 155
        byte = 19
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GearIndcnQosStsCntr:
        sig_name = "GearIndcnQosStsCntr"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 175
        byte = 21
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class GearIndcnQosStsChks:
        sig_name = "GearIndcnQosStsChks"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 167
        byte = 20
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GearIndcnQosSts_UB:
        sig_name = "GearIndcnQosSts_UB"
        sig_start_bit = 168
        update_id_bit = 168
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class CDCPrivateInfoCANFDFr01:
    msg_name = "CDCPrivateInfoCANFDFr01"
    msg_id = 512
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 32
    tx_node = "CDC"
    rx_nodes = ['CD']
    sig_group_dict = {'CDCFltSts': ['CDCFltStsCDCFltSts', 'CDCFltStsChks', 'CDCFltStsCntr'], 'CDCSafeEnable': ['CDCSafeEnableCDCSafeEnable', 'CDCSafeEnableChks', 'CDCSafeEnableCntr']}
    sig_group_dataid_dict = {'CDCFltSts': 8060, 'CDCSafeEnable': 8055}

    class CDCFltStsCDCFltSts:
        sig_name = "CDCFltStsCDCFltSts"
        sig_start_bit = 155
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CDCFltSts_No_fault': 0, 'CDCFltSts_Fault': 1, 'CDCFltSts_Serializer_fault': 2, 'CDCFltSts_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 155
        byte = 19
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CDCFltStsChks:
        sig_name = "CDCFltStsChks"
        sig_start_bit = 151
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 151
        byte = 18
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDCFltStsCntr:
        sig_name = "CDCFltStsCntr"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 159
        byte = 19
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CDCFltSts_UB:
        sig_name = "CDCFltSts_UB"
        sig_start_bit = 152
        update_id_bit = 152
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 152
        byte = 19
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CDCSafeEnableChks:
        sig_name = "CDCSafeEnableChks"
        sig_start_bit = 167
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 167
        byte = 20
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDCSafeEnable_UB:
        sig_name = "CDCSafeEnable_UB"
        sig_start_bit = 168
        update_id_bit = 168
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 168
        byte = 21
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CDCSafeEnableCDCSafeEnable:
        sig_name = "CDCSafeEnableCDCSafeEnable"
        sig_start_bit = 171
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 171
        byte = 21
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CDCSafeEnableCntr:
        sig_name = "CDCSafeEnableCntr"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 175
        byte = 21
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class AUDInfoCanFr07:
    msg_name = "AUDInfoCanFr07"
    msg_id = 33
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "AUD"
    rx_nodes = ['CDC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class AllmuteSts:
        sig_name = "AllmuteSts"
        sig_start_bit = 54
        update_id_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Unmute': 0, 'mute': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class CDPrivateInfoCANFDFr02:
    msg_name = "CDPrivateInfoCANFDFr02"
    msg_id = 1109
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 8.0
    msg_length = 16
    tx_node = "CD"
    rx_nodes = ['CDC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CDManufcter:
        sig_name = "CDManufcter"
        sig_start_bit = 7
        update_id_bit = 1
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
        startbit = 7
        byte = 0
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class SwDomainCode:
        sig_name = "SwDomainCode"
        sig_start_bit = 39
        update_id_bit = 79
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SwVersionCode:
        sig_name = "SwVersionCode"
        sig_start_bit = 63
        update_id_bit = 75
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 6565
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 63
        bmuws_info = [(7, 0b11111111, 0b00000000, 8, 0), (8, 0b11111111, 0b00000000, 8, 0)]

    class SwSuplerCode:
        sig_name = "SwSuplerCode"
        sig_start_bit = 35
        update_id_bit = 77
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CDFps:
        sig_name = "CDFps"
        sig_start_bit = 95
        update_id_bit = 73
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FPS_60fps': 0, 'FPS_30fps': 1, 'FPS_Reserve1': 2, 'FPS_Reserve2': 3, 'FPS_Reserve3': 4, 'FPS_Reserve4': 5, 'FPS_Reserve5': 6, 'FPS_Reserve6': 7, 'FPS_Reserve7': 8, 'FPS_Reserve8': 9, 'FPS_Reserve9': 10, 'FPS_Reserve10': 11, 'FPS_Reserve11': 12, 'FPS_Reserve12': 13, 'FPS_Reserve13': 14, 'FPS_Reserve14': 15}
        compute_method = None
        length = 4
        startbit = 95
        byte = 11
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CDDpi:
        sig_name = "CDDpi"
        sig_start_bit = 87
        update_id_bit = 74
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
        startbit = 87
        byte = 10
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class SwBaseLineCode:
        sig_name = "SwBaseLineCode"
        sig_start_bit = 23
        update_id_bit = 8
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 5
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class SampleType:
        sig_name = "SampleType"
        sig_start_bit = 11
        update_id_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Type2_A_Sample': 0, 'Type2_B_Sample': 1, 'Type2_C_Sample': 2, 'Type2_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SwTypeCode:
        sig_name = "SwTypeCode"
        sig_start_bit = 55
        update_id_bit = 76
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 19
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HwVersion:
        sig_name = "HwVersion"
        sig_start_bit = 15
        update_id_bit = 0
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HwVersion_Invalid': 0, 'HwVersion_1': 1, 'HwVersion_2': 2, 'HwVersion_3': 3, 'HwVersion_4': 4, 'HwVersion_5': 5, 'HwVersion_6': 6, 'HwVersion_7': 7, 'HwVersion_8': 8, 'HwVersion_9': 9, 'HwVersion_10': 10, 'HwVersion_11': 11, 'HwVersion_12': 12, 'HwVersion_13': 13, 'HwVersion_14': 14, 'HwVersion_15': 15}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SwECUCode:
        sig_name = "SwECUCode"
        sig_start_bit = 47
        update_id_bit = 78
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class AudToCdcInfoCanDiagRespFrame:
    msg_name = "AudToCdcInfoCanDiagRespFrame"
    msg_id = 1664
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "AUD"
    rx_nodes = ['CDC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CdcToAudInfoCanDiagReqFrame:
    msg_name = "CdcToAudInfoCanDiagReqFrame"
    msg_id = 1920
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CDC"
    rx_nodes = ['AUD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IhuDhuInfoCanFr21:
    msg_name = "IhuDhuInfoCanFr21"
    msg_id = 362
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD', 'CD']
    sig_group_dict = {'VehBattU': ['VehBattUSysU', 'VehBattUSysUQf']}
    sig_group_dataid_dict = {}

    class VehBattUSysU:
        sig_name = "VehBattUSysU"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehBattU_UB:
        sig_name = "VehBattU_UB"
        sig_start_bit = 26
        update_id_bit = 26
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VehBattUSysUQf:
        sig_name = "VehBattUSysUQf"
        sig_start_bit = 25
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class DhuInfoCanFr08:
    msg_name = "DhuInfoCanFr08"
    msg_id = 399
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class Allmute:
        sig_name = "Allmute"
        sig_start_bit = 47
        update_id_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Unmute': 0, 'mute': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CdcToCenterDisplayPrivateInfoCanDiagReqFrame:
    msg_name = "CdcToCenterDisplayPrivateInfoCanDiagReqFrame"
    msg_id = 1921
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 64
    tx_node = "CDC"
    rx_nodes = ['CD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IhuDhuInfoCanFr10:
    msg_name = "IhuDhuInfoCanFr10"
    msg_id = 32
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD', 'CD']
    sig_group_dict = {'VehSpdLgt': ['VehSpdLgtA', 'VehSpdLgtChks', 'VehSpdLgtCntr', 'VehSpdLgtQf']}
    sig_group_dataid_dict = {'VehSpdLgt': 55}

    class VehSpdLgtCntr:
        sig_name = "VehSpdLgtCntr"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehSpdLgt_UB:
        sig_name = "VehSpdLgt_UB"
        sig_start_bit = 39
        update_id_bit = 39
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehSpdLgtQf:
        sig_name = "VehSpdLgtQf"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VehSpdLgtChks:
        sig_name = "VehSpdLgtChks"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehSpdLgtA:
        sig_name = "VehSpdLgtA"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 31970
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class IhuDhuInfoCanFr07:
    msg_name = "IhuDhuInfoCanFr07"
    msg_id = 344
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class AudPowerMode:
        sig_name = "AudPowerMode"
        sig_start_bit = 19
        update_id_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AudPowerMode_Off': 0, 'AudPowerMode_Standby': 1, 'AudPowerMode_Full': 2}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class IhuDhuInfoCanFr08:
    msg_name = "IhuDhuInfoCanFr08"
    msg_id = 849
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD', 'CD']
    sig_group_dict = {'VehModMngtGlbSafe1': ['VehModMngtGlbSafe1CarModSts1', 'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp', 'VehModMngtGlbSafe1Chks', 'VehModMngtGlbSafe1Cntr', 'VehModMngtGlbSafe1EgyLvlElecMai', 'VehModMngtGlbSafe1EgyLvlElecSubtyp', 'VehModMngtGlbSafe1FltEgyCnsWdSts', 'VehModMngtGlbSafe1PwrLvlElecMai', 'VehModMngtGlbSafe1PwrLvlElecSubtyp', 'VehModMngtGlbSafe1UsgModSts']}
    sig_group_dataid_dict = {'VehModMngtGlbSafe1': 116}

    class VehModMngtGlbSafe1EgyLvlElecMai:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1Chks:
        sig_name = "VehModMngtGlbSafe1Chks"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehModMngtGlbSafe1Cntr:
        sig_name = "VehModMngtGlbSafe1Cntr"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 36
        byte = 4
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class VehModMngtGlbSafe1_UB:
        sig_name = "VehModMngtGlbSafe1_UB"
        sig_start_bit = 32
        update_id_bit = 32
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VehModMngtGlbSafe1CarModSts1:
        sig_name = "VehModMngtGlbSafe1CarModSts1"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarModSts1_CarModNorm': 0, 'CarModSts1_CarModTrnsp': 1, 'CarModSts1_CarModFcy': 2, 'CarModSts1_CarModCrash': 3, 'CarModSts1_CarModDyno': 5}
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class VehModMngtGlbSafe1PwrLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehModMngtGlbSafe1FltEgyCnsWdSts:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltEgyCns1_NoFlt': 0, 'FltEgyCns1_Flt': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VehModMngtGlbSafe1UsgModSts:
        sig_name = "VehModMngtGlbSafe1UsgModSts"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'UsgModSts1_UsgModAbdnd': 0, 'UsgModSts1_UsgModInActv': 1, 'UsgModSts1_UsgModCnvinc': 2, 'UsgModSts1_UsgModActv': 11, 'UsgModSts1_UsgModDrvg': 13}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1PwrLvlElecMai:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1EgyLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CenterDisplayPrivateInfoCANNmFr:
    msg_name = "CenterDisplayPrivateInfoCANNmFr"
    msg_id = 1282
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CD"
    rx_nodes = ['CDC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DhuInfoCanFr05:
    msg_name = "DhuInfoCanFr05"
    msg_id = 398
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']
    sig_group_dict = {'BrkPedlrRat': ['BrkPedlrRatPerc', 'BrkPedlrRatQf']}
    sig_group_dataid_dict = {}

    class BrkPedlrRatQf:
        sig_name = "BrkPedlrRatQf"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BrkPedlrRatPerc:
        sig_name = "BrkPedlrRatPerc"
        sig_start_bit = 30
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 25600
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 30
        bmuws_info = [(3, 0b01111111, 0b10000000, 7, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class BrkPedlrRat_UB:
        sig_name = "BrkPedlrRat_UB"
        sig_start_bit = 45
        update_id_bit = 45
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class CDCPrivateInfoCANFDFr03:
    msg_name = "CDCPrivateInfoCANFDFr03"
    msg_id = 544
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 32
    tx_node = "CDC"
    rx_nodes = ['AUD']
    sig_group_dict = {'WhlMotSysSpdActSafe800': ['WhlMotSysSpdActSafe800Chks', 'WhlMotSysSpdActSafe800Cntr', 'WhlMotSysSpdActSafe800IsgSpdActSgn800', 'WhlMotSysSpdActSafe800Qf'], 'WhlMotSysSpdActSafe': ['WhlMotSysSpdActSafeChks', 'WhlMotSysSpdActSafeCntr', 'WhlMotSysSpdActSafeIsgSpdWSgnTyp', 'WhlMotSysSpdActSafeQf']}
    sig_group_dataid_dict = {'WhlMotSysSpdActSafe800': 7002, 'WhlMotSysSpdActSafe': 7001}

    class WhlMotSysSpdActSafe800_UB:
        sig_name = "WhlMotSysSpdActSafe800_UB"
        sig_start_bit = 204
        update_id_bit = 204
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 204
        byte = 25
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WhlMotSysSpdActSafeQf:
        sig_name = "WhlMotSysSpdActSafeQf"
        sig_start_bit = 191
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 191
        byte = 23
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlMotSysSpdActSafe800IsgSpdActSgn800:
        sig_name = "WhlMotSysSpdActSafe800IsgSpdActSgn800"
        sig_start_bit = 215
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -32768
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 215
        bmuws_info = [(26, 0b11111111, 0b00000000, 8, 0), (27, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotSysSpdActSafeCntr:
        sig_name = "WhlMotSysSpdActSafeCntr"
        sig_start_bit = 163
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 163
        byte = 20
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class WhlMotSysSpdActSafeIsgSpdWSgnTyp:
        sig_name = "WhlMotSysSpdActSafeIsgSpdWSgnTyp"
        sig_start_bit = 175
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16383
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 175
        bmuws_info = [(21, 0b11111111, 0b00000000, 8, 0), (22, 0b11111110, 0b00000001, 7, 1)]

    class WhlMotSysSpdActSafe800Chks:
        sig_name = "WhlMotSysSpdActSafe800Chks"
        sig_start_bit = 199
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 199
        byte = 24
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMotSysSpdActSafe800Cntr:
        sig_name = "WhlMotSysSpdActSafe800Cntr"
        sig_start_bit = 203
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 203
        byte = 25
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class WhlMotSysSpdActSafe800Qf:
        sig_name = "WhlMotSysSpdActSafe800Qf"
        sig_start_bit = 207
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 207
        byte = 25
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WhlMotSysSpdActSafeChks:
        sig_name = "WhlMotSysSpdActSafeChks"
        sig_start_bit = 159
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 159
        byte = 19
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMotSysSpdActSafe_UB:
        sig_name = "WhlMotSysSpdActSafe_UB"
        sig_start_bit = 188
        update_id_bit = 188
        sig_length = 1
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 1
        startbit = 188
        byte = 23
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class CDCPrivateInfoCANFDFr04:
    msg_name = "CDCPrivateInfoCANFDFr04"
    msg_id = 800
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD', 'CD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EssDrivingMode:
        sig_name = "EssDrivingMode"
        sig_start_bit = 23
        update_id_bit = 19
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvModReqType1_Undefd': 0, 'DrvModReqType1_ECO': 1, 'DrvModReqType1_Comfort_Normal': 2, 'DrvModReqType1_Dynamic_Sport': 3, 'DrvModReqType1_Reserved1': 4, 'DrvModReqType1_Offroad_CrossTerrain': 5, 'DrvModReqType1_Adaptive': 6, 'DrvModReqType1_Race': 7, 'DrvModReqType1_Reserved2': 8, 'DrvModReqType1_ECO_PLUS': 9, 'DrvModReqType1_Power': 10, 'DrvModReqType1_Snow': 11, 'DrvModReqType1_Sand': 12, 'DrvModReqType1_Mud': 13, 'DrvModReqType1_Rock': 14, 'DrvModReqType1_Err': 15}
        compute_method = None
        length = 4
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CDDispErrProcess:
        sig_name = "CDDispErrProcess"
        sig_start_bit = 31
        update_id_bit = 32
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CDDispErrProcess_Waiting': 0, 'CDDispErrProcess_Log_Collecting': 1, 'CDDispErrProcess_Reseting': 2, 'CDDispErrProcess_Reserved': 3}
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DisplayAreaCtrl:
        sig_name = "DisplayAreaCtrl"
        sig_start_bit = 5
        update_id_bit = 2
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'All_Off': 0, 'All_On': 1, 'Only_Cluster_On': 2, 'Only_Entertainment_On': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CDCDisplayMode:
        sig_name = "CDCDisplayMode"
        sig_start_bit = 7
        update_id_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CDCDisplayMode_Daymode': 0, 'CDCDisplayMode_Nightmode': 1, 'CDCDisplayMode_Nosetting': 2, 'CDCDisplayMode_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LuminanceLevelReq:
        sig_name = "LuminanceLevelReq"
        sig_start_bit = 15
        update_id_bit = 1
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


