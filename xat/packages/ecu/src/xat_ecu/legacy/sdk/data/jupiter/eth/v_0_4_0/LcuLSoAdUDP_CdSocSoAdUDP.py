

class LCULToCCUSOCCDEthSignalIPdu07:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x504007
    pdu_length_bytes = 1
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-500ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {}

    class DrvrSeatOccpSnsrOKSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 6
        signal_description = "Driver Seat Occupy Sensor OK status"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' OkNotOk1_Ok', '0x1': ' OkNotOk1_NotOk'}


class LCULToCCUSOCCDEthSignalIPdu06:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x504006
    pdu_length_bytes = 32
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-40ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'FootwellLiFrntLeFnucSts': ['FootwellLiFrntLeFnucStsLightErrorCode', 'FootwellLiFrntLeFnucStsLightPriority', 'FootwellLiFrntLeFnucStsLightSts', 'FootwellLiFrntLeFnucStsLiPerc'], 'FootwellLiFrntRiFuncSts': ['FootwellLiFrntRiFuncStsLightPriority', 'FootwellLiFrntRiFuncStsLiPerc', 'FootwellLiFrntRiFuncStsLightSts', 'FootwellLiFrntRiFuncStsLightErrorCode'], 'FootwellLiSecLeFuncSts': ['FootwellLiSecLeFuncStsLiPerc', 'FootwellLiSecLeFuncStsLightErrorCode', 'FootwellLiSecLeFuncStsLightPriority', 'FootwellLiSecLeFuncStsLightSts'], 'FootwellLiSecRiFuncSts': ['FootwellLiSecRiFuncStsLiPerc', 'FootwellLiSecRiFuncStsLightSts', 'FootwellLiSecRiFuncStsLightPriority', 'FootwellLiSecRiFuncStsLightErrorCode'], 'FootwellLiThrdLeFuncSts': ['FootwellLiThrdLeFuncStsLightPriority', 'FootwellLiThrdLeFuncStsLiPerc', 'FootwellLiThrdLeFuncStsLightSts', 'FootwellLiThrdLeFuncStsLightErrorCode'], 'FootwellLiThrdRiFuncSts': ['FootwellLiThrdRiFuncStsLightPriority', 'FootwellLiThrdRiFuncStsLightErrorCode', 'FootwellLiThrdRiFuncStsLightSts', 'FootwellLiThrdRiFuncStsLiPerc']}

    class FootwellLiFrntLeFnucStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 52
        signal_description = "error status of footwell light"
        signal_length = 8
        start_position = 31
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FootwellLiFrntLeFnucStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 52
        signal_description = "Light status priority"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class FootwellLiFrntLeFnucStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 52
        signal_description = "light status of footwelll light"
        signal_length = 4
        start_position = 47
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FootwellLiFrntLeFnucStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 52
        signal_description = "Illumination percent"
        signal_length = 7
        start_position = 43
        value_definition = {}

    class FootwellLiFrntRiFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 84
        signal_description = "Light status priority"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class FootwellLiFrntRiFuncStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 84
        signal_description = "illumination percent"
        signal_length = 7
        start_position = 75
        value_definition = {}

    class FootwellLiFrntRiFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 84
        signal_description = "light status of footwelll light"
        signal_length = 4
        start_position = 79
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FootwellLiFrntRiFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 84
        signal_description = "error status of footwell light"
        signal_length = 8
        start_position = 63
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FootwellLiSecLeFuncStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 116
        signal_description = "illumination percent"
        signal_length = 7
        start_position = 107
        value_definition = {}

    class FootwellLiSecLeFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 116
        signal_description = "error status of footwell light"
        signal_length = 8
        start_position = 95
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FootwellLiSecLeFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 116
        signal_description = "Light status priority"
        signal_length = 8
        start_position = 103
        value_definition = {}

    class FootwellLiSecLeFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 116
        signal_description = "light status of footwelll light"
        signal_length = 4
        start_position = 111
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FootwellLiSecRiFuncStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 148
        signal_description = "illumination percent"
        signal_length = 7
        start_position = 139
        value_definition = {}

    class FootwellLiSecRiFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 148
        signal_description = "light status of footwelll light"
        signal_length = 4
        start_position = 143
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FootwellLiSecRiFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 148
        signal_description = "Light status priority"
        signal_length = 8
        start_position = 135
        value_definition = {}

    class FootwellLiSecRiFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 148
        signal_description = "error status of footwell light"
        signal_length = 8
        start_position = 127
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FootwellLiThrdLeFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 180
        signal_description = "Light status priority"
        signal_length = 8
        start_position = 167
        value_definition = {}

    class FootwellLiThrdLeFuncStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 180
        signal_description = "illumination percent"
        signal_length = 7
        start_position = 171
        value_definition = {}

    class FootwellLiThrdLeFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 180
        signal_description = "light status of footwelll light"
        signal_length = 4
        start_position = 175
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FootwellLiThrdLeFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 180
        signal_description = "error status of footwell light"
        signal_length = 8
        start_position = 159
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FootwellLiThrdRiFuncStsLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 212
        signal_description = "Light status priority"
        signal_length = 8
        start_position = 199
        value_definition = {}

    class FootwellLiThrdRiFuncStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 212
        signal_description = "error status of footwell light"
        signal_length = 8
        start_position = 191
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FootwellLiThrdRiFuncStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 212
        signal_description = "light status of footwelll light"
        signal_length = 4
        start_position = 207
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FootwellLiThrdRiFuncStsLiPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 212
        signal_description = "illumination percent"
        signal_length = 7
        start_position = 203
        value_definition = {}


class LCULToCCUSOCCDEthSignalIPdu02:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x504002
    pdu_length_bytes = 64
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-10ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'ExtrReViewMirrInMovmtStsDrvr': ['ExtrReViewMirrInMovmtStsDrvrInMovmtStsUpDown', 'ExtrReViewMirrInMovmtStsDrvrInMovmtStsLeRi'], 'ExtrReViewMirrPosnDrvr': ['ExtrReViewMirrPosnDrvrLeAndRi', 'ExtrReViewMirrPosnDrvrUpAndDown']}

    class ExtrReViewMirrInMovmtStsDrvrInMovmtStsUpDown:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 410
        signal_description = "the up and down motion status of external rear view mirror at driver"
        signal_length = 1
        start_position = 408
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ExtrReViewMirrInMovmtStsDrvrInMovmtStsLeRi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 410
        signal_description = "the left and right motion status of external rear view mirror at driver"
        signal_length = 1
        start_position = 409
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ExtrReViewMirrPosnDrvrLeAndRi:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 414
        signal_description = "external rear view mirror positing in the left and right direction at driver side."
        signal_length = 8
        start_position = 423
        value_definition = {}

    class ExtrReViewMirrPosnDrvrUpAndDown:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 414
        signal_description = "external rear view mirror position in the up and down direction at driver side"
        signal_length = 8
        start_position = 431
        value_definition = {}


class LCULToCCUSOCCDEthSignalIPdu03:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x504003
    pdu_length_bytes = 4
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-200ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'PwrContnsChLeCfgSts': ['PwrContnsChLeCfgStsContnsLeCh3CfgSts', 'PwrContnsChLeCfgStsContnsLeCh1CfgSts', 'PwrContnsChLeCfgStsContnsLeCh4CfgSts', 'PwrContnsChLeCfgStsContnsLeCh2CfgSts', 'PwrContnsChLeCfgStsContnsLeCh5CfgSts']}

    class DefrstDrvrFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 8
        signal_description = "defrosting failure of the driver side mirror"
        signal_length = 1
        start_position = 7
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class DefrstReFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 23
        signal_description = "the defrosting failure of the rear windshield "
        signal_length = 1
        start_position = 6
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class PwrContnsChLeCfgStsContnsLeCh3CfgSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "Left Zone Contns Power Channel 3 Config Status"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrContnsChLeCfgStsContnsLeCh1CfgSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "Left Zone Contns Power Channel 1 Config Status"
        signal_length = 1
        start_position = 15
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrContnsChLeCfgStsContnsLeCh4CfgSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "Left Zone Contns Power Channel 4 Config Status"
        signal_length = 1
        start_position = 14
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrContnsChLeCfgStsContnsLeCh2CfgSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "Left Zone Contns Power Channel 2 Config Status"
        signal_length = 1
        start_position = 13
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class PwrContnsChLeCfgStsContnsLeCh5CfgSts:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 20
        signal_description = "Left Zone Contns Power Channel 5 Config Status"
        signal_length = 1
        start_position = 12
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}


class LCULToCCUSOCCDEthSignalIPdu04:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x504004
    pdu_length_bytes = 64
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-20ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'SeatAdj1RowLeMotSts': ['SeatAdj1RowLeMotStsMotorStsOTTOAg', 'SeatAdj1RowLeMotStsMotorStsTilt', 'SeatAdj1RowLeMotStsMotorStsRe', 'SeatAdj1RowLeMotStsMotorStsLen', 'SeatAdj1RowLeMotStsMotorStsCLA', 'SeatAdj1RowLeMotStsMotorStsOTTOLen', 'SeatAdj1RowLeMotStsMotorStsBack', 'SeatAdj1RowLeMotStsMotorStsOTF', 'SeatAdj1RowLeMotStsMotorStsHei'], 'SeatAdj2RowLeMotSts': ['SeatAdj2RowLeMotStsMotorStsCLA', 'SeatAdj2RowLeMotStsMotorStsLen', 'SeatAdj2RowLeMotStsMotorStsRe', 'SeatAdj2RowLeMotStsMotorStsHei', 'SeatAdj2RowLeMotStsMotorStsBack', 'SeatAdj2RowLeMotStsMotorStsOTTOLen', 'SeatAdj2RowLeMotStsMotorStsTilt', 'SeatAdj2RowLeMotStsMotorStsOTF', 'SeatAdj2RowLeMotStsMotorStsOTTOAg'], 'SeatAdj3RowLeMotSts': ['SeatAdj3RowLeMotStsMotorStsOTTOLen', 'SeatAdj3RowLeMotStsMotorStsBack', 'SeatAdj3RowLeMotStsMotorStsOTTOAg', 'SeatAdj3RowLeMotStsMotorStsTilt', 'SeatAdj3RowLeMotStsMotorStsRe', 'SeatAdj3RowLeMotStsMotorStsCLA', 'SeatAdj3RowLeMotStsMotorStsOTF', 'SeatAdj3RowLeMotStsMotorStsLen', 'SeatAdj3RowLeMotStsMotorStsHei'], 'SftyBltTensionSts': ['SftyBltTensionStsTi', 'SftyBltTensionStsF'], 'SftyBltVibrationSts': ['SftyBltVibrationStsTotTi', 'SftyBltVibrationStsFrq', 'SftyBltVibrationStsRemainTi', 'SftyBltVibrationStsF'], 'SteerWhlLeMulFunButtonLe5Down': ['SteerWhlLeMulFunButtonLe5DownScButtUpDnStp', 'SteerWhlLeMulFunButtonLe5DownSteerWhlTouchSwt'], 'SteerWhlLeMulFunButtonLe5Up': ['SteerWhlLeMulFunButtonLe5UpSteerWhlTouchSwt', 'SteerWhlLeMulFunButtonLe5UpScButtUpDnStp'], 'SteerWhlRiMulFunButtonRi5Down': ['SteerWhlRiMulFunButtonRi5DownSteerWhlTouchSwt', 'SteerWhlRiMulFunButtonRi5DownScButtUpDnStp'], 'SteerWhlRiMulFunButtonRi5Le': ['SteerWhlRiMulFunButtonRi5LeCntr', 'SteerWhlRiMulFunButtonRi5LeSteerWhlTouchSwt', 'SteerWhlRiMulFunButtonRi5LeChks'], 'SteerWhlRiMulFunButtonRi5Mid': ['SteerWhlRiMulFunButtonRi5MidSteerWhlTouchSwt', 'SteerWhlRiMulFunButtonRi5MidCntr', 'SteerWhlRiMulFunButtonRi5MidChks'], 'SteerWhlRiMulFunButtonRi5Ri': ['SteerWhlRiMulFunButtonRi5RiCntr', 'SteerWhlRiMulFunButtonRi5RiSteerWhlTouchSwt', 'SteerWhlRiMulFunButtonRi5RiChks'], 'SteerWhlRiMulFunButtonRi5Up': ['SteerWhlRiMulFunButtonRi5UpSteerWhlTouchSwt', 'SteerWhlRiMulFunButtonRi5UpScButtUpDnStp'], 'SteerWhlStalkLe': ['SteerWhlStalkLeStalkButton', 'SteerWhlStalkLeStalkZone2', 'SteerWhlStalkLeStalkZone1', 'SteerWhlStalkLeChks', 'SteerWhlStalkLeCntr'], 'SteerWhlStalkRi': ['SteerWhlStalkRiChks', 'SteerWhlStalkRiStalkZone2', 'SteerWhlStalkRiCntr', 'SteerWhlStalkRiStalkZone1', 'SteerWhlStalkRiStalkButton'], 'SteerWhlTouchSwtLe1': ['SteerWhlTouchSwtLe1SteerWhlTouchSwt', 'SteerWhlTouchSwtLe1Chks', 'SteerWhlTouchSwtLe1Cntr'], 'SteerWhlTouchSwtLe2': ['SteerWhlTouchSwtLe2Chks', 'SteerWhlTouchSwtLe2SteerWhlTouchSwt', 'SteerWhlTouchSwtLe2Cntr'], 'SteerWhlTouchSwtLe3': ['SteerWhlTouchSwtLe3Chks', 'SteerWhlTouchSwtLe3SteerWhlTouchSwt', 'SteerWhlTouchSwtLe3Cntr'], 'SteerWhlTouchSwtRi1': ['SteerWhlTouchSwtRi1Cntr', 'SteerWhlTouchSwtRi1Chks', 'SteerWhlTouchSwtRi1SteerWhlTouchSwt'], 'SteerWhlTouchSwtRi2': ['SteerWhlTouchSwtRi2SteerWhlTouchSwt', 'SteerWhlTouchSwtRi2Cntr', 'SteerWhlTouchSwtRi2Chks'], 'SteerWhlTouchSwtRi3': ['SteerWhlTouchSwtRi3SteerWhlTouchSwt', 'SteerWhlTouchSwtRi3Chks', 'SteerWhlTouchSwtRi3Cntr'], 'WinDrvrBtnErrSts': ['WinDrvrBtnErrStsWinBtnErrFR', 'WinDrvrBtnErrStsWinBtnErrRR', 'WinDrvrBtnErrStsWinBtnErrRL', 'WinDrvrBtnErrStsWinBtnErrFL'], 'SteerWhlLeMulFunButtonLe5Mid': ['SteerWhlLeMulFunButtonLe5MidCntr', 'SteerWhlLeMulFunButtonLe5MidChks', 'SteerWhlLeMulFunButtonLe5MidSteerWhlTouchSwt']}

    class BeltRtrctrMotActrStsAtDrvr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 0
        signal_description = "Belt retraction motor actuator status at driver"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' BeltRtrctrMotActrSts_Invalid', '0x1': ' BeltRtrctrMotActrSts_NotActivated', '0x2': ' BeltRtrctrMotActrSts_Activating', '0x3': ' BeltRtrctrMotActrSts_Activated'}

    class BeltRtrctrStsAtDrvr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 2
        signal_description = "Belt retraction status at driver"
        signal_length = 3
        start_position = 5
        value_definition = {'0x0': ' BeltRtrctrSts_Invalid', '0x1': ' BeltRtrctrSts_NotReady', '0x2': ' BeltRtrctrSts_Ready', '0x3': ' BeltRtrctrSts_Disable', '0x4': ' BeltRtrctrSts_Error'}

    class FLDoorObstclDst:
        comments = ""
        factor = 0.5
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1
        signal_description = "Door obstacle detecting"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class RLDoorObstclDst:
        comments = ""
        factor = 0.5
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 205
        signal_description = "Door obstacle detecting"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class SeatAdj1RowLeMotStsMotorStsOTTOAg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 204
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 31
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowLeMotStsMotorStsTilt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 204
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 28
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowLeMotStsMotorStsRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 204
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 25
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowLeMotStsMotorStsLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 204
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 38
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowLeMotStsMotorStsCLA:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 204
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 35
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowLeMotStsMotorStsOTTOLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 204
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 32
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowLeMotStsMotorStsBack:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 204
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 45
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowLeMotStsMotorStsOTF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 204
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 42
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj1RowLeMotStsMotorStsHei:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 204
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 55
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowLeMotStsMotorStsCLA:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 203
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 52
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowLeMotStsMotorStsLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 203
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 49
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowLeMotStsMotorStsRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 203
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 62
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowLeMotStsMotorStsHei:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 203
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 59
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowLeMotStsMotorStsBack:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 203
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 56
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowLeMotStsMotorStsOTTOLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 203
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 69
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowLeMotStsMotorStsTilt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 203
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 66
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowLeMotStsMotorStsOTF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 203
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 79
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj2RowLeMotStsMotorStsOTTOAg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 203
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 76
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowLeMotStsMotorStsOTTOLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 202
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 73
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowLeMotStsMotorStsBack:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 202
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 86
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowLeMotStsMotorStsOTTOAg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 202
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 83
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowLeMotStsMotorStsTilt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 202
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 80
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowLeMotStsMotorStsRe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 202
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 93
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowLeMotStsMotorStsCLA:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 202
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 90
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowLeMotStsMotorStsOTF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 202
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 103
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowLeMotStsMotorStsLen:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 202
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 100
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatAdj3RowLeMotStsMotorStsHei:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 202
        signal_description = "Motr Run Status"
        signal_length = 3
        start_position = 97
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SeatLum1RowLeSwtErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 201
        signal_description = "1Row Left Lumbar Key Error Status"
        signal_length = 2
        start_position = 110
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class SeatLum1RowLeSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 200
        signal_description = "Lumbar Key Direction"
        signal_length = 3
        start_position = 108
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatLum2RowLeSwtErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 237
        signal_description = "2Row Left Lumbar Key Error Status"
        signal_length = 2
        start_position = 105
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class SeatLum2RowLeSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 236
        signal_description = "Lumbar Key Direction"
        signal_length = 3
        start_position = 119
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatLum3RowLeSwtErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 235
        signal_description = "3Row Left Lumbar Key Error Status"
        signal_length = 2
        start_position = 116
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class SeatLum3RowLeSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 234
        signal_description = "Lumbar Key Direction"
        signal_length = 3
        start_position = 114
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SftyBltTensionStsTi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 233
        signal_description = "time"
        signal_length = 16
        start_position = 127
        value_definition = {}

    class SftyBltTensionStsF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 233
        signal_description = "force"
        signal_length = 8
        start_position = 143
        value_definition = {}

    class SftyBltVibrationStsTotTi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 232
        signal_description = "total time"
        signal_length = 16
        start_position = 151
        value_definition = {}

    class SftyBltVibrationStsFrq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 232
        signal_description = "frequency"
        signal_length = 16
        start_position = 167
        value_definition = {}

    class SftyBltVibrationStsRemainTi:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 232
        signal_description = "remain time"
        signal_length = 16
        start_position = 183
        value_definition = {}

    class SftyBltVibrationStsF:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 232
        signal_description = "force"
        signal_length = 8
        start_position = 199
        value_definition = {}

    class SteerWhlLeMulFunButtonLe5DownScButtUpDnStp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 253
        signal_description = "The stp of SWTL Le5Down"
        signal_length = 8
        start_position = 215
        value_definition = {}

    class SteerWhlLeMulFunButtonLe5DownSteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 253
        signal_description = "The pressed/unpressed signal of SWTL Le5Down"
        signal_length = 2
        start_position = 223
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlLeMulFunButtonLe5Le:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 252
        signal_description = "The pressed/unpressed signal of SWTL Le5Left"
        signal_length = 2
        start_position = 207
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlLeMulFunButtonLe5Ri:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 250
        signal_description = "The pressed/unpressed signal of SWTL Le5Right"
        signal_length = 2
        start_position = 239
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlLeMulFunButtonLe5UpSteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 249
        signal_description = "The pressed/unpressed signal of SWTL Le5Up"
        signal_length = 2
        start_position = 255
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlLeMulFunButtonLe5UpScButtUpDnStp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 249
        signal_description = "The stp of SWTL Le5Up"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class SteerWhlRiMulFunButtonRi5DownSteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 248
        signal_description = "The pressed/unpressed signal of SWTR Ri5Down"
        signal_length = 2
        start_position = 271
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlRiMulFunButtonRi5DownScButtUpDnStp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 248
        signal_description = "The step signal of SWTR Ri5Down"
        signal_length = 8
        start_position = 263
        value_definition = {}

    class SteerWhlRiMulFunButtonRi5LeCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 289
        signal_description = "counter"
        signal_length = 4
        start_position = 269
        value_definition = {}

    class SteerWhlRiMulFunButtonRi5LeSteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 289
        signal_description = "The pressed/unpressed signal of SWTR multifunctional button Le"
        signal_length = 2
        start_position = 265
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlRiMulFunButtonRi5LeChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 289
        signal_description = "checksum"
        signal_length = 8
        start_position = 279
        value_definition = {}

    class SteerWhlRiMulFunButtonRi5MidSteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 288
        signal_description = "The pressed/unpressed signal of SWTR multifunctional button Push"
        signal_length = 2
        start_position = 295
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlRiMulFunButtonRi5MidCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 288
        signal_description = "counter"
        signal_length = 4
        start_position = 293
        value_definition = {}

    class SteerWhlRiMulFunButtonRi5MidChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 288
        signal_description = "checksum"
        signal_length = 8
        start_position = 287
        value_definition = {}

    class SteerWhlRiMulFunButtonRi5RiCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 305
        signal_description = "counter"
        signal_length = 4
        start_position = 309
        value_definition = {}

    class SteerWhlRiMulFunButtonRi5RiSteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 305
        signal_description = "The pressed/unpressed signal of SWTR multifunctional button Ri"
        signal_length = 2
        start_position = 311
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlRiMulFunButtonRi5RiChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 305
        signal_description = "checksum"
        signal_length = 8
        start_position = 303
        value_definition = {}

    class SteerWhlRiMulFunButtonRi5UpSteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 304
        signal_description = "The pressed/unpressed signal of SWTR Ri5Up"
        signal_length = 2
        start_position = 327
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlRiMulFunButtonRi5UpScButtUpDnStp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 304
        signal_description = "The pressed/unpressed signal of SWTR Ri5Up"
        signal_length = 8
        start_position = 319
        value_definition = {}

    class SteerWhlStalkLeStalkButton:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 325
        signal_description = "StalkButton"
        signal_length = 2
        start_position = 339
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlStalkLeStalkZone2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 325
        signal_description = "StalkZone2Position"
        signal_length = 3
        start_position = 350
        value_definition = {}

    class SteerWhlStalkLeStalkZone1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 325
        signal_description = "StalkZone1Position"
        signal_length = 3
        start_position = 337
        value_definition = {}

    class SteerWhlStalkLeChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 325
        signal_description = "Checksum"
        signal_length = 8
        start_position = 335
        value_definition = {}

    class SteerWhlStalkLeCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 325
        signal_description = "Counter"
        signal_length = 4
        start_position = 343
        value_definition = {}

    class SteerWhlStalkRiChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 324
        signal_description = "Checksum"
        signal_length = 8
        start_position = 359
        value_definition = {}

    class SteerWhlStalkRiStalkZone2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 324
        signal_description = "StalkZone2Position"
        signal_length = 3
        start_position = 367
        value_definition = {}

    class SteerWhlStalkRiCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 324
        signal_description = "Counter"
        signal_length = 4
        start_position = 364
        value_definition = {}

    class SteerWhlStalkRiStalkZone1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 324
        signal_description = "StalkZone1Position"
        signal_length = 3
        start_position = 360
        value_definition = {}

    class SteerWhlStalkRiStalkButton:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 324
        signal_description = "StalkButton"
        signal_length = 2
        start_position = 373
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlTouchSwtLe1SteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 385
        signal_description = "The pressed/unpressed signal of SWTL Le1"
        signal_length = 2
        start_position = 387
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlTouchSwtLe1Chks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 385
        signal_description = "checksum"
        signal_length = 8
        start_position = 383
        value_definition = {}

    class SteerWhlTouchSwtLe1Cntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 385
        signal_description = "counter"
        signal_length = 4
        start_position = 391
        value_definition = {}

    class SteerWhlTouchSwtLe2Chks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 401
        signal_description = "checksum"
        signal_length = 8
        start_position = 399
        value_definition = {}

    class SteerWhlTouchSwtLe2SteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 401
        signal_description = "The pressed/unpressed signal of SWTL Le2"
        signal_length = 2
        start_position = 407
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlTouchSwtLe2Cntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 401
        signal_description = "counter"
        signal_length = 4
        start_position = 405
        value_definition = {}

    class SteerWhlTouchSwtLe3Chks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 417
        signal_description = "checksum"
        signal_length = 8
        start_position = 415
        value_definition = {}

    class SteerWhlTouchSwtLe3SteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 417
        signal_description = "The pressed/unpressed signal of SWTL Le3"
        signal_length = 2
        start_position = 423
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlTouchSwtLe3Cntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 417
        signal_description = "counter"
        signal_length = 4
        start_position = 421
        value_definition = {}

    class SteerWhlTouchSwtRi1Cntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 433
        signal_description = "counter"
        signal_length = 4
        start_position = 439
        value_definition = {}

    class SteerWhlTouchSwtRi1Chks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 433
        signal_description = "checksum"
        signal_length = 8
        start_position = 431
        value_definition = {}

    class SteerWhlTouchSwtRi1SteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 433
        signal_description = "The pressed/unpressed signal of SWTL Ri1"
        signal_length = 2
        start_position = 435
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlTouchSwtRi2SteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 449
        signal_description = "The pressed/unpressed signal of SWTL Ri2"
        signal_length = 2
        start_position = 451
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlTouchSwtRi2Cntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 449
        signal_description = "counter"
        signal_length = 4
        start_position = 455
        value_definition = {}

    class SteerWhlTouchSwtRi2Chks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 449
        signal_description = "checksum"
        signal_length = 8
        start_position = 447
        value_definition = {}

    class SteerWhlTouchSwtRi3SteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 465
        signal_description = "The pressed/unpressed signal of SWTL Ri3"
        signal_length = 2
        start_position = 467
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}

    class SteerWhlTouchSwtRi3Chks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 465
        signal_description = "checksum"
        signal_length = 8
        start_position = 463
        value_definition = {}

    class SteerWhlTouchSwtRi3Cntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 465
        signal_description = "counter"
        signal_length = 4
        start_position = 471
        value_definition = {}

    class WinReLeBtnErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 478
        signal_description = "Window Button Error Status"
        signal_length = 2
        start_position = 473
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class WinReLeBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 477
        signal_description = "Window Button Status"
        signal_length = 3
        start_position = 487
        value_definition = {'0x0': ' WinBtnReq_Idle', '0x1': ' WinBtnReq_Up1', '0x2': ' WinBtnReq_Up2', '0x3': ' WinBtnReq_Dwn1', '0x4': ' WinBtnReq_Dwn2', '0x5': ' WinBtnReq_Undef', '0x6': ' WinBtnReq_Reserved1', '0x7': ' WinBtnReq_Reserved2'}

    class WinDrvrBtnErrStsWinBtnErrFR:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 251
        signal_description = "Front Right Window Button Error Status"
        signal_length = 2
        start_position = 229
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class WinDrvrBtnErrStsWinBtnErrRR:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 251
        signal_description = "Rear Right Window Button Error Status"
        signal_length = 2
        start_position = 225
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class WinDrvrBtnErrStsWinBtnErrRL:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 251
        signal_description = "Rear Left Window Button Error Status"
        signal_length = 2
        start_position = 227
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class WinDrvrBtnErrStsWinBtnErrFL:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 251
        signal_description = "Front Left Window Button Error Status"
        signal_length = 2
        start_position = 231
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class SteerWhlLeMulFunButtonLe5MidCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 497
        signal_description = "counter"
        signal_length = 4
        start_position = 503
        value_definition = {}

    class SteerWhlLeMulFunButtonLe5MidChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 497
        signal_description = "checksum"
        signal_length = 8
        start_position = 495
        value_definition = {}

    class SteerWhlLeMulFunButtonLe5MidSteerWhlTouchSwt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 497
        signal_description = "The pressed/unpressed signal of SWTL multifunctional button Push"
        signal_length = 2
        start_position = 499
        value_definition = {'0x0': ' SteerWhlTouchSwt_Inavailble', '0x1': ' SteerWhlTouchSwt_ShortPress', '0x2': ' SteerWhlTouchSwt_LongPress', '0x3': ' SteerWhlTouchSwt_Error'}


