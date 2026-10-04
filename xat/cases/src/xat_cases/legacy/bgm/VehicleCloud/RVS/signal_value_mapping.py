from enum import Enum, auto
from typing import Union

class BaseEnum(Enum):
    pass

#----------------------------->车辆状态(10102)<------------------------------
class VehicleStatusRvs(BaseEnum):
    VehicleModeNormal     = 0 #    普通模式   (NORMAL)
    VehicleModeTransport  = 1 #    运输模式   (TRANSPORT)
    VehicleModeFactory    = 2 #    工厂模式   (FACTORY)
    VehicleModeCrash      = 3 #    碰撞模式   (CRASH)
    VehicleModeDyno= 5 #    Dyno转毂  (DYNO)
    VehicleModeEmpty      = -1 # --

class UsageModeRvs(BaseEnum):
    UsageModeAbandoned    = 0  # Abandoned 车辆休眠  驻车状态 介于休眠和激活的中间状态 (ABANDONED)
    UsageModeInactive     = 1  # Inactive 车辆唤醒 未激活状态 介于休眠和激活的中间状态，部分ECU唤醒激活，但仅提供有限的功能支  (INACTIVE)
    UsageModeConvenience  = 2  # Convenience 充电 舒亨状态 用户上车，上高压，座舱功能全激活，动力底盘相关功能未激活 (CONVENIENCE)
    UsageModeActive= 11  # Active 车辆上电 激活状态 非正常模式，所有ECU全激活，但动力系统不工作  (ACTIVE)
    UsageModeDriving      = 13  # Driving 车辆驾驶 驾驶状态 用户有驾驶意图或驾驶中，所有ECU全激活  (DRIVING)
    UsageModeEmpty = -1  #--

#----------------------------->车身数据(10103)<------------------------------
class DoorIdRvs(BaseEnum):
    DoorFrontLeft    = 0 #    左前方 (kDoorFrontLeft)
    DoorFrontRight   = 1 #    右前方 (kDoorFrontRight)
    DoorRearLeft     = 2 #    左后方 (kDoorRearLeft)
    DoorRearRight    = 3 #    右后方 (kDoorRearRight)
    DoorAll  = 4 #    所有 (kDoorAll)
    DoorEmpty= -1

#车门状态
class DoorStatusRvs(BaseEnum):
    DoorStatusOpened = 0 # 门已经打开至最大 (kOpened)
    DoorStatusClosing  = 1 # 门正在关闭中 (kClosing)
    DoorStatusClosed  = 2 # 门已经关闭 (kClosed)
    DoorStatusLocked  = 3 # 门已经上锁 (kLocked) 不用这个枚举值
    DoorStatusUnlocked = 4 # 门已经解锁 (kUnlocked)
    DoorStatusOpening  = 5 # 门已经打开 (kOpening)
    DoorStatusHover  = 6 # 门悬停 (kHover)
    DoorStatusNA  = 7 # 状态未知 (kNA)
    DoorStatusEmpty  = -1 # --
    UNKNOWN_ENUM_VALUE_DoorStatus_10=10
    UNKNOWN_ENUM_VALUE_DoorStatus_8=8
    UNKNOWN_ENUM_VALUE_DoorStatus_9=9

#尾门状态
class TailGateStatusRvs(BaseEnum):
    TgsOpened   =0 # 尾门已经打开至最大 (kOpened)
    TgsClosing  =1 # 尾门正在关闭中 (kClosing)
    TgsClosed   =2 # 尾门已经关闭 (kClosed)
    TgsOpening  =3 # 尾门已经打开 (kOpening)
    TgsHover =4 # 尾门悬停 (kHover)
    TgsNA  =5 # 状态未知 (kNA)
    TgsEmpty = -1 # --

#前引擎盖状态
class BonnetStatusRvs(BaseEnum):
    BonnetStatusOpen  =0 # 开启 (kOpen)
    BonnetStatusClose  =1 # 关闭 (kClose)
    BonnetStatusInvalid =65535 # 无效 (kInvalid)
    BonnetStatusEmpty  = -1 # --

#车窗Id
class WindowIdRvs(BaseEnum):
    WindowFrontLeft  =0 # 左前窗 (kWindowFrontLeft)
    WindowFrontRight =1 # 右前窗 (kWindowFrontRight)
    WindowRearLeft  =2 # 左后窗 (kWindowRearLeft)
    WindowRearRight  =3 # 右后窗 (kWindowRearRight)
    WindowAll =4 # 全部 (kWindowAll)
    WindowEmpty  = -1 # --

