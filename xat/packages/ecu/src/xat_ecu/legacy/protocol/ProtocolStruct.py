#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File    : protocol_struct.py
#
#  ***********
#
#  ------------------------------------------------------------------
# @Time    : 2024/5/19 1:12
# @Author  : jiewen.deng
# Language: Python 3.9
#  ------------------------------------------------------------------
# Copyright (C) 2023-2024 jidu automotive technologies CO.,LTD.

from construct import *


class InitStruct(object):
    uds_service_with_0x67_len = 4
    uds_service_with_0x59_len = None
    uds_service_with_0x62_len = None
    uds_service_with_0x2e_len = None
    uds_service_with_0x27_len = None
    uds_service_with_0x36_len = None
    uds_service_with_0x76_len = 0
    uds_service_with_0x14_len = 3
    uds_service_with_muilt_count = None
    uds_service_with_0x37_len = None
    uds_service_with_0x77_len = None
    uds_service_with_0x46_len = None
    uds_service_with_0x31_len = None
    uds_service_with_0x71_len = None

    def __init__(self):
        pass


uds_frame_struct_with_0x59 = Struct(
    "ServiceID" /
    Int8ub,
    "SubFunction" /
    Int8ub,
    "DtcMask" /
    BitStruct(
        "WarningIndicatorRequested" /
        BitsInteger(1),
        "TestNotCompletedThisOperationCycle" /
        BitsInteger(1),
        "TestFailedSinceLastClear" /
        BitsInteger(1),
        "TestNotCompletedSinceLastClear" /
        BitsInteger(1),
        "ConfirmedDTC" /
        BitsInteger(1),
        "PendingDTC" /
        BitsInteger(1),
        "TestFailedThisOperationCycle" /
        BitsInteger(1),
        "TestFailed" /
        BitsInteger(1),
    ),
    "ConSecutiveInfo" / Switch(this.SubFunction, {
        0x2: Array(lambda this: InitStruct.uds_service_with_0x59_len, Struct(
            "DTCInfo" / Int24ub,
            "DTCStatus" / Int8ub,
        )
        ),
        0x1: Bytes(lambda this: InitStruct.uds_service_with_0x59_len),
        0x4: Bytes(lambda this: InitStruct.uds_service_with_0x59_len),
        0x6: Bytes(lambda this: InitStruct.uds_service_with_0x59_len),
        0xA: Array(lambda this: InitStruct.uds_service_with_0x59_len, Struct(
            "DTCInfo" / Int24ub,
            "DTCStatus" / Int8ub,
        )
        ),
    })

)

uds_frame_struct_with_0x10 = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub
)

uds_frame_struct_with_0x14 = Struct(
    "ServiceID" / Int8ub,
    "OpDTC" / Bytes(lambda this: InitStruct.uds_service_with_0x14_len)
)

uds_frame_struct_with_0x54 = Struct(
    "ServiceID" / Int8ub,
    "OpDTC" / Int24ub,
)

uds_frame_struct_with_0x50 = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub
)

uds_frame_struct_with_0x85 = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub
)

uds_frame_struct_with_0xc5 = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub
)

uds_frame_struct_with_0x2f = Struct(
    "ServiceID" / Int8ub,
    "DID" / Int16ub,
    "IOType" / Int8ub,
    "BriefData" / If(this.IOType == 3, Struct(
        "Subfunction" / Int8ub
    ))
)

uds_frame_struct_with_0x6f = Struct(
    "ServiceID" / Int8ub,
    "DID" / Int16ub,
    "IOType" / Int8ub,
    "BriefData" / If(this.IOType == 3, Struct(
        "Subfunction" / Int8ub
    ))
)

uds_frame_struct_with_0x34 = Struct(
    "ServiceID" / Int8ub,
    "DataFormatIdentifier" / BitStruct(
        "CompressionMethod" / BitsInteger(4),
        "EncryptingMethod" / BitsInteger(4),
    ),
    "IdentifierInfo" / BitStruct(
        "DataLength" / BitsInteger(4),
        "AddrLength" / BitsInteger(4),
    ),
    "AddrInfo" / Bytes(this.IdentifierInfo.AddrLength),
    "DataInfo" / Bytes(this.IdentifierInfo.DataLength),
)

