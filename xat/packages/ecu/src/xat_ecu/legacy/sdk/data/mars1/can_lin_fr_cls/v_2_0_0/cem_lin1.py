lin_scheduleTable = {'Cem_Lin1_DiagResponseSchedule01': [(0, 'DiagResponse', 0.015)], 'Cem_Lin1Schedule01_CEM_LIN1': [(0, 'CemCem_Lin1Fr01', 0.01), (1, 'RlsmCem_Lin1Fr01', 0.015), (2, 'CemCem_Lin1Fr02', 0.01), (3, 'CemCem_Lin1Fr03', 0.015), (4, 'CemCem_Lin1Fr04', 0.01), (5, 'CemCem_Lin1Fr05', 0.01), (6, 'WmmCem_Lin1Fr01', 0.01), (7, 'CemCem_Lin1Fr06', 0.005), (8, 'CemCem_Lin1Fr01', 0.01), (9, 'RlsmCem_Lin1Fr01', 0.015), (10, 'IrmmCem_Lin1Fr01', 0.01), (11, 'RlsmCem_Lin1Fr02', 0.015), (12, 'RlsmCem_Lin1Fr03', 0.015), (13, 'WmmCem_Lin1Fr01', 0.01), (14, 'CemCem_Lin1Fr06', 0.005)], 'Cem_Lin1ScheduleSerNrPartNrTable_CEM_LIN1': [(0, 'IrmmCem_Lin1SerNrFr01', 0.01), (1, 'IrmmCem_Lin1PartNrFr02', 0.015), (2, 'IrmmCem_Lin1PartNrFr01', 0.01), (3, 'RlsmCem_Lin1PartNrFr01', 0.01), (4, 'RlsmCem_Lin1PartNrFr02', 0.015), (5, 'RlsmCem_SerNrLin1Fr01', 0.01), (6, 'WmmCem_Lin1PartNrFr01', 0.01), (7, 'WmmCem_Lin1PartNrFr02', 0.015), (8, 'WmmCem_Lin1SerNrFr01', 0.01)], 'Cem_Lin1_DiagRequestSchedule01': [(0, 'DiagRequest', 0.015)]}


class RlsmCem_Lin1Fr03:
    msg_name = "RlsmCem_Lin1Fr03"
    msg_id = 2
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLSM"
    rx_nodes = ['BGM']
    sig_group_dict = {'RainSnsrDiagc': ['RainSnsrDiagcRainSnsrHiTDetd', 'RainSnsrDiagcRainSnsrHiVoltDetd']}
    sig_group_dataid_dict = {}

    class SolarSnsrRiValue:
        sig_name = "SolarSnsrRiValue"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 51
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 24
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SolarSnsrLeValue:
        sig_name = "SolarSnsrLeValue"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 5
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 51
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 16
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SolarSnsrErr:
        sig_name = "SolarSnsrErr"
        sig_start_bit = 0
        update_id_bit = None
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
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class RainDetected:
        sig_name = "RainDetected"
        sig_start_bit = 7
        update_id_bit = None
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RainfallAmnt:
        sig_name = "RainfallAmnt"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 14
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AmntSnsr_Amnt': 0, 'AmntSnsr_InitValue': 14, 'AmntSnsr_Error': 15}
        compute_method = None
        length = 4
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RainSnsrDiagcRainSnsrHiTDetd:
        sig_name = "RainSnsrDiagcRainSnsrHiTDetd"
        sig_start_bit = 4
        update_id_bit = None
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RainSnsrDiagcRainSnsrHiVoltDetd:
        sig_name = "RainSnsrDiagcRainSnsrHiVoltDetd"
        sig_start_bit = 3
        update_id_bit = None
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class LiOprnMod:
        sig_name = "LiOprnMod"
        sig_start_bit = 5
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LiOperMod_Night': 0, 'LiOperMod_Day': 1, 'LiOperMod_Twli': 2, 'LiOperMod_Tnl': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5


