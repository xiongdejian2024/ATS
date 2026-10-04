class CdcToCenterDisplayPrivateInfoCanDiagReqFrame:
    msg_name = "CdcToCenterDisplayPrivateInfoCanDiagReqFrame"
    msg_id = 1921
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['CD']


class CenterDisplayPrivateInfoCANNmFr:
    msg_name = "CenterDisplayPrivateInfoCANNmFr"
    msg_id = 1282
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CD"
    rx_nodes = ['CDC']


class CDCPrivateInfoCANFDFr05:
    msg_name = "CDCPrivateInfoCANFDFr05"
    msg_id = 1376
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']

    class VolLvlBgrnd1:
        sig_name = "VolLvlBgrnd1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 16
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class DhuInfoCanFr08:
    msg_name = "DhuInfoCanFr08"
    msg_id = 399
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']

    class Allmute:
        sig_name = "Allmute"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CdcToAudInfoCanDiagReqFrame:
    msg_name = "CdcToAudInfoCanDiagReqFrame"
    msg_id = 1920
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']


class CDCPrivateInfoCANFDFr03:
    msg_name = "CDCPrivateInfoCANFDFr03"
    msg_id = 544
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['CD']

    class TakeOverLampCheckStsTakeOverLampCheckSts:
        sig_name = "TakeOverLampCheckStsTakeOverLampCheckSts"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TakeOverLampQosStsCntr:
        sig_name = "TakeOverLampQosStsCntr"
        sig_start_bit = 63
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

    class TakeOverLampQosStsChks:
        sig_name = "TakeOverLampQosStsChks"
        sig_start_bit = 55
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

    class TakeOverLampTakeOverLamp:
        sig_name = "TakeOverLampTakeOverLamp"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TakeOverLampCntr:
        sig_name = "TakeOverLampCntr"
        sig_start_bit = 31
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

    class MarsDriverLampQosStsChks:
        sig_name = "MarsDriverLampQosStsChks"
        sig_start_bit = 7
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

    class TakeOverLampCheckStsChks:
        sig_name = "TakeOverLampCheckStsChks"
        sig_start_bit = 39
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

    class TakeOverLampCheckStsCntr:
        sig_name = "TakeOverLampCheckStsCntr"
        sig_start_bit = 47
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

    class MarsDriverLampQosStsMarsDriverLampQosSts:
        sig_name = "MarsDriverLampQosStsMarsDriverLampQosSts"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TakeOverLampChks:
        sig_name = "TakeOverLampChks"
        sig_start_bit = 23
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

    class TakeOverLampQosStsTakeOverLampQosSts:
        sig_name = "TakeOverLampQosStsTakeOverLampQosSts"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class MarsDriverLampQosStsCntr:
        sig_name = "MarsDriverLampQosStsCntr"
        sig_start_bit = 15
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


class CDPrivateInfoCANFDFr03:
    msg_name = "CDPrivateInfoCANFDFr03"
    msg_id = 96
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "CD"
    rx_nodes = ['CDC']

    class TouchStsChks:
        sig_name = "TouchStsChks"
        sig_start_bit = 55
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

    class CDVoltageStsCntr:
        sig_name = "CDVoltageStsCntr"
        sig_start_bit = 15
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

    class ScreenStsScreenSts:
        sig_name = "ScreenStsScreenSts"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Normal': 0, 'Fault': 1, 'Reserve1': 2, 'Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class TouchStsTouchSts:
        sig_name = "TouchStsTouchSts"
        sig_start_bit = 59
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Normal': 0, 'Fault': 1, 'Reserve1': 2, 'Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class TouchStsCntr:
        sig_name = "TouchStsCntr"
        sig_start_bit = 63
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

    class DimStsChks:
        sig_name = "DimStsChks"
        sig_start_bit = 23
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

    class CDVoltageStsCDVoltageSts:
        sig_name = "CDVoltageStsCDVoltageSts"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Normal': 0, 'Overvoltage': 1, 'Undervoltage': 2, 'Reserve': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DimStsCntr:
        sig_name = "DimStsCntr"
        sig_start_bit = 31
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

    class ScreenStsCntr:
        sig_name = "ScreenStsCntr"
        sig_start_bit = 47
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

    class CDVoltageStsChks:
        sig_name = "CDVoltageStsChks"
        sig_start_bit = 7
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

    class ScreenStsChks:
        sig_name = "ScreenStsChks"
        sig_start_bit = 39
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

    class DimStsDimSts:
        sig_name = "DimStsDimSts"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Normal': 0, 'Fault': 1, 'Reserve1': 2, 'Reserve2': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class CenterDisplayToCdcPrivateInfoCanDiagRespFrame:
    msg_name = "CenterDisplayToCdcPrivateInfoCanDiagRespFrame"
    msg_id = 1665
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CD"
    rx_nodes = ['CDC']


