class PscmChas1Fr03:
    msg_name = "PscmChas1Fr03"
    msg_id = 444
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['ACU', 'VDDM']

    class DrvrSteerWhlHldGroupDrvrSteerWhlHldQly:
        sig_name = "DrvrSteerWhlHldGroupDrvrSteerWhlHldQly"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2

    class DrvrSteerWhlHldGroupDrvrSteerWhlHld:
        sig_name = "DrvrSteerWhlHldGroupDrvrSteerWhlHld"
        sig_start_bit = 7
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OnOffDetd1_NoInfo': 0, 'OnOffDetd1_OffDetd': 1, 'OnOffDetd1_NotOnOrOffDetd': 2, 'OnOffDetd1_OnDetd': 3}
        compute_method = None
        length = 2
        startbit = 7
        byte = 0
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class SteerExtFctStsChks:
        sig_name = "SteerExtFctStsChks"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class SteerExtFctStsExtFctUpperLimActive:
        sig_name = "SteerExtFctStsExtFctUpperLimActive"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class SteerExtFctStsExtFctRateLimActive:
        sig_name = "SteerExtFctStsExtFctRateLimActive"
        sig_start_bit = 54
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
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class SteerExtFctStsDrvrSteerOvrd:
        sig_name = "SteerExtFctStsDrvrSteerOvrd"
        sig_start_bit = 52
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
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class SteerExtFctStsLatAgReqNotInRange:
        sig_name = "SteerExtFctStsLatAgReqNotInRange"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class SteerExtFctStsExtSafeLimActive:
        sig_name = "SteerExtFctStsExtSafeLimActive"
        sig_start_bit = 40
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
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class SteerExtFctStsExtFctLowerLimActive:
        sig_name = "SteerExtFctStsExtFctLowerLimActive"
        sig_start_bit = 53
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
        startbit = 53
        byte = 6
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class SteerExtFctStsLatCtrlReqNotInRange:
        sig_name = "SteerExtFctStsLatCtrlReqNotInRange"
        sig_start_bit = 42
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
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class SteerExtFctStsCntr:
        sig_name = "SteerExtFctStsCntr"
        sig_start_bit = 51
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

    class SteerErrReq:
        sig_name = "SteerErrReq"
        sig_start_bit = 46
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerErrReq3_NoReq': 0, 'SteerErrReq3_SteerAssiSrvRqrd': 1, 'SteerErrReq3_SteerErrStopSfty': 2, 'SteerErrReq3_SteerAssiUrgentSrvRqrd': 3, 'SteerErrReq3_SteerAssiTmpRedn': 4, 'SteerErrReq3_Spare01': 5, 'SteerErrReq3_Spare02': 6, 'SteerErrReq3_Spare03': 7}
        compute_method = None
        length = 3
        startbit = 46
        byte = 5
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class EcmChas1Fr13:
    msg_name = "EcmChas1Fr13"
    msg_id = 871
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class DchaChrgnTarValFb:
        sig_name = "DchaChrgnTarValFb"
        sig_start_bit = 45
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 200
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class HpcHpHeatgPwrSts_0_VDDMBackBoneSignalIPdu20:
        sig_name = "HpcHpHeatgPwrSts_0_VDDMBackBoneSignalIPdu20"
        sig_start_bit = 9
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
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class HpcHpModReq_0_VDDMBackBoneSignalIPdu20:
        sig_name = "HpcHpModReq_0_VDDMBackBoneSignalIPdu20"
        sig_start_bit = 6
        sig_length = 7
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 21
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HeatPmpModCmd_Initialization': 0, 'HeatPmpModCmd_Mode1': 1, 'HeatPmpModCmd_Mode2': 2, 'HeatPmpModCmd_Mode3': 3, 'HeatPmpModCmd_Mode4': 4, 'HeatPmpModCmd_Mode5': 5, 'HeatPmpModCmd_Mode6': 6, 'HeatPmpModCmd_Mode7': 7, 'HeatPmpModCmd_Mode8': 8, 'HeatPmpModCmd_Mode9': 9, 'HeatPmpModCmd_Mode10': 10, 'HeatPmpModCmd_Mode11': 11, 'HeatPmpModCmd_Mode12': 12, 'HeatPmpModCmd_Mode13': 13, 'HeatPmpModCmd_Mode14': 14, 'HeatPmpModCmd_Mode15': 15, 'HeatPmpModCmd_Mode16': 16, 'HeatPmpModCmd_Mode17': 17, 'HeatPmpModCmd_Mode18': 18, 'HeatPmpModCmd_Mode19': 19, 'HeatPmpModCmd_Mode20': 20, 'HeatPmpModCmd_Reserved': 21}
        compute_method = None
        length = 7
        startbit = 6
        byte = 0
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class HpcHpCoolgPwrSts_0_VDDMBackBoneSignalIPdu20:
        sig_name = "HpcHpCoolgPwrSts_0_VDDMBackBoneSignalIPdu20"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HpcSov1OnOffSts:
        sig_name = "HpcSov1OnOffSts"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class HpcDeiceReq_0_VDDMBackBoneSignalIPdu20:
        sig_name = "HpcDeiceReq_0_VDDMBackBoneSignalIPdu20"
        sig_start_bit = 15
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DeiceReq_NoReq': 0, 'DeiceReq_DeiceChecking': 1, 'DeiceReq_Deicing': 2, 'DeiceReq_Reserved': 3}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class BookChrgnTarValFb:
        sig_name = "BookChrgnTarValFb"
        sig_start_bit = 39
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11000000, 0b00111111, 2, 6)]


class EcmChas1Fr16:
    msg_name = "EcmChas1Fr16"
    msg_id = 979
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.26
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class GrlShttrDmdShttrPosnReq_0_EcmChas1SignalIPdu16:
        sig_name = "GrlShttrDmdShttrPosnReq_0_EcmChas1SignalIPdu16"
        sig_start_bit = 39
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

    class HvCooltHeatrEnadWhE2EHvchEnad_0_VDDMBackBoneSignalIPdu24:
        sig_name = "HvCooltHeatrEnadWhE2EHvchEnad_0_VDDMBackBoneSignalIPdu24"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class HpBattVlvPosSetReq_0_EcmChas1SignalIPdu16:
        sig_name = "HpBattVlvPosSetReq_0_EcmChas1SignalIPdu16"
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

    class HpBattFwvPosSetReq_0_EcmChas1SignalIPdu16:
        sig_name = "HpBattFwvPosSetReq_0_EcmChas1SignalIPdu16"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HvCooltHeatrEnadWhE2EChks_0_VDDMBackBoneSignalIPdu24:
        sig_name = "HvCooltHeatrEnadWhE2EChks_0_VDDMBackBoneSignalIPdu24"
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

    class HvCooltHeatrEnadWhE2ECntr_0_VDDMBackBoneSignalIPdu24:
        sig_name = "HvCooltHeatrEnadWhE2ECntr_0_VDDMBackBoneSignalIPdu24"
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

    class GrlShttrDmdShttrCalEna_0_EcmChas1SignalIPdu16:
        sig_name = "GrlShttrDmdShttrCalEna_0_EcmChas1SignalIPdu16"
        sig_start_bit = 24
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrCalEna_ShttrCalNotEnad': 0, 'ShttrCalEna_ShttrCalEnad': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CmprReqCmprSpdReq_0_EcmChas1SignalIPdu16:
        sig_name = "CmprReqCmprSpdReq_0_EcmChas1SignalIPdu16"
        sig_start_bit = 47
        sig_length = 8
        sig_value_factor = 50.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 254
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


class VddmChas1Fr43:
    msg_name = "VddmChas1Fr43"
    msg_id = 1255
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.17
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']

    class HvacAirTForRowSecAtFlrRiEvaprTQf_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowSecAtFlrRiEvaprTQf_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class HvacAirTForRowSecAtVentLeEvaprTQf_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowSecAtVentLeEvaprTQf_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class HvacAirTForRowSecAtVentRiEvaprTFrnt_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowSecAtVentRiEvaprTFrnt_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 52
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
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowSecAtVentRiEvaprTQf_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowSecAtVentRiEvaprTQf_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class HvacAirTForRowSecAtFlrLeEvaprTFrnt_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowSecAtFlrLeEvaprTFrnt_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 4
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
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowSecAtFlrLeEvaprTQf_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowSecAtFlrLeEvaprTQf_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class HvacAirTForRowSecAtFlrRiEvaprTFrnt_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowSecAtFlrRiEvaprTFrnt_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 20
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
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowSecAtVentLeEvaprTFrnt_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowSecAtVentLeEvaprTFrnt_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 36
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
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class EcmChas1Fr38:
    msg_name = "EcmChas1Fr38"
    msg_id = 1157
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class AcCompDischrgT:
        sig_name = "AcCompDischrgT"
        sig_start_bit = 7
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class AcEvapOutT:
        sig_name = "AcEvapOutT"
        sig_start_bit = 37
        sig_length = 9
        sig_value_factor = 0.5
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 120
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 37
        bmuws_info = [(4, 0b00111111, 0b11000000, 6, 0), (5, 0b11100000, 0b00011111, 3, 5)]

    class AcChllrOutT:
        sig_name = "AcChllrOutT"
        sig_start_bit = 9
        sig_length = 9
        sig_value_factor = 0.5
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 120
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 9
        bmuws_info = [(1, 0b00000011, 0b11111100, 2, 0), (2, 0b11111110, 0b00000001, 7, 1)]

    class AcCondOutT:
        sig_name = "AcCondOutT"
        sig_start_bit = 31
        sig_length = 9
        sig_value_factor = 0.5
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 120
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b10000000, 0b01111111, 1, 7)]


class PscmToVddmChas1DiagRespFrame:
    msg_name = "PscmToVddmChas1DiagRespFrame"
    msg_id = 1648
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['VDDM']


class VddmBcmtoETCXCPFr01:
    msg_name = "VddmBcmtoETCXCPFr01"
    msg_id = 1422
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['CCM']


class VddmChas1Fr53:
    msg_name = "VddmChas1Fr53"
    msg_id = 496
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1', 'SAS']

    class StandStillMgrStsForHld1:
        sig_name = "StandStillMgrStsForHld1"
        sig_start_bit = 30
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'StandStillMgrStsForHld1_StandStillMgrStsForHldVal0': 0, 'StandStillMgrStsForHld1_StandStillMgrStsForHldVal1': 1, 'StandStillMgrStsForHld1_StandStillMgrStsForHldVal2': 2, 'StandStillMgrStsForHld1_StandStillMgrStsForHldVal3': 3, 'StandStillMgrStsForHld1_StandStillMgrStsForHldVal4': 4, 'StandStillMgrStsForHld1_StandStillMgrStsForHldVal5': 5, 'StandStillMgrStsForHld1_StandStillMgrStsForHldVal6': 6, 'StandStillMgrStsForHld1_StandStillMgrStsForHldVal7': 7}
        compute_method = None
        length = 3
        startbit = 30
        byte = 3
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class StandStillMgrStsForHldCntr:
        sig_name = "StandStillMgrStsForHldCntr"
        sig_start_bit = 27
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

    class BkpOfDstTrvld_0_DIMBackBoneSignalIPdu04:
        sig_name = "BkpOfDstTrvld_0_DIMBackBoneSignalIPdu04"
        sig_start_bit = 7
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111000, 0b00000111, 5, 3)]

    class StandStillMgrStsForHldChks:
        sig_name = "StandStillMgrStsForHldChks"
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


class Pscm2ChassisCAN1NmFr:
    msg_name = "Pscm2ChassisCAN1NmFr"
    msg_id = 1331
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PSCM2"
    rx_nodes = ['BGM']


