class AfuCcm_Lin2Fr01:
    msg_name = "AfuCcm_Lin2Fr01"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class AirFragUndVoltErr:
        sig_name = "AirFragUndVoltErr"
        sig_start_bit = 63
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 63
        byte = 7
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AirFragMot3Err:
        sig_name = "AirFragMot3Err"
        sig_start_bit = 57
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 57
        byte = 7
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AirFragChgSts:
        sig_name = "AirFragChgSts"
        sig_start_bit = 45
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Init': 0, 'Changing': 1, 'Changesucceeded': 2, 'Changefailed': 3}
        compute_method = None
        length = 2
        startbit = 45
        byte = 5
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class AirFragCh4Type:
        sig_name = "AirFragCh4Type"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirFragTempErr:
        sig_name = "AirFragTempErr"
        sig_start_bit = 60
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempErr_Normal': 0, 'TempErr_OverTemp': 1, 'TempErr_UnderTemp': 2, 'TempErr_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 60
        byte = 7
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class AirFragCh1Type:
        sig_name = "AirFragCh1Type"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirFragMot2Err:
        sig_name = "AirFragMot2Err"
        sig_start_bit = 56
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AirFragLvlRspn:
        sig_name = "AirFragLvlRspn"
        sig_start_bit = 48
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RatUse_NoRequest': 0, 'RatUse_Low': 1, 'RatUse_Mid': 2, 'RatUse_High': 3}
        compute_method = None
        length = 2
        startbit = 48
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AirFragMot4Err:
        sig_name = "AirFragMot4Err"
        sig_start_bit = 58
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 58
        byte = 7
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AirFragCh3Type:
        sig_name = "AirFragCh3Type"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirFragCh1RunngSts:
        sig_name = "AirFragCh1RunngSts"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AirFragCh3RunngSts:
        sig_name = "AirFragCh3RunngSts"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AirFragOvrVoltErr:
        sig_name = "AirFragOvrVoltErr"
        sig_start_bit = 52
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AirFragMot5Err:
        sig_name = "AirFragMot5Err"
        sig_start_bit = 59
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AirFragCh5Type:
        sig_name = "AirFragCh5Type"
        sig_start_bit = 32
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirFragCh2Type:
        sig_name = "AirFragCh2Type"
        sig_start_bit = 8
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AirFragCh2RunngSts:
        sig_name = "AirFragCh2RunngSts"
        sig_start_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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


