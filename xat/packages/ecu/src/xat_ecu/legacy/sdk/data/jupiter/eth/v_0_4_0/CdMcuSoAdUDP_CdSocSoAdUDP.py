

class CCUMCUCDToCCUSOCCDEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204003
    pdu_length_bytes = 310
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-100ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'ActFusnSeatSts': ['ActFusnSeatStsDrvrSeatSts', 'ActFusnSeatStsThrdRowLeSeatSts', 'ActFusnSeatStsSecRowLeSeatSts', 'ActFusnSeatStsThrdRowMidSeatSts', 'ActFusnSeatStsThrdRowRiSeatSts', 'ActFusnSeatStsPassSeatSts', 'ActFusnSeatStsSecRowMidSeatSts', 'ActFusnSeatStsSecRowRiSeatSts'], 'BackLight': ['BackLightChks', 'BackLightSts', 'BackLightCntr'], 'BLEKeyPrsntSts': ['BLEKeyPrsntStsWelcomeZoneKeyPrsntSts', 'BLEKeyPrsntStsPEIntZoneKeyPrsntSts', 'BLEKeyPrsntStsDoorSideZoneKeyPrsntSts', 'BLEKeyPrsntStsWalkAwayZoneKeyPrsntSts', 'BLEKeyPrsntStsPEExtZoneKeyPrsntSts', 'BLEKeyPrsntStsConnectZoneKeyPrsntSts', 'BLEKeyPrsntStsPSZoneKeyPrsntSts', 'BLEKeyPrsntStsApproachZoneKeyPrsntSts'], 'CmptmtThermReqResp': ['CmptmtThermReqRespFrnt', 'CmptmtThermReqRespRear', 'CmptmtThermReqRespAllZone'], 'DigKeyCnctInfo1': ['DigKeyCnctInfo1PEKeyPrsntSts', 'DigKeyCnctInfo1KeyIdByte9', 'DigKeyCnctInfo1KeyIdByte11', 'DigKeyCnctInfo1KeyTyp', 'DigKeyCnctInfo1KeyIdByte15', 'DigKeyCnctInfo1PSEnaSts', 'DigKeyCnctInfo1KeyConnectInfo', 'DigKeyCnctInfo1KeyIdByte0', 'DigKeyCnctInfo1KeyIdByte6', 'DigKeyCnctInfo1KeyIdByte5', 'DigKeyCnctInfo1KeyIdByte7', 'DigKeyCnctInfo1AutoLockOnLeaveSetting', 'DigKeyCnctInfo1KeyIdByte1', 'DigKeyCnctInfo1KeyIdByte4', 'DigKeyCnctInfo1AutoUnlockOnApproachSetting', 'DigKeyCnctInfo1KeyIdByte13', 'DigKeyCnctInfo1AutoZoneKeyPrsntSts', 'DigKeyCnctInfo1KeyIdByte3', 'DigKeyCnctInfo1KeyIdByte10', 'DigKeyCnctInfo1KeyIdByte2', 'DigKeyCnctInfo1BattWarn', 'DigKeyCnctInfo1KeyIdByte8', 'DigKeyCnctInfo1KeyIdByte12', 'DigKeyCnctInfo1KeyIdByte14'], 'DigKeyCnctInfo2': ['DigKeyCnctInfo2KeyIdByte0', 'DigKeyCnctInfo2KeyIdByte5', 'DigKeyCnctInfo2KeyTyp', 'DigKeyCnctInfo2KeyIdByte3', 'DigKeyCnctInfo2AutoUnlockOnApproachSetting', 'DigKeyCnctInfo2AutoLockOnLeaveSetting', 'DigKeyCnctInfo2KeyIdByte9', 'DigKeyCnctInfo2PEKeyPrsntSts', 'DigKeyCnctInfo2KeyIdByte13', 'DigKeyCnctInfo2KeyIdByte15', 'DigKeyCnctInfo2KeyConnectInfo', 'DigKeyCnctInfo2KeyIdByte14', 'DigKeyCnctInfo2KeyIdByte6', 'DigKeyCnctInfo2KeyIdByte10', 'DigKeyCnctInfo2KeyIdByte11', 'DigKeyCnctInfo2KeyIdByte4', 'DigKeyCnctInfo2KeyIdByte7', 'DigKeyCnctInfo2KeyIdByte8', 'DigKeyCnctInfo2KeyIdByte12', 'DigKeyCnctInfo2AutoZoneKeyPrsntSts', 'DigKeyCnctInfo2KeyIdByte1', 'DigKeyCnctInfo2BattWarn', 'DigKeyCnctInfo2KeyIdByte2', 'DigKeyCnctInfo2PSEnaSts'], 'DigKeyCnctInfo3': ['DigKeyCnctInfo3KeyIdByte1', 'DigKeyCnctInfo3KeyIdByte8', 'DigKeyCnctInfo3KeyIdByte10', 'DigKeyCnctInfo3KeyIdByte11', 'DigKeyCnctInfo3KeyIdByte9', 'DigKeyCnctInfo3PSEnaSts', 'DigKeyCnctInfo3KeyIdByte3', 'DigKeyCnctInfo3KeyIdByte7', 'DigKeyCnctInfo3AutoLockOnLeaveSetting', 'DigKeyCnctInfo3KeyIdByte5', 'DigKeyCnctInfo3KeyIdByte2', 'DigKeyCnctInfo3KeyIdByte15', 'DigKeyCnctInfo3KeyIdByte6', 'DigKeyCnctInfo3KeyConnectInfo', 'DigKeyCnctInfo3KeyIdByte4', 'DigKeyCnctInfo3AutoZoneKeyPrsntSts', 'DigKeyCnctInfo3KeyIdByte12', 'DigKeyCnctInfo3PEKeyPrsntSts', 'DigKeyCnctInfo3BattWarn', 'DigKeyCnctInfo3KeyIdByte13', 'DigKeyCnctInfo3KeyTyp', 'DigKeyCnctInfo3KeyIdByte0', 'DigKeyCnctInfo3KeyIdByte14', 'DigKeyCnctInfo3AutoUnlockOnApproachSetting'], 'DigKeyCnctInfo4': ['DigKeyCnctInfo4KeyIdByte0', 'DigKeyCnctInfo4KeyIdByte14', 'DigKeyCnctInfo4KeyIdByte1', 'DigKeyCnctInfo4KeyIdByte6', 'DigKeyCnctInfo4KeyIdByte10', 'DigKeyCnctInfo4KeyIdByte15', 'DigKeyCnctInfo4BattWarn', 'DigKeyCnctInfo4KeyIdByte4', 'DigKeyCnctInfo4KeyTyp', 'DigKeyCnctInfo4KeyIdByte9', 'DigKeyCnctInfo4KeyIdByte2', 'DigKeyCnctInfo4KeyIdByte12', 'DigKeyCnctInfo4AutoLockOnLeaveSetting', 'DigKeyCnctInfo4KeyIdByte13', 'DigKeyCnctInfo4KeyIdByte7', 'DigKeyCnctInfo4PSEnaSts', 'DigKeyCnctInfo4PEKeyPrsntSts', 'DigKeyCnctInfo4KeyIdByte8', 'DigKeyCnctInfo4KeyIdByte3', 'DigKeyCnctInfo4KeyIdByte5', 'DigKeyCnctInfo4AutoZoneKeyPrsntSts', 'DigKeyCnctInfo4AutoUnlockOnApproachSetting', 'DigKeyCnctInfo4KeyConnectInfo', 'DigKeyCnctInfo4KeyIdByte11'], 'FrntMotInfo': ['FrntMotInfoDTCHig', 'FrntMotInfoEMSeqNr', 'FrntMotInfoPasDchaAlrmSt', 'FrntMotInfoPlsHeatAlrmSt', 'FrntMotInfoUDCAlrmSt', 'FrntMotInfoActvHeatgAlrmSt', 'FrntMotInfoDTCLow', 'FrntMotInfoModStRms', 'FrntMotInfoFltAlrmSt', 'FrntMotInfoBoostAlrmSt', 'FrntMotInfoTqAlrmSt', 'FrntMotInfoRatTypeInfo', 'FrntMotInfoIPhaAlrmSt', 'FrntMotInfoOilTAlrmSt', 'FrntMotInfoEMQnty', 'FrntMotInfoRslAlrmSt', 'FrntMotInfoActvDchaAlrmSt', 'FrntMotInfoInvrtTAlrmSt', 'FrntMotInfoDTCLMid', 'FrntMotInfoMotTAlrmSt', 'FrntMotInfoOverSpdAlrmSt', 'FrntMotInfoDTCSts'], 'FrontLeftTyreAlarmInfo': ['FrontLeftTyreAlarmInfoTWarnFlag', 'FrontLeftTyreAlarmInfoFastLoseWarnFlag', 'FrontLeftTyreAlarmInfoBattLowWarnFlag', 'FrontLeftTyreAlarmInfoPWarnFlag', 'FrontLeftTyreAlarmInfoSysWarnFlag'], 'FrontLeftTyreData': ['FrontLeftTyreDataTyreTemperature', 'FrontLeftTyreDataTyrePressure'], 'FrontRightTyreAlarmInfo': ['FrontRightTyreAlarmInfoBattLowWarnFlag', 'FrontRightTyreAlarmInfoSysWarnFlag', 'FrontRightTyreAlarmInfoPWarnFlag', 'FrontRightTyreAlarmInfoTWarnFlag', 'FrontRightTyreAlarmInfoFastLoseWarnFlag'], 'FrontRightTyreData': ['FrontRightTyreDataTyrePressure', 'FrontRightTyreDataTyreTemperature'], 'HVBattThermMngtPwrAct': ['HVBattThermMngtPwrActCoolgPwr', 'HVBattThermMngtPwrActHeatgPwr'], 'HVBattThermReqActual': ['HVBattThermReqActualThermLvlReq', 'HVBattThermReqActualCooltFlwReq', 'HVBattThermReqActualThermReq', 'HVBattThermReqActualCellTTar', 'HVBattThermReqActualCooltTReq', 'HVBattThermReqActualSourceID', 'HVBattThermReqActualCellTType'], 'LocalCenLockAbnormFb': ['LocalCenLockAbnormFbNFCLockUnlckFb', 'LocalCenLockAbnormFbAproLockUnlckFb', 'LocalCenLockAbnormFbPELockUnlckFb'], 'PWTThermReqActual': ['PWTThermReqActualCooltTMaxReq', 'PWTThermReqActualCoolgReq', 'PWTThermReqActualCooltTMinReq', 'PWTThermReqActualCooltFlwReq', 'PWTThermReqActualCoolgReqLvl', 'PWTThermReqActualSourceID'], 'RearLeftTyreAlarmInfo': ['RearLeftTyreAlarmInfoTWarnFlag', 'RearLeftTyreAlarmInfoBattLowWarnFlag', 'RearLeftTyreAlarmInfoSysWarnFlag', 'RearLeftTyreAlarmInfoPWarnFlag', 'RearLeftTyreAlarmInfoFastLoseWarnFlag'], 'RearLeftTyreData': ['RearLeftTyreDataTyrePressure', 'RearLeftTyreDataTyreTemperature'], 'RearRightTyreAlarmInfo': ['RearRightTyreAlarmInfoBattLowWarnFlag', 'RearRightTyreAlarmInfoTWarnFlag', 'RearRightTyreAlarmInfoSysWarnFlag', 'RearRightTyreAlarmInfoPWarnFlag', 'RearRightTyreAlarmInfoFastLoseWarnFlag'], 'RearRightTyreData': ['RearRightTyreDataTyrePressure', 'RearRightTyreDataTyreTemperature'], 'RefrigCircTDes': ['RefrigCircTDesFrntEvapTarT', 'RefrigCircTDesFrntHexTarT', 'RefrigCircTDesRearEvapTarT', 'RefrigCircTDesRearHexTarT'], 'ReMotInfo': ['ReMotInfoMotTAlrmSt', 'ReMotInfoOilTAlrmSt', 'ReMotInfoBoostAlrmSt', 'ReMotInfoUDCAlrmSt', 'ReMotInfoRatTypeInfo', 'ReMotInfoTqAlrmSt', 'ReMotInfoDTCLMid', 'ReMotInfoDTCSts', 'ReMotInfoDTCLow', 'ReMotInfoEMQnty', 'ReMotInfoActvHeatgAlrmSt', 'ReMotInfoPlsHeatAlrmSt', 'ReMotInfoEMSeqNr', 'ReMotInfoActvDchaAlrmSt', 'ReMotInfoFltAlrmSt', 'ReMotInfoDTCHig', 'ReMotInfoInvrtTAlrmSt', 'ReMotInfoRslAlrmSt', 'ReMotInfoOverSpdAlrmSt', 'ReMotInfoPasDchaAlrmSt', 'ReMotInfoIPhaAlrmSt', 'ReMotInfoModStRms'], 'VehDateAndTi': ['VehDateAndTiSec', 'VehDateAndTiValid', 'VehDateAndTiDay', 'VehDateAndTiYr', 'VehDateAndTiHr', 'VehDateAndTiMins', 'VehDateAndTiMth']}

    class ActFusnSeatStsDrvrSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Driver Seat Occupy Status with user action"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ActFusnSeatStsThrdRowLeSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Third row Left Seat Occupy Status with user action "
        signal_length = 1
        start_position = 6
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ActFusnSeatStsSecRowLeSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Second row Left Seat Occupy Status with user action "
        signal_length = 1
        start_position = 5
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ActFusnSeatStsThrdRowMidSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Third row middle Seat Occupy Status with user action "
        signal_length = 1
        start_position = 4
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ActFusnSeatStsThrdRowRiSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Third row right Seat Occupy Status with user action "
        signal_length = 1
        start_position = 3
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ActFusnSeatStsPassSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Passanger Seat Occupy Status with user action "
        signal_length = 1
        start_position = 2
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ActFusnSeatStsSecRowMidSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Second row middle Seat Occupy Status with user action "
        signal_length = 1
        start_position = 1
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ActFusnSeatStsSecRowRiSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Second row right Seat Occupy Status with user action "
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class BackLightChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "Checks"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class BackLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "The Front Screen BackLight Chip Status"
        signal_length = 2
        start_position = 19
        value_definition = {'0x0': ' BackLightSts_Off', '0x1': ' BackLightSts_Ready', '0x2': ' BackLightSts_Fault', '0x3': ' BackLightSts_Reserved1'}

    class BackLightCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "Counter"
        signal_length = 4
        start_position = 23
        value_definition = {}

    class BLEKeyPrsntStsWelcomeZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 163
        signal_description = "Welcome light zone key present status"
        signal_length = 1
        start_position = 24
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class BLEKeyPrsntStsPEIntZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 163
        signal_description = " PE function key present status of vehicle internal zone"
        signal_length = 1
        start_position = 25
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class BLEKeyPrsntStsDoorSideZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 163
        signal_description = "Driver door outside zone key present status"
        signal_length = 1
        start_position = 31
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class BLEKeyPrsntStsWalkAwayZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 163
        signal_description = "Walk away lock zone key present status"
        signal_length = 1
        start_position = 30
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class BLEKeyPrsntStsPEExtZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 163
        signal_description = " PE function key present status of vehicle external zone"
        signal_length = 1
        start_position = 29
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class BLEKeyPrsntStsConnectZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 163
        signal_description = "key connected zone key present status"
        signal_length = 1
        start_position = 28
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class BLEKeyPrsntStsPSZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 163
        signal_description = "PS zone key present Status"
        signal_length = 1
        start_position = 27
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class BLEKeyPrsntStsApproachZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 163
        signal_description = "Approach unlock zone key present status"
        signal_length = 1
        start_position = 26
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class BoostIDCHv1:
        comments = ""
        factor = 0.1
        initial_value = 30000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -3000
        sig_ub = 162
        signal_description = "Actual current on the high voltage side"
        signal_length = 16
        start_position = 39
        value_definition = {}

    class BoostIDCLv1:
        comments = ""
        factor = 0.1
        initial_value = 30000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -3000
        sig_ub = 161
        signal_description = "Actual current on the low voltage side"
        signal_length = 16
        start_position = 55
        value_definition = {}

    class BoostLvRlySts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 160
        signal_description = "Boost relay status"
        signal_length = 3
        start_position = 71
        value_definition = {'0x0': ' BoostLvRlySts1_Default', '0x1': ' BoostLvRlySts1_Open', '0x2': ' BoostLvRlySts1_Close', '0x3': ' BoostLvRlySts1_StuckOpen', '0x4': ' BoostLvRlySts1_StuckClose', '0x5': ' BoostLvRlySts1_Undefined', '0x6': ' BoostLvRlySts1_Reserved1', '0x7': ' BoostLvRlySts1_Reserved2'}

    class BoostUDCHv1:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 799
        signal_description = "The actual voltage on the high voltage side"
        signal_length = 16
        start_position = 79
        value_definition = {}

    class BoostUDCLv1:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 798
        signal_description = "Voltage of the low-voltage side of the booster module"
        signal_length = 16
        start_position = 95
        value_definition = {}

    class BrightnessLvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 797
        signal_description = "The percent of Brightness Value reported from The Front Screen"
        signal_length = 8
        start_position = 111
        value_definition = {'0xFF': 'BattSOH_Invalid'}

    class BrkSysTemp:
        comments = ""
        factor = 4.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 796
        signal_description = "brake system temperature "
        signal_length = 8
        start_position = 119
        value_definition = {}

    class CmptmtThermMngtHVPwrCns:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 793
        signal_description = "compartment thermal management HV power consume"
        signal_length = 13
        start_position = 135
        value_definition = {}

    class CmptmtThermPwrAllwd:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 792
        signal_description = "Compartment thermal management power allowed"
        signal_length = 13
        start_position = 138
        value_definition = {}

    class CmptmtThermReqRespFrnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 807
        signal_description = "Compartment Front Area Thermal Request Response"
        signal_length = 3
        start_position = 157
        value_definition = {'0x0': ' CmptHpMode_Idle', '0x1': ' CmptHpMode_Vent', '0x2': ' CmptHpMode_Heat', '0x3': ' CmptHpMode_Cool', '0x4': ' CmptHpMode_Dehum', '0x5': ' CmptHpMode_Cool_Heat', '0x6': ' CmptHpMode_Reserve'}

    class CmptmtThermReqRespRear:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 807
        signal_description = "Compartment Rear Area Thermal Request Response"
        signal_length = 3
        start_position = 154
        value_definition = {'0x0': ' CmptHpMode_Idle', '0x1': ' CmptHpMode_Vent', '0x2': ' CmptHpMode_Heat', '0x3': ' CmptHpMode_Cool', '0x4': ' CmptHpMode_Dehum', '0x5': ' CmptHpMode_Cool_Heat', '0x6': ' CmptHpMode_Reserve'}

    class CmptmtThermReqRespAllZone:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 807
        signal_description = "Compartment OverAll Area Thermal Request Response"
        signal_length = 3
        start_position = 167
        value_definition = {'0x0': ' CmptHpMode_Idle', '0x1': ' CmptHpMode_Vent', '0x2': ' CmptHpMode_Heat', '0x3': ' CmptHpMode_Cool', '0x4': ' CmptHpMode_Dehum', '0x5': ' CmptHpMode_Cool_Heat', '0x6': ' CmptHpMode_Reserve'}

    class CnvKeepSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 806
        signal_description = "CnvModSts"
        signal_length = 8
        start_position = 1439
        value_definition = {'0x0': ' CnvKeeplevel_Nokeep', '0x1': ' CnvKeeplevel_Level1', '0x2': ' CnvKeeplevel_Level2'}

    class DCDCFltElecWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 805
        signal_description = "DCDC Electrical malfunction"
        signal_length = 2
        start_position = 1447
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class DCDCFltTWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 804
        signal_description = "DCDC Over temperature"
        signal_length = 2
        start_position = 1445
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class DcDcLimnIndcnWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 803
        signal_description = "DCDC Output fault"
        signal_length = 16
        start_position = 175
        value_definition = {}

    class DiagcExtCom:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 802
        signal_description = "Represent External Diagnostic Requirement"
        signal_length = 1
        start_position = 164
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class DigKeyCnctInfo1PEKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "PE Zone key present status"
        signal_length = 3
        start_position = 191
        value_definition = {'0x0': ' PELocnSts_Idle', '0x1': ' PELocnSts_PEAllExt', '0x2': ' PELocnSts_PEDrvrExt', '0x3': ' PELocnSts_PEPassExt', '0x4': ' PELocnSts_PEFrntExt', '0x5': ' PELocnSts_PERearExt', '0x6': ' PELocnSts_PEAllInt', '0x7': ' PELocnSts_Reserved'}

    class DigKeyCnctInfo1KeyIdByte9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte9"
        signal_length = 8
        start_position = 287
        value_definition = {}

    class DigKeyCnctInfo1KeyIdByte11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte11"
        signal_length = 8
        start_position = 303
        value_definition = {}

    class DigKeyCnctInfo1KeyTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "key type info"
        signal_length = 4
        start_position = 187
        value_definition = {'0x0': ' KeyTyp_NoKeyConnected', '0x1': ' KeyTyp_NFC_Card', '0x2': ' KeyTyp_BLE_UWB_KeyFob', '0x3': ' KeyTyp_Phone_NFC_Key', '0x4': ' KeyTyp_Phone_BLE_Key', '0x5': ' KeyTyp_Phone_UWB_Key', '0x6': ' KeyTyp_Reserved1', '0x7': ' KeyTyp_Reserved2', '0x8': ' KeyTyp_Reserved3', '0x9': ' KeyTyp_Reserved4'}

    class DigKeyCnctInfo1KeyIdByte15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte15"
        signal_length = 8
        start_position = 335
        value_definition = {}

    class DigKeyCnctInfo1PSEnaSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "PS Zone key present status"
        signal_length = 1
        start_position = 188
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class DigKeyCnctInfo1KeyConnectInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Indicate if key is connected"
        signal_length = 1
        start_position = 192
        value_definition = {'0x0': ' ConnectionSts_Disconnect', '0x1': ' ConnectionSts_Connect'}

    class DigKeyCnctInfo1KeyIdByte0:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte0"
        signal_length = 8
        start_position = 215
        value_definition = {}

    class DigKeyCnctInfo1KeyIdByte6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte6"
        signal_length = 8
        start_position = 263
        value_definition = {}

    class DigKeyCnctInfo1KeyIdByte5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte5"
        signal_length = 8
        start_position = 255
        value_definition = {}

    class DigKeyCnctInfo1KeyIdByte7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte7"
        signal_length = 8
        start_position = 271
        value_definition = {}

    class DigKeyCnctInfo1AutoLockOnLeaveSetting:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Walk away lock setting"
        signal_length = 3
        start_position = 199
        value_definition = {'0x0': ' AutoLockOnLeaveSetting_Unkown', '0x1': ' AutoLockOnLeaveSetting_Off', '0x2': ' AutoLockOnLeaveSetting_OnWithoutAnyDoorClose', '0x3': ' AutoLockOnLeaveSetting_OnWithDriverDoorClose', '0x4': ' AutoLockOnLeaveSetting_OnWithSideDoorClose', '0x5': ' AutoLockOnLeaveSetting_OnWithAllDoorClose'}

    class DigKeyCnctInfo1KeyIdByte1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte1"
        signal_length = 8
        start_position = 223
        value_definition = {}

    class DigKeyCnctInfo1KeyIdByte4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte4"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class DigKeyCnctInfo1AutoUnlockOnApproachSetting:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Approach unlock setting"
        signal_length = 3
        start_position = 196
        value_definition = {'0x0': ' ApproachUnlockSetting_Unkown', '0x1': ' ApproachUnlockSetting_Off', '0x2': ' ApproachUnlockSetting_OnWithoutDoorOpen', '0x3': ' ApproachUnlockSetting_OnWithDoorMinAngleOpen', '0x4': ' ApproachUnlockSetting_OnWithDoorFullOpen'}

    class DigKeyCnctInfo1KeyIdByte13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte13"
        signal_length = 8
        start_position = 319
        value_definition = {}

    class DigKeyCnctInfo1AutoZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Approach Zone key present status"
        signal_length = 4
        start_position = 207
        value_definition = {'0x0': ' KeyPrsntZoneInfo_NotConnected', '0x1': ' KeyPrsntZoneInfo_Connected', '0x2': ' KeyPrsntZoneInfo_Welcome', '0x3': ' KeyPrsntZoneInfo_WalkAway', '0x4': ' KeyPrsntZoneInfo_LockUnlockBuffer', '0x5': ' KeyPrsntZoneInfo_Approach', '0x6': ' KeyPrsntZoneInfo_Door', '0x7': ' KeyPrsntZoneInfo_InCar', '0x8': ' KeyPrsntZoneInfo_InFL', '0x9': ' KeyPrsntZoneInfo_InFR', '0xA': ' KeyPrsntZoneInfo_InRL', '0xB': ' KeyPrsntZoneInfo_InRR', '0xC': ' KeyPrsntZoneInfo_Tr', '0xD': ' KeyPrsntZoneInfo_Reserved1', '0xE': ' KeyPrsntZoneInfo_Reserved2', '0xF': ' KeyPrsntZoneInfo_Reserved3'}

    class DigKeyCnctInfo1KeyIdByte3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte3"
        signal_length = 8
        start_position = 239
        value_definition = {}

    class DigKeyCnctInfo1KeyIdByte10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte10"
        signal_length = 8
        start_position = 295
        value_definition = {}

    class DigKeyCnctInfo1KeyIdByte2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte2"
        signal_length = 8
        start_position = 231
        value_definition = {}

    class DigKeyCnctInfo1BattWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Indicate if the key is in low battery state"
        signal_length = 1
        start_position = 193
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class DigKeyCnctInfo1KeyIdByte8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte8"
        signal_length = 8
        start_position = 279
        value_definition = {}

    class DigKeyCnctInfo1KeyIdByte12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte12"
        signal_length = 8
        start_position = 311
        value_definition = {}

    class DigKeyCnctInfo1KeyIdByte14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 801
        signal_description = "Keyid byte14"
        signal_length = 8
        start_position = 327
        value_definition = {}

    class DigKeyCnctInfo2KeyIdByte0:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte0"
        signal_length = 8
        start_position = 367
        value_definition = {}

    class DigKeyCnctInfo2KeyIdByte5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte5"
        signal_length = 8
        start_position = 407
        value_definition = {}

    class DigKeyCnctInfo2KeyTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "key type"
        signal_length = 4
        start_position = 343
        value_definition = {'0x0': ' KeyTyp_NoKeyConnected', '0x1': ' KeyTyp_NFC_Card', '0x2': ' KeyTyp_BLE_UWB_KeyFob', '0x3': ' KeyTyp_Phone_NFC_Key', '0x4': ' KeyTyp_Phone_BLE_Key', '0x5': ' KeyTyp_Phone_UWB_Key', '0x6': ' KeyTyp_Reserved1', '0x7': ' KeyTyp_Reserved2', '0x8': ' KeyTyp_Reserved3', '0x9': ' KeyTyp_Reserved4'}

    class DigKeyCnctInfo2KeyIdByte3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte3"
        signal_length = 8
        start_position = 391
        value_definition = {}

    class DigKeyCnctInfo2AutoUnlockOnApproachSetting:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Approach unlock setting"
        signal_length = 3
        start_position = 348
        value_definition = {'0x0': ' ApproachUnlockSetting_Unkown', '0x1': ' ApproachUnlockSetting_Off', '0x2': ' ApproachUnlockSetting_OnWithoutDoorOpen', '0x3': ' ApproachUnlockSetting_OnWithDoorMinAngleOpen', '0x4': ' ApproachUnlockSetting_OnWithDoorFullOpen'}

    class DigKeyCnctInfo2AutoLockOnLeaveSetting:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Walk away lock setting"
        signal_length = 3
        start_position = 351
        value_definition = {'0x0': ' AutoLockOnLeaveSetting_Unkown', '0x1': ' AutoLockOnLeaveSetting_Off', '0x2': ' AutoLockOnLeaveSetting_OnWithoutAnyDoorClose', '0x3': ' AutoLockOnLeaveSetting_OnWithDriverDoorClose', '0x4': ' AutoLockOnLeaveSetting_OnWithSideDoorClose', '0x5': ' AutoLockOnLeaveSetting_OnWithAllDoorClose'}

    class DigKeyCnctInfo2KeyIdByte9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte9"
        signal_length = 8
        start_position = 439
        value_definition = {}

    class DigKeyCnctInfo2PEKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "PE Zone key present status"
        signal_length = 3
        start_position = 339
        value_definition = {'0x0': ' PELocnSts_Idle', '0x1': ' PELocnSts_PEAllExt', '0x2': ' PELocnSts_PEDrvrExt', '0x3': ' PELocnSts_PEPassExt', '0x4': ' PELocnSts_PEFrntExt', '0x5': ' PELocnSts_PERearExt', '0x6': ' PELocnSts_PEAllInt', '0x7': ' PELocnSts_Reserved'}

    class DigKeyCnctInfo2KeyIdByte13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte13"
        signal_length = 8
        start_position = 471
        value_definition = {}

    class DigKeyCnctInfo2KeyIdByte15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte15"
        signal_length = 8
        start_position = 487
        value_definition = {}

    class DigKeyCnctInfo2KeyConnectInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Indicate if key is connected"
        signal_length = 1
        start_position = 344
        value_definition = {'0x0': ' ConnectionSts_Disconnect', '0x1': ' ConnectionSts_Connect'}

    class DigKeyCnctInfo2KeyIdByte14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte14"
        signal_length = 8
        start_position = 479
        value_definition = {}

    class DigKeyCnctInfo2KeyIdByte6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte6"
        signal_length = 8
        start_position = 415
        value_definition = {}

    class DigKeyCnctInfo2KeyIdByte10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte10"
        signal_length = 8
        start_position = 447
        value_definition = {}

    class DigKeyCnctInfo2KeyIdByte11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte11"
        signal_length = 8
        start_position = 455
        value_definition = {}

    class DigKeyCnctInfo2KeyIdByte4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte4"
        signal_length = 8
        start_position = 399
        value_definition = {}

    class DigKeyCnctInfo2KeyIdByte7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte7"
        signal_length = 8
        start_position = 423
        value_definition = {}

    class DigKeyCnctInfo2KeyIdByte8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte8"
        signal_length = 8
        start_position = 431
        value_definition = {}

    class DigKeyCnctInfo2KeyIdByte12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte12"
        signal_length = 8
        start_position = 463
        value_definition = {}

    class DigKeyCnctInfo2AutoZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Approach Zone key present status"
        signal_length = 4
        start_position = 359
        value_definition = {'0x0': ' KeyPrsntZoneInfo_NotConnected', '0x1': ' KeyPrsntZoneInfo_Connected', '0x2': ' KeyPrsntZoneInfo_Welcome', '0x3': ' KeyPrsntZoneInfo_WalkAway', '0x4': ' KeyPrsntZoneInfo_LockUnlockBuffer', '0x5': ' KeyPrsntZoneInfo_Approach', '0x6': ' KeyPrsntZoneInfo_Door', '0x7': ' KeyPrsntZoneInfo_InCar', '0x8': ' KeyPrsntZoneInfo_InFL', '0x9': ' KeyPrsntZoneInfo_InFR', '0xA': ' KeyPrsntZoneInfo_InRL', '0xB': ' KeyPrsntZoneInfo_InRR', '0xC': ' KeyPrsntZoneInfo_Tr', '0xD': ' KeyPrsntZoneInfo_Reserved1', '0xE': ' KeyPrsntZoneInfo_Reserved2', '0xF': ' KeyPrsntZoneInfo_Reserved3'}

    class DigKeyCnctInfo2KeyIdByte1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte1"
        signal_length = 8
        start_position = 375
        value_definition = {}

    class DigKeyCnctInfo2BattWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Indicate if the key is in low battery state"
        signal_length = 1
        start_position = 345
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class DigKeyCnctInfo2KeyIdByte2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "Keyid byte2"
        signal_length = 8
        start_position = 383
        value_definition = {}

    class DigKeyCnctInfo2PSEnaSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 800
        signal_description = "PS Zone key present status"
        signal_length = 1
        start_position = 336
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class DigKeyCnctInfo3KeyIdByte1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte1"
        signal_length = 8
        start_position = 527
        value_definition = {}

    class DigKeyCnctInfo3KeyIdByte8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte8"
        signal_length = 8
        start_position = 583
        value_definition = {}

    class DigKeyCnctInfo3KeyIdByte10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte10"
        signal_length = 8
        start_position = 599
        value_definition = {}

    class DigKeyCnctInfo3KeyIdByte11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte11"
        signal_length = 8
        start_position = 607
        value_definition = {}

    class DigKeyCnctInfo3KeyIdByte9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte9"
        signal_length = 8
        start_position = 591
        value_definition = {}

    class DigKeyCnctInfo3PSEnaSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "PS Zone key present status"
        signal_length = 1
        start_position = 488
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class DigKeyCnctInfo3KeyIdByte3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte3"
        signal_length = 8
        start_position = 543
        value_definition = {}

    class DigKeyCnctInfo3KeyIdByte7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte7"
        signal_length = 8
        start_position = 575
        value_definition = {}

    class DigKeyCnctInfo3AutoLockOnLeaveSetting:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Walk away lock setting"
        signal_length = 3
        start_position = 503
        value_definition = {'0x0': ' AutoLockOnLeaveSetting_Unkown', '0x1': ' AutoLockOnLeaveSetting_Off', '0x2': ' AutoLockOnLeaveSetting_OnWithoutAnyDoorClose', '0x3': ' AutoLockOnLeaveSetting_OnWithDriverDoorClose', '0x4': ' AutoLockOnLeaveSetting_OnWithSideDoorClose', '0x5': ' AutoLockOnLeaveSetting_OnWithAllDoorClose'}

    class DigKeyCnctInfo3KeyIdByte5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte5"
        signal_length = 8
        start_position = 559
        value_definition = {}

    class DigKeyCnctInfo3KeyIdByte2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte2"
        signal_length = 8
        start_position = 535
        value_definition = {}

    class DigKeyCnctInfo3KeyIdByte15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte15"
        signal_length = 8
        start_position = 639
        value_definition = {}

    class DigKeyCnctInfo3KeyIdByte6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte6"
        signal_length = 8
        start_position = 567
        value_definition = {}

    class DigKeyCnctInfo3KeyConnectInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Indicate if key is connected"
        signal_length = 1
        start_position = 496
        value_definition = {'0x0': ' ConnectionSts_Disconnect', '0x1': ' ConnectionSts_Connect'}

    class DigKeyCnctInfo3KeyIdByte4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte4"
        signal_length = 8
        start_position = 551
        value_definition = {}

    class DigKeyCnctInfo3AutoZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Approach Zone key present status"
        signal_length = 4
        start_position = 511
        value_definition = {'0x0': ' KeyPrsntZoneInfo_NotConnected', '0x1': ' KeyPrsntZoneInfo_Connected', '0x2': ' KeyPrsntZoneInfo_Welcome', '0x3': ' KeyPrsntZoneInfo_WalkAway', '0x4': ' KeyPrsntZoneInfo_LockUnlockBuffer', '0x5': ' KeyPrsntZoneInfo_Approach', '0x6': ' KeyPrsntZoneInfo_Door', '0x7': ' KeyPrsntZoneInfo_InCar', '0x8': ' KeyPrsntZoneInfo_InFL', '0x9': ' KeyPrsntZoneInfo_InFR', '0xA': ' KeyPrsntZoneInfo_InRL', '0xB': ' KeyPrsntZoneInfo_InRR', '0xC': ' KeyPrsntZoneInfo_Tr', '0xD': ' KeyPrsntZoneInfo_Reserved1', '0xE': ' KeyPrsntZoneInfo_Reserved2', '0xF': ' KeyPrsntZoneInfo_Reserved3'}

    class DigKeyCnctInfo3KeyIdByte12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte12"
        signal_length = 8
        start_position = 615
        value_definition = {}

    class DigKeyCnctInfo3PEKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "PE Zone key present status"
        signal_length = 3
        start_position = 491
        value_definition = {'0x0': ' PELocnSts_Idle', '0x1': ' PELocnSts_PEAllExt', '0x2': ' PELocnSts_PEDrvrExt', '0x3': ' PELocnSts_PEPassExt', '0x4': ' PELocnSts_PEFrntExt', '0x5': ' PELocnSts_PERearExt', '0x6': ' PELocnSts_PEAllInt', '0x7': ' PELocnSts_Reserved'}

    class DigKeyCnctInfo3BattWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Indicate if the key is in low battery state"
        signal_length = 1
        start_position = 497
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class DigKeyCnctInfo3KeyIdByte13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte13"
        signal_length = 8
        start_position = 623
        value_definition = {}

    class DigKeyCnctInfo3KeyTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Key type"
        signal_length = 4
        start_position = 495
        value_definition = {'0x0': ' KeyTyp_NoKeyConnected', '0x1': ' KeyTyp_NFC_Card', '0x2': ' KeyTyp_BLE_UWB_KeyFob', '0x3': ' KeyTyp_Phone_NFC_Key', '0x4': ' KeyTyp_Phone_BLE_Key', '0x5': ' KeyTyp_Phone_UWB_Key', '0x6': ' KeyTyp_Reserved1', '0x7': ' KeyTyp_Reserved2', '0x8': ' KeyTyp_Reserved3', '0x9': ' KeyTyp_Reserved4'}

    class DigKeyCnctInfo3KeyIdByte0:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte0"
        signal_length = 8
        start_position = 519
        value_definition = {}

    class DigKeyCnctInfo3KeyIdByte14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Keyid byte14"
        signal_length = 8
        start_position = 631
        value_definition = {}

    class DigKeyCnctInfo3AutoUnlockOnApproachSetting:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 815
        signal_description = "Approach unlock setting"
        signal_length = 3
        start_position = 500
        value_definition = {'0x0': ' ApproachUnlockSetting_Unkown', '0x1': ' ApproachUnlockSetting_Off', '0x2': ' ApproachUnlockSetting_OnWithoutDoorOpen', '0x3': ' ApproachUnlockSetting_OnWithDoorMinAngleOpen', '0x4': ' ApproachUnlockSetting_OnWithDoorFullOpen'}

    class DigKeyCnctInfo4KeyIdByte0:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte0"
        signal_length = 8
        start_position = 671
        value_definition = {}

    class DigKeyCnctInfo4KeyIdByte14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte14"
        signal_length = 8
        start_position = 783
        value_definition = {}

    class DigKeyCnctInfo4KeyIdByte1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte1"
        signal_length = 8
        start_position = 679
        value_definition = {}

    class DigKeyCnctInfo4KeyIdByte6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte6"
        signal_length = 8
        start_position = 719
        value_definition = {}

    class DigKeyCnctInfo4KeyIdByte10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte10"
        signal_length = 8
        start_position = 751
        value_definition = {}

    class DigKeyCnctInfo4KeyIdByte15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte15"
        signal_length = 8
        start_position = 791
        value_definition = {}

    class DigKeyCnctInfo4BattWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Indicate if the key is in low battery state"
        signal_length = 1
        start_position = 649
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class DigKeyCnctInfo4KeyIdByte4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte4"
        signal_length = 8
        start_position = 703
        value_definition = {}

    class DigKeyCnctInfo4KeyTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Key type info"
        signal_length = 4
        start_position = 647
        value_definition = {'0x0': ' KeyTyp_NoKeyConnected', '0x1': ' KeyTyp_NFC_Card', '0x2': ' KeyTyp_BLE_UWB_KeyFob', '0x3': ' KeyTyp_Phone_NFC_Key', '0x4': ' KeyTyp_Phone_BLE_Key', '0x5': ' KeyTyp_Phone_UWB_Key', '0x6': ' KeyTyp_Reserved1', '0x7': ' KeyTyp_Reserved2', '0x8': ' KeyTyp_Reserved3', '0x9': ' KeyTyp_Reserved4'}

    class DigKeyCnctInfo4KeyIdByte9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte9"
        signal_length = 8
        start_position = 743
        value_definition = {}

    class DigKeyCnctInfo4KeyIdByte2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte2"
        signal_length = 8
        start_position = 687
        value_definition = {}

    class DigKeyCnctInfo4KeyIdByte12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte12"
        signal_length = 8
        start_position = 767
        value_definition = {}

    class DigKeyCnctInfo4AutoLockOnLeaveSetting:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Walk away lock setting"
        signal_length = 3
        start_position = 655
        value_definition = {'0x0': ' AutoLockOnLeaveSetting_Unkown', '0x1': ' AutoLockOnLeaveSetting_Off', '0x2': ' AutoLockOnLeaveSetting_OnWithoutAnyDoorClose', '0x3': ' AutoLockOnLeaveSetting_OnWithDriverDoorClose', '0x4': ' AutoLockOnLeaveSetting_OnWithSideDoorClose', '0x5': ' AutoLockOnLeaveSetting_OnWithAllDoorClose'}

    class DigKeyCnctInfo4KeyIdByte13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte13"
        signal_length = 8
        start_position = 775
        value_definition = {}

    class DigKeyCnctInfo4KeyIdByte7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte7"
        signal_length = 8
        start_position = 727
        value_definition = {}

    class DigKeyCnctInfo4PSEnaSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "PS Zone key present status"
        signal_length = 1
        start_position = 640
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class DigKeyCnctInfo4PEKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "PE Zone key present status"
        signal_length = 3
        start_position = 643
        value_definition = {'0x0': ' PELocnSts_Idle', '0x1': ' PELocnSts_PEAllExt', '0x2': ' PELocnSts_PEDrvrExt', '0x3': ' PELocnSts_PEPassExt', '0x4': ' PELocnSts_PEFrntExt', '0x5': ' PELocnSts_PERearExt', '0x6': ' PELocnSts_PEAllInt', '0x7': ' PELocnSts_Reserved'}

    class DigKeyCnctInfo4KeyIdByte8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte8"
        signal_length = 8
        start_position = 735
        value_definition = {}

    class DigKeyCnctInfo4KeyIdByte3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte3"
        signal_length = 8
        start_position = 695
        value_definition = {}

    class DigKeyCnctInfo4KeyIdByte5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte5"
        signal_length = 8
        start_position = 711
        value_definition = {}

    class DigKeyCnctInfo4AutoZoneKeyPrsntSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Approach Zone key present status"
        signal_length = 4
        start_position = 663
        value_definition = {'0x0': ' KeyPrsntZoneInfo_NotConnected', '0x1': ' KeyPrsntZoneInfo_Connected', '0x2': ' KeyPrsntZoneInfo_Welcome', '0x3': ' KeyPrsntZoneInfo_WalkAway', '0x4': ' KeyPrsntZoneInfo_LockUnlockBuffer', '0x5': ' KeyPrsntZoneInfo_Approach', '0x6': ' KeyPrsntZoneInfo_Door', '0x7': ' KeyPrsntZoneInfo_InCar', '0x8': ' KeyPrsntZoneInfo_InFL', '0x9': ' KeyPrsntZoneInfo_InFR', '0xA': ' KeyPrsntZoneInfo_InRL', '0xB': ' KeyPrsntZoneInfo_InRR', '0xC': ' KeyPrsntZoneInfo_Tr', '0xD': ' KeyPrsntZoneInfo_Reserved1', '0xE': ' KeyPrsntZoneInfo_Reserved2', '0xF': ' KeyPrsntZoneInfo_Reserved3'}

    class DigKeyCnctInfo4AutoUnlockOnApproachSetting:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Approach unlock setting"
        signal_length = 3
        start_position = 652
        value_definition = {'0x0': ' ApproachUnlockSetting_Unkown', '0x1': ' ApproachUnlockSetting_Off', '0x2': ' ApproachUnlockSetting_OnWithoutDoorOpen', '0x3': ' ApproachUnlockSetting_OnWithDoorMinAngleOpen', '0x4': ' ApproachUnlockSetting_OnWithDoorFullOpen'}

    class DigKeyCnctInfo4KeyConnectInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Indicate if key is connected"
        signal_length = 1
        start_position = 648
        value_definition = {'0x0': ' ConnectionSts_Disconnect', '0x1': ' ConnectionSts_Connect'}

    class DigKeyCnctInfo4KeyIdByte11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Keyid byte11"
        signal_length = 8
        start_position = 759
        value_definition = {}

    class DisplayAreaSts:
        comments = ""
        factor = 1.0
        initial_value = 7
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 813
        signal_description = "The Srceen Display Area Status"
        signal_length = 3
        start_position = 911
        value_definition = {}

    class DoorOpenProtectSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 812
        signal_description = "function status of door open protect"
        signal_length = 1
        start_position = 908
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class DrvrInCarSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 811
        signal_description = "driver in car "
        signal_length = 1
        start_position = 907
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class DynoModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 810
        signal_description = "Dyno Mode Status"
        signal_length = 1
        start_position = 906
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ECUCoolgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 809
        signal_description = "ECUs Cooling Req"
        signal_length = 1
        start_position = 905
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class ECUCooltFlwReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 808
        signal_description = "ECUs coolant flow req"
        signal_length = 9
        start_position = 904
        value_definition = {}

    class FrntMotInfoDTCHig:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "DTC high byte"
        signal_length = 8
        start_position = 927
        value_definition = {}

    class FrntMotInfoEMSeqNr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Sequence number of electric motor"
        signal_length = 4
        start_position = 935
        value_definition = {}

    class FrntMotInfoPasDchaAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Passive discharge failure will set this alarm."
        signal_length = 2
        start_position = 931
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoPlsHeatAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Pulse heat failure will set this alarm."
        signal_length = 2
        start_position = 929
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoUDCAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "High voltage alarm status"
        signal_length = 2
        start_position = 943
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoActvHeatgAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Active heat failure will set this alarm."
        signal_length = 2
        start_position = 941
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoDTCLow:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "DTC low byte"
        signal_length = 8
        start_position = 951
        value_definition = {}

    class FrntMotInfoModStRms:
        comments = ""
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Motor status for RMS monitor"
        signal_length = 4
        start_position = 959
        value_definition = {'0x0': ' ModStatusRms_Invalid', '0x1': ' ModStatusRms_PwrCns', '0x2': ' ModStatusRms_PwrGen', '0x3': ' ModStatusRms_OffSts', '0x4': ' ModStatusRms_RdySts', '0x5': ' ModStatusRms_Abnormal', '0x6': ' ModStatusRms_Invalid1', '0x7': ' ModStatusRms_Invalid2', '0x8': ' ModStatusRms_Invalid3', '0x9': ' ModStatusRms_Invalid4', '0xA': ' ModStatusRms_Invalid5', '0xB': ' ModStatusRms_Invalid6', '0xC': ' ModStatusRms_Invalid7', '0xD': ' ModStatusRms_Invalid8', '0xE': ' ModStatusRms_Invalid9', '0xF': ' ModStatusRms_Invalid10'}

    class FrntMotInfoFltAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Fault alarm status"
        signal_length = 2
        start_position = 955
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoBoostAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Boost  failure will set this alarm."
        signal_length = 2
        start_position = 953
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoTqAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Torque limit failure will set this alarm."
        signal_length = 2
        start_position = 967
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoRatTypeInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Motor ratio information.0=not defined,1=Jupiter,with ratio=TBD"
        signal_length = 4
        start_position = 979
        value_definition = {}

    class FrntMotInfoIPhaAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "3 Phase current alarm status"
        signal_length = 2
        start_position = 961
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoOilTAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Oil temperature sensor failure will set this alarm."
        signal_length = 2
        start_position = 965
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoEMQnty:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Quantity of electric motor"
        signal_length = 4
        start_position = 939
        value_definition = {}

    class FrntMotInfoRslAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Resolver fault alarm status"
        signal_length = 2
        start_position = 963
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoActvDchaAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Active discharge failure will set this alarm"
        signal_length = 2
        start_position = 983
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoInvrtTAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Inverter temperature alarm status"
        signal_length = 2
        start_position = 981
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoDTCLMid:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "DTC middle byte"
        signal_length = 8
        start_position = 975
        value_definition = {}

    class FrntMotInfoMotTAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Motor temperature alarm status"
        signal_length = 2
        start_position = 999
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoOverSpdAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "Over speed alarm status"
        signal_length = 2
        start_position = 997
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class FrntMotInfoDTCSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 823
        signal_description = "DTC Status"
        signal_length = 8
        start_position = 991
        value_definition = {}

    class FrntMotOilTEstimd:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 822
        signal_description = "Front Motor Oil Estimd Temperature"
        signal_length = 13
        start_position = 1015
        value_definition = {}

    class FrontLeftTyreAlarmInfoTWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 821
        signal_description = "Warning that temperature is higher than normal"
        signal_length = 2
        start_position = 1027
        value_definition = {'0x0': ' TWarnFlag_Nromal', '0x1': ' TWarnFlag_HighTWarn', '0x2': ' TWarnFlag_Reserve1', '0x3': ' TWarnFlag_Reserve2'}

    class FrontLeftTyreAlarmInfoFastLoseWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 821
        signal_description = "Warning that Tire is leaking fast"
        signal_length = 1
        start_position = 1025
        value_definition = {'0x0': ' FastLoseWarnFlag_Normal', '0x1': ' FastLoseWarnFlag_Warning'}

    class FrontLeftTyreAlarmInfoBattLowWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 821
        signal_description = "Warning that battery level is lower than normal"
        signal_length = 1
        start_position = 1031
        value_definition = {'0x0': ' BattLowWarnFlag_Normal', '0x1': ' BattLowWarnFlag_Warning'}

    class FrontLeftTyreAlarmInfoPWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 821
        signal_description = "Warning that pressure is lower and higher than normal"
        signal_length = 2
        start_position = 1030
        value_definition = {'0x0': ' PWarnFlag_Normal', '0x1': ' PWarnFlag_LowPWarn', '0x2': ' PWarnFlag_Reserve1', '0x3': ' PWarnFlag_Reserve2'}

    class FrontLeftTyreAlarmInfoSysWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 821
        signal_description = "Warning of System fault"
        signal_length = 1
        start_position = 1028
        value_definition = {'0x0': ' SysWarnFlag_Nromal', '0x1': ' SysWarnFlag_Warning'}

    class FrontLeftTyreDataTyreTemperature:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -50
        sig_ub = 820
        signal_description = "Tire Temperature"
        signal_length = 8
        start_position = 1039
        value_definition = {}

    class FrontLeftTyreDataTyrePressure:
        comments = ""
        factor = 1.373
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 820
        signal_description = "Tire Pressure"
        signal_length = 8
        start_position = 1047
        value_definition = {}

    class FrontRightTyreAlarmInfoBattLowWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 819
        signal_description = "Warning that battery level is lower than normal"
        signal_length = 1
        start_position = 1055
        value_definition = {'0x0': ' BattLowWarnFlag_Normal', '0x1': ' BattLowWarnFlag_Warning'}

    class FrontRightTyreAlarmInfoSysWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 819
        signal_description = "Warning of System fault"
        signal_length = 1
        start_position = 1054
        value_definition = {'0x0': ' SysWarnFlag_Nromal', '0x1': ' SysWarnFlag_Warning'}

    class FrontRightTyreAlarmInfoPWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 819
        signal_description = "Warning that pressure is lower and higher than normal"
        signal_length = 2
        start_position = 1053
        value_definition = {'0x0': ' PWarnFlag_Normal', '0x1': ' PWarnFlag_LowPWarn', '0x2': ' PWarnFlag_Reserve1', '0x3': ' PWarnFlag_Reserve2'}

    class FrontRightTyreAlarmInfoTWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 819
        signal_description = "Warning that temperature is higher than normal"
        signal_length = 2
        start_position = 1051
        value_definition = {'0x0': ' TWarnFlag_Nromal', '0x1': ' TWarnFlag_HighTWarn', '0x2': ' TWarnFlag_Reserve1', '0x3': ' TWarnFlag_Reserve2'}

    class FrontRightTyreAlarmInfoFastLoseWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 819
        signal_description = "Warning that Tire is leaking fast"
        signal_length = 1
        start_position = 1049
        value_definition = {'0x0': ' FastLoseWarnFlag_Normal', '0x1': ' FastLoseWarnFlag_Warning'}

    class FrontRightTyreDataTyrePressure:
        comments = ""
        factor = 1.373
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 818
        signal_description = "Tire Pressure"
        signal_length = 8
        start_position = 1063
        value_definition = {}

    class FrontRightTyreDataTyreTemperature:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -50
        sig_ub = 818
        signal_description = "Tire Temperature"
        signal_length = 8
        start_position = 1071
        value_definition = {}

    class HVBattCellUMaxLim:
        comments = ""
        factor = 0.001
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 817
        signal_description = "The battery cell charging voltage limit when SOC is 100 percent."
        signal_length = 13
        start_position = 1079
        value_definition = {}

    class HVBattClimaTiEstimd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 816
        signal_description = "Hvbatt Thermal Management Count Down"
        signal_length = 8
        start_position = 1095
        value_definition = {}

    class HVBattCoolgPwrDes:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 831
        signal_description = "HvBatt Cooling Desired Power"
        signal_length = 13
        start_position = 1103
        value_definition = {}

    class HVBattHeatgPwrDes:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 830
        signal_description = "HvBatt Heating Desired Power"
        signal_length = 13
        start_position = 1106
        value_definition = {}

    class HVBattOptmzSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 829
        signal_description = "The hints state of HV battery full charge optimization"
        signal_length = 2
        start_position = 1125
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}

    class HvBattPackSOH:
        comments = ""
        factor = 0.5
        initial_value = 204
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 828
        signal_description = "The state-of-health Energy of HV Battery Pack"
        signal_length = 8
        start_position = 1135
        value_definition = {}

    class HVBattPackUMaxLim:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 827
        signal_description = "The  high limit  voltage of HV battery pack  (dynamically based on cell voltage distribution)."
        signal_length = 16
        start_position = 1143
        value_definition = {}

    class HVBattPackUMinLim:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 826
        signal_description = "The low limit  voltage of HV battery pack  (dynamically based on cell voltage distribution)."
        signal_length = 16
        start_position = 1159
        value_definition = {}

    class HVBattPcakSOCE:
        comments = ""
        factor = 0.05
        initial_value = 2040
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 825
        signal_description = "SOCE(the state of certified energy)"
        signal_length = 11
        start_position = 1175
        value_definition = {}

    class HVBattThermMngtHVPwrCns:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 824
        signal_description = "Hvbatt thermal management HV power consume"
        signal_length = 13
        start_position = 1180
        value_definition = {}

    class HVBattThermMngtPwrActCoolgPwr:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 839
        signal_description = "HV battery thermal management Cooling power actual"
        signal_length = 13
        start_position = 1199
        value_definition = {}

    class HVBattThermMngtPwrActHeatgPwr:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 839
        signal_description = "HV battery thermal management heating power actual"
        signal_length = 13
        start_position = 1202
        value_definition = {}

    class HVBattThermPwrAllwd:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 838
        signal_description = "hvbatt thermal management power allowed"
        signal_length = 13
        start_position = 1221
        value_definition = {}

    class HVBattThermReqActualThermLvlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 837
        signal_description = "merged thermal request level for HV battery"
        signal_length = 2
        start_position = 1265
        value_definition = {'0x0': ' ReqLvl_NoReq', '0x1': ' ReqLvl_LoReq', '0x2': ' ReqLvl_MidReq', '0x3': ' ReqLvl_HiReq'}

    class HVBattThermReqActualCooltFlwReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 837
        signal_description = "merged coolant flow request for HV battery"
        signal_length = 9
        start_position = 1239
        value_definition = {}

    class HVBattThermReqActualThermReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 837
        signal_description = "merged thermal request for HV battery"
        signal_length = 3
        start_position = 1246
        value_definition = {'0x0': ' HVBattThermReq_Idle', '0x1': ' HVBattThermReq_ThermalBalancing', '0x2': ' HVBattThermReq_PassiveHeating', '0x3': ' HVBattThermReq_ActiveHeating', '0x4': ' HVBattThermReq_PassiveCooling', '0x5': ' HVBattThermReq_ActiveCooling', '0x6': ' HVBattThermReq_CombinedCooling', '0x7': ' HVBattThermReq_Reserved'}

    class HVBattThermReqActualCellTTar:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = 837
        signal_description = "merged cell Target Temperature request for HV battery"
        signal_length = 11
        start_position = 1255
        value_definition = {}

    class HVBattThermReqActualCooltTReq:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = 837
        signal_description = "merged coolant Temperature request for HV battery"
        signal_length = 11
        start_position = 1260
        value_definition = {}

    class HVBattThermReqActualSourceID:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 837
        signal_description = "Source ID"
        signal_length = 16
        start_position = 1279
        value_definition = {}

    class HVBattThermReqActualCellTType:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 837
        signal_description = "merged Taget Cell Type"
        signal_length = 2
        start_position = 1243
        value_definition = {'0x0': ' BattTemperatureType_Idle', '0x1': ' BattTemperatureType_Tmin', '0x2': ' BattTemperatureType_TAvg', '0x3': ' BattTemperatureType_TMax'}

    class HVBattThermReqResp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 836
        signal_description = "HvBatt thermal management request Response"
        signal_length = 4
        start_position = 1935
        value_definition = {'0x0': ' HVBattThermReqFb_Idle', '0x1': ' HVBattThermReqFb_ThermalBalancing', '0x2': ' HVBattThermReqFb_PassiveHeating', '0x3': ' HVBattThermReqFb_ActiveHeating', '0x4': ' HVBattThermReqFb_PassiveCooling', '0x5': ' HVBattThermReqFb_ActiveCooling', '0x6': ' HVBattThermReqFb_CombineCooling', '0x7': ' HVBattThermReqFb_ActivePassiveHeating', '0x8': ' HVBattThermReqFb_Inhibt', '0x9': ' HVBattThermReqFb_HeatingFinish', '0xA': ' HVBattThermReqFb_CoolingFinish', '0xB': ' HVBattThermReqFb_Reserve01', '0xC': ' HVBattThermReqFb_Reserve02'}

    class HVIL1St:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 835
        signal_description = "HVIL status of HV battery connectors. "
        signal_length = 2
        start_position = 1943
        value_definition = {'0x0': ' OpenCls2_Default', '0x1': ' OpenCls2_Close', '0x2': ' OpenCls2_Open', '0x3': ' OpenCls2_Reserved'}

    class HVIL2St:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 834
        signal_description = "HVIL status of other HV component connectors except HV battery."
        signal_length = 2
        start_position = 1941
        value_definition = {'0x0': ' OpenCls2_Default', '0x1': ' OpenCls2_Close', '0x2': ' OpenCls2_Open', '0x3': ' OpenCls2_Reserved'}

    class HVIL3St:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 833
        signal_description = "HVIL status of other HV component connectors except HV battery."
        signal_length = 2
        start_position = 1939
        value_definition = {'0x0': ' OpenCls2_Default', '0x1': ' OpenCls2_Close', '0x2': ' OpenCls2_Open', '0x3': ' OpenCls2_Reserved'}

    class HVIsoCrashFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 832
        signal_description = "The status of Isolation resistance after crash."
        signal_length = 2
        start_position = 1937
        value_definition = {'0x0': ' IsoCrashFb_Idle', '0x1': ' IsoCrashFb_Evln', '0x2': ' IsoCrashFb_Nok', '0x3': ' IsoCrashFb_Ok'}

    class HVIsoRVal:
        comments = ""
        factor = 1.0
        initial_value = 60000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 847
        signal_description = "HV system insulation resistance value."
        signal_length = 16
        start_position = 1295
        value_definition = {}

    class HVSysIsoSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 846
        signal_description = "The isolation status of HV battery pack or HV system."
        signal_length = 2
        start_position = 1311
        value_definition = {'0x0': ' HvSysIsoSts_Default', '0x1': ' HvSysIsoSts_Error_Battery_before_HV_Ready', '0x2': ' HvSysIsoSts_Error_HV_bus_after_HV_Ready', '0x3': ' HvSysIsoSts_OK'}

    class IRawBCU1:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 845
        signal_description = "Current"
        signal_length = 13
        start_position = 1309
        value_definition = {}

    class IRawBCU2:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 844
        signal_description = "Current"
        signal_length = 13
        start_position = 1312
        value_definition = {}

    class IRawCCUCD:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 843
        signal_description = "Current"
        signal_length = 13
        start_position = 1331
        value_definition = {}

    class IRawPSCM2:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 842
        signal_description = "Current"
        signal_length = 13
        start_position = 1350
        value_definition = {}

    class KeyNotPrsntWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 841
        signal_description = "Key Not Present Warning"
        signal_length = 1
        start_position = 1353
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class LocalCenLockAbnormFbNFCLockUnlckFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 840
        signal_description = "Central lock abnormal feedback by NFC"
        signal_length = 4
        start_position = 1367
        value_definition = {'0x0': ' NFCLockUnlckFb_None', '0x1': ' NFCLockUnlckFb_LockUMNotfill', '0x2': ' NFCLockUnlckFb_LockSeatNotfill', '0x3': ' NFCLockUnlckFb_LockCardNotPrsnt', '0x4': ' NFCLockUnlckFb_LockDoorAntiPnch', '0x5': ' NFCLockUnlckFb_LockDoorNotClose', '0x6': ' NFCLockUnlckFb_LockKeyForget', '0x7': ' NFCLockUnlckFb_UnLckUMNotfill', '0x8': ' NFCLockUnlckFb_UnLckSeatNotfill'}

    class LocalCenLockAbnormFbAproLockUnlckFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 840
        signal_description = "Central lock abnormal feedback by Approach"
        signal_length = 4
        start_position = 1363
        value_definition = {'0x0': ' AproLockUnlckFb_None', '0x1': ' AproLockUnlckFb_LockUMNotfill', '0x2': ' AproLockUnlckFb_LockSeatNotfill', '0x3': ' AproLockUnlckFb_LockPerSetNotfill', '0x4': ' AproLockUnlckFb_LockResd1', '0x5': ' AproLockUnlckFb_LockDoorAntiPnch', '0x6': ' AproLockUnlckFb_LockDoorNotClose', '0x7': ' AproLockUnlckFb_UnLckUMNotfill', '0x8': ' AproLockUnlckFb_UnLckSeatNotfill', '0x9': ' AproLockUnlckFb_Resd1', '0xA': ' AproLockUnlckFb_Resd2', '0xB': ' AproLockUnlckFb_Resd3'}

    class LocalCenLockAbnormFbPELockUnlckFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 840
        signal_description = "Central lock abnormal feedback by PE"
        signal_length = 4
        start_position = 1375
        value_definition = {'0x0': ' PELockUnlckFb_None', '0x1': ' PELockUnlckFb_LockUMNotfill', '0x2': ' PELockUnlckFb_LockSeatNotfill', '0x3': ' PELockUnlckFb_LockNoKeyPresent', '0x4': ' PELockUnlckFb_LockKeyForget', '0x5': ' PELockUnlckFb_LockDoorAntiPnch', '0x6': ' PELockUnlckFb_LockDoorNotClose', '0x7': ' PELockUnlckFb_UnLckUMNotfill', '0x8': ' PELockUnlckFb_UnLckSeatNotfill', '0x9': ' PELockUnlckFb_UnLckNoKeyPresent', '0xA': ' PELockUnlckFb_Resd1', '0xB': ' PELockUnlckFb_Resd2', '0xC': ' PELockUnlckFb_Resd3', '0xD': ' PELockUnlckFb_Resd4', '0xE': ' PELockUnlckFb_Resd5', '0xF': ' PELockUnlckFb_Resd6'}

    class LocalClsDoorPrmpt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 855
        signal_description = "close door prompt"
        signal_length = 3
        start_position = 1931
        value_definition = {'0x0': ' ClsDoorPrmpt_Idle', '0x1': ' ClsDoorPrmpt_NFCClsDoorPrmpt', '0x2': ' ClsDoorPrmpt_AproClsDoorPrmpt', '0x3': ' ClsDoorPrmpt_PEClsDoorPrmpt', '0x4': ' ClsDoorPrmpt_OutdClsDoorPrmpt', '0x5': ' ClsDoorPrmpt_InsdClsDoorPrmpt', '0x6': ' ClsDoorPrmpt_Resd1', '0x7': ' ClsDoorPrmpt_Resd2'}

    class MotHeatgPwrDes:
        comments = ""
        factor = 20.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 854
        signal_description = "Desire motor heating power"
        signal_length = 10
        start_position = 1369
        value_definition = {}

    class MotHeatgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 853
        signal_description = "Motor Heating request"
        signal_length = 1
        start_position = 1371
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PassAirbEnaSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 852
        signal_description = "Passenger airbag enable status"
        signal_length = 2
        start_position = 1391
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class PassAirbInjSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 851
        signal_description = "Passenger airbag injection status"
        signal_length = 2
        start_position = 1389
        value_definition = {'0x0': ' OffOnInvld_Invalid1', '0x1': ' OffOnInvld_Off', '0x2': ' OffOnInvld_On', '0x3': ' OffOnInvld_Invalid2'}

    class PhoneDetn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 850
        signal_description = "Mobile phone forgotten reminder"
        signal_length = 2
        start_position = 1387
        value_definition = {'0x0': ' PhoneDetn_Idle', '0x1': ' PhoneDetn_Yes', '0x2': ' PhoneDetn_No', '0x3': ' PhoneDetn_Reserved'}

    class PhoneDetnPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 849
        signal_description = "Mobile phone forgotten reminder of passenger side"
        signal_length = 2
        start_position = 1385
        value_definition = {'0x0': ' PhoneDetn_Idle', '0x1': ' PhoneDetn_Yes', '0x2': ' PhoneDetn_No', '0x3': ' PhoneDetn_Reserved'}

    class PWTCoolgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 848
        signal_description = "PT Cooling Request"
        signal_length = 1
        start_position = 1398
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class PWTCoolgReqLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 863
        signal_description = "PT Coolant Request Level"
        signal_length = 2
        start_position = 1397
        value_definition = {'0x0': ' ReqLvl_NoReq', '0x1': ' ReqLvl_LoReq', '0x2': ' ReqLvl_MidReq', '0x3': ' ReqLvl_HiReq'}

    class PWTCooltFlwReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 862
        signal_description = "PT Coolant Flow Request"
        signal_length = 9
        start_position = 1395
        value_definition = {}

    class PWTCooltTMaxReq:
        comments = ""
        factor = 0.1
        initial_value = 5110
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 861
        signal_description = "PT Maximum Coolant Temperature Request"
        signal_length = 13
        start_position = 1402
        value_definition = {}

    class PWTCooltTMinReq:
        comments = ""
        factor = 0.1
        initial_value = 5110
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 860
        signal_description = "PT Minimum Coolant Temperature Request"
        signal_length = 13
        start_position = 1421
        value_definition = {}

    class PWTThermReqActualCooltTMaxReq:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = 1954
        signal_description = "Power train thermal request actual temperature max"
        signal_length = 11
        start_position = 1960
        value_definition = {}

    class PWTThermReqActualCoolgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1954
        signal_description = "Power train thermal request actual Cooling request"
        signal_length = 1
        start_position = 1986
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class PWTThermReqActualCooltTMinReq:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -60
        sig_ub = 1954
        signal_description = "Power train thermal request actual temperature min"
        signal_length = 11
        start_position = 1981
        value_definition = {}

    class PWTThermReqActualCooltFlwReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1954
        signal_description = "Power train thermal request actual coolant flow request"
        signal_length = 9
        start_position = 1953
        value_definition = {}

    class PWTThermReqActualCoolgReqLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1954
        signal_description = "Power train thermal request actual level"
        signal_length = 2
        start_position = 1985
        value_definition = {'0x0': ' ReqLvl_NoReq', '0x1': ' ReqLvl_LoReq', '0x2': ' ReqLvl_MidReq', '0x3': ' ReqLvl_HiReq'}

    class PWTThermReqActualSourceID:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1954
        signal_description = "SourceID"
        signal_length = 16
        start_position = 1999
        value_definition = {}

    class PWTThermReqResp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 858
        signal_description = "PWT thermal request respond"
        signal_length = 4
        start_position = 1467
        value_definition = {'0x0': ' PwtThermMod_Idle', '0x1': ' PwtThermMod_Off', '0x2': ' PwtThermMod_SeparateLoopCoolg', '0x3': ' PwtThermMod_SeparateLoopHeatg', '0x4': ' PwtThermMod_OneLoopCoolg', '0x5': ' PwtThermMod_OneLoopHeating', '0x6': ' PwtThermMod_AfterRun', '0x7': ' PwtThermMod_SuperChrgn', '0x8': ' PwtThermMod_Reserved1', '0x9': ' PwtThermMod_Reserved2'}

    class RearLeftTyreAlarmInfoTWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 857
        signal_description = "Warning that temperature is higher than normal"
        signal_length = 2
        start_position = 1479
        value_definition = {'0x0': ' TWarnFlag_Nromal', '0x1': ' TWarnFlag_HighTWarn', '0x2': ' TWarnFlag_Reserve1', '0x3': ' TWarnFlag_Reserve2'}

    class RearLeftTyreAlarmInfoBattLowWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 857
        signal_description = "Warning that battery level is lower than normal"
        signal_length = 1
        start_position = 1477
        value_definition = {'0x0': ' BattLowWarnFlag_Normal', '0x1': ' BattLowWarnFlag_Warning'}

    class RearLeftTyreAlarmInfoSysWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 857
        signal_description = "Warning of System fault"
        signal_length = 1
        start_position = 1476
        value_definition = {'0x0': ' SysWarnFlag_Nromal', '0x1': ' SysWarnFlag_Warning'}

    class RearLeftTyreAlarmInfoPWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 857
        signal_description = "Warning that pressure is lower and higher than normal"
        signal_length = 2
        start_position = 1475
        value_definition = {'0x0': ' PWarnFlag_Normal', '0x1': ' PWarnFlag_LowPWarn', '0x2': ' PWarnFlag_Reserve1', '0x3': ' PWarnFlag_Reserve2'}

    class RearLeftTyreAlarmInfoFastLoseWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 857
        signal_description = "Warning that Tire is leaking fast"
        signal_length = 1
        start_position = 1473
        value_definition = {'0x0': ' FastLoseWarnFlag_Normal', '0x1': ' FastLoseWarnFlag_Warning'}

    class RearLeftTyreDataTyrePressure:
        comments = ""
        factor = 1.373
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 856
        signal_description = "Tire Pressure"
        signal_length = 8
        start_position = 1487
        value_definition = {}

    class RearLeftTyreDataTyreTemperature:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -50
        sig_ub = 856
        signal_description = "Tire Temperature"
        signal_length = 8
        start_position = 1495
        value_definition = {}

    class RearRightTyreAlarmInfoBattLowWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 871
        signal_description = "Warning that battery level is lower than normal"
        signal_length = 1
        start_position = 1503
        value_definition = {'0x0': ' BattLowWarnFlag_Normal', '0x1': ' BattLowWarnFlag_Warning'}

    class RearRightTyreAlarmInfoTWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 871
        signal_description = "Warning that temperature is higher than normal"
        signal_length = 2
        start_position = 1502
        value_definition = {'0x0': ' TWarnFlag_Nromal', '0x1': ' TWarnFlag_HighTWarn', '0x2': ' TWarnFlag_Reserve1', '0x3': ' TWarnFlag_Reserve2'}

    class RearRightTyreAlarmInfoSysWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 871
        signal_description = "Warning of System fault"
        signal_length = 1
        start_position = 1500
        value_definition = {'0x0': ' SysWarnFlag_Nromal', '0x1': ' SysWarnFlag_Warning'}

    class RearRightTyreAlarmInfoPWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 871
        signal_description = "Warning that pressure is lower and higher than normal"
        signal_length = 2
        start_position = 1499
        value_definition = {'0x0': ' PWarnFlag_Normal', '0x1': ' PWarnFlag_LowPWarn', '0x2': ' PWarnFlag_Reserve1', '0x3': ' PWarnFlag_Reserve2'}

    class RearRightTyreAlarmInfoFastLoseWarnFlag:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 871
        signal_description = "Warning that Tire is leaking fast"
        signal_length = 1
        start_position = 1497
        value_definition = {'0x0': ' FastLoseWarnFlag_Normal', '0x1': ' FastLoseWarnFlag_Warning'}

    class RearRightTyreDataTyrePressure:
        comments = ""
        factor = 1.373
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 870
        signal_description = "Tire Pressure"
        signal_length = 8
        start_position = 1511
        value_definition = {}

    class RearRightTyreDataTyreTemperature:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -50
        sig_ub = 870
        signal_description = "Tire Temperature"
        signal_length = 8
        start_position = 1519
        value_definition = {}

    class RefrigCircDeiceReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 869
        signal_description = "Refrigerant circuit outside hex deice req"
        signal_length = 1
        start_position = 1527
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RefrigCircModAct:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 868
        signal_description = "Refrigerant Circult Actual Mode"
        signal_length = 5
        start_position = 1526
        value_definition = {'0x0': ' ThermMod_Mode0', '0x1': ' ThermMod_Mode1', '0x2': ' ThermMod_Mode2', '0x3': ' ThermMod_Mode3', '0x4': ' ThermMod_Mode4', '0x5': ' ThermMod_Mode5', '0x6': ' ThermMod_Mode6', '0x7': ' ThermMod_Mode7', '0x8': ' ThermMod_Mode8', '0x9': ' ThermMod_Mode9', '0xA': ' ThermMod_Mode10', '0xB': ' ThermMod_Mode11', '0xC': ' ThermMod_Mode12', '0xD': ' ThermMod_Mode13', '0xE': ' ThermMod_Mode14', '0xF': ' ThermMod_Mode15', '0x10': ' ThermMod_Mode16', '0x11': ' ThermMod_Mode17', '0x12': ' ThermMod_Mode18', '0x13': ' ThermMod_Mode19', '0x14': ' ThermMod_Mode20', '0x15': ' ThermMod_Mode21', '0x16': ' ThermMod_Mode22', '0x17': ' ThermMod_Mode23', '0x18': ' ThermMod_Mode24', '0x19': ' ThermMod_Mode25', '0x1A': ' ThermMod_Mode26', '0x1B': ' ThermMod_Mode27', '0x1C': ' ThermMod_Mode28', '0x1D': ' ThermMod_Mode29', '0x1E': ' ThermMod_Mode30', '0x1F': ' ThermMod_Mode31'}

    class RefrigCircModDes:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 867
        signal_description = "Desire refrigerant circuit mode"
        signal_length = 5
        start_position = 1521
        value_definition = {'0x0': ' ThermMod_Mode0', '0x1': ' ThermMod_Mode1', '0x2': ' ThermMod_Mode2', '0x3': ' ThermMod_Mode3', '0x4': ' ThermMod_Mode4', '0x5': ' ThermMod_Mode5', '0x6': ' ThermMod_Mode6', '0x7': ' ThermMod_Mode7', '0x8': ' ThermMod_Mode8', '0x9': ' ThermMod_Mode9', '0xA': ' ThermMod_Mode10', '0xB': ' ThermMod_Mode11', '0xC': ' ThermMod_Mode12', '0xD': ' ThermMod_Mode13', '0xE': ' ThermMod_Mode14', '0xF': ' ThermMod_Mode15', '0x10': ' ThermMod_Mode16', '0x11': ' ThermMod_Mode17', '0x12': ' ThermMod_Mode18', '0x13': ' ThermMod_Mode19', '0x14': ' ThermMod_Mode20', '0x15': ' ThermMod_Mode21', '0x16': ' ThermMod_Mode22', '0x17': ' ThermMod_Mode23', '0x18': ' ThermMod_Mode24', '0x19': ' ThermMod_Mode25', '0x1A': ' ThermMod_Mode26', '0x1B': ' ThermMod_Mode27', '0x1C': ' ThermMod_Mode28', '0x1D': ' ThermMod_Mode29', '0x1E': ' ThermMod_Mode30', '0x1F': ' ThermMod_Mode31'}

    class RefrigCircModSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 866
        signal_description = "Mode switch status"
        signal_length = 2
        start_position = 1532
        value_definition = {'0x0': ' StartFinish1_Start', '0x1': ' StartFinish1_Finish', '0x2': ' StartFinish1_Reserved1', '0x3': ' StartFinish1_Reserved2'}

    class RefrigCircTDesFrntEvapTarT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 865
        signal_description = "Front evaperator target temperature"
        signal_length = 13
        start_position = 1530
        value_definition = {}

    class RefrigCircTDesFrntHexTarT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 865
        signal_description = "Front hex target temperature "
        signal_length = 13
        start_position = 1549
        value_definition = {}

    class RefrigCircTDesRearEvapTarT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 865
        signal_description = "Rear evaperator target temperature"
        signal_length = 13
        start_position = 1552
        value_definition = {}

    class RefrigCircTDesRearHexTarT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 865
        signal_description = "Rear hex target temperature "
        signal_length = 13
        start_position = 1571
        value_definition = {}

    class ReMotInfoMotTAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Motor temperature alarm status"
        signal_length = 2
        start_position = 1589
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoOilTAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Oil temperature sensor failure will set this alarm."
        signal_length = 2
        start_position = 1587
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoBoostAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Boost  failure will set this alarm."
        signal_length = 2
        start_position = 1585
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoUDCAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "High voltage alarm status"
        signal_length = 2
        start_position = 1599
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoRatTypeInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Motor ratio information.0=not defined,1=Jupiter, with ratio = TBD"
        signal_length = 4
        start_position = 1597
        value_definition = {}

    class ReMotInfoTqAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Torque limit failure will set this alarm."
        signal_length = 2
        start_position = 1593
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoDTCLMid:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "DTC middle byte"
        signal_length = 8
        start_position = 1607
        value_definition = {}

    class ReMotInfoDTCSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "DTC Status"
        signal_length = 8
        start_position = 1615
        value_definition = {}

    class ReMotInfoDTCLow:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "DTC low byte"
        signal_length = 8
        start_position = 1623
        value_definition = {}

    class ReMotInfoEMQnty:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Quantity of electric motor"
        signal_length = 4
        start_position = 1631
        value_definition = {}

    class ReMotInfoActvHeatgAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Active heat failure will set this alarm."
        signal_length = 2
        start_position = 1627
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoPlsHeatAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Pulse heat failure will set this alarm."
        signal_length = 2
        start_position = 1625
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoEMSeqNr:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Sequence number of electric motor"
        signal_length = 4
        start_position = 1639
        value_definition = {}

    class ReMotInfoActvDchaAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Active discharge failure will set this alarm"
        signal_length = 2
        start_position = 1635
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoFltAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Fault alarm status"
        signal_length = 2
        start_position = 1633
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoDTCHig:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "DTC high byte"
        signal_length = 8
        start_position = 1647
        value_definition = {}

    class ReMotInfoInvrtTAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Inverter temperature alarm status"
        signal_length = 2
        start_position = 1655
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoRslAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Resolver fault alarm status"
        signal_length = 2
        start_position = 1653
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoOverSpdAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Over speed alarm status"
        signal_length = 2
        start_position = 1651
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoPasDchaAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Passive discharge failure will set this alarm."
        signal_length = 2
        start_position = 1649
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoIPhaAlrmSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "3 Phase current alarm status"
        signal_length = 2
        start_position = 1663
        value_definition = {'0x0': ' AlrmSts_Disarmd', '0x1': ' AlrmSts_Armd', '0x2': ' AlrmSts_Actv', '0x3': ' AlrmSts_Reserved'}

    class ReMotInfoModStRms:
        comments = ""
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Motor status for RMS monitor"
        signal_length = 4
        start_position = 1661
        value_definition = {'0x0': ' ModStatusRms_Invalid', '0x1': ' ModStatusRms_PwrCns', '0x2': ' ModStatusRms_PwrGen', '0x3': ' ModStatusRms_OffSts', '0x4': ' ModStatusRms_RdySts', '0x5': ' ModStatusRms_Abnormal', '0x6': ' ModStatusRms_Invalid1', '0x7': ' ModStatusRms_Invalid2', '0x8': ' ModStatusRms_Invalid3', '0x9': ' ModStatusRms_Invalid4', '0xA': ' ModStatusRms_Invalid5', '0xB': ' ModStatusRms_Invalid6', '0xC': ' ModStatusRms_Invalid7', '0xD': ' ModStatusRms_Invalid8', '0xE': ' ModStatusRms_Invalid9', '0xF': ' ModStatusRms_Invalid10'}

    class ReMotOilTEstimd:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 879
        signal_description = "Rear Motor Oil Estimd Temperature"
        signal_length = 13
        start_position = 1657
        value_definition = {}

    class ResdSigForClima01:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 878
        signal_description = "Reserved signal"
        signal_length = 16
        start_position = 1687
        value_definition = {}

    class ResdSigForClima02:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 877
        signal_description = "Reserved signal"
        signal_length = 16
        start_position = 1703
        value_definition = {}

    class ResdSigForClima03:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 876
        signal_description = "Reserved signal"
        signal_length = 16
        start_position = 1719
        value_definition = {}

    class ResdSigForClima04:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 875
        signal_description = "Reserved signal"
        signal_length = 16
        start_position = 1735
        value_definition = {}

    class ResdSigForClima05:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 874
        signal_description = "Reserved signal"
        signal_length = 16
        start_position = 1751
        value_definition = {}

    class ResdSigForClima06:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 873
        signal_description = "Reserved signal"
        signal_length = 16
        start_position = 1767
        value_definition = {}

    class ResdSigForClima07:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 872
        signal_description = "Reserved signal"
        signal_length = 16
        start_position = 1783
        value_definition = {}

    class ResdSigForClima08:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 887
        signal_description = "Reserved signal"
        signal_length = 16
        start_position = 1799
        value_definition = {}

    class ResdSigForClima09:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 886
        signal_description = "Reserved signal"
        signal_length = 16
        start_position = 1815
        value_definition = {}

    class ResdSigForClima10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 885
        signal_description = "Reserved signal"
        signal_length = 16
        start_position = 1831
        value_definition = {}

    class ScreenDispErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 884
        signal_description = "The All Display Error Status"
        signal_length = 8
        start_position = 1847
        value_definition = {}

    class SrceenTouchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 882
        signal_description = "The Srceen Touch Status is normal or fault"
        signal_length = 1
        start_position = 1863
        value_definition = {'0x0': ' OkNotOk1_Ok', '0x1': ' OkNotOk1_NotOk'}

    class TrlrModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 881
        signal_description = "Trailer Mode Status"
        signal_length = 2
        start_position = 1862
        value_definition = {'0x0': ' TrlrModSts_Off', '0x1': ' TrlrModSts_On'}

    class URawBCU1:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 880
        signal_description = "Voltage"
        signal_length = 9
        start_position = 1860
        value_definition = {}

    class URawBCU2:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 895
        signal_description = "Voltage"
        signal_length = 9
        start_position = 1867
        value_definition = {}

    class URawCCUCD:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 894
        signal_description = "Voltage"
        signal_length = 9
        start_position = 1874
        value_definition = {}

    class URawPSCM2:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 893
        signal_description = "Voltage"
        signal_length = 9
        start_position = 1881
        value_definition = {}

    class UsrInCarSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 892
        signal_description = "user in car"
        signal_length = 1
        start_position = 1888
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class VehChrgnSts:
        comments = ""
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 891
        signal_description = "Vehicle charging status (reported for GB/T 32960) "
        signal_length = 3
        start_position = 2407
        value_definition = {'0x0': ' ChrgnSts_Fault', '0x1': ' ChrgnSts_ChargingInParkingState', '0x2': ' ChrgnSts_ChargingInDrivingState', '0x3': ' ChrgnSts_NotCharging', '0x4': ' ChrgnSts_ChargingCompleted', '0x5': ' ChrgnSts_Invalid', '0x6': ' ChrgnSts_Reserved1', '0x7': ' ChrgnSts_Reserved2'}

    class VehDateAndTiSec:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 890
        signal_description = "Second:[0,59]"
        signal_length = 6
        start_position = 2415
        value_definition = {}

    class VehDateAndTiValid:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 890
        signal_description = "Validity: 0 invalid, 1 valid"
        signal_length = 1
        start_position = 2445
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class VehDateAndTiDay:
        comments = ""
        factor = 1.0
        initial_value = 2
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 890
        signal_description = "Day: [1,31]"
        signal_length = 5
        start_position = 2434
        value_definition = {}

    class VehDateAndTiYr:
        comments = ""
        factor = 1.0
        initial_value = 21
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 890
        signal_description = "Year: 21 to 99, i.e., 2021 to 2099"
        signal_length = 8
        start_position = 2431
        value_definition = {}

    class VehDateAndTiHr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 890
        signal_description = "Hour:[0,23]"
        signal_length = 5
        start_position = 2439
        value_definition = {}

    class VehDateAndTiMins:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 890
        signal_description = "Minute:[0,59]"
        signal_length = 6
        start_position = 2409
        value_definition = {}

    class VehDateAndTiMth:
        comments = ""
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 890
        signal_description = "Month:1 to 12"
        signal_length = 4
        start_position = 2419
        value_definition = {}

    class WirelessChrgnFltHwSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Wireless charging hardware fault status"
        signal_length = 2
        start_position = 2455
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class WirelessChrgnFltHwStsPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 888
        signal_description = "Wireless charging hardware fault status of passenger side"
        signal_length = 2
        start_position = 2453
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class WirelessChrgnFltPwrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Wireless charging power fault status"
        signal_length = 2
        start_position = 2451
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class WirelessChrgnFltPwrStsPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 902
        signal_description = "Wireless charging Power fault status of passenger side"
        signal_length = 2
        start_position = 2449
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class WirelessChrgnFltTSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Wireless charging temperature fault status"
        signal_length = 2
        start_position = 2463
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class WirelessChrgnFltTStsPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 900
        signal_description = "Wireless charging temperature fault status of passenger side"
        signal_length = 2
        start_position = 2461
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class WirelessChrgnFltUSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 899
        signal_description = "Wireless charging voltage fault status"
        signal_length = 2
        start_position = 2459
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class WirelessChrgnFltUStsPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 898
        signal_description = "Wireless charging voltage fault status of passenger side"
        signal_length = 2
        start_position = 2457
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class WirelsChrgnCoolgFanSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 897
        signal_description = "Wireless charging cooling fan status"
        signal_length = 1
        start_position = 2444
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class WirelsChrgnCoolgFanStsPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 896
        signal_description = "Wireless charging cooling fan status of passenger side"
        signal_length = 1
        start_position = 2471
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class WirelsChrgnModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2442
        signal_description = "Wireless charging mode status"
        signal_length = 3
        start_position = 2470
        value_definition = {'0x0': ' WirelsChrgnModSts_Standby', '0x1': ' WirelsChrgnModSts_Charging', '0x2': ' WirelsChrgnModSts_QFOD', '0x3': ' WirelsChrgnModSts_PFOD', '0x4': ' WirelsChrgnModSts_CardProt', '0x5': ' WirelsChrgnModSts_PhoneForgotten', '0x6': ' WirelsChrgnModSts_Reserved1', '0x7': ' WirelsChrgnModSts_Reserved2'}

    class WirelsChrgnModStsPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2441
        signal_description = "Wireless charging mode status of passenger side"
        signal_length = 3
        start_position = 2467
        value_definition = {'0x0': ' WirelsChrgnModSts_Standby', '0x1': ' WirelsChrgnModSts_Charging', '0x2': ' WirelsChrgnModSts_QFOD', '0x3': ' WirelsChrgnModSts_PFOD', '0x4': ' WirelsChrgnModSts_CardProt', '0x5': ' WirelsChrgnModSts_PhoneForgotten', '0x6': ' WirelsChrgnModSts_Reserved1', '0x7': ' WirelsChrgnModSts_Reserved2'}

    class WirelsChrgnSetFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2440
        signal_description = "Wireless charging setup feedback"
        signal_length = 1
        start_position = 2464
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class WirelsChrgnSetFbPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2401
        signal_description = "Wireless charging setup feedback of passenger side"
        signal_length = 1
        start_position = 2443
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class GearDispFedBck:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1457
        signal_description = "The large screen displays the CRC check and the feedback of the check result"
        signal_length = 3
        start_position = 1460
        value_definition = {'0x0': ' GearFltSts_Normal', '0x1': ' GearFltSts_PFlt', '0x2': ' GearFltSts_RFlt', '0x3': ' GearFltSts_NFlt', '0x4': ' GearFltSts_DFlt', '0x5': ' GearFltSts_SrvReq', '0x6': ' GearFltSts_Reserved1', '0x7': ' GearFltSts_Reserved2'}

    class FrntScrnWorkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1673
        signal_description = "Describe the front Screen working Status"
        signal_length = 3
        start_position = 1676
        value_definition = {'0x0': ' FrntScrnWorkSts_Unknow', '0x1': ' FrntScrnWorkSts_Start_up', '0x2': ' FrntScrnWorkSts_Shut_down', '0x3': ' FrntScrnWorkSts_Work_On', '0x4': ' FrntScrnWorkSts_Reserve1', '0x5': ' FrntScrnWorkSts_Reserve2', '0x6': ' FrntScrnWorkSts_Reserve3', '0x7': ' FrntScrnWorkSts_Reserve4'}

    class FotaModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 993
        signal_description = ""
        signal_length = 8
        start_position = 1007
        value_definition = {'0x0': ' FotaModStsType_Idle', '0x1': ' FotaModStsType_Update', '0x2': ' FotaModStsType_UpdateFail'}

    class FrntEndAirFlwEstimd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2065
        signal_description = "CRFM inlet air flow estimate "
        signal_length = 14
        start_position = 2063
        value_definition = {}

    class LuminanceLevelFedBck:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2064
        signal_description = "The front srceen real brightness to feedback"
        signal_length = 8
        start_position = 2079
        value_definition = {'0xFF': 'BattSOH_Invalid'}

    class MuteReqSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1907
        signal_description = "Mute require status to CD"
        signal_length = 1
        start_position = 1908
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class RTPReqSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1905
        signal_description = "RTP and audio require status to CD"
        signal_length = 1
        start_position = 1906
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ThisAlarmTimestamp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2051
        signal_description = "the timestamp of this alarm event"
        signal_length = 64
        start_position = 2087
        value_definition = {}

    class InhbHvOn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2146
        signal_description = "Inhibit HV on flag"
        signal_length = 2
        start_position = 2151
        value_definition = {'0x0': ' NoYesUkwn_No', '0x1': ' NoYesUkwn_Yes', '0x2': ' NoYesUkwn_Unknown', '0x3': ' NoYesUkwn_Reserved'}

    class InhbPrpsnRdy:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2147
        signal_description = "Inhibit PTReady flag"
        signal_length = 2
        start_position = 2149
        value_definition = {'0x0': ' NoYesUkwn_No', '0x1': ' NoYesUkwn_Yes', '0x2': ' NoYesUkwn_Unknown', '0x3': ' NoYesUkwn_Reserved'}

    class DCChrgrIsoUMax:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2145
        signal_description = "DC charging pile insulation test highest voltage"
        signal_length = 16
        start_position = 2159
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204002
    pdu_length_bytes = 64
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-10ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'AccrPedlPsd': ['AccrPedlPsdCntr', 'AccrPedlPsdAccrPedlPsd', 'AccrPedlPsdChks', 'AccrPedlPsdSafe'], 'AccrPedlVal': ['AccrPedlValCntr', 'AccrPedlValPedlFild', 'AccrPedlValChks'], 'FrntMotSpdActSafe': ['FrntMotSpdActSafeMotorSpdActSafe', 'FrntMotSpdActSafeCntr', 'FrntMotSpdActSafeChks', 'FrntMotSpdActSafeQf'], 'FrntMotTqAct': ['FrntMotTqActChks', 'FrntMotTqActTqQf', 'FrntMotTqActCntr', 'FrntMotTqActTq'], 'ReMotSpdActSafe': ['ReMotSpdActSafeChks', 'ReMotSpdActSafeCntr', 'ReMotSpdActSafeMotorSpdActSafe', 'ReMotSpdActSafeQf'], 'ReMotTqAct': ['ReMotTqActTq', 'ReMotTqActTqQf', 'ReMotTqActCntr', 'ReMotTqActChks'], 'WhlSpdFrnt': ['WhlSpdFrntRiQf', 'WhlSpdFrntLeSpd', 'WhlSpdFrntRiSpd', 'WhlSpdFrntLeQf', 'WhlSpdFrntCntr', 'WhlSpdFrntChks'], 'WhlSpdRe': ['WhlSpdReLeQf', 'WhlSpdReRiSpd', 'WhlSpdReLeSpd', 'WhlSpdReChks', 'WhlSpdReCntr', 'WhlSpdReRiQf'], 'PrpsnSysModSts': ['PrpsnSysModStsChks', 'PrpsnSysModStsPrpsnModSt', 'PrpsnSysModStsCntr']}

    class AccrPedlPsdCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 24
        signal_description = "couner"
        signal_length = 4
        start_position = 11
        value_definition = {}

    class AccrPedlPsdAccrPedlPsd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 24
        signal_description = "Describes if the accelerator pedal is pressed. Will indicate pressed for a small pedal press. Accompanying status signal will indicate the integrity of the information."
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' NoYesInitial_Initial', '0x1': ' NoYesInitial_No', '0x2': ' NoYesInitial_Yes'}

    class AccrPedlPsdChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 24
        signal_description = "checksum"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class AccrPedlPsdSafe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 24
        signal_description = "Describes if the accelerator pedal is pressed. Will indicate pressed for a small pedal press. Accompanying status signal will indicate the integrity of the information. AccrPedlPsd fulfills ASIL C integrity"
        signal_length = 2
        start_position = 13
        value_definition = {'0x0': ' NoYesInitial_Initial', '0x1': ' NoYesInitial_No', '0x2': ' NoYesInitial_Yes'}

    class AccrPedlTqReq:
        comments = ""
        factor = 1.0
        initial_value = 15000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -15000
        sig_ub = 60
        signal_description = "Torque request from driver via accelerator pedal."
        signal_length = 15
        start_position = 23
        value_definition = {}

    class AccrPedlValCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "Counter"
        signal_length = 4
        start_position = 47
        value_definition = {}

    class AccrPedlValPedlFild:
        comments = ""
        factor = 0.00390625
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "Accelerator Pedal Position with adapted 0 point. Value as percentage of fully pressed pedal"
        signal_length = 15
        start_position = 43
        value_definition = {}

    class AccrPedlValChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "Checksum"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class FrntMotSpdAct:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 58
        signal_description = "The actual rotational speed of FMCU"
        signal_length = 16
        start_position = 71
        value_definition = {}

    class FrntMotSpdActSafeMotorSpdActSafe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "The safe rotational speed of FMCU"
        signal_length = 16
        start_position = 103
        value_definition = {}

    class FrntMotSpdActSafeCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "Counter"
        signal_length = 4
        start_position = 95
        value_definition = {}

    class FrntMotSpdActSafeChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "Checksum"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class FrntMotSpdActSafeQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "Quality Factor"
        signal_length = 2
        start_position = 91
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class FrntMotTqActChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 56
        signal_description = "checksum"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class FrntMotTqActTqQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 56
        signal_description = "quality factor"
        signal_length = 2
        start_position = 123
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class FrntMotTqActCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 56
        signal_description = "counter"
        signal_length = 4
        start_position = 127
        value_definition = {}

    class FrntMotTqActTq:
        comments = ""
        factor = 1.0
        initial_value = 15000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -15000
        sig_ub = 56
        signal_description = "Estimation torque of Frnt Axle Control"
        signal_length = 15
        start_position = 121
        value_definition = {}

    class PedProtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 138
        signal_description = "Pedestrain protection status"
        signal_length = 2
        start_position = 151
        value_definition = {'0x0': ' PedProtnSts_Invalid', '0x1': ' PedProtnSts_NotActvn', '0x2': ' PedProtnSts_Actvn', '0x3': ' PedProtnSts_Error'}

    class PrpnSysStrtDlyInhbMsg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 137
        signal_description = "Vehicle start warning message"
        signal_length = 3
        start_position = 149
        value_definition = {'0x0': ' PrpnSysStrtMsg_NoInhb', '0x1': ' PrpnSysStrtMsg_StrtDly', '0x2': ' PrpnSysStrtMsg_InhbRemStrt', '0x3': ' PrpnSysStrtMsg_DiRemStrt', '0x4': ' PrpnSysStrtMsg_SelParkOrNeut', '0x5': ' PrpnSysStrtMsg_Resd1', '0x6': ' PrpnSysStrtMsg_Resd2'}

    class ReMotSpdAct:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 136
        signal_description = "The actual rotational speed of PDCU Motor"
        signal_length = 16
        start_position = 167
        value_definition = {}

    class ReMotSpdActSafeChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 234
        signal_description = "Checksum"
        signal_length = 8
        start_position = 183
        value_definition = {}

    class ReMotSpdActSafeCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 234
        signal_description = "Counter"
        signal_length = 4
        start_position = 191
        value_definition = {}

    class ReMotSpdActSafeMotorSpdActSafe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 234
        signal_description = "The safe rotational speed of PDCU Motor"
        signal_length = 16
        start_position = 199
        value_definition = {}

    class ReMotSpdActSafeQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 234
        signal_description = "Quality Factor"
        signal_length = 2
        start_position = 187
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class ReMotTqActTq:
        comments = ""
        factor = 1.0
        initial_value = 15000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -15000
        sig_ub = 233
        signal_description = "Estimation torque of Rear Axle Control"
        signal_length = 15
        start_position = 217
        value_definition = {}

    class ReMotTqActTqQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 233
        signal_description = "quality factor"
        signal_length = 2
        start_position = 219
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class ReMotTqActCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 233
        signal_description = "counter"
        signal_length = 4
        start_position = 223
        value_definition = {}

    class ReMotTqActChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 233
        signal_description = "checksum"
        signal_length = 8
        start_position = 215
        value_definition = {}

    class RestrntSysSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 232
        signal_description = "Restraint system status"
        signal_length = 3
        start_position = 146
        value_definition = {'0x0': ' RestrntSysSts_Invalid', '0x1': ' RestrntSysSts_Normal', '0x2': ' RestrntSysSts_Fault_Level1', '0x3': ' RestrntSysSts_Fault_Level2', '0x4': ' RestrntSysSts_Fault_Level3', '0x5': ' RestrntSysSts_Others'}

    class WhlSpdFrntRiQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Qf for wheel speed sensor"
        signal_length = 2
        start_position = 249
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class WhlSpdFrntLeSpd:
        comments = ""
        factor = 0.00391
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Individual wheel speed from front wheel speed sensors, fl"
        signal_length = 15
        start_position = 263
        value_definition = {}

    class WhlSpdFrntRiSpd:
        comments = ""
        factor = 0.00391
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Individual wheel speed from front wheel speed sensors, fr"
        signal_length = 15
        start_position = 279
        value_definition = {}

    class WhlSpdFrntLeQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Qf for wheel speed sensor"
        signal_length = 2
        start_position = 251
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class WhlSpdFrntCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "counter"
        signal_length = 4
        start_position = 255
        value_definition = {}

    class WhlSpdFrntChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "crc"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class WhlSpdReLeQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 352
        signal_description = "Qf for wheel speed sensor"
        signal_length = 2
        start_position = 323
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class WhlSpdReRiSpd:
        comments = ""
        factor = 0.00391
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 352
        signal_description = "Individual wheel speed from rear wheel speed sensors. rr"
        signal_length = 15
        start_position = 351
        value_definition = {}

    class WhlSpdReLeSpd:
        comments = ""
        factor = 0.00391
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 352
        signal_description = "Individual wheel speed from rear wheel speed sensors. rl"
        signal_length = 15
        start_position = 335
        value_definition = {}

    class WhlSpdReChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 352
        signal_description = "crc"
        signal_length = 8
        start_position = 319
        value_definition = {}

    class WhlSpdReCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 352
        signal_description = "counter"
        signal_length = 4
        start_position = 327
        value_definition = {}

    class WhlSpdReRiQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 352
        signal_description = "Qf for wheel speed sensor"
        signal_length = 2
        start_position = 321
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class AccrPedlValIntgr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 367
        signal_description = "Accelerator pedal opening value, accuracy 1percentage, GB32960,reported.0xFE indicates abnormal, 0xFF indicates invalid."
        signal_length = 8
        start_position = 295
        value_definition = {}

    class CrpTqReq:
        comments = ""
        factor = 1.0
        initial_value = 15000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -15000
        sig_ub = 304
        signal_description = "Creep required torque"
        signal_length = 15
        start_position = 303
        value_definition = {}

    class HVInhbReqFromSrvFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 157
        signal_description = "Fedback HV Inhibit require from service"
        signal_length = 2
        start_position = 159
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}

    class PrpsnSysModStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 376
        signal_description = "Checksum"
        signal_length = 8
        start_position = 375
        value_definition = {}

    class PrpsnSysModStsPrpsnModSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 376
        signal_description = "Power system mode status."
        signal_length = 3
        start_position = 379
        value_definition = {'0x0': ' PrpsnSysSts_initialize', '0x1': ' PrpsnSysSts_Awake', '0x2': ' PrpsnSysSts_Ready', '0x3': ' PrpsnSysSts_Standby', '0x4': ' PrpsnSysSts_Running', '0x5': ' PrpsnSysSts_AftRun', '0x6': ' PrpsnSysSts_Reserved1', '0x7': ' PrpsnSysSts_Reserved2'}

    class PrpsnSysModStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 376
        signal_description = "Counter"
        signal_length = 4
        start_position = 383
        value_definition = {}

    class HvSysActvSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 361
        signal_description = "The high-pressure system is active "
        signal_length = 2
        start_position = 363
        value_definition = {'0x0': ' HvSysActvSts_Default', '0x1': ' HvSysActvSts_CtrldSplyIsActivated', '0x2': ' HvSysActvSts_CtrldSplyPlusContactorsIsActivated', '0x3': ' HvSysActvSts_Error'}

    class DrvrGearShiftEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 364
        signal_description = "Shifting system feedback whether the shifting conditions are met (braking, speed, charging gun, etc.). 0: Not satisfied, 1: Yes"
        signal_length = 2
        start_position = 366
        value_definition = {'0x0': ' EnaDsblDefault_Default', '0x1': ' EnaDsblDefault_Enable', '0x2': ' EnaDsblDefault_Disable', '0x3': ' EnaDsblDefault_Reserved'}

    class VehSpdLimnTqReq:
        comments = ""
        factor = 1.0
        initial_value = 15000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -15000
        sig_ub = 392
        signal_description = "The speed limit requires torque "
        signal_length = 15
        start_position = 391
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204001
    pdu_length_bytes = 27
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-40ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'AbsFctSts': ['AbsFctStsActv', 'AbsFctStsChks', 'AbsFctStsEna', 'AbsFctStsCntr', 'AbsFctStsSts2'], 'AvhSts': ['AvhStsActv', 'AvhStsCntr', 'AvhStsEna', 'AvhStsChks', 'AvhStsSts2'], 'BrkSysWarnReq': ['BrkSysWarnReqBrkSysWarn', 'BrkSysWarnReqChks', 'BrkSysWarnReqCntr'], 'CdpSts': ['CdpStsActv', 'CdpStsCntr', 'CdpStsChks', 'CdpStsEna', 'CdpStsSts2'], 'CrbSts': ['CrbStsChks', 'CrbStsEna', 'CrbStsActv', 'CrbStsCntr', 'CrbStsSts2'], 'CstSts': ['CstStsEna', 'CstStsChks', 'CstStsActv', 'CstStsCntr', 'CstStsSts2'], 'DsrSts': ['DsrStsEna', 'DsrStsActv', 'DsrStsCntr', 'DsrStsChks', 'DsrStsSts2'], 'HdcSts': ['HdcStsChks', 'HdcStsEna', 'HdcStsCntr', 'HdcStsActv', 'HdcStsSts2'], 'SsmStsByBrk': ['SsmStsByBrkStandstilMgrSts', 'SsmStsByBrkChks', 'SsmStsByBrkCntr']}

    class AbsFctStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "ABS function active information"
        signal_length = 2
        start_position = 23
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class AbsFctStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "CRC"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class AbsFctStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "ABS function enable information"
        signal_length = 1
        start_position = 12
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class AbsFctStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "Counter"
        signal_length = 4
        start_position = 11
        value_definition = {}

    class AbsFctStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "function status"
        signal_length = 3
        start_position = 15
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class AvhLampReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 67
        signal_description = "Avh driver indication request"
        signal_length = 2
        start_position = 21
        value_definition = {'0x0': ' BrkLamp3_Off', '0x1': ' BrkLamp3_Standby', '0x2': ' BrkLamp3_Active', '0x3': ' BrkLamp3_Fault'}

    class AvhMsgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 66
        signal_description = "Avh msg request"
        signal_length = 3
        start_position = 19
        value_definition = {'0x0': ' AvhMsg_NoMsg', '0x1': ' AvhMsg_StandbyOn', '0x2': ' AvhMsg_ActiveOn', '0x3': ' AvhMsg_BrkPedlToRel', '0x4': ' AvhMsg_Fault', '0x5': ' AvhMsg_Reserved'}

    class AvhStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "Avh function active information"
        signal_length = 2
        start_position = 47
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class AvhStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "counter"
        signal_length = 4
        start_position = 35
        value_definition = {}

    class AvhStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "Avh function enable information"
        signal_length = 1
        start_position = 36
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class AvhStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "crc"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class AvhStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "function status"
        signal_length = 3
        start_position = 39
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class BrkSysWarnMsgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "Brake system Msg request"
        signal_length = 4
        start_position = 43
        value_definition = {'0x0': ' BrkMsg_NoMsg', '0x1': ' BrkMsg_EbdFault', '0x2': ' BrkMsg_AbsFault', '0x3': ' BrkMsg_EscFault', '0x4': ' BrkMsg_EscOff', '0x5': ' BrkMsg_TcsOff', '0x6': ' BrkMsg_Reduced', '0x7': ' BrkMsg_Reserved'}

    class BrkSysWarnReqBrkSysWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 90
        signal_description = " Yellow Brake Warning Tell tale request"
        signal_length = 1
        start_position = 59
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class BrkSysWarnReqChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 90
        signal_description = "crc"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class BrkSysWarnReqCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 90
        signal_description = "counter"
        signal_length = 4
        start_position = 63
        value_definition = {}

    class BrySysOvrheated:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 89
        signal_description = "brake system overheated"
        signal_length = 1
        start_position = 58
        value_definition = {'0x0': ' NoYes1_No', '0x1': ' NoYes1_Yes'}

    class BTCActvFrnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 88
        signal_description = "BTC function front axle active information"
        signal_length = 2
        start_position = 57
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class BTCActvRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 114
        signal_description = "BTC function rear axle active information"
        signal_length = 2
        start_position = 71
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class CbcActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 113
        signal_description = "Cbc function active information"
        signal_length = 2
        start_position = 69
        value_definition = {'0x0': ' ActvInActv2_Init', '0x1': ' ActvInActv2_InActv', '0x2': ' ActvInActv2_Actv'}

    class CdpStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Cdp function active information"
        signal_length = 2
        start_position = 95
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class CdpStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "counter"
        signal_length = 4
        start_position = 83
        value_definition = {}

    class CdpStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "crc"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class CdpStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Cdp function enable information"
        signal_length = 1
        start_position = 84
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class CdpStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "function status"
        signal_length = 3
        start_position = 87
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class CrbStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 117
        signal_description = "crc"
        signal_length = 8
        start_position = 103
        value_definition = {}

    class CrbStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 117
        signal_description = "Crb function enable information"
        signal_length = 1
        start_position = 108
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class CrbStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 117
        signal_description = "Crb function active information"
        signal_length = 2
        start_position = 119
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class CrbStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 117
        signal_description = "counter"
        signal_length = 4
        start_position = 107
        value_definition = {}

    class CrbStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 117
        signal_description = "function status"
        signal_length = 3
        start_position = 111
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class CstStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 112
        signal_description = "Cst function enable information"
        signal_length = 1
        start_position = 132
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class CstStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 112
        signal_description = "crc"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class CstStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 112
        signal_description = "Cst function active information"
        signal_length = 2
        start_position = 143
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class CstStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 112
        signal_description = "counter"
        signal_length = 4
        start_position = 131
        value_definition = {}

    class CstStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 112
        signal_description = "function status"
        signal_length = 3
        start_position = 135
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class DsrStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 165
        signal_description = "Dsr function enable information"
        signal_length = 1
        start_position = 156
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class DsrStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 165
        signal_description = "Dsr function active information"
        signal_length = 2
        start_position = 167
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class DsrStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 165
        signal_description = "counter"
        signal_length = 4
        start_position = 155
        value_definition = {}

    class DsrStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 165
        signal_description = "CRC"
        signal_length = 8
        start_position = 151
        value_definition = {}

    class DsrStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 165
        signal_description = "function status"
        signal_length = 3
        start_position = 159
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class DTCActvFrnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 161
        signal_description = "Dtc function active information for front axle"
        signal_length = 2
        start_position = 45
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class DTCActvRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 160
        signal_description = "Dtc function active information for rear axle"
        signal_length = 2
        start_position = 92
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class HdcLampReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 141
        signal_description = "Hdc driver indication request"
        signal_length = 2
        start_position = 116
        value_definition = {'0x0': ' BrkLamp3_Off', '0x1': ' BrkLamp3_Standby', '0x2': ' BrkLamp3_Active', '0x3': ' BrkLamp3_Fault'}

    class HdcMsgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 140
        signal_description = "Hdc Msg request"
        signal_length = 3
        start_position = 164
        value_definition = {'0x0': ' HdcMsg_NoReq', '0x1': ' HdcMsg_StandbyOn', '0x2': ' HdcMsg_ActiveOn', '0x3': ' HdcMsg_Fault', '0x4': ' HdcMsg_TempOff', '0x5': ' HdcMsg_Reserved'}

    class HdcStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "crc"
        signal_length = 8
        start_position = 175
        value_definition = {}

    class HdcStsEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "Hdc function enable information"
        signal_length = 1
        start_position = 180
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class HdcStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "counter"
        signal_length = 4
        start_position = 179
        value_definition = {}

    class HdcStsActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "Hdc function active information"
        signal_length = 2
        start_position = 191
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class HdcStsSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "function status"
        signal_length = 3
        start_position = 183
        value_definition = {'0x0': ' Sts2_Initial', '0x1': ' Sts2_Normal', '0x2': ' Sts2_Fault', '0x3': ' Sts2_Off'}

    class SsmStsByBrkStandstilMgrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 200
        signal_description = "Brake system hold status"
        signal_length = 3
        start_position = 203
        value_definition = {'0x0': ' StandstilMgrSts_Val0', '0x1': ' StandstilMgrSts_Val1', '0x2': ' StandstilMgrSts_Val2', '0x3': ' StandstilMgrSts_Val3', '0x4': ' StandstilMgrSts_Val4', '0x5': ' StandstilMgrSts_Val5', '0x6': ' StandstilMgrSts_Val6', '0x7': ' StandstilMgrSts_Val7'}

    class SsmStsByBrkChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 200
        signal_description = "crc"
        signal_length = 8
        start_position = 199
        value_definition = {}

    class SsmStsByBrkCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 200
        signal_description = "counter"
        signal_length = 4
        start_position = 207
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu08:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204008
    pdu_length_bytes = 150
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-50ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'DigKeyLiReq': ['DigKeyLiReqKeyIdByte4', 'DigKeyLiReqKeyIdByte15', 'DigKeyLiReqDigKeyApproachLightSts', 'DigKeyLiReqKeyIdByte7', 'DigKeyLiReqKeyIdByte12', 'DigKeyLiReqKeyIdByte8', 'DigKeyLiReqKeyIdByte3', 'DigKeyLiReqKeyIdByte1', 'DigKeyLiReqKeyIdByte10', 'DigKeyLiReqKeyIdByte14', 'DigKeyLiReqKeyIdByte2', 'DigKeyLiReqKeyIdByte5', 'DigKeyLiReqKeyIdByte11', 'DigKeyLiReqKeyIdByte13', 'DigKeyLiReqKeyTyp', 'DigKeyLiReqKeyIdByte0', 'DigKeyLiReqKeyIdByte9', 'DigKeyLiReqKeyIdByte6'], 'HVBattCellU': ['HVBattCellUUMaxId', 'HVBattCellUUMin', 'HVBattCellUUMinId', 'HVBattCellUUMax'], 'HVBattPackSOCLim': ['HVBattPackSOCLimMin', 'HVBattPackSOCLimMax', 'HVBattPackSOCLimLow', 'HVBattPackSOCLimHi'], 'KeyFindRespToService': ['KeyFindRespToServiceKeyIdByte11', 'KeyFindRespToServiceKeyIdByte7', 'KeyFindRespToServiceKeyTyp', 'KeyFindRespToServiceKeyIdByte4', 'KeyFindRespToServiceKeyIdByte5', 'KeyFindRespToServiceKeyIdByte9', 'KeyFindRespToServiceKeyIdByte3', 'KeyFindRespToServiceKeyIdByte14', 'KeyFindRespToServiceKeyIdByte15', 'KeyFindRespToServiceKeyIdByte2', 'KeyFindRespToServiceKeyIdByte13', 'KeyFindRespToServiceKeyIdByte10', 'KeyFindRespToServiceKeyFindSts', 'KeyFindRespToServiceKeyIdByte6', 'KeyFindRespToServiceKeyIdByte8', 'KeyFindRespToServiceKeyLocnSts', 'KeyFindRespToServiceKeyIdByte1', 'KeyFindRespToServiceKeyIdByte0', 'KeyFindRespToServiceKeyIdByte12'], 'OdometerHiResl': ['OdometerHiReslValidity', 'OdometerHiReslvalue'], 'SeatOccpSts': ['SeatOccpStsSecRowLeSeatSts', 'SeatOccpStsSecRowMidSeatSts', 'SeatOccpStsThrdRowLeSeatSts', 'SeatOccpStsThrdRowMidSeatSts', 'SeatOccpStsThrdRowRiSeatSts', 'SeatOccpStsDrvrSeatSts', 'SeatOccpStsPassSeatSts', 'SeatOccpStsSecRowRiSeatSts'], 'DimSts': ['DimStsCntr', 'DimStsChks', 'DimStsSts'], 'DCDCActILoSide': ['DCDCActILoSideDCDCILowside', 'DCDCActILoSideChks', 'DCDCActILoSideCntr'], 'ScreenICSts': ['ScreenICStsSts', 'ScreenICStsCntr', 'ScreenICStsChks']}

    class BoostStsFb1:
        comments = ""
        factor = 1.0
        initial_value = 7
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 159
        signal_description = "Electric drive boost state"
        signal_length = 3
        start_position = 7
        value_definition = {'0x0': ' BoostSt_Init', '0x1': ' BoostSt_C1Precharge', '0x2': ' BoostSt_BoostReady', '0x3': ' BoostSt_BoostActive', '0x4': ' BoostSt_C1activedischarge', '0x5': ' BoostSt_Fault', '0x6': ' BoostSt_Derating', '0x7': ' BoostSt_BoostOff'}

    class DigKeyLiReqKeyIdByte4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte4"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class DigKeyLiReqKeyIdByte15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte15"
        signal_length = 8
        start_position = 143
        value_definition = {}

    class DigKeyLiReqDigKeyApproachLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Indicate if welcome light is activated"
        signal_length = 1
        start_position = 12
        value_definition = {'0x0': ' EnableDisable2_Disabled', '0x1': ' EnableDisable2_Enabled'}

    class DigKeyLiReqKeyIdByte7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte7"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class DigKeyLiReqKeyIdByte12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte12"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class DigKeyLiReqKeyIdByte8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte8"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class DigKeyLiReqKeyIdByte3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte3"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class DigKeyLiReqKeyIdByte1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte1"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class DigKeyLiReqKeyIdByte10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte10"
        signal_length = 8
        start_position = 103
        value_definition = {}

    class DigKeyLiReqKeyIdByte14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte14"
        signal_length = 8
        start_position = 135
        value_definition = {}

    class DigKeyLiReqKeyIdByte2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte2"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class DigKeyLiReqKeyIdByte5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte5"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class DigKeyLiReqKeyIdByte11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte11"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class DigKeyLiReqKeyIdByte13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte13"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class DigKeyLiReqKeyTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Key type info"
        signal_length = 4
        start_position = 11
        value_definition = {'0x0': ' KeyTyp_NoKeyConnected', '0x1': ' KeyTyp_NFC_Card', '0x2': ' KeyTyp_BLE_UWB_KeyFob', '0x3': ' KeyTyp_Phone_NFC_Key', '0x4': ' KeyTyp_Phone_BLE_Key', '0x5': ' KeyTyp_Phone_UWB_Key', '0x6': ' KeyTyp_Reserved1', '0x7': ' KeyTyp_Reserved2', '0x8': ' KeyTyp_Reserved3', '0x9': ' KeyTyp_Reserved4'}

    class DigKeyLiReqKeyIdByte0:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte0"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class DigKeyLiReqKeyIdByte9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte9"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class DigKeyLiReqKeyIdByte6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Keyid byte6"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class HVBattCellUUMaxId:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "The ID of HV  battery  maximum cell voltage ."
        signal_length = 8
        start_position = 167
        value_definition = {}

    class HVBattCellUUMin:
        comments = ""
        factor = 0.001
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "The minimum cell  voltage of HV battery pack."
        signal_length = 13
        start_position = 175
        value_definition = {}

    class HVBattCellUUMinId:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "The ID of HV battery minimum cell  voltage."
        signal_length = 8
        start_position = 191
        value_definition = {}

    class HVBattCellUUMax:
        comments = ""
        factor = 0.001
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "The maximum cell  voltage of HV battery pack."
        signal_length = 13
        start_position = 199
        value_definition = {}

    class HVBattPackEgyAvlChrg:
        comments = ""
        factor = 20.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 15
        signal_description = "Usable charge energy up to HV battery pack SOC Max limit."
        signal_length = 13
        start_position = 202
        value_definition = {}

    class HVBattPackEgyAvlDcha:
        comments = ""
        factor = 20.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 14
        signal_description = "Usable discharge energy down to HV battery pack SOC Min limit."
        signal_length = 13
        start_position = 221
        value_definition = {}

    class HVBattPackILim:
        comments = ""
        factor = 0.1
        initial_value = 30000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -3000
        sig_ub = 13
        signal_description = "HV battery pack charging current limit."
        signal_length = 16
        start_position = 239
        value_definition = {}

    class HVBattPackOverDchaFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 151
        signal_description = "HV battery pack over discharge flag."
        signal_length = 2
        start_position = 255
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}

    class HVBattPackSOC:
        comments = ""
        factor = 0.05
        initial_value = 2040
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 150
        signal_description = "The actual state of charge of the HV battery pack."
        signal_length = 11
        start_position = 253
        value_definition = {}

    class HVBattPackSOCLimMin:
        comments = ""
        factor = 0.05
        initial_value = 2040
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 149
        signal_description = "The Minimum allowable state of charge of the HV battery pack.Used for protection of HV battery system."
        signal_length = 11
        start_position = 258
        value_definition = {}

    class HVBattPackSOCLimMax:
        comments = ""
        factor = 0.05
        initial_value = 2040
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 149
        signal_description = "The Maximum allowable state of charge of the HV battery pack.Used for protection of HV battery system."
        signal_length = 11
        start_position = 279
        value_definition = {}

    class HVBattPackSOCLimLow:
        comments = ""
        factor = 0.05
        initial_value = 2040
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 149
        signal_description = "The low  allowable state of charge of the HV battery pack."
        signal_length = 11
        start_position = 284
        value_definition = {}

    class HVBattPackSOCLimHi:
        comments = ""
        factor = 0.05
        initial_value = 2040
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 149
        signal_description = "The high allowable state of charge of the HV battery pack."
        signal_length = 11
        start_position = 289
        value_definition = {}

    class HVBattPackULim:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 148
        signal_description = "The  maximum voltage limit of HV battery pack when plug-in charging."
        signal_length = 16
        start_position = 319
        value_definition = {}

    class ImobStsIEM:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 147
        signal_description = "engine immoblise status2"
        signal_length = 2
        start_position = 335
        value_definition = {'0x0': ' ImobSts_Undefd', '0x1': ' ImobSts_ImobNotPass', '0x2': ' ImobSts_ImobPass', '0x3': ' ImobSts_ImobRemPass'}

    class ImobStsVCU:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 146
        signal_description = "engine immoblise status1"
        signal_length = 2
        start_position = 333
        value_definition = {'0x0': ' ImobSts_Undefd', '0x1': ' ImobSts_ImobNotPass', '0x2': ' ImobSts_ImobPass', '0x3': ' ImobSts_ImobRemPass'}

    class KeyFindRespToServiceKeyIdByte11:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte11"
        signal_length = 8
        start_position = 455
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte7"
        signal_length = 8
        start_position = 423
        value_definition = {}

    class KeyFindRespToServiceKeyTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "key type"
        signal_length = 4
        start_position = 355
        value_definition = {'0x0': ' KeyTyp_NoKeyConnected', '0x1': ' KeyTyp_NFC_Card', '0x2': ' KeyTyp_BLE_UWB_KeyFob', '0x3': ' KeyTyp_Phone_NFC_Key', '0x4': ' KeyTyp_Phone_BLE_Key', '0x5': ' KeyTyp_Phone_UWB_Key', '0x6': ' KeyTyp_Reserved1', '0x7': ' KeyTyp_Reserved2', '0x8': ' KeyTyp_Reserved3', '0x9': ' KeyTyp_Reserved4'}

    class KeyFindRespToServiceKeyIdByte4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte4"
        signal_length = 8
        start_position = 399
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte5"
        signal_length = 8
        start_position = 407
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte9:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte9"
        signal_length = 8
        start_position = 439
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte3"
        signal_length = 8
        start_position = 391
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte14"
        signal_length = 8
        start_position = 479
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte15:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte15"
        signal_length = 8
        start_position = 487
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte2"
        signal_length = 8
        start_position = 383
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte13:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte13"
        signal_length = 8
        start_position = 471
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte10"
        signal_length = 8
        start_position = 447
        value_definition = {}

    class KeyFindRespToServiceKeyFindSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Key Find Result"
        signal_length = 2
        start_position = 345
        value_definition = {'0x0': ' KeyPrsntSts_Idle', '0x1': ' KeyPrsntSts_InProgs', '0x2': ' KeyPrsntSts_NotPrsnt', '0x3': ' KeyPrsntSts_Prsnt'}

    class KeyFindRespToServiceKeyIdByte6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte6"
        signal_length = 8
        start_position = 415
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte8"
        signal_length = 8
        start_position = 431
        value_definition = {}

    class KeyFindRespToServiceKeyLocnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Feedback key zone consistent with key find request"
        signal_length = 4
        start_position = 359
        value_definition = {'0x0': ' KeyLocnReq_Idle', '0x1': ' KeyLocnReq_PEAllExtAndInt', '0x2': ' KeyLocnReq_PEAllExt', '0x3': ' KeyLocnReq_PEDrvrExt', '0x4': ' KeyLocnReq_PEPassExt', '0x5': ' KeyLocnReq_PEFrntExt', '0x6': ' KeyLocnReq_PERearExt', '0x7': ' KeyLocnReq_PEAllInt', '0x8': ' KeyLocnReq_PSAllInt', '0x9': ' KeyLocnReq_Reserved1', '0xA': ' KeyLocnReq_Reserved2'}

    class KeyFindRespToServiceKeyIdByte1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte1"
        signal_length = 8
        start_position = 375
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte0:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte0"
        signal_length = 8
        start_position = 367
        value_definition = {}

    class KeyFindRespToServiceKeyIdByte12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "Keyid byte12"
        signal_length = 8
        start_position = 463
        value_definition = {}

    class OdometerHiReslValidity:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 144
        signal_description = "Validity"
        signal_length = 1
        start_position = 488
        value_definition = {'0x0': ' Validity_NotValid', '0x1': ' Validity_Valid'}

    class OdometerHiReslvalue:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 144
        signal_description = "Vehicle OdometerHiResl,The Unit is Meter"
        signal_length = 32
        start_position = 503
        value_definition = {}

    class StrtMsg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 331
        signal_description = "Start Msg"
        signal_length = 8
        start_position = 343
        value_definition = {}

    class DCDCAvlIMaxLoSide:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1107
        signal_description = "Maximum available current for low voltage loads"
        signal_length = 12
        start_position = 1103
        value_definition = {}

    class SeatOccpStsSecRowLeSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1156
        signal_description = "Second row Left Seat Occupy Status"
        signal_length = 1
        start_position = 1165
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class SeatOccpStsSecRowMidSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1156
        signal_description = "Second row Mid Seat Occupy Status"
        signal_length = 1
        start_position = 1164
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class SeatOccpStsThrdRowLeSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1156
        signal_description = "Third row Left Seat Occupy Status"
        signal_length = 1
        start_position = 1162
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class SeatOccpStsThrdRowMidSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1156
        signal_description = "Third row Mid Seat Occupy Status"
        signal_length = 1
        start_position = 1161
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class SeatOccpStsThrdRowRiSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1156
        signal_description = "Third row Right Seat Occupy Status"
        signal_length = 1
        start_position = 1160
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class SeatOccpStsDrvrSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1156
        signal_description = "Driver Seat Occupy Status"
        signal_length = 1
        start_position = 1167
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class SeatOccpStsPassSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1156
        signal_description = "Passanger Seat Occupy Status"
        signal_length = 1
        start_position = 1166
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class SeatOccpStsSecRowRiSeatSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1156
        signal_description = "Second row Right Seat Occupy Status"
        signal_length = 1
        start_position = 1163
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class DCDCFltElecSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1115
        signal_description = "Electrical fault indication of DCDC"
        signal_length = 2
        start_position = 1119
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class DCDCFltTSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1114
        signal_description = "Temperature fault indication of DCDC"
        signal_length = 2
        start_position = 1117
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class DimStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1129
        signal_description = "Counter"
        signal_length = 4
        start_position = 1135
        value_definition = {}

    class DimStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1129
        signal_description = "Checksum"
        signal_length = 8
        start_position = 1127
        value_definition = {}

    class DimStsSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1129
        signal_description = "diming status"
        signal_length = 2
        start_position = 1131
        value_definition = {'0x0': ' DimmingSts_Off', '0x1': ' DimmingSts_Ready', '0x2': ' DimmingSts_Fault', '0x3': ' DimmingSts_Reserve'}

    class DCDCActILoSideDCDCILowside:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1106
        signal_description = "DCDC Actual output current on low side"
        signal_length = 12
        start_position = 1067
        value_definition = {}

    class DCDCActILoSideChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1106
        signal_description = "Checksum"
        signal_length = 8
        start_position = 1063
        value_definition = {}

    class DCDCActILoSideCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1106
        signal_description = "Counter"
        signal_length = 4
        start_position = 1071
        value_definition = {}

    class ScreenICStsSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1157
        signal_description = "Screen status"
        signal_length = 6
        start_position = 1147
        value_definition = {}

    class ScreenICStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1157
        signal_description = "counter"
        signal_length = 4
        start_position = 1151
        value_definition = {}

    class ScreenICStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1157
        signal_description = "checksum"
        signal_length = 8
        start_position = 1143
        value_definition = {}

    class DCDCActInpPwr:
        comments = ""
        factor = 10.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1092
        signal_description = "DCDC actual input power"
        signal_length = 11
        start_position = 1087
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu05:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204005
    pdu_length_bytes = 100
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-20ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'ElecGearShiftDevelpSignalGroup1': ['ElecGearShiftDevelpSignalGroup1DevelpSignalGroup8', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup6', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup2', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup7', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup4', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup1', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup3', 'ElecGearShiftDevelpSignalGroup1DevelpSignalGroup5'], 'ElecGearShiftDevelpSignalGroup2': ['ElecGearShiftDevelpSignalGroup2DevelpSignalGroup3', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup7', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup1', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup2', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup5', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup6', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup8', 'ElecGearShiftDevelpSignalGroup2DevelpSignalGroup4'], 'EpbLampReq': ['EpbLampReqCntr', 'EpbLampReqChks', 'EpbLampReqEpbLampReq'], 'EpbLampReqSec': ['EpbLampReqSecCntr', 'EpbLampReqSecChks', 'EpbLampReqSecEpbLampReq'], 'EpbTotSts': ['EpbTotStsCntr', 'EpbTotStsChks', 'EpbTotStsEpbSt'], 'HVBattThermRunAway': ['HVBattThermRunAwaySts', 'HVBattThermRunAwayErrSts'], 'HVMainRlySts': ['HVMainRlyStsMainRly1', 'HVMainRlyStsCntr', 'HVMainRlyStsChks'], 'ScreenTchIC': ['ScreenTchICSts', 'ScreenTchICChks', 'ScreenTchICCntr'], 'VehLgtAccelFromWhlSpd': ['VehLgtAccelFromWhlSpdLgt', 'VehLgtAccelFromWhlSpdChks', 'VehLgtAccelFromWhlSpdQf', 'VehLgtAccelFromWhlSpdCntr'], 'VehLgtAccelFromWhlSpdWithCmp': ['VehLgtAccelFromWhlSpdWithCmpCntr', 'VehLgtAccelFromWhlSpdWithCmpLgt', 'VehLgtAccelFromWhlSpdWithCmpQf', 'VehLgtAccelFromWhlSpdWithCmpChks'], 'VehSpdSafe': ['VehSpdSafeCntr', 'VehSpdSafeSpd', 'VehSpdSafeChks', 'VehSpdSafeQf'], 'WhlMovgDirFrnt': ['WhlMovgDirFrntChks', 'WhlMovgDirFrntCntr', 'WhlMovgDirFrntDirRi', 'WhlMovgDirFrntDirLe'], 'WhlMovgDirRe': ['WhlMovgDirReCntr', 'WhlMovgDirReDirLe', 'WhlMovgDirReDirRi', 'WhlMovgDirReChks'], 'VehMovgDir': ['VehMovgDirCntr', 'VehMovgDirVehMovgDir', 'VehMovgDirChks'], 'VehSpd': ['VehSpdQf', 'VehSpdChks', 'VehSpdCntr', 'VehSpdSpd'], 'TrsmParkLockSts': ['TrsmParkLockStsChks', 'TrsmParkLockStsCntr', 'TrsmParkLockStsTrsmParkLockSt']}

    class CrashEnd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "crash end"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class CrashSrt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 60
        signal_description = "crash start "
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class DCChrgrHndlSts:
        comments = ""
        factor = 1.0
        initial_value = 4
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 79
        signal_description = "Dc charging gun connection status "
        signal_length = 3
        start_position = 3
        value_definition = {'0x0': ' ChrgrHndlSt_Disconnected', '0x1': ' ChrgrHndlSt_ConnectedWithoutPower', '0x2': ' ChrgrHndlSt_PowerAvailableButNotActivated', '0x3': ' ChrgrHndlSt_ConnectedWithPower', '0x4': ' ChrgrHndlSt_Init', '0x5': ' ChrgrHndlSt_Fault', '0x6': ' ChrgrHndlSt_Reserved1', '0x7': ' ChrgrHndlSt_Reserved2'}

    class EDRLockd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 285
        signal_description = "EDR Locked"
        signal_length = 2
        start_position = 101
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class EDRTrig:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 286
        signal_description = "EDR trigger"
        signal_length = 2
        start_position = 99
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 287
        signal_description = "Electronic gear shifter develop signal group8"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 287
        signal_description = "Electronic gear shifter develop signal group6"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 287
        signal_description = "Electronic gear shifter develop signal group2"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 287
        signal_description = "Electronic gear shifter develop signal group7"
        signal_length = 8
        start_position = 135
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 287
        signal_description = "Electronic gear shifter develop signal group4"
        signal_length = 8
        start_position = 143
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 287
        signal_description = "Electronic gear shifter develop signal group1"
        signal_length = 8
        start_position = 151
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 287
        signal_description = "Electronic gear shifter develop signal group3"
        signal_length = 8
        start_position = 159
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup1DevelpSignalGroup5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 287
        signal_description = "Electronic gear shifter develop signal group5"
        signal_length = 8
        start_position = 167
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Electronic gear shifter develop signal group3"
        signal_length = 8
        start_position = 175
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Electronic gear shifter develop signal group7"
        signal_length = 8
        start_position = 183
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Electronic gear shifter develop signal group1"
        signal_length = 8
        start_position = 191
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Electronic gear shifter develop signal group2"
        signal_length = 8
        start_position = 199
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Electronic gear shifter develop signal group5"
        signal_length = 8
        start_position = 207
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Electronic gear shifter develop signal group6"
        signal_length = 8
        start_position = 215
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Electronic gear shifter develop signal group8"
        signal_length = 8
        start_position = 223
        value_definition = {}

    class ElecGearShiftDevelpSignalGroup2DevelpSignalGroup4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 280
        signal_description = "Electronic gear shifter develop signal group4"
        signal_length = 8
        start_position = 231
        value_definition = {}

    class ElecGearShiftLiSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 281
        signal_description = "EGSM active backlight display status, off is equal to 0, active is equal to 1, backlight fault is equal to 2."
        signal_length = 4
        start_position = 239
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class ElecGearShiftReqVirt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 232
        signal_description = "Virtual shift request in show car mode. "
        signal_length = 3
        start_position = 235
        value_definition = {'0x0': ' GearLvrIndcn_Default', '0x1': ' GearLvrIndcn_P', '0x2': ' GearLvrIndcn_R', '0x3': ' GearLvrIndcn_N', '0x4': ' GearLvrIndcn_D', '0x5': ' GearLvrIndcn_Reserved1', '0x6': ' GearLvrIndcn_Reserved2', '0x7': ' GearLvrIndcn_Undefd'}

    class EpbLampReqCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 248
        signal_description = "counter"
        signal_length = 4
        start_position = 255
        value_definition = {}

    class EpbLampReqChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 248
        signal_description = "crc"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class EpbLampReqEpbLampReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 248
        signal_description = "E2E secured Epb request to display Red EPB tell tale Record has checksum and counter Epb lamp request"
        signal_length = 3
        start_position = 251
        value_definition = {'0x0': ' EpbLampReq_On', '0x1': ' EpbLampReq_Off', '0x2': ' EpbLampReq_Flash2', '0x3': ' EpbLampReq_Flash3'}

    class EpbLampReqSecCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 264
        signal_description = "counter"
        signal_length = 4
        start_position = 271
        value_definition = {}

    class EpbLampReqSecChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 264
        signal_description = "crc"
        signal_length = 8
        start_position = 263
        value_definition = {}

    class EpbLampReqSecEpbLampReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 264
        signal_description = "E2E secured Epb request to display Red EPB tell tale.Record has checksum and counter Epb lamp request"
        signal_length = 3
        start_position = 267
        value_definition = {'0x0': ' EpbLampReq_On', '0x1': ' EpbLampReq_Off', '0x2': ' EpbLampReq_Flash2', '0x3': ' EpbLampReq_Flash3'}

    class EpbMsgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 308
        signal_description = "Request to HMI to display predefined messages and symbols for EPB function."
        signal_length = 4
        start_position = 279
        value_definition = {'0x0': ' EpbMsg_Msg0', '0x1': ' EpbMsg_Msg1', '0x2': ' EpbMsg_Msg2', '0x3': ' EpbMsg_Msg3', '0x4': ' EpbMsg_Msg4', '0x5': ' EpbMsg_Msg5', '0x6': ' EpbMsg_Msg6', '0x7': ' EpbMsg_Msg7', '0x8': ' EpbMsg_Msg8', '0x9': ' EpbMsg_Msg9', '0xA': ' EpbMsg_Msg10', '0xB': ' EpbMsg_Msg11', '0xC': ' EpbMsg_Msg12'}

    class EpbMsgReqSec:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 305
        signal_description = "Request to HMI to display predefined messages and symbols for EPB function."
        signal_length = 4
        start_position = 275
        value_definition = {'0x0': ' EpbMsg_Msg0', '0x1': ' EpbMsg_Msg1', '0x2': ' EpbMsg_Msg2', '0x3': ' EpbMsg_Msg3', '0x4': ' EpbMsg_Msg4', '0x5': ' EpbMsg_Msg5', '0x6': ' EpbMsg_Msg6', '0x7': ' EpbMsg_Msg7', '0x8': ' EpbMsg_Msg8', '0x9': ' EpbMsg_Msg9', '0xA': ' EpbMsg_Msg10', '0xB': ' EpbMsg_Msg11', '0xC': ' EpbMsg_Msg12'}

    class EpbPrimSt:
        comments = ""
        factor = 1.0
        initial_value = 4
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 304
        signal_description = "EPB actuator state for Primary EPB ECU. Only valid for Dual EPB"
        signal_length = 3
        start_position = 284
        value_definition = {'0x0': ' EpbActrSt_Applied', '0x1': ' EpbActrSt_Released', '0x2': ' EpbActrSt_Applying', '0x3': ' EpbActrSt_Releasing', '0x4': ' EpbActrSt_Unknown', '0x5': ' EpbActrSt_HoldApplied', '0x6': ' EpbActrSt_CompleteReleased', '0x7': ' EpbActrSt_HapPrepared'}

    class EpbTotStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 319
        signal_description = "counter"
        signal_length = 4
        start_position = 303
        value_definition = {}

    class EpbTotStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 319
        signal_description = "crc"
        signal_length = 8
        start_position = 295
        value_definition = {}

    class EpbTotStsEpbSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 319
        signal_description = "R-EPB total status"
        signal_length = 4
        start_position = 299
        value_definition = {'0x0': ' EpbSt_Reserved0', '0x1': ' EpbSt_Roller', '0x2': ' EpbSt_Maintain', '0x3': ' EpbSt_AllApplid', '0x4': ' EpbSt_PrimApplidSecUnkown', '0x5': ' EpbSt_AllTran', '0x6': ' EpbSt_ADBF', '0x7': ' EpbSt_PrimReldSecUnkown', '0x8': ' EpbSt_SecApplidPrimUnkown', '0x9': ' EpbSt_AllReleased', '0xA': ' EpbSt_DDBF', '0xB': ' EpbSt_SecReldPrimUnkown', '0xC': ' EpbSt_DBF', '0xD': ' EpbSt_OneSideAppliedAtLeast', '0xE': ' EpbSt_Reserved3', '0xF': ' EpbSt_Error'}

    class EpbWarnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 318
        signal_description = "Epb warnig indication request"
        signal_length = 1
        start_position = 307
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}

    class EpbWarnReqSec:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 317
        signal_description = "EPB warning request second"
        signal_length = 1
        start_position = 306
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}

    class FastBoostRlySt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 316
        signal_description = "Fast charge boost relay status"
        signal_length = 3
        start_position = 311
        value_definition = {'0x0': ' QCRlySt_Open', '0x1': ' QCRlySt_Closed', '0x2': ' QCRlySt_StuckOpen', '0x3': ' QCRlySt_StuckClosed', '0x4': ' QCRlySt_Reserved1', '0x5': ' QCRlySt_Reserved2', '0x6': ' QCRlySt_Reserved3', '0x7': ' QCRlySt_Reserved4'}

    class FrntMotIDc:
        comments = ""
        factor = 0.1
        initial_value = 30000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -3000
        sig_ub = 315
        signal_description = "DC current measured in FMCU"
        signal_length = 16
        start_position = 327
        value_definition = {}

    class FrntMotUDc:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 314
        signal_description = "The HVDC Voltage of FMCU"
        signal_length = 16
        start_position = 343
        value_definition = {}

    class HVBattPackU:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 313
        signal_description = "The  actual voltage of HV battery pack  (measuered before contactors, i.e. always giving HV battery pack voltage)"
        signal_length = 16
        start_position = 359
        value_definition = {}

    class HVBattQCNRlySt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 312
        signal_description = "Dc charging negative relay state"
        signal_length = 3
        start_position = 375
        value_definition = {'0x0': ' QCRlySt_Open', '0x1': ' QCRlySt_Closed', '0x2': ' QCRlySt_StuckOpen', '0x3': ' QCRlySt_StuckClosed', '0x4': ' QCRlySt_Reserved1', '0x5': ' QCRlySt_Reserved2', '0x6': ' QCRlySt_Reserved3', '0x7': ' QCRlySt_Reserved4'}

    class HVBattQCPRlySt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 409
        signal_description = "Dc charging positive relay status"
        signal_length = 3
        start_position = 372
        value_definition = {'0x0': ' QCRlySt_Open', '0x1': ' QCRlySt_Closed', '0x2': ' QCRlySt_StuckOpen', '0x3': ' QCRlySt_StuckClosed', '0x4': ' QCRlySt_Reserved1', '0x5': ' QCRlySt_Reserved2', '0x6': ' QCRlySt_Reserved3', '0x7': ' QCRlySt_Reserved4'}

    class HVBattSelfAwakeDetn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 408
        signal_description = "High voltage battery self-wake-up detection"
        signal_length = 1
        start_position = 369
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class HVBattThermRunAwaySts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 424
        signal_description = "The state of HV battery thermal run away"
        signal_length = 1
        start_position = 368
        value_definition = {'0x0': ' NoYes1_No', '0x1': ' NoYes1_Yes'}

    class HVBattThermRunAwayErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 424
        signal_description = "Thermal runaway fault status information"
        signal_length = 32
        start_position = 383
        value_definition = {}

    class HVMainRlyNegSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 432
        signal_description = "High voltage main negative relay state"
        signal_length = 3
        start_position = 415
        value_definition = {'0x0': ' QCRlySt_Open', '0x1': ' QCRlySt_Closed', '0x2': ' QCRlySt_StuckOpen', '0x3': ' QCRlySt_StuckClosed', '0x4': ' QCRlySt_Reserved1', '0x5': ' QCRlySt_Reserved2', '0x6': ' QCRlySt_Reserved3', '0x7': ' QCRlySt_Reserved4'}

    class HVMainRlyPosSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 441
        signal_description = "High voltage main positive relay status"
        signal_length = 3
        start_position = 412
        value_definition = {'0x0': ' QCRlySt_Open', '0x1': ' QCRlySt_Closed', '0x2': ' QCRlySt_StuckOpen', '0x3': ' QCRlySt_StuckClosed', '0x4': ' QCRlySt_Reserved1', '0x5': ' QCRlySt_Reserved2', '0x6': ' QCRlySt_Reserved3', '0x7': ' QCRlySt_Reserved4'}

    class HVMainRlyStsMainRly1:
        comments = ""
        factor = 1.0
        initial_value = 2
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 425
        signal_description = "Actual state of HV main contactors."
        signal_length = 2
        start_position = 427
        value_definition = {'0x0': ' MainRly1_Open', '0x1': ' MainRly1_Clsd', '0x2': ' MainRly1_KeepSt', '0x3': ' MainRly1_OpenAndReqActvDcha'}

    class HVMainRlyStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 425
        signal_description = "Counter for E2E"
        signal_length = 4
        start_position = 431
        value_definition = {}

    class HVMainRlyStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 425
        signal_description = "Checksum for E2E"
        signal_length = 8
        start_position = 423
        value_definition = {}

    class HVPreChrgRlySts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 440
        signal_description = "The state of HV precharge relay"
        signal_length = 3
        start_position = 439
        value_definition = {'0x0': ' QCRlySt_Open', '0x1': ' QCRlySt_Closed', '0x2': ' QCRlySt_StuckOpen', '0x3': ' QCRlySt_StuckClosed', '0x4': ' QCRlySt_Reserved1', '0x5': ' QCRlySt_Reserved2', '0x6': ' QCRlySt_Reserved3', '0x7': ' QCRlySt_Reserved4'}

    class HVSysActvInhb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 501
        signal_description = "The contactors is inhibited to Closing due to HV system fault or safety issue.Ok: No fault/issue present,contactors are allowed to be closed.NotOk: Fault/issue present, contactors are inhibited to close."
        signal_length = 2
        start_position = 436
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}

    class HVSysPwrOffReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 500
        signal_description = "Informs other ECU that HV contactors will open in 2s due to HV system fault or safety issue (BPO).Ok: No fault present, contactor will not open.NotOk: Fault present, contactors will open."
        signal_length = 2
        start_position = 434
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}

    class HVSysSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 499
        signal_description = "HV System Status during integrity test."
        signal_length = 2
        start_position = 447
        value_definition = {'0x0': ' HVSysSt_Inin', '0x1': ' HVSysSt_Test', '0x2': ' HVSysSt_Rdy'}

    class OnBdChrgrSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 498
        signal_description = "The charging state of OBC"
        signal_length = 4
        start_position = 445
        value_definition = {'0x0': ' ChrgrSts1_Idle', '0x1': ' ChrgrSts1_PreStrt', '0x2': ' ChrgrSts1_Chrgn', '0x3': ' ChrgrSts1_Alrm', '0x4': ' ChrgrSts1_Srv', '0x5': ' ChrgrSts1_Diagc', '0x6': ' ChrgrSts1_Boot', '0x7': ' ChrgrSts1_Rstrt', '0x8': ' ChrgrSts1_DisChrgn', '0x9': ' ChrgrSts1_BookChrgn', '0xA': ' ChrgrSts1_Shutdown', '0xB': ' ChrgrSts1_Heating', '0xC': ' ChrgrSts1_Cooling', '0xD': ' ChrgrSts1_Reserved1', '0xE': ' ChrgrSts1_Reserved2', '0xF': ' ChrgrSts1_Reserved3'}

    class ReMotIDc:
        comments = ""
        factor = 0.1
        initial_value = 30000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -3000
        sig_ub = 497
        signal_description = "DC current measured in the PDCU Motor."
        signal_length = 16
        start_position = 455
        value_definition = {}

    class ReMotUDc:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 496
        signal_description = "The HVDC Voltage of PDCU Motor"
        signal_length = 16
        start_position = 471
        value_definition = {}

    class ScreenTchICSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 523
        signal_description = "The All Error Status Of Screen module"
        signal_length = 6
        start_position = 491
        value_definition = {}

    class ScreenTchICChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 523
        signal_description = "Checks"
        signal_length = 8
        start_position = 487
        value_definition = {}

    class ScreenTchICCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 523
        signal_description = "counter"
        signal_length = 4
        start_position = 495
        value_definition = {}

    class StrtInhbSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 534
        signal_description = "Start Inhibit Status"
        signal_length = 1
        start_position = 535
        value_definition = {'0x0': ' Inhb1_NotInhb', '0x1': ' Inhb1_Inhb'}

    class VehLgtAccelFromWhlSpdLgt:
        comments = ""
        factor = 0.00097654254
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 524
        signal_description = "Longitudinal acceleration over ground"
        signal_length = 16
        start_position = 559
        value_definition = {}

    class VehLgtAccelFromWhlSpdChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 524
        signal_description = "crc"
        signal_length = 8
        start_position = 543
        value_definition = {}

    class VehLgtAccelFromWhlSpdQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 524
        signal_description = "qualify factor"
        signal_length = 2
        start_position = 547
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class VehLgtAccelFromWhlSpdCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 524
        signal_description = "counter"
        signal_length = 4
        start_position = 551
        value_definition = {}

    class VehLgtAccelFromWhlSpdWithCmpCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "counter"
        signal_length = 4
        start_position = 583
        value_definition = {}

    class VehLgtAccelFromWhlSpdWithCmpLgt:
        comments = ""
        factor = 0.00097654254
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "Calculated Longitudinal Ax with compensation of wheel speed and steer angle"
        signal_length = 16
        start_position = 591
        value_definition = {}

    class VehLgtAccelFromWhlSpdWithCmpQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "qualify factor"
        signal_length = 2
        start_position = 579
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class VehLgtAccelFromWhlSpdWithCmpChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 522
        signal_description = "crc"
        signal_length = 8
        start_position = 575
        value_definition = {}

    class VehSpdSafeCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 626
        signal_description = "counter"
        signal_length = 4
        start_position = 615
        value_definition = {}

    class VehSpdSafeSpd:
        comments = ""
        factor = 0.00391
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 626
        signal_description = "Vehicle speed longitudinal based on wheel speed sensors and longitudinal acceleration. ASIL D"
        signal_length = 15
        start_position = 609
        value_definition = {}

    class VehSpdSafeChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 626
        signal_description = "crc"
        signal_length = 8
        start_position = 607
        value_definition = {}

    class VehSpdSafeQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 626
        signal_description = "Quality factor for vehicle speed as measured by wheel speed sensors and longitudinal acceleration."
        signal_length = 2
        start_position = 611
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class WhlMovgDirFrntChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 640
        signal_description = "crc"
        signal_length = 8
        start_position = 655
        value_definition = {}

    class WhlMovgDirFrntCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 640
        signal_description = "counter"
        signal_length = 4
        start_position = 663
        value_definition = {}

    class WhlMovgDirFrntDirRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 640
        signal_description = "Rotational direction for the front individual wheels,fr"
        signal_length = 2
        start_position = 659
        value_definition = {'0x0': ' DirRi_Undefined', '0x1': ' DirRi_Standstill', '0x2': ' DirRi_Forward', '0x3': ' DirRi_Backward'}

    class WhlMovgDirFrntDirLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 640
        signal_description = "Rotational direction for the front individual wheels,fl"
        signal_length = 2
        start_position = 657
        value_definition = {'0x0': ' DirLe_Undefined', '0x1': ' DirLe_Standstill', '0x2': ' DirLe_Forward', '0x3': ' DirLe_Backward'}

    class WhlMovgDirReCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 625
        signal_description = "counter"
        signal_length = 4
        start_position = 671
        value_definition = {}

    class WhlMovgDirReDirLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 625
        signal_description = "Rotational direction for the rear individual wheels. rl"
        signal_length = 2
        start_position = 667
        value_definition = {'0x0': ' DirLe_Undefined', '0x1': ' DirLe_Standstill', '0x2': ' DirLe_Forward', '0x3': ' DirLe_Backward'}

    class WhlMovgDirReDirRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 625
        signal_description = "Rotational direction for the rear individual wheels. rr"
        signal_length = 2
        start_position = 665
        value_definition = {'0x0': ' DirRi_Undefined', '0x1': ' DirRi_Standstill', '0x2': ' DirRi_Forward', '0x3': ' DirRi_Backward'}

    class WhlMovgDirReChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 625
        signal_description = "crc"
        signal_length = 8
        start_position = 679
        value_definition = {}

    class VehMovgDirCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "counter"
        signal_length = 4
        start_position = 647
        value_definition = {}

    class VehMovgDirVehMovgDir:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "Vehicle motion state information based on wheel speed sensors. Provides information about vehicle stand still and vehicle rolling direction. Vehicle motion state"
        signal_length = 3
        start_position = 643
        value_definition = {'0x0': ' VehMovgDir_Unknown', '0x1': ' VehMovgDir_Standstill1', '0x2': ' VehMovgDir_Standstill2', '0x3': ' VehMovgDir_Standstill3', '0x4': ' VehMovgDir_Forward1', '0x5': ' VehMovgDir_Forward2', '0x6': ' VehMovgDir_Backward1', '0x7': ' VehMovgDir_Backward2'}

    class VehMovgDirChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 521
        signal_description = "crc"
        signal_length = 8
        start_position = 639
        value_definition = {}

    class VehSpdQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 520
        signal_description = "Quality factor for vehicle speed as measured by wheel speed sensors and longitudinal acceleration."
        signal_length = 2
        start_position = 691
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class VehSpdChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 520
        signal_description = "crc"
        signal_length = 8
        start_position = 687
        value_definition = {}

    class VehSpdCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 520
        signal_description = "counter"
        signal_length = 4
        start_position = 695
        value_definition = {}

    class VehSpdSpd:
        comments = ""
        factor = 0.00391
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 520
        signal_description = "Vehicle speed longitudinal based on wheel speed sensors and longitudinal acceleration."
        signal_length = 15
        start_position = 689
        value_definition = {}

    class TrsmParkLockStsChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 729
        signal_description = "Checksum"
        signal_length = 8
        start_position = 727
        value_definition = {}

    class TrsmParkLockStsCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 729
        signal_description = "Counter"
        signal_length = 4
        start_position = 735
        value_definition = {}

    class TrsmParkLockStsTrsmParkLockSt:
        comments = ""
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 729
        signal_description = "Transmission park lock status"
        signal_length = 2
        start_position = 731
        value_definition = {'0x0': ' TrsmParkLock_ParkNotEngd', '0x1': ' TrsmParkLock_ParkEngd', '0x2': ' TrsmParkLock_NotInUse', '0x3': ' TrsmParkLock_Undefd'}


