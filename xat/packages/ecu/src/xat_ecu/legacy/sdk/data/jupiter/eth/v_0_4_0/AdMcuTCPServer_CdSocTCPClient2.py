

class CCUSOCCDToCCUMCUADEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401002
    pdu_length_bytes = 2
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {'HeiLvlInhbReq': ['HeiLvlInhbReqLvlInhbPriority', 'HeiLvlInhbReqLvlInhb']}

    class HeiLvlInhbReqLvlInhbPriority:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Height level request (corner) Priority"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class HeiLvlInhbReqLvlInhb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Height level request (corner)"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' LvlInhb_NoInhibit', '0x1': ' LvlInhb_LevelDownInhibit', '0x2': ' LvlInhb_LevelUpInhibit', '0x3': ' LvlInhb_LevelInhibit'}


class CCUSOCCDToCCUMCUADEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401003
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class AvhActvPattern:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Avh activition patterns"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' AvhActvPattern_AvhActvPattern0', '0x1': ' AvhActvPattern_AvhActvPattern1', '0x2': ' AvhActvPattern_AvhActvPattern2', '0x3': ' AvhActvPattern_AvhActvPattern3'}

    class AvhSoftSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Avh soft switch"
        signal_length = 1
        start_position = 4
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}


class CCUSOCCDToCCUMCUADEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401001
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class AutLvlInhb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Automatic levelling inhibition"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}


class CCUSOCCDToCCUMCUADEthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401004
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class SteerAssiConvReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Assist Request under certain usage mode"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}


class CCUSOCCDToCCUMCUADEthSignalIPdu05:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401005
    pdu_length_bytes = 3
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-1000ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {'AmbPBasLocn': ['AmbPBasLocnPQf', 'AmbPBasLocnP']}

    class AmbPBasLocnPQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The signal quality of ambient pressure."
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class AmbPBasLocnP:
        comments = ""
        factor = 0.025
        initial_value = 40520
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Estimated ambient pressure based on global location."
        signal_length = 16
        start_position = 15
        value_definition = {}


class CCUSOCCDToCCUMCUADEthSignalIPdu06:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401006
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class AbsSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Abs function setting"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable_Enable', '0x1': ' EnableDisable_Disable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu07:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401007
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class ArpSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Arp function setting"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable_Enable', '0x1': ' EnableDisable_Disable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu08:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401008
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class BrkPedlCrvReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Brake pedal curve request"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' BrkCalParas_Nromal', '0x1': ' BrkCalParas_Comfort', '0x2': ' BrkCalParas_Sport', '0x3': ' BrkCalParas_Reserved1', '0x4': ' BrkCalParas_Reserved2', '0x5': ' BrkCalParas_Reserved3'}


class CCUSOCCDToCCUMCUADEthSignalIPdu09:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401009
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class CargoReq:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Cargo mode request (easy loading)"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToCCUMCUADEthSignalIPdu10:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40100A
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class CbcSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Cbc function setting"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable_Enable', '0x1': ' EnableDisable_Disable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu11:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40100B
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class CrbSoftSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Crb soft stich"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}


class CCUSOCCDToCCUMCUADEthSignalIPdu12:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40100C
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class CstSoftSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Cst soft switch"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}


class CCUSOCCDToCCUMCUADEthSignalIPdu13:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40100D
    pdu_length_bytes = 2
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {'DamprFixPerc': ['DamprFixPercDamprFixPriority', 'DamprFixPercDampingFixPerc']}

    class DamprFixPercDamprFixPriority:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Fix damping priority"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DamprFixPercDampingFixPerc:
        comments = ""
        factor = 0.393
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Fix damping percentage"
        signal_length = 8
        start_position = 7
        value_definition = {}


class CCUSOCCDToCCUMCUADEthSignalIPdu14:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40100E
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class DsrSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Dsr function setting"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable_Enable', '0x1': ' EnableDisable_Disable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu15:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40100F
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class DtcSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Dtc function setting"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable_Enable', '0x1': ' EnableDisable_Disable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu16:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401010
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class DtvSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Dtv function setting"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable_Enable', '0x1': ' EnableDisable_Disable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu17:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401011
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class EasyEntryEna:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Easy entry enable/disable "
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}


class CCUSOCCDToCCUMCUADEthSignalIPdu18:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401012
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class EbdSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Ebd function setting"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable_Enable', '0x1': ' EnableDisable_Disable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu19:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401013
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class EmgHeiStop:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Manual levelling emergency stop"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToCCUMCUADEthSignalIPdu20:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401014
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class EscSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Esc function setting"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' EscSet_Normal', '0x1': ' EscSet_Sprot1', '0x2': ' EscSet_Off', '0x3': ' EscSet_OffRoad1', '0x4': ' EscSet_OffRoad2', '0x5': ' EscSet_OffRoad3'}