#2：lengthFormatIdentifier，高四位表示参数maxNumberOfBlockLength的长度，低四位为保留位。
#3...：maxNumberOfBlockLength，表示用户每次传输数据的请求中包含的最大字节数。
uds_frame_struct_with_0x74 = Struct(
    "ServiceID" / Int8ub,
    "DataLenInfo" / BitStruct(
        "MaxDataSize" / BitsInteger(4),
        "Retain" / BitsInteger(4),
    ),
    "MaxDataValue" / Bytes(this.DataLenInfo.MaxDataSize)
)

uds_frame_struct_with_0x35 = Struct(
    "ServiceID" / Int8ub,
    "DataFormatIdentifier" / BitStruct(
        "CompressionMethod" / BitsInteger(4),
        "EncryptingMethod" / BitsInteger(4),
    ),
    "IdentifierInfo" / BitStruct(
        "DataLength" / BitsInteger(4),
        "AddrLength" / BitsInteger(4),
    ),
    "AddrInfo" / Bytes(this.IdentifierInfo.AddrLength),
    "DataInfo" / Bytes(this.IdentifierInfo.DataLength),
)

uds_frame_struct_with_0x75 = Struct(
    "ServiceID" / Int8ub,
    "DataLenInfo" / BitStruct(
        "MaxDataSize" / BitsInteger(4),
        "Retain" / BitsInteger(4),
    ),
    "MaxDataValue" / Bytes(this.DataLenInfo.MaxDataSize)
)

uds_frame_struct_with_0x36 = Struct(
    "ServiceID" / Int8ub,
    "BlockSequenceCounter" / Int8ub,
    "TransferData" / Bytes(lambda this: InitStruct.uds_service_with_0x36_len)
)

uds_frame_struct_with_0x31 = Struct(
    "ServiceID" / Int8ub,
    # 01：startRoutine（启动程序）;02：stopRoutine（停止程序）;03：requestRoutineResults（请求程序的运行结果）
    "routineControlType" / Int8ub,
    "routineIdentifier" / Int16ub,
    "routineControlOptionRecord" / \
    Bytes(lambda this: InitStruct.uds_service_with_0x31_len)
)

uds_frame_struct_with_0x71 = Struct(
    "ServiceID" / Int8ub,
    # 01：startRoutine（启动程序）;02：stopRoutine（停止程序）;03：requestRoutineResults（请求程序的运行结果）
    "routineControlType" / Int8ub,
    "routineIdentifier" / Int16ub,
    "routineControlOptionRecord" / \
    Bytes(lambda this: InitStruct.uds_service_with_0x71_len)
)

uds_frame_struct_with_0x37 = Struct(
    "ServiceID" / Int8ub,
    "TransferData" / Bytes(lambda this: InitStruct.uds_service_with_0x37_len)
)

uds_frame_struct_with_0x77 = Struct(
    "ServiceID" / Int8ub,
    "TransferData" / Bytes(lambda this: InitStruct.uds_service_with_0x77_len)
)

uds_frame_struct_with_0x76 = Struct(
    "ServiceID" / Int8ub,
    "BlockSequenceCounter" / Int8ub,
    "TransferData" / Bytes(lambda this: InitStruct.uds_service_with_0x76_len)
)

uds_frame_struct_with_0x7f = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub,
    "NCR" / Int8ub
)

uds_frame_struct_with_0x3e = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub
)

uds_frame_struct_with_0x7e = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub
)

uds_frame_struct_with_0x28 = Struct(
    "ServiceID" / Int8ub,
    "ControlType" / Int8ub,
    "CommunicationType" / Int8ub
)

uds_frame_struct_with_0x68 = Struct(
    "ServiceID" / Int8ub,
    "ControlTypeResult" / Int8ub
)

uds_frame_struct_with_0x11 = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub,
)

uds_frame_struct_with_0x51 = Struct(
    "ServiceID" / Int8ub,
    "PositiveResponseServiceID" / Int8ub,
    "SubFunctionResetType" / Int8ub
)

uds_frame_struct_with_0x27 = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub,
    "SecretKey" / Bytes(lambda this: InitStruct.uds_service_with_0x27_len)
)

uds_frame_struct_with_0x67 = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub,
    "SecretKey" / Bytes(lambda this: InitStruct.uds_service_with_0x67_len)
)

uds_frame_struct_with_0x22 = Struct(
    "ServiceID" / Int8ub,
    "DataIdentifier" / Int16ub
)