#车窗
class WindowStatusRvs(BaseEnum):
    WindowStatusOpened =0   # 完全打开 (kStatusOpened)
    WindowStatusClosed =1   # 完全关闭 (kStatusClosed)
    WindowStatusOpening =2   # 正在打开 (kStatusOpening)
    WindowStatusClosing =3   # 正在关闭 (kStatusClosing)
    WindowStatusOpenFail =4   # 打开失败 (kStatusOpenFail)
    WindowStatusCloseFail =5   # 关闭失败 (kStatusCloseFail)
    WindowStatusNA  =6   # 状态未知 (kStatusNa)
    WindowStatusEmpty  = -1 # --


class HeatVentWorkStatusRvs(BaseEnum):
    HeatVentNone  = 0 # 无状态（默认） (kNone)
    HeatVentOn    = 1 # 功能开启 (kOn)
    HeatVentOff   = 2 # 功能关闭 (kOff)
    HeatVentError = 3 # 功能错误 (kError)
    HeatVentFunctionLimit= 4 # 功能限制 (kFunctionLimit)
    HeatVentEnergyLimit  = 5 # 能量限制 (kEnergyLimit)
    HeatVentReserved1    = 6 # 预留1 (kReserved1)
    HeatVentReserved2    = 7 # 预留2 (kReserved2)
    HeatVentEmpty = -1 #-- (Empty)

# 香氛浓度等级
class FragranceLevelRvs(BaseEnum):
  FragranceValueNoWarn = 0 #未知 (kFragLevelOff)
  FragranceValueLevel1 = 1 #等级1 (kFragLevel1)
  FragranceValueLevel2 = 2 #等级2 (kFragLevel2)
  FragranceValueLevel3 = 3 #等级3 (kFragLevel3)
  FragranceValueEmpty  = -1 #--


# 香氛当前的香型
class FragranceChannelRvs(BaseEnum):
  FragranceNoReq= 0 #未知 (kNoReq)
  FragranceChannel1    = 1 #香型1 (kChannel_1)
  FragranceChannel2    = 2 #香型2 (kChannel_2)
  FragranceChannel3    = 3 #香型3 (kChannel_3)
  FragranceChannel4    = 4 #香型4 (kChannel_4)
  FragranceChannel5    = 5 #香型5 (kChannel_5)
  FragranceChannelEmpty= -1 #--


# 香氛消耗情况/剩余的量
class FragranceLeftValueRvs(BaseEnum):
  FlvNoWarn     = 0 #未知 （kValueNoWarn）
  FlvLevel1     = 1 #等级1 （kValueLevel1）
  FlvLevel2     = 2 #等级2 （kValueLevel2）
  FlvLevel3     = 3 #等级3 （kValueLevel3）
  FlEmpty= -1 #--


#挡风玻璃Id
class ShieldWindowIdRvs(BaseEnum):
  ShieldWindowAll      = 0 # 全部挡风玻璃 (kShieldWindowAll)
  ShieldWindowFront    = 1 # 前挡风玻璃 (kShieldWindowFront)
  ShieldWindowRear     = 2 # 后挡风玻璃 (kShieldWindowRear)
  ShieldWindowEmpty    = -1 #--

#挡风玻璃加热状态
class ShieldWindowHeatStatusRvs(BaseEnum):
  SwhsHeatStatusOff    = 0 # 关 (kHeatStatusOff)
  SwhsHeatStatusOn     = 1 # 开 (kHeatStatusOn)
  SwhsHeatStatusAutoOn = 2 # 自动开 (kHeatStatusAutoOn)
  SwhsEmpty     = -1#--


#摆风模式
class SwingModeRvs(BaseEnum):
  SwingModeOff  = 0 #停止摆风 (kSwingOff)
  SwingModeAllOn= 1 #上下左右同时摆风 (kSwingAllOn)
  SwingModeUpDown      = 2 #上下摆风 (kSwingUpDown)
  SwingModeLeftRight   = 3 #左右摆风 (kSwingLeftRight)
  SwingModeEmpty= -1 #-- (Empty)

#出风模式，用来定义风以什么样的特点吹到人身上
class AirVentModeRvs(BaseEnum):
  AirVentModeNormal    = 0 #出风口手动调节，用户可以设置出风口坐标 (kNormal)
  AirVentModeFocus     = 1 #出风口吹面，出风口调整到驾驶/副驾驶侧吹头的位置 (kFocus)
  AirVentModeAvoid     = 2 #出风口避免吹面，出风口调整到避免吹到驾驶/副驾驶乘员的位置 (kAvoid)
  AirVentModeCustomize = 3 #个性化，按照存储的个性化设置的出风口坐标值调整出风口 (kCustomize)
  AirVentModeEmpty     = -1 #-- (Empty)


