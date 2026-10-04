class BecmPropDevFr02:
    msg_name = "BecmPropDevFr02"
    msg_id = 1473
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup2': ['BECMdevelpsignalgroup2Functiondevpsignalgroup1', 'BECMdevelpsignalgroup2Functiondevpsignalgroup2', 'BECMdevelpsignalgroup2Functiondevpsignalgroup3', 'BECMdevelpsignalgroup2Functiondevpsignalgroup4', 'BECMdevelpsignalgroup2Functiondevpsignalgroup5', 'BECMdevelpsignalgroup2Functiondevpsignalgroup6', 'BECMdevelpsignalgroup2Functiondevpsignalgroup7', 'BECMdevelpsignalgroup2Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup2Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup2Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup2Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup7"
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

    class BECMdevelpsignalgroup2Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup3"
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

    class BECMdevelpsignalgroup2Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup2Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup2Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup5"
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

    class BECMdevelpsignalgroup2Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup2Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BecmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "BecmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2026
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr36:
    msg_name = "VddmPropFr36"
    msg_id = 1143
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.12
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1']
    sig_group_dict = {'Vin': ['VinBlockNr', 'VinVINSignalPos1', 'VinVINSignalPos2', 'VinVINSignalPos3', 'VinVINSignalPos4', 'VinVINSignalPos5', 'VinVINSignalPos6', 'VinVINSignalPos7']}
    sig_group_dataid_dict = {}

    class VinVINSignalPos5:
        sig_name = "VinVINSignalPos5"
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

    class VinVINSignalPos4:
        sig_name = "VinVINSignalPos4"
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

    class VinVINSignalPos3:
        sig_name = "VinVINSignalPos3"
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

    class VinBlockNr:
        sig_name = "VinBlockNr"
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

    class VinVINSignalPos1:
        sig_name = "VinVINSignalPos1"
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

    class VinVINSignalPos6:
        sig_name = "VinVINSignalPos6"
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

    class VinVINSignalPos2:
        sig_name = "VinVINSignalPos2"
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

    class VinVINSignalPos7:
        sig_name = "VinVINSignalPos7"
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


class HvcmPropFr02:
    msg_name = "HvcmPropFr02"
    msg_id = 657
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {'HVChrgnCCCPInfo': ['HVChrgnCCCPInfoAvlIMax', 'HVChrgnCCCPInfoCCRes1', 'HVChrgnCCCPInfoCPDuty', 'HVChrgnCCCPInfoCPFreq', 'HVChrgnCCCPInfoCPMag']}
    sig_group_dataid_dict = {}

    class HVChrgnCCCPInfoAvlIMax:
        sig_name = "HVChrgnCCCPInfoAvlIMax"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.3
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVChrgnCCCPInfoCCRes1:
        sig_name = "HVChrgnCCCPInfoCCRes1"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 8191
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class HVChrgnCCCPInfo_UB:
        sig_name = "HVChrgnCCCPInfo_UB"
        sig_start_bit = 55
        update_id_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HVChrgnCCCPInfoCPDuty:
        sig_name = "HVChrgnCCCPInfoCPDuty"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 127
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class HVChrgnCCCPInfoCPMag:
        sig_name = "HVChrgnCCCPInfoCPMag"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HVChrgnCCCPInfoCPFreq:
        sig_name = "HVChrgnCCCPInfoCPFreq"
        sig_start_bit = 27
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11111110, 0b00000001, 7, 1)]


class BgmPropulsionFr09:
    msg_name = "BgmPropulsionFr09"
    msg_id = 630
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []
    sig_group_dict = {'DischrgnMntnDlyTi': ['DischrgnMntnDlyTiChrgnTmrhour', 'DischrgnMntnDlyTiChrgnTmrmin']}
    sig_group_dataid_dict = {}

    class RemHvBattHeatgReqFromAC:
        sig_name = "RemHvBattHeatgReqFromAC"
        sig_start_bit = 14
        update_id_bit = 13
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RemHvBattHeatgReq_OFF': 0, 'RemHvBattHeatgReq_ON': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DischrgnMntnDlyTiChrgnTmrhour:
        sig_name = "DischrgnMntnDlyTiChrgnTmrhour"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReservedSigForTherm03:
        sig_name = "ReservedSigForTherm03"
        sig_start_bit = 39
        update_id_bit = 8
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
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DischrgnMntnDlyTiChrgnTmrmin:
        sig_name = "DischrgnMntnDlyTiChrgnTmrmin"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ReservedSigForTherm05:
        sig_name = "ReservedSigForTherm05"
        sig_start_bit = 47
        update_id_bit = 42
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

    class MaxAcInpCurrentSet:
        sig_name = "MaxAcInpCurrentSet"
        sig_start_bit = 7
        update_id_bit = 15
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

    class ReservedSigForTherm01:
        sig_name = "ReservedSigForTherm01"
        sig_start_bit = 31
        update_id_bit = 10
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

    class ReservedSigForTherm04:
        sig_name = "ReservedSigForTherm04"
        sig_start_bit = 35
        update_id_bit = 43
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

    class DischrgnMntnDlyTi_UB:
        sig_name = "DischrgnMntnDlyTi_UB"
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

    class ReservedSigForTherm02:
        sig_name = "ReservedSigForTherm02"
        sig_start_bit = 27
        update_id_bit = 9
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
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RemHvBattHeatgTarTFromAC:
        sig_name = "RemHvBattHeatgTarTFromAC"
        sig_start_bit = 23
        update_id_bit = 11
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 80
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class IemPropFr02:
    msg_name = "IemPropFr02"
    msg_id = 1125
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['CCM']
    sig_group_dict = {'IEMTestFr2': ['IEMTestFr2Byte0', 'IEMTestFr2Byte1', 'IEMTestFr2Byte2', 'IEMTestFr2Byte3', 'IEMTestFr2Byte4', 'IEMTestFr2Byte5', 'IEMTestFr2Byte6', 'IEMTestFr2Byte7']}
    sig_group_dataid_dict = {}

    class IEMTestFr2Byte5:
        sig_name = "IEMTestFr2Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IEMTestFr2Byte2:
        sig_name = "IEMTestFr2Byte2"
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

    class IEMTestFr2Byte6:
        sig_name = "IEMTestFr2Byte6"
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

    class IEMTestFr2Byte7:
        sig_name = "IEMTestFr2Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IEMTestFr2Byte3:
        sig_name = "IEMTestFr2Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IEMTestFr2Byte4:
        sig_name = "IEMTestFr2Byte4"
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

    class IEMTestFr2Byte0:
        sig_name = "IEMTestFr2Byte0"
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

    class IEMTestFr2Byte1:
        sig_name = "IEMTestFr2Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EvccPropulsionCANNmFr:
    msg_name = "EvccPropulsionCANNmFr"
    msg_id = 1315
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EgsmPropDvelFr02:
    msg_name = "EgsmPropDvelFr02"
    msg_id = 1093
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['CCM']
    sig_group_dict = {'EGSMdevelpsignalgroup2': ['EGSMdevelpsignalgroup2Functiondevpsignalgroup1', 'EGSMdevelpsignalgroup2Functiondevpsignalgroup2', 'EGSMdevelpsignalgroup2Functiondevpsignalgroup3', 'EGSMdevelpsignalgroup2Functiondevpsignalgroup4', 'EGSMdevelpsignalgroup2Functiondevpsignalgroup5', 'EGSMdevelpsignalgroup2Functiondevpsignalgroup6', 'EGSMdevelpsignalgroup2Functiondevpsignalgroup7', 'EGSMdevelpsignalgroup2Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class EGSMdevelpsignalgroup2Functiondevpsignalgroup7:
        sig_name = "EGSMdevelpsignalgroup2Functiondevpsignalgroup7"
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

    class EGSMdevelpsignalgroup2Functiondevpsignalgroup2:
        sig_name = "EGSMdevelpsignalgroup2Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EGSMdevelpsignalgroup2Functiondevpsignalgroup6:
        sig_name = "EGSMdevelpsignalgroup2Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EGSMdevelpsignalgroup2Functiondevpsignalgroup8:
        sig_name = "EGSMdevelpsignalgroup2Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EGSMdevelpsignalgroup2Functiondevpsignalgroup5:
        sig_name = "EGSMdevelpsignalgroup2Functiondevpsignalgroup5"
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

    class EGSMdevelpsignalgroup2Functiondevpsignalgroup3:
        sig_name = "EGSMdevelpsignalgroup2Functiondevpsignalgroup3"
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

    class EGSMdevelpsignalgroup2Functiondevpsignalgroup4:
        sig_name = "EGSMdevelpsignalgroup2Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EGSMdevelpsignalgroup2Functiondevpsignalgroup1:
        sig_name = "EGSMdevelpsignalgroup2Functiondevpsignalgroup1"
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


class EvccPropFr01:
    msg_name = "EvccPropFr01"
    msg_id = 768
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CCS2HndlLockSts:
        sig_name = "CCS2HndlLockSts"
        sig_start_bit = 9
        update_id_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockgSts_Unknown': 0, 'LockgSts_Locked': 1, 'LockgSts_Unlocked': 2, 'LockgSts_Fault': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CCS2HndlLockCtrlReq:
        sig_name = "CCS2HndlLockCtrlReq"
        sig_start_bit = 19
        update_id_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenClsReq_Default': 0, 'OpenClsReq_Open': 1, 'OpenClsReq_Close': 2, 'OpenClsReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class CCS2ChrgnS2Sts:
        sig_name = "CCS2ChrgnS2Sts"
        sig_start_bit = 21
        update_id_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'S2Sts_Default': 0, 'S2Sts_Open': 1, 'S2Sts_Closed': 2, 'S2Sts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EVCCFaultInfo:
        sig_name = "EVCCFaultInfo"
        sig_start_bit = 7
        update_id_bit = 15
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

    class CCS2ChrgnS2Req:
        sig_name = "CCS2ChrgnS2Req"
        sig_start_bit = 23
        update_id_bit = 14
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenClsReq_Default': 0, 'OpenClsReq_Open': 1, 'OpenClsReq_Close': 2, 'OpenClsReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BecmPropFr13:
    msg_name = "BecmPropFr13"
    msg_id = 664
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattChrgnPwrCritDes1:
        sig_name = "HvBattChrgnPwrCritDes1"
        sig_start_bit = 10
        update_id_bit = 11
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class HvBattChrgnPwrCns1:
        sig_name = "HvBattChrgnPwrCns1"
        sig_start_bit = 7
        update_id_bit = 12
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class HvBattChrgnPwrNormDes1:
        sig_name = "HvBattChrgnPwrNormDes1"
        sig_start_bit = 31
        update_id_bit = 36
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class HvBattEgyAvlChrg1:
        sig_name = "HvBattEgyAvlChrg1"
        sig_start_bit = 52
        update_id_bit = 53
        sig_length = 13
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class EcmPropFr24:
    msg_name = "EcmPropFr24"
    msg_id = 75
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'VDDM', 'EGSM']
    sig_group_dict = {'EngSt1WdSts': ['EngSt1WdStsChks', 'EngSt1WdStsCntr', 'EngSt1WdStsEngSt1WdSts'], 'DrvrDesDir': ['DrvrDesDirChks', 'DrvrDesDirCntr', 'DrvrDesDirDrvrDesDir']}
    sig_group_dataid_dict = {'EngSt1WdSts': 137, 'DrvrDesDir': 627}

    class EngSt1WdStsChks:
        sig_name = "EngSt1WdStsChks"
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

    class HvchSts:
        sig_name = "HvchSts"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCooltHeatrSts_Off': 0, 'HvCooltHeatrSts_LockedUntilNextStart': 1, 'HvCooltHeatrSts_LockedUntilService': 2, 'HvCooltHeatrSts_LockedPermanent': 3, 'HvCooltHeatrSts_Operation': 4, 'HvCooltHeatrSts_Reserved1': 5, 'HvCooltHeatrSts_Reserved2': 6, 'HvCooltHeatrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class WhlMotSysTqReq:
        sig_name = "WhlMotSysTqReq"
        sig_start_bit = 11
        update_id_bit = 12
        sig_length = 12
        sig_value_factor = 4.0
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class EngSt1WdStsCntr:
        sig_name = "EngSt1WdStsCntr"
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

    class DrvrDesDirCntr:
        sig_name = "DrvrDesDirCntr"
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

    class EngSt1WdSts_UB:
        sig_name = "EngSt1WdSts_UB"
        sig_start_bit = 31
        update_id_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DrvrDesDirChks:
        sig_name = "DrvrDesDirChks"
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

    class GearLvrIndcn:
        sig_name = "GearLvrIndcn"
        sig_start_bit = 27
        update_id_bit = 24
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcn2_ParkIndcn': 0, 'GearLvrIndcn2_RvsIndcn': 1, 'GearLvrIndcn2_NeutIndcn': 2, 'GearLvrIndcn2_DrvIndcn': 3, 'GearLvrIndcn2_ManModeIndcn': 4, 'GearLvrIndcn2_Resd1': 5, 'GearLvrIndcn2_Resd2': 6, 'GearLvrIndcn2_Undefd': 7}
        compute_method = None
        length = 3
        startbit = 27
        byte = 3
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class DrvrDesDir_UB:
        sig_name = "DrvrDesDir_UB"
        sig_start_bit = 56
        update_id_bit = 56
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
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DrvrDesDirDrvrDesDir:
        sig_name = "DrvrDesDirDrvrDesDir"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvrDesDir1_Undefd': 0, 'DrvrDesDir1_Fwd': 1, 'DrvrDesDir1_Rvs': 2, 'DrvrDesDir1_Neut': 3, 'DrvrDesDir1_Resd0': 4, 'DrvrDesDir1_Resd1': 5, 'DrvrDesDir1_Resd2': 6, 'DrvrDesDir1_Resd3': 7}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class EngSt1WdStsEngSt1WdSts:
        sig_name = "EngSt1WdStsEngSt1WdSts"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EngSt1_Ini': 0, 'EngSt1_Awake': 1, 'EngSt1_Rdy': 2, 'EngSt1_PreStrtg': 3, 'EngSt1_StrtgInProgs': 4, 'EngSt1_RunngRunng': 5, 'EngSt1_RunngStb': 6, 'EngSt1_RunngStrtgInProgs': 7, 'EngSt1_RunngRemStrtd': 8, 'EngSt1_AftRun': 9}
        compute_method = None
        length = 4
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class EcmPropFr30:
    msg_name = "EcmPropFr30"
    msg_id = 1168
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CooltInletT:
        sig_name = "CooltInletT"
        sig_start_bit = 47
        update_id_bit = 57
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -60.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class CooltOutletT:
        sig_name = "CooltOutletT"
        sig_start_bit = 52
        update_id_bit = 56
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -60.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111100, 0b00000011, 6, 2)]


class CddIgmPropFr01:
    msg_name = "CddIgmPropFr01"
    msg_id = 331
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['CCM', 'ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IDcDcActHiSide:
        sig_name = "IDcDcActHiSide"
        sig_start_bit = 23
        update_id_bit = 26
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = -410.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 4100
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111000, 0b00000111, 5, 3)]

    class UDcDcActHiSide:
        sig_name = "UDcDcActHiSide"
        sig_start_bit = 39
        update_id_bit = 42
        sig_length = 13
        sig_value_factor = 0.125
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8184
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class UDcDcActLoSide:
        sig_name = "UDcDcActLoSide"
        sig_start_bit = 7
        update_id_bit = 14
        sig_length = 9
        sig_value_factor = 0.025
        sig_value_offset = 5.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b10000000, 0b01111111, 1, 7)]

    class FltTDcDc:
        sig_name = "FltTDcDc"
        sig_start_bit = 9
        update_id_bit = 8
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DcDcActvd:
        sig_name = "DcDcActvd"
        sig_start_bit = 25
        update_id_bit = 24
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DcDcActvd_NoConversionToLVSide': 0, 'DcDcActvd_ConversionToLVSide': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class IDcDcAvlMaxLoSide:
        sig_name = "IDcDcAvlMaxLoSide"
        sig_start_bit = 55
        update_id_bit = 40
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11110000, 0b00001111, 4, 4)]

    class FltElecDcDc:
        sig_name = "FltElecDcDc"
        sig_start_bit = 11
        update_id_bit = 10
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3


class BecmPropDevFr01:
    msg_name = "BecmPropDevFr01"
    msg_id = 1472
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup1': ['BECMdevelpsignalgroup1Functiondevpsignalgroup1', 'BECMdevelpsignalgroup1Functiondevpsignalgroup2', 'BECMdevelpsignalgroup1Functiondevpsignalgroup3', 'BECMdevelpsignalgroup1Functiondevpsignalgroup4', 'BECMdevelpsignalgroup1Functiondevpsignalgroup5', 'BECMdevelpsignalgroup1Functiondevpsignalgroup6', 'BECMdevelpsignalgroup1Functiondevpsignalgroup7', 'BECMdevelpsignalgroup1Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup1Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup1Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup3"
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

    class BECMdevelpsignalgroup1Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup1Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup1Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup1Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup5"
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

    class BECMdevelpsignalgroup1Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup7"
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

    class BECMdevelpsignalgroup1Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup1Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class MgmPropFr05:
    msg_name = "MgmPropFr05"
    msg_id = 148
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['VDDM', 'ECM', 'S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IsgSpdActSgn800:
        sig_name = "IsgSpdActSgn800"
        sig_start_bit = 7
        update_id_bit = 23
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class IsgHeatPwrAct:
        sig_name = "IsgHeatPwrAct"
        sig_start_bit = 63
        update_id_bit = 51
        sig_length = 8
        sig_value_factor = 50
        sig_value_offset = 0
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


class BgmPropulsionFr08:
    msg_name = "BgmPropulsionFr08"
    msg_id = 593
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []
    sig_group_dict = {'ImobEngMgrReq13': ['ImobEngMgrReq13Chks', 'ImobEngMgrReq13Cntr', 'ImobEngMgrReq13ImobEngDataMgrReq0', 'ImobEngMgrReq13ImobEngDataMgrReq1', 'ImobEngMgrReq13ImobEngDataMgrReq2', 'ImobEngMgrReq13ImobEngDataMgrReq3', 'ImobEngMgrReq13ImobEngDataMgrReq4', 'ImobEngMgrReq13ImobEngDataMgrReq5', 'ImobEngMgrReq13ImobEngMgrCmdTar1']}
    sig_group_dataid_dict = {'ImobEngMgrReq13': 9731}

    class ImobEngMgrReq13ImobEngDataMgrReq1:
        sig_name = "ImobEngMgrReq13ImobEngDataMgrReq1"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq13Chks:
        sig_name = "ImobEngMgrReq13Chks"
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

    class ImobEngMgrReq13Cntr:
        sig_name = "ImobEngMgrReq13Cntr"
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

    class ImobEngMgrReq13ImobEngDataMgrReq4:
        sig_name = "ImobEngMgrReq13ImobEngDataMgrReq4"
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

    class ImobEngMgrReq13ImobEngDataMgrReq2:
        sig_name = "ImobEngMgrReq13ImobEngDataMgrReq2"
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

    class ImobEngMgrReq13_UB:
        sig_name = "ImobEngMgrReq13_UB"
        sig_start_bit = 12
        update_id_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ImobEngMgrReq13ImobEngDataMgrReq0:
        sig_name = "ImobEngMgrReq13ImobEngDataMgrReq0"
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

    class ImobEngMgrReq13ImobEngDataMgrReq3:
        sig_name = "ImobEngMgrReq13ImobEngDataMgrReq3"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq13ImobEngDataMgrReq5:
        sig_name = "ImobEngMgrReq13ImobEngDataMgrReq5"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq13ImobEngMgrCmdTar1:
        sig_name = "ImobEngMgrReq13ImobEngMgrCmdTar1"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobEngMgrReqCmd_ImobEngCmdTarIdle': 0, 'ImobEngMgrReqCmd_ImobEngMtnStrtReqCmd': 1, 'ImobEngMgrReqCmd_ImobEngNoMtnStrtReqCmd': 2, 'ImobEngMgrReqCmd_ImobEngTurnOffCmd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class VddmPropFr02:
    msg_name = "VddmPropFr02"
    msg_id = 98
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'BrkTq': ['BrkTqChks', 'BrkTqCntr', 'BrkTqQf', 'BrkTqRgnAtAxleReReq', 'BrkTqSts', 'BrkTqTotReqForPt']}
    sig_group_dataid_dict = {'BrkTq': 1201}

    class BrkTqRgnAtAxleReReq:
        sig_name = "BrkTqRgnAtAxleReReq"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class BrkTq_UB:
        sig_name = "BrkTq_UB"
        sig_start_bit = 6
        update_id_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BrkTqQf:
        sig_name = "BrkTqQf"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BrkTqSts:
        sig_name = "BrkTqSts"
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
        sig_value_table = {'BrkSts_NoBrake': 0, 'BrkSts_Brake': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkTqTotReqForPt:
        sig_name = "BrkTqTotReqForPt"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -16384
        sig_value_max = 16380
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111110, 0b00000001, 7, 1)]

    class BrkTqCntr:
        sig_name = "BrkTqCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RoadSgnInfoSts:
        sig_name = "RoadSgnInfoSts"
        sig_start_bit = 54
        update_id_bit = 55
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrfcSgnInfoSts_TSIUnknown': 0, 'TrfcSgnInfoSts_TSIOff': 1, 'TrfcSgnInfoSts_TSIOn_fusion': 2, 'TrfcSgnInfoSts_TSIOn_visiononlymode': 3, 'TrfcSgnInfoSts_TSIOn_navigationonlymode': 4, 'TrfcSgnInfoSts_TSIUnavailable': 5, 'TrfcSgnInfoSts_TSIServicerequired': 6, 'TrfcSgnInfoSts_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 54
        byte = 6
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class ChrgHndlStrtEna:
        sig_name = "ChrgHndlStrtEna"
        sig_start_bit = 51
        update_id_bit = 50
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgHndlStrtEna_PwrUpNotEna': 0, 'ChrgHndlStrtEna_PwrUpEna': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BrkTqChks:
        sig_name = "BrkTqChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class IgmMgmPropFr06:
    msg_name = "IgmMgmPropFr06"
    msg_id = 149
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['BECM1', 'ECM', 'VDDM']
    sig_group_dict = {'IsgTqAct': ['IsgTqActChks', 'IsgTqActCntr', 'IsgTqActIsgTqAct', 'IsgTqActQualityFactor']}
    sig_group_dataid_dict = {'IsgTqAct': 70}

    class IsgTqActQualityFactor:
        sig_name = "IsgTqActQualityFactor"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IsgTqActIsgTqAct:
        sig_name = "IsgTqActIsgTqAct"
        sig_start_bit = 21
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
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class IsgCluSts:
        sig_name = "IsgCluSts"
        sig_start_bit = 47
        update_id_bit = 5
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CluStsIndcn_Open': 0, 'CluStsIndcn_Close': 1, 'CluStsIndcn_StuckOpen': 2, 'CluStsIndcn_StuckClose': 3, 'CluStsIndcn_Undefined': 4, 'CluStsIndcn_Ongoing': 5}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class IsgTqAct_UB:
        sig_name = "IsgTqAct_UB"
        sig_start_bit = 4
        update_id_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class IsgTqActCntr:
        sig_name = "IsgTqActCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IsgModSts:
        sig_name = "IsgModSts"
        sig_start_bit = 38
        update_id_bit = 39
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IsgModTyp2_Inin': 0, 'IsgModTyp2_Stb': 1, 'IsgModTyp2_TqCtrl': 2, 'IsgModTyp2_SpdCtrl': 3, 'IsgModTyp2_UDcCtrl': 4, 'IsgModTyp2_PreChrg': 5, 'IsgModTyp2_PwrDwn': 6, 'IsgModTyp2_Flt': 7, 'IsgModTyp2_TcsCtrl': 8, 'IsgModTyp2_CluOpe': 9}
        compute_method = None
        length = 4
        startbit = 38
        byte = 4
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class BegCluReq:
        sig_name = "BegCluReq"
        sig_start_bit = 34
        update_id_bit = 32
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BegCluReq_Default': 0, 'BegCluReq_BegForCluReqClose': 1, 'BegCluReq_BegForCluReqOpen': 2, 'BegCluReq_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class IsgSpdActSgn:
        sig_name = "IsgSpdActSgn"
        sig_start_bit = 54
        update_id_bit = 55
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
        startbit = 54
        bmuws_info = [(6, 0b01111111, 0b10000000, 7, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class IsgTqActChks:
        sig_name = "IsgTqActChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class IemPropFr03:
    msg_name = "IemPropFr03"
    msg_id = 773
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlMotSysMotT:
        sig_name = "WhlMotSysMotT"
        sig_start_bit = 23
        update_id_bit = 8
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMotSysInvrT:
        sig_name = "WhlMotSysInvrT"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMotSysCoolgReq:
        sig_name = "WhlMotSysCoolgReq"
        sig_start_bit = 14
        update_id_bit = 11
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCoolg1_NoRequestForMoreCoolantPower': 0, 'HvCoolg1_IncreaseLevel1ForMoreCoolantPower': 1, 'HvCoolg1_IncreaseLevel2ForMoreCoolantPower': 2, 'HvCoolg1_MaxCoolingPower': 3, 'HvCoolg1_NotDefined': 4}
        compute_method = None
        length = 3
        startbit = 14
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class WhlMotSysErrIndcnReq:
        sig_name = "WhlMotSysErrIndcnReq"
        sig_start_bit = 10
        update_id_bit = 9
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
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class WhlMotClrRdyReq:
        sig_name = "WhlMotClrRdyReq"
        sig_start_bit = 24
        update_id_bit = 25
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
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class VddmPropFr21:
    msg_name = "VddmPropFr21"
    msg_id = 296
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'EpbSts': ['EpbStsChks', 'EpbStsCntr', 'EpbStsEpbSts']}
    sig_group_dataid_dict = {'EpbSts': 132}

    class EpbStsCntr:
        sig_name = "EpbStsCntr"
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

    class EpbStsChks:
        sig_name = "EpbStsChks"
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

    class EpbSts_UB:
        sig_name = "EpbSts_UB"
        sig_start_bit = 23
        update_id_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EpbStsEpbSts:
        sig_name = "EpbStsEpbSts"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EpbSts_Resd0': 0, 'EpbSts_Resd1': 1, 'EpbSts_Resd2': 2, 'EpbSts_AllAppld': 3, 'EpbSts_Resd4': 4, 'EpbSts_AllInTran': 5, 'EpbSts_BrkgDynByActr': 6, 'EpbSts_Resd7': 7, 'EpbSts_Resd8': 8, 'EpbSts_ActrAllReld': 9, 'EpbSts_BrkgDynDegraded': 10, 'EpbSts_Resd11': 11, 'EpbSts_BrkgDyn': 12, 'EpbSts_Resd13': 13, 'EpbSts_Resd14': 14, 'EpbSts_Err': 15}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class BecmPropFr28:
    msg_name = "BecmPropFr28"
    msg_id = 1180
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class TotDchaCap:
        sig_name = "TotDchaCap"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 32
        sig_value_factor = 0.01
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


class EcmPropFr04:
    msg_name = "EcmPropFr04"
    msg_id = 305
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'IEM', 'VDDM', 'HVCM']
    sig_group_dict = {'PtAllwdToTrsmActrSafe': ['PtAllwdToTrsmActrSafeChks', 'PtAllwdToTrsmActrSafeCntr', 'PtAllwdToTrsmActrSafePtAllwdToTrsmActr']}
    sig_group_dataid_dict = {'PtAllwdToTrsmActrSafe': 63}

    class PtDrftSts:
        sig_name = "PtDrftSts"
        sig_start_bit = 22
        update_id_bit = 19
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
        startbit = 22
        byte = 2
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class PtAllwdToTrsmActrSafeCntr:
        sig_name = "PtAllwdToTrsmActrSafeCntr"
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

    class PtAllwdToTrsmActrSafe_UB:
        sig_name = "PtAllwdToTrsmActrSafe_UB"
        sig_start_bit = 23
        update_id_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PtAllwdToTrsmActrSafeChks:
        sig_name = "PtAllwdToTrsmActrSafeChks"
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

    class DispHvBattLvlOfChrg:
        sig_name = "DispHvBattLvlOfChrg"
        sig_start_bit = 39
        update_id_bit = 43
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class DcDcActvdReq:
        sig_name = "DcDcActvdReq"
        sig_start_bit = 44
        update_id_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DcDcActvd_NoConversionToLVSide': 0, 'DcDcActvd_ConversionToLVSide': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PtAllwdToTrsmActrSafePtAllwdToTrsmActr:
        sig_name = "PtAllwdToTrsmActrSafePtAllwdToTrsmActr"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PtAllwdToTrsmActr1_NotAllwd1': 0, 'PtAllwdToTrsmActr1_RvsAllwd': 1, 'PtAllwdToTrsmActr1_RvsNotAllwd': 2, 'PtAllwdToTrsmActr1_NotAllwd2': 3, 'PtAllwdToTrsmActr1_ParkRelsAllwd': 4, 'PtAllwdToTrsmActr1_RvsAllwdAndParkRelsAllwd': 5, 'PtAllwdToTrsmActr1_RvsNotAllwdAndParkRelsAllwd': 6, 'PtAllwdToTrsmActr1_NotAllwd3': 7, 'PtAllwdToTrsmActr1_ParkRelsNotAllwd': 8, 'PtAllwdToTrsmActr1_RvsAllwdAndParkRelsNotAllwd': 9, 'PtAllwdToTrsmActr1_RvsNotAllwdAndParkRelsNotAllwd': 10, 'PtAllwdToTrsmActr1_NotAllwd4': 11, 'PtAllwdToTrsmActr1_NotAllwd5': 12, 'PtAllwdToTrsmActr1_NotAllwd6': 13, 'PtAllwdToTrsmActr1_NotAllwd7': 14, 'PtAllwdToTrsmActr1_NotAllwd8': 15}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class WhlMotSysPwrLimMax:
        sig_name = "WhlMotSysPwrLimMax"
        sig_start_bit = 41
        update_id_bit = 45
        sig_length = 10
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111111, 0b00000000, 8, 0)]


