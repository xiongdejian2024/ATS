class BecmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "BecmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2026
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class VgmToHvcmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToHvcmJ1979OBDPropCanReqFrame11"
    msg_id = 2021
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class MgmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "MgmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2028
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class VddmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "VddmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2030
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class SrsToVgmISO26021PropDiagResFrame11:
    msg_name = "SrsToVgmISO26021PropDiagResFrame11"
    msg_id = 2041
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class VgmToAllJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToAllJ1979OBDPropCanReqFrame11"
    msg_id = 2015
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class VgmPropFr01:
    msg_name = "VgmPropFr01"
    msg_id = 786
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class OnBdDiagLostCom:
        sig_name = "OnBdDiagLostCom"
        sig_start_bit = 6
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 6
        byte = 0
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3


class VgmToIemJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToIemJ1979OBDPropCanReqFrame11"
    msg_id = 2019
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class VgmToMgmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToMgmJ1979OBDPropCanReqFrame11"
    msg_id = 2020
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class VgmToVddmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToVddmJ1979OBDPropCanReqFrame11"
    msg_id = 2022
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class VgmToEcmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToEcmJ1979OBDPropCanReqFrame11"
    msg_id = 2016
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class BgmPropulsionCANNmFr:
    msg_name = "BgmPropulsionCANNmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class EcmToVgmJ1979OBDPropCanResFrame11:
    msg_name = "EcmToVgmJ1979OBDPropCanResFrame11"
    msg_id = 2024
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class VgmToSrsISO26021PropDiagResFrame11:
    msg_name = "VgmToSrsISO26021PropDiagResFrame11"
    msg_id = 2033
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class VgmToBecmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToBecmJ1979OBDPropCanReqFrame11"
    msg_id = 2018
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class HvcmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "HvcmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2029
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class IemToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "IemToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2027
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class HvcmPropulsionCANNmFr:
    msg_name = "HvcmPropulsionCANNmFr"
    msg_id = 1327
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class VcuPropFr02:
    msg_name = "VcuPropFr02"
    msg_id = 919
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ResvSupChrgThermSwt:
        sig_name = "ResvSupChrgThermSwt"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