class CemCem_Lin1Fr01:
    msg_name = "CemCem_Lin1Fr01"
    msg_id = 5
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 6
    tx_node = "BGM"
    rx_nodes = ['RLSM', 'WMM', 'IRMM']
    sig_group_dict = {'IntrMirrCmd': ['IntrMirrCmdDrvrSide', 'IntrMirrCmdIntrMirrAsyFanCmpMag', 'IntrMirrCmdIntrMirrDiagcRst', 'IntrMirrCmdIntrMirrDimSnvty', 'IntrMirrCmdIntrMirrEna', 'IntrMirrCmdIntrMirrInhbDim', 'IntrMirrCmdIntrMirrWindHeatrCmpMag'], 'WipgPwrActvnSafe': ['WipgPwrActvnSafeWipgPwrAcsyModSafe', 'WipgPwrActvnSafeWipgPwrDrvgModSafe'], 'WiprMotFrntLvrCmdSafe': ['WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe', 'WiprMotFrntLvrCmdSafeLvrInIntlPosn', 'WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe', 'WiprMotFrntLvrCmdSafeLvrInSnglStrokePos']}
    sig_group_dataid_dict = {}

    class RainSensActvn:
        sig_name = "RainSensActvn"
        sig_start_bit = 12
        update_id_bit = None
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
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class IntrMirrCmdIntrMirrAsyFanCmpMag:
        sig_name = "IntrMirrCmdIntrMirrAsyFanCmpMag"
        sig_start_bit = 39
        update_id_bit = None
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WipgPwrActvnSafeWipgPwrDrvgModSafe:
        sig_name = "WipgPwrActvnSafeWipgPwrDrvgModSafe"
        sig_start_bit = 10
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 10
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WipgPwrActvnSafeWipgPwrAcsyModSafe:
        sig_name = "WipgPwrActvnSafeWipgPwrAcsyModSafe"
        sig_start_bit = 8
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 8
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WiprPosnForSrvReq:
        sig_name = "WiprPosnForSrvReq"
        sig_start_bit = 27
        update_id_bit = None
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
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class WiprMotFrntOffsAg:
        sig_name = "WiprMotFrntOffsAg"
        sig_start_bit = 40
        update_id_bit = None
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

    class VehSpdForWipg:
        sig_name = "VehSpdForWipg"
        sig_start_bit = 0
        update_id_bit = None
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

    class WiprMotIntlCmd:
        sig_name = "WiprMotIntlCmd"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 6
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgSpdIntlFromHmi_Posn0': 0, 'WipgSpdIntlFromHmi_Posn1': 1, 'WipgSpdIntlFromHmi_Posn2': 2, 'WipgSpdIntlFromHmi_Posn3': 3, 'WipgSpdIntlFromHmi_Posn4': 4, 'WipgSpdIntlFromHmi_Posn5': 5, 'WipgSpdIntlFromHmi_Posn6': 6, 'WipgSpdIntlFromHmi_Posn7': 7}
        compute_method = None
        length = 3
        startbit = 24
        byte = 3
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe:
        sig_name = "WiprMotFrntLvrCmdSafeLvrInHiSpdPosnSafe"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IntrMirrCmdIntrMirrWindHeatrCmpMag:
        sig_name = "IntrMirrCmdIntrMirrWindHeatrCmpMag"
        sig_start_bit = 35
        update_id_bit = None
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
        startbit = 35
        byte = 4
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HomeLinkEna:
        sig_name = "HomeLinkEna"
        sig_start_bit = 22
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IdleEnaDis_Idle': 0, 'IdleEnaDis_Ena': 1, 'IdleEnaDis_Dis': 2}
        compute_method = None
        length = 2
        startbit = 22
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class IntrMirrCmdIntrMirrEna:
        sig_name = "IntrMirrCmdIntrMirrEna"
        sig_start_bit = 36
        update_id_bit = None
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
        startbit = 36
        byte = 4
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WshrLvrPosnSafe:
        sig_name = "WshrLvrPosnSafe"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class IntrMirrCmdDrvrSide:
        sig_name = "IntrMirrCmdDrvrSide"
        sig_start_bit = 34
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'RiLeTyp_Right': 0, 'RiLeTyp_Left': 1}
        compute_method = None
        length = 1
        startbit = 34
        byte = 4
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class WiprMotFrntLvrCmdSafeLvrInIntlPosn:
        sig_name = "WiprMotFrntLvrCmdSafeLvrInIntlPosn"
        sig_start_bit = 21
        update_id_bit = None
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
        startbit = 21
        byte = 2
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class IntrMirrCmdIntrMirrInhbDim:
        sig_name = "IntrMirrCmdIntrMirrInhbDim"
        sig_start_bit = 37
        update_id_bit = None
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class WiprMotFrntLvrCmdSafeLvrInSnglStrokePos:
        sig_name = "WiprMotFrntLvrCmdSafeLvrInSnglStrokePos"
        sig_start_bit = 20
        update_id_bit = None
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class IntrMirrCmdIntrMirrDimSnvty:
        sig_name = "IntrMirrCmdIntrMirrDimSnvty"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'IntrMirrDimSnvtyTyp_Normal': 0, 'IntrMirrDimSnvtyTyp_Dark': 1, 'IntrMirrDimSnvtyTyp_Light': 2, 'IntrMirrDimSnvtyTyp_Inhibit': 3}
        compute_method = None
        length = 2
        startbit = 32
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class IntrMirrCmdIntrMirrDiagcRst:
        sig_name = "IntrMirrCmdIntrMirrDiagcRst"
        sig_start_bit = 38
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe:
        sig_name = "WiprMotFrntLvrCmdSafeLvrInLoSpdPosnSafe"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class WmmCem_Lin1SerNrFr01:
    msg_name = "WmmCem_Lin1SerNrFr01"
    msg_id = 40
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "WMM"
    rx_nodes = ['BGM']
    sig_group_dict = {'WMMSerNo': ['WMMSerNoNr1', 'WMMSerNoNr2', 'WMMSerNoNr3', 'WMMSerNoNr4']}
    sig_group_dataid_dict = {}

    class WMMSerNoNr1:
        sig_name = "WMMSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
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

    class WMMSerNoNr2:
        sig_name = "WMMSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
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

    class WMMSerNoNr4:
        sig_name = "WMMSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
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

    class WMMSerNoNr3:
        sig_name = "WMMSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
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