class LCULToCCUSOCCDEthSignalIPdu01:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x504001
    pdu_length_bytes = 200
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-100ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'ChargeLidErrSts': ['ChargeLidErrStsTempErr', 'ChargeLidErrStsElecErr', 'ChargeLidErrStsHallErr', 'ChargeLidErrStsVoltErr'], 'ElecVentStsFrntLeLeX': ['ElecVentStsFrntLeLeXSpdSts', 'ElecVentStsFrntLeLeXCalSts', 'ElecVentStsFrntLeLeXClrSts', 'ElecVentStsFrntLeLeXVoltErr', 'ElecVentStsFrntLeLeXRngFb', 'ElecVentStsFrntLeLeXElecErr', 'ElecVentStsFrntLeLeXRunngSts', 'ElecVentStsFrntLeLeXActPosn', 'ElecVentStsFrntLeLeXDirSts', 'ElecVentStsFrntLeLeXCalSuccessFlg', 'ElecVentStsFrntLeLeXBlkSts', 'ElecVentStsFrntLeLeXOverTemp'], 'ElecVentStsFrntLeLeY': ['ElecVentStsFrntLeLeYClrSts', 'ElecVentStsFrntLeLeYCalSuccessFlg', 'ElecVentStsFrntLeLeYOverTemp', 'ElecVentStsFrntLeLeYElecErr', 'ElecVentStsFrntLeLeYRngFb', 'ElecVentStsFrntLeLeYVoltErr', 'ElecVentStsFrntLeLeYBlkSts', 'ElecVentStsFrntLeLeYRunngSts', 'ElecVentStsFrntLeLeYDirSts', 'ElecVentStsFrntLeLeYSpdSts', 'ElecVentStsFrntLeLeYCalSts', 'ElecVentStsFrntLeLeYActPosn'], 'ElecVentStsFrntLeRiX': ['ElecVentStsFrntLeRiXElecErr', 'ElecVentStsFrntLeRiXRngFb', 'ElecVentStsFrntLeRiXBlkSts', 'ElecVentStsFrntLeRiXCalSuccessFlg', 'ElecVentStsFrntLeRiXActPosn', 'ElecVentStsFrntLeRiXClrSts', 'ElecVentStsFrntLeRiXVoltErr', 'ElecVentStsFrntLeRiXRunngSts', 'ElecVentStsFrntLeRiXOverTemp', 'ElecVentStsFrntLeRiXCalSts', 'ElecVentStsFrntLeRiXDirSts', 'ElecVentStsFrntLeRiXSpdSts'], 'ElecVentStsFrntLeRiY': ['ElecVentStsFrntLeRiYBlkSts', 'ElecVentStsFrntLeRiYActPosn', 'ElecVentStsFrntLeRiYRngFb', 'ElecVentStsFrntLeRiYOverTemp', 'ElecVentStsFrntLeRiYDirSts', 'ElecVentStsFrntLeRiYCalSts', 'ElecVentStsFrntLeRiYClrSts', 'ElecVentStsFrntLeRiYVoltErr', 'ElecVentStsFrntLeRiYElecErr', 'ElecVentStsFrntLeRiYSpdSts', 'ElecVentStsFrntLeRiYRunngSts', 'ElecVentStsFrntLeRiYCalSuccessFlg'], 'ElecVentStsReLeX': ['ElecVentStsReLeXActPosn', 'ElecVentStsReLeXRngFb', 'ElecVentStsReLeXOverTemp', 'ElecVentStsReLeXRunngSts', 'ElecVentStsReLeXSpdSts', 'ElecVentStsReLeXDirSts', 'ElecVentStsReLeXCalSts', 'ElecVentStsReLeXVoltErr', 'ElecVentStsReLeXCalSuccessFlg', 'ElecVentStsReLeXClrSts', 'ElecVentStsReLeXBlkSts', 'ElecVentStsReLeXElecErr'], 'ElecVentStsReLeY': ['ElecVentStsReLeYElecErr', 'ElecVentStsReLeYVoltErr', 'ElecVentStsReLeYOverTemp', 'ElecVentStsReLeYSpdSts', 'ElecVentStsReLeYDirSts', 'ElecVentStsReLeYCalSts', 'ElecVentStsReLeYBlkSts', 'ElecVentStsReLeYRunngSts', 'ElecVentStsReLeYActPosn', 'ElecVentStsReLeYClrSts', 'ElecVentStsReLeYRngFb', 'ElecVentStsReLeYCalSuccessFlg'], 'ExtrReViewMirrFailrDrvr': ['ExtrReViewMirrFailrDrvrAdjXMotFailr', 'ExtrReViewMirrFailrDrvrFoldMotFailr', 'ExtrReViewMirrFailrDrvrAdjYMotFailr'], 'FrntSunroofCurtFailrFb': ['FrntSunroofCurtFailrFbMotShoCirc', 'FrntSunroofCurtFailrFbLoVolt', 'FrntSunroofCurtFailrFbMotOpenCirc', 'FrntSunroofCurtFailrFbOverTmp', 'FrntSunroofCurtFailrFbHallSnsrFailr', 'FrntSunroofCurtFailrFbHiVolt'], 'ModFlapStsBoost': ['ModFlapStsBoostRunngSts', 'ModFlapStsBoostVoltErr', 'ModFlapStsBoostClrSts', 'ModFlapStsBoostBlkSts', 'ModFlapStsBoostOverTemp', 'ModFlapStsBoostActPosn', 'ModFlapStsBoostCalSts', 'ModFlapStsBoostURng', 'ModFlapStsBoostElecErr', 'ModFlapStsBoostDirSts'], 'ModFlapStsFrntLe': ['ModFlapStsFrntLeRunngSts', 'ModFlapStsFrntLeBlkSts', 'ModFlapStsFrntLeVoltErr', 'ModFlapStsFrntLeCalSts', 'ModFlapStsFrntLeOverTemp', 'ModFlapStsFrntLeDirSts', 'ModFlapStsFrntLeURng', 'ModFlapStsFrntLeElecErr', 'ModFlapStsFrntLeActPosn', 'ModFlapStsFrntLeClrSts'], 'ModFlapStsReLe': ['ModFlapStsReLeClrSts', 'ModFlapStsReLeVoltErr', 'ModFlapStsReLeOverTemp', 'ModFlapStsReLeURng', 'ModFlapStsReLeActPosn', 'ModFlapStsReLeRunngSts', 'ModFlapStsReLeDirSts', 'ModFlapStsReLeCalSts', 'ModFlapStsReLeElecErr', 'ModFlapStsReLeBlkSts'], 'OutdBri': ['OutdBriCntr', 'OutdBriChks', 'OutdBriSts'], 'RefrigorAvlSts': ['RefrigorAvlStsEcoSts', 'RefrigorAvlStsChmbT', 'RefrigorAvlStsCmprSpd', 'RefrigorAvlStsSysSts', 'RefrigorAvlStsDoorSts', 'RefrigorAvlStsCoolgAbortRsn', 'RefrigorAvlStsLiSts', 'RefrigorAvlStsHeatgAbortRsn', 'RefrigorAvlStsActPwr', 'RefrigorAvlStsRunngSts'], 'ReSunroofCurtFailrFb': ['ReSunroofCurtFailrFbOverTmp', 'ReSunroofCurtFailrFbLoVolt', 'ReSunroofCurtFailrFbMotOpenCirc', 'ReSunroofCurtFailrFbMotShoCirc', 'ReSunroofCurtFailrFbHallSnsrFailr', 'ReSunroofCurtFailrFbHiVolt'], 'SeatAdj1RowLeStopCase': ['SeatAdj1RowLeStopCaseMotorStopCase', 'SeatAdj1RowLeStopCaseSeatCfg'], 'SeatAdj2RowLeStopCase': ['SeatAdj2RowLeStopCaseSeatCfg', 'SeatAdj2RowLeStopCaseMotorStopCase'], 'SeatAdj3RowLeStopCase': ['SeatAdj3RowLeStopCaseMotorStopCase', 'SeatAdj3RowLeStopCaseSeatCfg'], 'SeatClima1RowLeSts': ['SeatClima1RowLeStsHeatgActPwr', 'SeatClima1RowLeStsVentAvlSts', 'SeatClima1RowLeStsTEstimd', 'SeatClima1RowLeStsVentActPwr', 'SeatClima1RowLeStsHeatgAvlSts'], 'SeatClima2RowLeSts': ['SeatClima2RowLeStsVentActPwr', 'SeatClima2RowLeStsTEstimd', 'SeatClima2RowLeStsVentAvlSts', 'SeatClima2RowLeStsHeatgAvlSts', 'SeatClima2RowLeStsHeatgActPwr'], 'SeatClima3RowLeSts': ['SeatClima3RowLeStsVentActPwr', 'SeatClima3RowLeStsHeatgActPwr', 'SeatClima3RowLeStsTEstimd', 'SeatClima3RowLeStsHeatgAvlSts', 'SeatClima3RowLeStsVentAvlSts'], 'SeatClimaLeHeatgBtnSts': ['SeatClimaLeHeatgBtnStsRow1', 'SeatClimaLeHeatgBtnStsRow3', 'SeatClimaLeHeatgBtnStsRow2'], 'SteerWhlHeatgSts': ['SteerWhlHeatgStsAvlSts', 'SteerWhlHeatgStsActPwr', 'SteerWhlHeatgStsTEstimd'], 'TempFlapStsFrntLe': ['TempFlapStsFrntLeElecErr', 'TempFlapStsFrntLeVoltErr', 'TempFlapStsFrntLeActPosn', 'TempFlapStsFrntLeDirSts', 'TempFlapStsFrntLeRunngSts', 'TempFlapStsFrntLeCalSts', 'TempFlapStsFrntLeBlkSts', 'TempFlapStsFrntLeClrSts', 'TempFlapStsFrntLeOverTemp', 'TempFlapStsFrntLeURng'], 'TempFlapStsReLe': ['TempFlapStsReLeClrSts', 'TempFlapStsReLeURng', 'TempFlapStsReLeCalSts', 'TempFlapStsReLeRunngSts', 'TempFlapStsReLeOverTemp', 'TempFlapStsReLeElecErr', 'TempFlapStsReLeVoltErr', 'TempFlapStsReLeDirSts', 'TempFlapStsReLeBlkSts', 'TempFlapStsReLeActPosn'], 'TowBarHallSnsrFlt': ['TowBarHallSnsrFltHallAFlt', 'TowBarHallSnsrFltHallOutpFlt', 'TowBarHallSnsrFltHallBFlt'], 'TowBarMotFlt': ['TowBarMotFltMotOverCurrent', 'TowBarMotFltMotShoCircGND', 'TowBarMotFltTmrFlt', 'TowBarMotFltMotShoCircBatt', 'TowBarMotFltMotOpenCirc'], 'VentAirTEstimdFrntLe': ['VentAirTEstimdFrntLeFootT', 'VentAirTEstimdFrntLeFaceT', 'VentAirTEstimdFrntLeFaceTQf', 'VentAirTEstimdFrntLeFootTQf'], 'SunHumSnsrErr': ['SunHumSnsrErrSolarSnsr', 'SunHumSnsrErrRelHumSnsr'], 'VentAirTEstimdReLe': ['VentAirTEstimdReLeFootTQf', 'VentAirTEstimdReLeFootT', 'VentAirTEstimdReLeFaceTQf', 'VentAirTEstimdReLeFaceT'], 'SunHumEstimd': ['SunHumEstimdSolarIntenLeQf', 'SunHumEstimdSolarIntenRiQf', 'SunHumEstimdFrntWindRelHum', 'SunHumEstimdFrntWindT', 'SunHumEstimdFrntWindDewT', 'SunHumEstimdFrntWindRelHumQf', 'SunHumEstimdFrntWindDewTQf', 'SunHumEstimdSolarIntenLe', 'SunHumEstimdSolarIntenRi', 'SunHumEstimdFrntWindTQf'], 'WshrMotFailr': ['WshrMotFailrOpenCirc', 'WshrMotFailrShoCircToBatt', 'WshrMotFailrShoCircToGND'], 'ActvReSplrSts': ['ActvReSplrStsAvlStsForConLockg', 'ActvReSplrStsCtrldSts2', 'ActvReSplrStsNotAvlEve', 'ActvReSplrStsAvlStsForCDC']}

    class ActvdStsPNG1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 85
        signal_description = "Activated status of PNG"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}

    class ADCamDefrostSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 84
        signal_description = "AD Camera Defrost status"
        signal_length = 2
        start_position = 5
        value_definition = {'0x0': ' ADCamDefrostSts_Off', '0x1': ' ADCamDefrostSts_On', '0x2': ' ADCamDefrostSts_Fault'}

    class AutWinWipgCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 83
        signal_description = "Auto Wiper Speed"
        signal_length = 3
        start_position = 3
        value_definition = {'0x0': ' WipgSpd_WipgSpd0Rpm', '0x1': ' WipgSpd_WipgSpd40Rpm', '0x2': ' WipgSpd_WipgSpd43Rpm', '0x3': ' WipgSpd_WipgSpd46Rpm', '0x4': ' WipgSpd_WipgSpd50Rpm', '0x5': ' WipgSpd_WipgSpd54Rpm', '0x6': ' WipgSpd_WipgSpd57Rpm', '0x7': ' WipgSpd_WipgSpd60Rpm'}

    class ChargeLidErrStsTempErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 82
        signal_description = "charge lid over temperature error"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ChargeLidErrStsElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 82
        signal_description = "charge lid electric error"
        signal_length = 1
        start_position = 15
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ChargeLidErrStsHallErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 82
        signal_description = "charge lid stuck error"
        signal_length = 1
        start_position = 14
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class ChargeLidErrStsVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 82
        signal_description = "charge lid over voltage error"
        signal_length = 1
        start_position = 13
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class CmptFrntWindDewT:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 80
        signal_description = "Compartment Front Windscreen Dew Point Temperature"
        signal_length = 11
        start_position = 12
        value_definition = {}

    class CmptFrntWindT:
        comments = ""
        factor = 0.1
        initial_value = 650
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 81
        signal_description = "Compartment Front Windscreen Temperature"
        signal_length = 11
        start_position = 17
        value_definition = {}

    class DefrstDrvrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 95
        signal_description = "defrosting state of the driver side mirror"
        signal_length = 2
        start_position = 38
        value_definition = {'0x0': ' OffOnTmroff_Off', '0x1': ' OffOnTmroff_On', '0x2': ' OffOnTmroff_TmrOff'}

    class DefrstReSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 94
        signal_description = "defrosting state of the rear windshield"
        signal_length = 2
        start_position = 36
        value_definition = {'0x0': ' OffOnTmroff_Off', '0x1': ' OffOnTmroff_On', '0x2': ' OffOnTmroff_TmrOff'}

    class ElecVentStsFrntLeLeXSpdSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Speed Status"
        signal_length = 3
        start_position = 34
        value_definition = {'0x0': ' VentActrSpdSts_Stop', '0x1': ' VentActrSpdSts_Level1', '0x2': ' VentActrSpdSts_Level2', '0x3': ' VentActrSpdSts_Level3', '0x4': ' VentActrSpdSts_Level4', '0x5': ' VentActrSpdSts_Auto', '0x6': ' VentActrSpdSts_Reserved1', '0x7': ' VentActrSpdSts_Reserved2'}

    class ElecVentStsFrntLeLeXCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Calibration Status"
        signal_length = 2
        start_position = 47
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ElecVentStsFrntLeLeXClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Clear Block Status"
        signal_length = 2
        start_position = 45
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ElecVentStsFrntLeLeXVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Voltage Error"
        signal_length = 2
        start_position = 43
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ElecVentStsFrntLeLeXRngFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Working Range Feedback"
        signal_length = 10
        start_position = 41
        value_definition = {}

    class ElecVentStsFrntLeLeXElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Electrical Error"
        signal_length = 2
        start_position = 63
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ElecVentStsFrntLeLeXRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Running Status"
        signal_length = 2
        start_position = 61
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ElecVentStsFrntLeLeXActPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Actual Position"
        signal_length = 16
        start_position = 71
        value_definition = {}

    class ElecVentStsFrntLeLeXDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Running Direction"
        signal_length = 2
        start_position = 57
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ElecVentStsFrntLeLeXCalSuccessFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Calibration Success Flag"
        signal_length = 1
        start_position = 87
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class ElecVentStsFrntLeLeXBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Block Status"
        signal_length = 2
        start_position = 59
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ElecVentStsFrntLeLeXOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 93
        signal_description = "Vent Grill Motor 1 Over Temperature"
        signal_length = 1
        start_position = 86
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ElecVentStsFrntLeLeYClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Clear Block Status"
        signal_length = 2
        start_position = 116
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ElecVentStsFrntLeLeYCalSuccessFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Calibration Success Flag"
        signal_length = 1
        start_position = 114
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class ElecVentStsFrntLeLeYOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Over Temperature"
        signal_length = 1
        start_position = 92
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ElecVentStsFrntLeLeYElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Electrical Error"
        signal_length = 2
        start_position = 113
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ElecVentStsFrntLeLeYRngFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Working Range Feedback"
        signal_length = 10
        start_position = 91
        value_definition = {}

    class ElecVentStsFrntLeLeYVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Voltage Error"
        signal_length = 2
        start_position = 97
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ElecVentStsFrntLeLeYBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Block Status"
        signal_length = 2
        start_position = 111
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ElecVentStsFrntLeLeYRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Running Status"
        signal_length = 2
        start_position = 109
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ElecVentStsFrntLeLeYDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Running Direction"
        signal_length = 2
        start_position = 107
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ElecVentStsFrntLeLeYSpdSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Speed Status"
        signal_length = 3
        start_position = 105
        value_definition = {'0x0': ' VentActrSpdSts_Stop', '0x1': ' VentActrSpdSts_Level1', '0x2': ' VentActrSpdSts_Level2', '0x3': ' VentActrSpdSts_Level3', '0x4': ' VentActrSpdSts_Level4', '0x5': ' VentActrSpdSts_Auto', '0x6': ' VentActrSpdSts_Reserved1', '0x7': ' VentActrSpdSts_Reserved2'}

    class ElecVentStsFrntLeLeYCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Calibration Status"
        signal_length = 2
        start_position = 118
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ElecVentStsFrntLeLeYActPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 228
        signal_description = "Vent Grill Motor 2 Actual Position"
        signal_length = 16
        start_position = 127
        value_definition = {}

    class ElecVentStsFrntLeRiXElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Electrical Error"
        signal_length = 2
        start_position = 143
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ElecVentStsFrntLeRiXRngFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Working Range Feedback"
        signal_length = 10
        start_position = 141
        value_definition = {}

    class ElecVentStsFrntLeRiXBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Block Status"
        signal_length = 2
        start_position = 147
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ElecVentStsFrntLeRiXCalSuccessFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Calibration Success Flag"
        signal_length = 1
        start_position = 145
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class ElecVentStsFrntLeRiXActPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Actual Position"
        signal_length = 16
        start_position = 159
        value_definition = {}

    class ElecVentStsFrntLeRiXClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Clear Block Status"
        signal_length = 2
        start_position = 175
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ElecVentStsFrntLeRiXVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Voltage Error"
        signal_length = 2
        start_position = 173
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ElecVentStsFrntLeRiXRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Running Status"
        signal_length = 2
        start_position = 171
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ElecVentStsFrntLeRiXOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Over Temperature"
        signal_length = 1
        start_position = 169
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ElecVentStsFrntLeRiXCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Calibration Status"
        signal_length = 2
        start_position = 168
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ElecVentStsFrntLeRiXDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Running Direction"
        signal_length = 2
        start_position = 182
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ElecVentStsFrntLeRiXSpdSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 227
        signal_description = "Vent Grill Motor 3 Speed Status"
        signal_length = 3
        start_position = 180
        value_definition = {'0x0': ' VentActrSpdSts_Stop', '0x1': ' VentActrSpdSts_Level1', '0x2': ' VentActrSpdSts_Level2', '0x3': ' VentActrSpdSts_Level3', '0x4': ' VentActrSpdSts_Level4', '0x5': ' VentActrSpdSts_Auto', '0x6': ' VentActrSpdSts_Reserved1', '0x7': ' VentActrSpdSts_Reserved2'}

    class ElecVentStsFrntLeRiYBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Block Status"
        signal_length = 2
        start_position = 177
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ElecVentStsFrntLeRiYActPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Actual Position"
        signal_length = 16
        start_position = 191
        value_definition = {}

    class ElecVentStsFrntLeRiYRngFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Working Range Feedback"
        signal_length = 10
        start_position = 207
        value_definition = {}

    class ElecVentStsFrntLeRiYOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Over Temperature"
        signal_length = 1
        start_position = 213
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ElecVentStsFrntLeRiYDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Running Direction"
        signal_length = 2
        start_position = 212
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ElecVentStsFrntLeRiYCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Calibration Status"
        signal_length = 2
        start_position = 210
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ElecVentStsFrntLeRiYClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Clear Block Status"
        signal_length = 2
        start_position = 208
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ElecVentStsFrntLeRiYVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Voltage Error"
        signal_length = 2
        start_position = 222
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ElecVentStsFrntLeRiYElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Electrical Error"
        signal_length = 2
        start_position = 220
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ElecVentStsFrntLeRiYSpdSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Speed Status"
        signal_length = 3
        start_position = 218
        value_definition = {'0x0': ' VentActrSpdSts_Stop', '0x1': ' VentActrSpdSts_Level1', '0x2': ' VentActrSpdSts_Level2', '0x3': ' VentActrSpdSts_Level3', '0x4': ' VentActrSpdSts_Level4', '0x5': ' VentActrSpdSts_Auto', '0x6': ' VentActrSpdSts_Reserved1', '0x7': ' VentActrSpdSts_Reserved2'}

    class ElecVentStsFrntLeRiYRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Running Status"
        signal_length = 2
        start_position = 231
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ElecVentStsFrntLeRiYCalSuccessFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 226
        signal_description = "Vent Grill Motor 4 Calibration Success Flag"
        signal_length = 1
        start_position = 229
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class ElecVentStsReLeXActPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Actual Position"
        signal_length = 16
        start_position = 239
        value_definition = {}

    class ElecVentStsReLeXRngFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Working Range Feedback"
        signal_length = 10
        start_position = 255
        value_definition = {}

    class ElecVentStsReLeXOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Over Temperature"
        signal_length = 1
        start_position = 261
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ElecVentStsReLeXRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Running Status"
        signal_length = 2
        start_position = 260
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ElecVentStsReLeXSpdSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Speed Status"
        signal_length = 3
        start_position = 258
        value_definition = {'0x0': ' VentActrSpdSts_Stop', '0x1': ' VentActrSpdSts_Level1', '0x2': ' VentActrSpdSts_Level2', '0x3': ' VentActrSpdSts_Level3', '0x4': ' VentActrSpdSts_Level4', '0x5': ' VentActrSpdSts_Auto', '0x6': ' VentActrSpdSts_Reserved1', '0x7': ' VentActrSpdSts_Reserved2'}

    class ElecVentStsReLeXDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Running Direction"
        signal_length = 2
        start_position = 271
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ElecVentStsReLeXCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Calibration Status"
        signal_length = 2
        start_position = 269
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ElecVentStsReLeXVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Voltage Error"
        signal_length = 2
        start_position = 267
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ElecVentStsReLeXCalSuccessFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Calibration Success Flag"
        signal_length = 1
        start_position = 265
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class ElecVentStsReLeXClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Clear Block Status"
        signal_length = 2
        start_position = 264
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ElecVentStsReLeXBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Block Status"
        signal_length = 2
        start_position = 278
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ElecVentStsReLeXElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 225
        signal_description = "Vent Grill Motor 9 Electrical Error"
        signal_length = 2
        start_position = 276
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ElecVentStsReLeYElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Electrical Error"
        signal_length = 2
        start_position = 287
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ElecVentStsReLeYVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Voltage Error"
        signal_length = 2
        start_position = 284
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ElecVentStsReLeYOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Over Temperature"
        signal_length = 1
        start_position = 285
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ElecVentStsReLeYSpdSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Speed Status"
        signal_length = 3
        start_position = 290
        value_definition = {'0x0': ' VentActrSpdSts_Stop', '0x1': ' VentActrSpdSts_Level1', '0x2': ' VentActrSpdSts_Level2', '0x3': ' VentActrSpdSts_Level3', '0x4': ' VentActrSpdSts_Level4', '0x5': ' VentActrSpdSts_Auto', '0x6': ' VentActrSpdSts_Reserved1', '0x7': ' VentActrSpdSts_Reserved2'}

    class ElecVentStsReLeYDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Running Direction"
        signal_length = 2
        start_position = 282
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ElecVentStsReLeYCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Calibration Status"
        signal_length = 2
        start_position = 280
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ElecVentStsReLeYBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Block Status"
        signal_length = 2
        start_position = 294
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ElecVentStsReLeYRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Running Status"
        signal_length = 2
        start_position = 292
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ElecVentStsReLeYActPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Actual Position"
        signal_length = 16
        start_position = 303
        value_definition = {}

    class ElecVentStsReLeYClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Clear Block Status"
        signal_length = 2
        start_position = 319
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ElecVentStsReLeYRngFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Working Range Feedback"
        signal_length = 10
        start_position = 317
        value_definition = {}

    class ElecVentStsReLeYCalSuccessFlg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 224
        signal_description = "Vent Grill Motor 10 Calibration Success Flag"
        signal_length = 1
        start_position = 323
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class ErrStsPNG1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 274
        signal_description = "Error status"
        signal_length = 4
        start_position = 322
        value_definition = {'0x0': ' ErrStsPNG_Invalid', '0x1': ' ErrStsPNG_NoErr', '0x2': ' ErrStsPNG_OverVolt', '0x3': ' ErrStsPNG_LowVolt', '0x4': ' ErrStsPNG_OverT', '0x5': ' ErrStsPNG_HSHT', '0x6': ' ErrStsPNG_Others', '0x7': ' ErrStsPNG_Reserved2', '0x8': ' ErrStsPNG_Reserved3', '0x9': ' ErrStsPNG_Reserved4', '0xA': ' ErrStsPNG_Reserved5', '0xB': ' ErrStsPNG_Reserved6', '0xC': ' ErrStsPNG_Reserved7', '0xD': ' ErrStsPNG_Reserved8', '0xE': ' ErrStsPNG_Reserved9', '0xF': ' ErrStsPNG_Reserved10'}

    class ExtrReViewMirrFailrDrvrAdjXMotFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 273
        signal_description = "the adjusting motor failure in the X direction of external rear view mirror at driver side"
        signal_length = 1
        start_position = 334
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ExtrReViewMirrFailrDrvrFoldMotFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 273
        signal_description = "the folding motor failure of external rear view mirror at driver side"
        signal_length = 1
        start_position = 333
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class ExtrReViewMirrFailrDrvrAdjYMotFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 273
        signal_description = "the adjusting motor failure in the Y direction of external rear view mirror at driver side"
        signal_length = 1
        start_position = 332
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class FLDoorManResistSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 272
        signal_description = "Door manual resistance status"
        signal_length = 2
        start_position = 331
        value_definition = {'0x0': ' DoorManResistsSts_NoResist', '0x1': ' DoorManResistsSts_Level1', '0x2': ' DoorManResistsSts_Level2'}

    class FLDoorModSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 569
        signal_description = "power side door mode status"
        signal_length = 2
        start_position = 329
        value_definition = {'0x0': ' DoorModSts_ElecMode', '0x1': ' DoorModSts_ManualMode'}

    class FrntSunroofCurtFailrFbMotShoCirc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 568
        signal_description = "short circuit of  the front sunroof curt motor"
        signal_length = 1
        start_position = 343
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class FrntSunroofCurtFailrFbLoVolt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 568
        signal_description = "low voltage failure of  the front sunroof curt module"
        signal_length = 1
        start_position = 342
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class FrntSunroofCurtFailrFbMotOpenCirc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 568
        signal_description = "open circuit of   the front sunroof curt motor"
        signal_length = 1
        start_position = 341
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class FrntSunroofCurtFailrFbOverTmp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 568
        signal_description = "over temperature failure of  the front sunroof curt motor"
        signal_length = 1
        start_position = 340
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class FrntSunroofCurtFailrFbHallSnsrFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 568
        signal_description = "hall sensor failure of  the front sunroof curt motor"
        signal_length = 1
        start_position = 339
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class FrntSunroofCurtFailrFbHiVolt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 568
        signal_description = "high voltage failure of the front sunroof curt motor"
        signal_length = 1
        start_position = 338
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class FrntSunroofCurtImpactFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 583
        signal_description = "the impact fedback of the front sunroof curt"
        signal_length = 3
        start_position = 337
        value_definition = {'0x0': ' PinchAndBlkFb_Idle', '0x1': ' PinchAndBlkFb_ClsPinch', '0x2': ' PinchAndBlkFb_ClsBlk', '0x3': ' PinchAndBlkFb_OpenPinch', '0x4': ' PinchAndBlkFb_OpenBlk'}

    class FrntSunroofCurtlrnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 582
        signal_description = "the learn state of the front sunroof curt motor"
        signal_length = 2
        start_position = 350
        value_definition = {'0x0': ' LrnSts_Idle', '0x1': ' LrnSts_lrnOk', '0x2': ' LrnSts_lrnInProgs', '0x3': ' LrnSts_lrnFail'}

    class FrntSunroofCurtMvngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 613
        signal_description = "the motion state of the front sunroof curt motor"
        signal_length = 2
        start_position = 348
        value_definition = {'0x0': ' MoveSts_Idle', '0x1': ' MoveSts_Stop', '0x2': ' MoveSts_Opening', '0x3': ' MoveSts_Closing'}

    class FrntSunroofCurtPosnPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 612
        signal_description = "the position requestion of the front sunroof curt"
        signal_length = 5
        start_position = 346
        value_definition = {'0x0': ' PosnPerc_Idle', '0x1': ' PosnPerc_PosnPercUnknow', '0x2': ' PosnPerc_PosnPercFullCls', '0x3': ' PosnPerc_PosnPerc4', '0x4': ' PosnPerc_PosnPerc8', '0x5': ' PosnPerc_PosnPerc12', '0x6': ' PosnPerc_PosnPerc16', '0x7': ' PosnPerc_PosnPerc20', '0x8': ' PosnPerc_PosnPerc24', '0x9': ' PosnPerc_PosnPerc28', '0xA': ' PosnPerc_PosnPerc32', '0xB': ' PosnPerc_PosnPerc36', '0xC': ' PosnPerc_PosnPerc40', '0xD': ' PosnPerc_PosnPerc44', '0xE': ' PosnPerc_PosnPerc48', '0xF': ' PosnPerc_PosnPerc52', '0x10': ' PosnPerc_PosnPerc56', '0x11': ' PosnPerc_PosnPerc60', '0x12': ' PosnPerc_PosnPerc64', '0x13': ' PosnPerc_PosnPerc68', '0x14': ' PosnPerc_PosnPerc72', '0x15': ' PosnPerc_PosnPerc76', '0x16': ' PosnPerc_PosnPerc80', '0x17': ' PosnPerc_PosnPerc84', '0x18': ' PosnPerc_PosnPerc88', '0x19': ' PosnPerc_PosnPerc92', '0x1A': ' PosnPerc_PosnPerc96', '0x1B': ' PosnPerc_FullOpen', '0x1C': ' PosnPerc_Reserved1', '0x1D': ' PosnPerc_Reserved2', '0x1E': ' PosnPerc_Reserved3'}

    class HeatrCooltPmpActrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 611
        signal_description = "pump actuator status"
        signal_length = 3
        start_position = 357
        value_definition = {'0x0': ' PmpActrSts_NoErr', '0x1': ' PmpActrSts_OverVoltage', '0x2': ' PmpActrSts_UnderVoltage', '0x3': ' PmpActrSts_OverTemperature', '0x4': ' PmpActrSts_OverCurrent', '0x5': ' PmpActrSts_Stall', '0x6': ' PmpActrSts_DryRun', '0x7': ' PmpActrSts_OverLoad'}

    class HeatrCooltPmpCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 610
        signal_description = "HVCH Coolant Pump Command"
        signal_length = 10
        start_position = 354
        value_definition = {}

    class HVBattCooltPmpActrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 609
        signal_description = "pump actuator status"
        signal_length = 3
        start_position = 360
        value_definition = {'0x0': ' PmpActrSts_NoErr', '0x1': ' PmpActrSts_OverVoltage', '0x2': ' PmpActrSts_UnderVoltage', '0x3': ' PmpActrSts_OverTemperature', '0x4': ' PmpActrSts_OverCurrent', '0x5': ' PmpActrSts_Stall', '0x6': ' PmpActrSts_DryRun', '0x7': ' PmpActrSts_OverLoad'}

    class HVBattCooltPmpCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 608
        signal_description = "HVBatt Coolant Pump Command"
        signal_length = 10
        start_position = 373
        value_definition = {}

    class IRawLCU1:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 652
        signal_description = "Current"
        signal_length = 13
        start_position = 378
        value_definition = {}

    class IRawPNG1KL30A:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 651
        signal_description = "Current"
        signal_length = 13
        start_position = 397
        value_definition = {}

    class IRawPNG1KL30B:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 650
        signal_description = ""
        signal_length = 13
        start_position = 400
        value_definition = {}

    class IRawRML:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 649
        signal_description = "Current"
        signal_length = 13
        start_position = 419
        value_definition = {}

    class IRawWMM:
        comments = ""
        factor = 0.1
        initial_value = 4000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -400
        sig_ub = 648
        signal_description = "Current"
        signal_length = 13
        start_position = 438
        value_definition = {}

    class LeMotCirFLtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 709
        signal_description = "The Left Speaker Motor Circult Status"
        signal_length = 3
        start_position = 441
        value_definition = {'0x0': ' AudioChCirSts_Normal', '0x1': ' AudioChCirSts_CircuitOpen', '0x2': ' AudioChCirSts_CircuitShortToBattery', '0x3': ' AudioChCirSts_CircuitShortToGND', '0x4': ' AudioChCirSts_CircuitReversedWireConnection', '0x5': ' AudioChCirSts_CircuitReserved1', '0x6': ' AudioChCirSts_CircuitReserved2', '0x7': ' AudioChCirSts_CircuitReserved3'}

    class LeSpkrMovgSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 708
        signal_description = "The Left Speaker Motor Elevating Status"
        signal_length = 3
        start_position = 454
        value_definition = {'0x0': ' SpkMoviSts_FallingTotheButtom', '0x1': ' SpkMoviSts_Rising', '0x2': ' SpkMoviSts_RisingToTop', '0x3': ' SpkMoviSts_Falling', '0x4': ' SpkMoviSts_Stopping', '0x5': ' SpkMoviSts_Unkown', '0x6': ' SpkMoviSts_Reserved1', '0x7': ' SpkMoviSts_Reserved2'}

    class ModFlapActModFrntLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 707
        signal_description = "Compartment Front Left Area Air Distribution Flap Actual Mode"
        signal_length = 3
        start_position = 451
        value_definition = {'0x0': ' ModFlapMod_Face', '0x1': ' ModFlapMod_Foot', '0x2': ' ModFlapMod_Defroster', '0x3': ' ModFlapMod_Face_Foot', '0x4': ' ModFlapMod_Face_Defroster', '0x5': ' ModFlapMod_Foot_Defroster', '0x6': ' ModFlapMod_Face_Foot_Defroster', '0x7': ' ModFlapMod_Auto'}

    class ModFlapActModReLe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 706
        signal_description = "Compartment Rear Left Area Air Distribution Flap Actual Mode"
        signal_length = 3
        start_position = 448
        value_definition = {'0x0': ' ModFlapMod_Face', '0x1': ' ModFlapMod_Foot', '0x2': ' ModFlapMod_Defroster', '0x3': ' ModFlapMod_Face_Foot', '0x4': ' ModFlapMod_Face_Defroster', '0x5': ' ModFlapMod_Foot_Defroster', '0x6': ' ModFlapMod_Face_Foot_Defroster', '0x7': ' ModFlapMod_Auto'}

    class ModFlapStsBoostRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 705
        signal_description = "Compartment Booster Air Distribution Flap Running Status"
        signal_length = 2
        start_position = 461
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ModFlapStsBoostVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 705
        signal_description = "Compartment Booster Air Distribution Flap Voltage Error"
        signal_length = 2
        start_position = 459
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ModFlapStsBoostClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 705
        signal_description = "Compartment Booster Air Distribution Flap Clear Block Status"
        signal_length = 2
        start_position = 457
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ModFlapStsBoostBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 705
        signal_description = "Compartment Booster Air Distribution Flap Block Status"
        signal_length = 2
        start_position = 471
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ModFlapStsBoostOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 705
        signal_description = "Compartment Booster Air Distribution Flap Over Temperature"
        signal_length = 1
        start_position = 469
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ModFlapStsBoostActPosn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 705
        signal_description = "Compartment Booster Air Distribution Flap Actual Position"
        signal_length = 10
        start_position = 468
        value_definition = {}

    class ModFlapStsBoostCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 705
        signal_description = "Compartment Booster Air Distribution Flap Calibration Status"
        signal_length = 2
        start_position = 474
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ModFlapStsBoostURng:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 705
        signal_description = "Compartment Booster Air Distribution Flap Self-Learning Voltage Range"
        signal_length = 9
        start_position = 472
        value_definition = {}

    class ModFlapStsBoostElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 705
        signal_description = "Compartment Booster Air Distribution Flap Electrical Error"
        signal_length = 2
        start_position = 495
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ModFlapStsBoostDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 705
        signal_description = "Compartment Booster Air Distribution Flap Running Direction"
        signal_length = 2
        start_position = 493
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ModFlapStsFrntLeRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 704
        signal_description = "Compartment Front Left Area Air Distribution Flap Running Status"
        signal_length = 2
        start_position = 491
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ModFlapStsFrntLeBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 704
        signal_description = "Compartment Front Left Area Air Distribution Flap Block Status"
        signal_length = 2
        start_position = 489
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class ModFlapStsFrntLeVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 704
        signal_description = "Compartment Front Left Area Air Distribution Flap Voltage Error"
        signal_length = 2
        start_position = 503
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ModFlapStsFrntLeCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 704
        signal_description = "Compartment Front Left Area Air Distribution Flap Calibration Status"
        signal_length = 2
        start_position = 501
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ModFlapStsFrntLeOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 704
        signal_description = "Compartment Front Left Area Air Distribution Flap Over Temperature"
        signal_length = 1
        start_position = 499
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ModFlapStsFrntLeDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 704
        signal_description = "Compartment Front Left Area Air Distribution Flap Running Direction"
        signal_length = 2
        start_position = 498
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ModFlapStsFrntLeURng:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 704
        signal_description = "Compartment Front Left Area Air Distribution Flap Self Learning Voltage Range"
        signal_length = 9
        start_position = 496
        value_definition = {}

    class ModFlapStsFrntLeElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 704
        signal_description = "Compartment Front Left Area Air Distribution Flap Electrical Error"
        signal_length = 2
        start_position = 519
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ModFlapStsFrntLeActPosn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 704
        signal_description = "Compartment Front Left Area Air Distribution Flap Actual Position"
        signal_length = 10
        start_position = 517
        value_definition = {}

    class ModFlapStsFrntLeClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 704
        signal_description = "Compartment Front Left Area Air Distribution Flap Clear Block Status"
        signal_length = 2
        start_position = 523
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ModFlapStsReLeClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 749
        signal_description = "Compartment Rear Left Area Air Distribution Flap Clear Block Status"
        signal_length = 2
        start_position = 521
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class ModFlapStsReLeVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 749
        signal_description = "Compartment Rear Left Area Air Distribution Flap Voltage Error"
        signal_length = 2
        start_position = 535
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class ModFlapStsReLeOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 749
        signal_description = "Compartment Rear Left Area Air Distribution Flap Over Temperature"
        signal_length = 1
        start_position = 533
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class ModFlapStsReLeURng:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 749
        signal_description = "Compartment Rear Left Area Air Distribution Flap Self Learning Voltage Range"
        signal_length = 9
        start_position = 532
        value_definition = {}

    class ModFlapStsReLeActPosn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 749
        signal_description = "Compartment Rear Left Area Air Distribution Flap Actual Position"
        signal_length = 10
        start_position = 539
        value_definition = {}

    class ModFlapStsReLeRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 749
        signal_description = "Compartment Rear Left Area Air Distribution Flap Running Status"
        signal_length = 2
        start_position = 545
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class ModFlapStsReLeDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 749
        signal_description = "Compartment Rear Left Area Air Distribution Flap Running Direction"
        signal_length = 2
        start_position = 559
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class ModFlapStsReLeCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 749
        signal_description = "Compartment Rear Left Area Air Distribution Flap Calibration Status"
        signal_length = 2
        start_position = 557
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class ModFlapStsReLeElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 749
        signal_description = "Compartment Rear Left Area Air Distribution Flap Electrical Error"
        signal_length = 2
        start_position = 555
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class ModFlapStsReLeBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 749
        signal_description = "Compartment Rear Left Area Air Distribution Flap Block Status"
        signal_length = 2
        start_position = 553
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class OutdBriCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 748
        signal_description = "counter"
        signal_length = 4
        start_position = 575
        value_definition = {}

    class OutdBriChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 748
        signal_description = "check sum"
        signal_length = 8
        start_position = 567
        value_definition = {}

    class OutdBriSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 748
        signal_description = "information about day or night,from RLSM"
        signal_length = 2
        start_position = 571
        value_definition = {'0x0': ' OutdBriSts_Ukwn', '0x1': ' OutdBriSts_Night', '0x2': ' OutdBriSts_Day', '0x3': ' OutdBriSts_Invld'}

    class PNGFltLowUKL30A:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 747
        signal_description = ""
        signal_length = 1
        start_position = 581
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class PNGFltLowUKL30B:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 746
        signal_description = ""
        signal_length = 1
        start_position = 580
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class PNGFltOverIKL30A:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 745
        signal_description = ""
        signal_length = 1
        start_position = 579
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class PNGFltOverIKL30B:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 744
        signal_description = ""
        signal_length = 1
        start_position = 578
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class PNGFltOverUKL30A:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 780
        signal_description = ""
        signal_length = 2
        start_position = 577
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class PNGFltOverUKL30B:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 779
        signal_description = ""
        signal_length = 2
        start_position = 591
        value_definition = {'0x0': ' LVFaultSts_Idle', '0x1': ' LVFaultSts_Fault', '0x2': ' LVFaultSts_NoFault', '0x3': ' LVFaultSts_Reserved'}

    class PNGIPrmKL30A:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 778
        signal_description = ""
        signal_length = 12
        start_position = 589
        value_definition = {}

    class PNGIPrmKL30B:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 777
        signal_description = ""
        signal_length = 12
        start_position = 593
        value_definition = {}

    class PNGIPrmSetKL30AResp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 776
        signal_description = ""
        signal_length = 8
        start_position = 623
        value_definition = {}

    class PNGIPrmSetKL30BResp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 818
        signal_description = ""
        signal_length = 8
        start_position = 631
        value_definition = {}

    class PNGLowUKL30A:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 817
        signal_description = ""
        signal_length = 9
        start_position = 639
        value_definition = {}

    class PNGLowUKL30B:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 816
        signal_description = ""
        signal_length = 9
        start_position = 646
        value_definition = {}

    class PNGLowUSetKL30AResp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 831
        signal_description = ""
        signal_length = 8
        start_position = 663
        value_definition = {}

    class PNGLowUSetKL30BResp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 830
        signal_description = ""
        signal_length = 8
        start_position = 671
        value_definition = {}

    class PNGOverIFltCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 885
        signal_description = ""
        signal_length = 8
        start_position = 679
        value_definition = {}

    class PNGOverTKL30A:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 884
        signal_description = ""
        signal_length = 13
        start_position = 687
        value_definition = {}

    class PNGOverTKL30B:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 883
        signal_description = ""
        signal_length = 13
        start_position = 690
        value_definition = {}

    class PNGOverTSetKL30AResp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 882
        signal_description = ""
        signal_length = 8
        start_position = 719
        value_definition = {}

    class PNGOverTSetKL30BResp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 881
        signal_description = ""
        signal_length = 8
        start_position = 727
        value_definition = {}

    class PNGOverUKL30A:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 880
        signal_description = ""
        signal_length = 9
        start_position = 735
        value_definition = {}

    class PNGOverUKL30B:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 915
        signal_description = ""
        signal_length = 9
        start_position = 742
        value_definition = {}

    class PNGOverUSetKL30AResp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 914
        signal_description = ""
        signal_length = 8
        start_position = 759
        value_definition = {}

    class PNGOverUSetKL30BResp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 913
        signal_description = ""
        signal_length = 8
        start_position = 767
        value_definition = {}

    class PrimBattIQuiscRaw:
        comments = ""
        factor = 1.0
        initial_value = 2047
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -2047
        sig_ub = 912
        signal_description = "Primary battery quiet current"
        signal_length = 11
        start_position = 775
        value_definition = {}

    class PrimBattRRaw:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 927
        signal_description = "Primary battery resistance"
        signal_length = 8
        start_position = 791
        value_definition = {}

    class PrimBattSOHRaw:
        comments = ""
        factor = 1.0
        initial_value = 100
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 926
        signal_description = "Primary battery SOH"
        signal_length = 8
        start_position = 799
        value_definition = {'0xFF': 'BattSOH_Invalid'}

    class PrimBattSOHSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 925
        signal_description = "Primary battery SOH accuracy status"
        signal_length = 2
        start_position = 807
        value_definition = {'0x0': ' LVBattCal_Idle', '0x1': ' LVBattCal_CmplCal', '0x2': ' LVBattCal_InCmplCal', '0x3': ' LVBattCal_Resvd'}

    class PWTCooltPmpActrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 924
        signal_description = "pump actuator status"
        signal_length = 3
        start_position = 805
        value_definition = {'0x0': ' PmpActrSts_NoErr', '0x1': ' PmpActrSts_OverVoltage', '0x2': ' PmpActrSts_UnderVoltage', '0x3': ' PmpActrSts_OverTemperature', '0x4': ' PmpActrSts_OverCurrent', '0x5': ' PmpActrSts_Stall', '0x6': ' PmpActrSts_DryRun', '0x7': ' PmpActrSts_OverLoad'}

    class PWTCooltPmpCmd:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 923
        signal_description = "PWT Coolant Pump Command"
        signal_length = 10
        start_position = 802
        value_definition = {}

    class RainDetected:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 922
        signal_description = "Rain Detected By Rlsm"
        signal_length = 2
        start_position = 808
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class RainfallAmnt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 921
        signal_description = "the signal describe the amount of the rain falling"
        signal_length = 4
        start_position = 822
        value_definition = {'0x0': ' RainfallAmnt_0', '0x1': ' RainfallAmnt_1', '0x2': ' RainfallAmnt_2', '0x3': ' RainfallAmnt_3', '0x4': ' RainfallAmnt_4', '0x5': ' RainfallAmnt_5', '0x6': ' RainfallAmnt_6', '0x7': ' RainfallAmnt_7', '0x8': ' RainfallAmnt_8', '0x9': ' RainfallAmnt_9', '0xA': ' RainfallAmnt_10', '0xB': ' RainfallAmnt_11', '0xC': ' RainfallAmnt_12', '0xD': ' RainfallAmnt_13', '0xE': ' RainfallAmnt_InitValue', '0xF': ' RainfallAmnt_Error'}

    class RefrigorAvlStsEcoSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 920
        signal_description = "Cabin Refrigerator Eco Status"
        signal_length = 1
        start_position = 829
        value_definition = {'0x0': ' EcoSts_NoEco', '0x1': ' EcoSts_Eco'}

    class RefrigorAvlStsChmbT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 920
        signal_description = "Cabin Refrigerator Chamber Temperature"
        signal_length = 13
        start_position = 828
        value_definition = {}

    class RefrigorAvlStsCmprSpd:
        comments = ""
        factor = 50.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 920
        signal_description = "Cabin Refrigerator Compressor Speed"
        signal_length = 8
        start_position = 847
        value_definition = {}

    class RefrigorAvlStsSysSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 920
        signal_description = "Cabin Refrigerator System Status"
        signal_length = 3
        start_position = 855
        value_definition = {'0x0': ' RefrigeratorSysSts_Normal', '0x1': ' RefrigeratorSysSts_CmprSpdLimd', '0x2': ' RefrigeratorSysSts_DisChargrTLimd', '0x3': ' RefrigeratorSysSts_AntiIceLimd', '0x4': ' RefrigeratorSysSts_Reserved1', '0x5': ' RefrigeratorSysSts_Reserved2', '0x6': ' RefrigeratorSysSts_Reserved3', '0x7': ' RefrigeratorSysSts_Reserved4'}

    class RefrigorAvlStsDoorSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 920
        signal_description = "Cabin Refrigerator Door Status"
        signal_length = 4
        start_position = 852
        value_definition = {'0x0': ' DoorMtnSts_IniVal', '0x1': ' DoorMtnSts_FullOpen', '0x2': ' DoorMtnSts_FullClose', '0x3': ' DoorMtnSts_StopDurOpen', '0x4': ' DoorMtnSts_StopDurClose', '0x5': ' DoorMtnSts_MovingOut', '0x6': ' DoorMtnSts_MovingIn', '0x7': ' DoorMtnSts_HalfClose', '0x8': ' DoorMtnSts_Unknow', '0x9': ' DoorMtnSts_OnlyOpenPosn'}

    class RefrigorAvlStsCoolgAbortRsn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 920
        signal_description = "Cabin Refrigerator Cooling Abortion Reason"
        signal_length = 4
        start_position = 848
        value_definition = {'0x0': ' RefrigorCoolingAbortRsn_Normal', '0x1': ' RefrigorCoolingAbortRsn_ModFlt', '0x2': ' RefrigorCoolingAbortRsn_Temp', '0x3': ' RefrigorCoolingAbortRsn_DoorOpen', '0x4': ' RefrigorCoolingAbortRsn_TSnsrErr', '0x5': ' RefrigorCoolingAbortRsn_CoolingSysErr', '0x6': ' RefrigorCoolingAbortRsn_VoltSuplyErr', '0x7': ' RefrigorCoolingAbortRsn_ComErr'}

    class RefrigorAvlStsLiSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 920
        signal_description = "Cabin Refrigerator Light Status"
        signal_length = 1
        start_position = 860
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class RefrigorAvlStsHeatgAbortRsn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 920
        signal_description = "Cabin Refrigerator Heating Abortion Reason"
        signal_length = 4
        start_position = 859
        value_definition = {'0x0': ' RefrigorHeatingAbortRsn_Normal', '0x1': ' RefrigorHeatingAbortRsn_ModFlt', '0x2': ' RefrigorHeatingAbortRsn_Temp', '0x3': ' RefrigorHeatingAbortRsn_DoorOpen', '0x4': ' RefrigorHeatingAbortRsn_TSnsrErr', '0x5': ' RefrigorHeatingAbortRsn_HeatingSysErr', '0x6': ' RefrigorHeatingAbortRsn_VoltSuplyErr', '0x7': ' RefrigorHeatingAbortRsn_ComErr'}

    class RefrigorAvlStsActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 920
        signal_description = "Cabin Refrigerator Actual Power"
        signal_length = 12
        start_position = 871
        value_definition = {}

    class RefrigorAvlStsRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 920
        signal_description = "Cabin Refrigerator Running Status"
        signal_length = 3
        start_position = 875
        value_definition = {'0x0': ' RefrigeratorSts_Idle', '0x1': ' RefrigeratorSts_Cooling', '0x2': ' RefrigeratorSts_Heating', '0x3': ' RefrigeratorSts_Err', '0x4': ' RefrigeratorSts_Reserved1', '0x5': ' RefrigeratorSts_Reserved2', '0x6': ' RefrigeratorSts_Reserved3', '0x7': ' RefrigeratorSts_Reserved4'}

    class RefrigSov1ActvReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 935
        signal_description = "Refrigerant Solenoid Valve 1 Active Request"
        signal_length = 1
        start_position = 872
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class RefrigSov2ActvReq:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 934
        signal_description = "Refrigerant Solenoid Valve 2 Active Request"
        signal_length = 1
        start_position = 887
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class RelHumSnsrErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 955
        signal_description = "Compartment Relative Humidity Sensor Error"
        signal_length = 1
        start_position = 886
        value_definition = {'0x0': ' Err1_NoErr', '0x1': ' Err1_Err'}

    class RelHumSnsrRelHum:
        comments = ""
        factor = 0.5
        initial_value = 80
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 954
        signal_description = "Compartment Relative Humidity"
        signal_length = 8
        start_position = 895
        value_definition = {}

    class ReSunroofCurtFailrFbOverTmp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 953
        signal_description = "over temperature failure of the rear sunroof curt motor"
        signal_length = 1
        start_position = 903
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class ReSunroofCurtFailrFbLoVolt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 953
        signal_description = "low voltage failure of the rear sunroof curt module"
        signal_length = 1
        start_position = 902
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class ReSunroofCurtFailrFbMotOpenCirc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 953
        signal_description = "open circuit of the rear sunroof curt motor"
        signal_length = 1
        start_position = 901
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class ReSunroofCurtFailrFbMotShoCirc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 953
        signal_description = "short circuit of  the rear sunroof curt motor"
        signal_length = 1
        start_position = 900
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class ReSunroofCurtFailrFbHallSnsrFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 953
        signal_description = "short circuit of the rear sunroof curt motor"
        signal_length = 1
        start_position = 899
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class ReSunroofCurtFailrFbHiVolt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 953
        signal_description = "high voltage failure of the rear sunroof curt module"
        signal_length = 1
        start_position = 898
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class ReSunroofCurtImpactFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 952
        signal_description = "the impact fedback of the rear sunroof curt"
        signal_length = 3
        start_position = 897
        value_definition = {'0x0': ' PinchAndBlkFb_Idle', '0x1': ' PinchAndBlkFb_ClsPinch', '0x2': ' PinchAndBlkFb_ClsBlk', '0x3': ' PinchAndBlkFb_OpenPinch', '0x4': ' PinchAndBlkFb_OpenBlk'}

    class ReSunroofCurtlrnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 996
        signal_description = "the learn state of the rear sunroof curt motor"
        signal_length = 2
        start_position = 910
        value_definition = {'0x0': ' LrnSts_Idle', '0x1': ' LrnSts_lrnOk', '0x2': ' LrnSts_lrnInProgs', '0x3': ' LrnSts_lrnFail'}

    class ReSunroofCurtMvngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 995
        signal_description = "the motion state of the rear sunroof curt motor"
        signal_length = 2
        start_position = 908
        value_definition = {'0x0': ' MoveSts_Idle', '0x1': ' MoveSts_Stop', '0x2': ' MoveSts_Opening', '0x3': ' MoveSts_Closing'}

    class ReSunroofCurtPosnPerc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 994
        signal_description = "the position requestion of the rear sunroof curt"
        signal_length = 5
        start_position = 906
        value_definition = {'0x0': ' PosnPerc_Idle', '0x1': ' PosnPerc_PosnPercUnknow', '0x2': ' PosnPerc_PosnPercFullCls', '0x3': ' PosnPerc_PosnPerc4', '0x4': ' PosnPerc_PosnPerc8', '0x5': ' PosnPerc_PosnPerc12', '0x6': ' PosnPerc_PosnPerc16', '0x7': ' PosnPerc_PosnPerc20', '0x8': ' PosnPerc_PosnPerc24', '0x9': ' PosnPerc_PosnPerc28', '0xA': ' PosnPerc_PosnPerc32', '0xB': ' PosnPerc_PosnPerc36', '0xC': ' PosnPerc_PosnPerc40', '0xD': ' PosnPerc_PosnPerc44', '0xE': ' PosnPerc_PosnPerc48', '0xF': ' PosnPerc_PosnPerc52', '0x10': ' PosnPerc_PosnPerc56', '0x11': ' PosnPerc_PosnPerc60', '0x12': ' PosnPerc_PosnPerc64', '0x13': ' PosnPerc_PosnPerc68', '0x14': ' PosnPerc_PosnPerc72', '0x15': ' PosnPerc_PosnPerc76', '0x16': ' PosnPerc_PosnPerc80', '0x17': ' PosnPerc_PosnPerc84', '0x18': ' PosnPerc_PosnPerc88', '0x19': ' PosnPerc_PosnPerc92', '0x1A': ' PosnPerc_PosnPerc96', '0x1B': ' PosnPerc_FullOpen', '0x1C': ' PosnPerc_Reserved1', '0x1D': ' PosnPerc_Reserved2', '0x1E': ' PosnPerc_Reserved3'}

    class RLDoorManResistSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 993
        signal_description = "Door manual resistance status"
        signal_length = 2
        start_position = 917
        value_definition = {'0x0': ' DoorManResistsSts_NoResist', '0x1': ' DoorManResistsSts_Level1', '0x2': ' DoorManResistsSts_Level2'}

    class RLDoorSpdModeFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 992
        signal_description = "power side door mode status feedback"
        signal_length = 2
        start_position = 933
        value_definition = {'0x0': ' SpdMode_Low', '0x1': ' SpdMode_Middle', '0x2': ' SpdMode_High'}

    class SeatAdj1RowLeStopCaseMotorStopCase:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1036
        signal_description = "Detailed Stop Reason"
        signal_length = 4
        start_position = 931
        value_definition = {'0x0': ' MotorStopCase_idle', '0x1': ' MotorStopCase_MotorStall', '0x2': ' MotorStopCase_AntiPinch', '0x3': ' MotorStopCase_ThermalProtection', '0x4': ' MotorStopCase_Button', '0x5': ' MotorStopCase_Signal', '0x6': ' MotorStopCase_Speed', '0x7': ' MotorStopCase_HWerror', '0x8': ' MotorStopCase_reserved1', '0x9': ' MotorStopCase_reserved2', '0xA': ' MotorStopCase_reserved3', '0xB': ' MotorStopCase_reserved4', '0xC': ' MotorStopCase_reserved5', '0xD': ' MotorStopCase_reserved6', '0xE': ' MotorStopCase_reserved7', '0xF': ' MotorStopCase_reserved8'}

    class SeatAdj1RowLeStopCaseSeatCfg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1036
        signal_description = "Seat Motor Config"
        signal_length = 4
        start_position = 943
        value_definition = {'0x0': ' SeatCfg_Idle', '0x1': ' SeatCfg_Length', '0x2': ' SeatCfg_Height', '0x3': ' SeatCfg_Tilt', '0x4': ' SeatCfg_BackrestAngle', '0x5': ' SeatCfg_OTTOLength', '0x6': ' SeatCfg_OTTOAngle', '0x7': ' SeatCfg_CLA', '0x8': ' SeatCfg_Release', '0x9': ' SeatCfg_Reserved1', '0xA': ' SeatCfg_Reserved2', '0xB': ' SeatCfg_Reserved3', '0xC': ' SeatCfg_Reserved4', '0xD': ' SeatCfg_Reserved5', '0xE': ' SeatCfg_Reserved6', '0xF': ' SeatCfg_Reserved7'}

    class SeatAdj2RowLeStopCaseSeatCfg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1035
        signal_description = "Seat Motor Config"
        signal_length = 4
        start_position = 939
        value_definition = {'0x0': ' SeatCfg_Idle', '0x1': ' SeatCfg_Length', '0x2': ' SeatCfg_Height', '0x3': ' SeatCfg_Tilt', '0x4': ' SeatCfg_BackrestAngle', '0x5': ' SeatCfg_OTTOLength', '0x6': ' SeatCfg_OTTOAngle', '0x7': ' SeatCfg_CLA', '0x8': ' SeatCfg_Release', '0x9': ' SeatCfg_Reserved1', '0xA': ' SeatCfg_Reserved2', '0xB': ' SeatCfg_Reserved3', '0xC': ' SeatCfg_Reserved4', '0xD': ' SeatCfg_Reserved5', '0xE': ' SeatCfg_Reserved6', '0xF': ' SeatCfg_Reserved7'}

    class SeatAdj2RowLeStopCaseMotorStopCase:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1035
        signal_description = "Detailed Stop Reason"
        signal_length = 4
        start_position = 951
        value_definition = {'0x0': ' MotorStopCase_idle', '0x1': ' MotorStopCase_MotorStall', '0x2': ' MotorStopCase_AntiPinch', '0x3': ' MotorStopCase_ThermalProtection', '0x4': ' MotorStopCase_Button', '0x5': ' MotorStopCase_Signal', '0x6': ' MotorStopCase_Speed', '0x7': ' MotorStopCase_HWerror', '0x8': ' MotorStopCase_reserved1', '0x9': ' MotorStopCase_reserved2', '0xA': ' MotorStopCase_reserved3', '0xB': ' MotorStopCase_reserved4', '0xC': ' MotorStopCase_reserved5', '0xD': ' MotorStopCase_reserved6', '0xE': ' MotorStopCase_reserved7', '0xF': ' MotorStopCase_reserved8'}

    class SeatAdj3RowLeStopCaseMotorStopCase:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1034
        signal_description = "Detailed Stop Reason"
        signal_length = 4
        start_position = 947
        value_definition = {'0x0': ' MotorStopCase_idle', '0x1': ' MotorStopCase_MotorStall', '0x2': ' MotorStopCase_AntiPinch', '0x3': ' MotorStopCase_ThermalProtection', '0x4': ' MotorStopCase_Button', '0x5': ' MotorStopCase_Signal', '0x6': ' MotorStopCase_Speed', '0x7': ' MotorStopCase_HWerror', '0x8': ' MotorStopCase_reserved1', '0x9': ' MotorStopCase_reserved2', '0xA': ' MotorStopCase_reserved3', '0xB': ' MotorStopCase_reserved4', '0xC': ' MotorStopCase_reserved5', '0xD': ' MotorStopCase_reserved6', '0xE': ' MotorStopCase_reserved7', '0xF': ' MotorStopCase_reserved8'}

    class SeatAdj3RowLeStopCaseSeatCfg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1034
        signal_description = "Seat Motor Config"
        signal_length = 4
        start_position = 959
        value_definition = {'0x0': ' SeatCfg_Idle', '0x1': ' SeatCfg_Length', '0x2': ' SeatCfg_Height', '0x3': ' SeatCfg_Tilt', '0x4': ' SeatCfg_BackrestAngle', '0x5': ' SeatCfg_OTTOLength', '0x6': ' SeatCfg_OTTOAngle', '0x7': ' SeatCfg_CLA', '0x8': ' SeatCfg_Release', '0x9': ' SeatCfg_Reserved1', '0xA': ' SeatCfg_Reserved2', '0xB': ' SeatCfg_Reserved3', '0xC': ' SeatCfg_Reserved4', '0xD': ' SeatCfg_Reserved5', '0xE': ' SeatCfg_Reserved6', '0xF': ' SeatCfg_Reserved7'}

    class SeatClima1RowLeStsHeatgActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1033
        signal_description = "First Row Left Side Seat Heating Actual Power"
        signal_length = 8
        start_position = 967
        value_definition = {}

    class SeatClima1RowLeStsVentAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1033
        signal_description = "First Row Left Side Seat Venting Available Status"
        signal_length = 3
        start_position = 975
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClima1RowLeStsTEstimd:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 1033
        signal_description = "First Row Left Side Seat Heating Actual Temperature"
        signal_length = 11
        start_position = 972
        value_definition = {}

    class SeatClima1RowLeStsVentActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1033
        signal_description = "First Row Left Side Seat Venting Actual Power"
        signal_length = 8
        start_position = 991
        value_definition = {}

    class SeatClima1RowLeStsHeatgAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1033
        signal_description = "First Row Left Side Seat Heating Available Status"
        signal_length = 3
        start_position = 999
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClima2RowLeStsVentActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1032
        signal_description = "Second Row Left Side Seat Venting Actual Power"
        signal_length = 8
        start_position = 1007
        value_definition = {}

    class SeatClima2RowLeStsTEstimd:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 1032
        signal_description = "Second Row Left Side Seat Heating Actual Temperature"
        signal_length = 11
        start_position = 1015
        value_definition = {}

    class SeatClima2RowLeStsVentAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1032
        signal_description = "Second Row Left Side Seat Venting Available Status"
        signal_length = 3
        start_position = 1020
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClima2RowLeStsHeatgAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1032
        signal_description = "Second Row Left Side Seat Heating Available Status"
        signal_length = 3
        start_position = 1039
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClima2RowLeStsHeatgActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1032
        signal_description = "Second Row Left Side Seat Heating Actual Power"
        signal_length = 8
        start_position = 1031
        value_definition = {}

    class SeatClima3RowLeStsVentActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1083
        signal_description = "Third Row Left Side Seat Venting Actual Power"
        signal_length = 8
        start_position = 1047
        value_definition = {}

    class SeatClima3RowLeStsHeatgActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1083
        signal_description = "Third Row Left Side Seat Heating Actual Power"
        signal_length = 8
        start_position = 1055
        value_definition = {}

    class SeatClima3RowLeStsTEstimd:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 1083
        signal_description = "Third Row Left Side Seat Heating Actual Temperature"
        signal_length = 11
        start_position = 1063
        value_definition = {}

    class SeatClima3RowLeStsHeatgAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1083
        signal_description = "Third Row Left Side Seat Heating Available Status"
        signal_length = 3
        start_position = 1068
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClima3RowLeStsVentAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1083
        signal_description = "Third Row Left Side Seat Venting Available Status"
        signal_length = 3
        start_position = 1065
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SeatClimaLeHeatgBtnStsRow1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1082
        signal_description = "First Row Left Side Seat Heating Button Status"
        signal_length = 2
        start_position = 1078
        value_definition = {'0x0': ' SeatClimaLvl_Off', '0x1': ' SeatClimaLvl_Lvl1', '0x2': ' SeatClimaLvl_Lvl2', '0x3': ' SeatClimaLvl_Lvl3'}

    class SeatClimaLeHeatgBtnStsRow3:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1082
        signal_description = "Third Row Left Side Seat Heating Button Status"
        signal_length = 2
        start_position = 1076
        value_definition = {'0x0': ' SeatClimaLvl_Off', '0x1': ' SeatClimaLvl_Lvl1', '0x2': ' SeatClimaLvl_Lvl2', '0x3': ' SeatClimaLvl_Lvl3'}

    class SeatClimaLeHeatgBtnStsRow2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1082
        signal_description = "Second Row Left Side Seat Heating Button Status"
        signal_length = 2
        start_position = 1074
        value_definition = {'0x0': ' SeatClimaLvl_Off', '0x1': ' SeatClimaLvl_Lvl1', '0x2': ' SeatClimaLvl_Lvl2', '0x3': ' SeatClimaLvl_Lvl3'}

    class ShutDownTypPNG1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1081
        signal_description = "Shut down type"
        signal_length = 4
        start_position = 1072
        value_definition = {'0x0': ' ErrStsPNG_Invalid', '0x1': ' ErrStsPNG_NoErr', '0x2': ' ErrStsPNG_OverVolt', '0x3': ' ErrStsPNG_LowVolt', '0x4': ' ErrStsPNG_OverT', '0x5': ' ErrStsPNG_HSHT', '0x6': ' ErrStsPNG_Others', '0x7': ' ErrStsPNG_Reserved2', '0x8': ' ErrStsPNG_Reserved3', '0x9': ' ErrStsPNG_Reserved4', '0xA': ' ErrStsPNG_Reserved5', '0xB': ' ErrStsPNG_Reserved6', '0xC': ' ErrStsPNG_Reserved7', '0xD': ' ErrStsPNG_Reserved8', '0xE': ' ErrStsPNG_Reserved9', '0xF': ' ErrStsPNG_Reserved10'}

    class SolarSnsrErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1080
        signal_description = "Solar Sensor Error"
        signal_length = 1
        start_position = 1084
        value_definition = {'0x0': ' Err1_NoErr', '0x1': ' Err1_Err'}

    class SolarSnsrLeValue:
        comments = ""
        factor = 5.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1121
        signal_description = "Left Side Solar Intensity"
        signal_length = 8
        start_position = 1095
        value_definition = {}

    class SolarSnsrRiValue:
        comments = ""
        factor = 5.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1120
        signal_description = "Right Side Solar Intensity"
        signal_length = 8
        start_position = 1103
        value_definition = {}

    class SteerWhlHeatgStsAvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1135
        signal_description = "Steering Wheel Heating Available Status"
        signal_length = 3
        start_position = 1119
        value_definition = {'0x0': ' SeatClimaAvl_None', '0x1': ' SeatClimaAvl_On', '0x2': ' SeatClimaAvl_Off', '0x3': ' SeatClimaAvl_Error', '0x4': ' SeatClimaAvl_Functionallimit', '0x5': ' SeatClimaAvl_Energylimit', '0x6': ' SeatClimaAvl_Resvd1', '0x7': ' SeatClimaAvl_Resvd2'}

    class SteerWhlHeatgStsActPwr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1135
        signal_description = "Steering Wheel Heating Actual Power"
        signal_length = 8
        start_position = 1111
        value_definition = {}

    class SteerWhlHeatgStsTEstimd:
        comments = ""
        factor = 0.1
        initial_value = 400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 1135
        signal_description = "Steering Wheel Heating Actual Temperature"
        signal_length = 11
        start_position = 1116
        value_definition = {}

    class TempFlapStsFrntLeElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1134
        signal_description = "Compartment Front Left Area Temperature Flap Electrical Error"
        signal_length = 2
        start_position = 1132
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class TempFlapStsFrntLeVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1134
        signal_description = "Compartment Front Left Area Temperature Flap Voltage Error"
        signal_length = 2
        start_position = 1130
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class TempFlapStsFrntLeActPosn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1134
        signal_description = "Compartment Front Left Area Temperature Flap Actual Position"
        signal_length = 10
        start_position = 1128
        value_definition = {}

    class TempFlapStsFrntLeDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1134
        signal_description = "Compartment Front Left Area Temperature Flap Running Direction"
        signal_length = 2
        start_position = 1150
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class TempFlapStsFrntLeRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1134
        signal_description = "Compartment Front Left Area Temperature Flap Running Status"
        signal_length = 2
        start_position = 1148
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class TempFlapStsFrntLeCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1134
        signal_description = "Compartment Front Left Area Temperature Flap Calibration Status"
        signal_length = 2
        start_position = 1146
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class TempFlapStsFrntLeBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1134
        signal_description = "Compartment Front Left Area Temperature Flap Block Status"
        signal_length = 2
        start_position = 1144
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class TempFlapStsFrntLeClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1134
        signal_description = "Compartment Front Left Area Temperature Flap Clear Block Status"
        signal_length = 2
        start_position = 1158
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class TempFlapStsFrntLeOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1134
        signal_description = "Compartment Front Left Area Temperature Flap Over Temperature"
        signal_length = 1
        start_position = 1156
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class TempFlapStsFrntLeURng:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1134
        signal_description = "Compartment Front Left Area Temperature Flap Voltage Range"
        signal_length = 9
        start_position = 1155
        value_definition = {}

    class TempFlapStsReLeClrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1133
        signal_description = "Compartment Rear Left Area Temperature Flap Clear Block Status"
        signal_length = 2
        start_position = 1162
        value_definition = {'0x0': ' MotClrSts_Default', '0x1': ' MotClrSts_Excuting', '0x2': ' MotClrSts_Succeed', '0x3': ' MotClrSts_Failed'}

    class TempFlapStsReLeURng:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1133
        signal_description = " Compartment Rear Left Area Temperature Flap Voltage Range"
        signal_length = 9
        start_position = 1160
        value_definition = {}

    class TempFlapStsReLeCalSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1133
        signal_description = "Compartment Rear Left Area Temperature Flap Calibration Status"
        signal_length = 2
        start_position = 1183
        value_definition = {'0x0': ' MotCalSts_Default', '0x1': ' MotCalSts_Excuting', '0x2': ' MotCalSts_Succeed', '0x3': ' MotCalSts_Failed'}

    class TempFlapStsReLeRunngSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1133
        signal_description = "Compartment Rear Left Area Temperature Flap Running Status"
        signal_length = 2
        start_position = 1181
        value_definition = {'0x0': ' MotRunngSts_Normal', '0x1': ' MotRunngSts_Stop', '0x2': ' MotRunngSts_Signalinvalid', '0x3': ' MotRunngSts_Reserved'}

    class TempFlapStsReLeOverTemp:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1133
        signal_description = "Compartment Rear Left Area Temperature Flap Over Temperature"
        signal_length = 1
        start_position = 1179
        value_definition = {'0x0': ' MotOverTemp_Normal', '0x1': ' MotOverTemp_OverTemp'}

    class TempFlapStsReLeElecErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1133
        signal_description = "Compartment Rear Left Area Temperature Flap Electrical Error"
        signal_length = 2
        start_position = 1178
        value_definition = {'0x0': ' ElecErr_Normal', '0x1': ' ElecErr_ShortToGroundOrOpenCircuit', '0x2': ' ElecErr_ShortToBatt', '0x3': ' ElecErr_Reserved'}

    class TempFlapStsReLeVoltErr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1133
        signal_description = "Compartment Rear Left Area Temperature Flap Voltage Error"
        signal_length = 2
        start_position = 1176
        value_definition = {'0x0': ' VoltErr_Normal', '0x1': ' VoltErr_UnderVolt', '0x2': ' VoltErr_OverVolt', '0x3': ' VoltErr_Reserved'}

    class TempFlapStsReLeDirSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1133
        signal_description = "Compartment Rear Left Area Temperature Flap Running Direction"
        signal_length = 2
        start_position = 1190
        value_definition = {'0x0': ' MotDir_CW', '0x1': ' MotDir_CCW', '0x2': ' MotDir_Stop', '0x3': ' MotDir_Reserved'}

    class TempFlapStsReLeBlkSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1133
        signal_description = "Compartment Rear Left Area Temperature Flap Block Status"
        signal_length = 2
        start_position = 1188
        value_definition = {'0x0': ' MotBlkSts_NoBlock', '0x1': ' MotBlkSts_Block', '0x2': ' MotBlkSts_Signalinvalid', '0x3': ' MotBlkSts_Reserved'}

    class TempFlapStsReLeActPosn:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1133
        signal_description = "Compartment Rear Left Area Temperature Flap Actual Position"
        signal_length = 10
        start_position = 1186
        value_definition = {}

    class TowBarDrvrPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1284
        signal_description = "Tow Bar Driver Position"
        signal_length = 7
        start_position = 1192
        value_definition = {}

    class TowBarDrvrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1283
        signal_description = "Tow Bar Driver Status"
        signal_length = 3
        start_position = 1201
        value_definition = {'0x0': ' TowBarDrvrStsType_Invalid', '0x1': ' TowBarDrvrStsType_FoldPosn', '0x2': ' TowBarDrvrStsType_UnflodPosn', '0x3': ' TowBarDrvrStsType_MovgToFold', '0x4': ' TowBarDrvrStsType_MovgToUnfold', '0x5': ' TowBarDrvrStsType_Err'}

    class TowBarHallSnsrFltHallAFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1282
        signal_description = "Hall Sensor A Fault"
        signal_length = 2
        start_position = 1214
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class TowBarHallSnsrFltHallOutpFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1282
        signal_description = "Hall Sensor Output Fault"
        signal_length = 2
        start_position = 1212
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class TowBarHallSnsrFltHallBFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1282
        signal_description = "Hall Sensor B Fault"
        signal_length = 2
        start_position = 1210
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class TowBarMotFltMotOverCurrent:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1281
        signal_description = "Motor Over Current"
        signal_length = 2
        start_position = 1208
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class TowBarMotFltMotShoCircGND:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1281
        signal_description = "Motor Short Circuit GND"
        signal_length = 2
        start_position = 1220
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class TowBarMotFltTmrFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1281
        signal_description = "Timer Fault"
        signal_length = 2
        start_position = 1218
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class TowBarMotFltMotShoCircBatt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1281
        signal_description = "Motor Short Circuit Battery"
        signal_length = 2
        start_position = 1216
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class TowBarMotFltMotOpenCirc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1281
        signal_description = "Motor Open Circuit"
        signal_length = 2
        start_position = 1230
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class TrlrElecCnctSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1280
        signal_description = "Trailer Connection Status"
        signal_length = 1
        start_position = 1228
        value_definition = {'0x0': ' YesNo2_No', '0x1': ' YesNo2_Yes'}

    class TrlrMntnNotice:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1299
        signal_description = "Trailer Maintenance Notice"
        signal_length = 1
        start_position = 1227
        value_definition = {'0x0': ' Boolean_FALSE', '0x1': ' Boolean_TRUE'}

    class URawLCU1:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1298
        signal_description = "Voltage"
        signal_length = 9
        start_position = 1226
        value_definition = {}

    class URawPNG1KL30A:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1297
        signal_description = "Voltage"
        signal_length = 9
        start_position = 1233
        value_definition = {}

    class URawPNG1KL30B:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1296
        signal_description = ""
        signal_length = 9
        start_position = 1240
        value_definition = {}

    class URawRML:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1311
        signal_description = "Voltage"
        signal_length = 9
        start_position = 1263
        value_definition = {}

    class URawWMM:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1310
        signal_description = "Voltage"
        signal_length = 9
        start_position = 1270
        value_definition = {}

    class WinLockAutoClsEnableSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1309
        signal_description = "Request On Auto Close Window When Lock"
        signal_length = 2
        start_position = 1277
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class WinRainAutoClsEnableSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1308
        signal_description = "Status On Auto Close Window When Rain"
        signal_length = 2
        start_position = 1275
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class WipgAutFrntMod:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1307
        signal_description = "Information regarding rain sensor operational mode"
        signal_length = 2
        start_position = 1273
        value_definition = {'0x0': ' WipgAutFrntMod_Off', '0x1': ' WipgAutFrntMod_ImdMod', '0x2': ' WipgAutFrntMod_Intlmod', '0x3': ' WipgAutFrntMod_ContnsMod'}

    class WiprActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1306
        signal_description = "From WMM,the front wiper is activated"
        signal_length = 1
        start_position = 1287
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class WiprInPosnForSrv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1305
        signal_description = "the service position feedback of the WMM"
        signal_length = 1
        start_position = 1286
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class WiprInWipgAr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1304
        signal_description = "From WMM,the front wiper crank is in the wipering area or not"
        signal_length = 1
        start_position = 1285
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class WshngCycActv:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1317
        signal_description = "From WMM,washing activation lead to activation of the wiper linkage function."
        signal_length = 1
        start_position = 1302
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class VentAirTEstimdFrntLeFootT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1409
        signal_description = "Front Left Foot Air Temperature"
        signal_length = 13
        start_position = 1407
        value_definition = {}

    class VentAirTEstimdFrntLeFaceT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1409
        signal_description = "Front Left Face Air Temperature"
        signal_length = 13
        start_position = 1391
        value_definition = {}

    class VentAirTEstimdFrntLeFaceTQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1409
        signal_description = "Front Left Face Air Temperature Quality Flag"
        signal_length = 1
        start_position = 1394
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class VentAirTEstimdFrntLeFootTQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1409
        signal_description = "Front Left Foot Air Temperature Quality Flag"
        signal_length = 1
        start_position = 1410
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class RearWshrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1324
        signal_description = "rear washer status"
        signal_length = 1
        start_position = 1325
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SunHumSnsrErrSolarSnsr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1321
        signal_description = "Solar Sensor Error"
        signal_length = 1
        start_position = 1322
        value_definition = {'0x0': ' Err1_NoErr', '0x1': ' Err1_Err'}

    class SunHumSnsrErrRelHumSnsr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1321
        signal_description = "Relative Humidity Sensor Error"
        signal_length = 1
        start_position = 1323
        value_definition = {'0x0': ' Err1_NoErr', '0x1': ' Err1_Err'}

    class VentAirTEstimdReLeFootTQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1441
        signal_description = "Rear Left Foot Air Temperature Quality Flag"
        signal_length = 1
        start_position = 1442
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class VentAirTEstimdReLeFootT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1441
        signal_description = "Rear Left Foot Air Temperature"
        signal_length = 13
        start_position = 1439
        value_definition = {}

    class VentAirTEstimdReLeFaceTQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1441
        signal_description = "Rear Left Face Air Temperature Quality Flag"
        signal_length = 1
        start_position = 1426
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class VentAirTEstimdReLeFaceT:
        comments = ""
        factor = 0.1
        initial_value = 2560
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -256
        sig_ub = 1441
        signal_description = "Rear Left Face Air Temperature"
        signal_length = 13
        start_position = 1423
        value_definition = {}

    class FrntWshrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1326
        signal_description = "Front Washer Status"
        signal_length = 1
        start_position = 1327
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class SunHumEstimdSolarIntenLeQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1380
        signal_description = "Left Side Solar Intensity Quality Flag"
        signal_length = 1
        start_position = 1338
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class SunHumEstimdSolarIntenRiQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1380
        signal_description = "Right Side Solar Intensity Quality Flag"
        signal_length = 1
        start_position = 1336
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class SunHumEstimdFrntWindRelHum:
        comments = ""
        factor = 0.5
        initial_value = 80
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1380
        signal_description = "Front Windscreen Relative Humidity"
        signal_length = 8
        start_position = 1351
        value_definition = {}

    class SunHumEstimdFrntWindT:
        comments = ""
        factor = 0.1
        initial_value = 650
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 1380
        signal_description = "Front Windscreen Temperature"
        signal_length = 11
        start_position = 1375
        value_definition = {}

    class SunHumEstimdFrntWindDewT:
        comments = ""
        factor = 0.1
        initial_value = 600
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -40
        sig_ub = 1380
        signal_description = "Front Windscreen Dew Point Temperature"
        signal_length = 11
        start_position = 1335
        value_definition = {}

    class SunHumEstimdFrntWindRelHumQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1380
        signal_description = "Front Windscreen Relative Humidity Quality Flag"
        signal_length = 1
        start_position = 1339
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class SunHumEstimdFrntWindDewTQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1380
        signal_description = "Front Windscreen Dew Point Temperature Quality Flag"
        signal_length = 1
        start_position = 1340
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class SunHumEstimdSolarIntenLe:
        comments = ""
        factor = 5.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1380
        signal_description = "Left Side Solar Intensity"
        signal_length = 8
        start_position = 1359
        value_definition = {}

    class SunHumEstimdSolarIntenRi:
        comments = ""
        factor = 5.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1380
        signal_description = "Right Side Solar Intensity"
        signal_length = 8
        start_position = 1367
        value_definition = {}

    class SunHumEstimdFrntWindTQf:
        comments = ""
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1380
        signal_description = "Front Windscreen Temperature Quality Flag"
        signal_length = 1
        start_position = 1337
        value_definition = {'0x0': ' HVACTempQf_SnsrDataNotOk', '0x1': ' HVACTempQf_SnsrDataOk'}

    class WshrLvrPosnSafe:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1453
        signal_description = "the front washing activation state,with functional safety."
        signal_length = 2
        start_position = 1455
        value_definition = {'0x0': ' OnOffCrit1_NotVld1', '0x1': ' OnOffCrit1_Off', '0x2': ' OnOffCrit1_On', '0x3': ' OnOffCrit1_NotVld2'}

    class WshrMotFailrOpenCirc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1376
        signal_description = "the open-circuit fault of the washing motor"
        signal_length = 1
        start_position = 1379
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class WshrMotFailrShoCircToBatt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1376
        signal_description = "the short to batt fault of the washing motor"
        signal_length = 1
        start_position = 1378
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class WshrMotFailrShoCircToGND:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1376
        signal_description = "the short to GND fault of the washing motor"
        signal_length = 1
        start_position = 1377
        value_definition = {'0x0': ' FailrNoFailr1_NoFailr', '0x1': ' FailrNoFailr1_Failr'}

    class TowBarMotBlk:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1449
        signal_description = "Tow Bar Motor Block"
        signal_length = 1
        start_position = 1450
        value_definition = {'0x0': ' NoYes1_No', '0x1': ' NoYes1_Yes'}

    class RLDoorOpenTrigSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1451
        signal_description = "trigger source of power side door open"
        signal_length = 4
        start_position = 1459
        value_definition = {'0x0': ' DoorCtrlTriSrc_NoTrigSrc', '0x1': ' DoorCtrlTriSrc_InsdSwt', '0x2': ' DoorCtrlTriSrc_OutdSwt', '0x3': ' DoorCtrlTriSrc_NFC', '0x4': ' DoorCtrlTriSrc_Aproch', '0x5': ' DoorCtrlTriSrc_OutdCtrl', '0x6': ' DoorCtrlTriSrc_InsdCtrl', '0x7': ' DoorCtrlTriSrc_Resd1', '0x8': ' DoorCtrlTriSrc_Resd2', '0x9': ' DoorCtrlTriSrc_Resd3'}

    class WiprInPrkgPosnLo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1440
        signal_description = "the front wiper is in the park position or not,from WMM"
        signal_length = 1
        start_position = 1448
        value_definition = {'0x0': ' OnOff1_Off', '0x1': ' OnOff1_On'}

    class FLDoorOpenTrigSrc:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1452
        signal_description = "trigger source of power side door open"
        signal_length = 4
        start_position = 1463
        value_definition = {'0x0': ' DoorCtrlTriSrc_NoTrigSrc', '0x1': ' DoorCtrlTriSrc_InsdSwt', '0x2': ' DoorCtrlTriSrc_OutdSwt', '0x3': ' DoorCtrlTriSrc_NFC', '0x4': ' DoorCtrlTriSrc_Aproch', '0x5': ' DoorCtrlTriSrc_OutdCtrl', '0x6': ' DoorCtrlTriSrc_InsdCtrl', '0x7': ' DoorCtrlTriSrc_Resd1', '0x8': ' DoorCtrlTriSrc_Resd2', '0x9': ' DoorCtrlTriSrc_Resd3'}

    class ActvReSplrStsAvlStsForConLockg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1408
        signal_description = "ActiveWing  Controlled by CenLockg "
        signal_length = 1
        start_position = 1470
        value_definition = {'0x0': ' AvlStsForConLockg_NotAvl', '0x1': ' AvlStsForConLockg_Avl'}

    class ActvReSplrStsCtrldSts2:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1408
        signal_description = "The Trigger Souce of Active Wing "
        signal_length = 2
        start_position = 1469
        value_definition = {'0x0': ' CtrldSts2_NotCtrld', '0x1': ' CtrldSts2_CtrldByCDC', '0x2': ' CtrldSts2_CtrldByCenLockg'}

    class ActvReSplrStsNotAvlEve:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1408
        signal_description = "The Reason why ActiveWing cannot used"
        signal_length = 4
        start_position = 1467
        value_definition = {'0x0': ' NotAvlEve_No', '0x1': ' NotAvlEve_CarMod', '0x2': ' NotAvlEve_UsgMod', '0x3': ' NotAvlEve_MotBlk', '0x4': ' NotAvlEve_IceBreak', '0x5': ' NotAvlEve_Tr', '0x6': ' NotAvlEve_Trlr', '0x7': ' NotAvlEve_SysErr', '0x8': ' NotAvlEve_Reserve2', '0x9': ' NotAvlEve_Reserve3'}

    class ActvReSplrStsAvlStsForCDC:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 1408
        signal_description = "ActiveWing  Controlled by CDC "
        signal_length = 1
        start_position = 1471
        value_definition = {'0x0': ' AvlStsForCDC_NotAvl', '0x1': ' AvlStsForCDC_Avl'}


