class CCUVCUToDLCOBDDiagnosticCANDiagRespFrame:
    msg_name = "CCUVCUToDLCOBDDiagnosticCANDiagRespFrame"
    msg_id = 2024
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['DLC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CCUSRSToDLCOBDDiagnosticCANDiagRespFrame:
    msg_name = "CCUSRSToDLCOBDDiagnosticCANDiagRespFrame"
    msg_id = 2041
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCUMCUCD"
    rx_nodes = ['DLC']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DLCToCCUSRSOBDDiagnosticCANDiagReqFrame:
    msg_name = "DLCToCCUSRSOBDDiagnosticCANDiagReqFrame"
    msg_id = 2033
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "DLC"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DLCToAllOBDDiagnosticCANDiagFuncReqFrame:
    msg_name = "DLCToAllOBDDiagnosticCANDiagFuncReqFrame"
    msg_id = 2015
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "DLC"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class DLCToCCUVCUOBDDiagnosticCANDiagReqFrame:
    msg_name = "DLCToCCUVCUOBDDiagnosticCANDiagReqFrame"
    msg_id = 2016
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "DLC"
    rx_nodes = ['CCUMCUCD']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