class CddIgmPropFr02:
    msg_name = "CddIgmPropFr02"
    msg_id = 329
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'IDcDcActLoSide': ['IDcDcActLoSideChks', 'IDcDcActLoSideCntr', 'IDcDcActLoSideIDcDcActLoSide']}
    sig_group_dataid_dict = {'IDcDcActLoSide': 20}

    class TDcDc:
        sig_name = "TDcDc"
        sig_start_bit = 7
        update_id_bit = 12
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IDcDcActLoSideIDcDcActLoSide:
        sig_name = "IDcDcActLoSideIDcDcActLoSide"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11110000, 0b00001111, 4, 4)]

    class IDcDcActLoSide_UB:
        sig_name = "IDcDcActLoSide_UB"
        sig_start_bit = 20
        update_id_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class IDcDcActLoSideCntr:
        sig_name = "IDcDcActLoSideCntr"
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

    class IDcDcActLoSideChks:
        sig_name = "IDcDcActLoSideChks"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DcDcCoolgReq:
        sig_name = "DcDcCoolgReq"
        sig_start_bit = 10
        update_id_bit = 11
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCoolg1_NoRequestForMoreCoolantPower': 0, 'HvCoolg1_IncreaseLevel1ForMoreCoolantPower': 1, 'HvCoolg1_IncreaseLevel2ForMoreCoolantPower': 2, 'HvCoolg1_MaxCoolingPower': 3, 'HvCoolg1_NotDefined': 4}
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class LimnIndcnDcDc:
        sig_name = "LimnIndcnDcDc"
        sig_start_bit = 55
        update_id_bit = 21
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class MgmPropFr03:
    msg_name = "MgmPropFr03"
    msg_id = 640
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.12
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CluDisConSucsCntr:
        sig_name = "CluDisConSucsCntr"
        sig_start_bit = 39
        update_id_bit = 61
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class CluDisConFailCntr:
        sig_name = "CluDisConFailCntr"
        sig_start_bit = 55
        update_id_bit = 62
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

    class CluConFailCntr:
        sig_name = "CluConFailCntr"
        sig_start_bit = 15
        update_id_bit = 0
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

    class CluConSucsCntr:
        sig_name = "CluConSucsCntr"
        sig_start_bit = 23
        update_id_bit = 63
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class IemPropdTCFr16:
    msg_name = "IemPropdTCFr16"
    msg_id = 272
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'DmcStsRearToEsc': ['DmcStsRearToEscChks', 'DmcStsRearToEscCntr', 'DmcStsRearToEscDmcActAppTarTq', 'DmcStsRearToEscDmcSts', 'DmcStsRearToEscDmcSWInfo']}
    sig_group_dataid_dict = {'DmcStsRearToEsc': 6015}

    class DmcStsRearToEscDmcSts:
        sig_name = "DmcStsRearToEscDmcSts"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DMC_Init': 0, 'DMC_On': 1, 'DMC_Off': 2, 'DMC_Fault': 3}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DmcStsRearToEscDmcActAppTarTq:
        sig_name = "DmcStsRearToEscDmcActAppTarTq"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -30000
        sig_value_max = 30000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsRearToEscChks:
        sig_name = "DmcStsRearToEscChks"
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

    class DmcStsRearToEscCntr:
        sig_name = "DmcStsRearToEscCntr"
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

    class DmcStsRearToEscDmcSWInfo:
        sig_name = "DmcStsRearToEscDmcSWInfo"
        sig_start_bit = 39
        update_id_bit = None
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsRearToEsc_UB:
        sig_name = "DmcStsRearToEsc_UB"
        sig_start_bit = 56
        update_id_bit = 56
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
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class BecmPropVFCVectorFr:
    msg_name = "BecmPropVFCVectorFr"
    msg_id = 1345
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'VFCVectorBECM': ['VFCVectorBECMBlockID', 'VFCVectorBECMVFCid0', 'VFCVectorBECMVFCid1', 'VFCVectorBECMVFCid10', 'VFCVectorBECMVFCid11', 'VFCVectorBECMVFCid12', 'VFCVectorBECMVFCid13', 'VFCVectorBECMVFCid14', 'VFCVectorBECMVFCid15', 'VFCVectorBECMVFCid16', 'VFCVectorBECMVFCid17', 'VFCVectorBECMVFCid18', 'VFCVectorBECMVFCid19', 'VFCVectorBECMVFCid2', 'VFCVectorBECMVFCid20', 'VFCVectorBECMVFCid21', 'VFCVectorBECMVFCid22', 'VFCVectorBECMVFCid23', 'VFCVectorBECMVFCid24', 'VFCVectorBECMVFCid25', 'VFCVectorBECMVFCid26', 'VFCVectorBECMVFCid27', 'VFCVectorBECMVFCid28', 'VFCVectorBECMVFCid29', 'VFCVectorBECMVFCid3', 'VFCVectorBECMVFCid30', 'VFCVectorBECMVFCid31', 'VFCVectorBECMVFCid32', 'VFCVectorBECMVFCid33', 'VFCVectorBECMVFCid34', 'VFCVectorBECMVFCid35', 'VFCVectorBECMVFCid36', 'VFCVectorBECMVFCid37', 'VFCVectorBECMVFCid38', 'VFCVectorBECMVFCid39', 'VFCVectorBECMVFCid4', 'VFCVectorBECMVFCid40', 'VFCVectorBECMVFCid41', 'VFCVectorBECMVFCid42', 'VFCVectorBECMVFCid43', 'VFCVectorBECMVFCid44', 'VFCVectorBECMVFCid45', 'VFCVectorBECMVFCid46', 'VFCVectorBECMVFCid47', 'VFCVectorBECMVFCid48', 'VFCVectorBECMVFCid49', 'VFCVectorBECMVFCid5', 'VFCVectorBECMVFCid50', 'VFCVectorBECMVFCid51', 'VFCVectorBECMVFCid52', 'VFCVectorBECMVFCid53', 'VFCVectorBECMVFCid54', 'VFCVectorBECMVFCid55', 'VFCVectorBECMVFCid56', 'VFCVectorBECMVFCid57', 'VFCVectorBECMVFCid58', 'VFCVectorBECMVFCid59', 'VFCVectorBECMVFCid6', 'VFCVectorBECMVFCid60', 'VFCVectorBECMVFCid61', 'VFCVectorBECMVFCid7', 'VFCVectorBECMVFCid8', 'VFCVectorBECMVFCid9']}
    sig_group_dataid_dict = {}

    class VFCVectorBECMVFCid23:
        sig_name = "VFCVectorBECMVFCid23"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBECMVFCid9:
        sig_name = "VFCVectorBECMVFCid9"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid35:
        sig_name = "VFCVectorBECMVFCid35"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid11:
        sig_name = "VFCVectorBECMVFCid11"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid43:
        sig_name = "VFCVectorBECMVFCid43"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid30:
        sig_name = "VFCVectorBECMVFCid30"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBECMVFCid38:
        sig_name = "VFCVectorBECMVFCid38"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBECMVFCid32:
        sig_name = "VFCVectorBECMVFCid32"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBECMVFCid53:
        sig_name = "VFCVectorBECMVFCid53"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid42:
        sig_name = "VFCVectorBECMVFCid42"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid1:
        sig_name = "VFCVectorBECMVFCid1"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid15:
        sig_name = "VFCVectorBECMVFCid15"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBECMVFCid39:
        sig_name = "VFCVectorBECMVFCid39"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBECMVFCid26:
        sig_name = "VFCVectorBECMVFCid26"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid20:
        sig_name = "VFCVectorBECMVFCid20"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid4:
        sig_name = "VFCVectorBECMVFCid4"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid21:
        sig_name = "VFCVectorBECMVFCid21"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid5:
        sig_name = "VFCVectorBECMVFCid5"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid37:
        sig_name = "VFCVectorBECMVFCid37"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid41:
        sig_name = "VFCVectorBECMVFCid41"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid16:
        sig_name = "VFCVectorBECMVFCid16"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBECMVFCid44:
        sig_name = "VFCVectorBECMVFCid44"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid49:
        sig_name = "VFCVectorBECMVFCid49"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid19:
        sig_name = "VFCVectorBECMVFCid19"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid46:
        sig_name = "VFCVectorBECMVFCid46"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBECMVFCid2:
        sig_name = "VFCVectorBECMVFCid2"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid36:
        sig_name = "VFCVectorBECMVFCid36"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid45:
        sig_name = "VFCVectorBECMVFCid45"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid8:
        sig_name = "VFCVectorBECMVFCid8"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBECMVFCid0:
        sig_name = "VFCVectorBECMVFCid0"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBECMVFCid28:
        sig_name = "VFCVectorBECMVFCid28"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid33:
        sig_name = "VFCVectorBECMVFCid33"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid57:
        sig_name = "VFCVectorBECMVFCid57"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid55:
        sig_name = "VFCVectorBECMVFCid55"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBECMVFCid59:
        sig_name = "VFCVectorBECMVFCid59"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid51:
        sig_name = "VFCVectorBECMVFCid51"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid48:
        sig_name = "VFCVectorBECMVFCid48"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBECMVFCid47:
        sig_name = "VFCVectorBECMVFCid47"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBECMVFCid12:
        sig_name = "VFCVectorBECMVFCid12"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid3:
        sig_name = "VFCVectorBECMVFCid3"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid52:
        sig_name = "VFCVectorBECMVFCid52"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid25:
        sig_name = "VFCVectorBECMVFCid25"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid17:
        sig_name = "VFCVectorBECMVFCid17"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorBECMVFCid22:
        sig_name = "VFCVectorBECMVFCid22"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBECMVFCid13:
        sig_name = "VFCVectorBECMVFCid13"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid54:
        sig_name = "VFCVectorBECMVFCid54"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBECMVFCid61:
        sig_name = "VFCVectorBECMVFCid61"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid58:
        sig_name = "VFCVectorBECMVFCid58"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid29:
        sig_name = "VFCVectorBECMVFCid29"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorBECMVFCid34:
        sig_name = "VFCVectorBECMVFCid34"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid18:
        sig_name = "VFCVectorBECMVFCid18"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid10:
        sig_name = "VFCVectorBECMVFCid10"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid50:
        sig_name = "VFCVectorBECMVFCid50"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorBECMVFCid56:
        sig_name = "VFCVectorBECMVFCid56"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBECMVFCid40:
        sig_name = "VFCVectorBECMVFCid40"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBECMVFCid6:
        sig_name = "VFCVectorBECMVFCid6"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBECMVFCid60:
        sig_name = "VFCVectorBECMVFCid60"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorBECMVFCid7:
        sig_name = "VFCVectorBECMVFCid7"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBECMVFCid31:
        sig_name = "VFCVectorBECMVFCid31"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorBECMVFCid24:
        sig_name = "VFCVectorBECMVFCid24"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorBECMVFCid27:
        sig_name = "VFCVectorBECMVFCid27"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorBECMVFCid14:
        sig_name = "VFCVectorBECMVFCid14"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorBECMBlockID:
        sig_name = "VFCVectorBECMBlockID"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class BecmPropFr30:
    msg_name = "BecmPropFr30"
    msg_id = 1144
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class TotDchaEgy:
        sig_name = "TotDchaEgy"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 32
        sig_value_factor = 1.0
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


class IemPropFr12:
    msg_name = "IemPropFr12"
    msg_id = 393
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM', 'VDDM', 'S2SReceiver']
    sig_group_dict = {'WhlMotSysSpdActSafe': ['WhlMotSysSpdActSafeChks', 'WhlMotSysSpdActSafeCntr', 'WhlMotSysSpdActSafeIsgSpdWSgnTyp', 'WhlMotSysSpdActSafeQf']}
    sig_group_dataid_dict = {'WhlMotSysSpdActSafe': 7001}

    class WhlMotSysSpdActSafeQf:
        sig_name = "WhlMotSysSpdActSafeQf"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlMotSysSpdActSafeIsgSpdWSgnTyp:
        sig_name = "WhlMotSysSpdActSafeIsgSpdWSgnTyp"
        sig_start_bit = 23
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class BoostStsFb1:
        sig_name = "BoostStsFb1"
        sig_start_bit = 47
        update_id_bit = 40
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BoostSt_Init': 0, 'BoostSt_C1Precharge': 1, 'BoostSt_BoostReady': 2, 'BoostSt_BoostActive': 3, 'BoostSt_C1activedischarge': 4, 'BoostSt_Fault': 5, 'BoostSt_Derating': 6, 'BoostSt_BoostOff': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class WhlMotSysSpdActSafe_UB:
        sig_name = "WhlMotSysSpdActSafe_UB"
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

    class WhlMotSysSpdActSafeChks:
        sig_name = "WhlMotSysSpdActSafeChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class WhlMotSysSpdActSafeCntr:
        sig_name = "WhlMotSysSpdActSafeCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class HvcmPropVFCVectorFr:
    msg_name = "HvcmPropVFCVectorFr"
    msg_id = 1366
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['CCM']
    sig_group_dict = {'VFCVectorHVCM': ['VFCVectorHVCMBlockID', 'VFCVectorHVCMVFCid0', 'VFCVectorHVCMVFCid1', 'VFCVectorHVCMVFCid10', 'VFCVectorHVCMVFCid11', 'VFCVectorHVCMVFCid12', 'VFCVectorHVCMVFCid13', 'VFCVectorHVCMVFCid14', 'VFCVectorHVCMVFCid15', 'VFCVectorHVCMVFCid16', 'VFCVectorHVCMVFCid17', 'VFCVectorHVCMVFCid18', 'VFCVectorHVCMVFCid19', 'VFCVectorHVCMVFCid2', 'VFCVectorHVCMVFCid20', 'VFCVectorHVCMVFCid21', 'VFCVectorHVCMVFCid22', 'VFCVectorHVCMVFCid23', 'VFCVectorHVCMVFCid24', 'VFCVectorHVCMVFCid25', 'VFCVectorHVCMVFCid26', 'VFCVectorHVCMVFCid27', 'VFCVectorHVCMVFCid28', 'VFCVectorHVCMVFCid29', 'VFCVectorHVCMVFCid3', 'VFCVectorHVCMVFCid30', 'VFCVectorHVCMVFCid31', 'VFCVectorHVCMVFCid32', 'VFCVectorHVCMVFCid33', 'VFCVectorHVCMVFCid34', 'VFCVectorHVCMVFCid35', 'VFCVectorHVCMVFCid36', 'VFCVectorHVCMVFCid37', 'VFCVectorHVCMVFCid38', 'VFCVectorHVCMVFCid39', 'VFCVectorHVCMVFCid4', 'VFCVectorHVCMVFCid40', 'VFCVectorHVCMVFCid41', 'VFCVectorHVCMVFCid42', 'VFCVectorHVCMVFCid43', 'VFCVectorHVCMVFCid44', 'VFCVectorHVCMVFCid45', 'VFCVectorHVCMVFCid46', 'VFCVectorHVCMVFCid47', 'VFCVectorHVCMVFCid48', 'VFCVectorHVCMVFCid49', 'VFCVectorHVCMVFCid5', 'VFCVectorHVCMVFCid50', 'VFCVectorHVCMVFCid51', 'VFCVectorHVCMVFCid52', 'VFCVectorHVCMVFCid53', 'VFCVectorHVCMVFCid54', 'VFCVectorHVCMVFCid55', 'VFCVectorHVCMVFCid56', 'VFCVectorHVCMVFCid57', 'VFCVectorHVCMVFCid58', 'VFCVectorHVCMVFCid59', 'VFCVectorHVCMVFCid6', 'VFCVectorHVCMVFCid60', 'VFCVectorHVCMVFCid61', 'VFCVectorHVCMVFCid7', 'VFCVectorHVCMVFCid8', 'VFCVectorHVCMVFCid9']}
    sig_group_dataid_dict = {}

    class VFCVectorHVCMVFCid14:
        sig_name = "VFCVectorHVCMVFCid14"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorHVCMVFCid15:
        sig_name = "VFCVectorHVCMVFCid15"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorHVCMVFCid19:
        sig_name = "VFCVectorHVCMVFCid19"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid47:
        sig_name = "VFCVectorHVCMVFCid47"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorHVCMVFCid12:
        sig_name = "VFCVectorHVCMVFCid12"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMVFCid51:
        sig_name = "VFCVectorHVCMVFCid51"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid23:
        sig_name = "VFCVectorHVCMVFCid23"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorHVCMVFCid0:
        sig_name = "VFCVectorHVCMVFCid0"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorHVCMVFCid33:
        sig_name = "VFCVectorHVCMVFCid33"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid4:
        sig_name = "VFCVectorHVCMVFCid4"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMBlockID:
        sig_name = "VFCVectorHVCMBlockID"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VFCVectorHVCMVFCid31:
        sig_name = "VFCVectorHVCMVFCid31"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorHVCMVFCid43:
        sig_name = "VFCVectorHVCMVFCid43"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid46:
        sig_name = "VFCVectorHVCMVFCid46"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorHVCMVFCid53:
        sig_name = "VFCVectorHVCMVFCid53"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid22:
        sig_name = "VFCVectorHVCMVFCid22"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorHVCMVFCid5:
        sig_name = "VFCVectorHVCMVFCid5"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid28:
        sig_name = "VFCVectorHVCMVFCid28"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMVFCid30:
        sig_name = "VFCVectorHVCMVFCid30"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorHVCMVFCid21:
        sig_name = "VFCVectorHVCMVFCid21"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid1:
        sig_name = "VFCVectorHVCMVFCid1"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid9:
        sig_name = "VFCVectorHVCMVFCid9"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid3:
        sig_name = "VFCVectorHVCMVFCid3"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid27:
        sig_name = "VFCVectorHVCMVFCid27"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid39:
        sig_name = "VFCVectorHVCMVFCid39"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorHVCMVFCid45:
        sig_name = "VFCVectorHVCMVFCid45"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid16:
        sig_name = "VFCVectorHVCMVFCid16"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorHVCMVFCid11:
        sig_name = "VFCVectorHVCMVFCid11"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid24:
        sig_name = "VFCVectorHVCMVFCid24"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorHVCMVFCid41:
        sig_name = "VFCVectorHVCMVFCid41"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid40:
        sig_name = "VFCVectorHVCMVFCid40"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorHVCMVFCid32:
        sig_name = "VFCVectorHVCMVFCid32"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorHVCMVFCid18:
        sig_name = "VFCVectorHVCMVFCid18"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid34:
        sig_name = "VFCVectorHVCMVFCid34"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid29:
        sig_name = "VFCVectorHVCMVFCid29"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid6:
        sig_name = "VFCVectorHVCMVFCid6"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorHVCMVFCid38:
        sig_name = "VFCVectorHVCMVFCid38"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorHVCMVFCid54:
        sig_name = "VFCVectorHVCMVFCid54"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorHVCMVFCid52:
        sig_name = "VFCVectorHVCMVFCid52"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMVFCid61:
        sig_name = "VFCVectorHVCMVFCid61"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid49:
        sig_name = "VFCVectorHVCMVFCid49"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid10:
        sig_name = "VFCVectorHVCMVFCid10"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid58:
        sig_name = "VFCVectorHVCMVFCid58"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid37:
        sig_name = "VFCVectorHVCMVFCid37"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid56:
        sig_name = "VFCVectorHVCMVFCid56"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorHVCMVFCid8:
        sig_name = "VFCVectorHVCMVFCid8"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorHVCMVFCid25:
        sig_name = "VFCVectorHVCMVFCid25"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid7:
        sig_name = "VFCVectorHVCMVFCid7"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorHVCMVFCid2:
        sig_name = "VFCVectorHVCMVFCid2"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid44:
        sig_name = "VFCVectorHVCMVFCid44"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMVFCid20:
        sig_name = "VFCVectorHVCMVFCid20"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMVFCid42:
        sig_name = "VFCVectorHVCMVFCid42"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid55:
        sig_name = "VFCVectorHVCMVFCid55"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorHVCMVFCid57:
        sig_name = "VFCVectorHVCMVFCid57"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid36:
        sig_name = "VFCVectorHVCMVFCid36"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMVFCid13:
        sig_name = "VFCVectorHVCMVFCid13"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorHVCMVFCid26:
        sig_name = "VFCVectorHVCMVFCid26"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid35:
        sig_name = "VFCVectorHVCMVFCid35"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid60:
        sig_name = "VFCVectorHVCMVFCid60"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorHVCMVFCid17:
        sig_name = "VFCVectorHVCMVFCid17"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorHVCMVFCid50:
        sig_name = "VFCVectorHVCMVFCid50"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorHVCMVFCid59:
        sig_name = "VFCVectorHVCMVFCid59"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorHVCMVFCid48:
        sig_name = "VFCVectorHVCMVFCid48"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class BecmPropDevFr07:
    msg_name = "BecmPropDevFr07"
    msg_id = 1492
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup7': ['BECMdevelpsignalgroup7Functiondevpsignalgroup1', 'BECMdevelpsignalgroup7Functiondevpsignalgroup2', 'BECMdevelpsignalgroup7Functiondevpsignalgroup3', 'BECMdevelpsignalgroup7Functiondevpsignalgroup4', 'BECMdevelpsignalgroup7Functiondevpsignalgroup5', 'BECMdevelpsignalgroup7Functiondevpsignalgroup6', 'BECMdevelpsignalgroup7Functiondevpsignalgroup7', 'BECMdevelpsignalgroup7Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup7Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup7Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup7Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup7Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup7Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup7Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup7Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup7Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup7Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup7Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup7Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup7Functiondevpsignalgroup3"
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

    class BECMdevelpsignalgroup7Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup7Functiondevpsignalgroup7"
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

    class BECMdevelpsignalgroup7Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup7Functiondevpsignalgroup5"
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


class BecmPropFr08:
    msg_name = "BecmPropFr08"
    msg_id = 834
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvCellUOverFlt:
        sig_name = "HvCellUOverFlt"
        sig_start_bit = 53
        update_id_bit = 34
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvCellUUnderFlt:
        sig_name = "HvCellUUnderFlt"
        sig_start_bit = 15
        update_id_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattCodLen:
        sig_name = "HvBattCodLen"
        sig_start_bit = 23
        update_id_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattMismatchFlt:
        sig_name = "HvBattMismatchFlt"
        sig_start_bit = 7
        update_id_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvSocHiFlt:
        sig_name = "HvSocHiFlt"
        sig_start_bit = 63
        update_id_bit = 48
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvilFlt:
        sig_name = "HvilFlt"
        sig_start_bit = 0
        update_id_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HvBattPreHeatgReqForAC:
        sig_name = "HvBattPreHeatgReqForAC"
        sig_start_bit = 61
        update_id_bit = 59
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PreHeatgReq_Default': 0, 'PreHeatgReq_On': 1, 'PreHeatgReq_Off': 2, 'PreHeatgReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvBattNr:
        sig_name = "HvBattNr"
        sig_start_bit = 31
        update_id_bit = 37
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvIsoFlt:
        sig_name = "HvIsoFlt"
        sig_start_bit = 13
        update_id_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvCellTDifFlt:
        sig_name = "HvCellTDifFlt"
        sig_start_bit = 6
        update_id_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HvPackUOverFlt:
        sig_name = "HvPackUOverFlt"
        sig_start_bit = 9
        update_id_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HvPackUUnderFlt:
        sig_name = "HvPackUUnderFlt"
        sig_start_bit = 47
        update_id_bit = 32
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvCellUDifFlt:
        sig_name = "HvCellUDifFlt"
        sig_start_bit = 3
        update_id_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvSocLoFlt:
        sig_name = "HvSocLoFlt"
        sig_start_bit = 51
        update_id_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvCellTOverFlt:
        sig_name = "HvCellTOverFlt"
        sig_start_bit = 55
        update_id_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvPackOverChrgFlt:
        sig_name = "HvPackOverChrgFlt"
        sig_start_bit = 11
        update_id_bit = 40
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvSocHopFlt:
        sig_name = "HvSocHopFlt"
        sig_start_bit = 45
        update_id_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FauLevel_Normal': 0, 'FauLevel_LevelI': 1, 'FauLevel_LevelII': 2, 'FauLevel_LevelIII': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class BecmPropFr33:
    msg_name = "BecmPropFr33"
    msg_id = 1026
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {'RemoteBookStrtTiChrgnTmr': ['RemoteBookStrtTiChrgnTmrChrgnTmrhour', 'RemoteBookStrtTiChrgnTmrChrgnTmrmin'], 'RemoteBookStopTiChrgnTmr': ['RemoteBookStopTiChrgnTmrChrgnTmrhour', 'RemoteBookStopTiChrgnTmrChrgnTmrmin']}
    sig_group_dataid_dict = {}

    class RemoteBookStrtTiChrgnTmrChrgnTmrmin:
        sig_name = "RemoteBookStrtTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RemoteBookStrtTiChrgnTmrChrgnTmrhour:
        sig_name = "RemoteBookStrtTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RemoteBookStrtTiChrgnTmr_UB:
        sig_name = "RemoteBookStrtTiChrgnTmr_UB"
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

    class RemoteBookStopTiChrgnTmrChrgnTmrmin:
        sig_name = "RemoteBookStopTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RemoteBookStopTiChrgnTmr_UB:
        sig_name = "RemoteBookStopTiChrgnTmr_UB"
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

    class RemoteBookStopTiChrgnTmrChrgnTmrhour:
        sig_name = "RemoteBookStopTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BecmPropFr23:
    msg_name = "BecmPropFr23"
    msg_id = 322
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'HvBattCellUInfo': ['HvBattCellUInfoU1', 'HvBattCellUInfoU2', 'HvBattCellUInfoU3', 'HvBattCellUInfoU4']}
    sig_group_dataid_dict = {}

    class HvBattCellUInfoU3:
        sig_name = "HvBattCellUInfoU3"
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

    class HvBattCellUInfo_UB:
        sig_name = "HvBattCellUInfo_UB"
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

    class HvBattCellUInfoU2:
        sig_name = "HvBattCellUInfoU2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattLimnIndcn:
        sig_name = "HvBattLimnIndcn"
        sig_start_bit = 55
        update_id_bit = 40
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class HvBattCellUInfoU4:
        sig_name = "HvBattCellUInfoU4"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 13
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111000, 0b00000111, 5, 3)]

    class HvBattCellUInfoU1:
        sig_name = "HvBattCellUInfoU1"
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


