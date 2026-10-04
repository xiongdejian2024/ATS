

class CCUMCUADToLCULEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketLcuLSoAdUDP"
    pdu_header_id = 0x105001
    pdu_length_bytes = 4
    receiver = ['LCUL']
    send_type = "Cyclic-25ms"
    sender = "CCUMCUAD"
    server_socket = "SocketAdMcuSoAdUDP"
    signal_group = {}

    class CllsnReSideIndcn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 23
        signal_description = "Request to activate collision warning against rear object"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' CllsnReSideIndcn_NoWarn', '0x1': ' CllsnReSideIndcn_WarnLvl1', '0x2': ' CllsnReSideIndcn_NotUsed', '0x3': ' CllsnReSideIndcn_WarnLvl2'}

    class CllsnThreat:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 22
        signal_description = "collision threat"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' CllsnThreat1_Ukwn', '0x1': ' CllsnThreat1_ThreatLo', '0x2': ' CllsnThreat1_ThreatMed', '0x3': ' CllsnThreat1_ThreatHi'}

    class FctaIndcnLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 21
        signal_description = "FCTA left warning signal"
        signal_length = 2
        start_position = 3
        value_definition = {'0x0': ' CllsnReSideIndcn_NoWarn', '0x1': ' CllsnReSideIndcn_WarnLvl1', '0x2': ' CllsnReSideIndcn_NotUsed', '0x3': ' CllsnReSideIndcn_WarnLvl2'}

    class FctaIndcnRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "FCTA right warning signal"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': ' CllsnReSideIndcn_NoWarn', '0x1': ' CllsnReSideIndcn_WarnLvl1', '0x2': ' CllsnReSideIndcn_NotUsed', '0x3': ' CllsnReSideIndcn_WarnLvl2'}

    class HWLReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "hazard warning light request"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' AsySftyHWLReq_NoRequest', '0x1': ' AsySftyHWLReq_TurnOn', '0x2': ' AsySftyHWLReq_TurnOff', '0x3': ' AsySftyHWLReq_Reserved'}

    class RctaIndcnLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "RCTA left warning signal."
        signal_length = 2
        start_position = 13
        value_definition = {'0x0': ' CllsnReSideIndcn_NoWarn', '0x1': ' CllsnReSideIndcn_WarnLvl1', '0x2': ' CllsnReSideIndcn_NotUsed', '0x3': ' CllsnReSideIndcn_WarnLvl2'}

    class RctaIndcnRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "RCTA right warning signal"
        signal_length = 2
        start_position = 11
        value_definition = {'0x0': ' CllsnReSideIndcn_NoWarn', '0x1': ' CllsnReSideIndcn_WarnLvl1', '0x2': ' CllsnReSideIndcn_NotUsed', '0x3': ' CllsnReSideIndcn_WarnLvl2'}

    class RcwLiReq:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "RCW lit the hazard light request"
        signal_length = 1
        start_position = 9
        value_definition = {'0x0': ' YesNo1_Yes', '0x1': ' YesNo1_No'}
