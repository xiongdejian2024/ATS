#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : ProtocolConfigData.py
#
#  ***********
#
#  ------------------------------------------------------------------
# @Time    : 2024/5/19 11:25
# @Author  : jiewen.deng
# Language: Python 3.9
#  ------------------------------------------------------------------
# Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.

from collections import namedtuple


class ProtocolResponseConfigData:
    # uds否定响应为0x78特殊类型的获取肯定响应的超时时间(s)
    uds_ne_code_time_out = 5

    # uds当接收连续帧的数据，没有接收完成所允许的最大时间(s)
    uds_get_full_message_time_out = 10

    # uds获取服务返回数据超时时间(s)
    uds_get_call_message_time_out = 10

    # uds获取服务返回间隔时间(s)
    uds_get_call_message_interval_time = 0.05


defaultRawDataFDA0 = [12, 132, 26, 13, 0, 0, 10, 90, 110, 125, 162,
                      166, 168, 180, 90, 110, 125, 155, 158, 161,
                      170, 0, 160, 3, 232, 6, 64, 100, 1, 64, 60,
                      0, 32, 0, 1, 144, 1, 144, 1, 144, 20, 0, 30,
                      50, 0, 25, 12, 128, 200, 6, 64, 50, 25, 0,
                      90, 7, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50,
                      25, 0, 100, 8, 32, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 50, 25, 0, 100, 8, 32, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 50, 25, 0, 100, 8, 32, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 50, 25, 0, 100, 8, 32, 0, 0, 0, 0,
                      0, 0, 0, 0, 10, 240, 30, 68, 40, 24, 6, 64, 3,
                      240, 0, 0, 54, 238, 118, 6, 64, 7, 158, 60, 0,
                      180, 0, 192, 6, 64, 10, 4, 176, 50, 18, 176, 20,
                      10, 1, 3, 10, 40, 0, 0, 1, 232, 0, 0, 0, 0, 0, 128,
                      254, 0, 0, 0, 0, 0, 0, 128, 0, 161, 80, 0, 1, 61,
                      224, 2, 128, 10, 128, 10, 131, 231, 0, 161, 0, 0,
                      24, 6, 64, 3, 192, 0, 0, 54, 238, 118, 254, 0, 0,
                      0, 0, 0, 131, 121, 30, 1, 56, 128, 120, 120, 15,
                      60, 15, 160, 6, 5, 40, 20, 2, 4, 1, 24, 105, 241,
                      134, 159, 17, 2, 136, 15, 156, 20, 20, 0, 0, 160,
                      2, 0, 32, 2, 0, 160, 10, 30, 0, 160, 10, 3, 192,
                      75, 20, 3, 32, 100, 3, 33, 144, 6, 64, 130, 3, 33,
                      144, 6, 64, 130, 12, 4, 20, 20, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

uds_service_data = namedtuple('uds_service_data', ['raw_data', 'extends_data', 'seq_num'])

_uds_service_data_with_30 = {
    "ServiceID": 0x30,
    "DtcCode": 0xffffff,
    "Result": 1
}

_uds_service_custom_data = {

}

_uds_service_data_with_28 = {
    "ServiceID": 0x28,
    "ControlType": 1,
    "CommunicationType": 1
}

_uds_service_data_with_36 = {
    "ServiceID": 0x36,
    "BlockSequenceCounter": 1,
    "TransferData": b'\x01\x02\x03\x04\x01\x02\x03\x04\x05\x06\x07\x08\x05\x06\x07\x08\x01\x02\x03\x04'
                    b'\x01\x02\x03\x04\x05\x06\x07\x08\x05\x06\x07\x08\x01\x02\x03\x04\x01\x02\x03\x04'
                    b'\x01\x02\x03\x04\x01\x02\x03\x04\x05\x06\x07\x08\x05\x06\x07\x08\x01\x02\x03\x04'
                    b'\x01\x02\x03\x04\x05\x06\x07\x08\x05\x06\x07\x08\x01\x02\x03\x04\x01\x02\x03\x04'
}

_uds_service_data_with_76 = {
    "ServiceID": 0x76,
    "BlockSequenceCounter": 1,
    "TransferData": b'\x01\x02\x03\x04\x01\x02\x03\x04\x05\x06\x07\x08\x05\x06\x07\x08\x01\x02\x03\x04'
}

_uds_service_data_with_74 = {
    "ServiceID": 0x74,
    "DataLenInfo": {
        "MaxDataSize": 2,
        "Retain": 0
    },
    "MaxDataValue": b'\x00\x12'
}

_uds_service_data_with_34 = {
    "ServiceID": 0x34,
    "DataFormatIdentifier": {
        "CompressionMethod": 0,
        "EncryptingMethod": 0
    },
    "IdentifierInfo": {
        "DataLength": 4,
        "AddrLength": 4
    },
    "AddrInfo": b'\x80\x08\x00\x00',
    "DataInfo": b'\x00\x18\x00\x00'
}

_uds_service_data_with_75 = {
    "ServiceID": 0x75,
    "DataLenInfo": {
        "MaxDataSize": 2,
        "Retain": 0
    },
    "MaxDataValue": b'\x01\x02'
}

_uds_service_data_with_35 = {
    "ServiceID": 0x35,
    "DataFormatIdentifier": {
        "CompressionMethod": 0,
        "EncryptingMethod": 0
    },
    "IdentifierInfo": {
        "DataLength": 4,
        "AddrLength": 4
    },
    "AddrInfo": b'\x80\x08\x00\x00',
    "DataInfo": b'\x00\x18\x00\x00'
}

_uds_service_data_with_10 = {
    "ServiceID": 0x10,
    "SubFunction": 1,
}

_uds_service_data_with_37 = {
    "ServiceID": 0x37,
    "TransferData": b'',
}

_uds_service_data_with_77 = {
    "ServiceID": 0x77,
    "TransferData": b'',
}

_uds_service_data_with_85 = {
    "ServiceID": 0x85,
    "SubFunction": 1,
}

_uds_service_data_with_31 = {
    "ServiceID": 0x31,
    "routineControlType": 1,
    "routineIdentifier": 0x0101,
    "routineControlOptionRecord": b'',
}

_uds_service_data_with_19 = {
    "ServiceID": 0x19,
    "SubFunction": 10,
    "DidInfo": 0x111111,
    "DtcMask": {
        "WarningIndicatorRequested": 1,
        "TestNotCompletedThisOperationCycle": 1,
        "TestFailedSinceLastClear": 1,
        "TestNotCompletedSinceLastClear": 1,
        "ConfirmedDTC": 1,
        "PendingDTC": 1,
        "TestFailedThisOperationCycle": 1,
        "TestFailed": 1,
    },
}

_uds_service_data_with_50 = {
    "ServiceID": 0x50,
    "SubFunction": 2,
}

_uds_service_data_with_7F = {
    "ServiceID": 0x7F,
    "SubFunction": 2,
    "NCR": 0x10
}

_uds_service_data_with_3E = {
    "ServiceID": 0x3E,
    "SubFunction": 0x80
}

_uds_service_data_with_22 = {
    "ServiceID": 0x22,
    "DataIdentifier": 61876
}

_uds_service_data_with_27 = {
    "ServiceID": 0x27,
    "SubFunction": 0x01,
    "SecretKey": b''
}

_uds_service_data_with_14 = {
    "ServiceID": 0x14,
    "OpDTC": b'\xff\xff\xff'
}

_uds_service_data_with_2f = {
    "ServiceID": 0x2f,
    "DID": 0x010a,
    "IOType": 3,
    "BriefData": {
        "Subfunction": 0x01,
    }
}

_uds_service_data_with_6E = {
    "ServiceID": 0x6E,
    "DataIdentifier": 0x0123,
}

_uds_service_data_with_67 = {
    "ServiceID": 0x67,
    "SubFunction": 0x05,
    "SecretKey": b"\x08'\x11\xf0",
}

_uds_service_data_with_2e = {
    "ServiceID": 0x2E,
    "DataIdentifier": 0x010A,
    "DataIdData": b'\x01\x02\x03\x04\x01\x02\x03\x04\x01\x02\x03\x04'
}

_uds_service_data_with_11 = {
    "ServiceID": 0x11,
    "SubFunction": 0x01
}

_obd_service_data_with_01 = {
    "ServiceID": 0x01,
    "SubFunction": 0x00
}

_obd_service_data_with_02 = {
    "ServiceID": 0x2,
    "SubFunction": 0x00,
    "Frame": 0x00
}

_obd_service_data_with_03 = {
    "ServiceID": 0x3
}

_obd_service_data_with_04 = {
    "ServiceID": 0x4
}

_obd_service_data_with_06 = {
    "ServiceID": 0x6
}

_obd_service_data_with_07 = {
    "ServiceID": 0x7
}

_obd_service_data_with_08 = {
    "ServiceID": 0x8,
    "TID": 0x8,
}

_obd_service_data_with_09 = {
    "ServiceID": 0x9,
    "InfoType": 0x2,
}

fr_tp_frame_raw_data = {
    "TargetAddress": b"\x16\x01",
    "SourceAddress": b"\x0E\x80",
    "FrameType": {
        "C_PCIType": 0x4,
        "Ctr_Status": 0x0,
    },
    "MessageInfo": {
        "EffectiveLength": 0x2,
        "MaximumLoad": 0x2
    },
    "RawData": b"\x10\x03"
}

fr_tp_flow_control_frame_raw_data = {
    "TargetAddress": b"\x16\x01",
    "SourceAddress": b"\x0E\x80",
    "FrameType": {
        "C_PCIType": 0x8,
        "Ctr_Status": 0x3,
    },
    "MessageInfo": {
        "BC": 0x0,
        "BFS": 0xffff
    }
}

update_doip_service_data = {
    0x0000: [],
    0x0001: [],
    0x0002: [],
    0x0003: [],
    0x0004: [],
    0x0005: [],
    0x0006: [],
    0x0007: [],
    0x0008: [],
    0x8001: [],
    0x8002: [],
    0x8003: [],
    0x4001: [],
    0x4002: [],
    0x4003: [],
    0x4004: [],
}

doip_frame_raw_data_0x0000 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x0000,
    "DataLen": 0,
    "DataInfo": 0
}