class AfuCcm_Lin2SerNrFr01:
    msg_name = "AfuCcm_Lin2SerNrFr01"
    msg_id = 13
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class AFUSerNoNr2:
        sig_name = "AFUSerNoNr2"
        sig_start_bit = 8
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUSerNoNr1:
        sig_name = "AFUSerNoNr1"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUSerNoNr3:
        sig_name = "AFUSerNoNr3"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUSerNoNr4:
        sig_name = "AFUSerNoNr4"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CcsmCcm_Lin2Fr02:
    msg_name = "CcsmCcm_Lin2Fr02"
    msg_id = 30
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 3
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class Btn5ForUsrSwtPanFrntReq:
        sig_name = "Btn5ForUsrSwtPanFrntReq"
        sig_start_bit = 3
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class Btn7:
        sig_name = "Btn7"
        sig_start_bit = 4
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class Btn8:
        sig_name = "Btn8"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class PassSideTInc:
        sig_name = "PassSideTInc"
        sig_start_bit = 13
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class Btn2ForUsrSwtPanFrntReq:
        sig_name = "Btn2ForUsrSwtPanFrntReq"
        sig_start_bit = 2
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class DrvrSideTInc:
        sig_name = "DrvrSideTInc"
        sig_start_bit = 11
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class PassSideTDec:
        sig_name = "PassSideTDec"
        sig_start_bit = 12
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AirVolDec:
        sig_name = "AirVolDec"
        sig_start_bit = 0
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class DiagcCCSM:
        sig_name = "DiagcCCSM"
        sig_start_bit = 8
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DiagcForPanCenCtrl2_NoFlt': 0, 'DiagcForPanCenCtrl2_FanErr': 1, 'DiagcForPanCenCtrl2_OutdURng': 2, 'DiagcForPanCenCtrl2_TmrErr': 3, 'DiagcForPanCenCtrl2_MemErr': 4, 'DiagcForPanCenCtrl2_Spare6': 5, 'DiagcForPanCenCtrl2_Spare7': 6, 'DiagcForPanCenCtrl2_SnrFltT': 7}
        compute_method = None
        length = 3
        startbit = 8
        byte = 1
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class ModBtn:
        sig_name = "ModBtn"
        sig_start_bit = 15
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class Btn9:
        sig_name = "Btn9"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DrvrSideTDec:
        sig_name = "DrvrSideTDec"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class AirVolInc:
        sig_name = "AirVolInc"
        sig_start_bit = 1
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PsdNotPsd_NotPsd': 0, 'PsdNotPsd_Psd': 1}
        compute_method = None
        length = 1
        startbit = 1
        byte = 0
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class CdsCcm_Lin2PartNr10Fr08:
    msg_name = "CdsCcm_Lin2PartNr10Fr08"
    msg_id = 51
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class CDSPartNoCmplNr1:
        sig_name = "CDSPartNoCmplNr1"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNoCmplNr3:
        sig_name = "CDSPartNoCmplNr3"
        sig_start_bit = 40
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNoCmplNr4:
        sig_name = "CDSPartNoCmplNr4"
        sig_start_bit = 48
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNoCmplNr2:
        sig_name = "CDSPartNoCmplNr2"
        sig_start_bit = 32
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNoCmplEndSgn3:
        sig_name = "CDSPartNoCmplEndSgn3"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNoCmplEndSgn2:
        sig_name = "CDSPartNoCmplEndSgn2"
        sig_start_bit = 8
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNoCmplEndSgn1:
        sig_name = "CDSPartNoCmplEndSgn1"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class PmsiCcm_Lin2Fr01:
    msg_name = "PmsiCcm_Lin2Fr01"
    msg_id = 17
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class CmpmtInAirPmDnsty:
        sig_name = "CmpmtInAirPmDnsty"
        sig_start_bit = 0
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class InPm25FanErr:
        sig_name = "InPm25FanErr"
        sig_start_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FanErr_Noerr': 0, 'FanErr_Speedunstable': 1, 'FanErr_Poorcontact': 2, 'FanErr_Brokenline': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class InPm25SnrTempErr:
        sig_name = "InPm25SnrTempErr"
        sig_start_bit = 20
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TempErr_Normal': 0, 'TempErr_OverTemp': 1, 'TempErr_UnderTemp': 2, 'TempErr_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CmpmtInAirPmAQI:
        sig_name = "CmpmtInAirPmAQI"
        sig_start_bit = 11
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmpmtAirPmLvl_Level1': 0, 'CmpmtAirPmLvl_Level2': 1, 'CmpmtAirPmLvl_Level3': 2, 'CmpmtAirPmLvl_Level4': 3, 'CmpmtAirPmLvl_Level5': 4, 'CmpmtAirPmLvl_Level6': 5, 'CmpmtAirPmLvl_Reserved': 6, 'CmpmtAirPmLvl_Invalid': 7}
        compute_method = None
        length = 3
        startbit = 11
        byte = 1
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3

    class InPm25SensrIntErr:
        sig_name = "InPm25SensrIntErr"
        sig_start_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VentnActr01UrgcExist_False': 0, 'VentnActr01UrgcExist_True': 1, 'VentnActr01UrgcExist_Reserved': 2, 'VentnActr01UrgcExist_Signalinvalid': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class InPm25SnsrSts:
        sig_name = "InPm25SnsrSts"
        sig_start_bit = 18
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PmSnsrSts_Initial': 0, 'PmSnsrSts_Collecting': 1, 'PmSnsrSts_Complete': 2, 'PmSnsrSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class InPm25SnsrElecErr:
        sig_name = "InPm25SnsrElecErr"
        sig_start_bit = 16
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PmSnsrErrSts_NoError': 0, 'PmSnsrErrSts_ShortToGroundOrOpenCircuit': 1, 'PmSnsrErrSts_ShortToBatt': 2, 'PmSnsrErrSts_Resvd': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class InPm25SnrVoltgRangErr:
        sig_name = "InPm25SnrVoltgRangErr"
        sig_start_bit = 14
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PmSnrVoltgRangErr_NoError': 0, 'PmSnrVoltgRangErr_Undervoltage': 1, 'PmSnrVoltgRangErr_Overvoltage': 2}
        compute_method = None
        length = 2
        startbit = 14
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class PmsiCcm_Lin2SerNrFr01:
    msg_name = "PmsiCcm_Lin2SerNrFr01"
    msg_id = 35
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class SerNoPMSINr3:
        sig_name = "SerNoPMSINr3"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SerNoPMSINr1:
        sig_name = "SerNoPMSINr1"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SerNoPMSINr4:
        sig_name = "SerNoPMSINr4"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SerNoPMSINr2:
        sig_name = "SerNoPMSINr2"
        sig_start_bit = 8
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CcmCcm_Lin2Fr06:
    msg_name = "CcmCcm_Lin2Fr06"
    msg_id = 15
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class LiForBtn4ForUsrSwtPanFrntCmdCcm:
        sig_name = "LiForBtn4ForUsrSwtPanFrntCmdCcm"
        sig_start_bit = 60
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class LiForBtn5ForUsrSwtPanFrntCmdCcm:
        sig_name = "LiForBtn5ForUsrSwtPanFrntCmdCcm"
        sig_start_bit = 61
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HvacAirMFlowVent:
        sig_name = "HvacAirMFlowVent"
        sig_start_bit = 0
        sig_length = 10
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class AfuCcm_Lin2PartNr10Fr04:
    msg_name = "AfuCcm_Lin2PartNr10Fr04"
    msg_id = 59
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class AFUPartNo10CmplEndSgn1:
        sig_name = "AFUPartNo10CmplEndSgn1"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNo10CmplNr4:
        sig_name = "AFUPartNo10CmplNr4"
        sig_start_bit = 48
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNo10CmplEndSgn3:
        sig_name = "AFUPartNo10CmplEndSgn3"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNo10CmplNr2:
        sig_name = "AFUPartNo10CmplNr2"
        sig_start_bit = 32
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNo10CmplNr3:
        sig_name = "AFUPartNo10CmplNr3"
        sig_start_bit = 40
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNo10CmplNr5:
        sig_name = "AFUPartNo10CmplNr5"
        sig_start_bit = 56
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNo10CmplNr1:
        sig_name = "AFUPartNo10CmplNr1"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNo10CmplEndSgn2:
        sig_name = "AFUPartNo10CmplEndSgn2"
        sig_start_bit = 8
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class AfuCcm_Lin2Fr03:
    msg_name = "AfuCcm_Lin2Fr03"
    msg_id = 40
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class AirFragCh1AvlTi:
        sig_name = "AirFragCh1AvlTi"
        sig_start_bit = 0
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 360
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b10000000, 0b01111111, 1, 7)]

    class AirFragCh5RunngSts:
        sig_name = "AirFragCh5RunngSts"
        sig_start_bit = 60
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class AirFragCh5AvlTi:
        sig_name = "AirFragCh5AvlTi"
        sig_start_bit = 36
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 360
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 36
        bmuws_info = [(4, 0b11110000, 0b00001111, 4, 4), (5, 0b11111000, 0b00000111, 5, 3)]

    class AirFragCh3AvlTi:
        sig_name = "AirFragCh3AvlTi"
        sig_start_bit = 18
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 360
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 18
        bmuws_info = [(2, 0b11111100, 0b00000011, 6, 2), (3, 0b11100000, 0b00011111, 3, 5)]

    class AirFragCh4RunngSts:
        sig_name = "AirFragCh4RunngSts"
        sig_start_bit = 56
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 56
        byte = 7
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AFUGenErr:
        sig_name = "AFUGenErr"
        sig_start_bit = 45
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class AirFragCh4AvlTi:
        sig_name = "AirFragCh4AvlTi"
        sig_start_bit = 27
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 360
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 27
        bmuws_info = [(3, 0b11111000, 0b00000111, 5, 3), (4, 0b11110000, 0b00001111, 4, 4)]

    class AirFragCh2AvlTi:
        sig_name = "AirFragCh2AvlTi"
        sig_start_bit = 9
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 360
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 9
        bmuws_info = [(1, 0b11111110, 0b00000001, 7, 1), (2, 0b11000000, 0b00111111, 2, 6)]