class RlsmCem_SerNrLin1Fr01:
    msg_name = "RlsmCem_SerNrLin1Fr01"
    msg_id = 34
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "RLSM"
    rx_nodes = ['BGM']
    sig_group_dict = {'RLSMSerNo': ['RLSMSerNoNr1', 'RLSMSerNoNr2', 'RLSMSerNoNr3', 'RLSMSerNoNr4']}
    sig_group_dataid_dict = {}

    class RLSMSerNoNr2:
        sig_name = "RLSMSerNoNr2"
        sig_start_bit = 8
        update_id_bit = None
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

    class RLSMSerNoNr3:
        sig_name = "RLSMSerNoNr3"
        sig_start_bit = 16
        update_id_bit = None
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

    class RLSMSerNoNr1:
        sig_name = "RLSMSerNoNr1"
        sig_start_bit = 0
        update_id_bit = None
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

    class RLSMSerNoNr4:
        sig_name = "RLSMSerNoNr4"
        sig_start_bit = 24
        update_id_bit = None
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


class RlsmCem_Lin1Fr01:
    msg_name = "RlsmCem_Lin1Fr01"
    msg_id = 21
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLSM"
    rx_nodes = ['WMM', 'BGM']
    sig_group_dict = {'RainSnsrErr': ['RainSnsrErrCalErr', 'RainSnsrErrCalErrActv', 'RainSnsrErrRainDetnErr', 'RainSnsrErrRainDetnErrActv'], 'TwliBriRaw': ['TwliBriRawQf', 'TwliBriRawTwliBriRaw'], 'HudSnsrErr': ['HudSnsrErrParChk', 'HudSnsrErrSnsrErr'], 'OutdBri': ['OutdBriChks', 'OutdBriCntr', 'OutdBriSts']}
    sig_group_dataid_dict = {'OutdBri': 8002}

    class WipgAutFrntMod:
        sig_name = "WipgAutFrntMod"
        sig_start_bit = 12
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgAutFrntMod_Off': 0, 'WipgAutFrntMod_ImdtMod': 1, 'WipgAutFrntMod_IntlMod': 2, 'WipgAutFrntMod_ContnsMod': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class RainLi:
        sig_name = "RainLi"
        sig_start_bit = 7
        update_id_bit = None
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class RainSnsrErrCalErr:
        sig_name = "RainSnsrErrCalErr"
        sig_start_bit = 9
        update_id_bit = None
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
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class RainSnsrErrRainDetnErrActv:
        sig_name = "RainSnsrErrRainDetnErrActv"
        sig_start_bit = 11
        update_id_bit = None
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
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class TwliBriRawTwliBriRaw:
        sig_name = "TwliBriRawTwliBriRaw"
        sig_start_bit = 26
        update_id_bit = None
        sig_length = 14
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 26
        bmuws_info = [(3, 0b11111100, 0b00000011, 6, 2), (4, 0b11111111, 0b00000000, 8, 0)]

    class TwliBriRawQf:
        sig_name = "TwliBriRawQf"
        sig_start_bit = 24
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GenQf1_UndefindDataAccur': 0, 'GenQf1_TmpUndefdData': 1, 'GenQf1_DataAccurNotWithinSpcn': 2, 'GenQf1_AccurData': 3}
        compute_method = None
        length = 2
        startbit = 24
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class OutdBriChks:
        sig_name = "OutdBriChks"
        sig_start_bit = 48
        update_id_bit = None
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

    class OutdBriCntr:
        sig_name = "OutdBriCntr"
        sig_start_bit = 58
        update_id_bit = None
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
        startbit = 58
        byte = 7
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class RainSnsrErrRainDetnErr:
        sig_name = "RainSnsrErrRainDetnErr"
        sig_start_bit = 10
        update_id_bit = None
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
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class OutdBriSts:
        sig_name = "OutdBriSts"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OutdBriSts_Ukwn': 0, 'OutdBriSts_Night': 1, 'OutdBriSts_Day': 2, 'OutdBriSts_Invld': 3}
        compute_method = None
        length = 2
        startbit = 56
        byte = 7
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class HudSnsrErrParChk:
        sig_name = "HudSnsrErrParChk"
        sig_start_bit = 3
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ParChks1_Unevennrof1': 0, 'ParChks1_Evennrof1': 1}
        compute_method = None
        length = 1
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class RainSnsrErrCalErrActv:
        sig_name = "RainSnsrErrCalErrActv"
        sig_start_bit = 8
        update_id_bit = None
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
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class AutWinWipgCmd:
        sig_name = "AutWinWipgCmd"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'WipgSpd2_WipgSpd0Rpm': 0, 'WipgSpd2_WipgSpd40Rpm': 1, 'WipgSpd2_WipgSpd43Rpm': 2, 'WipgSpd2_WipgSpd46Rpm': 3, 'WipgSpd2_WipgSpd50Rpm': 4, 'WipgSpd2_WipgSpd54Rpm': 5, 'WipgSpd2_WipgSpd57Rpm': 6, 'WipgSpd2_WipgSpd60Rpm': 7}
        compute_method = None
        length = 3
        startbit = 0
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class HudSnsrErrSnsrErr:
        sig_name = "HudSnsrErrSnsrErr"
        sig_start_bit = 4
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FltStsSlaveBasc_FltStsTestPassd': 0, 'FltStsSlaveBasc_FltStsTestFaild': 1}
        compute_method = None
        length = 1
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4