class LCULToCCUSOCCDEthSignalIPdu05:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x504005
    pdu_length_bytes = 8
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-30ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'DrvStsOfTrlrLePositionLampRear': ['DrvStsOfTrlrLePositionLampRearLightErrorCode', 'DrvStsOfTrlrLePositionLampRearLightSts'], 'DrvStsOfTrlrRearFogLamp': ['DrvStsOfTrlrRearFogLampLightSts', 'DrvStsOfTrlrRearFogLampLightErrorCode'], 'DrvStsOfTrlrRiPositionLampRear': ['DrvStsOfTrlrRiPositionLampRearLightSts', 'DrvStsOfTrlrRiPositionLampRearLightErrorCode']}

    class DrvStsOfTrlrLePositionLampRearLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 35
        signal_description = "Light Error Code"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class DrvStsOfTrlrLePositionLampRearLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 35
        signal_description = "Light Status"
        signal_length = 4
        start_position = 15
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class DrvStsOfTrlrRearFogLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 34
        signal_description = "Light Status"
        signal_length = 4
        start_position = 11
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class DrvStsOfTrlrRearFogLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 34
        signal_description = "Light Error Code"
        signal_length = 8
        start_position = 23
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class DrvStsOfTrlrRiPositionLampRearLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 33
        signal_description = "Light Status"
        signal_length = 4
        start_position = 39
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class DrvStsOfTrlrRiPositionLampRearLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 33
        signal_description = "Light Error Code"
        signal_length = 8
        start_position = 31
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}


