

class LCURToCCUSOCCDEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x604001
    pdu_length_bytes = 160
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-100ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'AirFragCh1Sts': ['AirFragCh1StsRunngSts', 'AirFragCh1StsTyp', 'AirFragCh1StsAvlTi', 'AirFragCh1StsMotErr', 'AirFragCh1StsRelsRatFb', 'AirFragCh1StsUseUpWarn', 'AirFragCh1StsChgSts'], 'AirFragCh2Sts': ['AirFragCh2StsTyp', 'AirFragCh2StsAvlTi', 'AirFragCh2StsChgSts', 'AirFragCh2StsMotErr', 'AirFragCh2StsUseUpWarn', 'AirFragCh2StsRunngSts', 'AirFragCh2StsRelsRatFb'], 'AirFragCh3Sts': ['AirFragCh3StsRelsRatFb', 'AirFragCh3StsUseUpWarn', 'AirFragCh3StsTyp', 'AirFragCh3StsRunngSts', 'AirFragCh3StsChgSts', 'AirFragCh3StsAvlTi', 'AirFragCh3StsMotErr'], 'AirFragCh4Sts': ['AirFragCh4StsRunngSts', 'AirFragCh4StsRelsRatFb', 'AirFragCh4StsChgSts', 'AirFragCh4StsMotErr', 'AirFragCh4StsUseUpWarn', 'AirFragCh4StsAvlTi', 'AirFragCh4StsTyp'], 'AirFragCh5Sts': ['AirFragCh5StsTyp', 'AirFragCh5StsMotErr', 'AirFragCh5StsRelsRatFb', 'AirFragCh5StsAvlTi', 'AirFragCh5StsRunngSts', 'AirFragCh5StsChgSts', 'AirFragCh5StsUseUpWarn'], 'AirFragCtrlrErr': ['AirFragCtrlrErrFan', 'AirFragCtrlrErrUnderVolt', 'AirFragCtrlrErrOverVolt', 'AirFragCtrlrErrTemp', 'AirFragCtrlrErrMemChks'], 'AnionGenrSts': ['AnionGenrStsElecErr', 'AnionGenrStsRunngSts', 'AnionGenrStsVoltErr'], 'BEXVReq': ['BEXVReqExvCalReq', 'BEXVReqExvMovEna', 'BEXVReqExvPreHeatgReq', 'BEXVReqExvPosnReq'], 'BoostBlwrSts': ['BoostBlwrStsActPWM', 'BoostBlwrStsVoltErr', 'BoostBlwrStsOnOffSts', 'BoostBlwrStsElecErr', 'BoostBlwrStsOverTemp', 'BoostBlwrStsEgyLim'], 'CERVReq': ['CERVReqExvPosnReq', 'CERVReqExvPreHeatgReq', 'CERVReqExvMovEna', 'CERVReqExvCalReq'], 'EEXVReq': ['EEXVReqExvMovEna', 'EEXVReqExvPosnReq', 'EEXVReqExvCalReq', 'EEXVReqExvPreHeatgReq'], 'ElecVentStsFrntRiLeX': ['ElecVentStsFrntRiLeXBlkSts', 'ElecVentStsFrntRiLeXElecErr', 'ElecVentStsFrntRiLeXCalSts', 'ElecVentStsFrntRiLeXCalSuccessFlg', 'ElecVentStsFrntRiLeXSpdSts', 'ElecVentStsFrntRiLeXActPosn', 'ElecVentStsFrntRiLeXClrSts', 'ElecVentStsFrntRiLeXOverTemp', 'ElecVentStsFrntRiLeXDirSts', 'ElecVentStsFrntRiLeXRngFb', 'ElecVentStsFrntRiLeXRunngSts', 'ElecVentStsFrntRiLeXVoltErr'], 'ElecVentStsFrntRiLeY': ['ElecVentStsFrntRiLeYVoltErr', 'ElecVentStsFrntRiLeYDirSts', 'ElecVentStsFrntRiLeYBlkSts', 'ElecVentStsFrntRiLeYRngFb', 'ElecVentStsFrntRiLeYClrSts', 'ElecVentStsFrntRiLeYElecErr', 'ElecVentStsFrntRiLeYCalSts', 'ElecVentStsFrntRiLeYCalSuccessFlg', 'ElecVentStsFrntRiLeYOverTemp', 'ElecVentStsFrntRiLeYActPosn', 'ElecVentStsFrntRiLeYRunngSts', 'ElecVentStsFrntRiLeYSpdSts'], 'ElecVentStsFrntRiRiX': ['ElecVentStsFrntRiRiXVoltErr', 'ElecVentStsFrntRiRiXCalSuccessFlg', 'ElecVentStsFrntRiRiXRngFb', 'ElecVentStsFrntRiRiXActPosn', 'ElecVentStsFrntRiRiXOverTemp', 'ElecVentStsFrntRiRiXRunngSts', 'ElecVentStsFrntRiRiXBlkSts', 'ElecVentStsFrntRiRiXDirSts', 'ElecVentStsFrntRiRiXCalSts', 'ElecVentStsFrntRiRiXClrSts', 'ElecVentStsFrntRiRiXElecErr', 'ElecVentStsFrntRiRiXSpdSts'], 'ElecVentStsFrntRiRiY': ['ElecVentStsFrntRiRiYRunngSts', 'ElecVentStsFrntRiRiYCalSts', 'ElecVentStsFrntRiRiYSpdSts', 'ElecVentStsFrntRiRiYOverTemp', 'ElecVentStsFrntRiRiYActPosn', 'ElecVentStsFrntRiRiYClrSts', 'ElecVentStsFrntRiRiYRngFb', 'ElecVentStsFrntRiRiYVoltErr', 'ElecVentStsFrntRiRiYElecErr', 'ElecVentStsFrntRiRiYDirSts', 'ElecVentStsFrntRiRiYCalSuccessFlg', 'ElecVentStsFrntRiRiYBlkSts'], 'ExtrReViewMirrFailrPass': ['ExtrReViewMirrFailrPassAdjYMotFailr', 'ExtrReViewMirrFailrPassAdjXMotFailr', 'ExtrReViewMirrFailrPassFoldMotFailr'], 'FreshFlapSts': ['FreshFlapStsActPosn', 'FreshFlapStsURng', 'FreshFlapStsRunngSts', 'FreshFlapStsElecErr', 'FreshFlapStsCalSts', 'FreshFlapStsClrSts', 'FreshFlapStsOverTemp', 'FreshFlapStsDirSts', 'FreshFlapStsBlkSts', 'FreshFlapStsVoltErr'], 'InAirPM25Sts': ['InAirPM25StsFanErr', 'InAirPM25StsIntErr', 'InAirPM25StsElecErr', 'InAirPM25StsTempErr', 'InAirPM25StsVoltErr', 'InAirPM25StsRunngSts'], 'InAirPM25Val': ['InAirPM25ValDens', 'InAirPM25ValAQI'], 'ModFlapStsFrntRi': ['ModFlapStsFrntRiOverTemp', 'ModFlapStsFrntRiDirSts', 'ModFlapStsFrntRiCalSts', 'ModFlapStsFrntRiClrSts', 'ModFlapStsFrntRiURng', 'ModFlapStsFrntRiVoltErr', 'ModFlapStsFrntRiElecErr', 'ModFlapStsFrntRiActPosn', 'ModFlapStsFrntRiBlkSts', 'ModFlapStsFrntRiRunngSts'], 'ModFlapStsReRi': ['ModFlapStsReRiActPosn', 'ModFlapStsReRiCalSts', 'ModFlapStsReRiElecErr', 'ModFlapStsReRiRunngSts', 'ModFlapStsReRiBlkSts', 'ModFlapStsReRiVoltErr', 'ModFlapStsReRiClrSts', 'ModFlapStsReRiOverTemp', 'ModFlapStsReRiDirSts', 'ModFlapStsReRiURng'], 'OutAirQlyEstimd': ['OutAirQlyEstimdAQS', 'OutAirQlyEstimdAQSQf'], 'RecircFlapSts': ['RecircFlapStsDirSts', 'RecircFlapStsRunngSts', 'RecircFlapStsURng', 'RecircFlapStsCalSts', 'RecircFlapStsBlkSts', 'RecircFlapStsClrSts', 'RecircFlapStsOverTemp', 'RecircFlapStsActPosn', 'RecircFlapStsElecErr', 'RecircFlapStsVoltErr'], 'REXVReq': ['REXVReqExvMovEna', 'REXVReqExvPreHeatgReq', 'REXVReqExvCalReq', 'REXVReqExvPosnReq'], 'SeatAdj1RowRiStopCase': ['SeatAdj1RowRiStopCaseMotorStopCase', 'SeatAdj1RowRiStopCaseSeatCfg'], 'SeatAdj2RowRiStopCase': ['SeatAdj2RowRiStopCaseSeatCfg', 'SeatAdj2RowRiStopCaseMotorStopCase'], 'SeatAdj3RowRiStopCase': ['SeatAdj3RowRiStopCaseSeatCfg', 'SeatAdj3RowRiStopCaseMotorStopCase'], 'SeatClima1RowRiSts': ['SeatClima1RowRiStsTEstimd', 'SeatClima1RowRiStsHeatgActPwr', 'SeatClima1RowRiStsVentAvlSts', 'SeatClima1RowRiStsHeatgAvlSts', 'SeatClima1RowRiStsVentActPwr'], 'SeatClima2RowRiSts': ['SeatClima2RowRiStsVentActPwr', 'SeatClima2RowRiStsHeatgActPwr', 'SeatClima2RowRiStsTEstimd', 'SeatClima2RowRiStsVentAvlSts', 'SeatClima2RowRiStsHeatgAvlSts'], 'SeatClima3RowRiSts': ['SeatClima3RowRiStsHeatgAvlSts', 'SeatClima3RowRiStsVentActPwr', 'SeatClima3RowRiStsVentAvlSts', 'SeatClima3RowRiStsHeatgActPwr', 'SeatClima3RowRiStsTEstimd'], 'SeatClimaRiHeatgBtnSts': ['SeatClimaRiHeatgBtnStsRow2', 'SeatClimaRiHeatgBtnStsRow1', 'SeatClimaRiHeatgBtnStsRow3'], 'TempFlapStsFrntRi': ['TempFlapStsFrntRiRunngSts', 'TempFlapStsFrntRiDirSts', 'TempFlapStsFrntRiCalSts', 'TempFlapStsFrntRiOverTemp', 'TempFlapStsFrntRiClrSts', 'TempFlapStsFrntRiBlkSts', 'TempFlapStsFrntRiElecErr', 'TempFlapStsFrntRiActPosn', 'TempFlapStsFrntRiURng', 'TempFlapStsFrntRiVoltErr'], 'TempFlapStsReRi': ['TempFlapStsReRiVoltErr', 'TempFlapStsReRiRunngSts', 'TempFlapStsReRiDirSts', 'TempFlapStsReRiBlkSts', 'TempFlapStsReRiClrSts', 'TempFlapStsReRiURng', 'TempFlapStsReRiCalSts', 'TempFlapStsReRiActPosn', 'TempFlapStsReRiElecErr', 'TempFlapStsReRiOverTemp'], 'TERVReq': ['TERVReqExvMovEna', 'TERVReqExvPosnReq', 'TERVReqExvCalReq', 'TERVReqExvPreHeatgReq'], 'TrErrFb': ['TrErrFbCinchMotThermErrFb', 'TrErrFbHalfClsErrFb', 'TrErrFbRelsgErrFb', 'TrErrFbCinchErrFb', 'TrErrFbRelsMotThermErrFb', 'TrErrFbSpindleMotThermErrFb'], 'VentAirTEstimdFrntRi': ['VentAirTEstimdFrntRiFaceTQf', 'VentAirTEstimdFrntRiFootT', 'VentAirTEstimdFrntRiFootTQf', 'VentAirTEstimdFrntRiFaceT'], 'VentAirTEstimdReRi': ['VentAirTEstimdReRiFaceTQf', 'VentAirTEstimdReRiFootT', 'VentAirTEstimdReRiFootTQf', 'VentAirTEstimdReRiFaceT'], 'WERVReq': ['WERVReqExvPreHeatgReq', 'WERVReqExvMovEna', 'WERVReqExvCalReq', 'WERVReqExvPosnReq']}

    class AirFragActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 36
        signal_description = "Air Fragrance Unit Actual Power"
        signal_length = 6
        start_position = 7
        value_definition = {}

    class AirFragCh1StsRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 35
        signal_description = "Air Fragrance Channel 1 Running Status"
        signal_length = 1
        start_position = 1
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class AirFragCh1StsTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 35
        signal_description = "Air Fragrance Channel 1 Type"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class AirFragCh1StsAvlTi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 35
        signal_description = "Air Fragrance Channel 1 Available Time"
        signal_length = 9
        start_position = 23
        value_definition = {}

    class AirFragCh1StsMotErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 35
        signal_description = "Air Fragrance Channel 1 Motor Error"
        signal_length = 1
        start_position = 30
        value_definition = {'0x0': ' AirFragMotErr_NoErr', '0x1': ' AirFragMotErr_Err'}

    class AirFragCh1StsRelsRatFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 35
        signal_description = "Air Fragrance Channel 1 Release Ratio Feedback"
        signal_length = 7
        start_position = 29
        value_definition = {}

    class AirFragCh1StsUseUpWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 35
        signal_description = "Air Fragrance Channel 1 Use Up Warning"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': ' AirFragUseUpWarn_NoWarn', '0x1': ' AirFragUseUpWarn_Warn'}

    class AirFragCh1StsChgSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 35
        signal_description = "Air Fragrance Channel 1 Changing Status"
        signal_length = 2
        start_position = 38
        value_definition = {'0x0': ' AirFragChgSts_Initial', '0x1': ' AirFragChgSts_Changing', '0x2': ' AirFragChgSts_ChangeSucceeded', '0x3': ' AirFragChgSts_ChangeFailed'}

    class AirFragCh2StsTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 34
        signal_description = "Air Fragrance Channel 2 Type"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class AirFragCh2StsAvlTi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 34
        signal_description = "Air Fragrance Channel 2 Available Time"
        signal_length = 9
        start_position = 55
        value_definition = {}

    class AirFragCh2StsChgSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 34
        signal_description = "Air Fragrance Channel 2 Changing Status"
        signal_length = 2
        start_position = 62
        value_definition = {'0x0': ' AirFragChgSts_Initial', '0x1': ' AirFragChgSts_Changing', '0x2': ' AirFragChgSts_ChangeSucceeded', '0x3': ' AirFragChgSts_ChangeFailed'}

    class AirFragCh2StsMotErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 34
        signal_description = "Air Fragrance Channel 2 Motor Error"
        signal_length = 1
        start_position = 60
        value_definition = {'0x0': ' AirFragMotErr_NoErr', '0x1': ' AirFragMotErr_Err'}

    class AirFragCh2StsUseUpWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 34
        signal_description = "Air Fragrance Channel 2 Use Up Warning"
        signal_length = 1
        start_position = 59
        value_definition = {'0x0': ' AirFragUseUpWarn_NoWarn', '0x1': ' AirFragUseUpWarn_Warn'}

    class AirFragCh2StsRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 34
        signal_description = "Air Fragrance Channel 2 Running Status"
        signal_length = 1
        start_position = 58
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class AirFragCh2StsRelsRatFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 34
        signal_description = "Air Fragrance Channel 2 Release Ratio Feedback"
        signal_length = 7
        start_position = 57
        value_definition = {}

    class AirFragCh3StsRelsRatFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 33
        signal_description = "Air Fragrance Channel 3 Release Ratio Feedback"
        signal_length = 7
        start_position = 79
        value_definition = {}

    class AirFragCh3StsUseUpWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 33
        signal_description = "Air Fragrance Channel 3 Use Up Warning"
        signal_length = 1
        start_position = 72
        value_definition = {'0x0': ' AirFragUseUpWarn_NoWarn', '0x1': ' AirFragUseUpWarn_Warn'}

    class AirFragCh3StsTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 33
        signal_description = "Air Fragrance Channel 3 Type"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class AirFragCh3StsRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 33
        signal_description = "Air Fragrance Channel 3 Running Status"
        signal_length = 1
        start_position = 95
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class AirFragCh3StsChgSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 33
        signal_description = "Air Fragrance Channel 3 Changing Status"
        signal_length = 2
        start_position = 94
        value_definition = {'0x0': ' AirFragChgSts_Initial', '0x1': ' AirFragChgSts_Changing', '0x2': ' AirFragChgSts_ChangeSucceeded', '0x3': ' AirFragChgSts_ChangeFailed'}

    class AirFragCh3StsAvlTi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 33
        signal_description = "Air Fragrance Channel 3 Available Time"
        signal_length = 9
        start_position = 92
        value_definition = {}

    class AirFragCh3StsMotErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 33
        signal_description = "Air Fragrance Channel 3 Motor Error"
        signal_length = 1
        start_position = 99
        value_definition = {'0x0': ' AirFragMotErr_NoErr', '0x1': ' AirFragMotErr_Err'}

    class AirFragCh4StsRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Air Fragrance Channel 4 Running Status"
        signal_length = 1
        start_position = 104
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class AirFragCh4StsRelsRatFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Air Fragrance Channel 4 Release Ratio Feedback"
        signal_length = 7
        start_position = 119
        value_definition = {}

    class AirFragCh4StsChgSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Air Fragrance Channel 4 Changing Status"
        signal_length = 2
        start_position = 108
        value_definition = {'0x0': ' AirFragChgSts_Initial', '0x1': ' AirFragChgSts_Changing', '0x2': ' AirFragChgSts_ChangeSucceeded', '0x3': ' AirFragChgSts_ChangeFailed'}

    class AirFragCh4StsMotErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Air Fragrance Channel 4 Motor Error"
        signal_length = 1
        start_position = 106
        value_definition = {'0x0': ' AirFragMotErr_NoErr', '0x1': ' AirFragMotErr_Err'}

    class AirFragCh4StsUseUpWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Air Fragrance Channel 4 Use Up Warning"
        signal_length = 1
        start_position = 105
        value_definition = {'0x0': ' AirFragUseUpWarn_NoWarn', '0x1': ' AirFragUseUpWarn_Warn'}

    class AirFragCh4StsAvlTi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Air Fragrance Channel 4 Available Time"
        signal_length = 9
        start_position = 112
        value_definition = {}

    class AirFragCh4StsTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 32
        signal_description = "Air Fragrance Channel 4 Type"
        signal_length = 8
        start_position = 135
        value_definition = {}

    class AirFragCh5StsTyp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 66
        signal_description = "Air Fragrance Channel 5 Type"
        signal_length = 8
        start_position = 143
        value_definition = {}

    class AirFragCh5StsMotErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 66
        signal_description = "Air Fragrance Channel 5 Motor Error"
        signal_length = 1
        start_position = 151
        value_definition = {'0x0': ' AirFragMotErr_NoErr', '0x1': ' AirFragMotErr_Err'}

    class AirFragCh5StsRelsRatFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 66
        signal_description = "Air Fragrance Channel 5 Release Ratio Feedback"
        signal_length = 7
        start_position = 150
        value_definition = {}

    class AirFragCh5StsAvlTi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 66
        signal_description = "Air Fragrance Channel 5 Available Time"
        signal_length = 9
        start_position = 159
        value_definition = {}

    class AirFragCh5StsRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 66
        signal_description = "Air Fragrance Channel 5 Running Status"
        signal_length = 1
        start_position = 166
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class AirFragCh5StsChgSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 66
        signal_description = "Air Fragrance Channel 5 Changing Status"
        signal_length = 2
        start_position = 165
        value_definition = {'0x0': ' AirFragChgSts_Initial', '0x1': ' AirFragChgSts_Changing', '0x2': ' AirFragChgSts_ChangeSucceeded', '0x3': ' AirFragChgSts_ChangeFailed'}

    class AirFragCh5StsUseUpWarn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 66
        signal_description = "Air Fragrance Channel 5 Use Up Warning"
        signal_length = 1
        start_position = 163
        value_definition = {'0x0': ' AirFragUseUpWarn_NoWarn', '0x1': ' AirFragUseUpWarn_Warn'}

    class AirFragCtrlrErrFan:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "Air Fragrance Unit Fan Error"
        signal_length = 1
        start_position = 162
        value_definition = {'0x0': ' Err1_NoErr', '0x1': ' Err1_Err'}

    class AirFragCtrlrErrUnderVolt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "Air Fragrance Unit Under Voltage"
        signal_length = 1
        start_position = 161
        value_definition = {'0x0': ' Err1_NoErr', '0x1': ' Err1_Err'}

    class AirFragCtrlrErrOverVolt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "Air Fragrance Unit Over Voltage"
        signal_length = 1
        start_position = 160
        value_definition = {'0x0': ' Err1_NoErr', '0x1': ' Err1_Err'}

    class AirFragCtrlrErrTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "Air Fragrance Unit Temperature Error"
        signal_length = 2
        start_position = 175
        value_definition = {'0x0': ' TempErr_Normal', '0x1': ' TempErr_OverTemp', '0x2': ' TempErr_UnderTemp', '0x3': ' TempErr_Invalid'}

    class AirFragCtrlrErrMemChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 65
        signal_description = "Air Fragrance Unit Memory Checksum Error"
        signal_length = 1
        start_position = 173
        value_definition = {'0x0': ' Err1_NoErr', '0x1': ' Err1_Err'}

    class AirFragInitSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 64
        signal_description = "Air Fragrance Unit Initialization Status"
        signal_length = 2
        start_position = 172
        value_definition = {'0x0': ' InitialSts_NoInitialization', '0x1': ' InitialSts_Initializing', '0x2': ' InitialSts_InitializationOK', '0x3': ' InitialSts_InitializationFailed'}

    class AirFragRelsLvlFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 98
        signal_description = "Air Fragrance Unit Release Level Feedback"
        signal_length = 2
        start_position = 170
        value_definition = {'0x0': ' ReqLvl_NoReq', '0x1': ' ReqLvl_LoReq', '0x2': ' ReqLvl_MidReq', '0x3': ' ReqLvl_HiReq'}

    class AnionGenrStsElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 97
        signal_description = "Anion Generator Electrical Error"
        signal_length = 2
        start_position = 168
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class AnionGenrStsRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 97
        signal_description = "Anion Generator Running Status"
        signal_length = 2
        start_position = 182
        value_definition = {'0x0': ' AGURunngSts_Off', '0x1': ' AGURunngSts_On', '0x2': ' AGURunngSts_Sleep', '0x3': ' AGURunngSts_Reserved'}

    class AnionGenrStsVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 97
        signal_description = "Anion Generator Voltage Error"
        signal_length = 2
        start_position = 180
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class BEXVReqExvCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 96
        signal_description = "Bexv calibration request."
        signal_length = 1
        start_position = 178
        value_definition = {'0x0': ' ExvCalibReq_NoReq', '0x1': ' ExvCalibReq_InitializationReq'}

    class BEXVReqExvMovEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 96
        signal_description = "Bexv move enable."
        signal_length = 1
        start_position = 177
        value_definition = {'0x0': ' ExvMovEnable_EXVNotEnable', '0x1': ' ExvMovEnable_EXVEnable'}

    class BEXVReqExvPreHeatgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 96
        signal_description = "Bexv heating request."
        signal_length = 1
        start_position = 176
        value_definition = {'0x0': ' ExvHeatdReq_NoReq', '0x1': ' ExvHeatdReq_PreHeatedReq'}

    class BEXVReqExvPosnReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 96
        signal_description = "Bexv postion request."
        signal_length = 10
        start_position = 191
        value_definition = {}

    class BoostBlwrStsActPWM:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 111
        signal_description = "Compartment Booster Blower Actual PWM"
        signal_length = 10
        start_position = 197
        value_definition = {}

    class BoostBlwrStsVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 111
        signal_description = "Compartment Booster Blower Voltage Error"
        signal_length = 2
        start_position = 203
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class BoostBlwrStsOnOffSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 111
        signal_description = "Compartment Booster Blower OnOff Status"
        signal_length = 2
        start_position = 201
        value_definition = {'0x0': ' BlwrSts_OFF', '0x1': ' BlwrSts_ON', '0x2': ' BlwrSts_Err', '0x3': ' BlwrSts_Reserved'}

    class BoostBlwrStsElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 111
        signal_description = "Compartment Booster Blower Electrical Error"
        signal_length = 2
        start_position = 215
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class BoostBlwrStsOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 111
        signal_description = "Compartment Booster Blower Over Temperature"
        signal_length = 1
        start_position = 213
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class BoostBlwrStsEgyLim:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 111
        signal_description = "Compartment Booster Blower Energy Limit Status"
        signal_length = 1
        start_position = 212
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CERVReqExvPosnReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 110
        signal_description = "Cerv postion request."
        signal_length = 10
        start_position = 211
        value_definition = {}

    class CERVReqExvPreHeatgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 110
        signal_description = "Cerv heating request."
        signal_length = 1
        start_position = 217
        value_definition = {'0x0': ' ExvHeatdReq_NoReq', '0x1': ' ExvHeatdReq_PreHeatedReq'}

    class CERVReqExvMovEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 110
        signal_description = "Cerv move enable."
        signal_length = 1
        start_position = 216
        value_definition = {'0x0': ' ExvMovEnable_EXVNotEnable', '0x1': ' ExvMovEnable_EXVEnable'}

    class CERVReqExvCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 110
        signal_description = "Cerv calibration request."
        signal_length = 1
        start_position = 231
        value_definition = {'0x0': ' ExvCalibReq_NoReq', '0x1': ' ExvCalibReq_InitializationReq'}

    class CmprRunTime:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 109
        signal_description = "Compressor Running Time"
        signal_length = 11
        start_position = 230
        value_definition = {}

    class CmprSpdAct:
        comments = ""
        factor = 50.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 235
        signal_description = "Compressor Actual Speed"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class CoolgFanCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 234
        signal_description = "Cooling Fan Command"
        signal_length = 10
        start_position = 255
        value_definition = {}

    class DefrstPassSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 233
        signal_description = "defrosting state of the passenger side mirror"
        signal_length = 2
        start_position = 261
        value_definition = {'0x0': ' OffOnTmroff_Off', '0x1': ' OffOnTmroff_On', '0x2': ' OffOnTmroff_TmrOff'}

    class EEXVReqExvMovEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 232
        signal_description = "Eexv move enable."
        signal_length = 1
        start_position = 259
        value_definition = {'0x0': ' ExvMovEnable_EXVNotEnable', '0x1': ' ExvMovEnable_EXVEnable'}

    class EEXVReqExvPosnReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 232
        signal_description = "Eexv postion request."
        signal_length = 10
        start_position = 258
        value_definition = {}

    class EEXVReqExvCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 232
        signal_description = "Eexv calibration request."
        signal_length = 1
        start_position = 264
        value_definition = {'0x0': ' ExvCalibReq_NoReq', '0x1': ' ExvCalibReq_InitializationReq'}

    class EEXVReqExvPreHeatgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 232
        signal_description = "Eexv heating request."
        signal_length = 1
        start_position = 279
        value_definition = {'0x0': ' ExvHeatdReq_NoReq', '0x1': ' ExvHeatdReq_PreHeatedReq'}

    class ElecVentStsFrntRiLeXBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Block Status"
        signal_length = 2
        start_position = 283
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ElecVentStsFrntRiLeXElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Electrical Error"
        signal_length = 2
        start_position = 281
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ElecVentStsFrntRiLeXCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Calibration Status"
        signal_length = 2
        start_position = 273
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ElecVentStsFrntRiLeXCalSuccessFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Calibration Success Flag"
        signal_length = 1
        start_position = 284
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class ElecVentStsFrntRiLeXSpdSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Speed Status"
        signal_length = 3
        start_position = 287
        value_definition = {'0x0': ' VentActrSpdSts_Stop', '0x1': ' VentActrSpdSts_Level1', '0x2': ' VentActrSpdSts_Level2', '0x3': ' VentActrSpdSts_Level3', '0x4': ' VentActrSpdSts_Level4', '0x5': ' VentActrSpdSts_Auto', '0x6': ' VentActrSpdSts_Reserved1', '0x7': ' VentActrSpdSts_Reserved2'}

    class ElecVentStsFrntRiLeXActPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Actual Position"
        signal_length = 16
        start_position = 295
        value_definition = {}

    class ElecVentStsFrntRiLeXClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Clear Block Status"
        signal_length = 2
        start_position = 311
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ElecVentStsFrntRiLeXOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Over Temperature"
        signal_length = 1
        start_position = 309
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ElecVentStsFrntRiLeXDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Running Direction"
        signal_length = 2
        start_position = 308
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ElecVentStsFrntRiLeXRngFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Working Range Feedback"
        signal_length = 10
        start_position = 306
        value_definition = {}

    class ElecVentStsFrntRiLeXRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Running Status"
        signal_length = 2
        start_position = 312
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ElecVentStsFrntRiLeXVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 278
        signal_description = "Vent Grill Motor 5 Voltage Error"
        signal_length = 2
        start_position = 326
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ElecVentStsFrntRiLeYVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Voltage Error"
        signal_length = 2
        start_position = 335
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ElecVentStsFrntRiLeYDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Running Direction"
        signal_length = 2
        start_position = 345
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ElecVentStsFrntRiLeYBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Block Status"
        signal_length = 2
        start_position = 347
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ElecVentStsFrntRiLeYRngFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Working Range Feedback"
        signal_length = 10
        start_position = 333
        value_definition = {}

    class ElecVentStsFrntRiLeYClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Clear Block Status"
        signal_length = 2
        start_position = 339
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ElecVentStsFrntRiLeYElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Electrical Error"
        signal_length = 2
        start_position = 337
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ElecVentStsFrntRiLeYCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Calibration Status"
        signal_length = 2
        start_position = 351
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ElecVentStsFrntRiLeYCalSuccessFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Calibration Success Flag"
        signal_length = 1
        start_position = 348
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class ElecVentStsFrntRiLeYOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Over Temperature"
        signal_length = 1
        start_position = 349
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ElecVentStsFrntRiLeYActPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Actual Position"
        signal_length = 16
        start_position = 359
        value_definition = {}

    class ElecVentStsFrntRiLeYRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Running Status"
        signal_length = 2
        start_position = 375
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ElecVentStsFrntRiLeYSpdSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 277
        signal_description = "Vent Grill Motor 6 Speed Status"
        signal_length = 3
        start_position = 373
        value_definition = {'0x0': ' VentActrSpdSts_Stop', '0x1': ' VentActrSpdSts_Level1', '0x2': ' VentActrSpdSts_Level2', '0x3': ' VentActrSpdSts_Level3', '0x4': ' VentActrSpdSts_Level4', '0x5': ' VentActrSpdSts_Auto', '0x6': ' VentActrSpdSts_Reserved1', '0x7': ' VentActrSpdSts_Reserved2'}

    class ElecVentStsFrntRiRiXVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Voltage Error"
        signal_length = 2
        start_position = 380
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ElecVentStsFrntRiRiXCalSuccessFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Calibration Success Flag"
        signal_length = 1
        start_position = 378
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class ElecVentStsFrntRiRiXRngFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Working Range Feedback"
        signal_length = 10
        start_position = 377
        value_definition = {}

    class ElecVentStsFrntRiRiXActPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Actual Position"
        signal_length = 16
        start_position = 399
        value_definition = {}

    class ElecVentStsFrntRiRiXOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Over Temperature"
        signal_length = 1
        start_position = 415
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ElecVentStsFrntRiRiXRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Running Status"
        signal_length = 2
        start_position = 414
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ElecVentStsFrntRiRiXBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Block Status"
        signal_length = 2
        start_position = 412
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ElecVentStsFrntRiRiXDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Running Direction"
        signal_length = 2
        start_position = 410
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ElecVentStsFrntRiRiXCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Calibration Status"
        signal_length = 2
        start_position = 408
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ElecVentStsFrntRiRiXClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Clear Block Status"
        signal_length = 2
        start_position = 422
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ElecVentStsFrntRiRiXElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Electrical Error"
        signal_length = 2
        start_position = 420
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ElecVentStsFrntRiRiXSpdSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Vent Grill Motor 7 Speed Status"
        signal_length = 3
        start_position = 418
        value_definition = {'0x0': ' VentActrSpdSts_Stop', '0x1': ' VentActrSpdSts_Level1', '0x2': ' VentActrSpdSts_Level2', '0x3': ' VentActrSpdSts_Level3', '0x4': ' VentActrSpdSts_Level4', '0x5': ' VentActrSpdSts_Auto', '0x6': ' VentActrSpdSts_Reserved1', '0x7': ' VentActrSpdSts_Reserved2'}

    class ElecVentStsFrntRiRiYRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Running Status"
        signal_length = 2
        start_position = 431
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ElecVentStsFrntRiRiYCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Calibration Status"
        signal_length = 2
        start_position = 429
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ElecVentStsFrntRiRiYSpdSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Speed Status"
        signal_length = 3
        start_position = 427
        value_definition = {'0x0': ' VentActrSpdSts_Stop', '0x1': ' VentActrSpdSts_Level1', '0x2': ' VentActrSpdSts_Level2', '0x3': ' VentActrSpdSts_Level3', '0x4': ' VentActrSpdSts_Level4', '0x5': ' VentActrSpdSts_Auto', '0x6': ' VentActrSpdSts_Reserved1', '0x7': ' VentActrSpdSts_Reserved2'}

    class ElecVentStsFrntRiRiYOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Over Temperature"
        signal_length = 1
        start_position = 424
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ElecVentStsFrntRiRiYActPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Actual Position"
        signal_length = 16
        start_position = 439
        value_definition = {}

    class ElecVentStsFrntRiRiYClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Clear Block Status"
        signal_length = 2
        start_position = 455
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ElecVentStsFrntRiRiYRngFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Working Range Feedback"
        signal_length = 10
        start_position = 453
        value_definition = {}

    class ElecVentStsFrntRiRiYVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Voltage Error"
        signal_length = 2
        start_position = 459
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ElecVentStsFrntRiRiYElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Electrical Error"
        signal_length = 2
        start_position = 457
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ElecVentStsFrntRiRiYDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Running Direction"
        signal_length = 2
        start_position = 471
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ElecVentStsFrntRiRiYCalSuccessFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Calibration Success Flag"
        signal_length = 1
        start_position = 469
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class ElecVentStsFrntRiRiYBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 275
        signal_description = "Vent Grill Motor 8 Block Status"
        signal_length = 2
        start_position = 468
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ExtrReViewMirrFailrPassAdjYMotFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 274
        signal_description = "the adjusting motor failure in the Y direction of external rear view mirror at passenger side"
        signal_length = 1
        start_position = 466
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ExtrReViewMirrFailrPassAdjXMotFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 274
        signal_description = "the adjusting motor failure in the X direction of external rear view mirror at passenger side"
        signal_length = 1
        start_position = 465
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ExtrReViewMirrFailrPassFoldMotFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 274
        signal_description = "the folding motor failure of external rear view mirror at passenger side"
        signal_length = 1
        start_position = 464
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class FRDoorManResistSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 324
        signal_description = "Door manual resistance status"
        signal_length = 2
        start_position = 479
        value_definition = {'0x0': ' DoorManResistsSts_NoResist', '0x1': ' DoorManResistsSts_Level1', '0x2': ' DoorManResistsSts_Level2'}

    class FRDoorSpdModeFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 323
        signal_description = "power side door mode status feedback"
        signal_length = 2
        start_position = 477
        value_definition = {'0x0': ' SpdMode_Low', '0x1': ' SpdMode_Middle', '0x2': ' SpdMode_High'}

    class FreshFlapStsActPosn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 322
        signal_description = "Compartment Fresh Flap Actual Position"
        signal_length = 10
        start_position = 475
        value_definition = {}

    class FreshFlapStsURng:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 322
        signal_description = "Compartment Fresh Flap Self-Learning Voltage Range"
        signal_length = 9
        start_position = 481
        value_definition = {}

    class FreshFlapStsRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 322
        signal_description = "Compartment Fresh Flap Running Status"
        signal_length = 2
        start_position = 488
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class FreshFlapStsElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 322
        signal_description = "Compartment Fresh Flap Electrical Error"
        signal_length = 2
        start_position = 502
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class FreshFlapStsCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 322
        signal_description = "Compartment Fresh Flap Calibration Status"
        signal_length = 2
        start_position = 500
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class FreshFlapStsClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 322
        signal_description = "Compartment Fresh Flap Clear Block Status"
        signal_length = 2
        start_position = 498
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class FreshFlapStsOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 322
        signal_description = "Compartment Fresh Flap Over Temperature"
        signal_length = 1
        start_position = 496
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class FreshFlapStsDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 322
        signal_description = "Compartment Fresh Flap Running Direction"
        signal_length = 2
        start_position = 511
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class FreshFlapStsBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 322
        signal_description = "Compartment Fresh Flap Block Status"
        signal_length = 2
        start_position = 509
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class FreshFlapStsVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 322
        signal_description = "Compartment Fresh Flap Voltage Error"
        signal_length = 2
        start_position = 507
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class GrillShttrCalEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 321
        signal_description = "AGM shutter calculation enable"
        signal_length = 2
        start_position = 505
        value_definition = {'0x0': ' EnableDisable4_NoCmd', '0x1': ' EnableDisable4_Disable', '0x2': ' EnableDisable4_Enable'}

    class GrillShttrCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 320
        signal_description = "AGM Automatic calibration request."
        signal_length = 1
        start_position = 519
        value_definition = {'0x0': ' ReqSts1_NotReqd', '0x1': ' ReqSts1_Reqd'}

    class GrillShttrPosnReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 370
        signal_description = "AGM Position Request"
        signal_length = 7
        start_position = 518
        value_definition = {}

    class GrillShttrTqBoostReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 369
        signal_description = "AGM torque boost request"
        signal_length = 4
        start_position = 527
        value_definition = {'0x0': ' TorqueBoost_TorqueMode0', '0x1': ' TorqueBoost_TorqueMode1', '0x2': ' TorqueBoost_BoostMode0', '0x3': ' TorqueBoost_BoostMode1'}

    class InAirPM25StsFanErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 368
        signal_description = "Inside Air PM2.5 Fan Error"
        signal_length = 2
        start_position = 523
        value_definition = {'0x0': ' PM25FanErr_NoErr', '0x1': ' PM25FanErr_SpeedUnstable', '0x2': ' PM25FanErr_PoorContact', '0x3': ' PM25FanErr_BrokenLine'}

    class InAirPM25StsIntErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 368
        signal_description = "Inside Air PM2.5 Internal Error"
        signal_length = 2
        start_position = 521
        value_definition = {'0x0': ' PM25IntErr_False', '0x1': ' PM25IntErr_True', '0x2': ' PM25IntErr_Reserved', '0x3': ' PM25IntErr_Signalinvalid'}

    class InAirPM25StsElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 368
        signal_description = "Inside Air PM2.5 Electrical Error"
        signal_length = 2
        start_position = 535
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class InAirPM25StsTempErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 368
        signal_description = "Inside Air PM2.5 Temperature Error"
        signal_length = 2
        start_position = 533
        value_definition = {'0x0': ' TempErr_Normal', '0x1': ' TempErr_OverTemp', '0x2': ' TempErr_UnderTemp', '0x3': ' TempErr_Invalid'}

    class InAirPM25StsVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 368
        signal_description = "Inside Air PM2.5 Voltage Error"
        signal_length = 2
        start_position = 531
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class InAirPM25StsRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 368
        signal_description = "Inside Air PM2.5 Running Status"
        signal_length = 3
        start_position = 529
        value_definition = {'0x0': ' PM25RunngSts_Initial', '0x1': ' PM25RunngSts_Collecting', '0x2': ' PM25RunngSts_Complete', '0x3': ' PM25RunngSts_Error'}

    class InAirPM25ValDens:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 383
        signal_description = "Inside Air PM2.5 Density"
        signal_length = 10
        start_position = 542
        value_definition = {}

    class InAirPM25ValAQI:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 383
        signal_description = "Inside Air PM2.5 Level"
        signal_length = 3
        start_position = 548
        value_definition = {'0x0': ' PM25AQI_Level1', '0x1': ' PM25AQI_Level2', '0x2': ' PM25AQI_Level3', '0x3': ' PM25AQI_Level4', '0x4': ' PM25AQI_Level5', '0x5': ' PM25AQI_Level6', '0x6': ' PM25AQI_Reserved', '0x7': ' PM25AQI_Invalid'}

    class IncarTFrntFanSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 382
        signal_description = "Fan For Front Incar Temperature Running Status"
        signal_length = 1
        start_position = 545
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class InnerLightingModSts:
        comments = ""
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 381
        signal_description = "the select mode feedback of the interior lamp"
        signal_length = 2
        start_position = 544
        value_definition = {'0x0': ' IntrLampSelnModFb_Idle', '0x1': ' IntrLampSelnModFb_OFF', '0x2': ' IntrLampSelnModFb_ON', '0x3': ' IntrLampSelnModFb_Auto'}

    class InsdAirPM25Dens:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 664
        signal_description = "Inside Air PM2.5 Density,ug/m3"
        signal_length = 10
        start_position = 558
        value_definition = {}

    class IRawLCU2:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 815
        signal_description = "Current"
        signal_length = 13
        start_position = 564
        value_definition = {}

    class ModFlapActModFrntRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 814
        signal_description = "Compartment Front Right Area Air Distribution Flap Actual Mode"
        signal_length = 3
        start_position = 583
        value_definition = {'0x0': ' ModFlapMod_Face', '0x1': ' ModFlapMod_Foot', '0x2': ' ModFlapMod_Defroster', '0x3': ' ModFlapMod_Face_Foot', '0x4': ' ModFlapMod_Face_Defroster', '0x5': ' ModFlapMod_Foot_Defroster', '0x6': ' ModFlapMod_Face_Foot_Defroster', '0x7': ' ModFlapMod_Auto'}

    class ModFlapActModReRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 813
        signal_description = "Compartment Rear Right Area Air Distribution Flap Actual Mode"
        signal_length = 3
        start_position = 580
        value_definition = {'0x0': ' ModFlapMod_Face', '0x1': ' ModFlapMod_Foot', '0x2': ' ModFlapMod_Defroster', '0x3': ' ModFlapMod_Face_Foot', '0x4': ' ModFlapMod_Face_Defroster', '0x5': ' ModFlapMod_Foot_Defroster', '0x6': ' ModFlapMod_Face_Foot_Defroster', '0x7': ' ModFlapMod_Auto'}

    class ModFlapStsFrntRiOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 812
        signal_description = "Compartment Front Right Area Air Distribution Flap Over Temperature"
        signal_length = 1
        start_position = 577
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ModFlapStsFrntRiDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 812
        signal_description = "Compartment Front Right Area Air Distribution Flap Running Direction"
        signal_length = 2
        start_position = 576
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ModFlapStsFrntRiCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 812
        signal_description = "Compartment Front Right Area Air Distribution Flap Calibration Status"
        signal_length = 2
        start_position = 590
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ModFlapStsFrntRiClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 812
        signal_description = "Compartment Front Right Area Air Distribution Flap Clear Block Status"
        signal_length = 2
        start_position = 588
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ModFlapStsFrntRiURng:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 812
        signal_description = "Compartment Front Right Area Air Distribution Flap Self Learning Voltage Range"
        signal_length = 9
        start_position = 586
        value_definition = {}

    class ModFlapStsFrntRiVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 812
        signal_description = "Compartment Front Right Area Air Distribution Flap Voltage Error"
        signal_length = 2
        start_position = 593
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ModFlapStsFrntRiElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 812
        signal_description = "Compartment Front Right Area Air Distribution Flap Electrical Error"
        signal_length = 2
        start_position = 607
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ModFlapStsFrntRiActPosn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 812
        signal_description = "Compartment Front Right Area Air Distribution Flap Actual Position"
        signal_length = 10
        start_position = 605
        value_definition = {}

    class ModFlapStsFrntRiBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 812
        signal_description = "Compartment Front Right Area Air Distribution Flap Block Status"
        signal_length = 2
        start_position = 611
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ModFlapStsFrntRiRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 812
        signal_description = "Compartment Front Right Area Air Distribution Flap Running Status"
        signal_length = 2
        start_position = 609
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ModFlapStsReRiActPosn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 811
        signal_description = "Compartment Rear Right Area Air Distribution Flap Actual Position"
        signal_length = 10
        start_position = 623
        value_definition = {}

    class ModFlapStsReRiCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 811
        signal_description = "Compartment Rear Right Area Air Distribution Flap Calibration Status"
        signal_length = 2
        start_position = 629
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ModFlapStsReRiElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 811
        signal_description = "Compartment Rear Right Area Air Distribution Flap Electrical Error"
        signal_length = 2
        start_position = 627
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ModFlapStsReRiRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 811
        signal_description = "Compartment Rear Right Area Air Distribution Flap Running Status"
        signal_length = 2
        start_position = 625
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ModFlapStsReRiBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 811
        signal_description = "Compartment Rear Right Area Air Distribution Flap Block Status"
        signal_length = 2
        start_position = 639
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ModFlapStsReRiVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 811
        signal_description = "Compartment Rear Right Area Air Distribution Flap Voltage Error"
        signal_length = 2
        start_position = 637
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ModFlapStsReRiClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 811
        signal_description = "Compartment Rear Right Area Air Distribution Flap Clear Block Status"
        signal_length = 2
        start_position = 635
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ModFlapStsReRiOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 811
        signal_description = "Compartment Rear Right Area Air Distribution Flap Over Temperature"
        signal_length = 1
        start_position = 633
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ModFlapStsReRiDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 811
        signal_description = "Compartment Rear Right Area Air Distribution Flap Running Direction"
        signal_length = 2
        start_position = 632
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ModFlapStsReRiURng:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 811
        signal_description = "Compartment Rear Right Area Air Distribution Flap Self Learning Voltage Range"
        signal_length = 9
        start_position = 646
        value_definition = {}

    class OutAirQlyEstimdAQS:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 809
        signal_description = "AQS Value"
        signal_length = 7
        start_position = 653
        value_definition = {}

    class OutAirQlyEstimdAQSQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 809
        signal_description = "AQS Value Quality Flag "
        signal_length = 1
        start_position = 662
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class OutAirQlyLvl:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 808
        signal_description = "AQS Level"
        signal_length = 2
        start_position = 661
        value_definition = {'0x0': ' AQSLvl_No', '0x1': ' AQSLvl_Lo', '0x2': ' AQSLvl_Mid', '0x3': ' AQSLvl_Hi'}

    class RdntBattIQuiscRaw:
        comments = ""
        factor = 1.0
        initial_value = 2047
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -2047
        sig_ub = 810
        signal_description = "Redundant battery quiet current"
        signal_length = 11
        start_position = 659
        value_definition = {}

    class RdntBattRRaw:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 854
        signal_description = "Redundant battery resistance"
        signal_length = 8
        start_position = 679
        value_definition = {}

    class RdntBattSOHRaw:
        comments = ""
        factor = 1.0
        initial_value = 100
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 853
        signal_description = "Redundant battery SOH"
        signal_length = 8
        start_position = 687
        value_definition = {'0xFF': 'BattSOH_Invalid'}

    class RdntBattSOHSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 852
        signal_description = "Redundant battery SOH accuracy status"
        signal_length = 2
        start_position = 695
        value_definition = {'0x0': ' LVBattCal_Idle', '0x1': ' LVBattCal_CmplCal', '0x2': ' LVBattCal_InCmplCal', '0x3': ' LVBattCal_Resvd'}

    class RecircFlapStsDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 851
        signal_description = "Compartment Recirculated Flap Running Direction"
        signal_length = 2
        start_position = 693
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class RecircFlapStsRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 851
        signal_description = "Compartment Recirculated Flap Running Status"
        signal_length = 2
        start_position = 691
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class RecircFlapStsURng:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 851
        signal_description = "Compartment Recirculated Flap Self-Learning Voltage Range"
        signal_length = 9
        start_position = 689
        value_definition = {}

    class RecircFlapStsCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 851
        signal_description = "Compartment Recirculated Flap Calibration Status"
        signal_length = 2
        start_position = 696
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class RecircFlapStsBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 851
        signal_description = "Compartment Recirculated Flap Block Status"
        signal_length = 2
        start_position = 710
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class RecircFlapStsClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 851
        signal_description = "Compartment Recirculated Flap Clear Block Status"
        signal_length = 2
        start_position = 708
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class RecircFlapStsOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 851
        signal_description = "Compartment Recirculated Flap Over Temperature"
        signal_length = 1
        start_position = 706
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class RecircFlapStsActPosn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 851
        signal_description = "Compartment Recirculated Flap Actual Position"
        signal_length = 10
        start_position = 705
        value_definition = {}

    class RecircFlapStsElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 851
        signal_description = "Compartment Recirculated Flap Electrical Error"
        signal_length = 2
        start_position = 727
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class RecircFlapStsVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 851
        signal_description = "Compartment Recirculated Flap Voltage Error"
        signal_length = 2
        start_position = 725
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class RefrigSov3ActvReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 850
        signal_description = "Refrigerant Solenoid Valve 3 Active Request"
        signal_length = 1
        start_position = 723
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ReWiprFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 849
        signal_description = "the fault of the rear wiper"
        signal_length = 1
        start_position = 722
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ReWiprPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 848
        signal_description = "the position of the rear wiper crank,park or not park"
        signal_length = 1
        start_position = 721
        value_definition = {'0x0': ' ReWiprPosn_Park', '0x1': ' ReWiprPosn_UnPark'}

    class ReWprForSrvSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 892
        signal_description = "the rear wiper service positon state"
        signal_length = 1
        start_position = 720
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class REXVReqExvMovEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 891
        signal_description = "Rexv move enable."
        signal_length = 1
        start_position = 735
        value_definition = {'0x0': ' ExvMovEnable_EXVNotEnable', '0x1': ' ExvMovEnable_EXVEnable'}

    class REXVReqExvPreHeatgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 891
        signal_description = "Rexv heating request."
        signal_length = 1
        start_position = 734
        value_definition = {'0x0': ' ExvHeatdReq_NoReq', '0x1': ' ExvHeatdReq_PreHeatedReq'}

    class REXVReqExvCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 891
        signal_description = "Rexv calibration request."
        signal_length = 1
        start_position = 733
        value_definition = {'0x0': ' ExvCalibReq_NoReq', '0x1': ' ExvCalibReq_InitializationReq'}

    class REXVReqExvPosnReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 891
        signal_description = "Rexv postion request."
        signal_length = 10
        start_position = 732
        value_definition = {}

    class RiMotCirFLtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 890
        signal_description = "The Right Speaker Motor Circult Status"
        signal_length = 3
        start_position = 738
        value_definition = {'0x0': ' AudioChCirSts_Normal', '0x1': ' AudioChCirSts_CircuitOpen', '0x2': ' AudioChCirSts_CircuitShortToBattery', '0x3': ' AudioChCirSts_CircuitShortToGND', '0x4': ' AudioChCirSts_CircuitReversedWireConnection', '0x5': ' AudioChCirSts_CircuitReserved1', '0x6': ' AudioChCirSts_CircuitReserved2', '0x7': ' AudioChCirSts_CircuitReserved3'}

    class RiSpkrMovgSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "The Right Speaker Motor Elevating Status"
        signal_length = 3
        start_position = 751
        value_definition = {'0x0': ' SpkMoviSts_FallingTotheButtom', '0x1': ' SpkMoviSts_Rising', '0x2': ' SpkMoviSts_RisingToTop', '0x3': ' SpkMoviSts_Falling', '0x4': ' SpkMoviSts_Stopping', '0x5': ' SpkMoviSts_Unkown', '0x6': ' SpkMoviSts_Reserved1', '0x7': ' SpkMoviSts_Reserved2'}

    class RRDoorManResistSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 888
        signal_description = "Door manual resistance status"
        signal_length = 2
        start_position = 748
        value_definition = {'0x0': ' DoorManResistsSts_NoResist', '0x1': ' DoorManResistsSts_Level1', '0x2': ' DoorManResistsSts_Level2'}

    class RRDoorSpdModeFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1087
        signal_description = "power side door mode status feedback"
        signal_length = 2
        start_position = 746
        value_definition = {'0x0': ' SpdMode_Low', '0x1': ' SpdMode_Middle', '0x2': ' SpdMode_High'}

    class SeatAdj1RowRiStopCaseMotorStopCase:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1045
        signal_description = "Detailed Stop Reason"
        signal_length = 4
        start_position = 744
        value_definition = {'0x0': ' MotorStopCase_idle', '0x1': ' MotorStopCase_MotorStall', '0x2': ' MotorStopCase_AntiPinch', '0x3': ' MotorStopCase_ThermalProtection', '0x4': ' MotorStopCase_Button', '0x5': ' MotorStopCase_Signal', '0x6': ' MotorStopCase_Speed', '0x7': ' MotorStopCase_HWerror', '0x8': ' MotorStopCase_reserved1', '0x9': ' MotorStopCase_reserved2', '0xA': ' MotorStopCase_reserved3', '0xB': ' MotorStopCase_reserved4', '0xC': ' MotorStopCase_reserved5', '0xD': ' MotorStopCase_reserved6', '0xE': ' MotorStopCase_reserved7', '0xF': ' MotorStopCase_reserved8'}

    class SeatAdj1RowRiStopCaseSeatCfg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1045
        signal_description = "Seat Motor Config"
        signal_length = 4
        start_position = 756
        value_definition = {'0x0': ' SeatCfg_Idle', '0x1': ' SeatCfg_Length', '0x2': ' SeatCfg_Height', '0x3': ' SeatCfg_Tilt', '0x4': ' SeatCfg_BackrestAngle', '0x5': ' SeatCfg_OTTOLength', '0x6': ' SeatCfg_OTTOAngle', '0x7': ' SeatCfg_CLA', '0x8': ' SeatCfg_Release', '0x9': ' SeatCfg_Reserved1', '0xA': ' SeatCfg_Reserved2', '0xB': ' SeatCfg_Reserved3', '0xC': ' SeatCfg_Reserved4', '0xD': ' SeatCfg_Reserved5', '0xE': ' SeatCfg_Reserved6', '0xF': ' SeatCfg_Reserved7'}

    class SeatAdj2RowRiStopCaseSeatCfg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1044
        signal_description = "Seat Motor Config"
        signal_length = 4
        start_position = 752
        value_definition = {'0x0': ' SeatCfg_Idle', '0x1': ' SeatCfg_Length', '0x2': ' SeatCfg_Height', '0x3': ' SeatCfg_Tilt', '0x4': ' SeatCfg_BackrestAngle', '0x5': ' SeatCfg_OTTOLength', '0x6': ' SeatCfg_OTTOAngle', '0x7': ' SeatCfg_CLA', '0x8': ' SeatCfg_Release', '0x9': ' SeatCfg_Reserved1', '0xA': ' SeatCfg_Reserved2', '0xB': ' SeatCfg_Reserved3', '0xC': ' SeatCfg_Reserved4', '0xD': ' SeatCfg_Reserved5', '0xE': ' SeatCfg_Reserved6', '0xF': ' SeatCfg_Reserved7'}

    class SeatAdj2RowRiStopCaseMotorStopCase:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1044
        signal_description = "Detailed Stop Reason"
        signal_length = 4
        start_position = 764
        value_definition = {'0x0': ' MotorStopCase_idle', '0x1': ' MotorStopCase_MotorStall', '0x2': ' MotorStopCase_AntiPinch', '0x3': ' MotorStopCase_ThermalProtection', '0x4': ' MotorStopCase_Button', '0x5': ' MotorStopCase_Signal', '0x6': ' MotorStopCase_Speed', '0x7': ' MotorStopCase_HWerror', '0x8': ' MotorStopCase_reserved1', '0x9': ' MotorStopCase_reserved2', '0xA': ' MotorStopCase_reserved3', '0xB': ' MotorStopCase_reserved4', '0xC': ' MotorStopCase_reserved5', '0xD': ' MotorStopCase_reserved6', '0xE': ' MotorStopCase_reserved7', '0xF': ' MotorStopCase_reserved8'}

    class SeatAdj3RowRiStopCaseSeatCfg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1043
        signal_description = "Seat Motor Config"
        signal_length = 4
        start_position = 760
        value_definition = {'0x0': ' SeatCfg_Idle', '0x1': ' SeatCfg_Length', '0x2': ' SeatCfg_Height', '0x3': ' SeatCfg_Tilt', '0x4': ' SeatCfg_BackrestAngle', '0x5': ' SeatCfg_OTTOLength', '0x6': ' SeatCfg_OTTOAngle', '0x7': ' SeatCfg_CLA', '0x8': ' SeatCfg_Release', '0x9': ' SeatCfg_Reserved1', '0xA': ' SeatCfg_Reserved2', '0xB': ' SeatCfg_Reserved3', '0xC': ' SeatCfg_Reserved4', '0xD': ' SeatCfg_Reserved5', '0xE': ' SeatCfg_Reserved6', '0xF': ' SeatCfg_Reserved7'}

    class SeatAdj3RowRiStopCaseMotorStopCase:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1043
        signal_description = "Detailed Stop Reason"
        signal_length = 4
        start_position = 772
        value_definition = {'0x0': ' MotorStopCase_idle', '0x1': ' MotorStopCase_MotorStall', '0x2': ' MotorStopCase_AntiPinch', '0x3': ' MotorStopCase_ThermalProtection', '0x4': ' MotorStopCase_Button', '0x5': ' MotorStopCase_Signal', '0x6': ' MotorStopCase_Speed', '0x7': ' MotorStopCase_HWerror', '0x8': ' MotorStopCase_reserved1', '0x9': ' MotorStopCase_reserved2', '0xA': ' MotorStopCase_reserved3', '0xB': ' MotorStopCase_reserved4', '0xC': ' MotorStopCase_reserved5', '0xD': ' MotorStopCase_reserved6', '0xE': ' MotorStopCase_reserved7', '0xF': ' MotorStopCase_reserved8'}

    class SeatClima1RowRiStsTEstimd:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 1042
        signal_description = "First Row Right Side Seat Heating Actual Temperature"
        signal_length = 11
        start_position = 768
        value_definition = {}

    class SeatClima1RowRiStsHeatgActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1042
        signal_description = "First Row Right Side Seat Heating Actual Power"
        signal_length = 8
        start_position = 799
        value_definition = {}

    class SeatClima1RowRiStsVentAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1042
        signal_description = "First Row Right Side Seat Venting Available Status"
        signal_length = 3
        start_position = 786
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClima1RowRiStsHeatgAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1042
        signal_description = "First Row Right Side Seat Heating Available Status"
        signal_length = 3
        start_position = 789
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClima1RowRiStsVentActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1042
        signal_description = "First Row Right Side Seat Venting Actual Power"
        signal_length = 8
        start_position = 807
        value_definition = {}

    class SeatClima2RowRiStsVentActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1041
        signal_description = "Second Row Right Side Seat Venting Actual Power"
        signal_length = 8
        start_position = 823
        value_definition = {}

    class SeatClima2RowRiStsHeatgActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1041
        signal_description = "Second Row Right Side Seat Heating Actual Power"
        signal_length = 8
        start_position = 831
        value_definition = {}

    class SeatClima2RowRiStsTEstimd:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 1041
        signal_description = "Second Row Right Side Seat Heating Actual Temperature"
        signal_length = 11
        start_position = 839
        value_definition = {}

    class SeatClima2RowRiStsVentAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1041
        signal_description = "Second Row Right Side Seat Venting Available Status"
        signal_length = 3
        start_position = 844
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClima2RowRiStsHeatgAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1041
        signal_description = "Second Row Right Side Seat Heating Available Status"
        signal_length = 3
        start_position = 841
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClima3RowRiStsHeatgAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1040
        signal_description = "Third Row Right Side Seat Heating Available Status"
        signal_length = 3
        start_position = 868
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClima3RowRiStsVentActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1040
        signal_description = "Third Row Right Side Seat Venting Actual Power"
        signal_length = 8
        start_position = 863
        value_definition = {}

    class SeatClima3RowRiStsVentAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1040
        signal_description = "Third Row Right Side Seat Venting Available Status"
        signal_length = 3
        start_position = 871
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClima3RowRiStsHeatgActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1040
        signal_description = "Third Row Right Side Seat Heating Actual Power"
        signal_length = 8
        start_position = 879
        value_definition = {}

    class SeatClima3RowRiStsTEstimd:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 1040
        signal_description = "Third Row Right Side Seat Heating Actual Temperature"
        signal_length = 11
        start_position = 887
        value_definition = {}

    class SeatClimaRiHeatgBtnStsRow2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1185
        signal_description = "Second Row Right Side Seat Heating Button Status"
        signal_length = 2
        start_position = 901
        value_definition = {'0x0': ' SeatClimaLvl_Off', '0x1': ' SeatClimaLvl_Lvl1', '0x2': ' SeatClimaLvl_Lvl2', '0x3': ' SeatClimaLvl_Lvl3'}

    class SeatClimaRiHeatgBtnStsRow1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1185
        signal_description = "First Row Right Side Seat Heating Button Status"
        signal_length = 2
        start_position = 903
        value_definition = {'0x0': ' SeatClimaLvl_Off', '0x1': ' SeatClimaLvl_Lvl1', '0x2': ' SeatClimaLvl_Lvl2', '0x3': ' SeatClimaLvl_Lvl3'}

    class SeatClimaRiHeatgBtnStsRow3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1185
        signal_description = "Third Row Right Side Seat Heating Button Status"
        signal_length = 2
        start_position = 899
        value_definition = {'0x0': ' SeatClimaLvl_Off', '0x1': ' SeatClimaLvl_Lvl1', '0x2': ' SeatClimaLvl_Lvl2', '0x3': ' SeatClimaLvl_Lvl3'}

    class TempFlapStsFrntRiRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1198
        signal_description = "Compartment Front Right Area Temperature Flap Running Status"
        signal_length = 2
        start_position = 956
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class TempFlapStsFrntRiDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1198
        signal_description = "Compartment Front Right Area Temperature Flap Running Direction"
        signal_length = 2
        start_position = 954
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class TempFlapStsFrntRiCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1198
        signal_description = "Compartment Front Right Area Temperature Flap Calibration Status"
        signal_length = 2
        start_position = 952
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class TempFlapStsFrntRiOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1198
        signal_description = "Compartment Front Right Area Temperature Flap Over Temperature"
        signal_length = 1
        start_position = 966
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class TempFlapStsFrntRiClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1198
        signal_description = "Compartment Front Right Area Temperature Flap Clear Block Status"
        signal_length = 2
        start_position = 965
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class TempFlapStsFrntRiBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1198
        signal_description = "Compartment Front Right Area Temperature Flap Block Status"
        signal_length = 2
        start_position = 963
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class TempFlapStsFrntRiElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1198
        signal_description = "Compartment Front Right Area Temperature Flap Electrical Error"
        signal_length = 2
        start_position = 961
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class TempFlapStsFrntRiActPosn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1198
        signal_description = "Compartment Front Right Area Temperature Flap Actual Position"
        signal_length = 10
        start_position = 975
        value_definition = {}

    class TempFlapStsFrntRiURng:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1198
        signal_description = "Compartment Front Right Area Temperature Flap Voltage Range"
        signal_length = 9
        start_position = 981
        value_definition = {}

    class TempFlapStsFrntRiVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1198
        signal_description = "Compartment Front Right Area Temperature Flap Voltage Error"
        signal_length = 2
        start_position = 988
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class TempFlapStsReRiVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1197
        signal_description = "Compartment Rear Right Area Temperature Flap Voltage Error"
        signal_length = 2
        start_position = 986
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class TempFlapStsReRiRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1197
        signal_description = "Compartment Rear Right Area Temperature Flap Running Direction"
        signal_length = 2
        start_position = 984
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class TempFlapStsReRiDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1197
        signal_description = "Compartment Rear Right Area Temperature Flap Running Direction"
        signal_length = 2
        start_position = 998
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class TempFlapStsReRiBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1197
        signal_description = "Compartment Rear Right Area Temperature Flap Block Status"
        signal_length = 2
        start_position = 996
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class TempFlapStsReRiClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1197
        signal_description = "Compartment Rear Right Area Temperature Flap Clear Block Status"
        signal_length = 2
        start_position = 994
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class TempFlapStsReRiURng:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1197
        signal_description = "Compartment Rear Right Area Temperature Flap Voltage Range"
        signal_length = 9
        start_position = 992
        value_definition = {}

    class TempFlapStsReRiCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1197
        signal_description = "Compartment Rear Right Area Temperature Flap Calibration Status"
        signal_length = 2
        start_position = 1015
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class TempFlapStsReRiActPosn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1197
        signal_description = "Compartment Rear Right Area Temperature Flap Actual Position"
        signal_length = 10
        start_position = 1013
        value_definition = {}

    class TempFlapStsReRiElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1197
        signal_description = "Compartment Rear Right Area Temperature Flap Electrical Error"
        signal_length = 2
        start_position = 1019
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class TempFlapStsReRiOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1197
        signal_description = "Compartment Rear Right Area Temperature Flap Over Temperature"
        signal_length = 1
        start_position = 1017
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class TERVReqExvMovEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1196
        signal_description = "Terv move enable."
        signal_length = 1
        start_position = 1016
        value_definition = {'0x0': ' ExvMovEnable_EXVNotEnable', '0x1': ' ExvMovEnable_EXVEnable'}

    class TERVReqExvPosnReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1196
        signal_description = "Terv postion request."
        signal_length = 10
        start_position = 1031
        value_definition = {}

    class TERVReqExvCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1196
        signal_description = "Terv calibration request."
        signal_length = 1
        start_position = 1037
        value_definition = {'0x0': ' ExvCalibReq_NoReq', '0x1': ' ExvCalibReq_InitializationReq'}

    class TERVReqExvPreHeatgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1196
        signal_description = "Terv heating request."
        signal_length = 1
        start_position = 1036
        value_definition = {'0x0': ' ExvHeatdReq_NoReq', '0x1': ' ExvHeatdReq_PreHeatedReq'}

    class TrErrFbCinchMotThermErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1195
        signal_description = "cinch motor therm error feedback"
        signal_length = 1
        start_position = 1035
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class TrErrFbHalfClsErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1195
        signal_description = "half close status error feedback"
        signal_length = 1
        start_position = 1034
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class TrErrFbRelsgErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1195
        signal_description = "release error feedback"
        signal_length = 1
        start_position = 1033
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class TrErrFbCinchErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1195
        signal_description = "cinch error feedback"
        signal_length = 1
        start_position = 1032
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class TrErrFbRelsMotThermErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1195
        signal_description = "release motor therm error feedback"
        signal_length = 1
        start_position = 1047
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class TrErrFbSpindleMotThermErrFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1195
        signal_description = "Spindle motor therm error feedback"
        signal_length = 1
        start_position = 1046
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class TrMaxPosnSetFB:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1194
        signal_description = "trunk max position set feedback"
        signal_length = 8
        start_position = 1055
        value_definition = {}

    class URawLCU2:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1193
        signal_description = "Voltage"
        signal_length = 9
        start_position = 1063
        value_definition = {}

    class VentAirTEstimdFrntRiFaceTQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1207
        signal_description = "Front Right Face Air Temperature Quality Flag"
        signal_length = 1
        start_position = 1090
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class VentAirTEstimdFrntRiFootT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1207
        signal_description = "Front Right Foot Air Temperature"
        signal_length = 13
        start_position = 1089
        value_definition = {}

    class VentAirTEstimdFrntRiFootTQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1207
        signal_description = "Front Right Foot Air Temperature Quality Flag"
        signal_length = 1
        start_position = 1108
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class VentAirTEstimdFrntRiFaceT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1207
        signal_description = "Front Right Face Air Temperature"
        signal_length = 13
        start_position = 1107
        value_definition = {}

    class VentAirTEstimdReRiFaceTQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1205
        signal_description = "Rear Right Face Air Temperature Quality Flag"
        signal_length = 1
        start_position = 1146
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class VentAirTEstimdReRiFootT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1205
        signal_description = "Rear Right Foot Air Temperature"
        signal_length = 13
        start_position = 1145
        value_definition = {}

    class VentAirTEstimdReRiFootTQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1205
        signal_description = "Rear Right Foot Air Temperature Quality Flag"
        signal_length = 1
        start_position = 1164
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class VentAirTEstimdReRiFaceT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1205
        signal_description = "Rear Right Face Air Temperature"
        signal_length = 13
        start_position = 1163
        value_definition = {}

    class WERVReqExvPreHeatgReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1204
        signal_description = "Werv heating request."
        signal_length = 1
        start_position = 1182
        value_definition = {'0x0': ' ExvHeatdReq_NoReq', '0x1': ' ExvHeatdReq_PreHeatedReq'}

    class WERVReqExvMovEna:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1204
        signal_description = "Werv move enable."
        signal_length = 1
        start_position = 1181
        value_definition = {'0x0': ' ExvMovEnable_EXVNotEnable', '0x1': ' ExvMovEnable_EXVEnable'}

    class WERVReqExvCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1204
        signal_description = "Werv calibration request."
        signal_length = 1
        start_position = 1180
        value_definition = {'0x0': ' ExvCalibReq_NoReq', '0x1': ' ExvCalibReq_InitializationReq'}

    class WERVReqExvPosnReq:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1204
        signal_description = "Werv postion request."
        signal_length = 10
        start_position = 1179
        value_definition = {}

    class FRDoorOpenTrigSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 897
        signal_description = "trigger source of power side door open"
        signal_length = 4
        start_position = 907
        value_definition = {'0x0': ' DoorCtrlTriSrc_NoTrigSrc', '0x1': ' DoorCtrlTriSrc_InsdSwt', '0x2': ' DoorCtrlTriSrc_OutdSwt', '0x3': ' DoorCtrlTriSrc_NFC', '0x4': ' DoorCtrlTriSrc_Aproch', '0x5': ' DoorCtrlTriSrc_OutdCtrl', '0x6': ' DoorCtrlTriSrc_InsdCtrl', '0x7': ' DoorCtrlTriSrc_Resd1', '0x8': ' DoorCtrlTriSrc_Resd2', '0x9': ' DoorCtrlTriSrc_Resd3'}

    class AirFragEgyLimSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 910
        signal_description = "Air Fragrance Energy Limit Status"
        signal_length = 1
        start_position = 911
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class InAirPM25EgyLimSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 918
        signal_description = "Inside Air PM2.5 Energy Limit Status"
        signal_length = 1
        start_position = 919
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class AnionGenrEgyLimSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 908
        signal_description = "Anion Generator Energy Limit Status"
        signal_length = 1
        start_position = 909
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class WasherFluidLevelInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 896
        signal_description = "Washer Fluid Level Sts"
        signal_length = 1
        start_position = 917
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class RRDoorOpenTrigSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 916
        signal_description = "trigger source of power side door open"
        signal_length = 4
        start_position = 915
        value_definition = {'0x0': ' DoorCtrlTriSrc_NoTrigSrc', '0x1': ' DoorCtrlTriSrc_InsdSwt', '0x2': ' DoorCtrlTriSrc_OutdSwt', '0x3': ' DoorCtrlTriSrc_NFC', '0x4': ' DoorCtrlTriSrc_Aproch', '0x5': ' DoorCtrlTriSrc_OutdCtrl', '0x6': ' DoorCtrlTriSrc_InsdCtrl', '0x7': ' DoorCtrlTriSrc_Resd1', '0x8': ' DoorCtrlTriSrc_Resd2', '0x9': ' DoorCtrlTriSrc_Resd3'}