class PscmChas1Fr02:
    msg_name = "PscmChas1Fr02"
    msg_id = 70
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['ACU', 'VDDM']

    class SteerWhlTqAddl:
        sig_name = "SteerWhlTqAddl"
        sig_start_bit = 39
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = -7680
        sig_value_max = 7680
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class LatCtrlModCfmdLatCtrlMod:
        sig_name = "LatCtrlModCfmdLatCtrlMod"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LatCtrlMod1_NoReq': 0, 'LatCtrlMod1_HighWayAssist': 1, 'LatCtrlMod1_EmgyLaneKeepAidForObjRe': 2, 'LatCtrlMod1_EmgyLaneKeepAidForStat': 3, 'LatCtrlMod1_SftyLaneKeepAid': 4, 'LatCtrlMod1_SteerAssc': 5, 'LatCtrlMod1_DsrOversteer': 6, 'LatCtrlMod1_DsrMueSplit': 7, 'LatCtrlMod1_DsrTrlrStaby': 8, 'LatCtrlMod1_EmgyManvAssi': 9, 'LatCtrlMod1_Reserved1': 10, 'LatCtrlMod1_Reserved2': 11, 'LatCtrlMod1_SHWA': 12, 'LatCtrlMod1_APA': 13, 'LatCtrlMod1_RPA': 14, 'LatCtrlMod1_HPA': 15}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class LatCtrlModCfmdCntr:
        sig_name = "LatCtrlModCfmdCntr"
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

    class TqAssAddl:
        sig_name = "TqAssAddl"
        sig_start_bit = 53
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = -7680
        sig_value_max = 7680
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 53
        bmuws_info = [(6, 0b00111111, 0b11000000, 6, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class SteerServoSts:
        sig_name = "SteerServoSts"
        sig_start_bit = 40
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerServoSts1_SteerPwrAssidElecFullFct': 0, 'SteerServoSts1_SteerPwrAssidElecCritErr': 1}
        compute_method = None
        length = 1
        startbit = 40
        byte = 5
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class LatCtrlModCfmdChks:
        sig_name = "LatCtrlModCfmdChks"
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


class VddmChas1Fr44:
    msg_name = "VddmChas1Fr44"
    msg_id = 1267
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.17
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1']

    class HvacOsaAndRecActrQfForHp_1_CEMBackBoneSignalIpdu08:
        sig_name = "HvacOsaAndRecActrQfForHp_1_CEMBackBoneSignalIpdu08"
        sig_start_bit = 48
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Err1_NoErr': 0, 'Err1_Err': 1}
        compute_method = None
        length = 1
        startbit = 48
        byte = 6
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class EscStChks:
        sig_name = "EscStChks"
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

    class HvacCondsorTspEvaprTFrnt_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacCondsorTspEvaprTFrnt_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 20
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
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvacCondsorTspEvaprTQf_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacCondsorTspEvaprTQf_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class EscStCntr:
        sig_name = "EscStCntr"
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

    class HvacCondsorTEvaprTFrnt_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacCondsorTEvaprTFrnt_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 4
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
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvacCondsorTEvaprTQf_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacCondsorTEvaprTQf_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class EscStEscSt:
        sig_name = "EscStEscSt"
        sig_start_bit = 38
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EscSt1_Inin': 0, 'EscSt1_Ok': 1, 'EscSt1_TmpErr': 2, 'EscSt1_PrmntErr': 3, 'EscSt1_UsrOff': 4}
        compute_method = None
        length = 3
        startbit = 38
        byte = 4
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class PscmDevelpFr:
    msg_name = "PscmDevelpFr"
    msg_id = 1430
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['CCM']

    class PSCMdevelpsignalgroupresp1Functiondevpsignalgroup6:
        sig_name = "PSCMdevelpsignalgroupresp1Functiondevpsignalgroup6"
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

    class PSCMdevelpsignalgroupresp1Functiondevpsignalgroup2:
        sig_name = "PSCMdevelpsignalgroupresp1Functiondevpsignalgroup2"
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

    class PSCMdevelpsignalgroupresp1Functiondevpsignalgroup3:
        sig_name = "PSCMdevelpsignalgroupresp1Functiondevpsignalgroup3"
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

    class PSCMdevelpsignalgroupresp1Functiondevpsignalgroup5:
        sig_name = "PSCMdevelpsignalgroupresp1Functiondevpsignalgroup5"
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

    class PSCMdevelpsignalgroupresp1Functiondevpsignalgroup8:
        sig_name = "PSCMdevelpsignalgroupresp1Functiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class PSCMdevelpsignalgroupresp1Functiondevpsignalgroup4:
        sig_name = "PSCMdevelpsignalgroupresp1Functiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class PSCMdevelpsignalgroupresp1Functiondevpsignalgroup1:
        sig_name = "PSCMdevelpsignalgroupresp1Functiondevpsignalgroup1"
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

    class PSCMdevelpsignalgroupresp1Functiondevpsignalgroup7:
        sig_name = "PSCMdevelpsignalgroupresp1Functiondevpsignalgroup7"
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


class EcmChas1Fr25:
    msg_name = "EcmChas1Fr25"
    msg_id = 587
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class AirTFromHeatgEstimd_0_VDDMBackBoneSignalIPdu18:
        sig_name = "AirTFromHeatgEstimd_0_VDDMBackBoneSignalIPdu18"
        sig_start_bit = 36
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
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]


class BgmChassisCAN1NmFr:
    msg_name = "BgmChassisCAN1NmFr"
    msg_id = 1281
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['VDDM']


class AsdmChas1Fr03:
    msg_name = "AsdmChas1Fr03"
    msg_id = 51
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['PSCM1']

    class AsyAgCtrlTqLimCntr:
        sig_name = "AsyAgCtrlTqLimCntr"
        sig_start_bit = 12
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
        startbit = 12
        byte = 1
        mask = 0b00011110
        unmask = 0b11100001
        shift = 1

    class AsyPinionAgReqSafeAsyPinionAgReqCntr:
        sig_name = "AsyPinionAgReqSafeAsyPinionAgReqCntr"
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

    class AsyAgCtrlTqLimChks:
        sig_name = "AsyAgCtrlTqLimChks"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class AsyAgCtrlTqLimAgCtrlTqUpperLim:
        sig_name = "AsyAgCtrlTqLimAgCtrlTqUpperLim"
        sig_start_bit = 43
        sig_length = 9
        sig_value_factor = 0.125
        sig_value_offset = "-30"
        sig_value_min = 0
        sig_value_max = 480
        sig_byteorder = "Motorola"
        sig_value_init = 240
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 43
        bmuws_info = [(5, 0b00001111, 0b11110000, 4, 0), (6, 0b11111000, 0b00000111, 5, 3)]

    class AsyPinionAgReqSafeAsyPinionAgReq:
        sig_name = "AsyPinionAgReqSafeAsyPinionAgReq"
        sig_start_bit = 23
        sig_length = 15
        sig_value_factor = 0.0009765625
        sig_value_offset = "-14.5"
        sig_value_min = 0
        sig_value_max = 32767
        sig_byteorder = "Motorola"
        sig_value_init = 14848
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class AsyPinionAgReqSafeAsyPinionAgReqChks:
        sig_name = "AsyPinionAgReqSafeAsyPinionAgReqChks"
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

    class AsyAgCtrlTqLimAgCtrlTqLowrLim:
        sig_name = "AsyAgCtrlTqLimAgCtrlTqLowrLim"
        sig_start_bit = 6
        sig_length = 9
        sig_value_factor = 0.125
        sig_value_offset = "-30"
        sig_value_min = 0
        sig_value_max = 480
        sig_byteorder = "Motorola"
        sig_value_init = 240
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11000000, 0b00111111, 2, 6)]