class LCULToCCUSOCCDEthSignalIPdu08:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x504008
    pdu_length_bytes = 128
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-50ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'BackLiLocDrvrSideDrvSts': ['BackLiLocDrvrSideDrvStsLightSts', 'BackLiLocDrvrSideDrvStsLiPerc', 'BackLiLocDrvrSideDrvStsLightErrorCode'], 'BackLiLocRearLeDrvSts': ['BackLiLocRearLeDrvStsLightSts', 'BackLiLocRearLeDrvStsLiPerc', 'BackLiLocRearLeDrvStsLightErrorCode'], 'BackLiWinDrvrSideDrvSts': ['BackLiWinDrvrSideDrvStsLightSts', 'BackLiWinDrvrSideDrvStsLiPerc', 'BackLiWinDrvrSideDrvStsLightErrorCode'], 'BackLiWinRearLeDrvSts': ['BackLiWinRearLeDrvStsLightErrorCode', 'BackLiWinRearLeDrvStsLightSts', 'BackLiWinRearLeDrvStsLiPerc'], 'DrvStsOfTrlrRearLeTurnLamp': ['DrvStsOfTrlrRearLeTurnLampLightErrorCode', 'DrvStsOfTrlrRearLeTurnLampLightSts'], 'DrvStsOfTrlrRearRiTurnLamp': ['DrvStsOfTrlrRearRiTurnLampLightSts', 'DrvStsOfTrlrRearRiTurnLampLightErrorCode'], 'DrvStsOfTrlrReverseLamp': ['DrvStsOfTrlrReverseLampLightErrorCode', 'DrvStsOfTrlrReverseLampLightSts'], 'DrvStsOfTrlrStopLamp': ['DrvStsOfTrlrStopLampLightSts', 'DrvStsOfTrlrStopLampLightErrorCode'], 'FuncStsOfHighBeam': ['FuncStsOfHighBeamLightErrorCode', 'FuncStsOfHighBeamLightSts', 'FuncStsOfHighBeamLightPriority'], 'FuncStsOfLicensePlateLamp': ['FuncStsOfLicensePlateLampLightPriority', 'FuncStsOfLicensePlateLampLightSts', 'FuncStsOfLicensePlateLampLightErrorCode'], 'FuncStsOfOuterDoorSwLampFL': ['FuncStsOfOuterDoorSwLampFLLightMode', 'FuncStsOfOuterDoorSwLampFLLightErrorCode', 'FuncStsOfOuterDoorSwLampFLLightPriority'], 'FuncStsOfOuterDoorSwLampFR': ['FuncStsOfOuterDoorSwLampFRLightMode', 'FuncStsOfOuterDoorSwLampFRLightPriority', 'FuncStsOfOuterDoorSwLampFRLightErrorCode'], 'FuncStsOfOuterDoorSwLampRL': ['FuncStsOfOuterDoorSwLampRLLightErrorCode', 'FuncStsOfOuterDoorSwLampRLLightPriority', 'FuncStsOfOuterDoorSwLampRLLightMode'], 'FuncStsOfOuterDoorSwLampRR': ['FuncStsOfOuterDoorSwLampRRLightMode', 'FuncStsOfOuterDoorSwLampRRLightErrorCode', 'FuncStsOfOuterDoorSwLampRRLightPriority'], 'HandsFreeDetnHOD': ['HandsFreeDetnHODHodErrorSts', 'HandsFreeDetnHODCntr', 'HandsFreeDetnHODChks', 'HandsFreeDetnHODHandsOnSts'], 'HzrdWarnSwBackliDrvSts': ['HzrdWarnSwBackliDrvStsLiPerc', 'HzrdWarnSwBackliDrvStsLightErrorCode', 'HzrdWarnSwBackliDrvStsLightSts'], 'SeatAdj1RowLePosn': ['SeatAdj1RowLePosnCLAPos', 'SeatAdj1RowLePosnLengthPos', 'SeatAdj1RowLePosnHeightPos', 'SeatAdj1RowLePosnHeightQf', 'SeatAdj1RowLePosnOTTOAgPos', 'SeatAdj1RowLePosnBackRestQf', 'SeatAdj1RowLePosnTiltPos', 'SeatAdj1RowLePosnReleasePos', 'SeatAdj1RowLePosnTiltQf', 'SeatAdj1RowLePosnCLAQf', 'SeatAdj1RowLePosnOTTOLenQf', 'SeatAdj1RowLePosnLengthQf', 'SeatAdj1RowLePosnReleaseQf', 'SeatAdj1RowLePosnBackRestPos', 'SeatAdj1RowLePosnOTTOAgQf', 'SeatAdj1RowLePosnOTTOLenPos'], 'SeatAdj2RowLePosn': ['SeatAdj2RowLePosnBackRestPos', 'SeatAdj2RowLePosnOTTOAgPos', 'SeatAdj2RowLePosnBackRestQf', 'SeatAdj2RowLePosnLengthQf', 'SeatAdj2RowLePosnHeightQf', 'SeatAdj2RowLePosnCLAQf', 'SeatAdj2RowLePosnReleaseQf', 'SeatAdj2RowLePosnTiltPos', 'SeatAdj2RowLePosnTiltQf', 'SeatAdj2RowLePosnHeightPos', 'SeatAdj2RowLePosnReleasePos', 'SeatAdj2RowLePosnCLAPos', 'SeatAdj2RowLePosnOTTOLenQf', 'SeatAdj2RowLePosnOTTOAgQf', 'SeatAdj2RowLePosnLengthPos', 'SeatAdj2RowLePosnOTTOLenPos'], 'SeatAdj3RowLePosn': ['SeatAdj3RowLePosnOTTOAgQf', 'SeatAdj3RowLePosnReleaseQf', 'SeatAdj3RowLePosnCLAQf', 'SeatAdj3RowLePosnOTTOAgPos', 'SeatAdj3RowLePosnOTTOLenPos', 'SeatAdj3RowLePosnLengthPos', 'SeatAdj3RowLePosnLengthQf', 'SeatAdj3RowLePosnCLAPos', 'SeatAdj3RowLePosnReleasePos', 'SeatAdj3RowLePosnOTTOLenQf', 'SeatAdj3RowLePosnBackRestQf', 'SeatAdj3RowLePosnTiltQf', 'SeatAdj3RowLePosnBackRestPos', 'SeatAdj3RowLePosnHeightPos', 'SeatAdj3RowLePosnTiltPos', 'SeatAdj3RowLePosnHeightQf'], 'SeatLieDwnLeSwtSts': ['SeatLieDwnLeSwtStsPsdNotPsd1', 'SeatLieDwnLeSwtStsFlt'], 'SeatMassgFrntLeRunStsFb': ['SeatMassgFrntLeRunStsFbMassgLvlSts', 'SeatMassgFrntLeRunStsFbOnOffNoCmd', 'SeatMassgFrntLeRunStsFbMassgProg'], 'SeatMassgReLeRunStsFb': ['SeatMassgReLeRunStsFbMassgLvlSts', 'SeatMassgReLeRunStsFbMassgProg', 'SeatMassgReLeRunStsFbOnOffNoCmd'], 'SteerWhlMotSts': ['SteerWhlMotStsMotorSts', 'SteerWhlMotStsSteerWhlCfg'], 'SteerWhlPosn': ['SteerWhlPosnAg', 'SteerWhlPosnLen'], 'TwliBriRaw': ['TwliBriRawTwliBriRaw', 'TwliBriRawQf'], 'FuncStsOfHorn': ['FuncStsOfHornHornSts', 'FuncStsOfHornHornPriority', 'FuncStsOfHornHornErrorCode'], 'SeatAdj1RowLeBtnSts': ['SeatAdj1RowLeBtnStsSeatAdjTiltBtnSts', 'SeatAdj1RowLeBtnStsSeatAdjLenBtnSts', 'SeatAdj1RowLeBtnStsSeatAdjBackBtnSts', 'SeatAdj1RowLeBtnStsSeatAdjOTTOLenBtnSts', 'SeatAdj1RowLeBtnStsSeatAdjOTTOAgBtnSts', 'SeatAdj1RowLeBtnStsSeatAdjHeiBtnSts', 'SeatAdj1RowLeBtnStsSeatAdjCLABtnSts'], 'SeatAdj3RowLeBtnSts': ['SeatAdj3RowLeBtnStsSeatAdjCLABtnSts', 'SeatAdj3RowLeBtnStsSeatAdjLenBtnSts', 'SeatAdj3RowLeBtnStsSeatAdjTiltBtnSts', 'SeatAdj3RowLeBtnStsSeatAdjOTTOAgBtnSts', 'SeatAdj3RowLeBtnStsSeatAdjHeiBtnSts', 'SeatAdj3RowLeBtnStsSeatAdjBackBtnSts', 'SeatAdj3RowLeBtnStsSeatAdjOTTOLenBtnSts'], 'SeatAdj2RowLeBtnSts': ['SeatAdj2RowLeBtnStsSeatAdjLenBtnSts', 'SeatAdj2RowLeBtnStsSeatAdjTiltBtnSts', 'SeatAdj2RowLeBtnStsSeatAdjOTTOLenBtnSts', 'SeatAdj2RowLeBtnStsSeatAdjHeiBtnSts', 'SeatAdj2RowLeBtnStsSeatAdjOTTOAgBtnSts', 'SeatAdj2RowLeBtnStsSeatAdjBackBtnSts', 'SeatAdj2RowLeBtnStsSeatAdjCLABtnSts']}

    class BackLiLocDrvrSideDrvStsLightSts:
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

    class BackLiLocDrvrSideDrvStsLiPerc:
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

    class BackLiLocDrvrSideDrvStsLightErrorCode:
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

    class BackLiLocRearLeDrvStsLightSts:
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

    class BackLiLocRearLeDrvStsLiPerc:
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

    class BackLiLocRearLeDrvStsLightErrorCode:
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

    class BackLiWinDrvrSideDrvStsLightSts:
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

    class BackLiWinDrvrSideDrvStsLiPerc:
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

    class BackLiWinDrvrSideDrvStsLightErrorCode:
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

    class BackLiWinRearLeDrvStsLightErrorCode:
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

    class BackLiWinRearLeDrvStsLightSts:
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

    class BackLiWinRearLeDrvStsLiPerc:
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

    class DrvStsOfTrlrRearLeTurnLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 149
        signal_description = "Light Error Code"
        signal_length = 8
        start_position = 103
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class DrvStsOfTrlrRearLeTurnLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 149
        signal_description = "Light Status"
        signal_length = 4
        start_position = 111
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class DrvStsOfTrlrRearRiTurnLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 148
        signal_description = "Light Status"
        signal_length = 4
        start_position = 107
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class DrvStsOfTrlrRearRiTurnLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 148
        signal_description = "Light Error Code"
        signal_length = 8
        start_position = 119
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class DrvStsOfTrlrReverseLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 147
        signal_description = "Light Error Code"
        signal_length = 8
        start_position = 127
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class DrvStsOfTrlrReverseLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 147
        signal_description = "Light Status"
        signal_length = 4
        start_position = 135
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class DrvStsOfTrlrStopLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 146
        signal_description = "Light Status"
        signal_length = 4
        start_position = 131
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class DrvStsOfTrlrStopLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 146
        signal_description = "Light Error Code"
        signal_length = 8
        start_position = 143
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FLDoorSpdModeFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 145
        signal_description = "power side door mode status feedback"
        signal_length = 2
        start_position = 151
        value_definition = {'0x0': ' SpdMode_Low', '0x1': ' SpdMode_Middle', '0x2': ' SpdMode_High'}

    class FuncStsOfHighBeamLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 171
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 159
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfHighBeamLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 171
        signal_description = "LightSts"
        signal_length = 4
        start_position = 175
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfHighBeamLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 171
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 167
        value_definition = {}

    class FuncStsOfLicensePlateLampLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 195
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 191
        value_definition = {}

    class FuncStsOfLicensePlateLampLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 195
        signal_description = "LightSts"
        signal_length = 4
        start_position = 199
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfLicensePlateLampLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 195
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 183
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfOuterDoorSwLampFLLightMode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 91
        signal_description = "LightMode"
        signal_length = 8
        start_position = 207
        value_definition = {'0x0': ' LightMode_OFF', '0x1': ' LightMode_ON', '0x2': ' LightMode_FLASH', '0x3': ' LightMode_BREATH1', '0x4': ' LightMode_BREATH2', '0x5': ' LightMode_Reserved1', '0xFF': ' LightMode_Reserved'}

    class FuncStsOfOuterDoorSwLampFLLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 91
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 215
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfOuterDoorSwLampFLLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 91
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 223
        value_definition = {}

    class FuncStsOfOuterDoorSwLampFRLightMode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 90
        signal_description = "LightMode"
        signal_length = 8
        start_position = 231
        value_definition = {'0x0': ' LightMode_OFF', '0x1': ' LightMode_ON', '0x2': ' LightMode_FLASH', '0x3': ' LightMode_BREATH1', '0x4': ' LightMode_BREATH2', '0x5': ' LightMode_Reserved1', '0xFF': ' LightMode_Reserved'}

    class FuncStsOfOuterDoorSwLampFRLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 90
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 239
        value_definition = {}

    class FuncStsOfOuterDoorSwLampFRLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 90
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 247
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfOuterDoorSwLampRLLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 89
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 255
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfOuterDoorSwLampRLLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 89
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 263
        value_definition = {}

    class FuncStsOfOuterDoorSwLampRLLightMode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 89
        signal_description = "LightMode"
        signal_length = 8
        start_position = 271
        value_definition = {'0x0': ' LightMode_OFF', '0x1': ' LightMode_ON', '0x2': ' LightMode_FLASH', '0x3': ' LightMode_BREATH1', '0x4': ' LightMode_BREATH2', '0x5': ' LightMode_Reserved1', '0xFF': ' LightMode_Reserved'}

    class FuncStsOfOuterDoorSwLampRRLightMode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 88
        signal_description = "LightMode"
        signal_length = 8
        start_position = 279
        value_definition = {'0x0': ' LightMode_OFF', '0x1': ' LightMode_ON', '0x2': ' LightMode_FLASH', '0x3': ' LightMode_BREATH1', '0x4': ' LightMode_BREATH2', '0x5': ' LightMode_Reserved1', '0xFF': ' LightMode_Reserved'}

    class FuncStsOfOuterDoorSwLampRRLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 88
        signal_description = "ErrorCode"
        signal_length = 8
        start_position = 287
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class FuncStsOfOuterDoorSwLampRRLightPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 88
        signal_description = "LightPriority"
        signal_length = 8
        start_position = 295
        value_definition = {}

    class HandsFreeDetnHODHodErrorSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 144
        signal_description = "errorStatus"
        signal_length = 3
        start_position = 303
        value_definition = {'0x0': ' HodErrorSts_Init', '0x1': ' HodErrorSts_Reserved1', '0x2': ' HodErrorSts_Ready', '0x3': ' HodErrorSts_CUFault', '0x4': ' HodErrorSts_SMFault', '0x5': ' HodErrorSts_SVFault', '0x6': ' HodErrorSts_Reserved2', '0x7': ' HodErrorSts_Reserved3'}

    class HandsFreeDetnHODCntr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 144
        signal_description = "cntr"
        signal_length = 4
        start_position = 300
        value_definition = {}

    class HandsFreeDetnHODChks:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 144
        signal_description = "chks"
        signal_length = 8
        start_position = 311
        value_definition = {}

    class HandsFreeDetnHODHandsOnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 144
        signal_description = "handsOnStatus"
        signal_length = 2
        start_position = 319
        value_definition = {'0x0': ' HandsOnSts_Init', '0x1': ' HandsOnSts_HandsON', '0x2': ' HandsOnSts_HandsOFF', '0x3': ' HandsOnSts_Undetermined'}

    class HornSwtSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 312
        signal_description = "horn switch status"
        signal_length = 1
        start_position = 315
        value_definition = {'0x0': ' PsdNotPsd1_NotPsd', '0x1': ' PsdNotPsd1_Psd'}

    class HzrdWarnSwBackliDrvStsLiPerc:
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

    class HzrdWarnSwBackliDrvStsLightErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 340
        signal_description = "error code"
        signal_length = 8
        start_position = 327
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class HzrdWarnSwBackliDrvStsLightSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 340
        signal_description = "light status"
        signal_length = 4
        start_position = 335
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class SeatAdj1RowLeAntiPinchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 345
        signal_description = "Antipinch Work Status"
        signal_length = 2
        start_position = 469
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class SeatAdj1RowLePosnCLAPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 467
        value_definition = {}

    class SeatAdj1RowLePosnLengthPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 473
        value_definition = {}

    class SeatAdj1RowLePosnHeightPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 495
        value_definition = {}

    class SeatAdj1RowLePosnHeightQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 501
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowLePosnOTTOAgPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 499
        value_definition = {}

    class SeatAdj1RowLePosnBackRestQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 505
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowLePosnTiltPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 519
        value_definition = {}

    class SeatAdj1RowLePosnReleasePos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 525
        value_definition = {}

    class SeatAdj1RowLePosnTiltQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 531
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowLePosnCLAQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 529
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowLePosnOTTOLenQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 543
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowLePosnLengthQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 541
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowLePosnReleaseQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 539
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowLePosnBackRestPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 537
        value_definition = {}

    class SeatAdj1RowLePosnOTTOAgQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 559
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj1RowLePosnOTTOLenPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 344
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 557
        value_definition = {}

    class SeatAdj2RowLeAntiPinchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 359
        signal_description = "Antipinch Work Status"
        signal_length = 2
        start_position = 563
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class SeatAdj2RowLePosnBackRestPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 561
        value_definition = {}

    class SeatAdj2RowLePosnOTTOAgPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 583
        value_definition = {}

    class SeatAdj2RowLePosnBackRestQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 589
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowLePosnLengthQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 587
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowLePosnHeightQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 585
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowLePosnCLAQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 599
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowLePosnReleaseQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 597
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowLePosnTiltPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 595
        value_definition = {}

    class SeatAdj2RowLePosnTiltQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 601
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowLePosnHeightPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 615
        value_definition = {}

    class SeatAdj2RowLePosnReleasePos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 621
        value_definition = {}

    class SeatAdj2RowLePosnCLAPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 627
        value_definition = {}

    class SeatAdj2RowLePosnOTTOLenQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 633
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowLePosnOTTOAgQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 647
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj2RowLePosnLengthPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Motor Position Percentage"
        signal_length = 10
        start_position = 645
        value_definition = {}

    class SeatAdj2RowLePosnOTTOLenPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 358
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 651
        value_definition = {}

    class SeatAdj3RowLeAntiPinchSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 357
        signal_description = "Antipinch Work Status"
        signal_length = 2
        start_position = 657
        value_definition = {'0x0': ' EnableDisable3_Invalid', '0x1': ' EnableDisable3_Disabled', '0x2': ' EnableDisable3_Enabled'}

    class SeatAdj3RowLePosnOTTOAgQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 671
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowLePosnReleaseQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 669
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowLePosnCLAQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 667
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowLePosnOTTOAgPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 665
        value_definition = {}

    class SeatAdj3RowLePosnOTTOLenPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 687
        value_definition = {}

    class SeatAdj3RowLePosnLengthPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Motor Position Percentage"
        signal_length = 10
        start_position = 693
        value_definition = {}

    class SeatAdj3RowLePosnLengthQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 699
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowLePosnCLAPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 697
        value_definition = {}

    class SeatAdj3RowLePosnReleasePos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 719
        value_definition = {}

    class SeatAdj3RowLePosnOTTOLenQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 725
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowLePosnBackRestQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 723
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowLePosnTiltQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 721
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatAdj3RowLePosnBackRestPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 735
        value_definition = {}

    class SeatAdj3RowLePosnHeightPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 741
        value_definition = {}

    class SeatAdj3RowLePosnTiltPos:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Position Percentage"
        signal_length = 10
        start_position = 747
        value_definition = {}

    class SeatAdj3RowLePosnHeightQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 356
        signal_description = "Signal QF"
        signal_length = 2
        start_position = 753
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class SeatLieDwnLeSwtStsPsdNotPsd1:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 355
        signal_description = "Press status"
        signal_length = 1
        start_position = 767
        value_definition = {'0x0': ' PsdNotPsd1_NotPsd', '0x1': ' PsdNotPsd1_Psd'}

    class SeatLieDwnLeSwtStsFlt:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 355
        signal_description = "Fault or not"
        signal_length = 2
        start_position = 766
        value_definition = {'0x0': ' Flt_Initial', '0x1': ' Flt_NoFault', '0x2': ' Flt_Fault'}

    class SeatLumFrntLeRunStsFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 354
        signal_description = "Lumbar Work Status"
        signal_length = 2
        start_position = 764
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class SeatLumReLeRunStsFb:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 353
        signal_description = "Lumbar Work Status"
        signal_length = 2
        start_position = 762
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class SeatMassgEcuFrntLeErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 352
        signal_description = "Massage Module Error Status"
        signal_length = 2
        start_position = 760
        value_definition = {'0x0': ' EcuErrorType_Idle', '0x1': ' EcuErrorType_InternalError', '0x2': ' EcuErrorType_ExternalError', '0x3': ' EcuErrorType_reserved'}

    class SeatMassgEcuReLeErrSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 367
        signal_description = "Massage Module Error Status"
        signal_length = 2
        start_position = 774
        value_definition = {'0x0': ' EcuErrorType_Idle', '0x1': ' EcuErrorType_InternalError', '0x2': ' EcuErrorType_ExternalError', '0x3': ' EcuErrorType_reserved'}

    class SeatMassgFrntLeRunStsFbMassgLvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 366
        signal_description = "Massage Intensity Level Status"
        signal_length = 2
        start_position = 772
        value_definition = {'0x0': ' MassgLvlSts_Idle', '0x1': ' MassgLvlSts_Low', '0x2': ' MassgLvlSts_Mid', '0x3': ' MassgLvlSts_High'}

    class SeatMassgFrntLeRunStsFbOnOffNoCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 366
        signal_description = "Massage Work Status"
        signal_length = 2
        start_position = 770
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class SeatMassgFrntLeRunStsFbMassgProg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 366
        signal_description = "Massage Type"
        signal_length = 3
        start_position = 768
        value_definition = {'0x0': ' MassgProg_Prog0', '0x1': ' MassgProg_Prog1', '0x2': ' MassgProg_Prog2', '0x3': ' MassgProg_Prog3', '0x4': ' MassgProg_Prog4', '0x5': ' MassgProg_Prog5', '0x6': ' MassgProg_Prog6', '0x7': ' MassgProg_Prog7'}

    class SeatMassgReLeRunStsFbMassgLvlSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 365
        signal_description = "Massage Intensity Level Status"
        signal_length = 2
        start_position = 781
        value_definition = {'0x0': ' MassgLvlSts_Idle', '0x1': ' MassgLvlSts_Low', '0x2': ' MassgLvlSts_Mid', '0x3': ' MassgLvlSts_High'}

    class SeatMassgReLeRunStsFbMassgProg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 365
        signal_description = "Massage Type"
        signal_length = 3
        start_position = 779
        value_definition = {'0x0': ' MassgProg_Prog0', '0x1': ' MassgProg_Prog1', '0x2': ' MassgProg_Prog2', '0x3': ' MassgProg_Prog3', '0x4': ' MassgProg_Prog4', '0x5': ' MassgProg_Prog5', '0x6': ' MassgProg_Prog6', '0x7': ' MassgProg_Prog7'}

    class SeatMassgReLeRunStsFbOnOffNoCmd:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 365
        signal_description = "Massage Work Status"
        signal_length = 2
        start_position = 776
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class SteerWhlMotStsMotorSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 364
        signal_description = "Show Motor Status"
        signal_length = 3
        start_position = 790
        value_definition = {'0x0': ' MotorSts_Idle', '0x1': ' MotorSts_RunningUp', '0x2': ' MotorSts_RunningDown', '0x3': ' MotorSts_Stop', '0x4': ' MotorSts_Error', '0x5': ' MotorSts_Reserved1', '0x6': ' MotorSts_Reserved2', '0x7': ' MotorSts_Reserved3'}

    class SteerWhlMotStsSteerWhlCfg:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 364
        signal_description = "Show SteerWhl Config"
        signal_length = 2
        start_position = 787
        value_definition = {'0x0': ' SteerWhlCfg_Idle', '0x1': ' SteerWhlCfg_SteerWhlLen', '0x2': ' SteerWhlCfg_SteerWhlAg', '0x3': ' SteerWhlCfg_Reserved'}

    class SteerWhlPosnAg:
        comments = ""
        factor = 0.01
        initial_value = 2048
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -20
        sig_ub = 363
        signal_description = "SteerWheel Position On Angle"
        signal_length = 12
        start_position = 785
        value_definition = {}

    class SteerWhlPosnLen:
        comments = ""
        factor = 0.1
        initial_value = 2048
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = -204
        sig_ub = 363
        signal_description = "SteerWheel Position On Length"
        signal_length = 12
        start_position = 805
        value_definition = {}

    class TwliBriRawTwliBriRaw:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 362
        signal_description = "the value of the ambient ligth intensity,from RLSM"
        signal_length = 14
        start_position = 809
        value_definition = {}

    class TwliBriRawQf:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 362
        signal_description = "the quality factor of the ambient ligth intensity,from RLSM"
        signal_length = 2
        start_position = 827
        value_definition = {'0x0': ' GenQf1_UndefindDataAccur', '0x1': ' GenQf1_TmpUndefdData', '0x2': ' GenQf1_DataAccurNotWithinSpcn', '0x3': ' GenQf1_AccurData'}

    class WinDrvrPosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 361
        signal_description = "Window Position Feedback"
        signal_length = 5
        start_position = 825
        value_definition = {'0x0': ' PosnPerc_Idle', '0x1': ' PosnPerc_PosnPercUnknow', '0x2': ' PosnPerc_PosnPercFullCls', '0x3': ' PosnPerc_PosnPerc4', '0x4': ' PosnPerc_PosnPerc8', '0x5': ' PosnPerc_PosnPerc12', '0x6': ' PosnPerc_PosnPerc16', '0x7': ' PosnPerc_PosnPerc20', '0x8': ' PosnPerc_PosnPerc24', '0x9': ' PosnPerc_PosnPerc28', '0xA': ' PosnPerc_PosnPerc32', '0xB': ' PosnPerc_PosnPerc36', '0xC': ' PosnPerc_PosnPerc40', '0xD': ' PosnPerc_PosnPerc44', '0xE': ' PosnPerc_PosnPerc48', '0xF': ' PosnPerc_PosnPerc52', '0x10': ' PosnPerc_PosnPerc56', '0x11': ' PosnPerc_PosnPerc60', '0x12': ' PosnPerc_PosnPerc64', '0x13': ' PosnPerc_PosnPerc68', '0x14': ' PosnPerc_PosnPerc72', '0x15': ' PosnPerc_PosnPerc76', '0x16': ' PosnPerc_PosnPerc80', '0x17': ' PosnPerc_PosnPerc84', '0x18': ' PosnPerc_PosnPerc88', '0x19': ' PosnPerc_PosnPerc92', '0x1A': ' PosnPerc_PosnPerc96', '0x1B': ' PosnPerc_FullOpen', '0x1C': ' PosnPerc_Reserved1', '0x1D': ' PosnPerc_Reserved2', '0x1E': ' PosnPerc_Reserved3'}

    class WinDrvrRvsInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 375
        signal_description = "Window Antipinch Reverse Happened or Not"
        signal_length = 2
        start_position = 845
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class WinDrvrShoMoveSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 374
        signal_description = "Window Short Move Status"
        signal_length = 3
        start_position = 843
        value_definition = {'0x0': ' WinShoSts_Idle', '0x1': ' WinShoSts_ShoUping', '0x2': ' WinShoSts_ShoUp', '0x3': ' WinShoSts_ShoDwning', '0x4': ' WinShoSts_ShoDwn', '0x5': ' WinShoSts_Reserved'}

    class WinReLePosn:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 373
        signal_description = "Window Position Feedback"
        signal_length = 5
        start_position = 840
        value_definition = {'0x0': ' PosnPerc_Idle', '0x1': ' PosnPerc_PosnPercUnknow', '0x2': ' PosnPerc_PosnPercFullCls', '0x3': ' PosnPerc_PosnPerc4', '0x4': ' PosnPerc_PosnPerc8', '0x5': ' PosnPerc_PosnPerc12', '0x6': ' PosnPerc_PosnPerc16', '0x7': ' PosnPerc_PosnPerc20', '0x8': ' PosnPerc_PosnPerc24', '0x9': ' PosnPerc_PosnPerc28', '0xA': ' PosnPerc_PosnPerc32', '0xB': ' PosnPerc_PosnPerc36', '0xC': ' PosnPerc_PosnPerc40', '0xD': ' PosnPerc_PosnPerc44', '0xE': ' PosnPerc_PosnPerc48', '0xF': ' PosnPerc_PosnPerc52', '0x10': ' PosnPerc_PosnPerc56', '0x11': ' PosnPerc_PosnPerc60', '0x12': ' PosnPerc_PosnPerc64', '0x13': ' PosnPerc_PosnPerc68', '0x14': ' PosnPerc_PosnPerc72', '0x15': ' PosnPerc_PosnPerc76', '0x16': ' PosnPerc_PosnPerc80', '0x17': ' PosnPerc_PosnPerc84', '0x18': ' PosnPerc_PosnPerc88', '0x19': ' PosnPerc_PosnPerc92', '0x1A': ' PosnPerc_PosnPerc96', '0x1B': ' PosnPerc_FullOpen', '0x1C': ' PosnPerc_Reserved1', '0x1D': ' PosnPerc_Reserved2', '0x1E': ' PosnPerc_Reserved3'}

    class WinReLeRvsInfo:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 371
        signal_description = "Window Antipinch Reverse Happened or Not"
        signal_length = 2
        start_position = 860
        value_definition = {'0x0': ' OffOnNoCmd_NoCmd', '0x1': ' OffOnNoCmd_Off', '0x2': ' OffOnNoCmd_On'}

    class WinReLeShoMoveSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 370
        signal_description = "Window Short Move Status"
        signal_length = 3
        start_position = 858
        value_definition = {'0x0': ' WinShoSts_Idle', '0x1': ' WinShoSts_ShoUping', '0x2': ' WinShoSts_ShoUp', '0x3': ' WinShoSts_ShoDwning', '0x4': ' WinShoSts_ShoDwn', '0x5': ' WinShoSts_Reserved'}

    class ExtrReViewMirrFoldSrcDrvr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 368
        signal_description = ""
        signal_length = 5
        start_position = 869
        value_definition = {'0x0': ' ReViewMirrFoldSrc_IniValue', '0x1': ' ReViewMirrFoldSrc_AutoCtrl', '0x2': ' ReViewMirrFoldSrc_ManCtrl', '0x3': ' ReViewMirrFoldSrc_RemCtrl', '0x4': ' ReViewMirrFoldSrc_VehSpdUnfold', '0x5': ' ReViewMirrFoldSrc_Others'}

    class ReViewMirrDimEnaSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 194
        signal_description = "后视镜防眩目使能状态"
        signal_length = 2
        start_position = 193
        value_definition = {'0x0': ' OnOffNoCmd_NoCmd', '0x1': ' OnOffNoCmd_OFF', '0x2': ' OnOffNoCmd_ON'}

    class ExtrReViewMirrAutoFoldEnaStsDrvr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 369
        signal_description = "外后视镜自动折叠使能状态"
        signal_length = 2
        start_position = 871
        value_definition = {'0x0': ' MirrAutoEn_Idle', '0x1': ' MirrAutoEn_EnableBoth', '0x2': ' MirrAutoEn_EnableFoldOnly', '0x3': ' MirrAutoEn_EnableUnfoldOnly', '0x4': ' MirrAutoEn_Disable'}

    class DriverReViewMirrDimFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 170
        signal_description = "主驾侧后视镜防眩光故障"
        signal_length = 2
        start_position = 169
        value_definition = {'0x0': ' IntrReViewMirrDimFailr_NoFault', '0x1': ' IntrReViewMirrDimFailr_InternalFailure', '0x2': ' IntrReViewMirrDimFailr_Reserved1', '0x3': ' IntrReViewMirrDimFailr_Reserved2'}

    class FuncStsOfHornHornSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "horn status"
        signal_length = 4
        start_position = 895
        value_definition = {'0x0': ' LightSts_Off', '0x1': ' LightSts_On', '0x2': ' LightSts_Error', '0x3': ' LightSts_Reserved'}

    class FuncStsOfHornHornPriority:
        comments = ""
        factor = 1.0
        initial_value = 255
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "Horn priority"
        signal_length = 8
        start_position = 887
        value_definition = {}

    class FuncStsOfHornHornErrorCode:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 864
        signal_description = "horn status"
        signal_length = 8
        start_position = 879
        value_definition = {'0x0': ' LightErrorCode_ChipError', '0x1': ' LightErrorCode_ShortError', '0x2': ' LightErrorCode_OpenError', '0xFF': ' LightErrorCode_NoneError'}

    class IntrReViewMirrDimFailr:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 17
        signal_description = "内后视镜防眩目故障状态"
        signal_length = 2
        start_position = 19
        value_definition = {'0x0': ' IntrReViewMirrDimFailr_NoFault', '0x1': ' IntrReViewMirrDimFailr_InternalFailure', '0x2': ' IntrReViewMirrDimFailr_Reserved1', '0x3': ' IntrReViewMirrDimFailr_Reserved2'}

    class SeatAdj1RowLeBtnStsSeatAdjTiltBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 914
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 917
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowLeBtnStsSeatAdjLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 914
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 910
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowLeBtnStsSeatAdjBackBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 914
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 903
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowLeBtnStsSeatAdjOTTOLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 914
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 904
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowLeBtnStsSeatAdjOTTOAgBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 914
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 907
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowLeBtnStsSeatAdjHeiBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 914
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 897
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj1RowLeBtnStsSeatAdjCLABtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 914
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 900
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowLeBtnStsSeatAdjCLABtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 962
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 948
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowLeBtnStsSeatAdjLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 962
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 958
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowLeBtnStsSeatAdjTiltBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 962
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 965
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowLeBtnStsSeatAdjOTTOAgBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 962
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 955
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowLeBtnStsSeatAdjHeiBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 962
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 945
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowLeBtnStsSeatAdjBackBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 962
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 951
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj3RowLeBtnStsSeatAdjOTTOLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 962
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 952
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowLeBtnStsSeatAdjLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 938
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 934
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowLeBtnStsSeatAdjTiltBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 938
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 941
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowLeBtnStsSeatAdjOTTOLenBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 938
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 928
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowLeBtnStsSeatAdjHeiBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 938
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 921
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowLeBtnStsSeatAdjOTTOAgBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 938
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 931
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowLeBtnStsSeatAdjBackBtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 938
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 927
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}

    class SeatAdj2RowLeBtnStsSeatAdjCLABtnSts:
        comments = ""
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 938
        signal_description = "seat button sts"
        signal_length = 3
        start_position = 924
        value_definition = {'0x0': ' SeatDir_Idle', '0x1': ' SeatDir_Up_Fwd_ReleaseOn', '0x2': ' SeatDir_Dwn_Backw_ReleaseOff', '0x3': ' SeatDir_Fault', '0x4': ' SeatDir_Reserved2', '0x5': ' SeatDir_Reserved3', '0x6': ' SeatDir_Reserved4', '0x7': ' SeatDir_Reserved5'}