doip_frame_raw_data_0x0001 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x0001,
    "DataLen": 0,
    "DataInfo": 0
}

doip_frame_raw_data_0x0007 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x0007,
    "DataLen": 0,
    "DataInfo": 0
}

doip_frame_raw_data_0x4001 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x4001,
    "DataLen": 0,
    "DataInfo": 0
}

doip_frame_raw_data_0x4003 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x4003,
    "DataLen": 0,
    "DataInfo": 0
}

doip_frame_raw_data_0x0002 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x0002,
    "DataLen": 6,
    "DataInfo": bytes.fromhex("000000000001"),
}

doip_frame_raw_data_0x0003 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x0003,
    "DataLen": 17,
    "DataInfo": "LSTEST6R9F2086669",
}

doip_frame_raw_data_0x0004 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x0004,
    "DataLen": 32,
    "DataInfo": {
        'Vin': "LSTEST6R9F2086669",
        'LogicalAddress': 0x1001,
        'EID': bytes.fromhex("020000001011"),
        'GID': bytes.fromhex("000000000001"),
        'FurtherActionRequired': 0,
    },
}

doip_frame_raw_data_0x0005 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x0005,
    "DataLen": 7,
    "DataInfo": {
        'SourceAddress': 0x0e80,
        'ActivationType': 0,
        'ReservedForISO': b'\x00\x00\x00\x00'
    },
}