class IrmmCem_Lin1Fr01:
    msg_name = "IrmmCem_Lin1Fr01"
    msg_id = 16
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "IRMM"
    rx_nodes = ['BGM']
    sig_group_dict = {'IntrMirrResp': ['IntrMirrRespIntrMirrDimPerc', 'IntrMirrRespIntrMirrIntFailr', 'IntrMirrRespResdBoolean', 'IntrMirrRespResdUInt6']}
    sig_group_dataid_dict = {}

    class IntrMirrRespResdUInt6:
        sig_name = "IntrMirrRespResdUInt6"
        sig_start_bit = 8
        update_id_bit = None
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
        startbit = 8
        byte = 1
        mask = 0b00111111
        unmask = 0b11000000
        shift = 0

    class IntrMirrRespIntrMirrIntFailr:
        sig_name = "IntrMirrRespIntrMirrIntFailr"
        sig_start_bit = 14
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'FailrNoFailr1_NoFailr': 0, 'FailrNoFailr1_Failr': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class IntrMirrRespIntrMirrDimPerc:
        sig_name = "IntrMirrRespIntrMirrDimPerc"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.39215686274509803
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 0
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IntrMirrRespResdBoolean:
        sig_name = "IntrMirrRespResdBoolean"
        sig_start_bit = 15
        update_id_bit = None
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