class CdsCcm_Lin2Fr01:
    msg_name = "CdsCcm_Lin2Fr01"
    msg_id = 56
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 3
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class IntCo2RunSts_0_CdsCcm_Lin2SignalIPdu01:
        sig_name = "IntCo2RunSts_0_CdsCcm_Lin2SignalIPdu01"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PmSnsrSts_Initial': 0, 'PmSnsrSts_Collecting': 1, 'PmSnsrSts_Complete': 2, 'PmSnsrSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class IntCo2RunMod:
        sig_name = "IntCo2RunMod"
        sig_start_bit = 19
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CdsRunngMod_Standby': 0, 'CdsRunngMod_ActiveMode': 1}
        compute_method = None
        length = 1
        startbit = 19
        byte = 2
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class IntCo2Lvl:
        sig_name = "IntCo2Lvl"
        sig_start_bit = 16
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Co2Lvl_Lvl0Slight': 0, 'Co2Lvl_Lvl1Low': 1, 'Co2Lvl_Lvl2Middle': 2, 'Co2Lvl_Lvl3High': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class CdsClimaOnReq:
        sig_name = "CdsClimaOnReq"
        sig_start_bit = 18
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class IntCo2LvErr:
        sig_name = "IntCo2LvErr"
        sig_start_bit = 14
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class IntCo2HvErr:
        sig_name = "IntCo2HvErr"
        sig_start_bit = 12
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class IntCo2Conc_0_CdsCcm_Lin2SignalIPdu01:
        sig_name = "IntCo2Conc_0_CdsCcm_Lin2SignalIPdu01"
        sig_start_bit = 0
        sig_length = 10
        sig_value_factor = 10
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11000000, 0b00111111, 2, 6)]

    class IntCo2CircElecErr:
        sig_name = "IntCo2CircElecErr"
        sig_start_bit = 10
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PmSnsrErrSts_NoError': 0, 'PmSnsrErrSts_ShortToGroundOrOpenCircuit': 1, 'PmSnsrErrSts_ShortToBatt': 2, 'PmSnsrErrSts_Resvd': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class VbmrCcm_Lin2Fr01:
    msg_name = "VbmrCcm_Lin2Fr01"
    msg_id = 50
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class HvacFanSts2HvacFanExt2:
        sig_name = "HvacFanSts2HvacFanExt2"
        sig_start_bit = 48
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvacFanSts2HvacFanReSts2:
        sig_name = "HvacFanSts2HvacFanReSts2"
        sig_start_bit = 8
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 8
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacFanReSts2_Na': 0, 'HvacFanReSts2_ILimnActv': 1, 'HvacFanReSts2_SpOk': 2, 'HvacFanReSts2_Resd1': 3, 'HvacFanReSts2_EmgyOff': 4, 'HvacFanReSts2_Resd2': 5, 'HvacFanReSts2_StsInvld2': 8}
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HvacFanSts2HvacFanBattU2_0_VbmrCcm_Lin2SignalIPdu01:
        sig_name = "HvacFanSts2HvacFanBattU2_0_VbmrCcm_Lin2SignalIPdu01"
        sig_start_bit = 40
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvacFanSts2HvacFanBattI2_0_VbmrCcm_Lin2SignalIPdu01:
        sig_name = "HvacFanSts2HvacFanBattI2_0_VbmrCcm_Lin2SignalIPdu01"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = 0.25
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 253
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvacFanSts2HvacFanT2:
        sig_name = "HvacFanSts2HvacFanT2"
        sig_start_bit = 32
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = "-40"
        sig_value_min = 0
        sig_value_max = 250
        sig_byteorder = "Intel"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvacFanSts2HvacFanMotU2:
        sig_name = "HvacFanSts2HvacFanMotU2"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 254
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvacFanSts2HvacFanSw2:
        sig_name = "HvacFanSts2HvacFanSw2"
        sig_start_bit = 56
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 56
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class HvacFanSts2HvacFanHw2:
        sig_name = "HvacFanSts2HvacFanHw2"
        sig_start_bit = 60
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 60
        byte = 7
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class HvacFanSts2HvacFanReSts1:
        sig_name = "HvacFanSts2HvacFanReSts1"
        sig_start_bit = 0
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 32
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacFanReSts1_Na': 0, 'HvacFanReSts1_IntErr': 1, 'HvacFanReSts1_CircSho': 2, 'HvacFanReSts1_Resd1': 3, 'HvacFanReSts1_TOver': 4, 'HvacFanReSts1_Resd2': 5, 'HvacFanReSts1_MotIntrptDetd': 8, 'HvacFanReSts1_Resd3': 9, 'HvacFanReSts1_UHi': 16, 'HvacFanReSts1_Resd4': 17, 'HvacFanReSts1_Uli': 32}
        compute_method = None
        length = 6
        startbit = 0
        byte = 0
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class HvacFanSts2HvacFanStsVld2:
        sig_name = "HvacFanSts2HvacFanStsVld2"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'YesNo1_Yes': 0, 'YesNo1_No': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7