uds_frame_struct_with_0x30 = Struct(
    "ServiceID" / Int8ub,
    "DtcCode" / Int24ub,
    "Result" / Int8ub
)

uds_frame_struct_with_0x70 = Struct(
    "ServiceID" / Int8ub,
    "DtcCode" / Int24ub
)

uds_frame_struct_with_0x62 = Struct(
    "ServiceID" / Int8ub,
    "DataIdentifier" / Int16ub,
    "DataIdData" / Bytes(lambda this: InitStruct.uds_service_with_0x62_len)
)

uds_frame_struct_with_0x2e = Struct(
    "ServiceID" / Int8ub,
    "DataIdentifier" / Int16ub,
    "DataIdData" / Bytes(lambda this: InitStruct.uds_service_with_0x2e_len)
)

uds_frame_struct_with_0x6e = Struct(
    "ServiceID" / Int8ub,
    "DataIdentifier" / Int16ub
)

uds_frame_struct_with_0x19 = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub,
    "DidInfo" / If(this.SubFunction == 0x1 | this.SubFunction == 0x2 | this.SubFunction == 0x4 | this.SubFunction == 0x6, Int24ub),
    "DtcMask" / If(this.SubFunction != 0xA, BitStruct(
        "WarningIndicatorRequested" / BitsInteger(1),
        "TestNotCompletedThisOperationCycle" / BitsInteger(1),
        "TestFailedSinceLastClear" / BitsInteger(1),
        "TestNotCompletedSinceLastClear" / BitsInteger(1),
        "ConfirmedDTC" / BitsInteger(1),
        "PendingDTC" / BitsInteger(1),
        "TestFailedThisOperationCycle" / BitsInteger(1),
        "TestFailed" / BitsInteger(1),
    )
    ),
)

uds_single_frame_raw_struct = Struct(
    "MessageInfo" / BitStruct(
        "NameType" / BitsInteger(4),
        "FrameLen" / BitsInteger(4)
    )
)

uds_multi_frame_raw_struct = Array(
    lambda this: InitStruct.uds_service_with_muilt_count,
    Struct(
        "MessageInfo" /
        BitStruct(
            "NameType" /
            BitsInteger(4),
            "FrameLen" /
            BitsInteger(12)),
        "ConSecutiveInfo" /
        Array(
            lambda this: (
                this.MessageInfo.FrameLen -
                6) //
            7 if (
                this.MessageInfo.FrameLen -
                6) %
            7 == 0 else (
                this.MessageInfo.FrameLen -
                6) //
            7 +
            1,
            BitStruct(
                "NameType" /
                BitsInteger(4),
                "SequenceNumber" /
                BitsInteger(4)))))

uds_flow_control_frame_struct = Struct(
    "MessageInfo" / BitStruct(
        "NameType" / BitsInteger(4),
        # 0：CTS，代表发送者可以正常发送； 1， WT 代表发送者应该再等待下一个FC，并且重启N_BS
        # timer；2OVFLW，代表接收方缓存溢出，发送方收到此FS后，应该终止发送，调用N_USData.confirm 服务，with
        # N_BUFFER_OVFLW ；3-F， Reserved
        "FlowStatus" / BitsInteger(4)
    ),
    "BlockSize" / Int8ub,  # 0，代表没有BS限制，发送方不必等待FC，把所有的FC一次发送；1-FF，代表发送方发送BS数量的CF后，需等待FC
    # 该值表明两个CF之间的最小间隔，如果发送方收到一个FC，其STmin的值是Reserved，则发送方应默认STmin为7F（127ms）；STmin参数体现在程序中就是一个定时器，发送完一帧CF后，应该立即启动STmin
    # timer；timer超时之后才能发送下一个CF，我的实现方式如下，nt_timer_run(TIMER_STmin) < 0 代表STmin
    # timer超时
    "STmin" / Int8ub,
    "Reserved" / Bytes(5)
)

obd_frame_struct_with_0x01 = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub
)

obd_frame_struct_with_0x41 = Struct(
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub,  # 一种是读支持的pid， 第二种是直接读取Pid的值
    "SupportBytesInfo" / If(this.SubFunction == 0x0 | this.SubFunction == 0x20 | this.SubFunction == 0x40, Struct(
        "SupportByte1" / Int8ub,
        "SupportByte2" / Int8ub,
        "SupportByte3" / Int8ub,
        "SupportByte4" / Int8ub
    )),
    "PidValue" / If(this.SubFunction != 0x0 | this.SubFunction !=
                    0x20 | this.SubFunction != 0x40, GreedyString('ascii'))
)