class CemCem_Lin1Fr02:
    msg_name = "CemCem_Lin1Fr02"
    msg_id = 7
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['RLSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class AmbTForVisy:
        sig_name = "AmbTForVisy"
        sig_start_bit = 0
        update_id_bit = None
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


class CemCem_Lin1Fr04:
    msg_name = "CemCem_Lin1Fr04"
    msg_id = 9
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['RLSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class RainSnsrLiThd:
        sig_name = "RainSnsrLiThd"
        sig_start_bit = 44
        update_id_bit = None
        sig_length = 4
        sig_value_factor = 5
        sig_value_offset = -40
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Intel"
        sig_value_init = 8
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 4
        startbit = 44
        byte = 5
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class RlsmCem_Lin1PartNrFr02:
    msg_name = "RlsmCem_Lin1PartNrFr02"
    msg_id = 24
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLSM"
    rx_nodes = ['BGM']
    sig_group_dict = {'RLSMPartNo10': ['RLSMPartNo10EndSgn1', 'RLSMPartNo10EndSgn2', 'RLSMPartNo10EndSgn3', 'RLSMPartNo10Nr1', 'RLSMPartNo10Nr2', 'RLSMPartNo10Nr3', 'RLSMPartNo10Nr4', 'RLSMPartNo10Nr5']}
    sig_group_dataid_dict = {}

    class RLSMPartNo10EndSgn3:
        sig_name = "RLSMPartNo10EndSgn3"
        sig_start_bit = 56
        update_id_bit = None
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

    class RLSMPartNo10Nr4:
        sig_name = "RLSMPartNo10Nr4"
        sig_start_bit = 24
        update_id_bit = None
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

    class RLSMPartNo10Nr5:
        sig_name = "RLSMPartNo10Nr5"
        sig_start_bit = 32
        update_id_bit = None
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

    class RLSMPartNo10EndSgn2:
        sig_name = "RLSMPartNo10EndSgn2"
        sig_start_bit = 48
        update_id_bit = None
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

    class RLSMPartNo10Nr1:
        sig_name = "RLSMPartNo10Nr1"
        sig_start_bit = 0
        update_id_bit = None
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

    class RLSMPartNo10Nr2:
        sig_name = "RLSMPartNo10Nr2"
        sig_start_bit = 8
        update_id_bit = None
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

    class RLSMPartNo10Nr3:
        sig_name = "RLSMPartNo10Nr3"
        sig_start_bit = 16
        update_id_bit = None
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

    class RLSMPartNo10EndSgn1:
        sig_name = "RLSMPartNo10EndSgn1"
        sig_start_bit = 40
        update_id_bit = None
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


class CemCem_Lin1Fr03:
    msg_name = "CemCem_Lin1Fr03"
    msg_id = 23
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['RLSM', 'IRMM']
    sig_group_dict = {'RainSnsrSnvtyForUsrSnvty': ['RainSnsrSnvtyForUsrSnvty0', 'RainSnsrSnvtyForUsrSnvty1', 'RainSnsrSnvtyForUsrSnvty2', 'RainSnsrSnvtyForUsrSnvty3', 'RainSnsrSnvtyForUsrSnvty4', 'RainSnsrSnvtyForUsrSnvty5', 'RainSnsrSnvtyForUsrSnvty6'], 'WindCorrnVal': ['WindCorrnValAmb', 'WindCorrnValFrnt', 'WindCorrnValHud']}
    sig_group_dataid_dict = {}

    class WindCorrnValHud:
        sig_name = "WindCorrnValHud"
        sig_start_bit = 48
        update_id_bit = None
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

    class ReAdaptReq:
        sig_name = "ReAdaptReq"
        sig_start_bit = 60
        update_id_bit = None
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

    class RainSnsrSnvtyForUsrSnvty5:
        sig_name = "RainSnsrSnvtyForUsrSnvty5"
        sig_start_bit = 20
        update_id_bit = None
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
        startbit = 20
        byte = 2
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrqCfg:
        sig_name = "FrqCfg"
        sig_start_bit = 56
        update_id_bit = None
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

    class WindCorrnValAmb:
        sig_name = "WindCorrnValAmb"
        sig_start_bit = 32
        update_id_bit = None
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

    class RainSnsrSnvtyForUsrSnvty4:
        sig_name = "RainSnsrSnvtyForUsrSnvty4"
        sig_start_bit = 16
        update_id_bit = None
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
        startbit = 16
        byte = 2
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class WindCorrnValFrnt:
        sig_name = "WindCorrnValFrnt"
        sig_start_bit = 40
        update_id_bit = None
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

    class RainSnsrSnvtyForUsrSnvty2:
        sig_name = "RainSnsrSnvtyForUsrSnvty2"
        sig_start_bit = 8
        update_id_bit = None
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
        startbit = 8
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RainSnsrSnvtyForUsrSnvty0:
        sig_name = "RainSnsrSnvtyForUsrSnvty0"
        sig_start_bit = 0
        update_id_bit = None
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
        startbit = 0
        byte = 0
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class VehTyp:
        sig_name = "VehTyp"
        sig_start_bit = 28
        update_id_bit = None
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
        startbit = 28
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RainSnsrSnvtyForUsrSnvty3:
        sig_name = "RainSnsrSnvtyForUsrSnvty3"
        sig_start_bit = 12
        update_id_bit = None
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
        startbit = 12
        byte = 1
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class RainSnsrSnvtyForUsrSnvty6:
        sig_name = "RainSnsrSnvtyForUsrSnvty6"
        sig_start_bit = 24
        update_id_bit = None
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
        startbit = 24
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class RainSnsrSnvtyForUsrSnvty1:
        sig_name = "RainSnsrSnvtyForUsrSnvty1"
        sig_start_bit = 4
        update_id_bit = None
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
        startbit = 4
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4


class IrmmCem_Lin1PartNrFr01:
    msg_name = "IrmmCem_Lin1PartNrFr01"
    msg_id = 18
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "IRMM"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNoIRMM': ['PartNoIRMMEndSgn1', 'PartNoIRMMEndSgn2', 'PartNoIRMMEndSgn3', 'PartNoIRMMNr1', 'PartNoIRMMNr2', 'PartNoIRMMNr3', 'PartNoIRMMNr4']}
    sig_group_dataid_dict = {}

    class PartNoIRMMEndSgn2:
        sig_name = "PartNoIRMMEndSgn2"
        sig_start_bit = 40
        update_id_bit = None
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

    class PartNoIRMMNr4:
        sig_name = "PartNoIRMMNr4"
        sig_start_bit = 24
        update_id_bit = None
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

    class PartNoIRMMNr1:
        sig_name = "PartNoIRMMNr1"
        sig_start_bit = 0
        update_id_bit = None
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

    class PartNoIRMMEndSgn1:
        sig_name = "PartNoIRMMEndSgn1"
        sig_start_bit = 32
        update_id_bit = None
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

    class PartNoIRMMNr2:
        sig_name = "PartNoIRMMNr2"
        sig_start_bit = 8
        update_id_bit = None
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

    class PartNoIRMMNr3:
        sig_name = "PartNoIRMMNr3"
        sig_start_bit = 16
        update_id_bit = None
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

    class PartNoIRMMEndSgn3:
        sig_name = "PartNoIRMMEndSgn3"
        sig_start_bit = 48
        update_id_bit = None
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


class DiagRequest:
    msg_name = "DiagRequest"
    msg_id = 60
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = []
    sig_group_dict = {}
    sig_group_dataid_dict = {}


class IrmmCem_Lin1SerNrFr01:
    msg_name = "IrmmCem_Lin1SerNrFr01"
    msg_id = 20
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "IRMM"
    rx_nodes = ['BGM']
    sig_group_dict = {'SerNoIRMM': ['SerNoIRMMNr1', 'SerNoIRMMNr2', 'SerNoIRMMNr3', 'SerNoIRMMNr4']}
    sig_group_dataid_dict = {}

    class SerNoIRMMNr2:
        sig_name = "SerNoIRMMNr2"
        sig_start_bit = 8
        update_id_bit = None
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

    class SerNoIRMMNr3:
        sig_name = "SerNoIRMMNr3"
        sig_start_bit = 16
        update_id_bit = None
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

    class SerNoIRMMNr4:
        sig_name = "SerNoIRMMNr4"
        sig_start_bit = 24
        update_id_bit = None
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

    class SerNoIRMMNr1:
        sig_name = "SerNoIRMMNr1"
        sig_start_bit = 0
        update_id_bit = None
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


class CemCem_Lin1Fr05:
    msg_name = "CemCem_Lin1Fr05"
    msg_id = 10
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "BGM"
    rx_nodes = ['RLSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class EnaOfflineMonitor:
        sig_name = "EnaOfflineMonitor"
        sig_start_bit = 17
        update_id_bit = None
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Boolean_FALSE': 0, 'Boolean_TRUE': 1}
        compute_method = None
        length = 1
        startbit = 17
        byte = 2
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class CemCem_Lin1Fr06:
    msg_name = "CemCem_Lin1Fr06"
    msg_id = 39
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 1
    tx_node = "BGM"
    rx_nodes = ['RLSM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}

    class WiprInPrkgPosnLo:
        sig_name = "WiprInPrkgPosnLo"
        sig_start_bit = 5
        update_id_bit = None
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class WiprActv:
        sig_name = "WiprActv"
        sig_start_bit = 4
        update_id_bit = None
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WshngCycActv:
        sig_name = "WshngCycActv"
        sig_start_bit = 7
        update_id_bit = None
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WiprInWipgAr:
        sig_name = "WiprInWipgAr"
        sig_start_bit = 6
        update_id_bit = None
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
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class WmmCem_Lin1PartNrFr01:
    msg_name = "WmmCem_Lin1PartNrFr01"
    msg_id = 8
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "WMM"
    rx_nodes = ['BGM']
    sig_group_dict = {'WMMPartNo': ['WMMPartNoEndSgn1', 'WMMPartNoEndSgn2', 'WMMPartNoEndSgn3', 'WMMPartNoNr1', 'WMMPartNoNr2', 'WMMPartNoNr3', 'WMMPartNoNr4']}
    sig_group_dataid_dict = {}

    class WMMPartNoNr2:
        sig_name = "WMMPartNoNr2"
        sig_start_bit = 8
        update_id_bit = None
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

    class WMMPartNoEndSgn2:
        sig_name = "WMMPartNoEndSgn2"
        sig_start_bit = 40
        update_id_bit = None
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

    class WMMPartNoEndSgn3:
        sig_name = "WMMPartNoEndSgn3"
        sig_start_bit = 48
        update_id_bit = None
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

    class WMMPartNoNr3:
        sig_name = "WMMPartNoNr3"
        sig_start_bit = 16
        update_id_bit = None
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

    class WMMPartNoNr1:
        sig_name = "WMMPartNoNr1"
        sig_start_bit = 0
        update_id_bit = None
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

    class WMMPartNoNr4:
        sig_name = "WMMPartNoNr4"
        sig_start_bit = 24
        update_id_bit = None
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

    class WMMPartNoEndSgn1:
        sig_name = "WMMPartNoEndSgn1"
        sig_start_bit = 32
        update_id_bit = None
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


class IrmmCem_Lin1PartNrFr02:
    msg_name = "IrmmCem_Lin1PartNrFr02"
    msg_id = 22
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "IRMM"
    rx_nodes = ['BGM']
    sig_group_dict = {'PartNo10IRMM': ['PartNo10IRMMEndSgn1', 'PartNo10IRMMEndSgn2', 'PartNo10IRMMEndSgn3', 'PartNo10IRMMNr1', 'PartNo10IRMMNr2', 'PartNo10IRMMNr3', 'PartNo10IRMMNr4', 'PartNo10IRMMNr5']}
    sig_group_dataid_dict = {}

    class PartNo10IRMMEndSgn3:
        sig_name = "PartNo10IRMMEndSgn3"
        sig_start_bit = 56
        update_id_bit = None
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

    class PartNo10IRMMNr5:
        sig_name = "PartNo10IRMMNr5"
        sig_start_bit = 32
        update_id_bit = None
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

    class PartNo10IRMMNr1:
        sig_name = "PartNo10IRMMNr1"
        sig_start_bit = 0
        update_id_bit = None
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

    class PartNo10IRMMNr3:
        sig_name = "PartNo10IRMMNr3"
        sig_start_bit = 16
        update_id_bit = None
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

    class PartNo10IRMMNr4:
        sig_name = "PartNo10IRMMNr4"
        sig_start_bit = 24
        update_id_bit = None
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

    class PartNo10IRMMNr2:
        sig_name = "PartNo10IRMMNr2"
        sig_start_bit = 8
        update_id_bit = None
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

    class PartNo10IRMMEndSgn1:
        sig_name = "PartNo10IRMMEndSgn1"
        sig_start_bit = 40
        update_id_bit = None
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

    class PartNo10IRMMEndSgn2:
        sig_name = "PartNo10IRMMEndSgn2"
        sig_start_bit = 48
        update_id_bit = None
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


class RlsmCem_Lin1PartNrFr01:
    msg_name = "RlsmCem_Lin1PartNrFr01"
    msg_id = 32
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 7
    tx_node = "RLSM"
    rx_nodes = ['BGM']
    sig_group_dict = {'RLSMPartNo': ['RLSMPartNoEndSgn1', 'RLSMPartNoEndSgn2', 'RLSMPartNoEndSgn3', 'RLSMPartNoNr1', 'RLSMPartNoNr2', 'RLSMPartNoNr3', 'RLSMPartNoNr4']}
    sig_group_dataid_dict = {}

    class RLSMPartNoEndSgn3:
        sig_name = "RLSMPartNoEndSgn3"
        sig_start_bit = 48
        update_id_bit = None
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

    class RLSMPartNoNr2:
        sig_name = "RLSMPartNoNr2"
        sig_start_bit = 8
        update_id_bit = None
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

    class RLSMPartNoEndSgn2:
        sig_name = "RLSMPartNoEndSgn2"
        sig_start_bit = 40
        update_id_bit = None
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

    class RLSMPartNoNr4:
        sig_name = "RLSMPartNoNr4"
        sig_start_bit = 24
        update_id_bit = None
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

    class RLSMPartNoEndSgn1:
        sig_name = "RLSMPartNoEndSgn1"
        sig_start_bit = 32
        update_id_bit = None
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

    class RLSMPartNoNr1:
        sig_name = "RLSMPartNoNr1"
        sig_start_bit = 0
        update_id_bit = None
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

    class RLSMPartNoNr3:
        sig_name = "RLSMPartNoNr3"
        sig_start_bit = 16
        update_id_bit = None
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


class WmmCem_Lin1PartNrFr02:
    msg_name = "WmmCem_Lin1PartNrFr02"
    msg_id = 25
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "WMM"
    rx_nodes = ['BGM']
    sig_group_dict = {'WMMPartNo10': ['WMMPartNo10EndSgn1', 'WMMPartNo10EndSgn2', 'WMMPartNo10EndSgn3', 'WMMPartNo10Nr1', 'WMMPartNo10Nr2', 'WMMPartNo10Nr3', 'WMMPartNo10Nr4', 'WMMPartNo10Nr5']}
    sig_group_dataid_dict = {}

    class WMMPartNo10Nr3:
        sig_name = "WMMPartNo10Nr3"
        sig_start_bit = 16
        update_id_bit = None
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

    class WMMPartNo10Nr5:
        sig_name = "WMMPartNo10Nr5"
        sig_start_bit = 32
        update_id_bit = None
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

    class WMMPartNo10EndSgn2:
        sig_name = "WMMPartNo10EndSgn2"
        sig_start_bit = 48
        update_id_bit = None
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

    class WMMPartNo10EndSgn3:
        sig_name = "WMMPartNo10EndSgn3"
        sig_start_bit = 56
        update_id_bit = None
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

    class WMMPartNo10Nr2:
        sig_name = "WMMPartNo10Nr2"
        sig_start_bit = 8
        update_id_bit = None
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

    class WMMPartNo10EndSgn1:
        sig_name = "WMMPartNo10EndSgn1"
        sig_start_bit = 40
        update_id_bit = None
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

    class WMMPartNo10Nr4:
        sig_name = "WMMPartNo10Nr4"
        sig_start_bit = 24
        update_id_bit = None
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

    class WMMPartNo10Nr1:
        sig_name = "WMMPartNo10Nr1"
        sig_start_bit = 0
        update_id_bit = None
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


class WmmCem_Lin1Fr01:
    msg_name = "WmmCem_Lin1Fr01"
    msg_id = 37
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 4
    tx_node = "WMM"
    rx_nodes = ['BGM']
    sig_group_dict = {'WiprMotDiagc': ['WiprMotDiagcWiprMotHiVoltDetd', 'WiprMotDiagcWiprMotLoVoltDetd', 'WiprMotDiagcWiprMotOvldDetd']}
    sig_group_dataid_dict = {}

    class WiprInWipgArFromWMM:
        sig_name = "WiprInWipgArFromWMM"
        sig_start_bit = 11
        update_id_bit = None
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
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class WiprMotDiagcWiprMotOvldDetd:
        sig_name = "WiprMotDiagcWiprMotOvldDetd"
        sig_start_bit = 20
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 20
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WiprMotErrSafe:
        sig_name = "WiprMotErrSafe"
        sig_start_bit = 13
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 13
        byte = 1
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class WiprMotDiagcWiprMotHiVoltDetd:
        sig_name = "WiprMotDiagcWiprMotHiVoltDetd"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 16
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class WiprActvFromWMM:
        sig_name = "WiprActvFromWMM"
        sig_start_bit = 8
        update_id_bit = None
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
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class WiprMotDiagcWiprMotLoVoltDetd:
        sig_name = "WiprMotDiagcWiprMotLoVoltDetd"
        sig_start_bit = 18
        update_id_bit = None
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Intel"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffCrit1_NotVld1': 0, 'OnOffCrit1_Off': 1, 'OnOffCrit1_On': 2, 'OnOffCrit1_NotVld2': 3}
        compute_method = None
        length = 2
        startbit = 18
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WshngCycActvFromWMM:
        sig_name = "WshngCycActvFromWMM"
        sig_start_bit = 22
        update_id_bit = None
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class WiprInPrkgPosnLoFromWMM:
        sig_name = "WiprInPrkgPosnLoFromWMM"
        sig_start_bit = 10
        update_id_bit = None
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
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class WiprMotCrkAg:
        sig_name = "WiprMotCrkAg"
        sig_start_bit = 24
        update_id_bit = None
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


class RlsmCem_Lin1Fr02:
    msg_name = "RlsmCem_Lin1Fr02"
    msg_id = 44
    msg_tx_method = "cyclic"
    msg_cycle = 0.039
    msg_length = 8
    tx_node = "RLSM"
    rx_nodes = ['BGM']
    sig_group_dict = {'AmbIllmnFwdSts': ['AmbIllmnFwdStsAmblillmn1', 'AmbIllmnFwdStsAmblillmn2', 'AmbIllmnFwdStsChks', 'AmbIllmnFwdStsCntr']}
    sig_group_dataid_dict = {}

    class CmptFrntWindT:
        sig_name = "CmptFrntWindT"
        sig_start_bit = 45
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Intel"
        sig_value_init = 650
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 45
        bmuws_info = [(5, 0b11100000, 0b00011111, 3, 5), (6, 0b11111111, 0b00000000, 8, 0)]

    class AmbIllmnFwdStsCntr:
        sig_name = "AmbIllmnFwdStsCntr"
        sig_start_bit = 11
        update_id_bit = None
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
        startbit = 11
        byte = 1
        mask = 0b01111000
        unmask = 0b10000111
        shift = 3

    class AmbIllmnFwdStsAmblillmn2:
        sig_name = "AmbIllmnFwdStsAmblillmn2"
        sig_start_bit = 16
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 255
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

    class RelHumSnsrRelHum:
        sig_name = "RelHumSnsrRelHum"
        sig_start_bit = 56
        update_id_bit = None
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 200
        sig_byteorder = "Intel"
        sig_value_init = 80
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 56
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AmbIllmnFwdStsAmblillmn1:
        sig_name = "AmbIllmnFwdStsAmblillmn1"
        sig_start_bit = 32
        update_id_bit = None
        sig_length = 9
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Intel"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 32
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b00000001, 0b11111110, 1, 0)]

    class AmbIllmnFwdStsChks:
        sig_name = "AmbIllmnFwdStsChks"
        sig_start_bit = 24
        update_id_bit = None
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

    class RelHumSnsrErr:
        sig_name = "RelHumSnsrErr"
        sig_start_bit = 42
        update_id_bit = None
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
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CmptFrntWindDewT:
        sig_name = "CmptFrntWindDewT"
        sig_start_bit = 0
        update_id_bit = None
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = -40.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Intel"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 0
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b00000111, 0b11111000, 3, 0)]


class DiagResponse:
    msg_name = "DiagResponse"
    msg_id = 61
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = None
    rx_nodes = ['BGM']
    sig_group_dict = {}
    sig_group_dataid_dict = {}