class LCURToCCUSOCCDEthSignalIPdu08:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x604008
    pdu_length_bytes = 128
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-50ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'BackLiLocPasSideDrvSts': ['BackLiLocPasSideDrvStsLiPerc', 'BackLiLocPasSideDrvStsLightSts', 'BackLiLocPasSideDrvStsLightErrorCode'], 'BackLiLocRearRiDrvSts': ['BackLiLocRearRiDrvStsLiPerc', 'BackLiLocRearRiDrvStsLightSts', 'BackLiLocRearRiDrvStsLightErrorCode'], 'BackLiWinPasSideDrvSts': ['BackLiWinPasSideDrvStsLightErrorCode', 'BackLiWinPasSideDrvStsLiPerc', 'BackLiWinPasSideDrvStsLightSts'], 'BackLiWinRearRiDrvSts': ['BackLiWinRearRiDrvStsLightErrorCode', 'BackLiWinRearRiDrvStsLiPerc', 'BackLiWinRearRiDrvStsLightSts'], 'FuncStsOfDaytimeRunningLamp': ['FuncStsOfDaytimeRunningLampLightPriority', 'FuncStsOfDaytimeRunningLampLightSts', 'FuncStsOfDaytimeRunningLampLightErrorCode'], 'FuncStsOfFrontFogLamp': ['FuncStsOfFrontFogLampLightSts', 'FuncStsOfFrontFogLampLightErrorCode', 'FuncStsOfFrontFogLampLightPriority'], 'FuncStsOfLightShow': ['FuncStsOfLightShowLightPriority', 'FuncStsOfLightShowLightErrorCode', 'FuncStsOfLightShowLightSts'], 'FuncStsOfRearFogLamp': ['FuncStsOfRearFogLampLightPriority', 'FuncStsOfRearFogLampLightSts', 'FuncStsOfRearFogLampLightErrorCode'], 'FuncStsOfReverseLamp': ['FuncStsOfReverseLampLightSts', 'FuncStsOfReverseLampLightPriority', 'FuncStsOfReverseLampLightErrorCode'], 'ReadingLiFrntLeFuncSts': ['ReadingLiFrntLeFuncStsLightSts', 'ReadingLiFrntLeFuncStsLiPerc', 'ReadingLiFrntLeFuncStsLightPriority', 'ReadingLiFrntLeFuncStsLightErrorCode'], 'ReadingLiFrntRiFuncSts': ['ReadingLiFrntRiFuncStsLightSts', 'ReadingLiFrntRiFuncStsLightErrorCode', 'ReadingLiFrntRiFuncStsLightPriority', 'ReadingLiFrntRiFuncStsLiPerc'], 'ReadingLiSecLeFuncSts': ['ReadingLiSecLeFuncStsLightErrorCode', 'ReadingLiSecLeFuncStsLiPerc', 'ReadingLiSecLeFuncStsLightSts', 'ReadingLiSecLeFuncStsLightPriority'], 'ReadingLiSecRiFuncSts': ['ReadingLiSecRiFuncStsLightErrorCode', 'ReadingLiSecRiFuncStsLightSts', 'ReadingLiSecRiFuncStsLiPerc', 'ReadingLiSecRiFuncStsLightPriority'], 'ReadingLiThrdLeFuncSts': ['ReadingLiThrdLeFuncStsLightSts', 'ReadingLiThrdLeFuncStsLiPerc', 'ReadingLiThrdLeFuncStsLightErrorCode', 'ReadingLiThrdLeFuncStsLightPriority'], 'ReadingLiThrdRiFuncSts': ['ReadingLiThrdRiFuncStsLightErrorCode', 'ReadingLiThrdRiFuncStsLightPriority', 'ReadingLiThrdRiFuncStsLiPerc', 'ReadingLiThrdRiFuncStsLightSts'], 'SeatAdj1RowRiPosn': ['SeatAdj1RowRiPosnCLAPos', 'SeatAdj1RowRiPosnLengthQf', 'SeatAdj1RowRiPosnReleasePos', 'SeatAdj1RowRiPosnHeightPos', 'SeatAdj1RowRiPosnCLAQf', 'SeatAdj1RowRiPosnOTTOLenPos', 'SeatAdj1RowRiPosnReleaseQf', 'SeatAdj1RowRiPosnOTTOAgQf', 'SeatAdj1RowRiPosnHeightQf', 'SeatAdj1RowRiPosnTiltQf', 'SeatAdj1RowRiPosnLengthPos', 'SeatAdj1RowRiPosnTiltPos', 'SeatAdj1RowRiPosnOTTOAgPos', 'SeatAdj1RowRiPosnBackRestPos', 'SeatAdj1RowRiPosnBackRestQf', 'SeatAdj1RowRiPosnOTTOLenQf'], 'SeatAdj2RowRiPosn': ['SeatAdj2RowRiPosnOTTOLenQf', 'SeatAdj2RowRiPosnOTTOLenPos', 'SeatAdj2RowRiPosnReleaseQf', 'SeatAdj2RowRiPosnCLAPos', 'SeatAdj2RowRiPosnHeightPos', 'SeatAdj2RowRiPosnTiltPos', 'SeatAdj2RowRiPosnOTTOAgPos', 'SeatAdj2RowRiPosnReleasePos', 'SeatAdj2RowRiPosnBackRestQf', 'SeatAdj2RowRiPosnLengthPos', 'SeatAdj2RowRiPosnLengthQf', 'SeatAdj2RowRiPosnCLAQf', 'SeatAdj2RowRiPosnTiltQf', 'SeatAdj2RowRiPosnBackRestPos', 'SeatAdj2RowRiPosnOTTOAgQf', 'SeatAdj2RowRiPosnHeightQf'], 'SeatAdj3RowRiPosn': ['SeatAdj3RowRiPosnHeightQf', 'SeatAdj3RowRiPosnOTTOAgPos', 'SeatAdj3RowRiPosnOTTOLenPos', 'SeatAdj3RowRiPosnLengthQf', 'SeatAdj3RowRiPosnBackRestPos', 'SeatAdj3RowRiPosnReleasePos', 'SeatAdj3RowRiPosnBackRestQf', 'SeatAdj3RowRiPosnTiltPos', 'SeatAdj3RowRiPosnHeightPos', 'SeatAdj3RowRiPosnCLAPos', 'SeatAdj3RowRiPosnOTTOLenQf', 'SeatAdj3RowRiPosnOTTOAgQf', 'SeatAdj3RowRiPosnLengthPos', 'SeatAdj3RowRiPosnCLAQf', 'SeatAdj3RowRiPosnReleaseQf', 'SeatAdj3RowRiPosnTiltQf'], 'SeatLieDwnRiSwtSts': ['SeatLieDwnRiSwtStsFlt', 'SeatLieDwnRiSwtStsPsdNotPsd1'], 'SeatMassgFrntRiRunStsFb': ['SeatMassgFrntRiRunStsFbMassgProg', 'SeatMassgFrntRiRunStsFbOnOffNoCmd', 'SeatMassgFrntRiRunStsFbMassgLvlSts'], 'SeatMassgReRiRunStsFb': ['SeatMassgReRiRunStsFbOnOffNoCmd', 'SeatMassgReRiRunStsFbMassgProg', 'SeatMassgReRiRunStsFbMassgLvlSts'], 'TrAntiPnchSts': ['TrAntiPnchStsCloseAntiPnchSts', 'TrAntiPnchStsOPenAntiPnchSts'], 'TrunkLiFuncSts': ['TrunkLiFuncStsLightErrorCode', 'TrunkLiFuncStsLightPriority', 'TrunkLiFuncStsLightSts'], 'SeatAdj3RowRiBtnSts': ['SeatAdj3RowRiBtnStsSeatAdjTiltBtnSts', 'SeatAdj3RowRiBtnStsSeatAdjOTTOAgBtnSts', 'SeatAdj3RowRiBtnStsSeatAdjBackBtnSts', 'SeatAdj3RowRiBtnStsSeatAdjLenBtnSts', 'SeatAdj3RowRiBtnStsSeatAdjHeiBtnSts', 'SeatAdj3RowRiBtnStsSeatAdjCLABtnSts', 'SeatAdj3RowRiBtnStsSeatAdjOTTOLenBtnSts'], 'SeatAdj1RowRiBtnSts': ['SeatAdj1RowRiBtnStsSeatAdjTiltBtnSts', 'SeatAdj1RowRiBtnStsSeatAdjHeiBtnSts', 'SeatAdj1RowRiBtnStsSeatAdjOTTOAgBtnSts', 'SeatAdj1RowRiBtnStsSeatAdjLenBtnSts', 'SeatAdj1RowRiBtnStsSeatAdjOTTOLenBtnSts', 'SeatAdj1RowRiBtnStsSeatAdjCLABtnSts', 'SeatAdj1RowRiBtnStsSeatAdjBackBtnSts'], 'SeatAdj2RowRiBtnSts': ['SeatAdj2RowRiBtnStsSeatAdjOTTOAgBtnSts', 'SeatAdj2RowRiBtnStsSeatAdjLenBtnSts', 'SeatAdj2RowRiBtnStsSeatAdjBackBtnSts', 'SeatAdj2RowRiBtnStsSeatAdjHeiBtnSts', 'SeatAdj2RowRiBtnStsSeatAdjOTTOLenBtnSts', 'SeatAdj2RowRiBtnStsSeatAdjTiltBtnSts', 'SeatAdj2RowRiBtnStsSeatAdjCLABtnSts']}

    class BackLiLocPasSideDrvStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 11
        value_definition = {}

    class BackLiLocPasSideDrvStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "light status"
        signal_length = 4
        start_position = 15
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class BackLiLocPasSideDrvStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "error code"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class BackLiLocRearRiDrvStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 44
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 35
        value_definition = {}

    class BackLiLocRearRiDrvStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 44
        signal_description = "light status"
        signal_length = 4
        start_position = 39
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class BackLiLocRearRiDrvStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 44
        signal_description = "error code"
        signal_length = 8
        start_position = 31
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class BackLiWinPasSideDrvStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 68
        signal_description = "error code"
        signal_length = 8
        start_position = 55
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class BackLiWinPasSideDrvStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 68
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 59
        value_definition = {}

    class BackLiWinPasSideDrvStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 68
        signal_description = "light status"
        signal_length = 4
        start_position = 63
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class BackLiWinRearRiDrvStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 92
        signal_description = "error code"
        signal_length = 8
        start_position = 79
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class BackLiWinRearRiDrvStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 92
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 83
        value_definition = {}

    class BackLiWinRearRiDrvStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 92
        signal_description = "light status"
        signal_length = 4
        start_position = 87
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfDaytimeRunningLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 115
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class FuncStsOfDaytimeRunningLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 115
        signal_description = "LightStatus"
        signal_length = 4
        start_position = 119
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfDaytimeRunningLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 115
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 103
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfFrontFogLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "LightStatus"
        signal_length = 4
        start_position = 143
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfFrontFogLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 127
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfFrontFogLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 139
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 135
        value_definition = {}

    class FuncStsOfLightShowLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 163
        signal_description = "Priority"
        signal_length = 8
        start_position = 151
        value_definition = {}

    class FuncStsOfLightShowLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 163
        signal_description = "Error Code"
        signal_length = 8
        start_position = 159
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfLightShowLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 163
        signal_description = "Light Status"
        signal_length = 4
        start_position = 167
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfRearFogLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 187
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 183
        value_definition = {}

    class FuncStsOfRearFogLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 187
        signal_description = "LightStatus"
        signal_length = 4
        start_position = 191
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfRearFogLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 187
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 175
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfReverseLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 186
        signal_description = "LightStatus"
        signal_length = 4
        start_position = 215
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfReverseLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 186
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 207
        value_definition = {}

    class FuncStsOfReverseLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 186
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 199
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class HoodInsdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 208
        signal_description = "inside switch status of hood"
        signal_length = 3
        start_position = 211
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class ReadingLiFrntLeFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 244
        signal_description = "Light Status"
        signal_length = 4
        start_position = 239
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class ReadingLiFrntLeFuncStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 244
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 235
        value_definition = {}

    class ReadingLiFrntLeFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 244
        signal_description = "light priority"
        signal_length = 8
        start_position = 231
        value_definition = {}

    class ReadingLiFrntLeFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 244
        signal_description = "error status"
        signal_length = 8
        start_position = 223
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class ReadingLiFrntRiFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "Light Status"
        signal_length = 4
        start_position = 271
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class ReadingLiFrntRiFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "error status"
        signal_length = 8
        start_position = 255
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class ReadingLiFrntRiFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "light priority"
        signal_length = 8
        start_position = 263
        value_definition = {}

    class ReadingLiFrntRiFuncStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 276
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 267
        value_definition = {}

    class ReadingLiSecLeFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 308
        signal_description = "error status"
        signal_length = 8
        start_position = 287
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class ReadingLiSecLeFuncStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 308
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 299
        value_definition = {}

    class ReadingLiSecLeFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 308
        signal_description = "Light Status"
        signal_length = 4
        start_position = 303
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class ReadingLiSecLeFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 308
        signal_description = "light priority"
        signal_length = 8
        start_position = 295
        value_definition = {}

    class ReadingLiSecRiFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 340
        signal_description = "error status"
        signal_length = 8
        start_position = 319
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class ReadingLiSecRiFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 340
        signal_description = "Light Status"
        signal_length = 4
        start_position = 335
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class ReadingLiSecRiFuncStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 340
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 331
        value_definition = {}

    class ReadingLiSecRiFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 340
        signal_description = "light priority"
        signal_length = 8
        start_position = 327
        value_definition = {}

    class ReadingLiThrdLeFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 372
        signal_description = "Light Status"
        signal_length = 4
        start_position = 367
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class ReadingLiThrdLeFuncStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 372
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 363
        value_definition = {}

    class ReadingLiThrdLeFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 372
        signal_description = "error status"
        signal_length = 8
        start_position = 351
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class ReadingLiThrdLeFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 372
        signal_description = "light priority"
        signal_length = 8
        start_position = 359
        value_definition = {}

    class ReadingLiThrdRiFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 371
        signal_description = "error status"
        signal_length = 8
        start_position = 383
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class ReadingLiThrdRiFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 371
        signal_description = "light priority"
        signal_length = 8
        start_position = 391
        value_definition = {}

    class ReadingLiThrdRiFuncStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 371
        signal_description = "brightness percent"
        signal_length = 7
        start_position = 395
        value_definition = {}

    class ReadingLiThrdRiFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 371
        signal_description = "Light Status"
        signal_length = 4
        start_position = 399
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class SeatAdj1RowRiAntiPinchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 824
        signal_description = "Antipinch Work Status"
        signal_length = 2
        start_position = 490
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class SeatAdj1RowRiPosnCLAPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 488
        value_definition = {}

    class SeatAdj1RowRiPosnLengthQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 510
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowRiPosnReleasePos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 508
        value_definition = {}

    class SeatAdj1RowRiPosnHeightPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 514
        value_definition = {}

    class SeatAdj1RowRiPosnCLAQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 520
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowRiPosnOTTOLenPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 534
        value_definition = {}

    class SeatAdj1RowRiPosnReleaseQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 540
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowRiPosnOTTOAgQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 538
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowRiPosnHeightQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 536
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowRiPosnTiltQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 550
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowRiPosnLengthPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 548
        value_definition = {}

    class SeatAdj1RowRiPosnTiltPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 554
        value_definition = {}

    class SeatAdj1RowRiPosnOTTOAgPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 560
        value_definition = {}

    class SeatAdj1RowRiPosnBackRestPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 582
        value_definition = {}

    class SeatAdj1RowRiPosnBackRestQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 588
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowRiPosnOTTOLenQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 889
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 586
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowRiAntiPinchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 888
        signal_description = "Antipinch Work Status"
        signal_length = 2
        start_position = 584
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class SeatAdj2RowRiPosnOTTOLenQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 598
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowRiPosnOTTOLenPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 596
        value_definition = {}

    class SeatAdj2RowRiPosnReleaseQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 602
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowRiPosnCLAPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 600
        value_definition = {}

    class SeatAdj2RowRiPosnHeightPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 622
        value_definition = {}

    class SeatAdj2RowRiPosnTiltPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 628
        value_definition = {}

    class SeatAdj2RowRiPosnOTTOAgPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 634
        value_definition = {}

    class SeatAdj2RowRiPosnReleasePos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 640
        value_definition = {}

    class SeatAdj2RowRiPosnBackRestQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 662
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowRiPosnLengthPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 660
        value_definition = {}

    class SeatAdj2RowRiPosnLengthQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 666
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowRiPosnCLAQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 664
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowRiPosnTiltQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 678
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowRiPosnBackRestPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 676
        value_definition = {}

    class SeatAdj2RowRiPosnOTTOAgQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 682
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowRiPosnHeightQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 903
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 680
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowRiAntiPinchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 902
        signal_description = "Antipinch Work Status"
        signal_length = 2
        start_position = 694
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class SeatAdj3RowRiPosnHeightQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 692
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowRiPosnOTTOAgPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 690
        value_definition = {}

    class SeatAdj3RowRiPosnOTTOLenPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 696
        value_definition = {}

    class SeatAdj3RowRiPosnLengthQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 718
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowRiPosnBackRestPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 716
        value_definition = {}

    class SeatAdj3RowRiPosnReleasePos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 722
        value_definition = {}

    class SeatAdj3RowRiPosnBackRestQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 728
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowRiPosnTiltPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 742
        value_definition = {}

    class SeatAdj3RowRiPosnHeightPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 748
        value_definition = {}

    class SeatAdj3RowRiPosnCLAPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 754
        value_definition = {}

    class SeatAdj3RowRiPosnOTTOLenQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 760
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowRiPosnOTTOAgQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 774
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowRiPosnLengthPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Motor Position Percentage"
        signal_length = 10
        start_position = 772
        value_definition = {}

    class SeatAdj3RowRiPosnCLAQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 778
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowRiPosnReleaseQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 776
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowRiPosnTiltQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 901
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 790
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatLieDwnRiSwtStsFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 900
        signal_description = "Fault or not"
        signal_length = 2
        start_position = 788
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class SeatLieDwnRiSwtStsPsdNotPsd1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 900
        signal_description = "Press Status"
        signal_length = 1
        start_position = 786
        value_definition = {'0x0': ' PsdNotPsd1_NotPsd', '0x1': ' PsdNotPsd1_Psd'}

    class SeatLumFrntRiRunStsFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 899
        signal_description = "Lumbar Work Status"
        signal_length = 2
        start_position = 785
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class SeatLumReRiRunStsFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 898
        signal_description = "Lumbar Work Status"
        signal_length = 2
        start_position = 799
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class SeatMassgEcuFrntRiErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 897
        signal_description = "Massage Module Error Status"
        signal_length = 2
        start_position = 797
        value_definition = {'0x0': ' EcuErrorType_Idle', '0x1': ' EcuErrorType_InternalError', '0x2': ' EcuErrorType_ExternalError', '0x3': ' EcuErrorType_reserved'}

    class SeatMassgEcuReRiErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 896
        signal_description = "Massage Module Error Status"
        signal_length = 2
        start_position = 795
        value_definition = {'0x0': ' EcuErrorType_Idle', '0x1': ' EcuErrorType_InternalError', '0x2': ' EcuErrorType_ExternalError', '0x3': ' EcuErrorType_reserved'}

    class SeatMassgFrntRiRunStsFbMassgProg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 911
        signal_description = "Massage Type"
        signal_length = 3
        start_position = 793
        value_definition = {'0x0': ' MassgProg_Prog0', '0x1': ' MassgProg_Prog1', '0x2': ' MassgProg_Prog2', '0x3': ' MassgProg_Prog3', '0x4': ' MassgProg_Prog4', '0x5': ' MassgProg_Prog5', '0x6': ' MassgProg_Prog6', '0x7': ' MassgProg_Prog7'}

    class SeatMassgFrntRiRunStsFbOnOffNoCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 911
        signal_description = "Massage Work Status"
        signal_length = 2
        start_position = 806
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class SeatMassgFrntRiRunStsFbMassgLvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 911
        signal_description = "Massage Intensity Level Status"
        signal_length = 2
        start_position = 804
        value_definition = {'0x0': ' MassgLvlSts_Idle', '0x1': ' MassgLvlSts_Low', '0x2': ' MassgLvlSts_Mid', '0x3': ' MassgLvlSts_High'}

    class SeatMassgReRiRunStsFbOnOffNoCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 910
        signal_description = "Massage Work Status"
        signal_length = 2
        start_position = 802
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class SeatMassgReRiRunStsFbMassgProg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 910
        signal_description = "Massage Type"
        signal_length = 3
        start_position = 800
        value_definition = {'0x0': ' MassgProg_Prog0', '0x1': ' MassgProg_Prog1', '0x2': ' MassgProg_Prog2', '0x3': ' MassgProg_Prog3', '0x4': ' MassgProg_Prog4', '0x5': ' MassgProg_Prog5', '0x6': ' MassgProg_Prog6', '0x7': ' MassgProg_Prog7'}

    class SeatMassgReRiRunStsFbMassgLvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 910
        signal_description = "Massage Intensity Level Status"
        signal_length = 2
        start_position = 813
        value_definition = {'0x0': ' MassgLvlSts_Idle', '0x1': ' MassgLvlSts_Low', '0x2': ' MassgLvlSts_Mid', '0x3': ' MassgLvlSts_High'}

    class TrAng:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 909
        signal_description = "trunk open  angle"
        signal_length = 7
        start_position = 811
        value_definition = {}

    class TrAntiPnchStsCloseAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 908
        signal_description = "trunk close direction AntiPnch status"
        signal_length = 1
        start_position = 820
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class TrAntiPnchStsOPenAntiPnchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 908
        signal_description = "trunk open direction AntiPnch status"
        signal_length = 1
        start_position = 819
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class TrInsdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 907
        signal_description = "inside switch status of trunk"
        signal_length = 3
        start_position = 818
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class TrMtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 906
        signal_description = "Power trunk motion status"
        signal_length = 4
        start_position = 831
        value_definition = {'0x0': ' DoorMtnSts_IniVal', '0x1': ' DoorMtnSts_FullOpen', '0x2': ' DoorMtnSts_FullClose', '0x3': ' DoorMtnSts_StopDurOpen', '0x4': ' DoorMtnSts_StopDurClose', '0x5': ' DoorMtnSts_MovingOut', '0x6': ' DoorMtnSts_MovingIn', '0x7': ' DoorMtnSts_HalfClose', '0x8': ' DoorMtnSts_Unknow', '0x9': ' DoorMtnSts_OnlyOpenPosn'}

    class TrOutdSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 905
        signal_description = "Switch status of Outside trunk"
        signal_length = 3
        start_position = 827
        value_definition = {'0x0': ' SwtSts_IniVal', '0x1': ' SwtSts_Pressd', '0x2': ' SwtSts_NotPressd', '0x3': ' SwtSts_SWStuck', '0x4': ' SwtSts_Error'}

    class TrPosn:
        comments = ""
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 904
        signal_description = "Trunk position"
        signal_length = 8
        start_position = 839
        value_definition = {}

    class TrunkLiFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 919
        signal_description = "light error code"
        signal_length = 8
        start_position = 847
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class TrunkLiFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 919
        signal_description = "light priority"
        signal_length = 8
        start_position = 855
        value_definition = {}

    class TrunkLiFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 919
        signal_description = "light status feedback"
        signal_length = 4
        start_position = 863
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class WinPassPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 918
        signal_description = "Window Position Feedback"
        signal_length = 5
        start_position = 859
        value_definition = {'0x0': ' PosnPerc_Idle', '0x1': ' PosnPerc_PosnPercUnknow', '0x2': ' PosnPerc_PosnPercFullCls', '0x3': ' PosnPerc_PosnPerc4', '0x4': ' PosnPerc_PosnPerc8', '0x5': ' PosnPerc_PosnPerc12', '0x6': ' PosnPerc_PosnPerc16', '0x7': ' PosnPerc_PosnPerc20', '0x8': ' PosnPerc_PosnPerc24', '0x9': ' PosnPerc_PosnPerc28', '0xA': ' PosnPerc_PosnPerc32', '0xB': ' PosnPerc_PosnPerc36', '0xC': ' PosnPerc_PosnPerc40', '0xD': ' PosnPerc_PosnPerc44', '0xE': ' PosnPerc_PosnPerc48', '0xF': ' PosnPerc_PosnPerc52', '0x10': ' PosnPerc_PosnPerc56', '0x11': ' PosnPerc_PosnPerc60', '0x12': ' PosnPerc_PosnPerc64', '0x13': ' PosnPerc_PosnPerc68', '0x14': ' PosnPerc_PosnPerc72', '0x15': ' PosnPerc_PosnPerc76', '0x16': ' PosnPerc_PosnPerc80', '0x17': ' PosnPerc_PosnPerc84', '0x18': ' PosnPerc_PosnPerc88', '0x19': ' PosnPerc_PosnPerc92', '0x1A': ' PosnPerc_PosnPerc96', '0x1B': ' PosnPerc_FullOpen', '0x1C': ' PosnPerc_Reserved1', '0x1D': ' PosnPerc_Reserved2', '0x1E': ' PosnPerc_Reserved3'}

    class WinPassRvsInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 916
        signal_description = "Window Antipinch Reverse Happened or Not"
        signal_length = 2
        start_position = 879
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class WinPassShoMoveSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 915
        signal_description = "Window Short Move Status"
        signal_length = 3
        start_position = 877
        value_definition = {'0x0': ' WinShoSts_Idle', '0x1': ' WinShoSts_ShoUping', '0x2': ' WinShoSts_ShoUp', '0x3': ' WinShoSts_ShoDwning', '0x4': ' WinShoSts_ShoDwn', '0x5': ' WinShoSts_Reserved'}

    class WinReRiPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 914
        signal_description = "Window Position Feedback"
        signal_length = 5
        start_position = 874
        value_definition = {'0x0': ' PosnPerc_Idle', '0x1': ' PosnPerc_PosnPercUnknow', '0x2': ' PosnPerc_PosnPercFullCls', '0x3': ' PosnPerc_PosnPerc4', '0x4': ' PosnPerc_PosnPerc8', '0x5': ' PosnPerc_PosnPerc12', '0x6': ' PosnPerc_PosnPerc16', '0x7': ' PosnPerc_PosnPerc20', '0x8': ' PosnPerc_PosnPerc24', '0x9': ' PosnPerc_PosnPerc28', '0xA': ' PosnPerc_PosnPerc32', '0xB': ' PosnPerc_PosnPerc36', '0xC': ' PosnPerc_PosnPerc40', '0xD': ' PosnPerc_PosnPerc44', '0xE': ' PosnPerc_PosnPerc48', '0xF': ' PosnPerc_PosnPerc52', '0x10': ' PosnPerc_PosnPerc56', '0x11': ' PosnPerc_PosnPerc60', '0x12': ' PosnPerc_PosnPerc64', '0x13': ' PosnPerc_PosnPerc68', '0x14': ' PosnPerc_PosnPerc72', '0x15': ' PosnPerc_PosnPerc76', '0x16': ' PosnPerc_PosnPerc80', '0x17': ' PosnPerc_PosnPerc84', '0x18': ' PosnPerc_PosnPerc88', '0x19': ' PosnPerc_PosnPerc92', '0x1A': ' PosnPerc_PosnPerc96', '0x1B': ' PosnPerc_FullOpen', '0x1C': ' PosnPerc_Reserved1', '0x1D': ' PosnPerc_Reserved2', '0x1E': ' PosnPerc_Reserved3'}

    class WinReRiRvsInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 912
        signal_description = "Window Antipinch Reverse Happened or Not"
        signal_length = 2
        start_position = 894
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class WinReRiShoMoveSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 370
        signal_description = "Window Short Move Status"
        signal_length = 3
        start_position = 892
        value_definition = {'0x0': ' WinShoSts_Idle', '0x1': ' WinShoSts_ShoUping', '0x2': ' WinShoSts_ShoUp', '0x3': ' WinShoSts_ShoDwning', '0x4': ' WinShoSts_ShoDwn', '0x5': ' WinShoSts_Reserved'}

    class SeatAdj3RowRiBtnStsSeatAdjTiltBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 994
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 997
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowRiBtnStsSeatAdjOTTOAgBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 994
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 987
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowRiBtnStsSeatAdjBackBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 994
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 983
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowRiBtnStsSeatAdjLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 994
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 990
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowRiBtnStsSeatAdjHeiBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 994
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 977
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowRiBtnStsSeatAdjCLABtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 994
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 980
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowRiBtnStsSeatAdjOTTOLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 994
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 984
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class ExtrReViewMirrFoldSrcPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 922
        signal_description = ""
        signal_length = 5
        start_position = 927
        value_definition = {'0x0': ' ReViewMirrFoldSrc_IniValue', '0x1': ' ReViewMirrFoldSrc_AutoCtrl', '0x2': ' ReViewMirrFoldSrc_ManCtrl', '0x3': ' ReViewMirrFoldSrc_RemCtrl', '0x4': ' ReViewMirrFoldSrc_VehSpdUnfold', '0x5': ' ReViewMirrFoldSrc_Others'}

    class ExtrReViewMirrAutoFoldEnaStsPass:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "外后视镜自动折叠使能状态"
        signal_length = 2
        start_position = 19
        value_definition = {'0x0': ' MirrAutoEn_Idle', '0x1': ' MirrAutoEn_EnableBoth', '0x2': ' MirrAutoEn_EnableFoldOnly', '0x3': ' MirrAutoEn_EnableUnfoldOnly', '0x4': ' MirrAutoEn_Disable'}

    class SeatAdj1RowRiBtnStsSeatAdjTiltBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 946
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 949
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowRiBtnStsSeatAdjHeiBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 946
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 929
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowRiBtnStsSeatAdjOTTOAgBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 946
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 939
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowRiBtnStsSeatAdjLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 946
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 942
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowRiBtnStsSeatAdjOTTOLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 946
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 936
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowRiBtnStsSeatAdjCLABtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 946
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 932
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowRiBtnStsSeatAdjBackBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 946
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 935
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowRiBtnStsSeatAdjOTTOAgBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 970
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 963
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowRiBtnStsSeatAdjLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 970
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 966
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowRiBtnStsSeatAdjBackBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 970
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 959
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowRiBtnStsSeatAdjHeiBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 970
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 953
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowRiBtnStsSeatAdjOTTOLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 970
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 960
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowRiBtnStsSeatAdjTiltBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 970
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 973
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowRiBtnStsSeatAdjCLABtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 970
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 956
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}