class CCUSOCCDToCCUMCUADEthSignalIPdu21:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401015
    pdu_length_bytes = 2
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {'HeiReqOfFL': ['HeiReqOfFLHeightLevel', 'HeiReqOfFLHeightLevelPriority']}

    class HeiReqOfFLHeightLevel:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Height level request (corner)"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}

    class HeiReqOfFLHeightLevelPriority:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Height level request (corner) Priority"
        signal_length = 8
        start_position = 15
        value_definition = {}


class CCUSOCCDToCCUMCUADEthSignalIPdu22:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401016
    pdu_length_bytes = 2
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {'HeiReqOfFR': ['HeiReqOfFRHeightLevel', 'HeiReqOfFRHeightLevelPriority']}

    class HeiReqOfFRHeightLevel:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Height level request (corner)"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}

    class HeiReqOfFRHeightLevelPriority:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Height level request (corner) Priority"
        signal_length = 8
        start_position = 15
        value_definition = {}


class CCUSOCCDToCCUMCUADEthSignalIPdu23:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401017
    pdu_length_bytes = 2
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {'HeiReqOfRL': ['HeiReqOfRLHeightLevelPriority', 'HeiReqOfRLHeightLevel']}

    class HeiReqOfRLHeightLevelPriority:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Height level request (corner) Priority"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class HeiReqOfRLHeightLevel:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Height level request (corner)"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}


class CCUSOCCDToCCUMCUADEthSignalIPdu24:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401018
    pdu_length_bytes = 2
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {'HeiReqOfRR': ['HeiReqOfRRHeightLevel', 'HeiReqOfRRHeightLevelPriority']}

    class HeiReqOfRRHeightLevel:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Height level request (corner)"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}

    class HeiReqOfRRHeightLevelPriority:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Height level request (corner) Priority"
        signal_length = 8
        start_position = 15
        value_definition = {}


class CCUSOCCDToCCUMCUADEthSignalIPdu25:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401019
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class JackModReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Jack mode request"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToCCUMCUADEthSignalIPdu26:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40101A
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class LCDeactvnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Levelling control deactivate request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}


class CCUSOCCDToCCUMCUADEthSignalIPdu27:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40101B
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class LvlCtrlEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Level control enable/disable"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}


class CCUSOCCDToCCUMCUADEthSignalIPdu28:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40101C
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class ModReqOfDampr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Damper level request"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' DamprLvl_level1', '0x1': ' DamprLvl_level2', '0x2': ' DamprLvl_level3', '0x3': ' DamprLvl_Reserved1', '0x4': ' DamprLvl_Reserved2', '0x5': ' DamprLvl_Reserved3', '0x6': ' DamprLvl_Reserved4', '0x7': ' DamprLvl_Reserved5'}


class CCUSOCCDToCCUMCUADEthSignalIPdu29:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40101D
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class ModReqOfLvl:
        comments = ""
        factor = 1.0
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Level request "
        signal_length = 4
        start_position = 7
        value_definition = {'0x0': ' HeightLevel_LowLevel5', '0x1': ' HeightLevel_LowLevel4', '0x2': ' HeightLevel_LowLevel3', '0x3': ' HeightLevel_LowLevel2', '0x4': ' HeightLevel_LowLevel1', '0x5': ' HeightLevel_NormaLevel', '0x6': ' HeightLevel_HighLevel1', '0x7': ' HeightLevel_HighLevel2', '0x8': ' HeightLevel_HighLevel3', '0x9': ' HeightLevel_HighLevel4', '0xA': ' HeightLevel_HighLevel5', '0xB': ' HeightLevel_Reserved1', '0xC': ' HeightLevel_Reserved2', '0xD': ' HeightLevel_Reserved3', '0xE': ' HeightLevel_InitUnknow', '0xF': ' HeightLevel_Invalid'}


class CCUSOCCDToCCUMCUADEthSignalIPdu30:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40101E
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class PassAirbDiReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Passenger airbag disable request"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' EnableDisable4_NoCmd', '0x1': ' EnableDisable4_Disable', '0x2': ' EnableDisable4_Enable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu31:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40101F
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class SteerAssiLvlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Steering Assist Level Request"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' SteerAssiLvl_UnknownLevel', '0x1': ' SteerAssiLvl_Level1', '0x2': ' SteerAssiLvl_Level2', '0x3': ' SteerAssiLvl_Level3', '0x4': ' SteerAssiLvl_Level4', '0x5': ' SteerAssiLvl_Reserved1', '0x6': ' SteerAssiLvl_Reserved2', '0x7': ' SteerAssiLvl_Reserved3'}


class CCUSOCCDToCCUMCUADEthSignalIPdu32:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401020
    pdu_length_bytes = 2
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {'SteerWhlCntrCtrlReq': ['SteerWhlCntrCtrlReqSteerWhlCntrCtrlAgReq', 'SteerWhlCntrCtrlReqSteerWhlCntrCtrlReq']}

    class SteerWhlCntrCtrlReqSteerWhlCntrCtrlAgReq:
        comments = ""
        factor = 0.000976563
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Steering Wheel Centering Control Angle request"
        signal_length = 15
        start_position = 7
        value_definition = {}

    class SteerWhlCntrCtrlReqSteerWhlCntrCtrlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Steering Wheel Centering Control request"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}