obd_frame_struct_with_0x02 = Struct(  # 读取冻结帧
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub,
    "Frame" / Int8ub
)

obd_frame_struct_with_0x42 = Struct(  # 读取冻结帧
    "ServiceID" / Int8ub,
    "SubFunction" / Int8ub,
    "Frame" / Int8ub,
    "PidValue" / GreedyString('ascii')
)

obd_frame_struct_with_0x03 = Struct(  # 存储在ECU中的与排放相关的“confirmed” DTC
    "ServiceID" / Int8ub,
)

obd_frame_struct_with_0x43 = Struct(
    "ServiceID" / Int8ub,
    "DTCCount" / Int8ub,
    "DTCCount" / Array(this.DTCCount, "DTCInfo" / Int16ub)
)

obd_frame_struct_with_0x04 = Struct(  # 存储在ECU中的与排放相关的“confirmed” DTC
    "ServiceID" / Int8ub,
)

obd_frame_struct_with_0x44 = Struct(
    "ServiceID" / Int8ub,
)

obd_frame_struct_with_0x06 = Struct(
    "ServiceID" / Int8ub,
    "MID" / Int8ub,
)

obd_frame_struct_with_0x46 = Struct(
    "ServiceID" / Int8ub,
    "MIDInfo" / Array(
        lambda this: InitStruct.uds_service_with_0x46_len, Struct(
            "MID" / Int8ub,
            "TID" / Int8ub,
            "UnitAndScalingID" / Int8ub,
            "TestValue" / Int8ub,
            "MinTestValue" / Int8ub,
            "MaxTestValue" / Int8ub,
        ))
)

obd_frame_struct_with_0x07 = Struct(
    "ServiceID" / Int8ub,
)

obd_frame_struct_with_0x47 = Struct(
    "ServiceID" / Int8ub,
    "DTCCount" / Int8ub,
    "DTCInfo" / Array(this.DTCCount, "DTC" / Int16ub)
)

obd_frame_struct_with_0x08 = Struct(
    "ServiceID" / Int8ub,
    "TID" / Int8ub,
)

obd_frame_struct_with_0x48 = Struct(
    "ServiceID" / Int8ub,
    "TID" / Int8ub,
)

obd_frame_struct_with_0x09 = Struct(
    "ServiceID" / Int8ub,
    "InfoType" / Int8ub,
)

obd_frame_struct_with_0x49 = Struct(
    "ServiceID" / Int8ub,
    "InfoType" / Int8ub,
    "InfoTypeValue" / If(this.SubFunction == 0x02, PaddedString(17, "utf8"))
)

fr_tp_frame_raw_struct = Struct(
    "TargetAddress" / Bytes(2),
    "SourceAddress" / Bytes(2),
    "FrameType" / BitStruct(
        "C_PCIType" / BitsInteger(4),
        "Ctr_Status" / BitsInteger(4)
    ),
    "MessageInfo" / Switch(
        this.FrameType.C_PCIType, {
            0x4: Struct(
        "EffectiveLength" / Int8ub,
                "MaximumLoad" / Int16ub,
            ),
            0x5: Struct(
                "EffectiveLength" / Int8ub
            ),
            0x6: Struct(
                "EffectiveLength" / Int8ub
            ),
            0x7: Struct(
                "EffectiveLength" / Int8ub
            ),
            0x8: Switch(this.FrameType.Ctr_Status, {
                0x3: Struct(
                    "BC" / Int8ub,
                    "BFS" / Int16ub
                ),
                0x4: Struct(
                    "ACK" / Int8ub,
                    "BP" / Int16ub
                )
            }),
            0x9: Struct(
        "EffectiveLength" / Int8ub,
                "MaximumLoad" / Int16ub,
            )
        }
    ),
    "RawData" / If(this.FrameType.C_PCIType != 0x8, Bytes(this.MessageInfo.EffectiveLength))
)