class VddmChas1Fr42:
    msg_name = "VddmChas1Fr42"
    msg_id = 1243
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.17
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']

    class HvacAirTForRowFirstAtFlrRiEvaprTFrnt_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowFirstAtFlrRiEvaprTFrnt_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 20
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
        startbit = 20
        bmuws_info = [(2, 0b00011111, 0b11100000, 5, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowFirstAtFlrLeEvaprTFrnt_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowFirstAtFlrLeEvaprTFrnt_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 4
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
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowFirstAtVentLeEvaprTFrnt_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowFirstAtVentLeEvaprTFrnt_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 36
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
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowFirstAtVentLeEvaprTQf_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowFirstAtVentLeEvaprTQf_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class HvacAirTForRowFirstAtVentRiEvaprTFrnt_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowFirstAtVentRiEvaprTFrnt_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 52
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
        startbit = 52
        bmuws_info = [(6, 0b00011111, 0b11100000, 5, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class HvacAirTForRowFirstAtFlrLeEvaprTQf_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowFirstAtFlrLeEvaprTQf_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 5
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class HvacAirTForRowFirstAtFlrRiEvaprTQf_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowFirstAtFlrRiEvaprTQf_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 21
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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

    class HvacAirTForRowFirstAtVentRiEvaprTQf_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacAirTForRowFirstAtVentRiEvaprTQf_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 53
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
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


class EcmChas1Fr07:
    msg_name = "EcmChas1Fr07"
    msg_id = 554
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class CmprFbCmprSpd_1_EcmChas1SignalIPdu07:
        sig_name = "CmprFbCmprSpd_1_EcmChas1SignalIPdu07"
        sig_start_bit = 15
        sig_length = 8
        sig_value_factor = 50.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 254
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

    class CmprFbCmprSts2_1_EcmChas1SignalIPdu07:
        sig_name = "CmprFbCmprSts2_1_EcmChas1SignalIPdu07"
        sig_start_bit = 43
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CompStat_NormalOperation': 0, 'CompStat_DegradedOperation': 1, 'CompStat_Inoperative': 2}
        compute_method = None
        length = 4
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CmprFbCmprT2_1_EcmChas1SignalIPdu07:
        sig_name = "CmprFbCmprT2_1_EcmChas1SignalIPdu07"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = "-50.0"
        sig_value_min = 0
        sig_value_max = 254
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

    class CmprFbCmprIPha_1_EcmChas1SignalIPdu07:
        sig_name = "CmprFbCmprIPha_1_EcmChas1SignalIPdu07"
        sig_start_bit = 7
        sig_length = 8
        sig_value_factor = 0.5
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 254
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

    class CmprFbCmprU_1_EcmChas1SignalIPdu07:
        sig_name = "CmprFbCmprU_1_EcmChas1SignalIPdu07"
        sig_start_bit = 55
        sig_length = 10
        sig_value_factor = 2.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11000000, 0b00111111, 2, 6)]

    class CmprFbCmprI_1_EcmChas1SignalIPdu07:
        sig_name = "CmprFbCmprI_1_EcmChas1SignalIPdu07"
        sig_start_bit = 39
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

    class CmprFbCmprT1_1_EcmChas1SignalIPdu07:
        sig_name = "CmprFbCmprT1_1_EcmChas1SignalIPdu07"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = "-50.0"
        sig_value_min = 0
        sig_value_max = 254
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

    class CmprFbCmprSts1_1_EcmChas1SignalIPdu07:
        sig_name = "CmprFbCmprSts1_1_EcmChas1SignalIPdu07"
        sig_start_bit = 61
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmprSts_CmprOff': 0, 'CmprSts_CmprOn': 1, 'CmprSts_CmprPwrLimd': 2, 'CmprSts_CmprPreHeat': 3, 'CmprSts_Reserved1': 4, 'CmprSts_Reserved2': 5, 'CmprSts_Reserved3': 6, 'CmprSts_SigNotAvl': 7}
        compute_method = None
        length = 3
        startbit = 61
        byte = 7
        mask = 0b00111000
        unmask = 0b11000111
        shift = 3


class EtctoVddmDevelFr01:
    msg_name = "EtctoVddmDevelFr01"
    msg_id = 1432
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['VDDM']

    class VDDMdevelpsignalgroupreq1Functiondevpsignalgroup3:
        sig_name = "VDDMdevelpsignalgroupreq1Functiondevpsignalgroup3"
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

    class VDDMdevelpsignalgroupreq1Functiondevpsignalgroup2:
        sig_name = "VDDMdevelpsignalgroupreq1Functiondevpsignalgroup2"
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

    class VDDMdevelpsignalgroupreq1Functiondevpsignalgroup4:
        sig_name = "VDDMdevelpsignalgroupreq1Functiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class VDDMdevelpsignalgroupreq1Functiondevpsignalgroup5:
        sig_name = "VDDMdevelpsignalgroupreq1Functiondevpsignalgroup5"
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

    class VDDMdevelpsignalgroupreq1Functiondevpsignalgroup8:
        sig_name = "VDDMdevelpsignalgroupreq1Functiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class VDDMdevelpsignalgroupreq1Functiondevpsignalgroup6:
        sig_name = "VDDMdevelpsignalgroupreq1Functiondevpsignalgroup6"
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

    class VDDMdevelpsignalgroupreq1Functiondevpsignalgroup7:
        sig_name = "VDDMdevelpsignalgroupreq1Functiondevpsignalgroup7"
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

    class VDDMdevelpsignalgroupreq1Functiondevpsignalgroup1:
        sig_name = "VDDMdevelpsignalgroupreq1Functiondevpsignalgroup1"
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


class VddmToSasChas1DiagReqFrame:
    msg_name = "VddmToSasChas1DiagReqFrame"
    msg_id = 1906
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['SAS']


class EcmChas1Fr12:
    msg_name = "EcmChas1Fr12"
    msg_id = 859
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.17
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BGM', 'VDDM']

    class ResrvdSigForCCM3_0_VDDMBackBoneSignalIPdu30:
        sig_name = "ResrvdSigForCCM3_0_VDDMBackBoneSignalIPdu30"
        sig_start_bit = 23
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

    class ResrvdSigForCCM1_0_VDDMBackBoneSignalIPdu30:
        sig_name = "ResrvdSigForCCM1_0_VDDMBackBoneSignalIPdu30"
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

    class ResrvdSigForCCM2_0_VDDMBackBoneSignalIPdu30:
        sig_name = "ResrvdSigForCCM2_0_VDDMBackBoneSignalIPdu30"
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

    class TqModAct:
        sig_name = "TqModAct"
        sig_start_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvModReqType1_Undefd': 0, 'DrvModReqType1_ECO': 1, 'DrvModReqType1_Comfort_Normal': 2, 'DrvModReqType1_Dynamic_Sport': 3, 'DrvModReqType1_Reserved': 8, 'DrvModReqType1_Offroad_CrossTerrain': 5, 'DrvModReqType1_Adaptive': 6, 'DrvModReqType1_Race': 7, 'DrvModReqType1_ECO_PLUS': 9, 'DrvModReqType1_Power': 10, 'DrvModReqType1_Snow': 11, 'DrvModReqType1_Sand': 12, 'DrvModReqType1_Mud': 13, 'DrvModReqType1_Rock': 14, 'DrvModReqType1_Err': 15}
        compute_method = None
        length = 4
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class ResrvdSigForCCM4_0_VDDMBackBoneSignalIPdu30:
        sig_name = "ResrvdSigForCCM4_0_VDDMBackBoneSignalIPdu30"
        sig_start_bit = 39
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


class PscmChas1Fr07:
    msg_name = "PscmChas1Fr07"
    msg_id = 78
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['ACU', 'VDDM']

    class PinionSteerAgGroupPinionSteerAg1Qf_0_PscmChas1SignalIPdu07:
        sig_name = "PinionSteerAgGroupPinionSteerAg1Qf_0_PscmChas1SignalIPdu07"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PinionSteerAgGroupSteerWhlTqQf_0_PscmChas1SignalIPdu07:
        sig_name = "PinionSteerAgGroupSteerWhlTqQf_0_PscmChas1SignalIPdu07"
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

    class PinionSteerAgGroupPinionSteerAgSpd1Qf_0_PscmChas1SignalIPdu07:
        sig_name = "PinionSteerAgGroupPinionSteerAgSpd1Qf_0_PscmChas1SignalIPdu07"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class PinionSteerAgGroupChks_0_PscmChas1SignalIPdu07:
        sig_name = "PinionSteerAgGroupChks_0_PscmChas1SignalIPdu07"
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

    class PinionSteerAgGroupPinionSteerAgSpd1_0_PscmChas1SignalIPdu07:
        sig_name = "PinionSteerAgGroupPinionSteerAgSpd1_0_PscmChas1SignalIPdu07"
        sig_start_bit = 13
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
        startbit = 13
        bmuws_info = [(1, 0b00111111, 0b11000000, 6, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class PinionSteerAgGroupSteerWhlTq_0_PscmChas1SignalIPdu07:
        sig_name = "PinionSteerAgGroupSteerWhlTq_0_PscmChas1SignalIPdu07"
        sig_start_bit = 29
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = -7680
        sig_value_max = 7680
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 29
        bmuws_info = [(3, 0b00111111, 0b11000000, 6, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class PinionSteerAgGroupPinionSteerAg1_0_PscmChas1SignalIPdu07:
        sig_name = "PinionSteerAgGroupPinionSteerAg1_0_PscmChas1SignalIPdu07"
        sig_start_bit = 46
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
        startbit = 46
        bmuws_info = [(5, 0b01111111, 0b10000000, 7, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class PinionSteerAgGroupCntr_0_PscmChas1SignalIPdu07:
        sig_name = "PinionSteerAgGroupCntr_0_PscmChas1SignalIPdu07"
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


class EtctoVddmBcmXCPFr01:
    msg_name = "EtctoVddmBcmXCPFr01"
    msg_id = 1421
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['VDDM']


class VddmChas1Fr05:
    msg_name = "VddmChas1Fr05"
    msg_id = 224
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1', 'SAS']

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

    class DrvrCrsCtrlFctSeld:
        sig_name = "DrvrCrsCtrlFctSeld"
        sig_start_bit = 20
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvrCrsCtrlFctSeldTyp_Off': 0, 'DrvrCrsCtrlFctSeldTyp_SpdLimFct_Main_Swt': 1, 'DrvrCrsCtrlFctSeldTyp_SpdLimFct_Resu': 2, 'DrvrCrsCtrlFctSeldTyp_CrsCtrlFct_Main_Swt': 3, 'DrvrCrsCtrlFctSeldTyp_CrsCtrlFct_Resu': 4, 'DrvrCrsCtrlFctSeldTyp_AccFct_Main_Swt': 5, 'DrvrCrsCtrlFctSeldTyp_AccFct_Resu': 6, 'DrvrCrsCtrlFctSeldTyp_Reserved': 7}
        compute_method = None
        length = 3
        startbit = 20
        byte = 2
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class CnvnReq:
        sig_name = "CnvnReq"
        sig_start_bit = 23
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CnvnReq_NotReqd': 0, 'CnvnReq_Chrgn': 1, 'CnvnReq_Resd1': 2, 'CnvnReq_Resd2': 3, 'CnvnReq_Resd3': 4, 'CnvnReq_Resd4': 5, 'CnvnReq_Resd5': 6, 'CnvnReq_Resd6': 7}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5


class EcmChas1Fr27:
    msg_name = "EcmChas1Fr27"
    msg_id = 609
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class EldtPmpPwrCns:
        sig_name = "EldtPmpPwrCns"
        sig_start_bit = 19
        sig_length = 12
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class VddmChas1Fr21:
    msg_name = "VddmChas1Fr21"
    msg_id = 38
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']

    class IntelliClimaHvCooltHeatrTReq_1_VgmBackboneSignalIPdu11:
        sig_name = "IntelliClimaHvCooltHeatrTReq_1_VgmBackboneSignalIPdu11"
        sig_start_bit = 39
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = "-40.0"
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 40
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class IntelliClimaHvBattInCooltFlowReq_1_VgmBackboneSignalIPdu11:
        sig_name = "IntelliClimaHvBattInCooltFlowReq_1_VgmBackboneSignalIPdu11"
        sig_start_bit = 0
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
        startbit = 0
        bmuws_info = [(0, 0b00000001, 0b11111110, 1, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class ChrgSoftSwCtrlSt:
        sig_name = "ChrgSoftSwCtrlSt"
        sig_start_bit = 46
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
        startbit = 46
        byte = 5
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class IntelliClimaHvBattInCooltTReq_1_VgmBackboneSignalIPdu11:
        sig_name = "IntelliClimaHvBattInCooltTReq_1_VgmBackboneSignalIPdu11"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 1.0
        sig_value_offset = "-50.0"
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

    class IntelliClimaReq_1_VgmBackboneSignalIPdu11:
        sig_name = "IntelliClimaReq_1_VgmBackboneSignalIPdu11"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001110
        unmask = 0b11110001
        shift = 1

    class VFCInfoEna:
        sig_name = "VFCInfoEna"
        sig_start_bit = 62
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
        startbit = 62
        byte = 7
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class IntelliClimaHvacEvaprTSp_1_VgmBackboneSignalIPdu11:
        sig_name = "IntelliClimaHvacEvaprTSp_1_VgmBackboneSignalIPdu11"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = "-5.0"
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


class EcmChas1Fr30:
    msg_name = "EcmChas1Fr30"
    msg_id = 642
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class HpBattVlvPosRec_1_EcmChas1SignalIPdu30:
        sig_name = "HpBattVlvPosRec_1_EcmChas1SignalIPdu30"
        sig_start_bit = 1
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 1
        bmuws_info = [(0, 0b00000011, 0b11111100, 2, 0), (1, 0b11111111, 0b00000000, 8, 0)]


class VddmChas1DevFr01:
    msg_name = "VddmChas1DevFr01"
    msg_id = 1434
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['CCM']

    class VDDMdevelpsignalgroupresp1Functiondevpsignalgroup4:
        sig_name = "VDDMdevelpsignalgroupresp1Functiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class VDDMdevelpsignalgroupresp1Functiondevpsignalgroup3:
        sig_name = "VDDMdevelpsignalgroupresp1Functiondevpsignalgroup3"
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

    class VDDMdevelpsignalgroupresp1Functiondevpsignalgroup6:
        sig_name = "VDDMdevelpsignalgroupresp1Functiondevpsignalgroup6"
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

    class VDDMdevelpsignalgroupresp1Functiondevpsignalgroup7:
        sig_name = "VDDMdevelpsignalgroupresp1Functiondevpsignalgroup7"
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

    class VDDMdevelpsignalgroupresp1Functiondevpsignalgroup2:
        sig_name = "VDDMdevelpsignalgroupresp1Functiondevpsignalgroup2"
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

    class VDDMdevelpsignalgroupresp1Functiondevpsignalgroup1:
        sig_name = "VDDMdevelpsignalgroupresp1Functiondevpsignalgroup1"
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

    class VDDMdevelpsignalgroupresp1Functiondevpsignalgroup5:
        sig_name = "VDDMdevelpsignalgroupresp1Functiondevpsignalgroup5"
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

    class VDDMdevelpsignalgroupresp1Functiondevpsignalgroup8:
        sig_name = "VDDMdevelpsignalgroupresp1Functiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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


class AcuChassisCAN1NmFr:
    msg_name = "AcuChassisCAN1NmFr"
    msg_id = 1321
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['PSCM1']


class EcmChas1Fr21:
    msg_name = "EcmChas1Fr21"
    msg_id = 304
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.025
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class CnvnAllwd:
        sig_name = "CnvnAllwd"
        sig_start_bit = 52
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OkNotOk_NotOk': 0, 'OkNotOk_Ok': 1}
        compute_method = None
        length = 1
        startbit = 52
        byte = 6
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class AccrpedlSts:
        sig_name = "AccrpedlSts"
        sig_start_bit = 41
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flt_NoFault': 0, 'Flt_Fault': 1}
        compute_method = None
        length = 1
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class EcmChas1Fr42:
    msg_name = "EcmChas1Fr42"
    msg_id = 837
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.26
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class SlopRiseEngCoeffSlopEqu6:
        sig_name = "SlopRiseEngCoeffSlopEqu6"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SlopRiseEngCoeffSlopEqu4:
        sig_name = "SlopRiseEngCoeffSlopEqu4"
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

    class SlopRiseEngCoeffSlopEqu9:
        sig_name = "SlopRiseEngCoeffSlopEqu9"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SlopRiseEngCoeffSlopEqu12:
        sig_name = "SlopRiseEngCoeffSlopEqu12"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SlopRiseEngCoeffSlopEqu2:
        sig_name = "SlopRiseEngCoeffSlopEqu2"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas1Fr12:
    msg_name = "VddmChas1Fr12"
    msg_id = 1087
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.35
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']

    class ResrvdSigForECM1_1_CEMBackBoneSignalIpdu18:
        sig_name = "ResrvdSigForECM1_1_CEMBackBoneSignalIpdu18"
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

    class ResrvdSigForECM3_1_CEMBackBoneSignalIpdu18:
        sig_name = "ResrvdSigForECM3_1_CEMBackBoneSignalIpdu18"
        sig_start_bit = 31
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
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class ResrvdSigForECM2_1_CEMBackBoneSignalIpdu18:
        sig_name = "ResrvdSigForECM2_1_CEMBackBoneSignalIpdu18"
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

    class ResrvdSigForECM4_1_CEMBackBoneSignalIpdu18:
        sig_name = "ResrvdSigForECM4_1_CEMBackBoneSignalIpdu18"
        sig_start_bit = 47
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
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]


class VddmChas1Fr03:
    msg_name = "VddmChas1Fr03"
    msg_id = 160
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['PSCM1']

    class ADataRawSafeAVert_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeAVert_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 55
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 1155
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class ADataRawSafeCntr_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeCntr_3_AcuFLRCANFDSignalIPdu02"
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

    class ADataRawSafeALgt1Qf_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeALgt1Qf_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 9
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 9
        byte = 1
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADataRawSafeALgt_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeALgt_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 38
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ADataRawSafeALat1Qf_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeALat1Qf_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 11
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 11
        byte = 1
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADataRawSafeALat_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeALat_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 23
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111110, 0b00000001, 7, 1)]

    class ADataRawSafeAVertQf_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeAVertQf_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 24
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 24
        bmuws_info = [(3, 0b00000001, 0b11111110, 1, 0), (4, 0b10000000, 0b01111111, 1, 7)]

    class ADataRawSafeChks_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "ADataRawSafeChks_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class SasChassisCAN1NmFr:
    msg_name = "SasChassisCAN1NmFr"
    msg_id = 1319
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SAS"
    rx_nodes = ['ECM']


class VddmChas1Fr55:
    msg_name = "VddmChas1Fr55"
    msg_id = 439
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1']

    class WhlSpdCircumlReRiQf_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlReRiQf_3_AcuFLRCANFDSignalIPdu01"
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

    class WhlSpdCircumlReLeQf_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlReLeQf_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class WhlSpdCircumlReLe_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlReLe_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 6
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
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class WhlSpdCircumlReChks_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlReChks_3_AcuFLRCANFDSignalIPdu01"
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

    class WhlSpdCircumlReCntr_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlReCntr_3_AcuFLRCANFDSignalIPdu01"
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

    class WhlSpdCircumlReRi_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlReRi_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111110, 0b00000001, 7, 1)]


class EcmChas1Fr41:
    msg_name = "EcmChas1Fr41"
    msg_id = 832
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.26
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class HvCabinThermPwrCns:
        sig_name = "HvCabinThermPwrCns"
        sig_start_bit = 36
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
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111000, 0b00000111, 5, 3)]


class VddmChas1Fr08:
    msg_name = "VddmChas1Fr08"
    msg_id = 928
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.32
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'SAS']

    class CmptmtTReFanForCmptmtTRunng_1_CEMBackBoneSignalIpdu16:
        sig_name = "CmptmtTReFanForCmptmtTRunng_1_CEMBackBoneSignalIpdu16"
        sig_start_bit = 10
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class CmptmtTReCmptmtTFrnt_1_CEMBackBoneSignalIpdu16:
        sig_name = "CmptmtTReCmptmtTFrnt_1_CEMBackBoneSignalIpdu16"
        sig_start_bit = 7
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-60.0"
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

    class ReHvacBlowerSts_1_CEMBackBoneSignalIpdu16:
        sig_name = "ReHvacBlowerSts_1_CEMBackBoneSignalIpdu16"
        sig_start_bit = 38
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacFanSts_Off': 0, 'HvacFanSts_On': 1, 'HvacFanSts_Warning': 2, 'HvacFanSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 38
        byte = 4
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5

    class AmbTIndcdWithUnitAmbTIndcd:
        sig_name = "AmbTIndcdWithUnitAmbTIndcd"
        sig_start_bit = 19
        sig_length = 12
        sig_value_factor = 0.1
        sig_value_offset = "-100.0"
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 1000
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 19
        bmuws_info = [(2, 0b00001111, 0b11110000, 4, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class AmbTIndcdWithUnitQF:
        sig_name = "AmbTIndcdWithUnitQF"
        sig_start_bit = 21
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
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class CmptmtTReCmptmtTFrntQf_1_CEMBackBoneSignalIpdu16:
        sig_name = "CmptmtTReCmptmtTFrntQf_1_CEMBackBoneSignalIpdu16"
        sig_start_bit = 12
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptmtTFrntQf_SnsrDataUndefd': 0, 'CmptmtTFrntQf_FanNotRunning': 1, 'CmptmtTFrntQf_SnsrDataNotOk': 2, 'CmptmtTFrntQf_SnsrDataOk': 3}
        compute_method = None
        length = 2
        startbit = 12
        byte = 1
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class AmbTIndcdWithUnitAmbTIndcdUnit:
        sig_name = "AmbTIndcdWithUnitAmbTIndcdUnit"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'AmbTIndcdUnit_Celsius': 0, 'AmbTIndcdUnit_Fahrenheit': 1, 'AmbTIndcdUnit_UkwnUnit': 2}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class EcmChas1Fr19:
    msg_name = "EcmChas1Fr19"
    msg_id = 991
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.27
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class HvahFltIndcnReq_0_VDDMBackBoneSignalIPdu19:
        sig_name = "HvahFltIndcnReq_0_VDDMBackBoneSignalIPdu19"
        sig_start_bit = 45
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 45
        byte = 5
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class HvBattThermPwrCns:
        sig_name = "HvBattThermPwrCns"
        sig_start_bit = 23
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11000000, 0b00111111, 2, 6)]

    class FanPwrCns:
        sig_name = "FanPwrCns"
        sig_start_bit = 42
        sig_length = 11
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 42
        bmuws_info = [(5, 0b00000111, 0b11111000, 3, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class HvCooltHeatrICnsSig_1_EcmChas1SignalIPdu19:
        sig_name = "HvCooltHeatrICnsSig_1_EcmChas1SignalIPdu19"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = 0.25
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


class BgmChas1Fr01:
    msg_name = "BgmChas1Fr01"
    msg_id = 293
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.015
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['VDDM', 'ECM']

    class CDCDrvrGearShiftDirReq2UpTipAut:
        sig_name = "CDCDrvrGearShiftDirReq2UpTipAut"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CDCDrvrGearShiftDirReq2DwnRTipAut:
        sig_name = "CDCDrvrGearShiftDirReq2DwnRTipAut"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CDCDrvrGearShiftDirReq1DwnTipAut:
        sig_name = "CDCDrvrGearShiftDirReq1DwnTipAut"
        sig_start_bit = 14
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
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CDCDrvrGearShiftParkReqSts_0_BgmChas1SignalIPdu01:
        sig_name = "CDCDrvrGearShiftParkReqSts_0_BgmChas1SignalIPdu01"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class CDCDrvrGearShiftDirReq1Chks:
        sig_name = "CDCDrvrGearShiftDirReq1Chks"
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

    class CDCDrvrGearShiftDirReq1UpDTipAut:
        sig_name = "CDCDrvrGearShiftDirReq1UpDTipAut"
        sig_start_bit = 12
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

    class CDCDrvrGearShiftDirReq1Cntr:
        sig_name = "CDCDrvrGearShiftDirReq1Cntr"
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

    class CDCDrvrGearShiftParkReq1_0_BgmChas1SignalIPdu01:
        sig_name = "CDCDrvrGearShiftParkReq1_0_BgmChas1SignalIPdu01"
        sig_start_bit = 61
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
        startbit = 61
        byte = 7
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CDCDrvrGearShiftDirReq2PosnAut:
        sig_name = "CDCDrvrGearShiftDirReq2PosnAut"
        sig_start_bit = 37
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
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CDCDrvrGearShiftDirReq1UpTipAut:
        sig_name = "CDCDrvrGearShiftDirReq1UpTipAut"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CDCGearShiftUnitSt_0_BgmChas1SignalIPdu01:
        sig_name = "CDCGearShiftUnitSt_0_BgmChas1SignalIPdu01"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4

    class CDCDrvrGearShiftDirReq1PosnAut:
        sig_name = "CDCDrvrGearShiftDirReq1PosnAut"
        sig_start_bit = 13
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
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class CDCDrvrGearShiftDirReq2Chks:
        sig_name = "CDCDrvrGearShiftDirReq2Chks"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class CDCDrvrGearShiftDirReq2Cntr:
        sig_name = "CDCDrvrGearShiftDirReq2Cntr"
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

    class CDCDrvrGearShiftDirReq1DwnRTipAut:
        sig_name = "CDCDrvrGearShiftDirReq1DwnRTipAut"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class CDCDrvrGearShiftDirReq2UpDTipAut:
        sig_name = "CDCDrvrGearShiftDirReq2UpDTipAut"
        sig_start_bit = 36
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

    class CDCDrvrGearShiftParkReqCntr_0_BgmChas1SignalIPdu01:
        sig_name = "CDCDrvrGearShiftParkReqCntr_0_BgmChas1SignalIPdu01"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class CDCDrvrGearShiftDirReq2DwnTipAut:
        sig_name = "CDCDrvrGearShiftDirReq2DwnTipAut"
        sig_start_bit = 38
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
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class CDCDrvrGearShiftParkReqChks_0_BgmChas1SignalIPdu01:
        sig_name = "CDCDrvrGearShiftParkReqChks_0_BgmChas1SignalIPdu01"
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


class VddmChas1Fr23:
    msg_name = "VddmChas1Fr23"
    msg_id = 784
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.17
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['SAS']

    class CmptmtTFrntFanForCmptmtTRunng_2_VgmConnSignalIPdu13:
        sig_name = "CmptmtTFrntFanForCmptmtTRunng_2_VgmConnSignalIPdu13"
        sig_start_bit = 24
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Flg1_Rst': 0, 'Flg1_Set': 1}
        compute_method = None
        length = 1
        startbit = 24
        byte = 3
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CmptmtTFrntQf_2_VgmConnSignalIPdu13:
        sig_name = "CmptmtTFrntQf_2_VgmConnSignalIPdu13"
        sig_start_bit = 26
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'CmptmtTFrntQf_SnsrDataUndefd': 0, 'CmptmtTFrntQf_FanNotRunning': 1, 'CmptmtTFrntQf_SnsrDataNotOk': 2, 'CmptmtTFrntQf_SnsrDataOk': 3}
        compute_method = None
        length = 2
        startbit = 26
        byte = 3
        mask = 0b00000110
        unmask = 0b11111001
        shift = 1

    class CmptmtTFrntCmptmtTFrnt_2_VgmConnSignalIPdu13:
        sig_name = "CmptmtTFrntCmptmtTFrnt_2_VgmConnSignalIPdu13"
        sig_start_bit = 21
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 1850
        sig_byteorder = "Motorola"
        sig_value_init = 600
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 21
        bmuws_info = [(2, 0b00111111, 0b11000000, 6, 0), (3, 0b11111000, 0b00000111, 5, 3)]


class EtcToPscmDevelFr:
    msg_name = "EtcToPscmDevelFr"
    msg_id = 1431
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['PSCM1']

    class PSCMdevelpsignalgroupreq1Functiondevpsignalgroup2:
        sig_name = "PSCMdevelpsignalgroupreq1Functiondevpsignalgroup2"
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

    class PSCMdevelpsignalgroupreq1Functiondevpsignalgroup1:
        sig_name = "PSCMdevelpsignalgroupreq1Functiondevpsignalgroup1"
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

    class PSCMdevelpsignalgroupreq1Functiondevpsignalgroup3:
        sig_name = "PSCMdevelpsignalgroupreq1Functiondevpsignalgroup3"
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

    class PSCMdevelpsignalgroupreq1Functiondevpsignalgroup5:
        sig_name = "PSCMdevelpsignalgroupreq1Functiondevpsignalgroup5"
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

    class PSCMdevelpsignalgroupreq1Functiondevpsignalgroup8:
        sig_name = "PSCMdevelpsignalgroupreq1Functiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class PSCMdevelpsignalgroupreq1Functiondevpsignalgroup6:
        sig_name = "PSCMdevelpsignalgroupreq1Functiondevpsignalgroup6"
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

    class PSCMdevelpsignalgroupreq1Functiondevpsignalgroup4:
        sig_name = "PSCMdevelpsignalgroupreq1Functiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class PSCMdevelpsignalgroupreq1Functiondevpsignalgroup7:
        sig_name = "PSCMdevelpsignalgroupreq1Functiondevpsignalgroup7"
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


class VddmChas1Fr10:
    msg_name = "VddmChas1Fr10"
    msg_id = 433
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1']

    class BrkPedlPsdChks:
        sig_name = "BrkPedlPsdChks"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class WhlSpdCircumlFrntRiQf_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlFrntRiQf_3_AcuFLRCANFDSignalIPdu01"
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

    class BrkPedlPsdBrkPedlPsd:
        sig_name = "BrkPedlPsdBrkPedlPsd"
        sig_start_bit = 54
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
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class BrkPedlPsdQf:
        sig_name = "BrkPedlPsdQf"
        sig_start_bit = 53
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
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class WhlSpdCircumlFrntWhlSpdCircumlFrntRi_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlFrntWhlSpdCircumlFrntRi_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111110, 0b00000001, 7, 1)]

    class BrkPedlPsdBrkPedlNotPsdSafe:
        sig_name = "BrkPedlPsdBrkPedlNotPsdSafe"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WhlSpdCircumlFrntLe_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlFrntLe_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 6
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
        startbit = 6
        bmuws_info = [(0, 0b01111111, 0b10000000, 7, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class WhlSpdCircumlFrntCntr_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlFrntCntr_3_AcuFLRCANFDSignalIPdu01"
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

    class WhlSpdCircumlFrntChks_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlFrntChks_3_AcuFLRCANFDSignalIPdu01"
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

    class WhlSpdCircumlFrntLeQf_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "WhlSpdCircumlFrntLeQf_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class BrkPedlPsdCntr:
        sig_name = "BrkPedlPsdCntr"
        sig_start_bit = 51
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


class EtctoVddmDevelFr02:
    msg_name = "EtctoVddmDevelFr02"
    msg_id = 1433
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['VDDM']

    class VDDMdevelpsignalgroupreq2Functiondevpsignalgroup7:
        sig_name = "VDDMdevelpsignalgroupreq2Functiondevpsignalgroup7"
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

    class VDDMdevelpsignalgroupreq2Functiondevpsignalgroup6:
        sig_name = "VDDMdevelpsignalgroupreq2Functiondevpsignalgroup6"
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

    class VDDMdevelpsignalgroupreq2Functiondevpsignalgroup4:
        sig_name = "VDDMdevelpsignalgroupreq2Functiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class VDDMdevelpsignalgroupreq2Functiondevpsignalgroup1:
        sig_name = "VDDMdevelpsignalgroupreq2Functiondevpsignalgroup1"
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

    class VDDMdevelpsignalgroupreq2Functiondevpsignalgroup5:
        sig_name = "VDDMdevelpsignalgroupreq2Functiondevpsignalgroup5"
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

    class VDDMdevelpsignalgroupreq2Functiondevpsignalgroup2:
        sig_name = "VDDMdevelpsignalgroupreq2Functiondevpsignalgroup2"
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

    class VDDMdevelpsignalgroupreq2Functiondevpsignalgroup3:
        sig_name = "VDDMdevelpsignalgroupreq2Functiondevpsignalgroup3"
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

    class VDDMdevelpsignalgroupreq2Functiondevpsignalgroup8:
        sig_name = "VDDMdevelpsignalgroupreq2Functiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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


class EcmChas1Fr29:
    msg_name = "EcmChas1Fr29"
    msg_id = 632
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class GrlShttrStsShttrElecErr_1_EcmChas1SignalIPdu29:
        sig_name = "GrlShttrStsShttrElecErr_1_EcmChas1SignalIPdu29"
        sig_start_bit = 11
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrElecErr_ShttrNoElecErr': 0, 'ShttrElecErr_ShttrElecErr': 1}
        compute_method = None
        length = 1
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class GrlShttrStsShttrPosnRaw_1_EcmChas1SignalIPdu29:
        sig_name = "GrlShttrStsShttrPosnRaw_1_EcmChas1SignalIPdu29"
        sig_start_bit = 7
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

    class GrlShttrStsShttrActrFlt_1_EcmChas1SignalIPdu29:
        sig_name = "GrlShttrStsShttrActrFlt_1_EcmChas1SignalIPdu29"
        sig_start_bit = 15
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrActrFlt_ShttrActrNoFlt': 0, 'ShttrActrFlt_ShttrActrFlt': 1}
        compute_method = None
        length = 1
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class GrlShttrStsShttrCalIndcd_1_EcmChas1SignalIPdu29:
        sig_name = "GrlShttrStsShttrCalIndcd_1_EcmChas1SignalIPdu29"
        sig_start_bit = 12
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrCalIndcd_ShttrCalNotIndcd': 0, 'ShttrCalIndcd_ShttrCalIndcd': 1}
        compute_method = None
        length = 1
        startbit = 12
        byte = 1
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class GrlShttrStsShttrTErr_1_EcmChas1SignalIPdu29:
        sig_name = "GrlShttrStsShttrTErr_1_EcmChas1SignalIPdu29"
        sig_start_bit = 9
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrTErr_ShttrTNoErr': 0, 'ShttrTErr_ShttrTErr': 1}
        compute_method = None
        length = 1
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class ChrgnSpd_1_BgmConnectivitySignalIPdu03:
        sig_name = "ChrgnSpd_1_BgmConnectivitySignalIPdu03"
        sig_start_bit = 38
        sig_length = 11
        sig_value_factor = 1
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 38
        bmuws_info = [(4, 0b01111111, 0b10000000, 7, 0), (5, 0b11110000, 0b00001111, 4, 4)]

    class HpBattFwvPosRec_1_EcmChas1SignalIPdu29:
        sig_name = "HpBattFwvPosRec_1_EcmChas1SignalIPdu29"
        sig_start_bit = 43
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 43
        bmuws_info = [(5, 0b00001111, 0b11110000, 4, 0), (6, 0b11111100, 0b00000011, 6, 2)]

    class GrlShttrStsShttrSnsrFlt_1_EcmChas1SignalIPdu29:
        sig_name = "GrlShttrStsShttrSnsrFlt_1_EcmChas1SignalIPdu29"
        sig_start_bit = 10
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrSnsrFlt_ShttrSnsrNoFlt': 0, 'ShttrSnsrFlt_ShttrSnsrFlt': 1}
        compute_method = None
        length = 1
        startbit = 10
        byte = 1
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class GrlShttrStsShttrBlkd_1_EcmChas1SignalIPdu29:
        sig_name = "GrlShttrStsShttrBlkd_1_EcmChas1SignalIPdu29"
        sig_start_bit = 14
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrBlkd_ShttrNotBlkd': 0, 'ShttrBlkd_ShttrBlkd': 1}
        compute_method = None
        length = 1
        startbit = 14
        byte = 1
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class GrlShttrStsShttrULoErr_1_EcmChas1SignalIPdu29:
        sig_name = "GrlShttrStsShttrULoErr_1_EcmChas1SignalIPdu29"
        sig_start_bit = 8
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrULoErr_ShttrNoULoErr': 0, 'ShttrULoErr_ShttrULoErr': 1}
        compute_method = None
        length = 1
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class GrlShttrStsShttrCalActv_1_EcmChas1SignalIPdu29:
        sig_name = "GrlShttrStsShttrCalActv_1_EcmChas1SignalIPdu29"
        sig_start_bit = 13
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ShttrCalActv_NotActv': 0, 'ShttrCalActv_Actv': 1}
        compute_method = None
        length = 1
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class AsdmChas1Fr01:
    msg_name = "AsdmChas1Fr01"
    msg_id = 147
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "ACU"
    rx_nodes = ['ECM', 'PSCM1']

    class RctaBrkReqQM:
        sig_name = "RctaBrkReqQM"
        sig_start_bit = 13
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
        startbit = 13
        byte = 1
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class AsyADL3FuncCtrlStsCtrlSts_2_AsdmChas1SignalIPdu01:
        sig_name = "AsyADL3FuncCtrlStsCtrlSts_2_AsdmChas1SignalIPdu01"
        sig_start_bit = 33
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Primary': 0, 'Secondary': 1}
        compute_method = None
        length = 1
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AsyStrAllwdReqGroupChks:
        sig_name = "AsyStrAllwdReqGroupChks"
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

    class AsyADL3FuncCtrlStsQf_2_AsdmChas1SignalIPdu01:
        sig_name = "AsyADL3FuncCtrlStsQf_2_AsdmChas1SignalIPdu01"
        sig_start_bit = 25
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
        startbit = 25
        byte = 3
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AsyADL3FuncCtrlStsADMod_2_AsdmChas1SignalIPdu01:
        sig_name = "AsyADL3FuncCtrlStsADMod_2_AsdmChas1SignalIPdu01"
        sig_start_bit = 27
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ADMod_NAD_Mod': 0, 'ADMod_MarsParking': 1, 'ADMod_ANP': 2, 'ADMod_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AsyADModeReqCntr_2_AsdmChas1SignalIPdu01:
        sig_name = "AsyADModeReqCntr_2_AsdmChas1SignalIPdu01"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class AsyADL3FuncCtrlStsDegraded_2_AsdmChas1SignalIPdu01:
        sig_name = "AsyADL3FuncCtrlStsDegraded_2_AsdmChas1SignalIPdu01"
        sig_start_bit = 39
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

    class AsyADL3FuncCtrlStsSts_2_AsdmChas1SignalIPdu01:
        sig_name = "AsyADL3FuncCtrlStsSts_2_AsdmChas1SignalIPdu01"
        sig_start_bit = 35
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 35
        byte = 4
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class RcwmBrkReqQM:
        sig_name = "RcwmBrkReqQM"
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

    class AsyADL3FuncCtrlStsCntr_2_AsdmChas1SignalIPdu01:
        sig_name = "AsyADL3FuncCtrlStsCntr_2_AsdmChas1SignalIPdu01"
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

    class AsyStrAllwdReqGroupCntr:
        sig_name = "AsyStrAllwdReqGroupCntr"
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

    class AsyADModeReqADActiveReq_2_AsdmChas1SignalIPdu01:
        sig_name = "AsyADModeReqADActiveReq_2_AsdmChas1SignalIPdu01"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ADMod_NAD_Mod': 0, 'ADMod_MarsParking': 1, 'ADMod_ANP': 2, 'ADMod_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AsyStrAllwdReqGroupStrAllwdReq:
        sig_name = "AsyStrAllwdReqGroupStrAllwdReq"
        sig_start_bit = 59
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
        startbit = 59
        byte = 7
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class AsyADModeReqADDeactiveReq_2_AsdmChas1SignalIPdu01:
        sig_name = "AsyADModeReqADDeactiveReq_2_AsdmChas1SignalIPdu01"
        sig_start_bit = 49
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
        startbit = 49
        byte = 6
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AsyADModeReqChks_2_AsdmChas1SignalIPdu01:
        sig_name = "AsyADModeReqChks_2_AsdmChas1SignalIPdu01"
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

    class PASFuncActive:
        sig_name = "PASFuncActive"
        sig_start_bit = 15
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
        startbit = 15
        byte = 1
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class AsyADL3FuncCtrlStsChks_2_AsdmChas1SignalIPdu01:
        sig_name = "AsyADL3FuncCtrlStsChks_2_AsdmChas1SignalIPdu01"
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


class EcmChas1Fr31:
    msg_name = "EcmChas1Fr31"
    msg_id = 131
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['BGM', 'VDDM']

    class EngSt1WdStsEngSt1WdSts_0_EcmChas1SignalIPdu31:
        sig_name = "EngSt1WdStsEngSt1WdSts_0_EcmChas1SignalIPdu31"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class EngSt1WdStsCntr_0_EcmChas1SignalIPdu31:
        sig_name = "EngSt1WdStsCntr_0_EcmChas1SignalIPdu31"
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

    class StandStillReqForCmftToBrkgForEPedl:
        sig_name = "StandStillReqForCmftToBrkgForEPedl"
        sig_start_bit = 22
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
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EngSt1WdStsChks_0_EcmChas1SignalIPdu31:
        sig_name = "EngSt1WdStsChks_0_EcmChas1SignalIPdu31"
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


class VddmChas1Fr52:
    msg_name = "VddmChas1Fr52"
    msg_id = 17
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']

    class GearPrkgAssiReqGroupChks:
        sig_name = "GearPrkgAssiReqGroupChks"
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

    class LgtCtrlModReqSafeLgtCtrlModReqSafe:
        sig_name = "LgtCtrlModReqSafeLgtCtrlModReqSafe"
        sig_start_bit = 11
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ModCfmd_NoReq': 0, 'ModCfmd_MarsParking': 1, 'ModCfmd_Reserved2': 2, 'ModCfmd_Reserved3': 3, 'ModCfmd_Reserved4': 4, 'ModCfmd_ANP': 5, 'ModCfmd_Reserved6': 6, 'ModCfmd_Reserved7': 7, 'ModCfmd_Reserved8': 8, 'ModCfmd_ACC_HWA': 9, 'ModCfmd_PEB': 10, 'ModCfmd_APA': 11, 'ModCfmd_RPA': 12, 'ModCfmd_HPA': 13, 'ModCfmd_TJP_HWC': 14, 'ModCfmd_NOP': 15}
        compute_method = None
        length = 4
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class GearPrkgAssiReqGroupCntr:
        sig_name = "GearPrkgAssiReqGroupCntr"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class GearPrkgAssiReqGroupGearPrkgAssiReq1:
        sig_name = "GearPrkgAssiReqGroupGearPrkgAssiReq1"
        sig_start_bit = 51
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearPrkgAssiReq1_NoRequest': 0, 'GearPrkgAssiReq1_TargetgearP': 1, 'GearPrkgAssiReq1_TargetgearR': 2, 'GearPrkgAssiReq1_TargetgearD': 3}
        compute_method = None
        length = 2
        startbit = 51
        byte = 6
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class LgtCtrlModReqSafeLgtFctFailr:
        sig_name = "LgtCtrlModReqSafeLgtFctFailr"
        sig_start_bit = 23
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LgtFctFail_NoFailure': 0, 'LgtFctFail_MarsParkingFailure': 1, 'LgtFctFail_APAFailure': 2, 'LgtFctFail_RPAFailure': 3, 'LgtFctFail_HPAFailure': 4, 'LgtFctFail_ACCFailure': 5, 'LgtFctFail_ANPFailure': 6, 'LgtFctFail_E2EFailure': 7}
        compute_method = None
        length = 3
        startbit = 23
        byte = 2
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class LgtCtrlModReqSafeCntr:
        sig_name = "LgtCtrlModReqSafeCntr"
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

    class LgtCtrlModReqSafeChks:
        sig_name = "LgtCtrlModReqSafeChks"
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


class EcmChas1Fr18:
    msg_name = "EcmChas1Fr18"
    msg_id = 563
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class HeatrPmpIAct:
        sig_name = "HeatrPmpIAct"
        sig_start_bit = 55
        sig_length = 8
        sig_value_factor = 0.2
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 254
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

    class HeatrPmpPwrCns:
        sig_name = "HeatrPmpPwrCns"
        sig_start_bit = 35
        sig_length = 12
        sig_value_factor = 1.0
        sig_value_offset = 0.0
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

    class CmprRunTime:
        sig_name = "CmprRunTime"
        sig_start_bit = 7
        sig_length = 32
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 32
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]


class EcmChassisCAN1NmFr:
    msg_name = "EcmChassisCAN1NmFr"
    msg_id = 1296
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['SAS']


class VddmChas1Fr01:
    msg_name = "VddmChas1Fr01"
    msg_id = 81
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['PSCM1']

    class AsyDataWithCmpSafeALat1Qf:
        sig_name = "AsyDataWithCmpSafeALat1Qf"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AsyDataWithCmpSafeALatWithCmp:
        sig_name = "AsyDataWithCmpSafeALatWithCmp"
        sig_start_bit = 55
        sig_length = 15
        sig_value_factor = 0.0085
        sig_value_offset = 0.0
        sig_value_min = -16352
        sig_value_max = 16353
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 15
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11111110, 0b00000001, 7, 1)]

    class AsyDataWithCmpSafeALgt1Qf:
        sig_name = "AsyDataWithCmpSafeALgt1Qf"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class AsyDataWithCmpSafeGrdtOfALgt:
        sig_name = "AsyDataWithCmpSafeGrdtOfALgt"
        sig_start_bit = 31
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = -7680
        sig_value_max = 7680
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 31
        bmuws_info = [(3, 0b11111111, 0b00000000, 8, 0), (4, 0b11111100, 0b00000011, 6, 2)]

    class AsyDataWithCmpSafeCntr:
        sig_name = "AsyDataWithCmpSafeCntr"
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

    class AsyDataWithCmpSafeYawRateWithCmp:
        sig_name = "AsyDataWithCmpSafeYawRateWithCmp"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class AsyDataWithCmpSafeChks:
        sig_name = "AsyDataWithCmpSafeChks"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AsyDataWithCmpSafeYawRateQf:
        sig_name = "AsyDataWithCmpSafeYawRateQf"
        sig_start_bit = 33
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 33
        byte = 4
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0


