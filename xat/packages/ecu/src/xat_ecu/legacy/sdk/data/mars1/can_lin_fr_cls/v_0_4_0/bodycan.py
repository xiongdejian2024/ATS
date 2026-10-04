class CcmBodyFr53:
    msg_name = "CcmBodyFr53"
    msg_id = 1160
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig9Byte6:
        sig_name = "CcmCaliSig9Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig9Byte4:
        sig_name = "CcmCaliSig9Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig9Byte1:
        sig_name = "CcmCaliSig9Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig9Byte2:
        sig_name = "CcmCaliSig9Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig9Byte3:
        sig_name = "CcmCaliSig9Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig9Byte0:
        sig_name = "CcmCaliSig9Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig9Byte7:
        sig_name = "CcmCaliSig9Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig9Byte5:
        sig_name = "CcmCaliSig9Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CEMBodyFr15:
    msg_name = "CEMBodyFr15"
    msg_id = 384
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HmiCmptmtTSpForRowSecRi:
        sig_name = "HmiCmptmtTSpForRowSecRi"
        sig_start_bit = 28
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 15.0
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 14
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 28
        byte = 3
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class HpcHpCoolgPwrSts:
        sig_name = "HpcHpCoolgPwrSts"
        sig_start_bit = 47
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DrvrAirCdnrSetgIdPen:
        sig_name = "DrvrAirCdnrSetgIdPen"
        sig_start_bit = 63
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HmiCmptmtTSpForRowSecLe:
        sig_name = "HmiCmptmtTSpForRowSecLe"
        sig_start_bit = 20
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 15.0
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 14
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 20
        byte = 2
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class DrvrAirCdnrSetgAirCdnrSetg:
        sig_name = "DrvrAirCdnrSetgAirCdnrSetg"
        sig_start_bit = 59
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AirCdnrSetg_Normal': 0, 'AirCdnrSetg_ECO': 1, 'AirCdnrSetg_Reserved1': 2}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HpcHpModReq:
        sig_name = "HpcHpModReq"
        sig_start_bit = 38
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 21
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HeatPmpModCmd_Initialization': 0, 'HeatPmpModCmd_Mode1': 1, 'HeatPmpModCmd_Mode2': 2, 'HeatPmpModCmd_Mode3': 3, 'HeatPmpModCmd_Mode4': 4, 'HeatPmpModCmd_Mode5': 5, 'HeatPmpModCmd_Mode6': 6, 'HeatPmpModCmd_Mode7': 7, 'HeatPmpModCmd_Mode8': 8, 'HeatPmpModCmd_Mode9': 9, 'HeatPmpModCmd_Mode10': 10, 'HeatPmpModCmd_Mode11': 11, 'HeatPmpModCmd_Mode12': 12, 'HeatPmpModCmd_Mode13': 13, 'HeatPmpModCmd_Mode14': 14, 'HeatPmpModCmd_Mode15': 15, 'HeatPmpModCmd_Mode16': 16, 'HeatPmpModCmd_Mode17': 17, 'HeatPmpModCmd_Mode18': 18, 'HeatPmpModCmd_Mode19': 19, 'HeatPmpModCmd_Mode20': 20, 'HeatPmpModCmd_Reserved': 21}
        compute_method = None
        length = 7
        startbit = 38
        byte = 4
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class HmiCmptmtTSpSpclForRowSecRi:
        sig_name = "HmiCmptmtTSpSpclForRowSecRi"
        sig_start_bit = 30
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtTSpSpcl_Norm': 0, 'HmiCmptmtTSpSpcl_Lo': 1, 'HmiCmptmtTSpSpcl_Hi': 2}
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HmiCmptmtTSpSpclForRowSecLe:
        sig_name = "HmiCmptmtTSpSpclForRowSecLe"
        sig_start_bit = 22
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtTSpSpcl_Norm': 0, 'HmiCmptmtTSpSpcl_Lo': 1, 'HmiCmptmtTSpSpcl_Hi': 2}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HmiCmptmtTSpForRowFirstLe:
        sig_name = "HmiCmptmtTSpForRowFirstLe"
        sig_start_bit = 4
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 15.0
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 14
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 4
        byte = 0
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class HmiCmptmtTSpForRowFirstRi:
        sig_name = "HmiCmptmtTSpForRowFirstRi"
        sig_start_bit = 12
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 15.0
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 14
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 12
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class HmiCmptmtCoolgReq:
        sig_name = "HmiCmptmtCoolgReq"
        sig_start_bit = 52
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtCoolgReq_Off': 0, 'HmiCmptmtCoolgReq_Auto': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HmiElecAirPassSwtReq:
        sig_name = "HmiElecAirPassSwtReq"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HmiCmptmtTSpSpclForRowFirstLe:
        sig_name = "HmiCmptmtTSpSpclForRowFirstLe"
        sig_start_bit = 6
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtTSpSpcl_Norm': 0, 'HmiCmptmtTSpSpcl_Lo': 1, 'HmiCmptmtTSpSpcl_Hi': 2}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HmiElecAirDrvrSwtReq:
        sig_name = "HmiElecAirDrvrSwtReq"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class HpcHpHeatgPwrSts:
        sig_name = "HpcHpHeatgPwrSts"
        sig_start_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class HmiCmptmtTSpSpclForRowFirstRi:
        sig_name = "HmiCmptmtTSpSpclForRowFirstRi"
        sig_start_bit = 14
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtTSpSpcl_Norm': 0, 'HmiCmptmtTSpSpcl_Lo': 1, 'HmiCmptmtTSpSpcl_Hi': 2}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class HpcDeiceReq:
        sig_name = "HpcDeiceReq"
        sig_start_bit = 55
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DeiceReq_NoReq': 0, 'DeiceReq_DeiceChecking': 1, 'DeiceReq_Deicing': 2, 'DeiceReq_Reserved': 3}
        compute_method = None
        length = 3
        startbit = 55
        byte = 6
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class CcmBodyFr28:
    msg_name = "CcmBodyFr28"
    msg_id = 1168
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DrvrSeatHeatgPwrAllwd:
        sig_name = "DrvrSeatHeatgPwrAllwd"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AmbTEstimdQf:
        sig_name = "AmbTEstimdQf"
        sig_start_bit = 3
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PassSeatHeatgPwrAllwd:
        sig_name = "PassSeatHeatgPwrAllwd"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 100
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SecRowLeSeatHeatgPwrAllwd:
        sig_name = "SecRowLeSeatHeatgPwrAllwd"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 100
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AmbTEstimdAmbTEstimd:
        sig_name = "AmbTEstimdAmbTEstimd"
        sig_start_bit = 2
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-70.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class CemBodyFr107:
    msg_name = "CemBodyFr107"
    msg_id = 960
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehTiAndDataDay:
        sig_name = "VehTiAndDataDay"
        sig_start_bit = 28
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehTiAndDataHr1:
        sig_name = "VehTiAndDataHr1"
        sig_start_bit = 20
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehTiAndDataDataValid:
        sig_name = "VehTiAndDataDataValid"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class VehTiAndDataMth1:
        sig_name = "VehTiAndDataMth1"
        sig_start_bit = 35
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehTiAndDataSec1:
        sig_name = "VehTiAndDataSec1"
        sig_start_bit = 5
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehTiAndDataYr1:
        sig_name = "VehTiAndDataYr1"
        sig_start_bit = 46
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehTiAndDataMins1:
        sig_name = "VehTiAndDataMins1"
        sig_start_bit = 13
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CEMBodyFr26:
    msg_name = "CEMBodyFr26"
    msg_id = 768
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.21
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DrvModReq:
        sig_name = "DrvModReq"
        sig_start_bit = 59
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvModReqType1_Undefd': 0, 'DrvModReqType1_ECO': 1, 'DrvModReqType1_Comfort_Normal': 2, 'DrvModReqType1_Dynamic_Sport': 3, 'DrvModReqType1_Reserved': 8, 'DrvModReqType1_Offroad_CrossTerrain': 5, 'DrvModReqType1_Adaptive': 6, 'DrvModReqType1_Race': 7, 'DrvModReqType1_ECO_PLUS': 9, 'DrvModReqType1_Power': 10, 'DrvModReqType1_Snow': 11, 'DrvModReqType1_Sand': 12, 'DrvModReqType1_Mud': 13, 'DrvModReqType1_Rock': 14, 'DrvModReqType1_Err': 15}
        compute_method = None
        length = 4
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class CEMBodyFr28:
    msg_name = "CEMBodyFr28"
    msg_id = 464
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class AirTFromHeatgEstimd:
        sig_name = "AirTFromHeatgEstimd"
        sig_start_bit = 52
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class EcmRoilgCntr:
        sig_name = "EcmRoilgCntr"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class SeatOccptAtRowSecMid:
        sig_name = "SeatOccptAtRowSecMid"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PassSeatSts1_Empty': 0, 'PassSeatSts1_Fmale': 1, 'PassSeatSts1_OccptLrg': 2, 'PassSeatSts1_Ukwn': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class RoadInclnQly:
        sig_name = "RoadInclnQly"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qly2_Flt': 0, 'Qly2_NoInfo': 1, 'Qly2_Vld': 2}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WipgInfoWiprActv:
        sig_name = "WipgInfoWiprActv"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class WipgInfoWiprInWipgAr:
        sig_name = "WipgInfoWiprInWipgAr"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SunCurtPosnSts:
        sig_name = "SunCurtPosnSts"
        sig_start_bit = 28
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 28
        byte = 3
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class WipgInfoWipgSpdInfo:
        sig_name = "WipgInfoWipgSpdInfo"
        sig_start_bit = 34
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgSpdInfo_Off': 0, 'WipgSpdInfo_IntlLo': 1, 'WipgSpdInfo_IntlHi': 2, 'WipgSpdInfo_WipgSpd4045': 3, 'WipgSpdInfo_WipgSpd4650': 4, 'WipgSpdInfo_WipgSpd5155': 5, 'WipgSpdInfo_WipgSpd5660': 6, 'WipgSpdInfo_WiprErr': 7}
        compute_method = None
        length = 3
        startbit = 34
        byte = 4
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class RoadInclnRoadIncln:
        sig_name = "RoadInclnRoadIncln"
        sig_start_bit = 15
        sig_length = 16
        sig_value_factor = "3.0518E-5"
        sig_value_offset = 0.0
        sig_value_min = -32767
        sig_value_max = 32767
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class SunRoofPosnSts:
        sig_name = "SunRoofPosnSts"
        sig_start_bit = 7
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 7
        byte = 0
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3


class DdmBodyFr07:
    msg_name = "DdmBodyFr07"
    msg_id = 192
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CenLockMacKeyReq:
        sig_name = "CenLockMacKeyReq"
        sig_start_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockgCenReq2_Idle': 0, 'LockgCenReq2_Unlck': 1, 'LockgCenReq2_Lock': 2}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class CemBodyFr121:
    msg_name = "CemBodyFr121"
    msg_id = 276
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.075
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class InteCleanUnpleSmell:
        sig_name = "InteCleanUnpleSmell"
        sig_start_bit = 61
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
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class CemBodyFr90:
    msg_name = "CemBodyFr90"
    msg_id = 971
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.285
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class IntelliClimaHvCooltHeatrTReq:
        sig_name = "IntelliClimaHvCooltHeatrTReq"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = "-40.0"
        sig_value_min = 0
        sig_value_max = 255
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

    class IntelliClimaUsrHumPrefrnc:
        sig_name = "IntelliClimaUsrHumPrefrnc"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class IntelliClimaResd13:
        sig_name = "IntelliClimaResd13"
        sig_start_bit = 7
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaUsrFanPrefrnc:
        sig_name = "IntelliClimaUsrFanPrefrnc"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyFr109:
    msg_name = "CemBodyFr109"
    msg_id = 818
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HmiPassClimaAutReq:
        sig_name = "HmiPassClimaAutReq"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HmiDrvrClimaAutReq:
        sig_name = "HmiDrvrClimaAutReq"
        sig_start_bit = 17
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
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HmiCmptmtSecRowLeAirDistbn:
        sig_name = "HmiCmptmtSecRowLeAirDistbn"
        sig_start_bit = 7
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtAirDistbnFrnt_Flr': 0, 'HmiCmptmtAirDistbnFrnt_Vent': 1, 'HmiCmptmtAirDistbnFrnt_Defrst': 2, 'HmiCmptmtAirDistbnFrnt_FlrDefrst': 3, 'HmiCmptmtAirDistbnFrnt_FlrVent': 4, 'HmiCmptmtAirDistbnFrnt_VentDefrst': 5, 'HmiCmptmtAirDistbnFrnt_FlrVentDefrst': 6, 'HmiCmptmtAirDistbnFrnt_Aut': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HmiSecRowLeClimaAutReq:
        sig_name = "HmiSecRowLeClimaAutReq"
        sig_start_bit = 21
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
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HmiSecRowLeHvacFanLvl:
        sig_name = "HmiSecRowLeHvacFanLvl"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiHvacFanLvl_Off': 0, 'HmiHvacFanLvl_LvlMan1': 1, 'HmiHvacFanLvl_LvlMan2': 2, 'HmiHvacFanLvl_LvlMan3': 3, 'HmiHvacFanLvl_LvlMan4': 4, 'HmiHvacFanLvl_LvlMan5': 5, 'HmiHvacFanLvl_LvlMan6': 6, 'HmiHvacFanLvl_LvlMan7': 7, 'HmiHvacFanLvl_LvlMan8': 8, 'HmiHvacFanLvl_LvlMan9': 9, 'HmiHvacFanLvl_LvlAutMinusMinus': 10, 'HmiHvacFanLvl_LvlAutMinus': 11, 'HmiHvacFanLvl_LvlAutNorm': 12, 'HmiHvacFanLvl_LvlAutPlus': 13, 'HmiHvacFanLvl_LvlAutPlusPlus': 14, 'HmiHvacFanLvl_Reserved': 15}
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HmiPassHvacFanLvl:
        sig_name = "HmiPassHvacFanLvl"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiHvacFanLvl_Off': 0, 'HmiHvacFanLvl_LvlMan1': 1, 'HmiHvacFanLvl_LvlMan2': 2, 'HmiHvacFanLvl_LvlMan3': 3, 'HmiHvacFanLvl_LvlMan4': 4, 'HmiHvacFanLvl_LvlMan5': 5, 'HmiHvacFanLvl_LvlMan6': 6, 'HmiHvacFanLvl_LvlMan7': 7, 'HmiHvacFanLvl_LvlMan8': 8, 'HmiHvacFanLvl_LvlMan9': 9, 'HmiHvacFanLvl_LvlAutMinusMinus': 10, 'HmiHvacFanLvl_LvlAutMinus': 11, 'HmiHvacFanLvl_LvlAutNorm': 12, 'HmiHvacFanLvl_LvlAutPlus': 13, 'HmiHvacFanLvl_LvlAutPlusPlus': 14, 'HmiHvacFanLvl_Reserved': 15}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HmiSecRowRiClimaAutReq:
        sig_name = "HmiSecRowRiClimaAutReq"
        sig_start_bit = 26
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
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HmiSecRowRiHvacFanLvl:
        sig_name = "HmiSecRowRiHvacFanLvl"
        sig_start_bit = 39
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiHvacFanLvl_Off': 0, 'HmiHvacFanLvl_LvlMan1': 1, 'HmiHvacFanLvl_LvlMan2': 2, 'HmiHvacFanLvl_LvlMan3': 3, 'HmiHvacFanLvl_LvlMan4': 4, 'HmiHvacFanLvl_LvlMan5': 5, 'HmiHvacFanLvl_LvlMan6': 6, 'HmiHvacFanLvl_LvlMan7': 7, 'HmiHvacFanLvl_LvlMan8': 8, 'HmiHvacFanLvl_LvlMan9': 9, 'HmiHvacFanLvl_LvlAutMinusMinus': 10, 'HmiHvacFanLvl_LvlAutMinus': 11, 'HmiHvacFanLvl_LvlAutNorm': 12, 'HmiHvacFanLvl_LvlAutPlus': 13, 'HmiHvacFanLvl_LvlAutPlusPlus': 14, 'HmiHvacFanLvl_Reserved': 15}
        compute_method = None
        length = 4
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HmiCmptmtSecRowRiAirDistbn:
        sig_name = "HmiCmptmtSecRowRiAirDistbn"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtAirDistbnFrnt_Flr': 0, 'HmiCmptmtAirDistbnFrnt_Vent': 1, 'HmiCmptmtAirDistbnFrnt_Defrst': 2, 'HmiCmptmtAirDistbnFrnt_FlrDefrst': 3, 'HmiCmptmtAirDistbnFrnt_FlrVent': 4, 'HmiCmptmtAirDistbnFrnt_VentDefrst': 5, 'HmiCmptmtAirDistbnFrnt_FlrVentDefrst': 6, 'HmiCmptmtAirDistbnFrnt_Aut': 7}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class HmiDrvrHvacFanLvl:
        sig_name = "HmiDrvrHvacFanLvl"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiHvacFanLvl_Off': 0, 'HmiHvacFanLvl_LvlMan1': 1, 'HmiHvacFanLvl_LvlMan2': 2, 'HmiHvacFanLvl_LvlMan3': 3, 'HmiHvacFanLvl_LvlMan4': 4, 'HmiHvacFanLvl_LvlMan5': 5, 'HmiHvacFanLvl_LvlMan6': 6, 'HmiHvacFanLvl_LvlMan7': 7, 'HmiHvacFanLvl_LvlMan8': 8, 'HmiHvacFanLvl_LvlMan9': 9, 'HmiHvacFanLvl_LvlAutMinusMinus': 10, 'HmiHvacFanLvl_LvlAutMinus': 11, 'HmiHvacFanLvl_LvlAutNorm': 12, 'HmiHvacFanLvl_LvlAutPlus': 13, 'HmiHvacFanLvl_LvlAutPlusPlus': 14, 'HmiHvacFanLvl_Reserved': 15}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class SmpBodyFr01:
    msg_name = "SmpBodyFr01"
    msg_id = 304
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class PassSeatHeatgDesPwrCns:
        sig_name = "PassSeatHeatgDesPwrCns"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class PassSeatBtnPsd:
        sig_name = "PassSeatBtnPsd"
        sig_start_bit = 56
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class PassSeatVentnActlPwrCns:
        sig_name = "PassSeatVentnActlPwrCns"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class PassSeatMemSts:
        sig_name = "PassSeatMemSts"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class PassSeatInAutMovmt:
        sig_name = "PassSeatInAutMovmt"
        sig_start_bit = 58
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class PassSeatVentnDesPwrCns:
        sig_name = "PassSeatVentnDesPwrCns"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class PassSeatHeatgActlPwrCns:
        sig_name = "PassSeatHeatgActlPwrCns"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class RrdmToBgmBodyDiagRespFrame:
    msg_name = "RrdmToBgmBodyDiagRespFrame"
    msg_id = 1570
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CemBodyFr89:
    msg_name = "CemBodyFr89"
    msg_id = 967
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class IntelliClimaHvBattInCooltTReq:
        sig_name = "IntelliClimaHvBattInCooltTReq"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = "-50.0"
        sig_value_min = 0
        sig_value_max = 250
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

    class IntelliClimaHvBattInCooltFlowReq:
        sig_name = "IntelliClimaHvBattInCooltFlowReq"
        sig_start_bit = 32
        sig_length = 9
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 32
        bmuws_info = [(4, 0b00000001, 0b11111110, 1, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaHvacEvaprTSp:
        sig_name = "IntelliClimaHvacEvaprTSp"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = "-5.0"
        sig_value_min = 0
        sig_value_max = 250
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

    class IntelliClimaResd12:
        sig_name = "IntelliClimaResd12"
        sig_start_bit = 7
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class CEMBodyFr13:
    msg_name = "CEMBodyFr13"
    msg_id = 256
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ExtrMirrFoldSetgMirrDrvr:
        sig_name = "ExtrMirrFoldSetgMirrDrvr"
        sig_start_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ExtrMirrSelnHmiReq:
        sig_name = "ExtrMirrSelnHmiReq"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'idle': 0, 'left': 1, 'right': 2}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class EgyCnsAllwdForClima:
        sig_name = "EgyCnsAllwdForClima"
        sig_start_bit = 30
        sig_length = 7
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 127
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 30
        byte = 3
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class RelHumSnsrQf:
        sig_name = "RelHumSnsrQf"
        sig_start_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DataQf_NotOk': 0, 'DataQf_Ok': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ExtrMirrFoldHmiReq:
        sig_name = "ExtrMirrFoldHmiReq"
        sig_start_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class PrkgAssiSysRemPrkgSts:
        sig_name = "PrkgAssiSysRemPrkgSts"
        sig_start_bit = 43
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 14
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PrkgAssiSysRemPrkgSts_OFF': 0, 'PrkgAssiSysRemPrkgSts_Remoteparkinstandby': 1, 'PrkgAssiSysRemPrkgSts_Remoteparkoutstandby': 2, 'PrkgAssiSysRemPrkgSts_Searching': 3, 'PrkgAssiSysRemPrkgSts_Remoteparkinpreactive': 4, 'PrkgAssiSysRemPrkgSts_Remoteparkactive': 5, 'PrkgAssiSysRemPrkgSts_Parkprocessactive': 6, 'PrkgAssiSysRemPrkgSts_Suspend': 7, 'PrkgAssiSysRemPrkgSts_Abort': 8, 'PrkgAssiSysRemPrkgSts_Remoteparkprocesscompleted': 9, 'PrkgAssiSysRemPrkgSts_Remoteparkoutprocscompleted': 10, 'PrkgAssiSysRemPrkgSts_Remoteparkcompleted': 11, 'PrkgAssiSysRemPrkgSts_Quit': 12, 'PrkgAssiSysRemPrkgSts_Failure': 13, 'PrkgAssiSysRemPrkgSts_Cancel': 14}
        compute_method = None
        length = 4
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class LockgCenStsTrigSrc:
        sig_name = "LockgCenStsTrigSrc"
        sig_start_bit = 15
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockTrigSrc2_NoTrigSrc': 0, 'LockTrigSrc2_KeyRem': 1, 'LockTrigSrc2_Keyls': 2, 'LockTrigSrc2_IntrSwt': 3, 'LockTrigSrc2_SpdAut': 4, 'LockTrigSrc2_TmrAut': 5, 'LockTrigSrc2_Slam': 6, 'LockTrigSrc2_Telm': 7, 'LockTrigSrc2_Crash': 8, 'LockTrigSrc2_Apprch': 9, 'LockTrigSrc2_OutsOth': 10, 'LockTrigSrc2_InsOth': 11}
        compute_method = None
        length = 4
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class LockgCenStsLockSt:
        sig_name = "LockgCenStsLockSt"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSt3_LockUndefd': 0, 'LockSt3_LockUnlckd': 1, 'LockSt3_LockTrUnlckd': 2, 'LockSt3_LockLockd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ExtrMirrAdjHmiReq:
        sig_name = "ExtrMirrAdjHmiReq"
        sig_start_bit = 39
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MirrDirReqTyp_Idle': 0, 'MirrDirReqTyp_Up': 1, 'MirrDirReqTyp_Down': 2, 'MirrDirReqTyp_Left': 3, 'MirrDirReqTyp_Right': 4}
        compute_method = None
        length = 3
        startbit = 39
        byte = 4
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ExtrMirrTiltSetgIdPen:
        sig_name = "ExtrMirrTiltSetgIdPen"
        sig_start_bit = 19
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class LockgCenStsUpdEve:
        sig_name = "LockgCenStsUpdEve"
        sig_start_bit = 9
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ExtrMirrFoldSetgIdPen:
        sig_name = "ExtrMirrFoldSetgIdPen"
        sig_start_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ExtrMirrTiltSetgMirrPass:
        sig_name = "ExtrMirrTiltSetgMirrPass"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ExtrMirrFoldSetgMirrPass:
        sig_name = "ExtrMirrFoldSetgMirrPass"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SteerWhlHeatgPwrAct:
        sig_name = "SteerWhlHeatgPwrAct"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class IncomingAirQlyCtrlFromHmi:
        sig_name = "IncomingAirQlyCtrlFromHmi"
        sig_start_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ExtrMirrTiltSetgMirrDrvr:
        sig_name = "ExtrMirrTiltSetgMirrDrvr"
        sig_start_bit = 20
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class CcmBodyFr29:
    msg_name = "CcmBodyFr29"
    msg_id = 1184
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class IntPm25HiPopUp:
        sig_name = "IntPm25HiPopUp"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IntPmHiPopUp_NoReq': 0, 'IntPmHiPopUp_ClimaOn': 1, 'IntPmHiPopUp_ClimaOnAndWinClsd': 2, 'IntPmHiPopUp_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FragCh1Id:
        sig_name = "FragCh1Id"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class OutdAirQlyOutdAirQly:
        sig_name = "OutdAirQlyOutdAirQly"
        sig_start_bit = 57
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AirQly_No': 0, 'AirQly_LvlLo': 1, 'AirQly_LvlMed': 2, 'AirQly_LvlHi': 3}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ElecAirVentnAvlSts:
        sig_name = "ElecAirVentnAvlSts"
        sig_start_bit = 45
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StsFd_None': 0, 'StsFd_On': 1, 'StsFd_Off': 2, 'StsFd_Error': 3, 'StsFd_Functionallimit': 4, 'StsFd_Energylimit': 5, 'StsFd_Resvd1': 6, 'StsFd_Resvd2': 7}
        compute_method = None
        length = 3
        startbit = 45
        byte = 5
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class FragCh2Id:
        sig_name = "FragCh2Id"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class OutdAirQlyQf:
        sig_name = "OutdAirQlyQf"
        sig_start_bit = 58
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OutdAirQlyQf_SnsrNotOk': 0, 'OutdAirQlyQf_SnsrOk': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DefrstMaxSts:
        sig_name = "DefrstMaxSts"
        sig_start_bit = 63
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class FragCh3Id:
        sig_name = "FragCh3Id"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class FragCh4Id:
        sig_name = "FragCh4Id"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class FragCh5Id:
        sig_name = "FragCh5Id"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class FragRefreshPopUp:
        sig_name = "FragRefreshPopUp"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class CemBodyFr91:
    msg_name = "CemBodyFr91"
    msg_id = 975
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.285
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class IntelliClimaResd14:
        sig_name = "IntelliClimaResd14"
        sig_start_bit = 7
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaUsrHumPrefrncEn:
        sig_name = "IntelliClimaUsrHumPrefrncEn"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IntelliClimaUsrTPrefrncEn:
        sig_name = "IntelliClimaUsrTPrefrncEn"
        sig_start_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IntelliClimaUsrTPrefrnc:
        sig_name = "IntelliClimaUsrTPrefrnc"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class IntelliClimaUsrFanPrefrncEn:
        sig_name = "IntelliClimaUsrFanPrefrncEn"
        sig_start_bit = 34
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 34
        byte = 4
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1


class RldmToBgmBodyDiagRespFrame:
    msg_name = "RldmToBgmBodyDiagRespFrame"
    msg_id = 1569
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CemBodyFr03:
    msg_name = "CemBodyFr03"
    msg_id = 118
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class RadioFrqAM:
        sig_name = "RadioFrqAM"
        sig_start_bit = 55
        sig_length = 11
        sig_value_factor = 1
        sig_value_offset = 522
        sig_value_min = 0
        sig_value_max = 1188
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11100000, 0b00011111, 3, 5)]

    class VehSpdLgtChks:
        sig_name = "VehSpdLgtChks"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ActvnOfIndcrIndcrOut:
        sig_name = "ActvnOfIndcrIndcrOut"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IndcrSts1_Off': 0, 'IndcrSts1_LeOn': 1, 'IndcrSts1_RiOn': 2, 'IndcrSts1_LeAndRiOn': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ActvnOfIndcrIndcrOutCntr:
        sig_name = "ActvnOfIndcrIndcrOutCntr"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehSpdLgtCntr:
        sig_name = "VehSpdLgtCntr"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ActvnOfIndcrIndcrOutChks:
        sig_name = "ActvnOfIndcrIndcrOutChks"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehSpdLgtA:
        sig_name = "VehSpdLgtA"
        sig_start_bit = 22
        sig_length = 15
        sig_value_factor = 0.00391
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 31970
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 22
        bmuws_info = [(2, 0b01111111, 0b10000000, 7, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class VehSpdLgtQf:
        sig_name = "VehSpdLgtQf"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class CEMBodyFr27:
    msg_name = "CEMBodyFr27"
    msg_id = 784
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.175
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class CamStsCamFrntCalNotStrtd:
        sig_name = "CamStsCamFrntCalNotStrtd"
        sig_start_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CamStsCntr:
        sig_name = "CamStsCntr"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CamStsCamFrntBlkd3:
        sig_name = "CamStsCamFrntBlkd3"
        sig_start_bit = 47
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CamStsCamFrntFaulty:
        sig_name = "CamStsCamFrntFaulty"
        sig_start_bit = 53
        sig_length = 12
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 53
        bmuws_info = [(6, 0b00111111, 0b11000000, 6, 0), (7, 0b11111100, 0b00000011, 6, 2)]

    class CamStsCamFrntBlkd2:
        sig_name = "CamStsCamFrntBlkd2"
        sig_start_bit = 32
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CamStsCamCamFrntCalNotCmpl:
        sig_name = "CamStsCamCamFrntCalNotCmpl"
        sig_start_bit = 35
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CamStsCamFrntBlkd1:
        sig_name = "CamStsCamFrntBlkd1"
        sig_start_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CamStsCamFrontEna:
        sig_name = "CamStsCamFrontEna"
        sig_start_bit = 55
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CamStsCamMissCom:
        sig_name = "CamStsCamMissCom"
        sig_start_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CamStsChks:
        sig_name = "CamStsChks"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CamStsCamFrntBlkd4:
        sig_name = "CamStsCamFrntBlkd4"
        sig_start_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CamStsCamCamHeatrActv:
        sig_name = "CamStsCamCamHeatrActv"
        sig_start_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CamStsCamFrntBlkd6:
        sig_name = "CamStsCamFrntBlkd6"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CamStsCamFrntBlkd8:
        sig_name = "CamStsCamFrntBlkd8"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CamStsCamFrntBlkd5:
        sig_name = "CamStsCamFrntBlkd5"
        sig_start_bit = 45
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CamStsCamFrntBlkd7:
        sig_name = "CamStsCamFrntBlkd7"
        sig_start_bit = 43
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYes1_No': 0, 'NoYes1_Yes': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BkpOfDstTrvld:
        sig_name = "BkpOfDstTrvld"
        sig_start_bit = 4
        sig_length = 21
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 21
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CemBodyFr103:
    msg_name = "CemBodyFr103"
    msg_id = 91
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ShortDropWinLeReDoor:
        sig_name = "ShortDropWinLeReDoor"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShortDrop_Idle': 0, 'ShortDrop_Close': 1, 'ShortDrop_Open': 2}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HvBattLimnIndcn:
        sig_name = "HvBattLimnIndcn"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class ShortDropWinRiReDoor:
        sig_name = "ShortDropWinRiReDoor"
        sig_start_bit = 14
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShortDrop_Idle': 0, 'ShortDrop_Close': 1, 'ShortDrop_Open': 2}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class ShortDropWinPassDoor:
        sig_name = "ShortDropWinPassDoor"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShortDrop_Idle': 0, 'ShortDrop_Close': 1, 'ShortDrop_Open': 2}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ShortDropWinDrvrDoor:
        sig_name = "ShortDropWinDrvrDoor"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShortDrop_Idle': 0, 'ShortDrop_Close': 1, 'ShortDrop_Open': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BgmToCcmBodyDiagReqFrame:
    msg_name = "BgmToCcmBodyDiagReqFrame"
    msg_id = 1809
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class SwtlToBgmBodyDiagRespFrame:
    msg_name = "SwtlToBgmBodyDiagRespFrame"
    msg_id = 1666
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CemBodyFr92:
    msg_name = "CemBodyFr92"
    msg_id = 952
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class WinOpenAppReqWinOpenClsGlbSts:
        sig_name = "WinOpenAppReqWinOpenClsGlbSts"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinOpenClsGlbReqFromTelm_Idle': 0, 'WinOpenClsGlbReqFromTelm_Open': 1, 'WinOpenClsGlbReqFromTelm_Close': 2}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class MirrOpenClsReq:
        sig_name = "MirrOpenClsReq"
        sig_start_bit = 38
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MirrFoldCmdTyp_Idle': 0, 'MirrFoldCmdTyp_FoldIn': 1, 'MirrFoldCmdTyp_FoldOut': 2}
        compute_method = None
        length = 2
        startbit = 38
        byte = 4
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class IntelliClimaResd15:
        sig_name = "IntelliClimaResd15"
        sig_start_bit = 7
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class TelmDefrostReq:
        sig_name = "TelmDefrostReq"
        sig_start_bit = 61
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WinOpenAppReqWindowOpenValue:
        sig_name = "WinOpenAppReqWindowOpenValue"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class HmiHvacRecircLongPsdSts:
        sig_name = "HmiHvacRecircLongPsdSts"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class SmpBodyFr02:
    msg_name = "SmpBodyFr02"
    msg_id = 275
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class PassSeatPosPercSeatPosHeiPerc:
        sig_name = "PassSeatPosPercSeatPosHeiPerc"
        sig_start_bit = 17
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class PassSeatPosPercSeatPosSldPerc:
        sig_name = "PassSeatPosPercSeatPosSldPerc"
        sig_start_bit = 39
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class SeatBackAngleRowFirstPass:
        sig_name = "SeatBackAngleRowFirstPass"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 180
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

    class PassSeatPosPercSeatPosSldQF:
        sig_name = "PassSeatPosPercSeatPosSldQF"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PassSeatPosPercSeatPosFrntHeiQF:
        sig_name = "PassSeatPosPercSeatPosFrntHeiQF"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PassSeatPosPercSeatPosFrntHeiPerc:
        sig_name = "PassSeatPosPercSeatPosFrntHeiPerc"
        sig_start_bit = 15
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11000000, 0b00111111, 2, 6)]

    class PassSeatPosPercSeatPosHeiQF:
        sig_name = "PassSeatPosPercSeatPosHeiQF"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class CcmBodyFr39:
    msg_name = "CcmBodyFr39"
    msg_id = 868
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmIntelliClimaResd9:
        sig_name = "CcmIntelliClimaResd9"
        sig_start_bit = 47
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class CcmIntelliClimaResd5:
        sig_name = "CcmIntelliClimaResd5"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmIntelliClimaResd15:
        sig_name = "CcmIntelliClimaResd15"
        sig_start_bit = 15
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]