class DiagRequest6:
    msg_name = "DiagRequest6"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']


class DiagResponse6:
    msg_name = "DiagResponse6"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']


class CcmCcm_Lin2Fr05:
    msg_name = "CcmCcm_Lin2Fr05"
    msg_id = 19
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class IntCo2AmbSnsrTmpAmbTEstimd:
        sig_name = "IntCo2AmbSnsrTmpAmbTEstimd"
        sig_start_bit = 0
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-70.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Intel"
        sig_value_init = 950
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class IntCo2SnsrActv:
        sig_name = "IntCo2SnsrActv"
        sig_start_bit = 16
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqSts1_NotReqd': 0, 'ReqSts1_Reqd': 1}
        compute_method = None
        length = 1
        startbit = 16
        byte = 2
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class IntCo2SetStartTime:
        sig_name = "IntCo2SetStartTime"
        sig_start_bit = 48
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 48
        byte = 6
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class IntrBriStsCcm:
        sig_name = "IntrBriStsCcm"
        sig_start_bit = 40
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 40
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class TwliBriStsCcm:
        sig_name = "TwliBriStsCcm"
        sig_start_bit = 13
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'TwliBriSts1_Night': 0, 'TwliBriSts1_Day': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ActvnOfSwtIllmnCenCcm:
        sig_name = "ActvnOfSwtIllmnCenCcm"
        sig_start_bit = 15
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class IntCo2SolarIntenLe:
        sig_name = "IntCo2SolarIntenLe"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = 5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IntCo2SetStopTime:
        sig_name = "IntCo2SetStopTime"
        sig_start_bit = 17
        sig_length = 6
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 59
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 17
        byte = 2
        mask = 0b01111110
        unmask = 0b10000001
        shift = 1

    class IntCo2AmbSnsrTmpAmbTEstimdQf:
        sig_name = "IntCo2AmbSnsrTmpAmbTEstimdQf"
        sig_start_bit = 11
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class IntCo2SolarIntenRi:
        sig_name = "IntCo2SolarIntenRi"
        sig_start_bit = 32
        sig_length = 8
        sig_value_factor = 5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class PmsiCcm_Lin2PartNr10Fr04:
    msg_name = "PmsiCcm_Lin2PartNr10Fr04"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class PMSIPartNo10HwEndSgn2:
        sig_name = "PMSIPartNo10HwEndSgn2"
        sig_start_bit = 8
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNo10HwNr5:
        sig_name = "PMSIPartNo10HwNr5"
        sig_start_bit = 56
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNo10HwNr2:
        sig_name = "PMSIPartNo10HwNr2"
        sig_start_bit = 32
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNo10HwEndSgn3:
        sig_name = "PMSIPartNo10HwEndSgn3"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNo10HwNr1:
        sig_name = "PMSIPartNo10HwNr1"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNo10HwNr3:
        sig_name = "PMSIPartNo10HwNr3"
        sig_start_bit = 40
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNo10HwEndSgn1:
        sig_name = "PMSIPartNo10HwEndSgn1"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNo10HwNr4:
        sig_name = "PMSIPartNo10HwNr4"
        sig_start_bit = 48
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CdsCcm_Lin2SerNrFr01:
    msg_name = "CdsCcm_Lin2SerNrFr01"
    msg_id = 55
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 4
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class CDSSerNoNr4:
        sig_name = "CDSSerNoNr4"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSSerNoNr2:
        sig_name = "CDSSerNoNr2"
        sig_start_bit = 8
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSSerNoNr1:
        sig_name = "CDSSerNoNr1"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSSerNoNr3:
        sig_name = "CDSSerNoNr3"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CcmCcm_Lin2Fr07:
    msg_name = "CcmCcm_Lin2Fr07"
    msg_id = 1
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class CmptmtAirTEstimdExtdComptmtT:
        sig_name = "CmptmtAirTEstimdExtdComptmtT"
        sig_start_bit = 0
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 1850
        sig_byteorder = "Intel"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11100000, 0b00011111, 3, 5)]

    class HvacRecircAct:
        sig_name = "HvacRecircAct"
        sig_start_bit = 16
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 7
        startbit = 16
        byte = 2
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class CmptmtAirTEstimdExtdQlyFlg:
        sig_name = "CmptmtAirTEstimdExtdQlyFlg"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3