class LCURToCCUSOCCDEthSignalIPdu05:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x604005
    pdu_length_bytes = 20
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-20ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'SeatAdj1RowRiMotSts': ['SeatAdj1RowRiMotStsMotorStsTilt', 'SeatAdj1RowRiMotStsMotorStsCLA', 'SeatAdj1RowRiMotStsMotorStsHei', 'SeatAdj1RowRiMotStsMotorStsOTTOLen', 'SeatAdj1RowRiMotStsMotorStsLen', 'SeatAdj1RowRiMotStsMotorStsOTF', 'SeatAdj1RowRiMotStsMotorStsRe', 'SeatAdj1RowRiMotStsMotorStsOTTOAg', 'SeatAdj1RowRiMotStsMotorStsBack'], 'SeatAdj2RowRiMotSts': ['SeatAdj2RowRiMotStsMotorStsOTTOLen', 'SeatAdj2RowRiMotStsMotorStsRe', 'SeatAdj2RowRiMotStsMotorStsCLA', 'SeatAdj2RowRiMotStsMotorStsLen', 'SeatAdj2RowRiMotStsMotorStsOTF', 'SeatAdj2RowRiMotStsMotorStsHei', 'SeatAdj2RowRiMotStsMotorStsBack', 'SeatAdj2RowRiMotStsMotorStsOTTOAg', 'SeatAdj2RowRiMotStsMotorStsTilt'], 'SeatAdj3RowRiMotSts': ['SeatAdj3RowRiMotStsMotorStsHei', 'SeatAdj3RowRiMotStsMotorStsBack', 'SeatAdj3RowRiMotStsMotorStsOTF', 'SeatAdj3RowRiMotStsMotorStsTilt', 'SeatAdj3RowRiMotStsMotorStsCLA', 'SeatAdj3RowRiMotStsMotorStsRe', 'SeatAdj3RowRiMotStsMotorStsLen', 'SeatAdj3RowRiMotStsMotorStsOTTOAg', 'SeatAdj3RowRiMotStsMotorStsOTTOLen']}

    class FRDoorObstclDst:
        comments = ""
        factor = 0.5
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 125
        signal_description = "Door obstacle detecting"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class RRDoorObstclDst:
        comments = ""
        factor = 0.5
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 124
        signal_description = "Door obstacle detecting"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class SeatAdj1RowRiMotStsMotorStsTilt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 123
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 23
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowRiMotStsMotorStsCLA:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 123
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 20
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowRiMotStsMotorStsHei:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 123
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 17
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowRiMotStsMotorStsOTTOLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 123
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 30
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowRiMotStsMotorStsLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 123
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 27
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowRiMotStsMotorStsOTF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 123
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 24
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowRiMotStsMotorStsRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 123
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 37
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowRiMotStsMotorStsOTTOAg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 123
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 34
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowRiMotStsMotorStsBack:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 123
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 47
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowRiMotStsMotorStsOTTOLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 122
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 44
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowRiMotStsMotorStsRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 122
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 41
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowRiMotStsMotorStsCLA:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 122
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 54
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowRiMotStsMotorStsLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 122
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 51
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowRiMotStsMotorStsOTF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 122
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 48
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowRiMotStsMotorStsHei:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 122
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 61
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowRiMotStsMotorStsBack:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 122
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 58
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowRiMotStsMotorStsOTTOAg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 122
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 71
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowRiMotStsMotorStsTilt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 122
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 68
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowRiMotStsMotorStsHei:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 121
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 65
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowRiMotStsMotorStsBack:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 121
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 78
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowRiMotStsMotorStsOTF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 121
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 75
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowRiMotStsMotorStsTilt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 121
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 72
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowRiMotStsMotorStsCLA:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 121
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 85
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowRiMotStsMotorStsRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 121
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 82
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowRiMotStsMotorStsLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 121
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 95
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowRiMotStsMotorStsOTTOAg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 121
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 92
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowRiMotStsMotorStsOTTOLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 121
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 89
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatLum1RowRiSwtErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 120
        signal_description = "1Row Right Lumbar Key Error Status"
        signal_length = 2
        start_position = 102
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class SeatLum1RowRiSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 135
        signal_description = "Lumbar Key Direction"
        signal_length = 3
        start_position = 100
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatLum2RowRiSwtErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 134
        signal_description = "2Row Right Lumbar Key Error Status"
        signal_length = 2
        start_position = 97
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class SeatLum2RowRiSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 133
        signal_description = "Lumbar Key Direction"
        signal_length = 3
        start_position = 111
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatLum3RowRiSwtErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 132
        signal_description = "3Row Right Lumbar Key Error Status"
        signal_length = 2
        start_position = 108
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class SeatLum3RowRiSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 131
        signal_description = "Lumbar Key Direction"
        signal_length = 3
        start_position = 106
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class WinPassBtnErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 130
        signal_description = "Window Button Error Status"
        signal_length = 2
        start_position = 119
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class WinPassBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 129
        signal_description = "Window Button Status"
        signal_length = 3
        start_position = 117
        value_definition = {'0x0': ' WinBtnReq_Idle', '0x1': ' WinBtnReq_Up1', '0x2': ' WinBtnReq_Up2', '0x3': ' WinBtnReq_Dwn1', '0x4': ' WinBtnReq_Dwn2', '0x5': ' WinBtnReq_Undef', '0x6': ' WinBtnReq_Reserved1', '0x7': ' WinBtnReq_Reserved2'}

    class WinReRiBtnErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 128
        signal_description = "Window Button Error Status"
        signal_length = 2
        start_position = 114
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class WinReRiBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 143
        signal_description = "Window Button Status"
        signal_length = 3
        start_position = 112
        value_definition = {'0x0': ' WinBtnReq_Idle', '0x1': ' WinBtnReq_Up1', '0x2': ' WinBtnReq_Up2', '0x3': ' WinBtnReq_Dwn1', '0x4': ' WinBtnReq_Dwn2', '0x5': ' WinBtnReq_Undef', '0x6': ' WinBtnReq_Reserved1', '0x7': ' WinBtnReq_Reserved2'}


class LCURToCCUSOCCDEthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x604004
    pdu_length_bytes = 1
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-200ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'PwrContnsChRiCfgSts': ['PwrContnsChRiCfgStsContnsRiCh1CfgSts', 'PwrContnsChRiCfgStsContnsRiCh4CfgSts', 'PwrContnsChRiCfgStsContnsRiCh2CfgSts', 'PwrContnsChRiCfgStsContnsRiCh3CfgSts', 'PwrContnsChRiCfgStsContnsRiCh5CfgSts']}

    class DefrstPassFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "defrosting failure of the passenger side mirror"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class PwrContnsChRiCfgStsContnsRiCh1CfgSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "Right Zone Contns Power Channel 1 Config Status"
        signal_length = 1
        start_position = 6
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrContnsChRiCfgStsContnsRiCh4CfgSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "Right Zone Contns Power Channel 4 Config Status"
        signal_length = 1
        start_position = 5
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrContnsChRiCfgStsContnsRiCh2CfgSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "Right Zone Contns Power Channel 2 Config Status"
        signal_length = 1
        start_position = 4
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrContnsChRiCfgStsContnsRiCh3CfgSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "Right Zone Contns Power Channel 3 Config Status"
        signal_length = 1
        start_position = 3
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrContnsChRiCfgStsContnsRiCh5CfgSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "Right Zone Contns Power Channel 5 Config Status"
        signal_length = 1
        start_position = 2
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class LCURToCCUSOCCDEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x604002
    pdu_length_bytes = 51
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-10ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'PwrChRiCurrVal': ['PwrChRiCurrValSwilPwrChRi19CurrVal', 'PwrChRiCurrValSwilPwrChRi9CurrVal', 'PwrChRiCurrValSwilPwrChRi28CurrVal', 'PwrChRiCurrValSwilPwrChRi11CurrVal', 'PwrChRiCurrValSwilPwrChRi17CurrVal', 'PwrChRiCurrValSwilPwrChRi14CurrVal', 'PwrChRiCurrValSwilPwrChRi6CurrVal', 'PwrChRiCurrValSwilPwrChRi25CurrVal', 'PwrChRiCurrValSwilPwrChRi15CurrVal', 'PwrChRiCurrValSwilPwrChRi13CurrVal', 'PwrChRiCurrValSwilPwrChRi1CurrVal', 'PwrChRiCurrValSwilPwrChRi26CurrVal', 'PwrChRiCurrValSwilPwrChRi16CurrVal', 'PwrChRiCurrValSwilPwrChRi3CurrVal', 'PwrChRiCurrValSwilPwrChRi21CurrVal', 'PwrChRiCurrValSwilPwrChRi4CurrVal', 'PwrChRiCurrValSwilPwrChRi18CurrVal', 'PwrChRiCurrValSwilPwrChRi20CurrVal', 'PwrChRiCurrValSwilPwrChRi23CurrVal', 'PwrChRiCurrValContnsPwrChRi4CurrVal', 'PwrChRiCurrValSwilPwrChRi7CurrVal', 'PwrChRiCurrValContnsPwrChRi5CurrVal', 'PwrChRiCurrValContnsPwrChRi3CurrVal', 'PwrChRiCurrValSwilPwrChRi24CurrVal', 'PwrChRiCurrValContnsPwrChRi2CurrVal', 'PwrChRiCurrValSwilPwrChRi5CurrVal', 'PwrChRiCurrValSwilPwrChRi12CurrVal', 'PwrChRiCurrValSwilPwrChRi29CurrVal', 'PwrChRiCurrValSwilPwrChRi8CurrVal', 'PwrChRiCurrValSwilPwrChRi22CurrVal', 'PwrChRiCurrValSwilPwrChRi2CurrVal', 'PwrChRiCurrValSwilPwrChRi10CurrVal', 'PwrChRiCurrValContnsPwrChRi1CurrVal', 'PwrChRiCurrValSwilPwrChRi27CurrVal']}

    class PwrChRiCurrValSwilPwrChRi19CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 19 Current Value"
        signal_length = 12
        start_position = 7
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi9CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 9 Current Value"
        signal_length = 12
        start_position = 11
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi28CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 28 Current Value"
        signal_length = 12
        start_position = 31
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi11CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 11 Current Value"
        signal_length = 12
        start_position = 35
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi17CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 17 Current Value"
        signal_length = 12
        start_position = 55
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi14CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 14 Current Value"
        signal_length = 12
        start_position = 59
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi6CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 6 Current Value"
        signal_length = 12
        start_position = 79
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi25CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 25 Current Value"
        signal_length = 12
        start_position = 83
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi15CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 15 Current Value"
        signal_length = 12
        start_position = 103
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi13CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 13 Current Value"
        signal_length = 12
        start_position = 107
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi1CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 1 Current Value"
        signal_length = 12
        start_position = 127
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi26CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 26 Current Value"
        signal_length = 12
        start_position = 131
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi16CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 16 Current Value"
        signal_length = 12
        start_position = 151
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi3CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 3 Current Value"
        signal_length = 12
        start_position = 155
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi21CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 21 Current Value"
        signal_length = 12
        start_position = 175
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi4CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 4 Current Value"
        signal_length = 12
        start_position = 179
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi18CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 18 Current Value"
        signal_length = 12
        start_position = 199
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi20CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 20 Current Value"
        signal_length = 12
        start_position = 203
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi23CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 23 Current Value"
        signal_length = 12
        start_position = 223
        value_definition = {}

    class PwrChRiCurrValContnsPwrChRi4CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Contns Power Channel 4 Current Value"
        signal_length = 12
        start_position = 227
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi7CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 7 Current Value"
        signal_length = 12
        start_position = 247
        value_definition = {}

    class PwrChRiCurrValContnsPwrChRi5CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Contns Power Channel 5 Current Value"
        signal_length = 12
        start_position = 251
        value_definition = {}

    class PwrChRiCurrValContnsPwrChRi3CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Contns Power Channel 3 Current Value"
        signal_length = 12
        start_position = 271
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi24CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 24 Current Value"
        signal_length = 12
        start_position = 275
        value_definition = {}

    class PwrChRiCurrValContnsPwrChRi2CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Contns Power Channel 2 Current Value"
        signal_length = 12
        start_position = 295
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi5CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 5 Current Value"
        signal_length = 12
        start_position = 299
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi12CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 12 Current Value"
        signal_length = 12
        start_position = 319
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi29CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 29 Current Value"
        signal_length = 12
        start_position = 323
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi8CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 8 Current Value"
        signal_length = 12
        start_position = 343
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi22CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 22 Current Value"
        signal_length = 12
        start_position = 347
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi2CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 2 Current Value"
        signal_length = 12
        start_position = 367
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi10CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 10 Current Value"
        signal_length = 12
        start_position = 371
        value_definition = {}

    class PwrChRiCurrValContnsPwrChRi1CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Contns Power Channel 1 Current Value"
        signal_length = 12
        start_position = 391
        value_definition = {}

    class PwrChRiCurrValSwilPwrChRi27CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = None
        signal_description = "Right Zone Swil Power Channel 27 Current Value"
        signal_length = 12
        start_position = 395
        value_definition = {}