uds_doip_frame_struct = Struct(
    "ProtocolVersion" / Int8ub,
    "ProtocolVersionCrc" / Int8ub,
    "DataType" / Int16ub,
    "DataLen" / Int32ub,
    "DataInfo"/ If(this.DataLen != 0,
                   Switch(this.DataType, {
                    0x0000: Int8ub,  # 0:格式错误；1：未知的负载类型 2：报文长度过长 3：超出内存 4：无效的负载长度
                    # 0x0001: Int8ub,   #0x0001的DataLen应该为0
                    0x0002: Bytes(6),
                    0x0003: PaddedString(17, "utf8"),
                    0x0004: Struct(
                        "Vin" / PaddedString(17, "utf8"),
                        "LogicalAddress" / Int16ub,
                        "EID" / Bytes(6),
                        "GID" / Bytes(6),
                        "FurtherActionRequired" / Int8ub, # 0: no further action required;0x10: routing activation required to initate central secunity
                        # 如果长度多1，则：0：vin and/or gid are synchronized 0x10:vin and gid not synchronized
                    ),
                    0x0005: Struct(
                        "SourceAddress" / Int16ub,
                        "ActivationType" / Int8ub, # 0：default 1: diagnostic communication required by regulation ;0xE0: central secuity ;0xE1-0XEF: available for additional oem-specifimc use
                        "ReservedForISO" / Bytes(4)
                        # 注意多可选4个字节
                    ),
                    0x0006: Struct(
                        "TargetAddress" / Int16ub,
                        "SourceAddress" / Int16ub,
                        "ResCode" / Int8ub,  # 0x10: 激活成功
                        "ReservedForISO" / Bytes(4)
                        # 长度多4个，代表可选生效，：Reserved for OEM

                    ),
                    # 0x0007: Int8ub,  # 在线检测  长度为0
                    0x0008: Int16ub,  # 在线检测响应, 通常长度为2，代表SA
                    0x8001: Struct(
                "SourceAddress" / Int16ub,
                        "TargetAddress" / Int16ub,
                        "DiagData" / Bytes(this._.DataLen - 4)
                    ),
                    0x8002: Struct(
                "SourceAddress" / Int16ub,
                        "TargetAddress" / Int16ub,
                        "ReturnCode" / Bytes(this._.DataLen - 4)
                    ),   # 肯定响应
                    0x8003: Struct(
                "SourceAddress" / Int16ub,
                        "TargetAddress" / Int16ub,
                        "NRCCode" / Int8ub
                           # {
                           #     0x2: "invalid source address",
                           #     0x3: "unknown target address",
                           #     0x4: "diagnostic message too large",
                           #     0x5: "out of memory",
                           #     0x6: "target unreachable",
                           #     0x7: "unknown network",
                           #     0x8: "transport protocl error",
                           #
                           # }
                        # 可选可多字节数
                    ),   # 否定响应
                    # 0x4001: Int8ub,  #doip实体状态请求，长度通常为0
                    0x4002: Struct(
                        "NodeType" / Int8ub,  # 0: doip网关；1: doip节点
                        "TCP_DATA_MAX_NUMBER" / Int8ub,
                        "NOW_TCP_DATA_OPEN_NUMBER" / Int8ub,
                        # 最大数据存储空间 可选4个字节，单位G
                    ),
                    # 0x4003: Int8ub,  #诊断电源模式请求，长度通常为0
                    0x4004: Int8ub,  # 0：not ready 1:ready 2:not supported
                })
    )
)

_Intelligent_ambient_light_with_0x111 = Struct(
    "ProtocolType" / Int16ub,
    "Chip_Id" / Int8ub,
    "RGBL_INFO" / Array(16, Struct(
        "R_VALUE" / Int8ub,
        "G_VALUE" / Int8ub,
        "B_VALUE" / Int8ub,
        "L_VALUE" / Int8ub,
    )),
    "CRC_1" / Int8ub,
    "CRC_2" / Int8ub
)

Intelligent_ambient_light_with_0x101 = Struct(
    "ProtocolType" / Int16ub,
    "Chip_Id" / Int8ub,
    # "Status" / BitStruct(
    #     "Reverse" / BitsInteger(5),
    #     "SALM3U1TmpSts" / BitsInteger(1),
    #     "SALM3U1VltSts" / BitsInteger(1),
    #     "SALM3U1LEDSts" / BitsInteger(1),
    # ),
    # "CRC_1" / Int8ub,
    # "CRC_2" / Int8ub
)

Intelligent_ambient_light_with_0x111 = Struct(
    "RunDataInfo" / Array(8, _Intelligent_ambient_light_with_0x111),
    "DiagDataInfo" / Intelligent_ambient_light_with_0x101
)