class DhuInfoCanFr07:
    msg_name = "DhuInfoCanFr07"
    msg_id = 379
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']

    class AmplifrTurnOn:
        sig_name = "AmplifrTurnOn"
        sig_start_bit = 6
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


class IhuDhuInfoCanFr02:
    msg_name = "IhuDhuInfoCanFr02"
    msg_id = 913
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']

    class VolLvlBgrnd:
        sig_name = "VolLvlBgrnd"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 16
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class AudToCdcInfoCanDiagRespFrame:
    msg_name = "AudToCdcInfoCanDiagRespFrame"
    msg_id = 1664
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "AUD"
    rx_nodes = ['CDC']


class CDCPrivateInfoCANFDFr04:
    msg_name = "CDCPrivateInfoCANFDFr04"
    msg_id = 800
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['CD']

    class CDCDisplayMode:
        sig_name = "CDCDisplayMode"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Daymode': 0, 'Nightmode': 1, 'Nosetting': 2, 'Reserve': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DisplayAreaCtrl:
        sig_name = "DisplayAreaCtrl"
        sig_start_bit = 5
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

    class LuminanceLevelReq:
        sig_name = "LuminanceLevelReq"
        sig_start_bit = 15
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


class CDPrivateInfoCANFDFr02:
    msg_name = "CDPrivateInfoCANFDFr02"
    msg_id = 1109
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 8.0
    msg_length = 16
    tx_node = "CD"
    rx_nodes = ['CDC']

    class SwDomainCode:
        sig_name = "SwDomainCode"
        sig_start_bit = 39
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

    class SampleType:
        sig_name = "SampleType"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'A_Sample': 0, 'B_Sample': 1, 'C_Sample': 2, 'Reserve': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SwSuplerCode:
        sig_name = "SwSuplerCode"
        sig_start_bit = 35
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

    class SwVersionCode:
        sig_name = "SwVersionCode"
        sig_start_bit = 63
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

    class SwTypeCode:
        sig_name = "SwTypeCode"
        sig_start_bit = 55
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

    class CDFps:
        sig_name = "CDFps"
        sig_start_bit = 95
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

    class HwVersion:
        sig_name = "HwVersion"
        sig_start_bit = 15
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

    class SwBaseLineCode:
        sig_name = "SwBaseLineCode"
        sig_start_bit = 23
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

    class SwECUCode:
        sig_name = "SwECUCode"
        sig_start_bit = 47
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

    class CDManufcter:
        sig_name = "CDManufcter"
        sig_start_bit = 7
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


class AUDInfoCanFr03:
    msg_name = "AUDInfoCanFr03"
    msg_id = 944
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "AUD"
    rx_nodes = ['CDC']

    class OutChState2:
        sig_name = "OutChState2"
        sig_start_bit = 23
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

    class OutChState1:
        sig_name = "OutChState1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BgrndForVolLvlSts:
        sig_name = "BgrndForVolLvlSts"
        sig_start_bit = 47
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