doip_frame_raw_data_0x0006 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x0006,
    "DataLen": 9,
    "DataInfo": {
        'TargetAddress': 0x0e80,
        'SourceAddress': 0x1401,
        'ResCode': 16,
        'ReservedForISO': b'\x00\x00\x00\x00'
    },
}

doip_frame_raw_data_0x0008 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x0008,
    "DataLen": 2,
    "DataInfo": 0x0e80,
}

doip_frame_raw_data_0x8001 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x8001,
    "DataLen": 7,
    "DataInfo": {
        'SourceAddress': 0x0e80,
        'TargetAddress': 0x1002,
        'DiagData': b'\x22\xD1\x35'
    },
}

doip_frame_raw_data_0x8002 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x8002,
    "DataLen": 5,
    "DataInfo": {
        'TargetAddress': 0x1001,
        'SourceAddress': 0x1401,
        'ReturnCode': 0
    },
}

doip_frame_raw_data_0x8003 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x8003,
    "DataLen": 5,
    "DataInfo": {
        'TargetAddress': 0x1001,
        'SourceAddress': 0x1401,
        'NRCCode': 4
    },
}

doip_frame_raw_data_0x4002 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x4002,
    "DataLen": 3,
    "DataInfo": {
        'NodeType': 0,
        'TCP_DATA_MAX_NUMBER': 10,
        'NOW_TCP_DATA_OPEN_NUMBER': 5
    },
}