class BgmToRldmBodyDiagReqFrame:
    msg_name = "BgmToRldmBodyDiagReqFrame"
    msg_id = 1825
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyFr67:
    msg_name = "CemBodyFr67"
    msg_id = 570
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.035
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DCChrgnHndlSts:
        sig_name = "DCChrgnHndlSts"
        sig_start_bit = 58
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnBdChrgrHndlSts_Disconnected': 0, 'OnBdChrgrHndlSts_ConnectedWithoutPower': 1, 'OnBdChrgrHndlSts_PowerAvailableButNotActivated': 2, 'OnBdChrgrHndlSts_ConnectedWithPower': 3, 'OnBdChrgrHndlSts_Init': 4, 'OnBdChrgrHndlSts_Fault': 5}
        compute_method = None
        length = 3
        startbit = 58
        byte = 7
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DefrstStsWinDefrstRe:
        sig_name = "DefrstStsWinDefrstRe"
        sig_start_bit = 20
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActrDefrstSts_Off': 0, 'ActrDefrstSts_On': 1, 'ActrDefrstSts_Limited': 2, 'ActrDefrstSts_NotAvailable': 3, 'ActrDefrstSts_TmrOff': 4, 'ActrDefrstSts_AutoCdn': 5}
        compute_method = None
        length = 3
        startbit = 20
        byte = 2
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class IsgMotT:
        sig_name = "IsgMotT"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = "-50.0"
        sig_value_min = 0
        sig_value_max = 250
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

    class DefrstStsWinDefrstFrnt:
        sig_name = "DefrstStsWinDefrstFrnt"
        sig_start_bit = 23
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActrDefrstSts_Off': 0, 'ActrDefrstSts_On': 1, 'ActrDefrstSts_Limited': 2, 'ActrDefrstSts_NotAvailable': 3, 'ActrDefrstSts_TmrOff': 4, 'ActrDefrstSts_AutoCdn': 5}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DefrstStsMirrDefrst:
        sig_name = "DefrstStsMirrDefrst"
        sig_start_bit = 10
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActrDefrstSts_Off': 0, 'ActrDefrstSts_On': 1, 'ActrDefrstSts_Limited': 2, 'ActrDefrstSts_NotAvailable': 3, 'ActrDefrstSts_TmrOff': 4, 'ActrDefrstSts_AutoCdn': 5}
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class WiprFrntSrvModReq:
        sig_name = "WiprFrntSrvModReq"
        sig_start_bit = 44
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoActn': 0, 'ActvtSrvPosn': 1, 'DeActvtSrvPosn': 2}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class SwtlPrivateDHUCanFr06:
    msg_name = "SwtlPrivateDHUCanFr06"
    msg_id = 52
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DiagcFailrTouchPanSWTLVibrationFltSts:
        sig_name = "DiagcFailrTouchPanSWTLVibrationFltSts"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltSts_NoFlt': 0, 'FltSts_VibrationShoCirc': 1, 'FltSts_VibrationOpenCirc': 2, 'FltSts_invalid': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DiagcFailrTouchPanSWTLCmnFltSts:
        sig_name = "DiagcFailrTouchPanSWTLCmnFltSts"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmnFltSts_NoFlt': 0, 'CmnFltSts_OutdURng': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DiagcFailrTouchPanSWTLSnsrFltSts:
        sig_name = "DiagcFailrTouchPanSWTLSnsrFltSts"
        sig_start_bit = 6
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrFltSts_NoFlt': 0, 'SnsrFltSts_FSnsrInvld': 1, 'SnsrFltSts_FSnsrShoCircToGnd': 2, 'SnsrFltSts_FSnsrShoCircToBatt': 3, 'SnsrFltSts_FSnsrOpenCirc': 4}
        compute_method = None
        length = 3
        startbit = 6
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DiagcFailrTouchPanSWTLTouchdFltSts:
        sig_name = "DiagcFailrTouchPanSWTLTouchdFltSts"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltSts_NoFlt': 0, 'FltSts_TouchdInvld': 1, 'FltSts_TouchdOutdOfRng': 2}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class PotBodyFr02:
    msg_name = "PotBodyFr02"
    msg_id = 149
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class SwtTrClsReq:
        sig_name = "SwtTrClsReq"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrSfbtncmd_Idle': 0, 'TrSfbtncmd_ShoPsd': 1, 'TrSfbtncmd_DlyCls': 2, 'TrSfbtncmd_PosnSet': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TopPosHmiFeedBack:
        sig_name = "TopPosHmiFeedBack"
        sig_start_bit = 15
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TailgatePos_Unknown': 0, 'TailgatePos_Fail': 1, 'TailgatePos_0to20PercTopPos': 2, 'TailgatePos_21to40PercTopPos': 3, 'TailgatePos_41to60PercTopPos': 4, 'TailgatePos_61to80PercTopPos': 5, 'TailgatePos_81to100PercTopPos': 6}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class TrOpenerSts:
        sig_name = "TrOpenerSts"
        sig_start_bit = 3
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 10
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrOpenerSts1_Ukwn': 0, 'TrOpenerSts1_FullClsd': 1, 'TrOpenerSts1_MovgUp': 2, 'TrOpenerSts1_MovgUpBrkg': 3, 'TrOpenerSts1_StopDurgOpen': 4, 'TrOpenerSts1_FullOpend': 5, 'TrOpenerSts1_MovgDwn': 6, 'TrOpenerSts1_MovgDwnBrkg': 7, 'TrOpenerSts1_StopDurgCls': 8, 'TrOpenerSts1_HalfClsd': 9, 'TrOpenerSts1_StopMinPntForCls': 10}
        compute_method = None
        length = 4
        startbit = 3
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SwtTrClsSts:
        sig_name = "SwtTrClsSts"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class TrObstclDetn:
        sig_name = "TrObstclDetn"
        sig_start_bit = 10
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class TrAntiPnch:
        sig_name = "TrAntiPnch"
        sig_start_bit = 8
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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


class CEMBodyFr34:
    msg_name = "CEMBodyFr34"
    msg_id = 832
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehCfgPrmCCPBytePosn2:
        sig_name = "VehCfgPrmCCPBytePosn2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn5:
        sig_name = "VehCfgPrmCCPBytePosn5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn4:
        sig_name = "VehCfgPrmCCPBytePosn4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn6:
        sig_name = "VehCfgPrmCCPBytePosn6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmBlkIDBytePosn1:
        sig_name = "VehCfgPrmBlkIDBytePosn1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn7:
        sig_name = "VehCfgPrmCCPBytePosn7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmCCPBytePosn8:
        sig_name = "VehCfgPrmCCPBytePosn8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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


class CcmBodyFr08:
    msg_name = "CcmBodyFr08"
    msg_id = 289
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CmptmtTFrntQf:
        sig_name = "CmptmtTFrntQf"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptmtTFrntQf_SnsrDataUndefd': 0, 'CmptmtTFrntQf_FanNotRunning': 1, 'CmptmtTFrntQf_SnsrDataNotOk': 2, 'CmptmtTFrntQf_SnsrDataOk': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CmptmtTFrntCmptmtTFrnt:
        sig_name = "CmptmtTFrntCmptmtTFrnt"
        sig_start_bit = 34
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 1850
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class CmptmtAirTEstimdAtRowFirstLoResl:
        sig_name = "CmptmtAirTEstimdAtRowFirstLoResl"
        sig_start_bit = 18
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 1850
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class CmptmtTFrntFanForCmptmtTRunng:
        sig_name = "CmptmtTFrntFanForCmptmtTRunng"
        sig_start_bit = 35
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CmptmtAirTEstimdExtdComptmtT:
        sig_name = "CmptmtAirTEstimdExtdComptmtT"
        sig_start_bit = 2
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 1850
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class RlyCrashForClimaReq:
        sig_name = "RlyCrashForClimaReq"
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

    class CmptmtAirTEstimdExtdQlyFlg:
        sig_name = "CmptmtAirTEstimdExtdQlyFlg"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class EngRunngReqByClima:
        sig_name = "EngRunngReqByClima"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EngRunngReq_Dft': 0, 'EngRunngReq_StopInhb': 1, 'EngRunngReq_RunReq': 2, 'EngRunngReq_Resd': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class CemBodyFr88:
    msg_name = "CemBodyFr88"
    msg_id = 963
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class IntelliClimaResd11:
        sig_name = "IntelliClimaResd11"
        sig_start_bit = 23
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaResd10:
        sig_name = "IntelliClimaResd10"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class CemBodyFr09:
    msg_name = "CemBodyFr09"
    msg_id = 65
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ChdLockReRiCtrlHmiReq:
        sig_name = "ChdLockReRiCtrlHmiReq"
        sig_start_bit = 63
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockgCenReq2_Idle': 0, 'LockgCenReq2_Unlck': 1, 'LockgCenReq2_Lock': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HmiSeatClimaTmrHmiSeatHeatgFirstRiTmr:
        sig_name = "HmiSeatClimaTmrHmiSeatHeatgFirstRiTmr"
        sig_start_bit = 13
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 15
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 13
        byte = 1
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class HmiSeatClimaTmrHmiSeatHeatgSecLeTmr:
        sig_name = "HmiSeatClimaTmrHmiSeatHeatgSecLeTmr"
        sig_start_bit = 23
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 15
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 23
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class ChdLockReLeCtrlHmiReq:
        sig_name = "ChdLockReLeCtrlHmiReq"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockgCenReq2_Idle': 0, 'LockgCenReq2_Unlck': 1, 'LockgCenReq2_Lock': 2}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HmiSeatClimaTmrHmiSeatVentnFirstRiTmr:
        sig_name = "HmiSeatClimaTmrHmiSeatVentnFirstRiTmr"
        sig_start_bit = 37
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 15
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 37
        byte = 4
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class HmiSeatClimaTmrIdPen:
        sig_name = "HmiSeatClimaTmrIdPen"
        sig_start_bit = 7
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
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

    class HmiSeatClimaTmrHmiSeatHeatgSecRiTmr:
        sig_name = "HmiSeatClimaTmrHmiSeatHeatgSecRiTmr"
        sig_start_bit = 17
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 15
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class HmiSeatClimaTmrHmiSeatHeatgFirstLeTmr:
        sig_name = "HmiSeatClimaTmrHmiSeatHeatgFirstLeTmr"
        sig_start_bit = 3
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 15
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 3
        bmuws_info = [(0, 0b00001111, 0b11110000, 4, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class HmiSeatClimaTmrHmiSeatVentnFirstLeTmr:
        sig_name = "HmiSeatClimaTmrHmiSeatVentnFirstLeTmr"
        sig_start_bit = 27
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 15
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11000000, 0b00111111, 2, 6)]

    class HmiSeatClimaTmrHmiSeatVentnSecLeTmr:
        sig_name = "HmiSeatClimaTmrHmiSeatVentnSecLeTmr"
        sig_start_bit = 47
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 15
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 47
        byte = 5
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class HmiSeatClimaTmrHmiSeatVentnSecRiTmr:
        sig_name = "HmiSeatClimaTmrHmiSeatVentnSecRiTmr"
        sig_start_bit = 41
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 15
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 41
        bmuws_info = [(5, 0b00000011, 0b11111100, 2, 0), (6, 0b11110000, 0b00001111, 4, 4)]


class CemBodyFr68:
    msg_name = "CemBodyFr68"
    msg_id = 178
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.035
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class TiDrvgCycOff:
        sig_name = "TiDrvgCycOff"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class WinOpenReRiReq:
        sig_name = "WinOpenReRiReq"
        sig_start_bit = 63
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 63
        byte = 7
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class ClimaRqrdFromHmi:
        sig_name = "ClimaRqrdFromHmi"
        sig_start_bit = 18
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class WinVentnOpenReq:
        sig_name = "WinVentnOpenReq"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class WinOpenPassReq:
        sig_name = "WinOpenPassReq"
        sig_start_bit = 47
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 47
        byte = 5
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class WinOpenReLeReq:
        sig_name = "WinOpenReLeReq"
        sig_start_bit = 55
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 55
        byte = 6
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class WinOpenDrvrReq:
        sig_name = "WinOpenDrvrReq"
        sig_start_bit = 39
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 39
        byte = 4
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class ActvnOfHndlDoorLiHndlDoorLiDrvr:
        sig_name = "ActvnOfHndlDoorLiHndlDoorLiDrvr"
        sig_start_bit = 31
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ApproachLiSetReq_Off': 0, 'ApproachLiSetReq_ONStatic': 1, 'ApproachLiSetReq_ONDynamic': 2}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ActvnOfHndlDoorLiHndlDoorLiPassRe:
        sig_name = "ActvnOfHndlDoorLiHndlDoorLiPassRe"
        sig_start_bit = 28
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ApproachLiSetReq_Off': 0, 'ApproachLiSetReq_ONStatic': 1, 'ApproachLiSetReq_ONDynamic': 2}
        compute_method = None
        length = 1
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ActvnOfHndlDoorLiHndlDoorLiDrvrRe:
        sig_name = "ActvnOfHndlDoorLiHndlDoorLiDrvrRe"
        sig_start_bit = 30
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ApproachLiSetReq_Off': 0, 'ApproachLiSetReq_ONStatic': 1, 'ApproachLiSetReq_ONDynamic': 2}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class LVPwrSplyErrSts:
        sig_name = "LVPwrSplyErrSts"
        sig_start_bit = 23
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PwrSplyErrSts_SysOk': 0, 'PwrSplyErrSts_UhiDurgDrvg': 1, 'PwrSplyErrSts_UloDurgdrvg': 2, 'PwrSplyErrSts_BattRlyFlt': 3, 'PwrSplyErrSts_BattSnsrComFlt': 4, 'PwrSplyErrSts_BattSnsrHwFlt': 5, 'PwrSplyErrSts_FltComDcDc': 6, 'PwrSplyErrSts_FltElecDcDc': 7, 'PwrSplyErrSts_FltDcDc': 8, 'PwrSplyErrSts_SupCptrHwFlt': 9, 'PwrSplyErrSts_AltFltMecl': 10, 'PwrSplyErrSts_AltFltElec': 11, 'PwrSplyErrSts_AltFltT': 12, 'PwrSplyErrSts_AltFltCom': 13, 'PwrSplyErrSts_SpprtBattFltChrgn': 14, 'PwrSplyErrSts_Spare6': 15}
        compute_method = None
        length = 4
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class ActvnOfHndlDoorLiHndlDoorLiPass:
        sig_name = "ActvnOfHndlDoorLiHndlDoorLiPass"
        sig_start_bit = 29
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ApproachLiSetReq_Off': 0, 'ApproachLiSetReq_ONStatic': 1, 'ApproachLiSetReq_ONDynamic': 2}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class CcmBodyFr31:
    msg_name = "CcmBodyFr31"
    msg_id = 295
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class SecRowRiSeatVentnPwrAllwd:
        sig_name = "SecRowRiSeatVentnPwrAllwd"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class SteerWhlHeatgDurgClima:
        sig_name = "SteerWhlHeatgDurgClima"
        sig_start_bit = 45
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SecRowRiSeatHeatgPwrAllwd:
        sig_name = "SecRowRiSeatHeatgPwrAllwd"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class PassSeatVentnPwrAllwd:
        sig_name = "PassSeatVentnPwrAllwd"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AirFragCh5RunngSts:
        sig_name = "AirFragCh5RunngSts"
        sig_start_bit = 51
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
        startbit = 51
        byte = 6
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DrvrSeatVentnPwrAllwd:
        sig_name = "DrvrSeatVentnPwrAllwd"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class AirFragCh3RunngSts:
        sig_name = "AirFragCh3RunngSts"
        sig_start_bit = 53
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
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AirFragCh4RunngSts:
        sig_name = "AirFragCh4RunngSts"
        sig_start_bit = 52
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
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AirFragCh1RunngSts:
        sig_name = "AirFragCh1RunngSts"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RemClimaDefrstSts:
        sig_name = "RemClimaDefrstSts"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AirFragCh2RunngSts:
        sig_name = "AirFragCh2RunngSts"
        sig_start_bit = 54
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
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EcoClimaSts:
        sig_name = "EcoClimaSts"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SecRowLeSeatVentnPwrAllwd:
        sig_name = "SecRowLeSeatVentnPwrAllwd"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CcmBodyFr51:
    msg_name = "CcmBodyFr51"
    msg_id = 1158
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig7Byte2:
        sig_name = "CcmCaliSig7Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig7Byte1:
        sig_name = "CcmCaliSig7Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig7Byte6:
        sig_name = "CcmCaliSig7Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig7Byte7:
        sig_name = "CcmCaliSig7Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig7Byte0:
        sig_name = "CcmCaliSig7Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig7Byte5:
        sig_name = "CcmCaliSig7Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig7Byte4:
        sig_name = "CcmCaliSig7Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig7Byte3:
        sig_name = "CcmCaliSig7Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyDevFr01:
    msg_name = "CemBodyDevFr01"
    msg_id = 1434
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DiagFrameForECMByte7:
        sig_name = "DiagFrameForECMByte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DiagFrameForECMByte1:
        sig_name = "DiagFrameForECMByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DiagFrameForECMByte2:
        sig_name = "DiagFrameForECMByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DiagFrameForECMByte5:
        sig_name = "DiagFrameForECMByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DiagFrameForECMByte6:
        sig_name = "DiagFrameForECMByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DiagFrameForECMByte4:
        sig_name = "DiagFrameForECMByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DiagFrameForECMByte3:
        sig_name = "DiagFrameForECMByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DiagFrameForECMByte0:
        sig_name = "DiagFrameForECMByte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CEMBodyFr35:
    msg_name = "CEMBodyFr35"
    msg_id = 306
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehCfgPrmExtCCPBytePosn6:
        sig_name = "VehCfgPrmExtCCPBytePosn6"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn5:
        sig_name = "VehCfgPrmExtCCPBytePosn5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn3:
        sig_name = "VehCfgPrmExtCCPBytePosn3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn4:
        sig_name = "VehCfgPrmExtCCPBytePosn4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn8:
        sig_name = "VehCfgPrmExtCCPBytePosn8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn7:
        sig_name = "VehCfgPrmExtCCPBytePosn7"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class VehCfgPrmExtCCPBytePosn2:
        sig_name = "VehCfgPrmExtCCPBytePosn2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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