class CDCPrivateInfoCANFDFr01:
    msg_name = "CDCPrivateInfoCANFDFr01"
    msg_id = 512
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 32
    tx_node = "CDC"
    rx_nodes = ['CD']

    class ChildLockLampQosStsChildLockLampQosSts:
        sig_name = "ChildLockLampQosStsChildLockLampQosSts"
        sig_start_bit = 219
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
        startbit = 219
        byte = 27
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BrakeRedLampCntr:
        sig_name = "BrakeRedLampCntr"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ECSWarnLampQosStsCntr:
        sig_name = "ECSWarnLampQosStsCntr"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ECSWarnLampQosStsECSWarnLampQosSts:
        sig_name = "ECSWarnLampQosStsECSWarnLampQosSts"
        sig_start_bit = 235
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
        startbit = 235
        byte = 29
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AirbagLampQosStsCntr:
        sig_name = "AirbagLampQosStsCntr"
        sig_start_bit = 95
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
        startbit = 95
        byte = 11
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CDCFltStsChks:
        sig_name = "CDCFltStsChks"
        sig_start_bit = 151
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

    class AirbagLampCntr:
        sig_name = "AirbagLampCntr"
        sig_start_bit = 63
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

    class BrakeRedLampQosStsChks:
        sig_name = "BrakeRedLampQosStsChks"
        sig_start_bit = 135
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

    class BrakeRedLampQosStsCntr:
        sig_name = "BrakeRedLampQosStsCntr"
        sig_start_bit = 143
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

    class BrakeRedLampQosStsBrakeRedLampQosSts:
        sig_name = "BrakeRedLampQosStsBrakeRedLampQosSts"
        sig_start_bit = 139
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
        startbit = 139
        byte = 17
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ChildLockLampCntr:
        sig_name = "ChildLockLampCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ChildLockLampQosStsChks:
        sig_name = "ChildLockLampQosStsChks"
        sig_start_bit = 215
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
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BrakeRedLampBrakeRedLamp:
        sig_name = "BrakeRedLampBrakeRedLamp"
        sig_start_bit = 107
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
        startbit = 107
        byte = 13
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ECSWarnLampQosStsChks:
        sig_name = "ECSWarnLampQosStsChks"
        sig_start_bit = 231
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
        startbit = 231
        byte = 28
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ABSLampQosStsChks:
        sig_name = "ABSLampQosStsChks"
        sig_start_bit = 39
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

    class ChildLockLampChks:
        sig_name = "ChildLockLampChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ABSLampCntr:
        sig_name = "ABSLampCntr"
        sig_start_bit = 15
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

    class AirbagLampChks:
        sig_name = "AirbagLampChks"
        sig_start_bit = 55
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

    class ChildLockLampChildLockLamp:
        sig_name = "ChildLockLampChildLockLamp"
        sig_start_bit = 187
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
        startbit = 187
        byte = 23
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AirbagLampCheckStsCntr:
        sig_name = "AirbagLampCheckStsCntr"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class BrakeRedLampCheckStsChks:
        sig_name = "BrakeRedLampCheckStsChks"
        sig_start_bit = 119
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
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ABSLampQosStsCntr:
        sig_name = "ABSLampQosStsCntr"
        sig_start_bit = 47
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

    class CDCSafeEnableCDCSafeEnable:
        sig_name = "CDCSafeEnableCDCSafeEnable"
        sig_start_bit = 171
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

    class CDCSafeEnableChks:
        sig_name = "CDCSafeEnableChks"
        sig_start_bit = 167
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

    class AirbagLampAirbagLamp:
        sig_name = "AirbagLampAirbagLamp"
        sig_start_bit = 59
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Off': 0, 'On': 1, 'Flash': 2, 'Reserve': 3}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CDCSafeEnableCntr:
        sig_name = "CDCSafeEnableCntr"
        sig_start_bit = 175
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

    class ChildLockLampCheckStsChildLockLampCheckSts:
        sig_name = "ChildLockLampCheckStsChildLockLampCheckSts"
        sig_start_bit = 203
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
        startbit = 203
        byte = 25
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AirbagLampCheckStsAirbagLampCheckSts:
        sig_name = "AirbagLampCheckStsAirbagLampCheckSts"
        sig_start_bit = 75
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
        startbit = 75
        byte = 9
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ABSLampQosStsABSLampQosSts:
        sig_name = "ABSLampQosStsABSLampQosSts"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BrakeRedLampCheckStsCntr:
        sig_name = "BrakeRedLampCheckStsCntr"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AirbagLampCheckStsChks:
        sig_name = "AirbagLampCheckStsChks"
        sig_start_bit = 71
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
        startbit = 71
        byte = 8
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ABSLampCheckStsABSLampCheckSts:
        sig_name = "ABSLampCheckStsABSLampCheckSts"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ChildLockLampQosStsCntr:
        sig_name = "ChildLockLampQosStsCntr"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ABSLampABSLamp:
        sig_name = "ABSLampABSLamp"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ABSLampCheckStsChks:
        sig_name = "ABSLampCheckStsChks"
        sig_start_bit = 23
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

    class ABSLampChks:
        sig_name = "ABSLampChks"
        sig_start_bit = 7
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

    class ChildLockLampCheckStsChks:
        sig_name = "ChildLockLampCheckStsChks"
        sig_start_bit = 199
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

    class CDCFltStsCntr:
        sig_name = "CDCFltStsCntr"
        sig_start_bit = 159
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

    class ChildLockLampCheckStsCntr:
        sig_name = "ChildLockLampCheckStsCntr"
        sig_start_bit = 207
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
        startbit = 207
        byte = 25
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AirbagLampQosStsAirbagLampQosSts:
        sig_name = "AirbagLampQosStsAirbagLampQosSts"
        sig_start_bit = 91
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
        startbit = 91
        byte = 11
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CDCFltStsCDCFltSts:
        sig_name = "CDCFltStsCDCFltSts"
        sig_start_bit = 155
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'No_fault': 0, 'Fault': 1, 'Serializer_fault': 2, 'Reserve': 3}
        compute_method = None
        length = 2
        startbit = 155
        byte = 19
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BrakeRedLampCheckStsBrakeRedLampCheckSts:
        sig_name = "BrakeRedLampCheckStsBrakeRedLampCheckSts"
        sig_start_bit = 123
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
        startbit = 123
        byte = 15
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BrakeRedLampChks:
        sig_name = "BrakeRedLampChks"
        sig_start_bit = 103
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
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ABSLampCheckStsCntr:
        sig_name = "ABSLampCheckStsCntr"
        sig_start_bit = 31
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

    class AirbagLampQosStsChks:
        sig_name = "AirbagLampQosStsChks"
        sig_start_bit = 87
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