class SasChas1Fr01:
    msg_name = "SasChas1Fr01"
    msg_id = 64
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "SAS"
    rx_nodes = ['ACU', 'VDDM', 'ECM', 'PSCM1']

    class SteerWhlSnsrCntr_0_SasChas1SignalIPdu01:
        sig_name = "SteerWhlSnsrCntr_0_SasChas1SignalIPdu01"
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

    class SteerWhlSnsrAgSpd_0_SasChas1SignalIPdu01:
        sig_name = "SteerWhlSnsrAgSpd_0_SasChas1SignalIPdu01"
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

    class SteerWhlSnsrQf_0_SasChas1SignalIPdu01:
        sig_name = "SteerWhlSnsrQf_0_SasChas1SignalIPdu01"
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

    class SteerWhlSnsrChks_0_SasChas1SignalIPdu01:
        sig_name = "SteerWhlSnsrChks_0_SasChas1SignalIPdu01"
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

    class SteerWhlSnsrAg_0_SasChas1SignalIPdu01:
        sig_name = "SteerWhlSnsrAg_0_SasChas1SignalIPdu01"
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


class EcmChas1Fr43:
    msg_name = "EcmChas1Fr43"
    msg_id = 822
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.26
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class SpdRelatWghtSpdEqu100:
        sig_name = "SpdRelatWghtSpdEqu100"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SpdRelatWghtSpdEqu40:
        sig_name = "SpdRelatWghtSpdEqu40"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SpdRelatWghtSpdEqu140:
        sig_name = "SpdRelatWghtSpdEqu140"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SpdRelatWghtSpdEqu80:
        sig_name = "SpdRelatWghtSpdEqu80"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SpdRelatWghtSpdEqu120:
        sig_name = "SpdRelatWghtSpdEqu120"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SpdRelatWghtSpdEqu20:
        sig_name = "SpdRelatWghtSpdEqu20"
        sig_start_bit = 15
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

    class SpdRelatWghtSpdEqu10:
        sig_name = "SpdRelatWghtSpdEqu10"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SpdRelatWghtSpdEqu60:
        sig_name = "SpdRelatWghtSpdEqu60"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas1Fr50:
    msg_name = "VddmChas1Fr50"
    msg_id = 896
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.7
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['PSCM1', 'SAS']

    class VehBattUSysUQf_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehBattUSysUQf_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 49
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
        startbit = 49
        byte = 6
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class VehBattUSysU_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehBattUSysU_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 63
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
        startbit = 63
        byte = 7
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmChas1Fr54:
    msg_name = "VddmChas1Fr54"
    msg_id = 580
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.2
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['PSCM1']

    class IDcDcActLoSideChks:
        sig_name = "IDcDcActLoSideChks"
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

    class IDcDcActLoSideIDcDcActLoSide:
        sig_name = "IDcDcActLoSideIDcDcActLoSide"
        sig_start_bit = 23
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11110000, 0b00001111, 4, 4)]

    class IDcDcActLoSideCntr:
        sig_name = "IDcDcActLoSideCntr"
        sig_start_bit = 3
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