class BeltStatusRvs(BaseEnum):
    BeltStatusBeltLocked   = 0#安全带已扣
    BeltStatusBeltUnlock  = 1#安全带未扣
    BeltStatusBeltNa  = 2#安全带未知
    BeltStatusBeltEmpty = -1# --



class ViewFoldStatusRvs(BaseEnum):
    VfsStatusNa = 0#状态未知（未定义） (kStatusNa)
    VfsStatusUnfolded = 1#后视镜已经展开 (kStatusUnfolded)
    VfsStatusFolded = 2#后视镜已经折叠 (kStatusFolded)
    VfsStatusUnfolding = 3#后视镜展开中 (kStatusUnfolding)
    VfsStatusFolding = 4#后视镜折叠中 (kStatusFolding)
    VfsStatusHover = 5#后视镜悬停在中间位置 (kStatusHover)
    VfsEmpty = -1 # --

#尾翼位置
class TailWingPositionRvs(BaseEnum):
    TwpTailWingPosition0 = 0# 尾翼位置0, 收回状态 (kTailWingPosition0)
    TwpTailWingPosition1 = 1# 展开到尾翼位置1 (kTailWingPosition1)
    TwpTailWingPosition2 = 2# 展开到尾翼位置2 (kTailWingPosition2)
    TwpTailWingPosition3 = 3# 展开到尾翼位置3 (kTailWingPosition3)
    TwpTailWingPositionNA = 4# 尾翼位置未知 (kTailWingPositionNA)
    TwpEmpty = -1 # --

#尾翼模式
class TailWingModeRvs(BaseEnum):
    TwmTailWingModeOff = 0# 关闭主动控制 (kTailWingModeOff)
    TwmTailWingModeOn = 1# 使能主动控制 (kTailWingModeOn)
    TwmTailWingModeAuto = 2# 自动控制 (kTailWingModeAuto)
    TwmTailWingModeNA = 3# 模式未知 (kTailWingModeNA)
    TwmEmpty = -1 # --



# 方向盘加热等级
class SteerWheelHeatLevelRvs(BaseEnum):
    SteerWheelHeatOff     = 0 # 关闭 (kHeatOff)
    SteerWheelHeatLow     = 1 # 低热 (kHeatLow)
    SteerWheelHeatMedium  = 2 # 中热 (kHeatMedium)
    SteerWheelHeatHigh    = 3 # 高热 (kHeatHigh)
    SteerWheelEmpty= -1#--

#方向盘加热可用状态 SteerHeatAvailiable
class HeatingAvailableStatusRvs(BaseEnum):
    HasNone      = 0 #初始状态 默认值 (kNone)
    HasOn = 1 #加热开启 (kOn)
    HasOff= 2 #加热关闭 (kOff)
    HasError     = 3 #加热错误 (kError)
    HasFunctionalLimit  = 4  #功能受限 (kFuncational_Limit)
    HasEnergyLimit      = 5  #能量受限 (kEnergy_Limit)
    HasEmpty     = -1#--

# 座椅位置
class SeatIdRvs(BaseEnum):
    SeatFrontLeft  = 0 # 前排左 (kSeatFrontLeft)
    SeatFrontRight = 1 # 前排右 (kSeatFrontRight)
    SeatFrontMiddle= 2 # 前排中 (kSeatFrontMiddle)
    SeatFrontRow   = 3 # 第一排全部座椅 (kSeatFrontRow)
    SeatRearLeft   = 4 # 后排左 (kSeatRearLeft)
    SeatRearMiddle = 5 # 后排中 (kSeatRearMiddle)
    SeatRearRight  = 6 # 后排右 (kSeatRearRight)
    SeatRearRow    = 7 # 后排全部座椅 (kSeatRearRow)
    SeatThirdLeft  = 8 # 第三排左 (kSeatThirdLeft)
    SeatThirdMiddle= 9 # 第三排中间 (kSeatThirdMiddle)
    SeatThirdRight = 10 # 第三排右 (kSeatThirdRight)
    SeatThirdRow   = 11 # 第三排全部座椅 (kSeatThirdRow)
    SeatAll = 12 # 全车座椅 (kSeatAll)
    SeatEmpty      = -1 #-- (Empty)