class CDPrivateInfoCANFDFr01:
    msg_name = "CDPrivateInfoCANFDFr01"
    msg_id = 576
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 16
    tx_node = "CD"
    rx_nodes = ['CDC']

    class DisplayAreaSts:
        sig_name = "DisplayAreaSts"
        sig_start_bit = 34
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
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Unknow': 0, 'Start_up': 1, 'Shut_down': 2, 'Work_On': 3, 'Reserve1': 4, 'Reserve2': 5, 'Reserve3': 6, 'Reserve4': 7}
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CDTemp:
        sig_name = "CDTemp"
        sig_start_bit = 15
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 125
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 15
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class LVBattLampDispFedBck:
        sig_name = "LVBattLampDispFedBck"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalOff': 0, 'WrongOn': 1, 'NormalOn': 2, 'WrongOff': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LuminanceLevelFedBck:
        sig_name = "LuminanceLevelFedBck"
        sig_start_bit = 63
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

    class MarsDriverLampDispFedBck:
        sig_name = "MarsDriverLampDispFedBck"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalOff': 0, 'WrongOn': 1, 'NormalOn': 2, 'WrongOff': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ESCOffLampDispFedBck:
        sig_name = "ESCOffLampDispFedBck"
        sig_start_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalOff': 0, 'WrongOn': 1, 'NormalOn': 2, 'WrongOff': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AirbagLampDispFedBck:
        sig_name = "AirbagLampDispFedBck"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalOff': 0, 'WrongOn': 1, 'NormalOn': 2, 'WrongOff': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CDTempSts:
        sig_name = "CDTempSts"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempErr_Normal': 0, 'TempErr_OverTemp': 1, 'TempErr_UnderTemp': 2, 'TempErr_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TakeOverLampDispFedBck:
        sig_name = "TakeOverLampDispFedBck"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalOff': 0, 'WrongOn': 1, 'NormalOn': 2, 'WrongOff': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class GearDispFedBck:
        sig_name = "GearDispFedBck"
        sig_start_bit = 55
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

    class EPBLampDispFedBck:
        sig_name = "EPBLampDispFedBck"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalOff': 0, 'WrongOn': 1, 'NormalOn': 2, 'WrongOff': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CDVoltage:
        sig_name = "CDVoltage"
        sig_start_bit = 31
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

    class ChildLockLampDispFedBck:
        sig_name = "ChildLockLampDispFedBck"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalOff': 0, 'WrongOn': 1, 'NormalOn': 2, 'WrongOff': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class BrakeRedLampDispFedBck:
        sig_name = "BrakeRedLampDispFedBck"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalOff': 0, 'WrongOn': 1, 'NormalOn': 2, 'WrongOff': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ESCWarnLampDispFedBck:
        sig_name = "ESCWarnLampDispFedBck"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalOff': 0, 'WrongOn': 1, 'NormalOn': 2, 'WrongOff': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ABSLampDispFedBck:
        sig_name = "ABSLampDispFedBck"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NormalOff': 0, 'WrongOn': 1, 'NormalOn': 2, 'WrongOff': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CDDisplayModeFedBck:
        sig_name = "CDDisplayModeFedBck"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Daymode': 0, 'Nightmode': 1, 'Nosetting': 2, 'Reserve': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class AudPrivateInfoCANNmFr:
    msg_name = "AudPrivateInfoCANNmFr"
    msg_id = 1281
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "AUD"
    rx_nodes = ['CD']