class CCUMCUCDToCCUSOCCDEthSignalIPdu07:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204007
    pdu_length_bytes = 1
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-500ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {}

    class HVBattCellBalFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 5
        signal_description = "HV battery  cell balance flag"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}


class CCUMCUCDToCCUSOCCDEthSignalIPdu15:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x20400F
    pdu_length_bytes = 24
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'ReMotDevelpSignalGroup1': ['ReMotDevelpSignalGroup1DTC2HighByte', 'ReMotDevelpSignalGroup1DTC1HighByte', 'ReMotDevelpSignalGroup1DTC2LowByte', 'ReMotDevelpSignalGroup1DTC2Sts', 'ReMotDevelpSignalGroup1DTC1Sts', 'ReMotDevelpSignalGroup1DTC2MiddleByte', 'ReMotDevelpSignalGroup1DTC1LowByte', 'ReMotDevelpSignalGroup1DTC1MiddleByte'], 'ReMotDevelpSignalGroup2': ['ReMotDevelpSignalGroup2DTC2HighByte', 'ReMotDevelpSignalGroup2DTC1MiddleByte', 'ReMotDevelpSignalGroup2DTC1HighByte', 'ReMotDevelpSignalGroup2DTC1Sts', 'ReMotDevelpSignalGroup2DTC1LowByte', 'ReMotDevelpSignalGroup2DTC2LowByte', 'ReMotDevelpSignalGroup2DTC2MiddleByte', 'ReMotDevelpSignalGroup2DTC2Sts'], 'ReMotDevelpSignalGroup3': ['ReMotDevelpSignalGroup3DevelpSignalGroup6', 'ReMotDevelpSignalGroup3DevelpSignalGroup2', 'ReMotDevelpSignalGroup3DevelpSignalGroup3', 'ReMotDevelpSignalGroup3DevelpSignalGroup1', 'ReMotDevelpSignalGroup3DevelpSignalGroup5', 'ReMotDevelpSignalGroup3DevelpSignalGroup4', 'ReMotDevelpSignalGroup3DevelpSignalGroup7', 'ReMotDevelpSignalGroup3DevelpSignalGroup8']}

    class ReMotDevelpSignalGroup1DTC2HighByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 high byte"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ReMotDevelpSignalGroup1DTC1HighByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 high byte"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class ReMotDevelpSignalGroup1DTC2LowByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 low byte"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class ReMotDevelpSignalGroup1DTC2Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 status"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class ReMotDevelpSignalGroup1DTC1Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 status"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class ReMotDevelpSignalGroup1DTC2MiddleByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 middle byte"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class ReMotDevelpSignalGroup1DTC1LowByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 low byte"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class ReMotDevelpSignalGroup1DTC1MiddleByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 middle byte"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class ReMotDevelpSignalGroup2DTC2HighByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 high byte"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class ReMotDevelpSignalGroup2DTC1MiddleByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 middle byte"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class ReMotDevelpSignalGroup2DTC1HighByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 high byte"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class ReMotDevelpSignalGroup2DTC1Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 status"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class ReMotDevelpSignalGroup2DTC1LowByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 low byte"
        signal_length = 8
        start_position = 103
        value_definition = {}

    class ReMotDevelpSignalGroup2DTC2LowByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 low byte"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class ReMotDevelpSignalGroup2DTC2MiddleByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 middle byte"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class ReMotDevelpSignalGroup2DTC2Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 status"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class ReMotDevelpSignalGroup3DevelpSignalGroup6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rear motor develop signal "
        signal_length = 8
        start_position = 135
        value_definition = {}

    class ReMotDevelpSignalGroup3DevelpSignalGroup2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rear motor develop signal "
        signal_length = 8
        start_position = 143
        value_definition = {}

    class ReMotDevelpSignalGroup3DevelpSignalGroup3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rear motor develop signal "
        signal_length = 8
        start_position = 151
        value_definition = {}

    class ReMotDevelpSignalGroup3DevelpSignalGroup1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rear motor develop signal "
        signal_length = 8
        start_position = 159
        value_definition = {}

    class ReMotDevelpSignalGroup3DevelpSignalGroup5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rear motor develop signal "
        signal_length = 8
        start_position = 167
        value_definition = {}

    class ReMotDevelpSignalGroup3DevelpSignalGroup4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rear motor develop signal "
        signal_length = 8
        start_position = 175
        value_definition = {}

    class ReMotDevelpSignalGroup3DevelpSignalGroup7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rear motor develop signal "
        signal_length = 8
        start_position = 183
        value_definition = {}

    class ReMotDevelpSignalGroup3DevelpSignalGroup8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "rear motor develop signal "
        signal_length = 8
        start_position = 191
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu12:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x20400C
    pdu_length_bytes = 2
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {}

    class RTCAlarmSetResult:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "setting result of this alarm setting"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class UsgModSwtInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "UsageMode Switch Info"
        signal_length = 8
        start_position = 15
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu14:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x20400E
    pdu_length_bytes = 3
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {}

    class RoofFolderDisplayBrightnessLevelStatus:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The Brightness of RFD status: 0-100perc"
        signal_length = 8
        start_position = 7
        value_definition = {'0xFF': 'BattSOH_Invalid'}

    class RoofFolderDisplayErrorStatus:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The faults of RFD"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class RoofFolderDisplayFoldedStatus:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "The status of RFD: folded/unfolded"
        signal_length = 2
        start_position = 23
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu10:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x20400A
    pdu_length_bytes = 24
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'FrntMotDevelpSignalGroup1': ['FrntMotDevelpSignalGroup1DTC2Sts', 'FrntMotDevelpSignalGroup1DTC2HighByte', 'FrntMotDevelpSignalGroup1DTC1HighByte', 'FrntMotDevelpSignalGroup1DTC1MiddleByte', 'FrntMotDevelpSignalGroup1DTC2MiddleByte', 'FrntMotDevelpSignalGroup1DTC1LowByte', 'FrntMotDevelpSignalGroup1DTC2LowByte', 'FrntMotDevelpSignalGroup1DTC1Sts'], 'FrntMotDevelpSignalGroup2': ['FrntMotDevelpSignalGroup2DTC2HighByte', 'FrntMotDevelpSignalGroup2DTC2LowByte', 'FrntMotDevelpSignalGroup2DTC1HighByte', 'FrntMotDevelpSignalGroup2DTC1LowByte', 'FrntMotDevelpSignalGroup2DTC1Sts', 'FrntMotDevelpSignalGroup2DTC2MiddleByte', 'FrntMotDevelpSignalGroup2DTC1MiddleByte', 'FrntMotDevelpSignalGroup2DTC2Sts'], 'FrntMotDevelpSignalGroup3': ['FrntMotDevelpSignalGroup3DevelpSignalGroup4', 'FrntMotDevelpSignalGroup3DevelpSignalGroup8', 'FrntMotDevelpSignalGroup3DevelpSignalGroup5', 'FrntMotDevelpSignalGroup3DevelpSignalGroup3', 'FrntMotDevelpSignalGroup3DevelpSignalGroup6', 'FrntMotDevelpSignalGroup3DevelpSignalGroup2', 'FrntMotDevelpSignalGroup3DevelpSignalGroup7', 'FrntMotDevelpSignalGroup3DevelpSignalGroup1']}

    class FrntMotDevelpSignalGroup1DTC2Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 status"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class FrntMotDevelpSignalGroup1DTC2HighByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 high byte"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FrntMotDevelpSignalGroup1DTC1HighByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 high byte"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class FrntMotDevelpSignalGroup1DTC1MiddleByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 middle byte"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class FrntMotDevelpSignalGroup1DTC2MiddleByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 middle byte"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class FrntMotDevelpSignalGroup1DTC1LowByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 low byte"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class FrntMotDevelpSignalGroup1DTC2LowByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 low byte"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class FrntMotDevelpSignalGroup1DTC1Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 status"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class FrntMotDevelpSignalGroup2DTC2HighByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 high byte"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class FrntMotDevelpSignalGroup2DTC2LowByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 low byte"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class FrntMotDevelpSignalGroup2DTC1HighByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 high byte"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class FrntMotDevelpSignalGroup2DTC1LowByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 low byte"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class FrntMotDevelpSignalGroup2DTC1Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 status"
        signal_length = 8
        start_position = 103
        value_definition = {}

    class FrntMotDevelpSignalGroup2DTC2MiddleByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 middle byte"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class FrntMotDevelpSignalGroup2DTC1MiddleByte:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC1 middle byte"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class FrntMotDevelpSignalGroup2DTC2Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DTC2 status"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class FrntMotDevelpSignalGroup3DevelpSignalGroup4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front motor develop signal "
        signal_length = 8
        start_position = 135
        value_definition = {}

    class FrntMotDevelpSignalGroup3DevelpSignalGroup8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front motor develop signal "
        signal_length = 8
        start_position = 143
        value_definition = {}

    class FrntMotDevelpSignalGroup3DevelpSignalGroup5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front motor develop signal "
        signal_length = 8
        start_position = 151
        value_definition = {}

    class FrntMotDevelpSignalGroup3DevelpSignalGroup3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front motor develop signal "
        signal_length = 8
        start_position = 159
        value_definition = {}

    class FrntMotDevelpSignalGroup3DevelpSignalGroup6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front motor develop signal "
        signal_length = 8
        start_position = 167
        value_definition = {}

    class FrntMotDevelpSignalGroup3DevelpSignalGroup2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front motor develop signal "
        signal_length = 8
        start_position = 175
        value_definition = {}

    class FrntMotDevelpSignalGroup3DevelpSignalGroup7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front motor develop signal "
        signal_length = 8
        start_position = 183
        value_definition = {}

    class FrntMotDevelpSignalGroup3DevelpSignalGroup1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Front motor develop signal "
        signal_length = 8
        start_position = 191
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu04:
    base_type = "Boolean"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204004
    pdu_length_bytes = 90
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-200ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'BLEChrgrPileInfo': ['BLEChrgrPileInfoChrgrPileInfo', 'BLEChrgrPileInfoChrgrPileTyp', 'BLEChrgrPileInfoChrgrPilePwr'], 'HvBattCellT': ['HvBattCellTMin', 'HvBattCellTMax', 'HvBattCellTAvg'], 'HVBattCellTVal': ['HVBattCellTValCellTMax', 'HVBattCellTValCellTSnsrT', 'HVBattCellTValCellTSnsrNr', 'HVBattCellTValCellTMin', 'HVBattCellTValCellTMinSnsrSerlNr', 'HVBattCellTValCellTMaxSnsrSerlNr'], 'HVBattCellUVal': ['HVBattCellUValU3', 'HVBattCellUValU4', 'HVBattCellUValU1', 'HVBattCellUValU2'], 'HvBattCod': ['HvBattCodPackCodeX3', 'HvBattCodPackCodeX6', 'HvBattCodPackCodeX5', 'HvBattCodPackCodeIndex', 'HvBattCodPackCodeX2', 'HvBattCodPackCodeX1', 'HvBattCodPackCodeX4']}

    class BLEChrgrPileInfoChrgrPileInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "Represernt the Public or Private property of the charging pile"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' ChrgrPileInfo_Invalid', '0x1': ' ChrgrPileInfo_Private', '0x2': ' ChrgrPileInfo_Public', '0x3': ' ChrgrPileInfo_Reserved'}

    class BLEChrgrPileInfoChrgrPileTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "Charger Pile Type"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' ChrgrPileTyp_Invalid', '0x1': ' ChrgrPileTyp_DC', '0x2': ' ChrgrPileTyp_AC', '0x3': ' ChrgrPileTyp_Reserved'}

    class BLEChrgrPileInfoChrgrPilePwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "Charger Pile Power"
        signal_length = 3
        start_position = 3
        value_definition = {'0x0': ' ChrgrPilePwr_Invalid', '0x1': ' ChrgrPilePwr_7KW', '0x2': ' ChrgrPilePwr_360KW', '0x3': ' ChrgrPilePwr_800KW', '0x4': ' ChrgrPilePwr_Reserved1', '0x5': ' ChrgrPilePwr_Reserved2', '0x6': ' ChrgrPilePwr_Reserved3', '0x7': ' ChrgrPilePwr_Reserved4'}

    class BLESlotKeyWhiteListVers:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 78
        signal_description = "BLE Key white list version info"
        signal_length = 64
        start_position = 15
        value_definition = {}

    class BLEWarnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 77
        signal_description = "Indicate BLE Anchor fault state"
        signal_length = 1
        start_position = 79
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class EntityKeyWhiteListVers:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 76
        signal_description = "Entity Key white list version"
        signal_length = 64
        start_position = 87
        value_definition = {}

    class HvBattCellTMin:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 176
        signal_description = "The Min cell temperature of HV battery."
        signal_length = 13
        start_position = 151
        value_definition = {}

    class HvBattCellTMax:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 176
        signal_description = "The Max cell temperature of HV battery."
        signal_length = 13
        start_position = 154
        value_definition = {}

    class HvBattCellTAvg:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 176
        signal_description = "The average cell temperature of HV battery."
        signal_length = 13
        start_position = 173
        value_definition = {}

    class HVBattCellTMaxSerlNr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 75
        signal_description = "The serial number of the maximum cell temperature subsystem."
        signal_length = 8
        start_position = 191
        value_definition = {}

    class HVBattCellTMinSerlNr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 74
        signal_description = "The serial number of the minimum cell temperature subsystem."
        signal_length = 8
        start_position = 199
        value_definition = {}

    class HVBattCellTSnsrNr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 73
        signal_description = "The total number of all cell temperature sensors."
        signal_length = 8
        start_position = 207
        value_definition = {}

    class HVBattCellTValCellTMax:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 72
        signal_description = "HV battery Max cell temperature"
        signal_length = 8
        start_position = 215
        value_definition = {}

    class HVBattCellTValCellTSnsrT:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 72
        signal_description = "The cell temperature of HV battery"
        signal_length = 8
        start_position = 223
        value_definition = {}

    class HVBattCellTValCellTSnsrNr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 72
        signal_description = "The total number of all cell temperature sensors"
        signal_length = 8
        start_position = 231
        value_definition = {}

    class HVBattCellTValCellTMin:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 72
        signal_description = "HV battery Min cell temperature"
        signal_length = 8
        start_position = 239
        value_definition = {}

    class HVBattCellTValCellTMinSnsrSerlNr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 72
        signal_description = "The serial number of Min temperature sensor in HV battery"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class HVBattCellTValCellTMaxSnsrSerlNr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 72
        signal_description = "The serial number of Max temperature sensor in HV battery"
        signal_length = 8
        start_position = 255
        value_definition = {}

    class HVBattCellUValU3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 381
        signal_description = "List of cell voltage values of U3."
        signal_length = 8
        start_position = 263
        value_definition = {}

    class HVBattCellUValU4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 381
        signal_description = "List of cell voltage values of U4."
        signal_length = 13
        start_position = 271
        value_definition = {}

    class HVBattCellUValU1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 381
        signal_description = "List of cell voltage values of U1."
        signal_length = 8
        start_position = 287
        value_definition = {}

    class HVBattCellUValU2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 381
        signal_description = "List of cell voltage values of U2."
        signal_length = 8
        start_position = 295
        value_definition = {}

    class HvBattCodPackCodeX3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 380
        signal_description = "Pack code X3/X9/X15/X21"
        signal_length = 8
        start_position = 303
        value_definition = {}

    class HvBattCodPackCodeX6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 380
        signal_description = "Pack code X6/X12/X18/X24"
        signal_length = 8
        start_position = 311
        value_definition = {}

    class HvBattCodPackCodeX5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 380
        signal_description = "Pack code X5/X11/X17/X23"
        signal_length = 8
        start_position = 319
        value_definition = {}

    class HvBattCodPackCodeIndex:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 380
        signal_description = "message pack index"
        signal_length = 8
        start_position = 327
        value_definition = {}

    class HvBattCodPackCodeX2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 380
        signal_description = "Pack code X2/X8/X14/X20"
        signal_length = 8
        start_position = 335
        value_definition = {}

    class HvBattCodPackCodeX1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 380
        signal_description = "Pack code X1/X7/X13/X19"
        signal_length = 8
        start_position = 343
        value_definition = {}

    class HvBattCodPackCodeX4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 380
        signal_description = "Pack code X4/X10/X16/22"
        signal_length = 8
        start_position = 351
        value_definition = {}

    class HVBattCodLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 379
        signal_description = "The coding length of pack"
        signal_length = 8
        start_position = 359
        value_definition = {}

    class HVBattCp:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 378
        signal_description = "The rated capacity of the HV  battery."
        signal_length = 16
        start_position = 367
        value_definition = {}

    class HVBattFltIndcn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 377
        signal_description = "HV battery pack MIL ilumination require."
        signal_length = 1
        start_position = 383
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class HVBattMatchErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 376
        signal_description = "The fault of REESS Mismatching."
        signal_length = 1
        start_position = 382
        value_definition = {'0x0': ' DevErrSts2_NoFlt', '0x1': ' DevErrSts2_Flt'}

    class HVBattMngtSysNr:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 413
        signal_description = "Number of battery management systems"
        signal_length = 8
        start_position = 391
        value_definition = {}

    class HVBattMngtSysPackNr:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 412
        signal_description = "HV battery management system corresponds to the number of power battery packs"
        signal_length = 8
        start_position = 399
        value_definition = {}

    class HVBattPackSOCR:
        comments = ""
        factor = 0.1
        initial_value = 1020
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 411
        signal_description = "SOCR state of HV battery pack."
        signal_length = 10
        start_position = 407
        value_definition = {}

    class HVBattSubSysNr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 410
        signal_description = "The number of the battery subsystem."
        signal_length = 8
        start_position = 423
        value_definition = {}

    class HvBattTotChrgCap:
        comments = ""
        factor = 0.01
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 409
        signal_description = "The total accumulated charge capacity,only for plug-in charging."
        signal_length = 32
        start_position = 431
        value_definition = {}

    class HvBattTotChrgEgy:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 408
        signal_description = "The total accumulated charge energy ,only for plug-in charging."
        signal_length = 32
        start_position = 463
        value_definition = {}

    class HvBattTotDchaCap:
        comments = ""
        factor = 0.01
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 623
        signal_description = "The total accumulated discharge capacity,except charging."
        signal_length = 32
        start_position = 495
        value_definition = {}

    class HvBattTotDchaEgy:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 622
        signal_description = "The total accumulated discharge energy ,except charging."
        signal_length = 32
        start_position = 527
        value_definition = {}

    class HVBattUMaxSerlNr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 621
        signal_description = "The serial number of the maximum cell voltage subsystem."
        signal_length = 8
        start_position = 559
        value_definition = {}

    class HVBattUMinSerlNr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 620
        signal_description = "The serial number of the minimum cell voltage subsystem."
        signal_length = 8
        start_position = 567
        value_definition = {}

    class HVCellTDifFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 619
        signal_description = "The fault level of HV battery cell temperature uniformity."
        signal_length = 2
        start_position = 575
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class HVCellTOverFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 618
        signal_description = "The fault level of HV battery cell over temperature."
        signal_length = 2
        start_position = 573
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class HVCellUDifFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 617
        signal_description = "The fault level of HV battery cell voltage uniformity."
        signal_length = 2
        start_position = 571
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class HVCellUOverFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 616
        signal_description = "The fault level of HV battery cell over voltage."
        signal_length = 2
        start_position = 569
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class HVCellUUnderFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 631
        signal_description = "The fault level of HV battery cell under voltage."
        signal_length = 2
        start_position = 583
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class HVILFltSt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 630
        signal_description = "High voltage interlock state alarm"
        signal_length = 2
        start_position = 581
        value_definition = {'0x0': ' OpenCls2_Default', '0x1': ' OpenCls2_Close', '0x2': ' OpenCls2_Open', '0x3': ' OpenCls2_Reserved'}

    class HVIsoFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 629
        signal_description = "The fault level of InsulationRes Fault."
        signal_length = 2
        start_position = 579
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class HVPackOverChrgFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 628
        signal_description = "The fault level of HV battery pack over charge."
        signal_length = 2
        start_position = 577
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class HVPackSerlNr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 627
        signal_description = "The serial number of the pack subsystem."
        signal_length = 8
        start_position = 591
        value_definition = {}

    class HVPackUOverFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 626
        signal_description = "The fault level of HV battery pack over voltage."
        signal_length = 2
        start_position = 599
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class HVPackUUnderFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 625
        signal_description = "The fault level of HV battery pack under voltage."
        signal_length = 2
        start_position = 597
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class HVSOCHiFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 624
        signal_description = "The fault level of HV battery pack over SOC."
        signal_length = 2
        start_position = 595
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class HVSOCHopFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 639
        signal_description = "The fault level of HV battery pack SOC hop."
        signal_length = 2
        start_position = 593
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class HVSOCLoFltLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 638
        signal_description = "The fault level of HV battery pack low SOC."
        signal_length = 2
        start_position = 607
        value_definition = {'0x0': ' FltLvl_Normal', '0x1': ' FltLvl_LevelI', '0x2': ' FltLvl_LevelII', '0x3': ' FltLvl_LevelIII'}

    class InsdNFCWarnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 637
        signal_description = "Inside NFC reader warn status"
        signal_length = 1
        start_position = 605
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class LVAvlPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 636
        signal_description = "available low voltage power from DCDC"
        signal_length = 12
        start_position = 603
        value_definition = {}

    class OutdNFCWarnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 635
        signal_description = "Inside NFC reader warn status"
        signal_length = 1
        start_position = 604
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}