doip_frame_raw_data_0x4004 = {
    "ProtocolVersion": 2,
    "ProtocolVersionCrc": 0xFD,
    "DataType": 0x4004,
    "DataLen": 1,
    "DataInfo": 1,
}

uds_single_frame_raw_data = {
    "MessageInfo": {
        "NameType": 0,
        "FrameLen": 4
    }
}

uds_multi_frame_raw_data = {
    "MessageInfo": {
        "NameType": 1,
        "FrameLen": 13
    },
    "ConSecutiveInfo": [
        {
            "NameType": 2,
            "SequenceNumber": 1
        },
    ]
}

_uds_flow_control_frame_data = {
    "MessageInfo": {
        "NameType": 3,
        "FlowStatus": 0
    },
    "BlockSize": 0,
    "STmin": 0x01,
    "Reserved": b'\xcc\xcc\xcc\xcc\xcc'
}

doip_req_to_res_map = {
    0x0001: [0x0000, 0x0004],
    0x0002: [0x0000, 0x0004],
    0x0003: [0x0000, 0x0004],
    0x0005: [0x0000, 0x0006],
    0x0007: [0x0000, 0x0008],
    0x8001: [0x0000, 0x8001, 0x8002, 0x8003],
    0x4001: [0x0000, 0x4002],
    0x4003: [0x0000, 0x4004],
}

uds_service_data_with_11 = uds_service_data(_uds_service_data_with_11, None, None)
uds_service_data_with_2e = uds_service_data(_uds_service_data_with_2e, None, None)
uds_service_data_with_67 = uds_service_data(_uds_service_data_with_67, None, None)
uds_service_data_with_6E = uds_service_data(_uds_service_data_with_6E, None, None)
uds_service_data_with_2f = uds_service_data(_uds_service_data_with_2f, None, None)
uds_service_data_with_14 = uds_service_data(_uds_service_data_with_14, None, None)
uds_service_data_with_27 = uds_service_data(_uds_service_data_with_27, None, None)
uds_service_data_with_22 = uds_service_data(_uds_service_data_with_22, None, None)
uds_service_data_with_3E = uds_service_data(_uds_service_data_with_3E, None, None)
uds_service_data_with_7F = uds_service_data(_uds_service_data_with_7F, None, None)
uds_service_data_with_50 = uds_service_data(_uds_service_data_with_50, None, None)
uds_service_data_with_19 = uds_service_data(_uds_service_data_with_19, None, None)
uds_service_data_with_31 = uds_service_data(_uds_service_data_with_31, None, None)
uds_service_data_with_85 = uds_service_data(_uds_service_data_with_85, None, None)
uds_service_data_with_77 = uds_service_data(_uds_service_data_with_77, None, None)
uds_service_data_with_37 = uds_service_data(_uds_service_data_with_37, None, None)
uds_service_data_with_10 = uds_service_data(_uds_service_data_with_10, None, None)
uds_service_data_with_35 = uds_service_data(_uds_service_data_with_35, None, None)
uds_service_data_with_75 = uds_service_data(_uds_service_data_with_75, None, None)
uds_service_data_with_34 = uds_service_data(_uds_service_data_with_34, None, None)
uds_service_data_with_74 = uds_service_data(_uds_service_data_with_74, None, None)
uds_service_data_with_76 = uds_service_data(_uds_service_data_with_76, None, None)
uds_service_data_with_36 = uds_service_data(_uds_service_data_with_36, None, None)
uds_service_data_with_28 = uds_service_data(_uds_service_data_with_28, None, None)
uds_service_data_with_30 = uds_service_data(_uds_service_data_with_30, None, None)
uds_service_custom_data = uds_service_data(_uds_service_custom_data, None, None)
uds_flow_control_frame_data = uds_service_data(_uds_flow_control_frame_data, None, None)

