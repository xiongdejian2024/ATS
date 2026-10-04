

class CDNADToCCUMCUCDEthDTCPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x8020F0
    pdu_length_bytes = 1028
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUNAD"
    server_socket = "SocketCdNadTCPClient1"
    signal_group = {'CDNADDiagDTCInfo': ['CDNADDiagDTCInfoDTCCode', 'CDNADDiagDTCInfoDTCStatus']}

    class CDNADDiagDTCInfoDTCCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC Code info"
        signal_length = 24
        start_position = 7
        value_definition = {}

    class CDNADDiagDTCInfoDTCStatus:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC status flag"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class CDNADDiagDTCInfoData:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC payload data"
        signal_length = 8192
        start_position = 32
        value_definition = {}


class CDNADToCCUMCUCDEthDummyPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x8020F1
    pdu_length_bytes = 1024
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUNAD"
    server_socket = "SocketCdNadTCPClient1"
    signal_group = {}

    class CDNAD2CDMCUDummyData:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Dynamic array for backup use between CDMCU & CDNAD"
        signal_length = 8192
        start_position = 0
        value_definition = {}


class CDNADToCCUMCUCDEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x802003
    pdu_length_bytes = 1
    receiver = ['CCUMCUCD']
    send_type = "Cyclic-100ms"
    sender = "CCUNAD"
    server_socket = "SocketCdNadTCPClient1"
    signal_group = {}

    class RemVehWakeupReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Remote vehicle wakeup Request for CCU"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' RemVehWakeUpReq_Default', '0x1': ' RemVehWakeUpReq_CDOnly', '0x2': ' RemVehWakeUpReq_ADOnly', '0x3': ' RemVehWakeUpReq_CDAndAD'}


class CDNADToCCUMCUCDEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x802002
    pdu_length_bytes = 8
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUNAD"
    server_socket = "SocketCdNadTCPClient1"
    signal_group = {}

    class NTPTime:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "NTP time, in UTC timestamp format, unit ms"
        signal_length = 64
        start_position = 7
        value_definition = {}


class CDNADToCCUMCUCDEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdMcuTCPServer"
    pdu_header_id = 0x802001
    pdu_length_bytes = 9
    receiver = ['CCUMCUCD']
    send_type = "EventTriggered"
    sender = "CCUNAD"
    server_socket = "SocketCdNadTCPClient1"
    signal_group = {'GnssTime': ['GnssTimeSrc', 'GnssTimestamp']}

    class GnssTimeSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "source of the following GNSS time, 0 invalid, 4 LPGNSSTime(NAD GNSS), 5 HPGNSSTime(AD GNSS), Others Invalid"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class GnssTimestamp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "lastest GnssTimestamp, contains UTCdate and UTCtime, in UTC timestamp format, Unit64, unit ms"
        signal_length = 64
        start_position = 15
        value_definition = {}