class EcmChas1Fr22:
    msg_name = "EcmChas1Fr22"
    msg_id = 1135
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['ACU', 'VDDM']

    class DrvrGearShiftParkReqSts:
        sig_name = "DrvrGearShiftParkReqSts"
        sig_start_bit = 27
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
        startbit = 27
        byte = 3
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class DrvrGearShiftParkReq1:
        sig_name = "DrvrGearShiftParkReq1"
        sig_start_bit = 25
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
        startbit = 25
        byte = 3
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class DrvrGearShiftParkReqChks:
        sig_name = "DrvrGearShiftParkReqChks"
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

    class BattCooltIndcnReq:
        sig_name = "BattCooltIndcnReq"
        sig_start_bit = 8
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
        startbit = 8
        byte = 1
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class CooltFlowInCmptmtCirc_0_EcmChas1SignalIPdu22:
        sig_name = "CooltFlowInCmptmtCirc_0_EcmChas1SignalIPdu22"
        sig_start_bit = 55
        sig_length = 10
        sig_value_factor = 0.05
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1023
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 55
        bmuws_info = [(6, 0b11111111, 0b00000000, 8, 0), (7, 0b11000000, 0b00111111, 2, 6)]

    class USecDcDcActHiSide_1_EcmChas1SignalIPdu22:
        sig_name = "USecDcDcActHiSide_1_EcmChas1SignalIPdu22"
        sig_start_bit = 7
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class SecDcDcActvd_1_EcmChas1SignalIPdu22:
        sig_name = "SecDcDcActvd_1_EcmChas1SignalIPdu22"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DcDcActvd2_DcDcInactive': 0, 'DcDcActvd2_DcDcActive': 1, 'DcDcActvd2_Abnormal': 2, 'DcDcActvd2_Invalid': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class DrvrGearShiftParkReqCntr:
        sig_name = "DrvrGearShiftParkReqCntr"
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

    class TelltlPwrLoss:
        sig_name = "TelltlPwrLoss"
        sig_start_bit = 46
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
        startbit = 46
        byte = 5
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6


class VddmChas1Fr22:
    msg_name = "VddmChas1Fr22"
    msg_id = 1123
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.17
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1']

    class HvacEvaprTSpRe_1_CEMBackBoneSignalIpdu12:
        sig_name = "HvacEvaprTSpRe_1_CEMBackBoneSignalIpdu12"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = 0.1
        sig_value_offset = "-5.0"
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

    class EvaprTReEvaprTFrnt_1_CEMBackBoneSignalIpdu12:
        sig_name = "EvaprTReEvaprTFrnt_1_CEMBackBoneSignalIpdu12"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111000, 0b00000111, 5, 3)]

    class EvaprTReEvaprTQf_1_CEMBackBoneSignalIpdu12:
        sig_name = "EvaprTReEvaprTQf_1_CEMBackBoneSignalIpdu12"
        sig_start_bit = 42
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacTIfQf_SnsrDataNotOk': 0, 'HvacTIfQf_SnsrDataOk': 1}
        compute_method = None
        length = 1
        startbit = 42
        byte = 5
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2

    class SteerAsscLvl:
        sig_name = "SteerAsscLvl"
        sig_start_bit = 60
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerAsscLvl_Ukwn': 0, 'SteerAsscLvl_Lvl1': 1, 'SteerAsscLvl_Lvl2': 2, 'SteerAsscLvl_Lvl3': 3, 'SteerAsscLvl_Lvl4': 4, 'SteerAsscLvl_Resd5': 5, 'SteerAsscLvl_Resd6': 6, 'SteerAsscLvl_Resd7': 7}
        compute_method = None
        length = 3
        startbit = 60
        byte = 7
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2


class Pscm1ChassisCAN1NmFr:
    msg_name = "Pscm1ChassisCAN1NmFr"
    msg_id = 1315
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['PSCM2']


class VddmChas1Fr48:
    msg_name = "VddmChas1Fr48"
    msg_id = 1159
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.7
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['PSCM1']

    class VehMtnStCntr_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehMtnStCntr_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 6
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

    class VehMtnStVehMtnSt_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehMtnStVehMtnSt_3_AcuFLRCANFDSignalIPdu01"
        sig_start_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000111
        unmask = 0b11111000
        shift = 0

    class VehMtnStChks_3_AcuFLRCANFDSignalIPdu01:
        sig_name = "VehMtnStChks_3_AcuFLRCANFDSignalIPdu01"
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


class VddmChas1Fr04:
    msg_name = "VddmChas1Fr04"
    msg_id = 400
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1']

    class AbsCtrlActvChks_0_BcmVddmBackBoneSignalIPdu00:
        sig_name = "AbsCtrlActvChks_0_BcmVddmBackBoneSignalIPdu00"
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

    class AmbTRawAmbTVal:
        sig_name = "AmbTRawAmbTVal"
        sig_start_bit = 50
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-70.0"
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

    class LatCtrlReqSafeSteerTqReq:
        sig_name = "LatCtrlReqSafeSteerTqReq"
        sig_start_bit = 39
        sig_length = 14
        sig_value_factor = 0.00390625
        sig_value_offset = 0.0
        sig_value_min = -7680
        sig_value_max = 7680
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 14
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111100, 0b00000011, 6, 2)]

    class LatCtrlReqSafeSteerWhlHptcWarnReq:
        sig_name = "LatCtrlReqSafeSteerWhlHptcWarnReq"
        sig_start_bit = 41
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
        startbit = 41
        byte = 5
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AbsCtrlActvCntr_0_BcmVddmBackBoneSignalIPdu00:
        sig_name = "AbsCtrlActvCntr_0_BcmVddmBackBoneSignalIPdu00"
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

    class AmbTRawQly:
        sig_name = "AmbTRawQly"
        sig_start_bit = 52
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
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class LatCtrlReqSafeCntr:
        sig_name = "LatCtrlReqSafeCntr"
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

    class LatCtrlReqSafeChks:
        sig_name = "LatCtrlReqSafeChks"
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

    class AbsCtrlActvCtrlSts1_0_BcmVddmBackBoneSignalIPdu00:
        sig_name = "AbsCtrlActvCtrlSts1_0_BcmVddmBackBoneSignalIPdu00"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class LatCtrlReqSafeLatCtrlModReq:
        sig_name = "LatCtrlReqSafeLatCtrlModReq"
        sig_start_bit = 27
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LatCtrlMod1_NoReq': 0, 'LatCtrlMod1_HighWayAssist': 1, 'LatCtrlMod1_EmgyLaneKeepAidForObjRe': 2, 'LatCtrlMod1_EmgyLaneKeepAidForStat': 3, 'LatCtrlMod1_SftyLaneKeepAid': 4, 'LatCtrlMod1_SteerAssc': 5, 'LatCtrlMod1_DsrOversteer': 6, 'LatCtrlMod1_DsrMueSplit': 7, 'LatCtrlMod1_DsrTrlrStaby': 8, 'LatCtrlMod1_EmgyManvAssi': 9, 'LatCtrlMod1_Reserved1': 10, 'LatCtrlMod1_Reserved2': 11, 'LatCtrlMod1_SHWA': 12, 'LatCtrlMod1_APA': 13, 'LatCtrlMod1_RPA': 14, 'LatCtrlMod1_HPA': 15}
        compute_method = None
        length = 4
        startbit = 27
        byte = 3
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class VddmChas1Fr47:
    msg_name = "VddmChas1Fr47"
    msg_id = 26
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.1
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1']

    class AgDataCmpQualityPitchRateCmpQuality:
        sig_name = "AgDataCmpQualityPitchRateCmpQuality"
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

    class AgDataCmpQualityRollRateCmpQuality:
        sig_name = "AgDataCmpQualityRollRateCmpQuality"
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

    class AgDataCmpQualityYawRateCmpQuality:
        sig_name = "AgDataCmpQualityYawRateCmpQuality"
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

    class EgyRgnLvlSet:
        sig_name = "EgyRgnLvlSet"
        sig_start_bit = 46
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EgyRgnLvlSet_Level1': 0, 'EgyRgnLvlSet_Level2': 1, 'EgyRgnLvlSet_Level3': 2, 'EgyRgnLvlSet_Level4': 3}
        compute_method = None
        length = 2
        startbit = 46
        byte = 5
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5