obd_service_data_with_01 = uds_service_data(_obd_service_data_with_01, None, None)
obd_service_data_with_02 = uds_service_data(_obd_service_data_with_02, None, None)
obd_service_data_with_03 = uds_service_data(_obd_service_data_with_03, None, None)
obd_service_data_with_04 = uds_service_data(_obd_service_data_with_04, None, None)
obd_service_data_with_06 = uds_service_data(_obd_service_data_with_06, None, None)
obd_service_data_with_07 = uds_service_data(_obd_service_data_with_07, None, None)
obd_service_data_with_08 = uds_service_data(_obd_service_data_with_08, None, None)
obd_service_data_with_09 = uds_service_data(_obd_service_data_with_09, None, None)

negative_response_data = {
    0x10: "GeneralReject",
    0x11: "ServiceNotSupport",
    0x12: "SubFunctionNotSupported",
    0x13: "IncorrectMessageLength",
    0x22: "ConditionsNotCorrect",
    0x24: "RequestSequenceError",
    0x31: "RequestOutOfRange",
    0x33: "SecurityAccessDenied",
    0x35: "InvalidKey",
    0x36: "ExceedNumberOfAttempts",
    0x37: "RequiredTimeDelayNotExpired",
    0x71: "TransferDataSuspended",
    0x72: "GeneralProgrammingFailure",
    0x73: "WrongBlockSequenceCounter",
    0x78: "WaitingHandleSuccess",
    0x7E: "SubFunctionNotSupportedInActiveSession",
    0x7F: "ServiceNotSupportedInActiveSession",
}

data_ids = {
    "ABM1": 0x003A,
    "ABS3": 0x0028,
    "ACC3_ACC_FD2": 0x0056,
    "ACC4_ACC_FD2": 0x0057,
    "ACC6_ACC_FD2": 0x0058,
    "ACC7_ACC_FD2": 0x0059,
    "ACC8_ACC_FD2": 0x006D,
    "AEB2_AEB_FD2": 0x005B,
    "AEB3_AEB_FD2": 0x005C,
    # "BMS4": ,
    "DCT7": 0x0025,
    # "DHT_FD1": ,
    "EPB1": 0x002A,
    "EPS_FD1": 0x0035,
    "EPS1": 0x0035,
    "ABS3_ESP_FD2": 0x0028,
    "ESP1_ESP_FD2": 0x002B,
    "ESP2_ESP_FD2": 0x002C,
    "ESP1": 0x002B,
    "ESP2": 0x002C,
    "HC1": 0x0060,
    # "HCU_HP5": ,
    # "HCU_PT4": ,
    # "HCU_PT7": ,
    "HUT_IP2": 0x00E2,
    "HUT32": 0x0040,
    "IFC3_IFC_FD2": 0x004F,
    "IFC4_IFC_FD2": 0x0050,
    "IFC5_IFC_FD2": 0x0051,
    "IFC6_IFC_FD2": 0x0052,
}