# 加热/通风状态信息
class HeatVentWorkStatusRvs(BaseEnum):
    HeatVentNone   = 0 # 无状态（默认） (kNone)
    HeatVentOn     = 1 # 功能开启 (kOn)
    HeatVentOff    = 2 # 功能关闭 (kOff)
    HeatVentError  = 3 # 功能错误 (kError)
    HeatVentFunctionLimit = 4 # 功能限制 (kFunctionLimit)
    HeatVentEnergyLimit   = 5 # 能量限制 (kEnergyLimit)
    HeatVentReserved1     = 6 # 预留1 (kReserved1)
    HeatVentReserved2     = 7 # 预留2 (kReserved2)
    HeatVentEmpty  = -1 #-- (Empty)

# 香氛浓度等级
class  FragranceLevelRvs(BaseEnum):
    FragranceValueNoWarn  = 0 #未知 (kFragLevelOff)
    FragranceValueLevel1  = 1 #等级1 (kFragLevel1)
    FragranceValueLevel2  = 2 #等级2 (kFragLevel2)
    FragranceValueLevel3  = 3 #等级3 (kFragLevel3)
    FragranceValueEmpty   = -1 #--


# 香氛当前的香型
class FragranceChannelRvs(BaseEnum):
    FragranceNoReq = 0 #未知 (kNoReq)
    FragranceChannel1     = 1 #香型1 (kChannel_1)
    FragranceChannel2     = 2 #香型2 (kChannel_2)
    FragranceChannel3     = 3 #香型3 (kChannel_3)
    FragranceChannel4     = 4 #香型4 (kChannel_4)
    FragranceChannel5     = 5 #香型5 (kChannel_5)
    FragranceChannelEmpty = -1 #--


# 香氛消耗情况/剩余的量
class  FragranceLeftValueRvs(BaseEnum):
    FlvNoWarn      = 0 #未知 （kValueNoWarn）
    FlvLevel1      = 1 #等级1 （kValueLevel1）
    FlvLevel2      = 2 #等级2 （kValueLevel2）
    FlvLevel3      = 3 #等级3 （kValueLevel3）
    FlEmpty = -1 #--


#挡风玻璃Id
class ShieldWindowIdRvs(BaseEnum):
    ShieldWindowAll= 0 # 全部挡风玻璃 (kShieldWindowAll)
    ShieldWindowFront     = 1 # 前挡风玻璃 (kShieldWindowFront)
    ShieldWindowRear      = 2 # 后挡风玻璃 (kShieldWindowRear)
    ShieldWindowEmpty     = -1 #--

#挡风玻璃加热状态
class ShieldWindowHeatStatusRvs(BaseEnum):
    SwhsHeatStatusOff     = 0 # 关 (kHeatStatusOff)
    SwhsHeatStatusOn      = 1 # 开 (kHeatStatusOn)
    SwhsHeatStatusAutoOn  = 2 # 自动开 (kHeatStatusAutoOn)
    SwhsEmpty      = -1#--


#摆风模式
class SwingModeRvs(BaseEnum):
    SwingModeOff   = 0 #停止摆风 (kSwingOff)
    SwingModeAllOn = 1 #上下左右同时摆风 (kSwingAllOn)
    SwingModeUpDown= 2 #上下摆风 (kSwingUpDown)
    SwingModeLeftRight    = 3 #左右摆风 (kSwingLeftRight)
    SwingModeEmpty = -1 #-- (Empty)

#出风模式，用来定义风以什么样的特点吹到人身上
class AirVentModeRvs(BaseEnum):
    AirVentModeNormal     = 0 #出风口手动调节，用户可以设置出风口坐标 (kNormal)
    AirVentModeFocus      = 1 #出风口吹面，出风口调整到驾驶/副驾驶侧吹头的位置 (kFocus)
    AirVentModeAvoid      = 2 #出风口避免吹面，出风口调整到避免吹到驾驶/副驾驶乘员的位置 (kAvoid)
    AirVentModeCustomize  = 3 #个性化，按照存储的个性化设置的出风口坐标值调整出风口 (kCustomize)
    AirVentModeEmpty      = -1 #-- (Empty)


