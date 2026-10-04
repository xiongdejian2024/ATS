

class BGMIntEthPDU0001:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 1
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class UsgModKeeperReq:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "使用模式设置"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'UsgModSts1_UsgModAbdnd', '0x1': 'UsgModSts1_UsgModInActv', '0x2': 'UsgModSts1_UsgModCnvinc', '0xB': 'UsgModSts1_UsgModActv', '0xD': 'UsgModSts1_UsgModDrvg'}


class BGMIntEthPDU0002:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 2
    pdu_length_bytes = 9
    receiver = "SoC"
    send_type = "Cyclic-200ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'UsgModKeeperRsp': ['UsgModKeeperRspStatus', 'UsgModKeeperRspKeyIssue', 'UsgModKeeperRspStaticIssue', 'UsgModKeeperRspPreStatusIssue', 'UsgModKeeperRspEngstIssue', 'UsgModKeeperRspImobIssue', 'UsgModKeeperRspInputArbitrationIssue', 'UsgModKeeperRspCCIssue', 'UsgModKeeperRspUsgModSts1']}

    class UsgModKeeperRspStatus:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "使用模式设置反馈"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModKeeperRspKeyIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "钥匙验证通过情况"
        signal_length = 8
        start_position = 15
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModKeeperRspStaticIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "车辆静止条件验证通过情况"
        signal_length = 8
        start_position = 23
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModKeeperRspPreStatusIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "前置条件验证通过情况"
        signal_length = 8
        start_position = 31
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModKeeperRspEngstIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "电机状态验证通过情况"
        signal_length = 8
        start_position = 39
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModKeeperRspImobIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Imo验证通过情况"
        signal_length = 8
        start_position = 47
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModKeeperRspInputArbitrationIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "转向锁定验证通过情况"
        signal_length = 8
        start_position = 55
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModKeeperRspCCIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "车辆配置验证通过情况"
        signal_length = 8
        start_position = 63
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModKeeperRspUsgModSts1:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "仲裁成功的客户端模式请求"
        signal_length = 4
        start_position = 67
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}


class BGMIntEthPDU0003:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 3
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class UsgModDwnSwtReq:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "强制切换到Inactive模式"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'UsgModSts1_UsgModAbdnd', '0x1': 'UsgModSts1_UsgModInActv', '0x2': 'UsgModSts1_UsgModCnvinc', '0xB': 'UsgModSts1_UsgModActv', '0xD': 'UsgModSts1_UsgModDrvg'}


class BGMIntEthPDU0004:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 4
    pdu_length_bytes = 6
    receiver = "SoC"
    send_type = "Cyclic-200ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'UsgModDwnSwtRsp': ['UsgModDwnSwtRspStatus', 'UsgModDwnSwtRspKeyIssue', 'UsgModDwnSwtRspStaticIssue', 'UsgModDwnSwtRspPreStatusIssue', 'UsgModDwnSwtRspCCIssue', 'UsgModDwnSwtRspUsgModSts1']}

    class UsgModDwnSwtRspStatus:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "使用模式设置反馈"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModDwnSwtRspKeyIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "钥匙验证通过情况"
        signal_length = 8
        start_position = 15
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModDwnSwtRspStaticIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "车辆静止条件验证通过情况"
        signal_length = 8
        start_position = 23
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModDwnSwtRspPreStatusIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "前置条件验证通过情况"
        signal_length = 8
        start_position = 31
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModDwnSwtRspCCIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "车辆配置验证通过情况"
        signal_length = 8
        start_position = 39
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class UsgModDwnSwtRspUsgModSts1:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "仲裁成功的客户端模式请求"
        signal_length = 4
        start_position = 43
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}


class BGMIntEthPDU0005:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 5
    pdu_length_bytes = 5
    receiver = "SoC"
    send_type = "Cyclic-100ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class IgnRlyCmdActr:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "IGN Relay当前的状态"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffSafe1_OnOffSafeInvld1', '0x1': 'OnOffSafe1_OnOffSafeOn', '0x2': 'OnOffSafe1_OnOffSafeOff', '0x3': 'OnOffSafe1_OnOffSafeInvld2'}

    class RlyPwrDistbnCmd1WdIgnRlyExtCmd:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "IGN Relay Extend当前的状态"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class RlyPwrCmd:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Power Outlet Relay当前的状态"
        signal_length = 1
        start_position = 16
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class RlyPwrDistbnCmd1WdBattSaveCmd:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Battery SaverRelay当前的状态"
        signal_length = 1
        start_position = 24
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class IgnRly3Cmd:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "KL15_3 Relay当前的状态"
        signal_length = 1
        start_position = 32
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU0006:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class BevPwrCtrl:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "下高压请求"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU0007:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 7
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class PrkgCmftModTiCtrl:
        comments = "MCU SWC接收;底层软件需要配置信号路由"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "维持在Convenience模式的时长"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU0008:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 8
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class AudWarnActv:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "未驻车相关的音频提醒的触发情况"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'NoYesCrit1_NotVld1', '0x1': 'NoYesCrit1_No', '0x2': 'NoYesCrit1_Yes', '0x3': 'NoYesCrit1_NotVld2'}


class BGMIntEthPDU0009:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 9
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class PasAlrmDeactvnReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "临时禁用开关On、Off"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU0010:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class AntithftRednReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "设防降级开关On、Off"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU0011:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 11
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-500ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class FOTAStatus:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "FOTA状态"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': 'Idle', '0x1': 'Query', '0x2': 'Downloading', '0x3': 'Active', '0x4': 'Update', '0x5': 'Rollback', '0x6': 'UpdateFailNotDriving'}


class BGMIntEthPDU0013:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 13
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class CarModChgReq:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 4
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "车辆模式请求"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': 'CarModeReq_NORMAL', '0x1': 'CarModeReq_TRANSPORT', '0x2': 'CarModeReq_FACTORY', '0x3': 'CarModeReq_CRASH', '0x4': 'CarModeReq_IDLE', '0x5': 'CarModeReq_DYNO'}


class BGMIntEthPDU0014:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 14
    pdu_length_bytes = 4
    receiver = "SoC"
    send_type = "Cyclic-200ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'CarModChgRsp': ['CarModChgRspAlrmIssue', 'CarModChgRspCarModSts1', 'CarModChgRspStaticIssue', 'CarModChgRspStatus']}

    class CarModChgRspAlrmIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "使用模式设置反馈"
        signal_length = 8
        start_position = 7
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class CarModChgRspCarModSts1:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "车辆静止条件验证通过情况"
        signal_length = 3
        start_position = 10
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class CarModChgRspStaticIssue:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "前置条件验证通过情况"
        signal_length = 8
        start_position = 23
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}

    class CarModChgRspStatus:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "发送请求的Car mode"
        signal_length = 8
        start_position = 31
        value_definition = {'0x0': 'Status_Idle', '0x1': 'Status_Failure', '0x2': 'Status_Succeed'}


class BGMIntEthPDU0015:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class LocalBookChrgnTarVal:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "充电目标SOC设置"
        signal_length = 10
        start_position = 1
        value_definition = {}


class BGMIntEthPDU0016:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 16
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ChrgSoftSwCtrlSt:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "充电状态设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU0017:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 17
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HVActvForProxy:
        comments = "MCU SWC接收;底层软件需要配置信号路由"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "请求的高压状态"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU0018:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 18
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class MaintainBattTCtrl:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "电池维温设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU0019:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 19
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class WirelschrgActvReqFromHmi:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "无线充电控制参数"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU0020:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 20
    pdu_length_bytes = 5
    receiver = "SoC"
    send_type = "Cyclic-50ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class BattSoc2Sts:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "小电池状态"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'BattSocSts_Larger15Per', '0x1': 'BattSocSts_LessOrEqual15Per', '0x2': 'BattSocSts_LessOrEqual10Per', '0x3': 'BattSocSts_Invalid'}

    class BattSocRaw2:
        comments = "MCU SWC发送"
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "小电池SOC值"
        signal_length = 10
        start_position = 9
        value_definition = {}

    class BattSohRaw2:
        comments = "MCU SWC发送"
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "小电池SOH值"
        signal_length = 10
        start_position = 25
        value_definition = {}


class BGMIntEthPDU0021:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 21
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class PrkgAssiSysRemPrkgSts:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "无钥匙场景的Usagemode切换请求"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'PrkgAssiSysRemPrkgSts_OFF', '0x1': 'PrkgAssiSysRemPrkgSts_Remoteparkinstandby', '0x2': 'PrkgAssiSysRemPrkgSts_Remoteparkoutstandby', '0x3': 'PrkgAssiSysRemPrkgSts_Searching', '0x4': 'PrkgAssiSysRemPrkgSts_Remoteparkinpreactive', '0x5': 'PrkgAssiSysRemPrkgSts_Remoteparkactive', '0x6': 'PrkgAssiSysRemPrkgSts_Parkprocessactive', '0x7': 'PrkgAssiSysRemPrkgSts_Suspend', '0x8': 'PrkgAssiSysRemPrkgSts_Abort', '0x9': 'PrkgAssiSysRemPrkgSts_Remoteparkprocesscompleted', '0xA': 'PrkgAssiSysRemPrkgSts_Remoteparkoutprocscompleted', '0xB': 'PrkgAssiSysRemPrkgSts_Remoteparkcompleted', '0xC': 'PrkgAssiSysRemPrkgSts_Quit', '0xD': 'PrkgAssiSysRemPrkgSts_Failure', '0xE': 'PrkgAssiSysRemPrkgSts_Cancel'}


class BGMIntEthPDU0022:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 22
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class RemHvBattHeatgReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "电池加热开关设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'RemHvBattHeatgReq_OFF', '0x1': 'RemHvBattHeatgReq_ON'}

    class RemHvBattHeatgTarT:
        comments = "底层软件需配置信号路由；"
        factor = 0.5
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = -40
        signal_description = "电池加热目标温度"
        signal_length = 8
        start_position = 15
        value_definition = {}


class BGMIntEthPDU0023:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 23
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class BookChrgSetReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Book charging Setting Request"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU0024:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 24
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class StopBookChrgnReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "cancel reservation charging request "
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'ReqSts1_NotReqd', '0x1': 'ReqSts1_Reqd'}


class BGMIntEthPDU0025:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 25
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class BookChrgnActvdReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Book Charging ACtivted Request"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU0026:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 26
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class BookStopTiAchieved:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Stop charging time Achieved"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU0027:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 27
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class RemLvBattSocSet:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "远程低压电池SOC开关设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'RemLvBattSocSet_NoRequest', '0x1': 'RemLvBattSocSet_RemLvBattSocSetOn', '0x2': 'RemLvBattSocSet_RemLvBattSocSetOff', '0x3': 'RemLvBattSocSet_Invalid'}

    class RemLvBattSocStsSet:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "远程低压电池SOC状态设置"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'RemLvBattSocStsSet_Larger15Per', '0x1': 'RemLvBattSocStsSet_LessOrEqual15Per', '0x2': 'RemLvBattSocStsSet_LessOfEqual10Per', '0x3': 'RemLvBattSocStsSet_Invalid'}

    class RemLvBattSocSetVal:
        comments = "MCU SWC接收"
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "远程低压电池SOC设置"
        signal_length = 10
        start_position = 17
        value_definition = {}


class BGMIntEthPDU0028:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 28
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'LocalBookStrtTiChrgnTmr': ['LocalBookStrtTiChrgnTmrChrgnTmrmin', 'LocalBookStrtTiChrgnTmrChrgnTmrhour'], 'LocalBookStopTiChrgnTmr': ['LocalBookStopTiChrgnTmrChrgnTmrmin', 'LocalBookStopTiChrgnTmrChrgnTmrhour']}

    class LocalBookStrtTiChrgnTmrChrgnTmrmin:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 60
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "本地预约充电开始时间_分"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class LocalBookStopTiChrgnTmrChrgnTmrmin:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 60
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "本地预约充电开始时间_分"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class LocalBookStrtTiChrgnTmrChrgnTmrhour:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 24
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "本地预约充电开始时间_时"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class LocalBookStopTiChrgnTmrChrgnTmrhour:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 24
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "本地预约充电开始时间_时"
        signal_length = 8
        start_position = 23
        value_definition = {}


class BGMIntEthPDU3006:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 3006
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class StartInhibitReq:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "车辆禁止启动命令"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU3007:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 3007
    pdu_length_bytes = 1
    receiver = "SoC"
    send_type = "Cyclic-200ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class StartInhibitSts:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "车辆禁止启动"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU3008:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 3008
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class BattSaveRlyProxyReq:
        comments = "MCU SWC接收;底层软件需要配置信号路由"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "控制BattSaver继电器闭合"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5001:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5001
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiClimaFrntAutReq:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "前排空调Auto模式设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5002:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5002
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiClimaReAutReq:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "后排空调Auto模式设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5003:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5003
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiCmptmtCoolgReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "制冷模式设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'HmiCmptmtCoolgReq_Off', '0x1': 'HmiCmptmtCoolgReq_Auto'}


class BGMIntEthPDU5004:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5004
    pdu_length_bytes = 8
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HmiCmptmtTSp': ['HmiCmptmtTSpForRowFirstLe', 'HmiCmptmtTSpForRowFirstRi', 'HmiCmptmtTSpForRowSecLe', 'HmiCmptmtTSpForRowSecRi', 'HmiCmptmtTSpSpclForRowFirstLe', 'HmiCmptmtTSpSpclForRowFirstRi', 'HmiCmptmtTSpSpclForRowSecLe', 'HmiCmptmtTSpSpclForRowSecRi']}

    class HmiCmptmtTSpForRowFirstLe:
        comments = "底层软件需配置信号路由；"
        factor = 0.5
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 15
        signal_description = "空调温度调节前左温度值"
        signal_length = 5
        start_position = 4
        value_definition = {}

    class HmiCmptmtTSpForRowFirstRi:
        comments = "底层软件需配置信号路由；"
        factor = 0.5
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 15
        signal_description = "空调温度调节前右温度值"
        signal_length = 5
        start_position = 20
        value_definition = {}

    class HmiCmptmtTSpForRowSecLe:
        comments = "底层软件需配置信号路由；"
        factor = 0.5
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 15
        signal_description = "空调温度调节后左温度值"
        signal_length = 5
        start_position = 36
        value_definition = {}

    class HmiCmptmtTSpForRowSecRi:
        comments = "底层软件需配置信号路由；"
        factor = 0.5
        initial_value = 14
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 15
        signal_description = "空调温度调节后右温度值"
        signal_length = 5
        start_position = 52
        value_definition = {}

    class HmiCmptmtTSpSpclForRowFirstLe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "空调温度调节前左高中低"
        signal_length = 2
        start_position = 9
        value_definition = {}

    class HmiCmptmtTSpSpclForRowFirstRi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "空调温度调节前右高中低"
        signal_length = 2
        start_position = 25
        value_definition = {}

    class HmiCmptmtTSpSpclForRowSecLe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "空调温度调节后左高中低"
        signal_length = 2
        start_position = 41
        value_definition = {}

    class HmiCmptmtTSpSpclForRowSecRi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "空调温度调节后右高中低"
        signal_length = 2
        start_position = 57
        value_definition = {}


class BGMIntEthPDU5008:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5008
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiHvacFanLvlFrnt:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "前排风速设置"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'HmiHvacFanLvl_Off', '0x1': 'HmiHvacFanLvl_LvlMan1', '0x2': 'HmiHvacFanLvl_LvlMan2', '0x3': 'HmiHvacFanLvl_LvlMan3', '0x4': 'HmiHvacFanLvl_LvlMan4', '0x5': 'HmiHvacFanLvl_LvlMan5', '0x6': 'HmiHvacFanLvl_LvlMan6', '0x7': 'HmiHvacFanLvl_LvlMan7', '0x8': 'HmiHvacFanLvl_LvlMan8', '0x9': 'HmiHvacFanLvl_LvlMan9', '0xA': 'HmiHvacFanLvl_LvlAutMinusMinus', '0xB': 'HmiHvacFanLvl_LvlAutMinus', '0xC': 'HmiHvacFanLvl_LvlAutNorm', '0xD': 'HmiHvacFanLvl_LvlAutPlus', '0xE': 'HmiHvacFanLvl_LvlAutPlusPlus', '0xF': 'HmiHvacFanLvl_Reserved'}


class BGMIntEthPDU5009:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5009
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiHvacFanLvlRe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "后排风速设置"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'HmiHvacFanLvl_Off', '0x1': 'HmiHvacFanLvl_LvlMan1', '0x2': 'HmiHvacFanLvl_LvlMan2', '0x3': 'HmiHvacFanLvl_LvlMan3', '0x4': 'HmiHvacFanLvl_LvlMan4', '0x5': 'HmiHvacFanLvl_LvlMan5', '0x6': 'HmiHvacFanLvl_LvlMan6', '0x7': 'HmiHvacFanLvl_LvlMan7', '0x8': 'HmiHvacFanLvl_LvlMan8', '0x9': 'HmiHvacFanLvl_LvlMan9', '0xA': 'HmiHvacFanLvl_LvlAutMinusMinus', '0xB': 'HmiHvacFanLvl_LvlAutMinus', '0xC': 'HmiHvacFanLvl_LvlAutNorm', '0xD': 'HmiHvacFanLvl_LvlAutPlus', '0xE': 'HmiHvacFanLvl_LvlAutPlusPlus', '0xF': 'HmiHvacFanLvl_Reserved'}


class BGMIntEthPDU5010:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5010
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiHvacRecircCmd:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "循环模式设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'HmiHvacRecircCmd_Aut', '0x1': 'HmiHvacRecircCmd_AutWithAirQly', '0x2': 'HmiHvacRecircCmd_RecircFull', '0x3': 'HmiHvacRecircCmd_OscircFull'}


class BGMIntEthPDU5011:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5011
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiDefrstMaxReq:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "最大除霜模式"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ActrReq_Off', '0x1': 'ActrReq_On', '0x2': 'ActrReq_AutOn'}


class BGMIntEthPDU5012:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5012
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiCmptmtAirDistbnFrntLe:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "吹风模式设置-前左"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'HmiCmptmtAirDistbnFrnt_Flr', '0x1': 'HmiCmptmtAirDistbnFrnt_Vent', '0x2': 'HmiCmptmtAirDistbnFrnt_Defrst', '0x3': 'HmiCmptmtAirDistbnFrnt_FlrDefrst', '0x4': 'HmiCmptmtAirDistbnFrnt_FlrVent', '0x5': 'HmiCmptmtAirDistbnFrnt_VentDefrst', '0x6': 'HmiCmptmtAirDistbnFrnt_FlrVentDefrst', '0x7': 'HmiCmptmtAirDistbnFrnt_Aut'}


class BGMIntEthPDU5013:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5013
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiCmptmtAirDistbnFrntRi:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "吹风模式设置-前右"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'HmiCmptmtAirDistbnFrnt_Flr', '0x1': 'HmiCmptmtAirDistbnFrnt_Vent', '0x2': 'HmiCmptmtAirDistbnFrnt_Defrst', '0x3': 'HmiCmptmtAirDistbnFrnt_FlrDefrst', '0x4': 'HmiCmptmtAirDistbnFrnt_FlrVent', '0x5': 'HmiCmptmtAirDistbnFrnt_VentDefrst', '0x6': 'HmiCmptmtAirDistbnFrnt_FlrVentDefrst', '0x7': 'HmiCmptmtAirDistbnFrnt_Aut'}


class BGMIntEthPDU5014:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5014
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiCmptmtAirDistbnRe:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "吹风模式设置-后"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'HmiCmptmtAirDistbnFrnt_Flr', '0x1': 'HmiCmptmtAirDistbnFrnt_Vent', '0x2': 'HmiCmptmtAirDistbnFrnt_Defrst', '0x3': 'HmiCmptmtAirDistbnFrnt_FlrDefrst', '0x4': 'HmiCmptmtAirDistbnFrnt_FlrVent', '0x5': 'HmiCmptmtAirDistbnFrnt_VentDefrst', '0x6': 'HmiCmptmtAirDistbnFrnt_FlrVentDefrst', '0x7': 'HmiCmptmtAirDistbnFrnt_Aut'}


class BGMIntEthPDU5015:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5015
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiPopUpResp:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "用户对空调Popup请求的响应"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'BookChargeSetResponse_Default', '0x1': 'BookChargeSetResponse_Success', '0x2': 'BookChargeSetResponse_Cancelled', '0x3': 'BookChargeSetResponse_Fail'}


class BGMIntEthPDU5016:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5016
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TWinRfClsdPopUpReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "温度处于Comfort_level时的自动关窗提醒设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5017:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5017
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class FrntCamDefrostReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "前摄像头加热请求"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ADFrntCamDefrostReq_Off', '0x1': 'ADFrntCamDefrostReq_On', '0x2': 'ADFrntCamDefrostReq_Invalid'}


class BGMIntEthPDU5018:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5018
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HmiDefrstElecReq': ['HmiDefrstElecReqFrntElecReq', 'HmiDefrstElecReqMirrElecReq', 'HmiDefrstElecReqReElecReq']}

    class HmiDefrstElecReqFrntElecReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "前风挡加热请求"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ActrReq_Off', '0x1': 'ActrReq_On', '0x2': 'ActrReq_AutOn'}

    class HmiDefrstElecReqMirrElecReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "后视镜加热请求"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'ActrReq_Off', '0x1': 'ActrReq_On', '0x2': 'ActrReq_AutOn'}

    class HmiDefrstElecReqReElecReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "后风挡加热请求"
        signal_length = 2
        start_position = 17
        value_definition = {'0x0': 'ActrReq_Off', '0x1': 'ActrReq_On', '0x2': 'ActrReq_AutOn'}


class BGMIntEthPDU5020:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 5020
    pdu_length_bytes = 1
    receiver = "SoC"
    send_type = "Cyclic-300ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class FrntCamDefrostSts:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "前摄像头加热状态反馈"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ADFrntCamDefrostSts_Off', '0x1': 'ADFrntCamDefrostSts_On', '0x2': 'ADFrntCamDefrostSts_Fault'}


class BGMIntEthPDU5021:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5021
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiMaxACReq:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "MAXAC功能开启关闭"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5022:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5022
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HMIClimaEgySaveReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "ECO模式使能失能"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'VentnActr01BlckInd_Disabled', '0x1': 'VentnActr01BlckInd_Enabled', '0x2': 'VentnActr01BlckInd_Reserved', '0x3': 'VentnActr01BlckInd_Signalinvalid'}


class BGMIntEthPDU5023:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5023
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiHumCtrlEna:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "自动除湿开启关闭"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5024:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5024
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ClimaRqrdFromHmi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "PreCliamte开启关闭"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU5025:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5025
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiAutDefrstEna:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "自动除雾开启关闭"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5026:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5026
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'DrvrAirCdnrSetg': ['DrvrAirCdnrSetgIdPen', 'DrvrAirCdnrSetgAirCdnrSetg']}

    class DrvrAirCdnrSetgIdPen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "个性化设置Idpen"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'AirCdnrSetg_Normal', '0x1': 'AirCdnrSetg_ECO', '0x2': 'AirCdnrSetg_Reserved1'}

    class DrvrAirCdnrSetgAirCdnrSetg:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "个人模式时ECO模式的设置"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'AirCdnrSetg_Normal', '0x1': 'AirCdnrSetg_ECO', '0x2': 'AirCdnrSetg_Reserved1'}


class BGMIntEthPDU5027:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 5027
    pdu_length_bytes = 3
    receiver = "SoC"
    send_type = "Cyclic-200ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'HmiDefrstrElecSts': ['HmiDefrstrElecStsFrnt', 'HmiDefrstrElecStsMirrr', 'HmiDefrstrElecStsRe']}

    class HmiDefrstrElecStsFrnt:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "前挡风玻璃电加热状态"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'ActrDefrstSts_Off', '0x1': 'ActrDefrstSts_On', '0x2': 'ActrDefrstSts_Limited', '0x3': 'ActrDefrstSts_NotAvailable', '0x4': 'ActrDefrstSts_TmrOff', '0x5': 'ActrDefrstSts_AutoCdn'}

    class HmiDefrstrElecStsMirrr:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "后视镜电加热状态"
        signal_length = 3
        start_position = 10
        value_definition = {'0x0': 'ActrDefrstSts_Off', '0x1': 'ActrDefrstSts_On', '0x2': 'ActrDefrstSts_Limited', '0x3': 'ActrDefrstSts_NotAvailable', '0x4': 'ActrDefrstSts_TmrOff', '0x5': 'ActrDefrstSts_AutoCdn'}

    class HmiDefrstrElecStsRe:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "后挡风玻璃电加热状态"
        signal_length = 3
        start_position = 18
        value_definition = {'0x0': 'ActrDefrstSts_Off', '0x1': 'ActrDefrstSts_On', '0x2': 'ActrDefrstSts_Limited', '0x3': 'ActrDefrstSts_NotAvailable', '0x4': 'ActrDefrstSts_TmrOff', '0x5': 'ActrDefrstSts_AutoCdn'}


class BGMIntEthPDU5028:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5028
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class InteCleanUnpleSmell:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "座舱清洁设置开关"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5029:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5029
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmClimaReqSP:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "远程开启空调请求"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU5030:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5030
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'TelmClimaTSetSP': ['TelmClimaTSetSPTempRange', 'TelmClimaTSetSPHmiCmptmtTSpSpcl']}

    class TelmClimaTSetSPTempRange:
        comments = "MCU SWC接收"
        factor = 0.5
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 15
        signal_description = "远程温度调节温度值"
        signal_length = 5
        start_position = 12
        value_definition = {}

    class TelmClimaTSetSPHmiCmptmtTSpSpcl:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "远程温度调节高中低"
        signal_length = 2
        start_position = 1
        value_definition = {}


class BGMIntEthPDU5031:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5031
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'RemStrtHvCtrlReq': ['RemStrtHvCtrlReqErsCmd', 'RemStrtHvCtrlReqErsRunTime']}

    class RemStrtHvCtrlReqErsCmd:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程请求空调上高压请求"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ErsCmd_ErsCmdNotSet', '0x1': 'ErsCmd_ErsCmdOn', '0x2': 'ErsCmd_ErsCmdOff'}

    class RemStrtHvCtrlReqErsRunTime:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程请求空调上高压时间设置"
        signal_length = 6
        start_position = 13
        value_definition = {'0x0': 'ErsCmd_ErsCmdNotSet', '0x1': 'ErsCmd_ErsCmdOn', '0x2': 'ErsCmd_ErsCmdOff'}


class BGMIntEthPDU5032:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5032
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class RemStrtExtnTiReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程请求空调延长高压 "
        signal_length = 6
        start_position = 5
        value_definition = {}


class BGMIntEthPDU5101:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5101
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiElecAirDrvrSwtReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口开启关闭设置-主驾驶"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5102:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5102
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiElecAirPassSwtReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口开启关闭设置-副驾驶"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5103:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5103
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HmiElecAirSwngReq': ['HmiElecAirSwngReqDrvrLeRiSwng', 'HmiElecAirSwngReqDrvrUpOnSwng', 'HmiElecAirSwngReqPassLeRiSwng', 'HmiElecAirSwngReqPassUpOnSwng']}

    class HmiElecAirSwngReqDrvrLeRiSwng:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "扫风方向设置主驾驶左右"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class HmiElecAirSwngReqDrvrUpOnSwng:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "扫风方向设置主驾驶上下"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class HmiElecAirSwngReqPassLeRiSwng:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "扫风方向设置副驾驶左右"
        signal_length = 1
        start_position = 16
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class HmiElecAirSwngReqPassUpOnSwng:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "扫风方向设置副驾驶上下"
        signal_length = 1
        start_position = 24
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5104:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5104
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HmiElecAirDirModReq': ['HmiElecAirDirModReqDrvrMod', 'HmiElecAirDirModReqPassMod']}

    class HmiElecAirDirModReqDrvrMod:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口模式设置-主驾驶"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'AirDirModReq_Normal', '0x1': 'AirDirModReq_Focus', '0x2': 'AirDirModReq_Avoid', '0x3': 'AirDirModReq_Customize'}

    class HmiElecAirDirModReqPassMod:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口模式设置-副驾驶"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'AirDirModReq_Normal', '0x1': 'AirDirModReq_Focus', '0x2': 'AirDirModReq_Avoid', '0x3': 'AirDirModReq_Customize'}


class BGMIntEthPDU5105:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5105
    pdu_length_bytes = 8
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HmiElecAirDirCrtlReq': ['HmiElecAirDirCrtlReqDrvrLePosX', 'HmiElecAirDirCrtlReqDrvrLePosY', 'HmiElecAirDirCrtlReqDrvrRiPosX', 'HmiElecAirDirCrtlReqDrvrRiPosY', 'HmiElecAirDirCrtlReqPassLePosX', 'HmiElecAirDirCrtlReqPassLePosY', 'HmiElecAirDirCrtlReqPassRiPosX', 'HmiElecAirDirCrtlReqPassRiPosY']}

    class HmiElecAirDirCrtlReqDrvrLePosX:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置主驾驶左X"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class HmiElecAirDirCrtlReqDrvrLePosY:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置主驾驶左Y"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class HmiElecAirDirCrtlReqDrvrRiPosX:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置主驾驶右X"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class HmiElecAirDirCrtlReqDrvrRiPosY:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置主驾驶右Y"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class HmiElecAirDirCrtlReqPassLePosX:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置副驾驶左X"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class HmiElecAirDirCrtlReqPassLePosY:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置副驾驶左Y"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class HmiElecAirDirCrtlReqPassRiPosX:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置副驾驶右X"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class HmiElecAirDirCrtlReqPassRiPosY:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置副驾驶右Y"
        signal_length = 8
        start_position = 63
        value_definition = {}


class BGMIntEthPDU5106:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5106
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiElecAirRearSwtReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口开启关闭设置-后排"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5107:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5107
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HmiReElecAirSwngReq': ['HmiReElecAirSwngReqSecRowLeLeRiSwng', 'HmiReElecAirSwngReqSecRowLeUpDnSwng']}

    class HmiReElecAirSwngReqSecRowLeLeRiSwng:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "扫风方向设置后排左右"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class HmiReElecAirSwngReqSecRowLeUpDnSwng:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "扫风方向设置后排上下"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5108:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5108
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HmiReElecAirDirModReq': ['HmiReElecAirDirModReqReLeElecAirDirModReq', 'HmiReElecAirDirModReqReRiElecAirDirModReq']}

    class HmiReElecAirDirModReqReLeElecAirDirModReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口模式设置-后排左"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'AirDirModReq_Normal', '0x1': 'AirDirModReq_Focus', '0x2': 'AirDirModReq_Avoid', '0x3': 'AirDirModReq_Customize'}

    class HmiReElecAirDirModReqReRiElecAirDirModReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口模式设置-后排右"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'AirDirModReq_Normal', '0x1': 'AirDirModReq_Focus', '0x2': 'AirDirModReq_Avoid', '0x3': 'AirDirModReq_Customize'}


class BGMIntEthPDU5109:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5109
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HmiReElecAirDirCrtlReq': ['HmiReElecAirDirCrtlReqSecRowLePosX', 'HmiReElecAirDirCrtlReqSecRowLePosY', 'HmiReElecAirDirCrtlReqSecRowRiPosX', 'HmiReElecAirDirCrtlReqSecRowRiPosY']}

    class HmiReElecAirDirCrtlReqSecRowLePosX:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置后排左X"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class HmiReElecAirDirCrtlReqSecRowLePosY:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置后排左Y"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class HmiReElecAirDirCrtlReqSecRowRiPosX:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置后排右X"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class HmiReElecAirDirCrtlReqSecRowRiPosY:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "出风口坐标设置后排右Y"
        signal_length = 8
        start_position = 31
        value_definition = {}


class BGMIntEthPDU5152:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5152
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ExtrMirrFoldHmiReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "后视镜折叠控制"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'PsdNotPsd1_NotPsd', '0x1': 'PsdNotPsd1_Psd'}


class BGMIntEthPDU5153:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5153
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'ExtrMirrTiltSetg': ['ExtrMirrTiltSetgIdPen', 'ExtrMirrTiltSetgMirrDrvr', 'ExtrMirrTiltSetgMirrPass']}

    class ExtrMirrTiltSetgIdPen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "个性化设置Idpen"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'OnOff2_On', '0x1': 'OnOff2_Off'}

    class ExtrMirrTiltSetgMirrDrvr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾后视镜下翻控制"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'OnOff2_On', '0x1': 'OnOff2_Off'}

    class ExtrMirrTiltSetgMirrPass:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾后视镜下翻控制"
        signal_length = 1
        start_position = 16
        value_definition = {'0x0': 'OnOff2_On', '0x1': 'OnOff2_Off'}


class BGMIntEthPDU5154:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5154
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'ExtrMirrFoldSetg': ['ExtrMirrFoldSetgIdPen', 'ExtrMirrFoldSetgMirrDrvr', 'ExtrMirrFoldSetgMirrPass']}

    class ExtrMirrFoldSetgIdPen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "个性化设置Idpen"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'OnOff2_On', '0x1': 'OnOff2_Off'}

    class ExtrMirrFoldSetgMirrDrvr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾后视镜折叠控制"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'OnOff2_On', '0x1': 'OnOff2_Off'}

    class ExtrMirrFoldSetgMirrPass:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾后视镜折叠控制"
        signal_length = 1
        start_position = 16
        value_definition = {'0x0': 'OnOff2_On', '0x1': 'OnOff2_Off'}


class BGMIntEthPDU5155:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5155
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HMIMirrDimmEn:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "内后视镜防眩目使能"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5156:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5156
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DrvrExtrMirrAdjHmiReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左外后视镜调节"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'MirrDirReqTyp_Idle', '0x1': 'MirrDirReqTyp_Up', '0x2': 'MirrDirReqTyp_Down', '0x3': 'MirrDirReqTyp_Left', '0x4': 'MirrDirReqTyp_Right'}


class BGMIntEthPDU5157:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5157
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class PassExtrMirrAdjHmiReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "右外后视镜调节"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'MirrDirReqTyp_Idle', '0x1': 'MirrDirReqTyp_Up', '0x2': 'MirrDirReqTyp_Down', '0x3': 'MirrDirReqTyp_Left', '0x4': 'MirrDirReqTyp_Right'}


class BGMIntEthPDU5201:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5201
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ChrgLidReCtrlHmiReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "充电小门控制：解锁、上锁"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'LockgCenReq2_Idle', '0x1': 'LockgCenReq2_Unlck', '0x2': 'LockgCenReq2_Lock'}


class BGMIntEthPDU5204:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 5204
    pdu_length_bytes = 1
    receiver = "SoC"
    send_type = "Cyclic-100ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class ChrgLidManvgFailWarnDCorACDCSts:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "充电小门操作失败提醒"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU5205:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 5205
    pdu_length_bytes = 1
    receiver = "SoC"
    send_type = "Cyclic-100ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class ActvOfHorn:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "喇叭激活状态"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5206:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5206
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HornAdvCtrl': ['HornAdvCtrlHornOnTi', 'HornAdvCtrlHornOffTi', 'HornAdvCtrlNrOfHornActvn']}

    class HornAdvCtrlHornOnTi:
        comments = "MCU SWC接收"
        factor = 100.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "喇叭单周期OnTime"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class HornAdvCtrlHornOffTi:
        comments = "MCU SWC接收"
        factor = 100.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "喇叭单周期OffTime"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class HornAdvCtrlNrOfHornActvn:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "喇叭激活次数"
        signal_length = 8
        start_position = 23
        value_definition = {}


class BGMIntEthPDU5207:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5207
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class FCSILEDIndctn:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "充电灯光显示控制"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'NO_COLOR', '0x1': 'WHITE', '0x2': 'BLUE', '0x3': 'GREEN_BREATH', '0x4': 'GREEN', '0x5': 'BLUE_BREATH', '0x6': 'RESERVED', '0x7': 'RED'}


class BGMIntEthPDU5301:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5301
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DrvrAsscSysIndcrReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "转向灯控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'PASTurnIndcrReq_NoRequest', '0x1': 'PASTurnIndcrReq_LeftRequest', '0x2': 'PASTurnIndcrReq_RightRequest', '0x3': 'PASTurnIndcrReq_HWLReq'}


class BGMIntEthPDU5304:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5304
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class FogSetReReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "后雾灯开启关闭控制"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5305:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5305
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HiBeamSw:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "远光灯控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'HiFlashBeam_None', '0x1': 'HiFlashBeam_Request_Flash', '0x2': 'HiFlashBeam_Request_HiBeam'}


class BGMIntEthPDU5306:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5306
    pdu_length_bytes = 5
    receiver = "MCU"
    send_type = "Cyclic-100ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'SwtCDCLi': ['SwtCDCLiLoBeamSw', 'SwtCDCLiPosLampSw', 'SwtCDCLiAutoLampSw', 'SwtCDCLiCntr', 'SwtCDCLiChks']}

    class SwtCDCLiLoBeamSw:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "外灯模式控制-近光"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class SwtCDCLiPosLampSw:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "外灯模式控制-位置灯"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class SwtCDCLiAutoLampSw:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "外灯模式控制-Auto"
        signal_length = 1
        start_position = 16
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class SwtCDCLiCntr:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "外灯模式控制Cntr"
        signal_length = 4
        start_position = 27
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class SwtCDCLiChks:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "外灯模式控制Chks"
        signal_length = 8
        start_position = 39
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5308:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5308
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class StaticLightingModeReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "灯光秀激活设置标志位"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU5309:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5309
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'LiHomeSafeReq': ['LiHomeSafeReqPen', 'LiHomeSafeReqSts']}

    class LiHomeSafeReqPen:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "伴我回家设置-Idpen"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'LiTi2_Sec0', '0x1': 'LiTi2_Sec10', '0x2': 'LiTi2_Sec20', '0x3': 'LiTi2_Sec30', '0x4': 'LiTi2_Sec40', '0x5': 'LiTi2_Sec50', '0x6': 'LiTi2_Sec60', '0x7': 'LiTi2_Sec70', '0x8': 'LiTi2_Sec80', '0x9': 'LiTi2_Sec90', '0xA': 'LiTi2_Sec100', '0xB': 'LiTi2_Sec110', '0xC': 'LiTi2_Sec120', '0xD': 'LiTi2_Resd1', '0xE': 'LiTi2_Resd2', '0xF': 'LiTi2_Resd3'}

    class LiHomeSafeReqSts:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "伴我回家设置-持续时间"
        signal_length = 4
        start_position = 11
        value_definition = {'0x0': 'LiTi2_Sec0', '0x1': 'LiTi2_Sec10', '0x2': 'LiTi2_Sec20', '0x3': 'LiTi2_Sec30', '0x4': 'LiTi2_Sec40', '0x5': 'LiTi2_Sec50', '0x6': 'LiTi2_Sec60', '0x7': 'LiTi2_Sec70', '0x8': 'LiTi2_Sec80', '0x9': 'LiTi2_Sec90', '0xA': 'LiTi2_Sec100', '0xB': 'LiTi2_Sec110', '0xC': 'LiTi2_Sec120', '0xD': 'LiTi2_Resd1', '0xE': 'LiTi2_Resd2', '0xF': 'LiTi2_Resd3'}


class BGMIntEthPDU5310:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5310
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetOfPosnLampScopeReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "位置灯图案编辑设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU5311:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5311
    pdu_length_bytes = 6
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'AIInteractionLampLeft': ['AIInteractionLampLeftY1', 'AIInteractionLampLeftY2', 'AIInteractionLampLeftY3', 'AIInteractionLampLeftY4', 'AIInteractionLampLeftY5', 'AIInteractionLampLeftY6']}

    class AIInteractionLampLeftY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左AI灯控制"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class AIInteractionLampLeftY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左AI灯控制"
        signal_length = 7
        start_position = 14
        value_definition = {}

    class AIInteractionLampLeftY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左AI灯控制"
        signal_length = 7
        start_position = 22
        value_definition = {}

    class AIInteractionLampLeftY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左AI灯控制"
        signal_length = 7
        start_position = 30
        value_definition = {}

    class AIInteractionLampLeftY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左AI灯控制"
        signal_length = 7
        start_position = 38
        value_definition = {}

    class AIInteractionLampLeftY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左AI灯控制"
        signal_length = 7
        start_position = 46
        value_definition = {}


class BGMIntEthPDU5312:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5312
    pdu_length_bytes = 6
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'AIInteractionLampRight': ['AIInteractionLampRightY1', 'AIInteractionLampRightY2', 'AIInteractionLampRightY3', 'AIInteractionLampRightY4', 'AIInteractionLampRightY5', 'AIInteractionLampRightY6']}

    class AIInteractionLampRightY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "右AI灯控制"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class AIInteractionLampRightY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "右AI灯控制"
        signal_length = 7
        start_position = 14
        value_definition = {}

    class AIInteractionLampRightY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "右AI灯控制"
        signal_length = 7
        start_position = 22
        value_definition = {}

    class AIInteractionLampRightY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "右AI灯控制"
        signal_length = 7
        start_position = 30
        value_definition = {}

    class AIInteractionLampRightY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "右AI灯控制"
        signal_length = 7
        start_position = 38
        value_definition = {}

    class AIInteractionLampRightY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "右AI灯控制"
        signal_length = 7
        start_position = 46
        value_definition = {}


class BGMIntEthPDU5313:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5313
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Cyclic-100ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'DIPriorityFlag': ['DIPriorityFlagDIPriorityFlag', 'DIPriorityFlagCntr', 'DIPriorityFlagChks']}

    class DIPriorityFlagDIPriorityFlag:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "转向控制优先级标记"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}

    class DIPriorityFlagCntr:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "转向控制优先级标记Cntr"
        signal_length = 4
        start_position = 11
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}

    class DIPriorityFlagChks:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "转向控制优先级标记Chks"
        signal_length = 8
        start_position = 23
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU5314:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5314
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HiBeamLe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class HiBeamRi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 14
        value_definition = {}

    class LoBeamLe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 22
        value_definition = {}

    class LoBeamRi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 30
        value_definition = {}


class BGMIntEthPDU5315:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5315
    pdu_length_bytes = 132
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'PIXFrntLeX1': ['PIXFrntLeX1Y1', 'PIXFrntLeX1Y2', 'PIXFrntLeX1Y3', 'PIXFrntLeX1Y4', 'PIXFrntLeX1Y5', 'PIXFrntLeX1Y6'], 'PIXFrntLeX2': ['PIXFrntLeX2Y1', 'PIXFrntLeX2Y2', 'PIXFrntLeX2Y3', 'PIXFrntLeX2Y4', 'PIXFrntLeX2Y5', 'PIXFrntLeX2Y6'], 'PIXFrntLeX3': ['PIXFrntLeX3Y1', 'PIXFrntLeX3Y2', 'PIXFrntLeX3Y3', 'PIXFrntLeX3Y4', 'PIXFrntLeX3Y5', 'PIXFrntLeX3Y6'], 'PIXFrntLeX4': ['PIXFrntLeX4Y1', 'PIXFrntLeX4Y2', 'PIXFrntLeX4Y3', 'PIXFrntLeX4Y4', 'PIXFrntLeX4Y5', 'PIXFrntLeX4Y6'], 'PIXFrntLeX5': ['PIXFrntLeX5Y1', 'PIXFrntLeX5Y2', 'PIXFrntLeX5Y3', 'PIXFrntLeX5Y4', 'PIXFrntLeX5Y5', 'PIXFrntLeX5Y6'], 'PIXFrntLeX6': ['PIXFrntLeX6Y1', 'PIXFrntLeX6Y2', 'PIXFrntLeX6Y3', 'PIXFrntLeX6Y4', 'PIXFrntLeX6Y5', 'PIXFrntLeX6Y6'], 'PIXFrntLeX7': ['PIXFrntLeX7Y1', 'PIXFrntLeX7Y2', 'PIXFrntLeX7Y3', 'PIXFrntLeX7Y4', 'PIXFrntLeX7Y5', 'PIXFrntLeX7Y6'], 'PIXFrntLeX8': ['PIXFrntLeX8Y1', 'PIXFrntLeX8Y2', 'PIXFrntLeX8Y3', 'PIXFrntLeX8Y4', 'PIXFrntLeX8Y5', 'PIXFrntLeX8Y6'], 'PIXFrntLeX9': ['PIXFrntLeX9Y1', 'PIXFrntLeX9Y2', 'PIXFrntLeX9Y3', 'PIXFrntLeX9Y4', 'PIXFrntLeX9Y5', 'PIXFrntLeX9Y6'], 'PIXFrntLeXA': ['PIXFrntLeXAY1', 'PIXFrntLeXAY2', 'PIXFrntLeXAY3', 'PIXFrntLeXAY4', 'PIXFrntLeXAY5', 'PIXFrntLeXAY6'], 'PIXFrntLeXB': ['PIXFrntLeXBY1', 'PIXFrntLeXBY2', 'PIXFrntLeXBY3', 'PIXFrntLeXBY4', 'PIXFrntLeXBY5', 'PIXFrntLeXBY6'], 'PIXFrntRiX1': ['PIXFrntRiX1Y1', 'PIXFrntRiX1Y2', 'PIXFrntRiX1Y3', 'PIXFrntRiX1Y4', 'PIXFrntRiX1Y5', 'PIXFrntRiX1Y6'], 'PIXFrntRiX2': ['PIXFrntRiX2Y1', 'PIXFrntRiX2Y2', 'PIXFrntRiX2Y3', 'PIXFrntRiX2Y4', 'PIXFrntRiX2Y5', 'PIXFrntRiX2Y6'], 'PIXFrntRiX3': ['PIXFrntRiX3Y1', 'PIXFrntRiX3Y2', 'PIXFrntRiX3Y3', 'PIXFrntRiX3Y4', 'PIXFrntRiX3Y5', 'PIXFrntRiX3Y6'], 'PIXFrntRiX4': ['PIXFrntRiX4Y1', 'PIXFrntRiX4Y2', 'PIXFrntRiX4Y3', 'PIXFrntRiX4Y4', 'PIXFrntRiX4Y5', 'PIXFrntRiX4Y6'], 'PIXFrntRiX5': ['PIXFrntRiX5Y1', 'PIXFrntRiX5Y2', 'PIXFrntRiX5Y3', 'PIXFrntRiX5Y4', 'PIXFrntRiX5Y5', 'PIXFrntRiX5Y6'], 'PIXFrntRiX6': ['PIXFrntRiX6Y1', 'PIXFrntRiX6Y2', 'PIXFrntRiX6Y3', 'PIXFrntRiX6Y4', 'PIXFrntRiX6Y5', 'PIXFrntRiX6Y6'], 'PIXFrntRiX7': ['PIXFrntRiX7Y1', 'PIXFrntRiX7Y2', 'PIXFrntRiX7Y3', 'PIXFrntRiX7Y4', 'PIXFrntRiX7Y5', 'PIXFrntRiX7Y6'], 'PIXFrntRiX8': ['PIXFrntRiX8Y1', 'PIXFrntRiX8Y2', 'PIXFrntRiX8Y3', 'PIXFrntRiX8Y4', 'PIXFrntRiX8Y5', 'PIXFrntRiX8Y6'], 'PIXFrntRiX9': ['PIXFrntRiX9Y1', 'PIXFrntRiX9Y2', 'PIXFrntRiX9Y3', 'PIXFrntRiX9Y4', 'PIXFrntRiX9Y5', 'PIXFrntRiX9Y6'], 'PIXFrntRiXA': ['PIXFrntRiXAY1', 'PIXFrntRiXAY2', 'PIXFrntRiXAY3', 'PIXFrntRiXAY4', 'PIXFrntRiXAY5', 'PIXFrntRiXAY6'], 'PIXFrntRiXB': ['PIXFrntRiXBY1', 'PIXFrntRiXBY2', 'PIXFrntRiXBY3', 'PIXFrntRiXBY4', 'PIXFrntRiXBY5', 'PIXFrntRiXBY6']}

    class PIXFrntLeX1Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class PIXFrntLeX1Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 14
        value_definition = {}

    class PIXFrntLeX1Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 22
        value_definition = {}

    class PIXFrntLeX1Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 30
        value_definition = {}

    class PIXFrntLeX1Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 38
        value_definition = {}

    class PIXFrntLeX1Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 46
        value_definition = {}

    class PIXFrntLeX2Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 54
        value_definition = {}

    class PIXFrntLeX2Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 62
        value_definition = {}

    class PIXFrntLeX2Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 70
        value_definition = {}

    class PIXFrntLeX2Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 78
        value_definition = {}

    class PIXFrntLeX2Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 86
        value_definition = {}

    class PIXFrntLeX2Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 94
        value_definition = {}

    class PIXFrntLeX3Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 102
        value_definition = {}

    class PIXFrntLeX3Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 110
        value_definition = {}

    class PIXFrntLeX3Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 118
        value_definition = {}

    class PIXFrntLeX3Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 126
        value_definition = {}

    class PIXFrntLeX3Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 134
        value_definition = {}

    class PIXFrntLeX3Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 142
        value_definition = {}

    class PIXFrntLeX4Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 150
        value_definition = {}

    class PIXFrntLeX4Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 158
        value_definition = {}

    class PIXFrntLeX4Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 166
        value_definition = {}

    class PIXFrntLeX4Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 174
        value_definition = {}

    class PIXFrntLeX4Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 182
        value_definition = {}

    class PIXFrntLeX4Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 190
        value_definition = {}

    class PIXFrntLeX5Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 198
        value_definition = {}

    class PIXFrntLeX5Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 206
        value_definition = {}

    class PIXFrntLeX5Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 214
        value_definition = {}

    class PIXFrntLeX5Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 222
        value_definition = {}

    class PIXFrntLeX5Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 230
        value_definition = {}

    class PIXFrntLeX5Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 238
        value_definition = {}

    class PIXFrntLeX6Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 246
        value_definition = {}

    class PIXFrntLeX6Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 254
        value_definition = {}

    class PIXFrntLeX6Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 262
        value_definition = {}

    class PIXFrntLeX6Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 270
        value_definition = {}

    class PIXFrntLeX6Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 278
        value_definition = {}

    class PIXFrntLeX6Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 286
        value_definition = {}

    class PIXFrntLeX7Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 294
        value_definition = {}

    class PIXFrntLeX7Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 302
        value_definition = {}

    class PIXFrntLeX7Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 310
        value_definition = {}

    class PIXFrntLeX7Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 318
        value_definition = {}

    class PIXFrntLeX7Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 326
        value_definition = {}

    class PIXFrntLeX7Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 334
        value_definition = {}

    class PIXFrntLeX8Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 342
        value_definition = {}

    class PIXFrntLeX8Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 350
        value_definition = {}

    class PIXFrntLeX8Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 358
        value_definition = {}

    class PIXFrntLeX8Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 366
        value_definition = {}

    class PIXFrntLeX8Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 374
        value_definition = {}

    class PIXFrntLeX8Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 382
        value_definition = {}

    class PIXFrntLeX9Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 390
        value_definition = {}

    class PIXFrntLeX9Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 398
        value_definition = {}

    class PIXFrntLeX9Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 406
        value_definition = {}

    class PIXFrntLeX9Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 414
        value_definition = {}

    class PIXFrntLeX9Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 422
        value_definition = {}

    class PIXFrntLeX9Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 430
        value_definition = {}

    class PIXFrntLeXAY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 438
        value_definition = {}

    class PIXFrntLeXAY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 446
        value_definition = {}

    class PIXFrntLeXAY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 454
        value_definition = {}

    class PIXFrntLeXAY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 462
        value_definition = {}

    class PIXFrntLeXAY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 470
        value_definition = {}

    class PIXFrntLeXAY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 478
        value_definition = {}

    class PIXFrntLeXBY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 486
        value_definition = {}

    class PIXFrntLeXBY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 494
        value_definition = {}

    class PIXFrntLeXBY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 502
        value_definition = {}

    class PIXFrntLeXBY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 510
        value_definition = {}

    class PIXFrntLeXBY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 518
        value_definition = {}

    class PIXFrntLeXBY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 526
        value_definition = {}

    class PIXFrntRiX1Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 534
        value_definition = {}

    class PIXFrntRiX1Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 542
        value_definition = {}

    class PIXFrntRiX1Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 550
        value_definition = {}

    class PIXFrntRiX1Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 558
        value_definition = {}

    class PIXFrntRiX1Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 566
        value_definition = {}

    class PIXFrntRiX1Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 574
        value_definition = {}

    class PIXFrntRiX2Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 582
        value_definition = {}

    class PIXFrntRiX2Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 590
        value_definition = {}

    class PIXFrntRiX2Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 598
        value_definition = {}

    class PIXFrntRiX2Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 606
        value_definition = {}

    class PIXFrntRiX2Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 614
        value_definition = {}

    class PIXFrntRiX2Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 622
        value_definition = {}

    class PIXFrntRiX3Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 630
        value_definition = {}

    class PIXFrntRiX3Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 638
        value_definition = {}

    class PIXFrntRiX3Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 646
        value_definition = {}

    class PIXFrntRiX3Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 654
        value_definition = {}

    class PIXFrntRiX3Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 662
        value_definition = {}

    class PIXFrntRiX3Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 670
        value_definition = {}

    class PIXFrntRiX4Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 678
        value_definition = {}

    class PIXFrntRiX4Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 686
        value_definition = {}

    class PIXFrntRiX4Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 694
        value_definition = {}

    class PIXFrntRiX4Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 702
        value_definition = {}

    class PIXFrntRiX4Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 710
        value_definition = {}

    class PIXFrntRiX4Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 718
        value_definition = {}

    class PIXFrntRiX5Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 726
        value_definition = {}

    class PIXFrntRiX5Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 734
        value_definition = {}

    class PIXFrntRiX5Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 742
        value_definition = {}

    class PIXFrntRiX5Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 750
        value_definition = {}

    class PIXFrntRiX5Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 758
        value_definition = {}

    class PIXFrntRiX5Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 766
        value_definition = {}

    class PIXFrntRiX6Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 774
        value_definition = {}

    class PIXFrntRiX6Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 782
        value_definition = {}

    class PIXFrntRiX6Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 790
        value_definition = {}

    class PIXFrntRiX6Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 798
        value_definition = {}

    class PIXFrntRiX6Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 806
        value_definition = {}

    class PIXFrntRiX6Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 814
        value_definition = {}

    class PIXFrntRiX7Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 822
        value_definition = {}

    class PIXFrntRiX7Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 830
        value_definition = {}

    class PIXFrntRiX7Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 838
        value_definition = {}

    class PIXFrntRiX7Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 846
        value_definition = {}

    class PIXFrntRiX7Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 854
        value_definition = {}

    class PIXFrntRiX7Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 862
        value_definition = {}

    class PIXFrntRiX8Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 870
        value_definition = {}

    class PIXFrntRiX8Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 878
        value_definition = {}

    class PIXFrntRiX8Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 886
        value_definition = {}

    class PIXFrntRiX8Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 894
        value_definition = {}

    class PIXFrntRiX8Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 902
        value_definition = {}

    class PIXFrntRiX8Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 910
        value_definition = {}

    class PIXFrntRiX9Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 918
        value_definition = {}

    class PIXFrntRiX9Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 926
        value_definition = {}

    class PIXFrntRiX9Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 934
        value_definition = {}

    class PIXFrntRiX9Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 942
        value_definition = {}

    class PIXFrntRiX9Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 950
        value_definition = {}

    class PIXFrntRiX9Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 958
        value_definition = {}

    class PIXFrntRiXAY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 966
        value_definition = {}

    class PIXFrntRiXAY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 974
        value_definition = {}

    class PIXFrntRiXAY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 982
        value_definition = {}

    class PIXFrntRiXAY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 990
        value_definition = {}

    class PIXFrntRiXAY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 998
        value_definition = {}

    class PIXFrntRiXAY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1006
        value_definition = {}

    class PIXFrntRiXBY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1014
        value_definition = {}

    class PIXFrntRiXBY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1022
        value_definition = {}

    class PIXFrntRiXBY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1030
        value_definition = {}

    class PIXFrntRiXBY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1038
        value_definition = {}

    class PIXFrntRiXBY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1046
        value_definition = {}

    class PIXFrntRiXBY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1054
        value_definition = {}


class BGMIntEthPDU5316:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5316
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'DIDRLFrntLe': ['DIDRLFrntLeIsYellow', 'DIDRLFrntLeBrightness'], 'DIDRLFrntRi': ['DIDRLFrntRiIsYellow', 'DIDRLFrntRiBrightness']}

    class DIDRLFrntLeIsYellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class DIDRLFrntLeBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 14
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class DIDRLFrntRiIsYellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 16
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class DIDRLFrntRiBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 30
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}


class BGMIntEthPDU5317:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5317
    pdu_length_bytes = 70
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'CrossFrntX1': ['CrossFrntX1Y1', 'CrossFrntX1Y2', 'CrossFrntX1Y3', 'CrossFrntX1Y4', 'CrossFrntX1Y5', 'CrossFrntX1Y6', 'CrossFrntX1Y7', 'CrossFrntX1Y8', 'CrossFrntX1Y9', 'CrossFrntX1Y10', 'CrossFrntX1Y11', 'CrossFrntX1Y12', 'CrossFrntX1Y13', 'CrossFrntX1Y14', 'CrossFrntX1Y15', 'CrossFrntX1Y16', 'CrossFrntX1Y17', 'CrossFrntX1Y18', 'CrossFrntX1Y19', 'CrossFrntX1Y20', 'CrossFrntX1Y21', 'CrossFrntX1Y22', 'CrossFrntX1Y23', 'CrossFrntX1Y24', 'CrossFrntX1Y25', 'CrossFrntX1Y26', 'CrossFrntX1Y27', 'CrossFrntX1Y28', 'CrossFrntX1Y29', 'CrossFrntX1Y30', 'CrossFrntX1Y31', 'CrossFrntX1Y32', 'CrossFrntX1Y33', 'CrossFrntX1Y34', 'CrossFrntX1Y35', 'CrossFrntX1Y36', 'CrossFrntX1Y37', 'CrossFrntX1Y38', 'CrossFrntX1Y39', 'CrossFrntX1Y40', 'CrossFrntX1Y41', 'CrossFrntX1Y42', 'CrossFrntX1Y43', 'CrossFrntX1Y44', 'CrossFrntX1Y45', 'CrossFrntX1Y46', 'CrossFrntX1Y47', 'CrossFrntX1Y48', 'CrossFrntX1Y49', 'CrossFrntX1Y50', 'CrossFrntX1Y51', 'CrossFrntX1Y52', 'CrossFrntX1Y53', 'CrossFrntX1Y54', 'CrossFrntX1Y55', 'CrossFrntX1Y56', 'CrossFrntX1Y57', 'CrossFrntX1Y58', 'CrossFrntX1Y59', 'CrossFrntX1Y60', 'CrossFrntX1Y61', 'CrossFrntX1Y62', 'CrossFrntX1Y63', 'CrossFrntX1Y64', 'CrossFrntX1Y65', 'CrossFrntX1Y66', 'CrossFrntX1Y67', 'CrossFrntX1Y68', 'CrossFrntX1Y69', 'CrossFrntX1Y70']}

    class CrossFrntX1Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class CrossFrntX1Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 14
        value_definition = {}

    class CrossFrntX1Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 22
        value_definition = {}

    class CrossFrntX1Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 30
        value_definition = {}

    class CrossFrntX1Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 38
        value_definition = {}

    class CrossFrntX1Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 46
        value_definition = {}

    class CrossFrntX1Y7:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 54
        value_definition = {}

    class CrossFrntX1Y8:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 62
        value_definition = {}

    class CrossFrntX1Y9:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 70
        value_definition = {}

    class CrossFrntX1Y10:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 78
        value_definition = {}

    class CrossFrntX1Y11:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 86
        value_definition = {}

    class CrossFrntX1Y12:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 94
        value_definition = {}

    class CrossFrntX1Y13:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 102
        value_definition = {}

    class CrossFrntX1Y14:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 110
        value_definition = {}

    class CrossFrntX1Y15:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 118
        value_definition = {}

    class CrossFrntX1Y16:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 126
        value_definition = {}

    class CrossFrntX1Y17:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 134
        value_definition = {}

    class CrossFrntX1Y18:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 142
        value_definition = {}

    class CrossFrntX1Y19:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 150
        value_definition = {}

    class CrossFrntX1Y20:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 158
        value_definition = {}

    class CrossFrntX1Y21:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 166
        value_definition = {}

    class CrossFrntX1Y22:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 174
        value_definition = {}

    class CrossFrntX1Y23:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 182
        value_definition = {}

    class CrossFrntX1Y24:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 190
        value_definition = {}

    class CrossFrntX1Y25:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 198
        value_definition = {}

    class CrossFrntX1Y26:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 206
        value_definition = {}

    class CrossFrntX1Y27:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 214
        value_definition = {}

    class CrossFrntX1Y28:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 222
        value_definition = {}

    class CrossFrntX1Y29:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 230
        value_definition = {}

    class CrossFrntX1Y30:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 238
        value_definition = {}

    class CrossFrntX1Y31:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 246
        value_definition = {}

    class CrossFrntX1Y32:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 254
        value_definition = {}

    class CrossFrntX1Y33:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 262
        value_definition = {}

    class CrossFrntX1Y34:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 270
        value_definition = {}

    class CrossFrntX1Y35:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 278
        value_definition = {}

    class CrossFrntX1Y36:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 286
        value_definition = {}

    class CrossFrntX1Y37:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 294
        value_definition = {}

    class CrossFrntX1Y38:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 302
        value_definition = {}

    class CrossFrntX1Y39:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 310
        value_definition = {}

    class CrossFrntX1Y40:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 318
        value_definition = {}

    class CrossFrntX1Y41:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 326
        value_definition = {}

    class CrossFrntX1Y42:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 334
        value_definition = {}

    class CrossFrntX1Y43:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 342
        value_definition = {}

    class CrossFrntX1Y44:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 350
        value_definition = {}

    class CrossFrntX1Y45:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 358
        value_definition = {}

    class CrossFrntX1Y46:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 366
        value_definition = {}

    class CrossFrntX1Y47:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 374
        value_definition = {}

    class CrossFrntX1Y48:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 382
        value_definition = {}

    class CrossFrntX1Y49:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 390
        value_definition = {}

    class CrossFrntX1Y50:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 398
        value_definition = {}

    class CrossFrntX1Y51:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 406
        value_definition = {}

    class CrossFrntX1Y52:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 414
        value_definition = {}

    class CrossFrntX1Y53:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 422
        value_definition = {}

    class CrossFrntX1Y54:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 430
        value_definition = {}

    class CrossFrntX1Y55:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 438
        value_definition = {}

    class CrossFrntX1Y56:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 446
        value_definition = {}

    class CrossFrntX1Y57:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 454
        value_definition = {}

    class CrossFrntX1Y58:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 462
        value_definition = {}

    class CrossFrntX1Y59:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 470
        value_definition = {}

    class CrossFrntX1Y60:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 478
        value_definition = {}

    class CrossFrntX1Y61:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 486
        value_definition = {}

    class CrossFrntX1Y62:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 494
        value_definition = {}

    class CrossFrntX1Y63:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 502
        value_definition = {}

    class CrossFrntX1Y64:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 510
        value_definition = {}

    class CrossFrntX1Y65:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 518
        value_definition = {}

    class CrossFrntX1Y66:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 526
        value_definition = {}

    class CrossFrntX1Y67:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 534
        value_definition = {}

    class CrossFrntX1Y68:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 542
        value_definition = {}

    class CrossFrntX1Y69:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 550
        value_definition = {}

    class CrossFrntX1Y70:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 558
        value_definition = {}


class BGMIntEthPDU5318:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5318
    pdu_length_bytes = 100
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'CrossReLeX1': ['CrossReLeX1Y1', 'CrossReLeX1Y2', 'CrossReLeX1Y3', 'CrossReLeX1Y4', 'CrossReLeX1Y5', 'CrossReLeX1Y6', 'CrossReLeX1Y7', 'CrossReLeX1Y8', 'CrossReLeX1Y9', 'CrossReLeX1Y10', 'CrossReLeX1Y11', 'CrossReLeX1Y12', 'CrossReLeX1Y13', 'CrossReLeX1Y14', 'CrossReLeX1Y15', 'CrossReLeX1Y16', 'CrossReLeX1Y17', 'CrossReLeX1Y18', 'CrossReLeX1Y19', 'CrossReLeX1Y20'], 'CrossReRiX1': ['CrossReRiX1Y1', 'CrossReRiX1Y2', 'CrossReRiX1Y3', 'CrossReRiX1Y4', 'CrossReRiX1Y5', 'CrossReRiX1Y6', 'CrossReRiX1Y7', 'CrossReRiX1Y8', 'CrossReRiX1Y9', 'CrossReRiX1Y10', 'CrossReRiX1Y11', 'CrossReRiX1Y12', 'CrossReRiX1Y13', 'CrossReRiX1Y14', 'CrossReRiX1Y15', 'CrossReRiX1Y16', 'CrossReRiX1Y17', 'CrossReRiX1Y18', 'CrossReRiX1Y19', 'CrossReRiX1Y20'], 'CrossReMidX1': ['CrossReMidX1Y1', 'CrossReMidX1Y2', 'CrossReMidX1Y3', 'CrossReMidX1Y4', 'CrossReMidX1Y5', 'CrossReMidX1Y6', 'CrossReMidX1Y7', 'CrossReMidX1Y8', 'CrossReMidX1Y9', 'CrossReMidX1Y10', 'CrossReMidX1Y11', 'CrossReMidX1Y12', 'CrossReMidX1Y13', 'CrossReMidX1Y14', 'CrossReMidX1Y15', 'CrossReMidX1Y16', 'CrossReMidX1Y17', 'CrossReMidX1Y18', 'CrossReMidX1Y19', 'CrossReMidX1Y20', 'CrossReMidX1Y21', 'CrossReMidX1Y22', 'CrossReMidX1Y23', 'CrossReMidX1Y24', 'CrossReMidX1Y25', 'CrossReMidX1Y26', 'CrossReMidX1Y27', 'CrossReMidX1Y28', 'CrossReMidX1Y29', 'CrossReMidX1Y30', 'CrossReMidX1Y31', 'CrossReMidX1Y32', 'CrossReMidX1Y33', 'CrossReMidX1Y34', 'CrossReMidX1Y35', 'CrossReMidX1Y36', 'CrossReMidX1Y37', 'CrossReMidX1Y38', 'CrossReMidX1Y39', 'CrossReMidX1Y40', 'CrossReMidX1Y41', 'CrossReMidX1Y42', 'CrossReMidX1Y43', 'CrossReMidX1Y44', 'CrossReMidX1Y45', 'CrossReMidX1Y46', 'CrossReMidX1Y47', 'CrossReMidX1Y48', 'CrossReMidX1Y49', 'CrossReMidX1Y50', 'CrossReMidX1Y51', 'CrossReMidX1Y52', 'CrossReMidX1Y53', 'CrossReMidX1Y54', 'CrossReMidX1Y55', 'CrossReMidX1Y56', 'CrossReMidX1Y57', 'CrossReMidX1Y58', 'CrossReMidX1Y59', 'CrossReMidX1Y60']}

    class CrossReLeX1Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class CrossReLeX1Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 14
        value_definition = {}

    class CrossReLeX1Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 22
        value_definition = {}

    class CrossReLeX1Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 30
        value_definition = {}

    class CrossReLeX1Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 38
        value_definition = {}

    class CrossReLeX1Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 46
        value_definition = {}

    class CrossReLeX1Y7:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 54
        value_definition = {}

    class CrossReLeX1Y8:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 62
        value_definition = {}

    class CrossReLeX1Y9:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 70
        value_definition = {}

    class CrossReLeX1Y10:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 78
        value_definition = {}

    class CrossReLeX1Y11:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 86
        value_definition = {}

    class CrossReLeX1Y12:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 94
        value_definition = {}

    class CrossReLeX1Y13:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 102
        value_definition = {}

    class CrossReLeX1Y14:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 110
        value_definition = {}

    class CrossReLeX1Y15:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 118
        value_definition = {}

    class CrossReLeX1Y16:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 126
        value_definition = {}

    class CrossReLeX1Y17:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 134
        value_definition = {}

    class CrossReLeX1Y18:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 142
        value_definition = {}

    class CrossReLeX1Y19:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 150
        value_definition = {}

    class CrossReLeX1Y20:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 158
        value_definition = {}

    class CrossReRiX1Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 166
        value_definition = {}

    class CrossReRiX1Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 174
        value_definition = {}

    class CrossReRiX1Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 182
        value_definition = {}

    class CrossReRiX1Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 190
        value_definition = {}

    class CrossReRiX1Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 198
        value_definition = {}

    class CrossReRiX1Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 206
        value_definition = {}

    class CrossReRiX1Y7:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 214
        value_definition = {}

    class CrossReRiX1Y8:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 222
        value_definition = {}

    class CrossReRiX1Y9:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 230
        value_definition = {}

    class CrossReRiX1Y10:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 238
        value_definition = {}

    class CrossReRiX1Y11:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 246
        value_definition = {}

    class CrossReRiX1Y12:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 254
        value_definition = {}

    class CrossReRiX1Y13:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 262
        value_definition = {}

    class CrossReRiX1Y14:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 270
        value_definition = {}

    class CrossReRiX1Y15:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 278
        value_definition = {}

    class CrossReRiX1Y16:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 286
        value_definition = {}

    class CrossReRiX1Y17:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 294
        value_definition = {}

    class CrossReRiX1Y18:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 302
        value_definition = {}

    class CrossReRiX1Y19:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 310
        value_definition = {}

    class CrossReRiX1Y20:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 318
        value_definition = {}

    class CrossReMidX1Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 326
        value_definition = {}

    class CrossReMidX1Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 334
        value_definition = {}

    class CrossReMidX1Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 342
        value_definition = {}

    class CrossReMidX1Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 350
        value_definition = {}

    class CrossReMidX1Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 358
        value_definition = {}

    class CrossReMidX1Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 366
        value_definition = {}

    class CrossReMidX1Y7:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 374
        value_definition = {}

    class CrossReMidX1Y8:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 382
        value_definition = {}

    class CrossReMidX1Y9:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 390
        value_definition = {}

    class CrossReMidX1Y10:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 398
        value_definition = {}

    class CrossReMidX1Y11:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 406
        value_definition = {}

    class CrossReMidX1Y12:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 414
        value_definition = {}

    class CrossReMidX1Y13:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 422
        value_definition = {}

    class CrossReMidX1Y14:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 430
        value_definition = {}

    class CrossReMidX1Y15:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 438
        value_definition = {}

    class CrossReMidX1Y16:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 446
        value_definition = {}

    class CrossReMidX1Y17:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 454
        value_definition = {}

    class CrossReMidX1Y18:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 462
        value_definition = {}

    class CrossReMidX1Y19:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 470
        value_definition = {}

    class CrossReMidX1Y20:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 478
        value_definition = {}

    class CrossReMidX1Y21:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 486
        value_definition = {}

    class CrossReMidX1Y22:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 494
        value_definition = {}

    class CrossReMidX1Y23:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 502
        value_definition = {}

    class CrossReMidX1Y24:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 510
        value_definition = {}

    class CrossReMidX1Y25:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 518
        value_definition = {}

    class CrossReMidX1Y26:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 526
        value_definition = {}

    class CrossReMidX1Y27:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 534
        value_definition = {}

    class CrossReMidX1Y28:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 542
        value_definition = {}

    class CrossReMidX1Y29:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 550
        value_definition = {}

    class CrossReMidX1Y30:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 558
        value_definition = {}

    class CrossReMidX1Y31:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 566
        value_definition = {}

    class CrossReMidX1Y32:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 574
        value_definition = {}

    class CrossReMidX1Y33:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 582
        value_definition = {}

    class CrossReMidX1Y34:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 590
        value_definition = {}

    class CrossReMidX1Y35:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 598
        value_definition = {}

    class CrossReMidX1Y36:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 606
        value_definition = {}

    class CrossReMidX1Y37:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 614
        value_definition = {}

    class CrossReMidX1Y38:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 622
        value_definition = {}

    class CrossReMidX1Y39:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 630
        value_definition = {}

    class CrossReMidX1Y40:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 638
        value_definition = {}

    class CrossReMidX1Y41:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 646
        value_definition = {}

    class CrossReMidX1Y42:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 654
        value_definition = {}

    class CrossReMidX1Y43:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 662
        value_definition = {}

    class CrossReMidX1Y44:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 670
        value_definition = {}

    class CrossReMidX1Y45:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 678
        value_definition = {}

    class CrossReMidX1Y46:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 686
        value_definition = {}

    class CrossReMidX1Y47:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 694
        value_definition = {}

    class CrossReMidX1Y48:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 702
        value_definition = {}

    class CrossReMidX1Y49:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 710
        value_definition = {}

    class CrossReMidX1Y50:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 718
        value_definition = {}

    class CrossReMidX1Y51:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 726
        value_definition = {}

    class CrossReMidX1Y52:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 734
        value_definition = {}

    class CrossReMidX1Y53:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 742
        value_definition = {}

    class CrossReMidX1Y54:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 750
        value_definition = {}

    class CrossReMidX1Y55:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 758
        value_definition = {}

    class CrossReMidX1Y56:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 766
        value_definition = {}

    class CrossReMidX1Y57:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 774
        value_definition = {}

    class CrossReMidX1Y58:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 782
        value_definition = {}

    class CrossReMidX1Y59:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 790
        value_definition = {}

    class CrossReMidX1Y60:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 798
        value_definition = {}


class BGMIntEthPDU5319:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5319
    pdu_length_bytes = 204
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'PIXReLeX1': ['PIXReLeX1Y1', 'PIXReLeX1Y2', 'PIXReLeX1Y3', 'PIXReLeX1Y4', 'PIXReLeX1Y5', 'PIXReLeX1Y6', 'PIXReLeX1IsY1Yellow', 'PIXReLeX1IsY2Yellow', 'PIXReLeX1IsY3Yellow', 'PIXReLeX1IsY4Yellow', 'PIXReLeX1IsY5Yellow', 'PIXReLeX1IsY6Yellow'], 'PIXReLeX2': ['PIXReLeX2Y1', 'PIXReLeX2Y2', 'PIXReLeX2Y3', 'PIXReLeX2Y4', 'PIXReLeX2Y5', 'PIXReLeX2Y6', 'PIXReLeX2IsY1Yellow', 'PIXReLeX2IsY2Yellow', 'PIXReLeX2IsY3Yellow', 'PIXReLeX2IsY4Yellow', 'PIXReLeX2IsY5Yellow', 'PIXReLeX2IsY6Yellow'], 'PIXReLeX3': ['PIXReLeX3Y1', 'PIXReLeX3Y2', 'PIXReLeX3Y3', 'PIXReLeX3Y4', 'PIXReLeX3Y5', 'PIXReLeX3Y6'], 'PIXReLeX4': ['PIXReLeX4Y1', 'PIXReLeX4Y2', 'PIXReLeX4Y3', 'PIXReLeX4Y4', 'PIXReLeX4Y5', 'PIXReLeX4Y6'], 'PIXReLeX5': ['PIXReLeX5Y1', 'PIXReLeX5Y2', 'PIXReLeX5Y3', 'PIXReLeX5Y4', 'PIXReLeX5Y5', 'PIXReLeX5Y6'], 'PIXReLeX6': ['PIXReLeX6Y1', 'PIXReLeX6Y2', 'PIXReLeX6Y3', 'PIXReLeX6Y4', 'PIXReLeX6Y5', 'PIXReLeX6Y6'], 'PIXReLeX7': ['PIXReLeX7Y1', 'PIXReLeX7Y2', 'PIXReLeX7Y3', 'PIXReLeX7Y4', 'PIXReLeX7Y5', 'PIXReLeX7Y6'], 'PIXReLeX8': ['PIXReLeX8Y1', 'PIXReLeX8Y2', 'PIXReLeX8Y3', 'PIXReLeX8Y4', 'PIXReLeX8Y5', 'PIXReLeX8Y6'], 'PIXReLeX9': ['PIXReLeX9Y1', 'PIXReLeX9Y2', 'PIXReLeX9Y3', 'PIXReLeX9Y4', 'PIXReLeX9Y5', 'PIXReLeX9Y6'], 'PIXReLeXA': ['PIXReLeXAY1', 'PIXReLeXAY2', 'PIXReLeXAY3', 'PIXReLeXAY4', 'PIXReLeXAY5', 'PIXReLeXAY6'], 'PIXReLeXB': ['PIXReLeXBY1', 'PIXReLeXBY2', 'PIXReLeXBY3', 'PIXReLeXBY4', 'PIXReLeXBY5', 'PIXReLeXBY6'], 'PIXReLeXC': ['PIXReLeXCY1', 'PIXReLeXCY2', 'PIXReLeXCY3', 'PIXReLeXCY4', 'PIXReLeXCY5', 'PIXReLeXCY6'], 'PIXReLeXD': ['PIXReLeXDY1', 'PIXReLeXDY2', 'PIXReLeXDY3', 'PIXReLeXDY4', 'PIXReLeXDY5', 'PIXReLeXDY6'], 'PIXReLeXE': ['PIXReLeXEY1', 'PIXReLeXEY2', 'PIXReLeXEY3', 'PIXReLeXEY4', 'PIXReLeXEY5', 'PIXReLeXEY6'], 'PIXReLeXF': ['PIXReLeXFY1', 'PIXReLeXFY2', 'PIXReLeXFY3', 'PIXReLeXFY4', 'PIXReLeXFY5', 'PIXReLeXFY6'], 'PIXReRiX1': ['PIXReRiX1Y1', 'PIXReRiX1Y2', 'PIXReRiX1Y3', 'PIXReRiX1Y4', 'PIXReRiX1Y5', 'PIXReRiX1Y6', 'PIXReRiX1IsY1Yellow', 'PIXReRiX1IsY2Yellow', 'PIXReRiX1IsY3Yellow', 'PIXReRiX1IsY4Yellow', 'PIXReRiX1IsY5Yellow', 'PIXReRiX1IsY6Yellow'], 'PIXReRiX2': ['PIXReRiX2Y1', 'PIXReRiX2Y2', 'PIXReRiX2Y3', 'PIXReRiX2Y4', 'PIXReRiX2Y5', 'PIXReRiX2Y6', 'PIXReRiX2IsY1Yellow', 'PIXReRiX2IsY2Yellow', 'PIXReRiX2IsY3Yellow', 'PIXReRiX2IsY4Yellow', 'PIXReRiX2IsY5Yellow', 'PIXReRiX2IsY6Yellow'], 'PIXReRiX3': ['PIXReRiX3Y1', 'PIXReRiX3Y2', 'PIXReRiX3Y3', 'PIXReRiX3Y4', 'PIXReRiX3Y5', 'PIXReRiX3Y6'], 'PIXReRiX4': ['PIXReRiX4Y1', 'PIXReRiX4Y2', 'PIXReRiX4Y3', 'PIXReRiX4Y4', 'PIXReRiX4Y5', 'PIXReRiX4Y6'], 'PIXReRiX5': ['PIXReRiX5Y1', 'PIXReRiX5Y2', 'PIXReRiX5Y3', 'PIXReRiX5Y4', 'PIXReRiX5Y5', 'PIXReRiX5Y6'], 'PIXReRiX6': ['PIXReRiX6Y1', 'PIXReRiX6Y2', 'PIXReRiX6Y3', 'PIXReRiX6Y4', 'PIXReRiX6Y5', 'PIXReRiX6Y6'], 'PIXReRiX7': ['PIXReRiX7Y1', 'PIXReRiX7Y2', 'PIXReRiX7Y3', 'PIXReRiX7Y4', 'PIXReRiX7Y5', 'PIXReRiX7Y6'], 'PIXReRiX8': ['PIXReRiX8Y1', 'PIXReRiX8Y2', 'PIXReRiX8Y3', 'PIXReRiX8Y4', 'PIXReRiX8Y5', 'PIXReRiX8Y6'], 'PIXReRiX9': ['PIXReRiX9Y1', 'PIXReRiX9Y2', 'PIXReRiX9Y3', 'PIXReRiX9Y4', 'PIXReRiX9Y5', 'PIXReRiX9Y6'], 'PIXReRiXA': ['PIXReRiXAY1', 'PIXReRiXAY2', 'PIXReRiXAY3', 'PIXReRiXAY4', 'PIXReRiXAY5', 'PIXReRiXAY6'], 'PIXReRiXB': ['PIXReRiXBY1', 'PIXReRiXBY2', 'PIXReRiXBY3', 'PIXReRiXBY4', 'PIXReRiXBY5', 'PIXReRiXBY6'], 'PIXReRiXC': ['PIXReRiXCY1', 'PIXReRiXCY2', 'PIXReRiXCY3', 'PIXReRiXCY4', 'PIXReRiXCY5', 'PIXReRiXCY6'], 'PIXReRiXD': ['PIXReRiXDY1', 'PIXReRiXDY2', 'PIXReRiXDY3', 'PIXReRiXDY4', 'PIXReRiXDY5', 'PIXReRiXDY6'], 'PIXReRiXE': ['PIXReRiXEY1', 'PIXReRiXEY2', 'PIXReRiXEY3', 'PIXReRiXEY4', 'PIXReRiXEY5', 'PIXReRiXEY6'], 'PIXReRiXF': ['PIXReRiXFY1', 'PIXReRiXFY2', 'PIXReRiXFY3', 'PIXReRiXFY4', 'PIXReRiXFY5', 'PIXReRiXFY6']}

    class PIXReLeX1Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 6
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX1Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 14
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX1Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 22
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX1Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 30
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX1Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 38
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX1Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 46
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX1IsY1Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 48
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX1IsY2Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 56
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX1IsY3Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 64
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX1IsY4Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 72
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX1IsY5Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 80
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX1IsY6Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 88
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 102
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 110
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 118
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 126
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 134
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 142
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2IsY1Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 144
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2IsY2Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 152
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2IsY3Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 160
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2IsY4Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 168
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2IsY5Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 176
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX2IsY6Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 184
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReLeX3Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 198
        value_definition = {}

    class PIXReLeX3Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 206
        value_definition = {}

    class PIXReLeX3Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 214
        value_definition = {}

    class PIXReLeX3Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 222
        value_definition = {}

    class PIXReLeX3Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 230
        value_definition = {}

    class PIXReLeX3Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 238
        value_definition = {}

    class PIXReLeX4Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 246
        value_definition = {}

    class PIXReLeX4Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 254
        value_definition = {}

    class PIXReLeX4Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 262
        value_definition = {}

    class PIXReLeX4Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 270
        value_definition = {}

    class PIXReLeX4Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 278
        value_definition = {}

    class PIXReLeX4Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 286
        value_definition = {}

    class PIXReLeX5Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 294
        value_definition = {}

    class PIXReLeX5Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 302
        value_definition = {}

    class PIXReLeX5Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 310
        value_definition = {}

    class PIXReLeX5Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 318
        value_definition = {}

    class PIXReLeX5Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 326
        value_definition = {}

    class PIXReLeX5Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 334
        value_definition = {}

    class PIXReLeX6Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 342
        value_definition = {}

    class PIXReLeX6Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 350
        value_definition = {}

    class PIXReLeX6Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 358
        value_definition = {}

    class PIXReLeX6Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 366
        value_definition = {}

    class PIXReLeX6Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 374
        value_definition = {}

    class PIXReLeX6Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 382
        value_definition = {}

    class PIXReLeX7Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 390
        value_definition = {}

    class PIXReLeX7Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 398
        value_definition = {}

    class PIXReLeX7Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 406
        value_definition = {}

    class PIXReLeX7Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 414
        value_definition = {}

    class PIXReLeX7Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 422
        value_definition = {}

    class PIXReLeX7Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 430
        value_definition = {}

    class PIXReLeX8Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 438
        value_definition = {}

    class PIXReLeX8Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 446
        value_definition = {}

    class PIXReLeX8Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 454
        value_definition = {}

    class PIXReLeX8Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 462
        value_definition = {}

    class PIXReLeX8Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 470
        value_definition = {}

    class PIXReLeX8Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 478
        value_definition = {}

    class PIXReLeX9Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 486
        value_definition = {}

    class PIXReLeX9Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 494
        value_definition = {}

    class PIXReLeX9Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 502
        value_definition = {}

    class PIXReLeX9Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 510
        value_definition = {}

    class PIXReLeX9Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 518
        value_definition = {}

    class PIXReLeX9Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 526
        value_definition = {}

    class PIXReLeXAY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 534
        value_definition = {}

    class PIXReLeXAY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 542
        value_definition = {}

    class PIXReLeXAY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 550
        value_definition = {}

    class PIXReLeXAY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 558
        value_definition = {}

    class PIXReLeXAY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 566
        value_definition = {}

    class PIXReLeXAY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 574
        value_definition = {}

    class PIXReLeXBY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 582
        value_definition = {}

    class PIXReLeXBY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 590
        value_definition = {}

    class PIXReLeXBY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 598
        value_definition = {}

    class PIXReLeXBY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 606
        value_definition = {}

    class PIXReLeXBY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 614
        value_definition = {}

    class PIXReLeXBY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 622
        value_definition = {}

    class PIXReLeXCY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 630
        value_definition = {}

    class PIXReLeXCY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 638
        value_definition = {}

    class PIXReLeXCY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 646
        value_definition = {}

    class PIXReLeXCY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 654
        value_definition = {}

    class PIXReLeXCY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 662
        value_definition = {}

    class PIXReLeXCY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 670
        value_definition = {}

    class PIXReLeXDY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 678
        value_definition = {}

    class PIXReLeXDY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 686
        value_definition = {}

    class PIXReLeXDY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 694
        value_definition = {}

    class PIXReLeXDY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 702
        value_definition = {}

    class PIXReLeXDY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 710
        value_definition = {}

    class PIXReLeXDY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 718
        value_definition = {}

    class PIXReLeXEY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 726
        value_definition = {}

    class PIXReLeXEY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 734
        value_definition = {}

    class PIXReLeXEY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 742
        value_definition = {}

    class PIXReLeXEY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 750
        value_definition = {}

    class PIXReLeXEY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 758
        value_definition = {}

    class PIXReLeXEY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 766
        value_definition = {}

    class PIXReLeXFY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 774
        value_definition = {}

    class PIXReLeXFY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 782
        value_definition = {}

    class PIXReLeXFY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 790
        value_definition = {}

    class PIXReLeXFY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 798
        value_definition = {}

    class PIXReLeXFY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 806
        value_definition = {}

    class PIXReLeXFY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 814
        value_definition = {}

    class PIXReRiX1Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 822
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX1Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 830
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX1Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 838
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX1Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 846
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX1Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 854
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX1Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 862
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX1IsY1Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 864
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX1IsY2Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 872
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX1IsY3Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 880
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX1IsY4Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 888
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX1IsY5Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 896
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX1IsY6Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 904
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 918
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 926
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 934
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 942
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 950
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 958
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2IsY1Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 960
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2IsY2Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 968
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2IsY3Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 976
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2IsY4Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 984
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2IsY5Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 992
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX2IsY6Yellow:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 1
        start_position = 1000
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PIXReRiX3Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1014
        value_definition = {}

    class PIXReRiX3Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1022
        value_definition = {}

    class PIXReRiX3Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1030
        value_definition = {}

    class PIXReRiX3Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1038
        value_definition = {}

    class PIXReRiX3Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1046
        value_definition = {}

    class PIXReRiX3Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1054
        value_definition = {}

    class PIXReRiX4Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1062
        value_definition = {}

    class PIXReRiX4Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1070
        value_definition = {}

    class PIXReRiX4Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1078
        value_definition = {}

    class PIXReRiX4Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1086
        value_definition = {}

    class PIXReRiX4Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1094
        value_definition = {}

    class PIXReRiX4Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1102
        value_definition = {}

    class PIXReRiX5Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1110
        value_definition = {}

    class PIXReRiX5Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1118
        value_definition = {}

    class PIXReRiX5Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1126
        value_definition = {}

    class PIXReRiX5Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1134
        value_definition = {}

    class PIXReRiX5Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1142
        value_definition = {}

    class PIXReRiX5Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1150
        value_definition = {}

    class PIXReRiX6Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1158
        value_definition = {}

    class PIXReRiX6Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1166
        value_definition = {}

    class PIXReRiX6Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1174
        value_definition = {}

    class PIXReRiX6Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1182
        value_definition = {}

    class PIXReRiX6Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1190
        value_definition = {}

    class PIXReRiX6Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1198
        value_definition = {}

    class PIXReRiX7Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1206
        value_definition = {}

    class PIXReRiX7Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1214
        value_definition = {}

    class PIXReRiX7Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1222
        value_definition = {}

    class PIXReRiX7Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1230
        value_definition = {}

    class PIXReRiX7Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1238
        value_definition = {}

    class PIXReRiX7Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1246
        value_definition = {}

    class PIXReRiX8Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1254
        value_definition = {}

    class PIXReRiX8Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1262
        value_definition = {}

    class PIXReRiX8Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1270
        value_definition = {}

    class PIXReRiX8Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1278
        value_definition = {}

    class PIXReRiX8Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1286
        value_definition = {}

    class PIXReRiX8Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1294
        value_definition = {}

    class PIXReRiX9Y1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1302
        value_definition = {}

    class PIXReRiX9Y2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1310
        value_definition = {}

    class PIXReRiX9Y3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1318
        value_definition = {}

    class PIXReRiX9Y4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1326
        value_definition = {}

    class PIXReRiX9Y5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1334
        value_definition = {}

    class PIXReRiX9Y6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1342
        value_definition = {}

    class PIXReRiXAY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1350
        value_definition = {}

    class PIXReRiXAY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1358
        value_definition = {}

    class PIXReRiXAY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1366
        value_definition = {}

    class PIXReRiXAY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1374
        value_definition = {}

    class PIXReRiXAY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1382
        value_definition = {}

    class PIXReRiXAY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1390
        value_definition = {}

    class PIXReRiXBY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1398
        value_definition = {}

    class PIXReRiXBY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1406
        value_definition = {}

    class PIXReRiXBY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1414
        value_definition = {}

    class PIXReRiXBY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1422
        value_definition = {}

    class PIXReRiXBY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1430
        value_definition = {}

    class PIXReRiXBY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1438
        value_definition = {}

    class PIXReRiXCY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1446
        value_definition = {}

    class PIXReRiXCY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1454
        value_definition = {}

    class PIXReRiXCY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1462
        value_definition = {}

    class PIXReRiXCY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1470
        value_definition = {}

    class PIXReRiXCY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1478
        value_definition = {}

    class PIXReRiXCY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1486
        value_definition = {}

    class PIXReRiXDY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1494
        value_definition = {}

    class PIXReRiXDY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1502
        value_definition = {}

    class PIXReRiXDY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1510
        value_definition = {}

    class PIXReRiXDY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1518
        value_definition = {}

    class PIXReRiXDY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1526
        value_definition = {}

    class PIXReRiXDY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1534
        value_definition = {}

    class PIXReRiXEY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1542
        value_definition = {}

    class PIXReRiXEY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1550
        value_definition = {}

    class PIXReRiXEY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1558
        value_definition = {}

    class PIXReRiXEY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1566
        value_definition = {}

    class PIXReRiXEY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1574
        value_definition = {}

    class PIXReRiXEY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1582
        value_definition = {}

    class PIXReRiXFY1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1590
        value_definition = {}

    class PIXReRiXFY2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1598
        value_definition = {}

    class PIXReRiXFY3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1606
        value_definition = {}

    class PIXReRiXFY4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1614
        value_definition = {}

    class PIXReRiXFY5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1622
        value_definition = {}

    class PIXReRiXFY6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 1630
        value_definition = {}


class BGMIntEthPDU5320:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5320
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ReverseRi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class ReFogLe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 14
        value_definition = {}


class BGMIntEthPDU5321:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5321
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class WheelLampFrntLe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class WheelLampFrntRi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 14
        value_definition = {}

    class WheelLampRearLe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 22
        value_definition = {}

    class WheelLampRearRi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "灯光秀像素设置"
        signal_length = 7
        start_position = 30
        value_definition = {}


class BGMIntEthPDU5322:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5322
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class OuterDoorSwLightReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "车门按键指示灯模式"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OFF', '0x1': 'ON_Static', '0x2': 'ON_Dynamic'}


class BGMIntEthPDU5323:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5323
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-100ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DirHoldFlagFromACU:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "设置转向灯保持标志"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5402:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5402
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ClsAutEna:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "锁车自动关窗开启关闭设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'EnableDisableCoding_Disabled', '0x1': 'EnableDisableCoding_Enabled'}


class BGMIntEthPDU5403:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5403
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetAutLockInGearP:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "P档解锁功能开启关闭设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5404:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5404
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ChdLockReLeCtrlHmiReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "童锁控制左后"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'LockgCenReq2_Idle', '0x1': 'LockgCenReq2_Unlck', '0x2': 'LockgCenReq2_Lock'}


class BGMIntEthPDU5405:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5405
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ChdLockReRiCtrlHmiReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "童锁控制右后"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'LockgCenReq2_Idle', '0x1': 'LockgCenReq2_Unlck', '0x2': 'LockgCenReq2_Lock'}


class BGMIntEthPDU5406:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5406
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class CenLockHmiReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "整车解闭控制(中控)"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'LockgCenReq2_Idle', '0x1': 'LockgCenReq2_Unlck', '0x2': 'LockgCenReq2_Lock'}


class BGMIntEthPDU5407:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5407
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VehPrkgLockTheftReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "整车解闭控制(PA)"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'VehPrkgLockTheftReq_NoRequest', '0x1': 'VehPrkgLockTheftReq_InsideLockAndIncompleteArmRequest', '0x2': 'VehPrkgLockTheftReq_OutsideLockAndCompleteArmRequest', '0x3': 'VehPrkgLockTheftReq_UnlockAndDisarmRequest'}


class BGMIntEthPDU5409:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5409
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmCenLockReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Telematics控制整车解闭锁"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'MobDevCenLockReq_NoRequest', '0x1': 'MobDevCenLockReq_Unlock', '0x2': 'MobDevCenLockReq_NormalLock', '0x3': 'MobDevCenLockReq_LockWithAllDoorClosed', '0x4': 'MobDevCenLockReq_Reserved1', '0x5': 'MobDevCenLockReq_Reserved2', '0x6': 'MobDevCenLockReq_Reserved3', '0x7': 'MobDevCenLockReq_Reserved4'}


class BGMIntEthPDU5451:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5451
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class IntrLampSelnMod:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 2
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "内灯模式控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OffOnAut1_Off', '0x1': 'OffOnAut1_On', '0x2': 'OffOnAut1_Aut'}


class BGMIntEthPDU5452:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5452
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'IntrBriLvlCtrlSts': ['IntrBriLvlCtrlStsIdPen1', 'IntrBriLvlCtrlStsIntrBriSts']}

    class IntrBriLvlCtrlStsIdPen1:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "背光灯亮度调节-Idpen"
        signal_length = 4
        start_position = 3
        value_definition = {}

    class IntrBriLvlCtrlStsIntrBriSts:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "背光灯亮度调节level"
        signal_length = 4
        start_position = 11
        value_definition = {}


class BGMIntEthPDU5453:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5453
    pdu_length_bytes = 6
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'ReadLiOpenReq': ['ReadLiOpenReqFrontLeft', 'ReadLiOpenReqFrontRight', 'ReadLiOpenReqSecondRowLeft', 'ReadLiOpenReqSecondRowRight', 'ReadLiOpenReqThirdRowLeft', 'ReadLiOpenReqThirdRowRight']}

    class ReadLiOpenReqFrontLeft:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "阅读灯开关控制前左"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}

    class ReadLiOpenReqFrontRight:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "阅读灯开关控制前右"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}

    class ReadLiOpenReqSecondRowLeft:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "阅读灯开关控制二排左"
        signal_length = 2
        start_position = 17
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}

    class ReadLiOpenReqSecondRowRight:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "阅读灯开关控制二排右"
        signal_length = 2
        start_position = 25
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}

    class ReadLiOpenReqThirdRowLeft:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "阅读灯开关控制三排左"
        signal_length = 2
        start_position = 33
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}

    class ReadLiOpenReqThirdRowRight:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "阅读灯开关控制三排右"
        signal_length = 2
        start_position = 41
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU5454:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5454
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class IfPThenIsOrNotCourtesy:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "P档触发迎宾功能开关设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU5502:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5502
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class WiprFrntSrvModReq:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "前雨刮维修模式控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'WiprSrvModReq_NoActn', '0x1': 'WiprSrvModReq_ActvtSrvPosn', '0x2': 'WiprSrvModReq_DeActvtSrvPosn'}


class BGMIntEthPDU5503:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5503
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class WinWshrLvrCmd:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "洗涤控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'WinWshrLvrCmd1_WinWshrOff', '0x1': 'WinWshrLvrCmd1_FrntWshrCmd', '0x2': 'WinWshrLvrCmd1_ReWshrCmd'}


class BGMIntEthPDU5504:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5504
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'FrntWiprSelnMod': ['FrntWiprSelnModFrntWiprSelnMod', 'FrntWiprSelnModFrntWiprSelnModQf', 'FrntWiprSelnModFrntWiprSelnModChks', 'FrntWiprSelnModFrntWiprSelnModCntr']}

    class FrntWiprSelnModFrntWiprSelnMod:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "前雨刮模式设置withE2E"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'WiprMod_Off', '0x1': 'WiprMod_SingleWipe', '0x2': 'WiprMod_IntLow', '0x3': 'WiprMod_IntHigh', '0x4': 'WiprMod_Low', '0x5': 'WiprMod_High', '0x6': 'WiprMod_Auto', '0x7': 'WiprMod_Error'}

    class FrntWiprSelnModFrntWiprSelnModQf:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "前雨刮模式设置withE2E"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'WiprMod_Off', '0x1': 'WiprMod_SingleWipe', '0x2': 'WiprMod_IntLow', '0x3': 'WiprMod_IntHigh', '0x4': 'WiprMod_Low', '0x5': 'WiprMod_High', '0x6': 'WiprMod_Auto', '0x7': 'WiprMod_Error'}

    class FrntWiprSelnModFrntWiprSelnModChks:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "前雨刮模式设置withE2E"
        signal_length = 8
        start_position = 23
        value_definition = {'0x0': 'WiprMod_Off', '0x1': 'WiprMod_SingleWipe', '0x2': 'WiprMod_IntLow', '0x3': 'WiprMod_IntHigh', '0x4': 'WiprMod_Low', '0x5': 'WiprMod_High', '0x6': 'WiprMod_Auto', '0x7': 'WiprMod_Error'}

    class FrntWiprSelnModFrntWiprSelnModCntr:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "前雨刮模式设置withE2E"
        signal_length = 4
        start_position = 27
        value_definition = {'0x0': 'WiprMod_Off', '0x1': 'WiprMod_SingleWipe', '0x2': 'WiprMod_IntLow', '0x3': 'WiprMod_IntHigh', '0x4': 'WiprMod_Low', '0x5': 'WiprMod_High', '0x6': 'WiprMod_Auto', '0x7': 'WiprMod_Error'}


class BGMIntEthPDU5551:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5551
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ActvReSplrSeldCmd:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "主动尾翼模式控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OffOnAut1_Off', '0x1': 'OffOnAut1_On', '0x2': 'OffOnAut1_Aut'}


class BGMIntEthPDU5552:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 5552
    pdu_length_bytes = 4
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'ActvReSplrSts': ['ActvReSplrStsAvlStsForCDC', 'ActvReSplrStsCtrlSts2', 'ActvReSplrStsNotAvlEve', 'ActvReSplrStsAvlStsForCenLockg']}

    class ActvReSplrStsAvlStsForCDC:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "尾翼控制可用状态For外部调用"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'AvlSts2_NotAvl', '0x1': 'AvlSts2_Avl'}

    class ActvReSplrStsCtrlSts2:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "尾翼动作触发源"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'AvlSts2_NotAvl', '0x1': 'AvlSts2_Avl'}

    class ActvReSplrStsNotAvlEve:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "尾翼控制不可用原因"
        signal_length = 4
        start_position = 19
        value_definition = {'0x0': 'AvlSts2_NotAvl', '0x1': 'AvlSts2_Avl'}

    class ActvReSplrStsAvlStsForCenLockg:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "尾翼控制可用状态For中控锁"
        signal_length = 1
        start_position = 24
        value_definition = {'0x0': 'AvlSts2_NotAvl', '0x1': 'AvlSts2_Avl'}


class BGMIntEthPDU5651:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5651
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'DoorDrvrOpenHmiReq': ['DoorDrvrOpenHmiReqDoorOpenerReq1', 'DoorDrvrOpenHmiReqChks', 'DoorDrvrOpenHmiReqCntr']}

    class DoorDrvrOpenHmiReqDoorOpenerReq1:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "主驾驶电动门运动控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}

    class DoorDrvrOpenHmiReqChks:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "主驾驶电动门运动控制CheckSum"
        signal_length = 8
        start_position = 15
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}

    class DoorDrvrOpenHmiReqCntr:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "主驾驶电动门运动控制RollingCounter"
        signal_length = 4
        start_position = 19
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}


class BGMIntEthPDU5652:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5652
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'DoorPassOpenHmiReq': ['DoorPassOpenHmiReqDoorOpenerReq1', 'DoorPassOpenHmiReqChks', 'DoorPassOpenHmiReqCntr']}

    class DoorPassOpenHmiReqDoorOpenerReq1:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "副驾驶电动门运动控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}

    class DoorPassOpenHmiReqChks:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "副驾驶电动门运动控制CheckSum"
        signal_length = 8
        start_position = 15
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}

    class DoorPassOpenHmiReqCntr:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "副驾驶电动门运动控制RollingCounter"
        signal_length = 4
        start_position = 19
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}


class BGMIntEthPDU5653:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5653
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'DoorLeReOpenHmiReq': ['DoorLeReOpenHmiReqDoorOpenerReq1', 'DoorLeReOpenHmiReqChks', 'DoorLeReOpenHmiReqCntr']}

    class DoorLeReOpenHmiReqDoorOpenerReq1:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "左后电动门运动控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}

    class DoorLeReOpenHmiReqChks:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "左后电动门运动控制CheckSum"
        signal_length = 8
        start_position = 15
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}

    class DoorLeReOpenHmiReqCntr:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "左后电动门运动控制RollingCounter"
        signal_length = 4
        start_position = 19
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}


class BGMIntEthPDU5654:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5654
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'DoorRiReOpenHmiReq': ['DoorRiReOpenHmiReqDoorOpenerReq1', 'DoorRiReOpenHmiReqChks', 'DoorRiReOpenHmiReqCntr']}

    class DoorRiReOpenHmiReqDoorOpenerReq1:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "右后电动门运动控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}

    class DoorRiReOpenHmiReqChks:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "右后电动门运动控制CheckSum"
        signal_length = 8
        start_position = 15
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}

    class DoorRiReOpenHmiReqCntr:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "右后电动门运动控制RollingCounter"
        signal_length = 4
        start_position = 19
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}


class BGMIntEthPDU5655:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5655
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetPwrDoorClsInGearDR:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "电动门D档关门设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5656:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5656
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetPwrDoorFeel:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "电动门手动操作力设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ClassnQly_Low', '0x1': 'ClassnQly_Medium', '0x2': 'ClassnQly_High'}


class BGMIntEthPDU5657:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5657
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetPwrDoorWindCatch:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "电动门风抖消除设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5658:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5658
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetPwrDoorOpenSpd:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "电动门开启速度设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ClassnQly_Low', '0x1': 'ClassnQly_Medium', '0x2': 'ClassnQly_High'}


class BGMIntEthPDU5659:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5659
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetPwrDoorClsSpd:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "电动门关闭速度设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ClassnQly_Low', '0x1': 'ClassnQly_Medium', '0x2': 'ClassnQly_High'}


class BGMIntEthPDU5660:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5660
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DoorDrvrPercSetFromHmi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾驶电动门最大开度设置"
        signal_length = 7
        start_position = 6
        value_definition = {}


class BGMIntEthPDU5661:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5661
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DoorPassPercSetFromHmi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾驶电动门最大开度设置"
        signal_length = 7
        start_position = 6
        value_definition = {}


class BGMIntEthPDU5662:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5662
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DoorLeRePercSetFromHmi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左后电动门最大开度设置"
        signal_length = 7
        start_position = 6
        value_definition = {}


class BGMIntEthPDU5663:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5663
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DoorRiRePercSetFromHmi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左后电动门最大开度设置"
        signal_length = 7
        start_position = 6
        value_definition = {}


class BGMIntEthPDU5664:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5664
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DoorDrvrTargPercReqFromHmi:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾驶电动门开度控制"
        signal_length = 7
        start_position = 6
        value_definition = {}


class BGMIntEthPDU5665:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5665
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DoorPassTargPercReqFromHmi:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾驶电动门开度控制"
        signal_length = 7
        start_position = 6
        value_definition = {}


class BGMIntEthPDU5666:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5666
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DoorLeReTargPercReqFromHmi:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左后电动门开度控制"
        signal_length = 7
        start_position = 6
        value_definition = {}


class BGMIntEthPDU5667:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5667
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DoorRiReTargPercReqFromHmi:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左后电动门开度控制"
        signal_length = 7
        start_position = 6
        value_definition = {}


class BGMIntEthPDU5668:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5668
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetDrvrPwrDoorAutOperMode:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾驶电动门开启模式设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5669:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5669
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetPassPwrDoorAutOperMode:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾驶电动门开启模式设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5670:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5670
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetLeRePwrDoorAutOperMode:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左后电动门开启模式设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5671:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5671
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetRiRePwrDoorAutOperMode:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "右后电动门开启模式设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5673:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5673
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetDRMMode:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "设置电动门雷达工作模式"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'No_Request', '0x1': 'Sentry_Mode', '0x2': 'AVP_Mode', '0x3': 'Reserved_3', '0x4': 'Reserved_4', '0x5': 'Reserved_5', '0x6': 'Reserved_6', '0x7': 'Reserved_7'}


class BGMIntEthPDU5701:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5701
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class IncomingAirQlyPopUpReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "PM2.5PopUp提醒功能开启/关闭设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5702:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5702
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class IncomingAirQlyCtrlFromHmi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "PM2.5功能开启关闭设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5751:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5751
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiFragraLvlReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "香氛等级设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'LvlOff', '0x1': 'Lvl1', '0x2': 'Lvl2', '0x3': 'Lvl3'}


class BGMIntEthPDU5752:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5752
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmAirFragTasteReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "香氛型号设置"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'TelmAirFragChReq_NoReq', '0x1': 'TelmAirFragChReq_Ch1', '0x2': 'TelmAirFragChReq_Ch2', '0x3': 'TelmAirFragChReq_Ch3', '0x4': 'TelmAirFragChReq_Ch4', '0x5': 'TelmAirFragChReq_Ch5'}


class BGMIntEthPDU5753:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5753
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class FragRefrshAutSetg:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "香氛提神功能开启、关闭设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5754:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5754
    pdu_length_bytes = 5
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HmiFragraChRatReq': ['HmiFragraChRatReqFragRatForCh1', 'HmiFragraChRatReqFragRatForCh2', 'HmiFragraChRatReqFragRatForCh3', 'HmiFragraChRatReqFragRatForCh4', 'HmiFragraChRatReqFragRatForCh5']}

    class HmiFragraChRatReqFragRatForCh1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "香氛通道1浓度"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class HmiFragraChRatReqFragRatForCh2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "香氛通道2浓度"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class HmiFragraChRatReqFragRatForCh3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "香氛通道3浓度"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class HmiFragraChRatReqFragRatForCh4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "香氛通道4浓度"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class HmiFragraChRatReqFragRatForCh5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "香氛通道5浓度"
        signal_length = 8
        start_position = 39
        value_definition = {}


class BGMIntEthPDU5801:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5801
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class WinOpenDrvrReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾驶车窗位置控制"
        signal_length = 5
        start_position = 4
        value_definition = {'0x0': 'WinAndRoofAndCurtPosnTyp_PosnUkwn', '0x1': 'WinAndRoofAndCurtPosnTyp_ClsFull', '0x2': 'WinAndRoofAndCurtPosnTyp_PercOpen4', '0x3': 'WinAndRoofAndCurtPosnTyp_PercOpen8', '0x4': 'WinAndRoofAndCurtPosnTyp_PercOpen12', '0x5': 'WinAndRoofAndCurtPosnTyp_PercOpen16', '0x6': 'WinAndRoofAndCurtPosnTyp_PercOpen20', '0x7': 'WinAndRoofAndCurtPosnTyp_PercOpen24', '0x8': 'WinAndRoofAndCurtPosnTyp_PercOpen28', '0x9': 'WinAndRoofAndCurtPosnTyp_PercOpen32', '0xA': 'WinAndRoofAndCurtPosnTyp_PercOpen36', '0xB': 'WinAndRoofAndCurtPosnTyp_PercOpen40', '0xC': 'WinAndRoofAndCurtPosnTyp_PercOpen44', '0xD': 'WinAndRoofAndCurtPosnTyp_PercOpen48', '0xE': 'WinAndRoofAndCurtPosnTyp_PercOpen52', '0xF': 'WinAndRoofAndCurtPosnTyp_PercOpen56', '0x10': 'WinAndRoofAndCurtPosnTyp_PercOpen60', '0x11': 'WinAndRoofAndCurtPosnTyp_PercOpen64', '0x12': 'WinAndRoofAndCurtPosnTyp_PercOpen68', '0x13': 'WinAndRoofAndCurtPosnTyp_PercOpen72', '0x14': 'WinAndRoofAndCurtPosnTyp_PercOpen76', '0x15': 'WinAndRoofAndCurtPosnTyp_PercOpen80', '0x16': 'WinAndRoofAndCurtPosnTyp_PercOpen84', '0x17': 'WinAndRoofAndCurtPosnTyp_PercOpen88', '0x18': 'WinAndRoofAndCurtPosnTyp_PercOpen92', '0x19': 'WinAndRoofAndCurtPosnTyp_PercOpen96', '0x1A': 'WinAndRoofAndCurtPosnTyp_OpenFull', '0x1B': 'WinAndRoofAndCurtPosnTyp_Resd1', '0x1C': 'WinAndRoofAndCurtPosnTyp_Resd2', '0x1D': 'WinAndRoofAndCurtPosnTyp_Resd3', '0x1E': 'WinAndRoofAndCurtPosnTyp_Resd4', '0x1F': 'WinAndRoofAndCurtPosnTyp_Movg'}


class BGMIntEthPDU5802:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5802
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class WinOpenPassReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾驶车窗位置控制"
        signal_length = 5
        start_position = 4
        value_definition = {'0x0': 'WinAndRoofAndCurtPosnTyp_PosnUkwn', '0x1': 'WinAndRoofAndCurtPosnTyp_ClsFull', '0x2': 'WinAndRoofAndCurtPosnTyp_PercOpen4', '0x3': 'WinAndRoofAndCurtPosnTyp_PercOpen8', '0x4': 'WinAndRoofAndCurtPosnTyp_PercOpen12', '0x5': 'WinAndRoofAndCurtPosnTyp_PercOpen16', '0x6': 'WinAndRoofAndCurtPosnTyp_PercOpen20', '0x7': 'WinAndRoofAndCurtPosnTyp_PercOpen24', '0x8': 'WinAndRoofAndCurtPosnTyp_PercOpen28', '0x9': 'WinAndRoofAndCurtPosnTyp_PercOpen32', '0xA': 'WinAndRoofAndCurtPosnTyp_PercOpen36', '0xB': 'WinAndRoofAndCurtPosnTyp_PercOpen40', '0xC': 'WinAndRoofAndCurtPosnTyp_PercOpen44', '0xD': 'WinAndRoofAndCurtPosnTyp_PercOpen48', '0xE': 'WinAndRoofAndCurtPosnTyp_PercOpen52', '0xF': 'WinAndRoofAndCurtPosnTyp_PercOpen56', '0x10': 'WinAndRoofAndCurtPosnTyp_PercOpen60', '0x11': 'WinAndRoofAndCurtPosnTyp_PercOpen64', '0x12': 'WinAndRoofAndCurtPosnTyp_PercOpen68', '0x13': 'WinAndRoofAndCurtPosnTyp_PercOpen72', '0x14': 'WinAndRoofAndCurtPosnTyp_PercOpen76', '0x15': 'WinAndRoofAndCurtPosnTyp_PercOpen80', '0x16': 'WinAndRoofAndCurtPosnTyp_PercOpen84', '0x17': 'WinAndRoofAndCurtPosnTyp_PercOpen88', '0x18': 'WinAndRoofAndCurtPosnTyp_PercOpen92', '0x19': 'WinAndRoofAndCurtPosnTyp_PercOpen96', '0x1A': 'WinAndRoofAndCurtPosnTyp_OpenFull', '0x1B': 'WinAndRoofAndCurtPosnTyp_Resd1', '0x1C': 'WinAndRoofAndCurtPosnTyp_Resd2', '0x1D': 'WinAndRoofAndCurtPosnTyp_Resd3', '0x1E': 'WinAndRoofAndCurtPosnTyp_Resd4', '0x1F': 'WinAndRoofAndCurtPosnTyp_Movg'}


class BGMIntEthPDU5803:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5803
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class WinOpenReLeReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "左后车窗位置控制"
        signal_length = 5
        start_position = 4
        value_definition = {'0x0': 'WinAndRoofAndCurtPosnTyp_PosnUkwn', '0x1': 'WinAndRoofAndCurtPosnTyp_ClsFull', '0x2': 'WinAndRoofAndCurtPosnTyp_PercOpen4', '0x3': 'WinAndRoofAndCurtPosnTyp_PercOpen8', '0x4': 'WinAndRoofAndCurtPosnTyp_PercOpen12', '0x5': 'WinAndRoofAndCurtPosnTyp_PercOpen16', '0x6': 'WinAndRoofAndCurtPosnTyp_PercOpen20', '0x7': 'WinAndRoofAndCurtPosnTyp_PercOpen24', '0x8': 'WinAndRoofAndCurtPosnTyp_PercOpen28', '0x9': 'WinAndRoofAndCurtPosnTyp_PercOpen32', '0xA': 'WinAndRoofAndCurtPosnTyp_PercOpen36', '0xB': 'WinAndRoofAndCurtPosnTyp_PercOpen40', '0xC': 'WinAndRoofAndCurtPosnTyp_PercOpen44', '0xD': 'WinAndRoofAndCurtPosnTyp_PercOpen48', '0xE': 'WinAndRoofAndCurtPosnTyp_PercOpen52', '0xF': 'WinAndRoofAndCurtPosnTyp_PercOpen56', '0x10': 'WinAndRoofAndCurtPosnTyp_PercOpen60', '0x11': 'WinAndRoofAndCurtPosnTyp_PercOpen64', '0x12': 'WinAndRoofAndCurtPosnTyp_PercOpen68', '0x13': 'WinAndRoofAndCurtPosnTyp_PercOpen72', '0x14': 'WinAndRoofAndCurtPosnTyp_PercOpen76', '0x15': 'WinAndRoofAndCurtPosnTyp_PercOpen80', '0x16': 'WinAndRoofAndCurtPosnTyp_PercOpen84', '0x17': 'WinAndRoofAndCurtPosnTyp_PercOpen88', '0x18': 'WinAndRoofAndCurtPosnTyp_PercOpen92', '0x19': 'WinAndRoofAndCurtPosnTyp_PercOpen96', '0x1A': 'WinAndRoofAndCurtPosnTyp_OpenFull', '0x1B': 'WinAndRoofAndCurtPosnTyp_Resd1', '0x1C': 'WinAndRoofAndCurtPosnTyp_Resd2', '0x1D': 'WinAndRoofAndCurtPosnTyp_Resd3', '0x1E': 'WinAndRoofAndCurtPosnTyp_Resd4', '0x1F': 'WinAndRoofAndCurtPosnTyp_Movg'}


class BGMIntEthPDU5804:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5804
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class WinOpenReRiReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "右后车窗位置控制"
        signal_length = 5
        start_position = 4
        value_definition = {'0x0': 'WinAndRoofAndCurtPosnTyp_PosnUkwn', '0x1': 'WinAndRoofAndCurtPosnTyp_ClsFull', '0x2': 'WinAndRoofAndCurtPosnTyp_PercOpen4', '0x3': 'WinAndRoofAndCurtPosnTyp_PercOpen8', '0x4': 'WinAndRoofAndCurtPosnTyp_PercOpen12', '0x5': 'WinAndRoofAndCurtPosnTyp_PercOpen16', '0x6': 'WinAndRoofAndCurtPosnTyp_PercOpen20', '0x7': 'WinAndRoofAndCurtPosnTyp_PercOpen24', '0x8': 'WinAndRoofAndCurtPosnTyp_PercOpen28', '0x9': 'WinAndRoofAndCurtPosnTyp_PercOpen32', '0xA': 'WinAndRoofAndCurtPosnTyp_PercOpen36', '0xB': 'WinAndRoofAndCurtPosnTyp_PercOpen40', '0xC': 'WinAndRoofAndCurtPosnTyp_PercOpen44', '0xD': 'WinAndRoofAndCurtPosnTyp_PercOpen48', '0xE': 'WinAndRoofAndCurtPosnTyp_PercOpen52', '0xF': 'WinAndRoofAndCurtPosnTyp_PercOpen56', '0x10': 'WinAndRoofAndCurtPosnTyp_PercOpen60', '0x11': 'WinAndRoofAndCurtPosnTyp_PercOpen64', '0x12': 'WinAndRoofAndCurtPosnTyp_PercOpen68', '0x13': 'WinAndRoofAndCurtPosnTyp_PercOpen72', '0x14': 'WinAndRoofAndCurtPosnTyp_PercOpen76', '0x15': 'WinAndRoofAndCurtPosnTyp_PercOpen80', '0x16': 'WinAndRoofAndCurtPosnTyp_PercOpen84', '0x17': 'WinAndRoofAndCurtPosnTyp_PercOpen88', '0x18': 'WinAndRoofAndCurtPosnTyp_PercOpen92', '0x19': 'WinAndRoofAndCurtPosnTyp_PercOpen96', '0x1A': 'WinAndRoofAndCurtPosnTyp_OpenFull', '0x1B': 'WinAndRoofAndCurtPosnTyp_Resd1', '0x1C': 'WinAndRoofAndCurtPosnTyp_Resd2', '0x1D': 'WinAndRoofAndCurtPosnTyp_Resd3', '0x1E': 'WinAndRoofAndCurtPosnTyp_Resd4', '0x1F': 'WinAndRoofAndCurtPosnTyp_Movg'}


class BGMIntEthPDU5805:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5805
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetRainAutoClsWin:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "设置雨天自动关窗"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5806:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5806
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetWinGlbCmd1Ack:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "设置雨天关窗反馈"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU5851:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5851
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TopPercTrFromHmi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "最大开启高度设置"
        signal_length = 7
        start_position = 6
        value_definition = {}


class BGMIntEthPDU5852:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5852
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TrOpenPosnReqFromHmi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "尾门开度控制"
        signal_length = 7
        start_position = 6
        value_definition = {}


class BGMIntEthPDU5853:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5853
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TrunkOpenHmiReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "尾门运动控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'DoorOpenerIdle', '0x1': 'DoorOpenerOpen', '0x2': 'DoorOpenerCls', '0x3': 'DoorOpenerStop'}


class BGMIntEthPDU5901:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5901
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class BackRestAdjmtRowFirstDrvr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾座椅靠背调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtHozlSts1_Idle', '0x1': 'SwtHozlSts1_Fwd', '0x2': 'SwtHozlSts1_Backw'}


class BGMIntEthPDU5902:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5902
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SeatHeiAdjmtRowFirstDrvr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾座椅高度调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtVertSts1_Idle', '0x1': 'SwtVertSts1_Up', '0x2': 'SwtVertSts1_Dwn'}


class BGMIntEthPDU5903:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5903
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SeatLenAdjmtRowFirstDrvr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾座椅前后调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtHozlSts1_Idle', '0x1': 'SwtHozlSts1_Fwd', '0x2': 'SwtHozlSts1_Backw'}


class BGMIntEthPDU5904:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5904
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SeatCushTiltAdjmtRowFirstDrvr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾座椅前部坐垫高度调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtVertSts1_Idle', '0x1': 'SwtVertSts1_Up', '0x2': 'SwtVertSts1_Dwn'}


class BGMIntEthPDU5905:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5905
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class LumHeiAdjmtRowFirstDrvr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾座椅腰托高度调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtVertSts1_Idle', '0x1': 'SwtVertSts1_Up', '0x2': 'SwtVertSts1_Dwn'}


class BGMIntEthPDU5906:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5906
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class LumLenAdjmtRowFirstDrvr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾座椅腰托前后调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtHozlSts1_Idle', '0x1': 'SwtHozlSts1_Fwd', '0x2': 'SwtHozlSts1_Backw'}


class BGMIntEthPDU5907:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5907
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'DrvrSeatDispMassgFct': ['DrvrSeatDispMassgFctOnOff', 'DrvrSeatDispMassgFctMassgProg', 'DrvrSeatDispMassgFctMassgInten']}

    class DrvrSeatDispMassgFctOnOff:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾座椅按摩设置开关"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class DrvrSeatDispMassgFctMassgProg:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾座椅按摩类型设置"
        signal_length = 3
        start_position = 10
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class DrvrSeatDispMassgFctMassgInten:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾座椅按摩强度设置"
        signal_length = 2
        start_position = 17
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5911:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5911
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class BackRestAdjmtRowFirstPass:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾座椅靠背调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtHozlSts1_Idle', '0x1': 'SwtHozlSts1_Fwd', '0x2': 'SwtHozlSts1_Backw'}


class BGMIntEthPDU5912:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5912
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SeatHeiAdjmtRowFirstPass:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾座椅高度调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtVertSts1_Idle', '0x1': 'SwtVertSts1_Up', '0x2': 'SwtVertSts1_Dwn'}


class BGMIntEthPDU5913:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5913
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SeatLenAdjmtRowFirstPass:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾座椅前后调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtHozlSts1_Idle', '0x1': 'SwtHozlSts1_Fwd', '0x2': 'SwtHozlSts1_Backw'}


class BGMIntEthPDU5914:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5914
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SeatCushTiltAdjmtRowFirstPass:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾座椅前部坐垫高度调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtVertSts1_Idle', '0x1': 'SwtVertSts1_Up', '0x2': 'SwtVertSts1_Dwn'}


class BGMIntEthPDU5915:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5915
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class LumHeiAdjmtRowFirstPass:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾座椅腰托高度调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtVertSts1_Idle', '0x1': 'SwtVertSts1_Up', '0x2': 'SwtVertSts1_Dwn'}


class BGMIntEthPDU5916:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5916
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class LumLenAdjmtRowFirstPass:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾座椅腰托前后调节"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SwtHozlSts1_Idle', '0x1': 'SwtHozlSts1_Fwd', '0x2': 'SwtHozlSts1_Backw'}


class BGMIntEthPDU5917:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5917
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'PassSeatDispMassgFct': ['PassSeatDispMassgFctOnOff', 'PassSeatDispMassgFctMassgProg', 'PassSeatDispMassgFctMassgInten']}

    class PassSeatDispMassgFctOnOff:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾座椅按摩设置开关"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class PassSeatDispMassgFctMassgProg:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾座椅按摩类型设置"
        signal_length = 3
        start_position = 10
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}

    class PassSeatDispMassgFctMassgInten:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾座椅按摩强度设置"
        signal_length = 2
        start_position = 17
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU5951:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5951
    pdu_length_bytes = 8
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HmiSeatClima': ['HmiSeatClimaHmiSeatHeatgForRowFirstLe', 'HmiSeatClimaHmiSeatHeatgForRowFirstRi', 'HmiSeatClimaHmiSeatHeatgForRowSecLe', 'HmiSeatClimaHmiSeatHeatgForRowSecRi', 'HmiSeatClimaHmiSeatVentnForRowFirstLe', 'HmiSeatClimaHmiSeatVentnForRowFirstRi', 'HmiSeatClimaHmiSeatVentnForRowSecLe', 'HmiSeatClimaHmiSeatVentnForRowSecRi']}

    class HmiSeatClimaHmiSeatHeatgForRowFirstLe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "一排左加热等级"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SeatClimaLvl_Off', '0x1': 'SeatClimaLvl_Lvl1', '0x2': 'SeatClimaLvl_Lvl2', '0x3': 'SeatClimaLvl_Lvl3'}

    class HmiSeatClimaHmiSeatHeatgForRowFirstRi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "一排右加热等级"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'SeatClimaLvl_Off', '0x1': 'SeatClimaLvl_Lvl1', '0x2': 'SeatClimaLvl_Lvl2', '0x3': 'SeatClimaLvl_Lvl3'}

    class HmiSeatClimaHmiSeatHeatgForRowSecLe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "二排左加热等级"
        signal_length = 2
        start_position = 17
        value_definition = {'0x0': 'SeatClimaLvl_Off', '0x1': 'SeatClimaLvl_Lvl1', '0x2': 'SeatClimaLvl_Lvl2', '0x3': 'SeatClimaLvl_Lvl3'}

    class HmiSeatClimaHmiSeatHeatgForRowSecRi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "二排右加热等级"
        signal_length = 2
        start_position = 25
        value_definition = {'0x0': 'SeatClimaLvl_Off', '0x1': 'SeatClimaLvl_Lvl1', '0x2': 'SeatClimaLvl_Lvl2', '0x3': 'SeatClimaLvl_Lvl3'}

    class HmiSeatClimaHmiSeatVentnForRowFirstLe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "一排左通风等级"
        signal_length = 2
        start_position = 33
        value_definition = {'0x0': 'SeatClimaLvl_Off', '0x1': 'SeatClimaLvl_Lvl1', '0x2': 'SeatClimaLvl_Lvl2', '0x3': 'SeatClimaLvl_Lvl3'}

    class HmiSeatClimaHmiSeatVentnForRowFirstRi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "一排右通风等级"
        signal_length = 2
        start_position = 41
        value_definition = {'0x0': 'SeatClimaLvl_Off', '0x1': 'SeatClimaLvl_Lvl1', '0x2': 'SeatClimaLvl_Lvl2', '0x3': 'SeatClimaLvl_Lvl3'}

    class HmiSeatClimaHmiSeatVentnForRowSecLe:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "二排左通风等级"
        signal_length = 2
        start_position = 49
        value_definition = {'0x0': 'SeatClimaLvl_Off', '0x1': 'SeatClimaLvl_Lvl1', '0x2': 'SeatClimaLvl_Lvl2', '0x3': 'SeatClimaLvl_Lvl3'}

    class HmiSeatClimaHmiSeatVentnForRowSecRi:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "二排右通风等级"
        signal_length = 2
        start_position = 57
        value_definition = {'0x0': 'SeatClimaLvl_Off', '0x1': 'SeatClimaLvl_Lvl1', '0x2': 'SeatClimaLvl_Lvl2', '0x3': 'SeatClimaLvl_Lvl3'}


class BGMIntEthPDU5952:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5952
    pdu_length_bytes = 9
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'HmiSeatClimaTmr': ['HmiSeatClimaTmrHmiSeatHeatgFirstLeTmr', 'HmiSeatClimaTmrHmiSeatHeatgFirstRiTmr', 'HmiSeatClimaTmrHmiSeatHeatgSecLeTmr', 'HmiSeatClimaTmrHmiSeatHeatgSecRiTmr', 'HmiSeatClimaTmrHmiSeatVentnFirstLeTmr', 'HmiSeatClimaTmrHmiSeatVentnFirstRiTmr', 'HmiSeatClimaTmrHmiSeatVentnSecLeTmr', 'HmiSeatClimaTmrHmiSeatVentnSecRiTmr', 'HmiSeatClimaTmrIdPen']}

    class HmiSeatClimaTmrHmiSeatHeatgFirstLeTmr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 15
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "一排左加热时间"
        signal_length = 6
        start_position = 5
        value_definition = {}

    class HmiSeatClimaTmrHmiSeatHeatgFirstRiTmr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 15
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "一排右加热时间"
        signal_length = 6
        start_position = 13
        value_definition = {}

    class HmiSeatClimaTmrHmiSeatHeatgSecLeTmr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 15
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "二排左加热时间"
        signal_length = 6
        start_position = 21
        value_definition = {}

    class HmiSeatClimaTmrHmiSeatHeatgSecRiTmr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 15
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "二排右加热时间"
        signal_length = 6
        start_position = 29
        value_definition = {}

    class HmiSeatClimaTmrHmiSeatVentnFirstLeTmr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 15
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "一排左通风时间"
        signal_length = 6
        start_position = 37
        value_definition = {}

    class HmiSeatClimaTmrHmiSeatVentnFirstRiTmr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 15
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "一排右通风时间"
        signal_length = 6
        start_position = 45
        value_definition = {}

    class HmiSeatClimaTmrHmiSeatVentnSecLeTmr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 15
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "二排左通风时间"
        signal_length = 6
        start_position = 53
        value_definition = {}

    class HmiSeatClimaTmrHmiSeatVentnSecRiTmr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 15
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "二排右通风时间"
        signal_length = 6
        start_position = 61
        value_definition = {}

    class HmiSeatClimaTmrIdPen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "座椅通风加热个性化IDPen"
        signal_length = 4
        start_position = 67
        value_definition = {}


class BGMIntEthPDU5953:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5953
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmSeatDrvHeatClimaLvlSP:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "远程座椅加热设置-主驾驶"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'TelmSeatClimaLvl_off', '0x1': 'TelmSeatClimaLvl_Lvl1', '0x2': 'TelmSeatClimaLvl_Lvl2', '0x3': 'TelmSeatClimaLvl_Lvl3'}


class BGMIntEthPDU5954:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5954
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmSeatPassHeatClimaLvlSP:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "远程座椅加热设置-副驾驶"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'TelmSeatClimaLvl_off', '0x1': 'TelmSeatClimaLvl_Lvl1', '0x2': 'TelmSeatClimaLvl_Lvl2', '0x3': 'TelmSeatClimaLvl_Lvl3'}


class BGMIntEthPDU5955:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5955
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmSeatSecLeHeatClimaLvl:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程第二排左侧座椅加热等级"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'TelmSeatClimaLvl_off', '0x1': 'TelmSeatClimaLvl_Lvl1', '0x2': 'TelmSeatClimaLvl_Lvl2', '0x3': 'TelmSeatClimaLvl_Lvl3'}


class BGMIntEthPDU5956:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5956
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmSeatSecRiHeatClimaLvl:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程第二排右侧座椅加热等级"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'TelmSeatClimaLvl_off', '0x1': 'TelmSeatClimaLvl_Lvl1', '0x2': 'TelmSeatClimaLvl_Lvl2', '0x3': 'TelmSeatClimaLvl_Lvl3'}


class BGMIntEthPDU5957:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5957
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmSeatSecLeVentnClimaLvl:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程第二排左侧座椅通风等级"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'TelmSeatClimaLvl_off', '0x1': 'TelmSeatClimaLvl_Lvl1', '0x2': 'TelmSeatClimaLvl_Lvl2', '0x3': 'TelmSeatClimaLvl_Lvl3'}


class BGMIntEthPDU5958:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 5958
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmSeatSecRiVentnClimaLvl:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程第二排右侧座椅通风等级"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'TelmSeatClimaLvl_off', '0x1': 'TelmSeatClimaLvl_Lvl1', '0x2': 'TelmSeatClimaLvl_Lvl2', '0x3': 'TelmSeatClimaLvl_Lvl3'}


class BGMIntEthPDU6001:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6001
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SteerAdjSwtBackSts:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘位置后调节"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}

    class SteerAdjSwtFwdSts:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘位置前调节"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU6002:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6002
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SteerAdjSwtUpSts:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘位置上调节"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}

    class SteerAdjSwtDwnSts:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘位置下调节"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU6051:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6051
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class GlvBoxOpenReqFromUI:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "手套箱开关控制"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'PsdNotPsd_NotPsd', '0x1': 'PsdNotPsd_Psd'}


class BGMIntEthPDU6052:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6052
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class LockgPrsnlReqFromHmi:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "手套箱隐私锁设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU6151:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6151
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SteerWhlHeatgOnReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘加热控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'SteerWhlHeatgOnCmdTyp_Off', '0x1': 'SteerWhlHeatgOnCmdTyp_Lo', '0x2': 'SteerWhlHeatgOnCmdTyp_Med', '0x3': 'SteerWhlHeatgOnCmdTyp_Hi'}


class BGMIntEthPDU6152:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6152
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SteerWhlHeatngAutStrtReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘加热自动开启设置"
        signal_length = 1
        start_position = 0
        value_definition = {}


class BGMIntEthPDU6154:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6154
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmSteerWhlHeatgReqLvl:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "设置方向盘远程加热状态"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'TelmSeatClimaLvl_off', '0x1': 'TelmSeatClimaLvl_Lvl1', '0x2': 'TelmSeatClimaLvl_Lvl2', '0x3': 'TelmSeatClimaLvl_Lvl3'}


class BGMIntEthPDU6155:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6155
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmPM25Req:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "查询PM2.5"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'ReqSts1_NotReqd', '0x1': 'ReqSts1_Reqd'}


class BGMIntEthPDU6156:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6156
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmSeatDrvVentnClimaLvl:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程前排座椅通风主驾驶"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'TelmSeatClimaLvl_off', '0x1': 'TelmSeatClimaLvl_Lvl1', '0x2': 'TelmSeatClimaLvl_Lvl2', '0x3': 'TelmSeatClimaLvl_Lvl3'}


class BGMIntEthPDU6157:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6157
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmSeatPassVentnClimaLvl:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程前排座椅通风副驾驶"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'TelmSeatClimaLvl_off', '0x1': 'TelmSeatClimaLvl_Lvl1', '0x2': 'TelmSeatClimaLvl_Lvl2', '0x3': 'TelmSeatClimaLvl_Lvl3'}


class BGMIntEthPDU6158:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6158
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ReqFragLvlTelm:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程香氛等级设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ReqFragLvl_OFF', '0x1': 'ReqFragLvl_Level1', '0x2': 'ReqFragLvl_Level2', '0x3': 'ReqFragLvl_Level3'}


class BGMIntEthPDU6159:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6159
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class RemVentReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程通风设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU6160:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6160
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmDefrostReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程除雾设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU6161:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6161
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class LocalHvBattThermReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "本地高压电池加热请求"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'CmptSts_NoRequest', '0x1': 'CmptSts_CoolingRequest', '0x2': 'CmptSts_HeatingRequest', '0x3': 'CmptSts_CoolingAndHeatingRequest', '0x4': 'CmptSts_PostHeating'}

    class LocalHvBattThermTarT:
        comments = "底层软件需配置信号路由；"
        factor = 0.5
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = -40
        signal_description = "本地高压电池加热目标温度"
        signal_length = 8
        start_position = 15
        value_definition = {}


class BGMIntEthPDU6163:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6163
    pdu_length_bytes = 48
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'PosnBrief': ['PosnBriefPosnLgt', 'PosnBriefPosnLat'], 'PosnFromSatlt': ['PosnFromSatltPosnLgt', 'PosnFromSatltPosnLat', 'PosnFromSatltUTCForDay', 'PosnFromSatltUTCForMth', 'PosnFromSatltCntr', 'PosnFromSatltPosnAlti', 'PosnFromSatltPosnDir', 'PosnFromSatltPosnSpd', 'PosnFromSatltPosnVHozl', 'PosnFromSatltPosnVVert', 'PosnFromSatltTiForMins', 'PosnFromSatltTiForMsec', 'PosnFromSatltTiForSec', 'PosnFromSatltUTCForHr', 'PosnFromSatltUTCForMins', 'PosnFromSatltUTCForSec', 'PosnFromSatltUTCForYr'], 'UTCTiFromEth': ['UTCTiFromEthMth1', 'UTCTiFromEthDay', 'UTCTiFromEthYr1', 'UTCTiFromEthHr1', 'UTCTiFromEthMins1', 'UTCTiFromEthSec1', 'UTCTiFromEthDataValid']}

    class PosnBriefPosnLgt:
        comments = "底层软件需配置信号路由；"
        factor = 2.7777777777777776e-07
        initial_value = 180
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "海拔经度"
        signal_length = 31
        start_position = 38
        value_definition = {}

    class PosnFromSatltPosnLgt:
        comments = "底层软件需配置信号路由；"
        factor = 2.7777777777777776e-07
        initial_value = 180
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "海拔经度"
        signal_length = 31
        start_position = 142
        value_definition = {}

    class PosnBriefPosnLat:
        comments = "底层软件需配置信号路由；"
        factor = 2.77777777777778e-07
        initial_value = 90
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "海拔纬度"
        signal_length = 30
        start_position = 5
        value_definition = {}

    class PosnFromSatltPosnLat:
        comments = "底层软件需配置信号路由；"
        factor = 2.77777777777778e-07
        initial_value = 90
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "海拔纬度"
        signal_length = 30
        start_position = 109
        value_definition = {}

    class PosnFromSatltUTCForDay:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC天"
        signal_length = 5
        start_position = 276
        value_definition = {}

    class PosnFromSatltUTCForMth:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC月"
        signal_length = 4
        start_position = 299
        value_definition = {}

    class UTCTiFromEthMth1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC月"
        signal_length = 4
        start_position = 331
        value_definition = {}

    class UTCTiFromEthDay:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC日"
        signal_length = 5
        start_position = 340
        value_definition = {}

    class GpsStatus:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "GPS状态"
        signal_length = 1
        start_position = 376
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class PosnFromSatltCntr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "rollingCounter"
        signal_length = 3
        start_position = 66
        value_definition = {}

    class PosnFromSatltPosnAlti:
        comments = "底层软件需配置信号路由；"
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = -100
        signal_description = "海拔高度"
        signal_length = 16
        start_position = 79
        value_definition = {}

    class PosnFromSatltPosnDir:
        comments = "底层软件需配置信号路由；"
        factor = 0.01
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向"
        signal_length = 16
        start_position = 95
        value_definition = {}

    class PosnFromSatltPosnSpd:
        comments = "底层软件需配置信号路由；"
        factor = 0.001
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "速度"
        signal_length = 17
        start_position = 168
        value_definition = {}

    class PosnFromSatltPosnVHozl:
        comments = "底层软件需配置信号路由；"
        factor = 0.001
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "水平速度"
        signal_length = 17
        start_position = 192
        value_definition = {}

    class PosnFromSatltPosnVVert:
        comments = "底层软件需配置信号路由；"
        factor = 0.001
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "垂直速度"
        signal_length = 18
        start_position = 217
        value_definition = {}

    class PosnFromSatltTiForMins:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "分钟"
        signal_length = 6
        start_position = 245
        value_definition = {}

    class PosnFromSatltTiForMsec:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "毫秒"
        signal_length = 10
        start_position = 249
        value_definition = {}

    class PosnFromSatltTiForSec:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "秒"
        signal_length = 6
        start_position = 269
        value_definition = {}

    class PosnFromSatltUTCForHr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC小时"
        signal_length = 5
        start_position = 284
        value_definition = {}

    class PosnFromSatltUTCForMins:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC分钟"
        signal_length = 6
        start_position = 293
        value_definition = {}

    class PosnFromSatltUTCForSec:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC秒"
        signal_length = 6
        start_position = 309
        value_definition = {}

    class PosnFromSatltUTCForYr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC年"
        signal_length = 7
        start_position = 318
        value_definition = {}

    class UTCTiFromEthYr1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC年"
        signal_length = 7
        start_position = 326
        value_definition = {}

    class UTCTiFromEthHr1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC时"
        signal_length = 5
        start_position = 348
        value_definition = {}

    class UTCTiFromEthMins1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC分"
        signal_length = 6
        start_position = 357
        value_definition = {}

    class UTCTiFromEthSec1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "UTC秒"
        signal_length = 6
        start_position = 365
        value_definition = {}

    class UTCTiFromEthDataValid:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "DataValid"
        signal_length = 1
        start_position = 368
        value_definition = {}


class BGMIntEthPDU6201:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6201
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'SteerWhlSymbolLightCtrlLe': ['SteerWhlSymbolLightCtrlLeBrightness', 'SteerWhlSymbolLightCtrlLeRed', 'SteerWhlSymbolLightCtrlLeGreen', 'SteerWhlSymbolLightCtrlLeBlue']}

    class SteerWhlSymbolLightCtrlLeBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘灯带左Symbol亮度"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class SteerWhlSymbolLightCtrlLeRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘灯带左SymbolRed调节"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class SteerWhlSymbolLightCtrlLeGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘灯带左SymbolGreen调节"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class SteerWhlSymbolLightCtrlLeBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘灯带左SymbolBlue调节"
        signal_length = 8
        start_position = 31
        value_definition = {}


class BGMIntEthPDU6202:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6202
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'SteerWhlSymbolLightCtrlRi': ['SteerWhlSymbolLightCtrlRiBrightness', 'SteerWhlSymbolLightCtrlRiRed', 'SteerWhlSymbolLightCtrlRiGreen', 'SteerWhlSymbolLightCtrlRiBlue']}

    class SteerWhlSymbolLightCtrlRiBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘灯带右Symbol亮度"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class SteerWhlSymbolLightCtrlRiRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘灯带右SymbolRed调节"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class SteerWhlSymbolLightCtrlRiGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘灯带右SymbolGreen调节"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class SteerWhlSymbolLightCtrlRiBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘灯带右SymbolBlue调节"
        signal_length = 8
        start_position = 31
        value_definition = {}


class BGMIntEthPDU6203:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6203
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'SteerWhlLightingBarCtrl': ['SteerWhlLightingBarCtrlBrightness', 'SteerWhlLightingBarCtrlRed', 'SteerWhlLightingBarCtrlGreen', 'SteerWhlLightingBarCtrlBlue']}

    class SteerWhlLightingBarCtrlBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘Lighting Bar亮度"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class SteerWhlLightingBarCtrlRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘Lighting Bar Red调节"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class SteerWhlLightingBarCtrlGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘Lighting Bar Green调节"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class SteerWhlLightingBarCtrlBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "方向盘Lighting Bar Blue调节"
        signal_length = 8
        start_position = 31
        value_definition = {}


class BGMIntEthPDU6251:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6251
    pdu_length_bytes = 864
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'SmartAmbientLightIpRight0': ['SmartAmbientLightIpRight0Brightness', 'SmartAmbientLightIpRight0Red', 'SmartAmbientLightIpRight0Green', 'SmartAmbientLightIpRight0Blue'], 'SmartAmbientLightIpRight1': ['SmartAmbientLightIpRight1Brightness', 'SmartAmbientLightIpRight1Red', 'SmartAmbientLightIpRight1Green', 'SmartAmbientLightIpRight1Blue'], 'SmartAmbientLightIpRight2': ['SmartAmbientLightIpRight2Brightness', 'SmartAmbientLightIpRight2Red', 'SmartAmbientLightIpRight2Green', 'SmartAmbientLightIpRight2Blue'], 'SmartAmbientLightIpRight3': ['SmartAmbientLightIpRight3Brightness', 'SmartAmbientLightIpRight3Red', 'SmartAmbientLightIpRight3Green', 'SmartAmbientLightIpRight3Blue'], 'SmartAmbientLightIpRight4': ['SmartAmbientLightIpRight4Brightness', 'SmartAmbientLightIpRight4Red', 'SmartAmbientLightIpRight4Green', 'SmartAmbientLightIpRight4Blue'], 'SmartAmbientLightIpRight5': ['SmartAmbientLightIpRight5Brightness', 'SmartAmbientLightIpRight5Red', 'SmartAmbientLightIpRight5Green', 'SmartAmbientLightIpRight5Blue'], 'SmartAmbientLightIpRight6': ['SmartAmbientLightIpRight6Brightness', 'SmartAmbientLightIpRight6Red', 'SmartAmbientLightIpRight6Green', 'SmartAmbientLightIpRight6Blue'], 'SmartAmbientLightIpRight7': ['SmartAmbientLightIpRight7Brightness', 'SmartAmbientLightIpRight7Red', 'SmartAmbientLightIpRight7Green', 'SmartAmbientLightIpRight7Blue'], 'SmartAmbientLightIpRight8': ['SmartAmbientLightIpRight8Brightness', 'SmartAmbientLightIpRight8Red', 'SmartAmbientLightIpRight8Green', 'SmartAmbientLightIpRight8Blue'], 'SmartAmbientLightIpRight9': ['SmartAmbientLightIpRight9Brightness', 'SmartAmbientLightIpRight9Red', 'SmartAmbientLightIpRight9Green', 'SmartAmbientLightIpRight9Blue'], 'SmartAmbientLightIpRight10': ['SmartAmbientLightIpRight10Brightness', 'SmartAmbientLightIpRight10Red', 'SmartAmbientLightIpRight10Green', 'SmartAmbientLightIpRight10Blue'], 'SmartAmbientLightIpRight11': ['SmartAmbientLightIpRight11Brightness', 'SmartAmbientLightIpRight11Red', 'SmartAmbientLightIpRight11Green', 'SmartAmbientLightIpRight11Blue'], 'SmartAmbientLightIpRight12': ['SmartAmbientLightIpRight12Brightness', 'SmartAmbientLightIpRight12Red', 'SmartAmbientLightIpRight12Green', 'SmartAmbientLightIpRight12Blue'], 'SmartAmbientLightIpRight13': ['SmartAmbientLightIpRight13Brightness', 'SmartAmbientLightIpRight13Red', 'SmartAmbientLightIpRight13Green', 'SmartAmbientLightIpRight13Blue'], 'SmartAmbientLightIpRight14': ['SmartAmbientLightIpRight14Brightness', 'SmartAmbientLightIpRight14Red', 'SmartAmbientLightIpRight14Green', 'SmartAmbientLightIpRight14Blue'], 'SmartAmbientLightIpRight15': ['SmartAmbientLightIpRight15Brightness', 'SmartAmbientLightIpRight15Red', 'SmartAmbientLightIpRight15Green', 'SmartAmbientLightIpRight15Blue'], 'SmartAmbientLightIpRight16': ['SmartAmbientLightIpRight16Brightness', 'SmartAmbientLightIpRight16Red', 'SmartAmbientLightIpRight16Green', 'SmartAmbientLightIpRight16Blue'], 'SmartAmbientLightIpRight17': ['SmartAmbientLightIpRight17Brightness', 'SmartAmbientLightIpRight17Red', 'SmartAmbientLightIpRight17Green', 'SmartAmbientLightIpRight17Blue'], 'SmartAmbientLightIpRight18': ['SmartAmbientLightIpRight18Brightness', 'SmartAmbientLightIpRight18Red', 'SmartAmbientLightIpRight18Green', 'SmartAmbientLightIpRight18Blue'], 'SmartAmbientLightIpRight19': ['SmartAmbientLightIpRight19Brightness', 'SmartAmbientLightIpRight19Red', 'SmartAmbientLightIpRight19Green', 'SmartAmbientLightIpRight19Blue'], 'SmartAmbientLightIpRight20': ['SmartAmbientLightIpRight20Brightness', 'SmartAmbientLightIpRight20Red', 'SmartAmbientLightIpRight20Green', 'SmartAmbientLightIpRight20Blue'], 'SmartAmbientLightIpRight21': ['SmartAmbientLightIpRight21Brightness', 'SmartAmbientLightIpRight21Red', 'SmartAmbientLightIpRight21Green', 'SmartAmbientLightIpRight21Blue'], 'SmartAmbientLightIpRight22': ['SmartAmbientLightIpRight22Brightness', 'SmartAmbientLightIpRight22Red', 'SmartAmbientLightIpRight22Green', 'SmartAmbientLightIpRight22Blue'], 'SmartAmbientLightIpRight23': ['SmartAmbientLightIpRight23Brightness', 'SmartAmbientLightIpRight23Red', 'SmartAmbientLightIpRight23Green', 'SmartAmbientLightIpRight23Blue'], 'SmartAmbientLightIpRight24': ['SmartAmbientLightIpRight24Brightness', 'SmartAmbientLightIpRight24Red', 'SmartAmbientLightIpRight24Green', 'SmartAmbientLightIpRight24Blue'], 'SmartAmbientLightIpRight25': ['SmartAmbientLightIpRight25Brightness', 'SmartAmbientLightIpRight25Red', 'SmartAmbientLightIpRight25Green', 'SmartAmbientLightIpRight25Blue'], 'SmartAmbientLightIpRight26': ['SmartAmbientLightIpRight26Brightness', 'SmartAmbientLightIpRight26Red', 'SmartAmbientLightIpRight26Green', 'SmartAmbientLightIpRight26Blue'], 'SmartAmbientLightIpRight27': ['SmartAmbientLightIpRight27Brightness', 'SmartAmbientLightIpRight27Red', 'SmartAmbientLightIpRight27Green', 'SmartAmbientLightIpRight27Blue'], 'SmartAmbientLightIpRight28': ['SmartAmbientLightIpRight28Brightness', 'SmartAmbientLightIpRight28Red', 'SmartAmbientLightIpRight28Green', 'SmartAmbientLightIpRight28Blue'], 'SmartAmbientLightIpRight29': ['SmartAmbientLightIpRight29Brightness', 'SmartAmbientLightIpRight29Red', 'SmartAmbientLightIpRight29Green', 'SmartAmbientLightIpRight29Blue'], 'SmartAmbientLightIpRight30': ['SmartAmbientLightIpRight30Brightness', 'SmartAmbientLightIpRight30Red', 'SmartAmbientLightIpRight30Green', 'SmartAmbientLightIpRight30Blue'], 'SmartAmbientLightIpRight31': ['SmartAmbientLightIpRight31Brightness', 'SmartAmbientLightIpRight31Red', 'SmartAmbientLightIpRight31Green', 'SmartAmbientLightIpRight31Blue'], 'SmartAmbientLightIpRight32': ['SmartAmbientLightIpRight32Brightness', 'SmartAmbientLightIpRight32Red', 'SmartAmbientLightIpRight32Green', 'SmartAmbientLightIpRight32Blue'], 'SmartAmbientLightIpRight33': ['SmartAmbientLightIpRight33Brightness', 'SmartAmbientLightIpRight33Red', 'SmartAmbientLightIpRight33Green', 'SmartAmbientLightIpRight33Blue'], 'SmartAmbientLightIpRight34': ['SmartAmbientLightIpRight34Brightness', 'SmartAmbientLightIpRight34Red', 'SmartAmbientLightIpRight34Green', 'SmartAmbientLightIpRight34Blue'], 'SmartAmbientLightIpRight35': ['SmartAmbientLightIpRight35Brightness', 'SmartAmbientLightIpRight35Red', 'SmartAmbientLightIpRight35Green', 'SmartAmbientLightIpRight35Blue'], 'SmartAmbientLightIpRight36': ['SmartAmbientLightIpRight36Brightness', 'SmartAmbientLightIpRight36Red', 'SmartAmbientLightIpRight36Green', 'SmartAmbientLightIpRight36Blue'], 'SmartAmbientLightIpRight37': ['SmartAmbientLightIpRight37Brightness', 'SmartAmbientLightIpRight37Red', 'SmartAmbientLightIpRight37Green', 'SmartAmbientLightIpRight37Blue'], 'SmartAmbientLightIpRight38': ['SmartAmbientLightIpRight38Brightness', 'SmartAmbientLightIpRight38Red', 'SmartAmbientLightIpRight38Green', 'SmartAmbientLightIpRight38Blue'], 'SmartAmbientLightIpRight39': ['SmartAmbientLightIpRight39Brightness', 'SmartAmbientLightIpRight39Red', 'SmartAmbientLightIpRight39Green', 'SmartAmbientLightIpRight39Blue'], 'SmartAmbientLightIpRight40': ['SmartAmbientLightIpRight40Brightness', 'SmartAmbientLightIpRight40Red', 'SmartAmbientLightIpRight40Green', 'SmartAmbientLightIpRight40Blue'], 'SmartAmbientLightIpRight41': ['SmartAmbientLightIpRight41Brightness', 'SmartAmbientLightIpRight41Red', 'SmartAmbientLightIpRight41Green', 'SmartAmbientLightIpRight41Blue'], 'SmartAmbientLightIpRight42': ['SmartAmbientLightIpRight42Brightness', 'SmartAmbientLightIpRight42Red', 'SmartAmbientLightIpRight42Green', 'SmartAmbientLightIpRight42Blue'], 'SmartAmbientLightIpRight43': ['SmartAmbientLightIpRight43Brightness', 'SmartAmbientLightIpRight43Red', 'SmartAmbientLightIpRight43Green', 'SmartAmbientLightIpRight43Blue'], 'SmartAmbientLightIpRight44': ['SmartAmbientLightIpRight44Brightness', 'SmartAmbientLightIpRight44Red', 'SmartAmbientLightIpRight44Green', 'SmartAmbientLightIpRight44Blue'], 'SmartAmbientLightIpRight45': ['SmartAmbientLightIpRight45Brightness', 'SmartAmbientLightIpRight45Red', 'SmartAmbientLightIpRight45Green', 'SmartAmbientLightIpRight45Blue'], 'SmartAmbientLightIpRight46': ['SmartAmbientLightIpRight46Brightness', 'SmartAmbientLightIpRight46Red', 'SmartAmbientLightIpRight46Green', 'SmartAmbientLightIpRight46Blue'], 'SmartAmbientLightIpRight47': ['SmartAmbientLightIpRight47Brightness', 'SmartAmbientLightIpRight47Red', 'SmartAmbientLightIpRight47Green', 'SmartAmbientLightIpRight47Blue'], 'SmartAmbientLightIpLeft0': ['SmartAmbientLightIpLeft0Brightness', 'SmartAmbientLightIpLeft0Red', 'SmartAmbientLightIpLeft0Green', 'SmartAmbientLightIpLeft0Blue'], 'SmartAmbientLightIpLeft1': ['SmartAmbientLightIpLeft1Brightness', 'SmartAmbientLightIpLeft1Red', 'SmartAmbientLightIpLeft1Green', 'SmartAmbientLightIpLeft1Blue'], 'SmartAmbientLightIpLeft2': ['SmartAmbientLightIpLeft2Brightness', 'SmartAmbientLightIpLeft2Red', 'SmartAmbientLightIpLeft2Green', 'SmartAmbientLightIpLeft2Blue'], 'SmartAmbientLightIpLeft3': ['SmartAmbientLightIpLeft3Brightness', 'SmartAmbientLightIpLeft3Red', 'SmartAmbientLightIpLeft3Green', 'SmartAmbientLightIpLeft3Blue'], 'SmartAmbientLightIpLeft4': ['SmartAmbientLightIpLeft4Brightness', 'SmartAmbientLightIpLeft4Red', 'SmartAmbientLightIpLeft4Green', 'SmartAmbientLightIpLeft4Blue'], 'SmartAmbientLightIpLeft5': ['SmartAmbientLightIpLeft5Brightness', 'SmartAmbientLightIpLeft5Red', 'SmartAmbientLightIpLeft5Green', 'SmartAmbientLightIpLeft5Blue'], 'SmartAmbientLightIpLeft6': ['SmartAmbientLightIpLeft6Brightness', 'SmartAmbientLightIpLeft6Red', 'SmartAmbientLightIpLeft6Green', 'SmartAmbientLightIpLeft6Blue'], 'SmartAmbientLightIpLeft7': ['SmartAmbientLightIpLeft7Brightness', 'SmartAmbientLightIpLeft7Red', 'SmartAmbientLightIpLeft7Green', 'SmartAmbientLightIpLeft7Blue'], 'SmartAmbientLightIpLeft8': ['SmartAmbientLightIpLeft8Brightness', 'SmartAmbientLightIpLeft8Red', 'SmartAmbientLightIpLeft8Green', 'SmartAmbientLightIpLeft8Blue'], 'SmartAmbientLightIpLeft9': ['SmartAmbientLightIpLeft9Brightness', 'SmartAmbientLightIpLeft9Red', 'SmartAmbientLightIpLeft9Green', 'SmartAmbientLightIpLeft9Blue'], 'SmartAmbientLightIpLeft10': ['SmartAmbientLightIpLeft10Brightness', 'SmartAmbientLightIpLeft10Red', 'SmartAmbientLightIpLeft10Green', 'SmartAmbientLightIpLeft10Blue'], 'SmartAmbientLightIpLeft11': ['SmartAmbientLightIpLeft11Brightness', 'SmartAmbientLightIpLeft11Red', 'SmartAmbientLightIpLeft11Green', 'SmartAmbientLightIpLeft11Blue'], 'SmartAmbientLightIpLeft12': ['SmartAmbientLightIpLeft12Brightness', 'SmartAmbientLightIpLeft12Red', 'SmartAmbientLightIpLeft12Green', 'SmartAmbientLightIpLeft12Blue'], 'SmartAmbientLightIpLeft13': ['SmartAmbientLightIpLeft13Brightness', 'SmartAmbientLightIpLeft13Red', 'SmartAmbientLightIpLeft13Green', 'SmartAmbientLightIpLeft13Blue'], 'SmartAmbientLightIpLeft14': ['SmartAmbientLightIpLeft14Brightness', 'SmartAmbientLightIpLeft14Red', 'SmartAmbientLightIpLeft14Green', 'SmartAmbientLightIpLeft14Blue'], 'SmartAmbientLightIpLeft15': ['SmartAmbientLightIpLeft15Brightness', 'SmartAmbientLightIpLeft15Red', 'SmartAmbientLightIpLeft15Green', 'SmartAmbientLightIpLeft15Blue'], 'SmartAmbientLightIpLeft16': ['SmartAmbientLightIpLeft16Brightness', 'SmartAmbientLightIpLeft16Red', 'SmartAmbientLightIpLeft16Green', 'SmartAmbientLightIpLeft16Blue'], 'SmartAmbientLightIpLeft17': ['SmartAmbientLightIpLeft17Brightness', 'SmartAmbientLightIpLeft17Red', 'SmartAmbientLightIpLeft17Green', 'SmartAmbientLightIpLeft17Blue'], 'SmartAmbientLightIpLeft18': ['SmartAmbientLightIpLeft18Brightness', 'SmartAmbientLightIpLeft18Red', 'SmartAmbientLightIpLeft18Green', 'SmartAmbientLightIpLeft18Blue'], 'SmartAmbientLightIpLeft19': ['SmartAmbientLightIpLeft19Brightness', 'SmartAmbientLightIpLeft19Red', 'SmartAmbientLightIpLeft19Green', 'SmartAmbientLightIpLeft19Blue'], 'SmartAmbientLightIpLeft20': ['SmartAmbientLightIpLeft20Brightness', 'SmartAmbientLightIpLeft20Red', 'SmartAmbientLightIpLeft20Green', 'SmartAmbientLightIpLeft20Blue'], 'SmartAmbientLightIpLeft21': ['SmartAmbientLightIpLeft21Brightness', 'SmartAmbientLightIpLeft21Red', 'SmartAmbientLightIpLeft21Green', 'SmartAmbientLightIpLeft21Blue'], 'SmartAmbientLightIpLeft22': ['SmartAmbientLightIpLeft22Brightness', 'SmartAmbientLightIpLeft22Red', 'SmartAmbientLightIpLeft22Green', 'SmartAmbientLightIpLeft22Blue'], 'SmartAmbientLightIpLeft23': ['SmartAmbientLightIpLeft23Brightness', 'SmartAmbientLightIpLeft23Red', 'SmartAmbientLightIpLeft23Green', 'SmartAmbientLightIpLeft23Blue'], 'SmartAmbientLightIpLeft24': ['SmartAmbientLightIpLeft24Brightness', 'SmartAmbientLightIpLeft24Red', 'SmartAmbientLightIpLeft24Green', 'SmartAmbientLightIpLeft24Blue'], 'SmartAmbientLightIpLeft25': ['SmartAmbientLightIpLeft25Brightness', 'SmartAmbientLightIpLeft25Red', 'SmartAmbientLightIpLeft25Green', 'SmartAmbientLightIpLeft25Blue'], 'SmartAmbientLightIpLeft26': ['SmartAmbientLightIpLeft26Brightness', 'SmartAmbientLightIpLeft26Red', 'SmartAmbientLightIpLeft26Green', 'SmartAmbientLightIpLeft26Blue'], 'SmartAmbientLightIpLeft27': ['SmartAmbientLightIpLeft27Brightness', 'SmartAmbientLightIpLeft27Red', 'SmartAmbientLightIpLeft27Green', 'SmartAmbientLightIpLeft27Blue'], 'SmartAmbientLightIpLeft28': ['SmartAmbientLightIpLeft28Brightness', 'SmartAmbientLightIpLeft28Red', 'SmartAmbientLightIpLeft28Green', 'SmartAmbientLightIpLeft28Blue'], 'SmartAmbientLightIpLeft29': ['SmartAmbientLightIpLeft29Brightness', 'SmartAmbientLightIpLeft29Red', 'SmartAmbientLightIpLeft29Green', 'SmartAmbientLightIpLeft29Blue'], 'SmartAmbientLightIpLeft30': ['SmartAmbientLightIpLeft30Brightness', 'SmartAmbientLightIpLeft30Red', 'SmartAmbientLightIpLeft30Green', 'SmartAmbientLightIpLeft30Blue'], 'SmartAmbientLightIpLeft31': ['SmartAmbientLightIpLeft31Brightness', 'SmartAmbientLightIpLeft31Red', 'SmartAmbientLightIpLeft31Green', 'SmartAmbientLightIpLeft31Blue'], 'SmartAmbientLightIpLeft32': ['SmartAmbientLightIpLeft32Brightness', 'SmartAmbientLightIpLeft32Red', 'SmartAmbientLightIpLeft32Green', 'SmartAmbientLightIpLeft32Blue'], 'SmartAmbientLightIpLeft33': ['SmartAmbientLightIpLeft33Brightness', 'SmartAmbientLightIpLeft33Red', 'SmartAmbientLightIpLeft33Green', 'SmartAmbientLightIpLeft33Blue'], 'SmartAmbientLightIpLeft34': ['SmartAmbientLightIpLeft34Brightness', 'SmartAmbientLightIpLeft34Red', 'SmartAmbientLightIpLeft34Green', 'SmartAmbientLightIpLeft34Blue'], 'SmartAmbientLightIpLeft35': ['SmartAmbientLightIpLeft35Brightness', 'SmartAmbientLightIpLeft35Red', 'SmartAmbientLightIpLeft35Green', 'SmartAmbientLightIpLeft35Blue'], 'SmartAmbientLightFrontRight0': ['SmartAmbientLightFrontRight0Brightness', 'SmartAmbientLightFrontRight0Red', 'SmartAmbientLightFrontRight0Green', 'SmartAmbientLightFrontRight0Blue'], 'SmartAmbientLightFrontRight1': ['SmartAmbientLightFrontRight1Brightness', 'SmartAmbientLightFrontRight1Red', 'SmartAmbientLightFrontRight1Green', 'SmartAmbientLightFrontRight1Blue'], 'SmartAmbientLightFrontRight2': ['SmartAmbientLightFrontRight2Brightness', 'SmartAmbientLightFrontRight2Red', 'SmartAmbientLightFrontRight2Green', 'SmartAmbientLightFrontRight2Blue'], 'SmartAmbientLightFrontRight3': ['SmartAmbientLightFrontRight3Brightness', 'SmartAmbientLightFrontRight3Red', 'SmartAmbientLightFrontRight3Green', 'SmartAmbientLightFrontRight3Blue'], 'SmartAmbientLightFrontRight4': ['SmartAmbientLightFrontRight4Brightness', 'SmartAmbientLightFrontRight4Red', 'SmartAmbientLightFrontRight4Green', 'SmartAmbientLightFrontRight4Blue'], 'SmartAmbientLightFrontRight5': ['SmartAmbientLightFrontRight5Brightness', 'SmartAmbientLightFrontRight5Red', 'SmartAmbientLightFrontRight5Green', 'SmartAmbientLightFrontRight5Blue'], 'SmartAmbientLightFrontRight6': ['SmartAmbientLightFrontRight6Brightness', 'SmartAmbientLightFrontRight6Red', 'SmartAmbientLightFrontRight6Green', 'SmartAmbientLightFrontRight6Blue'], 'SmartAmbientLightFrontRight7': ['SmartAmbientLightFrontRight7Brightness', 'SmartAmbientLightFrontRight7Red', 'SmartAmbientLightFrontRight7Green', 'SmartAmbientLightFrontRight7Blue'], 'SmartAmbientLightFrontRight8': ['SmartAmbientLightFrontRight8Brightness', 'SmartAmbientLightFrontRight8Red', 'SmartAmbientLightFrontRight8Green', 'SmartAmbientLightFrontRight8Blue'], 'SmartAmbientLightFrontRight9': ['SmartAmbientLightFrontRight9Brightness', 'SmartAmbientLightFrontRight9Red', 'SmartAmbientLightFrontRight9Green', 'SmartAmbientLightFrontRight9Blue'], 'SmartAmbientLightFrontRight10': ['SmartAmbientLightFrontRight10Brightness', 'SmartAmbientLightFrontRight10Red', 'SmartAmbientLightFrontRight10Green', 'SmartAmbientLightFrontRight10Blue'], 'SmartAmbientLightFrontRight11': ['SmartAmbientLightFrontRight11Brightness', 'SmartAmbientLightFrontRight11Red', 'SmartAmbientLightFrontRight11Green', 'SmartAmbientLightFrontRight11Blue'], 'SmartAmbientLightFrontRight12': ['SmartAmbientLightFrontRight12Brightness', 'SmartAmbientLightFrontRight12Red', 'SmartAmbientLightFrontRight12Green', 'SmartAmbientLightFrontRight12Blue'], 'SmartAmbientLightFrontRight13': ['SmartAmbientLightFrontRight13Brightness', 'SmartAmbientLightFrontRight13Red', 'SmartAmbientLightFrontRight13Green', 'SmartAmbientLightFrontRight13Blue'], 'SmartAmbientLightFrontRight14': ['SmartAmbientLightFrontRight14Brightness', 'SmartAmbientLightFrontRight14Red', 'SmartAmbientLightFrontRight14Green', 'SmartAmbientLightFrontRight14Blue'], 'SmartAmbientLightFrontRight15': ['SmartAmbientLightFrontRight15Brightness', 'SmartAmbientLightFrontRight15Red', 'SmartAmbientLightFrontRight15Green', 'SmartAmbientLightFrontRight15Blue'], 'SmartAmbientLightFrontRight16': ['SmartAmbientLightFrontRight16Brightness', 'SmartAmbientLightFrontRight16Red', 'SmartAmbientLightFrontRight16Green', 'SmartAmbientLightFrontRight16Blue'], 'SmartAmbientLightFrontRight17': ['SmartAmbientLightFrontRight17Brightness', 'SmartAmbientLightFrontRight17Red', 'SmartAmbientLightFrontRight17Green', 'SmartAmbientLightFrontRight17Blue'], 'SmartAmbientLightFrontRight18': ['SmartAmbientLightFrontRight18Brightness', 'SmartAmbientLightFrontRight18Red', 'SmartAmbientLightFrontRight18Green', 'SmartAmbientLightFrontRight18Blue'], 'SmartAmbientLightFrontRight19': ['SmartAmbientLightFrontRight19Brightness', 'SmartAmbientLightFrontRight19Red', 'SmartAmbientLightFrontRight19Green', 'SmartAmbientLightFrontRight19Blue'], 'SmartAmbientLightFrontRight20': ['SmartAmbientLightFrontRight20Brightness', 'SmartAmbientLightFrontRight20Red', 'SmartAmbientLightFrontRight20Green', 'SmartAmbientLightFrontRight20Blue'], 'SmartAmbientLightFrontRight21': ['SmartAmbientLightFrontRight21Brightness', 'SmartAmbientLightFrontRight21Red', 'SmartAmbientLightFrontRight21Green', 'SmartAmbientLightFrontRight21Blue'], 'SmartAmbientLightFrontRight22': ['SmartAmbientLightFrontRight22Brightness', 'SmartAmbientLightFrontRight22Red', 'SmartAmbientLightFrontRight22Green', 'SmartAmbientLightFrontRight22Blue'], 'SmartAmbientLightFrontRight23': ['SmartAmbientLightFrontRight23Brightness', 'SmartAmbientLightFrontRight23Red', 'SmartAmbientLightFrontRight23Green', 'SmartAmbientLightFrontRight23Blue'], 'SmartAmbientLightFrontRight24': ['SmartAmbientLightFrontRight24Brightness', 'SmartAmbientLightFrontRight24Red', 'SmartAmbientLightFrontRight24Green', 'SmartAmbientLightFrontRight24Blue'], 'SmartAmbientLightFrontRight25': ['SmartAmbientLightFrontRight25Brightness', 'SmartAmbientLightFrontRight25Red', 'SmartAmbientLightFrontRight25Green', 'SmartAmbientLightFrontRight25Blue'], 'SmartAmbientLightFrontRight26': ['SmartAmbientLightFrontRight26Brightness', 'SmartAmbientLightFrontRight26Red', 'SmartAmbientLightFrontRight26Green', 'SmartAmbientLightFrontRight26Blue'], 'SmartAmbientLightFrontRight27': ['SmartAmbientLightFrontRight27Brightness', 'SmartAmbientLightFrontRight27Red', 'SmartAmbientLightFrontRight27Green', 'SmartAmbientLightFrontRight27Blue'], 'SmartAmbientLightFrontRight28': ['SmartAmbientLightFrontRight28Brightness', 'SmartAmbientLightFrontRight28Red', 'SmartAmbientLightFrontRight28Green', 'SmartAmbientLightFrontRight28Blue'], 'SmartAmbientLightFrontRight29': ['SmartAmbientLightFrontRight29Brightness', 'SmartAmbientLightFrontRight29Red', 'SmartAmbientLightFrontRight29Green', 'SmartAmbientLightFrontRight29Blue'], 'SmartAmbientLightFrontRight30': ['SmartAmbientLightFrontRight30Brightness', 'SmartAmbientLightFrontRight30Red', 'SmartAmbientLightFrontRight30Green', 'SmartAmbientLightFrontRight30Blue'], 'SmartAmbientLightFrontRight31': ['SmartAmbientLightFrontRight31Brightness', 'SmartAmbientLightFrontRight31Red', 'SmartAmbientLightFrontRight31Green', 'SmartAmbientLightFrontRight31Blue'], 'SmartAmbientLightFrontRight32': ['SmartAmbientLightFrontRight32Brightness', 'SmartAmbientLightFrontRight32Red', 'SmartAmbientLightFrontRight32Green', 'SmartAmbientLightFrontRight32Blue'], 'SmartAmbientLightFrontRight33': ['SmartAmbientLightFrontRight33Brightness', 'SmartAmbientLightFrontRight33Red', 'SmartAmbientLightFrontRight33Green', 'SmartAmbientLightFrontRight33Blue'], 'SmartAmbientLightFrontRight34': ['SmartAmbientLightFrontRight34Brightness', 'SmartAmbientLightFrontRight34Red', 'SmartAmbientLightFrontRight34Green', 'SmartAmbientLightFrontRight34Blue'], 'SmartAmbientLightFrontRight35': ['SmartAmbientLightFrontRight35Brightness', 'SmartAmbientLightFrontRight35Red', 'SmartAmbientLightFrontRight35Green', 'SmartAmbientLightFrontRight35Blue'], 'SmartAmbientLightFrontLeft0': ['SmartAmbientLightFrontLeft0Brightness', 'SmartAmbientLightFrontLeft0Red', 'SmartAmbientLightFrontLeft0Green', 'SmartAmbientLightFrontLeft0Blue'], 'SmartAmbientLightFrontLeft1': ['SmartAmbientLightFrontLeft1Brightness', 'SmartAmbientLightFrontLeft1Red', 'SmartAmbientLightFrontLeft1Green', 'SmartAmbientLightFrontLeft1Blue'], 'SmartAmbientLightFrontLeft2': ['SmartAmbientLightFrontLeft2Brightness', 'SmartAmbientLightFrontLeft2Red', 'SmartAmbientLightFrontLeft2Green', 'SmartAmbientLightFrontLeft2Blue'], 'SmartAmbientLightFrontLeft3': ['SmartAmbientLightFrontLeft3Brightness', 'SmartAmbientLightFrontLeft3Red', 'SmartAmbientLightFrontLeft3Green', 'SmartAmbientLightFrontLeft3Blue'], 'SmartAmbientLightFrontLeft4': ['SmartAmbientLightFrontLeft4Brightness', 'SmartAmbientLightFrontLeft4Red', 'SmartAmbientLightFrontLeft4Green', 'SmartAmbientLightFrontLeft4Blue'], 'SmartAmbientLightFrontLeft5': ['SmartAmbientLightFrontLeft5Brightness', 'SmartAmbientLightFrontLeft5Red', 'SmartAmbientLightFrontLeft5Green', 'SmartAmbientLightFrontLeft5Blue'], 'SmartAmbientLightFrontLeft6': ['SmartAmbientLightFrontLeft6Brightness', 'SmartAmbientLightFrontLeft6Red', 'SmartAmbientLightFrontLeft6Green', 'SmartAmbientLightFrontLeft6Blue'], 'SmartAmbientLightFrontLeft7': ['SmartAmbientLightFrontLeft7Brightness', 'SmartAmbientLightFrontLeft7Red', 'SmartAmbientLightFrontLeft7Green', 'SmartAmbientLightFrontLeft7Blue'], 'SmartAmbientLightFrontLeft8': ['SmartAmbientLightFrontLeft8Brightness', 'SmartAmbientLightFrontLeft8Red', 'SmartAmbientLightFrontLeft8Green', 'SmartAmbientLightFrontLeft8Blue'], 'SmartAmbientLightFrontLeft9': ['SmartAmbientLightFrontLeft9Brightness', 'SmartAmbientLightFrontLeft9Red', 'SmartAmbientLightFrontLeft9Green', 'SmartAmbientLightFrontLeft9Blue'], 'SmartAmbientLightFrontLeft10': ['SmartAmbientLightFrontLeft10Brightness', 'SmartAmbientLightFrontLeft10Red', 'SmartAmbientLightFrontLeft10Green', 'SmartAmbientLightFrontLeft10Blue'], 'SmartAmbientLightFrontLeft11': ['SmartAmbientLightFrontLeft11Brightness', 'SmartAmbientLightFrontLeft11Red', 'SmartAmbientLightFrontLeft11Green', 'SmartAmbientLightFrontLeft11Blue'], 'SmartAmbientLightFrontLeft12': ['SmartAmbientLightFrontLeft12Brightness', 'SmartAmbientLightFrontLeft12Red', 'SmartAmbientLightFrontLeft12Green', 'SmartAmbientLightFrontLeft12Blue'], 'SmartAmbientLightFrontLeft13': ['SmartAmbientLightFrontLeft13Brightness', 'SmartAmbientLightFrontLeft13Red', 'SmartAmbientLightFrontLeft13Green', 'SmartAmbientLightFrontLeft13Blue'], 'SmartAmbientLightFrontLeft14': ['SmartAmbientLightFrontLeft14Brightness', 'SmartAmbientLightFrontLeft14Red', 'SmartAmbientLightFrontLeft14Green', 'SmartAmbientLightFrontLeft14Blue'], 'SmartAmbientLightFrontLeft15': ['SmartAmbientLightFrontLeft15Brightness', 'SmartAmbientLightFrontLeft15Red', 'SmartAmbientLightFrontLeft15Green', 'SmartAmbientLightFrontLeft15Blue'], 'SmartAmbientLightFrontLeft16': ['SmartAmbientLightFrontLeft16Brightness', 'SmartAmbientLightFrontLeft16Red', 'SmartAmbientLightFrontLeft16Green', 'SmartAmbientLightFrontLeft16Blue'], 'SmartAmbientLightFrontLeft17': ['SmartAmbientLightFrontLeft17Brightness', 'SmartAmbientLightFrontLeft17Red', 'SmartAmbientLightFrontLeft17Green', 'SmartAmbientLightFrontLeft17Blue'], 'SmartAmbientLightFrontLeft18': ['SmartAmbientLightFrontLeft18Brightness', 'SmartAmbientLightFrontLeft18Red', 'SmartAmbientLightFrontLeft18Green', 'SmartAmbientLightFrontLeft18Blue'], 'SmartAmbientLightFrontLeft19': ['SmartAmbientLightFrontLeft19Brightness', 'SmartAmbientLightFrontLeft19Red', 'SmartAmbientLightFrontLeft19Green', 'SmartAmbientLightFrontLeft19Blue'], 'SmartAmbientLightFrontLeft20': ['SmartAmbientLightFrontLeft20Brightness', 'SmartAmbientLightFrontLeft20Red', 'SmartAmbientLightFrontLeft20Green', 'SmartAmbientLightFrontLeft20Blue'], 'SmartAmbientLightFrontLeft21': ['SmartAmbientLightFrontLeft21Brightness', 'SmartAmbientLightFrontLeft21Red', 'SmartAmbientLightFrontLeft21Green', 'SmartAmbientLightFrontLeft21Blue'], 'SmartAmbientLightFrontLeft22': ['SmartAmbientLightFrontLeft22Brightness', 'SmartAmbientLightFrontLeft22Red', 'SmartAmbientLightFrontLeft22Green', 'SmartAmbientLightFrontLeft22Blue'], 'SmartAmbientLightFrontLeft23': ['SmartAmbientLightFrontLeft23Brightness', 'SmartAmbientLightFrontLeft23Red', 'SmartAmbientLightFrontLeft23Green', 'SmartAmbientLightFrontLeft23Blue'], 'SmartAmbientLightFrontLeft24': ['SmartAmbientLightFrontLeft24Brightness', 'SmartAmbientLightFrontLeft24Red', 'SmartAmbientLightFrontLeft24Green', 'SmartAmbientLightFrontLeft24Blue'], 'SmartAmbientLightFrontLeft25': ['SmartAmbientLightFrontLeft25Brightness', 'SmartAmbientLightFrontLeft25Red', 'SmartAmbientLightFrontLeft25Green', 'SmartAmbientLightFrontLeft25Blue'], 'SmartAmbientLightFrontLeft26': ['SmartAmbientLightFrontLeft26Brightness', 'SmartAmbientLightFrontLeft26Red', 'SmartAmbientLightFrontLeft26Green', 'SmartAmbientLightFrontLeft26Blue'], 'SmartAmbientLightFrontLeft27': ['SmartAmbientLightFrontLeft27Brightness', 'SmartAmbientLightFrontLeft27Red', 'SmartAmbientLightFrontLeft27Green', 'SmartAmbientLightFrontLeft27Blue'], 'SmartAmbientLightFrontLeft28': ['SmartAmbientLightFrontLeft28Brightness', 'SmartAmbientLightFrontLeft28Red', 'SmartAmbientLightFrontLeft28Green', 'SmartAmbientLightFrontLeft28Blue'], 'SmartAmbientLightFrontLeft29': ['SmartAmbientLightFrontLeft29Brightness', 'SmartAmbientLightFrontLeft29Red', 'SmartAmbientLightFrontLeft29Green', 'SmartAmbientLightFrontLeft29Blue'], 'SmartAmbientLightFrontLeft30': ['SmartAmbientLightFrontLeft30Brightness', 'SmartAmbientLightFrontLeft30Red', 'SmartAmbientLightFrontLeft30Green', 'SmartAmbientLightFrontLeft30Blue'], 'SmartAmbientLightFrontLeft31': ['SmartAmbientLightFrontLeft31Brightness', 'SmartAmbientLightFrontLeft31Red', 'SmartAmbientLightFrontLeft31Green', 'SmartAmbientLightFrontLeft31Blue'], 'SmartAmbientLightFrontLeft32': ['SmartAmbientLightFrontLeft32Brightness', 'SmartAmbientLightFrontLeft32Red', 'SmartAmbientLightFrontLeft32Green', 'SmartAmbientLightFrontLeft32Blue'], 'SmartAmbientLightFrontLeft33': ['SmartAmbientLightFrontLeft33Brightness', 'SmartAmbientLightFrontLeft33Red', 'SmartAmbientLightFrontLeft33Green', 'SmartAmbientLightFrontLeft33Blue'], 'SmartAmbientLightFrontLeft34': ['SmartAmbientLightFrontLeft34Brightness', 'SmartAmbientLightFrontLeft34Red', 'SmartAmbientLightFrontLeft34Green', 'SmartAmbientLightFrontLeft34Blue'], 'SmartAmbientLightFrontLeft35': ['SmartAmbientLightFrontLeft35Brightness', 'SmartAmbientLightFrontLeft35Red', 'SmartAmbientLightFrontLeft35Green', 'SmartAmbientLightFrontLeft35Blue'], 'SmartAmbientLightRearRight0': ['SmartAmbientLightRearRight0Brightness', 'SmartAmbientLightRearRight0Red', 'SmartAmbientLightRearRight0Green', 'SmartAmbientLightRearRight0Blue'], 'SmartAmbientLightRearRight1': ['SmartAmbientLightRearRight1Brightness', 'SmartAmbientLightRearRight1Red', 'SmartAmbientLightRearRight1Green', 'SmartAmbientLightRearRight1Blue'], 'SmartAmbientLightRearRight2': ['SmartAmbientLightRearRight2Brightness', 'SmartAmbientLightRearRight2Red', 'SmartAmbientLightRearRight2Green', 'SmartAmbientLightRearRight2Blue'], 'SmartAmbientLightRearRight3': ['SmartAmbientLightRearRight3Brightness', 'SmartAmbientLightRearRight3Red', 'SmartAmbientLightRearRight3Green', 'SmartAmbientLightRearRight3Blue'], 'SmartAmbientLightRearRight4': ['SmartAmbientLightRearRight4Brightness', 'SmartAmbientLightRearRight4Red', 'SmartAmbientLightRearRight4Green', 'SmartAmbientLightRearRight4Blue'], 'SmartAmbientLightRearRight5': ['SmartAmbientLightRearRight5Brightness', 'SmartAmbientLightRearRight5Red', 'SmartAmbientLightRearRight5Green', 'SmartAmbientLightRearRight5Blue'], 'SmartAmbientLightRearRight6': ['SmartAmbientLightRearRight6Brightness', 'SmartAmbientLightRearRight6Red', 'SmartAmbientLightRearRight6Green', 'SmartAmbientLightRearRight6Blue'], 'SmartAmbientLightRearRight7': ['SmartAmbientLightRearRight7Brightness', 'SmartAmbientLightRearRight7Red', 'SmartAmbientLightRearRight7Green', 'SmartAmbientLightRearRight7Blue'], 'SmartAmbientLightRearRight8': ['SmartAmbientLightRearRight8Brightness', 'SmartAmbientLightRearRight8Red', 'SmartAmbientLightRearRight8Green', 'SmartAmbientLightRearRight8Blue'], 'SmartAmbientLightRearRight9': ['SmartAmbientLightRearRight9Brightness', 'SmartAmbientLightRearRight9Red', 'SmartAmbientLightRearRight9Green', 'SmartAmbientLightRearRight9Blue'], 'SmartAmbientLightRearRight10': ['SmartAmbientLightRearRight10Brightness', 'SmartAmbientLightRearRight10Red', 'SmartAmbientLightRearRight10Green', 'SmartAmbientLightRearRight10Blue'], 'SmartAmbientLightRearRight11': ['SmartAmbientLightRearRight11Brightness', 'SmartAmbientLightRearRight11Red', 'SmartAmbientLightRearRight11Green', 'SmartAmbientLightRearRight11Blue'], 'SmartAmbientLightRearRight12': ['SmartAmbientLightRearRight12Brightness', 'SmartAmbientLightRearRight12Red', 'SmartAmbientLightRearRight12Green', 'SmartAmbientLightRearRight12Blue'], 'SmartAmbientLightRearRight13': ['SmartAmbientLightRearRight13Brightness', 'SmartAmbientLightRearRight13Red', 'SmartAmbientLightRearRight13Green', 'SmartAmbientLightRearRight13Blue'], 'SmartAmbientLightRearRight14': ['SmartAmbientLightRearRight14Brightness', 'SmartAmbientLightRearRight14Red', 'SmartAmbientLightRearRight14Green', 'SmartAmbientLightRearRight14Blue'], 'SmartAmbientLightRearRight15': ['SmartAmbientLightRearRight15Brightness', 'SmartAmbientLightRearRight15Red', 'SmartAmbientLightRearRight15Green', 'SmartAmbientLightRearRight15Blue'], 'SmartAmbientLightRearRight16': ['SmartAmbientLightRearRight16Brightness', 'SmartAmbientLightRearRight16Red', 'SmartAmbientLightRearRight16Green', 'SmartAmbientLightRearRight16Blue'], 'SmartAmbientLightRearRight17': ['SmartAmbientLightRearRight17Brightness', 'SmartAmbientLightRearRight17Red', 'SmartAmbientLightRearRight17Green', 'SmartAmbientLightRearRight17Blue'], 'SmartAmbientLightRearRight18': ['SmartAmbientLightRearRight18Brightness', 'SmartAmbientLightRearRight18Red', 'SmartAmbientLightRearRight18Green', 'SmartAmbientLightRearRight18Blue'], 'SmartAmbientLightRearRight19': ['SmartAmbientLightRearRight19Brightness', 'SmartAmbientLightRearRight19Red', 'SmartAmbientLightRearRight19Green', 'SmartAmbientLightRearRight19Blue'], 'SmartAmbientLightRearRight20': ['SmartAmbientLightRearRight20Brightness', 'SmartAmbientLightRearRight20Red', 'SmartAmbientLightRearRight20Green', 'SmartAmbientLightRearRight20Blue'], 'SmartAmbientLightRearRight21': ['SmartAmbientLightRearRight21Brightness', 'SmartAmbientLightRearRight21Red', 'SmartAmbientLightRearRight21Green', 'SmartAmbientLightRearRight21Blue'], 'SmartAmbientLightRearRight22': ['SmartAmbientLightRearRight22Brightness', 'SmartAmbientLightRearRight22Red', 'SmartAmbientLightRearRight22Green', 'SmartAmbientLightRearRight22Blue'], 'SmartAmbientLightRearRight23': ['SmartAmbientLightRearRight23Brightness', 'SmartAmbientLightRearRight23Red', 'SmartAmbientLightRearRight23Green', 'SmartAmbientLightRearRight23Blue'], 'SmartAmbientLightRearRight24': ['SmartAmbientLightRearRight24Brightness', 'SmartAmbientLightRearRight24Red', 'SmartAmbientLightRearRight24Green', 'SmartAmbientLightRearRight24Blue'], 'SmartAmbientLightRearRight25': ['SmartAmbientLightRearRight25Brightness', 'SmartAmbientLightRearRight25Red', 'SmartAmbientLightRearRight25Green', 'SmartAmbientLightRearRight25Blue'], 'SmartAmbientLightRearRight26': ['SmartAmbientLightRearRight26Brightness', 'SmartAmbientLightRearRight26Red', 'SmartAmbientLightRearRight26Green', 'SmartAmbientLightRearRight26Blue'], 'SmartAmbientLightRearRight27': ['SmartAmbientLightRearRight27Brightness', 'SmartAmbientLightRearRight27Red', 'SmartAmbientLightRearRight27Green', 'SmartAmbientLightRearRight27Blue'], 'SmartAmbientLightRearRight28': ['SmartAmbientLightRearRight28Brightness', 'SmartAmbientLightRearRight28Red', 'SmartAmbientLightRearRight28Green', 'SmartAmbientLightRearRight28Blue'], 'SmartAmbientLightRearRight29': ['SmartAmbientLightRearRight29Brightness', 'SmartAmbientLightRearRight29Red', 'SmartAmbientLightRearRight29Green', 'SmartAmbientLightRearRight29Blue'], 'SmartAmbientLightRearLeft0': ['SmartAmbientLightRearLeft0Brightness', 'SmartAmbientLightRearLeft0Red', 'SmartAmbientLightRearLeft0Green', 'SmartAmbientLightRearLeft0Blue'], 'SmartAmbientLightRearLeft1': ['SmartAmbientLightRearLeft1Brightness', 'SmartAmbientLightRearLeft1Red', 'SmartAmbientLightRearLeft1Green', 'SmartAmbientLightRearLeft1Blue'], 'SmartAmbientLightRearLeft2': ['SmartAmbientLightRearLeft2Brightness', 'SmartAmbientLightRearLeft2Red', 'SmartAmbientLightRearLeft2Green', 'SmartAmbientLightRearLeft2Blue'], 'SmartAmbientLightRearLeft3': ['SmartAmbientLightRearLeft3Brightness', 'SmartAmbientLightRearLeft3Red', 'SmartAmbientLightRearLeft3Green', 'SmartAmbientLightRearLeft3Blue'], 'SmartAmbientLightRearLeft4': ['SmartAmbientLightRearLeft4Brightness', 'SmartAmbientLightRearLeft4Red', 'SmartAmbientLightRearLeft4Green', 'SmartAmbientLightRearLeft4Blue'], 'SmartAmbientLightRearLeft5': ['SmartAmbientLightRearLeft5Brightness', 'SmartAmbientLightRearLeft5Red', 'SmartAmbientLightRearLeft5Green', 'SmartAmbientLightRearLeft5Blue'], 'SmartAmbientLightRearLeft6': ['SmartAmbientLightRearLeft6Brightness', 'SmartAmbientLightRearLeft6Red', 'SmartAmbientLightRearLeft6Green', 'SmartAmbientLightRearLeft6Blue'], 'SmartAmbientLightRearLeft7': ['SmartAmbientLightRearLeft7Brightness', 'SmartAmbientLightRearLeft7Red', 'SmartAmbientLightRearLeft7Green', 'SmartAmbientLightRearLeft7Blue'], 'SmartAmbientLightRearLeft8': ['SmartAmbientLightRearLeft8Brightness', 'SmartAmbientLightRearLeft8Red', 'SmartAmbientLightRearLeft8Green', 'SmartAmbientLightRearLeft8Blue'], 'SmartAmbientLightRearLeft9': ['SmartAmbientLightRearLeft9Brightness', 'SmartAmbientLightRearLeft9Red', 'SmartAmbientLightRearLeft9Green', 'SmartAmbientLightRearLeft9Blue'], 'SmartAmbientLightRearLeft10': ['SmartAmbientLightRearLeft10Brightness', 'SmartAmbientLightRearLeft10Red', 'SmartAmbientLightRearLeft10Green', 'SmartAmbientLightRearLeft10Blue'], 'SmartAmbientLightRearLeft11': ['SmartAmbientLightRearLeft11Brightness', 'SmartAmbientLightRearLeft11Red', 'SmartAmbientLightRearLeft11Green', 'SmartAmbientLightRearLeft11Blue'], 'SmartAmbientLightRearLeft12': ['SmartAmbientLightRearLeft12Brightness', 'SmartAmbientLightRearLeft12Red', 'SmartAmbientLightRearLeft12Green', 'SmartAmbientLightRearLeft12Blue'], 'SmartAmbientLightRearLeft13': ['SmartAmbientLightRearLeft13Brightness', 'SmartAmbientLightRearLeft13Red', 'SmartAmbientLightRearLeft13Green', 'SmartAmbientLightRearLeft13Blue'], 'SmartAmbientLightRearLeft14': ['SmartAmbientLightRearLeft14Brightness', 'SmartAmbientLightRearLeft14Red', 'SmartAmbientLightRearLeft14Green', 'SmartAmbientLightRearLeft14Blue'], 'SmartAmbientLightRearLeft15': ['SmartAmbientLightRearLeft15Brightness', 'SmartAmbientLightRearLeft15Red', 'SmartAmbientLightRearLeft15Green', 'SmartAmbientLightRearLeft15Blue'], 'SmartAmbientLightRearLeft16': ['SmartAmbientLightRearLeft16Brightness', 'SmartAmbientLightRearLeft16Red', 'SmartAmbientLightRearLeft16Green', 'SmartAmbientLightRearLeft16Blue'], 'SmartAmbientLightRearLeft17': ['SmartAmbientLightRearLeft17Brightness', 'SmartAmbientLightRearLeft17Red', 'SmartAmbientLightRearLeft17Green', 'SmartAmbientLightRearLeft17Blue'], 'SmartAmbientLightRearLeft18': ['SmartAmbientLightRearLeft18Brightness', 'SmartAmbientLightRearLeft18Red', 'SmartAmbientLightRearLeft18Green', 'SmartAmbientLightRearLeft18Blue'], 'SmartAmbientLightRearLeft19': ['SmartAmbientLightRearLeft19Brightness', 'SmartAmbientLightRearLeft19Red', 'SmartAmbientLightRearLeft19Green', 'SmartAmbientLightRearLeft19Blue'], 'SmartAmbientLightRearLeft20': ['SmartAmbientLightRearLeft20Brightness', 'SmartAmbientLightRearLeft20Red', 'SmartAmbientLightRearLeft20Green', 'SmartAmbientLightRearLeft20Blue'], 'SmartAmbientLightRearLeft21': ['SmartAmbientLightRearLeft21Brightness', 'SmartAmbientLightRearLeft21Red', 'SmartAmbientLightRearLeft21Green', 'SmartAmbientLightRearLeft21Blue'], 'SmartAmbientLightRearLeft22': ['SmartAmbientLightRearLeft22Brightness', 'SmartAmbientLightRearLeft22Red', 'SmartAmbientLightRearLeft22Green', 'SmartAmbientLightRearLeft22Blue'], 'SmartAmbientLightRearLeft23': ['SmartAmbientLightRearLeft23Brightness', 'SmartAmbientLightRearLeft23Red', 'SmartAmbientLightRearLeft23Green', 'SmartAmbientLightRearLeft23Blue'], 'SmartAmbientLightRearLeft24': ['SmartAmbientLightRearLeft24Brightness', 'SmartAmbientLightRearLeft24Red', 'SmartAmbientLightRearLeft24Green', 'SmartAmbientLightRearLeft24Blue'], 'SmartAmbientLightRearLeft25': ['SmartAmbientLightRearLeft25Brightness', 'SmartAmbientLightRearLeft25Red', 'SmartAmbientLightRearLeft25Green', 'SmartAmbientLightRearLeft25Blue'], 'SmartAmbientLightRearLeft26': ['SmartAmbientLightRearLeft26Brightness', 'SmartAmbientLightRearLeft26Red', 'SmartAmbientLightRearLeft26Green', 'SmartAmbientLightRearLeft26Blue'], 'SmartAmbientLightRearLeft27': ['SmartAmbientLightRearLeft27Brightness', 'SmartAmbientLightRearLeft27Red', 'SmartAmbientLightRearLeft27Green', 'SmartAmbientLightRearLeft27Blue'], 'SmartAmbientLightRearLeft28': ['SmartAmbientLightRearLeft28Brightness', 'SmartAmbientLightRearLeft28Red', 'SmartAmbientLightRearLeft28Green', 'SmartAmbientLightRearLeft28Blue'], 'SmartAmbientLightRearLeft29': ['SmartAmbientLightRearLeft29Brightness', 'SmartAmbientLightRearLeft29Red', 'SmartAmbientLightRearLeft29Green', 'SmartAmbientLightRearLeft29Blue']}

    class SmartAmbientLightIpRight0Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class SmartAmbientLightIpRight0Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class SmartAmbientLightIpRight0Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class SmartAmbientLightIpRight0Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class SmartAmbientLightIpRight1Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 38
        value_definition = {}

    class SmartAmbientLightIpRight1Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class SmartAmbientLightIpRight1Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class SmartAmbientLightIpRight1Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class SmartAmbientLightIpRight2Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 70
        value_definition = {}

    class SmartAmbientLightIpRight2Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class SmartAmbientLightIpRight2Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class SmartAmbientLightIpRight2Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class SmartAmbientLightIpRight3Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 102
        value_definition = {}

    class SmartAmbientLightIpRight3Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class SmartAmbientLightIpRight3Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class SmartAmbientLightIpRight3Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class SmartAmbientLightIpRight4Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 134
        value_definition = {}

    class SmartAmbientLightIpRight4Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 143
        value_definition = {}

    class SmartAmbientLightIpRight4Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 151
        value_definition = {}

    class SmartAmbientLightIpRight4Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 159
        value_definition = {}

    class SmartAmbientLightIpRight5Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 166
        value_definition = {}

    class SmartAmbientLightIpRight5Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 175
        value_definition = {}

    class SmartAmbientLightIpRight5Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 183
        value_definition = {}

    class SmartAmbientLightIpRight5Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 191
        value_definition = {}

    class SmartAmbientLightIpRight6Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 198
        value_definition = {}

    class SmartAmbientLightIpRight6Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 207
        value_definition = {}

    class SmartAmbientLightIpRight6Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 215
        value_definition = {}

    class SmartAmbientLightIpRight6Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 223
        value_definition = {}

    class SmartAmbientLightIpRight7Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 230
        value_definition = {}

    class SmartAmbientLightIpRight7Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 239
        value_definition = {}

    class SmartAmbientLightIpRight7Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class SmartAmbientLightIpRight7Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 255
        value_definition = {}

    class SmartAmbientLightIpRight8Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 262
        value_definition = {}

    class SmartAmbientLightIpRight8Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 271
        value_definition = {}

    class SmartAmbientLightIpRight8Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 279
        value_definition = {}

    class SmartAmbientLightIpRight8Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 287
        value_definition = {}

    class SmartAmbientLightIpRight9Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 294
        value_definition = {}

    class SmartAmbientLightIpRight9Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 303
        value_definition = {}

    class SmartAmbientLightIpRight9Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 311
        value_definition = {}

    class SmartAmbientLightIpRight9Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 319
        value_definition = {}

    class SmartAmbientLightIpRight10Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 326
        value_definition = {}

    class SmartAmbientLightIpRight10Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 335
        value_definition = {}

    class SmartAmbientLightIpRight10Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 343
        value_definition = {}

    class SmartAmbientLightIpRight10Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 351
        value_definition = {}

    class SmartAmbientLightIpRight11Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 358
        value_definition = {}

    class SmartAmbientLightIpRight11Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 367
        value_definition = {}

    class SmartAmbientLightIpRight11Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 375
        value_definition = {}

    class SmartAmbientLightIpRight11Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 383
        value_definition = {}

    class SmartAmbientLightIpRight12Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 390
        value_definition = {}

    class SmartAmbientLightIpRight12Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 399
        value_definition = {}

    class SmartAmbientLightIpRight12Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 407
        value_definition = {}

    class SmartAmbientLightIpRight12Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 415
        value_definition = {}

    class SmartAmbientLightIpRight13Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 422
        value_definition = {}

    class SmartAmbientLightIpRight13Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 431
        value_definition = {}

    class SmartAmbientLightIpRight13Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 439
        value_definition = {}

    class SmartAmbientLightIpRight13Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 447
        value_definition = {}

    class SmartAmbientLightIpRight14Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 454
        value_definition = {}

    class SmartAmbientLightIpRight14Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 463
        value_definition = {}

    class SmartAmbientLightIpRight14Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 471
        value_definition = {}

    class SmartAmbientLightIpRight14Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 479
        value_definition = {}

    class SmartAmbientLightIpRight15Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 486
        value_definition = {}

    class SmartAmbientLightIpRight15Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 495
        value_definition = {}

    class SmartAmbientLightIpRight15Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 503
        value_definition = {}

    class SmartAmbientLightIpRight15Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 511
        value_definition = {}

    class SmartAmbientLightIpRight16Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 518
        value_definition = {}

    class SmartAmbientLightIpRight16Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 527
        value_definition = {}

    class SmartAmbientLightIpRight16Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 535
        value_definition = {}

    class SmartAmbientLightIpRight16Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 543
        value_definition = {}

    class SmartAmbientLightIpRight17Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 550
        value_definition = {}

    class SmartAmbientLightIpRight17Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 559
        value_definition = {}

    class SmartAmbientLightIpRight17Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 567
        value_definition = {}

    class SmartAmbientLightIpRight17Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 575
        value_definition = {}

    class SmartAmbientLightIpRight18Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 582
        value_definition = {}

    class SmartAmbientLightIpRight18Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 591
        value_definition = {}

    class SmartAmbientLightIpRight18Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 599
        value_definition = {}

    class SmartAmbientLightIpRight18Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 607
        value_definition = {}

    class SmartAmbientLightIpRight19Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 614
        value_definition = {}

    class SmartAmbientLightIpRight19Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 623
        value_definition = {}

    class SmartAmbientLightIpRight19Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 631
        value_definition = {}

    class SmartAmbientLightIpRight19Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 639
        value_definition = {}

    class SmartAmbientLightIpRight20Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 646
        value_definition = {}

    class SmartAmbientLightIpRight20Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 655
        value_definition = {}

    class SmartAmbientLightIpRight20Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 663
        value_definition = {}

    class SmartAmbientLightIpRight20Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 671
        value_definition = {}

    class SmartAmbientLightIpRight21Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 678
        value_definition = {}

    class SmartAmbientLightIpRight21Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 687
        value_definition = {}

    class SmartAmbientLightIpRight21Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 695
        value_definition = {}

    class SmartAmbientLightIpRight21Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 703
        value_definition = {}

    class SmartAmbientLightIpRight22Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 710
        value_definition = {}

    class SmartAmbientLightIpRight22Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 719
        value_definition = {}

    class SmartAmbientLightIpRight22Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 727
        value_definition = {}

    class SmartAmbientLightIpRight22Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 735
        value_definition = {}

    class SmartAmbientLightIpRight23Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 742
        value_definition = {}

    class SmartAmbientLightIpRight23Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 751
        value_definition = {}

    class SmartAmbientLightIpRight23Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 759
        value_definition = {}

    class SmartAmbientLightIpRight23Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 767
        value_definition = {}

    class SmartAmbientLightIpRight24Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 774
        value_definition = {}

    class SmartAmbientLightIpRight24Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 783
        value_definition = {}

    class SmartAmbientLightIpRight24Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 791
        value_definition = {}

    class SmartAmbientLightIpRight24Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 799
        value_definition = {}

    class SmartAmbientLightIpRight25Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 806
        value_definition = {}

    class SmartAmbientLightIpRight25Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 815
        value_definition = {}

    class SmartAmbientLightIpRight25Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 823
        value_definition = {}

    class SmartAmbientLightIpRight25Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 831
        value_definition = {}

    class SmartAmbientLightIpRight26Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 838
        value_definition = {}

    class SmartAmbientLightIpRight26Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 847
        value_definition = {}

    class SmartAmbientLightIpRight26Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 855
        value_definition = {}

    class SmartAmbientLightIpRight26Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 863
        value_definition = {}

    class SmartAmbientLightIpRight27Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 870
        value_definition = {}

    class SmartAmbientLightIpRight27Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 879
        value_definition = {}

    class SmartAmbientLightIpRight27Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 887
        value_definition = {}

    class SmartAmbientLightIpRight27Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 895
        value_definition = {}

    class SmartAmbientLightIpRight28Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 902
        value_definition = {}

    class SmartAmbientLightIpRight28Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 911
        value_definition = {}

    class SmartAmbientLightIpRight28Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 919
        value_definition = {}

    class SmartAmbientLightIpRight28Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 927
        value_definition = {}

    class SmartAmbientLightIpRight29Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 934
        value_definition = {}

    class SmartAmbientLightIpRight29Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 943
        value_definition = {}

    class SmartAmbientLightIpRight29Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 951
        value_definition = {}

    class SmartAmbientLightIpRight29Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 959
        value_definition = {}

    class SmartAmbientLightIpRight30Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 966
        value_definition = {}

    class SmartAmbientLightIpRight30Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 975
        value_definition = {}

    class SmartAmbientLightIpRight30Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 983
        value_definition = {}

    class SmartAmbientLightIpRight30Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 991
        value_definition = {}

    class SmartAmbientLightIpRight31Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 998
        value_definition = {}

    class SmartAmbientLightIpRight31Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1007
        value_definition = {}

    class SmartAmbientLightIpRight31Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1015
        value_definition = {}

    class SmartAmbientLightIpRight31Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1023
        value_definition = {}

    class SmartAmbientLightIpRight32Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1030
        value_definition = {}

    class SmartAmbientLightIpRight32Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1039
        value_definition = {}

    class SmartAmbientLightIpRight32Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1047
        value_definition = {}

    class SmartAmbientLightIpRight32Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1055
        value_definition = {}

    class SmartAmbientLightIpRight33Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1062
        value_definition = {}

    class SmartAmbientLightIpRight33Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1071
        value_definition = {}

    class SmartAmbientLightIpRight33Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1079
        value_definition = {}

    class SmartAmbientLightIpRight33Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1087
        value_definition = {}

    class SmartAmbientLightIpRight34Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1094
        value_definition = {}

    class SmartAmbientLightIpRight34Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1103
        value_definition = {}

    class SmartAmbientLightIpRight34Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1111
        value_definition = {}

    class SmartAmbientLightIpRight34Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1119
        value_definition = {}

    class SmartAmbientLightIpRight35Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1126
        value_definition = {}

    class SmartAmbientLightIpRight35Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1135
        value_definition = {}

    class SmartAmbientLightIpRight35Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1143
        value_definition = {}

    class SmartAmbientLightIpRight35Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1151
        value_definition = {}

    class SmartAmbientLightIpRight36Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1158
        value_definition = {}

    class SmartAmbientLightIpRight36Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1167
        value_definition = {}

    class SmartAmbientLightIpRight36Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1175
        value_definition = {}

    class SmartAmbientLightIpRight36Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1183
        value_definition = {}

    class SmartAmbientLightIpRight37Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1190
        value_definition = {}

    class SmartAmbientLightIpRight37Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1199
        value_definition = {}

    class SmartAmbientLightIpRight37Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1207
        value_definition = {}

    class SmartAmbientLightIpRight37Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1215
        value_definition = {}

    class SmartAmbientLightIpRight38Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1222
        value_definition = {}

    class SmartAmbientLightIpRight38Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1231
        value_definition = {}

    class SmartAmbientLightIpRight38Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1239
        value_definition = {}

    class SmartAmbientLightIpRight38Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1247
        value_definition = {}

    class SmartAmbientLightIpRight39Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1254
        value_definition = {}

    class SmartAmbientLightIpRight39Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1263
        value_definition = {}

    class SmartAmbientLightIpRight39Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1271
        value_definition = {}

    class SmartAmbientLightIpRight39Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1279
        value_definition = {}

    class SmartAmbientLightIpRight40Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1286
        value_definition = {}

    class SmartAmbientLightIpRight40Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1295
        value_definition = {}

    class SmartAmbientLightIpRight40Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1303
        value_definition = {}

    class SmartAmbientLightIpRight40Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1311
        value_definition = {}

    class SmartAmbientLightIpRight41Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1318
        value_definition = {}

    class SmartAmbientLightIpRight41Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1327
        value_definition = {}

    class SmartAmbientLightIpRight41Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1335
        value_definition = {}

    class SmartAmbientLightIpRight41Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1343
        value_definition = {}

    class SmartAmbientLightIpRight42Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1350
        value_definition = {}

    class SmartAmbientLightIpRight42Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1359
        value_definition = {}

    class SmartAmbientLightIpRight42Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1367
        value_definition = {}

    class SmartAmbientLightIpRight42Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1375
        value_definition = {}

    class SmartAmbientLightIpRight43Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1382
        value_definition = {}

    class SmartAmbientLightIpRight43Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1391
        value_definition = {}

    class SmartAmbientLightIpRight43Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1399
        value_definition = {}

    class SmartAmbientLightIpRight43Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1407
        value_definition = {}

    class SmartAmbientLightIpRight44Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1414
        value_definition = {}

    class SmartAmbientLightIpRight44Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1423
        value_definition = {}

    class SmartAmbientLightIpRight44Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1431
        value_definition = {}

    class SmartAmbientLightIpRight44Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1439
        value_definition = {}

    class SmartAmbientLightIpRight45Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1446
        value_definition = {}

    class SmartAmbientLightIpRight45Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1455
        value_definition = {}

    class SmartAmbientLightIpRight45Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1463
        value_definition = {}

    class SmartAmbientLightIpRight45Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1471
        value_definition = {}

    class SmartAmbientLightIpRight46Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1478
        value_definition = {}

    class SmartAmbientLightIpRight46Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1487
        value_definition = {}

    class SmartAmbientLightIpRight46Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1495
        value_definition = {}

    class SmartAmbientLightIpRight46Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1503
        value_definition = {}

    class SmartAmbientLightIpRight47Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1510
        value_definition = {}

    class SmartAmbientLightIpRight47Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1519
        value_definition = {}

    class SmartAmbientLightIpRight47Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1527
        value_definition = {}

    class SmartAmbientLightIpRight47Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1535
        value_definition = {}

    class SmartAmbientLightIpLeft0Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1542
        value_definition = {}

    class SmartAmbientLightIpLeft0Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1551
        value_definition = {}

    class SmartAmbientLightIpLeft0Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1559
        value_definition = {}

    class SmartAmbientLightIpLeft0Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1567
        value_definition = {}

    class SmartAmbientLightIpLeft1Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1574
        value_definition = {}

    class SmartAmbientLightIpLeft1Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1583
        value_definition = {}

    class SmartAmbientLightIpLeft1Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1591
        value_definition = {}

    class SmartAmbientLightIpLeft1Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1599
        value_definition = {}

    class SmartAmbientLightIpLeft2Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1606
        value_definition = {}

    class SmartAmbientLightIpLeft2Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1615
        value_definition = {}

    class SmartAmbientLightIpLeft2Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1623
        value_definition = {}

    class SmartAmbientLightIpLeft2Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1631
        value_definition = {}

    class SmartAmbientLightIpLeft3Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1638
        value_definition = {}

    class SmartAmbientLightIpLeft3Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1647
        value_definition = {}

    class SmartAmbientLightIpLeft3Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1655
        value_definition = {}

    class SmartAmbientLightIpLeft3Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1663
        value_definition = {}

    class SmartAmbientLightIpLeft4Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1670
        value_definition = {}

    class SmartAmbientLightIpLeft4Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1679
        value_definition = {}

    class SmartAmbientLightIpLeft4Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1687
        value_definition = {}

    class SmartAmbientLightIpLeft4Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1695
        value_definition = {}

    class SmartAmbientLightIpLeft5Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1702
        value_definition = {}

    class SmartAmbientLightIpLeft5Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1711
        value_definition = {}

    class SmartAmbientLightIpLeft5Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1719
        value_definition = {}

    class SmartAmbientLightIpLeft5Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1727
        value_definition = {}

    class SmartAmbientLightIpLeft6Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1734
        value_definition = {}

    class SmartAmbientLightIpLeft6Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1743
        value_definition = {}

    class SmartAmbientLightIpLeft6Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1751
        value_definition = {}

    class SmartAmbientLightIpLeft6Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1759
        value_definition = {}

    class SmartAmbientLightIpLeft7Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1766
        value_definition = {}

    class SmartAmbientLightIpLeft7Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1775
        value_definition = {}

    class SmartAmbientLightIpLeft7Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1783
        value_definition = {}

    class SmartAmbientLightIpLeft7Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1791
        value_definition = {}

    class SmartAmbientLightIpLeft8Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1798
        value_definition = {}

    class SmartAmbientLightIpLeft8Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1807
        value_definition = {}

    class SmartAmbientLightIpLeft8Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1815
        value_definition = {}

    class SmartAmbientLightIpLeft8Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1823
        value_definition = {}

    class SmartAmbientLightIpLeft9Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1830
        value_definition = {}

    class SmartAmbientLightIpLeft9Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1839
        value_definition = {}

    class SmartAmbientLightIpLeft9Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1847
        value_definition = {}

    class SmartAmbientLightIpLeft9Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1855
        value_definition = {}

    class SmartAmbientLightIpLeft10Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1862
        value_definition = {}

    class SmartAmbientLightIpLeft10Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1871
        value_definition = {}

    class SmartAmbientLightIpLeft10Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1879
        value_definition = {}

    class SmartAmbientLightIpLeft10Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1887
        value_definition = {}

    class SmartAmbientLightIpLeft11Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1894
        value_definition = {}

    class SmartAmbientLightIpLeft11Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1903
        value_definition = {}

    class SmartAmbientLightIpLeft11Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1911
        value_definition = {}

    class SmartAmbientLightIpLeft11Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1919
        value_definition = {}

    class SmartAmbientLightIpLeft12Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1926
        value_definition = {}

    class SmartAmbientLightIpLeft12Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1935
        value_definition = {}

    class SmartAmbientLightIpLeft12Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1943
        value_definition = {}

    class SmartAmbientLightIpLeft12Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1951
        value_definition = {}

    class SmartAmbientLightIpLeft13Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1958
        value_definition = {}

    class SmartAmbientLightIpLeft13Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1967
        value_definition = {}

    class SmartAmbientLightIpLeft13Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1975
        value_definition = {}

    class SmartAmbientLightIpLeft13Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1983
        value_definition = {}

    class SmartAmbientLightIpLeft14Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 1990
        value_definition = {}

    class SmartAmbientLightIpLeft14Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 1999
        value_definition = {}

    class SmartAmbientLightIpLeft14Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2007
        value_definition = {}

    class SmartAmbientLightIpLeft14Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2015
        value_definition = {}

    class SmartAmbientLightIpLeft15Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2022
        value_definition = {}

    class SmartAmbientLightIpLeft15Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2031
        value_definition = {}

    class SmartAmbientLightIpLeft15Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2039
        value_definition = {}

    class SmartAmbientLightIpLeft15Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2047
        value_definition = {}

    class SmartAmbientLightIpLeft16Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2054
        value_definition = {}

    class SmartAmbientLightIpLeft16Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2063
        value_definition = {}

    class SmartAmbientLightIpLeft16Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2071
        value_definition = {}

    class SmartAmbientLightIpLeft16Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2079
        value_definition = {}

    class SmartAmbientLightIpLeft17Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2086
        value_definition = {}

    class SmartAmbientLightIpLeft17Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2095
        value_definition = {}

    class SmartAmbientLightIpLeft17Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2103
        value_definition = {}

    class SmartAmbientLightIpLeft17Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2111
        value_definition = {}

    class SmartAmbientLightIpLeft18Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2118
        value_definition = {}

    class SmartAmbientLightIpLeft18Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2127
        value_definition = {}

    class SmartAmbientLightIpLeft18Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2135
        value_definition = {}

    class SmartAmbientLightIpLeft18Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2143
        value_definition = {}

    class SmartAmbientLightIpLeft19Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2150
        value_definition = {}

    class SmartAmbientLightIpLeft19Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2159
        value_definition = {}

    class SmartAmbientLightIpLeft19Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2167
        value_definition = {}

    class SmartAmbientLightIpLeft19Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2175
        value_definition = {}

    class SmartAmbientLightIpLeft20Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2182
        value_definition = {}

    class SmartAmbientLightIpLeft20Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2191
        value_definition = {}

    class SmartAmbientLightIpLeft20Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2199
        value_definition = {}

    class SmartAmbientLightIpLeft20Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2207
        value_definition = {}

    class SmartAmbientLightIpLeft21Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2214
        value_definition = {}

    class SmartAmbientLightIpLeft21Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2223
        value_definition = {}

    class SmartAmbientLightIpLeft21Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2231
        value_definition = {}

    class SmartAmbientLightIpLeft21Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2239
        value_definition = {}

    class SmartAmbientLightIpLeft22Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2246
        value_definition = {}

    class SmartAmbientLightIpLeft22Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2255
        value_definition = {}

    class SmartAmbientLightIpLeft22Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2263
        value_definition = {}

    class SmartAmbientLightIpLeft22Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2271
        value_definition = {}

    class SmartAmbientLightIpLeft23Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2278
        value_definition = {}

    class SmartAmbientLightIpLeft23Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2287
        value_definition = {}

    class SmartAmbientLightIpLeft23Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2295
        value_definition = {}

    class SmartAmbientLightIpLeft23Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2303
        value_definition = {}

    class SmartAmbientLightIpLeft24Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2310
        value_definition = {}

    class SmartAmbientLightIpLeft24Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2319
        value_definition = {}

    class SmartAmbientLightIpLeft24Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2327
        value_definition = {}

    class SmartAmbientLightIpLeft24Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2335
        value_definition = {}

    class SmartAmbientLightIpLeft25Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2342
        value_definition = {}

    class SmartAmbientLightIpLeft25Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2351
        value_definition = {}

    class SmartAmbientLightIpLeft25Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2359
        value_definition = {}

    class SmartAmbientLightIpLeft25Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2367
        value_definition = {}

    class SmartAmbientLightIpLeft26Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2374
        value_definition = {}

    class SmartAmbientLightIpLeft26Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2383
        value_definition = {}

    class SmartAmbientLightIpLeft26Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2391
        value_definition = {}

    class SmartAmbientLightIpLeft26Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2399
        value_definition = {}

    class SmartAmbientLightIpLeft27Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2406
        value_definition = {}

    class SmartAmbientLightIpLeft27Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2415
        value_definition = {}

    class SmartAmbientLightIpLeft27Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2423
        value_definition = {}

    class SmartAmbientLightIpLeft27Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2431
        value_definition = {}

    class SmartAmbientLightIpLeft28Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2438
        value_definition = {}

    class SmartAmbientLightIpLeft28Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2447
        value_definition = {}

    class SmartAmbientLightIpLeft28Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2455
        value_definition = {}

    class SmartAmbientLightIpLeft28Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2463
        value_definition = {}

    class SmartAmbientLightIpLeft29Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2470
        value_definition = {}

    class SmartAmbientLightIpLeft29Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2479
        value_definition = {}

    class SmartAmbientLightIpLeft29Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2487
        value_definition = {}

    class SmartAmbientLightIpLeft29Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2495
        value_definition = {}

    class SmartAmbientLightIpLeft30Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2502
        value_definition = {}

    class SmartAmbientLightIpLeft30Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2511
        value_definition = {}

    class SmartAmbientLightIpLeft30Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2519
        value_definition = {}

    class SmartAmbientLightIpLeft30Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2527
        value_definition = {}

    class SmartAmbientLightIpLeft31Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2534
        value_definition = {}

    class SmartAmbientLightIpLeft31Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2543
        value_definition = {}

    class SmartAmbientLightIpLeft31Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2551
        value_definition = {}

    class SmartAmbientLightIpLeft31Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2559
        value_definition = {}

    class SmartAmbientLightIpLeft32Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2566
        value_definition = {}

    class SmartAmbientLightIpLeft32Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2575
        value_definition = {}

    class SmartAmbientLightIpLeft32Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2583
        value_definition = {}

    class SmartAmbientLightIpLeft32Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2591
        value_definition = {}

    class SmartAmbientLightIpLeft33Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2598
        value_definition = {}

    class SmartAmbientLightIpLeft33Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2607
        value_definition = {}

    class SmartAmbientLightIpLeft33Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2615
        value_definition = {}

    class SmartAmbientLightIpLeft33Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2623
        value_definition = {}

    class SmartAmbientLightIpLeft34Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2630
        value_definition = {}

    class SmartAmbientLightIpLeft34Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2639
        value_definition = {}

    class SmartAmbientLightIpLeft34Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2647
        value_definition = {}

    class SmartAmbientLightIpLeft34Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2655
        value_definition = {}

    class SmartAmbientLightIpLeft35Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2662
        value_definition = {}

    class SmartAmbientLightIpLeft35Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2671
        value_definition = {}

    class SmartAmbientLightIpLeft35Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2679
        value_definition = {}

    class SmartAmbientLightIpLeft35Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2687
        value_definition = {}

    class SmartAmbientLightFrontRight0Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2694
        value_definition = {}

    class SmartAmbientLightFrontRight0Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2703
        value_definition = {}

    class SmartAmbientLightFrontRight0Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2711
        value_definition = {}

    class SmartAmbientLightFrontRight0Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2719
        value_definition = {}

    class SmartAmbientLightFrontRight1Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2726
        value_definition = {}

    class SmartAmbientLightFrontRight1Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2735
        value_definition = {}

    class SmartAmbientLightFrontRight1Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2743
        value_definition = {}

    class SmartAmbientLightFrontRight1Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2751
        value_definition = {}

    class SmartAmbientLightFrontRight2Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2758
        value_definition = {}

    class SmartAmbientLightFrontRight2Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2767
        value_definition = {}

    class SmartAmbientLightFrontRight2Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2775
        value_definition = {}

    class SmartAmbientLightFrontRight2Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2783
        value_definition = {}

    class SmartAmbientLightFrontRight3Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2790
        value_definition = {}

    class SmartAmbientLightFrontRight3Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2799
        value_definition = {}

    class SmartAmbientLightFrontRight3Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2807
        value_definition = {}

    class SmartAmbientLightFrontRight3Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2815
        value_definition = {}

    class SmartAmbientLightFrontRight4Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2822
        value_definition = {}

    class SmartAmbientLightFrontRight4Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2831
        value_definition = {}

    class SmartAmbientLightFrontRight4Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2839
        value_definition = {}

    class SmartAmbientLightFrontRight4Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2847
        value_definition = {}

    class SmartAmbientLightFrontRight5Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2854
        value_definition = {}

    class SmartAmbientLightFrontRight5Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2863
        value_definition = {}

    class SmartAmbientLightFrontRight5Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2871
        value_definition = {}

    class SmartAmbientLightFrontRight5Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2879
        value_definition = {}

    class SmartAmbientLightFrontRight6Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2886
        value_definition = {}

    class SmartAmbientLightFrontRight6Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2895
        value_definition = {}

    class SmartAmbientLightFrontRight6Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2903
        value_definition = {}

    class SmartAmbientLightFrontRight6Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2911
        value_definition = {}

    class SmartAmbientLightFrontRight7Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2918
        value_definition = {}

    class SmartAmbientLightFrontRight7Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2927
        value_definition = {}

    class SmartAmbientLightFrontRight7Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2935
        value_definition = {}

    class SmartAmbientLightFrontRight7Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2943
        value_definition = {}

    class SmartAmbientLightFrontRight8Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2950
        value_definition = {}

    class SmartAmbientLightFrontRight8Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2959
        value_definition = {}

    class SmartAmbientLightFrontRight8Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2967
        value_definition = {}

    class SmartAmbientLightFrontRight8Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2975
        value_definition = {}

    class SmartAmbientLightFrontRight9Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 2982
        value_definition = {}

    class SmartAmbientLightFrontRight9Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2991
        value_definition = {}

    class SmartAmbientLightFrontRight9Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 2999
        value_definition = {}

    class SmartAmbientLightFrontRight9Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3007
        value_definition = {}

    class SmartAmbientLightFrontRight10Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3014
        value_definition = {}

    class SmartAmbientLightFrontRight10Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3023
        value_definition = {}

    class SmartAmbientLightFrontRight10Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3031
        value_definition = {}

    class SmartAmbientLightFrontRight10Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3039
        value_definition = {}

    class SmartAmbientLightFrontRight11Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3046
        value_definition = {}

    class SmartAmbientLightFrontRight11Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3055
        value_definition = {}

    class SmartAmbientLightFrontRight11Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3063
        value_definition = {}

    class SmartAmbientLightFrontRight11Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3071
        value_definition = {}

    class SmartAmbientLightFrontRight12Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3078
        value_definition = {}

    class SmartAmbientLightFrontRight12Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3087
        value_definition = {}

    class SmartAmbientLightFrontRight12Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3095
        value_definition = {}

    class SmartAmbientLightFrontRight12Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3103
        value_definition = {}

    class SmartAmbientLightFrontRight13Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3110
        value_definition = {}

    class SmartAmbientLightFrontRight13Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3119
        value_definition = {}

    class SmartAmbientLightFrontRight13Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3127
        value_definition = {}

    class SmartAmbientLightFrontRight13Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3135
        value_definition = {}

    class SmartAmbientLightFrontRight14Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3142
        value_definition = {}

    class SmartAmbientLightFrontRight14Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3151
        value_definition = {}

    class SmartAmbientLightFrontRight14Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3159
        value_definition = {}

    class SmartAmbientLightFrontRight14Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3167
        value_definition = {}

    class SmartAmbientLightFrontRight15Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3174
        value_definition = {}

    class SmartAmbientLightFrontRight15Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3183
        value_definition = {}

    class SmartAmbientLightFrontRight15Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3191
        value_definition = {}

    class SmartAmbientLightFrontRight15Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3199
        value_definition = {}

    class SmartAmbientLightFrontRight16Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3206
        value_definition = {}

    class SmartAmbientLightFrontRight16Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3215
        value_definition = {}

    class SmartAmbientLightFrontRight16Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3223
        value_definition = {}

    class SmartAmbientLightFrontRight16Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3231
        value_definition = {}

    class SmartAmbientLightFrontRight17Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3238
        value_definition = {}

    class SmartAmbientLightFrontRight17Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3247
        value_definition = {}

    class SmartAmbientLightFrontRight17Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3255
        value_definition = {}

    class SmartAmbientLightFrontRight17Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3263
        value_definition = {}

    class SmartAmbientLightFrontRight18Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3270
        value_definition = {}

    class SmartAmbientLightFrontRight18Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3279
        value_definition = {}

    class SmartAmbientLightFrontRight18Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3287
        value_definition = {}

    class SmartAmbientLightFrontRight18Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3295
        value_definition = {}

    class SmartAmbientLightFrontRight19Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3302
        value_definition = {}

    class SmartAmbientLightFrontRight19Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3311
        value_definition = {}

    class SmartAmbientLightFrontRight19Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3319
        value_definition = {}

    class SmartAmbientLightFrontRight19Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3327
        value_definition = {}

    class SmartAmbientLightFrontRight20Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3334
        value_definition = {}

    class SmartAmbientLightFrontRight20Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3343
        value_definition = {}

    class SmartAmbientLightFrontRight20Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3351
        value_definition = {}

    class SmartAmbientLightFrontRight20Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3359
        value_definition = {}

    class SmartAmbientLightFrontRight21Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3366
        value_definition = {}

    class SmartAmbientLightFrontRight21Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3375
        value_definition = {}

    class SmartAmbientLightFrontRight21Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3383
        value_definition = {}

    class SmartAmbientLightFrontRight21Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3391
        value_definition = {}

    class SmartAmbientLightFrontRight22Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3398
        value_definition = {}

    class SmartAmbientLightFrontRight22Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3407
        value_definition = {}

    class SmartAmbientLightFrontRight22Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3415
        value_definition = {}

    class SmartAmbientLightFrontRight22Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3423
        value_definition = {}

    class SmartAmbientLightFrontRight23Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3430
        value_definition = {}

    class SmartAmbientLightFrontRight23Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3439
        value_definition = {}

    class SmartAmbientLightFrontRight23Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3447
        value_definition = {}

    class SmartAmbientLightFrontRight23Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3455
        value_definition = {}

    class SmartAmbientLightFrontRight24Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3462
        value_definition = {}

    class SmartAmbientLightFrontRight24Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3471
        value_definition = {}

    class SmartAmbientLightFrontRight24Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3479
        value_definition = {}

    class SmartAmbientLightFrontRight24Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3487
        value_definition = {}

    class SmartAmbientLightFrontRight25Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3494
        value_definition = {}

    class SmartAmbientLightFrontRight25Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3503
        value_definition = {}

    class SmartAmbientLightFrontRight25Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3511
        value_definition = {}

    class SmartAmbientLightFrontRight25Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3519
        value_definition = {}

    class SmartAmbientLightFrontRight26Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3526
        value_definition = {}

    class SmartAmbientLightFrontRight26Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3535
        value_definition = {}

    class SmartAmbientLightFrontRight26Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3543
        value_definition = {}

    class SmartAmbientLightFrontRight26Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3551
        value_definition = {}

    class SmartAmbientLightFrontRight27Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3558
        value_definition = {}

    class SmartAmbientLightFrontRight27Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3567
        value_definition = {}

    class SmartAmbientLightFrontRight27Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3575
        value_definition = {}

    class SmartAmbientLightFrontRight27Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3583
        value_definition = {}

    class SmartAmbientLightFrontRight28Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3590
        value_definition = {}

    class SmartAmbientLightFrontRight28Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3599
        value_definition = {}

    class SmartAmbientLightFrontRight28Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3607
        value_definition = {}

    class SmartAmbientLightFrontRight28Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3615
        value_definition = {}

    class SmartAmbientLightFrontRight29Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3622
        value_definition = {}

    class SmartAmbientLightFrontRight29Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3631
        value_definition = {}

    class SmartAmbientLightFrontRight29Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3639
        value_definition = {}

    class SmartAmbientLightFrontRight29Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3647
        value_definition = {}

    class SmartAmbientLightFrontRight30Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3654
        value_definition = {}

    class SmartAmbientLightFrontRight30Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3663
        value_definition = {}

    class SmartAmbientLightFrontRight30Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3671
        value_definition = {}

    class SmartAmbientLightFrontRight30Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3679
        value_definition = {}

    class SmartAmbientLightFrontRight31Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3686
        value_definition = {}

    class SmartAmbientLightFrontRight31Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3695
        value_definition = {}

    class SmartAmbientLightFrontRight31Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3703
        value_definition = {}

    class SmartAmbientLightFrontRight31Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3711
        value_definition = {}

    class SmartAmbientLightFrontRight32Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3718
        value_definition = {}

    class SmartAmbientLightFrontRight32Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3727
        value_definition = {}

    class SmartAmbientLightFrontRight32Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3735
        value_definition = {}

    class SmartAmbientLightFrontRight32Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3743
        value_definition = {}

    class SmartAmbientLightFrontRight33Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3750
        value_definition = {}

    class SmartAmbientLightFrontRight33Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3759
        value_definition = {}

    class SmartAmbientLightFrontRight33Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3767
        value_definition = {}

    class SmartAmbientLightFrontRight33Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3775
        value_definition = {}

    class SmartAmbientLightFrontRight34Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3782
        value_definition = {}

    class SmartAmbientLightFrontRight34Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3791
        value_definition = {}

    class SmartAmbientLightFrontRight34Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3799
        value_definition = {}

    class SmartAmbientLightFrontRight34Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3807
        value_definition = {}

    class SmartAmbientLightFrontRight35Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3814
        value_definition = {}

    class SmartAmbientLightFrontRight35Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3823
        value_definition = {}

    class SmartAmbientLightFrontRight35Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3831
        value_definition = {}

    class SmartAmbientLightFrontRight35Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3839
        value_definition = {}

    class SmartAmbientLightFrontLeft0Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3846
        value_definition = {}

    class SmartAmbientLightFrontLeft0Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3855
        value_definition = {}

    class SmartAmbientLightFrontLeft0Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3863
        value_definition = {}

    class SmartAmbientLightFrontLeft0Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3871
        value_definition = {}

    class SmartAmbientLightFrontLeft1Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3878
        value_definition = {}

    class SmartAmbientLightFrontLeft1Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3887
        value_definition = {}

    class SmartAmbientLightFrontLeft1Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3895
        value_definition = {}

    class SmartAmbientLightFrontLeft1Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3903
        value_definition = {}

    class SmartAmbientLightFrontLeft2Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3910
        value_definition = {}

    class SmartAmbientLightFrontLeft2Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3919
        value_definition = {}

    class SmartAmbientLightFrontLeft2Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3927
        value_definition = {}

    class SmartAmbientLightFrontLeft2Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3935
        value_definition = {}

    class SmartAmbientLightFrontLeft3Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3942
        value_definition = {}

    class SmartAmbientLightFrontLeft3Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3951
        value_definition = {}

    class SmartAmbientLightFrontLeft3Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3959
        value_definition = {}

    class SmartAmbientLightFrontLeft3Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3967
        value_definition = {}

    class SmartAmbientLightFrontLeft4Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 3974
        value_definition = {}

    class SmartAmbientLightFrontLeft4Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3983
        value_definition = {}

    class SmartAmbientLightFrontLeft4Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3991
        value_definition = {}

    class SmartAmbientLightFrontLeft4Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 3999
        value_definition = {}

    class SmartAmbientLightFrontLeft5Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4006
        value_definition = {}

    class SmartAmbientLightFrontLeft5Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4015
        value_definition = {}

    class SmartAmbientLightFrontLeft5Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4023
        value_definition = {}

    class SmartAmbientLightFrontLeft5Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4031
        value_definition = {}

    class SmartAmbientLightFrontLeft6Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4038
        value_definition = {}

    class SmartAmbientLightFrontLeft6Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4047
        value_definition = {}

    class SmartAmbientLightFrontLeft6Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4055
        value_definition = {}

    class SmartAmbientLightFrontLeft6Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4063
        value_definition = {}

    class SmartAmbientLightFrontLeft7Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4070
        value_definition = {}

    class SmartAmbientLightFrontLeft7Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4079
        value_definition = {}

    class SmartAmbientLightFrontLeft7Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4087
        value_definition = {}

    class SmartAmbientLightFrontLeft7Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4095
        value_definition = {}

    class SmartAmbientLightFrontLeft8Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4102
        value_definition = {}

    class SmartAmbientLightFrontLeft8Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4111
        value_definition = {}

    class SmartAmbientLightFrontLeft8Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4119
        value_definition = {}

    class SmartAmbientLightFrontLeft8Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4127
        value_definition = {}

    class SmartAmbientLightFrontLeft9Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4134
        value_definition = {}

    class SmartAmbientLightFrontLeft9Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4143
        value_definition = {}

    class SmartAmbientLightFrontLeft9Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4151
        value_definition = {}

    class SmartAmbientLightFrontLeft9Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4159
        value_definition = {}

    class SmartAmbientLightFrontLeft10Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4166
        value_definition = {}

    class SmartAmbientLightFrontLeft10Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4175
        value_definition = {}

    class SmartAmbientLightFrontLeft10Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4183
        value_definition = {}

    class SmartAmbientLightFrontLeft10Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4191
        value_definition = {}

    class SmartAmbientLightFrontLeft11Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4198
        value_definition = {}

    class SmartAmbientLightFrontLeft11Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4207
        value_definition = {}

    class SmartAmbientLightFrontLeft11Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4215
        value_definition = {}

    class SmartAmbientLightFrontLeft11Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4223
        value_definition = {}

    class SmartAmbientLightFrontLeft12Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4230
        value_definition = {}

    class SmartAmbientLightFrontLeft12Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4239
        value_definition = {}

    class SmartAmbientLightFrontLeft12Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4247
        value_definition = {}

    class SmartAmbientLightFrontLeft12Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4255
        value_definition = {}

    class SmartAmbientLightFrontLeft13Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4262
        value_definition = {}

    class SmartAmbientLightFrontLeft13Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4271
        value_definition = {}

    class SmartAmbientLightFrontLeft13Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4279
        value_definition = {}

    class SmartAmbientLightFrontLeft13Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4287
        value_definition = {}

    class SmartAmbientLightFrontLeft14Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4294
        value_definition = {}

    class SmartAmbientLightFrontLeft14Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4303
        value_definition = {}

    class SmartAmbientLightFrontLeft14Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4311
        value_definition = {}

    class SmartAmbientLightFrontLeft14Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4319
        value_definition = {}

    class SmartAmbientLightFrontLeft15Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4326
        value_definition = {}

    class SmartAmbientLightFrontLeft15Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4335
        value_definition = {}

    class SmartAmbientLightFrontLeft15Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4343
        value_definition = {}

    class SmartAmbientLightFrontLeft15Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4351
        value_definition = {}

    class SmartAmbientLightFrontLeft16Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4358
        value_definition = {}

    class SmartAmbientLightFrontLeft16Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4367
        value_definition = {}

    class SmartAmbientLightFrontLeft16Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4375
        value_definition = {}

    class SmartAmbientLightFrontLeft16Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4383
        value_definition = {}

    class SmartAmbientLightFrontLeft17Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4390
        value_definition = {}

    class SmartAmbientLightFrontLeft17Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4399
        value_definition = {}

    class SmartAmbientLightFrontLeft17Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4407
        value_definition = {}

    class SmartAmbientLightFrontLeft17Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4415
        value_definition = {}

    class SmartAmbientLightFrontLeft18Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4422
        value_definition = {}

    class SmartAmbientLightFrontLeft18Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4431
        value_definition = {}

    class SmartAmbientLightFrontLeft18Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4439
        value_definition = {}

    class SmartAmbientLightFrontLeft18Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4447
        value_definition = {}

    class SmartAmbientLightFrontLeft19Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4454
        value_definition = {}

    class SmartAmbientLightFrontLeft19Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4463
        value_definition = {}

    class SmartAmbientLightFrontLeft19Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4471
        value_definition = {}

    class SmartAmbientLightFrontLeft19Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4479
        value_definition = {}

    class SmartAmbientLightFrontLeft20Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4486
        value_definition = {}

    class SmartAmbientLightFrontLeft20Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4495
        value_definition = {}

    class SmartAmbientLightFrontLeft20Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4503
        value_definition = {}

    class SmartAmbientLightFrontLeft20Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4511
        value_definition = {}

    class SmartAmbientLightFrontLeft21Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4518
        value_definition = {}

    class SmartAmbientLightFrontLeft21Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4527
        value_definition = {}

    class SmartAmbientLightFrontLeft21Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4535
        value_definition = {}

    class SmartAmbientLightFrontLeft21Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4543
        value_definition = {}

    class SmartAmbientLightFrontLeft22Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4550
        value_definition = {}

    class SmartAmbientLightFrontLeft22Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4559
        value_definition = {}

    class SmartAmbientLightFrontLeft22Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4567
        value_definition = {}

    class SmartAmbientLightFrontLeft22Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4575
        value_definition = {}

    class SmartAmbientLightFrontLeft23Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4582
        value_definition = {}

    class SmartAmbientLightFrontLeft23Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4591
        value_definition = {}

    class SmartAmbientLightFrontLeft23Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4599
        value_definition = {}

    class SmartAmbientLightFrontLeft23Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4607
        value_definition = {}

    class SmartAmbientLightFrontLeft24Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4614
        value_definition = {}

    class SmartAmbientLightFrontLeft24Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4623
        value_definition = {}

    class SmartAmbientLightFrontLeft24Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4631
        value_definition = {}

    class SmartAmbientLightFrontLeft24Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4639
        value_definition = {}

    class SmartAmbientLightFrontLeft25Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4646
        value_definition = {}

    class SmartAmbientLightFrontLeft25Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4655
        value_definition = {}

    class SmartAmbientLightFrontLeft25Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4663
        value_definition = {}

    class SmartAmbientLightFrontLeft25Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4671
        value_definition = {}

    class SmartAmbientLightFrontLeft26Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4678
        value_definition = {}

    class SmartAmbientLightFrontLeft26Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4687
        value_definition = {}

    class SmartAmbientLightFrontLeft26Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4695
        value_definition = {}

    class SmartAmbientLightFrontLeft26Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4703
        value_definition = {}

    class SmartAmbientLightFrontLeft27Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4710
        value_definition = {}

    class SmartAmbientLightFrontLeft27Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4719
        value_definition = {}

    class SmartAmbientLightFrontLeft27Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4727
        value_definition = {}

    class SmartAmbientLightFrontLeft27Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4735
        value_definition = {}

    class SmartAmbientLightFrontLeft28Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4742
        value_definition = {}

    class SmartAmbientLightFrontLeft28Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4751
        value_definition = {}

    class SmartAmbientLightFrontLeft28Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4759
        value_definition = {}

    class SmartAmbientLightFrontLeft28Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4767
        value_definition = {}

    class SmartAmbientLightFrontLeft29Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4774
        value_definition = {}

    class SmartAmbientLightFrontLeft29Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4783
        value_definition = {}

    class SmartAmbientLightFrontLeft29Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4791
        value_definition = {}

    class SmartAmbientLightFrontLeft29Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4799
        value_definition = {}

    class SmartAmbientLightFrontLeft30Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4806
        value_definition = {}

    class SmartAmbientLightFrontLeft30Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4815
        value_definition = {}

    class SmartAmbientLightFrontLeft30Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4823
        value_definition = {}

    class SmartAmbientLightFrontLeft30Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4831
        value_definition = {}

    class SmartAmbientLightFrontLeft31Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4838
        value_definition = {}

    class SmartAmbientLightFrontLeft31Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4847
        value_definition = {}

    class SmartAmbientLightFrontLeft31Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4855
        value_definition = {}

    class SmartAmbientLightFrontLeft31Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4863
        value_definition = {}

    class SmartAmbientLightFrontLeft32Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4870
        value_definition = {}

    class SmartAmbientLightFrontLeft32Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4879
        value_definition = {}

    class SmartAmbientLightFrontLeft32Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4887
        value_definition = {}

    class SmartAmbientLightFrontLeft32Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4895
        value_definition = {}

    class SmartAmbientLightFrontLeft33Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4902
        value_definition = {}

    class SmartAmbientLightFrontLeft33Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4911
        value_definition = {}

    class SmartAmbientLightFrontLeft33Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4919
        value_definition = {}

    class SmartAmbientLightFrontLeft33Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4927
        value_definition = {}

    class SmartAmbientLightFrontLeft34Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4934
        value_definition = {}

    class SmartAmbientLightFrontLeft34Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4943
        value_definition = {}

    class SmartAmbientLightFrontLeft34Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4951
        value_definition = {}

    class SmartAmbientLightFrontLeft34Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4959
        value_definition = {}

    class SmartAmbientLightFrontLeft35Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4966
        value_definition = {}

    class SmartAmbientLightFrontLeft35Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4975
        value_definition = {}

    class SmartAmbientLightFrontLeft35Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4983
        value_definition = {}

    class SmartAmbientLightFrontLeft35Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 4991
        value_definition = {}

    class SmartAmbientLightRearRight0Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 4998
        value_definition = {}

    class SmartAmbientLightRearRight0Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5007
        value_definition = {}

    class SmartAmbientLightRearRight0Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5015
        value_definition = {}

    class SmartAmbientLightRearRight0Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5023
        value_definition = {}

    class SmartAmbientLightRearRight1Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5030
        value_definition = {}

    class SmartAmbientLightRearRight1Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5039
        value_definition = {}

    class SmartAmbientLightRearRight1Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5047
        value_definition = {}

    class SmartAmbientLightRearRight1Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5055
        value_definition = {}

    class SmartAmbientLightRearRight2Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5062
        value_definition = {}

    class SmartAmbientLightRearRight2Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5071
        value_definition = {}

    class SmartAmbientLightRearRight2Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5079
        value_definition = {}

    class SmartAmbientLightRearRight2Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5087
        value_definition = {}

    class SmartAmbientLightRearRight3Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5094
        value_definition = {}

    class SmartAmbientLightRearRight3Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5103
        value_definition = {}

    class SmartAmbientLightRearRight3Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5111
        value_definition = {}

    class SmartAmbientLightRearRight3Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5119
        value_definition = {}

    class SmartAmbientLightRearRight4Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5126
        value_definition = {}

    class SmartAmbientLightRearRight4Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5135
        value_definition = {}

    class SmartAmbientLightRearRight4Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5143
        value_definition = {}

    class SmartAmbientLightRearRight4Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5151
        value_definition = {}

    class SmartAmbientLightRearRight5Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5158
        value_definition = {}

    class SmartAmbientLightRearRight5Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5167
        value_definition = {}

    class SmartAmbientLightRearRight5Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5175
        value_definition = {}

    class SmartAmbientLightRearRight5Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5183
        value_definition = {}

    class SmartAmbientLightRearRight6Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5190
        value_definition = {}

    class SmartAmbientLightRearRight6Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5199
        value_definition = {}

    class SmartAmbientLightRearRight6Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5207
        value_definition = {}

    class SmartAmbientLightRearRight6Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5215
        value_definition = {}

    class SmartAmbientLightRearRight7Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5222
        value_definition = {}

    class SmartAmbientLightRearRight7Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5231
        value_definition = {}

    class SmartAmbientLightRearRight7Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5239
        value_definition = {}

    class SmartAmbientLightRearRight7Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5247
        value_definition = {}

    class SmartAmbientLightRearRight8Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5254
        value_definition = {}

    class SmartAmbientLightRearRight8Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5263
        value_definition = {}

    class SmartAmbientLightRearRight8Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5271
        value_definition = {}

    class SmartAmbientLightRearRight8Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5279
        value_definition = {}

    class SmartAmbientLightRearRight9Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5286
        value_definition = {}

    class SmartAmbientLightRearRight9Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5295
        value_definition = {}

    class SmartAmbientLightRearRight9Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5303
        value_definition = {}

    class SmartAmbientLightRearRight9Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5311
        value_definition = {}

    class SmartAmbientLightRearRight10Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5318
        value_definition = {}

    class SmartAmbientLightRearRight10Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5327
        value_definition = {}

    class SmartAmbientLightRearRight10Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5335
        value_definition = {}

    class SmartAmbientLightRearRight10Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5343
        value_definition = {}

    class SmartAmbientLightRearRight11Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5350
        value_definition = {}

    class SmartAmbientLightRearRight11Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5359
        value_definition = {}

    class SmartAmbientLightRearRight11Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5367
        value_definition = {}

    class SmartAmbientLightRearRight11Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5375
        value_definition = {}

    class SmartAmbientLightRearRight12Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5382
        value_definition = {}

    class SmartAmbientLightRearRight12Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5391
        value_definition = {}

    class SmartAmbientLightRearRight12Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5399
        value_definition = {}

    class SmartAmbientLightRearRight12Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5407
        value_definition = {}

    class SmartAmbientLightRearRight13Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5414
        value_definition = {}

    class SmartAmbientLightRearRight13Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5423
        value_definition = {}

    class SmartAmbientLightRearRight13Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5431
        value_definition = {}

    class SmartAmbientLightRearRight13Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5439
        value_definition = {}

    class SmartAmbientLightRearRight14Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5446
        value_definition = {}

    class SmartAmbientLightRearRight14Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5455
        value_definition = {}

    class SmartAmbientLightRearRight14Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5463
        value_definition = {}

    class SmartAmbientLightRearRight14Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5471
        value_definition = {}

    class SmartAmbientLightRearRight15Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5478
        value_definition = {}

    class SmartAmbientLightRearRight15Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5487
        value_definition = {}

    class SmartAmbientLightRearRight15Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5495
        value_definition = {}

    class SmartAmbientLightRearRight15Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5503
        value_definition = {}

    class SmartAmbientLightRearRight16Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5510
        value_definition = {}

    class SmartAmbientLightRearRight16Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5519
        value_definition = {}

    class SmartAmbientLightRearRight16Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5527
        value_definition = {}

    class SmartAmbientLightRearRight16Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5535
        value_definition = {}

    class SmartAmbientLightRearRight17Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5542
        value_definition = {}

    class SmartAmbientLightRearRight17Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5551
        value_definition = {}

    class SmartAmbientLightRearRight17Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5559
        value_definition = {}

    class SmartAmbientLightRearRight17Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5567
        value_definition = {}

    class SmartAmbientLightRearRight18Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5574
        value_definition = {}

    class SmartAmbientLightRearRight18Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5583
        value_definition = {}

    class SmartAmbientLightRearRight18Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5591
        value_definition = {}

    class SmartAmbientLightRearRight18Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5599
        value_definition = {}

    class SmartAmbientLightRearRight19Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5606
        value_definition = {}

    class SmartAmbientLightRearRight19Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5615
        value_definition = {}

    class SmartAmbientLightRearRight19Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5623
        value_definition = {}

    class SmartAmbientLightRearRight19Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5631
        value_definition = {}

    class SmartAmbientLightRearRight20Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5638
        value_definition = {}

    class SmartAmbientLightRearRight20Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5647
        value_definition = {}

    class SmartAmbientLightRearRight20Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5655
        value_definition = {}

    class SmartAmbientLightRearRight20Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5663
        value_definition = {}

    class SmartAmbientLightRearRight21Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5670
        value_definition = {}

    class SmartAmbientLightRearRight21Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5679
        value_definition = {}

    class SmartAmbientLightRearRight21Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5687
        value_definition = {}

    class SmartAmbientLightRearRight21Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5695
        value_definition = {}

    class SmartAmbientLightRearRight22Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5702
        value_definition = {}

    class SmartAmbientLightRearRight22Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5711
        value_definition = {}

    class SmartAmbientLightRearRight22Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5719
        value_definition = {}

    class SmartAmbientLightRearRight22Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5727
        value_definition = {}

    class SmartAmbientLightRearRight23Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5734
        value_definition = {}

    class SmartAmbientLightRearRight23Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5743
        value_definition = {}

    class SmartAmbientLightRearRight23Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5751
        value_definition = {}

    class SmartAmbientLightRearRight23Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5759
        value_definition = {}

    class SmartAmbientLightRearRight24Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5766
        value_definition = {}

    class SmartAmbientLightRearRight24Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5775
        value_definition = {}

    class SmartAmbientLightRearRight24Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5783
        value_definition = {}

    class SmartAmbientLightRearRight24Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5791
        value_definition = {}

    class SmartAmbientLightRearRight25Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5798
        value_definition = {}

    class SmartAmbientLightRearRight25Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5807
        value_definition = {}

    class SmartAmbientLightRearRight25Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5815
        value_definition = {}

    class SmartAmbientLightRearRight25Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5823
        value_definition = {}

    class SmartAmbientLightRearRight26Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5830
        value_definition = {}

    class SmartAmbientLightRearRight26Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5839
        value_definition = {}

    class SmartAmbientLightRearRight26Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5847
        value_definition = {}

    class SmartAmbientLightRearRight26Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5855
        value_definition = {}

    class SmartAmbientLightRearRight27Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5862
        value_definition = {}

    class SmartAmbientLightRearRight27Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5871
        value_definition = {}

    class SmartAmbientLightRearRight27Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5879
        value_definition = {}

    class SmartAmbientLightRearRight27Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5887
        value_definition = {}

    class SmartAmbientLightRearRight28Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5894
        value_definition = {}

    class SmartAmbientLightRearRight28Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5903
        value_definition = {}

    class SmartAmbientLightRearRight28Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5911
        value_definition = {}

    class SmartAmbientLightRearRight28Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5919
        value_definition = {}

    class SmartAmbientLightRearRight29Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5926
        value_definition = {}

    class SmartAmbientLightRearRight29Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5935
        value_definition = {}

    class SmartAmbientLightRearRight29Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5943
        value_definition = {}

    class SmartAmbientLightRearRight29Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5951
        value_definition = {}

    class SmartAmbientLightRearLeft0Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5958
        value_definition = {}

    class SmartAmbientLightRearLeft0Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5967
        value_definition = {}

    class SmartAmbientLightRearLeft0Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5975
        value_definition = {}

    class SmartAmbientLightRearLeft0Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5983
        value_definition = {}

    class SmartAmbientLightRearLeft1Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 5990
        value_definition = {}

    class SmartAmbientLightRearLeft1Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 5999
        value_definition = {}

    class SmartAmbientLightRearLeft1Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6007
        value_definition = {}

    class SmartAmbientLightRearLeft1Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6015
        value_definition = {}

    class SmartAmbientLightRearLeft2Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6022
        value_definition = {}

    class SmartAmbientLightRearLeft2Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6031
        value_definition = {}

    class SmartAmbientLightRearLeft2Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6039
        value_definition = {}

    class SmartAmbientLightRearLeft2Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6047
        value_definition = {}

    class SmartAmbientLightRearLeft3Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6054
        value_definition = {}

    class SmartAmbientLightRearLeft3Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6063
        value_definition = {}

    class SmartAmbientLightRearLeft3Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6071
        value_definition = {}

    class SmartAmbientLightRearLeft3Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6079
        value_definition = {}

    class SmartAmbientLightRearLeft4Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6086
        value_definition = {}

    class SmartAmbientLightRearLeft4Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6095
        value_definition = {}

    class SmartAmbientLightRearLeft4Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6103
        value_definition = {}

    class SmartAmbientLightRearLeft4Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6111
        value_definition = {}

    class SmartAmbientLightRearLeft5Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6118
        value_definition = {}

    class SmartAmbientLightRearLeft5Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6127
        value_definition = {}

    class SmartAmbientLightRearLeft5Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6135
        value_definition = {}

    class SmartAmbientLightRearLeft5Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6143
        value_definition = {}

    class SmartAmbientLightRearLeft6Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6150
        value_definition = {}

    class SmartAmbientLightRearLeft6Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6159
        value_definition = {}

    class SmartAmbientLightRearLeft6Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6167
        value_definition = {}

    class SmartAmbientLightRearLeft6Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6175
        value_definition = {}

    class SmartAmbientLightRearLeft7Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6182
        value_definition = {}

    class SmartAmbientLightRearLeft7Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6191
        value_definition = {}

    class SmartAmbientLightRearLeft7Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6199
        value_definition = {}

    class SmartAmbientLightRearLeft7Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6207
        value_definition = {}

    class SmartAmbientLightRearLeft8Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6214
        value_definition = {}

    class SmartAmbientLightRearLeft8Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6223
        value_definition = {}

    class SmartAmbientLightRearLeft8Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6231
        value_definition = {}

    class SmartAmbientLightRearLeft8Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6239
        value_definition = {}

    class SmartAmbientLightRearLeft9Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6246
        value_definition = {}

    class SmartAmbientLightRearLeft9Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6255
        value_definition = {}

    class SmartAmbientLightRearLeft9Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6263
        value_definition = {}

    class SmartAmbientLightRearLeft9Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6271
        value_definition = {}

    class SmartAmbientLightRearLeft10Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6278
        value_definition = {}

    class SmartAmbientLightRearLeft10Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6287
        value_definition = {}

    class SmartAmbientLightRearLeft10Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6295
        value_definition = {}

    class SmartAmbientLightRearLeft10Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6303
        value_definition = {}

    class SmartAmbientLightRearLeft11Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6310
        value_definition = {}

    class SmartAmbientLightRearLeft11Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6319
        value_definition = {}

    class SmartAmbientLightRearLeft11Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6327
        value_definition = {}

    class SmartAmbientLightRearLeft11Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6335
        value_definition = {}

    class SmartAmbientLightRearLeft12Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6342
        value_definition = {}

    class SmartAmbientLightRearLeft12Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6351
        value_definition = {}

    class SmartAmbientLightRearLeft12Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6359
        value_definition = {}

    class SmartAmbientLightRearLeft12Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6367
        value_definition = {}

    class SmartAmbientLightRearLeft13Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6374
        value_definition = {}

    class SmartAmbientLightRearLeft13Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6383
        value_definition = {}

    class SmartAmbientLightRearLeft13Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6391
        value_definition = {}

    class SmartAmbientLightRearLeft13Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6399
        value_definition = {}

    class SmartAmbientLightRearLeft14Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6406
        value_definition = {}

    class SmartAmbientLightRearLeft14Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6415
        value_definition = {}

    class SmartAmbientLightRearLeft14Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6423
        value_definition = {}

    class SmartAmbientLightRearLeft14Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6431
        value_definition = {}

    class SmartAmbientLightRearLeft15Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6438
        value_definition = {}

    class SmartAmbientLightRearLeft15Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6447
        value_definition = {}

    class SmartAmbientLightRearLeft15Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6455
        value_definition = {}

    class SmartAmbientLightRearLeft15Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6463
        value_definition = {}

    class SmartAmbientLightRearLeft16Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6470
        value_definition = {}

    class SmartAmbientLightRearLeft16Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6479
        value_definition = {}

    class SmartAmbientLightRearLeft16Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6487
        value_definition = {}

    class SmartAmbientLightRearLeft16Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6495
        value_definition = {}

    class SmartAmbientLightRearLeft17Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6502
        value_definition = {}

    class SmartAmbientLightRearLeft17Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6511
        value_definition = {}

    class SmartAmbientLightRearLeft17Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6519
        value_definition = {}

    class SmartAmbientLightRearLeft17Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6527
        value_definition = {}

    class SmartAmbientLightRearLeft18Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6534
        value_definition = {}

    class SmartAmbientLightRearLeft18Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6543
        value_definition = {}

    class SmartAmbientLightRearLeft18Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6551
        value_definition = {}

    class SmartAmbientLightRearLeft18Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6559
        value_definition = {}

    class SmartAmbientLightRearLeft19Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6566
        value_definition = {}

    class SmartAmbientLightRearLeft19Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6575
        value_definition = {}

    class SmartAmbientLightRearLeft19Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6583
        value_definition = {}

    class SmartAmbientLightRearLeft19Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6591
        value_definition = {}

    class SmartAmbientLightRearLeft20Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6598
        value_definition = {}

    class SmartAmbientLightRearLeft20Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6607
        value_definition = {}

    class SmartAmbientLightRearLeft20Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6615
        value_definition = {}

    class SmartAmbientLightRearLeft20Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6623
        value_definition = {}

    class SmartAmbientLightRearLeft21Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6630
        value_definition = {}

    class SmartAmbientLightRearLeft21Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6639
        value_definition = {}

    class SmartAmbientLightRearLeft21Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6647
        value_definition = {}

    class SmartAmbientLightRearLeft21Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6655
        value_definition = {}

    class SmartAmbientLightRearLeft22Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6662
        value_definition = {}

    class SmartAmbientLightRearLeft22Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6671
        value_definition = {}

    class SmartAmbientLightRearLeft22Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6679
        value_definition = {}

    class SmartAmbientLightRearLeft22Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6687
        value_definition = {}

    class SmartAmbientLightRearLeft23Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6694
        value_definition = {}

    class SmartAmbientLightRearLeft23Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6703
        value_definition = {}

    class SmartAmbientLightRearLeft23Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6711
        value_definition = {}

    class SmartAmbientLightRearLeft23Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6719
        value_definition = {}

    class SmartAmbientLightRearLeft24Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6726
        value_definition = {}

    class SmartAmbientLightRearLeft24Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6735
        value_definition = {}

    class SmartAmbientLightRearLeft24Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6743
        value_definition = {}

    class SmartAmbientLightRearLeft24Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6751
        value_definition = {}

    class SmartAmbientLightRearLeft25Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6758
        value_definition = {}

    class SmartAmbientLightRearLeft25Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6767
        value_definition = {}

    class SmartAmbientLightRearLeft25Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6775
        value_definition = {}

    class SmartAmbientLightRearLeft25Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6783
        value_definition = {}

    class SmartAmbientLightRearLeft26Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6790
        value_definition = {}

    class SmartAmbientLightRearLeft26Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6799
        value_definition = {}

    class SmartAmbientLightRearLeft26Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6807
        value_definition = {}

    class SmartAmbientLightRearLeft26Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6815
        value_definition = {}

    class SmartAmbientLightRearLeft27Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6822
        value_definition = {}

    class SmartAmbientLightRearLeft27Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6831
        value_definition = {}

    class SmartAmbientLightRearLeft27Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6839
        value_definition = {}

    class SmartAmbientLightRearLeft27Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6847
        value_definition = {}

    class SmartAmbientLightRearLeft28Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6854
        value_definition = {}

    class SmartAmbientLightRearLeft28Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6863
        value_definition = {}

    class SmartAmbientLightRearLeft28Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6871
        value_definition = {}

    class SmartAmbientLightRearLeft28Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6879
        value_definition = {}

    class SmartAmbientLightRearLeft29Brightness:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 7
        start_position = 6886
        value_definition = {}

    class SmartAmbientLightRearLeft29Red:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6895
        value_definition = {}

    class SmartAmbientLightRearLeft29Green:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6903
        value_definition = {}

    class SmartAmbientLightRearLeft29Blue:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Smart氛围灯控制信号"
        signal_length = 8
        start_position = 6911
        value_definition = {}


class BGMIntEthPDU6252:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6252
    pdu_length_bytes = 44
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'OrdinaryAmbientLightFrontLeft': ['OrdinaryAmbientLightFrontLeftBrightness', 'OrdinaryAmbientLightFrontLeftRed', 'OrdinaryAmbientLightFrontLeftGreen', 'OrdinaryAmbientLightFrontLeftBlue'], 'OrdinaryAmbientLightFrontRight': ['OrdinaryAmbientLightFrontRightBrightness', 'OrdinaryAmbientLightFrontRightRed', 'OrdinaryAmbientLightFrontRightGreen', 'OrdinaryAmbientLightFrontRightBlue'], 'OrdinaryAmbientLightRearLeft': ['OrdinaryAmbientLightRearLeftBrightness', 'OrdinaryAmbientLightRearLeftRed', 'OrdinaryAmbientLightRearLeftGreen', 'OrdinaryAmbientLightRearLeftBlue'], 'OrdinaryAmbientLightRearRight': ['OrdinaryAmbientLightRearRightBrightness', 'OrdinaryAmbientLightRearRightRed', 'OrdinaryAmbientLightRearRightGreen', 'OrdinaryAmbientLightRearRightBlue'], 'OrdinaryAmbientLightCCRight': ['OrdinaryAmbientLightCCRightBrightness', 'OrdinaryAmbientLightCCRightRed', 'OrdinaryAmbientLightCCRightGreen', 'OrdinaryAmbientLightCCRightBlue'], 'OrdinaryAmbientLightCCLeft': ['OrdinaryAmbientLightCCLeftBrightness', 'OrdinaryAmbientLightCCLeftRed', 'OrdinaryAmbientLightCCLeftGreen', 'OrdinaryAmbientLightCCLeftBlue'], 'OrdinaryAmbientLightTweeterLeft': ['OrdinaryAmbientLightTweeterLeftBrightness', 'OrdinaryAmbientLightTweeterLeftRed', 'OrdinaryAmbientLightTweeterLeftGreen', 'OrdinaryAmbientLightTweeterLeftBlue'], 'OrdinaryAmbientLightTweeterRight': ['OrdinaryAmbientLightTweeterRightBrightness', 'OrdinaryAmbientLightTweeterRightRed', 'OrdinaryAmbientLightTweeterRightGreen', 'OrdinaryAmbientLightTweeterRightBlue'], 'OrdinaryAmbientLightCCMiddleRight': ['OrdinaryAmbientLightCCMiddleRightBrightness', 'OrdinaryAmbientLightCCMiddleRightRed', 'OrdinaryAmbientLightCCMiddleRightGreen', 'OrdinaryAmbientLightCCMiddleRightBlue'], 'OrdinaryAmbientLightCCMiddleLeft': ['OrdinaryAmbientLightCCMiddleLeftBrightness', 'OrdinaryAmbientLightCCMiddleLeftRed', 'OrdinaryAmbientLightCCMiddleLeftGreen', 'OrdinaryAmbientLightCCMiddleLeftBlue'], 'OrdinaryAmbientLightCCUnder': ['OrdinaryAmbientLightCCUnderBrightness', 'OrdinaryAmbientLightCCUnderRed', 'OrdinaryAmbientLightCCUnderGreen', 'OrdinaryAmbientLightCCUnderBlue']}

    class OrdinaryAmbientLightFrontLeftBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 7
        start_position = 6
        value_definition = {}

    class OrdinaryAmbientLightFrontLeftRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class OrdinaryAmbientLightFrontLeftGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class OrdinaryAmbientLightFrontLeftBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class OrdinaryAmbientLightFrontRightBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 7
        start_position = 38
        value_definition = {}

    class OrdinaryAmbientLightFrontRightRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class OrdinaryAmbientLightFrontRightGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class OrdinaryAmbientLightFrontRightBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class OrdinaryAmbientLightRearLeftBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 7
        start_position = 70
        value_definition = {}

    class OrdinaryAmbientLightRearLeftRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class OrdinaryAmbientLightRearLeftGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class OrdinaryAmbientLightRearLeftBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class OrdinaryAmbientLightRearRightBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 7
        start_position = 102
        value_definition = {}

    class OrdinaryAmbientLightRearRightRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class OrdinaryAmbientLightRearRightGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class OrdinaryAmbientLightRearRightBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class OrdinaryAmbientLightCCRightBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 7
        start_position = 134
        value_definition = {}

    class OrdinaryAmbientLightCCRightRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 143
        value_definition = {}

    class OrdinaryAmbientLightCCRightGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 151
        value_definition = {}

    class OrdinaryAmbientLightCCRightBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 159
        value_definition = {}

    class OrdinaryAmbientLightCCLeftBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 7
        start_position = 166
        value_definition = {}

    class OrdinaryAmbientLightCCLeftRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 175
        value_definition = {}

    class OrdinaryAmbientLightCCLeftGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 183
        value_definition = {}

    class OrdinaryAmbientLightCCLeftBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 191
        value_definition = {}

    class OrdinaryAmbientLightTweeterLeftBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 7
        start_position = 198
        value_definition = {}

    class OrdinaryAmbientLightTweeterLeftRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 207
        value_definition = {}

    class OrdinaryAmbientLightTweeterLeftGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 215
        value_definition = {}

    class OrdinaryAmbientLightTweeterLeftBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 223
        value_definition = {}

    class OrdinaryAmbientLightTweeterRightBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 7
        start_position = 230
        value_definition = {}

    class OrdinaryAmbientLightTweeterRightRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 239
        value_definition = {}

    class OrdinaryAmbientLightTweeterRightGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 247
        value_definition = {}

    class OrdinaryAmbientLightTweeterRightBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 255
        value_definition = {}

    class OrdinaryAmbientLightCCMiddleRightBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 7
        start_position = 262
        value_definition = {}

    class OrdinaryAmbientLightCCMiddleRightRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 271
        value_definition = {}

    class OrdinaryAmbientLightCCMiddleRightGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 279
        value_definition = {}

    class OrdinaryAmbientLightCCMiddleRightBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 287
        value_definition = {}

    class OrdinaryAmbientLightCCMiddleLeftBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 7
        start_position = 294
        value_definition = {}

    class OrdinaryAmbientLightCCMiddleLeftRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 303
        value_definition = {}

    class OrdinaryAmbientLightCCMiddleLeftGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 311
        value_definition = {}

    class OrdinaryAmbientLightCCMiddleLeftBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 319
        value_definition = {}

    class OrdinaryAmbientLightCCUnderBrightness:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 7
        start_position = 326
        value_definition = {}

    class OrdinaryAmbientLightCCUnderRed:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 335
        value_definition = {}

    class OrdinaryAmbientLightCCUnderGreen:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 343
        value_definition = {}

    class OrdinaryAmbientLightCCUnderBlue:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "Ordinary氛围灯控制信号"
        signal_length = 8
        start_position = 351
        value_definition = {}


class BGMIntEthPDU6301:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6301
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class RiseOrFallControl:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "可升降高音扬声器升降控制"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'RiseOrFallControl_stop', '0x1': 'RiseOrFallControl_Rise', '0x2': 'RiseOrFallControl_fall', '0x3': 'RiseOrFallControl_reserved'}


class BGMIntEthPDU6353:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6353
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class MobDevCenLockReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "RKE控制整车解闭锁"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'MobDevCenLockReq_NoRequest', '0x1': 'MobDevCenLockReq_Unlock', '0x2': 'MobDevCenLockReq_NormalLock', '0x3': 'MobDevCenLockReq_LockWithAllDoorClosed', '0x4': 'MobDevCenLockReq_Reserved1', '0x5': 'MobDevCenLockReq_Reserved2', '0x6': 'MobDevCenLockReq_Reserved3', '0x7': 'MobDevCenLockReq_Reserved4'}


class BGMIntEthPDU6354:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6354
    pdu_length_bytes = 4095
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DKDataDownLink:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        signal_description = "数字钥匙数据下行（RKE数据，长度可变）"
        signal_length = 32768
        start_position = 0
        value_definition = {}


class BGMIntEthPDU6355:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 6355
    pdu_length_bytes = 4095
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class DKDataUpLink:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        signal_description = "数字钥匙数据上行（RKE数据，长度可变）"
        signal_length = 32768
        start_position = 0
        value_definition = {}


class BGMIntEthPDU6356:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6356
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DstTrvldFromCDC:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "设置CDC备份的行驶里程"
        signal_length = 32
        start_position = 7
        value_definition = {}


class BGMIntEthPDU6357:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6357
    pdu_length_bytes = 4095
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class BLEVehDataUpdEth:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        signal_description = "设置蓝牙传输整车数据（长度可变）"
        signal_length = 32768
        start_position = 0
        value_definition = {}


class BGMIntEthPDU6358:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6358
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DKServiceSts:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "数字钥匙应用处理数据能力状态"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU6360:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6360
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetExhibitionModeReq:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "展车模式开启关闭设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU6361:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6361
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ProxyCarFindrHornLiReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "寻车请求"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'CarFindrHornLiReqFromTelm_NoReq', '0x1': 'CarFindrHornLiReqFromTelm_HornReq', '0x2': 'CarFindrHornLiReqFromTelm_LiReq', '0x3': 'CarFindrHornLiReqFromTelm_HornLiReq'}


class BGMIntEthPDU6362:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6362
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class PEKeySearchZoneSet:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "设置PE解锁时对应寻钥匙的区域"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'PEKeySearchZoneSet_AllExternalZone', '0x1': 'PEKeySearchZoneSet_DedicatedSideZone'}


class BGMIntEthPDU6363:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6363
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiAirVentDrvrLeSwtReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "驾驶侧左边出风口关闭请求"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU6364:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6364
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiAirVentPassLeSwtReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾侧左边出风口关闭请求"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU6365:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6365
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiAirVentDrvrRiSwtReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "驾驶侧右边出风口关闭请求"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU6366:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6366
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiAirVentPassRiSwtReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "副驾侧右边出风口关闭请求"
        signal_length = 1
        start_position = 0
        value_definition = {}


class BGMIntEthPDU6367:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6367
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiAirVentSecLeLeSwtReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "二排左侧的左边出风口关闭请求"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU6368:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6368
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiAirVentSecLeRiSwtReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "二排左侧的右边出风口关闭请求"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU6369:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6369
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiAirVentSecRiLeSwtReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "二排右侧的左边出风口关闭请求"
        signal_length = 1
        start_position = 0
        value_definition = {}


class BGMIntEthPDU6370:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 6370
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HmiAirVentSecRiRiSwtReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = " 二排右侧的右边出风口关闭请求"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU10003:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10003
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class EgyRgnLvlSetETH:
        comments = "MCU SWC接收；"
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "能力回收等级设置"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'EgyRgnLvlSet_Level1', '0x1': 'EgyRgnLvlSet_Level2', '0x2': 'EgyRgnLvlSet_Level3', '0x3': 'EgyRgnLvlSet_Level4'}


class BGMIntEthPDU10004:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10004
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class CstRgnModSetETH:
        comments = "MCU SWC接收；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "滑行能量功能开启关闭"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff2_On', '0x1': 'OnOff2_Off'}


class BGMIntEthPDU10005:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10005
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class EpbSoftSwtCtrlStETH:
        comments = "MCU SWC接收；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "EPB的夹紧释放控制请求"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'EpbSoftSwtCtrlSt_NoRequest', '0x1': 'EpbSoftSwtCtrlSt_ApplyRequest', '0x2': 'EpbSoftSwtCtrlSt_ReleaseRequest', '0x3': 'EpbSoftSwtCtrlSt_Forbidden', '0x4': 'EpbSoftSwtCtrlSt_Unknown'}


class BGMIntEthPDU10006:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10006
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SteerAsscLvlETH:
        comments = "MCU SWC接收；"
        factor = 1.0
        initial_value = 3
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "转向强度等级"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'SteerAsscLvl_Ukwn', '0x1': 'SteerAsscLvl_Lvl1', '0x2': 'SteerAsscLvl_Lvl2', '0x3': 'SteerAsscLvl_Lvl3', '0x4': 'SteerAsscLvl_Lvl4', '0x5': 'SteerAsscLvl_Resd5', '0x6': 'SteerAsscLvl_Resd6', '0x7': 'SteerAsscLvl_Resd7'}


class BGMIntEthPDU10007:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10007
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ModReqOfDampr:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "悬架减震阻尼等级"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'Level1', '0x1': 'Level2', '0x2': 'Level3', '0x3': 'Level4', '0x4': 'Reserved1', '0x5': 'Reserved2', '0x6': 'Reserved3', '0x7': 'Reserved4'}


class BGMIntEthPDU10008:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10008
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HillDwnCtrlStETH:
        comments = "MCU SWC接收；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "陡坡缓降功能的开启和关闭"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU10009:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10009
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'EscSptModReqdByDrvrETH': ['EscSptModReqdByDrvrETHPen', 'EscSptModReqdByDrvrETHEscSptModReqdByDrvr']}

    class EscSptModReqdByDrvrETHPen:
        comments = "MCU SWC接收；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "个性化ID"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}

    class EscSptModReqdByDrvrETHEscSptModReqdByDrvr:
        comments = "MCU SWC接收；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "ESC运动模式开关设置"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'NoYes1_No', '0x1': 'NoYes1_Yes'}


class BGMIntEthPDU10010:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10010
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class CrpModSetETH:
        comments = "MCU SWC接收；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "蠕行模式设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff2_On', '0x1': 'OnOff2_Off'}


class BGMIntEthPDU10011:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10011
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TqModReqETH:
        comments = "MCU SWC接收；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "扭矩模式"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'DrvModReqType1_Undefd', '0x1': 'DrvModReqType1_ECO', '0x2': 'DrvModReqType1_Comfort_Normal', '0x3': 'DrvModReqType1_Dynamic_Sport', '0x4': 'DrvModReqType1_Reserved1', '0x5': 'DrvModReqType1_Offroad_CrossTerrain', '0x6': 'DrvModReqType1_Adaptive', '0x7': 'DrvModReqType1_Race', '0x8': 'DrvModReqType1_Reserved2', '0x9': 'DrvModReqType1_ECO_PLUS', '0xA': 'DrvModReqType1_Power', '0xB': 'DrvModReqType1_Snow', '0xC': 'DrvModReqType1_Sand', '0xD': 'DrvModReqType1_Mud', '0xE': 'DrvModReqType1_Rock', '0xF': 'DrvModReqType1_Err'}


class BGMIntEthPDU10012:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10012
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class AutoHldSoftSwtCtrlStETH:
        comments = "MCU SWC接收；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "AVH功能的开启和关闭"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU10013:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10013
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DrvModReqETH:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "驾驶模式（针对旧平台的）内部以太网信号"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'DrvModReqType1_Undefd', '0x1': 'DrvModReqType1_ECO', '0x2': 'DrvModReqType1_Comfort_Normal', '0x3': 'DrvModReqType1_Dynamic_Sport', '0x4': 'DrvModReqType1_Reserved1', '0x5': 'DrvModReqType1_Offroad_CrossTerrain', '0x6': 'DrvModReqType1_Adaptive', '0x7': 'DrvModReqType1_Race', '0x8': 'DrvModReqType1_Reserved2', '0x9': 'DrvModReqType1_ECO_PLUS', '0xA': 'DrvModReqType1_Power', '0xB': 'DrvModReqType1_Snow', '0xC': 'DrvModReqType1_Sand', '0xD': 'DrvModReqType1_Mud', '0xE': 'DrvModReqType1_Rock', '0xF': 'DrvModReqType1_Err'}


class BGMIntEthPDU10014:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10014
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class GearLvrIndcnInv:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "设置EGSM虚拟挡位显示状态"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'GearLvrIndcnInv_P', '0x1': 'GearLvrIndcnInv_R', '0x2': 'GearLvrIndcnInv_D', '0x3': 'GearLvrIndcnInv_Reserved1', '0x4': 'GearLvrIndcnInv_Reserved2', '0x5': 'GearLvrIndcnInv_Reserved3', '0x6': 'GearLvrIndcnInv_Reserved4', '0x7': 'GearLvrIndcnInv_NOINDICATION'}


class BGMIntEthPDU10015:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 10015
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class AxleTqDistbnReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 12
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "前后电机扭矩分配比例"
        signal_length = 4
        start_position = 3
        value_definition = {'0': 'PosnUkwn', '1': 'PosnMin', '2': 'Perc10', '3': 'Perc20', '4': 'Perc30', '5': 'Perc40', '6': 'Perc50', '7': 'Perc60', '8': 'Perc70', '9': 'Perc80', '10': 'Perc90', '11': 'PosnMax', '12': 'kIntialValue'}


class BGMIntEthPDU15001:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15001
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class MobDevRPAReqResp:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "PA控制请求的反馈	"
        signal_length = 4
        start_position = 3
        value_definition = {}


class BGMIntEthPDU15002:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15002
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class RemFctReqResp:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "AVP控制请求的反馈"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'Reserve1', '0x1': 'Failure', '0x2': 'Success', '0x3': 'Reserve2'}


class BGMIntEthPDU15006:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15006
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class RemCntDwn:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "倒计时计数"
        signal_length = 10
        start_position = 1
        value_definition = {}


class BGMIntEthPDU15009:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15009
    pdu_length_bytes = 8
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'AVPAccountInfo': ['AVPAccountInfoByte0', 'AVPAccountInfoByte1', 'AVPAccountInfoByte2', 'AVPAccountInfoByte3', 'AVPAccountInfoByte4', 'AVPAccountInfoByte5', 'AVPAccountInfoByte6', 'AVPAccountInfoByte7']}

    class AVPAccountInfoByte0:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "AVP功能当前用户账户信息Byte0"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class AVPAccountInfoByte1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "AVP功能当前用户账户信息Byte1"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class AVPAccountInfoByte2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "AVP功能当前用户账户信息Byte2"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class AVPAccountInfoByte3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "AVP功能当前用户账户信息Byte3"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class AVPAccountInfoByte4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "AVP功能当前用户账户信息Byte4"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class AVPAccountInfoByte5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "AVP功能当前用户账户信息Byte5"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class AVPAccountInfoByte6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "AVP功能当前用户账户信息Byte6"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class AVPAccountInfoByte7:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "AVP功能当前用户账户信息Byte7"
        signal_length = 8
        start_position = 63
        value_definition = {}


class BGMIntEthPDU15010:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 15010
    pdu_length_bytes = 10
    receiver = "SoC"
    send_type = "Cyclic-50ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'BLEAccountInfo': ['BLEAccountInfoByte0', 'BLEAccountInfoByte1', 'BLEAccountInfoByte2', 'BLEAccountInfoByte3', 'BLEAccountInfoByte4', 'BLEAccountInfoByte5', 'BLEAccountInfoByte6', 'BLEAccountInfoByte7']}

    class BLEAccountInfoByte0:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "蓝牙用户账号信息Byte0"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class BLEAccountInfoByte1:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "蓝牙用户账号信息Byte1"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class BLEAccountInfoByte2:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "蓝牙用户账号信息Byte2"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class BLEAccountInfoByte3:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "蓝牙用户账号信息Byte3"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class BLEAccountInfoByte4:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "蓝牙用户账号信息Byte4"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class BLEAccountInfoByte5:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "蓝牙用户账号信息Byte5"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class BLEAccountInfoByte6:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "蓝牙用户账号信息Byte6"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class BLEAccountInfoByte7:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "蓝牙用户账号信息Byte7"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class MobDevAVPReq:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "远程AVP功能请求"
        signal_length = 3
        start_position = 66
        value_definition = {'0x0': 'AVPFct_NoReq', '0x1': 'AVPFct_StartPrepare', '0x2': 'AVPFct_Start', '0x3': 'AVPFct_Stop', '0x4': 'AVPFct_StopRecover', '0x5': 'AVPFct_Out', '0x6': 'AVPFct_Reserved1', '0x7': 'AVPFct_Reserved2'}

    class MobDevRPAReq:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "远程RPA控制请求"
        signal_length = 4
        start_position = 75
        value_definition = {'0x0': 'RPAReqJIDU_NoRequest', '0x1': 'RPAReqJIDU_RPA_Start_Request', '0x2': 'RPAReqJIDU_APA_Quit_Request', '0x3': 'RPAReqJIDU_ParkOutMod_Request', '0x4': 'RPAReqJIDU_APA_ParkOut_Request', '0x5': 'RPAReqJIDU_Park_Out_Front_Left', '0x6': 'RPAReqJIDU_Park_Out_Front_Right', '0x7': 'RPAReqJIDU_Park_Out_Rear_Left', '0x8': 'RPAReqJIDU_Park_Out_Rear_Right', '0x9': 'RPAReqJIDU_Park_Out_Left_Front', '0xA': 'RPAReqJIDU_Park_Out_Right_Front', '0xB': 'RPAReqJIDU_APA_Pausing_Request', '0xC': 'RPAReqJIDU_APA_Continue_Request', '0xD': 'RPAReqJIDU_Quit_Because_Mobile_Device_Power_Low', '0xE': 'RPAReqJIDU_Park_Out_Front', '0xF': 'RPAReqJIDU_Park_Out_Rear'}


class BGMIntEthPDU15011:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 15011
    pdu_length_bytes = 18
    receiver = "SoC"
    send_type = "Cyclic-100ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'EveKeyId': ['EveKeyIdByte0', 'EveKeyIdByte1', 'EveKeyIdByte2', 'EveKeyIdByte3', 'EveKeyIdByte4', 'EveKeyIdByte5', 'EveKeyIdByte6', 'EveKeyIdByte7', 'EveKeyIdByte8', 'EveKeyIdByte9', 'EveKeyIdByte10', 'EveKeyIdByte11', 'EveKeyIdByte12', 'EveKeyIdByte13', 'EveKeyIdByte14', 'EveKeyIdByte15']}

    class EveKeyIdByte0:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte0"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class EveKeyIdByte1:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte1"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class EveKeyIdByte2:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte2"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class EveKeyIdByte3:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte3"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class EveKeyIdByte4:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte4"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class EveKeyIdByte5:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte5"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class EveKeyIdByte6:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte6"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class EveKeyIdByte7:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte7"
        signal_length = 8
        start_position = 63
        value_definition = {}

    class EveKeyIdByte8:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte8"
        signal_length = 8
        start_position = 71
        value_definition = {}

    class EveKeyIdByte9:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte9"
        signal_length = 8
        start_position = 79
        value_definition = {}

    class EveKeyIdByte10:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte10"
        signal_length = 8
        start_position = 87
        value_definition = {}

    class EveKeyIdByte11:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte11"
        signal_length = 8
        start_position = 95
        value_definition = {}

    class EveKeyIdByte12:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte12"
        signal_length = 8
        start_position = 103
        value_definition = {}

    class EveKeyIdByte13:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte13"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class EveKeyIdByte14:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte14"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class EveKeyIdByte15:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID Byte15"
        signal_length = 8
        start_position = 127
        value_definition = {}

    class KeyIdEveTyp:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID更新的事件类型"
        signal_length = 3
        start_position = 130
        value_definition = {'0x0': 'Invalid', '0x1': 'Approach_Light', '0x2': 'Approach_Second', '0x3': 'Unlock', '0x4': 'Reserved1', '0x5': 'Reserved2'}

    class EveKeyTyp:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "指示Key ID更新的钥匙类型"
        signal_length = 4
        start_position = 139
        value_definition = {'0x0': 'KeyTyp_NoKeyConnected', '0x1': 'KeyTyp_NFC_Card', '0x2': 'KeyTyp_BLE_Key', '0x3': 'KeyTyp_BLE_UWB_KeyFob', '0x4': 'KeyTyp_Temp_BLE_Key', '0x5': 'KeyTyp_ICCE_BLE_Key', '0x6': 'KeyTyp_ICCE_NFC_Key', '0x7': 'KeyTyp_CCC_NFC_BLE_UWB_Key', '0x8': 'KeyTyp_CCC_NFC_Key', '0x9': 'KeyTyp_CCC_NFC_BLE_Key'}


class BGMIntEthPDU15014:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15014
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DrvrDoorOpenWhenUnlockHmi:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "车外解锁关联主驾电动门开启功能开启关闭"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'EnableDisable_Enable', '0x1': 'EnableDisable_Disable'}


class BGMIntEthPDU15015:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15015
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ApproachUnlockHmi:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "靠近解锁开关"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'EnableDisable_Enable', '0x1': 'EnableDisable_Disable'}

    class WalkAwayLockHmi:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 2
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "离车上锁开关"
        signal_length = 3
        start_position = 10
        value_definition = {'0x0': 'WalkAwayLockHmi_Off', '0x1': 'WalkAwayLockHmi_OnWithoutAnyDoorClose', '0x2': 'WalkAwayLockHmi_OnWithDriverDoorClose', '0x3': 'WalkAwayLockHmi_OnWithAllDoorClose', '0x4': 'WalkAwayLockHmi_OnWithAllDoorAndTailgateClose', '0x5': 'WalkAwayLockHmi_Reserved1', '0x6': 'WalkAwayLockHmi_Reserved2', '0x7': 'WalkAwayLockHmi_Reserved3'}


class BGMIntEthPDU15017:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15017
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ReminderWhileLock:
        comments = "底层软件需配置信号路由"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "闭锁时的状态提示"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'ReminderWhileLock_IDLE', '0x1': 'ReminderWhileLock_NOT_SET_APPROACH_LOCK_HMI', '0x2': 'ReminderWhileLock_DOOR_CLOSE_STOP_DUR_CLOSE_BY_APPROACH', '0x3': 'ReminderWhileLock_DOOR_CLOSE_STOP_DUR_CLOSE_BY_NFC_PE', '0x4': 'ReminderWhileLock_KEY_FORGET_REMINDER_NFC'}


class BGMIntEthPDU15018:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15018
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class KeyReadReqFromSrv:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "寻钥匙请求"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'KeyLocn1_KeyLocnIdle', '0x1': 'KeyLocn1_KeyLocnAll', '0x2': 'KeyLocn1_KeyLocnAllExt', '0x3': 'KeyLocn1_KeyLocnDrvrExt', '0x4': 'KeyLocn1_KeyLocnPassExt', '0x5': 'KeyLocn1_KeyLocnTrExt', '0x6': 'KeyLocn1_KeyLocnAllInt', '0x7': 'KeyLocn1_KeyLocnDrvrInt', '0x8': 'KeyLocn1_KeyLocnPassInt', '0x9': 'KeyLocn1_KeyLocnResvInt', '0xA': 'KeyLocn1_KeyLocnResvIntSimple'}


class BGMIntEthPDU15019:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 15019
    pdu_length_bytes = 1
    receiver = "SoC"
    send_type = "Cyclic-100ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class KeyReadStsToSrv:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "寻钥匙结果"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'KeyPrsntSts1_KeyPrsntStsIdle', '0x1': 'KeyPrsntSts1_KeyPrsntStsInProgs', '0x2': 'KeyPrsntSts1_KeyPrsntStsNotPrsnt', '0x3': 'KeyPrsntSts1_KeyPrsntStsPrsnt'}


class BGMIntEthPDU15020:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15020
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class AvpTargetpkgtpe:
        comments = "底层软件需配置信号路由"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "车位形态"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ParkLotVertical', '0x1': 'ParkLotLatitude', '0x2': 'ParkLotInclined'}


class BGMIntEthPDU15021:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15021
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HavpMatchSts:
        comments = "底层软件需配置信号路由"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "路线匹配状态"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'Math_No_Info', '0x1': 'Math_False', '0x2': 'Math_True'}


class BGMIntEthPDU15022:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15022
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class RemPATarpkgDir:
        comments = "底层软件需配置信号路由"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "目标车位方向"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'PATarpkgDirNoInfo', '0x1': 'PATarpkgDirLeft', '0x2': 'PATarpkgDirRight'}


class BGMIntEthPDU15023:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15023
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ETCWorkStsReq:
        comments = "底层软件需配置信号路由"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "ETC开启关闭设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU15024:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 15024
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-1000ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TelmRemoteAuthStartSts:
        comments = "底层软件需配置信号路由;MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程授权启动状态"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU20001:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20001
    pdu_length_bytes = 25
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class UTCTimeEth:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 1609459200000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "UTC，timestamp  距离1970/01/01 00:00:00的时间戳 单位ms"
        signal_length = 64
        start_position = 7
        value_definition = {}

    class TimeZoneEth:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 8
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "时区"
        signal_length = 8
        start_position = 135
        value_definition = {'0x0': ' TimeZoneEth_MIDDLE_ZONE', '0x1': ' TimeZoneEth_EAST_1', '0x2': ' TimeZoneEth_EAST_2', '0x3': ' TimeZoneEth_EAST_3', '0x4': ' TimeZoneEth_EAST_4', '0x5': ' TimeZoneEth_EAST_5', '0x6': ' TimeZoneEth_EAST_6', '0x7': ' TimeZoneEth_EAST_7', '0x8': ' TimeZoneEth_EAST_8', '0x9': ' TimeZoneEth_EAST_9', '0xA': ' TimeZoneEth_EAST_10', '0xB': ' TimeZoneEth_EAST_11', '0xC': ' TimeZoneEth_EAST_WEST_12', '0xD': ' TimeZoneEth_WEST_11', '0xE': ' TimeZoneEth_WEST_10', '0xF': ' TimeZoneEth_WEST_9', '0x10': ' TimeZoneEth_WEST_8', '0x11': ' TimeZoneEth_WEST_7', '0x12': ' TimeZoneEth_WEST_6', '0x13': ' TimeZoneEth_WEST_5', '0x14': ' TimeZoneEth_WEST_4', '0x15': ' TimeZoneEth_WEST_3', '0x16': ' TimeZoneEth_WEST_2', '0x17': ' TimeZoneEth_WEST_1'}

    class GlobalTimeEth:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 316224000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "全局时间"
        signal_length = 64
        start_position = 143
        value_definition = {}

    class UTCTimeBcdEth:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 9043487450726400
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "UTC (BCD格式)"
        signal_length = 64
        start_position = 71
        value_definition = {}


class BGMIntEthPDU20002:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 20002
    pdu_length_bytes = 2
    receiver = "SoC"
    send_type = "Cyclic-100ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class OBDStatusEth:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "OBD接入状态反馈"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class RebootIndicateEth:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU即将重启标志"
        signal_length = 8
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20003:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 20003
    pdu_length_bytes = 1
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class AppointmentWakeupSetResp:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "预约设置结果反馈"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20004:
    base_type = "unsigned"
    client_socket = "SocketPMSocTCPUp"
    pdu_header_id = 20004
    pdu_length_bytes = 3
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'IpcVucPmStateInfoRep': ['WakeupReason', 'PowerMode', 'RebootReason']}

    class WakeupReason:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "power master电源状态信息上报"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class PowerMode:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "power master电源状态信息上报"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class RebootReason:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "power master电源状态信息上报"
        signal_length = 8
        start_position = 23
        value_definition = {}


class BGMIntEthPDU20005:
    base_type = "unsigned"
    client_socket = "SocketPMSocTCPDown"
    pdu_header_id = 20005
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class IpcVucPmStateInfoReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Slave 请求 Master电源消息"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20006:
    base_type = "unsigned"
    client_socket = "SocketPMSocTCPUp"
    pdu_header_id = 20006
    pdu_length_bytes = 1
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class IpcVucShutdownReq:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Power master 通知slave准备shutdown"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20007:
    base_type = "unsigned"
    client_socket = "SocketPMSocTCPDown"
    pdu_header_id = 20007
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class IpcSlvResetReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Slave请求Power master重启BGM系统"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20008:
    base_type = "unsigned"
    client_socket = "SocketPMSocTCPDown"
    pdu_header_id = 20008
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class IpcSlvPmWatchdog:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Slave 电源心跳通知"
        signal_length = 16
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20009:
    base_type = "unsigned"
    client_socket = "SocketPMSocTCPDown"
    pdu_header_id = 20009
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class IpcSlvShutdownReady:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Slave shutdown ready通知"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20010:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20010
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ECUsEthCommSts:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "与其他域控的以太网通信状态"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20011:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20011
    pdu_length_bytes = 1028
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'DataSet': ['GenericID', 'GenericLength', 'GenericData']}

    class GenericID:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "通用ID"
        signal_length = 16
        start_position = 7
        value_definition = {}

    class GenericLength:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "通用长度"
        signal_length = 16
        start_position = 23
        value_definition = {}

    class GenericData:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        signal_description = "变长通用数据，由通用长度决定实际长度"
        signal_length = 8192
        start_position = 39
        value_definition = {}


class BGMIntEthPDU20012:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20012
    pdu_length_bytes = 10
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'AppointmentWakeup': ['AppointmentWakeupSrc', 'AppointmentWakeupTime']}

    class AppointmentWakeupSrc:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "预约唤醒源"
        signal_length = 16
        start_position = 7
        value_definition = {}

    class AppointmentWakeupTime:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "预约唤醒时间"
        signal_length = 64
        start_position = 23
        value_definition = {}


class BGMIntEthPDU20013:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20013
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class GenericID1:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "通用ID"
        signal_length = 16
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20014:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 20014
    pdu_length_bytes = 1028
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'DataReport2': ['GenericID2', 'GenericLength2', 'GenericData2']}

    class GenericID2:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "通用ID"
        signal_length = 16
        start_position = 7
        value_definition = {}

    class GenericLength2:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "通用长度"
        signal_length = 16
        start_position = 23
        value_definition = {}

    class GenericData2:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        signal_description = "变长通用数据，由通用长度决定实际长度"
        signal_length = 8192
        start_position = 39
        value_definition = {}


class BGMIntEthPDU20015:
    base_type = "unsigned"
    client_socket = "SocketTIMESocTCPUp"
    pdu_header_id = 20015
    pdu_length_bytes = 1028
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'DataReport': ['FunctionID', 'DataLength', 'Data']}

    class FunctionID:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "功能ID"
        signal_length = 16
        start_position = 7
        value_definition = {}

    class DataLength:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "数据长度"
        signal_length = 16
        start_position = 23
        value_definition = {}

    class Data:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        signal_description = "变长数据，由通用长度决定实际长度"
        signal_length = 8192
        start_position = 39
        value_definition = {}


class BGMIntEthPDU20018:
    base_type = "unsigned"
    client_socket = "SocketPMSocTCPDown"
    pdu_header_id = 20018
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class IpcSlvBootCompleted:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "Slave boot完成通知"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20019:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 20019
    pdu_length_bytes = 8
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class UTCTimeEthUp:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 1609459200000
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "UTC上行数据"
        signal_length = 64
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20020:
    base_type = "unsigned"
    client_socket = "SocketPMSocTCPUp"
    pdu_header_id = 20020
    pdu_length_bytes = 1
    receiver = "SoC"
    send_type = "Cyclic-100ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class HeartbeatMonitorUp:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "心跳监测MCU"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20021:
    base_type = "unsigned"
    client_socket = "SocketPMSocTCPDown"
    pdu_header_id = 20021
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-100ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HeartbeatMonitorDown:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "心跳监控MPU"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU20022:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20022
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqInfotainmentPush:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeInfotainmentPush:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20023:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20023
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqLocking:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeLocking:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20024:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20024
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqExteriorLighting:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeExteriorLighting:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20025:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20025
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqPowerClosures:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimePowerClosures:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20026:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20026
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqPostClimatisation:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimePostClimatisation:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20027:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20027
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqVisibility:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeVisibilit:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20028:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20028
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqSettingsComfort:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeSettingsComfort:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20029:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20029
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqRemoteKeyFunctionality:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeRemoteKeyFunctionality:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20030:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20030
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqSettingsProfile:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeSettingsProfile:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20031:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20031
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqSettingsVehicle:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeSettingsVehicle:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20032:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20032
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqIPWakeup:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeIPWakeup:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20033:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20033
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqFunctionmarket:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeFunctionmarket:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20034:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20034
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqPropulsionStart:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimePropulsionStart:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20035:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20035
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqChargingHV:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeChargingHV:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20036:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20036
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqChargingLVInit:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeChargingLVInit:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20037:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20037
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqImmobilizer:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeImmobilizer:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20038:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20038
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqParkingDrivingClimatization:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeParkingDrivingClimatization:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20039:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20039
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqTelematicsConnectivity:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeTelematicsConnectivity:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20040:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20040
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqTrailerCaravanFunctions:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeTrailerCaravanFunctions:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20041:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20041
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqLifeDetection:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeLifeDetection:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20042:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20042
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqVisualAssist:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeVisualAssist:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20043:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20043
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqVehicleDriving:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeVehicleDriving:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20044:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20044
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqVehicleModeManagement:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeVehicleModeManagement:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20045:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20045
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqDiagnostic:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeDiagnostic:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20046:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20046
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqGlobalShortDuration:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeGlobalShortDuration:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20047:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20047
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqInfotainmentPoll:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeInfotainmentPoll:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20048:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20048
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqInteriorLighting:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeInteriorLighting:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20049:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20049
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqAlarm:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeAlarm:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20050:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20050
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqBrake:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeBrake:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20051:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20051
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqHVBatteryThermalEventWarning:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeHVBatteryThermalEventWarning:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20052:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20052
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqHVEngergyStorage:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeHVEngergyStorage:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20053:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20053
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqPowertrainParkingClimatization:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimePowertrainParkingClimatization:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20054:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20054
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqDoorOpenWarning:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeDoorOpenWarning:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20055:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20055
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqWindows:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeWindows:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20056:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20056
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqSeatComFortFunctions:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeSeatComFortFunctions:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20057:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20057
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqBodyPreClimatisation:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeBodyPreClimatisation:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20058:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20058
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqExteriorLightsHazard:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeExteriorLightsHazard:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20059:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20059
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqCrash:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeCrash:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20060:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20060
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqPassiveSafety:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimePassiveSafety:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20061:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20061
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class VFCReqBackboneFlexray:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC Activate / Deactivate"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ActDurTimeBackboneFlexray:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "VFC激活持续时间"
        signal_length = 16
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20062:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 20062
    pdu_length_bytes = 2
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'DiagToolStatus': ['ActivationLineStatus', 'ObdCANStatus']}

    class ActivationLineStatus:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "诊断激活线状态"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class ObdCANStatus:
        comments = "MCU SWC发送 收到诊断报文，变为active 6s 没有诊断报文，变为inactive"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "OBD CAN 诊断状态"
        signal_length = 8
        start_position = 15
        value_definition = {}


class BGMIntEthPDU20063:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20063
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DiagcExtCom:
        comments = "MCU SWC接收；对应接收Port为DiagcExtCom，同时需删除原发送Port；底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "诊断仪连接状态"
        signal_length = 1
        start_position = 0
        value_definition = {}

    class DiagcComActv:
        comments = "底层软件需配置信号路由；MCU SWC接收；对应接收Port为DiagcComActv，同时需删除原发送Port"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "诊断仪(内部/外部)通信激活状态"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'YesNo2_No', '0x1': 'YesNo2_Yes'}


class BGMIntEthPDU20064:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 20064
    pdu_length_bytes = 1040
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'LvSocCalibInfo': ['LvSocCalibType', 'LvSocCalibSubType', 'LvSocCalibData']}

    class LvSocCalibType:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "低压SOC标定信息"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class LvSocCalibSubType:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "低压SOC标定信息"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class LvSocCalibData:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        signal_description = "低压SOC标定信息"
        signal_length = 8192
        start_position = 16
        value_definition = {}


class BGMIntEthPDU20065:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 20065
    pdu_length_bytes = 1040
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'LvSocUploadInfo': ['LvSocUpBlockNum', 'LvSocUpBlockIndex', 'LvSocUpData']}

    class LvSocUpBlockNum:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "低压SOC缓存信息上传"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class LvSocUpBlockIndex:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "低压SOC缓存信息上传"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class LvSocUpData:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        signal_description = "低压SOC缓存信息上传"
        signal_length = 8192
        start_position = 16
        value_definition = {}


class BGMIntEthPDU20070:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 20070
    pdu_length_bytes = 28
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'version': ['CoreAssemblyPN', 'DeliveryAssemblyPN', 'SerialNumber', 'PBLPN']}

    class CoreAssemblyPN:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "硬件号 F1AA"
        signal_length = 64
        start_position = 7
        value_definition = {}

    class DeliveryAssemblyPN:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "总成号 F1AB"
        signal_length = 64
        start_position = 71
        value_definition = {}

    class SerialNumber:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "序列号 F18C"
        signal_length = 32
        start_position = 135
        value_definition = {}

    class PBLPN:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "序列号 F1A5"
        signal_length = 64
        start_position = 167
        value_definition = {}


class BGMIntEthPDU20100:
    base_type = "unsigned"
    client_socket = "SocketPMSocTCPDown"
    pdu_header_id = 20100
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class IpcSlvKeepAlive:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "保持mcu唤醒时间"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU21001:
    base_type = "unsigned"
    client_socket = "SocketLOGSocTCPUp"
    pdu_header_id = 21001
    pdu_length_bytes = 21
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'McuDetTrace': ['McuDetLogBlkNo', 'McuDetModuleId', 'McuDetInstanceId', 'McuDetApiId', 'McuDetErrorId', 'McuDetReportType', 'McuDetOccurrTime', 'McuDetSpeed', 'McuDetVoltage', 'McuDetUsgMode', 'McuDetOdoMeter', 'McuDetReserve']}

    class McuDetLogBlkNo:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 Log Block no"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class McuDetModuleId:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 Module ID"
        signal_length = 16
        start_position = 15
        value_definition = {}

    class McuDetInstanceId:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 Instance ID"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class McuDetApiId:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 API ID"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class McuDetErrorId:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 Error ID"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class McuDetReportType:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 ReportType"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class McuDetOccurrTime:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 OccurrTime (CarTiGlb)"
        signal_length = 32
        start_position = 63
        value_definition = {}

    class McuDetSpeed:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 Speed"
        signal_length = 16
        start_position = 95
        value_definition = {}

    class McuDetVoltage:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 Voltage"
        signal_length = 8
        start_position = 111
        value_definition = {}

    class McuDetUsgMode:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 UsgMode"
        signal_length = 8
        start_position = 119
        value_definition = {}

    class McuDetOdoMeter:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 OdoMeter"
        signal_length = 16
        start_position = 127
        value_definition = {}

    class McuDetReserve:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Det现场 Reserve"
        signal_length = 32
        start_position = 143
        value_definition = {}


class BGMIntEthPDU21002:
    base_type = "unsigned"
    client_socket = "SocketLOGSocTCPUp"
    pdu_header_id = 21002
    pdu_length_bytes = 17
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'McuModuleTrace': ['McuModuleId', 'McuModuleReserve1', 'McuModuleReserve2', 'McuModuleReserve3', 'McuModuleReserve4']}

    class McuModuleId:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Module信息 ID"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class McuModuleReserve1:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Module信息 Reserve1"
        signal_length = 32
        start_position = 15
        value_definition = {}

    class McuModuleReserve2:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Module信息 Reserve2"
        signal_length = 32
        start_position = 47
        value_definition = {}

    class McuModuleReserve3:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Module信息 Reserve3"
        signal_length = 32
        start_position = 79
        value_definition = {}

    class McuModuleReserve4:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "MCU Module信息 Reserve4"
        signal_length = 32
        start_position = 111
        value_definition = {}


class BGMIntEthPDU21003:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 21003
    pdu_length_bytes = 17
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class VIN_ETH:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        signal_description = "VIN"
        signal_length = 136
        start_position = 0
        value_definition = {}


class BGMIntEthPDU21004:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 21004
    pdu_length_bytes = 1556
    receiver = "SoC"
    send_type = "Event Trigger"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class CarConfig:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "N"
        offset = 0
        signal_description = "CarConfig"
        signal_length = 12448
        start_position = 0
        value_definition = {}


class BGMIntEthPDU25001:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 25001
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class WashModeSts:
        comments = "底层软件需配置信号路由；MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "洗车模式"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU30001:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30001
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DrvModSet:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "驾驶模式"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'DrvModReqType1_Undefd', '0x1': 'DrvModReqType1_ECO', '0x2': 'DrvModReqType1_Comfort_Normal', '0x3': 'DrvModReqType1_Dynamic_Sport', '0x4': 'DrvModReqType1_Reserved1', '0x5': 'DrvModReqType1_Offroad_CrossTerrain', '0x6': 'DrvModReqType1_Adaptive', '0x7': 'DrvModReqType1_Race', '0x8': 'DrvModReqType1_Reserved2', '0x9': 'DrvModReqType1_ECO_PLUS', '0xA': 'DrvModReqType1_Power', '0xB': 'DrvModReqType1_Snow', '0xC': 'DrvModReqType1_Sand', '0xD': 'DrvModReqType1_Mud', '0xE': 'DrvModReqType1_Rock', '0xF': 'DrvModReqType1_Err'}


class BGMIntEthPDU30003:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30003
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SceneModSeld:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "场景模式"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'PatSeld_NoSeld', '0x1': 'PatSeld_RefrshPatSeld', '0x2': 'PatSeld_ParentchildPatSeld', '0x3': 'PatSeld_Restpatseld', '0x4': 'PatSeld_RomanticPatseld', '0x5': 'PatSeld_StrangerPatseld', '0x6': 'PatSeld_TheaterPatseld', '0x7': 'PatSeld_PetPatseld', '0x8': 'PatSeld_BiochalPatseld', '0x9': 'PatSeld_CarWashPatseld', '0xA': 'PatSeld_EcoPatseld', '0xB': 'PatSeld_KingPatseld', '0xC': 'PatSeld_CustomizationPatseld', '0xD': 'PatSeld_MeetingPatseld'}


class BGMIntEthPDU30004:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30004
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DrvrPfmncAlrmReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "主驾安全带震动控制"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'DrvrPfmncWarnReq_Unavailable', '0x1': 'DrvrPfmncWarnReq_Unknown', '0x2': 'DrvrPfmncWarnReq_NoWarning', '0x3': 'DrvrPfmncWarnReq_Distractive', '0x4': 'DrvrPfmncWarnReq_Warninglevel1', '0x5': 'DrvrPfmncWarnReq_Warninglevel2', '0x6': 'DrvrPfmncWarnReq_Reserved'}


class BGMIntEthPDU30005:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30005
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SwtPwrStsOfVehSurrndgsVisnRec:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "哨兵模式下DVR激活状态"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU30006:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30006
    pdu_length_bytes = 28
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HavpSts:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "HAVP功能状态"
        signal_length = 4
        start_position = 3
        value_definition = {'0x0': 'Off', '0x1': 'Enable', '0x2': 'Standby', '0x3': 'Learningpath', '0x4': 'Active', '0x5': 'Pausing', '0x6': 'Completed', '0x7': 'Disabled', '0x8': 'Terminated', '0x9': 'Failure', '0xA': 'Reserve1', '0xB': 'Reserve2', '0xC': 'Reserve3', '0xD': 'Reserve4', '0xE': 'Reserve5', '0xF': 'Reserve6'}

    class HavpBleFctSts:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "HAVP是否允许蓝牙控制"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}

    class HavpSysStsDisp:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "HAVP退出/暂停原因"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class HavpReminder:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "AVP提示信息"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class HavpLstHndlTyp:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "HAVP上次控制方式"
        signal_length = 3
        start_position = 34
        value_definition = {'0x0': 'DEFAULT', '0x1': 'CDC_SOFT_SWITCH', '0x2': 'CDC_INSIDE_VOICE', '0x3': 'CDC_OUTSIDE_VOICE', '0x4': 'STEEL_KEY', '0x5': 'BLUETOOTH', '0x6': 'TELEMATICS'}

    class HavpSlamID:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Opaque"
        mcu_routing = "Y"
        offset = 0
        signal_description = "路线SlamID"
        signal_length = 184
        start_position = 40
        value_definition = {}


class BGMIntEthPDU30007:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30007
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class MobDevRPASts:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "PA功能状态"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class RPASysDisp:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "PA提示信息"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class PALstHndlTyp:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "APA上次控制方式"
        signal_length = 3
        start_position = 18
        value_definition = {'0x0': 'DEFAULT', '0x1': 'CDC_SOFT_SWITCH', '0x2': 'CDC_INSIDE_VOICE', '0x3': 'CDC_OUTSIDE_VOICE', '0x4': 'BLUETOOTH'}


class BGMIntEthPDU30008:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30008
    pdu_length_bytes = 16
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'PrkgOutModBtnStsToAPP': ['PrkgOutModBtnStsToAPPPrkgOutModBtnSts1', 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts2', 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts3', 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts4', 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts5', 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts6', 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts7', 'PrkgOutModBtnStsToAPPPrkgOutModBtnSts8'], 'BleCtrlRPABtnSts': ['BleCtrlRPABtnStsFrnt', 'BleCtrlRPABtnStsRear', 'BleCtrlRPABtnStsLftTurn', 'BleCtrlRPABtnStsRgtTurn']}

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "泊出车位控制前左控制按键显示状态"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "泊出车位控制前右控制按键显示状态"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "泊出车位控制后左控制按键显示状态"
        signal_length = 2
        start_position = 17
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "泊出车位控制后右控制按键显示状态"
        signal_length = 2
        start_position = 25
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "泊出车位控制左前控制按键显示状态"
        signal_length = 2
        start_position = 33
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "泊出车位控制右前控制按键显示状态"
        signal_length = 2
        start_position = 41
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts7:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "泊出车位控制直前控制按键显示状态"
        signal_length = 2
        start_position = 49
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class PrkgOutModBtnStsToAPPPrkgOutModBtnSts8:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "泊出车位控制直后控制按键显示状态"
        signal_length = 2
        start_position = 57
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class BleCtrlRPABtnStsFrnt:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "RPA前进控制按键显示状态"
        signal_length = 2
        start_position = 65
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class BleCtrlRPABtnStsRear:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "RPA后退控制按键显示状态"
        signal_length = 2
        start_position = 73
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class BleCtrlRPABtnStsLftTurn:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "RPA左转控制按键显示状态"
        signal_length = 2
        start_position = 81
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class BleCtrlRPABtnStsRgtTurn:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "RPA右转控制按键显示状态"
        signal_length = 2
        start_position = 89
        value_definition = {'0x0': 'ActvnAvl4_Idle', '0x1': 'ActvnAvl4_Actvn', '0x2': 'ActvnAvl4_Deactvn', '0x3': 'ActvnAvl4_Recommand'}

    class HavpModBtnSts1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "预留按键状态"
        signal_length = 2
        start_position = 97
        value_definition = {}

    class HavpModBtnSts2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "预留按键状态"
        signal_length = 2
        start_position = 105
        value_definition = {}

    class HavpModBtnSts3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "预留按键状态"
        signal_length = 2
        start_position = 113
        value_definition = {}

    class HavpModBtnSts4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "预留按键状态"
        signal_length = 2
        start_position = 121
        value_definition = {}


class BGMIntEthPDU30009:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30009
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class MirrOpenClsReq:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "外后视镜折叠展开请求状态"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'MirrFoldCmdTyp_Idle', '0x1': 'MirrFoldCmdTyp_FoldIn', '0x2': 'MirrFoldCmdTyp_FoldOut'}


class BGMIntEthPDU30010:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30010
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class LnchModSwt:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "设置弹射起步功能开启关闭"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU30011:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30011
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TrackModSwt:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "设置赛道模式功能开启关闭"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU30012:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30012
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DelayCloseDoorHMI:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "延时关门"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU30013:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30013
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-500ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class BrakeCloseDoorInhibitStatus:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "踩刹车自动关门禁用状态"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU30014:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30014
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-100ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class WakeUpCDCFromProxy:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "唤醒CDC"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}

    class WakeUpACUFromProxy:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "唤醒ACU"
        signal_length = 1
        start_position = 1
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU30015:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30015
    pdu_length_bytes = 4
    receiver = "MCU"
    send_type = "Cyclic-500ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class MinTiLVBattChargeReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "最小充电时间"
        signal_length = 16
        start_position = 7
        value_definition = {}

    class MaxTiLVBattReChargeReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "最大补电间隔时间"
        signal_length = 16
        start_position = 23
        value_definition = {}


class BGMIntEthPDU30016:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30016
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class WirelschrgActvReqFromHmiPass:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "设置副驾无线充电功能开启关闭"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU30017:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30017
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetInsdWinSWInhibit:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "车内车窗开关动作禁止"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU30018:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30018
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetInsdoorSWInhibit:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "车内门开关动作禁止"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU30019:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30019
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class RlyPwrCmdProxyReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "12V继电器服务请求"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU30020:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30020
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class IgnRlyExtCmdProxyReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "KL15_2继电器服务请求"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU30021:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30021
    pdu_length_bytes = 8
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'BGMMPUCtrlACU': ['BGMMPUCtrlACUByte0', 'BGMMPUCtrlACUByte1', 'BGMMPUCtrlACUByte2', 'BGMMPUCtrlACUByte3', 'BGMMPUCtrlACUByte4', 'BGMMPUCtrlACUByte5', 'BGMMPUCtrlACUByte6', 'BGMMPUCtrlACUByte7']}

    class BGMMPUCtrlACUByte0:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制ACU MCU专用信号0"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class BGMMPUCtrlACUByte1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制ACU MCU专用信号1"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class BGMMPUCtrlACUByte2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制ACU MCU专用信号2"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class BGMMPUCtrlACUByte3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制ACU MCU专用信号3"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class BGMMPUCtrlACUByte4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制ACU MCU专用信号4"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class BGMMPUCtrlACUByte5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制ACU MCU专用信号5"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class BGMMPUCtrlACUByte6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制ACU MCU专用信号6"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class BGMMPUCtrlACUByte7:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制ACU MCU专用信号7"
        signal_length = 8
        start_position = 63
        value_definition = {}


class BGMIntEthPDU30022:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30022
    pdu_length_bytes = 8
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'BGMMPUCtrlCDC': ['BGMMPUCtrlCDCByte0', 'BGMMPUCtrlCDCByte1', 'BGMMPUCtrlCDCByte2', 'BGMMPUCtrlCDCByte3', 'BGMMPUCtrlCDCByte4', 'BGMMPUCtrlCDCByte5', 'BGMMPUCtrlCDCByte6', 'BGMMPUCtrlCDCByte7']}

    class BGMMPUCtrlCDCByte0:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制CDC MCU专用信号0"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class BGMMPUCtrlCDCByte1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制CDC MCU专用信号1"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class BGMMPUCtrlCDCByte2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制CDC MCU专用信号2"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class BGMMPUCtrlCDCByte3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制CDC MCU专用信号3"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class BGMMPUCtrlCDCByte4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制CDC MCU专用信号4"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class BGMMPUCtrlCDCByte5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制CDC MCU专用信号5"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class BGMMPUCtrlCDCByte6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制CDC MCU专用信号6"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class BGMMPUCtrlCDCByte7:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制CDC MCU专用信号7"
        signal_length = 8
        start_position = 63
        value_definition = {}


class BGMIntEthPDU30023:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30023
    pdu_length_bytes = 8
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'BGMMPUCtrlTCAM': ['BGMMPUCtrlTCAMByte0', 'BGMMPUCtrlTCAMByte1', 'BGMMPUCtrlTCAMByte2', 'BGMMPUCtrlTCAMByte3', 'BGMMPUCtrlTCAMByte4', 'BGMMPUCtrlTCAMByte5', 'BGMMPUCtrlTCAMByte6', 'BGMMPUCtrlTCAMByte7']}

    class BGMMPUCtrlTCAMByte0:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制TCAM MCU专用信号0"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class BGMMPUCtrlTCAMByte1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制TCAM MCU专用信号1"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class BGMMPUCtrlTCAMByte2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制TCAM MCU专用信号2"
        signal_length = 8
        start_position = 23
        value_definition = {}

    class BGMMPUCtrlTCAMByte3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制TCAM MCU专用信号3"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class BGMMPUCtrlTCAMByte4:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制TCAM MCU专用信号4"
        signal_length = 8
        start_position = 39
        value_definition = {}

    class BGMMPUCtrlTCAMByte5:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制TCAM MCU专用信号5"
        signal_length = 8
        start_position = 47
        value_definition = {}

    class BGMMPUCtrlTCAMByte6:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制TCAM MCU专用信号6"
        signal_length = 8
        start_position = 55
        value_definition = {}

    class BGMMPUCtrlTCAMByte7:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "BGM MPU控制TCAM MCU专用信号7"
        signal_length = 8
        start_position = 63
        value_definition = {}


class BGMIntEthPDU30024:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30024
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class PlsHeatgReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "脉冲加热请求"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU30025:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30025
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class HvBattClimaPrioReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "加热电池优先请求"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'ClimaPriority_Default', '0x1': 'ClimaPriority_HeatgPrioReq', '0x2': 'ClimaPriority_CoolgPrioReq', '0x3': 'ClimaPriority_Reserved'}


class BGMIntEthPDU30026:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30026
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Cyclic-100ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class UsrInVehSts:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "车内有无人状态"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}

    class UsrInVehStsforDigKey:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "数字钥匙专用车内有无人状态"
        signal_length = 1
        start_position = 8
        value_definition = {'0x0': 'Boolean_FALSE', '0x1': 'Boolean_TRUE'}


class BGMIntEthPDU30027:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30027
    pdu_length_bytes = 7
    receiver = "MCU"
    send_type = "Cyclic-200ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class MaxAcInpCurrentSet:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "设置交流充电最大电流"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DstToDestination:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "距离目的地剩余里程"
        signal_length = 32
        start_position = 15
        value_definition = {}

    class HVIntelligentChrgSWSt:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "高压静态补电开关状态"
        signal_length = 2
        start_position = 49
        value_definition = {'0x0': 'OnOffCrit1_NotVld1', '0x1': 'OnOffCrit1_Off', '0x2': 'OnOffCrit1_On', '0x3': 'OnOffCrit1_NotVld2'}

    class ReservedSigForHVBatt1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "电池控制预留下行信息1"
        signal_length = 4
        start_position = 43
        value_definition = {}

    class ReservedSigForHVBatt3:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "电池控制预留下行信息3"
        signal_length = 4
        start_position = 47
        value_definition = {}


class BGMIntEthPDU30028:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30028
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-50ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class V2XDchaSwt:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "放电开关状态"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'DisChrgrSW_Off', '0x1': 'DisChrgrSW_V2V', '0x2': 'DisChrgrSW_V2L'}


class BGMIntEthPDU30030:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30030
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class RemHvBattHeatgReqFromAC:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "远程电池加热请求"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'RemHvBattHeatgReq_OFF', '0x1': 'RemHvBattHeatgReq_ON'}


class BGMIntEthPDU30031:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30031
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DriftModReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "漂移模式请求"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OnOffNoReq_NoReq', '0x1': 'OnOffNoReq_On', '0x2': 'OnOffNoReq_Off'}


class BGMIntEthPDU30032:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30032
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class BoostModAutoReq:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "扭矩增压模式请求"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'AutoModReq_Default', '0x1': 'AutoModReq_Auto', '0x2': 'AutoModReq_Manual', '0x3': 'AutoModReq_Reserve'}


class BGMIntEthPDU30033:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30033
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ResvReq1:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "预留请求信号1"
        signal_length = 4
        start_position = 3
        value_definition = {}


class BGMIntEthPDU30034:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30034
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ResvReq2:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "预留请求信号2"
        signal_length = 4
        start_position = 3
        value_definition = {}


class BGMIntEthPDU30035:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30035
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class SetPwrDoorAutoClsMode:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "电动门关门方式设置"
        signal_length = 1
        start_position = 0
        value_definition = {'0x0': 'OnOff1_Off', '0x1': 'OnOff1_On'}


class BGMIntEthPDU30036:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30036
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DoorOpenResistCmd:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "开门阻力增加请求"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'DoorOpenResistCmd_Idle', '0x1': 'DoorOpenResistCmd_AddResist', '0x2': 'DoorOpenResistCmd_SubtResist', '0x3': 'DoorOpenResistCmd_Resd'}


class BGMIntEthPDU30037:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30037
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Cyclic-100ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DrvrSeatSts2:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 1.0
        initial_value = 1
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "融合视觉感知主驾占位状态"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'OccptPresSt1_Undefd1', '0x1': 'OccptPresSt1_OccptNotPrsnt', '0x2': 'OccptPresSt1_OccptPrsnt', '0x3': 'OccptPresSt1_Undefd2'}


class BGMIntEthPDU30038:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 30038
    pdu_length_bytes = 1
    receiver = "SoC"
    send_type = "Cyclic-50ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {}

    class StsOfLedChargingLidLamp:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "充电口盖照明灯状态"
        signal_length = 2
        start_position = 1
        value_definition = {'0x0': 'DevSts4_Off', ' 0x1': 'DevSts4_On', ' 0x2': 'DevSts4_Err', ' 0x3': 'DevSts4_Resd'}


class BGMIntEthPDU30039:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30039
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DchaChrgnTarVal:
        comments = "底层软件需配置信号路由；MCU SWC需接收"
        factor = 0.1
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "设置放电目标SOC值"
        signal_length = 10
        start_position = 9
        value_definition = {}


class BGMIntEthPDU30040:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30040
    pdu_length_bytes = 2
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class DstFromDestination:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "目标行驶里程"
        signal_length = 10
        start_position = 9
        value_definition = {}


class BGMIntEthPDU30043:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30043
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class RemHvBattHeatgTarTFromAC:
        comments = "底层软件需配置信号路由；"
        factor = 0.5
        initial_value = -40
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = -40
        signal_description = "远程电池目标加热温度"
        signal_length = 8
        start_position = 7
        value_definition = {}


class BGMIntEthPDU30044:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30044
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ReservedSigForTherm01:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "空调预留信息1"
        signal_length = 4
        start_position = 3
        value_definition = {}


class BGMIntEthPDU30045:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30045
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ReservedSigForTherm02:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "空调预留信息2"
        signal_length = 4
        start_position = 3
        value_definition = {}


class BGMIntEthPDU30046:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30046
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ReservedSigForTherm03:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "空调预留信息3"
        signal_length = 4
        start_position = 3
        value_definition = {}


class BGMIntEthPDU30047:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30047
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ReservedSigForTherm04:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "空调预留信息4"
        signal_length = 4
        start_position = 3
        value_definition = {}


class BGMIntEthPDU30048:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30048
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class ReservedSigForTherm05:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "空调预留信息5"
        signal_length = 4
        start_position = 3
        value_definition = {}


class BGMIntEthPDU30049:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 30049
    pdu_length_bytes = 7
    receiver = "SoC"
    send_type = "Cyclic-20ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'ScButtUpDnStpMidLe1ETH': ['ScButtUpDnStpMidLe1ETHScButtUpDnStp', 'ScButtUpDnStpMidLe1ETHUpDnSts', 'ScButtUpDnStpMidLe1ETHCntr', 'ScButtUpDnStpMidLe1ETHChks'], 'ScButtTypMidLe1ETH': ['ScButtTypMidLe1ETHTyp', 'ScButtTypMidLe1ETHCntr', 'ScButtTypMidLe1ETHChks']}

    class ScButtUpDnStpMidLe1ETHScButtUpDnStp:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘L2滚轮按键步进值"
        signal_length = 6
        start_position = 5
        value_definition = {}

    class ScButtUpDnStpMidLe1ETHUpDnSts:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘L2滚轮按键状态"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'UpDnSts_Not_Available', '0x1': 'UpDnSts_Up', '0x2': 'UpDnSts_Down', '0x3': 'UpDnSts_Error'}

    class ScButtUpDnStpMidLe1ETHCntr:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘L2滚轮按键Cntr"
        signal_length = 4
        start_position = 19
        value_definition = {}

    class ScButtUpDnStpMidLe1ETHChks:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘L2滚轮按键Chks"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class ScButtTypMidLe1ETHTyp:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘L2开关类型"
        signal_length = 1
        start_position = 32
        value_definition = {'0x0': 'Typ_Toggle', '0x1': 'Typ_Scroller'}

    class ScButtTypMidLe1ETHCntr:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘L2开关类型Cntr"
        signal_length = 4
        start_position = 43
        value_definition = {}

    class ScButtTypMidLe1ETHChks:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘L2开关类型Chks"
        signal_length = 8
        start_position = 55
        value_definition = {}


class BGMIntEthPDU30050:
    base_type = "unsigned"
    client_socket = "SocketSocTCPUp"
    pdu_header_id = 30050
    pdu_length_bytes = 7
    receiver = "SoC"
    send_type = "Cyclic-20ms"
    sender = "MCU"
    server_socket = "SocketMcuTCPUp"
    signal_group = {'ScButtUpDnStpMidRi1ETH': ['ScButtUpDnStpMidRi1ETHScButtUpDnStp', 'ScButtUpDnStpMidRi1ETHUpDnSts', 'ScButtUpDnStpMidRi1ETHCntr', 'ScButtUpDnStpMidRi1ETHChks'], 'ScButtTypMidRi1ETH': ['ScButtTypMidRi1ETHTyp', 'ScButtTypMidRi1ETHCntr', 'ScButtTypMidRi1ETHChks']}

    class ScButtUpDnStpMidRi1ETHScButtUpDnStp:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘R2滚轮按键步进值"
        signal_length = 6
        start_position = 5
        value_definition = {}

    class ScButtUpDnStpMidRi1ETHUpDnSts:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘R2滚轮按键状态"
        signal_length = 2
        start_position = 9
        value_definition = {'0x0': 'UpDnSts_Not_Available', '0x1': 'UpDnSts_Up', '0x2': 'UpDnSts_Down', '0x3': 'UpDnSts_Error'}

    class ScButtUpDnStpMidRi1ETHCntr:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘R2滚轮按键Cntr"
        signal_length = 4
        start_position = 19
        value_definition = {}

    class ScButtUpDnStpMidRi1ETHChks:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘R2滚轮按键Chks"
        signal_length = 8
        start_position = 31
        value_definition = {}

    class ScButtTypMidRi1ETHTyp:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘R2开关类型"
        signal_length = 1
        start_position = 32
        value_definition = {'0x0': 'Typ_Toggle', '0x1': 'Typ_Scroller'}

    class ScButtTypMidRi1ETHCntr:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘R2开关类型Cntr"
        signal_length = 4
        start_position = 43
        value_definition = {}

    class ScButtTypMidRi1ETHChks:
        comments = "MCU SWC发送"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "方向盘R2开关类型Chks"
        signal_length = 8
        start_position = 55
        value_definition = {}


class BGMIntEthPDU30051:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30051
    pdu_length_bytes = 3
    receiver = "MCU"
    send_type = "Cyclic-100ms"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {'DischrgnMntnDlyTi': ['DischrgnMntnDlyTiChrgnTmrhour', 'DischrgnMntnDlyTiChrgnTmrmin']}

    class DischrgnMntnDlyTiChrgnTmrhour:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 24
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "放电维持小时时间"
        signal_length = 8
        start_position = 7
        value_definition = {}

    class DischrgnMntnDlyTiChrgnTmrmin:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 60
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "放电维持分钟时间"
        signal_length = 8
        start_position = 15
        value_definition = {}

    class DischrgInCarSw:
        comments = "底层软件需配置信号路由；"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "Y"
        offset = 0
        signal_description = "车内放电开关状态"
        signal_length = 2
        start_position = 17
        value_definition = {'0x0': 'DisChrgrSW_Off', '0x1': 'DisChrgrSW_V2V', '0x2': 'DisChrgrSW_V2L'}


class BGMIntEthPDU30052:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30052
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class MobDevBtnTrReq:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 0
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "手机控制尾门动作"
        signal_length = 3
        start_position = 2
        value_definition = {'0x0': 'TrReq_Idle', '0x1': 'TrReq_Open', '0x2': 'TrReq_Close', '0x3': 'TrReq_Stop', '0x4': 'TrReq_Enable', '0x5': 'TrReq_Reserved1', '0x6': 'TrReq_Reserved2', '0x7': 'TrReq_Reserved3'}


class BGMIntEthPDU30053:
    base_type = "unsigned"
    client_socket = "SocketSocTCPDown"
    pdu_header_id = 30053
    pdu_length_bytes = 1
    receiver = "MCU"
    send_type = "Event Trigger"
    sender = "SoC"
    server_socket = "SocketMcuTCPDown"
    signal_group = {}

    class TrOpenPosnReqFromOutd:
        comments = "MCU SWC接收"
        factor = 1.0
        initial_value = 101
        layout_format = "Motorola MSB"
        mcu_routing = "N"
        offset = 0
        signal_description = "尾门开度外部请求"
        signal_length = 7
        start_position = 6
        value_definition = {}