class CEMBodyFr33:
    msg_name = "CEMBodyFr33"
    msg_id = 816
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.215
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HvCooltHeatrEnadWhE2ECntr:
        sig_name = "HvCooltHeatrEnadWhE2ECntr"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehBattUSysU:
        sig_name = "VehBattUSysU"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 250
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

    class ProfPenSts1:
        sig_name = "ProfPenSts1"
        sig_start_bit = 23
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehBattUSysUQf:
        sig_name = "VehBattUSysUQf"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class HvCooltHeatrEnadWhE2EChks:
        sig_name = "HvCooltHeatrEnadWhE2EChks"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class HvCooltHeatrEnadWhE2EHvchEnad:
        sig_name = "HvCooltHeatrEnadWhE2EHvchEnad"
        sig_start_bit = 59
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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


class CemBodyFr71:
    msg_name = "CemBodyFr71"
    msg_id = 853
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class StrtRemSts1WdStrtRemSts:
        sig_name = "StrtRemSts1WdStrtRemSts"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StrtRemSts1_Idle': 0, 'StrtRemSts1_Strtg': 1, 'StrtRemSts1_Actv': 2}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ActvnOfWshrFrntSafe:
        sig_name = "ActvnOfWshrFrntSafe"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class CcmBodyFr16:
    msg_name = "CcmBodyFr16"
    msg_id = 1034
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class HvacAirTForRowSecAtVentLeEvaprTFrnt:
        sig_name = "HvacAirTForRowSecAtVentLeEvaprTFrnt"
        sig_start_bit = 36
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowSecAtFlrRiEvaprTQf:
        sig_name = "HvacAirTForRowSecAtFlrRiEvaprTQf"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvacAirTForRowSecAtVentLeEvaprTQf:
        sig_name = "HvacAirTForRowSecAtVentLeEvaprTQf"
        sig_start_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvacAirTForRowSecAtFlrLeEvaprTFrnt:
        sig_name = "HvacAirTForRowSecAtFlrLeEvaprTFrnt"
        sig_start_bit = 4
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowSecAtFlrLeEvaprTQf:
        sig_name = "HvacAirTForRowSecAtFlrLeEvaprTQf"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvacAirTForRowSecAtVentRiEvaprTQf:
        sig_name = "HvacAirTForRowSecAtVentRiEvaprTQf"
        sig_start_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvacAirTForRowSecAtFlrRiEvaprTFrnt:
        sig_name = "HvacAirTForRowSecAtFlrRiEvaprTFrnt"
        sig_start_bit = 20
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowSecAtVentRiEvaprTFrnt:
        sig_name = "HvacAirTForRowSecAtVentRiEvaprTFrnt"
        sig_start_bit = 52
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class BgmToDdmBodyDiagReqFrame:
    msg_name = "BgmToDdmBodyDiagReqFrame"
    msg_id = 1810
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CEMBodyFr14:
    msg_name = "CEMBodyFr14"
    msg_id = 320
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HmiHvacRecircCmd:
        sig_name = "HmiHvacRecircCmd"
        sig_start_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiHvacRecircCmd_Aut': 0, 'HmiHvacRecircCmd_AutWithAirQly': 1, 'HmiHvacRecircCmd_RecircFull': 2, 'HmiHvacRecircCmd_OscircFull': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HmiIImSptFragraReq:
        sig_name = "HmiIImSptFragraReq"
        sig_start_bit = 0
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class IncomingAirQlyPopUpReq:
        sig_name = "IncomingAirQlyPopUpReq"
        sig_start_bit = 60
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvSysRlyStsChks:
        sig_name = "HvSysRlyStsChks"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class HvSysRlyStsHvSysRlySts:
        sig_name = "HvSysRlyStsHvSysRlySts"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvActvnSts_Open': 0, 'HvActvnSts_Clsd': 1, 'HvActvnSts_KeepSt': 2, 'HvActvnSts_OpenAndReqActvDcha': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HmiHvacFanLvlRe:
        sig_name = "HmiHvacFanLvlRe"
        sig_start_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiHvacFanLvl_Off': 0, 'HmiHvacFanLvl_LvlMan1': 1, 'HmiHvacFanLvl_LvlMan2': 2, 'HmiHvacFanLvl_LvlMan3': 3, 'HmiHvacFanLvl_LvlMan4': 4, 'HmiHvacFanLvl_LvlMan5': 5, 'HmiHvacFanLvl_LvlMan6': 6, 'HmiHvacFanLvl_LvlMan7': 7, 'HmiHvacFanLvl_LvlMan8': 8, 'HmiHvacFanLvl_LvlMan9': 9, 'HmiHvacFanLvl_LvlAutMinusMinus': 10, 'HmiHvacFanLvl_LvlAutMinus': 11, 'HmiHvacFanLvl_LvlAutNorm': 12, 'HmiHvacFanLvl_LvlAutPlus': 13, 'HmiHvacFanLvl_LvlAutPlusPlus': 14, 'HmiHvacFanLvl_Reserved': 15}
        compute_method = None
        length = 4
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HvCooltHeatrStsSig:
        sig_name = "HvCooltHeatrStsSig"
        sig_start_bit = 42
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvCooltHeatrSts_Off': 0, 'HvCooltHeatrSts_LockedUntilNextStart': 1, 'HvCooltHeatrSts_LockedUntilService': 2, 'HvCooltHeatrSts_LockedPermanent': 3, 'HvCooltHeatrSts_Operation': 4, 'HvCooltHeatrSts_Reserved1': 5, 'HvCooltHeatrSts_Reserved2': 6, 'HvCooltHeatrSts_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 42
        byte = 5
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class SecClimaAutoSet:
        sig_name = "SecClimaAutoSet"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class CbnOverHeatProtnEna:
        sig_name = "CbnOverHeatProtnEna"
        sig_start_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HvSysRlyStsCntr:
        sig_name = "HvSysRlyStsCntr"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class FragRefrshAutSetg:
        sig_name = "FragRefrshAutSetg"
        sig_start_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CmptmtCoolgSts:
        sig_name = "CmptmtCoolgSts"
        sig_start_bit = 23
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptmtCoolgSts_OffNoReq': 0, 'CmptmtCoolgSts_OffByEvaprTLo': 1, 'CmptmtCoolgSts_OffByPLo': 2, 'CmptmtCoolgSts_OffByAmbTOutOfRng': 3, 'CmptmtCoolgSts_OffBySysFailr': 4, 'CmptmtCoolgSts_OffByLoadCut': 5, 'CmptmtCoolgSts_OnWithBattCoolg': 6, 'CmptmtCoolgSts_On': 7}
        compute_method = None
        length = 4
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class TWinRfClsdPopUpReq:
        sig_name = "TWinRfClsdPopUpReq"
        sig_start_bit = 15
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HmiDefrstMaxReq:
        sig_name = "HmiDefrstMaxReq"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ActrReq_Off': 0, 'ActrReq_On': 1, 'ActrReq_AutOn': 2}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HmiHvacFanLvlFrnt:
        sig_name = "HmiHvacFanLvlFrnt"
        sig_start_bit = 7
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiHvacFanLvl_Off': 0, 'HmiHvacFanLvl_LvlMan1': 1, 'HmiHvacFanLvl_LvlMan2': 2, 'HmiHvacFanLvl_LvlMan3': 3, 'HmiHvacFanLvl_LvlMan4': 4, 'HmiHvacFanLvl_LvlMan5': 5, 'HmiHvacFanLvl_LvlMan6': 6, 'HmiHvacFanLvl_LvlMan7': 7, 'HmiHvacFanLvl_LvlMan8': 8, 'HmiHvacFanLvl_LvlMan9': 9, 'HmiHvacFanLvl_LvlAutMinusMinus': 10, 'HmiHvacFanLvl_LvlAutMinus': 11, 'HmiHvacFanLvl_LvlAutNorm': 12, 'HmiHvacFanLvl_LvlAutPlus': 13, 'HmiHvacFanLvl_LvlAutPlusPlus': 14, 'HmiHvacFanLvl_Reserved': 15}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HmiHvacReCtrl:
        sig_name = "HmiHvacReCtrl"
        sig_start_bit = 63
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiHvacReCtrl_Off': 0, 'HmiHvacReCtrl_OffWithNoOccpt': 1, 'HmiHvacReCtrl_On': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HvClimaCmd:
        sig_name = "HvClimaCmd"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HVBattChargnCmd_OK': 0, 'HVBattChargnCmd_NOK': 1, 'HVBattChargnCmd_INIT': 2, 'HVBattChargnCmd_HOLD': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class CcmBodyFr01:
    msg_name = "CcmBodyFr01"
    msg_id = 177
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class EvaprTFrntEvaprTFrnt:
        sig_name = "EvaprTFrntEvaprTFrnt"
        sig_start_bit = 36
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class EvaprTFrntEvaprTQf:
        sig_name = "EvaprTFrntEvaprTQf"
        sig_start_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvacRecircAct:
        sig_name = "HvacRecircAct"
        sig_start_bit = 54
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 54
        byte = 6
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class HvacCoolgEnaFrnt:
        sig_name = "HvacCoolgEnaFrnt"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class IntPm25LvlFrmClima:
        sig_name = "IntPm25LvlFrmClima"
        sig_start_bit = 58
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmpmtAirPmLvl_Level1': 0, 'CmpmtAirPmLvl_Level2': 1, 'CmpmtAirPmLvl_Level3': 2, 'CmpmtAirPmLvl_Level4': 3, 'CmpmtAirPmLvl_Level5': 4, 'CmpmtAirPmLvl_Level6': 5, 'CmpmtAirPmLvl_Reserved': 6, 'CmpmtAirPmLvl_Invalid': 7}
        compute_method = None
        length = 3
        startbit = 58
        byte = 7
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class CcmBodyFr22:
    msg_name = "CcmBodyFr22"
    msg_id = 1040
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class RemClimaHvSts:
        sig_name = "RemClimaHvSts"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HvacCondsorTspEvaprTFrnt:
        sig_name = "HvacCondsorTspEvaprTFrnt"
        sig_start_bit = 44
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 44
        bmuws_info = [(5, 0b00011111, 0b11100000, 5, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class RemClimaHvRspn:
        sig_name = "RemClimaHvRspn"
        sig_start_bit = 61
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
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HpReqCritSts:
        sig_name = "HpReqCritSts"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RemClimaExtnTiRspn:
        sig_name = "RemClimaExtnTiRspn"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HvacCondsorTEvaprTQf:
        sig_name = "HvacCondsorTEvaprTQf"
        sig_start_bit = 29
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CmptModForHp:
        sig_name = "CmptModForHp"
        sig_start_bit = 23
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 5
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModeCmptHp_vent': 0, 'ModeCmptHp_cool': 1, 'ModeCmptHp_hot': 2, 'ModeCmptHp_cool_hot': 3, 'ModeCmptHp_cool_defog': 4, 'ModeCmptHp_hot_defog': 5, 'ModeCmptHp_cool_hot_defog': 6, 'ModeCmptHp_reserved': 7}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class RemClimaDelaySts:
        sig_name = "RemClimaDelaySts"
        sig_start_bit = 57
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
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HvacCondsorTEvaprTFrnt:
        sig_name = "HvacCondsorTEvaprTFrnt"
        sig_start_bit = 28
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 28
        bmuws_info = [(3, 0b00011111, 0b11100000, 5, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class HvacCondsorTspEvaprTQf:
        sig_name = "HvacCondsorTspEvaprTQf"
        sig_start_bit = 45
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvahBlwReq:
        sig_name = "HvahBlwReq"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaOffReq_NoReq': 0, 'ClimaOffReq_SecRowOffReq': 1, 'ClimaOffReq_TrdRowOffReq': 2, 'ClimaOffReq_ClimaOff': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvahPwrReq:
        sig_name = "HvahPwrReq"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 20
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyFr10:
    msg_name = "CemBodyFr10"
    msg_id = 1196
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DrvrSeatHallPosDownLdSeatFrntHeiPos:
        sig_name = "DrvrSeatHallPosDownLdSeatFrntHeiPos"
        sig_start_bit = 33
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DrvrSeatHallPosDownLdSeatHeiPos:
        sig_name = "DrvrSeatHallPosDownLdSeatHeiPos"
        sig_start_bit = 27
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 27
        bmuws_info = [(3, 0b00001111, 0b11110000, 4, 0), (4, 0b11111100, 0b00000011, 6, 2)]

    class DrvrSeatHallPosDownLdSeatSldPos:
        sig_name = "DrvrSeatHallPosDownLdSeatSldPos"
        sig_start_bit = 23
        sig_length = 12
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class DrvrSeatHallPosDownLdSeatInclPos:
        sig_name = "DrvrSeatHallPosDownLdSeatInclPos"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class CcmBodyFr38:
    msg_name = "CcmBodyFr38"
    msg_id = 865
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmIntelliClimaResd14:
        sig_name = "CcmIntelliClimaResd14"
        sig_start_bit = 15
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class CcmIntelliClimaResd8:
        sig_name = "CcmIntelliClimaResd8"
        sig_start_bit = 47
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class CcmIntelliClimaResd4:
        sig_name = "CcmIntelliClimaResd4"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class BgmToSmpBodyDiagReqFrame:
    msg_name = "BgmToSmpBodyDiagReqFrame"
    msg_id = 1832
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CcmToBgmBodyDiagRespFrame:
    msg_name = "CcmToBgmBodyDiagRespFrame"
    msg_id = 1553
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class BgmToAllFuncBodyDiagReqFrame:
    msg_name = "BgmToAllFuncBodyDiagReqFrame"
    msg_id = 2047
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyFr54:
    msg_name = "CemBodyFr54"
    msg_id = 151
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.645
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class LumHeiAdjmtRowFirstPass:
        sig_name = "LumHeiAdjmtRowFirstPass"
        sig_start_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class BackRestSideSpprtAdjmtRowFirstDrvr:
        sig_name = "BackRestSideSpprtAdjmtRowFirstDrvr"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LumLenAdjmtRowFirstDrvr:
        sig_name = "LumLenAdjmtRowFirstDrvr"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BackRestSideSpprtAdjmtRowFirstPass:
        sig_name = "BackRestSideSpprtAdjmtRowFirstPass"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class LumHeiAdjmtRowFirstDrvr:
        sig_name = "LumHeiAdjmtRowFirstDrvr"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LumLenAdjmtRowFirstPass:
        sig_name = "LumLenAdjmtRowFirstPass"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class CemBodyFr131:
    msg_name = "CemBodyFr131"
    msg_id = 280
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.085
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class TrOpenPosnReqFromHmi:
        sig_name = "TrOpenPosnReqFromHmi"
        sig_start_bit = 14
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 14
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class TopPercTrFromHmi:
        sig_name = "TopPercTrFromHmi"
        sig_start_bit = 6
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 6
        byte = 0
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0


class SmpToBgmBodyDiagRespFrame:
    msg_name = "SmpToBgmBodyDiagRespFrame"
    msg_id = 1576
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class RrdmBodyFr01:
    msg_name = "RrdmBodyFr01"
    msg_id = 117
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DoorRiReHndlSts:
        sig_name = "DoorRiReHndlSts"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorHndlSts_Ukwn': 0, 'DoorHndlSts_FullRtrctd': 1, 'DoorHndlSts_MovgOut': 2, 'DoorHndlSts_StopDurgDply': 3, 'DoorHndlSts_FullDplyd': 4, 'DoorHndlSts_MovgIn': 5, 'DoorHndlSts_StopDurgRtrct': 6, 'DoorHndlSts_Flt': 7}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DoorRiReOpenReqInsdSwt1:
        sig_name = "DoorRiReOpenReqInsdSwt1"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorRiReCinhIntFailInfCinchFlt1:
        sig_name = "DoorRiReCinhIntFailInfCinchFlt1"
        sig_start_bit = 35
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ChdLockRightSts:
        sig_name = "ChdLockRightSts"
        sig_start_bit = 6
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class DoorRiReLatPawlSt:
        sig_name = "DoorRiReLatPawlSt"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorRiReLatPosn:
        sig_name = "DoorRiReLatPosn"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorPos_Undefined': 0, 'DoorPos_FullyClosed': 1, 'DoorPos_SecondaryPosition': 2, 'DoorPos_FullyOpen': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DoorRiReOpenLowReqOutdSwt1:
        sig_name = "DoorRiReOpenLowReqOutdSwt1"
        sig_start_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ShortDropWinReRiSts:
        sig_name = "ShortDropWinReRiSts"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShortDropSts_Idle': 0, 'ShortDropSts_WindowDown': 1, 'ShortDropSts_WindowClosed': 2, 'ShortDropSts_NotUsed': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorRiReCinhIntFailInfCinchRestFlt:
        sig_name = "DoorRiReCinhIntFailInfCinchRestFlt"
        sig_start_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class DoorRiReSwtLockgSts:
        sig_name = "DoorRiReSwtLockgSts"
        sig_start_bit = 14
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DoorRiReLockSts:
        sig_name = "DoorRiReLockSts"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WinFailrStsAtReRi:
        sig_name = "WinFailrStsAtReRi"
        sig_start_bit = 31
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WinPosnStsAtReRi:
        sig_name = "WinPosnStsAtReRi"
        sig_start_bit = 12
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 12
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0


class CcmBodyFr56:
    msg_name = "CcmBodyFr56"
    msg_id = 1163
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig12Byte5:
        sig_name = "CcmCaliSig12Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig12Byte7:
        sig_name = "CcmCaliSig12Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig12Byte2:
        sig_name = "CcmCaliSig12Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig12Byte4:
        sig_name = "CcmCaliSig12Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig12Byte3:
        sig_name = "CcmCaliSig12Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig12Byte0:
        sig_name = "CcmCaliSig12Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig12Byte6:
        sig_name = "CcmCaliSig12Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig12Byte1:
        sig_name = "CcmCaliSig12Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyFr55:
    msg_name = "CemBodyFr55"
    msg_id = 153
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.545
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HdRestAdjmtRowFirstPass:
        sig_name = "HdRestAdjmtRowFirstPass"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CushSideSpprtAdjmtRowFirstDrvr:
        sig_name = "CushSideSpprtAdjmtRowFirstDrvr"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HdRestHeiAdjmtRowFirstDrvr:
        sig_name = "HdRestHeiAdjmtRowFirstDrvr"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CushExtnFirstDrvr:
        sig_name = "CushExtnFirstDrvr"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HdRestAdjmtRowFirstDrvr:
        sig_name = "HdRestAdjmtRowFirstDrvr"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HdRestHeiAdjmtRowFirstPass:
        sig_name = "HdRestHeiAdjmtRowFirstPass"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HvahFltIndcnReq:
        sig_name = "HvahFltIndcnReq"
        sig_start_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CushExtnFirstPass:
        sig_name = "CushExtnFirstPass"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PassAirbSts:
        sig_name = "PassAirbSts"
        sig_start_bit = 47
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff2_On': 0, 'OnOff2_Off': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CushSideSpprtAdjmtRowFirstPass:
        sig_name = "CushSideSpprtAdjmtRowFirstPass"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class CcmBodyFr34:
    msg_name = "CcmBodyFr34"
    msg_id = 831
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CarTiIntForClima:
        sig_name = "CarTiIntForClima"
        sig_start_bit = 39
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class RlyCmftForClimaReq:
        sig_name = "RlyCmftForClimaReq"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class UBoostReqByClima:
        sig_name = "UBoostReqByClima"
        sig_start_bit = 20
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ClimaHeatgReqLvl:
        sig_name = "ClimaHeatgReqLvl"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattCoolgReq_NotReqd': 0, 'HvBattCoolgReq_LoReq': 1, 'HvBattCoolgReq_MedReq': 2, 'HvBattCoolgReq_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ClimaOvrHeatPrtSts:
        sig_name = "ClimaOvrHeatPrtSts"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ReHvacBlowerSts:
        sig_name = "ReHvacBlowerSts"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacFanSts_Off': 0, 'HvacFanSts_On': 1, 'HvacFanSts_Warning': 2, 'HvacFanSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ClimaCoolgReqLvl:
        sig_name = "ClimaCoolgReqLvl"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvBattCoolgReq_NotReqd': 0, 'HvBattCoolgReq_LoReq': 1, 'HvBattCoolgReq_MedReq': 2, 'HvBattCoolgReq_HiReq': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class CemBodyFr01:
    msg_name = "CemBodyFr01"
    msg_id = 32
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DoorLeReLockCmd:
        sig_name = "DoorLeReLockCmd"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 14
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockActvnSafe1_LockActvnOff': 0, 'LockActvnSafe1_LockActvnUnlck': 1, 'LockActvnSafe1_LockActvnLock': 2, 'LockActvnSafe1_LockActvnSafe': 3, 'LockActvnSafe1_LockActvnUnlckByCrash0': 12, 'LockActvnSafe1_LockActvnUnlckByCrash1': 4, 'LockActvnSafe1_LockActvnUnlckByCrash2': 8, 'LockActvnSafe1_LockActvnUnlckByCrash3': 14, 'LockActvnSafe1_LockActvnUnlckByCrash4': 13}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HmiSeatClimaHmiSeatHeatgForRowFirstRi:
        sig_name = "HmiSeatClimaHmiSeatHeatgForRowFirstRi"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HmiSeatClimaHmiSeatHeatgForRowFirstLe:
        sig_name = "HmiSeatClimaHmiSeatHeatgForRowFirstLe"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorRiReRelsReq:
        sig_name = "DoorRiReRelsReq"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class GlvBoxOpenReqFromUI:
        sig_name = "GlvBoxOpenReqFromUI"
        sig_start_bit = 18
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DigVideoRecSwt:
        sig_name = "DigVideoRecSwt"
        sig_start_bit = 17
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DoorPassLockCmd:
        sig_name = "DoorPassLockCmd"
        sig_start_bit = 23
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 14
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockActvnSafe1_LockActvnOff': 0, 'LockActvnSafe1_LockActvnUnlck': 1, 'LockActvnSafe1_LockActvnLock': 2, 'LockActvnSafe1_LockActvnSafe': 3, 'LockActvnSafe1_LockActvnUnlckByCrash0': 12, 'LockActvnSafe1_LockActvnUnlckByCrash1': 4, 'LockActvnSafe1_LockActvnUnlckByCrash2': 8, 'LockActvnSafe1_LockActvnUnlckByCrash3': 14, 'LockActvnSafe1_LockActvnUnlckByCrash4': 13}
        compute_method = None
        length = 4
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HmiSeatClimaHmiSeatVentnForRowFirstRi:
        sig_name = "HmiSeatClimaHmiSeatVentnForRowFirstRi"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HmiSeatClimaHmiSeatHeatgForRowSecRi:
        sig_name = "HmiSeatClimaHmiSeatHeatgForRowSecRi"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HmiSeatClimaHmiSeatHeatgForRowSecLe:
        sig_name = "HmiSeatClimaHmiSeatHeatgForRowSecLe"
        sig_start_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HmiSeatClimaHmiSeatVentnForRowFirstLe:
        sig_name = "HmiSeatClimaHmiSeatVentnForRowFirstLe"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorDrvrLockCmd:
        sig_name = "DoorDrvrLockCmd"
        sig_start_bit = 7
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 14
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockActvnSafe1_LockActvnOff': 0, 'LockActvnSafe1_LockActvnUnlck': 1, 'LockActvnSafe1_LockActvnLock': 2, 'LockActvnSafe1_LockActvnSafe': 3, 'LockActvnSafe1_LockActvnUnlckByCrash0': 12, 'LockActvnSafe1_LockActvnUnlckByCrash1': 4, 'LockActvnSafe1_LockActvnUnlckByCrash2': 8, 'LockActvnSafe1_LockActvnUnlckByCrash3': 14, 'LockActvnSafe1_LockActvnUnlckByCrash4': 13}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DoorRiReLockCmd:
        sig_name = "DoorRiReLockCmd"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 14
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockActvnSafe1_LockActvnOff': 0, 'LockActvnSafe1_LockActvnUnlck': 1, 'LockActvnSafe1_LockActvnLock': 2, 'LockActvnSafe1_LockActvnSafe': 3, 'LockActvnSafe1_LockActvnUnlckByCrash0': 12, 'LockActvnSafe1_LockActvnUnlckByCrash1': 4, 'LockActvnSafe1_LockActvnUnlckByCrash2': 8, 'LockActvnSafe1_LockActvnUnlckByCrash3': 14, 'LockActvnSafe1_LockActvnUnlckByCrash4': 13}
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HmiSeatClimaHmiSeatVentnForRowSecLe:
        sig_name = "HmiSeatClimaHmiSeatVentnForRowSecLe"
        sig_start_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DoorPassRelsReq:
        sig_name = "DoorPassRelsReq"
        sig_start_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 35
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HmiSeatClimaHmiSeatVentnForRowSecRi:
        sig_name = "HmiSeatClimaHmiSeatVentnForRowSecRi"
        sig_start_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorLeReRelsReq:
        sig_name = "DoorLeReRelsReq"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class IndcrSts:
        sig_name = "IndcrSts"
        sig_start_bit = 58
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IndcrSts1_Off': 0, 'IndcrSts1_LeOn': 1, 'IndcrSts1_RiOn': 2, 'IndcrSts1_LeAndRiOn': 3}
        compute_method = None
        length = 2
        startbit = 58
        byte = 7
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class DoorDrvrRelsReq:
        sig_name = "DoorDrvrRelsReq"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CemBodyFr99:
    msg_name = "CemBodyFr99"
    msg_id = 827
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.24
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ErsCmdByKey:
        sig_name = "ErsCmdByKey"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ErsCmd_ErsCmdNotSet': 0, 'ErsCmd_ErsCmdOn': 1, 'ErsCmd_ErsCmdOff': 2}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class ClimaCmd:
        sig_name = "ClimaCmd"
        sig_start_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OkNotOk_NotOk': 0, 'OkNotOk_Ok': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RainfallAmnt:
        sig_name = "RainfallAmnt"
        sig_start_bit = 43
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 14
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AmntSnsr_Amnt': 0, 'AmntSnsr_InitValue': 14, 'AmntSnsr_Error': 15}
        compute_method = None
        length = 4
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class TInCooltAtStrtOfClima:
        sig_name = "TInCooltAtStrtOfClima"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = "-40.0"
        sig_value_min = 0
        sig_value_max = 255
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


class CEMBodyFr36:
    msg_name = "CEMBodyFr36"
    msg_id = 849
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VFCInfoEna:
        sig_name = "VFCInfoEna"
        sig_start_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisableCoding_Disabled': 0, 'EnableDisableCoding_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DrvrSeatHallPosExtDownLdSeatHeadrHozlPos:
        sig_name = "DrvrSeatHallPosExtDownLdSeatHeadrHozlPos"
        sig_start_bit = 13
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11110000, 0b00001111, 4, 4)]

    class DrvrSeatHallPosExtDownLdSeatCushExtPos:
        sig_name = "DrvrSeatHallPosExtDownLdSeatCushExtPos"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class HmiPopUpResp:
        sig_name = "HmiPopUpResp"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BookChargeSetResponse_Default': 0, 'BookChargeSetResponse_Success': 1, 'BookChargeSetResponse_Cancelled': 2, 'BookChargeSetResponse_Fail': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DrvrSeatHallPosExtDownLdSeatHeadrVertPos:
        sig_name = "DrvrSeatHallPosExtDownLdSeatHeadrVertPos"
        sig_start_bit = 19
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111100, 0b00000011, 6, 2)]