#空调系统故障
class ClimateFaultIdRvs(BaseEnum):
    ClimateFaultIdOK= 0 # 无故障 OK
    ClimateFaultIdFaultOutletError= 1 # 电动出风口故障
    ClimateFaultIdFaultExternalTempSensorError  = 2 # 舱外温度传感器故障，当传感器的QF不等于GENQF1_ACCUR_DATA时，上报该故障码
    ClimateFaultIdFaultInternalTempSensorError  = 3 # 舱内温度传感器故障，当传感器的QF不等于GENQF1_ACCUR_DATA时，上报该故障码
    ClimateFaultIdFaultOutletEnergyLimit = 4 # 由于能耗限制，无法调节出风口
    ClimateFaultIdFaultAQSSensorError    = 5 # AQS传感器故障
    ClimateFaultIdFaultCoolantLow = 6 # 冷却液不足
    ClimateFaultIdFaultBatteryLow = 7 # 电量不足  (kFaultBatteryLow)
    ClimateFaultIdFaultCoolantLowAndBatteryLow  = 8 # 冷却液和电量不足  (kFaultCoolantLowAndBatteryLow)
    ClimateFaultIdFaultTemperatureLow    = 9 # 温度过低  (kFaultTemperatureLow)
    ClimateFaultIdFaultTemperatureHigh   = 10 # 温度过高  (kFaultTemperatureHigh)
    ClimateFaultIdFaultClimateError      = 11 # 空调异常  (kFaultClimateError)
    ClimateFaultIdFaultHighVoltageError  = 12 # 高压异常  (kFaultHighVoltageError)
    ClimateFaultIdFaultActivationLimited = 13 # 开启时间已满  (kFaultActivationLimited)
    ClimateFaultIdNA= 14 # 未知故障
    ClimateFaultIdEmpty    = -1 # -- (Empty)


 #PM2.5检测状态 PM2.5传感器工作状态
class  SensorWorkStatusRvs(BaseEnum):
    SensorInitial   = 0  #初始化 (kInitial)
    SensorCollecting= 1  #正在收集 (kCollecting)
    SensorComplete  = 2  #已完成 (kComplete)
    SensorError     = 3  #出错 (kError)
    SensorEmpty     = -1  #--

 #PM2.5等级
class  PM25LevelRvs(BaseEnum):
    PmLevel1     = 0    #等级1 (kLevel1)
    PmLevel2     = 1    #等级2 (kLevel2)
    PmLevel3     = 2    #等级3 (kLevel3)
    PmLevel4     = 3    #等级4 (kLevel4)
    PmLevel5     = 4    #等级5 (kLevel5)
    PmLevel6     = 5    #等级6 (kLevel6)
    PmLevelReserved =    6    #重置 (kLevelReserved)
    PmLevelInvalid  =    7    #无效 (kLevelInvalid)
    PmEmpty         = -1  #--


 #空调分区ID
class  ClimateZoneIdRvs(BaseEnum):
    ClimateAllZone = 0  #所有区域 (kAllZone)
    ClimateFirstRow= 1  #第一排 (kFirstRow)
    ClimateSecondRow                   = 2  #第二排 (kSecondRow)
    ClimateFirstRowLeft                = 3  #第一排左 (kFirstRowLeft)
    ClimateFirstRowRight               = 4  #第一排右 (kFirstRowRight)
    ClimateSecondRowLeft               = 5  #第二排左 (kSecondRowLeft)
    ClimateSecondRowMiddle             = 6  #第二排中间 (kSecondRowMiddle)
    ClimateSecondRowRight              = 7  #第二排右 (kSecondRowRight)
    ClimateEmpty   = -1  #-- (Empty)


class PluggerStatusRvs(BaseEnum):
    PsDisconnected   = 0  #未连接 (StatusDisconnected)
    PsConnectedWithoutPower  = 1  #连接未充电 (StatusConnectedWithoutPower)
    PsPowerAvailableButNotActivated = 2  #PowerAvailableButNotActivated (StatusPowerAvailableButNotActivated)
    PsConnectedWithPower = 3  #连接充电 (StatusConnectedWithPower)
    PsInit  = 4  #Init (StatusInit)
    PsFaul   = 5  #Fault (StatusFault)
    PsEmpty = -1  #--


class ChargeStatusRvs(BaseEnum):
    CsNoCharging   = 1 
    CsDCCharging  = 15
    CsSuperCharging = 24
    CsDCChargingEnd = 26

#中控锁状态
class CentralLockStatus(BaseEnum):
    ClsUnknown = 0 #状态未知 中控锁状态 (kUndef)
    ClsUnlock  = 1 #中控解锁 即4个门和尾门都处于解锁状态 (kUnlocked)
    ClsTailUnlock  = 2 #中控上锁尾门解锁 即4个门处于闭锁状态，尾门处于解锁状态 (kFourDoorLockedTailUnlocked)
    ClsLocked  = 3 #中控上锁 即4个门和尾门都处于闭锁状态 (kAllLocked)
    ClsEmpty = -1 #-- (Empty)





# def transfer_key_to_value(class_name,key):
#    return class_name.get(key).value

if __name__ == '__main__':
    key = "HeatVentOn"
    # obj = getattr(HeatVentWorkStatusRvs, key)
    print(getattr(VehicleStatusRvs, "VehicleModeDyno").value)