class EcmChas1Fr39:
    msg_name = "EcmChas1Fr39"
    msg_id = 1158
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 1.0
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class HpcSov2OnOffSts:
        sig_name = "HpcSov2OnOffSts"
        sig_start_bit = 9
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
        startbit = 9
        byte = 1
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1

    class AcHexOutT:
        sig_name = "AcHexOutT"
        sig_start_bit = 7
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
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111000, 0b00000111, 5, 3)]

    class AcLoSideP:
        sig_name = "AcLoSideP"
        sig_start_bit = 23
        sig_length = 13
        sig_value_factor = 1.0
        sig_value_offset = 0
        sig_value_min = 0
        sig_value_max = 5000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 13
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111000, 0b00000111, 5, 3)]

    class HpcThmMngtSts:
        sig_name = "HpcThmMngtSts"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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


class EcmChas1Fr37:
    msg_name = "EcmChas1Fr37"
    msg_id = 752
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['SAS']

    class EngSt1WdSts1:
        sig_name = "EngSt1WdSts1"
        sig_start_bit = 11
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
        startbit = 11
        byte = 1
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0


class EcmChas1Fr24:
    msg_name = "EcmChas1Fr24"
    msg_id = 455
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['ACU', 'VDDM']

    class PropLgtCtrlModCfmdChks:
        sig_name = "PropLgtCtrlModCfmdChks"
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

    class PropLgtCtrlModCfmdCntr:
        sig_name = "PropLgtCtrlModCfmdCntr"
        sig_start_bit = 43
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

    class PropLgtCtrlModCfmdLgtDegradation:
        sig_name = "PropLgtCtrlModCfmdLgtDegradation"
        sig_start_bit = 47
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LgtDegrad_NoDegradation': 0, 'LgtDegrad_TorqueLimitation': 1, 'LgtDegrad_TotallyFault': 2, 'LgtDegrad_Reserved1': 3, 'LgtDegrad_Reserved2': 4, 'LgtDegrad_Reserved3': 5, 'LgtDegrad_Reserved4': 6, 'LgtDegrad_Reserved5': 7}
        compute_method = None
        length = 3
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class PropLgtCtrlModCfmdPropLgtCtrlModCfmd:
        sig_name = "PropLgtCtrlModCfmdPropLgtCtrlModCfmd"
        sig_start_bit = 55
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LgtCtrlModCfmd_NotRequest': 0, 'LgtCtrlModCfmd_MarsParking': 1, 'LgtCtrlModCfmd_APA': 2, 'LgtCtrlModCfmd_RPA': 3, 'LgtCtrlModCfmd_HPA': 4, 'LgtCtrlModCfmd_ANP': 5, 'LgtCtrlModCfmd_E2E': 6, 'LgtCtrlModCfmd_Reserved3': 7}
        compute_method = None
        length = 3
        startbit = 55
        byte = 6
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class HvActvSts:
        sig_name = "HvActvSts"
        sig_start_bit = 31
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvActvSts_Default': 0, 'HvActvSts_CPSRIsActivated': 1, 'HvActvSts_CPSRPlusContactorsIsActivated': 2, 'HvActvSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 31
        byte = 3
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6


class BgmChas1Fr02:
    msg_name = "BgmChas1Fr02"
    msg_id = 294
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.06
    msg_length = 8
    tx_node = "BGM"
    rx_nodes = ['ECM']

    class CstRgnModSet:
        sig_name = "CstRgnModSet"
        sig_start_bit = 0
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
        startbit = 0
        byte = 0
        mask = 0b00000001
        unmask = 0b11111110
        shift = 0

    class TqModReq:
        sig_name = "TqModReq"
        sig_start_bit = 7
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvModReqType1_Undefd': 0, 'DrvModReqType1_ECO': 1, 'DrvModReqType1_Comfort_Normal': 2, 'DrvModReqType1_Dynamic_Sport': 3, 'DrvModReqType1_Reserved': 8, 'DrvModReqType1_Offroad_CrossTerrain': 5, 'DrvModReqType1_Adaptive': 6, 'DrvModReqType1_Race': 7, 'DrvModReqType1_ECO_PLUS': 9, 'DrvModReqType1_Power': 10, 'DrvModReqType1_Snow': 11, 'DrvModReqType1_Sand': 12, 'DrvModReqType1_Mud': 13, 'DrvModReqType1_Rock': 14, 'DrvModReqType1_Err': 15}
        compute_method = None
        length = 4
        startbit = 7
        byte = 0
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class CrpModSet:
        sig_name = "CrpModSet"
        sig_start_bit = 2
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
        startbit = 2
        byte = 0
        mask = 0b00000100
        unmask = 0b11111011
        shift = 2


class VddmChas1Fr30:
    msg_name = "VddmChas1Fr30"
    msg_id = 592
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['PSCM1', 'SAS']

    class VehCfgPrmCCPBytePosn7:
        sig_name = "VehCfgPrmCCPBytePosn7"
        sig_start_bit = 55
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

    class VehCfgPrmCCPBytePosn3:
        sig_name = "VehCfgPrmCCPBytePosn3"
        sig_start_bit = 23
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

    class VehCfgPrmCCPBytePosn5:
        sig_name = "VehCfgPrmCCPBytePosn5"
        sig_start_bit = 39
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

    class VehCfgPrmCCPBytePosn8:
        sig_name = "VehCfgPrmCCPBytePosn8"
        sig_start_bit = 63
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

    class VehCfgPrmBlkIDBytePosn1:
        sig_name = "VehCfgPrmBlkIDBytePosn1"
        sig_start_bit = 7
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


class VddmChas1Fr49:
    msg_name = "VddmChas1Fr49"
    msg_id = 864
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.08
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1', 'SAS']

    class HvacHeatrInletTempReqEvaprTQf_1_CEMBackBoneSignalIpdu21:
        sig_name = "HvacHeatrInletTempReqEvaprTQf_1_CEMBackBoneSignalIpdu21"
        sig_start_bit = 38
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
        startbit = 38
        byte = 4
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class HvacHeatrInletTempReqEvaprTFrnt_1_CEMBackBoneSignalIpdu21:
        sig_name = "HvacHeatrInletTempReqEvaprTFrnt_1_CEMBackBoneSignalIpdu21"
        sig_start_bit = 37
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
        startbit = 37
        bmuws_info = [(4, 0b00111111, 0b11000000, 6, 0), (5, 0b11111110, 0b00000001, 7, 1)]

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


class EcmChas1Fr17:
    msg_name = "EcmChas1Fr17"
    msg_id = 1039
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.3
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class EctvCmdVlvMovEna_0_EcmChas1SignalIPdu17:
        sig_name = "EctvCmdVlvMovEna_0_EcmChas1SignalIPdu17"
        sig_start_bit = 7
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'MoveDisable': 0, 'MoveEnable': 1}
        compute_method = None
        length = 1
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class EctvCmdVlvPosSetReq_0_EcmChas1SignalIPdu17:
        sig_name = "EctvCmdVlvPosSetReq_0_EcmChas1SignalIPdu17"
        sig_start_bit = 4
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 21
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvPosSetReq_MovetofullClosePosition': 0, 'VlvPosSetReq_MovetoLevel1OpenPosition': 1, 'VlvPosSetReq_MovetoLevel2OpenPosition': 2, 'VlvPosSetReq_MovetoLevel3OpenPosition': 3, 'VlvPosSetReq_MovetoLevel4OpenPosition': 4, 'VlvPosSetReq_MovetoLevel5OpenPosition': 5, 'VlvPosSetReq_MovetoLevel6OpenPosition': 6, 'VlvPosSetReq_MovetoLevel7OpenPosition': 7, 'VlvPosSetReq_MovetoLevel8OpenPosition': 8, 'VlvPosSetReq_MovetoLevel9OpenPosition': 9, 'VlvPosSetReq_MovetoLevel10OpenPosition': 10, 'VlvPosSetReq_MovetoLevel11OpenPosition': 11, 'VlvPosSetReq_MovetoLevel12OpenPosition': 12, 'VlvPosSetReq_MovetoLevel13OpenPosition': 13, 'VlvPosSetReq_MovetoLevel14OpenPosition': 14, 'VlvPosSetReq_MovetoLevel15OpenPosition': 15, 'VlvPosSetReq_MovetoLevel16OpenPosition': 16, 'VlvPosSetReq_MovetoLevel17OpenPosition': 17, 'VlvPosSetReq_MovetoLevel18OpenPosition': 18, 'VlvPosSetReq_MovetoLevel19OpenPosition': 19, 'VlvPosSetReq_MovetofullOpenPosition': 20, 'VlvPosSetReq_Reserved': 21}
        compute_method = None
        length = 5
        startbit = 4
        byte = 0
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0

    class EctvCmdVlvSpdLvlReq_0_EcmChas1SignalIPdu17:
        sig_name = "EctvCmdVlvSpdLvlReq_0_EcmChas1SignalIPdu17"
        sig_start_bit = 6
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvSpdLvlReq_Invalid': 0, 'VlvSpdLvlReq_Level1': 1, 'VlvSpdLvlReq_Level2': 2, 'VlvSpdLvlReq_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 6
        byte = 0
        mask = 0b01100000
        unmask = 0b10011111
        shift = 5