class PotToBgmBodyDiagRespFrame:
    msg_name = "PotToBgmBodyDiagRespFrame"
    msg_id = 1557
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CcmBodyFr30:
    msg_name = "CcmBodyFr30"
    msg_id = 1025
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class HvacHeatrInletTempReqEvaprTQf:
        sig_name = "HvacHeatrInletTempReqEvaprTQf"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvacHexAirTHvacAirTForHeatrFrntQf:
        sig_name = "HvacHexAirTHvacAirTForHeatrFrntQf"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OkNotOk_NotOk': 0, 'OkNotOk_Ok': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvacHexAirTHvacAirTForHeatrFrnt:
        sig_name = "HvacHexAirTHvacAirTForHeatrFrnt"
        sig_start_bit = 20
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvacHeatrInletTempReqEvaprTFrnt:
        sig_name = "HvacHeatrInletTempReqEvaprTFrnt"
        sig_start_bit = 4
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvacHeatgReq:
        sig_name = "HvacHeatgReq"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ClimaActvAlrmSts:
        sig_name = "ClimaActvAlrmSts"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvacHeatElmAirMFlowEstimd:
        sig_name = "HvacHeatElmAirMFlowEstimd"
        sig_start_bit = 39
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class CcmRollgCntrSts:
        sig_name = "CcmRollgCntrSts"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyFr52:
    msg_name = "CemBodyFr52"
    msg_id = 356
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.285
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class IntelliClimaModDistbnReq:
        sig_name = "IntelliClimaModDistbnReq"
        sig_start_bit = 33
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaCmptmtAirTEstimd:
        sig_name = "IntelliClimaCmptmtAirTEstimd"
        sig_start_bit = 31
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 1850
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class IntelliClimaFanSpdReq:
        sig_name = "IntelliClimaFanSpdReq"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 20
        sig_value_offset = 300
        sig_value_min = 0
        sig_value_max = 255
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

    class IntelliClimaActrPosnTempRiFrnt:
        sig_name = "IntelliClimaActrPosnTempRiFrnt"
        sig_start_bit = 9
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaActrPosnTempLeFrnt:
        sig_name = "IntelliClimaActrPosnTempLeFrnt"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class IntelliClimaRecFlapPosnReq:
        sig_name = "IntelliClimaRecFlapPosnReq"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class SwtlPrivateDHUCanFr02:
    msg_name = "SwtlPrivateDHUCanFr02"
    msg_id = 773
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class SteerWhlTouchTurnLightSwtRi:
        sig_name = "SteerWhlTouchTurnLightSwtRi"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotAvailable': 0, 'LightPress': 1, 'FullPress': 2, 'Error': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SteerWhlTouchBdCrsResuQf1:
        sig_name = "SteerWhlTouchBdCrsResuQf1"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlTouchBdCnclQf1:
        sig_name = "SteerWhlTouchBdCnclQf1"
        sig_start_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerWhlTouchBdCnclCntr:
        sig_name = "SteerWhlTouchBdCnclCntr"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SteerWhlTouchBdCnclSteerWhlTouchBdSts:
        sig_name = "SteerWhlTouchBdCnclSteerWhlTouchBdSts"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchBdSts_NotActive': 0, 'SteerWhlTouchBdSts_Touch': 1, 'SteerWhlTouchBdSts_TouchAndPress': 2, 'SteerWhlTouchBdSts_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlTouchBdCrsResuSteerWhlTouchBdSts:
        sig_name = "SteerWhlTouchBdCrsResuSteerWhlTouchBdSts"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchBdSts_NotActive': 0, 'SteerWhlTouchBdSts_Touch': 1, 'SteerWhlTouchBdSts_TouchAndPress': 2, 'SteerWhlTouchBdSts_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerWhlTouchTurnLightSwtLe:
        sig_name = "SteerWhlTouchTurnLightSwtLe"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NotAvailable': 0, 'LightPress': 1, 'FullPress': 2, 'Error': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SteerWhlTouchBdADAS:
        sig_name = "SteerWhlTouchBdADAS"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerWhlTouchBdSts_NotActive': 0, 'SteerWhlTouchBdSts_Touch': 1, 'SteerWhlTouchBdSts_TouchAndPress': 2, 'SteerWhlTouchBdSts_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerWhlTouchBdCnclChks:
        sig_name = "SteerWhlTouchBdCnclChks"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CcmBodyFr46:
    msg_name = "CcmBodyFr46"
    msg_id = 1153
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig2Byte4:
        sig_name = "CcmCaliSig2Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig2Byte1:
        sig_name = "CcmCaliSig2Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig2Byte5:
        sig_name = "CcmCaliSig2Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig2Byte7:
        sig_name = "CcmCaliSig2Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig2Byte6:
        sig_name = "CcmCaliSig2Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig2Byte2:
        sig_name = "CcmCaliSig2Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig2Byte0:
        sig_name = "CcmCaliSig2Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig2Byte3:
        sig_name = "CcmCaliSig2Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class SmdBodyFr05:
    msg_name = "SmdBodyFr05"
    msg_id = 272
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DrvrSeatPosPercSeatPosFrntHeiPerc:
        sig_name = "DrvrSeatPosPercSeatPosFrntHeiPerc"
        sig_start_bit = 15
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11000000, 0b00111111, 2, 6)]

    class DrvrSeatPosPercSeatPosHeiQF:
        sig_name = "DrvrSeatPosPercSeatPosHeiQF"
        sig_start_bit = 19
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DrvrSeatPosPercSeatPosSldQF:
        sig_name = "DrvrSeatPosPercSeatPosSldQF"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DrvrSeatExtAdjAllowd:
        sig_name = "DrvrSeatExtAdjAllowd"
        sig_start_bit = 3
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class DrvrSeatPosPercSeatPosSldPerc:
        sig_name = "DrvrSeatPosPercSeatPosSldPerc"
        sig_start_bit = 39
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]

    class DrvrSeatPosPercSeatPosFrntHeiQF:
        sig_name = "DrvrSeatPosPercSeatPosFrntHeiQF"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DrvrSeatPosPercSeatPosHeiPerc:
        sig_name = "DrvrSeatPosPercSeatPosHeiPerc"
        sig_start_bit = 17
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class CEMBodyFr12:
    msg_name = "CEMBodyFr12"
    msg_id = 240
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class VehModMngtGlbSafe1PwrLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DoorDrvrHndlCmd:
        sig_name = "DoorDrvrHndlCmd"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorHndlCmd_Idle': 0, 'DoorHndlCmd_Deploy': 1, 'DoorHndlCmd_Retract': 2}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class OnBdChrgrHndlSts1:
        sig_name = "OnBdChrgrHndlSts1"
        sig_start_bit = 59
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_value_init = 8
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnBdChrgrHndlSts1_Disconnected': 0, 'OnBdChrgrHndlSts1_ConnectedWithoutPower': 1, 'OnBdChrgrHndlSts1_PowerAvailableButNotActivated': 2, 'OnBdChrgrHndlSts1_ConnectedWithPower': 3, 'OnBdChrgrHndlSts1_DischargeConnectwithoutpowerincar': 4, 'OnBdChrgrHndlSts1_DischargeConnectwithoutpoweroutcar': 5, 'OnBdChrgrHndlSts1_DischargeConnectwithpowerincar': 6, 'OnBdChrgrHndlSts1_DischargeConnectwithpoweroutcar': 7, 'OnBdChrgrHndlSts1_Init': 8, 'OnBdChrgrHndlSts1_Fault': 9, 'OnBdChrgrHndlSts1_NotCompleteConnnected': 10, 'OnBdChrgrHndlSts1_Reserved0': 11, 'OnBdChrgrHndlSts1_Reserved1': 12, 'OnBdChrgrHndlSts1_Reserved2': 13}
        compute_method = None
        length = 4
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1EgyLvlElecSubtyp:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehModMngtGlbSafe1PwrLvlElecMai:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecMai"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DrvrCtrlOfPassSeatFrntReqd:
        sig_name = "DrvrCtrlOfPassSeatFrntReqd"
        sig_start_bit = 60
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
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class VehModMngtGlbSafe1UsgModSts:
        sig_name = "VehModMngtGlbSafe1UsgModSts"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
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

    class VehModMngtGlbSafe1CarModSts1:
        sig_name = "VehModMngtGlbSafe1CarModSts1"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CarModSts1_CarModNorm': 0, 'CarModSts1_CarModTrnsp': 1, 'CarModSts1_CarModFcy': 2, 'CarModSts1_CarModCrash': 3, 'CarModSts1_CarModDyno': 5}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp:
        sig_name = "VehModMngtGlbSafe1CarModSubtypWdCarModSubtyp"
        sig_start_bit = 5
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 5
        byte = 0
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class DoorLeReHndlCmd:
        sig_name = "DoorLeReHndlCmd"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorHndlCmd_Idle': 0, 'DoorHndlCmd_Deploy': 1, 'DoorHndlCmd_Retract': 2}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehModMngtGlbSafe1Cntr:
        sig_name = "VehModMngtGlbSafe1Cntr"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class VehModMngtGlbSafe1EgyLvlElecMai:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehModMngtGlbSafe1Chks:
        sig_name = "VehModMngtGlbSafe1Chks"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class VehModMngtGlbSafe1FltEgyCnsWdSts:
        sig_name = "VehModMngtGlbSafe1FltEgyCnsWdSts"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltEgyCns1_NoFlt': 0, 'FltEgyCns1_Flt': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DoorPassHndlCmd:
        sig_name = "DoorPassHndlCmd"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorHndlCmd_Idle': 0, 'DoorHndlCmd_Deploy': 1, 'DoorHndlCmd_Retract': 2}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorRiReHndlCmd:
        sig_name = "DoorRiReHndlCmd"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorHndlCmd_Idle': 0, 'DoorHndlCmd_Deploy': 1, 'DoorHndlCmd_Retract': 2}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class PdmBodyFr03:
    msg_name = "PdmBodyFr03"
    msg_id = 293
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class WinFailrStsAtPass:
        sig_name = "WinFailrStsAtPass"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class MirrPosnToCldAtPassMirrPosnAdjCldUpDwn:
        sig_name = "MirrPosnToCldAtPassMirrPosnAdjCldUpDwn"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 180
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

    class MirrDefrstAtPassSts:
        sig_name = "MirrDefrstAtPassSts"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DoorPassCinhIntFailInfCinchFlt1:
        sig_name = "DoorPassCinhIntFailInfCinchFlt1"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AmbTURawAtPassSide:
        sig_name = "AmbTURawAtPassSide"
        sig_start_bit = 55
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = "-70"
        sig_value_min = 0
        sig_value_max = 4095
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11110000, 0b00001111, 4, 4)]

    class DoorPassCinhIntFailInfCinchRestFlt:
        sig_name = "DoorPassCinhIntFailInfCinchRestFlt"
        sig_start_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AmbTRawAtPassSideAmbTVal:
        sig_name = "AmbTRawAtPassSideAmbTVal"
        sig_start_bit = 26
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-70.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 26
        bmuws_info = [(3, 0b00000111, 0b11111000, 3, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class MirrPosnToCldAtPassMirrPosnAdjCldLeRi:
        sig_name = "MirrPosnToCldAtPassMirrPosnAdjCldLeRi"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 180
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

    class DoorPassHndlSts:
        sig_name = "DoorPassHndlSts"
        sig_start_bit = 19
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorHndlSts_Ukwn': 0, 'DoorHndlSts_FullRtrctd': 1, 'DoorHndlSts_MovgOut': 2, 'DoorHndlSts_StopDurgDply': 3, 'DoorHndlSts_FullDplyd': 4, 'DoorHndlSts_MovgIn': 5, 'DoorHndlSts_StopDurgRtrct': 6, 'DoorHndlSts_Flt': 7}
        compute_method = None
        length = 3
        startbit = 19
        byte = 2
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class AmbTRawAtPassSideQly:
        sig_name = "AmbTRawAtPassSideQly"
        sig_start_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class CcmBodyFr55:
    msg_name = "CcmBodyFr55"
    msg_id = 1162
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig11Byte2:
        sig_name = "CcmCaliSig11Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig11Byte3:
        sig_name = "CcmCaliSig11Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig11Byte1:
        sig_name = "CcmCaliSig11Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig11Byte5:
        sig_name = "CcmCaliSig11Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig11Byte6:
        sig_name = "CcmCaliSig11Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig11Byte4:
        sig_name = "CcmCaliSig11Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig11Byte0:
        sig_name = "CcmCaliSig11Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig11Byte7:
        sig_name = "CcmCaliSig11Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyFr80:
    msg_name = "CemBodyFr80"
    msg_id = 1045
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.6
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ResrvdSigForCCM4:
        sig_name = "ResrvdSigForCCM4"
        sig_start_bit = 39
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ResrvdSigForCCM2:
        sig_name = "ResrvdSigForCCM2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ResrvdSigForCCM1:
        sig_name = "ResrvdSigForCCM1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ResrvdSigForCCM3:
        sig_name = "ResrvdSigForCCM3"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class CcmBodyFr57:
    msg_name = "CcmBodyFr57"
    msg_id = 805
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CmptmtTReCmptmtTFrntQf:
        sig_name = "CmptmtTReCmptmtTFrntQf"
        sig_start_bit = 20
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptmtTFrntQf_SnsrDataUndefd': 0, 'CmptmtTFrntQf_FanNotRunning': 1, 'CmptmtTFrntQf_SnsrDataNotOk': 2, 'CmptmtTFrntQf_SnsrDataOk': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class EvaprTReEvaprTFrnt:
        sig_name = "EvaprTReEvaprTFrnt"
        sig_start_bit = 4
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class CmptmtTReCmptmtTFrnt:
        sig_name = "CmptmtTReCmptmtTFrnt"
        sig_start_bit = 18
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 1850
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class EvaprTReEvaprTQf:
        sig_name = "EvaprTReEvaprTQf"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CmptmtTReFanForCmptmtTRunng:
        sig_name = "CmptmtTReFanForCmptmtTRunng"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class SmdBodyFr04:
    msg_name = "SmdBodyFr04"
    msg_id = 665
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DrvrMassgRunng:
        sig_name = "DrvrMassgRunng"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DrvrSeatHeatgLvlSts:
        sig_name = "DrvrSeatHeatgLvlSts"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DrvrSeatActvSpplFct:
        sig_name = "DrvrSeatActvSpplFct"
        sig_start_bit = 47
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatActvSpplFct1_NotAvl': 0, 'SeatActvSpplFct1_LumExtnAndLumHei': 1, 'SeatActvSpplFct1_BackBlster': 2, 'SeatActvSpplFct1_CushExtn': 3, 'SeatActvSpplFct1_HdrestHeiAndHdrestTilt': 4, 'SeatActvSpplFct1_MassgFct': 5, 'SeatActvSpplFct1_ShoulderFct': 6, 'SeatActvSpplFct1_LegrestFct': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class DrvrSeatVentAvlSts:
        sig_name = "DrvrSeatVentAvlSts"
        sig_start_bit = 6
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StsFd_None': 0, 'StsFd_On': 1, 'StsFd_Off': 2, 'StsFd_Error': 3, 'StsFd_Functionallimit': 4, 'StsFd_Energylimit': 5, 'StsFd_Resvd1': 6, 'StsFd_Resvd2': 7}
        compute_method = None
        length = 3
        startbit = 6
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DrvrSeatHeatgAvlSts:
        sig_name = "DrvrSeatHeatgAvlSts"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StsFd_None': 0, 'StsFd_On': 1, 'StsFd_Off': 2, 'StsFd_Error': 3, 'StsFd_Functionallimit': 4, 'StsFd_Energylimit': 5, 'StsFd_Resvd1': 6, 'StsFd_Resvd2': 7}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DrvrSeatHeatgDesPwrCns:
        sig_name = "DrvrSeatHeatgDesPwrCns"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DrvrSeatVentnLvlSts:
        sig_name = "DrvrSeatVentnLvlSts"
        sig_start_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class DrvrSeatHeatgActlPwrCns:
        sig_name = "DrvrSeatHeatgActlPwrCns"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class BgmToPdmBodyDiagReqFrame:
    msg_name = "BgmToPdmBodyDiagReqFrame"
    msg_id = 1811
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class EtcmToBgmBodyDiagRespFrame:
    msg_name = "EtcmToBgmBodyDiagRespFrame"
    msg_id = 1558
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CcmBodyFr37:
    msg_name = "CcmBodyFr37"
    msg_id = 860
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmIntelliClimaResd13:
        sig_name = "CcmIntelliClimaResd13"
        sig_start_bit = 15
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class CcmIntelliClimaResd3:
        sig_name = "CcmIntelliClimaResd3"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmIntelliClimaResd7:
        sig_name = "CcmIntelliClimaResd7"
        sig_start_bit = 47
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]


class CcmBodyFr15:
    msg_name = "CcmBodyFr15"
    msg_id = 1033
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class HvacAirTForRowFirstAtVentLeEvaprTQf:
        sig_name = "HvacAirTForRowFirstAtVentLeEvaprTQf"
        sig_start_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvacAirTForRowFirstAtVentRiEvaprTQf:
        sig_name = "HvacAirTForRowFirstAtVentRiEvaprTQf"
        sig_start_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvacAirTForRowFirstAtFlrRiEvaprTFrnt:
        sig_name = "HvacAirTForRowFirstAtFlrRiEvaprTFrnt"
        sig_start_bit = 20
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowFirstAtFlrLeEvaprTFrnt:
        sig_name = "HvacAirTForRowFirstAtFlrLeEvaprTFrnt"
        sig_start_bit = 4
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowFirstAtFlrLeEvaprTQf:
        sig_name = "HvacAirTForRowFirstAtFlrLeEvaprTQf"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvacAirTForRowFirstAtVentLeEvaprTFrnt:
        sig_name = "HvacAirTForRowFirstAtVentLeEvaprTFrnt"
        sig_start_bit = 36
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowFirstAtVentRiEvaprTFrnt:
        sig_name = "HvacAirTForRowFirstAtVentRiEvaprTFrnt"
        sig_start_bit = 52
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowFirstAtFlrRiEvaprTQf:
        sig_name = "HvacAirTForRowFirstAtFlrRiEvaprTQf"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class PdmToBgmBodyDiagRespuFrame:
    msg_name = "PdmToBgmBodyDiagRespuFrame"
    msg_id = 1555
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CcmBodyFr49:
    msg_name = "CcmBodyFr49"
    msg_id = 1156
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig5Byte1:
        sig_name = "CcmCaliSig5Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig5Byte6:
        sig_name = "CcmCaliSig5Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig5Byte5:
        sig_name = "CcmCaliSig5Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig5Byte2:
        sig_name = "CcmCaliSig5Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig5Byte7:
        sig_name = "CcmCaliSig5Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig5Byte0:
        sig_name = "CcmCaliSig5Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig5Byte4:
        sig_name = "CcmCaliSig5Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig5Byte3:
        sig_name = "CcmCaliSig5Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CcmBodyFr20:
    msg_name = "CcmBodyFr20"
    msg_id = 933
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class HvacFanSet2HvacFanSpd2:
        sig_name = "HvacFanSet2HvacFanSpd2"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class HvacFanSts2HvacFanBattU2:
        sig_name = "HvacFanSts2HvacFanBattU2"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 254
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

    class HvacFanSts3HvacFanBattI:
        sig_name = "HvacFanSts3HvacFanBattI"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 0.15
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class HvacFanSts2HvacFanBattI2:
        sig_name = "HvacFanSts2HvacFanBattI2"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 253
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

    class HvacFanSts3HvacFanBattU:
        sig_name = "HvacFanSts3HvacFanBattU"
        sig_start_bit = 9
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class HvacFanSts3HvacFanSpdFd:
        sig_name = "HvacFanSts3HvacFanSpdFd"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 20
        sig_value_offset = 300
        sig_value_min = 0
        sig_value_max = 255
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


class CemBodyFr78:
    msg_name = "CemBodyFr78"
    msg_id = 180
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DoorOpenerLeReReqCntr:
        sig_name = "DoorOpenerLeReReqCntr"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DoorOpenerDrvrReqChks:
        sig_name = "DoorOpenerDrvrReqChks"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class MobDevVentReq:
        sig_name = "MobDevVentReq"
        sig_start_bit = 59
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DoorOpenerDrvrReqDoorOpenerReq:
        sig_name = "DoorOpenerDrvrReqDoorOpenerReq"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerIdle': 0, 'DoorOpenerOpen': 1, 'DoorOpenerCls': 2, 'DoorOpenerStop': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorOpenerDrvrReqCntr:
        sig_name = "DoorOpenerDrvrReqCntr"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class SceneModSeld:
        sig_name = "SceneModSeld"
        sig_start_bit = 63
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 13
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PatSeld_NoSeld': 0, 'PatSeld_RefrshPatSeld': 1, 'PatSeld_ParentchildPatSeld': 2, 'PatSeld_Restpatseld': 3, 'PatSeld_RomanticPatseld': 4, 'PatSeld_StrangerPatseld': 5, 'PatSeld_TheaterPatseld': 6, 'PatSeld_PetPatseld': 7, 'PatSeld_BiochalPatseld': 8, 'PatSeld_CarWashPatseld': 9, 'PatSeld_EcoPatseld': 10, 'PatSeld_KingPatseld': 11, 'PatSeld_CustomizationPatseld': 12, 'PatSeld_MeetingPatseld': 13}
        compute_method = None
        length = 4
        startbit = 63
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DoorOpenerDrvrReqTrigSrc:
        sig_name = "DoorOpenerDrvrReqTrigSrc"
        sig_start_bit = 14
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoTrigSrc': 0, 'KeyRem': 1, 'HMI': 2, 'Telm': 3, 'OutdSwt': 4, 'InsdSwt': 5}
        compute_method = None
        length = 3
        startbit = 14
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DoorOpenerLeReReqDoorOpenerReq:
        sig_name = "DoorOpenerLeReReqDoorOpenerReq"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerIdle': 0, 'DoorOpenerOpen': 1, 'DoorOpenerCls': 2, 'DoorOpenerStop': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorOpenerLeReReqChks:
        sig_name = "DoorOpenerLeReReqChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DoorOpenerLeReReqTrigSrc:
        sig_name = "DoorOpenerLeReReqTrigSrc"
        sig_start_bit = 38
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoTrigSrc': 0, 'KeyRem': 1, 'HMI': 2, 'Telm': 3, 'OutdSwt': 4, 'InsdSwt': 5}
        compute_method = None
        length = 3
        startbit = 38
        byte = 4
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class CemBodyFr73:
    msg_name = "CemBodyFr73"
    msg_id = 152
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.065
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HvEgyCnsAllwdForClima:
        sig_name = "HvEgyCnsAllwdForClima"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 50.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class DrvrDesDirCntr:
        sig_name = "DrvrDesDirCntr"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class DrvrDesDirChks:
        sig_name = "DrvrDesDirChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class OnBdChrgrSt:
        sig_name = "OnBdChrgrSt"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 12
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ChrgrSts1_Idle': 0, 'ChrgrSts1_PreStrt': 1, 'ChrgrSts1_Chrgn': 2, 'ChrgrSts1_Alrm': 3, 'ChrgrSts1_Srv': 4, 'ChrgrSts1_Diagc': 5, 'ChrgrSts1_Boot': 6, 'ChrgrSts1_Rstrt': 7, 'ChrgrSts1_DisChrgn': 8, 'ChrgrSts1_BookChrgn': 9, 'ChrgrSts1_Shutdown': 10, 'ChrgrSts1_Heating': 11, 'ChrgrSts1_Cooling': 12}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DrvrDesDirDrvrDesDir:
        sig_name = "DrvrDesDirDrvrDesDir"
        sig_start_bit = 51
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvrDesDir1_Undefd': 0, 'DrvrDesDir1_Fwd': 1, 'DrvrDesDir1_Rvs': 2, 'DrvrDesDir1_Neut': 3, 'DrvrDesDir1_Resd0': 4, 'DrvrDesDir1_Resd1': 5, 'DrvrDesDir1_Resd2': 6, 'DrvrDesDir1_Resd3': 7}
        compute_method = None
        length = 3
        startbit = 51
        byte = 6
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class CbnOverHeatProtnEnaFromTelm:
        sig_name = "CbnOverHeatProtnEnaFromTelm"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class SmdBodyFr03:
    msg_name = "SmdBodyFr03"
    msg_id = 1193
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DrvrSeatHallPosUpldSeatInclPos:
        sig_name = "DrvrSeatHallPosUpldSeatInclPos"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class DrvrSeatHallPosUpldSeatSldPos:
        sig_name = "DrvrSeatHallPosUpldSeatSldPos"
        sig_start_bit = 3
        sig_length = 12
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 3
        bmuws_info = [(0, 0b00001111, 0b11110000, 4, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class DrvrSeatHallPosUpldSeatHeiPos:
        sig_name = "DrvrSeatHallPosUpldSeatHeiPos"
        sig_start_bit = 33
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DrvrSeatHallPosUpldSeatFrntHeiPos:
        sig_name = "DrvrSeatHallPosUpldSeatFrntHeiPos"
        sig_start_bit = 49
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 49
        bmuws_info = [(6, 0b00000011, 0b11111100, 2, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class CcmBodyFr21:
    msg_name = "CcmBodyFr21"
    msg_id = 1037
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class ResrvdSigForECM3:
        sig_name = "ResrvdSigForECM3"
        sig_start_bit = 31
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class WindIceDetdFrnt:
        sig_name = "WindIceDetdFrnt"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ResrvdSigForECM4:
        sig_name = "ResrvdSigForECM4"
        sig_start_bit = 47
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class WindIceDetdRe:
        sig_name = "WindIceDetdRe"
        sig_start_bit = 18
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ResrvdSigForECM2:
        sig_name = "ResrvdSigForECM2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ResrvdSigForECM1:
        sig_name = "ResrvdSigForECM1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RemClimaWarn:
        sig_name = "RemClimaWarn"
        sig_start_bit = 59
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaWarn_NoWarn': 0, 'ClimaWarn_FuLo': 1, 'ClimaWarn_BattLo': 2, 'ClimaWarn_FuAndBattLo': 3, 'ClimaWarn_TLo': 4, 'ClimaWarn_THi': 5, 'ClimaWarn_Error': 6, 'ClimaWarn_HVError': 7, 'ClimaWarn_ActvnLimd': 8}
        compute_method = None
        length = 4
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class CemBodyFr49:
    msg_name = "CemBodyFr49"
    msg_id = 944
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.285
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HmiElecAirDirCrtlReqPassLePosY:
        sig_name = "HmiElecAirDirCrtlReqPassLePosY"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class HmiElecAirDirCrtlReqPassRiPosY:
        sig_name = "HmiElecAirDirCrtlReqPassRiPosY"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class HmiElecAirDirCrtlReqDrvrLePosX:
        sig_name = "HmiElecAirDirCrtlReqDrvrLePosX"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class HmiElecAirDirCrtlReqPassRiPosX:
        sig_name = "HmiElecAirDirCrtlReqPassRiPosX"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class HmiElecAirDirCrtlReqDrvrRiPosY:
        sig_name = "HmiElecAirDirCrtlReqDrvrRiPosY"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class HmiElecAirDirCrtlReqDrvrRiPosX:
        sig_name = "HmiElecAirDirCrtlReqDrvrRiPosX"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class HmiElecAirDirCrtlReqDrvrLePosY:
        sig_name = "HmiElecAirDirCrtlReqDrvrLePosY"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class HmiElecAirDirCrtlReqPassLePosX:
        sig_name = "HmiElecAirDirCrtlReqPassLePosX"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class DdmBodyFr04:
    msg_name = "DdmBodyFr04"
    msg_id = 5
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class MirrPosnFromCldAtPassFb:
        sig_name = "MirrPosnFromCldAtPassFb"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DoorDrvrLatPawlSt:
        sig_name = "DoorDrvrLatPawlSt"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorDrvrLatPosn:
        sig_name = "DoorDrvrLatPosn"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorPos_Undefined': 0, 'DoorPos_FullyClosed': 1, 'DoorPos_SecondaryPosition': 2, 'DoorPos_FullyOpen': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class MirrPosnFromCldAtDrvrFb:
        sig_name = "MirrPosnFromCldAtDrvrFb"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DoorDrvrOpenLowReqOutdSwt1:
        sig_name = "DoorDrvrOpenLowReqOutdSwt1"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class MirrBtnPsdAtDrvr:
        sig_name = "MirrBtnPsdAtDrvr"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class MirrPosnDownLdSts:
        sig_name = "MirrPosnDownLdSts"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorDrvrOpenReqInsdSwt1:
        sig_name = "DoorDrvrOpenReqInsdSwt1"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ChdPrtnLeftFailStsToHmi:
        sig_name = "ChdPrtnLeftFailStsToHmi"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class WinPosnStsAtDrvr:
        sig_name = "WinPosnStsAtDrvr"
        sig_start_bit = 39
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 39
        byte = 4
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class MirrAtDrvrInMovmt:
        sig_name = "MirrAtDrvrInMovmt"
        sig_start_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DoorDrvrLockSts:
        sig_name = "DoorDrvrLockSts"
        sig_start_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ChdPrtnLeftStsToHmi:
        sig_name = "ChdPrtnLeftStsToHmi"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorDrvrSwtIntrLockgReq:
        sig_name = "DoorDrvrSwtIntrLockgReq"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockgCenReq2_Idle': 0, 'LockgCenReq2_Unlck': 1, 'LockgCenReq2_Lock': 2}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class MirrPosnMemSts:
        sig_name = "MirrPosnMemSts"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class SwtrPrivateDHUCanFr06:
    msg_name = "SwtrPrivateDHUCanFr06"
    msg_id = 56
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DiagcFailrTouchPanSWTRSnsrFltSts:
        sig_name = "DiagcFailrTouchPanSWTRSnsrFltSts"
        sig_start_bit = 6
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SnsrFltSts_NoFlt': 0, 'SnsrFltSts_FSnsrInvld': 1, 'SnsrFltSts_FSnsrShoCircToGnd': 2, 'SnsrFltSts_FSnsrShoCircToBatt': 3, 'SnsrFltSts_FSnsrOpenCirc': 4}
        compute_method = None
        length = 3
        startbit = 6
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DiagcFailrTouchPanSWTRVibrationFltSts:
        sig_name = "DiagcFailrTouchPanSWTRVibrationFltSts"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltSts_NoFlt': 0, 'FltSts_VibrationShoCirc': 1, 'FltSts_VibrationOpenCirc': 2, 'FltSts_invalid': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DiagcFailrTouchPanSWTRTouchdFltSts:
        sig_name = "DiagcFailrTouchPanSWTRTouchdFltSts"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltSts_NoFlt': 0, 'FltSts_TouchdInvld': 1, 'FltSts_TouchdOutdOfRng': 2}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DiagcFailrTouchPanSWTRCmnFltSts:
        sig_name = "DiagcFailrTouchPanSWTRCmnFltSts"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmnFltSts_NoFlt': 0, 'CmnFltSts_OutdURng': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class BgmToSwtlBodyDiagReqFrame:
    msg_name = "BgmToSwtlBodyDiagReqFrame"
    msg_id = 1922
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyFr69:
    msg_name = "CemBodyFr69"
    msg_id = 196
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DoorOpenwarnRiIndcn:
        sig_name = "DoorOpenwarnRiIndcn"
        sig_start_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LcmaIndcn_NoLcmaWarn': 0, 'LcmaIndcn_LcmaWarnLvl1': 1, 'LcmaIndcn_NotUsed': 2, 'LcmaIndcn_LcmaWarnLvl2': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RctaIndcnRi:
        sig_name = "RctaIndcnRi"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LcmaIndcn_NoLcmaWarn': 0, 'LcmaIndcn_LcmaWarnLvl1': 1, 'LcmaIndcn_NotUsed': 2, 'LcmaIndcn_LcmaWarnLvl2': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadAndStoreReqInOutEasy:
        sig_name = "LoadAndStoreReqInOutEasy"
        sig_start_bit = 28
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
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class LoadAndStoreReqErgoPosn:
        sig_name = "LoadAndStoreReqErgoPosn"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MemPosn_ProfPosn': 0, 'MemPosn_MemBnk1': 1, 'MemPosn_MemBnk2': 2, 'MemPosn_MemBnk3': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class LoadAndStoreReqIdPen:
        sig_name = "LoadAndStoreReqIdPen"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DoorOpenwarnLeIndcn:
        sig_name = "DoorOpenwarnLeIndcn"
        sig_start_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LcmaIndcn_NoLcmaWarn': 0, 'LcmaIndcn_LcmaWarnLvl1': 1, 'LcmaIndcn_NotUsed': 2, 'LcmaIndcn_LcmaWarnLvl2': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class LoadAndStoreReqErgoSetgEve:
        sig_name = "LoadAndStoreReqErgoSetgEve"
        sig_start_bit = 31
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EveMemPosn_Idle': 0, 'EveMemPosn_Store': 1, 'EveMemPosn_Load': 2, 'EveMemPosn_Stop': 3, 'EveMemPosn_AutMovmt': 4, 'EveMemPosn_Upload': 5, 'EveMemPosn_Download': 6, 'EveMemPosn_Clear': 7}
        compute_method = None
        length = 3
        startbit = 31
        byte = 3
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class PwrAvlDelta:
        sig_name = "PwrAvlDelta"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = -32768
        sig_value_max = 32767
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class RctaIndcnLe:
        sig_name = "RctaIndcnLe"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LcmaIndcn_NoLcmaWarn': 0, 'LcmaIndcn_LcmaWarnLvl1': 1, 'LcmaIndcn_NotUsed': 2, 'LcmaIndcn_LcmaWarnLvl2': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class VehWinSunRoofClsReq:
        sig_name = "VehWinSunRoofClsReq"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenCls3_NoRequest': 0, 'OpenCls3_Close': 1, 'OpenCls3_Reserved1': 2, 'OpenCls3_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class CcmBodyFr52:
    msg_name = "CcmBodyFr52"
    msg_id = 1159
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig8Byte2:
        sig_name = "CcmCaliSig8Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig8Byte1:
        sig_name = "CcmCaliSig8Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig8Byte5:
        sig_name = "CcmCaliSig8Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig8Byte6:
        sig_name = "CcmCaliSig8Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig8Byte0:
        sig_name = "CcmCaliSig8Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig8Byte7:
        sig_name = "CcmCaliSig8Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig8Byte4:
        sig_name = "CcmCaliSig8Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig8Byte3:
        sig_name = "CcmCaliSig8Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class SmdToBgmBodyDiagRespFrame:
    msg_name = "SmdToBgmBodyDiagRespFrame"
    msg_id = 1575
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class SmdBodyFr01:
    msg_name = "SmdBodyFr01"
    msg_id = 105
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DrvrSeatMemSts:
        sig_name = "DrvrSeatMemSts"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DrvrSeatVentnActlPwrCns:
        sig_name = "DrvrSeatVentnActlPwrCns"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DrvrSeatBtnPsd:
        sig_name = "DrvrSeatBtnPsd"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class SeatBackAngleRowFirstDrvr:
        sig_name = "SeatBackAngleRowFirstDrvr"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 180
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

    class DrvrSeatInAutMovmt:
        sig_name = "DrvrSeatInAutMovmt"
        sig_start_bit = 19
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DrvrSeatVentnDesPwrCns:
        sig_name = "DrvrSeatVentnDesPwrCns"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyFr84:
    msg_name = "CemBodyFr84"
    msg_id = 468
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.18
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class PassSeatDispSpplFct:
        sig_name = "PassSeatDispSpplFct"
        sig_start_bit = 15
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatActvSpplFct1_NotAvl': 0, 'SeatActvSpplFct1_LumExtnAndLumHei': 1, 'SeatActvSpplFct1_BackBlster': 2, 'SeatActvSpplFct1_CushExtn': 3, 'SeatActvSpplFct1_HdrestHeiAndHdrestTilt': 4, 'SeatActvSpplFct1_MassgFct': 5, 'SeatActvSpplFct1_ShoulderFct': 6, 'SeatActvSpplFct1_LegrestFct': 7}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CrashStsSafeSts:
        sig_name = "CrashStsSafeSts"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CrashSts2_NoCrash': 0, 'CrashSts2_Crash': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class PassSeatDispMassgFctMassgInten:
        sig_name = "PassSeatDispMassgFctMassgInten"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgIntenLvl_IntenLo': 0, 'MassgIntenLvl_IntenNorm': 1, 'MassgIntenLvl_IntenHi': 2, 'MassgIntenLvl_Off': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DrvrSeatDispSpplFct:
        sig_name = "DrvrSeatDispSpplFct"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatActvSpplFct1_NotAvl': 0, 'SeatActvSpplFct1_LumExtnAndLumHei': 1, 'SeatActvSpplFct1_BackBlster': 2, 'SeatActvSpplFct1_CushExtn': 3, 'SeatActvSpplFct1_HdrestHeiAndHdrestTilt': 4, 'SeatActvSpplFct1_MassgFct': 5, 'SeatActvSpplFct1_ShoulderFct': 6, 'SeatActvSpplFct1_LegrestFct': 7}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DrvrSeatDispMassgFctMassgProg:
        sig_name = "DrvrSeatDispMassgFctMassgProg"
        sig_start_bit = 19
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgProgTyp_Prog1': 0, 'MassgProgTyp_Prog2': 1, 'MassgProgTyp_Prog3': 2, 'MassgProgTyp_Prog4': 3, 'MassgProgTyp_Prog5': 4, 'MassgProgTyp_Prog6': 5, 'MassgProgTyp_Prog7': 6, 'MassgProgTyp_Prog8': 7}
        compute_method = None
        length = 3
        startbit = 19
        byte = 2
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class DrvrSeatDispMassgFctOnOff:
        sig_name = "DrvrSeatDispMassgFctOnOff"
        sig_start_bit = 16
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
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CrashStsSafeCntr:
        sig_name = "CrashStsSafeCntr"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RemStrtHvCtrlReqErsCmd:
        sig_name = "RemStrtHvCtrlReqErsCmd"
        sig_start_bit = 63
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ErsCmd_ErsCmdNotSet': 0, 'ErsCmd_ErsCmdOn': 1, 'ErsCmd_ErsCmdOff': 2}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CrashStsSafeChks:
        sig_name = "CrashStsSafeChks"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RemStrtHvCtrlReqErsRunTime:
        sig_name = "RemStrtHvCtrlReqErsRunTime"
        sig_start_bit = 61
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 61
        byte = 7
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class DrvrSeatDispMassgFctMassgInten:
        sig_name = "DrvrSeatDispMassgFctMassgInten"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgIntenLvl_IntenLo': 0, 'MassgIntenLvl_IntenNorm': 1, 'MassgIntenLvl_IntenHi': 2, 'MassgIntenLvl_Off': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PassSeatDispMassgFctOnOff:
        sig_name = "PassSeatDispMassgFctOnOff"
        sig_start_bit = 24
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
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PassSeatDispMassgFctMassgProg:
        sig_name = "PassSeatDispMassgFctMassgProg"
        sig_start_bit = 27
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MassgProgTyp_Prog1': 0, 'MassgProgTyp_Prog2': 1, 'MassgProgTyp_Prog3': 2, 'MassgProgTyp_Prog4': 3, 'MassgProgTyp_Prog5': 4, 'MassgProgTyp_Prog6': 5, 'MassgProgTyp_Prog7': 6, 'MassgProgTyp_Prog8': 7}
        compute_method = None
        length = 3
        startbit = 27
        byte = 3
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1


class CcmBodyFr26:
    msg_name = "CcmBodyFr26"
    msg_id = 901
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class IntCo2Conc:
        sig_name = "IntCo2Conc"
        sig_start_bit = 1
        sig_length = 10
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 1
        bmuws_info = [(0, 0b00000011, 0b11111100, 2, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class CEMBodyFr30:
    msg_name = "CEMBodyFr30"
    msg_id = 880
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.62
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class CarTiGlb:
        sig_name = "CarTiGlb"
        sig_start_bit = 39
        sig_length = 32
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4294967295
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class EngSt1WdStsChks:
        sig_name = "EngSt1WdStsChks"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class EngSt1WdStsEngSt1WdSts:
        sig_name = "EngSt1WdStsEngSt1WdSts"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 9
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EngSt1_Ini': 0, 'EngSt1_Awake': 1, 'EngSt1_Rdy': 2, 'EngSt1_PreStrtg': 3, 'EngSt1_StrtgInProgs': 4, 'EngSt1_RunngRunng': 5, 'EngSt1_RunngStb': 6, 'EngSt1_RunngStrtgInProgs': 7, 'EngSt1_RunngRemStrtd': 8, 'EngSt1_AftRun': 9}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EngSt1WdStsCntr:
        sig_name = "EngSt1WdStsCntr"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class CemBodyFr06:
    msg_name = "CemBodyFr06"
    msg_id = 1120
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.19
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class CmptmtClngPreStrtReq:
        sig_name = "CmptmtClngPreStrtReq"
        sig_start_bit = 42
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 42
        byte = 5
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class VibrationFbToSwtp:
        sig_name = "VibrationFbToSwtp"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class ActvnOfSteerWhlIllmn:
        sig_name = "ActvnOfSteerWhlIllmn"
        sig_start_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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


class CcmBodyFr54:
    msg_name = "CcmBodyFr54"
    msg_id = 1161
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig10Byte3:
        sig_name = "CcmCaliSig10Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig10Byte4:
        sig_name = "CcmCaliSig10Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig10Byte0:
        sig_name = "CcmCaliSig10Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig10Byte6:
        sig_name = "CcmCaliSig10Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig10Byte2:
        sig_name = "CcmCaliSig10Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig10Byte1:
        sig_name = "CcmCaliSig10Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig10Byte5:
        sig_name = "CcmCaliSig10Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig10Byte7:
        sig_name = "CcmCaliSig10Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CemBodyFr08:
    msg_name = "CemBodyFr08"
    msg_id = 1171
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DrvrPfmncAlrmReq:
        sig_name = "DrvrPfmncAlrmReq"
        sig_start_bit = 19
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 6
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvrPfmncWarnReq_Unavailable': 0, 'DrvrPfmncWarnReq_Unknown': 1, 'DrvrPfmncWarnReq_NoWarning': 2, 'DrvrPfmncWarnReq_Distractive': 3, 'DrvrPfmncWarnReq_Warninglevel1': 4, 'DrvrPfmncWarnReq_Warninglevel2': 5, 'DrvrPfmncWarnReq_Reserved': 6}
        compute_method = None
        length = 3
        startbit = 19
        byte = 2
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class CooltHeatrTIntk:
        sig_name = "CooltHeatrTIntk"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 250
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

    class BltLockStAtPassBltLockSt1:
        sig_name = "BltLockStAtPassBltLockSt1"
        sig_start_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BltLockSt1_Unlock': 0, 'BltLockSt1_Lock': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BltLockStAtRowThrdRiBltLockEquid:
        sig_name = "BltLockStAtRowThrdRiBltLockEquid"
        sig_start_bit = 39
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CptEquid_Equid': 0, 'CptEquid_NotEquid': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BltLockStAtDrvrBltLockSt1:
        sig_name = "BltLockStAtDrvrBltLockSt1"
        sig_start_bit = 23
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BltLockSt1_Unlock': 0, 'BltLockSt1_Lock': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BltLockStAtPassBltLockSts:
        sig_name = "BltLockStAtPassBltLockSts"
        sig_start_bit = 32
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BltLockStAtRowSecMidBltLockSts:
        sig_name = "BltLockStAtRowSecMidBltLockSts"
        sig_start_bit = 0
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BltLockStAtRowThrdRiBltLockSt1:
        sig_name = "BltLockStAtRowThrdRiBltLockSt1"
        sig_start_bit = 38
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BltLockSt1_Unlock': 0, 'BltLockSt1_Lock': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class AmbTRawAmbTVal:
        sig_name = "AmbTRawAmbTVal"
        sig_start_bit = 42
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-70.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 42
        bmuws_info = [(5, 0b00000111, 0b11111000, 3, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class AmbTRawQly:
        sig_name = "AmbTRawQly"
        sig_start_bit = 44
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
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

    class CooltHeatrTOutl:
        sig_name = "CooltHeatrTOutl"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 250
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class BltLockStAtRowThrdLeBltLockEquid:
        sig_name = "BltLockStAtRowThrdLeBltLockEquid"
        sig_start_bit = 26
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CptEquid_Equid': 0, 'CptEquid_NotEquid': 1}
        compute_method = None
        length = 1
        startbit = 26
        byte = 3
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BltLockStAtRowThrdRiBltLockSts:
        sig_name = "BltLockStAtRowThrdRiBltLockSts"
        sig_start_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BltLockStAtRowSecLeBltLockSts:
        sig_name = "BltLockStAtRowSecLeBltLockSts"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BltLockStAtRowSecLeBltLockSt1:
        sig_name = "BltLockStAtRowSecLeBltLockSt1"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BltLockSt1_Unlock': 0, 'BltLockSt1_Lock': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BltLockStAtRowThrdLeBltLockSt1:
        sig_name = "BltLockStAtRowThrdLeBltLockSt1"
        sig_start_bit = 25
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BltLockSt1_Unlock': 0, 'BltLockSt1_Lock': 1}
        compute_method = None
        length = 1
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RemChkTInVeh:
        sig_name = "RemChkTInVeh"
        sig_start_bit = 35
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class BltLockStAtRowSecRiBltLockSts:
        sig_name = "BltLockStAtRowSecRiBltLockSts"
        sig_start_bit = 29
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class BltLockStAtRowSecRiBltLockSt1:
        sig_name = "BltLockStAtRowSecRiBltLockSt1"
        sig_start_bit = 30
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BltLockSt1_Unlock': 0, 'BltLockSt1_Lock': 1}
        compute_method = None
        length = 1
        startbit = 30
        byte = 3
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BltLockStAtRowSecMidBltLockSt1:
        sig_name = "BltLockStAtRowSecMidBltLockSt1"
        sig_start_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'BltLockSt1_Unlock': 0, 'BltLockSt1_Lock': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class BltLockStAtRowSecRiBltLockEquid:
        sig_name = "BltLockStAtRowSecRiBltLockEquid"
        sig_start_bit = 31
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CptEquid_Equid': 0, 'CptEquid_NotEquid': 1}
        compute_method = None
        length = 1
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BltLockStAtRowSecMidBltLockEquid:
        sig_name = "BltLockStAtRowSecMidBltLockEquid"
        sig_start_bit = 2
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CptEquid_Equid': 0, 'CptEquid_NotEquid': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class BltLockStAtRowSecLeBltLockEquid:
        sig_name = "BltLockStAtRowSecLeBltLockEquid"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CptEquid_Equid': 0, 'CptEquid_NotEquid': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class BltLockStAtRowThrdLeBltLockSts:
        sig_name = "BltLockStAtRowThrdLeBltLockSts"
        sig_start_bit = 24
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class BltLockStAtDrvrBltLockSts:
        sig_name = "BltLockStAtDrvrBltLockSts"
        sig_start_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class CEMBodyFr19:
    msg_name = "CEMBodyFr19"
    msg_id = 528
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.235
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HvPwrEgyPrio:
        sig_name = "HvPwrEgyPrio"
        sig_start_bit = 42
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvPwrEgyPrio_Standby': 0, 'HvPwrEgyPrio_Dischrgning': 1, 'HvPwrEgyPrio_Chrgning': 2, 'HvPwrEgyPrio_ClimaWithAc': 3, 'HvPwrEgyPrio_ClimaWithoutAc': 4, 'HvPwrEgyPrio_RemoteClimatisaiton': 5}
        compute_method = None
        length = 3
        startbit = 42
        byte = 5
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class EngTEngT:
        sig_name = "EngTEngT"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = "-50.0"
        sig_value_min = 0
        sig_value_max = 250
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

    class PassSeatSts:
        sig_name = "PassSeatSts"
        sig_start_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PassSeatSts1_Empty': 0, 'PassSeatSts1_Fmale': 1, 'PassSeatSts1_OccptLrg': 2, 'PassSeatSts1_Ukwn': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EngTQf:
        sig_name = "EngTQf"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SeatDispBtnPsdDrvrSeatDispBtnPsd:
        sig_name = "SeatDispBtnPsdDrvrSeatDispBtnPsd"
        sig_start_bit = 61
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class MirrDefrstAtPassCmd:
        sig_name = "MirrDefrstAtPassCmd"
        sig_start_bit = 57
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
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class MirrDefrstAtDrvrCmd:
        sig_name = "MirrDefrstAtDrvrCmd"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class SeatOccptAtRowSecLe:
        sig_name = "SeatOccptAtRowSecLe"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PassSeatSts1_Empty': 0, 'PassSeatSts1_Fmale': 1, 'PassSeatSts1_OccptLrg': 2, 'PassSeatSts1_Ukwn': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SeatDispBtnPsdPassSeatDispBtnPsd:
        sig_name = "SeatDispBtnPsdPassSeatDispBtnPsd"
        sig_start_bit = 62
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class CoolgLoadGroupCoolgLimd:
        sig_name = "CoolgLoadGroupCoolgLimd"
        sig_start_bit = 39
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CoolgLoadGroupCoolgLoad2:
        sig_name = "CoolgLoadGroupCoolgLoad2"
        sig_start_bit = 38
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 38
        byte = 4
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class SeatOccptAtRowSecRi:
        sig_name = "SeatOccptAtRowSecRi"
        sig_start_bit = 30
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PassSeatSts1_Empty': 0, 'PassSeatSts1_Fmale': 1, 'PassSeatSts1_OccptLrg': 2, 'PassSeatSts1_Ukwn': 3}
        compute_method = None
        length = 2
        startbit = 30
        byte = 3
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5


class SmdBodyFr02:
    msg_name = "SmdBodyFr02"
    msg_id = 864
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DrvrSeatHallPosExtUpldSeatHeadrHozlPos:
        sig_name = "DrvrSeatHallPosExtUpldSeatHeadrHozlPos"
        sig_start_bit = 17
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class DrvrSeatHallPosExtUpldSeatHeadrVertPos:
        sig_name = "DrvrSeatHallPosExtUpldSeatHeadrVertPos"
        sig_start_bit = 33
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class DrvrSeatHallPosExtUpldSeatCushExtPos:
        sig_name = "DrvrSeatHallPosExtUpldSeatCushExtPos"
        sig_start_bit = 1
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 1
        bmuws_info = [(0, 0b00000011, 0b11111100, 2, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class DrvrSeatHallPosDownLdSts:
        sig_name = "DrvrSeatHallPosDownLdSts"
        sig_start_bit = 4
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Sts_Resd': 0, 'Sts_Err': 1, 'Sts_CmplOk': 2, 'Sts_InProgs': 3}
        compute_method = None
        length = 2
        startbit = 4
        byte = 0
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class PotBodyFr03:
    msg_name = "PotBodyFr03"
    msg_id = 578
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class TopPosHmiFeedBack2:
        sig_name = "TopPosHmiFeedBack2"
        sig_start_bit = 6
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_value_init = 95
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 6
        byte = 0
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class TrOpenPosn:
        sig_name = "TrOpenPosn"
        sig_start_bit = 14
        sig_length = 7
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 101
        sig_value_init = 101
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 14
        byte = 1
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0


class CcmBodyFr25:
    msg_name = "CcmBodyFr25"
    msg_id = 1049
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class HeatrAirTReq:
        sig_name = "HeatrAirTReq"
        sig_start_bit = 7
        sig_length = 9
        sig_value_factor = 0.5
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 511
        sig_value_init = 120
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b10000000, 0b01111111, 1, 7)]

    class ElecDefrstReqWinDefrstFrntReq:
        sig_name = "ElecDefrstReqWinDefrstFrntReq"
        sig_start_bit = 49
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
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class FrntHvacBlowerSts:
        sig_name = "FrntHvacBlowerSts"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacFanSts_Off': 0, 'HvacFanSts_On': 1, 'HvacFanSts_Warning': 2, 'HvacFanSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class FragCh1UseUpWrn:
        sig_name = "FragCh1UseUpWrn"
        sig_start_bit = 60
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 60
        byte = 7
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class IntPm25StsFrmClima:
        sig_name = "IntPm25StsFrmClima"
        sig_start_bit = 52
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PmSnsrSts_Initial': 0, 'PmSnsrSts_Collecting': 1, 'PmSnsrSts_Complete': 2, 'PmSnsrSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class HvahAirTsp:
        sig_name = "HvahAirTsp"
        sig_start_bit = 18
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-40.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 18
        bmuws_info = [(2, 0b00000111, 0b11111000, 3, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class FragLvlFrmClima:
        sig_name = "FragLvlFrmClima"
        sig_start_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RatUse_NoRequest': 0, 'RatUse_Low': 1, 'RatUse_Mid': 2, 'RatUse_High': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ClimaSts:
        sig_name = "ClimaSts"
        sig_start_bit = 20
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaSts_Start': 0, 'ClimaSts_Finish': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class ElecDefrstReqMirrDefrstReq:
        sig_name = "ElecDefrstReqMirrDefrstReq"
        sig_start_bit = 50
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
        startbit = 50
        byte = 6
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class ElecDefrstReqWinDefrstReReq:
        sig_name = "ElecDefrstReqWinDefrstReReq"
        sig_start_bit = 48
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
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class PostDrvgClimaAvl:
        sig_name = "PostDrvgClimaAvl"
        sig_start_bit = 32
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
        startbit = 32
        byte = 4
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class FragStsFrmClima:
        sig_name = "FragStsFrmClima"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 1
        sig_value_max = 3
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AirFragSts_OFF': 1, 'AirFragSts_ON': 2, 'AirFragSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class FragCh5UseUpWrn:
        sig_name = "FragCh5UseUpWrn"
        sig_start_bit = 46
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class FragCh3UseUpWrn:
        sig_name = "FragCh3UseUpWrn"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FragCh2UseUpWrn:
        sig_name = "FragCh2UseUpWrn"
        sig_start_bit = 58
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HvahHeatgReq:
        sig_name = "HvahHeatgReq"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HvacOsaAndRecActrQfForHp:
        sig_name = "HvacOsaAndRecActrQfForHp"
        sig_start_bit = 10
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class FragCh4UseUpWrn:
        sig_name = "FragCh4UseUpWrn"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvacCoolgEnaRe:
        sig_name = "HvacCoolgEnaRe"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CemBodyFr04:
    msg_name = "CemBodyFr04"
    msg_id = 1072
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.14
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class LeSolarData:
        sig_name = "LeSolarData"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_value_init = 51
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class RlyCmdCmft:
        sig_name = "RlyCmdCmft"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ClimRlyCmd:
        sig_name = "ClimRlyCmd"
        sig_start_bit = 46
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
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SolarSnsrVluQf:
        sig_name = "SolarSnsrVluQf"
        sig_start_bit = 47
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DataQf_NotOk': 0, 'DataQf_Ok': 1}
        compute_method = None
        length = 1
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RiSolarData:
        sig_name = "RiSolarData"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_value_init = 51
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CcmBodyFr40:
    msg_name = "CcmBodyFr40"
    msg_id = 596
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class ElecVentnMotPwrCnsAct:
        sig_name = "ElecVentnMotPwrCnsAct"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class HvacModFlapActlPosnFrstRowRi:
        sig_name = "HvacModFlapActlPosnFrstRowRi"
        sig_start_bit = 33
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HvacModFlapActlPosnFrstRowLe:
        sig_name = "HvacModFlapActlPosnFrstRowLe"
        sig_start_bit = 55
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11000000, 0b00111111, 2, 6)]

    class HvacDefrstFlapActlPosn:
        sig_name = "HvacDefrstFlapActlPosn"
        sig_start_bit = 31
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11000000, 0b00111111, 2, 6)]

    class ElecVentnMotPwrCnsDes:
        sig_name = "ElecVentnMotPwrCnsDes"
        sig_start_bit = 9
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class BgmBodyCANNmFr:
    msg_name = "BgmBodyCANNmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class RldmBodyFr01:
    msg_name = "RldmBodyFr01"
    msg_id = 112
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DoorLeReLatPawlSt:
        sig_name = "DoorLeReLatPawlSt"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WinFailrStsAtReLe:
        sig_name = "WinFailrStsAtReLe"
        sig_start_bit = 27
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class DoorLeReOpenLowReqOutdSwt1:
        sig_name = "DoorLeReOpenLowReqOutdSwt1"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorLeReSwtLockgSts:
        sig_name = "DoorLeReSwtLockgSts"
        sig_start_bit = 14
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd1_NotPsd': 0, 'PsdNotPsd1_Psd': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DoorLeReCinhIntFailInfCinchRestFlt:
        sig_name = "DoorLeReCinhIntFailInfCinchRestFlt"
        sig_start_bit = 34
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class WinPosnStsAtReLe:
        sig_name = "WinPosnStsAtReLe"
        sig_start_bit = 12
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 12
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class DoorLeReLatPosn:
        sig_name = "DoorLeReLatPosn"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorPos_Undefined': 0, 'DoorPos_FullyClosed': 1, 'DoorPos_SecondaryPosition': 2, 'DoorPos_FullyOpen': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ShortDropWinReLeSts:
        sig_name = "ShortDropWinReLeSts"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShortDropSts_Idle': 0, 'ShortDropSts_WindowDown': 1, 'ShortDropSts_WindowClosed': 2, 'ShortDropSts_NotUsed': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorLeReLockSts:
        sig_name = "DoorLeReLockSts"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorLeReOpenReqInsdSwt1:
        sig_name = "DoorLeReOpenReqInsdSwt1"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class ChdLockLeftSts:
        sig_name = "ChdLockLeftSts"
        sig_start_bit = 6
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class DoorLeReCinhIntFailInfCinchFlt1:
        sig_name = "DoorLeReCinhIntFailInfCinchFlt1"
        sig_start_bit = 35
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class DoorLeReHndlSts:
        sig_name = "DoorLeReHndlSts"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorHndlSts_Ukwn': 0, 'DoorHndlSts_FullRtrctd': 1, 'DoorHndlSts_MovgOut': 2, 'DoorHndlSts_StopDurgDply': 3, 'DoorHndlSts_FullDplyd': 4, 'DoorHndlSts_MovgIn': 5, 'DoorHndlSts_StopDurgRtrct': 6, 'DoorHndlSts_Flt': 7}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class CcmBodyFr03:
    msg_name = "CcmBodyFr03"
    msg_id = 512
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class ClimaPwrNormDes:
        sig_name = "ClimaPwrNormDes"
        sig_start_bit = 47
        sig_length = 11
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]

    class ClimaPwrCritDes:
        sig_name = "ClimaPwrCritDes"
        sig_start_bit = 26
        sig_length = 11
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 26
        bmuws_info = [(3, 0b00000111, 0b11111000, 3, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class ClimaPwrCns:
        sig_name = "ClimaPwrCns"
        sig_start_bit = 2
        sig_length = 11
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class LvlOfClimaCmft:
        sig_name = "LvlOfClimaCmft"
        sig_start_bit = 7
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LvlOfClimaCmft_Off': 0, 'LvlOfClimaCmft_Lvl1': 1, 'LvlOfClimaCmft_Lvl2': 2, 'LvlOfClimaCmft_Lvl3': 3, 'LvlOfClimaCmft_Lvl4': 4, 'LvlOfClimaCmft_Lvl5': 5, 'LvlOfClimaCmft_Lvl6': 6, 'LvlOfClimaCmft_Lvl7': 7}
        compute_method = None
        length = 3
        startbit = 7
        byte = 0
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ClimaActv:
        sig_name = "ClimaActv"
        sig_start_bit = 28
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
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SteerWhlHeatgPwrAllwd:
        sig_name = "SteerWhlHeatgPwrAllwd"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class RemClimaActv:
        sig_name = "RemClimaActv"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CcmBodyFr47:
    msg_name = "CcmBodyFr47"
    msg_id = 1154
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig3Byte5:
        sig_name = "CcmCaliSig3Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig3Byte1:
        sig_name = "CcmCaliSig3Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig3Byte4:
        sig_name = "CcmCaliSig3Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig3Byte3:
        sig_name = "CcmCaliSig3Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig3Byte0:
        sig_name = "CcmCaliSig3Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig3Byte6:
        sig_name = "CcmCaliSig3Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig3Byte2:
        sig_name = "CcmCaliSig3Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig3Byte7:
        sig_name = "CcmCaliSig3Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class SmblBodyFr02:
    msg_name = "SmblBodyFr02"
    msg_id = 1059
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class SecRowSeatVentnActlPwrCnsLe:
        sig_name = "SecRowSeatVentnActlPwrCnsLe"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class SecRowSeatHeatgActlPwrCnsLe:
        sig_name = "SecRowSeatHeatgActlPwrCnsLe"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class SeatVentnLvlStsRowSecLe:
        sig_name = "SeatVentnLvlStsRowSecLe"
        sig_start_bit = 20
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class SeatHeatgLvlStsRowSecLe:
        sig_name = "SeatHeatgLvlStsRowSecLe"
        sig_start_bit = 36
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 36
        byte = 4
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class SecRowSeatHeatgDesPwrCnsLe:
        sig_name = "SecRowSeatHeatgDesPwrCnsLe"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class SecRowSeatVentnDesPwrCnsLe:
        sig_name = "SecRowSeatVentnDesPwrCnsLe"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class PdmBodyFr01:
    msg_name = "PdmBodyFr01"
    msg_id = 16
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DoorPassLatPawlSt:
        sig_name = "DoorPassLatPawlSt"
        sig_start_bit = 44
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class DoorPassLatPosn:
        sig_name = "DoorPassLatPosn"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorPos_Undefined': 0, 'DoorPos_FullyClosed': 1, 'DoorPos_SecondaryPosition': 2, 'DoorPos_FullyOpen': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class MirrFoldStsAtPass:
        sig_name = "MirrFoldStsAtPass"
        sig_start_bit = 11
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MirrFoldStsTyp_MirrFoldPosnUndefd': 0, 'MirrFoldStsTyp_MirrNotFoldPosn': 1, 'MirrFoldStsTyp_MirrFoldPosn': 2, 'MirrFoldStsTyp_MirrMovgToNotFold': 3, 'MirrFoldStsTyp_MirrMovgToFold': 4}
        compute_method = None
        length = 3
        startbit = 11
        byte = 1
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class DoorPassSwtIntrLockgReq:
        sig_name = "DoorPassSwtIntrLockgReq"
        sig_start_bit = 18
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockgCenReq2_Idle': 0, 'LockgCenReq2_Unlck': 1, 'LockgCenReq2_Lock': 2}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class MirrAtPassInMovmt:
        sig_name = "MirrAtPassInMovmt"
        sig_start_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class WinPosnStsAtPass:
        sig_name = "WinPosnStsAtPass"
        sig_start_bit = 7
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 31
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinAndRoofAndCurtPosnTyp_PosnUkwn': 0, 'WinAndRoofAndCurtPosnTyp_ClsFull': 1, 'WinAndRoofAndCurtPosnTyp_PercOpen4': 2, 'WinAndRoofAndCurtPosnTyp_PercOpen8': 3, 'WinAndRoofAndCurtPosnTyp_PercOpen12': 4, 'WinAndRoofAndCurtPosnTyp_PercOpen16': 5, 'WinAndRoofAndCurtPosnTyp_PercOpen20': 6, 'WinAndRoofAndCurtPosnTyp_PercOpen24': 7, 'WinAndRoofAndCurtPosnTyp_PercOpen28': 8, 'WinAndRoofAndCurtPosnTyp_PercOpen32': 9, 'WinAndRoofAndCurtPosnTyp_PercOpen36': 10, 'WinAndRoofAndCurtPosnTyp_PercOpen40': 11, 'WinAndRoofAndCurtPosnTyp_PercOpen44': 12, 'WinAndRoofAndCurtPosnTyp_PercOpen48': 13, 'WinAndRoofAndCurtPosnTyp_PercOpen52': 14, 'WinAndRoofAndCurtPosnTyp_PercOpen56': 15, 'WinAndRoofAndCurtPosnTyp_PercOpen60': 16, 'WinAndRoofAndCurtPosnTyp_PercOpen64': 17, 'WinAndRoofAndCurtPosnTyp_PercOpen68': 18, 'WinAndRoofAndCurtPosnTyp_PercOpen72': 19, 'WinAndRoofAndCurtPosnTyp_PercOpen76': 20, 'WinAndRoofAndCurtPosnTyp_PercOpen80': 21, 'WinAndRoofAndCurtPosnTyp_PercOpen84': 22, 'WinAndRoofAndCurtPosnTyp_PercOpen88': 23, 'WinAndRoofAndCurtPosnTyp_PercOpen92': 24, 'WinAndRoofAndCurtPosnTyp_PercOpen96': 25, 'WinAndRoofAndCurtPosnTyp_OpenFull': 26, 'WinAndRoofAndCurtPosnTyp_Resd1': 27, 'WinAndRoofAndCurtPosnTyp_Resd2': 28, 'WinAndRoofAndCurtPosnTyp_Resd3': 29, 'WinAndRoofAndCurtPosnTyp_Resd4': 30, 'WinAndRoofAndCurtPosnTyp_Movg': 31}
        compute_method = None
        length = 5
        startbit = 7
        byte = 0
        mask = 0b11111000
        unmask = 0b00000111
        shift = 3

    class ShortDropWinPassSts:
        sig_name = "ShortDropWinPassSts"
        sig_start_bit = 38
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShortDropSts_Idle': 0, 'ShortDropSts_WindowDown': 1, 'ShortDropSts_WindowClosed': 2, 'ShortDropSts_NotUsed': 3}
        compute_method = None
        length = 2
        startbit = 38
        byte = 4
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class PassMemBtnPsdMemBtn3:
        sig_name = "PassMemBtnPsdMemBtn3"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DoorPassOpenLowReqOutdSwt1:
        sig_name = "DoorPassOpenLowReqOutdSwt1"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorPassOpenReqInsdSwt1:
        sig_name = "DoorPassOpenReqInsdSwt1"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd3_NoInfo1': 0, 'PsdNotPsd3_Psd': 1, 'PsdNotPsd3_NotPsd': 2, 'PsdNotPsd3_NoInfo2': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PassMemBtnPsdMemBtn1:
        sig_name = "PassMemBtnPsdMemBtn1"
        sig_start_bit = 23
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PassMemBtnPsdMemBtn2:
        sig_name = "PassMemBtnPsdMemBtn2"
        sig_start_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class PassMemBtnPsdMemButM:
        sig_name = "PassMemBtnPsdMemButM"
        sig_start_bit = 20
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class FltOfIndcrTurnOnPassSide:
        sig_name = "FltOfIndcrTurnOnPassSide"
        sig_start_bit = 29
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 29
        byte = 3
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class DoorPassLockSts:
        sig_name = "DoorPassLockSts"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LockSts2_LockStsUkwn': 0, 'LockSts2_Unlckd': 1, 'LockSts2_Lockd': 2, 'LockSts2_SafeLockd': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class CemBodyFr87:
    msg_name = "CemBodyFr87"
    msg_id = 958
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class WinOpenClsGlbReqFromTelmWinOpenClsGlbSts:
        sig_name = "WinOpenClsGlbReqFromTelmWinOpenClsGlbSts"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinOpenClsGlbReqFromTelm_Idle': 0, 'WinOpenClsGlbReqFromTelm_Open': 1, 'WinOpenClsGlbReqFromTelm_Close': 2}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WinOpenClsGlbReqFromTelmWindowOpenValue:
        sig_name = "WinOpenClsGlbReqFromTelmWindowOpenValue"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class IntelliClimaResd7:
        sig_name = "IntelliClimaResd7"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaResd9:
        sig_name = "IntelliClimaResd9"
        sig_start_bit = 39
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaResd8:
        sig_name = "IntelliClimaResd8"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class CcmBodyFr58:
    msg_name = "CcmBodyFr58"
    msg_id = 579
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CdsParkgClimaActv:
        sig_name = "CdsParkgClimaActv"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ClimaOvrHeatProActvSts:
        sig_name = "ClimaOvrHeatProActvSts"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class RemVentActvSts:
        sig_name = "RemVentActvSts"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RemVentWarnSts:
        sig_name = "RemVentWarnSts"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RemVentWarningSts_NoErr': 0, 'RemVentWarningSts_Err': 1, 'RemVentWarningSts_PwrNotAllwd': 2, 'RemVentWarningSts_EgyNotAllwd': 3}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RemVentReqRspnFb:
        sig_name = "RemVentReqRspnFb"
        sig_start_bit = 1
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
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class CcmBodyFr27:
    msg_name = "CcmBodyFr27"
    msg_id = 1145
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class SunDataElevn:
        sig_name = "SunDataElevn"
        sig_start_bit = 7
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-90.0"
        sig_value_min = 0
        sig_value_max = 1800
        sig_value_init = 900
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class CmptmtIntrMtrlTEstimdMtrlSnsrT:
        sig_name = "CmptmtIntrMtrlTEstimdMtrlSnsrT"
        sig_start_bit = 36
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class SunDataAzi:
        sig_name = "SunDataAzi"
        sig_start_bit = 16
        sig_length = 9
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 16
        bmuws_info = [(2, 0b00000001, 0b11111110, 1, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class PwrAllwdForElecAirVentn:
        sig_name = "PwrAllwdForElecAirVentn"
        sig_start_bit = 50
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class CmptmtIntrMtrlTEstimdMtrlSnsrTQly2:
        sig_name = "CmptmtIntrMtrlTEstimdMtrlSnsrTQly2"
        sig_start_bit = 38
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qly2_Flt': 0, 'Qly2_NoInfo': 1, 'Qly2_Vld': 2}
        compute_method = None
        length = 2
        startbit = 38
        byte = 4
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class EgyDesForClima:
        sig_name = "EgyDesForClima"
        sig_start_bit = 23
        sig_length = 7
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 127
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 23
        byte = 2
        mask = 0b11111110
        unmask = 0b00000001
        shift = 1


class CemBodyFr86:
    msg_name = "CemBodyFr86"
    msg_id = 956
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class IntelliClimaResd2:
        sig_name = "IntelliClimaResd2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class IntelliClimaResd3:
        sig_name = "IntelliClimaResd3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class IntelliClimaResd6:
        sig_name = "IntelliClimaResd6"
        sig_start_bit = 47
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class IntelliClimaResd1:
        sig_name = "IntelliClimaResd1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class IntelliClimaResd5:
        sig_name = "IntelliClimaResd5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class IntelliClimaResd4:
        sig_name = "IntelliClimaResd4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CcmBodyFr44:
    msg_name = "CcmBodyFr44"
    msg_id = 593
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class WinRfClsdReqForCoolgDwn:
        sig_name = "WinRfClsdReqForCoolgDwn"
        sig_start_bit = 0
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Warn2_NoWarn': 0, 'Warn2_Warn': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class WinAndRoofReqFrmClima:
        sig_name = "WinAndRoofReqFrmClima"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WinOpenClsGlbReqFromTelm_Idle': 0, 'WinOpenClsGlbReqFromTelm_Open': 1, 'WinOpenClsGlbReqFromTelm_Close': 2}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ClimaOvrHeatProRspn:
        sig_name = "ClimaOvrHeatProRspn"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AutoDeHumPopUp:
        sig_name = "AutoDeHumPopUp"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ClimaOnReq:
        sig_name = "ClimaOnReq"
        sig_start_bit = 26
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaOnReqSts_NoReq': 0, 'ClimaOnReqSts_FstRowOn': 1, 'ClimaOnReqSts_SecRowOn': 2, 'ClimaOnReqSts_TrdRowOn': 3, 'ClimaOnReqSts_AllOn': 4, 'ClimaOnReqSts_FstAndSecRowOn': 5, 'ClimaOnReqSts_SecAndTrdRowOn': 6, 'ClimaOnReqSts_Rsvd': 7}
        compute_method = None
        length = 3
        startbit = 26
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class AutoDefrstReqPopUp:
        sig_name = "AutoDefrstReqPopUp"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SunRoofOpnPopUpForHmi:
        sig_name = "SunRoofOpnPopUpForHmi"
        sig_start_bit = 10
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class RemStrtClimaRspn:
        sig_name = "RemStrtClimaRspn"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class Co2WarnForTelm:
        sig_name = "Co2WarnForTelm"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class ClimaOvrHeatProWarn:
        sig_name = "ClimaOvrHeatProWarn"
        sig_start_bit = 29
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaOvrheatProWarnSts_NoWarn': 0, 'ClimaOvrheatProWarnSts_Err': 1, 'ClimaOvrheatProWarnSts_PwrLo': 2, 'ClimaOvrheatProWarnSts_Tout': 3}
        compute_method = None
        length = 2
        startbit = 29
        byte = 3
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ClimaOffReq:
        sig_name = "ClimaOffReq"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaOffReq_NoReq': 0, 'ClimaOffReq_SecRowOffReq': 1, 'ClimaOffReq_TrdRowOffReq': 2, 'ClimaOffReq_ClimaOff': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class DiDblLock:
        sig_name = "DiDblLock"
        sig_start_bit = 2
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnableDisableCoding_Disabled': 0, 'EnableDisableCoding_Enabled': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class SwtrToBgmBodyDiagRespFrame:
    msg_name = "SwtrToBgmBodyDiagRespFrame"
    msg_id = 1667
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CemBodyFr79:
    msg_name = "CemBodyFr79"
    msg_id = 184
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class DoorOpenerPassReqChks:
        sig_name = "DoorOpenerPassReqChks"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class DoorOpenerRiReReqCntr:
        sig_name = "DoorOpenerRiReReqCntr"
        sig_start_bit = 35
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
        startbit = 35
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DoorOpenerRiReReqTrigSrc:
        sig_name = "DoorOpenerRiReReqTrigSrc"
        sig_start_bit = 38
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoTrigSrc': 0, 'KeyRem': 1, 'HMI': 2, 'Telm': 3, 'OutdSwt': 4, 'InsdSwt': 5}
        compute_method = None
        length = 3
        startbit = 38
        byte = 4
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DoorOpenerPassReqDoorOpenerReq:
        sig_name = "DoorOpenerPassReqDoorOpenerReq"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerIdle': 0, 'DoorOpenerOpen': 1, 'DoorOpenerCls': 2, 'DoorOpenerStop': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorOpenerRiReReqDoorOpenerReq:
        sig_name = "DoorOpenerRiReReqDoorOpenerReq"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorOpenerIdle': 0, 'DoorOpenerOpen': 1, 'DoorOpenerCls': 2, 'DoorOpenerStop': 3}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorOpenerPassReqCntr:
        sig_name = "DoorOpenerPassReqCntr"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DoorOpenerPassReqTrigSrc:
        sig_name = "DoorOpenerPassReqTrigSrc"
        sig_start_bit = 14
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoTrigSrc': 0, 'KeyRem': 1, 'HMI': 2, 'Telm': 3, 'OutdSwt': 4, 'InsdSwt': 5}
        compute_method = None
        length = 3
        startbit = 14
        byte = 1
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class DoorOpenerRiReReqChks:
        sig_name = "DoorOpenerRiReReqChks"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 255
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CcmBodyFr02:
    msg_name = "CcmBodyFr02"
    msg_id = 37
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class HvacAirMFlowEstimd:
        sig_name = "HvacAirMFlowEstimd"
        sig_start_bit = 33
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class PrkgClimaWarn:
        sig_name = "PrkgClimaWarn"
        sig_start_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ClimaWarn_NoWarn': 0, 'ClimaWarn_FuLo': 1, 'ClimaWarn_BattLo': 2, 'ClimaWarn_FuAndBattLo': 3, 'ClimaWarn_TLo': 4, 'ClimaWarn_THi': 5, 'ClimaWarn_Error': 6, 'ClimaWarn_HVError': 7, 'ClimaWarn_ActvnLimd': 8}
        compute_method = None
        length = 4
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class IntPm25VluFrmClima:
        sig_name = "IntPm25VluFrmClima"
        sig_start_bit = 9
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class HvEgyDesForClima:
        sig_name = "HvEgyDesForClima"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 50.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
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

    class ClimaStsDisp:
        sig_name = "ClimaStsDisp"
        sig_start_bit = 54
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class CemBodyFr47:
    msg_name = "CemBodyFr47"
    msg_id = 645
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class TelmClimaTSetHmiCmptmtTSpSpcl:
        sig_name = "TelmClimaTSetHmiCmptmtTSpSpcl"
        sig_start_bit = 38
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtTSpSpcl_Norm': 0, 'HmiCmptmtTSpSpcl_Lo': 1, 'HmiCmptmtTSpSpcl_Hi': 2}
        compute_method = None
        length = 2
        startbit = 38
        byte = 4
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class TelmClimaReq:
        sig_name = "TelmClimaReq"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TelmSeatSecLeHeatClimaLvl:
        sig_name = "TelmSeatSecLeHeatClimaLvl"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class TelmSeatPassVentnClimaLvl:
        sig_name = "TelmSeatPassVentnClimaLvl"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TelmClimaTmr:
        sig_name = "TelmClimaTmr"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class SeatHeatDurgClimaEnadFromTelm:
        sig_name = "SeatHeatDurgClimaEnadFromTelm"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatHeatDurgClimaEnad2_SeatHeatOff': 0, 'SeatHeatDurgClimaEnad2_SeatDrvOn': 1, 'SeatHeatDurgClimaEnad2_SeatPassOn': 2, 'SeatHeatDurgClimaEnad2_SeatDrvrAndPass': 3, 'SeatHeatDurgClimaEnad2_SeatLeftRearOn': 4, 'SeatHeatDurgClimaEnad2_SeatRightRearOn': 5}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class ClimaTmrStsTelmRqrd:
        sig_name = "ClimaTmrStsTelmRqrd"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SteerWhlHeatgDurgClimaEnadFromTelm:
        sig_name = "SteerWhlHeatgDurgClimaEnadFromTelm"
        sig_start_bit = 8
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
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class IntelliClimaReq:
        sig_name = "IntelliClimaReq"
        sig_start_bit = 42
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptSts_NoRequest': 0, 'CmptSts_CoolingRequest': 1, 'CmptSts_HeatingRequest': 2, 'CmptSts_CoolingAndHeatingRequest': 3, 'CmptSts_PostHeating': 4}
        compute_method = None
        length = 3
        startbit = 42
        byte = 5
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class TelmSeatSecRiHeatClimaLvl:
        sig_name = "TelmSeatSecRiHeatClimaLvl"
        sig_start_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class RemVentReq:
        sig_name = "RemVentReq"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
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

    class TelmSeatSecLeVentnClimaLvl:
        sig_name = "TelmSeatSecLeVentnClimaLvl"
        sig_start_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TelmClimaTSetTempRange:
        sig_name = "TelmClimaTSetTempRange"
        sig_start_bit = 36
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 15.5
        sig_value_min = 0
        sig_value_max = 26
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 36
        byte = 4
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class TelmSeatSecRiVentnClimaLvl:
        sig_name = "TelmSeatSecRiVentnClimaLvl"
        sig_start_bit = 57
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class BgmToPotBodyDiagReqFrame:
    msg_name = "BgmToPotBodyDiagReqFrame"
    msg_id = 1813
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyFr48:
    msg_name = "CemBodyFr48"
    msg_id = 855
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class TelmSeatPassHeatClimaLvl:
        sig_name = "TelmSeatPassHeatClimaLvl"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TelmSeatDrvVentnClimaLvl:
        sig_name = "TelmSeatDrvVentnClimaLvl"
        sig_start_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 35
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class TelmSeatDrvHeatClimaLvl:
        sig_name = "TelmSeatDrvHeatClimaLvl"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmSeatClimaLvl_off': 0, 'TelmSeatClimaLvl_Lvl1': 1, 'TelmSeatClimaLvl_Lvl2': 2, 'TelmSeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class TelmPM25Req:
        sig_name = "TelmPM25Req"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HMIClimaEgySaveReq:
        sig_name = "HMIClimaEgySaveReq"
        sig_start_bit = 57
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01BlckInd_Disabled': 0, 'VentnActr01BlckInd_Enabled': 1, 'VentnActr01BlckInd_Reserved': 2, 'VentnActr01BlckInd_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 57
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class MirrPosnFromCldAtPassMirrPosnAdjCldLeRi:
        sig_name = "MirrPosnFromCldAtPassMirrPosnAdjCldLeRi"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 180
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

    class MirrPosnFromCldAtPassMirrPosnAdjCldUpDwn:
        sig_name = "MirrPosnFromCldAtPassMirrPosnAdjCldUpDwn"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 180
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

    class TelmAirFragTasteReq:
        sig_name = "TelmAirFragTasteReq"
        sig_start_bit = 50
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TelmAirFragChReq_NoReq': 0, 'TelmAirFragChReq_Ch1': 1, 'TelmAirFragChReq_Ch2': 2, 'TelmAirFragChReq_Ch3': 3, 'TelmAirFragChReq_Ch4': 4, 'TelmAirFragChReq_Ch5': 5}
        compute_method = None
        length = 3
        startbit = 50
        byte = 6
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class ClimaRqrd1:
        sig_name = "ClimaRqrd1"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffNoReq_NoReq': 0, 'OnOffNoReq_On': 1, 'OnOffNoReq_Off': 2}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HmiEcoClimaSetgOnOff1:
        sig_name = "HmiEcoClimaSetgOnOff1"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class MirrPosnFromCldAtDrvrMirrPosnAdjCldLeRi:
        sig_name = "MirrPosnFromCldAtDrvrMirrPosnAdjCldLeRi"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 180
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

    class MirrPosnFromCldAtDrvrMirrPosnAdjCldUpDwn:
        sig_name = "MirrPosnFromCldAtDrvrMirrPosnAdjCldUpDwn"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 180
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

    class ReqFragLvlTelm:
        sig_name = "ReqFragLvlTelm"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqFragLvl_OFF': 0, 'ReqFragLvl_Level1': 1, 'ReqFragLvl_Level2': 2, 'ReqFragLvl_Level3': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HmiEcoClimaSetgIdPen:
        sig_name = "HmiEcoClimaSetgIdPen"
        sig_start_bit = 62
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdPen_ProfUkwn': 0, 'IdPen_Prof1': 1, 'IdPen_Prof2': 2, 'IdPen_Prof3': 3, 'IdPen_Prof4': 4, 'IdPen_Prof5': 5, 'IdPen_Prof6': 6, 'IdPen_Prof7': 7, 'IdPen_Prof8': 8, 'IdPen_Prof9': 9, 'IdPen_Prof10': 10, 'IdPen_Prof11': 11, 'IdPen_Prof12': 12, 'IdPen_Prof13': 13, 'IdPen_Resd14': 14, 'IdPen_ProfAll': 15}
        compute_method = None
        length = 4
        startbit = 62
        byte = 7
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3


class CemBodyFr60:
    msg_name = "CemBodyFr60"
    msg_id = 300
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class CmptmtRelHum:
        sig_name = "CmptmtRelHum"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 200
        sig_value_init = 80
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CmptmtFrntWindT:
        sig_name = "CmptmtFrntWindT"
        sig_start_bit = 50
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-40.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 650
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 50
        bmuws_info = [(6, 0b00000111, 0b11111000, 3, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class TempPodSys:
        sig_name = "TempPodSys"
        sig_start_bit = 38
        sig_length = 7
        sig_value_factor = 1.0
        sig_value_offset = "-40.0"
        sig_value_min = 0
        sig_value_max = 125
        sig_value_init = 121
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 38
        byte = 4
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CmptmtFrntWindDewT:
        sig_name = "CmptmtFrntWindDewT"
        sig_start_bit = 47
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-40.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11100000, 0b00011111, 3, 5)]


class CcmBodyFr48:
    msg_name = "CcmBodyFr48"
    msg_id = 1155
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig4Byte7:
        sig_name = "CcmCaliSig4Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig4Byte0:
        sig_name = "CcmCaliSig4Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig4Byte6:
        sig_name = "CcmCaliSig4Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig4Byte2:
        sig_name = "CcmCaliSig4Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig4Byte1:
        sig_name = "CcmCaliSig4Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig4Byte3:
        sig_name = "CcmCaliSig4Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig4Byte4:
        sig_name = "CcmCaliSig4Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig4Byte5:
        sig_name = "CcmCaliSig4Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CcmBodyFr41:
    msg_name = "CcmBodyFr41"
    msg_id = 600
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class HvacModFlapActlPosnSecRowRi:
        sig_name = "HvacModFlapActlPosnSecRowRi"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class HvacRecFlapActlPosn:
        sig_name = "HvacRecFlapActlPosn"
        sig_start_bit = 31
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11000000, 0b00111111, 2, 6)]

    class HvacOsaFlapActlPosn:
        sig_name = "HvacOsaFlapActlPosn"
        sig_start_bit = 33
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HvacModFlapActlPosnSecRowLe:
        sig_name = "HvacModFlapActlPosnSecRowLe"
        sig_start_bit = 9
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]


class CEMBodyFr24:
    msg_name = "CEMBodyFr24"
    msg_id = 656
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.445
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class CnctSrvFragChRatReqFragRatForCh2:
        sig_name = "CnctSrvFragChRatReqFragRatForCh2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class CnctSrvFragChRatReqFragRatForCh1:
        sig_name = "CnctSrvFragChRatReqFragRatForCh1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class CnctSrvFragLvlReq:
        sig_name = "CnctSrvFragLvlReq"
        sig_start_bit = 46
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LvlOff': 0, 'Lvl1': 1, 'Lvl2': 2, 'Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 46
        byte = 5
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class CnctSrvFragChRatReqFragRatForCh5:
        sig_name = "CnctSrvFragChRatReqFragRatForCh5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class CnctSrvFragChRatReqFragRatForCh3:
        sig_name = "CnctSrvFragChRatReqFragRatForCh3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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

    class CnctSrvFragChRatReqFragRatForCh4:
        sig_name = "CnctSrvFragChRatReqFragRatForCh4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
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


class CemBodyFr51:
    msg_name = "CemBodyFr51"
    msg_id = 951
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.285
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HmiFragraChRatReqFragRatForCh4:
        sig_name = "HmiFragraChRatReqFragRatForCh4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_value_init = 100
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HmiFragraChRatReqFragRatForCh5:
        sig_name = "HmiFragraChRatReqFragRatForCh5"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_value_init = 100
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HmiMaxACReq:
        sig_name = "HmiMaxACReq"
        sig_start_bit = 44
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
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HmiFragraChRatReqFragRatForCh1:
        sig_name = "HmiFragraChRatReqFragRatForCh1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_value_init = 100
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HmiFragraChRatReqFragRatForCh3:
        sig_name = "HmiFragraChRatReqFragRatForCh3"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_value_init = 100
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HmiFragraChRatReqFragRatForCh2:
        sig_name = "HmiFragraChRatReqFragRatForCh2"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 100
        sig_value_init = 100
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 15
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class SwtrBodyCANNmFr:
    msg_name = "SwtrBodyCANNmFr"
    msg_id = 1314
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CemBodyFr74:
    msg_name = "CemBodyFr74"
    msg_id = 309
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.135
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class SeatLenAdjmtRowFirstPass:
        sig_name = "SeatLenAdjmtRowFirstPass"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SeatCushTiltAdjmtRowFirstPass:
        sig_name = "SeatCushTiltAdjmtRowFirstPass"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class SeatLenAdjmtRowFirstDrvr:
        sig_name = "SeatLenAdjmtRowFirstDrvr"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BackRestAdjmtRowFirstDrvr:
        sig_name = "BackRestAdjmtRowFirstDrvr"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SeatHeiAdjmtRowFirstPass:
        sig_name = "SeatHeiAdjmtRowFirstPass"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class SeatCushTiltAdjmtRowFirstDrvr:
        sig_name = "SeatCushTiltAdjmtRowFirstDrvr"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SeatHeiAdjmtRowFirstDrvr:
        sig_name = "SeatHeiAdjmtRowFirstDrvr"
        sig_start_bit = 15
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class BackRestAdjmtRowFirstPass:
        sig_name = "BackRestAdjmtRowFirstPass"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class BgmToSmdBodyDiagReqFrame:
    msg_name = "BgmToSmdBodyDiagReqFrame"
    msg_id = 1831
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CemBodyFr02:
    msg_name = "CemBodyFr02"
    msg_id = 64
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class TrNoKeyPrsntAcoustReq:
        sig_name = "TrNoKeyPrsntAcoustReq"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class LcmaIndcnRi:
        sig_name = "LcmaIndcnRi"
        sig_start_bit = 63
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WarnLvl_NoWarn': 0, 'WarnLvl_WarnLvl1': 1, 'WarnLvl_WarnLvl2_NoAudio': 2, 'WarnLvl_WarnLvl3_Audio': 3}
        compute_method = None
        length = 2
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class TwliBriSts:
        sig_name = "TwliBriSts"
        sig_start_bit = 23
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TwliBriSts1_Night': 0, 'TwliBriSts1_Day': 1}
        compute_method = None
        length = 1
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DoorLeReSts:
        sig_name = "DoorLeReSts"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LcmaIndcnLe:
        sig_name = "LcmaIndcnLe"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WarnLvl_NoWarn': 0, 'WarnLvl_WarnLvl1': 1, 'WarnLvl_WarnLvl2_NoAudio': 2, 'WarnLvl_WarnLvl3_Audio': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class SaveSetgToMemPrmnt:
        sig_name = "SaveSetgToMemPrmnt"
        sig_start_bit = 49
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OffOnAut1_Off': 0, 'OffOnAut1_On': 1, 'OffOnAut1_Aut': 2}
        compute_method = None
        length = 2
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DoorDrvrSts:
        sig_name = "DoorDrvrSts"
        sig_start_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class VehMtnStChks:
        sig_name = "VehMtnStChks"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class IHUAPSts:
        sig_name = "IHUAPSts"
        sig_start_bit = 58
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
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class VehMtnStVehMtnSt:
        sig_name = "VehMtnStVehMtnSt"
        sig_start_bit = 2
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehMtnSt2_Ukwn': 0, 'VehMtnSt2_StandStillVal1': 1, 'VehMtnSt2_StandStillVal2': 2, 'VehMtnSt2_StandStillVal3': 3, 'VehMtnSt2_RollgFwdVal1': 4, 'VehMtnSt2_RollgFwdVal2': 5, 'VehMtnSt2_RollgBackwVal1': 6, 'VehMtnSt2_RollgBackwVal2': 7}
        compute_method = None
        length = 3
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class TrOpenerReqTrigSrc:
        sig_name = "TrOpenerReqTrigSrc"
        sig_start_bit = 18
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrOpenerTrigSrc1_TrNoTrigSrc': 0, 'TrOpenerTrigSrc1_TrKeyRem': 1, 'TrOpenerTrigSrc1_TrSwtIntr': 2, 'TrOpenerTrigSrc1_TrByFootOper': 3, 'TrOpenerTrigSrc1_TrHndlOutd': 4, 'TrOpenerTrigSrc1_TrShutFace': 5, 'TrOpenerTrigSrc1_TrHMI': 6, 'TrOpenerTrigSrc1_TrByAppch': 7}
        compute_method = None
        length = 3
        startbit = 18
        byte = 2
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class WinGlbCmd:
        sig_name = "WinGlbCmd"
        sig_start_bit = 34
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OpenClsGlbCmd_Idle': 0, 'OpenClsGlbCmd_GlobalOpenWindow': 1, 'OpenClsGlbCmd_GlobalCloseWindowAndSunroof': 2, 'OpenClsGlbCmd_GlobalCloseWindow': 3, 'OpenClsGlbCmd_GlobalStop': 4, 'OpenClsGlbCmd_Resd1': 5, 'OpenClsGlbCmd_Resd2': 6, 'OpenClsGlbCmd_Resd3': 7}
        compute_method = None
        length = 3
        startbit = 34
        byte = 4
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class PassLoadAndStoreReqErgoPosn:
        sig_name = "PassLoadAndStoreReqErgoPosn"
        sig_start_bit = 28
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PassMemPosn_Idle': 0, 'PassMemPosn_MemBnk1': 1, 'PassMemPosn_MemBnk2': 2, 'PassMemPosn_MemBnk3': 3}
        compute_method = None
        length = 2
        startbit = 28
        byte = 3
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class DoorPassIntrSwtLedLockgCmd:
        sig_name = "DoorPassIntrSwtLedLockgCmd"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PassLoadAndStoreReqErgoSetgEve:
        sig_name = "PassLoadAndStoreReqErgoSetgEve"
        sig_start_bit = 26
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EveMemPosn_Idle': 0, 'EveMemPosn_Store': 1, 'EveMemPosn_Load': 2, 'EveMemPosn_Stop': 3, 'EveMemPosn_AutMovmt': 4, 'EveMemPosn_Upload': 5, 'EveMemPosn_Download': 6, 'EveMemPosn_Clear': 7}
        compute_method = None
        length = 3
        startbit = 26
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class TrOpenerReqTrOpenerReq:
        sig_name = "TrOpenerReqTrOpenerReq"
        sig_start_bit = 21
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TrOpenerReq1_TrOpenerIdle': 0, 'TrOpenerReq1_TrOpenerOpen': 1, 'TrOpenerReq1_TrOpenerCls': 2, 'TrOpenerReq1_TrOpenerStop': 3, 'TrOpenerReq1_TrOpenerClsDly': 4}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class VehMtnStCntr:
        sig_name = "VehMtnStCntr"
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

    class DoorDrvrIntrSwtLedLockgCmd:
        sig_name = "DoorDrvrIntrSwtLedLockgCmd"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class CEMBodyFr32:
    msg_name = "CEMBodyFr32"
    msg_id = 896
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.045
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class IndcrPatCmd1WdTiOn:
        sig_name = "IndcrPatCmd1WdTiOn"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class ClimaPwrAllwd:
        sig_name = "ClimaPwrAllwd"
        sig_start_bit = 34
        sig_length = 11
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 34
        bmuws_info = [(4, 0b00000111, 0b11111000, 3, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class IndcrPatCmd1WdTiOff:
        sig_name = "IndcrPatCmd1WdTiOff"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = 0.001
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 65535
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class DoorLeReIntrSwtLedLockgCmd:
        sig_name = "DoorLeReIntrSwtLedLockgCmd"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DoorRiReIntrSwtLedLockgCmd:
        sig_name = "DoorRiReIntrSwtLedLockgCmd"
        sig_start_bit = 54
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
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class CcmBodyFr35:
    msg_name = "CcmBodyFr35"
    msg_id = 851
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmIntelliClimaResd1:
        sig_name = "CcmIntelliClimaResd1"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmIntelliClimaResd11:
        sig_name = "CcmIntelliClimaResd11"
        sig_start_bit = 15
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class CcmIntelliClimaResd10:
        sig_name = "CcmIntelliClimaResd10"
        sig_start_bit = 47
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]


class CemBodyFr46:
    msg_name = "CemBodyFr46"
    msg_id = 928
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.285
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class HmiElecAirSwngReqDrvrLeRiSwng:
        sig_name = "HmiElecAirSwngReqDrvrLeRiSwng"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class HmiAutDefrstReq:
        sig_name = "HmiAutDefrstReq"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HmiFragraLvlReq:
        sig_name = "HmiFragraLvlReq"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LvlOff': 0, 'Lvl1': 1, 'Lvl2': 2, 'Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HmiCmptmtAirDistbnFrntLe:
        sig_name = "HmiCmptmtAirDistbnFrntLe"
        sig_start_bit = 15
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtAirDistbnFrnt_Flr': 0, 'HmiCmptmtAirDistbnFrnt_Vent': 1, 'HmiCmptmtAirDistbnFrnt_Defrst': 2, 'HmiCmptmtAirDistbnFrnt_FlrDefrst': 3, 'HmiCmptmtAirDistbnFrnt_FlrVent': 4, 'HmiCmptmtAirDistbnFrnt_VentDefrst': 5, 'HmiCmptmtAirDistbnFrnt_FlrVentDefrst': 6, 'HmiCmptmtAirDistbnFrnt_Aut': 7}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HmiFragraModReq:
        sig_name = "HmiFragraModReq"
        sig_start_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiFragraModReq_Single': 0, 'HmiFragraModReq_Mix': 1, 'HmiFragraModReq_Scene': 2, 'HmiFragraModReq_Reserve': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class HmiClimaReAutReq:
        sig_name = "HmiClimaReAutReq"
        sig_start_bit = 17
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
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HmiElecAirSwngReqPassLeRiSwng:
        sig_name = "HmiElecAirSwngReqPassLeRiSwng"
        sig_start_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HmiAutDefrstEna:
        sig_name = "HmiAutDefrstEna"
        sig_start_bit = 20
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HmiElecAirDirModReqPassMod:
        sig_name = "HmiElecAirDirModReqPassMod"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AirDirModReq_Normal': 0, 'AirDirModReq_Focus': 1, 'AirDirModReq_Avoid': 2, 'AirDirModReq_Customize': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HmiClimaFrntAutReq:
        sig_name = "HmiClimaFrntAutReq"
        sig_start_bit = 18
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
        startbit = 18
        byte = 2
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class HmiElecAirSwngReqDrvrUpOnSwng:
        sig_name = "HmiElecAirSwngReqDrvrUpOnSwng"
        sig_start_bit = 38
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
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class HmiElecAirSwngReqPassUpOnSwng:
        sig_name = "HmiElecAirSwngReqPassUpOnSwng"
        sig_start_bit = 36
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HmiCmptmtAirDistbnFrntRi:
        sig_name = "HmiCmptmtAirDistbnFrntRi"
        sig_start_bit = 12
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtAirDistbnFrnt_Flr': 0, 'HmiCmptmtAirDistbnFrnt_Vent': 1, 'HmiCmptmtAirDistbnFrnt_Defrst': 2, 'HmiCmptmtAirDistbnFrnt_FlrDefrst': 3, 'HmiCmptmtAirDistbnFrnt_FlrVent': 4, 'HmiCmptmtAirDistbnFrnt_VentDefrst': 5, 'HmiCmptmtAirDistbnFrnt_FlrVentDefrst': 6, 'HmiCmptmtAirDistbnFrnt_Aut': 7}
        compute_method = None
        length = 3
        startbit = 12
        byte = 1
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class HmiCmptmtAirDistbnRe:
        sig_name = "HmiCmptmtAirDistbnRe"
        sig_start_bit = 23
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HmiCmptmtAirDistbnFrnt_Flr': 0, 'HmiCmptmtAirDistbnFrnt_Vent': 1, 'HmiCmptmtAirDistbnFrnt_Defrst': 2, 'HmiCmptmtAirDistbnFrnt_FlrDefrst': 3, 'HmiCmptmtAirDistbnFrnt_FlrVent': 4, 'HmiCmptmtAirDistbnFrnt_VentDefrst': 5, 'HmiCmptmtAirDistbnFrnt_FlrVentDefrst': 6, 'HmiCmptmtAirDistbnFrnt_Aut': 7}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CmprSpdAct:
        sig_name = "CmprSpdAct"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 50.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 254
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

    class HmiElecAirDirModReqDrvrMod:
        sig_name = "HmiElecAirDirModReqDrvrMod"
        sig_start_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AirDirModReq_Normal': 0, 'AirDirModReq_Focus': 1, 'AirDirModReq_Avoid': 2, 'AirDirModReq_Customize': 3}
        compute_method = None
        length = 2
        startbit = 35
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HmiHumCtrlEna:
        sig_name = "HmiHumCtrlEna"
        sig_start_bit = 61
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class CemBodyFr108:
    msg_name = "CemBodyFr108"
    msg_id = 243
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class ActvnOfPudLi:
        sig_name = "ActvnOfPudLi"
        sig_start_bit = 53
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
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class BgmToRrdmBodyDiagReqFrame:
    msg_name = "BgmToRrdmBodyDiagReqFrame"
    msg_id = 1826
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CcmBodyFr43:
    msg_name = "CcmBodyFr43"
    msg_id = 607
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class TgtHvacAirTForRowSecRi:
        sig_name = "TgtHvacAirTForRowSecRi"
        sig_start_bit = 55
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111000, 0b00000111, 5, 3)]

    class TgtHvacAirTForRowSecLe:
        sig_name = "TgtHvacAirTForRowSecLe"
        sig_start_bit = 39
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class TgtHvacAirTForRowFirstRi:
        sig_name = "TgtHvacAirTForRowFirstRi"
        sig_start_bit = 23
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111000, 0b00000111, 5, 3)]

    class TgtHvacAirTForRowFirstLe:
        sig_name = "TgtHvacAirTForRowFirstLe"
        sig_start_bit = 7
        sig_length = 13
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = -2560
        sig_value_max = 2559
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]


class CemBodyFr70:
    msg_name = "CemBodyFr70"
    msg_id = 257
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.065
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class CustomModSeatDrvrRela:
        sig_name = "CustomModSeatDrvrRela"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RainDetected:
        sig_name = "RainDetected"
        sig_start_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class CustomModSeatSeatAdjmt:
        sig_name = "CustomModSeatSeatAdjmt"
        sig_start_bit = 61
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Adjmt4_Idle': 0, 'Adjmt4_Save': 1, 'Adjmt4_Move': 2}
        compute_method = None
        length = 2
        startbit = 61
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CustomModSeatPassRela:
        sig_name = "CustomModSeatPassRela"
        sig_start_bit = 62
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
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CustomModSeatSecRiRela:
        sig_name = "CustomModSeatSecRiRela"
        sig_start_bit = 58
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
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CustomModSeatSecLeRela:
        sig_name = "CustomModSeatSecLeRela"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class CustomModSeatCustomModSeld:
        sig_name = "CustomModSeatCustomModSeld"
        sig_start_bit = 50
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModSeld_NoSeld': 0, 'ModSeld_CustomizationMod1': 1, 'ModSeld_CustomizationMod2': 2, 'ModSeld_CustomizationMod3': 3}
        compute_method = None
        length = 3
        startbit = 50
        byte = 6
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class HvBattSoc:
        sig_name = "HvBattSoc"
        sig_start_bit = 23
        sig_length = 11
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11100000, 0b00011111, 3, 5)]


class SmbrBodyFr02:
    msg_name = "SmbrBodyFr02"
    msg_id = 301
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class SeatVentnLvlStsRowSecRi:
        sig_name = "SeatVentnLvlStsRowSecRi"
        sig_start_bit = 20
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class SecRowSeatVentnActlPwrCnsRi:
        sig_name = "SecRowSeatVentnActlPwrCnsRi"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class SecRowSeatHeatgActlPwrCnsRi:
        sig_name = "SecRowSeatHeatgActlPwrCnsRi"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class SecRowSeatVentnDesPwrCnsRi:
        sig_name = "SecRowSeatVentnDesPwrCnsRi"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class SecRowSeatHeatgDesPwrCnsRi:
        sig_name = "SecRowSeatHeatgDesPwrCnsRi"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CcmBodyFr36:
    msg_name = "CcmBodyFr36"
    msg_id = 856
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmIntelliClimaResd6:
        sig_name = "CcmIntelliClimaResd6"
        sig_start_bit = 47
        sig_length = 16
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class CcmIntelliClimaResd12:
        sig_name = "CcmIntelliClimaResd12"
        sig_start_bit = 15
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 15
        bmuws_info = [(1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class CcmIntelliClimaResd2:
        sig_name = "CcmIntelliClimaResd2"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class BgmToEtcmBodyDiagReqFrame:
    msg_name = "BgmToEtcmBodyDiagReqFrame"
    msg_id = 1814
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CEMBodyFr11:
    msg_name = "CEMBodyFr11"
    msg_id = 224
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class TrSts:
        sig_name = "TrSts"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IntrBriSts:
        sig_name = "IntrBriSts"
        sig_start_bit = 43
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
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DoorPassSts:
        sig_name = "DoorPassSts"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class DoorRiReSts:
        sig_name = "DoorRiReSts"
        sig_start_bit = 13
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorSts2_Ukwn': 0, 'DoorSts2_Opend': 1, 'DoorSts2_Clsd': 2}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class TopPosTrFromHmi:
        sig_name = "TopPosTrFromHmi"
        sig_start_bit = 58
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PosPerc1_NoReq': 0, 'PosPerc1_0to20PercTopPos': 1, 'PosPerc1_21to40PercTopPos': 2, 'PosPerc1_41to60PercTopPos': 3, 'PosPerc1_61to80PercTopPos': 4, 'PosPerc1_81to100PercTopPos': 5}
        compute_method = None
        length = 3
        startbit = 58
        byte = 7
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class SteerWhlHeatgDesPwr:
        sig_name = "SteerWhlHeatgDesPwr"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class MirrTintgCmd:
        sig_name = "MirrTintgCmd"
        sig_start_bit = 54
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 54
        byte = 6
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class HvPwrAvlForClimaEstimd:
        sig_name = "HvPwrAvlForClimaEstimd"
        sig_start_bit = 25
        sig_length = 10
        sig_value_factor = 20.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class TrPosnUpprProgmReq:
        sig_name = "TrPosnUpprProgmReq"
        sig_start_bit = 28
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
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class SmpBodyFr03:
    msg_name = "SmpBodyFr03"
    msg_id = 1063
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class PassSeatHeatgLvlSts:
        sig_name = "PassSeatHeatgLvlSts"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PassSeatSwtSts2PassSeatSwtInclSts:
        sig_name = "PassSeatSwtSts2PassSeatSwtInclSts"
        sig_start_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PassMassgRunng:
        sig_name = "PassMassgRunng"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PassSeatSwtSts2PassSeatSwtHeiSts:
        sig_name = "PassSeatSwtSts2PassSeatSwtHeiSts"
        sig_start_bit = 47
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 47
        byte = 5
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctHozlSts:
        sig_name = "PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctHozlSts"
        sig_start_bit = 25
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PassSeatSwtSts2PassSeatSwtSelnOfSpplFctStsSts:
        sig_name = "PassSeatSwtSts2PassSeatSwtSelnOfSpplFctStsSts"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PassSeatSwtSts2PassSeatSwtHdrstHozlSts:
        sig_name = "PassSeatSwtSts2PassSeatSwtHdrstHozlSts"
        sig_start_bit = 37
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 37
        byte = 4
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctVerSts:
        sig_name = "PassSeatSwtSts2PassSeatSwtAdjmtOfSpplFctVerSts"
        sig_start_bit = 39
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 39
        byte = 4
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PassSeatSwtSts2PassSeatSwtSldSts:
        sig_name = "PassSeatSwtSts2PassSeatSwtSldSts"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtHozlSts1_Idle': 0, 'SwtHozlSts1_Fwd': 1, 'SwtHozlSts1_Backw': 2}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PassSeatVentnLvlSts:
        sig_name = "PassSeatVentnLvlSts"
        sig_start_bit = 20
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatClimaLvl_Off': 0, 'SeatClimaLvl_Lvl1': 1, 'SeatClimaLvl_Lvl2': 2, 'SeatClimaLvl_Lvl3': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class PassSeatActvSpplFct:
        sig_name = "PassSeatActvSpplFct"
        sig_start_bit = 4
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SeatActvSpplFct1_NotAvl': 0, 'SeatActvSpplFct1_LumExtnAndLumHei': 1, 'SeatActvSpplFct1_BackBlster': 2, 'SeatActvSpplFct1_CushExtn': 3, 'SeatActvSpplFct1_HdrestHeiAndHdrestTilt': 4, 'SeatActvSpplFct1_MassgFct': 5, 'SeatActvSpplFct1_ShoulderFct': 6, 'SeatActvSpplFct1_LegrestFct': 7}
        compute_method = None
        length = 3
        startbit = 4
        byte = 0
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class PassSeatSwtSts2PassSeatSwtHeiFrntSts:
        sig_name = "PassSeatSwtSts2PassSeatSwtHeiFrntSts"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class PassSeatVentAvlSts:
        sig_name = "PassSeatVentAvlSts"
        sig_start_bit = 13
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StsFd_None': 0, 'StsFd_On': 1, 'StsFd_Off': 2, 'StsFd_Error': 3, 'StsFd_Functionallimit': 4, 'StsFd_Energylimit': 5, 'StsFd_Resvd1': 6, 'StsFd_Resvd2': 7}
        compute_method = None
        length = 3
        startbit = 13
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class PassSeatSwtSts2PassSeatSwtHdrstVertSts:
        sig_name = "PassSeatSwtSts2PassSeatSwtHdrstVertSts"
        sig_start_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SwtVertSts1_Idle': 0, 'SwtVertSts1_Up': 1, 'SwtVertSts1_Dwn': 2}
        compute_method = None
        length = 2
        startbit = 35
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class PassSeatHeatgAvlSts:
        sig_name = "PassSeatHeatgAvlSts"
        sig_start_bit = 10
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StsFd_None': 0, 'StsFd_On': 1, 'StsFd_Off': 2, 'StsFd_Error': 3, 'StsFd_Functionallimit': 4, 'StsFd_Energylimit': 5, 'StsFd_Resvd1': 6, 'StsFd_Resvd2': 7}
        compute_method = None
        length = 3
        startbit = 10
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0


class DdmBodyFr03:
    msg_name = "DdmBodyFr03"
    msg_id = 291
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class AmbTURawAtDrvrSide:
        sig_name = "AmbTURawAtDrvrSide"
        sig_start_bit = 55
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = "-70"
        sig_value_min = 0
        sig_value_max = 4095
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11110000, 0b00001111, 4, 4)]

    class MirrPosnToCldAtDrvrMirrPosnAdjCldLeRi:
        sig_name = "MirrPosnToCldAtDrvrMirrPosnAdjCldLeRi"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 180
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

    class MirrDwnStsAtDrvr:
        sig_name = "MirrDwnStsAtDrvr"
        sig_start_bit = 18
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MirrDwnStsTyp_MirrTiltUndefd': 0, 'MirrDwnStsTyp_MirrUpPosn': 1, 'MirrDwnStsTyp_MirrTiltPosn': 2, 'MirrDwnStsTyp_MirrMovgToUpPosn': 3, 'MirrDwnStsTyp_MirrMovgToTiltPosn': 4}
        compute_method = None
        length = 3
        startbit = 18
        byte = 2
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class DoorDrvrCinhIntFailInfCinchRestFlt:
        sig_name = "DoorDrvrCinhIntFailInfCinchRestFlt"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 44
        byte = 5
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class DoorDrvrCinhIntFailInfCinchFlt1:
        sig_name = "DoorDrvrCinhIntFailInfCinchFlt1"
        sig_start_bit = 45
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class MirrPosnToCldAtDrvrMirrPosnAdjCldUpDwn:
        sig_name = "MirrPosnToCldAtDrvrMirrPosnAdjCldUpDwn"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 180
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

    class DoorDrvrHndlSts:
        sig_name = "DoorDrvrHndlSts"
        sig_start_bit = 21
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DoorHndlSts_Ukwn': 0, 'DoorHndlSts_FullRtrctd': 1, 'DoorHndlSts_MovgOut': 2, 'DoorHndlSts_StopDurgDply': 3, 'DoorHndlSts_FullDplyd': 4, 'DoorHndlSts_MovgIn': 5, 'DoorHndlSts_StopDurgRtrct': 6, 'DoorHndlSts_Flt': 7}
        compute_method = None
        length = 3
        startbit = 21
        byte = 2
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3


class BgmToSwtrBodyDiagReqFrame:
    msg_name = "BgmToSwtrBodyDiagReqFrame"
    msg_id = 1923
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []


class CcmBodyFr42:
    msg_name = "CcmBodyFr42"
    msg_id = 604
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class HvacTempFlapActlPosnFrstRowLe:
        sig_name = "HvacTempFlapActlPosnFrstRowLe"
        sig_start_bit = 7
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class IntCo2RunSts:
        sig_name = "IntCo2RunSts"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PmSnsrSts_Initial': 0, 'PmSnsrSts_Collecting': 1, 'PmSnsrSts_Complete': 2, 'PmSnsrSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvacTempFlapActlPosnFrstRowRi:
        sig_name = "HvacTempFlapActlPosnFrstRowRi"
        sig_start_bit = 9
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class HvacTempFlapActlPosnSecRowLe:
        sig_name = "HvacTempFlapActlPosnSecRowLe"
        sig_start_bit = 31
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11000000, 0b00111111, 2, 6)]

    class InCarCo2HighWarn:
        sig_name = "InCarCo2HighWarn"
        sig_start_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Co2Lvl_Lvl0Slight': 0, 'Co2Lvl_Lvl1Low': 1, 'Co2Lvl_Lvl2Middle': 2, 'Co2Lvl_Lvl3High': 3}
        compute_method = None
        length = 2
        startbit = 35
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class HvacTempFlapActlPosnSecRowRi:
        sig_name = "HvacTempFlapActlPosnSecRowRi"
        sig_start_bit = 33
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 33
        bmuws_info = [(4, 0b00000011, 0b11111100, 2, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirMFlowReEstimd:
        sig_name = "HvacAirMFlowReEstimd"
        sig_start_bit = 49
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 49
        bmuws_info = [(6, 0b00000011, 0b11111100, 2, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class CcmBodyFr45:
    msg_name = "CcmBodyFr45"
    msg_id = 1152
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig1Byte0:
        sig_name = "CcmCaliSig1Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig1Byte3:
        sig_name = "CcmCaliSig1Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig1Byte4:
        sig_name = "CcmCaliSig1Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig1Byte7:
        sig_name = "CcmCaliSig1Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig1Byte5:
        sig_name = "CcmCaliSig1Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig1Byte1:
        sig_name = "CcmCaliSig1Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig1Byte2:
        sig_name = "CcmCaliSig1Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig1Byte6:
        sig_name = "CcmCaliSig1Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class CcmBodyFr50:
    msg_name = "CcmBodyFr50"
    msg_id = 1157
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class CcmCaliSig6Byte6:
        sig_name = "CcmCaliSig6Byte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig6Byte2:
        sig_name = "CcmCaliSig6Byte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig6Byte4:
        sig_name = "CcmCaliSig6Byte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig6Byte1:
        sig_name = "CcmCaliSig6Byte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig6Byte0:
        sig_name = "CcmCaliSig6Byte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig6Byte7:
        sig_name = "CcmCaliSig6Byte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig6Byte3:
        sig_name = "CcmCaliSig6Byte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class CcmCaliSig6Byte5:
        sig_name = "CcmCaliSig6Byte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class DdmBodyFr01:
    msg_name = "DdmBodyFr01"
    msg_id = 48
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class ChdLockRightStsToHmi:
        sig_name = "ChdLockRightStsToHmi"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class MemBtnPsdMemButM:
        sig_name = "MemBtnPsdMemButM"
        sig_start_bit = 11
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class ShortDropWinDrvrSts:
        sig_name = "ShortDropWinDrvrSts"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShortDropSts_Idle': 0, 'ShortDropSts_WindowDown': 1, 'ShortDropSts_WindowClosed': 2, 'ShortDropSts_NotUsed': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class MemBtnPsdMemBtn3:
        sig_name = "MemBtnPsdMemBtn3"
        sig_start_bit = 12
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class MirrFoldStsAtDrvr:
        sig_name = "MirrFoldStsAtDrvr"
        sig_start_bit = 55
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MirrFoldStsTyp_MirrFoldPosnUndefd': 0, 'MirrFoldStsTyp_MirrNotFoldPosn': 1, 'MirrFoldStsTyp_MirrFoldPosn': 2, 'MirrFoldStsTyp_MirrMovgToNotFold': 3, 'MirrFoldStsTyp_MirrMovgToFold': 4}
        compute_method = None
        length = 3
        startbit = 55
        byte = 6
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class FltOfIndcrTurnOnDrvrSide:
        sig_name = "FltOfIndcrTurnOnDrvrSide"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DevErrSts2_NoFlt': 0, 'DevErrSts2_Flt': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class WinFailrStsAtDrvr:
        sig_name = "WinFailrStsAtDrvr"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class MemBtnPsdMemBtn1:
        sig_name = "MemBtnPsdMemBtn1"
        sig_start_bit = 14
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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

    class MemBtnPsdMemBtn2:
        sig_name = "MemBtnPsdMemBtn2"
        sig_start_bit = 13
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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


class PotBodyFr01:
    msg_name = "PotBodyFr01"
    msg_id = 416
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class BodyMissComPrmntFromBoot:
        sig_name = "BodyMissComPrmntFromBoot"
        sig_start_bit = 0
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
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


class CemBodyFr63:
    msg_name = "CemBodyFr63"
    msg_id = 447
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.275
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class StrtInProgs:
        sig_name = "StrtInProgs"
        sig_start_bit = 62
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StrtInProgs1_StrtStsOff': 0, 'StrtInProgs1_StrtStsImminent': 1, 'StrtInProgs1_StrtStsStrtng': 2, 'StrtInProgs1_StrtStsRunng': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class PostDrvgClimaReq:
        sig_name = "PostDrvgClimaReq"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RemStrtExtnTiReq:
        sig_name = "RemStrtExtnTiReq"
        sig_start_bit = 53
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 53
        byte = 6
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0


class CcmBodyDevFr02:
    msg_name = "CcmBodyDevFr02"
    msg_id = 1435
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class DvlpFrameForCCMByte6:
        sig_name = "DvlpFrameForCCMByte6"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DvlpFrameForCCMByte5:
        sig_name = "DvlpFrameForCCMByte5"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DvlpFrameForCCMByte4:
        sig_name = "DvlpFrameForCCMByte4"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DvlpFrameForCCMByte3:
        sig_name = "DvlpFrameForCCMByte3"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DvlpFrameForCCMByte1:
        sig_name = "DvlpFrameForCCMByte1"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DvlpFrameForCCMByte0:
        sig_name = "DvlpFrameForCCMByte0"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DvlpFrameForCCMByte7:
        sig_name = "DvlpFrameForCCMByte7"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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

    class DvlpFrameForCCMByte2:
        sig_name = "DvlpFrameForCCMByte2"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
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


class DdmToBgmBodyDiagRespFrame:
    msg_name = "DdmToBgmBodyDiagRespFrame"
    msg_id = 1554
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']


class CemBodyFr44:
    msg_name = "CemBodyFr44"
    msg_id = 937
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.3
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []

    class PosnBriefPosnLat:
        sig_name = "PosnBriefPosnLat"
        sig_start_bit = 5
        sig_length = 30
        sig_value_factor = "2.7777777777777776E-7"
        sig_value_offset = 0.0
        sig_value_min = -324000000
        sig_value_max = 324000000
        sig_value_init = 324000000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 30
        startbit = 5
        bmuws_info = [(0, 0b00111111, 0b11000000, 6, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class PosnBriefPosnLgt:
        sig_name = "PosnBriefPosnLgt"
        sig_start_bit = 38
        sig_length = 31
        sig_value_factor = "2.7777777777777776E-7"
        sig_value_offset = 0.0
        sig_value_min = -648000000
        sig_value_max = 648000000
        sig_value_init = 648000000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 31
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111111, 0b00000000, 8, 0)]


class DdmBodyFr02:
    msg_name = "DdmBodyFr02"
    msg_id = 480
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class MirrDefrstAtDrvSts:
        sig_name = "MirrDefrstAtDrvSts"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class ChdLockRightFailStsToHmi:
        sig_name = "ChdLockRightFailStsToHmi"
        sig_start_bit = 44
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffSafe1_OnOffSafeInvld1': 0, 'OnOffSafe1_OnOffSafeOn': 1, 'OnOffSafe1_OnOffSafeOff': 2, 'OnOffSafe1_OnOffSafeInvld2': 3}
        compute_method = None
        length = 2
        startbit = 44
        byte = 5
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class AmbTRawAtDrvrSideAmbTVal:
        sig_name = "AmbTRawAtDrvrSideAmbTVal"
        sig_start_bit = 7
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-70.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class AmbTRawAtDrvrSideQly:
        sig_name = "AmbTRawAtDrvrSideQly"
        sig_start_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class CcmBodyFr11:
    msg_name = "CcmBodyFr11"
    msg_id = 1029
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']

    class AirTFbFromClimaDataQf:
        sig_name = "AirTFbFromClimaDataQf"
        sig_start_bit = 0
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DataQf_NotOk': 0, 'DataQf_Ok': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AirTFbFromClimaAirTFbFromClima:
        sig_name = "AirTFbFromClimaAirTFbFromClima"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = -128
        sig_value_max = 127
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

    class CupHoldrActvAllwd:
        sig_name = "CupHoldrActvAllwd"
        sig_start_bit = 25
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class ClimaCmptSts:
        sig_name = "ClimaCmptSts"
        sig_start_bit = 5
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptSts_NoRequest': 0, 'CmptSts_CoolingRequest': 1, 'CmptSts_HeatingRequest': 2, 'CmptSts_CoolingAndHeatingRequest': 3, 'CmptSts_PostHeating': 4}
        compute_method = None
        length = 3
        startbit = 5
        byte = 0
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class ClimaOvrHeatProActv:
        sig_name = "ClimaOvrHeatProActv"
        sig_start_bit = 54
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
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ClimaDefrstSts:
        sig_name = "ClimaDefrstSts"
        sig_start_bit = 28
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
        startbit = 28
        byte = 3
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HvacEvaprTSpFrnt:
        sig_name = "HvacEvaprTSpFrnt"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = "-5.0"
        sig_value_min = 0
        sig_value_max = 250
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

    class HvacEvaprTSpRe:
        sig_name = "HvacEvaprTSpRe"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = "-5.0"
        sig_value_min = 0
        sig_value_max = 250
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