class IgmMgmPropFr04:
    msg_name = "IgmMgmPropFr04"
    msg_id = 512
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ImobEngChk3': ['ImobEngChk3ImobEngChkSts', 'ImobEngChk3ImobEngDataChk0', 'ImobEngChk3ImobEngDataChk1', 'ImobEngChk3ImobEngDataChk2', 'ImobEngChk3ImobEngDataChk3', 'ImobEngChk3ImobEngDataChk4', 'ImobEngChk3ImobEngDataChk5', 'ImobEngChk3ImobEngDataChk6']}
    sig_group_dataid_dict = {}

    class ImobEngChk3_UB:
        sig_name = "ImobEngChk3_UB"
        sig_start_bit = 1
        update_id_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ImobEngChk3ImobEngDataChk5:
        sig_name = "ImobEngChk3ImobEngDataChk5"
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

    class ImobEngChk3ImobEngDataChk3:
        sig_name = "ImobEngChk3ImobEngDataChk3"
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

    class ImobEngChk3ImobEngChkSts:
        sig_name = "ImobEngChk3ImobEngChkSts"
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
        sig_value_table = {'AvlSts2_NotAvl': 0, 'AvlSts2_Avl': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ImobEngChk3ImobEngDataChk6:
        sig_name = "ImobEngChk3ImobEngDataChk6"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk3ImobEngDataChk1:
        sig_name = "ImobEngChk3ImobEngDataChk1"
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

    class ImobEngChk3ImobEngDataChk4:
        sig_name = "ImobEngChk3ImobEngDataChk4"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngSts3:
        sig_name = "ImobEngSts3"
        sig_start_bit = 3
        update_id_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobSts_ImobUndefd': 0, 'ImobSts_ImobImobn': 1, 'ImobSts_ImobMtn': 2, 'ImobSts_ImobNoMtn': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ImobEngChk3ImobEngDataChk0:
        sig_name = "ImobEngChk3ImobEngDataChk0"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk3ImobEngDataChk2:
        sig_name = "ImobEngChk3ImobEngDataChk2"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class IemEduPropFr01:
    msg_name = "IemEduPropFr01"
    msg_id = 76
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['BECM1', 'ECM', 'VDDM']
    sig_group_dict = {'WhlMotSysTqAvl': ['WhlMotSysTqAvlTqAvlMax', 'WhlMotSysTqAvlTqAvlMin'], 'WhlMotSysTqEst': ['WhlMotSysTqEstChks', 'WhlMotSysTqEstCntr', 'WhlMotSysTqEstIsgTqAct', 'WhlMotSysTqEstQualityFactor']}
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

    class WhlMotSysModSts:
        sig_name = "WhlMotSysModSts"
        sig_start_bit = 35
        update_id_bit = 36
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysModStsTyp2_Inin': 0, 'WhlMotSysModStsTyp2_Stb': 1, 'WhlMotSysModStsTyp2_TqCtrl': 2, 'WhlMotSysModStsTyp2_SpdCtrlIdle': 3, 'WhlMotSysModStsTyp2_CluOper': 4, 'WhlMotSysModStsTyp2_PreChrg': 5, 'WhlMotSysModStsTyp2_PwrDwn': 6, 'WhlMotSysModStsTyp2_Flt': 7, 'WhlMotSysModStsTyp2_TcsCtrl': 8}
        compute_method = None
        length = 4
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

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

    class WhlMotSysTqAvl_UB:
        sig_name = "WhlMotSysTqAvl_UB"
        sig_start_bit = 37
        update_id_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

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

    class WhlMotSysTqAvlTqAvlMin:
        sig_name = "WhlMotSysTqAvlTqAvlMin"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 4.0
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 51
        bmuws_info = [(6, 0b00001111, 0b11110000, 4, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotSysTqAvlTqAvlMax:
        sig_name = "WhlMotSysTqAvlTqAvlMax"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 12
        sig_value_factor = 4.0
        sig_value_offset = -8188.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11110000, 0b00001111, 4, 4)]


class VddmPropFr17:
    msg_name = "VddmPropFr17"
    msg_id = 354
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'HVCM', 'EGSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BattProtectSwt:
        sig_name = "BattProtectSwt"
        sig_start_bit = 59
        update_id_bit = 57
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

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


class BecmPropFr17:
    msg_name = "BecmPropFr17"
    msg_id = 837
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattThermMod:
        sig_name = "HvBattThermMod"
        sig_start_bit = 63
        update_id_bit = 34
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattThermMod_Idle': 0, 'HvBattThermMod_ThermalBalancing': 1, 'HvBattThermMod_PassiveHeating': 2, 'HvBattThermMod_ActiveHeating': 3, 'HvBattThermMod_PassiveCooling': 4, 'HvBattThermMod_ActiveCooling': 5, 'HvBattThermMod_CombinedCooling': 6, 'HvBattThermMod_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 63
        byte = 7
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HvBattTMaxSerlNr:
        sig_name = "HvBattTMaxSerlNr"
        sig_start_bit = 23
        update_id_bit = 38
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCellTNr:
        sig_name = "HvBattCellTNr"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65531
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvBattCooltMaxTReq:
        sig_name = "HvBattCooltMaxTReq"
        sig_start_bit = 47
        update_id_bit = 36
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattTMinSerlNr:
        sig_name = "HvBattTMinSerlNr"
        sig_start_bit = 31
        update_id_bit = 37
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattPreHeatgReq:
        sig_name = "HvBattPreHeatgReq"
        sig_start_bit = 60
        update_id_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PreHeatgReq_Default': 0, 'PreHeatgReq_On': 1, 'PreHeatgReq_Off': 2, 'PreHeatgReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HvBattCooltMinTReq:
        sig_name = "HvBattCooltMinTReq"
        sig_start_bit = 55
        update_id_bit = 35
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BecmPropFr11:
    msg_name = "BecmPropFr11"
    msg_id = 817
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattCooltFlowReq:
        sig_name = "HvBattCooltFlowReq"
        sig_start_bit = 8
        update_id_bit = 38
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 8
        bmuws_info = [(1, 0b00000001, 0b11111110, 1, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class HvBattBalFlg:
        sig_name = "HvBattBalFlg"
        sig_start_bit = 11
        update_id_bit = 10
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

    class DCChrgnNegPortT:
        sig_name = "DCChrgnNegPortT"
        sig_start_bit = 63
        update_id_bit = 12
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCoolgEgyReq1:
        sig_name = "HvBattCoolgEgyReq1"
        sig_start_bit = 7
        update_id_bit = 39
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class DCChrgnPosPortT:
        sig_name = "DCChrgnPosPortT"
        sig_start_bit = 31
        update_id_bit = 13
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCooltT:
        sig_name = "HvBattCooltT"
        sig_start_bit = 47
        update_id_bit = 37
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -60.0
        sig_value_min = 0
        sig_value_max = 1850
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]


class HvcmToVddmPropDiagRespFrame:
    msg_name = "HvcmToVddmPropDiagRespFrame"
    msg_id = 1616
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VcuPropFr01:
    msg_name = "VcuPropFr01"
    msg_id = 678
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class MCUBoostChrgRlyReq:
        sig_name = "MCUBoostChrgRlyReq"
        sig_start_bit = 23
        update_id_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgRlySt_Open': 0, 'ChrgRlySt_Close': 1, 'ChrgRlySt_Reserved1': 2, 'ChrgRlySt_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BgmPropulsionFr01:
    msg_name = "BgmPropulsionFr01"
    msg_id = 636
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1', 'S2SReceiver', 'EGSM', 'ECM']
    sig_group_dict = {'ExhibitionModeSts': ['ExhibitionModeStsChks', 'ExhibitionModeStsCntr', 'ExhibitionModeStsExhibitionModeSts']}
    sig_group_dataid_dict = {'ExhibitionModeSts': 9001}

    class LocalHvBattThermReq:
        sig_name = "LocalHvBattThermReq"
        sig_start_bit = 35
        update_id_bit = 32
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptSts_NoRequest': 0, 'CmptSts_CoolingRequest': 1, 'CmptSts_HeatingRequest': 2, 'CmptSts_CoolingAndHeatingRequest': 3, 'CmptSts_PostHeating': 4}
        compute_method = None
        length = 3
        startbit = 35
        byte = 4
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class LocalHvBattThermTarT:
        sig_name = "LocalHvBattThermTarT"
        sig_start_bit = 55
        update_id_bit = 56
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 80
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ExhibitionModeStsChks:
        sig_name = "ExhibitionModeStsChks"
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

    class ExhibitionModeStsExhibitionModeSts:
        sig_name = "ExhibitionModeStsExhibitionModeSts"
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
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class NOPCoolReqFromCDC:
        sig_name = "NOPCoolReqFromCDC"
        sig_start_bit = 6
        update_id_bit = 5
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ActvnOfDoorSwtIllmn:
        sig_name = "ActvnOfDoorSwtIllmn"
        sig_start_bit = 39
        update_id_bit = 38
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

    class ExhibitionModeStsCntr:
        sig_name = "ExhibitionModeStsCntr"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RemHvBattHeatgTarT:
        sig_name = "RemHvBattHeatgTarT"
        sig_start_bit = 15
        update_id_bit = 3
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 80
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RemHvBattHeatgReq:
        sig_name = "RemHvBattHeatgReq"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RemHvBattHeatgReq_OFF': 0, 'RemHvBattHeatgReq_ON': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class GearLvrIndcnInv:
        sig_name = "GearLvrIndcnInv"
        sig_start_bit = 47
        update_id_bit = 44
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 7
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrIndcnInv_P': 0, 'GearLvrIndcnInv_R': 1, 'GearLvrIndcnInv_D': 2, 'GearLvrIndcnInv_Reserved1': 3, 'GearLvrIndcnInv_Reserved2': 4, 'GearLvrIndcnInv_Reserved3': 5, 'GearLvrIndcnInv_Reserved4': 6, 'GearLvrIndcnInv_NOINDICATION': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HvBattClimaPrioReq:
        sig_name = "HvBattClimaPrioReq"
        sig_start_bit = 42
        update_id_bit = 40
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaPriority_Default': 0, 'ClimaPriority_BattClimaPrio': 1, 'ClimaPriority_CmptmtClimaPrio': 2, 'ClimaPriority_Reserved1': 3}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class DischrgInCarSw:
        sig_name = "DischrgInCarSw"
        sig_start_bit = 37
        update_id_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DisChrgrSW_Off': 0, 'DisChrgrSW_V2V': 1, 'DisChrgrSW_V2L': 2}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ExhibitionModeSts_UB:
        sig_name = "ExhibitionModeSts_UB"
        sig_start_bit = 29
        update_id_bit = 29
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
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PlsHeatgReq:
        sig_name = "PlsHeatgReq"
        sig_start_bit = 1
        update_id_bit = 0
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class BgmPropulsionFr02:
    msg_name = "BgmPropulsionFr02"
    msg_id = 1008
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1']
    sig_group_dict = {'LocalBookStrtTiChrgnTmr': ['LocalBookStrtTiChrgnTmrChrgnTmrhour', 'LocalBookStrtTiChrgnTmrChrgnTmrmin'], 'LocalBookStopTiChrgnTmr': ['LocalBookStopTiChrgnTmrChrgnTmrhour', 'LocalBookStopTiChrgnTmrChrgnTmrmin']}
    sig_group_dataid_dict = {}

    class LocalBookStopTiChrgnTmrChrgnTmrhour:
        sig_name = "LocalBookStopTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LocalBookStrtTiChrgnTmr_UB:
        sig_name = "LocalBookStrtTiChrgnTmr_UB"
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

    class ReservedSigForHVBatt1:
        sig_name = "ReservedSigForHVBatt1"
        sig_start_bit = 47
        update_id_bit = 43
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

    class LocalBookStrtTiChrgnTmrChrgnTmrhour:
        sig_name = "LocalBookStrtTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LocalBookStopTiChrgnTmrChrgnTmrmin:
        sig_name = "LocalBookStopTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LocalBookStrtTiChrgnTmrChrgnTmrmin:
        sig_name = "LocalBookStrtTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LocalBookStopTiChrgnTmr_UB:
        sig_name = "LocalBookStopTiChrgnTmr_UB"
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

    class ReservedSigForHVBatt3:
        sig_name = "ReservedSigForHVBatt3"
        sig_start_bit = 63
        update_id_bit = 59
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

    class HVIntelligentChrgSWSt:
        sig_name = "HVIntelligentChrgSWSt"
        sig_start_bit = 23
        update_id_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FOTAStatus:
        sig_name = "FOTAStatus"
        sig_start_bit = 55
        update_id_bit = 56
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Idle': 0, 'Query': 1, 'Downloading': 2, 'Active': 3, 'Update': 4, 'Rollback': 5, 'UpdateFailNotDriving': 6}
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VgmToSrsISO26021PropDiagResFrame11:
    msg_name = "VgmToSrsISO26021PropDiagResFrame11"
    msg_id = 2033
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['SRS']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MgmPropFr02:
    msg_name = "MgmPropFr02"
    msg_id = 1179
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['CCM']
    sig_group_dict = {'MGMTestFr2': ['MGMTestFr2Byte0', 'MGMTestFr2Byte1', 'MGMTestFr2Byte2', 'MGMTestFr2Byte3', 'MGMTestFr2Byte4', 'MGMTestFr2Byte5', 'MGMTestFr2Byte6', 'MGMTestFr2Byte7']}
    sig_group_dataid_dict = {}

    class MGMTestFr2Byte7:
        sig_name = "MGMTestFr2Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MGMTestFr2Byte6:
        sig_name = "MGMTestFr2Byte6"
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

    class MGMTestFr2Byte1:
        sig_name = "MGMTestFr2Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MGMTestFr2Byte4:
        sig_name = "MGMTestFr2Byte4"
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

    class MGMTestFr2Byte0:
        sig_name = "MGMTestFr2Byte0"
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

    class MGMTestFr2Byte2:
        sig_name = "MGMTestFr2Byte2"
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

    class MGMTestFr2Byte3:
        sig_name = "MGMTestFr2Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MGMTestFr2Byte5:
        sig_name = "MGMTestFr2Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VgmToEcmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToEcmJ1979OBDPropCanReqFrame11"
    msg_id = 2016
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmPropFr00:
    msg_name = "EcmPropFr00"
    msg_id = 74
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'VDDM', 'BGM']
    sig_group_dict = {'AccrPedlRat': ['AccrPedlRatAccrPedlRat', 'AccrPedlRatChks', 'AccrPedlRatCntr']}
    sig_group_dataid_dict = {'AccrPedlRat': 868}

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

    class IsgCluOperTypReq:
        sig_name = "IsgCluOperTypReq"
        sig_start_bit = 27
        update_id_bit = 24
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysCluStsTyp1_NoReq': 0, 'WhlMotSysCluStsTyp1_ReqDisEngd': 1, 'WhlMotSysCluStsTyp1_SlwPosDiffSpd': 2, 'WhlMotSysCluStsTyp1_FstPosDiffSpd': 3, 'WhlMotSysCluStsTyp1_SlwNegDiffSpd': 4, 'WhlMotSysCluStsTyp1_FstNegDiffSpd': 5, 'WhlMotSysCluStsTyp1_Reserved1': 6, 'WhlMotSysCluStsTyp1_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 27
        byte = 3
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

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

    class IsgModReq:
        sig_name = "IsgModReq"
        sig_start_bit = 47
        update_id_bit = 43
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IsgModTyp1_Inin': 0, 'IsgModTyp1_Stb': 1, 'IsgModTyp1_TqCtrl': 2, 'IsgModTyp1_SpdCtrl': 3, 'IsgModTyp1_UDcCtrl': 4, 'IsgModTyp1_PreChrg': 5, 'IsgModTyp1_PwrDwn': 6, 'IsgModTyp1_Flt': 7, 'IsgModTyp1_TcsCtrl': 8, 'IsgModTyp1_Reserved1': 9, 'IsgModTyp1_Reserved2': 10, 'IsgModTyp1_Reserved3': 11, 'IsgModTyp1_Reserved4': 12, 'IsgModTyp1_Reserved5': 13, 'IsgModTyp1_Reserved6': 14, 'IsgModTyp1_Reserved7': 15}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class IsgSpdReq:
        sig_name = "IsgSpdReq"
        sig_start_bit = 54
        update_id_bit = 55
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
        startbit = 54
        bmuws_info = [(6, 0b01111111, 0b10000000, 7, 0), (7, 0b11111111, 0b00000000, 8, 0)]

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


class CddObcPropFr03:
    msg_name = "CddObcPropFr03"
    msg_id = 298
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class OnBdChrgrS2Sts:
        sig_name = "OnBdChrgrS2Sts"
        sig_start_bit = 31
        update_id_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'S2Sts_Default': 0, 'S2Sts_Open': 1, 'S2Sts_Closed': 2, 'S2Sts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class OnBdChrgrUAct:
        sig_name = "OnBdChrgrUAct"
        sig_start_bit = 50
        update_id_bit = 55
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class DchaEgyAct:
        sig_name = "DchaEgyAct"
        sig_start_bit = 10
        update_id_bit = 37
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class HndlLockgSts:
        sig_name = "HndlLockgSts"
        sig_start_bit = 52
        update_id_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockgSts_Unknown': 0, 'LockgSts_Locked': 1, 'LockgSts_Unlocked': 2, 'LockgSts_Fault': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class OnBdChrgrUDc:
        sig_name = "OnBdChrgrUDc"
        sig_start_bit = 36
        update_id_bit = 53
        sig_length = 13
        sig_value_factor = 0.2
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 6000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ReservedSigForHVBatt2:
        sig_name = "ReservedSigForHVBatt2"
        sig_start_bit = 29
        update_id_bit = 24
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
        startbit = 29
        byte = 3
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class OnBdChrgrIDc:
        sig_name = "OnBdChrgrIDc"
        sig_start_bit = 6
        update_id_bit = 54
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = -200.0
        sig_value_min = 0
        sig_value_max = 4000
        sig_byteorder = "Motorola"
        sig_value_init = 2000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111000, 0b00000111, 5, 3)]


class VddmPropFr32:
    msg_name = "VddmPropFr32"
    msg_id = 1042
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.5
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'ClimateCtrlInFuture': ['ClimateCtrlInFuturePwrAtTime', 'ClimateCtrlInFutureSequenceNo', 'ClimateCtrlInFutureTempAtTime', 'ClimateCtrlInFutureThermModAtTime', 'ClimateCtrlInFutureTime', 'ClimateCtrlInFutureVersionNo']}
    sig_group_dataid_dict = {}

    class ClimateCtrlInFutureTempAtTime:
        sig_name = "ClimateCtrlInFutureTempAtTime"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ClimateCtrlInFutureThermModAtTime:
        sig_name = "ClimateCtrlInFutureThermModAtTime"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Idle': 0, 'ThermalBalancing': 1, 'PassiveHeating': 2, 'ActiveHeating': 3, 'PassiveCooling': 4, 'ActiveCooling': 5, 'CombinedCooling': 6, 'Reserved': 7}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ClimateCtrlInFutureSequenceNo:
        sig_name = "ClimateCtrlInFutureSequenceNo"
        sig_start_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class ClimateCtrlInFutureTime:
        sig_name = "ClimateCtrlInFutureTime"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ClimateCtrlInFuture_UB:
        sig_name = "ClimateCtrlInFuture_UB"
        sig_start_bit = 3
        update_id_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ClimateCtrlInFutureVersionNo:
        sig_name = "ClimateCtrlInFutureVersionNo"
        sig_start_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class ClimateCtrlInFuturePwrAtTime:
        sig_name = "ClimateCtrlInFuturePwrAtTime"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 50
        sig_value_offset = -25000.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class BecmPropDevFr05:
    msg_name = "BecmPropDevFr05"
    msg_id = 1490
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup5': ['BECMdevelpsignalgroup5Functiondevpsignalgroup1', 'BECMdevelpsignalgroup5Functiondevpsignalgroup2', 'BECMdevelpsignalgroup5Functiondevpsignalgroup3', 'BECMdevelpsignalgroup5Functiondevpsignalgroup4', 'BECMdevelpsignalgroup5Functiondevpsignalgroup5', 'BECMdevelpsignalgroup5Functiondevpsignalgroup6', 'BECMdevelpsignalgroup5Functiondevpsignalgroup7', 'BECMdevelpsignalgroup5Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup5Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup5Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup5Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup5Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup5Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup5Functiondevpsignalgroup5"
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

    class BECMdevelpsignalgroup5Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup5Functiondevpsignalgroup7"
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

    class BECMdevelpsignalgroup5Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup5Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup5Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup5Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup5Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup5Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup5Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup5Functiondevpsignalgroup3"
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