class LCULToCCUSOCCDEthSignalIPdu09:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x504009
    pdu_length_bytes = 1
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-80ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {}

    class SwitchBackLightingModSts:
        comments = ""
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 5
        signal_description = "mode status feedback"
        signal_length = 2
        start_position = 7
        value_definition = {'0x0': ' IntrLampSelnMod_NoCmd', '0x1': ' IntrLampSelnMod_OFF', '0x2': ' IntrLampSelnMod_ON', '0x3': ' IntrLampSelnMod_AUTO'}


class LCULToCCUSOCCDEthSignalIPdu10:
    base_type = "Unsigned"
    client_socket = "SocketCdSocSoAdUDP"
    pdu_header_id = 0x50400A
    pdu_length_bytes = 64
    receiver = ['CCUSOCCD']
    send_type = "Cyclic-10ms"
    sender = "LCUL"
    server_socket = "SocketLcuLSoAdUDP"
    signal_group = {'PwrChLeCurrVal': ['PwrChLeCurrValSwilPwrChLe8CurrVal', 'PwrChLeCurrValSwilPwrChLe17CurrVal', 'PwrChLeCurrValSwilPwrChLe26CurrVal', 'PwrChLeCurrValSwilPwrChLe15CurrVal', 'PwrChLeCurrValSwilPwrChLe13CurrVal', 'PwrChLeCurrValContnsPwrChLe2CurrVal', 'PwrChLeCurrValSwilPwrChLe9CurrVal', 'PwrChLeCurrValContnsPwrChLe4CurrVal', 'PwrChLeCurrValContnsPwrChLe1CurrVal', 'PwrChLeCurrValSwilPwrChLe20CurrVal', 'PwrChLeCurrValContnsPwrChLe5CurrVal', 'PwrChLeCurrValSwilPwrChLe21CurrVal', 'PwrChLeCurrValSwilPwrChLe14CurrVal', 'PwrChLeCurrValSwilPwrChLe6CurrVal', 'PwrChLeCurrValSwilPwrChLe1CurrVal', 'PwrChLeCurrValSwilPwrChLe16CurrVal', 'PwrChLeCurrValSwilPwrChLe27CurrVal', 'PwrChLeCurrValSwilPwrChLe10CurrVal', 'PwrChLeCurrValSwilPwrChLe19CurrVal', 'PwrChLeCurrValSwilPwrChLe5CurrVal', 'PwrChLeCurrValSwilPwrChLe11CurrVal', 'PwrChLeCurrValSwilPwrChLe4CurrVal', 'PwrChLeCurrValSwilPwrChLe2CurrVal', 'PwrChLeCurrValSwilPwrChLe28CurrVal', 'PwrChLeCurrValSwilPwrChLe24CurrVal', 'PwrChLeCurrValSwilPwrChLe25CurrVal', 'PwrChLeCurrValSwilPwrChLe7CurrVal', 'PwrChLeCurrValSwilPwrChLe12CurrVal', 'PwrChLeCurrValSwilPwrChLe3CurrVal', 'PwrChLeCurrValSwilPwrChLe22CurrVal', 'PwrChLeCurrValContnsPwrChLe3CurrVal', 'PwrChLeCurrValSwilPwrChLe29CurrVal', 'PwrChLeCurrValSwilPwrChLe23CurrVal', 'PwrChLeCurrValSwilPwrChLe18CurrVal']}

    class PwrChLeCurrValSwilPwrChLe8CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 8 Current Value"
        signal_length = 12
        start_position = 7
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe17CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 17 Current Value"
        signal_length = 12
        start_position = 11
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe26CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 26 Current Value"
        signal_length = 12
        start_position = 31
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe15CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 15 Current Value"
        signal_length = 12
        start_position = 35
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe13CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 13 Current Value"
        signal_length = 12
        start_position = 55
        value_definition = {}

    class PwrChLeCurrValContnsPwrChLe2CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Contns Power Channel 2 Current Value"
        signal_length = 12
        start_position = 59
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe9CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 9 Current Value"
        signal_length = 12
        start_position = 79
        value_definition = {}

    class PwrChLeCurrValContnsPwrChLe4CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Contns Power Channel 4 Current Value"
        signal_length = 12
        start_position = 83
        value_definition = {}

    class PwrChLeCurrValContnsPwrChLe1CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Contns Power Channel 1 Current Value"
        signal_length = 12
        start_position = 103
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe20CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 20 Current Value"
        signal_length = 12
        start_position = 107
        value_definition = {}

    class PwrChLeCurrValContnsPwrChLe5CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Contns Power Channel 5 Current Value"
        signal_length = 12
        start_position = 127
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe21CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 21 Current Value"
        signal_length = 12
        start_position = 131
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe14CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 14 Current Value"
        signal_length = 12
        start_position = 151
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe6CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 6 Current Value"
        signal_length = 12
        start_position = 155
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe1CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 1 Current Value"
        signal_length = 12
        start_position = 175
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe16CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 16 Current Value"
        signal_length = 12
        start_position = 179
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe27CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 27 Current Value"
        signal_length = 12
        start_position = 199
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe10CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 10 Current Value"
        signal_length = 12
        start_position = 203
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe19CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 19 Current Value"
        signal_length = 12
        start_position = 223
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe5CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 5 Current Value"
        signal_length = 12
        start_position = 227
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe11CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 11 Current Value"
        signal_length = 12
        start_position = 247
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe4CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 4 Current Value"
        signal_length = 12
        start_position = 251
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe2CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 2 Current Value"
        signal_length = 12
        start_position = 271
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe28CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 28 Current Value"
        signal_length = 12
        start_position = 275
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe24CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 24 Current Value"
        signal_length = 12
        start_position = 295
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe25CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 25 Current Value"
        signal_length = 12
        start_position = 299
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe7CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 7 Current Value"
        signal_length = 12
        start_position = 319
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe12CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 12 Current Value"
        signal_length = 12
        start_position = 323
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe3CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 3 Current Value"
        signal_length = 12
        start_position = 343
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe22CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 22 Current Value"
        signal_length = 12
        start_position = 347
        value_definition = {}

    class PwrChLeCurrValContnsPwrChLe3CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Contns Power Channel 3 Current Value"
        signal_length = 12
        start_position = 367
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe29CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 29 Current Value"
        signal_length = 12
        start_position = 371
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe23CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 23 Current Value"
        signal_length = 12
        start_position = 391
        value_definition = {}

    class PwrChLeCurrValSwilPwrChLe18CurrVal:
        comments = ""
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        sig_ub = 415
        signal_description = "Left Zone Swil Power Channel 18 Current Value"
        signal_length = 12
        start_position = 395
        value_definition = {}
