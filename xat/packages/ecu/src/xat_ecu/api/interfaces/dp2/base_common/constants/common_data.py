#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :common_data.py
@Time         :2024/11/6 10:27
@Author       :dejian.xiong@jiduauto.com
@Description  :公共常量
"""
from enum import Enum


class BaseEnum(Enum):
    pass


class DeviceName(BaseEnum):
    CCU_CD = 'CCU_CD'
    CCU_CD_AD = 'CCU_CD_AD'
    CCU_CD_LCU = 'CCU_CD_LCU'
    CCU_CD_AD_LCU = 'CCU_CD_AD_LCU'
    LCU_L = 'LCU_L'
    LCU_R = 'LCU_R'


class BusName(BaseEnum):
    publiccanfd = 'publiccanfd'
    diagnosticcan = 'diagnosticcan'
    propulsioncanfd = 'propulsioncanfd'
    chassis2canfd = 'chassis2canfd'
    infocanfd = 'infocanfd'


class UdpChannel(BaseEnum):
    CCUMCUAD_Multicast = 'AdMcuSoAdUDP_Multicast'
    CCUMCUCD_Multicast = 'CdMcuSoAdUDP_Multicast'
    LcuL_Multicast = 'LcuLSoAdUDP_Multicast'
    LcuR_Multicast = 'LcuRSoAdUDP_Multicast'
    LcuL_CCUSOCCD = 'LcuLSoAdUDP_CdSocSoAdUDP'
    LcuR_CCUSOCCD = 'LcuRSoAdUDP_CdSocSoAdUDP'
    CCUMCUAD_CCUSOCCD = 'AdMcuSoAdUDP_CdSocSoAdUDP'
    CCUMCUCD_CCUSOCCD = 'CdMcuSoAdUDP_CdSocSoAdUDP'


class TcpChannel(BaseEnum):
    CdMcuTCPServer_CdNadTCPClient1 = 'CdMcuTCPServer_CdNadTCPClient1'
    CdMcuTCPServer_CdSocPMTCPClient = 'CdMcuTCPServer_CdSocPMTCPClient'
    CdMcuTCPServer_CdSocTCPClient1 = 'CdMcuTCPServer_CdSocTCPClient1'
    AdMcuTCPServer_AdSocTCPClient = 'AdMcuTCPServer_AdSocTCPClient'
    AdMcuTCPServer_CdSocTCPClient2 = 'AdMcuTCPServer_CdSocTCPClient2'
    LcuLTCPServer_CdSocTCPClient3 = 'LcuLTCPServer_CdSocTCPClient3'
    LcuRTCPServer_CdSocTCPClient4 = 'LcuRTCPServer_CdSocTCPClient4'


class ErrorCode(BaseEnum):
    kOk = 0                         # 可执行
    kRequestOutOfRange = 1          # 参数超出范围
    kVehicleNotStandstill = 2       # 车辆未静止
    kUsageModeNotAllowed = 3        # 使用模式不满足
    kLVBatterySocLow = 4            # 低压电池SOC低
    kHVBatterySocLow = 5            # 高压电池SOC低
    kHVIsON = 6                     # 高压处于上电状态
    kHVIsOff = 7                    # 高压处于下电状态
    kServiceInhibited = 8           # 接口被禁用
    kServiceOccupied = 9            # 接口被占用
    kServiceBusy = 10               # 接口忙
    kPermissionDenied = 11          # 接口权限限制
    kCarModeNotAllowed = 12         # 车辆模式不满足
    kVehicleSpeedNotSatisfied = 13  # 车速不满足
    kGearNotSatisfied = 14          # 档位不满足    
    kDoorRadarNotActivate = 15      # 门雷达未激活
    kAmbientTempNotSatisfied = 16   # 环境温度不满足
    kSwitchStateNotSatisfied = 17   # 开关状态不满足
    kTailGateStateNotSatisfied = 18 # 尾门状态不满足
    kVehicleLaunching = 19          # UsageMode正在上切Drving
    kParemeterConflicts = 20        # 参数冲突
    kOtherError = 65535             # 其他错误


class ValidityLevel(BaseEnum):
    kValid = 0                      # 有效
    kSignalUnknownStatus = 1        # 未从底层获取到信息（参数保持为初始值）
    kQualityFactor2 = 2             # 信号的qualityfactor=2（对应参数的值赋值为当前获取的值）
    kE2ECounter = 3                 # 信号E2E的Couter错误（对应参数的值赋值为当前获取的值）
    kSignalMissing = 4              # 信号超时或丢失（对应参数的值保持为保持lastvalue）
    kE2ECheckSum = 5                # E2Echecksum校验失败（对应参数的值保持为保持lastvalue）
    kQualityFactor1 = 6             # 信号的qualityfactor=1（对应参数的值赋值为当前获取的值）
    kE2EGeneral = 7                 # E2Ecounter和checksum都错误（对应参数的值赋值保持lastvalue）
    kQualityFactor0 = 8             # 信号的qualityfactor=0（对应参数的值赋值保持lastvalue）
    kFatal = 9                      # 信号严重故障,不可信（对应参数的值保持lastvalue）


class SourceId(BaseEnum):
    kVoiceControl = 10000           # 语音控制
    kScreenControl = 20000          # 屏幕控制
    kRemoteControl = 30000          # 远程控制
    kAPA = 2010000                  # 泊车辅助
    kAVP = 2020000                  # 代客泊车
    kANP = 2030000                  # 领航辅助
    kGameMode = 2040000             # 游戏模式
    kOthers = 2147483647            # 其他
    