class PmsiCcm_Lin1PartNrFr08:
    msg_name = "PmsiCcm_Lin1PartNrFr08"
    msg_id = 25
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class PMSIPartNoHwNr3:
        sig_name = "PMSIPartNoHwNr3"
        sig_start_bit = 40
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNoHwNr4:
        sig_name = "PMSIPartNoHwNr4"
        sig_start_bit = 48
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNoHwEndSgn3:
        sig_name = "PMSIPartNoHwEndSgn3"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNoHwEndSgn2:
        sig_name = "PMSIPartNoHwEndSgn2"
        sig_start_bit = 8
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNoHwNr2:
        sig_name = "PMSIPartNoHwNr2"
        sig_start_bit = 32
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNoHwNr1:
        sig_name = "PMSIPartNoHwNr1"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class PMSIPartNoHwEndSgn1:
        sig_name = "PMSIPartNoHwEndSgn1"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CcmCcm_Lin2Fr04:
    msg_name = "CcmCcm_Lin2Fr04"
    msg_id = 6
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class AirFragCh3:
        sig_name = "AirFragCh3"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class AirFragCh1:
        sig_name = "AirFragCh1"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOff1_Off': 0, 'OnOff1_On': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AirFragCh2:
        sig_name = "AirFragCh2"
        sig_start_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class AirFragCh4:
        sig_name = "AirFragCh4"
        sig_start_bit = 43
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class VehMktForPmSnsrAirMtrlSnsrReq:
        sig_name = "VehMktForPmSnsrAirMtrlSnsrReq"
        sig_start_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AirMtrlSnsrReq_SNA': 0, 'AirMtrlSnsrReq_Off': 1, 'AirMtrlSnsrReq_On': 2, 'AirMtrlSnsrReq_Calibrate': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class VehMktForPmSnsrVehMktGlb:
        sig_name = "VehMktForPmSnsrVehMktGlb"
        sig_start_bit = 48
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 16
        sig_byteorder = "Intel"
        sig_value_init = 10
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VehMktGlb_SNA': 0, 'VehMktGlb_World': 1, 'VehMktGlb_Europe': 2, 'VehMktGlb_NorthAmerica': 3, 'VehMktGlb_SouthAmerica': 4, 'VehMktGlb_MiddleEastAfrica': 5, 'VehMktGlb_SouthEastAsia': 6, 'VehMktGlb_Pacific': 7, 'VehMktGlb_Russia': 8, 'VehMktGlb_Korea': 9, 'VehMktGlb_China': 10, 'VehMktGlb_Taiwan': 11, 'VehMktGlb_Japan': 12, 'VehMktGlb_India': 13, 'VehMktGlb_Israel': 14, 'VehMktGlb_Turkey': 15, 'VehMktGlb_Spare': 16}
        compute_method = None
        length = 5
        startbit = 48
        byte = 6
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class AirFragCh5:
        sig_name = "AirFragCh5"
        sig_start_bit = 44
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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