class CCUMCUCDToCCUSOCCDEthSignalIPdu13:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x20400D
    pdu_length_bytes = 32
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'HVBattDevelpSignalGroup1': ['HVBattDevelpSignalGroup1DevelpSignalGroup5', 'HVBattDevelpSignalGroup1DevelpSignalGroup1', 'HVBattDevelpSignalGroup1DevelpSignalGroup3', 'HVBattDevelpSignalGroup1DevelpSignalGroup7', 'HVBattDevelpSignalGroup1DevelpSignalGroup6', 'HVBattDevelpSignalGroup1DevelpSignalGroup2', 'HVBattDevelpSignalGroup1DevelpSignalGroup8', 'HVBattDevelpSignalGroup1DevelpSignalGroup4'], 'HVBattDevelpSignalGroup2': ['HVBattDevelpSignalGroup2DevelpSignalGroup7', 'HVBattDevelpSignalGroup2DevelpSignalGroup6', 'HVBattDevelpSignalGroup2DevelpSignalGroup4', 'HVBattDevelpSignalGroup2DevelpSignalGroup5', 'HVBattDevelpSignalGroup2DevelpSignalGroup3', 'HVBattDevelpSignalGroup2DevelpSignalGroup8', 'HVBattDevelpSignalGroup2DevelpSignalGroup1', 'HVBattDevelpSignalGroup2DevelpSignalGroup2'], 'HVBattDevelpSignalGroup3': ['HVBattDevelpSignalGroup3DevelpSignalGroup7', 'HVBattDevelpSignalGroup3DevelpSignalGroup5', 'HVBattDevelpSignalGroup3DevelpSignalGroup8', 'HVBattDevelpSignalGroup3DevelpSignalGroup2', 'HVBattDevelpSignalGroup3DevelpSignalGroup6', 'HVBattDevelpSignalGroup3DevelpSignalGroup4', 'HVBattDevelpSignalGroup3DevelpSignalGroup1', 'HVBattDevelpSignalGroup3DevelpSignalGroup3'], 'HVBattDevelpSignalGroup4': ['HVBattDevelpSignalGroup4DevelpSignalGroup3', 'HVBattDevelpSignalGroup4DevelpSignalGroup6', 'HVBattDevelpSignalGroup4DevelpSignalGroup7', 'HVBattDevelpSignalGroup4DevelpSignalGroup1', 'HVBattDevelpSignalGroup4DevelpSignalGroup4', 'HVBattDevelpSignalGroup4DevelpSignalGroup8', 'HVBattDevelpSignalGroup4DevelpSignalGroup5', 'HVBattDevelpSignalGroup4DevelpSignalGroup2']}

    class HVBattDevelpSignalGroup1DevelpSignalGroup5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class HVBattDevelpSignalGroup1DevelpSignalGroup1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class HVBattDevelpSignalGroup1DevelpSignalGroup3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class HVBattDevelpSignalGroup1DevelpSignalGroup7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class HVBattDevelpSignalGroup1DevelpSignalGroup6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class HVBattDevelpSignalGroup1DevelpSignalGroup2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class HVBattDevelpSignalGroup1DevelpSignalGroup8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class HVBattDevelpSignalGroup1DevelpSignalGroup4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class HVBattDevelpSignalGroup2DevelpSignalGroup7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class HVBattDevelpSignalGroup2DevelpSignalGroup6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class HVBattDevelpSignalGroup2DevelpSignalGroup4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class HVBattDevelpSignalGroup2DevelpSignalGroup5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class HVBattDevelpSignalGroup2DevelpSignalGroup3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 103
        value_definition = {}

    class HVBattDevelpSignalGroup2DevelpSignalGroup8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class HVBattDevelpSignalGroup2DevelpSignalGroup1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class HVBattDevelpSignalGroup2DevelpSignalGroup2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class HVBattDevelpSignalGroup3DevelpSignalGroup7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 135
        value_definition = {}

    class HVBattDevelpSignalGroup3DevelpSignalGroup5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 143
        value_definition = {}

    class HVBattDevelpSignalGroup3DevelpSignalGroup8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 151
        value_definition = {}

    class HVBattDevelpSignalGroup3DevelpSignalGroup2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 159
        value_definition = {}

    class HVBattDevelpSignalGroup3DevelpSignalGroup6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 167
        value_definition = {}

    class HVBattDevelpSignalGroup3DevelpSignalGroup4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 175
        value_definition = {}

    class HVBattDevelpSignalGroup3DevelpSignalGroup1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 183
        value_definition = {}

    class HVBattDevelpSignalGroup3DevelpSignalGroup3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 191
        value_definition = {}

    class HVBattDevelpSignalGroup4DevelpSignalGroup3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 199
        value_definition = {}

    class HVBattDevelpSignalGroup4DevelpSignalGroup6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 207
        value_definition = {}

    class HVBattDevelpSignalGroup4DevelpSignalGroup7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 215
        value_definition = {}

    class HVBattDevelpSignalGroup4DevelpSignalGroup1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 223
        value_definition = {}

    class HVBattDevelpSignalGroup4DevelpSignalGroup4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 231
        value_definition = {}

    class HVBattDevelpSignalGroup4DevelpSignalGroup8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 239
        value_definition = {}

    class HVBattDevelpSignalGroup4DevelpSignalGroup5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class HVBattDevelpSignalGroup4DevelpSignalGroup2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "develop signal group"
        signal_length = 8
        start_position = 255
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu06:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204006
    pdu_length_bytes = 8
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-30ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {}

    class HVBattPackIDC:
        comments = ""
        factor = 0.1
        initial_value = 65535
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -3000
        sig_ub = 21
        signal_description = "The actual current of HV battery pack,Positive current is discharging."
        signal_length = 16
        start_position = 7
        value_definition = {}

    class HVBattSOCCorrnFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "HV battery  SOC correction flag"
        signal_length = 2
        start_position = 23
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}