class EcmPropFr29:
    msg_name = "EcmPropFr29"
    msg_id = 278
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvAuxActPwr:
        sig_name = "HvAuxActPwr"
        sig_start_bit = 7
        update_id_bit = 13
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class VgmToIemJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToIemJ1979OBDPropCanReqFrame11"
    msg_id = 2019
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['IEM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EgsmPropVFCVectorFr:
    msg_name = "EgsmPropVFCVectorFr"
    msg_id = 1349
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['CCM']
    sig_group_dict = {'VFCVectorEGSM': ['VFCVectorEGSMBlockID', 'VFCVectorEGSMVFCid0', 'VFCVectorEGSMVFCid1', 'VFCVectorEGSMVFCid10', 'VFCVectorEGSMVFCid11', 'VFCVectorEGSMVFCid12', 'VFCVectorEGSMVFCid13', 'VFCVectorEGSMVFCid14', 'VFCVectorEGSMVFCid15', 'VFCVectorEGSMVFCid16', 'VFCVectorEGSMVFCid17', 'VFCVectorEGSMVFCid18', 'VFCVectorEGSMVFCid19', 'VFCVectorEGSMVFCid2', 'VFCVectorEGSMVFCid20', 'VFCVectorEGSMVFCid21', 'VFCVectorEGSMVFCid22', 'VFCVectorEGSMVFCid23', 'VFCVectorEGSMVFCid24', 'VFCVectorEGSMVFCid25', 'VFCVectorEGSMVFCid26', 'VFCVectorEGSMVFCid27', 'VFCVectorEGSMVFCid28', 'VFCVectorEGSMVFCid29', 'VFCVectorEGSMVFCid3', 'VFCVectorEGSMVFCid30', 'VFCVectorEGSMVFCid31', 'VFCVectorEGSMVFCid32', 'VFCVectorEGSMVFCid33', 'VFCVectorEGSMVFCid34', 'VFCVectorEGSMVFCid35', 'VFCVectorEGSMVFCid36', 'VFCVectorEGSMVFCid37', 'VFCVectorEGSMVFCid38', 'VFCVectorEGSMVFCid39', 'VFCVectorEGSMVFCid4', 'VFCVectorEGSMVFCid40', 'VFCVectorEGSMVFCid41', 'VFCVectorEGSMVFCid42', 'VFCVectorEGSMVFCid43', 'VFCVectorEGSMVFCid44', 'VFCVectorEGSMVFCid45', 'VFCVectorEGSMVFCid46', 'VFCVectorEGSMVFCid47', 'VFCVectorEGSMVFCid48', 'VFCVectorEGSMVFCid49', 'VFCVectorEGSMVFCid5', 'VFCVectorEGSMVFCid50', 'VFCVectorEGSMVFCid51', 'VFCVectorEGSMVFCid52', 'VFCVectorEGSMVFCid53', 'VFCVectorEGSMVFCid54', 'VFCVectorEGSMVFCid55', 'VFCVectorEGSMVFCid56', 'VFCVectorEGSMVFCid57', 'VFCVectorEGSMVFCid58', 'VFCVectorEGSMVFCid59', 'VFCVectorEGSMVFCid6', 'VFCVectorEGSMVFCid60', 'VFCVectorEGSMVFCid61', 'VFCVectorEGSMVFCid7', 'VFCVectorEGSMVFCid8', 'VFCVectorEGSMVFCid9']}
    sig_group_dataid_dict = {}

    class VFCVectorEGSMVFCid11:
        sig_name = "VFCVectorEGSMVFCid11"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid25:
        sig_name = "VFCVectorEGSMVFCid25"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid7:
        sig_name = "VFCVectorEGSMVFCid7"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorEGSMVFCid31:
        sig_name = "VFCVectorEGSMVFCid31"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorEGSMVFCid46:
        sig_name = "VFCVectorEGSMVFCid46"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorEGSMVFCid61:
        sig_name = "VFCVectorEGSMVFCid61"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid40:
        sig_name = "VFCVectorEGSMVFCid40"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorEGSMVFCid0:
        sig_name = "VFCVectorEGSMVFCid0"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorEGSMVFCid36:
        sig_name = "VFCVectorEGSMVFCid36"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid15:
        sig_name = "VFCVectorEGSMVFCid15"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorEGSMVFCid14:
        sig_name = "VFCVectorEGSMVFCid14"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorEGSMVFCid1:
        sig_name = "VFCVectorEGSMVFCid1"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid32:
        sig_name = "VFCVectorEGSMVFCid32"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorEGSMVFCid20:
        sig_name = "VFCVectorEGSMVFCid20"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid37:
        sig_name = "VFCVectorEGSMVFCid37"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid49:
        sig_name = "VFCVectorEGSMVFCid49"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid19:
        sig_name = "VFCVectorEGSMVFCid19"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid17:
        sig_name = "VFCVectorEGSMVFCid17"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid29:
        sig_name = "VFCVectorEGSMVFCid29"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid39:
        sig_name = "VFCVectorEGSMVFCid39"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorEGSMVFCid4:
        sig_name = "VFCVectorEGSMVFCid4"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid26:
        sig_name = "VFCVectorEGSMVFCid26"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorEGSMVFCid10:
        sig_name = "VFCVectorEGSMVFCid10"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorEGSMVFCid5:
        sig_name = "VFCVectorEGSMVFCid5"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid47:
        sig_name = "VFCVectorEGSMVFCid47"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorEGSMVFCid27:
        sig_name = "VFCVectorEGSMVFCid27"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid55:
        sig_name = "VFCVectorEGSMVFCid55"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorEGSMVFCid44:
        sig_name = "VFCVectorEGSMVFCid44"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid9:
        sig_name = "VFCVectorEGSMVFCid9"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid3:
        sig_name = "VFCVectorEGSMVFCid3"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid42:
        sig_name = "VFCVectorEGSMVFCid42"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorEGSMVFCid35:
        sig_name = "VFCVectorEGSMVFCid35"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid23:
        sig_name = "VFCVectorEGSMVFCid23"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorEGSMVFCid52:
        sig_name = "VFCVectorEGSMVFCid52"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid28:
        sig_name = "VFCVectorEGSMVFCid28"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid43:
        sig_name = "VFCVectorEGSMVFCid43"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid58:
        sig_name = "VFCVectorEGSMVFCid58"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorEGSMVFCid59:
        sig_name = "VFCVectorEGSMVFCid59"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid2:
        sig_name = "VFCVectorEGSMVFCid2"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorEGSMVFCid45:
        sig_name = "VFCVectorEGSMVFCid45"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid54:
        sig_name = "VFCVectorEGSMVFCid54"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorEGSMVFCid60:
        sig_name = "VFCVectorEGSMVFCid60"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid30:
        sig_name = "VFCVectorEGSMVFCid30"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorEGSMBlockID:
        sig_name = "VFCVectorEGSMBlockID"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VFCVectorEGSMVFCid18:
        sig_name = "VFCVectorEGSMVFCid18"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorEGSMVFCid8:
        sig_name = "VFCVectorEGSMVFCid8"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorEGSMVFCid13:
        sig_name = "VFCVectorEGSMVFCid13"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid33:
        sig_name = "VFCVectorEGSMVFCid33"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid56:
        sig_name = "VFCVectorEGSMVFCid56"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorEGSMVFCid22:
        sig_name = "VFCVectorEGSMVFCid22"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorEGSMVFCid24:
        sig_name = "VFCVectorEGSMVFCid24"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorEGSMVFCid51:
        sig_name = "VFCVectorEGSMVFCid51"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorEGSMVFCid16:
        sig_name = "VFCVectorEGSMVFCid16"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorEGSMVFCid21:
        sig_name = "VFCVectorEGSMVFCid21"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid34:
        sig_name = "VFCVectorEGSMVFCid34"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorEGSMVFCid48:
        sig_name = "VFCVectorEGSMVFCid48"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorEGSMVFCid38:
        sig_name = "VFCVectorEGSMVFCid38"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorEGSMVFCid53:
        sig_name = "VFCVectorEGSMVFCid53"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorEGSMVFCid12:
        sig_name = "VFCVectorEGSMVFCid12"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorEGSMVFCid6:
        sig_name = "VFCVectorEGSMVFCid6"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorEGSMVFCid57:
        sig_name = "VFCVectorEGSMVFCid57"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid41:
        sig_name = "VFCVectorEGSMVFCid41"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorEGSMVFCid50:
        sig_name = "VFCVectorEGSMVFCid50"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class EcmPropulsionCANNmFr:
    msg_name = "EcmPropulsionCANNmFr"
    msg_id = 1312
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['HVCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MgmPropFr08:
    msg_name = "MgmPropFr08"
    msg_id = 550
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IsgHeatPwrMax:
        sig_name = "IsgHeatPwrMax"
        sig_start_bit = 7
        update_id_bit = 13
        sig_length = 8
        sig_value_factor = 50
        sig_value_offset = 0
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

    class IsgHeatFdBck:
        sig_name = "IsgHeatFdBck"
        sig_start_bit = 15
        update_id_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IsgHeatFdBck_On': 0, 'IsgHeatFdBck_Off': 1, 'IsgHeatFdBck_Inhibt': 2, 'IsgHeatFdBck_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class IemToVddmPropDiagRespFrame:
    msg_name = "IemToVddmPropDiagRespFrame"
    msg_id = 1591
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmPropulsionFr05:
    msg_name = "BgmPropulsionFr05"
    msg_id = 42
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ChrgSoftSwCtrlSt:
        sig_name = "ChrgSoftSwCtrlSt"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BecmPropFr03:
    msg_name = "BecmPropFr03"
    msg_id = 376
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['IEM', 'ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattCoolgReq:
        sig_name = "HvBattCoolgReq"
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
        sig_value_table = {'HvBattCoolgReq_NotReqd': 0, 'HvBattCoolgReq_LoReq': 1, 'HvBattCoolgReq_MedReq': 2, 'HvBattCoolgReq_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvSysLimnIndcn:
        sig_name = "HvSysLimnIndcn"
        sig_start_bit = 23
        update_id_bit = 35
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvBattChrgnCmpl:
        sig_name = "HvBattChrgnCmpl"
        sig_start_bit = 7
        update_id_bit = 6
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvBattSoc:
        sig_name = "HvBattSoc"
        sig_start_bit = 47
        update_id_bit = 52
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class HvBattULim:
        sig_name = "HvBattULim"
        sig_start_bit = 50
        update_id_bit = 51
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class HvBattILim:
        sig_name = "HvBattILim"
        sig_start_bit = 4
        update_id_bit = 5
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class SrsPropulsionCANNmFr:
    msg_name = "SrsPropulsionCANNmFr"
    msg_id = 1306
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['MGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmToHvcmPropDiagReqFrame:
    msg_name = "VddmToHvcmPropDiagReqFrame"
    msg_id = 1872
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['HVCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MgmToVddmPropDiagRespFrame:
    msg_name = "MgmToVddmPropDiagRespFrame"
    msg_id = 1585
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr35:
    msg_name = "VddmPropFr35"
    msg_id = 304
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM']
    sig_group_dict = {'SpdRotlForWhlsAtAxleFrnt': ['SpdRotlForWhlsAtAxleFrntChks', 'SpdRotlForWhlsAtAxleFrntCntr', 'SpdRotlForWhlsAtAxleFrntSpdRotlForWhlsAtAxleFrnt'], 'WhlDirRotlFrnt': ['WhlDirRotlFrntChks', 'WhlDirRotlFrntCntr', 'WhlDirRotlFrntLe', 'WhlDirRotlFrntRi']}
    sig_group_dataid_dict = {'SpdRotlForWhlsAtAxleFrnt': 53, 'WhlDirRotlFrnt': 552}

    class SpdRotlForWhlsAtAxleFrnt_UB:
        sig_name = "SpdRotlForWhlsAtAxleFrnt_UB"
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

    class WhlDirRotlFrnt_UB:
        sig_name = "WhlDirRotlFrnt_UB"
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

    class SpdRotlForWhlsAtAxleFrntSpdRotlForWhlsAtAxleFrnt:
        sig_name = "SpdRotlForWhlsAtAxleFrntSpdRotlForWhlsAtAxleFrnt"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class WhlDirRotlFrntCntr:
        sig_name = "WhlDirRotlFrntCntr"
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

    class SpdRotlForWhlsAtAxleFrntCntr:
        sig_name = "SpdRotlForWhlsAtAxleFrntCntr"
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

    class SpdRotlForWhlsAtAxleFrntChks:
        sig_name = "SpdRotlForWhlsAtAxleFrntChks"
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

    class WhlDirRotlFrntChks:
        sig_name = "WhlDirRotlFrntChks"
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

    class WhlDirRotlFrntLe:
        sig_name = "WhlDirRotlFrntLe"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WhlDirRotlFrntRi:
        sig_name = "WhlDirRotlFrntRi"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlRotlDirStd1_Undefd': 0, 'WhlRotlDirStd1_StandStill': 1, 'WhlRotlDirStd1_Fwd': 2, 'WhlRotlDirStd1_Backw': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class IgmMgmPropFr02:
    msg_name = "IgmMgmPropFr02"
    msg_id = 629
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.16
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IsgCoolgReqInvr:
        sig_name = "IsgCoolgReqInvr"
        sig_start_bit = 52
        update_id_bit = 3
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCoolg1_NoRequestForMoreCoolantPower': 0, 'HvCoolg1_IncreaseLevel1ForMoreCoolantPower': 1, 'HvCoolg1_IncreaseLevel2ForMoreCoolantPower': 2, 'HvCoolg1_MaxCoolingPower': 3, 'HvCoolg1_NotDefined': 4}
        compute_method = None
        length = 3
        startbit = 52
        byte = 6
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class IsgCooltFlowMinReq:
        sig_name = "IsgCooltFlowMinReq"
        sig_start_bit = 25
        update_id_bit = 26
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class IsgInvrT:
        sig_name = "IsgInvrT"
        sig_start_bit = 63
        update_id_bit = 4
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmToVddmPropDiagRespFrame:
    msg_name = "EcmToVddmPropDiagRespFrame"
    msg_id = 1584
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MgmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "MgmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2028
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr22:
    msg_name = "BecmPropFr22"
    msg_id = 83
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM', 'S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ChrgEquipIDc:
        sig_name = "ChrgEquipIDc"
        sig_start_bit = 47
        update_id_bit = 48
        sig_length = 15
        sig_value_factor = 0.1
        sig_value_offset = -1638.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 16380
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class CPSRU:
        sig_name = "CPSRU"
        sig_start_bit = 39
        update_id_bit = 24
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

    class HVBattChrgnCCOrCVMod:
        sig_name = "HVBattChrgnCCOrCVMod"
        sig_start_bit = 18
        update_id_bit = 16
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CCOrCVModSt_Default': 0, 'CCOrCVModSt_CV': 1, 'CCOrCVModSt_CC': 2, 'CCOrCVModSt_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class HvBattSupChrgThermSts:
        sig_name = "HvBattSupChrgThermSts"
        sig_start_bit = 22
        update_id_bit = 23
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ThermSts1_Idle': 0, 'ThermSts1_Prestart': 1, 'ThermSts1_Standby': 2, 'ThermSts1_Active': 3, 'ThermSts1_off': 4}
        compute_method = None
        length = 4
        startbit = 22
        byte = 2
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3


class EcmPropFr09:
    msg_name = "EcmPropFr09"
    msg_id = 406
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ChrgnOrDisChrgnStsFb:
        sig_name = "ChrgnOrDisChrgnStsFb"
        sig_start_bit = 29
        update_id_bit = 24
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 30
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgnSts2_default': 0, 'ChrgnSts2_NoCharging': 1, 'ChrgnSts2_ACCharging': 2, 'ChrgnSts2_ACChargingEnd': 3, 'ChrgnSts2_ChargingCmpl': 4, 'ChrgnSts2_Heating': 5, 'ChrgnSts2_Booking': 6, 'ChrgnSts2_NoDischaring': 7, 'ChrgnSts2_Discharging': 8, 'ChrgnSts2_DischargingEnd': 9, 'ChrgnSts2_DischargingCmpl': 10, 'ChrgnSts2_Chargingfalut': 11, 'ChrgnSts2_DischargingFalut': 12, 'ChrgnSts2_ACChrgnFltChrgrSide': 14, 'ChrgnSts2_DCCharging': 15, 'ChrgnSts2_DCChrgnFltVehSide': 18, 'ChrgnSts2_DCChrgnFltChrgrSideTempFlt': 19, 'ChrgnSts2_DCChrgnFltChrgrSideConFlt': 20, 'ChrgnSts2_DCChrgnFltChrgrSideHwFlt': 21, 'ChrgnSts2_DCChrgnFltChrgrSideEmgyFlt': 22, 'ChrgnSts2_DCChrgnFltChrgrSideComFlt': 23, 'ChrgnSts2_SuperCharging': 24, 'ChrgnSts2_ACChargingSuspend': 25, 'ChrgnSts2_DCChargingEnd': 26, 'ChrgnSts2_ACChrgnFltVehSide': 27, 'ChrgnSts2_Boostcharging': 28, 'ChrgnSts2_BoostchargingFlt': 29, 'ChrgnSts2_WirelessCharging': 30}
        compute_method = None
        length = 5
        startbit = 29
        byte = 3
        mask = 0b00111110
        unmask = 0b11000001
        shift = 1

    class HvBattChrgnCmd:
        sig_name = "HvBattChrgnCmd"
        sig_start_bit = 52
        update_id_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVBattChargnCmd_OK': 0, 'HVBattChargnCmd_NOK': 1, 'HVBattChargnCmd_INIT': 2, 'HVBattChargnCmd_HOLD': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class ObdAccrPedRat:
        sig_name = "ObdAccrPedRat"
        sig_start_bit = 63
        update_id_bit = 54
        sig_length = 8
        sig_value_factor = 0.3921568628
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


class VgmToBecmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToBecmJ1979OBDPropCanReqFrame11"
    msg_id = 2018
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class CddObcPropFr01:
    msg_name = "CddObcPropFr01"
    msg_id = 536
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver', 'BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class OnBdChrgrT:
        sig_name = "OnBdChrgrT"
        sig_start_bit = 31
        update_id_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OnBdChrgrHndlSts1:
        sig_name = "OnBdChrgrHndlSts1"
        sig_start_bit = 19
        update_id_bit = 20
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 8
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnBdChrgrHndlSts1_Disconnected': 0, 'OnBdChrgrHndlSts1_ConnectedWithoutPower': 1, 'OnBdChrgrHndlSts1_PowerAvailableButNotActivated': 2, 'OnBdChrgrHndlSts1_ConnectedWithPower': 3, 'OnBdChrgrHndlSts1_DischargeConnectwithoutpowerincar': 4, 'OnBdChrgrHndlSts1_DischargeConnectwithoutpoweroutcar': 5, 'OnBdChrgrHndlSts1_DischargeConnectwithpowerincar': 6, 'OnBdChrgrHndlSts1_DischargeConnectwithpoweroutcar': 7, 'OnBdChrgrHndlSts1_Init': 8, 'OnBdChrgrHndlSts1_Fault': 9, 'OnBdChrgrHndlSts1_NotCompleteConnnected': 10, 'OnBdChrgrHndlSts1_Reserved0': 11, 'OnBdChrgrHndlSts1_Reserved1': 12, 'OnBdChrgrHndlSts1_Reserved2': 13}
        compute_method = None
        length = 4
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PwrEgyMgrAvl:
        sig_name = "PwrEgyMgrAvl"
        sig_start_bit = 39
        update_id_bit = 44
        sig_length = 11
        sig_value_factor = 20
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11100000, 0b00011111, 3, 5)]


class IemPropFr09:
    msg_name = "IemPropFr09"
    msg_id = 1126
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['CCM']
    sig_group_dict = {'IEMTestFr3': ['IEMTestFr3Byte0', 'IEMTestFr3Byte1', 'IEMTestFr3Byte2', 'IEMTestFr3Byte3', 'IEMTestFr3Byte4', 'IEMTestFr3Byte5', 'IEMTestFr3Byte6', 'IEMTestFr3Byte7']}
    sig_group_dataid_dict = {}

    class IEMTestFr3Byte1:
        sig_name = "IEMTestFr3Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IEMTestFr3Byte3:
        sig_name = "IEMTestFr3Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IEMTestFr3Byte4:
        sig_name = "IEMTestFr3Byte4"
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

    class IEMTestFr3Byte0:
        sig_name = "IEMTestFr3Byte0"
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

    class IEMTestFr3Byte6:
        sig_name = "IEMTestFr3Byte6"
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

    class IEMTestFr3Byte7:
        sig_name = "IEMTestFr3Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IEMTestFr3Byte2:
        sig_name = "IEMTestFr3Byte2"
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

    class IEMTestFr3Byte5:
        sig_name = "IEMTestFr3Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class IemPropFr06:
    msg_name = "IemPropFr06"
    msg_id = 626
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'IemGeneric': ['IemGenericADAlrmSt', 'IemGenericDTCHig', 'IemGenericDTCLow', 'IemGenericDTCMid', 'IemGenericDTCSts', 'IemGenericEMQnty', 'IemGenericEMSeqNr', 'IemGenericFltAlrmSt', 'IemGenericIacAlrmSt', 'IemGenericInvrtTAlrmSt', 'IemGenericModStatusRms', 'IemGenericMotTAlrmSt', 'IemGenericRslAlrmSt', 'IemGenericSpdAlrmSt', 'IemGenericTypeInfo', 'IemGenericUDcAlrmSt']}
    sig_group_dataid_dict = {}

    class IemGenericDTCHig:
        sig_name = "IemGenericDTCHig"
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

    class IemGenericMotTAlrmSt:
        sig_name = "IemGenericMotTAlrmSt"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IemGenericADAlrmSt:
        sig_name = "IemGenericADAlrmSt"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IemGenericModStatusRms:
        sig_name = "IemGenericModStatusRms"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModStatusRms_Invalid': 0, 'ModStatusRms_PwrCns': 1, 'ModStatusRms_PwrGen': 2, 'ModStatusRms_OffSts': 3, 'ModStatusRms_RdySts': 4, 'ModStatusRms_Abnormal': 5, 'ModStatusRms_Invalid1': 6, 'ModStatusRms_Invalid2': 7, 'ModStatusRms_Invalid3': 8, 'ModStatusRms_Invalid4': 9, 'ModStatusRms_Invalid5': 10, 'ModStatusRms_Invalid6': 11, 'ModStatusRms_Invalid7': 12, 'ModStatusRms_Invalid8': 13, 'ModStatusRms_Invalid9': 14, 'ModStatusRms_Invalid10': 15}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class IemGenericRslAlrmSt:
        sig_name = "IemGenericRslAlrmSt"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IemGenericEMSeqNr:
        sig_name = "IemGenericEMSeqNr"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IemGenericDTCSts:
        sig_name = "IemGenericDTCSts"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IemGenericDTCMid:
        sig_name = "IemGenericDTCMid"
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

    class IemGenericSpdAlrmSt:
        sig_name = "IemGenericSpdAlrmSt"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class IemGenericFltAlrmSt:
        sig_name = "IemGenericFltAlrmSt"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IemGenericTypeInfo:
        sig_name = "IemGenericTypeInfo"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IemGenericEMQnty:
        sig_name = "IemGenericEMQnty"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class IemGenericDTCLow:
        sig_name = "IemGenericDTCLow"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IemGenericInvrtTAlrmSt:
        sig_name = "IemGenericInvrtTAlrmSt"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IemGenericUDcAlrmSt:
        sig_name = "IemGenericUDcAlrmSt"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IemGenericIacAlrmSt:
        sig_name = "IemGenericIacAlrmSt"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class EgsmPropFr01:
    msg_name = "EgsmPropFr01"
    msg_id = 309
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['BGM', 'VDDM', 'S2SReceiver', 'ECM']
    sig_group_dict = {'DrvrGearShiftParkReq': ['DrvrGearShiftParkReq1', 'DrvrGearShiftParkReqChks', 'DrvrGearShiftParkReqCntr', 'DrvrGearShiftParkReqSts']}
    sig_group_dataid_dict = {'DrvrGearShiftParkReq': 527}

    class DrvrGearShiftParkReqCntr:
        sig_name = "DrvrGearShiftParkReqCntr"
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

    class GearLvrIllmnSts:
        sig_name = "GearLvrIllmnSts"
        sig_start_bit = 35
        update_id_bit = 34
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DrvrGearShiftReqInv:
        sig_name = "DrvrGearShiftReqInv"
        sig_start_bit = 47
        update_id_bit = 40
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvrGearShiftReqInv_NoPress': 0, 'DrvrGearShiftReqInv_PressP': 1, 'DrvrGearShiftReqInv_PressR': 2, 'DrvrGearShiftReqInv_PressD': 3, 'DrvrGearShiftReqInv_Reserved1': 4, 'DrvrGearShiftReqInv_Reserved2': 5, 'DrvrGearShiftReqInv_Reserved3': 6, 'DrvrGearShiftReqInv_Reserved4': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DrvrGearShiftParkReq_UB:
        sig_name = "DrvrGearShiftParkReq_UB"
        sig_start_bit = 15
        update_id_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class GearLock:
        sig_name = "GearLock"
        sig_start_bit = 28
        update_id_bit = 29
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActvInActv_Active': 0, 'ActvInActv_Inactive': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DrvrGearShiftParkReq1:
        sig_name = "DrvrGearShiftParkReq1"
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
        sig_value_table = {'SwtPark1_SwtParkNotActv': 0, 'SwtPark1_SwtParkActv': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DrvrGearShiftParkReqSts:
        sig_name = "DrvrGearShiftParkReqSts"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClutchPedlPsd_No': 0, 'ClutchPedlPsd_Yes': 1, 'ClutchPedlPsd_Reserved1': 2, 'ClutchPedlPsd_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DrvrGearShiftParkReqChks:
        sig_name = "DrvrGearShiftParkReqChks"
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

    class GearShiftUnitSts:
        sig_name = "GearShiftUnitSts"
        sig_start_bit = 26
        update_id_bit = 27
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoFlt': 0, 'NoUpTipAut': 1, 'NoDwnTipAut': 2, 'NoPark': 3, 'SrvRqrd': 4, 'NoUpUpTipAut': 5, 'NoDownDownTipAut': 6, 'Nounlock': 7}
        compute_method = None
        length = 3
        startbit = 26
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class EcmPropFr11:
    msg_name = "EcmPropFr11"
    msg_id = 647
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'VDDM', 'HVCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class CooltTSigForDtElec:
        sig_name = "CooltTSigForDtElec"
        sig_start_bit = 39
        update_id_bit = 5
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 1800
        sig_byteorder = "Motorola"
        sig_value_init = 400
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11100000, 0b00011111, 3, 5)]

    class ChrgnSts:
        sig_name = "ChrgnSts"
        sig_start_bit = 44
        update_id_bit = 63
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgnSts_Fault': 0, 'ChrgnSts_ChargingInParkingState': 1, 'ChrgnSts_ChargingInDrivingState': 2, 'ChrgnSts_NotCharging': 3, 'ChrgnSts_ChargingCompleted': 4, 'ChrgnSts_Invalid': 5}
        compute_method = None
        length = 3
        startbit = 44
        byte = 5
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class CmptmtCoolgSts:
        sig_name = "CmptmtCoolgSts"
        sig_start_bit = 3
        update_id_bit = 4
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptmtCoolgSts_OffNoReq': 0, 'CmptmtCoolgSts_OffByEvaprTLo': 1, 'CmptmtCoolgSts_OffByPLo': 2, 'CmptmtCoolgSts_OffByAmbTOutOfRng': 3, 'CmptmtCoolgSts_OffBySysFailr': 4, 'CmptmtCoolgSts_OffByLoadCut': 5, 'CmptmtCoolgSts_OnWithBattCoolg': 6, 'CmptmtCoolgSts_On': 7}
        compute_method = None
        length = 4
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class BookChargeSetResponse:
        sig_name = "BookChargeSetResponse"
        sig_start_bit = 62
        update_id_bit = 56
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BookChargeSetResponse_Default': 0, 'BookChargeSetResponse_Success': 1, 'BookChargeSetResponse_Cancelled': 2, 'BookChargeSetResponse_Fail': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class PrpsnSysActv:
        sig_name = "PrpsnSysActv"
        sig_start_bit = 20
        update_id_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotCmpl1_NotCmpl': 0, 'NotCmpl1_Cmpl': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvConvPwrAllwd:
        sig_name = "HvConvPwrAllwd"
        sig_start_bit = 15
        update_id_bit = 7
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 1023
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11000000, 0b00111111, 2, 6)]

    class DeactvtTestCom:
        sig_name = "DeactvtTestCom"
        sig_start_bit = 60
        update_id_bit = 57
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CooltFlowForDtElec:
        sig_name = "CooltFlowForDtElec"
        sig_start_bit = 41
        update_id_bit = 6
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11111110, 0b00000001, 7, 1)]


class CddObcPropFr02:
    msg_name = "CddObcPropFr02"
    msg_id = 534
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class OnBdChrgrIAct:
        sig_name = "OnBdChrgrIAct"
        sig_start_bit = 2
        update_id_bit = 3
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = -200.0
        sig_value_min = 0
        sig_value_max = 4000
        sig_byteorder = "Motorola"
        sig_value_init = 2000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b10000000, 0b01111111, 1, 7)]

    class OnBdChrgrSt:
        sig_name = "OnBdChrgrSt"
        sig_start_bit = 22
        update_id_bit = 6
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 12
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgrSts1_Idle': 0, 'ChrgrSts1_PreStrt': 1, 'ChrgrSts1_Chrgn': 2, 'ChrgrSts1_Alrm': 3, 'ChrgrSts1_Srv': 4, 'ChrgrSts1_Diagc': 5, 'ChrgrSts1_Boot': 6, 'ChrgrSts1_Rstrt': 7, 'ChrgrSts1_DisChrgn': 8, 'ChrgrSts1_BookChrgn': 9, 'ChrgrSts1_Shutdown': 10, 'ChrgrSts1_Heating': 11, 'ChrgrSts1_Cooling': 12}
        compute_method = None
        length = 4
        startbit = 22
        byte = 2
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class DchaUAct:
        sig_name = "DchaUAct"
        sig_start_bit = 52
        update_id_bit = 57
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111100, 0b00000011, 6, 2)]

    class DchaPwrAct:
        sig_name = "DchaPwrAct"
        sig_start_bit = 18
        update_id_bit = 25
        sig_length = 9
        sig_value_factor = 100
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class DchaIAct:
        sig_name = "DchaIAct"
        sig_start_bit = 47
        update_id_bit = 7
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]


class EcmPropComFr10:
    msg_name = "EcmPropComFr10"
    msg_id = 341
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['CCM', 'EGSM', 'VDDM']
    sig_group_dict = {'TrsmParkLockd': ['TrsmParkLockdChks', 'TrsmParkLockdCntr', 'TrsmParkLockdTrsmParkLockd']}
    sig_group_dataid_dict = {'TrsmParkLockd': 50}

    class VehRefSpd:
        sig_name = "VehRefSpd"
        sig_start_bit = 47
        update_id_bit = 48
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
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class EGSMLightOn:
        sig_name = "EGSMLightOn"
        sig_start_bit = 7
        update_id_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EGSMLightOn_Default': 0, 'EGSMLightOn_LightOn': 1, 'EGSMLightOn_LightOff': 2}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class TrsmParkLockdChks:
        sig_name = "TrsmParkLockdChks"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VehDrvSt:
        sig_name = "VehDrvSt"
        sig_start_bit = 39
        update_id_bit = 35
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehDrvSts_NoTq': 0, 'VehDrvSts_BrkTq': 1, 'VehDrvSts_Launch': 2, 'VehDrvSts_Crp': 3, 'VehDrvSts_Reserved1': 4, 'VehDrvSts_PedalMap': 5, 'VehDrvSts_Reserved2': 6, 'VehDrvSts_BrkSTop': 7, 'VehDrvSts_Reserved3': 8, 'VehDrvSts_AVP': 9, 'VehDrvSts_ANP': 10}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class LgtCtrlModActvSts:
        sig_name = "LgtCtrlModActvSts"
        sig_start_bit = 3
        update_id_bit = 2
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

    class TrsmParkLockdCntr:
        sig_name = "TrsmParkLockdCntr"
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

    class TrsmParkLockdTrsmParkLockd:
        sig_name = "TrsmParkLockdTrsmParkLockd"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrsmParkLock1_ParkNotEngd': 0, 'TrsmParkLock1_ParkEngd': 1, 'TrsmParkLock1_NotInUse': 2, 'TrsmParkLock1_Undefd': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TrsmParkLockd_UB:
        sig_name = "TrsmParkLockd_UB"
        sig_start_bit = 22
        update_id_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class VddmPropFr31:
    msg_name = "VddmPropFr31"
    msg_id = 1051
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.5
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'ECM']
    sig_group_dict = {'BattThermMngtInFuture': ['BattThermMngtInFuturePwrAtTime', 'BattThermMngtInFutureSequenceNo', 'BattThermMngtInFutureTempAtTime', 'BattThermMngtInFutureThermModAtTime', 'BattThermMngtInFutureTime', 'BattThermMngtInFutureVersionNo'], 'AmbTEstimd': ['AmbTEstimdAmbTEstimd', 'AmbTEstimdQf']}
    sig_group_dataid_dict = {}

    class BattThermMngtInFutureTime:
        sig_name = "BattThermMngtInFutureTime"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BattThermMngtInFuture_UB:
        sig_name = "BattThermMngtInFuture_UB"
        sig_start_bit = 3
        update_id_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BattThermMngtInFutureSequenceNo:
        sig_name = "BattThermMngtInFutureSequenceNo"
        sig_start_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class BattThermMngtInFuturePwrAtTime:
        sig_name = "BattThermMngtInFuturePwrAtTime"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 50
        sig_value_offset = -25000.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class AmbTEstimd_UB:
        sig_name = "AmbTEstimd_UB"
        sig_start_bit = 52
        update_id_bit = 52
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
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AmbTEstimdQf:
        sig_name = "AmbTEstimdQf"
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
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BattThermMngtInFutureThermModAtTime:
        sig_name = "BattThermMngtInFutureThermModAtTime"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Idle': 0, 'ThermalBalancing': 1, 'PassiveHeating': 2, 'ActiveHeating': 3, 'PassiveCooling': 4, 'ActiveCooling': 5, 'CombinedCooling': 6, 'Reserved': 7}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class AmbTEstimdAmbTEstimd:
        sig_name = "AmbTEstimdAmbTEstimd"
        sig_start_bit = 50
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -70.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class BattThermMngtInFutureTempAtTime:
        sig_name = "BattThermMngtInFutureTempAtTime"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BattThermMngtInFutureVersionNo:
        sig_name = "BattThermMngtInFutureVersionNo"
        sig_start_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class EcmToVgmJ1979OBDPropCanResFrame11:
    msg_name = "EcmToVgmJ1979OBDPropCanResFrame11"
    msg_id = 2024
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr19:
    msg_name = "VddmPropFr19"
    msg_id = 645
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'HVCM', 'EGSM', 'ECM']
    sig_group_dict = {'AmbTRaw': ['AmbTRawAmbTVal', 'AmbTRawQly'], 'VehBattU': ['VehBattUSysU', 'VehBattUSysUQf']}
    sig_group_dataid_dict = {}

    class AmbTRaw_UB:
        sig_name = "AmbTRaw_UB"
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

    class VehBattU_UB:
        sig_name = "VehBattU_UB"
        sig_start_bit = 2
        update_id_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BkpOfDstTrvld:
        sig_name = "BkpOfDstTrvld"
        sig_start_bit = 20
        update_id_bit = 21
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
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class VehBattUSysUQf:
        sig_name = "VehBattUSysUQf"
        sig_start_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AbsClrRdyReq:
        sig_name = "AbsClrRdyReq"
        sig_start_bit = 3
        update_id_bit = 4
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VehBattUSysU:
        sig_name = "VehBattUSysU"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AmbTRawQly:
        sig_name = "AmbTRawQly"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class AmbTRawAmbTVal:
        sig_name = "AmbTRawAmbTVal"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -70.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 42
        bmuws_info = [(5, 0b00000111, 0b11111000, 3, 0), (6, 0b11111111, 0b00000000, 8, 0)]


class IemEduPropFr02:
    msg_name = "IemEduPropFr02"
    msg_id = 96
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['BECM1', 'BGM', 'VDDM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlMotSysSpdAct:
        sig_name = "WhlMotSysSpdAct"
        sig_start_bit = 6
        update_id_bit = 7
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
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotSysLimnIndcn:
        sig_name = "WhlMotSysLimnIndcn"
        sig_start_bit = 55
        update_id_bit = 39
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class ImobEngSts2:
        sig_name = "ImobEngSts2"
        sig_start_bit = 36
        update_id_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobSts_ImobUndefd': 0, 'ImobSts_ImobImobn': 1, 'ImobSts_ImobMtn': 2, 'ImobSts_ImobNoMtn': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class WhlMotSysUdc:
        sig_name = "WhlMotSysUdc"
        sig_start_bit = 34
        update_id_bit = 38
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotSysCooltT:
        sig_name = "WhlMotSysCooltT"
        sig_start_bit = 31
        update_id_bit = 16
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmToMgmPropDiagReqFrame:
    msg_name = "VddmToMgmPropDiagReqFrame"
    msg_id = 1841
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MgmPropFr09:
    msg_name = "MgmPropFr09"
    msg_id = 594
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']
    sig_group_dict = {'ImobEngChk13': ['ImobEngChk13Chks', 'ImobEngChk13Cntr', 'ImobEngChk13ImobEngChkSts', 'ImobEngChk13ImobEngDataChk0', 'ImobEngChk13ImobEngDataChk1', 'ImobEngChk13ImobEngDataChk2', 'ImobEngChk13ImobEngDataChk3', 'ImobEngChk13ImobEngDataChk4', 'ImobEngChk13ImobEngDataChk5']}
    sig_group_dataid_dict = {'ImobEngChk13': 9475}

    class ImobEngChk13ImobEngChkSts:
        sig_name = "ImobEngChk13ImobEngChkSts"
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
        sig_value_table = {'AvlSts2_NotAvl': 0, 'AvlSts2_Avl': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ImobEngChk13ImobEngDataChk3:
        sig_name = "ImobEngChk13ImobEngDataChk3"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk13ImobEngDataChk0:
        sig_name = "ImobEngChk13ImobEngDataChk0"
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

    class ImobEngChk13Chks:
        sig_name = "ImobEngChk13Chks"
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

    class ImobEngChk13ImobEngDataChk5:
        sig_name = "ImobEngChk13ImobEngDataChk5"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk13ImobEngDataChk1:
        sig_name = "ImobEngChk13ImobEngDataChk1"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk13_UB:
        sig_name = "ImobEngChk13_UB"
        sig_start_bit = 12
        update_id_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ImobEngChk13Cntr:
        sig_name = "ImobEngChk13Cntr"
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

    class ImobEngChk13ImobEngDataChk4:
        sig_name = "ImobEngChk13ImobEngDataChk4"
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

    class ImobEngChk13ImobEngDataChk2:
        sig_name = "ImobEngChk13ImobEngDataChk2"
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


class BecmPropFr36:
    msg_name = "BecmPropFr36"
    msg_id = 672
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FastBoostRlySt:
        sig_name = "FastBoostRlySt"
        sig_start_bit = 9
        update_id_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgRlySt_Open': 0, 'ChrgRlySt_Close': 1, 'ChrgRlySt_Reserved1': 2, 'ChrgRlySt_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DCChrgrUMax:
        sig_name = "DCChrgrUMax"
        sig_start_bit = 39
        update_id_bit = 42
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11110000, 0b00001111, 4, 4)]

    class ChrgEquipUDc:
        sig_name = "ChrgEquipUDc"
        sig_start_bit = 23
        update_id_bit = 26
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class C1TargetChrgU:
        sig_name = "C1TargetChrgU"
        sig_start_bit = 7
        update_id_bit = 10
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]


class IemToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "IemToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2027
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EgsmPropFr02:
    msg_name = "EgsmPropFr02"
    msg_id = 310
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'DrvrGearShiftDirReq1': ['DrvrGearShiftDirReq1Chks', 'DrvrGearShiftDirReq1Cntr', 'DrvrGearShiftDirReq1DwnDwnTipAut', 'DrvrGearShiftDirReq1DwnTipAut', 'DrvrGearShiftDirReq1PosnAut', 'DrvrGearShiftDirReq1UpTipAut', 'DrvrGearShiftDirReq1UpUpTipAut'], 'DrvrGearShiftDirReq2': ['DrvrGearShiftDirReq2Chks', 'DrvrGearShiftDirReq2Cntr', 'DrvrGearShiftDirReq2DwnDwnTipAut', 'DrvrGearShiftDirReq2DwnTipAut', 'DrvrGearShiftDirReq2PosnAut', 'DrvrGearShiftDirReq2UpTipAut', 'DrvrGearShiftDirReq2UpUpTipAut']}
    sig_group_dataid_dict = {'DrvrGearShiftDirReq1': 57, 'DrvrGearShiftDirReq2': 98}

    class DrvrGearShiftDirReq2UpTipAut:
        sig_name = "DrvrGearShiftDirReq2UpTipAut"
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
        sig_value_table = {'UpTipAut1_UpTipAutNotActv': 0, 'UpTipAut1_UpTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DrvrGearShiftDirReq2Cntr:
        sig_name = "DrvrGearShiftDirReq2Cntr"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DrvrGearShiftDirReq1_UB:
        sig_name = "DrvrGearShiftDirReq1_UB"
        sig_start_bit = 1
        update_id_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DrvrGearShiftDirReq2DwnDwnTipAut:
        sig_name = "DrvrGearShiftDirReq2DwnDwnTipAut"
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
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DrvrGearShiftDirReq2_UB:
        sig_name = "DrvrGearShiftDirReq2_UB"
        sig_start_bit = 25
        update_id_bit = 25
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
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DrvrGearShiftDirReq2DwnTipAut:
        sig_name = "DrvrGearShiftDirReq2DwnTipAut"
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
        sig_value_table = {'DwnTipAut1_DwnTipAutNotActv': 0, 'DwnTipAut1_DwnTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DrvrGearShiftDirReq1Cntr:
        sig_name = "DrvrGearShiftDirReq1Cntr"
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

    class DrvrGearShiftDirReq1DwnDwnTipAut:
        sig_name = "DrvrGearShiftDirReq1DwnDwnTipAut"
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
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DrvrGearShiftDirReq1PosnAut:
        sig_name = "DrvrGearShiftDirReq1PosnAut"
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
        sig_value_table = {'PosnAut_PosnAutNotActv': 0, 'PosnAut_PosnAutActv': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DrvrGearShiftDirReq2UpUpTipAut:
        sig_name = "DrvrGearShiftDirReq2UpUpTipAut"
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
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DrvrGearShiftDirReq2Chks:
        sig_name = "DrvrGearShiftDirReq2Chks"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DrvrGearShiftDirReq1Chks:
        sig_name = "DrvrGearShiftDirReq1Chks"
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

    class DrvrGearShiftDirReq1DwnTipAut:
        sig_name = "DrvrGearShiftDirReq1DwnTipAut"
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
        sig_value_table = {'DwnTipAut1_DwnTipAutNotActv': 0, 'DwnTipAut1_DwnTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DrvrGearShiftDirReq1UpUpTipAut:
        sig_name = "DrvrGearShiftDirReq1UpUpTipAut"
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
        sig_value_table = {'NotActvActv1_NotActv': 0, 'NotActvActv1_Actv': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DrvrGearShiftDirReq1UpTipAut:
        sig_name = "DrvrGearShiftDirReq1UpTipAut"
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
        sig_value_table = {'UpTipAut1_UpTipAutNotActv': 0, 'UpTipAut1_UpTipAutActv': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DrvrGearShiftDirReq2PosnAut:
        sig_name = "DrvrGearShiftDirReq2PosnAut"
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
        sig_value_table = {'PosnAut_PosnAutNotActv': 0, 'PosnAut_PosnAutActv': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class MgmPropdTCFr09:
    msg_name = "MgmPropdTCFr09"
    msg_id = 299
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'DmcStsFrntToEsc': ['DmcStsFrntToEscChks', 'DmcStsFrntToEscCntr', 'DmcStsFrntToEscDmcActAppTarTq', 'DmcStsFrntToEscDmcSts', 'DmcStsFrntToEscDmcSWInfo']}
    sig_group_dataid_dict = {'DmcStsFrntToEsc': 6014}

    class DmcStsFrntToEscDmcSts:
        sig_name = "DmcStsFrntToEscDmcSts"
        sig_start_bit = 11
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DMC_Init': 0, 'DMC_On': 1, 'DMC_Off': 2, 'DMC_Fault': 3}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DmcStsFrntToEscDmcSWInfo:
        sig_name = "DmcStsFrntToEscDmcSWInfo"
        sig_start_bit = 39
        update_id_bit = None
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsFrntToEscChks:
        sig_name = "DmcStsFrntToEscChks"
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

    class DmcStsFrntToEscCntr:
        sig_name = "DmcStsFrntToEscCntr"
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

    class DmcStsFrntToEscDmcActAppTarTq:
        sig_name = "DmcStsFrntToEscDmcActAppTarTq"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -30000
        sig_value_max = 30000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class DmcStsFrntToEsc_UB:
        sig_name = "DmcStsFrntToEsc_UB"
        sig_start_bit = 56
        update_id_bit = 56
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
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class VddmToEvccPropDiagReqFrame:
    msg_name = "VddmToEvccPropDiagReqFrame"
    msg_id = 1844
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EvccPropFr02:
    msg_name = "EvccPropFr02"
    msg_id = 1072
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {'EVCCLimnIndcn': ['EVCCLimnIndcnByte0', 'EVCCLimnIndcnByte1', 'EVCCLimnIndcnByte2', 'EVCCLimnIndcnByte3', 'EVCCLimnIndcnByte4', 'EVCCLimnIndcnByte5', 'EVCCLimnIndcnByte6', 'EVCCLimnIndcnByte7']}
    sig_group_dataid_dict = {}

    class EVCCLimnIndcnByte2:
        sig_name = "EVCCLimnIndcnByte2"
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

    class EVCCLimnIndcnByte0:
        sig_name = "EVCCLimnIndcnByte0"
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

    class EVCCLimnIndcnByte7:
        sig_name = "EVCCLimnIndcnByte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EVCCLimnIndcnByte3:
        sig_name = "EVCCLimnIndcnByte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EVCCLimnIndcnByte5:
        sig_name = "EVCCLimnIndcnByte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EVCCLimnIndcnByte4:
        sig_name = "EVCCLimnIndcnByte4"
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

    class EVCCLimnIndcnByte6:
        sig_name = "EVCCLimnIndcnByte6"
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

    class EVCCLimnIndcnByte1:
        sig_name = "EVCCLimnIndcnByte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmPropFr06:
    msg_name = "VddmPropFr06"
    msg_id = 565
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'HVCM', 'EGSM']
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


class EcmPropVFCVectorFr:
    msg_name = "EcmPropVFCVectorFr"
    msg_id = 1347
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['CCM']
    sig_group_dict = {'VFCVectorECM': ['VFCVectorECMBlockID', 'VFCVectorECMVFCid0', 'VFCVectorECMVFCid1', 'VFCVectorECMVFCid10', 'VFCVectorECMVFCid11', 'VFCVectorECMVFCid12', 'VFCVectorECMVFCid13', 'VFCVectorECMVFCid14', 'VFCVectorECMVFCid15', 'VFCVectorECMVFCid16', 'VFCVectorECMVFCid17', 'VFCVectorECMVFCid18', 'VFCVectorECMVFCid19', 'VFCVectorECMVFCid2', 'VFCVectorECMVFCid20', 'VFCVectorECMVFCid21', 'VFCVectorECMVFCid22', 'VFCVectorECMVFCid23', 'VFCVectorECMVFCid24', 'VFCVectorECMVFCid25', 'VFCVectorECMVFCid26', 'VFCVectorECMVFCid27', 'VFCVectorECMVFCid28', 'VFCVectorECMVFCid29', 'VFCVectorECMVFCid3', 'VFCVectorECMVFCid30', 'VFCVectorECMVFCid31', 'VFCVectorECMVFCid32', 'VFCVectorECMVFCid33', 'VFCVectorECMVFCid34', 'VFCVectorECMVFCid35', 'VFCVectorECMVFCid36', 'VFCVectorECMVFCid37', 'VFCVectorECMVFCid38', 'VFCVectorECMVFCid39', 'VFCVectorECMVFCid4', 'VFCVectorECMVFCid40', 'VFCVectorECMVFCid41', 'VFCVectorECMVFCid42', 'VFCVectorECMVFCid43', 'VFCVectorECMVFCid44', 'VFCVectorECMVFCid45', 'VFCVectorECMVFCid46', 'VFCVectorECMVFCid47', 'VFCVectorECMVFCid48', 'VFCVectorECMVFCid49', 'VFCVectorECMVFCid5', 'VFCVectorECMVFCid50', 'VFCVectorECMVFCid51', 'VFCVectorECMVFCid52', 'VFCVectorECMVFCid53', 'VFCVectorECMVFCid54', 'VFCVectorECMVFCid55', 'VFCVectorECMVFCid56', 'VFCVectorECMVFCid57', 'VFCVectorECMVFCid58', 'VFCVectorECMVFCid59', 'VFCVectorECMVFCid6', 'VFCVectorECMVFCid60', 'VFCVectorECMVFCid61', 'VFCVectorECMVFCid7', 'VFCVectorECMVFCid8', 'VFCVectorECMVFCid9']}
    sig_group_dataid_dict = {}

    class VFCVectorECMVFCid22:
        sig_name = "VFCVectorECMVFCid22"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorECMVFCid57:
        sig_name = "VFCVectorECMVFCid57"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid46:
        sig_name = "VFCVectorECMVFCid46"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorECMVFCid23:
        sig_name = "VFCVectorECMVFCid23"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorECMVFCid34:
        sig_name = "VFCVectorECMVFCid34"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorECMVFCid10:
        sig_name = "VFCVectorECMVFCid10"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorECMVFCid38:
        sig_name = "VFCVectorECMVFCid38"
        sig_start_bit = 40
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorECMVFCid7:
        sig_name = "VFCVectorECMVFCid7"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorECMVFCid18:
        sig_name = "VFCVectorECMVFCid18"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorECMVFCid26:
        sig_name = "VFCVectorECMVFCid26"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorECMVFCid16:
        sig_name = "VFCVectorECMVFCid16"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorECMVFCid51:
        sig_name = "VFCVectorECMVFCid51"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMVFCid1:
        sig_name = "VFCVectorECMVFCid1"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid25:
        sig_name = "VFCVectorECMVFCid25"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid27:
        sig_name = "VFCVectorECMVFCid27"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMVFCid45:
        sig_name = "VFCVectorECMVFCid45"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid21:
        sig_name = "VFCVectorECMVFCid21"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid41:
        sig_name = "VFCVectorECMVFCid41"
        sig_start_bit = 43
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid15:
        sig_name = "VFCVectorECMVFCid15"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorECMVFCid32:
        sig_name = "VFCVectorECMVFCid32"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorECMVFCid11:
        sig_name = "VFCVectorECMVFCid11"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMVFCid13:
        sig_name = "VFCVectorECMVFCid13"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid49:
        sig_name = "VFCVectorECMVFCid49"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid5:
        sig_name = "VFCVectorECMVFCid5"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid47:
        sig_name = "VFCVectorECMVFCid47"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorECMVFCid42:
        sig_name = "VFCVectorECMVFCid42"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorECMVFCid33:
        sig_name = "VFCVectorECMVFCid33"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid6:
        sig_name = "VFCVectorECMVFCid6"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorECMVFCid2:
        sig_name = "VFCVectorECMVFCid2"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorECMVFCid43:
        sig_name = "VFCVectorECMVFCid43"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMVFCid56:
        sig_name = "VFCVectorECMVFCid56"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorECMVFCid53:
        sig_name = "VFCVectorECMVFCid53"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid39:
        sig_name = "VFCVectorECMVFCid39"
        sig_start_bit = 41
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorECMVFCid24:
        sig_name = "VFCVectorECMVFCid24"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorECMVFCid31:
        sig_name = "VFCVectorECMVFCid31"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class VFCVectorECMVFCid35:
        sig_name = "VFCVectorECMVFCid35"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMVFCid59:
        sig_name = "VFCVectorECMVFCid59"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMVFCid61:
        sig_name = "VFCVectorECMVFCid61"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid30:
        sig_name = "VFCVectorECMVFCid30"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorECMBlockID:
        sig_name = "VFCVectorECMBlockID"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VFCVectorECMVFCid28:
        sig_name = "VFCVectorECMVFCid28"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid44:
        sig_name = "VFCVectorECMVFCid44"
        sig_start_bit = 46
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid20:
        sig_name = "VFCVectorECMVFCid20"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid58:
        sig_name = "VFCVectorECMVFCid58"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorECMVFCid48:
        sig_name = "VFCVectorECMVFCid48"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorECMVFCid12:
        sig_name = "VFCVectorECMVFCid12"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid3:
        sig_name = "VFCVectorECMVFCid3"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMVFCid40:
        sig_name = "VFCVectorECMVFCid40"
        sig_start_bit = 42
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorECMVFCid50:
        sig_name = "VFCVectorECMVFCid50"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VFCVectorECMVFCid4:
        sig_name = "VFCVectorECMVFCid4"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid17:
        sig_name = "VFCVectorECMVFCid17"
        sig_start_bit = 19
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid54:
        sig_name = "VFCVectorECMVFCid54"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorECMVFCid14:
        sig_name = "VFCVectorECMVFCid14"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class VFCVectorECMVFCid0:
        sig_name = "VFCVectorECMVFCid0"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorECMVFCid19:
        sig_name = "VFCVectorECMVFCid19"
        sig_start_bit = 21
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class VFCVectorECMVFCid29:
        sig_name = "VFCVectorECMVFCid29"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid52:
        sig_name = "VFCVectorECMVFCid52"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid60:
        sig_name = "VFCVectorECMVFCid60"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid8:
        sig_name = "VFCVectorECMVFCid8"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VFCVectorECMVFCid9:
        sig_name = "VFCVectorECMVFCid9"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class VFCVectorECMVFCid37:
        sig_name = "VFCVectorECMVFCid37"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VFCVectorECMVFCid36:
        sig_name = "VFCVectorECMVFCid36"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class VFCVectorECMVFCid55:
        sig_name = "VFCVectorECMVFCid55"
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
        sig_value_table = {'VFCOnOff_Off': 0, 'VFCOnOff_On': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class VddmToEgsmPropDiagReqFrame:
    msg_name = "VddmToEgsmPropDiagReqFrame"
    msg_id = 1843
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['EGSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EtcSrsPropDevFr01:
    msg_name = "EtcSrsPropDevFr01"
    msg_id = 1457
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['SRS']
    sig_group_dict = {'SRSdevelpsignalgroupRX': ['SRSdevelpsignalgroupRXFunctiondevpsignalgroup1', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup2', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup3', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup4', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup5', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup6', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup7', 'SRSdevelpsignalgroupRXFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup3:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup3"
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

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup4:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup8:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup1:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup1"
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

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup2:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup6:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup5:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup5"
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

    class SRSdevelpsignalgroupRXFunctiondevpsignalgroup7:
        sig_name = "SRSdevelpsignalgroupRXFunctiondevpsignalgroup7"
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


class BecmPropFr12:
    msg_name = "BecmPropFr12"
    msg_id = 769
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'ECM', 'S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattPwrCdn:
        sig_name = "HvBattPwrCdn"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 200
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

    class HvBattChrgnPwrCritDes800:
        sig_name = "HvBattChrgnPwrCritDes800"
        sig_start_bit = 31
        update_id_bit = 49
        sig_length = 12
        sig_value_factor = 100
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class HvBattChrgnPwrNormDes800:
        sig_name = "HvBattChrgnPwrNormDes800"
        sig_start_bit = 35
        update_id_bit = 48
        sig_length = 12
        sig_value_factor = 100
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 35
        bmuws_info = [(4, 0b00001111, 0b11110000, 4, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HvBattChrgnPwrCns800:
        sig_name = "HvBattChrgnPwrCns800"
        sig_start_bit = 11
        update_id_bit = 14
        sig_length = 12
        sig_value_factor = 100
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class MgmPropFr06:
    msg_name = "MgmPropFr06"
    msg_id = 384
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['ECM', 'S2SReceiver']
    sig_group_dict = {'IsgSpdActSgnSafe800': ['IsgSpdActSgnSafe800Chks', 'IsgSpdActSgnSafe800Cntr', 'IsgSpdActSgnSafe800IsgSpdActSgn800', 'IsgSpdActSgnSafe800Qf'], 'IsgSpdActSgnSafe': ['IsgSpdActSgnSafeChks', 'IsgSpdActSgnSafeCntr', 'IsgSpdActSgnSafeIsgSpdWSgnTyp', 'IsgSpdActSgnSafeQf']}
    sig_group_dataid_dict = {'IsgSpdActSgnSafe800': 7004, 'IsgSpdActSgnSafe': 7003}

    class IsgSpdActSgnSafeCntr:
        sig_name = "IsgSpdActSgnSafeCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IsgSpdActSgnSafe800Cntr:
        sig_name = "IsgSpdActSgnSafe800Cntr"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IsgSpdActSgnSafeChks:
        sig_name = "IsgSpdActSgnSafeChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IsgSpdActSgnSafeIsgSpdWSgnTyp:
        sig_name = "IsgSpdActSgnSafeIsgSpdWSgnTyp"
        sig_start_bit = 23
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class IsgSpdActSgnSafe800Chks:
        sig_name = "IsgSpdActSgnSafe800Chks"
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

    class IsgSpdActSgnSafe800_UB:
        sig_name = "IsgSpdActSgnSafe800_UB"
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

    class IsgSpdActSgnSafe_UB:
        sig_name = "IsgSpdActSgnSafe_UB"
        sig_start_bit = 6
        update_id_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class IsgSpdActSgnSafe800Qf:
        sig_name = "IsgSpdActSgnSafe800Qf"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IsgSpdActSgnSafeQf:
        sig_name = "IsgSpdActSgnSafeQf"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IsgSpdActSgnSafe800IsgSpdActSgn800:
        sig_name = "IsgSpdActSgnSafe800IsgSpdActSgn800"
        sig_start_bit = 55
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class BecmPropFr07:
    msg_name = "BecmPropFr07"
    msg_id = 662
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'HvBattHeatStopReq': ['HvBattHeatStopReqBrkLiOnReqChks', 'HvBattHeatStopReqBrkLiOnReqCntr', 'HvBattHeatStopReqBrkLiOnReqSts']}
    sig_group_dataid_dict = {'HvBattHeatStopReq': 7005}

    class HvBattHeatStopReqBrkLiOnReqCntr:
        sig_name = "HvBattHeatStopReqBrkLiOnReqCntr"
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

    class HvBattCooltTReq:
        sig_name = "HvBattCooltTReq"
        sig_start_bit = 7
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class FastChrgnLockCtrl:
        sig_name = "FastChrgnLockCtrl"
        sig_start_bit = 14
        update_id_bit = 13
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
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class HvBattHeatStopReqBrkLiOnReqSts:
        sig_name = "HvBattHeatStopReqBrkLiOnReqSts"
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
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvBattHeatStopReq_UB:
        sig_name = "HvBattHeatStopReq_UB"
        sig_start_bit = 12
        update_id_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvBattHeatStopReqBrkLiOnReqChks:
        sig_name = "HvBattHeatStopReqBrkLiOnReqChks"
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


class VddmPropFr28:
    msg_name = "VddmPropFr28"
    msg_id = 667
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class NOPCoolReq:
        sig_name = "NOPCoolReq"
        sig_start_bit = 2
        update_id_bit = 1
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
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class EstimdLeSocToDest:
        sig_name = "EstimdLeSocToDest"
        sig_start_bit = 31
        update_id_bit = 24
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_byteorder = "Motorola"
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 31
        byte = 3
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class ChrgStationPwr:
        sig_name = "ChrgStationPwr"
        sig_start_bit = 10
        update_id_bit = 0
        sig_length = 10
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111110, 0b00000001, 7, 1)]


class BecmPropFr32:
    msg_name = "BecmPropFr32"
    msg_id = 1025
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {'BthBookStrtTiChrgnTmr': ['BthBookStrtTiChrgnTmrChrgnTmrhour', 'BthBookStrtTiChrgnTmrChrgnTmrmin'], 'BthBookStopTiChrgnTmr': ['BthBookStopTiChrgnTmrChrgnTmrhour', 'BthBookStopTiChrgnTmrChrgnTmrmin']}
    sig_group_dataid_dict = {}

    class BthBookStrtTiChrgnTmrChrgnTmrhour:
        sig_name = "BthBookStrtTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BthBookStopTiChrgnTmrChrgnTmrhour:
        sig_name = "BthBookStopTiChrgnTmrChrgnTmrhour"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 24
        sig_byteorder = "Motorola"
        sig_value_init = 24
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BthBookStrtTiChrgnTmr_UB:
        sig_name = "BthBookStrtTiChrgnTmr_UB"
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

    class ChrgPilBookChrgn:
        sig_name = "ChrgPilBookChrgn"
        sig_start_bit = 55
        update_id_bit = 48
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgPilBookChrgn_Default': 0, 'ChrgPilBookChrgn_On': 1, 'ChrgPilBookChrgn_Off': 2, 'ChrgPilBookChrgn_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BthBookStopTiChrgnTmrChrgnTmrmin:
        sig_name = "BthBookStopTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BthBookStrtTiChrgnTmrChrgnTmrmin:
        sig_name = "BthBookStrtTiChrgnTmrChrgnTmrmin"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60
        sig_byteorder = "Motorola"
        sig_value_init = 60
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BthBookStopTiChrgnTmr_UB:
        sig_name = "BthBookStopTiChrgnTmr_UB"
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


class EcmPropFr05:
    msg_name = "EcmPropFr05"
    msg_id = 132
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'VDDM']
    sig_group_dict = {'WhlMotSysTqAllwd': ['WhlMotSysTqAllwdChks', 'WhlMotSysTqAllwdCntr', 'WhlMotSysTqAllwdWhlMotSysTqAllwd']}
    sig_group_dataid_dict = {'WhlMotSysTqAllwd': 79}

    class WhlMotSysTqAllwdCntr:
        sig_name = "WhlMotSysTqAllwdCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class WhlMotSysTqAllwd_UB:
        sig_name = "WhlMotSysTqAllwd_UB"
        sig_start_bit = 6
        update_id_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class IsgPwrLimMin:
        sig_name = "IsgPwrLimMin"
        sig_start_bit = 31
        update_id_bit = 37
        sig_length = 10
        sig_value_factor = 0.5
        sig_value_offset = -511.0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Motorola"
        sig_value_init = 1022
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11000000, 0b00111111, 2, 6)]

    class OnBdChrgrPwrEnaAllwd:
        sig_name = "OnBdChrgrPwrEnaAllwd"
        sig_start_bit = 51
        update_id_bit = 54
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

    class WhlMotSysTqAllwdChks:
        sig_name = "WhlMotSysTqAllwdChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvPwrEgyPrio:
        sig_name = "HvPwrEgyPrio"
        sig_start_bit = 18
        update_id_bit = 19
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvPwrEgyPrio_Standby': 0, 'HvPwrEgyPrio_Dischrgning': 1, 'HvPwrEgyPrio_Chrgning': 2, 'HvPwrEgyPrio_ClimaWithAc': 3, 'HvPwrEgyPrio_ClimaWithoutAc': 4, 'HvPwrEgyPrio_RemoteClimatisaiton': 5}
        compute_method = None
        length = 3
        startbit = 18
        byte = 2
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class WhlMotSysTqAllwdWhlMotSysTqAllwd:
        sig_name = "WhlMotSysTqAllwdWhlMotSysTqAllwd"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IsgPwrLimMax:
        sig_name = "IsgPwrLimMax"
        sig_start_bit = 33
        update_id_bit = 55
        sig_length = 10
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class VddmBcmPropdTCFr01:
    msg_name = "VddmBcmPropdTCFr01"
    msg_id = 302
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'IEM']
    sig_group_dict = {'EscVariantToDmc': ['EscVariantToDmcChks', 'EscVariantToDmcCntr', 'EscVariantToDmcEscVariantToDmc']}
    sig_group_dataid_dict = {'EscVariantToDmc': 6564}

    class EscVariantToDmcChks:
        sig_name = "EscVariantToDmcChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EscVariantToDmcEscVariantToDmc:
        sig_name = "EscVariantToDmcEscVariantToDmc"
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

    class EscVariantToDmc_UB:
        sig_name = "EscVariantToDmc_UB"
        sig_start_bit = 4
        update_id_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class EscVariantToDmcCntr:
        sig_name = "EscVariantToDmcCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class MgmPropFr01:
    msg_name = "MgmPropFr01"
    msg_id = 1178
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['CCM']
    sig_group_dict = {'MGMTestFr1': ['MGMTestFr1Byte0', 'MGMTestFr1Byte1', 'MGMTestFr1Byte2', 'MGMTestFr1Byte3', 'MGMTestFr1Byte4', 'MGMTestFr1Byte5', 'MGMTestFr1Byte6', 'MGMTestFr1Byte7']}
    sig_group_dataid_dict = {}

    class MGMTestFr1Byte0:
        sig_name = "MGMTestFr1Byte0"
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

    class MGMTestFr1Byte7:
        sig_name = "MGMTestFr1Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MGMTestFr1Byte2:
        sig_name = "MGMTestFr1Byte2"
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

    class MGMTestFr1Byte5:
        sig_name = "MGMTestFr1Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MGMTestFr1Byte4:
        sig_name = "MGMTestFr1Byte4"
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

    class MGMTestFr1Byte3:
        sig_name = "MGMTestFr1Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MGMTestFr1Byte6:
        sig_name = "MGMTestFr1Byte6"
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

    class MGMTestFr1Byte1:
        sig_name = "MGMTestFr1Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BecmPropDevFr08:
    msg_name = "BecmPropDevFr08"
    msg_id = 1493
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup8': ['BECMdevelpsignalgroup8Functiondevpsignalgroup1', 'BECMdevelpsignalgroup8Functiondevpsignalgroup2', 'BECMdevelpsignalgroup8Functiondevpsignalgroup3', 'BECMdevelpsignalgroup8Functiondevpsignalgroup4', 'BECMdevelpsignalgroup8Functiondevpsignalgroup5', 'BECMdevelpsignalgroup8Functiondevpsignalgroup6', 'BECMdevelpsignalgroup8Functiondevpsignalgroup7', 'BECMdevelpsignalgroup8Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup8Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup8Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup8Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup8Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup8Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup8Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup8Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup8Functiondevpsignalgroup3"
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

    class BECMdevelpsignalgroup8Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup8Functiondevpsignalgroup5"
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

    class BECMdevelpsignalgroup8Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup8Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup8Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup8Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup8Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup8Functiondevpsignalgroup7"
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


class BecmPropFr24:
    msg_name = "BecmPropFr24"
    msg_id = 656
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM', 'S2SReceiver']
    sig_group_dict = {'HvBattCellTInfo': ['HvBattCellTInfoHvBattSnsrT', 'HvBattCellTInfoHvBattTMax', 'HvBattCellTInfoHvBattTMin', 'HvBattCellTInfoHvBattTSnsrNr', 'HvBattCellTInfoHvTempSnsrTMaxsSerlNr', 'HvBattCellTInfoHvTempSnsrTMinSerlNr']}
    sig_group_dataid_dict = {}

    class HvBattCellTInfoHvBattTMin:
        sig_name = "HvBattCellTInfoHvBattTMin"
        sig_start_bit = 23
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCellTInfo_UB:
        sig_name = "HvBattCellTInfo_UB"
        sig_start_bit = 55
        update_id_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvBattCellTInfoHvBattSnsrT:
        sig_name = "HvBattCellTInfoHvBattSnsrT"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCellTInfoHvBattTSnsrNr:
        sig_name = "HvBattCellTInfoHvBattTSnsrNr"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCellTInfoHvTempSnsrTMinSerlNr:
        sig_name = "HvBattCellTInfoHvTempSnsrTMinSerlNr"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCellTInfoHvBattTMax:
        sig_name = "HvBattCellTInfoHvBattTMax"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
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

    class LocalHvBattThermReqFb:
        sig_name = "LocalHvBattThermReqFb"
        sig_start_bit = 63
        update_id_bit = 56
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LocalHvBattThermReqFb_Idle': 0, 'LocalHvBattThermReqFb_Cooling': 1, 'LocalHvBattThermReqFb_Heating': 2, 'LocalHvBattThermReqFb_Erro': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattOptmzHint:
        sig_name = "HvBattOptmzHint"
        sig_start_bit = 53
        update_id_bit = 54
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvBattCellTInfoHvTempSnsrTMaxsSerlNr:
        sig_name = "HvBattCellTInfoHvTempSnsrTMaxsSerlNr"
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


class BecmPropFr09:
    msg_name = "BecmPropFr09"
    msg_id = 789
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'HvBattT': ['HvBattTAvg', 'HvBattTMax', 'HvBattTMin']}
    sig_group_dataid_dict = {}

    class HvBattTMin:
        sig_name = "HvBattTMin"
        sig_start_bit = 28
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 28
        bmuws_info = [(3, 0b00011111, 0b11100000, 5, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class HvBattTAvg:
        sig_name = "HvBattTAvg"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111100, 0b00000011, 6, 2)]

    class HvBattChrgnSts:
        sig_name = "HvBattChrgnSts"
        sig_start_bit = 56
        update_id_bit = 57
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaSts_Start': 0, 'ClimaSts_Finish': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HvBattTMax:
        sig_name = "HvBattTMax"
        sig_start_bit = 9
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11100000, 0b00011111, 3, 5)]

    class HvBattT_UB:
        sig_name = "HvBattT_UB"
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


class BecmPropFr19:
    msg_name = "BecmPropFr19"
    msg_id = 839
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'HvBattCod': ['HvBattCodPackCodeX1', 'HvBattCodPackCodeX2', 'HvBattCodPackCodeX3', 'HvBattCodPackCodeX4', 'HvBattCodPackCodeX5', 'HvBattCodPackCodeX6', 'HvBattCodPackIndex']}
    sig_group_dataid_dict = {}

    class HvBattCod_UB:
        sig_name = "HvBattCod_UB"
        sig_start_bit = 63
        update_id_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvBattCodPackIndex:
        sig_name = "HvBattCodPackIndex"
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

    class HvBattCodPackCodeX3:
        sig_name = "HvBattCodPackCodeX3"
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

    class HvBattCodPackCodeX2:
        sig_name = "HvBattCodPackCodeX2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCodPackCodeX6:
        sig_name = "HvBattCodPackCodeX6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCodPackCodeX4:
        sig_name = "HvBattCodPackCodeX4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCodPackCodeX1:
        sig_name = "HvBattCodPackCodeX1"
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

    class HvBattCodPackCodeX5:
        sig_name = "HvBattCodPackCodeX5"
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