dtc_infos = {
    0x980016: "电瓶电压故障",
    0x980017: "电瓶电压故障",
    0x980119: "USB1 接口电路过电流",
    0x980348: "MMI高温（IHU温度过高）",
    0x980441: "MCU和R5通讯故障",
    0x980504: "收音电路控制故障（读I2C故障）",
    0x980511: "收音天线异常",
    0x980513: "收音天线异常",
    0x980644: "存储器读写故障",
    0x980985: "速度信号不正常",
    0x981000: "TBOX Connection Fault(USB )",
    0x98161A: "前左扬声器故障-短路(AMP)",
    0x981613: "前左扬声器故障-连接断开(AMP)",
    0x98171A: "前右扬声器故障-短路(AMP)",
    0x981713: "前右扬声器故障-连接断开(AMP)",
    0x98181A: "后左扬声器故障-短路(AMP)",
    0x981813: "后左扬声器-连接断开(AMP)",
    0x98191A: "后右扬声器故障-短路(AMP)",
    0x981913: "后右扬声器-连接断开",
    0x981A1A: "左环绕扬声器故障-短路(AMP)",
    0x981A13: "左环绕扬声器-连接断开",
    0x981B1A: "右环绕扬声器故障-短路(AMP)",
    0x981B13: "右环绕扬声器-连接断开",
    0x981C1A: "左露营扬声器故障-短路(AMP)",
    0x981C13: "左露营扬声器-连接断开",
    0x981D1A: "右露营扬声器故障-短路(AMP)",
    0x981D13: "右露营扬声器-连接断开",
    0x981E1A: "低音炮1故障-短路(AMP)",
    0x981E13: "低音炮1-连接断开",
    0x981F1A: "低音炮2故障-短路(AMP)",
    0x981F13: "低音炮2-连接断开",
    0x98201A: "中置扬声器故障-短路(AMP)",
    0x982013: "中置扬声器-连接断开",
    0x982131: "外置功放内部故障TDA7803_1 I2C故障",
    0x982196: "外置功放内部故障TDA7803_1 PLL 故障",
    0x982193: "外置功放内部故障TDA7803_1 初始化失败故障",
    0x982198: "外置功放内部故障TDA7803_1温度过高故障",
    0x982231: "外置功放内部故障TDA7803_2 I2C故障",
    0x982296: "外置功放内部故障TDA7803_2 PLL 故障",
    0x982293: "外置功放内部故障TDA7803_2 初始化失败故障",
    0x982298: "外置功放内部故障TDA7803_2温度过高故障",
    0x982331: "外置功放内部故障TDA7803_3 I2C故障",
    0x982396: "外置功放内部故障TDA7803_3 PLL 故障",
    0x982393: "外置功放内部故障TDA7803_3 初始化失败故障",
    0x982398: "外置功放内部故障TDA7803_3温度过高故障",
    0x982496: "外置功放内部故障DSP工作异常故障",
    0x981831: "A2B失去通讯",
    0x983000: "中控显示屏整体功能",
    0x983003: "中控显示屏与主机I2C通信异常故障",
    0x983004: "中控显示屏未开机",
    0x983029: "中控屏-视频信号异常故障",
    0x983196: "中控显示屏背光功能状态故障",
    0x983198: "中控显示屏背光温度高",
    0x983191: "中控显示屏背光亮度值异常",
    0x983296: "中控显示功能状态故障",
    0x983316: "中控显示屏供电-欠压",
    0x983317: "中控显示屏供电-过压",
    0x983496: "中控屏-触摸功能异常故障",
    0x983413: "与中控屏LVDS通讯丢失",
    0x983513: "MIC2连接异常",
    0x983696: "DSP故障",
    0x983796: "Apple鉴权故障",
    0x983896: "BT或WIFI故障",
    0x983996: "与TOX通讯音频相关的故障",
    0x983A96: "降噪FM1388故障",
    0x983B96: "以太网故障",
    0x983C96: "AHD单摄像头（RVC）故障",
    0x983C13: "AHD单摄像头（RVC）通讯故障",
    0x983D96: "OMS（DVR）摄像头故障",
    0x983D13: "OMS（DVR）摄像头通讯故障",
    0x983E96: "DMS摄像头故障",
    0x983E13: "DMS摄像头通讯故障",
    0x983F96: "AHD-AVM摄像头故障",
    0x984013: "AHD-AVM摄像头（前）故障",
    0x984113: "AHD-AVM摄像头（后）故障",
    0x984213: "AHD-AVM摄像头（左）故障",
    0x984313: "AHD-AVM摄像头（右）故障",
    0x985013: "LIN1通讯故障",
    0x985113: "LIN2通讯故障",
    0xC15231: "与雷达MCU失去通讯",
    0x910000: "仪表显示屏整体功能",
    0x910003: "仪表显示屏与主机I2C通信异常故障",
    0x910004: "仪表显示屏未开机",
    0x910029: "仪表显示屏-视频信号异常故障",
    0x91011B: "燃油传感器开路故障",
    0x91011A: "燃油传感器短路故障",
    0x910296: "仪表显示屏背光功能状态故障",
    0x910298: "仪表显示屏背光温度高",
    0x910291: "仪表显示屏背光亮度值异常",
    0x910396: "仪表显示屏功能状态故障",
    0x910416: "仪表显示屏供电-欠压",
    0x910417: "仪表显示屏供电-过压",
    0x910813: "与仪表屏LVDS通讯丢失",
    0xD11387: "Limphome mode",
    0xC00100: "高速CAN通讯线路故障",
    0xC07688: "Control Module Communication Bus Off（InfoCAN）",
    0xC14087: "与车身控制器失去通讯",
    0xC10387: "与电子换挡模块失去通讯",
    0xC12687: "与转角传感器失去通信",
    0xC13187: "与电动助力转向控制器失去通讯",
    0xC15187: "与气囊控制器失去通讯",
    0xC16487: "与空调控制器失去通讯",
    0xC23087: "与电动尾门失去通讯",
    0xC10087: "与发动机控制器失去通讯",
    0xC10187: "与变速箱控制器失去通讯",
    0xC12987: "与制动系统控制器失去通讯",
    0xD10487: "与单目摄像头失去通讯",
    0xD10A87: "与PM2.5失去通讯与PM2.5模块失去通讯",
    0xD10B87: "与WCM失去通讯与无线充电模块失去通讯",
    0xD11A87: "与WCM2失去通讯与无线充电模块2失去通讯",
    0xC14987: "与CGM Info CAN通信丢失",
    0xC19887: "与TBOX失去通讯(CAN)",
    0xD11487: "与MFL失去通讯",
    0xD11587: "与自动泊车辅助失去通讯",
    0xD11687: "与驾驶员座椅控制模块失去通讯",
    0xD11787: "与座椅加热通风模块失去通讯",
    0xD11887: "与近距离无线通讯模块失去通讯",
    0xD30055: "软件配置错误",
    0xC14687: "网关节点丢失",
    0xC24587: "娱乐主机节点丢失",
    0xD12187: "ESP报文丢失",
    0xD15987: "驻车雷达控制单元报文丢失",
    0xD16487: "空调控制器报文丢失",
    0xD14087: "车身控制单元1报文丢失",
    0xD19987: "左前门模块报文丢失",
    0xD20087: "右前门模块报文丢失",
    0xD20187: "左后门模块报文丢失",
    0xD20287: "右后门模块报文丢失",
    0xD21287: "转向柱调节控制单元报文丢失",
    0xD10087: "发动机控制单元报文丢失",
    0xD10187: "变速箱控制单元报文丢失",
    0xD23087: "后背门控制单元报文丢失",
    0xD14687: "网关控制单元报文丢失",
    0x944300: "LCD screen fault detection",
    0x94424B: "High temperature of system",
}