class LCURToCCUSOCCDEthSignalIPdu06:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x604006
    pdu_length_bytes = 3
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-30ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'FuncStsOfLowBeam': ['FuncStsOfLowBeamLightSts', 'FuncStsOfLowBeamLightPriority', 'FuncStsOfLowBeamLightErrorCode']}

    class FuncStsOfLowBeamLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "LightSts"
        signal_length = 4
        start_position = 23
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfLowBeamLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class FuncStsOfLowBeamLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 19
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}


class LCURToCCUSOCCDEthSignalIPdu07:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x604007
    pdu_length_bytes = 3
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-40ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'ExtrReViewMirrInMovmtStsPass': ['ExtrReViewMirrInMovmtStsPassInMovmtStsLeRi', 'ExtrReViewMirrInMovmtStsPassInMovmtStsUpDown'], 'ExtrReViewMirrPosnPass': ['ExtrReViewMirrPosnPassLeAndRi', 'ExtrReViewMirrPosnPassUpAndDown']}

    class ExtrReViewMirrInMovmtStsPassInMovmtStsLeRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "the left and right motion status of external rear view mirror at passenger"
        signal_length = 1
        start_position = 4
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ExtrReViewMirrInMovmtStsPassInMovmtStsUpDown:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "the up and down motion status of external rear view mirror at passenger"
        signal_length = 1
        start_position = 3
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ExtrReViewMirrPosnPassLeAndRi:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "external rear view mirror positing in the left and right direction at passenger side."
        signal_length = 8
        start_position = 15
        value_definition = {}

    class ExtrReViewMirrPosnPassUpAndDown:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "external rear view mirror position in the up and down direction at passenger side"
        signal_length = 8
        start_position = 23
        value_definition = {}


class LCURToCCUSOCCDEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x604003
    pdu_length_bytes = 24
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-160ms"
    sender = "LCUR"
    server_socket = "SocketLcuRSoAdUDP"
    signal_group = {'HVAirHeatrE2E': ['HVAirHeatrE2ECntr', 'HVAirHeatrE2EHvahEnad', 'HVAirHeatrE2EChks'], 'HvCooltHeatrEnadWhE2E': ['HvCooltHeatrEnadWhE2EHvchEnad', 'HvCooltHeatrEnadWhE2EChks', 'HvCooltHeatrEnadWhE2ECntr']}

    class BCFVCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 102
        signal_description = "BCFV reference drive request to learn mechanical stops."
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' RefDrvReq_NoReq', '0x1': ' RefDrvReq_REFDRV_Req', '0x2': ' RefDrvReq_Reserved', '0x3': ' RefDrvReq_SNA'}

    class BCFVPosnSaveReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 101
        signal_description = "BCFV position request before power off."
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' ActiveSaveReq_NoReq', '0x1': ' ActiveSaveReq_ActiveSave_Req', '0x2': ' ActiveSaveReq_Reserved', '0x3': ' ActiveSaveReq_SNA'}

    class BCFVPosnSetReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 100
        signal_description = "BCFV position request."
        signal_length = 7
        start_position = 3
        value_definition = {}

    class BCFVSpdLvlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 99
        signal_description = "BCFV move speed level request."
        signal_length = 2
        start_position = 12
        value_definition = {'0x0': ' SpdLvlReq_Level0_Slow', '0x1': ' SpdLvlReq_Level1_Normal', '0x2': ' SpdLvlReq_Level2_Fast', '0x3': ' SpdLvlReq_SNA'}

    class BCTVCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 98
        signal_description = "Battery three-way valve reference drive request to learn mechanical stops."
        signal_length = 2
        start_position = 10
        value_definition = {'0x0': ' RefDrvReq_NoReq', '0x1': ' RefDrvReq_REFDRV_Req', '0x2': ' RefDrvReq_Reserved', '0x3': ' RefDrvReq_SNA'}

    class BCTVPosnSaveReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 97
        signal_description = "Battery three-way valve save valve position request before power off."
        signal_length = 2
        start_position = 8
        value_definition = {'0x0': ' ActiveSaveReq_NoReq', '0x1': ' ActiveSaveReq_ActiveSave_Req', '0x2': ' ActiveSaveReq_Reserved', '0x3': ' ActiveSaveReq_SNA'}

    class BCTVPosnSetReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 96
        signal_description = "Battery three-way valve position request."
        signal_length = 7
        start_position = 22
        value_definition = {}

    class BCTVSpdLvlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 114
        signal_description = "Battery three-way valve move speed level request."
        signal_length = 2
        start_position = 31
        value_definition = {'0x0': ' SpdLvlReq_Level0_Slow', '0x1': ' SpdLvlReq_Level1_Normal', '0x2': ' SpdLvlReq_Level2_Fast', '0x3': ' SpdLvlReq_SNA'}

    class CCTVCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 113
        signal_description = "CCTV reference drive request to learn mechanical stops."
        signal_length = 2
        start_position = 29
        value_definition = {'0x0': ' RefDrvReq_NoReq', '0x1': ' RefDrvReq_REFDRV_Req', '0x2': ' RefDrvReq_Reserved', '0x3': ' RefDrvReq_SNA'}

    class CCTVPosnSaveReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 112
        signal_description = "CCTV save valve position request before power off."
        signal_length = 2
        start_position = 27
        value_definition = {'0x0': ' ActiveSaveReq_NoReq', '0x1': ' ActiveSaveReq_ActiveSave_Req', '0x2': ' ActiveSaveReq_Reserved', '0x3': ' ActiveSaveReq_SNA'}

    class CCTVPosnSetReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 130
        signal_description = "CCTV position request."
        signal_length = 7
        start_position = 25
        value_definition = {}

    class CCTVSpdLvlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 129
        signal_description = "CCTV move speed level request."
        signal_length = 2
        start_position = 34
        value_definition = {'0x0': ' SpdLvlReq_Level0_Slow', '0x1': ' SpdLvlReq_Level1_Normal', '0x2': ' SpdLvlReq_Level2_Fast', '0x3': ' SpdLvlReq_SNA'}

    class CooltFlowInCmptmtCirc:
        comments = ""
        factor = 0.05
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 128
        signal_description = "Informs of coolant flow in the heat exchange. Created for the short coolant circuit in hybrid cars."
        signal_length = 10
        start_position = 32
        value_definition = {}

    class DCTVCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 162
        signal_description = "DCTV reference drive request to learn mechanical stops."
        signal_length = 2
        start_position = 54
        value_definition = {'0x0': ' RefDrvReq_NoReq', '0x1': ' RefDrvReq_REFDRV_Req', '0x2': ' RefDrvReq_Reserved', '0x3': ' RefDrvReq_SNA'}

    class DCTVPosnSaveReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 161
        signal_description = "DCTV position request before power off."
        signal_length = 2
        start_position = 52
        value_definition = {'0x0': ' ActiveSaveReq_NoReq', '0x1': ' ActiveSaveReq_ActiveSave_Req', '0x2': ' ActiveSaveReq_Reserved', '0x3': ' ActiveSaveReq_SNA'}

    class DCTVPosnSetReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 160
        signal_description = "DCTV position request."
        signal_length = 7
        start_position = 50
        value_definition = {}

    class DCTVSpdLvlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 175
        signal_description = "DCTV move speed level request."
        signal_length = 2
        start_position = 59
        value_definition = {'0x0': ' SpdLvlReq_Level0_Slow', '0x1': ' SpdLvlReq_Level1_Normal', '0x2': ' SpdLvlReq_Level2_Fast', '0x3': ' SpdLvlReq_SNA'}

    class ECTVCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 174
        signal_description = "ECTV reference drive request to learn mechanical stops."
        signal_length = 2
        start_position = 57
        value_definition = {'0x0': ' RefDrvReq_NoReq', '0x1': ' RefDrvReq_REFDRV_Req', '0x2': ' RefDrvReq_Reserved', '0x3': ' RefDrvReq_SNA'}

    class ECTVPosnSaveReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 173
        signal_description = "ECTV position request before power off."
        signal_length = 2
        start_position = 71
        value_definition = {'0x0': ' ActiveSaveReq_NoReq', '0x1': ' ActiveSaveReq_ActiveSave_Req', '0x2': ' ActiveSaveReq_Reserved', '0x3': ' ActiveSaveReq_SNA'}

    class ECTVPosnSetReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 172
        signal_description = "ECTV position request."
        signal_length = 7
        start_position = 69
        value_definition = {}

    class ECTVSpdLvlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 171
        signal_description = "ECTV move speed level request."
        signal_length = 2
        start_position = 78
        value_definition = {'0x0': ' SpdLvlReq_Level0_Slow', '0x1': ' SpdLvlReq_Level1_Normal', '0x2': ' SpdLvlReq_Level2_Fast', '0x3': ' SpdLvlReq_SNA'}

    class HCTVCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 170
        signal_description = "HCTV reference drive request to learn mechanical stops."
        signal_length = 2
        start_position = 76
        value_definition = {'0x0': ' RefDrvReq_NoReq', '0x1': ' RefDrvReq_REFDRV_Req', '0x2': ' RefDrvReq_Reserved', '0x3': ' RefDrvReq_SNA'}

    class HCTVPosnSaveReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 169
        signal_description = "HCTV position request before power off."
        signal_length = 2
        start_position = 74
        value_definition = {'0x0': ' ActiveSaveReq_NoReq', '0x1': ' ActiveSaveReq_ActiveSave_Req', '0x2': ' ActiveSaveReq_Reserved', '0x3': ' ActiveSaveReq_SNA'}

    class HCTVPosnSetReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 168
        signal_description = "HCTV position request."
        signal_length = 7
        start_position = 72
        value_definition = {}

    class HCTVSpdLvlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 183
        signal_description = "HCTV move speed level request."
        signal_length = 2
        start_position = 81
        value_definition = {'0x0': ' SpdLvlReq_Level0_Slow', '0x1': ' SpdLvlReq_Level1_Normal', '0x2': ' SpdLvlReq_Level2_Fast', '0x3': ' SpdLvlReq_SNA'}

    class HVAirHeatrCtrlMod:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 182
        signal_description = "HVAH Control Mode"
        signal_length = 2
        start_position = 95
        value_definition = {'0x0': ' PTCCtrlMod_Default', '0x1': ' PTCCtrlMod_Duty', '0x2': ' PTCCtrlMod_Pwr', '0x3': ' PTCCtrlMod_Reserved'}

    class HVAirHeatrDutyReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 181
        signal_description = "HVAH Duty Request"
        signal_length = 7
        start_position = 93
        value_definition = {}

    class HVAirHeatrE2ECntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 180
        signal_description = "Counter for E2E."
        signal_length = 4
        start_position = 119
        value_definition = {}

    class HVAirHeatrE2EHvahEnad:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 180
        signal_description = "HVAH enable."
        signal_length = 1
        start_position = 115
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class HVAirHeatrE2EChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 180
        signal_description = "Checksum for E2E."
        signal_length = 8
        start_position = 111
        value_definition = {}

    class HvCooltHeatrEnadWhE2EHvchEnad:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 179
        signal_description = "HVCH enable."
        signal_length = 1
        start_position = 131
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class HvCooltHeatrEnadWhE2EChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 179
        signal_description = "Checksum for E2E."
        signal_length = 8
        start_position = 127
        value_definition = {}

    class HvCooltHeatrEnadWhE2ECntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 179
        signal_description = "Counter for E2E."
        signal_length = 4
        start_position = 135
        value_definition = {}

    class HvWtrHeatrPwrCnsAllwd:
        comments = ""
        factor = 40.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 178
        signal_description = "Power consumption allowed for HVCH"
        signal_length = 8
        start_position = 143
        value_definition = {}

    class HvWtrHeatrWtrTDes:
        comments = ""
        factor = 1.0
        initial_value = 40
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 177
        signal_description = "Water temperature desired from heating manager."
        signal_length = 8
        start_position = 151
        value_definition = {}

    class LCTVCalReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 176
        signal_description = "LCTV reference drive request to learn mechanical stops."
        signal_length = 2
        start_position = 159
        value_definition = {'0x0': ' RefDrvReq_NoReq', '0x1': ' RefDrvReq_REFDRV_Req', '0x2': ' RefDrvReq_Reserved', '0x3': ' RefDrvReq_SNA'}

    class LCTVPosnSaveReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 191
        signal_description = "LCTV position request before power off."
        signal_length = 2
        start_position = 157
        value_definition = {'0x0': ' ActiveSaveReq_NoReq', '0x1': ' ActiveSaveReq_ActiveSave_Req', '0x2': ' ActiveSaveReq_Reserved', '0x3': ' ActiveSaveReq_SNA'}

    class LCTVPosnSetReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 190
        signal_description = "LCTV position request."
        signal_length = 7
        start_position = 155
        value_definition = {}

    class LCTVSpdLvlReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 189
        signal_description = "LCTV move speed level request."
        signal_length = 2
        start_position = 164
        value_definition = {'0x0': ' SpdLvlReq_Level0_Slow', '0x1': ' SpdLvlReq_Level1_Normal', '0x2': ' SpdLvlReq_Level2_Fast', '0x3': ' SpdLvlReq_SNA'}