class VddmChas1Fr46:
    msg_name = "VddmChas1Fr46"
    msg_id = 1099
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.17
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1']

    class WhlRotToothCntrReRi:
        sig_name = "WhlRotToothCntrReRi"
        sig_start_bit = 63
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

    class AmbTEstimdQf:
        sig_name = "AmbTEstimdQf"
        sig_start_bit = 3
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
        startbit = 3
        byte = 0
        mask = 0b00001000
        unmask = 0b11110111
        shift = 3

    class WhlRotToothCntrCntr:
        sig_name = "WhlRotToothCntrCntr"
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

    class HvacHeatgReq_1_CEMBackBoneSignalIpdu21:
        sig_name = "HvacHeatgReq_1_CEMBackBoneSignalIpdu21"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class WhlRotToothCntrFrntLe:
        sig_name = "WhlRotToothCntrFrntLe"
        sig_start_bit = 39
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

    class WhlRotToothCntrFrntRi:
        sig_name = "WhlRotToothCntrFrntRi"
        sig_start_bit = 47
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

    class BrkTracCtrlActv_0_BcmVddmBackBoneSignalIPdu08:
        sig_name = "BrkTracCtrlActv_0_BcmVddmBackBoneSignalIPdu08"
        sig_start_bit = 20
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
        startbit = 20
        byte = 2
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class WhlRotToothCntrChks:
        sig_name = "WhlRotToothCntrChks"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class AmbTEstimdAmbTEstimd:
        sig_name = "AmbTEstimdAmbTEstimd"
        sig_start_bit = 2
        sig_length = 11
        sig_value_factor = 0.1
        sig_value_offset = "-70.0"
        sig_value_min = 0
        sig_value_max = 2047
        sig_byteorder = "Motorola"
        sig_value_init = 700
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 11
        startbit = 2
        bmuws_info = [(0, 0b00000111, 0b11111000, 3, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class WhlRotToothCntrReLe:
        sig_name = "WhlRotToothCntrReLe"
        sig_start_bit = 55
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


class EcmChas1Fr40:
    msg_name = "EcmChas1Fr40"
    msg_id = 820
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.26
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class SlopReducEngCoeffSlopEqu4:
        sig_name = "SlopReducEngCoeffSlopEqu4"
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

    class DstEstimdToEmptyForDrvgElecPred:
        sig_name = "DstEstimdToEmptyForDrvgElecPred"
        sig_start_bit = 45
        sig_length = 10
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = None
        sig_value_max = None
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "IDENTICAL"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 45
        bmuws_info = [(5, 0b00111111, 0b11000000, 6, 0), (6, 0b11110000, 0b00001111, 4, 4)]

    class SlopReducEngCoeffSlopEqu9:
        sig_name = "SlopReducEngCoeffSlopEqu9"
        sig_start_bit = 31
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
        startbit = 31
        byte = 3
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SlopReducEngCoeffSlopEqu12:
        sig_name = "SlopReducEngCoeffSlopEqu12"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SlopReducEngCoeffSlopEqu6:
        sig_name = "SlopReducEngCoeffSlopEqu6"
        sig_start_bit = 23
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
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class SlopReducEngCoeffSlopEqu2:
        sig_name = "SlopReducEngCoeffSlopEqu2"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0


class VddmToPscm1Chas1DiagReqFrame:
    msg_name = "VddmToPscm1Chas1DiagReqFrame"
    msg_id = 1904
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['PSCM1']


class SasToVddmChas1DiagRespFrame:
    msg_name = "SasToVddmChas1DiagRespFrame"
    msg_id = 1650
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "SAS"
    rx_nodes = ['VDDM']


class EcmChas1Fr23:
    msg_name = "EcmChas1Fr23"
    msg_id = 576
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.8
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class HvBattPmpPwrCns:
        sig_name = "HvBattPmpPwrCns"
        sig_start_bit = 3
        sig_length = 12
        sig_value_factor = 1.0
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 4095
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 12
        startbit = 3
        bmuws_info = [(0, 0b00001111, 0b11110000, 4, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class HeatrPmpUAct:
        sig_name = "HeatrPmpUAct"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class HeatrPmpSpdAct:
        sig_name = "HeatrPmpSpdAct"
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

    class HeatrPmpSpdReq:
        sig_name = "HeatrPmpSpdReq"
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


class EcmChas1Fr26:
    msg_name = "EcmChas1Fr26"
    msg_id = 543
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.04
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['VDDM']

    class EctvStatVlvSpdLvl_1_EcmChas1SignalIPdu26:
        sig_name = "EctvStatVlvSpdLvl_1_EcmChas1SignalIPdu26"
        sig_start_bit = 1
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvSpdLvl_Invalid': 0, 'VlvSpdLvl_Level1': 1, 'VlvSpdLvl_Level2': 2, 'VlvSpdLvl_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 1
        byte = 0
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class EctvStatVlvTempSts_1_EcmChas1SignalIPdu26:
        sig_name = "EctvStatVlvTempSts_1_EcmChas1SignalIPdu26"
        sig_start_bit = 3
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvTempSts_TemperaureOK': 0, 'VlvTempSts_OverTemperatureWarning': 1, 'VlvTempSts_Reserved1': 2, 'VlvTempSts_Reserved2': 3}
        compute_method = None
        length = 2
        startbit = 3
        byte = 0
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class EctvStatVoltSts_1_EcmChas1SignalIPdu26:
        sig_name = "EctvStatVoltSts_1_EcmChas1SignalIPdu26"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VoltSts_VoltageOK': 0, 'VoltSts_OverVoltage': 1, 'VoltSts_UnderVoltage': 2, 'VoltSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class EctvStatVlvRunSts_1_EcmChas1SignalIPdu26:
        sig_name = "EctvStatVlvRunSts_1_EcmChas1SignalIPdu26"
        sig_start_bit = 6
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvRunSts_NotMoving': 0, 'VlvRunSts_Moving': 1}
        compute_method = None
        length = 1
        startbit = 6
        byte = 0
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class EctvStatVlvFaultSts_1_EcmChas1SignalIPdu26:
        sig_name = "EctvStatVlvFaultSts_1_EcmChas1SignalIPdu26"
        sig_start_bit = 15
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvFaultSts_NoFault': 0, 'VlvFaultSts_MotorCoilShort': 1, 'VlvFaultSts_MotorCoilOpen': 2, 'VlvFaultSts_OverTemperatureShutdown': 3, 'VlvFaultSts_FaultStateIndeterminate': 4, 'VlvFaultSts_Reserved': 5}
        compute_method = None
        length = 3
        startbit = 15
        byte = 1
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class GearMov:
        sig_name = "GearMov"
        sig_start_bit = 23
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 2
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoYesUnknown_No': 0, 'NoYesUnknown_Yes': 1, 'NoYesUnknown_Unknown': 2}
        compute_method = None
        length = 2
        startbit = 23
        byte = 2
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class EctvStatVlvPosSts_1_EcmChas1SignalIPdu26:
        sig_name = "EctvStatVlvPosSts_1_EcmChas1SignalIPdu26"
        sig_start_bit = 12
        sig_length = 5
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 22
        sig_byteorder = "Motorola"
        sig_value_init = 21
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'VlvPosSts_FullClosePosition': 0, 'VlvPosSts_Level1OpenPosition': 1, 'VlvPosSts_Level2OpenPosition': 2, 'VlvPosSts_Level3OpenPosition': 3, 'VlvPosSts_Level4OpenPosition': 4, 'VlvPosSts_Level5OpenPosition': 5, 'VlvPosSts_Level6OpenPosition': 6, 'VlvPosSts_Level7OpenPosition': 7, 'VlvPosSts_Level8OpenPosition': 8, 'VlvPosSts_Level9OpenPosition': 9, 'VlvPosSts_Level10OpenPosition': 10, 'VlvPosSts_Level11OpenPosition': 11, 'VlvPosSts_Level12OpenPosition': 12, 'VlvPosSts_Level13OpenPosition': 13, 'VlvPosSts_Level14OpenPosition': 14, 'VlvPosSts_Level15OpenPosition': 15, 'VlvPosSts_Level16OpenPosition': 16, 'VlvPosSts_Level17OpenPosition': 17, 'VlvPosSts_Level18OpenPosition': 18, 'VlvPosSts_Level19OpenPosition': 19, 'VlvPosSts_FullOpenPosition': 20, 'VlvPosSts_UnknowPosition': 21, 'VlvPosSts_Reserved': 22}
        compute_method = None
        length = 5
        startbit = 12
        byte = 1
        mask = 0b00011111
        unmask = 0b11100000
        shift = 0


class VddmChassisCAN1NmFr:
    msg_name = "VddmChassisCAN1NmFr"
    msg_id = 1313
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ACU']


class VddmChas1Fr34:
    msg_name = "VddmChas1Fr34"
    msg_id = 775
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']

    class BookStopTiAchieved:
        sig_name = "BookStopTiAchieved"
        sig_start_bit = 3
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

    class LocalBookChrgnTarVal:
        sig_name = "LocalBookChrgnTarVal"
        sig_start_bit = 17
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 17
        bmuws_info = [(2, 0b00000011, 0b11111100, 2, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class BookChrgSetReq:
        sig_name = "BookChrgSetReq"
        sig_start_bit = 4
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
        startbit = 4
        byte = 0
        mask = 0b00010000
        unmask = 0b11101111
        shift = 4

    class RemBookChrgnTarVal_0_BgmConnSignalIPdu08:
        sig_name = "RemBookChrgnTarVal_0_BgmConnSignalIPdu08"
        sig_start_bit = 1
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 1
        bmuws_info = [(0, 0b00000011, 0b11111100, 2, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class BookChrgnActvdReq:
        sig_name = "BookChrgnActvdReq"
        sig_start_bit = 5
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
        startbit = 5
        byte = 0
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5


class PscmToEtcChas1XcpFr02:
    msg_name = "PscmToEtcChas1XcpFr02"
    msg_id = 1417
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['CCM']


class VddmChas1Fr33:
    msg_name = "VddmChas1Fr33"
    msg_id = 1015
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1']

    class VehCfgPrmExtCCPBytePosn8:
        sig_name = "VehCfgPrmExtCCPBytePosn8"
        sig_start_bit = 63
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

    class VehCfgPrmExtCCPBytePosn7:
        sig_name = "VehCfgPrmExtCCPBytePosn7"
        sig_start_bit = 55
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

    class VehCfgPrmExtCCPBytePosn5:
        sig_name = "VehCfgPrmExtCCPBytePosn5"
        sig_start_bit = 39
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

    class VehCfgPrmExtCCPBytePosn4:
        sig_name = "VehCfgPrmExtCCPBytePosn4"
        sig_start_bit = 31
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

    class VehCfgPrmExtCCPBytePosn3:
        sig_name = "VehCfgPrmExtCCPBytePosn3"
        sig_start_bit = 23
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

    class VehCfgPrmExtBlkIDBytePosn1:
        sig_name = "VehCfgPrmExtBlkIDBytePosn1"
        sig_start_bit = 7
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

    class VehCfgPrmExtCCPBytePosn6:
        sig_name = "VehCfgPrmExtCCPBytePosn6"
        sig_start_bit = 47
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

    class VehCfgPrmExtCCPBytePosn2:
        sig_name = "VehCfgPrmExtCCPBytePosn2"
        sig_start_bit = 15
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


class VddmChas1Fr24:
    msg_name = "VddmChas1Fr24"
    msg_id = 137
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.02
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1']

    class WhlFastSpdSafeChks:
        sig_name = "WhlFastSpdSafeChks"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class WhlFastSpdSafeCntr:
        sig_name = "WhlFastSpdSafeCntr"
        sig_start_bit = 3
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

    class WhlFastSpdSafeQF:
        sig_name = "WhlFastSpdSafeQF"
        sig_start_bit = 5
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

    class WhlFastSpdSafeA:
        sig_name = "WhlFastSpdSafeA"
        sig_start_bit = 14
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
        startbit = 14
        bmuws_info = [(1, 0b01111111, 0b10000000, 7, 0), (2, 0b11111111, 0b00000000, 8, 0)]

    class DriftModStsDriftModDeactive_1_VgmConnSignalIPdu31:
        sig_name = "DriftModStsDriftModDeactive_1_VgmConnSignalIPdu31"
        sig_start_bit = 54
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
        startbit = 54
        byte = 6
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class DriftModStsDriftModDendReason_1_VgmConnSignalIPdu31:
        sig_name = "DriftModStsDriftModDendReason_1_VgmConnSignalIPdu31"
        sig_start_bit = 39
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

    class LVPwrSplyErrSts_0_CEMBackBoneSignalIpdu06:
        sig_name = "LVPwrSplyErrSts_0_CEMBackBoneSignalIpdu06"
        sig_start_bit = 51
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'PwrSplyErrSts_SysOk': 0, 'PwrSplyErrSts_UhiDurgDrvg': 1, 'PwrSplyErrSts_UloDurgdrvg': 2, 'PwrSplyErrSts_BattRlyFlt': 3, 'PwrSplyErrSts_BattSnsrComFlt': 4, 'PwrSplyErrSts_BattSnsrHwFlt': 5, 'PwrSplyErrSts_FltComDcDc': 6, 'PwrSplyErrSts_FltElecDcDc': 7, 'PwrSplyErrSts_FltDcDc': 8, 'PwrSplyErrSts_SupCptrHwFlt': 9, 'PwrSplyErrSts_AltFltMecl': 10, 'PwrSplyErrSts_AltFltElec': 11, 'PwrSplyErrSts_AltFltT': 12, 'PwrSplyErrSts_AltFltCom': 13, 'PwrSplyErrSts_SpprtBattFltChrgn': 14, 'PwrSplyErrSts_Spare6': 15}
        compute_method = None
        length = 4
        startbit = 51
        byte = 6
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class DriftModStsDriftModActSts_1_VgmConnSignalIPdu31:
        sig_name = "DriftModStsDriftModActSts_1_VgmConnSignalIPdu31"
        sig_start_bit = 55
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
        startbit = 55
        byte = 6
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class DriftModStsDriftModEnaSts_1_VgmConnSignalIPdu31:
        sig_name = "DriftModStsDriftModEnaSts_1_VgmConnSignalIPdu31"
        sig_start_bit = 53
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'EnaSts_ActvDi': 0, 'EnaSts_ActvEna': 1, 'EnaSts_OffDi': 2, 'EnaSts_OffEna': 3}
        compute_method = None
        length = 2
        startbit = 53
        byte = 6
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class EtcToPscmChas1XcpFr02:
    msg_name = "EtcToPscmChas1XcpFr02"
    msg_id = 1416
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "CCM"
    rx_nodes = ['PSCM1']


class VddmChas1Fr19:
    msg_name = "VddmChas1Fr19"
    msg_id = 736
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.07
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['PSCM1', 'SAS']

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

    class VehModMngtGlbSafe1PwrLvlElecSubtyp_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1PwrLvlElecSubtyp_3_AcuFLRCANFDSignalIPdu02"
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

    class VehModMngtGlbSafe1EgyLvlElecMai_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecMai_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 27
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

    class VehModMngtGlbSafe1EgyLvlElecSubtyp_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1EgyLvlElecSubtyp_3_AcuFLRCANFDSignalIPdu02"
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

    class VehModMngtGlbSafe1UsgModSts_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "VehModMngtGlbSafe1UsgModSts_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 11
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


class EcmChas1Fr08:
    msg_name = "EcmChas1Fr08"
    msg_id = 1111
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.05
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['PSCM1']

    class PtTqAtWhlFrntActPtTqAtWhlFrntLeAct_0_EcmChas1SignalIPdu08:
        sig_name = "PtTqAtWhlFrntActPtTqAtWhlFrntLeAct_0_EcmChas1SignalIPdu08"
        sig_start_bit = 39
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
        startbit = 39
        bmuws_info = [(4, 0b11111111, 0b00000000, 8, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtWhlFrntActPtTqAtAxleFrntAct_0_EcmChas1SignalIPdu08:
        sig_name = "PtTqAtWhlFrntActPtTqAtAxleFrntAct_0_EcmChas1SignalIPdu08"
        sig_start_bit = 55
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

    class PtTqAtWhlFrntActCntr_0_EcmChas1SignalIPdu08:
        sig_name = "PtTqAtWhlFrntActCntr_0_EcmChas1SignalIPdu08"
        sig_start_bit = 3
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

    class PtTqAtWhlFrntActChks_0_EcmChas1SignalIPdu08:
        sig_name = "PtTqAtWhlFrntActChks_0_EcmChas1SignalIPdu08"
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

    class PtTqAtWhlFrntActPtTqAtWhlFrntRiAct_0_EcmChas1SignalIPdu08:
        sig_name = "PtTqAtWhlFrntActPtTqAtWhlFrntRiAct_0_EcmChas1SignalIPdu08"
        sig_start_bit = 23
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
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class PtTqAtWhlFrntActPtTqAtWhlsFrntQly_0_EcmChas1SignalIPdu08:
        sig_name = "PtTqAtWhlFrntActPtTqAtWhlsFrntQly_0_EcmChas1SignalIPdu08"
        sig_start_bit = 6
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qly3_De0': 0, 'Qly3_De1': 1, 'Qly3_De2': 2, 'Qly3_De3': 3, 'Qly3_De4': 4, 'Qly3_De5': 5, 'Qly3_De6': 6, 'Qly3_De7': 7}
        compute_method = None
        length = 3
        startbit = 6
        byte = 0
        mask = 0b01110000
        unmask = 0b10001111
        shift = 4


class VddmToAllChas1DiagReqFrame:
    msg_name = "VddmToAllChas1DiagReqFrame"
    msg_id = 2047
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['PSCM1', 'SAS']


class VddmChas1Fr37:
    msg_name = "VddmChas1Fr37"
    msg_id = 823
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.165
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM']

    class FrntHvacBlowerSts_1_CEMBackBoneSignalIpdu12:
        sig_name = "FrntHvacBlowerSts_1_CEMBackBoneSignalIpdu12"
        sig_start_bit = 55
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'HvacFanSts_Off': 0, 'HvacFanSts_On': 1, 'HvacFanSts_Warning': 2, 'HvacFanSts_Error': 3}
        compute_method = None
        length = 2
        startbit = 55
        byte = 6
        mask = 0b11000000
        unmask = 0b00111111
        shift = 6

    class HeatrAirTReq_1_CEMBackBoneSignalIpdu16:
        sig_name = "HeatrAirTReq_1_CEMBackBoneSignalIpdu16"
        sig_start_bit = 48
        sig_length = 9
        sig_value_factor = 0.5
        sig_value_offset = "-60.0"
        sig_value_min = 0
        sig_value_max = 511
        sig_byteorder = "Motorola"
        sig_value_init = 120
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 9
        startbit = 48
        bmuws_info = [(6, 0b00000001, 0b11111110, 1, 0), (7, 0b11111111, 0b00000000, 8, 0)]

    class CarTiIntForClima_1_CemBackBoneSignalIPdu15:
        sig_name = "CarTiIntForClima_1_CemBackBoneSignalIPdu15"
        sig_start_bit = 4
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
        startbit = 4
        bmuws_info = [(0, 0b00011111, 0b11100000, 5, 0), (1, 0b11111111, 0b00000000, 8, 0), (2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0), (4, 0b11100000, 0b00011111, 3, 5)]

    class ClimaCmptSts_1_CEMBackBoneSignalIpdu07:
        sig_name = "ClimaCmptSts_1_CEMBackBoneSignalIpdu07"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class ClimaDefrstSts_1_CEMBackBoneSignalIpdu07:
        sig_name = "ClimaDefrstSts_1_CEMBackBoneSignalIpdu07"
        sig_start_bit = 33
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
        startbit = 33
        byte = 4
        mask = 0b00000010
        unmask = 0b11111101
        shift = 1


class VddmChas1DevFr02:
    msg_name = "VddmChas1DevFr02"
    msg_id = 1435
    msg_type = "can"
    msg_tx_method = "spontaneous"
    msg_cycle = None
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['CCM']

    class VDDMdevelpsignalgroupresp2Functiondevpsignalgroup5:
        sig_name = "VDDMdevelpsignalgroupresp2Functiondevpsignalgroup5"
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

    class VDDMdevelpsignalgroupresp2Functiondevpsignalgroup1:
        sig_name = "VDDMdevelpsignalgroupresp2Functiondevpsignalgroup1"
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

    class VDDMdevelpsignalgroupresp2Functiondevpsignalgroup4:
        sig_name = "VDDMdevelpsignalgroupresp2Functiondevpsignalgroup4"
        sig_start_bit = 31
        sig_length = 8
        sig_value_factor = None
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

    class VDDMdevelpsignalgroupresp2Functiondevpsignalgroup7:
        sig_name = "VDDMdevelpsignalgroupresp2Functiondevpsignalgroup7"
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

    class VDDMdevelpsignalgroupresp2Functiondevpsignalgroup8:
        sig_name = "VDDMdevelpsignalgroupresp2Functiondevpsignalgroup8"
        sig_start_bit = 63
        sig_length = 8
        sig_value_factor = None
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

    class VDDMdevelpsignalgroupresp2Functiondevpsignalgroup6:
        sig_name = "VDDMdevelpsignalgroupresp2Functiondevpsignalgroup6"
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

    class VDDMdevelpsignalgroupresp2Functiondevpsignalgroup3:
        sig_name = "VDDMdevelpsignalgroupresp2Functiondevpsignalgroup3"
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

    class VDDMdevelpsignalgroupresp2Functiondevpsignalgroup2:
        sig_name = "VDDMdevelpsignalgroupresp2Functiondevpsignalgroup2"
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


class PscmChas1Fr01:
    msg_name = "PscmChas1Fr01"
    msg_id = 246
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.01
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['ACU', 'VDDM']

    class DrvrSteerActvDrvrSteerActv:
        sig_name = "DrvrSteerActvDrvrSteerActv"
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

    class ADL3LatCtrlStsCtrlSts:
        sig_name = "ADL3LatCtrlStsCtrlSts"
        sig_start_bit = 22
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Primary': 0, 'Secondary': 1}
        compute_method = None
        length = 1
        startbit = 22
        byte = 2
        mask = 0b01000000
        unmask = 0b10111111
        shift = 6

    class ADL3LatCtrlStsChks:
        sig_name = "ADL3LatCtrlStsChks"
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

    class UBoostReqBySteerFrnt:
        sig_name = "UBoostReqBySteerFrnt"
        sig_start_bit = 59
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ReqStsSteer_NoReq': 0, 'ReqStsSteer_ParkReq': 1, 'ReqStsSteer_EvasiveReq': 2, 'ReqStsSteer_Spare01': 3}
        compute_method = None
        length = 2
        startbit = 59
        byte = 7
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADL3LatCtrlStsDegraded:
        sig_name = "ADL3LatCtrlStsDegraded"
        sig_start_bit = 31
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 11
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'LatDegrad_NoDegradation_Green': 0, 'LatDegrad_Red_fault1': 1, 'LatDegrad_Yellow_fault2': 2, 'LatDegrad_Yellow_fault3': 3, 'LatDegrad_Yellow_fault4': 4, 'LatDegrad_Yellow_fault5': 5, 'LatDegrad_Yellow_fault6': 6, 'LatDegrad_Yellow_fault7': 7, 'LatDegrad_Yellow_fault8': 8, 'LatDegrad_Yellow_fault9': 9, 'LatDegrad_Yellow_fault10': 10, 'LatDegrad_Reserved1': 11}
        compute_method = None
        length = 4
        startbit = 31
        byte = 3
        mask = 0b11110000
        unmask = 0b00001111
        shift = 4

    class FrntSteerFEstimd1:
        sig_name = "FrntSteerFEstimd1"
        sig_start_bit = 47
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
        startbit = 47
        bmuws_info = [(5, 0b11111111, 0b00000000, 8, 0), (6, 0b11111111, 0b00000000, 8, 0)]

    class DrvrSteerActvChks:
        sig_name = "DrvrSteerActvChks"
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

    class ADL3LatCtrlStsCntr:
        sig_name = "ADL3LatCtrlStsCntr"
        sig_start_bit = 27
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

    class DrvrSteerActvCntr:
        sig_name = "DrvrSteerActvCntr"
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

    class ADL3LatCtrlStsADMod:
        sig_name = "ADL3LatCtrlStsADMod"
        sig_start_bit = 17
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ADMod_NAD_Mod': 0, 'ADMod_MarsParking': 1, 'ADMod_ANP': 2, 'ADMod_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 17
        byte = 2
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class ADL3LatCtrlStsQf:
        sig_name = "ADL3LatCtrlStsQf"
        sig_start_bit = 19
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
        startbit = 19
        byte = 2
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2

    class ADL3LatCtrlStsSts:
        sig_name = "ADL3LatCtrlStsSts"
        sig_start_bit = 21
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ColorSts_Red': 0, 'ColorSts_Yellow': 1, 'ColorSts_Green': 2, 'ColorSts_Reserved': 3}
        compute_method = None
        length = 2
        startbit = 21
        byte = 2
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4


class EcmChas1Fr09:
    msg_name = "EcmChas1Fr09"
    msg_id = 708
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.13
    msg_length = 8
    tx_node = "ECM"
    rx_nodes = ['ACU', 'BGM', 'VDDM']

    class GearShiftUnitSts:
        sig_name = "GearShiftUnitSts"
        sig_start_bit = 47
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
        startbit = 47
        byte = 5
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class CrpModAct:
        sig_name = "CrpModAct"
        sig_start_bit = 7
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
        startbit = 7
        byte = 0
        mask = 0b10000000
        unmask = 0b01111111
        shift = 7

    class PtVehSpdMaxReq:
        sig_name = "PtVehSpdMaxReq"
        sig_start_bit = 23
        sig_length = 8
        sig_value_factor = 0.4
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 255
        sig_byteorder = "Motorola"
        sig_value_init = 250
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 8
        startbit = 23
        byte = 2
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class GearLvrFaultIndcn:
        sig_name = "GearLvrFaultIndcn"
        sig_start_bit = 31
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 5
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'NoFlt': 0, 'CDCFltEGSMNoFlt': 1, 'CDCSerFltEGSMSligtFlt': 2, 'CDCNoFltEGSMFlt': 3, 'CDCSligtFltEGSMSerFlt': 4, 'CDCSerFltEGSMSerFlt': 5}
        compute_method = None
        length = 3
        startbit = 31
        byte = 3
        mask = 0b11100000
        unmask = 0b00011111
        shift = 5

    class GearLvrLockIndcn:
        sig_name = "GearLvrLockIndcn"
        sig_start_bit = 43
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 4
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'GearLvrLockIndcn_NoIndcn': 0, 'GearLvrLockIndcn_GearShiftSrvRqrd': 1, 'GearLvrLockIndcn_GearLvrSpdLimExc': 2, 'GearLvrLockIndcn_GearLvrRelsByBrkPedl': 3, 'GearLvrLockIndcn_GearLvrRelsByChgBatt': 4}
        compute_method = None
        length = 4
        startbit = 43
        byte = 5
        mask = 0b00001111
        unmask = 0b11110000
        shift = 0

    class PtVehSpdMaxChks:
        sig_name = "PtVehSpdMaxChks"
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

    class WtrPmpAuxReq:
        sig_name = "WtrPmpAuxReq"
        sig_start_bit = 62
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
        startbit = 62
        byte = 7
        mask = 0b01111111
        unmask = 0b10000000
        shift = 0

    class FanPwmReq:
        sig_name = "FanPwmReq"
        sig_start_bit = 25
        sig_length = 10
        sig_value_factor = 0.1
        sig_value_offset = 0.0
        sig_value_min = 0
        sig_value_max = 1000
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 10
        startbit = 25
        bmuws_info = [(3, 0b00000011, 0b11111100, 2, 0), (4, 0b11111111, 0b00000000, 8, 0)]

    class PtVehSpdMaxCntr:
        sig_name = "PtVehSpdMaxCntr"
        sig_start_bit = 3
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


class VddmChas1Fr41:
    msg_name = "VddmChas1Fr41"
    msg_id = 686
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.12
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1']

    class HvacHexAirTHvacAirTForHeatrFrntQf_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacHexAirTHvacAirTForHeatrFrntQf_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 37
        sig_length = 1
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 1
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'OkNotOk_NotOk': 0, 'OkNotOk_Ok': 1}
        compute_method = None
        length = 1
        startbit = 37
        byte = 4
        mask = 0b00100000
        unmask = 0b11011111
        shift = 5

    class ULoWarnCntr:
        sig_name = "ULoWarnCntr"
        sig_start_bit = 3
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

    class HvacHexAirTHvacAirTForHeatrFrnt_1_CEMBackBoneSignalIpdu20:
        sig_name = "HvacHexAirTHvacAirTForHeatrFrnt_1_CEMBackBoneSignalIpdu20"
        sig_start_bit = 36
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
        startbit = 36
        bmuws_info = [(4, 0b00011111, 0b11100000, 5, 0), (5, 0b11111111, 0b00000000, 8, 0)]

    class ULoWarnULoWarn:
        sig_name = "ULoWarnULoWarn"
        sig_start_bit = 5
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 2
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'ULoWarn_UOk': 0, 'ULoWarn_ULoTmp': 1, 'ULoWarn_ULoPrmnt': 2}
        compute_method = None
        length = 2
        startbit = 5
        byte = 0
        mask = 0b00110000
        unmask = 0b11001111
        shift = 4

    class ULoWarnChks:
        sig_name = "ULoWarnChks"
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

    class DrvModReq_1_VddmChas1SignalIPdu41:
        sig_name = "DrvModReq_1_VddmChas1SignalIPdu41"
        sig_start_bit = 61
        sig_length = 4
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 15
        sig_byteorder = "Motorola"
        sig_value_init = 3
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'DrvModReqType1_Undefd': 0, 'DrvModReqType1_ECO': 1, 'DrvModReqType1_Comfort_Normal': 2, 'DrvModReqType1_Dynamic_Sport': 3, 'DrvModReqType1_Reserved': 8, 'DrvModReqType1_Offroad_CrossTerrain': 5, 'DrvModReqType1_Adaptive': 6, 'DrvModReqType1_Race': 7, 'DrvModReqType1_ECO_PLUS': 9, 'DrvModReqType1_Power': 10, 'DrvModReqType1_Snow': 11, 'DrvModReqType1_Sand': 12, 'DrvModReqType1_Mud': 13, 'DrvModReqType1_Rock': 14, 'DrvModReqType1_Err': 15}
        compute_method = None
        length = 4
        startbit = 61
        byte = 7
        mask = 0b00111100
        unmask = 0b11000011
        shift = 2