class CcmCcm_Lin2Fr03:
    msg_name = "CcmCcm_Lin2Fr03"
    msg_id = 39
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class HvacFanSet2HvacFanRxFrq2:
        sig_name = "HvacFanSet2HvacFanRxFrq2"
        sig_start_bit = 0
        sig_length = 12
        sig_value_factor = 1
        sig_value_offset = 150
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Intel"
        sig_value_init = 4095
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11110000, 0b00001111, 4, 4)]

    class HvacFanSet2HvacFanIMaxMax2:
        sig_name = "HvacFanSet2HvacFanIMaxMax2"
        sig_start_bit = 18
        sig_length = 6
        sig_value_factor = 0.5
        sig_value_offset = 8
        sig_value_min = 0
        sig_value_max = 63
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 6
        startbit = 18
        byte = 2
        mask = 0b11111100
        unmask = 0b00000011
        shift = 2

    class HvacFanSet2HvacFanKneeU2:
        sig_name = "HvacFanSet2HvacFanKneeU2"
        sig_start_bit = 29
        sig_length = 3
        sig_value_factor = 0.5
        sig_value_offset = 8.5
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 3
        startbit = 29
        byte = 3
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class AirFragConcReq:
        sig_name = "AirFragConcReq"
        sig_start_bit = 62
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqFragLvl_OFF': 0, 'ReqFragLvl_Level1': 1, 'ReqFragLvl_Level2': 2, 'ReqFragLvl_Level3': 3}
        compute_method = None
        length = 2
        startbit = 62
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class InPm25SnsrActnReq:
        sig_name = "InPm25SnsrActnReq"
        sig_start_bit = 60
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HvacFanSet2HvacFanIMaxMin2:
        sig_name = "HvacFanSet2HvacFanIMaxMin2"
        sig_start_bit = 24
        sig_length = 5
        sig_value_factor = 0.5
        sig_value_offset = 2
        sig_value_min = 0
        sig_value_max = 31
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 5
        startbit = 24
        byte = 3
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class HvacFanSet2HvacSftyRunSpd2:
        sig_name = "HvacFanSet2HvacSftyRunSpd2"
        sig_start_bit = 48
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvacFanSet2HvacFanSeln2:
        sig_name = "HvacFanSet2HvacFanSeln2"
        sig_start_bit = 16
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacFanSeln_BlowerHalf': 0, 'HvacFanSeln_BlowerThreeQuarters': 1, 'HvacFanSeln_Invalid': 2, 'HvacFanSeln_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HvacFanSet2HvacFanRamp2:
        sig_name = "HvacFanSet2HvacFanRamp2"
        sig_start_bit = 36
        sig_length = 4
        sig_value_factor = 0.5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 36
        byte = 4
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AirFragActEnad:
        sig_name = "AirFragActEnad"
        sig_start_bit = 61
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
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

    class HvacFanSet2HvacFanSftyRunThd2:
        sig_name = "HvacFanSet2HvacFanSftyRunThd2"
        sig_start_bit = 32
        sig_length = 4
        sig_value_factor = 0.1
        sig_value_offset = 11.5
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 32
        byte = 4
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class AfuCcm_Lin2Fr02:
    msg_name = "AfuCcm_Lin2Fr02"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 6
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class AirFragInitSts:
        sig_name = "AirFragInitSts"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Noinitialization': 0, 'Initializing': 1, 'InitializationOK': 2, 'Initializationfailed': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class AirFragMot1Err:
        sig_name = "AirFragMot1Err"
        sig_start_bit = 43
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 43
        byte = 5
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AirFragFanErr:
        sig_name = "AirFragFanErr"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0