class CdcPrivateInfoCANNmFr:
    msg_name = "CdcPrivateInfoCANNmFr"
    msg_id = 1339
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']


class AUDInfoCanFr07:
    msg_name = "AUDInfoCanFr07"
    msg_id = 33
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "AUD"
    rx_nodes = ['CDC']

    class AllmuteSts:
        sig_name = "AllmuteSts"
        sig_start_bit = 54
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


class IhuDhuInfoCanFr08:
    msg_name = "IhuDhuInfoCanFr08"
    msg_id = 849
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']

    class VehModMngtGlbSafe1FltEgyCnsWdSts_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 33
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

    class VehModMngtGlbSafe1EgyLvlElecSubtyp_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 23
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

    class VehModMngtGlbSafe1CarModSts1_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1CarModSts1_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 39
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

    class VehModMngtGlbSafe1Cntr_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1Cntr_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 15
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

    class VehModMngtGlbSafe1PwrLvlElecMai_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 19
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

    class VehModMngtGlbSafe1EgyLvlElecMai_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 11
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

    class VehModMngtGlbSafe1UsgModSts_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1UsgModSts_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 27
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

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 36
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

    class VehModMngtGlbSafe1PwrLvlElecSubtyp_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 31
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

    class VehModMngtGlbSafe1Chks_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1Chks_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 7
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


class IhuDhuInfoCanFr21:
    msg_name = "IhuDhuInfoCanFr21"
    msg_id = 362
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']

    class VehBattUSysUQf_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehBattUSysUQf_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 25
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

    class VehBattUSysU_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehBattUSysU_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 39
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


class AUDPrivateInfoCANFDFr10:
    msg_name = "AUDPrivateInfoCANFDFr10"
    msg_id = 1360
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "AUD"
    rx_nodes = ['CDC']

    class Bgrnd1ForVolLvlSts:
        sig_name = "Bgrnd1ForVolLvlSts"
        sig_start_bit = 7
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