class CCUMCUCDToCCUSOCCDEthSignalIPdu09:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204009
    pdu_length_bytes = 4
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-70ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {}

    class HVBattLimnIndcnDTCInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 23
        signal_description = "HV battery management system DTC code"
        signal_length = 16
        start_position = 7
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu17:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204011
    pdu_length_bytes = 8
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'CDPowerStateInfo': ['CDPowerStateInfoByte3', 'CDPowerStateInfoByte2', 'CDPowerStateInfoByte0', 'CDPowerStateInfoByte1', 'CDPowerStateInfoByte4', 'CDPowerStateInfoByte7', 'CDPowerStateInfoByte6', 'CDPowerStateInfoByte5']}

    class CDPowerStateInfoByte3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CD MCU power management debug info byte3"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class CDPowerStateInfoByte2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CD MCU power management debug info byte2"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class CDPowerStateInfoByte0:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CD MCU power management debug info byte0"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class CDPowerStateInfoByte1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CD MCU power management debug info byte1"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class CDPowerStateInfoByte4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CD MCU power management debug info byte4"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class CDPowerStateInfoByte7:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CD MCU power management debug info byte7"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class CDPowerStateInfoByte6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CD MCU power management debug info byte6"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class CDPowerStateInfoByte5:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "CD MCU power management debug info byte5"
        signal_length = 8
        start_position = 63
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu21:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204015
    pdu_length_bytes = 34
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-100ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'BLEBookStopTiChrgnTmr': ['BLEBookStopTiChrgnTmrHr', 'BLEBookStopTiChrgnTmrMins'], 'BLEBookStrtTiChrgnTmr': ['BLEBookStrtTiChrgnTmrHr', 'BLEBookStrtTiChrgnTmrMins'], 'DchaEgyStrg': ['DchaEgyStrgDchaCarTi', 'DchaEgyStrgDchaEgy'], 'RemBookStopTiChrgnTmr': ['RemBookStopTiChrgnTmrHr', 'RemBookStopTiChrgnTmrMins'], 'RemBookStrtTiChrgnTmr': ['RemBookStrtTiChrgnTmrHr', 'RemBookStrtTiChrgnTmrMins']}

    class BLEBookStopTiChrgnTmrHr:
        comments = ""
        factor = 1.0
        initial_value = 24
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 28
        signal_description = "Hour"
        signal_length = 5
        start_position = 7
        value_definition = {}

    class BLEBookStopTiChrgnTmrMins:
        comments = ""
        factor = 1.0
        initial_value = 60
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 28
        signal_description = "Minutes "
        signal_length = 6
        start_position = 2
        value_definition = {}

    class BLEBookStrtTiChrgnTmrHr:
        comments = ""
        factor = 1.0
        initial_value = 24
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 27
        signal_description = "Hour"
        signal_length = 5
        start_position = 12
        value_definition = {}

    class BLEBookStrtTiChrgnTmrMins:
        comments = ""
        factor = 1.0
        initial_value = 60
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 27
        signal_description = "Minutes "
        signal_length = 6
        start_position = 23
        value_definition = {}

    class BookChrgSetResp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 26
        signal_description = "Book charging settings status feedback"
        signal_length = 2
        start_position = 17
        value_definition = {'0x0': ' BookChargeSetResponse_Default', '0x1': ' BookChargeSetResponse_Success', '0x2': ' BookChargeSetResponse_Cancelled', '0x3': ' BookChargeSetResponse_Fail'}

    class CstRgnModAct:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 25
        signal_description = "Energy recovery mode feedback"
        signal_length = 1
        start_position = 31
        value_definition = {'0x0': ' OnOff2_On', '0x1': ' OnOff2_Off'}

    class DCChrgPilBookChrgn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 24
        signal_description = "The pre-charge event activation status of the pile end "
        signal_length = 2
        start_position = 30
        value_definition = {'0x0': ' ChrgPilBookChrgn_Default', '0x1': ' ChrgPilBookChrgn_On', '0x2': ' ChrgPilBookChrgn_Off', '0x3': ' ChrgPilBookChrgn_Reserve'}

    class DCChrgrUMaxDetn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 255
        signal_description = "Highest insulation test voltage of Chrgr"
        signal_length = 16
        start_position = 39
        value_definition = {}

    class DchaEgyStrgDchaCarTi:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 254
        signal_description = "Feedback the time of the OBC storage."
        signal_length = 32
        start_position = 55
        value_definition = {}

    class DchaEgyStrgDchaEgy:
        comments = ""
        factor = 100.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 254
        signal_description = "Feedback the discharge energy of the OBC storage"
        signal_length = 11
        start_position = 87
        value_definition = {}

    class DrvgCycSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 253
        signal_description = "Driving cycle status."
        signal_length = 2
        start_position = 92
        value_definition = {'0x0': ' OffOnInvld_Invalid1', '0x1': ' OffOnInvld_Off', '0x2': ' OffOnInvld_On', '0x3': ' OffOnInvld_Invalid2'}

    class GearLvrIndcnVirt:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 252
        signal_description = "Virtual gear information feedback"
        signal_length = 3
        start_position = 90
        value_definition = {'0x0': ' GearLvrIndcn_Default', '0x1': ' GearLvrIndcn_P', '0x2': ' GearLvrIndcn_R', '0x3': ' GearLvrIndcn_N', '0x4': ' GearLvrIndcn_D', '0x5': ' GearLvrIndcn_Reserved1', '0x6': ' GearLvrIndcn_Reserved2', '0x7': ' GearLvrIndcn_Undefd'}

    class HMIEPedlIndcnMsg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 251
        signal_description = "Pedal mode deceleration function feedback, including the function due to user operation, failure and other cases caused by the function of limited prompts."
        signal_length = 4
        start_position = 103
        value_definition = {}

    class HMIGearShiftFailMsg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 250
        signal_description = "Gear shift failure information feedback, including braking, charging gun, speed, front hatch cover, seat back and other information."
        signal_length = 4
        start_position = 99
        value_definition = {}

    class HMIGearShiftrFltMsg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 249
        signal_description = "Shift fault information feedback, including screen shifters and EGSM shifters."
        signal_length = 3
        start_position = 111
        value_definition = {}

    class HMILnchModFailIndcnMsg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 248
        signal_description = "Launch mode fault indication message"
        signal_length = 5
        start_position = 108
        value_definition = {}

    class HMILnchModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 263
        signal_description = "Status feedback of the ejection start function, including disable, initial, standby, ready, active, and failed."
        signal_length = 3
        start_position = 119
        value_definition = {'0x0': ' LaunchModeSts_Disable', '0x1': ' LaunchModeSts_Initial', '0x2': ' LaunchModeSts_Standby', '0x3': ' LaunchModeSts_Ready', '0x4': ' LaunchModeSts_Active', '0x5': ' LaunchModeSts_Failed', '0x6': ' LaunchModeSts_Reserved1', '0x7': ' LaunchModeSts_Reserved2'}

    class HndlLockgSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 262
        signal_description = "Status of charge inlet electric lock"
        signal_length = 2
        start_position = 116
        value_definition = {'0x0': ' LockgSts_Unknown', '0x1': ' LockgSts_Locked', '0x2': ' LockgSts_Unlocked', '0x3': ' LockgSts_Fault'}

    class HVBattChrgnTiEstim:
        comments = ""
        factor = 1.0
        initial_value = 2047
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 261
        signal_description = "Estimated remaining charging time "
        signal_length = 11
        start_position = 114
        value_definition = {}

    class HVBattChrgPwrActCns1:
        comments = ""
        factor = 100.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 260
        signal_description = "HV battery actual charging power consumption."
        signal_length = 13
        start_position = 135
        value_definition = {}

    class HVBattChrgPwrCritDes1:
        comments = ""
        factor = 100.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 259
        signal_description = "HV battery critically desired charging power."
        signal_length = 13
        start_position = 138
        value_definition = {}

    class HVBattChrgPwrNormDes1:
        comments = ""
        factor = 100.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 258
        signal_description = "HV battery desired charging power."
        signal_length = 13
        start_position = 157
        value_definition = {}

    class HvBattDisChrgnTiEstim:
        comments = ""
        factor = 1.0
        initial_value = 2047
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 181
        signal_description = "Estimated remaining discharge time "
        signal_length = 11
        start_position = 160
        value_definition = {}

    class OnBdChrgrHndlSts:
        comments = ""
        factor = 1.0
        initial_value = 8
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 180
        signal_description = "AC charging gun connection status"
        signal_length = 4
        start_position = 179
        value_definition = {'0x0': ' OBCChrgrHndlSt_Disconnected', '0x1': ' OBCChrgrHndlSt_ConnectedWithoutPower', '0x2': ' OBCChrgrHndlSt_PowerAvailableButNotActivated', '0x3': ' OBCChrgrHndlSt_ConnectedWithPower', '0x4': ' OBCChrgrHndlSt_DischargeConnectwithoutpowerincar', '0x5': ' OBCChrgrHndlSt_DischargeConnectwithoutpoweroutcar', '0x6': ' OBCChrgrHndlSt_DischargeConnectwithpowerincar', '0x7': ' OBCChrgrHndlSt_DischargeConnectwithpoweroutcar', '0x8': ' OBCChrgrHndlSt_Init', '0x9': ' OBCChrgrHndlSt_Fault', '0xA': ' OBCChrgrHndlSt_NotCompleteConnnected', '0xB': ' OBCChrgrHndlSt_ConnectedWithPowerButNotPWM', '0xC': ' OBCChrgrHndlSt_Reserved1', '0xD': ' OBCChrgrHndlSt_Reserved2', '0xE': ' OBCChrgrHndlSt_Reserved3'}

    class OnBdChrgrPortT:
        comments = ""
        factor = 1.0
        initial_value = 40
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 257
        signal_description = "Onboard Charger Socket Inlet Temperature"
        signal_length = 8
        start_position = 191
        value_definition = {}

    class PlsHeatgSts1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 256
        signal_description = "Pulse heating states"
        signal_length = 3
        start_position = 199
        value_definition = {'0x0': ' PlsHeatgSts_Idle', '0x1': ' PlsHeatgSts_Init', '0x2': ' PlsHeatgSts_Heatg', '0x3': ' PlsHeatgSts_Finish', '0x4': ' PlsHeatgSts_Err', '0x5': ' PlsHeatgSts_Inhb', '0x6': ' PlsHeatgSts_Reserve1', '0x7': ' PlsHeatgSts_Reserve2'}

    class PrpsnSysDrftModAllwd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 271
        signal_description = "Powertrain feedback whether drift mode is allowed to open."
        signal_length = 2
        start_position = 196
        value_definition = {'0x0': ' AllwdorNot_Init', '0x1': ' AllwdorNot_NotAllwd', '0x2': ' AllwdorNot_Allwd', '0x3': ' AllwdorNot_Resd1'}

    class PrpsnSysECOPlusModAllwd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 270
        signal_description = "Power system feedback whether ECO Plus mode is allowed to open. "
        signal_length = 2
        start_position = 194
        value_definition = {'0x0': ' AllwdorNot_Init', '0x1': ' AllwdorNot_NotAllwd', '0x2': ' AllwdorNot_Allwd', '0x3': ' AllwdorNot_Resd1'}

    class PrpsnSysOffRoadModAllwd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 269
        signal_description = "Powertrain feedback whether off-road mode is allowed to open. "
        signal_length = 2
        start_position = 192
        value_definition = {'0x0': ' AllwdorNot_Init', '0x1': ' AllwdorNot_NotAllwd', '0x2': ' AllwdorNot_Allwd', '0x3': ' AllwdorNot_Resd1'}

    class PrpsnSysRaceModAllwd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 268
        signal_description = "Powertrain feedback whether race mode is allowed to open. "
        signal_length = 2
        start_position = 206
        value_definition = {'0x0': ' AllwdorNot_Init', '0x1': ' AllwdorNot_NotAllwd', '0x2': ' AllwdorNot_Allwd', '0x3': ' AllwdorNot_Resd1'}

    class PrpsnSysSptModAllwd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 267
        signal_description = "Powertrain feedback whether sport mode is allowed to open."
        signal_length = 2
        start_position = 204
        value_definition = {'0x0': ' AllwdorNot_Init', '0x1': ' AllwdorNot_NotAllwd', '0x2': ' AllwdorNot_Allwd', '0x3': ' AllwdorNot_Resd1'}

    class PrpsnSysTracModAllwd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 266
        signal_description = "Powertrain feedback whether Traction mode is allowed to open. "
        signal_length = 2
        start_position = 202
        value_definition = {'0x0': ' AllwdorNot_Init', '0x1': ' AllwdorNot_NotAllwd', '0x2': ' AllwdorNot_Allwd', '0x3': ' AllwdorNot_Resd1'}

    class RemBookStopTiChrgnTmrHr:
        comments = ""
        factor = 1.0
        initial_value = 24
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 240
        signal_description = "Hour"
        signal_length = 5
        start_position = 200
        value_definition = {}

    class RemBookStopTiChrgnTmrMins:
        comments = ""
        factor = 1.0
        initial_value = 60
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 240
        signal_description = "Minutes "
        signal_length = 6
        start_position = 211
        value_definition = {}

    class RemBookStrtTiChrgnTmrHr:
        comments = ""
        factor = 1.0
        initial_value = 24
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 241
        signal_description = "Hour"
        signal_length = 5
        start_position = 221
        value_definition = {}

    class RemBookStrtTiChrgnTmrMins:
        comments = ""
        factor = 1.0
        initial_value = 60
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 241
        signal_description = "Minutes "
        signal_length = 6
        start_position = 216
        value_definition = {}

    class RoadSlopInfo:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 242
        signal_description = "Slope value, unit percentage, accuracy 0.1percentage."
        signal_length = 11
        start_position = 226
        value_definition = {}

    class VehPrpsnSysActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 243
        signal_description = "Propulsion system status indicating vehicle is propulsive or not"
        signal_length = 2
        start_position = 247
        value_definition = {'0x0': ' ActvInActv2_Init', '0x1': ' ActvInActv2_InActv', '0x2': ' ActvInActv2_Actv'}

    class VirtGearShiftModeAct:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 244
        signal_description = "Virtual shift mode actual state feedback."
        signal_length = 1
        start_position = 245
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class CCUMCUCDToCCUSOCCDEthSignalIPdu19:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204013
    pdu_length_bytes = 8
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-30ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'ChrgnEquipAct': ['ChrgnEquipActU', 'ChrgnEquipActI']}

    class AdjSpdLimnActvnOk:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 5
        signal_description = "The signal informs if Speed Limiter (ASL/AVSL) can be activated or not. Primarily used by HMI to know if Speed Limiter activation requests by driver should be ignored or not."
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class ChrgnEquipActU:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 4
        signal_description = "The actual output voltage from DC charging equipment."
        signal_length = 16
        start_position = 15
        value_definition = {}

    class ChrgnEquipActI:
        comments = ""
        factor = 0.1
        initial_value = 30000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -3000
        sig_ub = 4
        signal_description = "The actual output current from DC charging equipment."
        signal_length = 16
        start_position = 31
        value_definition = {}

    class HMIBattTracFailrIndcnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 3
        signal_description = "Power battery failure light on request. "
        signal_length = 2
        start_position = 47
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}

    class HMIHzrdLiIndcnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2
        signal_description = "Drive system hazard light on request. "
        signal_length = 2
        start_position = 45
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}

    class HMIPrpsnSysErrIndcnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Drive system fault indicator light request. "
        signal_length = 1
        start_position = 43
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}

    class HMIPrpsnSysFltMsg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "Fault information about the driver system "
        signal_length = 4
        start_position = 42
        value_definition = {}

    class HMITurtlePwrLossIndcn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 52
        signal_description = "Drive system power limited turtle light on request "
        signal_length = 2
        start_position = 54
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}

    class PrpsnSysLimnIndcnFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 51
        signal_description = "Drive system fault feedback information "
        signal_length = 8
        start_position = 63
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu20:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204014
    pdu_length_bytes = 86
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-50ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'ChrgnEquipMax': ['ChrgnEquipMaxI', 'ChrgnEquipMaxU'], 'DCChrgrPortT': ['DCChrgrPortTPosPortT', 'DCChrgrPortTNegPortT'], 'EgyCnsFacVehSpd': ['EgyCnsFacVehSpdSpd40', 'EgyCnsFacVehSpdSpd140', 'EgyCnsFacVehSpdSpd20', 'EgyCnsFacVehSpdSpd60', 'EgyCnsFacVehSpdSpd100', 'EgyCnsFacVehSpdSpd120', 'EgyCnsFacVehSpdSpd10', 'EgyCnsFacVehSpdSpd80'], 'EgyConsSlopReducCoeff': ['EgyConsSlopReducCoeffSlop4', 'EgyConsSlopReducCoeffSlop12', 'EgyConsSlopReducCoeffSlop2', 'EgyConsSlopReducCoeffSlop6', 'EgyConsSlopReducCoeffSlop10', 'EgyConsSlopReducCoeffSlop14', 'EgyConsSlopReducCoeffSlop8'], 'EgyConsSlopRiseCoeff': ['EgyConsSlopRiseCoeffSlop14', 'EgyConsSlopRiseCoeffSlop6', 'EgyConsSlopRiseCoeffSlop2', 'EgyConsSlopRiseCoeffSlop4', 'EgyConsSlopRiseCoeffSlop8', 'EgyConsSlopRiseCoeffSlop12', 'EgyConsSlopRiseCoeffSlop10'], 'VehAxleTqDistbnAct': ['VehAxleTqDistbnActManualAuto', 'VehAxleTqDistbnActPerc']}

    class AccrTqModSteplessAct:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "Drive torque mode stepless adjustment of actual feedback, 1-100 percentage."
        signal_length = 8
        start_position = 7
        value_definition = {}

    class BookChrgnActStsFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 18
        signal_description = "Feedback status of book charging"
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' BookChrgnSts_Default', '0x1': ' BookChrgnSts_Success', '0x2': ' BookChrgnSts_Finished', '0x3': ' BookChrgnSts_Fail'}

    class BookChrgnTarSocFb:
        comments = ""
        factor = 0.1
        initial_value = 1020
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "Charge target SOC (explicit value) feedback "
        signal_length = 10
        start_position = 13
        value_definition = {}

    class C1TargetChrgU:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 16
        signal_description = "C1 Capacitor charging target voltage"
        signal_length = 16
        start_position = 31
        value_definition = {}

    class ChrgnEquipMaxI:
        comments = ""
        factor = 0.1
        initial_value = 30000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -3000
        sig_ub = 93
        signal_description = "The maximum output current from the DC charging equipment."
        signal_length = 16
        start_position = 47
        value_definition = {}

    class ChrgnEquipMaxU:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "The maximum output voltage from the DC charging equipment."
        signal_length = 16
        start_position = 63
        value_definition = {}

    class ChrgnOrDChrgnStsFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 92
        signal_description = "Charging and discharging status feedback."
        signal_length = 5
        start_position = 79
        value_definition = {'0x0': ' ChrgnOrDChrgnSts_default', '0x1': ' ChrgnOrDChrgnSts_NoCharging', '0x2': ' ChrgnOrDChrgnSts_ACCharging', '0x3': ' ChrgnOrDChrgnSts_ACChargingEnd', '0x4': ' ChrgnOrDChrgnSts_ChrgnCmpl', '0x5': ' ChrgnOrDChrgnSts_Heating', '0x6': ' ChrgnOrDChrgnSts_BookCharging', '0x7': ' ChrgnOrDChrgnSts_NoDisCharging', '0x8': ' ChrgnOrDChrgnSts_DisCharging', '0x9': ' ChrgnOrDChrgnSts_DisChargingEnd', '0xA': ' ChrgnOrDChrgnSts_DisChrgnCmpl', '0xB': ' ChrgnOrDChrgnSts_ChrgnFault', '0xC': ' ChrgnOrDChrgnSts_DisChrgnFault', '0xD': ' ChrgnOrDChrgnSts_Reserved1', '0xE': ' ChrgnOrDChrgnSts_ACChrgnFltChrgrSide', '0xF': ' ChrgnOrDChrgnSts_DCCharging', '0x10': ' ChrgnOrDChrgnSts_Reserved2', '0x11': ' ChrgnOrDChrgnSts_Reserved3', '0x12': ' ChrgnOrDChrgnSts_ACChargingFaultVehSide', '0x13': ' ChrgnOrDChrgnSts_DCChargingFaultChrgrSideTemp', '0x14': ' ChrgnOrDChrgnSts_DCChargingFaultChrgrSideCon', '0x15': ' ChrgnOrDChrgnSts_DCChargingFaultChrgrSideHw', '0x16': ' ChrgnOrDChrgnSts_DCChargingFaultChrgrSideEmgy', '0x17': ' ChrgnOrDChrgnSts_DCChargingFaultChrgrSideCom', '0x18': ' ChrgnOrDChrgnSts_SuperCharging', '0x19': ' ChrgnOrDChrgnSts_ACChargingSuspend', '0x1A': ' ChrgnOrDChrgnSts_DCChargingEnd', '0x1B': ' ChrgnOrDChrgnSts_ACChrgnFltVehSide', '0x1C': ' ChrgnOrDChrgnSts_BoostCharging', '0x1D': ' ChrgnOrDChrgnSts_BoostchargingFlt', '0x1E': ' ChrgnOrDChrgnSts_WirelessCharging'}

    class ChrgnSpdIndcnVal:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 91
        signal_description = "Charging speed indication to driver in kph."
        signal_length = 11
        start_position = 74
        value_definition = {}

    class CrpModStsAct:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 90
        signal_description = "Actual Creep Mode status."
        signal_length = 2
        start_position = 95
        value_definition = {'0x0': ' OffOnInvld_Invalid1', '0x1': ' OffOnInvld_Off', '0x2': ' OffOnInvld_On', '0x3': ' OffOnInvld_Invalid2'}

    class DCChrgrPortTPosPortT:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -50
        sig_ub = 89
        signal_description = "Temperature of the positive column of the DC charging."
        signal_length = 8
        start_position = 103
        value_definition = {}

    class DCChrgrPortTNegPortT:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -50
        sig_ub = 89
        signal_description = "Temperature of the negative column of the DC charging."
        signal_length = 8
        start_position = 111
        value_definition = {}

    class DchaEgyAct:
        comments = ""
        factor = 100.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 88
        signal_description = "The OBC actual AC output discharging energy and which represents a discharge cycle"
        signal_length = 11
        start_position = 119
        value_definition = {}

    class DchaIAct:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 188
        signal_description = "The discharging current of AC"
        signal_length = 11
        start_position = 124
        value_definition = {}

    class DchaPwrAct:
        comments = ""
        factor = 100.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 187
        signal_description = "Acutual discharing power "
        signal_length = 11
        start_position = 129
        value_definition = {}

    class DchaUAct:
        comments = ""
        factor = 0.25
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 186
        signal_description = "The discharging voltage of AC"
        signal_length = 11
        start_position = 150
        value_definition = {}

    class DchrgChrgnTarSOCFb:
        comments = ""
        factor = 0.1
        initial_value = 200
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 185
        signal_description = "Discharge target SOC (apparent SOC) feedback "
        signal_length = 11
        start_position = 155
        value_definition = {}

    class DchrgPwrAllwd:
        comments = ""
        factor = 20.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 184
        signal_description = "Power available for Discharging in real time. From wall socket if plugged in, from propulsion or high voltage battery."
        signal_length = 10
        start_position = 160
        value_definition = {}

    class DischrgStopByTarDrvrIndcn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 427
        signal_description = "Discharge abort driver alert."
        signal_length = 2
        start_position = 182
        value_definition = {'0x0': ' ReqSts2_Default', '0x1': ' ReqSts2_NotReqd', '0x2': ' ReqSts2_Reqd', '0x3': ' ReqSts2_Reserved'}

    class DrvModAct:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 426
        signal_description = "Actual drive mode"
        signal_length = 4
        start_position = 180
        value_definition = {'0x0': ' DrvModReqType_Undefd', '0x1': ' DrvModReqType_ECO', '0x2': ' DrvModReqType_Comfort_Normal', '0x3': ' DrvModReqType_Dynamic_Sport', '0x4': ' DrvModReqType_Tank', '0x5': ' DrvModReqType_Offroad_CrossTerrain', '0x6': ' DrvModReqType_Adaptive', '0x7': ' DrvModReqType_Race', '0x8': ' DrvModReqType_Reserved', '0x9': ' DrvModReqType_ECO_PLUS', '0xA': ' DrvModReqType_Power', '0xB': ' DrvModReqType_Snow', '0xC': ' DrvModReqType_Sand', '0xD': ' DrvModReqType_Mud', '0xE': ' DrvModReqType_Rock', '0xF': ' DrvModReqType_Err'}

    class DrvModActInd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 425
        signal_description = "Customize the actual driving mode, including normal, sport, snow, etc"
        signal_length = 4
        start_position = 176
        value_definition = {'0x0': ' DrvModReqType_Undefd', '0x1': ' DrvModReqType_ECO', '0x2': ' DrvModReqType_Comfort_Normal', '0x3': ' DrvModReqType_Dynamic_Sport', '0x4': ' DrvModReqType_Tank', '0x5': ' DrvModReqType_Offroad_CrossTerrain', '0x6': ' DrvModReqType_Adaptive', '0x7': ' DrvModReqType_Race', '0x8': ' DrvModReqType_Reserved', '0x9': ' DrvModReqType_ECO_PLUS', '0xA': ' DrvModReqType_Power', '0xB': ' DrvModReqType_Snow', '0xC': ' DrvModReqType_Sand', '0xD': ' DrvModReqType_Mud', '0xE': ' DrvModReqType_Rock', '0xF': ' DrvModReqType_Err'}

    class EgyCnsFacVehSpdSpd40:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 424
        signal_description = "Energy consumption coefficiency at vehicle speeds=40kph."
        signal_length = 8
        start_position = 199
        value_definition = {}

    class EgyCnsFacVehSpdSpd140:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 424
        signal_description = "Energy consumption coefficiency at vehicle speeds=140kph."
        signal_length = 8
        start_position = 207
        value_definition = {}

    class EgyCnsFacVehSpdSpd20:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 424
        signal_description = "Energy consumption coefficiency at vehicle speeds=20kph."
        signal_length = 8
        start_position = 215
        value_definition = {}

    class EgyCnsFacVehSpdSpd60:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 424
        signal_description = "Energy consumption coefficiency at vehicle speeds=60kph."
        signal_length = 8
        start_position = 223
        value_definition = {}

    class EgyCnsFacVehSpdSpd100:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 424
        signal_description = "Energy consumption coefficiency at vehicle speeds=100kph."
        signal_length = 8
        start_position = 231
        value_definition = {}

    class EgyCnsFacVehSpdSpd120:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 424
        signal_description = "Energy consumption coefficiency at vehicle speeds=120kph."
        signal_length = 8
        start_position = 239
        value_definition = {}

    class EgyCnsFacVehSpdSpd10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 424
        signal_description = "Energy consumption coefficiency at vehicle speeds=10kph."
        signal_length = 8
        start_position = 247
        value_definition = {}

    class EgyCnsFacVehSpdSpd80:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 424
        signal_description = "Energy consumption coefficiency at vehicle speeds=80kph."
        signal_length = 8
        start_position = 255
        value_definition = {}

    class EgyConsSlopReducCoeffSlop4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 475
        signal_description = "Energy consumption reduce coefficiency at road slopes=-4 degrees."
        signal_length = 7
        start_position = 263
        value_definition = {}

    class EgyConsSlopReducCoeffSlop12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 475
        signal_description = "Energy consumption reduce coefficiency at road slopes=-12 degrees."
        signal_length = 7
        start_position = 256
        value_definition = {}

    class EgyConsSlopReducCoeffSlop2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 475
        signal_description = "Energy consumption reduce coefficiency at road slopes=-2 degrees."
        signal_length = 7
        start_position = 265
        value_definition = {}

    class EgyConsSlopReducCoeffSlop6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 475
        signal_description = "Energy consumption reduce coefficiency at road slopes=-6 degrees."
        signal_length = 7
        start_position = 274
        value_definition = {}

    class EgyConsSlopReducCoeffSlop10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 475
        signal_description = "Energy consumption reduce coefficiency at road slopes=-10 degrees."
        signal_length = 7
        start_position = 283
        value_definition = {}

    class EgyConsSlopReducCoeffSlop14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 475
        signal_description = "Energy consumption reduce coefficiency at road slopes=-14 degrees."
        signal_length = 7
        start_position = 292
        value_definition = {}

    class EgyConsSlopReducCoeffSlop8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 475
        signal_description = "Energy consumption reduce coefficiency at road slopes=-8 degrees."
        signal_length = 7
        start_position = 301
        value_definition = {}

    class EgyConsSlopRiseCoeffSlop14:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 474
        signal_description = "Energy consumption rise coefficiency at road slopes=14 degrees."
        signal_length = 7
        start_position = 310
        value_definition = {}

    class EgyConsSlopRiseCoeffSlop6:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 474
        signal_description = "Energy consumption rise coefficiency at road slopes=6 degrees."
        signal_length = 7
        start_position = 319
        value_definition = {}

    class EgyConsSlopRiseCoeffSlop2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 474
        signal_description = "Energy consumption rise coefficiency at road slopes=2 degrees."
        signal_length = 7
        start_position = 312
        value_definition = {}

    class EgyConsSlopRiseCoeffSlop4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 474
        signal_description = "Energy consumption rise coefficiency at road slopes=4 degrees."
        signal_length = 7
        start_position = 321
        value_definition = {}

    class EgyConsSlopRiseCoeffSlop8:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 474
        signal_description = "Energy consumption rise coefficiency at road slopes=8 degrees."
        signal_length = 7
        start_position = 330
        value_definition = {}

    class EgyConsSlopRiseCoeffSlop12:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 474
        signal_description = "Energy consumption rise coefficiency at road slopes=12 degrees."
        signal_length = 7
        start_position = 339
        value_definition = {}

    class EgyConsSlopRiseCoeffSlop10:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 474
        signal_description = "Energy consumption rise coefficiency at road slopes=10 degrees."
        signal_length = 7
        start_position = 348
        value_definition = {}

    class EgyResdOfDischrg:
        comments = ""
        factor = 20.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 473
        signal_description = "The reserved energy for discharge. "
        signal_length = 13
        start_position = 357
        value_definition = {}

    class EgyRgnLimCmpSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 472
        signal_description = "Braking compensation function status feedback when energy recovery is limited "
        signal_length = 2
        start_position = 360
        value_definition = {'0x1': ' CrsCtrlrSts_Off', '0x2': ' CrsCtrlrSts_Stb', '0x3': ' CrsCtrlrSts_Actv'}

    class FrntMotPwrLimMax:
        comments = ""
        factor = 0.5
        initial_value = 1022
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -511
        sig_ub = 487
        signal_description = "Maximum usable power limit of front motor"
        signal_length = 11
        start_position = 374
        value_definition = {}

    class FrntMotPwrLimMin:
        comments = ""
        factor = 0.5
        initial_value = 1022
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -511
        sig_ub = 486
        signal_description = "Minimum usable power limit of front motor"
        signal_length = 11
        start_position = 379
        value_definition = {}

    class HMIBrkRgnPwrPercMin:
        comments = ""
        factor = 0.1
        initial_value = 500
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -50
        sig_ub = 485
        signal_description = "Percentage of maximum available energy recovery capacity "
        signal_length = 10
        start_position = 384
        value_definition = {}

    class HMIDstEstimdFromTarFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 484
        signal_description = "Whether the current available energy meets the status information feedback of the target driving distance"
        signal_length = 3
        start_position = 406
        value_definition = {}

    class HMIDstEstimdRemainDstRngECO:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 483
        signal_description = "Forecast remaining range in economy driving mode (air conditioning off)"
        signal_length = 10
        start_position = 403
        value_definition = {}

    class HMIEgyRgnLimCmpMsg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 482
        signal_description = "Energy recovery limited, braking compensation function activated"
        signal_length = 4
        start_position = 409
        value_definition = {}

    class HMIEstimdRemainDstRng:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 600
        signal_description = "Remaining range."
        signal_length = 10
        start_position = 421
        value_definition = {}

    class HMIHvBattEgyIn:
        comments = ""
        factor = 0.5
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 615
        signal_description = "Electric battery energy absorbed by the HV Battery"
        signal_length = 8
        start_position = 439
        value_definition = {}

    class HMIHvBattEgyOut:
        comments = ""
        factor = 0.5
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 614
        signal_description = "Electric battery energy delivered by the HV Battery. "
        signal_length = 8
        start_position = 447
        value_definition = {}

    class HMIPrpsnSysEgyRgnPwrLimd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 613
        signal_description = "Power system energy recovery power is limited or not"
        signal_length = 2
        start_position = 455
        value_definition = {'0x0': ' OffOnInvld_Invalid1', '0x1': ' OffOnInvld_Off', '0x2': ' OffOnInvld_On', '0x3': ' OffOnInvld_Invalid2'}

    class HMIPrpsnSysMod:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 612
        signal_description = "Drive system energy flow status display "
        signal_length = 4
        start_position = 453
        value_definition = {}

    class HMIPwrPrpsnPercAct:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 611
        signal_description = "Actual driving power as a percentage of total power "
        signal_length = 11
        start_position = 449
        value_definition = {}

    class HMIStopModAct:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 609
        signal_description = "Stop mode feedback, including: stop, slow, roll."
        signal_length = 3
        start_position = 470
        value_definition = {'0x0': ' EPedlMod_Initial', '0x1': ' EPedlMod_Crp', '0x2': ' EPedlMod_EPedl', '0x3': ' EPedlMod_Roll', '0x4': ' EPedlMod_Resvd'}

    class HMIVehSpdLimnIndcnMsg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 608
        signal_description = "Feedback of the speed limiting function, including the information that the speed limiting has been canceled or disabled."
        signal_length = 4
        start_position = 467
        value_definition = {}

    class HMIVehSpdLimnVisAudWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 623
        signal_description = "The vehicle speed limit function indicates when the set speed limit is exceeded, including voice and text."
        signal_length = 2
        start_position = 479
        value_definition = {'0x0': ' AdjSpdLimnWarnCoding_NoWarn', '0x1': ' AdjSpdLimnWarnCoding_SoundWarn', '0x2': ' AdjSpdLimnWarnCoding_VisWarn', '0x3': ' AdjSpdLimnWarnCoding_SoundAndVisWarn'}

    class HVChrgnAllwd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 622
        signal_description = "Charge permit signal "
        signal_length = 2
        start_position = 477
        value_definition = {'0x0': ' ChrgnAllwd_Init', '0x1': ' ChrgnAllwd_NOK', '0x2': ' ChrgnAllwd_OK', '0x3': ' ChrgnAllwd_HOLD'}

    class HVPwrAvlForClimaEstim:
        comments = ""
        factor = 20.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 621
        signal_description = "Power available for climatization"
        signal_length = 10
        start_position = 481
        value_definition = {}

    class MaxACInpISetFdb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 620
        signal_description = "Feedback received Maximum AC Input Current Setting"
        signal_length = 8
        start_position = 503
        value_definition = {}

    class OnBdChrgrCCResis:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 619
        signal_description = "OBC CC resistance"
        signal_length = 16
        start_position = 511
        value_definition = {}

    class OnBdChrgrIAct:
        comments = ""
        factor = 0.1
        initial_value = 2000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -200
        sig_ub = 610
        signal_description = "The actual AC input current"
        signal_length = 12
        start_position = 527
        value_definition = {}

    class OnBdChrgrIDc:
        comments = ""
        factor = 0.1
        initial_value = 2000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -200
        sig_ub = 618
        signal_description = "The actual DC output current of OBC"
        signal_length = 12
        start_position = 531
        value_definition = {}

    class OnBdChrgrUAct:
        comments = ""
        factor = 0.25
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 617
        signal_description = "The actual AC input voltage"
        signal_length = 11
        start_position = 551
        value_definition = {}

    class OnBdChrgrUDc:
        comments = ""
        factor = 0.2
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 616
        signal_description = "The actual DC output voltage of OBC"
        signal_length = 13
        start_position = 556
        value_definition = {}

    class PwrDegradedSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 631
        signal_description = "Onboard Charger power derating reasons(such as charging socket over temperature,OBC over temperature,.etc)"
        signal_length = 4
        start_position = 575
        value_definition = {'0x0': ' PwrDegraded_Default', '0x1': ' PwrDegraded_OBCOverT', '0x2': ' PwrDegraded_ChrgrOverT', '0x3': ' PwrDegraded_HndlLockgFlt', '0x4': ' PwrDegraded_IntElecFlt', '0x5': ' PwrDegraded_OBCCoolingOverT', '0x6': ' PwrDegraded_OBCLowT', '0x7': ' PwrDegraded_Reserved8'}

    class PwrEgyMgrAvl:
        comments = ""
        factor = 20.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 630
        signal_description = "Available power from OBC to HVEPM (HV Energy Power Manager)"
        signal_length = 13
        start_position = 571
        value_definition = {}

    class ReMotPwrLimMax:
        comments = ""
        factor = 0.5
        initial_value = 1022
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -511
        sig_ub = 629
        signal_description = "Maximum usable power limit of rear motor "
        signal_length = 11
        start_position = 590
        value_definition = {}

    class ReMotPwrLimMin:
        comments = ""
        factor = 0.5
        initial_value = 1022
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -511
        sig_ub = 628
        signal_description = "Minimum usable power limit of rear motor"
        signal_length = 11
        start_position = 595
        value_definition = {}

    class TyreSlipRatFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 627
        signal_description = "Left front tire slip rate."
        signal_length = 7
        start_position = 625
        value_definition = {}

    class TyreSlipRatFrntRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 626
        signal_description = "Right front tire slip rate."
        signal_length = 7
        start_position = 634
        value_definition = {}

    class TyreSlipRatReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 658
        signal_description = "Left rear tire slip rate."
        signal_length = 7
        start_position = 643
        value_definition = {}

    class TyreSlipRatReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 657
        signal_description = "Right rear tire slip rate. "
        signal_length = 7
        start_position = 652
        value_definition = {}

    class V2XDchaSwtFdb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 656
        signal_description = "OBC feedback discharging switch status."
        signal_length = 3
        start_position = 661
        value_definition = {}

    class VehAxleTqDistbnActManualAuto:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 675
        signal_description = "Can distinguish between manual and automatic."
        signal_length = 4
        start_position = 679
        value_definition = {'0x0': ' VehAxleTqDistbnMod_Initial', '0x1': ' VehAxleTqDistbnMod_Auto', '0x2': ' VehAxleTqDistbnMod_Manual', '0x3': ' VehAxleTqDistbnMod_Unknow', '0x4': ' VehAxleTqDistbnMod_Reserved'}

    class VehAxleTqDistbnActPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 675
        signal_description = "The range is 0-100 percent, 1 represents the front motor distribution 100 percent, the rear motor distribution 0 .100 percent means that the front motor is allocated 0, the back motor is allocated 100 percent, and so on. "
        signal_length = 8
        start_position = 671
        value_definition = {}

    class VehAxleTqDistbnModAct:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 683
        signal_description = "Actual vehicle axle torque distribution mode"
        signal_length = 4
        start_position = 687
        value_definition = {'0x0': ' VehAxleTqDistbnMod_Initial', '0x1': ' VehAxleTqDistbnMod_Auto', '0x2': ' VehAxleTqDistbnMod_Manual', '0x3': ' VehAxleTqDistbnMod_Unknow', '0x4': ' VehAxleTqDistbnMod_Reserved'}