class CCUSOCCDToCCUMCUADEthSignalIPdu33:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401021
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class SteerWhlHptcWarnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Steering Wheel Haptic Warning Request"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}


class CCUSOCCDToCCUMCUADEthSignalIPdu34:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401022
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class StfnLvlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "stiffness level request"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' StfnLvl_Level1', '0x1': ' StfnLvl_Level2', '0x2': ' StfnLvl_Level3', '0x3': ' StfnLvl_Level4', '0x4': ' StfnLvl_Level5', '0x5': ' StfnLvl_Level6', '0x6': ' StfnLvl_Level7', '0x7': ' StfnLvl_Level8'}


class CCUSOCCDToCCUMCUADEthSignalIPdu35:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401023
    pdu_length_bytes = 2
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {'SusConStfnReq': ['SusConStfnReqStfnConReqPriority', 'SusConStfnReqStfnConReq']}

    class SusConStfnReqStfnConReqPriority:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "constant stiffnesss setting request Priority"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class SusConStfnReqStfnConReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "constant stiffnesss setting request"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUSOCCDToCCUMCUADEthSignalIPdu36:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401024
    pdu_length_bytes = 2
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {'SusStfnInhbReq': ['SusStfnInhbReqStfnInhbReqPriority', 'SusStfnInhbReqStfnInhbReq']}

    class SusStfnInhbReqStfnInhbReqPriority:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Stiffness inhibtion request priority"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class SusStfnInhbReqStfnInhbReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Stiffness inhibtion request"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}


class CCUSOCCDToCCUMCUADEthSignalIPdu37:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401025
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class TcsBtcSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Btc function setting"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable_Enable', '0x1': ' EnableDisable_Disable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu38:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401026
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class TcsPtcSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Ptc  function setting"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' TcsSet_None', '0x1': ' TcsSet_PtcDisable', '0x2': ' TcsSet_BtcDisable', '0x3': ' TcsSet_AllDisable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu39:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401027
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class TscSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Tsc function setting"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable_Enable', '0x1': ' EnableDisable_Disable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu40:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401028
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class VdcSet:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Vdc function setting"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' EnableDisable_Enable', '0x1': ' EnableDisable_Disable'}


class CCUSOCCDToCCUMCUADEthSignalIPdu42:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40102A
    pdu_length_bytes = 3
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-50ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {'ScrnGearShiftReq1': ['ScrnGearShiftReq1GearReq', 'ScrnGearShiftReq1Chks', 'ScrnGearShiftReq1Cntr', 'ScrnGearShiftReq1GearFltSts']}

    class ScrnGearShiftReq1GearReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Screen Shift request signal Group 1, containing NoReq/P/R/N (reserved) /D files.E2E verification."
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' GearLvrIndcn_Default', '0x1': ' GearLvrIndcn_P', '0x2': ' GearLvrIndcn_R', '0x3': ' GearLvrIndcn_N', '0x4': ' GearLvrIndcn_D', '0x5': ' GearLvrIndcn_Reserved1', '0x6': ' GearLvrIndcn_Reserved2', '0x7': ' GearLvrIndcn_Undefd'}

    class ScrnGearShiftReq1Chks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Checksum"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class ScrnGearShiftReq1Cntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Counter"
        signal_length = 4
        start_position = 23
        value_definition = {}

    class ScrnGearShiftReq1GearFltSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Screen Shift request signal Group 1 quality status."
        signal_length = 3
        start_position = 19
        value_definition = {'0x0': ' GearFltSts_Normal', '0x1': ' GearFltSts_PFlt', '0x2': ' GearFltSts_RFlt', '0x3': ' GearFltSts_NFlt', '0x4': ' GearFltSts_DFlt', '0x5': ' GearFltSts_SrvReq', '0x6': ' GearFltSts_Reserved1', '0x7': ' GearFltSts_Reserved2'}


class CCUSOCCDToCCUMCUADEthSignalIPdu43:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x40102B
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class SetDrivingwithoutkeyProxyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Set UsageMode Up Proxy Request"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}


class CCUSOCCDToCCUMCUADEthSignalIPdu41:
    base_type = "Unsigned"
    client_socket = "SocketAdMcuTCPServer"
    pdu_header_id = 0x401029
    pdu_length_bytes = 1
    receiver = ['CCUMCUAD']
    send_type = "Cyclic-100ms"
    sender = "CCUSOCCD"
    server_socket = "SocketCdSocTCPClient2"
    signal_group = {}

    class DiagcComActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Represent Vehicle Diagnostic Requirement"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}