class CDCPrivateInfoCANFDFr02:
    msg_name = "CDCPrivateInfoCANFDFr02"
    msg_id = 528
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 32
    tx_node = "CDC"
    rx_nodes = ['CD']

    class ESCWarnLampESCWarnLamp:
        sig_name = "ESCWarnLampESCWarnLamp"
        sig_start_bit = 107
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Off': 0, 'On': 1, 'Flash': 2, 'Reserve': 3}
        compute_method = None
        length = 2
        startbit = 107
        byte = 13
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ESCWarnLampCheckStsChks:
        sig_name = "ESCWarnLampCheckStsChks"
        sig_start_bit = 119
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
        startbit = 119
        byte = 14
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MarsDriverLampMarsDriverLamp:
        sig_name = "MarsDriverLampMarsDriverLamp"
        sig_start_bit = 235
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Off': 0, 'Standby': 1, 'Ready': 2, 'Active': 3}
        compute_method = None
        length = 2
        startbit = 235
        byte = 29
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EPBLampQosStsChks:
        sig_name = "EPBLampQosStsChks"
        sig_start_bit = 39
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

    class ESCOffLampQosStsChks:
        sig_name = "ESCOffLampQosStsChks"
        sig_start_bit = 87
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

    class ESCOffLampCheckStsChks:
        sig_name = "ESCOffLampCheckStsChks"
        sig_start_bit = 71
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
        startbit = 71
        byte = 8
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EPBLampCheckStsChks:
        sig_name = "EPBLampCheckStsChks"
        sig_start_bit = 23
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

    class GearIndcnCheckStsGearIndcnCheckSts:
        sig_name = "GearIndcnCheckStsGearIndcnCheckSts"
        sig_start_bit = 155
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

    class EPBLampQosStsEPBLampQosSts:
        sig_name = "EPBLampQosStsEPBLampQosSts"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EPBLampEPBLamp:
        sig_name = "EPBLampEPBLamp"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Off': 0, 'On': 1, 'Flash': 2, 'Reserve': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LVBattLampCheckStsCntr:
        sig_name = "LVBattLampCheckStsCntr"
        sig_start_bit = 207
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
        startbit = 207
        byte = 25
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ESCOffLampESCOffLamp:
        sig_name = "ESCOffLampESCOffLamp"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ESCOffLampQosStsCntr:
        sig_name = "ESCOffLampQosStsCntr"
        sig_start_bit = 95
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
        startbit = 95
        byte = 11
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EPBLampQosStsCntr:
        sig_name = "EPBLampQosStsCntr"
        sig_start_bit = 47
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

    class MarsDriverLampCheckStsMarsDriverLampCheckSts:
        sig_name = "MarsDriverLampCheckStsMarsDriverLampCheckSts"
        sig_start_bit = 251
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
        startbit = 251
        byte = 31
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GearIndcnGearIndcn:
        sig_name = "GearIndcnGearIndcn"
        sig_start_bit = 139
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'P': 0, 'R': 1, 'N': 2, 'D': 3, 'Reserve1': 4, 'Reserve2': 5, 'Reserve3': 6, 'Invalid': 7}
        compute_method = None
        length = 3
        startbit = 139
        byte = 17
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class MarsDriverLampCheckStsCntr:
        sig_name = "MarsDriverLampCheckStsCntr"
        sig_start_bit = 255
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
        startbit = 255
        byte = 31
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ESCWarnLampChks:
        sig_name = "ESCWarnLampChks"
        sig_start_bit = 103
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
        startbit = 103
        byte = 12
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ESCOffLampCheckStsCntr:
        sig_name = "ESCOffLampCheckStsCntr"
        sig_start_bit = 79
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
        startbit = 79
        byte = 9
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ESCWarnLampCheckStsESCWarnLampCheckSts:
        sig_name = "ESCWarnLampCheckStsESCWarnLampCheckSts"
        sig_start_bit = 123
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
        startbit = 123
        byte = 15
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GearIndcnCheckStsChks:
        sig_name = "GearIndcnCheckStsChks"
        sig_start_bit = 151
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

    class EPBLampCntr:
        sig_name = "EPBLampCntr"
        sig_start_bit = 15
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

    class LVBattLampQosStsCntr:
        sig_name = "LVBattLampQosStsCntr"
        sig_start_bit = 223
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
        startbit = 223
        byte = 27
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EPBLampCheckStsCntr:
        sig_name = "EPBLampCheckStsCntr"
        sig_start_bit = 31
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

    class ESCOffLampCntr:
        sig_name = "ESCOffLampCntr"
        sig_start_bit = 63
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

    class ESCOffLampChks:
        sig_name = "ESCOffLampChks"
        sig_start_bit = 55
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

    class LVBattLampCheckStsChks:
        sig_name = "LVBattLampCheckStsChks"
        sig_start_bit = 199
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

    class GearIndcnCheckStsCntr:
        sig_name = "GearIndcnCheckStsCntr"
        sig_start_bit = 159
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

    class MarsDriverLampCntr:
        sig_name = "MarsDriverLampCntr"
        sig_start_bit = 239
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
        startbit = 239
        byte = 29
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class GearIndcnQosStsCntr:
        sig_name = "GearIndcnQosStsCntr"
        sig_start_bit = 175
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

    class LVBattLampCntr:
        sig_name = "LVBattLampCntr"
        sig_start_bit = 191
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
        startbit = 191
        byte = 23
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class LVBattLampCheckStsLVBattLampCheckSts:
        sig_name = "LVBattLampCheckStsLVBattLampCheckSts"
        sig_start_bit = 203
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
        startbit = 203
        byte = 25
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class EPBLampChks:
        sig_name = "EPBLampChks"
        sig_start_bit = 7
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

    class GearIndcnChks:
        sig_name = "GearIndcnChks"
        sig_start_bit = 135
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

    class ESCOffLampQosStsESCOffLampQosSts:
        sig_name = "ESCOffLampQosStsESCOffLampQosSts"
        sig_start_bit = 91
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
        startbit = 91
        byte = 11
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GearIndcnQosStsGearIndcnQosSts:
        sig_name = "GearIndcnQosStsGearIndcnQosSts"
        sig_start_bit = 171
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

    class MarsDriverLampChks:
        sig_name = "MarsDriverLampChks"
        sig_start_bit = 231
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
        startbit = 231
        byte = 28
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MarsDriverLampCheckStsChks:
        sig_name = "MarsDriverLampCheckStsChks"
        sig_start_bit = 247
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
        startbit = 247
        byte = 30
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ESCWarnLampCntr:
        sig_name = "ESCWarnLampCntr"
        sig_start_bit = 111
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
        startbit = 111
        byte = 13
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ESCWarnLampCheckStsCntr:
        sig_name = "ESCWarnLampCheckStsCntr"
        sig_start_bit = 127
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
        startbit = 127
        byte = 15
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EPBLampCheckStsEPBLampCheckSts:
        sig_name = "EPBLampCheckStsEPBLampCheckSts"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GearIndcnCntr:
        sig_name = "GearIndcnCntr"
        sig_start_bit = 143
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

    class LVBattLampQosStsLVBattLampQosSts:
        sig_name = "LVBattLampQosStsLVBattLampQosSts"
        sig_start_bit = 219
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
        startbit = 219
        byte = 27
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class LVBattLampLVBattLamp:
        sig_name = "LVBattLampLVBattLamp"
        sig_start_bit = 187
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
        startbit = 187
        byte = 23
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ESCOffLampCheckStsESCOffLampCheckSts:
        sig_name = "ESCOffLampCheckStsESCOffLampCheckSts"
        sig_start_bit = 75
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
        startbit = 75
        byte = 9
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class LVBattLampQosStsChks:
        sig_name = "LVBattLampQosStsChks"
        sig_start_bit = 215
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
        startbit = 215
        byte = 26
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LVBattLampChks:
        sig_name = "LVBattLampChks"
        sig_start_bit = 183
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
        startbit = 183
        byte = 22
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GearIndcnQosStsChks:
        sig_name = "GearIndcnQosStsChks"
        sig_start_bit = 167
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