class CddObcPropFr05:
    msg_name = "CddObcPropFr05"
    msg_id = 785
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {'DchaEgyStrg': ['DchaEgyStrgDchaCarTiGlb', 'DchaEgyStrgDchaEgy']}
    sig_group_dataid_dict = {}

    class DchaEgyStrg_UB:
        sig_name = "DchaEgyStrg_UB"
        sig_start_bit = 44
        update_id_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DchaEgyStrgDchaCarTiGlb:
        sig_name = "DchaEgyStrgDchaCarTiGlb"
        sig_start_bit = 7
        update_id_bit = None
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

    class DchaEgyStrgDchaEgy:
        sig_name = "DchaEgyStrgDchaEgy"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11100000, 0b00011111, 3, 5)]

    class V2XDchaSwtFdb:
        sig_name = "V2XDchaSwtFdb"
        sig_start_bit = 43
        update_id_bit = 40
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
        startbit = 43
        byte = 5
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class MaxACInpISetFdb:
        sig_name = "MaxACInpISetFdb"
        sig_start_bit = 54
        update_id_bit = 55
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 64
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 54
        byte = 6
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0


class BecmPropFr31:
    msg_name = "BecmPropFr31"
    msg_id = 261
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['CCM', 'ECM', 'S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DisChrgrFlg:
        sig_name = "DisChrgrFlg"
        sig_start_bit = 59
        update_id_bit = 56
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffUnknown_Init': 0, 'OnOffUnknown_On': 1, 'OnOffUnknown_Off': 2, 'OnOffUnknown_Unknown': 3, 'OnOffUnknown_Reserved1': 4, 'OnOffUnknown_Reserved2': 5}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class HvBattPwrLimDchaSoft800:
        sig_name = "HvBattPwrLimDchaSoft800"
        sig_start_bit = 27
        update_id_bit = 49
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class HVChrgModReq:
        sig_name = "HVChrgModReq"
        sig_start_bit = 63
        update_id_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 15
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgModeReq_No_Request': 0, 'ChrgModeReq_AC_Charging': 1, 'ChrgModeReq_Boost_PreCharging': 2, 'ChrgModeReq_Boost_Charging': 3, 'ChrgModeReq_DC_Charging': 4, 'ChrgModeReq_Reserved1': 5, 'ChrgModeReq_Reserved2': 6, 'ChrgModeReq_Init': 15}
        compute_method = None
        length = 4
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HvBattPwrLimDcha800:
        sig_name = "HvBattPwrLimDcha800"
        sig_start_bit = 23
        update_id_bit = 50
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class DCChrgrIMax:
        sig_name = "DCChrgrIMax"
        sig_start_bit = 7
        update_id_bit = 8
        sig_length = 15
        sig_value_factor = 0.1
        sig_value_offset = -1638.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 16380
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111110, 0b00000001, 7, 1)]

    class HvBattUDynMaxLim800:
        sig_name = "HvBattUDynMaxLim800"
        sig_start_bit = 47
        update_id_bit = 48
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11110000, 0b00001111, 4, 4)]


class VcuPropFr02:
    msg_name = "VcuPropFr02"
    msg_id = 919
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class ResvSupChrgThermSwt:
        sig_name = "ResvSupChrgThermSwt"
        sig_start_bit = 6
        update_id_bit = 7
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class VddmPropFr26:
    msg_name = "VddmPropFr26"
    msg_id = 566
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'HVCM', 'EGSM']
    sig_group_dict = {'VehCfgPrmExt': ['VehCfgPrmExtBlkIDBytePosn1', 'VehCfgPrmExtCCPBytePosn2', 'VehCfgPrmExtCCPBytePosn3', 'VehCfgPrmExtCCPBytePosn4', 'VehCfgPrmExtCCPBytePosn5', 'VehCfgPrmExtCCPBytePosn6', 'VehCfgPrmExtCCPBytePosn7', 'VehCfgPrmExtCCPBytePosn8']}
    sig_group_dataid_dict = {}

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


class EtcToVddmDevelFr:
    msg_name = "EtcToVddmDevelFr"
    msg_id = 1513
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'VDDMPropCANInternalDevReqMesg': ['VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup1', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup2', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup3', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup4', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup5', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup6', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup7', 'VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup5:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup5"
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

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup4:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup3:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup3"
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

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup2:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup7:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup7"
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

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup1:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup1"
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

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup6:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup8:
        sig_name = "VDDMPropCANInternalDevReqMesgFunctiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BgmPropulsionCANNmFr:
    msg_name = "BgmPropulsionCANNmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr07:
    msg_name = "VddmPropFr07"
    msg_id = 113
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class AxleSlipRelAct:
        sig_name = "AxleSlipRelAct"
        sig_start_bit = 53
        update_id_bit = 54
        sig_length = 14
        sig_value_factor = 0.003906369
        sig_value_offset = 0.0
        sig_value_min = -7679
        sig_value_max = 7680
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 53
        bmuws_info = [(6, 0b00111111, 0b11000000, 6, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class BecmPropDevFr06:
    msg_name = "BecmPropDevFr06"
    msg_id = 1491
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup6': ['BECMdevelpsignalgroup6Functiondevpsignalgroup1', 'BECMdevelpsignalgroup6Functiondevpsignalgroup2', 'BECMdevelpsignalgroup6Functiondevpsignalgroup3', 'BECMdevelpsignalgroup6Functiondevpsignalgroup4', 'BECMdevelpsignalgroup6Functiondevpsignalgroup5', 'BECMdevelpsignalgroup6Functiondevpsignalgroup6', 'BECMdevelpsignalgroup6Functiondevpsignalgroup7', 'BECMdevelpsignalgroup6Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup6Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup6Functiondevpsignalgroup5"
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

    class BECMdevelpsignalgroup6Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup6Functiondevpsignalgroup7"
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

    class BECMdevelpsignalgroup6Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup6Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup6Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup6Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup6Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup6Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup6Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup6Functiondevpsignalgroup3"
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

    class BECMdevelpsignalgroup6Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup6Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup6Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup6Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class IemPropFr01:
    msg_name = "IemPropFr01"
    msg_id = 1111
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['CCM']
    sig_group_dict = {'IEMTestFr1': ['IEMTestFr1Byte0', 'IEMTestFr1Byte1', 'IEMTestFr1Byte2', 'IEMTestFr1Byte3', 'IEMTestFr1Byte4', 'IEMTestFr1Byte5', 'IEMTestFr1Byte6', 'IEMTestFr1Byte7']}
    sig_group_dataid_dict = {}

    class IEMTestFr1Byte4:
        sig_name = "IEMTestFr1Byte4"
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

    class IEMTestFr1Byte5:
        sig_name = "IEMTestFr1Byte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IEMTestFr1Byte7:
        sig_name = "IEMTestFr1Byte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IEMTestFr1Byte6:
        sig_name = "IEMTestFr1Byte6"
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

    class IEMTestFr1Byte1:
        sig_name = "IEMTestFr1Byte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IEMTestFr1Byte2:
        sig_name = "IEMTestFr1Byte2"
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

    class IEMTestFr1Byte0:
        sig_name = "IEMTestFr1Byte0"
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

    class IEMTestFr1Byte3:
        sig_name = "IEMTestFr1Byte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VgmToAllJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToAllJ1979OBDPropCanReqFrame11"
    msg_id = 2015
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'VDDM', 'HVCM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class Ecm3PropDvelFr01:
    msg_name = "Ecm3PropDvelFr01"
    msg_id = 1530
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['CCM']
    sig_group_dict = {'Ecm3develpsignalgroup': ['Ecm3develpsignalgroupFunctiondevpsignalgroup1', 'Ecm3develpsignalgroupFunctiondevpsignalgroup2', 'Ecm3develpsignalgroupFunctiondevpsignalgroup3', 'Ecm3develpsignalgroupFunctiondevpsignalgroup4', 'Ecm3develpsignalgroupFunctiondevpsignalgroup5', 'Ecm3develpsignalgroupFunctiondevpsignalgroup6', 'Ecm3develpsignalgroupFunctiondevpsignalgroup7', 'Ecm3develpsignalgroupFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class Ecm3develpsignalgroupFunctiondevpsignalgroup3:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup3"
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

    class Ecm3develpsignalgroupFunctiondevpsignalgroup2:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class Ecm3develpsignalgroupFunctiondevpsignalgroup6:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class Ecm3develpsignalgroupFunctiondevpsignalgroup1:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup1"
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

    class Ecm3develpsignalgroupFunctiondevpsignalgroup7:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup7"
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

    class Ecm3develpsignalgroupFunctiondevpsignalgroup8:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class Ecm3develpsignalgroupFunctiondevpsignalgroup5:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup5"
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

    class Ecm3develpsignalgroupFunctiondevpsignalgroup4:
        sig_name = "Ecm3develpsignalgroupFunctiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BecmPropDevFr04:
    msg_name = "BecmPropDevFr04"
    msg_id = 1489
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup4': ['BECMdevelpsignalgroup4Functiondevpsignalgroup1', 'BECMdevelpsignalgroup4Functiondevpsignalgroup2', 'BECMdevelpsignalgroup4Functiondevpsignalgroup3', 'BECMdevelpsignalgroup4Functiondevpsignalgroup4', 'BECMdevelpsignalgroup4Functiondevpsignalgroup5', 'BECMdevelpsignalgroup4Functiondevpsignalgroup6', 'BECMdevelpsignalgroup4Functiondevpsignalgroup7', 'BECMdevelpsignalgroup4Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup4Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup4Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup4Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup4Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup4Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup4Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup7"
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

    class BECMdevelpsignalgroup4Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup5"
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

    class BECMdevelpsignalgroup4Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup4Functiondevpsignalgroup3"
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


class BecmPropFr27:
    msg_name = "BecmPropFr27"
    msg_id = 1177
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattCap:
        sig_name = "HvBattCap"
        sig_start_bit = 7
        update_id_bit = 23
        sig_length = 16
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class TotChrgCap:
        sig_name = "TotChrgCap"
        sig_start_bit = 39
        update_id_bit = 22
        sig_length = 32
        sig_value_factor = 0.01
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


class VddmToAllPropDiagReqFrame:
    msg_name = "VddmToAllPropDiagReqFrame"
    msg_id = 2047
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'HVCM', 'EGSM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HvcmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "HvcmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2029
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HvcmPropulsionCANNmFr:
    msg_name = "HvcmPropulsionCANNmFr"
    msg_id = 1327
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class MgmPropulsionCANNmFr:
    msg_name = "MgmPropulsionCANNmFr"
    msg_id = 1325
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['IEM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class HvcmPropFr01:
    msg_name = "HvcmPropFr01"
    msg_id = 631
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['CCM', 'S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class OnBdChrgrFaultSts:
        sig_name = "OnBdChrgrFaultSts"
        sig_start_bit = 27
        update_id_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FaultType_NoErr': 0, 'FaultType_Warning': 1, 'FaultType_Recoverable_Fault': 2, 'FaultType_Unrecoverable_Fault': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class OnBdChrgrCCSts:
        sig_name = "OnBdChrgrCCSts"
        sig_start_bit = 20
        update_id_bit = 17
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CCSts_NotConnected': 0, 'CCSts_HalfConnected': 1, 'CCSts_Connected': 2, 'CCSts_Connected_V2L': 3, 'CCSts_Short_Circuit': 4}
        compute_method = None
        length = 3
        startbit = 20
        byte = 2
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class OnBdChrgrPortT:
        sig_name = "OnBdChrgrPortT"
        sig_start_bit = 7
        update_id_bit = 11
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
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

    class DCDCInSts:
        sig_name = "DCDCInSts"
        sig_start_bit = 23
        update_id_bit = 8
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DCDCSts_Default': 0, 'DCDCSts_Init': 1, 'DCDCSts_Standby': 2, 'DCDCSts_Buck': 3, 'DCDCSts_Failure': 4, 'DCDCSts_Reserved1': 5, 'DCDCSts_Reserved2': 6, 'DCDCSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class PwrDegradedSts:
        sig_name = "PwrDegradedSts"
        sig_start_bit = 15
        update_id_bit = 10
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PwrDegradedSts_Default': 0, 'PwrDegradedSts_OBCOverT': 1, 'PwrDegradedSts_ChrgrOverT': 2, 'PwrDegradedSts_HndlLockgFlt': 3, 'PwrDegradedSts_IntElecFlt': 4, 'PwrDegradedSts_OBCCoolingOverT': 5, 'PwrDegradedSts_OBCLowT': 6, 'PwrDegradedSts_Reserved1': 7, 'PwrDegradedSts_Reserved2': 8, 'PwrDegradedSts_Reserved': 15}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class OnBdChrgrHndlSts2:
        sig_name = "OnBdChrgrHndlSts2"
        sig_start_bit = 39
        update_id_bit = 24
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 8
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnBdChrgrHndlSts2_Disconnected': 0, 'OnBdChrgrHndlSts2_ConnectedWithoutPower': 1, 'OnBdChrgrHndlSts2_PowerAvailableButNotActivated': 2, 'OnBdChrgrHndlSts2_ConnectedWithPower': 3, 'OnBdChrgrHndlSts2_DischargeConnectwithoutpowerincar': 4, 'OnBdChrgrHndlSts2_DischargeConnectwithoutpoweroutcar': 5, 'OnBdChrgrHndlSts2_DischargeConnectwithpowerincar': 6, 'OnBdChrgrHndlSts2_DischargeConnectwithpoweroutcar': 7, 'OnBdChrgrHndlSts2_Init': 8, 'OnBdChrgrHndlSts2_Fault': 9, 'OnBdChrgrHndlSts2_NotCompleteConnnected': 10, 'OnBdChrgrHndlSts2_ConnectedWithPowerButNotPWM': 11, 'OnBdChrgrHndlSts2_Reserved1': 12, 'OnBdChrgrHndlSts2_Reserved2': 13}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class OnBdChrgrCPSts:
        sig_name = "OnBdChrgrCPSts"
        sig_start_bit = 31
        update_id_bit = 28
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CPSts_0V': 0, 'CPSts_9V': 1, 'CPSts_9V_PWM': 2, 'CPSts_6V': 3, 'CPSts_6V_PWM': 4, 'CPSts_Failure': 5, 'CPSts_Digital': 6, 'CPSts_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 31
        byte = 3
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class VddmPropFr15:
    msg_name = "VddmPropFr15"
    msg_id = 609
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'MGM']
    sig_group_dict = {'ImobEngMgrReq3': ['ImobEngMgrReq3ImobEngDataMgrReq0', 'ImobEngMgrReq3ImobEngDataMgrReq1', 'ImobEngMgrReq3ImobEngDataMgrReq2', 'ImobEngMgrReq3ImobEngDataMgrReq3', 'ImobEngMgrReq3ImobEngDataMgrReq4', 'ImobEngMgrReq3ImobEngDataMgrReq5', 'ImobEngMgrReq3ImobEngDataMgrReq6', 'ImobEngMgrReq3ImobEngMgrCmdTar1']}
    sig_group_dataid_dict = {}

    class ImobEngMgrReq3_UB:
        sig_name = "ImobEngMgrReq3_UB"
        sig_start_bit = 2
        update_id_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ImobEngMgrReq3ImobEngDataMgrReq6:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq6"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MaintainBattTCtrl:
        sig_name = "MaintainBattTCtrl"
        sig_start_bit = 3
        update_id_bit = 4
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ImobEngMgrReq3ImobEngMgrCmdTar1:
        sig_name = "ImobEngMgrReq3ImobEngMgrCmdTar1"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobEngMgrReqCmd_ImobEngCmdTarIdle': 0, 'ImobEngMgrReqCmd_ImobEngMtnStrtReqCmd': 1, 'ImobEngMgrReqCmd_ImobEngNoMtnStrtReqCmd': 2, 'ImobEngMgrReqCmd_ImobEngTurnOffCmd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ImobEngMgrReq3ImobEngDataMgrReq3:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq3"
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

    class ImobEngMgrReq3ImobEngDataMgrReq1:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq1"
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

    class ImobEngMgrReq3ImobEngDataMgrReq5:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq5"
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

    class ImobEngMgrReq3ImobEngDataMgrReq4:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq4"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq3ImobEngDataMgrReq2:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq2"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq3ImobEngDataMgrReq0:
        sig_name = "ImobEngMgrReq3ImobEngDataMgrReq0"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class BgmPropulsionFr04:
    msg_name = "BgmPropulsionFr04"
    msg_id = 1018
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.32
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ECM']
    sig_group_dict = {'CDCActT': ['CDCActTEngT', 'CDCActTEngTQf'], 'ACUActT': ['ACUActTEngT', 'ACUActTEngTQf']}
    sig_group_dataid_dict = {}

    class ACUActTEngT:
        sig_name = "ACUActTEngT"
        sig_start_bit = 7
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDCCoolantFlwReq:
        sig_name = "CDCCoolantFlwReq"
        sig_start_bit = 55
        update_id_bit = 40
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 511
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b10000000, 0b01111111, 1, 7)]

    class ACUActTEngTQf:
        sig_name = "ACUActTEngTQf"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ACUCoolantFlwReq:
        sig_name = "ACUCoolantFlwReq"
        sig_start_bit = 23
        update_id_bit = 8
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 511
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b10000000, 0b01111111, 1, 7)]

    class CDCActTEngT:
        sig_name = "CDCActTEngT"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDCActT_UB:
        sig_name = "CDCActT_UB"
        sig_start_bit = 41
        update_id_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ACUActT_UB:
        sig_name = "ACUActT_UB"
        sig_start_bit = 9
        update_id_bit = 9
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
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CDCActTEngTQf:
        sig_name = "CDCActTEngTQf"
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
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BecmPropFr01:
    msg_name = "BecmPropFr01"
    msg_id = 321
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['IEM', 'S2SReceiver', 'MGM', 'VDDM', 'HVCM', 'ECM']
    sig_group_dict = {'HvSysRlySts': ['HvSysRlyStsChks', 'HvSysRlyStsCntr', 'HvSysRlyStsHvSysRlySts']}
    sig_group_dataid_dict = {'HvSysRlySts': 21}

    class HvSysRlyStsCntr:
        sig_name = "HvSysRlyStsCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HvBattUDc800:
        sig_name = "HvBattUDc800"
        sig_start_bit = 55
        update_id_bit = 39
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11110000, 0b00001111, 4, 4)]

    class HvSysRlyStsHvSysRlySts:
        sig_name = "HvSysRlyStsHvSysRlySts"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvActvnSts_Open': 0, 'HvActvnSts_Clsd': 1, 'HvActvnSts_KeepSt': 2, 'HvActvnSts_OpenAndReqActvDcha': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvSysPwrOff:
        sig_name = "HvSysPwrOff"
        sig_start_bit = 59
        update_id_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OkNotOk1_Ok': 0, 'OkNotOk1_NotOk': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HvSysActvnInhb:
        sig_name = "HvSysActvnInhb"
        sig_start_bit = 37
        update_id_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OkNotOk1_Ok': 0, 'OkNotOk1_NotOk': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvSysRlySts_UB:
        sig_name = "HvSysRlySts_UB"
        sig_start_bit = 22
        update_id_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class HvSysSts:
        sig_name = "HvSysSts"
        sig_start_bit = 58
        update_id_bit = 56
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvSysSts_Inin': 0, 'HvSysSts_Test': 1, 'HvSysSts_Rdy': 2}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class HvBattUDc:
        sig_name = "HvBattUDc"
        sig_start_bit = 18
        update_id_bit = 19
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvSysRlyStsChks:
        sig_name = "HvSysRlyStsChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattUDynMaxLim:
        sig_name = "HvBattUDynMaxLim"
        sig_start_bit = 34
        update_id_bit = 35
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class EcmPropXEVFr16:
    msg_name = "EcmPropXEVFr16"
    msg_id = 649
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattCoolgEgyCnsAllwd1:
        sig_name = "HvBattCoolgEgyCnsAllwd1"
        sig_start_bit = 17
        update_id_bit = 54
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class RadFanCoolgSts:
        sig_name = "RadFanCoolgSts"
        sig_start_bit = 39
        update_id_bit = 8
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
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HvBattChrgnEgyCnsAllwd1:
        sig_name = "HvBattChrgnEgyCnsAllwd1"
        sig_start_bit = 52
        update_id_bit = 53
        sig_length = 13
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class HvBattChrgnILim:
        sig_name = "HvBattChrgnILim"
        sig_start_bit = 36
        update_id_bit = 55
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class VddmPropFr18:
    msg_name = "VddmPropFr18"
    msg_id = 86
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'HVCM', 'EGSM']
    sig_group_dict = {'VehModMngtGlbSafe1': ['VehModMngtGlbSafe1CarModSts1', 'VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp', 'VehModMngtGlbSafe1Chks', 'VehModMngtGlbSafe1Cntr', 'VehModMngtGlbSafe1EgyLvlElecMai', 'VehModMngtGlbSafe1EgyLvlElecSubtyp', 'VehModMngtGlbSafe1FltEgyCnsWdSts', 'VehModMngtGlbSafe1PwrLvlElecMai', 'VehModMngtGlbSafe1PwrLvlElecSubtyp', 'VehModMngtGlbSafe1UsgModSts']}
    sig_group_dataid_dict = {'VehModMngtGlbSafe1': 116}

    class VehModMngtGlbSafe1PwrLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp"
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

    class ChrgnUReq:
        sig_name = "ChrgnUReq"
        sig_start_bit = 55
        update_id_bit = 40
        sig_length = 8
        sig_value_factor = 0.025
        sig_value_offset = 10.6
        sig_value_min = 0
        sig_value_max = 216
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

    class IntrBriSts:
        sig_name = "IntrBriSts"
        sig_start_bit = 44
        update_id_bit = 45
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
        startbit = 44
        byte = 5
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

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

    class VehModMngtGlbSafe1EgyLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp"
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

    class VehModMngtGlbSafe1UsgModSts:
        sig_name = "VehModMngtGlbSafe1UsgModSts"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

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

    class TwliBriSts:
        sig_name = "TwliBriSts"
        sig_start_bit = 47
        update_id_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TwliBriSts1_Night': 0, 'TwliBriSts1_Day': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class VehModMngtGlbSafe1EgyLvlElecMai:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
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


class IemPropFr14:
    msg_name = "IemPropFr14"
    msg_id = 544
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlMotSysHeatPwrMax:
        sig_name = "WhlMotSysHeatPwrMax"
        sig_start_bit = 7
        update_id_bit = 12
        sig_length = 8
        sig_value_factor = 50
        sig_value_offset = 0
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

    class WhlMotSysHeatFdBck:
        sig_name = "WhlMotSysHeatFdBck"
        sig_start_bit = 15
        update_id_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysHeatFdBck_On': 0, 'WhlMotSysHeatFdBck_Off': 1, 'WhlMotSysHeatFdBck_Inhibt': 2, 'WhlMotSysHeatFdBck_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class EcmPropFr08:
    msg_name = "EcmPropFr08"
    msg_id = 369
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'VDDM', 'HVCM']
    sig_group_dict = {'EngT': ['EngTEngT', 'EngTQf']}
    sig_group_dataid_dict = {}

    class HvOnMaiReq:
        sig_name = "HvOnMaiReq"
        sig_start_bit = 60
        update_id_bit = 58
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvActvnSts_Open': 0, 'HvActvnSts_Clsd': 1, 'HvActvnSts_KeepSt': 2, 'HvActvnSts_OpenAndReqActvDcha': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class EngT_UB:
        sig_name = "EngT_UB"
        sig_start_bit = 34
        update_id_bit = 34
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
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class EngTEngT:
        sig_name = "EngTEngT"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IsgActvDampgModReq:
        sig_name = "IsgActvDampgModReq"
        sig_start_bit = 39
        update_id_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysActvDampgModCodSts_NoDampg': 0, 'WhlMotSysActvDampgModCodSts_LoDampg': 1, 'WhlMotSysActvDampgModCodSts_MedDampg': 2, 'WhlMotSysActvDampgModCodSts_HiDampg': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattCoolgCmd:
        sig_name = "HvBattCoolgCmd"
        sig_start_bit = 63
        update_id_bit = 61
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVBattChargnCmd_OK': 0, 'HVBattChargnCmd_NOK': 1, 'HVBattChargnCmd_INIT': 2, 'HVBattChargnCmd_HOLD': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PrpsnFbLimnIndcn:
        sig_name = "PrpsnFbLimnIndcn"
        sig_start_bit = 22
        update_id_bit = 23
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
        startbit = 22
        byte = 2
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class TqModAct:
        sig_name = "TqModAct"
        sig_start_bit = 55
        update_id_bit = 51
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
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class EngTQf:
        sig_name = "EngTQf"
        sig_start_bit = 33
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class IgmMgmPropFr05:
    msg_name = "IgmMgmPropFr05"
    msg_id = 342
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['BECM1', 'VDDM', 'S2SReceiver', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class IsgUDc800:
        sig_name = "IsgUDc800"
        sig_start_bit = 31
        update_id_bit = 23
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11110000, 0b00001111, 4, 4)]

    class IsgLimnIndcn:
        sig_name = "IsgLimnIndcn"
        sig_start_bit = 55
        update_id_bit = 20
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
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class IsgUDc:
        sig_name = "IsgUDc"
        sig_start_bit = 2
        update_id_bit = 3
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class EcmPropFr01:
    msg_name = "EcmPropFr01"
    msg_id = 80
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'VDDM']
    sig_group_dict = {'AccrPedlLnr': ['AccrPedlLnrAccrPedlRat', 'AccrPedlLnrChks', 'AccrPedlLnrCntr']}
    sig_group_dataid_dict = {'AccrPedlLnr': 707}

    class AccrPedlLnrChks:
        sig_name = "AccrPedlLnrChks"
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

    class AccrPedlLnrCntr:
        sig_name = "AccrPedlLnrCntr"
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

    class PrpsnTqFrntReq:
        sig_name = "PrpsnTqFrntReq"
        sig_start_bit = 55
        update_id_bit = 7
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class AccrPedlLnr_UB:
        sig_name = "AccrPedlLnr_UB"
        sig_start_bit = 43
        update_id_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AccrPedlLnrAccrPedlRat:
        sig_name = "AccrPedlLnrAccrPedlRat"
        sig_start_bit = 23
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class IsgTqReq:
        sig_name = "IsgTqReq"
        sig_start_bit = 5
        update_id_bit = 6
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
        startbit = 5
        bmuws_info = [(0, 0b00111111, 0b11000000, 6, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class BecmPropFr16:
    msg_name = "BecmPropFr16"
    msg_id = 833
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattClimaPwr:
        sig_name = "HvBattClimaPwr"
        sig_start_bit = 2
        update_id_bit = 3
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class TotChrgEgy:
        sig_name = "TotChrgEgy"
        sig_start_bit = 39
        update_id_bit = 20
        sig_length = 32
        sig_value_factor = 1.0
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

    class HvBattHeatgEgyReq:
        sig_name = "HvBattHeatgEgyReq"
        sig_start_bit = 17
        update_id_bit = 7
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvBattClrRdyReq:
        sig_name = "HvBattClrRdyReq"
        sig_start_bit = 18
        update_id_bit = 19
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class BecmPropFr05:
    msg_name = "BecmPropFr05"
    msg_id = 661
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvSysCrashFb:
        sig_name = "HvSysCrashFb"
        sig_start_bit = 54
        update_id_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CrashFb_Idle': 0, 'CrashFb_Evln': 1, 'CrashFb_Nok': 2, 'CrashFb_Ok': 3}
        compute_method = None
        length = 2
        startbit = 54
        byte = 6
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HvBattPVal:
        sig_name = "HvBattPVal"
        sig_start_bit = 7
        update_id_bit = 10
        sig_length = 13
        sig_value_factor = 0.05
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class HvIsoSts:
        sig_name = "HvIsoSts"
        sig_start_bit = 52
        update_id_bit = 50
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Insulation_Default': 0, 'Insulation_Error_Battery_before_HV_Ready': 1, 'Insulation_Error_HV_bus_after_HV_Ready': 2, 'Insulation_OK': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HVIL3Sts:
        sig_name = "HVIL3Sts"
        sig_start_bit = 33
        update_id_bit = 32
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenClose_Open': 0, 'OpenClose_Close': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HVIL2Sts:
        sig_name = "HVIL2Sts"
        sig_start_bit = 35
        update_id_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenClose_Open': 0, 'OpenClose_Close': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HVIL1Sts:
        sig_name = "HVIL1Sts"
        sig_start_bit = 39
        update_id_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenClose_Open': 0, 'OpenClose_Close': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvBattCoolgSts:
        sig_name = "HvBattCoolgSts"
        sig_start_bit = 36
        update_id_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaSts_Start': 0, 'ClimaSts_Finish': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class VddmPropVFCInfoEnaFr:
    msg_name = "VddmPropVFCInfoEnaFr"
    msg_id = 1375
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 1
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'EGSM', 'HVCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class VFCInfoEna:
        sig_name = "VFCInfoEna"
        sig_start_bit = 0
        update_id_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisableCoding_Disabled': 0, 'EnableDisableCoding_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class VddmToBecmPropDiagReqFrame:
    msg_name = "VddmToBecmPropDiagReqFrame"
    msg_id = 1845
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr14:
    msg_name = "VddmPropFr14"
    msg_id = 358
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'LimForDecel': ['LimForDecelChks', 'LimForDecelCntr', 'LimForDecelNotExcd']}
    sig_group_dataid_dict = {'LimForDecel': 139}

    class LimForDecelCntr:
        sig_name = "LimForDecelCntr"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class LimForDecel_UB:
        sig_name = "LimForDecel_UB"
        sig_start_bit = 53
        update_id_bit = 53
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
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class LimForDecelNotExcd:
        sig_name = "LimForDecelNotExcd"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class LimForDecelChks:
        sig_name = "LimForDecelChks"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class TiDrvgCycOff:
        sig_name = "TiDrvgCycOff"
        sig_start_bit = 23
        update_id_bit = 38
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class EcmPropXevFr06:
    msg_name = "EcmPropXevFr06"
    msg_id = 328
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'IEM']
    sig_group_dict = {'IsgTqAllwd': ['IsgTqAllwdChks', 'IsgTqAllwdCntr', 'IsgTqAllwdIsgTqAllwd']}
    sig_group_dataid_dict = {'IsgTqAllwd': 80}

    class IsgTqAllwdCntr:
        sig_name = "IsgTqAllwdCntr"
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

    class WhlMotSysActvDampgModReq:
        sig_name = "WhlMotSysActvDampgModReq"
        sig_start_bit = 50
        update_id_bit = 48
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysActvDampgModCodSts_NoDampg': 0, 'WhlMotSysActvDampgModCodSts_LoDampg': 1, 'WhlMotSysActvDampgModCodSts_MedDampg': 2, 'WhlMotSysActvDampgModCodSts_HiDampg': 3}
        compute_method = None
        length = 2
        startbit = 50
        byte = 6
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class IsgTqAllwdIsgTqAllwd:
        sig_name = "IsgTqAllwdIsgTqAllwd"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IsgTqAllwdChks:
        sig_name = "IsgTqAllwdChks"
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

    class IsgTqAllwd_UB:
        sig_name = "IsgTqAllwd_UB"
        sig_start_bit = 54
        update_id_bit = 54
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
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class WhlMotSysPwrLimMin:
        sig_name = "WhlMotSysPwrLimMin"
        sig_start_bit = 23
        update_id_bit = 29
        sig_length = 10
        sig_value_factor = 0.5
        sig_value_offset = -511.0
        sig_value_min = 0
        sig_value_max = 1022
        sig_byteorder = "Motorola"
        sig_value_init = 1022
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11000000, 0b00111111, 2, 6)]