class CCUMCUCDToCCUSOCCDEthSignalIPdu22:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204016
    pdu_length_bytes = 4
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {}

    class PrpsnDevelpSignalGroup1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Powertrain test frame, containing internal variables."
        signal_length = 8
        start_position = 7
        value_definition = {}

    class PrpsnDevelpSignalGroup2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Powertrain test frame, containing internal variables."
        signal_length = 8
        start_position = 15
        value_definition = {}

    class PrpsnDevelpSignalGroup3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Powertrain test frame, containing internal variables."
        signal_length = 8
        start_position = 23
        value_definition = {}

    class PrpsnDevelpSignalGroup4:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Powertrain test frame, containing internal variables."
        signal_length = 8
        start_position = 31
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthSignalIPdu18:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x204012
    pdu_length_bytes = 9
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-20ms"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {}

    class AccrpedlFltSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 33
        signal_description = " It should provide acceleration pedal Status signal ( AccrpedlSts ) to predict whether the accelerator pedal  has fault or not.1-Fault 0-NoFault"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class BrkPrioActvorNot:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 34
        signal_description = "Brake priority mode active or not"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' Actv_NoActv', '0x1': ' Actv_Actv', '0x2': ' Actv_Reserved1', '0x3': ' Actv_Reserved2'}

    class DCChrgModReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "DC charging mode request"
        signal_length = 3
        start_position = 3
        value_definition = {'0x0': ' DCChrgModReq_Default', '0x1': ' DCChrgModReq_CC', '0x2': ' DCChrgModReq_CV', '0x3': ' DCChrgModReq_Reserved1', '0x4': ' DCChrgModReq_Reserved2', '0x5': ' DCChrgModReq_Reserved3', '0x6': ' DCChrgModReq_Reserved4', '0x7': ' DCChrgModReq_Reserved5'}

    class DCChrgnLockCtrl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 51
        signal_description = "The state of DC charging port locking control request. Off is unlock,on is lock."
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class DisChrgrFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 50
        signal_description = "Discharge gun marker "
        signal_length = 2
        start_position = 15
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}

    class HMIEPedlInhbnFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 49
        signal_description = "E-Pedal inhibit flag."
        signal_length = 2
        start_position = 13
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class HMIEPedlModSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 48
        signal_description = "Pedal mode deceleration function status feedback. "
        signal_length = 2
        start_position = 11
        value_definition = {'0x1': ' CrsCtrlrSts_Off', '0x2': ' CrsCtrlrSts_Stb', '0x3': ' CrsCtrlrSts_Actv'}

    class HMIHvBattSOC:
        comments = ""
        factor = 0.1
        initial_value = 1020
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 63
        signal_description = "Displayed High voltage battery SOC"
        signal_length = 10
        start_position = 9
        value_definition = {}

    class HVBattChrgCmpl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 62
        signal_description = "Plug-in charging of the HV Battery is completed/not completed."
        signal_length = 2
        start_position = 31
        value_definition = {'0x0': ' NoYesUkwn_No', '0x1': ' NoYesUkwn_Yes', '0x2': ' NoYesUkwn_Unknown', '0x3': ' NoYesUkwn_Reserved'}

    class HVBattPreHeatgFaild:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 61
        signal_description = "HV Battery preheating  failed  before charging  due to small charging power."
        signal_length = 2
        start_position = 29
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}

    class HVChrgnStopReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 60
        signal_description = "Stop charging request"
        signal_length = 2
        start_position = 27
        value_definition = {'0x0': ' HVChrgnStopReq_Default', '0x1': ' HVChrgnStopReq_BST', '0x2': ' HVChrgnStopReq_CST', '0x3': ' HVChrgnStopReq_Reserved'}

    class OnBdChrgrPwrEnaAllwd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 59
        signal_description = "Ac charge allowance"
        signal_length = 1
        start_position = 25
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class OnBdChrgrS2Sts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 58
        signal_description = "Onboard Charger S2 contactor status"
        signal_length = 2
        start_position = 24
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}

    class OwnBrandChrgrFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 57
        signal_description = "The recongnised status for JIDU charger"
        signal_length = 2
        start_position = 38
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}

    class PrpsnEgyRgnLimCmpAllwd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 56
        signal_description = "The brake compensation function allows flag bits when energy recovery is limited"
        signal_length = 2
        start_position = 36
        value_definition = {'0x0': ' AllwdorNot_Init', '0x1': ' AllwdorNot_NotAllwd', '0x2': ' AllwdorNot_Allwd', '0x3': ' AllwdorNot_Resd1'}

    class PrpsnEgyRgnLvlAct:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 71
        signal_description = "Energy recovery level actual feedback, according to the request value feedback actual value. "
        signal_length = 8
        start_position = 47
        value_definition = {}

    class VehSpdLimnAllwd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 70
        signal_description = "Whether the speed limiting function allows feedback. "
        signal_length = 2
        start_position = 55
        value_definition = {'0x0': ' AllwdorNot_Init', '0x1': ' AllwdorNot_NotAllwd', '0x2': ' AllwdorNot_Allwd', '0x3': ' AllwdorNot_Resd1'}

    class VehSpdLimnModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 69
        signal_description = "Vehicle Speed limiting function mode status feedback. "
        signal_length = 2
        start_position = 53
        value_definition = {'0x0': ' OffStbActvOvrd_Off', '0x1': ' OffStbActvOvrd_Stb', '0x2': ' OffStbActvOvrd_Actv', '0x3': ' OffStbActvOvrd_Ovrd'}


class CCUMCUCDToCCUSOCCDEthDIDPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x2040F0
    pdu_length_bytes = 1027
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {'CDMCUDiagDIDInfo': ['CDMCUDiagDIDInfoDIDCode', 'CDMCUDiagDIDInfoLength']}

    class CDMCUDiagDIDInfoDIDCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DID Code info"
        signal_length = 16
        start_position = 7
        value_definition = {}

    class CDMCUDiagDIDInfoLength:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DID data length"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class CDMCUDiagDIDInfoData:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "DID payload  data"
        signal_length = 8192
        start_position = 24
        value_definition = {}


class CCUMCUCDToCCUSOCCDEthDummyPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x2040F1
    pdu_length_bytes = 1024
    receiver = ['CCUSOCCD']
    send_type = "EventTriggered"
    sender = "CCUMCUCD"
    server_socket = "SocketCdMcuSoAdUDP"
    signal_group = {}

    class CDMCU2CDSOCDummyData:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Dynamic array for backup use between CDMCU & CDSOC"
        signal_length = 8192
        start_position = 0
        value_definition = {}