class VddmChas1Fr14:
    msg_name = "VddmChas1Fr14"
    msg_id = 432
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.03
    msg_length = 8
    tx_node = "VDDM"
    rx_nodes = ['ECM', 'PSCM1']

    class AgDataRawSafeRollRate_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "AgDataRawSafeRollRate_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 7
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 7
        bmuws_info = [(0, 0b11111111, 0b00000000, 8, 0), (1, 0b11111111, 0b00000000, 8, 0)]

    class RemHvStrtActvReq_0_TcamConnectivitySignalIPdu12:
        sig_name = "RemHvStrtActvReq_0_TcamConnectivitySignalIPdu12"
        sig_start_bit = 52
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
        startbit = 52
        byte = 6
        mask = 0b00011000
        unmask = 0b11100111
        shift = 3

    class AgDataRawSafeChks_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "AgDataRawSafeChks_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 39
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
        startbit = 39
        byte = 4
        mask = 0b11111111
        unmask = 0b00000000
        shift = 0

    class AgDataRawSafeYawRateQf_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "AgDataRawSafeYawRateQf_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 41
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 41
        byte = 5
        mask = 0b00000011
        unmask = 0b11111100
        shift = 0

    class AgDataRawSafeYawRate_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "AgDataRawSafeYawRate_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 23
        sig_length = 16
        sig_value_factor = "2.44140625E-4"
        sig_value_offset = 0.0
        sig_value_min = -24576
        sig_value_max = 24576
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "LINEAR"
        sig_value_table = None
        compute_method = None
        length = 16
        startbit = 23
        bmuws_info = [(2, 0b11111111, 0b00000000, 8, 0), (3, 0b11111111, 0b00000000, 8, 0)]

    class AgDataRawSafeCntr_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "AgDataRawSafeCntr_3_AcuFLRCANFDSignalIPdu02"
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

    class AgDataRawSafeRollRateQf_3_AcuFLRCANFDSignalIPdu02:
        sig_name = "AgDataRawSafeRollRateQf_3_AcuFLRCANFDSignalIPdu02"
        sig_start_bit = 43
        sig_length = 2
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 3
        sig_byteorder = "Motorola"
        sig_value_init = 1
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'Qf1_DevOfDataUndefd': 0, 'Qf1_DataTmpUndefdAndEvlnInProgs': 1, 'Qf1_DevOfDataNotWithinRngAllwd': 2, 'Qf1_DataCalcdWithDevDefd': 3}
        compute_method = None
        length = 2
        startbit = 43
        byte = 5
        mask = 0b00001100
        unmask = 0b11110011
        shift = 2


class PscmChas1Fr06:
    msg_name = "PscmChas1Fr06"
    msg_id = 955
    msg_type = "can"
    msg_tx_method = "cyclic"
    msg_cycle = 0.4
    msg_length = 8
    tx_node = "PSCM1"
    rx_nodes = ['VDDM', 'BGM']

    class SteerAsscLvlCfmd:
        sig_name = "SteerAsscLvlCfmd"
        sig_start_bit = 20
        sig_length = 3
        sig_value_factor = None
        sig_value_offset = None
        sig_value_min = 0
        sig_value_max = 7
        sig_byteorder = "Motorola"
        sig_value_init = 0
        sig_value_type = "TEXTTABLE"
        sig_value_table = {'SteerAsscLvl_Ukwn': 0, 'SteerAsscLvl_Lvl1': 1, 'SteerAsscLvl_Lvl2': 2, 'SteerAsscLvl_Lvl3': 3, 'SteerAsscLvl_Lvl4': 4, 'SteerAsscLvl_Resd5': 5, 'SteerAsscLvl_Resd6': 6, 'SteerAsscLvl_Resd7': 7}
        compute_method = None
        length = 3
        startbit = 20
        byte = 2
        mask = 0b00011100
        unmask = 0b11100011
        shift = 2

    class PinionSteerAgMax1:
        sig_name = "PinionSteerAgMax1"
        sig_start_bit = 54
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
        startbit = 54
        bmuws_info = [(6, 0b01111111, 0b10000000, 7, 0), (7, 0b11111111, 0b00000000, 8, 0)]