class BecmPropFr14:
    msg_name = "BecmPropFr14"
    msg_id = 646
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.14
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattHeatGenn:
        sig_name = "HvBattHeatGenn"
        sig_start_bit = 43
        update_id_bit = 48
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 43
        bmuws_info = [(5, 0b00001111, 0b11110000, 4, 0), (6, 0b11111110, 0b00000001, 7, 1)]

    class PackNr:
        sig_name = "PackNr"
        sig_start_bit = 63
        update_id_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattDchaTiEstimd:
        sig_name = "HvBattDchaTiEstimd"
        sig_start_bit = 23
        update_id_bit = 28
        sig_length = 11
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11100000, 0b00011111, 3, 5)]

    class HvBattPreHeatFaild:
        sig_name = "HvBattPreHeatFaild"
        sig_start_bit = 45
        update_id_bit = 44
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
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvBattEgyAvlDcha1:
        sig_name = "HvBattEgyAvlDcha1"
        sig_start_bit = 4
        update_id_bit = 5
        sig_length = 13
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class VddmPropFr05:
    msg_name = "VddmPropFr05"
    msg_id = 118
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'HVCM', 'EGSM']
    sig_group_dict = {'VehSpdLgt': ['VehSpdLgtA', 'VehSpdLgtChks', 'VehSpdLgtCntr', 'VehSpdLgtQf'], 'VehMtnSt': ['VehMtnStChks', 'VehMtnStCntr', 'VehMtnStVehMtnSt']}
    sig_group_dataid_dict = {'VehSpdLgt': 55, 'VehMtnSt': 54}

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

    class VehMtnStCntr:
        sig_name = "VehMtnStCntr"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class VehMtnStVehMtnSt:
        sig_name = "VehMtnStVehMtnSt"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehMtnSt2_Ukwn': 0, 'VehMtnSt2_StandStillVal1': 1, 'VehMtnSt2_StandStillVal2': 2, 'VehMtnSt2_StandStillVal3': 3, 'VehMtnSt2_RollgFwdVal1': 4, 'VehMtnSt2_RollgFwdVal2': 5, 'VehMtnSt2_RollgBackwVal1': 6, 'VehMtnSt2_RollgBackwVal2': 7}
        compute_method = None
        length = 3
        startbit = 18
        byte = 2
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class VehMtnSt_UB:
        sig_name = "VehMtnSt_UB"
        sig_start_bit = 57
        update_id_bit = 57
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
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

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

    class VehMtnStChks:
        sig_name = "VehMtnStChks"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

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


class IgmMgmPropFr07:
    msg_name = "IgmMgmPropFr07"
    msg_id = 627
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {'IgmGeneric': ['IgmGenericADAlrmSt', 'IgmGenericDTCHig', 'IgmGenericDTCLow', 'IgmGenericDTCMid', 'IgmGenericDTCSts', 'IgmGenericEMQnty', 'IgmGenericEMSeqNr', 'IgmGenericFltAlrmSt', 'IgmGenericIacAlrmSt', 'IgmGenericInvrtTAlrmSt', 'IgmGenericModStatusRms', 'IgmGenericMotTAlrmSt', 'IgmGenericRslAlrmSt', 'IgmGenericSpdAlrmSt', 'IgmGenericTypeInfo', 'IgmGenericUDcAlrmSt']}
    sig_group_dataid_dict = {}

    class IgmGenericADAlrmSt:
        sig_name = "IgmGenericADAlrmSt"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IgmGenericRslAlrmSt:
        sig_name = "IgmGenericRslAlrmSt"
        sig_start_bit = 61
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IgmGenericSpdAlrmSt:
        sig_name = "IgmGenericSpdAlrmSt"
        sig_start_bit = 59
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class IgmGenericUDcAlrmSt:
        sig_name = "IgmGenericUDcAlrmSt"
        sig_start_bit = 57
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IgmGenericFltAlrmSt:
        sig_name = "IgmGenericFltAlrmSt"
        sig_start_bit = 53
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IgmGenericTypeInfo:
        sig_name = "IgmGenericTypeInfo"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IgmGenericMotTAlrmSt:
        sig_name = "IgmGenericMotTAlrmSt"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IgmGenericModStatusRms:
        sig_name = "IgmGenericModStatusRms"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModStatusRms_Invalid': 0, 'ModStatusRms_PwrCns': 1, 'ModStatusRms_PwrGen': 2, 'ModStatusRms_OffSts': 3, 'ModStatusRms_RdySts': 4, 'ModStatusRms_Abnormal': 5, 'ModStatusRms_Invalid1': 6, 'ModStatusRms_Invalid2': 7, 'ModStatusRms_Invalid3': 8, 'ModStatusRms_Invalid4': 9, 'ModStatusRms_Invalid5': 10, 'ModStatusRms_Invalid6': 11, 'ModStatusRms_Invalid7': 12, 'ModStatusRms_Invalid8': 13, 'ModStatusRms_Invalid9': 14, 'ModStatusRms_Invalid10': 15}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class IgmGenericDTCLow:
        sig_name = "IgmGenericDTCLow"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IgmGenericDTCHig:
        sig_name = "IgmGenericDTCHig"
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

    class IgmGenericDTCMid:
        sig_name = "IgmGenericDTCMid"
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

    class IgmGenericInvrtTAlrmSt:
        sig_name = "IgmGenericInvrtTAlrmSt"
        sig_start_bit = 49
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IgmGenericDTCSts:
        sig_name = "IgmGenericDTCSts"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IgmGenericEMQnty:
        sig_name = "IgmGenericEMQnty"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class IgmGenericEMSeqNr:
        sig_name = "IgmGenericEMSeqNr"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IgmGenericIacAlrmSt:
        sig_name = "IgmGenericIacAlrmSt"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class IemPropFr15:
    msg_name = "IemPropFr15"
    msg_id = 674
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BoostUDCHv1:
        sig_name = "BoostUDCHv1"
        sig_start_bit = 55
        update_id_bit = 40
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11110000, 0b00001111, 4, 4)]

    class BoostIDCLv1:
        sig_name = "BoostIDCLv1"
        sig_start_bit = 7
        update_id_bit = 8
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111100, 0b00000011, 6, 2)]

    class BoostLvRlySts:
        sig_name = "BoostLvRlySts"
        sig_start_bit = 59
        update_id_bit = 56
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BoostLvRlySts_Default': 0, 'BoostLvRlySts_Open': 1, 'BoostLvRlySts_Close': 2, 'BoostLvRlySts_StuckOpen': 3, 'BoostLvRlySts_StuckClose': 4, 'BoostLvRlySts_Undefined': 5, 'BoostLvRlySts_Reserved1': 6, 'BoostLvRlySts_Reserved2': 7}
        compute_method = None
        length = 3
        startbit = 59
        byte = 7
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class BoostUDCLv1:
        sig_name = "BoostUDCLv1"
        sig_start_bit = 39
        update_id_bit = 41
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11110000, 0b00001111, 4, 4)]

    class BoostIDCHv1:
        sig_name = "BoostIDCHv1"
        sig_start_bit = 23
        update_id_bit = 24
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111100, 0b00000011, 6, 2)]


class BecmToVddmPropDiagRespFrame:
    msg_name = "BecmToVddmPropDiagRespFrame"
    msg_id = 1589
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmToEtcDevelFr:
    msg_name = "VddmToEtcDevelFr"
    msg_id = 1518
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['CCM']
    sig_group_dict = {'VDDMPropCANInternalDevRespMesg': ['VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup1', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup2', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup3', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup4', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup5', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup6', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup7', 'VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup8:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup4:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup2:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup3:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup3"
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

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup5:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup5"
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

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup7:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup7"
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

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup1:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup1"
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

    class VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup6:
        sig_name = "VDDMPropCANInternalDevRespMesgFunctiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class IemPropFr07:
    msg_name = "IemPropFr07"
    msg_id = 643
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.15
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlMotCooltFlowMinReq:
        sig_name = "WhlMotCooltFlowMinReq"
        sig_start_bit = 1
        update_id_bit = 54
        sig_length = 10
        sig_value_factor = 0.01
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 1
        bmuws_info = [(0, 0b00000011, 0b11111100, 2, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class BecmPropFr02:
    msg_name = "BecmPropFr02"
    msg_id = 373
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['IEM', 'CCM', 'MGM', 'VDDM', 'S2SReceiver', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class MaintainBattTReq:
        sig_name = "MaintainBattTReq"
        sig_start_bit = 31
        update_id_bit = 30
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaSts_Start': 0, 'ClimaSts_Finish': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class JIDUChgrFlg:
        sig_name = "JIDUChgrFlg"
        sig_start_bit = 7
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattThermTiEstimd:
        sig_name = "HvBattThermTiEstimd"
        sig_start_bit = 15
        update_id_bit = 0
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
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

    class DisChrgnSts:
        sig_name = "DisChrgnSts"
        sig_start_bit = 4
        update_id_bit = 23
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DisChrgnSts_Init': 0, 'DisChrgnSts_Prestart': 1, 'DisChrgnSts_DisChrgn': 2, 'DisChrgnSts_Finish': 3, 'DisChrgnSts_Fault': 4, 'DisChrgnSts_Reserved': 5, 'DisChrgnSts_Reserved1': 6, 'DisChrgnSts_Reserved2': 7}
        compute_method = None
        length = 4
        startbit = 4
        byte = 0
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class MaintainBattTFb:
        sig_name = "MaintainBattTFb"
        sig_start_bit = 59
        update_id_bit = 57
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BookChrgnStsFb_Default': 0, 'BookChrgnStsFb_Success': 1, 'BookChrgnStsFb_Fail': 2, 'BookChrgnStsFb_Finished': 3}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvBattUDynMinLim:
        sig_name = "HvBattUDynMinLim"
        sig_start_bit = 26
        update_id_bit = 27
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2044
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 26
        bmuws_info = [(3, 0b00000111, 0b11111000, 3, 0), (4, 0b11111111, 0b00000000, 8, 0)]


class EgsmPropulsionCANNmFr:
    msg_name = "EgsmPropulsionCANNmFr"
    msg_id = 1302
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr08:
    msg_name = "VddmPropFr08"
    msg_id = 65
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'MGM', 'IEM']
    sig_group_dict = {'PtTqAtAxleMaxReq': ['PtTqAtAxleMaxReqChks', 'PtTqAtAxleMaxReqCntr', 'PtTqAtAxleMaxReqPtTqAtAxleFrntReq', 'PtTqAtAxleMaxReqPtTqAtAxleReReq']}
    sig_group_dataid_dict = {'PtTqAtAxleMaxReq': 1109}

    class PtTqAtAxleMaxReqPtTqAtAxleReReq:
        sig_name = "PtTqAtAxleMaxReqPtTqAtAxleReReq"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 20000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class BrkTqAtWhlsReq:
        sig_name = "BrkTqAtWhlsReq"
        sig_start_bit = 7
        update_id_bit = 11
        sig_length = 12
        sig_value_factor = 4.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]

    class PtTqAtAxleMaxReqPtTqAtAxleFrntReq:
        sig_name = "PtTqAtAxleMaxReqPtTqAtAxleFrntReq"
        sig_start_bit = 39
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 20000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtAxleMaxReq_UB:
        sig_name = "PtTqAtAxleMaxReq_UB"
        sig_start_bit = 20
        update_id_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PtTqAtAxleMaxReqChks:
        sig_name = "PtTqAtAxleMaxReqChks"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PtTqAtAxleMaxReqCntr:
        sig_name = "PtTqAtAxleMaxReqCntr"
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


class BecmPropFr20:
    msg_name = "BecmPropFr20"
    msg_id = 325
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattOverDchaFlg:
        sig_name = "HvBattOverDchaFlg"
        sig_start_bit = 34
        update_id_bit = 33
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
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CellUMaxLim:
        sig_name = "CellUMaxLim"
        sig_start_bit = 31
        update_id_bit = 10
        sig_length = 13
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111000, 0b00000111, 5, 3)]

    class CellUMax:
        sig_name = "CellUMax"
        sig_start_bit = 7
        update_id_bit = 8
        sig_length = 13
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class CellUMaxId:
        sig_name = "CellUMaxId"
        sig_start_bit = 23
        update_id_bit = 9
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
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

    class CellUMin:
        sig_name = "CellUMin"
        sig_start_bit = 47
        update_id_bit = 32
        sig_length = 13
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111000, 0b00000111, 5, 3)]

    class CellUMinId:
        sig_name = "CellUMinId"
        sig_start_bit = 63
        update_id_bit = 48
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
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


class EcmPropFr06:
    msg_name = "EcmPropFr06"
    msg_id = 816
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.26
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvCooltHeatrStsSig:
        sig_name = "HvCooltHeatrStsSig"
        sig_start_bit = 15
        update_id_bit = 12
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCooltHeatrSts_Off': 0, 'HvCooltHeatrSts_LockedUntilNextStart': 1, 'HvCooltHeatrSts_LockedUntilService': 2, 'HvCooltHeatrSts_LockedPermanent': 3, 'HvCooltHeatrSts_Operation': 4, 'HvCooltHeatrSts_Reserved1': 5, 'HvCooltHeatrSts_Reserved2': 6, 'HvCooltHeatrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HvCooltWtrHeatrWtrTInOutl:
        sig_name = "HvCooltWtrHeatrWtrTInOutl"
        sig_start_bit = 7
        update_id_bit = 11
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattHeatgPwrPreEstimd:
        sig_name = "HvBattHeatgPwrPreEstimd"
        sig_start_bit = 10
        update_id_bit = 16
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 10
        bmuws_info = [(1, 0b00000111, 0b11111000, 3, 0), (2, 0b11111110, 0b00000001, 7, 1)]


class EvccToVddmPropDiagRespFrame:
    msg_name = "EvccToVddmPropDiagRespFrame"
    msg_id = 1588
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr29:
    msg_name = "BecmPropFr29"
    msg_id = 1161
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.9
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM']
    sig_group_dict = {'HvBattThermInfoInFuture': ['HvBattThermInfoInFuturePwrAtTime', 'HvBattThermInfoInFutureSequenceNo', 'HvBattThermInfoInFutureTempAtTime', 'HvBattThermInfoInFutureThermModAtTime', 'HvBattThermInfoInFutureTime', 'HvBattThermInfoInFutureVersionNo']}
    sig_group_dataid_dict = {}

    class HvBattThermInfoInFutureTime:
        sig_name = "HvBattThermInfoInFutureTime"
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

    class HvBattThermInfoInFuture_UB:
        sig_name = "HvBattThermInfoInFuture_UB"
        sig_start_bit = 5
        update_id_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvBattThermInfoInFuturePwrAtTime:
        sig_name = "HvBattThermInfoInFuturePwrAtTime"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 50
        sig_value_offset = -25000.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class HvBattThermInfoInFutureTempAtTime:
        sig_name = "HvBattThermInfoInFutureTempAtTime"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattThermInfoInFutureThermModAtTime:
        sig_name = "HvBattThermInfoInFutureThermModAtTime"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Idle': 0, 'ThermalBalancing': 1, 'PassiveHeating': 2, 'ActiveHeating': 3, 'PassiveCooling': 4, 'ActiveCooling': 5, 'CombinedCooling': 6, 'Reserved': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HvBattThermInfoInFutureVersionNo:
        sig_name = "HvBattThermInfoInFutureVersionNo"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class HvBattThermInfoInFutureSequenceNo:
        sig_name = "HvBattThermInfoInFutureSequenceNo"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0