class IhuDhuInfoCanFr09:
    msg_name = "IhuDhuInfoCanFr09"
    msg_id = 1104
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['CD', 'AUD']

    class CarTiGlb_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "CarTiGlb_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 7
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

    class BkpOfDstTrvld_0_DIMBackBoneSignalIPdu04:
        sig_name = "BkpOfDstTrvld_0_DIMBackBoneSignalIPdu04"
        sig_start_bit = 36
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


class CdcToAllInfoCanDiagReqFrame:
    msg_name = "CdcToAllInfoCanDiagReqFrame"
    msg_id = 2047
    msg_type = "can_fd"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['CD', 'AUD']


class IhuDhuInfoCanFr03:
    msg_name = "IhuDhuInfoCanFr03"
    msg_id = 336
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']

    class BgrndForAudOutpCh17:
        sig_name = "BgrndForAudOutpCh17"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BgrndForAudOutpCh5:
        sig_name = "BgrndForAudOutpCh5"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BgrndForAudOutpCh7:
        sig_name = "BgrndForAudOutpCh7"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BgrndForAudOutpCh2:
        sig_name = "BgrndForAudOutpCh2"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BgrndForAudOutpCh4:
        sig_name = "BgrndForAudOutpCh4"
        sig_start_bit = 34
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
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BgrndForAudOutpCh13:
        sig_name = "BgrndForAudOutpCh13"
        sig_start_bit = 55
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

    class BgrndForAudOutpCh14:
        sig_name = "BgrndForAudOutpCh14"
        sig_start_bit = 54
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

    class BgrndForAudOutpCh9:
        sig_name = "BgrndForAudOutpCh9"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BgrndForAudOutpCh10:
        sig_name = "BgrndForAudOutpCh10"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BgrndForAudOutpCh12:
        sig_name = "BgrndForAudOutpCh12"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BgrndForAudOutpCh16:
        sig_name = "BgrndForAudOutpCh16"
        sig_start_bit = 52
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
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class BgrndForAudOutpCh1:
        sig_name = "BgrndForAudOutpCh1"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BgrndForAudOutpCh18:
        sig_name = "BgrndForAudOutpCh18"
        sig_start_bit = 50
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
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BgrndForAudOutpCh11:
        sig_name = "BgrndForAudOutpCh11"
        sig_start_bit = 42
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
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BgrndForAudOutpCh15:
        sig_name = "BgrndForAudOutpCh15"
        sig_start_bit = 53
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
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BgrndForAudOutpCh6:
        sig_name = "BgrndForAudOutpCh6"
        sig_start_bit = 33
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
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BgrndForAudOutpCh8:
        sig_name = "BgrndForAudOutpCh8"
        sig_start_bit = 45
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
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BgrndForAudOutpCh3:
        sig_name = "BgrndForAudOutpCh3"
        sig_start_bit = 46
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
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class IhuDhuInfoCanFr19:
    msg_name = "IhuDhuInfoCanFr19"
    msg_id = 85
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = []

    class SteerWhlSnsrChks_2_IhuDhuInfoCanSignalIPdu19:
        sig_name = "SteerWhlSnsrChks_2_IhuDhuInfoCanSignalIPdu19"
        sig_start_bit = 39
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

    class SteerWhlSnsrCntr_2_IhuDhuInfoCanSignalIPdu19:
        sig_name = "SteerWhlSnsrCntr_2_IhuDhuInfoCanSignalIPdu19"
        sig_start_bit = 47
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

    class SteerWhlSnsrAg_2_IhuDhuInfoCanSignalIPdu19:
        sig_name = "SteerWhlSnsrAg_2_IhuDhuInfoCanSignalIPdu19"
        sig_start_bit = 6
        sig_length = 15
        sig_value_factor = "9.765625E-4"
        sig_value_offset = 0.0
        sig_value_min = -14848
        sig_value_max = 14848
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class SteerWhlSnsrQf_2_IhuDhuInfoCanSignalIPdu19:
        sig_name = "SteerWhlSnsrQf_2_IhuDhuInfoCanSignalIPdu19"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlSnsrAgSpd_2_IhuDhuInfoCanSignalIPdu19:
        sig_name = "SteerWhlSnsrAgSpd_2_IhuDhuInfoCanSignalIPdu19"
        sig_start_bit = 21
        sig_length = 14
        sig_value_factor = 0.0078125
        sig_value_offset = 0.0
        sig_value_min = -6400
        sig_value_max = 6400
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class IhuDhuInfoCanFr10:
    msg_name = "IhuDhuInfoCanFr10"
    msg_id = 32
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']

    class VehSpdLgtChks_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtChks_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 55
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

    class VehSpdLgtA_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtA_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 38
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

    class VehSpdLgtCntr_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtCntr_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 63
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

    class VehSpdLgtQf_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehSpdLgtQf_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 59
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


class IhuDhuInfoCanFr07:
    msg_name = "IhuDhuInfoCanFr07"
    msg_id = 344
    msg_type = "can_fd"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "CDC"
    rx_nodes = ['AUD']

    class MmedAudPwrMod:
        sig_name = "MmedAudPwrMod"
        sig_start_bit = 46
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MmedAudPwrMod_Off': 0, 'MmedAudPwrMod_Partial': 1, 'MmedAudPwrMod_Full': 2}
        compute_method = None
        length = 2
        startbit = 46
        byte = 5
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5