class AfuCcm_Lin2PartNrFr08:
    msg_name = "AfuCcm_Lin2PartNrFr08"
    msg_id = 53
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class AFUPartNoCmplEndSgn1:
        sig_name = "AFUPartNoCmplEndSgn1"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNoCmplEndSgn2:
        sig_name = "AFUPartNoCmplEndSgn2"
        sig_start_bit = 8
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNoCmplNr1:
        sig_name = "AFUPartNoCmplNr1"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNoCmplNr2:
        sig_name = "AFUPartNoCmplNr2"
        sig_start_bit = 32
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNoCmplNr3:
        sig_name = "AFUPartNoCmplNr3"
        sig_start_bit = 40
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNoCmplEndSgn3:
        sig_name = "AFUPartNoCmplEndSgn3"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AFUPartNoCmplNr4:
        sig_name = "AFUPartNoCmplNr4"
        sig_start_bit = 48
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class CdsCcm_Lin2PartNr10Fr04:
    msg_name = "CdsCcm_Lin2PartNr10Fr04"
    msg_id = 46
    msg_tx_method = "cyclic"
    msg_cycle = 0.073
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['CDC', 'ACU']

    class CDSPartNo10CmplEndSgn1:
        sig_name = "CDSPartNo10CmplEndSgn1"
        sig_start_bit = 0
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNo10CmplNr1:
        sig_name = "CDSPartNo10CmplNr1"
        sig_start_bit = 24
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNo10CmplNr5:
        sig_name = "CDSPartNo10CmplNr5"
        sig_start_bit = 56
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNo10CmplNr3:
        sig_name = "CDSPartNo10CmplNr3"
        sig_start_bit = 40
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 40
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNo10CmplNr2:
        sig_name = "CDSPartNo10CmplNr2"
        sig_start_bit = 32
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 32
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNo10CmplNr4:
        sig_name = "CDSPartNo10CmplNr4"
        sig_start_bit = 48
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 48
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNo10CmplEndSgn2:
        sig_name = "CDSPartNo10CmplEndSgn2"
        sig_start_bit = 8
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 8
        byte = 1
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class CDSPartNo10CmplEndSgn3:
        sig_name = "CDSPartNo10CmplEndSgn3"
        sig_start_bit = 16
        sig_length = 8
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