class VddmToIemPropDiagReqFrame:
    msg_name = "VddmToIemPropDiagReqFrame"
    msg_id = 1847
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['IEM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VgmToHvcmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToHvcmJ1979OBDPropCanReqFrame11"
    msg_id = 2021
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['HVCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IemPropulsionCANNmFr:
    msg_name = "IemPropulsionCANNmFr"
    msg_id = 1308
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['EGSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BgmPropulsionFr06:
    msg_name = "BgmPropulsionFr06"
    msg_id = 389
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['BECM1', 'CCM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class TqModReq:
        sig_name = "TqModReq"
        sig_start_bit = 7
        update_id_bit = 15
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
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class TrackModSwt:
        sig_name = "TrackModSwt"
        sig_start_bit = 3
        update_id_bit = 14
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class IemPropFr08:
    msg_name = "IemPropFr08"
    msg_id = 99
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['ECM', 'VDDM', 'S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WhlMotSysSpdAct800:
        sig_name = "WhlMotSysSpdAct800"
        sig_start_bit = 39
        update_id_bit = 17
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotSysUDc800:
        sig_name = "WhlMotSysUDc800"
        sig_start_bit = 55
        update_id_bit = 16
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11110000, 0b00001111, 4, 4)]

    class WhlMotSysIdc:
        sig_name = "WhlMotSysIdc"
        sig_start_bit = 5
        update_id_bit = 6
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
        startbit = 5
        bmuws_info = [(0, 0b00111111, 0b11000000, 6, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class WhlMotSysHeatPwrAct:
        sig_name = "WhlMotSysHeatPwrAct"
        sig_start_bit = 31
        update_id_bit = 19
        sig_length = 8
        sig_value_factor = 50
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


class SrsToVgmISO26021PropDiagResFrame11:
    msg_name = "SrsToVgmISO26021PropDiagResFrame11"
    msg_id = 2041
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropDevFr03:
    msg_name = "BecmPropDevFr03"
    msg_id = 1488
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['CCM']
    sig_group_dict = {'BECMdevelpsignalgroup3': ['BECMdevelpsignalgroup3Functiondevpsignalgroup1', 'BECMdevelpsignalgroup3Functiondevpsignalgroup2', 'BECMdevelpsignalgroup3Functiondevpsignalgroup3', 'BECMdevelpsignalgroup3Functiondevpsignalgroup4', 'BECMdevelpsignalgroup3Functiondevpsignalgroup5', 'BECMdevelpsignalgroup3Functiondevpsignalgroup6', 'BECMdevelpsignalgroup3Functiondevpsignalgroup7', 'BECMdevelpsignalgroup3Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class BECMdevelpsignalgroup3Functiondevpsignalgroup4:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup3Functiondevpsignalgroup3:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup3"
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

    class BECMdevelpsignalgroup3Functiondevpsignalgroup2:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup3Functiondevpsignalgroup5:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup5"
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

    class BECMdevelpsignalgroup3Functiondevpsignalgroup6:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup3Functiondevpsignalgroup1:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup1"
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

    class BECMdevelpsignalgroup3Functiondevpsignalgroup8:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BECMdevelpsignalgroup3Functiondevpsignalgroup7:
        sig_name = "BECMdevelpsignalgroup3Functiondevpsignalgroup7"
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


class IgmMgmPropFr03:
    msg_name = "IgmMgmPropFr03"
    msg_id = 314
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "MGM"
    rx_nodes = ['BECM1', 'ECM', 'VDDM']
    sig_group_dict = {'IsgTqAvl': ['IsgTqAvlMax', 'IsgTqAvlMin']}
    sig_group_dataid_dict = {}

    class IsgIDc:
        sig_name = "IsgIDc"
        sig_start_bit = 53
        update_id_bit = 54
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
        startbit = 53
        bmuws_info = [(6, 0b00111111, 0b11000000, 6, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class IsgTqAvlMax:
        sig_name = "IsgTqAvlMax"
        sig_start_bit = 7
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111100, 0b00000011, 6, 2)]

    class IsgTqAvl_UB:
        sig_name = "IsgTqAvl_UB"
        sig_start_bit = 25
        update_id_bit = 25
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
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class IsgMotT:
        sig_name = "IsgMotT"
        sig_start_bit = 39
        update_id_bit = 24
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IsgTqAvlMin:
        sig_name = "IsgTqAvlMin"
        sig_start_bit = 23
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111100, 0b00000011, 6, 2)]

    class IsgCooltT:
        sig_name = "IsgCooltT"
        sig_start_bit = 47
        update_id_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EcmPropFr25:
    msg_name = "EcmPropFr25"
    msg_id = 634
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DChrgTarValLnr:
        sig_name = "DChrgTarValLnr"
        sig_start_bit = 34
        update_id_bit = 38
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DrvgCyc:
        sig_name = "DrvgCyc"
        sig_start_bit = 5
        update_id_bit = 4
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ResdEgyOfDischrgn:
        sig_name = "ResdEgyOfDischrgn"
        sig_start_bit = 15
        update_id_bit = 39
        sig_length = 13
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]


class VgmPropFr01:
    msg_name = "VgmPropFr01"
    msg_id = 786
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class OnBdDiagLostCom:
        sig_name = "OnBdDiagLostCom"
        sig_start_bit = 6
        update_id_bit = 7
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
        startbit = 6
        byte = 0
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3


class SrsPropFr02:
    msg_name = "SrsPropFr02"
    msg_id = 53
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['BECM1', 'IEM', 'MGM', 'ECM']
    sig_group_dict = {'CrashStsSafe': ['CrashStsSafeChks', 'CrashStsSafeCntr', 'CrashStsSafeSts']}
    sig_group_dataid_dict = {'CrashStsSafe': 1035}

    class CrashStsSafeCntr:
        sig_name = "CrashStsSafeCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CrashStsSafe_UB:
        sig_name = "CrashStsSafe_UB"
        sig_start_bit = 5
        update_id_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CrashStsSafeChks:
        sig_name = "CrashStsSafeChks"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CrashStsSafeSts:
        sig_name = "CrashStsSafeSts"
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
        sig_value_table = {'CrashSts2_NoCrash': 0, 'CrashSts2_Crash': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class VddmPropFr38:
    msg_name = "VddmPropFr38"
    msg_id = 819
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1']
    sig_group_dict = {'UTCTiFromEth': ['UTCTiFromEthDataValid', 'UTCTiFromEthDay', 'UTCTiFromEthHr1', 'UTCTiFromEthMins1', 'UTCTiFromEthMth1', 'UTCTiFromEthSec1', 'UTCTiFromEthYr1']}
    sig_group_dataid_dict = {}

    class UTCTiFromEthMth1:
        sig_name = "UTCTiFromEthMth1"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class GpsStatus:
        sig_name = "GpsStatus"
        sig_start_bit = 43
        update_id_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class UTCTiFromEthSec1:
        sig_name = "UTCTiFromEthSec1"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class UTCTiFromEthDataValid:
        sig_name = "UTCTiFromEthDataValid"
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
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class UTCTiFromEthYr1:
        sig_name = "UTCTiFromEthYr1"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class UTCTiFromEth_UB:
        sig_name = "UTCTiFromEth_UB"
        sig_start_bit = 6
        update_id_bit = 6
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class UTCTiFromEthHr1:
        sig_name = "UTCTiFromEthHr1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class UTCTiFromEthMins1:
        sig_name = "UTCTiFromEthMins1"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class UTCTiFromEthDay:
        sig_name = "UTCTiFromEthDay"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0


class EvccPropFr03:
    msg_name = "EvccPropFr03"
    msg_id = 1152
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {'EVCCDataEvt': ['EVCCDataEvtByte0', 'EVCCDataEvtByte1', 'EVCCDataEvtByte2', 'EVCCDataEvtByte3', 'EVCCDataEvtByte4', 'EVCCDataEvtByte5', 'EVCCDataEvtByte6', 'EVCCDataEvtByte7']}
    sig_group_dataid_dict = {}

    class EVCCDataEvtByte1:
        sig_name = "EVCCDataEvtByte1"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EVCCDataEvtByte7:
        sig_name = "EVCCDataEvtByte7"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EVCCDataEvtByte0:
        sig_name = "EVCCDataEvtByte0"
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

    class EVCCDataEvtByte3:
        sig_name = "EVCCDataEvtByte3"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EVCCDataEvtByte6:
        sig_name = "EVCCDataEvtByte6"
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

    class EVCCDataEvtByte2:
        sig_name = "EVCCDataEvtByte2"
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

    class EVCCDataEvtByte4:
        sig_name = "EVCCDataEvtByte4"
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

    class EVCCDataEvtByte5:
        sig_name = "EVCCDataEvtByte5"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class SrsEtcPropDevFr01:
    msg_name = "SrsEtcPropDevFr01"
    msg_id = 1456
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SRS"
    rx_nodes = ['CCM']
    sig_group_dict = {'SRSdevelpsignalgroupTX': ['SRSdevelpsignalgroupTXFunctiondevpsignalgroup1', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup2', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup3', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup4', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup5', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup6', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup7', 'SRSdevelpsignalgroupTXFunctiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup7:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup7"
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

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup4:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup6:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup2:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup3:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup3"
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

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup1:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup1"
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

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup8:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SRSdevelpsignalgroupTXFunctiondevpsignalgroup5:
        sig_name = "SRSdevelpsignalgroupTXFunctiondevpsignalgroup5"
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


class BecmPropFr18:
    msg_name = "BecmPropFr18"
    msg_id = 838
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattCooltLvl:
        sig_name = "HvBattCooltLvl"
        sig_start_bit = 36
        update_id_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattCooltLvl_Full': 0, 'HvBattCooltLvl_Empty': 1}
        compute_method = None
        length = 1
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvBattVoltMinSerlNr:
        sig_name = "HvBattVoltMinSerlNr"
        sig_start_bit = 31
        update_id_bit = 38
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattHeatgPwr:
        sig_name = "HvBattHeatgPwr"
        sig_start_bit = 47
        update_id_bit = 35
        sig_length = 11
        sig_value_factor = 100.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class HvBattVoltMaxSerlNr:
        sig_name = "HvBattVoltMaxSerlNr"
        sig_start_bit = 23
        update_id_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattCooltOutletT:
        sig_name = "HvBattCooltOutletT"
        sig_start_bit = 7
        update_id_bit = 12
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -60.0
        sig_value_min = 0
        sig_value_max = 1850
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11100000, 0b00011111, 3, 5)]


class CddIgmPropFr05:
    msg_name = "CddIgmPropFr05"
    msg_id = 1109
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "HVCM"
    rx_nodes = ['CCM', 'ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class DischargeEfficiency:
        sig_name = "DischargeEfficiency"
        sig_start_bit = 15
        update_id_bit = 8
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 15
        byte = 1
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class DcDcMinCooltFlow:
        sig_name = "DcDcMinCooltFlow"
        sig_start_bit = 7
        update_id_bit = 0
        sig_length = 7
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 127
        sig_byteorder = "Motorola"
        sig_value_init = 20
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 7
        byte = 0
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1

    class TDcDcCoolt:
        sig_name = "TDcDcCoolt"
        sig_start_bit = 31
        update_id_bit = 16
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class EtctoEcmXCPFr01:
    msg_name = "EtctoEcmXCPFr01"
    msg_id = 1412
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmPropComFr12:
    msg_name = "EcmPropComFr12"
    msg_id = 259
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class BookChrgTarValLnr:
        sig_name = "BookChrgTarValLnr"
        sig_start_bit = 31
        update_id_bit = 5
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 2000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]


class BecmPropFr21:
    msg_name = "BecmPropFr21"
    msg_id = 648
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class FastChrgnLEDIndctn:
        sig_name = "FastChrgnLEDIndctn"
        sig_start_bit = 35
        update_id_bit = 41
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FastChrgnLEDIndctn_Default': 0, 'FastChrgnLEDIndctn_Green1': 1, 'FastChrgnLEDIndctn_Green2': 2, 'FastChrgnLEDIndctn_Green3': 3, 'FastChrgnLEDIndctn_Green4': 4, 'FastChrgnLEDIndctn_Red': 5, 'FastChrgnLEDIndctn_Green5': 6, 'FastChrgnLEDIndctn_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 35
        byte = 4
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class HvBattWMDSts:
        sig_name = "HvBattWMDSts"
        sig_start_bit = 55
        update_id_bit = 49
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
        startbit = 55
        byte = 6
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class DCChrgSt:
        sig_name = "DCChrgSt"
        sig_start_bit = 39
        update_id_bit = 20
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DCChrgrSts_Idle': 0, 'DCChrgrSts_Prestart': 1, 'DCChrgrSts_Charging': 2, 'DCChrgrSts_DCChrgnFltVehSide': 3, 'DCChrgrSts_DCChrgnFltChrgrSideTempFlt': 4, 'DCChrgrSts_DCChrgnFltChrgrSideConnectFlt': 5, 'DCChrgrSts_DCChrgnFltChrgrSideOtherFlt': 6, 'DCChrgrSts_DCChrgnFltChrgrSideEmgyFlt': 7, 'DCChrgrSts_DCChrgnFltChrgrSideComFlt': 8, 'DCChrgrSts_Bookcharging': 9, 'DCChrgrSts_Shuntdown': 10, 'DCChrgrSts_Heating': 11, 'DCChrgrSts_Supercharging': 12, 'DCChrgrSts_SuperchargingEnd': 13}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HvIsoR:
        sig_name = "HvIsoR"
        sig_start_bit = 7
        update_id_bit = 23
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 60000
        sig_byteorder = "Motorola"
        sig_value_init = 5000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvBattChrgnTiEstimd:
        sig_name = "HvBattChrgnTiEstimd"
        sig_start_bit = 18
        update_id_bit = 19
        sig_length = 11
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 2047
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class VddmToVgmJ1979OBDPropDiagResFrame11:
    msg_name = "VddmToVgmJ1979OBDPropDiagResFrame11"
    msg_id = 2030
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VddmPropFr29:
    msg_name = "VddmPropFr29"
    msg_id = 49
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'AccrOvrdnAllwdForAutDrv': ['AccrOvrdnAllwdForAutDrvChks', 'AccrOvrdnAllwdForAutDrvCntr', 'AccrOvrdnAllwdForAutDrvYesNo1']}
    sig_group_dataid_dict = {}

    class AccrOvrdnAllwdForAutDrvCntr:
        sig_name = "AccrOvrdnAllwdForAutDrvCntr"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class AccrOvrdnAllwdForAutDrvYesNo1:
        sig_name = "AccrOvrdnAllwdForAutDrvYesNo1"
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
        sig_value_table = {'YesNo1_Yes': 0, 'YesNo1_No': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AccrOvrdnAllwdForAutDrvChks:
        sig_name = "AccrOvrdnAllwdForAutDrvChks"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AccrOvrdnAllwdForAutDrv_UB:
        sig_name = "AccrOvrdnAllwdForAutDrv_UB"
        sig_start_bit = 53
        update_id_bit = 53
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
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class VddmPropFr12:
    msg_name = "VddmPropFr12"
    msg_id = 353
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class V2XDchaSwt:
        sig_name = "V2XDchaSwt"
        sig_start_bit = 54
        update_id_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DisChrgrSW_Off': 0, 'DisChrgrSW_V2V': 1, 'DisChrgrSW_V2L': 2}
        compute_method = None
        length = 2
        startbit = 54
        byte = 6
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5


class EgsmPropDvelFr01:
    msg_name = "EgsmPropDvelFr01"
    msg_id = 1092
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['CCM']
    sig_group_dict = {'EGSMdevelpsignalgroup1': ['EGSMdevelpsignalgroup1Functiondevpsignalgroup1', 'EGSMdevelpsignalgroup1Functiondevpsignalgroup2', 'EGSMdevelpsignalgroup1Functiondevpsignalgroup3', 'EGSMdevelpsignalgroup1Functiondevpsignalgroup4', 'EGSMdevelpsignalgroup1Functiondevpsignalgroup5', 'EGSMdevelpsignalgroup1Functiondevpsignalgroup6', 'EGSMdevelpsignalgroup1Functiondevpsignalgroup7', 'EGSMdevelpsignalgroup1Functiondevpsignalgroup8']}
    sig_group_dataid_dict = {}

    class EGSMdevelpsignalgroup1Functiondevpsignalgroup2:
        sig_name = "EGSMdevelpsignalgroup1Functiondevpsignalgroup2"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EGSMdevelpsignalgroup1Functiondevpsignalgroup8:
        sig_name = "EGSMdevelpsignalgroup1Functiondevpsignalgroup8"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EGSMdevelpsignalgroup1Functiondevpsignalgroup3:
        sig_name = "EGSMdevelpsignalgroup1Functiondevpsignalgroup3"
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

    class EGSMdevelpsignalgroup1Functiondevpsignalgroup5:
        sig_name = "EGSMdevelpsignalgroup1Functiondevpsignalgroup5"
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

    class EGSMdevelpsignalgroup1Functiondevpsignalgroup6:
        sig_name = "EGSMdevelpsignalgroup1Functiondevpsignalgroup6"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EGSMdevelpsignalgroup1Functiondevpsignalgroup4:
        sig_name = "EGSMdevelpsignalgroup1Functiondevpsignalgroup4"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class EGSMdevelpsignalgroup1Functiondevpsignalgroup1:
        sig_name = "EGSMdevelpsignalgroup1Functiondevpsignalgroup1"
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

    class EGSMdevelpsignalgroup1Functiondevpsignalgroup7:
        sig_name = "EGSMdevelpsignalgroup1Functiondevpsignalgroup7"
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


class CddObcPropFr04:
    msg_name = "CddObcPropFr04"
    msg_id = 1041
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class OnBdChrgrTLLCPri:
        sig_name = "OnBdChrgrTLLCPri"
        sig_start_bit = 23
        update_id_bit = 25
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class OnBdChrgrTTabSec:
        sig_name = "OnBdChrgrTTabSec"
        sig_start_bit = 55
        update_id_bit = 24
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class LimnIndcnOBC:
        sig_name = "LimnIndcnOBC"
        sig_start_bit = 39
        update_id_bit = 26
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class VddmPropFr16:
    msg_name = "VddmPropFr16"
    msg_id = 597
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['IEM']
    sig_group_dict = {'ImobEngMgrReq2': ['ImobEngMgrReq2ImobEngDataMgrReq0', 'ImobEngMgrReq2ImobEngDataMgrReq1', 'ImobEngMgrReq2ImobEngDataMgrReq2', 'ImobEngMgrReq2ImobEngDataMgrReq3', 'ImobEngMgrReq2ImobEngDataMgrReq4', 'ImobEngMgrReq2ImobEngDataMgrReq5', 'ImobEngMgrReq2ImobEngDataMgrReq6', 'ImobEngMgrReq2ImobEngMgrCmdTar1']}
    sig_group_dataid_dict = {}

    class ImobEngMgrReq2ImobEngDataMgrReq2:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq2"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq2ImobEngDataMgrReq1:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq1"
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

    class ImobEngMgrReq2ImobEngDataMgrReq0:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq0"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq2ImobEngDataMgrReq5:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq5"
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

    class ImobEngMgrReq2ImobEngDataMgrReq4:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq4"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq2ImobEngDataMgrReq6:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq6"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngMgrReq2ImobEngMgrCmdTar1:
        sig_name = "ImobEngMgrReq2ImobEngMgrCmdTar1"
        sig_start_bit = 1
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ImobEngMgrReqCmd_ImobEngCmdTarIdle': 0, 'ImobEngMgrReqCmd_ImobEngMtnStrtReqCmd': 1, 'ImobEngMgrReqCmd_ImobEngNoMtnStrtReqCmd': 2, 'ImobEngMgrReqCmd_ImobEngTurnOffCmd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ImobEngMgrReq2ImobEngDataMgrReq3:
        sig_name = "ImobEngMgrReq2ImobEngDataMgrReq3"
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

    class ImobEngMgrReq2_UB:
        sig_name = "ImobEngMgrReq2_UB"
        sig_start_bit = 2
        update_id_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class EcmPropFr02:
    msg_name = "EcmPropFr02"
    msg_id = 102
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['IEM', 'CCM', 'VDDM', 'S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class RollAgValPrpsn:
        sig_name = "RollAgValPrpsn"
        sig_start_bit = 46
        update_id_bit = 0
        sig_length = 16
        sig_value_factor = 3.0518e-05
        sig_value_offset = 0.0
        sig_value_min = -32767
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 46
        bmuws_info = [(5, 0b01111111, 0b10000000, 7, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b10000000, 0b01111111, 1, 7)]

    class WhlMotSysModReq:
        sig_name = "WhlMotSysModReq"
        sig_start_bit = 58
        update_id_bit = 59
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysModStsTyp1_Inin': 0, 'WhlMotSysModStsTyp1_Stb': 1, 'WhlMotSysModStsTyp1_TqCtrl': 2, 'WhlMotSysModStsTyp1_SpdCtrlIdle': 3, 'WhlMotSysModStsTyp1_CluOper': 4, 'WhlMotSysModStsTyp1_PreChrg': 5, 'WhlMotSysModStsTyp1_PwrDwn': 6, 'WhlMotSysModStsTyp1_Flt': 7}
        compute_method = None
        length = 3
        startbit = 58
        byte = 7
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class CrpTqAct:
        sig_name = "CrpTqAct"
        sig_start_bit = 15
        update_id_bit = 31
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -20000
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class RoadSlopPrpsn:
        sig_name = "RoadSlopPrpsn"
        sig_start_bit = 30
        update_id_bit = 1
        sig_length = 16
        sig_value_factor = 3.0518e-05
        sig_value_offset = 0.0
        sig_value_min = -32767
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 30
        bmuws_info = [(3, 0b01111111, 0b10000000, 7, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b10000000, 0b01111111, 1, 7)]

    class WhlMotSysModReq800:
        sig_name = "WhlMotSysModReq800"
        sig_start_bit = 7
        update_id_bit = 2
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WhlMotSysModStsTyp2_Inin': 0, 'WhlMotSysModStsTyp2_Stb': 1, 'WhlMotSysModStsTyp2_TqCtrl': 2, 'WhlMotSysModStsTyp2_SpdCtrlIdle': 3, 'WhlMotSysModStsTyp2_CluOper': 4, 'WhlMotSysModStsTyp2_PreChrg': 5, 'WhlMotSysModStsTyp2_PwrDwn': 6, 'WhlMotSysModStsTyp2_Flt': 7, 'WhlMotSysModStsTyp2_TcsCtrl': 8}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class BecmPropulsionCANNmFr:
    msg_name = "BecmPropulsionCANNmFr"
    msg_id = 1305
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EgsmToVddmPropDiagRespFrame:
    msg_name = "EgsmToVddmPropDiagRespFrame"
    msg_id = 1587
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "EGSM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class BecmPropFr34:
    msg_name = "BecmPropFr34"
    msg_id = 552
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['S2SReceiver']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattULim800:
        sig_name = "HvBattULim800"
        sig_start_bit = 11
        update_id_bit = 24
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 11
        bmuws_info = [(1, 0b00001111, 0b11110000, 4, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class HvBattUDynMinLim800:
        sig_name = "HvBattUDynMinLim800"
        sig_start_bit = 7
        update_id_bit = 25
        sig_length = 12
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]


class EcmPropFr28:
    msg_name = "EcmPropFr28"
    msg_id = 401
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['MGM', 'IEM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class RearHeatModEnad:
        sig_name = "RearHeatModEnad"
        sig_start_bit = 11
        update_id_bit = 14
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FrntHeatModEnad_Heatg': 0, 'FrntHeatModEnad_PwrLoss': 1, 'FrntHeatModEnad_Off': 2, 'FrntHeatModEnad_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class RearHeatPwrAllwd:
        sig_name = "RearHeatPwrAllwd"
        sig_start_bit = 23
        update_id_bit = 15
        sig_length = 8
        sig_value_factor = 50
        sig_value_offset = 0
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

    class FrntHeatPwrAllwd:
        sig_name = "FrntHeatPwrAllwd"
        sig_start_bit = 7
        update_id_bit = 13
        sig_length = 8
        sig_value_factor = 50
        sig_value_offset = 0
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

    class FrntHeatModEnad:
        sig_name = "FrntHeatModEnad"
        sig_start_bit = 9
        update_id_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FrntHeatModEnad_Heatg': 0, 'FrntHeatModEnad_PwrLoss': 1, 'FrntHeatModEnad_Off': 2, 'FrntHeatModEnad_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class VddmPropFr11:
    msg_name = "VddmPropFr11"
    msg_id = 313
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['BECM1', 'ECM', 'IEM']
    sig_group_dict = {'LockgCenSts': ['LockgCenStsLockSt', 'LockgCenStsTrigSrc', 'LockgCenStsUpdEve'], 'BrkFricTqTotAtWhlsAct': ['BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct', 'BrkFricTqTotAtWhlsActChks', 'BrkFricTqTotAtWhlsActCntr']}
    sig_group_dataid_dict = {'BrkFricTqTotAtWhlsAct': 123}

    class YawStabyCtrlActv:
        sig_name = "YawStabyCtrlActv"
        sig_start_bit = 27
        update_id_bit = 26
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CtrlSts1_NoCtrl': 0, 'CtrlSts1_InCtrl': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class LockgCenStsTrigSrc:
        sig_name = "LockgCenStsTrigSrc"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 12
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockTrigSrc2_NoTrigSrc': 0, 'LockTrigSrc2_KeyRem': 1, 'LockTrigSrc2_Keyls': 2, 'LockTrigSrc2_IntrSwt': 3, 'LockTrigSrc2_SpdAut': 4, 'LockTrigSrc2_TmrAut': 5, 'LockTrigSrc2_Slam': 6, 'LockTrigSrc2_Telm': 7, 'LockTrigSrc2_Crash': 8, 'LockTrigSrc2_Apprch': 9, 'LockTrigSrc2_OutsOth': 10, 'LockTrigSrc2_InsOth': 11, 'Locktrigsrc2_NFC': 12}
        compute_method = None
        length = 4
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class SpdRotlForWhlsAtAxleRe:
        sig_name = "SpdRotlForWhlsAtAxleRe"
        sig_start_bit = 38
        update_id_bit = 39
        sig_length = 15
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class LockgCenSts_UB:
        sig_name = "LockgCenSts_UB"
        sig_start_bit = 48
        update_id_bit = 48
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
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BrkFricTqTotAtWhlsActChks:
        sig_name = "BrkFricTqTotAtWhlsActChks"
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

    class LockgCenStsUpdEve:
        sig_name = "LockgCenStsUpdEve"
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

    class BrkFricTqTotAtWhlsAct_UB:
        sig_name = "BrkFricTqTotAtWhlsAct_UB"
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

    class BrkFricTqTotAtWhlsActCntr:
        sig_name = "BrkFricTqTotAtWhlsActCntr"
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

    class LockgCenStsLockSt:
        sig_name = "LockgCenStsLockSt"
        sig_start_bit = 51
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSt3_LockUndefd': 0, 'LockSt3_LockUnlckd': 1, 'LockSt3_LockTrUnlckd': 2, 'LockSt3_LockLockd': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct:
        sig_name = "BrkFricTqTotAtWhlsActBrkFricTqTotAtWhlsAct"
        sig_start_bit = 6
        update_id_bit = None
        sig_length = 15
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 20000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class VddmToEcmPropDiagReqFrame:
    msg_name = "VddmToEcmPropDiagReqFrame"
    msg_id = 1840
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmPropFr22:
    msg_name = "EcmPropFr22"
    msg_id = 392
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BECM1', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattChrgnPwrAllwd1:
        sig_name = "HvBattChrgnPwrAllwd1"
        sig_start_bit = 7
        update_id_bit = 10
        sig_length = 13
        sig_value_factor = 20
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class HvBattThermReqFb:
        sig_name = "HvBattThermReqFb"
        sig_start_bit = 47
        update_id_bit = 37
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattThermReqFb_Default': 0, 'HvBattThermReqFb_Heating': 1, 'HvBattThermReqFb_HeatFinished': 2, 'HvBattThermReqFb_RadiatorCooling': 3, 'HvBattThermReqFb_CompressorCooling': 4, 'HvBattThermReqFb_CoolingFinish': 5, 'HvBattThermReqFb_Inhibited': 6, 'HvBattThermReqFb_HeatingByEmotCoolt': 7, 'HvBattThermReqFb_Fault': 8}
        compute_method = None
        length = 4
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HvBattFlwEstmd:
        sig_name = "HvBattFlwEstmd"
        sig_start_bit = 40
        update_id_bit = 43
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 40
        bmuws_info = [(5, 0b00000001, 0b11111110, 1, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class DchaPwrAllwd:
        sig_name = "DchaPwrAllwd"
        sig_start_bit = 9
        update_id_bit = 35
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class BecmPropFr04:
    msg_name = "BecmPropFr04"
    msg_id = 659
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['ECM', 'VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattErrIndcnReq:
        sig_name = "HvBattErrIndcnReq"
        sig_start_bit = 21
        update_id_bit = 22
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
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvBattSocLimHi:
        sig_name = "HvBattSocLimHi"
        sig_start_bit = 42
        update_id_bit = 43
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 42
        bmuws_info = [(5, 0b00000111, 0b11111000, 3, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class HvBattHeatgReq:
        sig_name = "HvBattHeatgReq"
        sig_start_bit = 7
        update_id_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattCoolgReq_NotReqd': 0, 'HvBattCoolgReq_LoReq': 1, 'HvBattCoolgReq_MedReq': 2, 'HvBattCoolgReq_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattSocLimLo:
        sig_name = "HvBattSocLimLo"
        sig_start_bit = 39
        update_id_bit = 44
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11100000, 0b00011111, 3, 5)]

    class HvBattSocLimMax:
        sig_name = "HvBattSocLimMax"
        sig_start_bit = 18
        update_id_bit = 19
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvBattSocLimMin:
        sig_name = "HvBattSocLimMin"
        sig_start_bit = 2
        update_id_bit = 23
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvBattEgyCdn:
        sig_name = "HvBattEgyCdn"
        sig_start_bit = 63
        update_id_bit = 20
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 200
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


class IemPropFr04:
    msg_name = "IemPropFr04"
    msg_id = 613
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "IEM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'ImobEngChk2': ['ImobEngChk2ImobEngChkSts', 'ImobEngChk2ImobEngDataChk0', 'ImobEngChk2ImobEngDataChk1', 'ImobEngChk2ImobEngDataChk2', 'ImobEngChk2ImobEngDataChk3', 'ImobEngChk2ImobEngDataChk4', 'ImobEngChk2ImobEngDataChk5', 'ImobEngChk2ImobEngDataChk6']}
    sig_group_dataid_dict = {}

    class ImobEngChk2ImobEngDataChk6:
        sig_name = "ImobEngChk2ImobEngDataChk6"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk2ImobEngDataChk1:
        sig_name = "ImobEngChk2ImobEngDataChk1"
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

    class ImobEngChk2ImobEngChkSts:
        sig_name = "ImobEngChk2ImobEngChkSts"
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
        sig_value_table = {'AvlSts2_NotAvl': 0, 'AvlSts2_Avl': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class ImobEngChk2ImobEngDataChk2:
        sig_name = "ImobEngChk2ImobEngDataChk2"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk2_UB:
        sig_name = "ImobEngChk2_UB"
        sig_start_bit = 1
        update_id_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ImobEngChk2ImobEngDataChk0:
        sig_name = "ImobEngChk2ImobEngDataChk0"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk2ImobEngDataChk4:
        sig_name = "ImobEngChk2ImobEngDataChk4"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class ImobEngChk2ImobEngDataChk3:
        sig_name = "ImobEngChk2ImobEngDataChk3"
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

    class ImobEngChk2ImobEngDataChk5:
        sig_name = "ImobEngChk2ImobEngDataChk5"
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


class VddmPropdTCFr38:
    msg_name = "VddmPropdTCFr38"
    msg_id = 282
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['MGM', 'IEM']
    sig_group_dict = {'StcStsToDmc': ['StcStsToDmcChks', 'StcStsToDmcCntr', 'StcStsToDmcEngRotTarSpdDMCFrnt', 'StcStsToDmcEngRotTarSpdDMCRear', 'StcStsToDmcFrnt', 'StcStsToDmcRear']}
    sig_group_dataid_dict = {'StcStsToDmc': 6565}

    class StcStsToDmcEngRotTarSpdDMCFrnt:
        sig_name = "StcStsToDmcEngRotTarSpdDMCFrnt"
        sig_start_bit = 23
        update_id_bit = None
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class StcStsToDmcEngRotTarSpdDMCRear:
        sig_name = "StcStsToDmcEngRotTarSpdDMCRear"
        sig_start_bit = 39
        update_id_bit = None
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class StcStsToDmcCntr:
        sig_name = "StcStsToDmcCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class StcStsToDmcRear:
        sig_name = "StcStsToDmcRear"
        sig_start_bit = 63
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModeDMC_Off': 0, 'ModeDMC_Rpm': 1, 'ModeDMC_Trq': 2}
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class StcStsToDmc_UB:
        sig_name = "StcStsToDmc_UB"
        sig_start_bit = 4
        update_id_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class StcStsToDmcChks:
        sig_name = "StcStsToDmcChks"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class StcStsToDmcFrnt:
        sig_name = "StcStsToDmcFrnt"
        sig_start_bit = 55
        update_id_bit = None
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModeDMC_Off': 0, 'ModeDMC_Rpm': 1, 'ModeDMC_Trq': 2}
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VgmToVddmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToVddmJ1979OBDPropCanReqFrame11"
    msg_id = 2022
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['VDDM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class VgmToMgmJ1979OBDPropCanReqFrame11:
    msg_name = "VgmToMgmJ1979OBDPropCanReqFrame11"
    msg_id = 2020
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['MGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class EcmPropFr14:
    msg_name = "EcmPropFr14"
    msg_id = 1160
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']
    sig_group_dict = {'HvBattThermInfoCorrInFuture': ['HvBattThermInfoCorrInFuturePwrAtTime', 'HvBattThermInfoCorrInFutureSequenceNo', 'HvBattThermInfoCorrInFutureTempAtTime', 'HvBattThermInfoCorrInFutureThermModAtTime', 'HvBattThermInfoCorrInFutureTime', 'HvBattThermInfoCorrInFutureVersionNo']}
    sig_group_dataid_dict = {}

    class HvBattThermInfoCorrInFuture_UB:
        sig_name = "HvBattThermInfoCorrInFuture_UB"
        sig_start_bit = 5
        update_id_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvBattThermInfoCorrInFutureVersionNo:
        sig_name = "HvBattThermInfoCorrInFutureVersionNo"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class HvBattThermInfoCorrInFutureTempAtTime:
        sig_name = "HvBattThermInfoCorrInFutureTempAtTime"
        sig_start_bit = 31
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = -50.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 50
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvBattThermInfoCorrInFutureThermModAtTime:
        sig_name = "HvBattThermInfoCorrInFutureThermModAtTime"
        sig_start_bit = 47
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Idle': 0, 'ThermalBalancing': 1, 'PassiveHeating': 2, 'ActiveHeating': 3, 'PassiveCooling': 4, 'ActiveCooling': 5, 'CombinedCooling': 6, 'Reserved': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HvBattThermInfoCorrInFutureTime:
        sig_name = "HvBattThermInfoCorrInFutureTime"
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

    class HvBattThermInfoCorrInFuturePwrAtTime:
        sig_name = "HvBattThermInfoCorrInFuturePwrAtTime"
        sig_start_bit = 15
        update_id_bit = None
        sig_length = 16
        sig_value_factor = 50
        sig_value_offset = -25000.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 500
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class HvBattThermInfoCorrInFutureSequenceNo:
        sig_name = "HvBattThermInfoCorrInFutureSequenceNo"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0


class BecmPropFr15:
    msg_name = "BecmPropFr15"
    msg_id = 323
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BECM1"
    rx_nodes = ['MGM', 'VDDM', 'S2SReceiver', 'HVCM', 'ECM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class HvBattPreChrgReq:
        sig_name = "HvBattPreChrgReq"
        sig_start_bit = 37
        update_id_bit = 36
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HVChrgnStopReq:
        sig_name = "HVChrgnStopReq"
        sig_start_bit = 39
        update_id_bit = 56
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVChrgnStopReq_Default': 0, 'HVChrgnStopReq_BST': 1, 'HVChrgnStopReq_CST': 2, 'HVChrgnStopReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvBattPwrLimChrg1:
        sig_name = "HvBattPwrLimChrg1"
        sig_start_bit = 18
        update_id_bit = 19
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvBattPwrLimDchaSoft:
        sig_name = "HvBattPwrLimDchaSoft"
        sig_start_bit = 55
        update_id_bit = 60
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11100000, 0b00011111, 3, 5)]

    class HvBattPwrLimDcha1:
        sig_name = "HvBattPwrLimDcha1"
        sig_start_bit = 34
        update_id_bit = 20
        sig_length = 11
        sig_value_factor = 0.25
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HvBattIDc1:
        sig_name = "HvBattIDc1"
        sig_start_bit = 6
        update_id_bit = 7
        sig_length = 15
        sig_value_factor = 0.1
        sig_value_offset = -1638.0
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 16380
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class DCChrgnHndlSts:
        sig_name = "DCChrgnHndlSts"
        sig_start_bit = 23
        update_id_bit = 35
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnBdChrgrHndlSts_Disconnected': 0, 'OnBdChrgrHndlSts_ConnectedWithoutPower': 1, 'OnBdChrgrHndlSts_PowerAvailableButNotActivated': 2, 'OnBdChrgrHndlSts_ConnectedWithPower': 3, 'OnBdChrgrHndlSts_Init': 4, 'OnBdChrgrHndlSts_Fault': 5}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class VddmPropFr10:
    msg_name = "VddmPropFr10"
    msg_id = 312
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']
    sig_group_dict = {'BrkFricTqAtWhlAct': ['BrkFricTqAtWhlActBrkFricTqAtWhlFrntLeAct', 'BrkFricTqAtWhlActBrkFricTqAtWhlFrntRiAct', 'BrkFricTqAtWhlActBrkFricTqAtWhlReLeAct', 'BrkFricTqAtWhlActBrkFricTqAtWhlReRiAct']}
    sig_group_dataid_dict = {}

    class BrkFricTqAtWhlActBrkFricTqAtWhlFrntRiAct:
        sig_name = "BrkFricTqAtWhlActBrkFricTqAtWhlFrntRiAct"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class BrkFricTqAtWhlActBrkFricTqAtWhlFrntLeAct:
        sig_name = "BrkFricTqAtWhlActBrkFricTqAtWhlFrntLeAct"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class BrkFricTqAtWhlActBrkFricTqAtWhlReRiAct:
        sig_name = "BrkFricTqAtWhlActBrkFricTqAtWhlReRiAct"
        sig_start_bit = 52
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class BrkFricTqAtWhlActBrkFricTqAtWhlReLeAct:
        sig_name = "BrkFricTqAtWhlActBrkFricTqAtWhlReLeAct"
        sig_start_bit = 36
        update_id_bit = None
        sig_length = 13
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 8191
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class BrkFricTqAtWhlAct_UB:
        sig_name = "BrkFricTqAtWhlAct_UB"
        sig_start_bit = 5
        update_id_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class VddmPropulsionCANNmFr:
    msg_name = "VddmPropulsionCANNmFr"
    msg_id = 1318
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['SRS']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


