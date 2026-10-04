from enum import Enum, auto
from typing import Union

class BaseEnum(Enum):
    pass

DLC_DATA_BYTE_CNT = (
    0, 1, 2, 3, 4, 5, 6, 7,
    8, 12, 16, 20, 24, 32, 48, 64
)

class FailType(BaseEnum):
    FAILTYPE_SUCCESS = 0
    FAILTYPE_TIMEOUT = -1
    FAILTYPE_SERVICE_BUSY = -2
    FAILTYPE_SERVICE_UNAVAILIABLE = -3
    FAILTYPE_TIME_OUT = 600  # operation timed out
    FAILTYPE_NO_MEMORY = auto()  # memory allocatoin failure
    FAILTYPE_OBJECT_NOT_EXIST = auto()  # no such object
    FAILTYPE_NO_PERMISSION = auto()  # no permission for operation
    FAILTYPE_INITIALIZE = auto()  # initialization failure
    FAILTYPE_NO_IMPLEMENT = auto()  # implementation unavailable
    FAILTYPE_BAD_TYPECODE = auto()  # bad typecode
    FAILTYPE_BAD_OPERATION = auto()  # invalid operation
    FAILTYPE_NO_RESPONSE = auto()  # response not yet available
    FAILTYPE_BAD_PARAM = auto()  # an invalid parameter was passed
    FAILTYPE_FREE_MEM = auto()  # no permission for operation
    FAILTYPE_SERIALIZATION_FAILURE = auto()  # serialization failure
    FAILTYPE_DESERIALIZATION_FAILURE = auto()  # deserialization failure
    FAILTYPE_SEND_DATA_FAILURE = auto()  # send data failure
    FAILTYPE_RECEIVE_DATA_FAILURE = auto()  # receive data failure
    FAILTYPE_WRONG_DATA_TYPE = auto()  # wrong data type
    FAILTYPE_OTHER_ERROR = auto()  # other error


class UsageMode(BaseEnum):
    ABANDONED = 0
    INACTIVE = 1
    CONVENIENCE = 2
    ACTIVE = 11
    DRIVING = 13


class CarMode(BaseEnum):
    NORMAL = 0
    TRANSPORT = 1
    FACTORY = 2
    CRASH = 3
    DYNO = 5


class DoorLock(BaseEnum):
    unlock = 1
    lock = 2
    close_and_unlock = 3


class DoorPos(BaseEnum):
    Dirver = 0
    Pass = 1
    RearLeft = 2
    RearRight = 3
    Tailgate = 4
    All = 5
    Hood = 6


class ClimateControl(BaseEnum):
    open = 1
    close = -1


class Door(BaseEnum):
    open = 1
    close = 2


class HoodSts(BaseEnum):
    Ukwn = 0
    Open = 1
    Close = 2


class Seat(BaseEnum):
    unlock = 1
    lock = 2


class PowerType(BaseEnum):
    BGM = 'BGM_P'
    TCAM = 'TCAM_P'
    ACU = 'ACU_P'
    CDC = 'CDC_P'
    PCAN = 'PCAN_P'
    Toomoss = 'Toomoss_P'
    BGM_D = 'BGM_D'
    TCAM_KL15 = 'TCAM_KL15'


class PowerStatus(BaseEnum):
    open = 'OPEN'
    close = 'CLOSE'


class WiperWashing(BaseEnum):
    open = 'OPEN'
    close = 'CLOSE'


class DeviceName(BaseEnum):
    BGM = 'BGM'
    TCAM = 'TCAM'
    ACU = 'ACU'
    CDCQ = 'CDCQ'
    CCU_CD = 'CCU_CD'
    CCU_CD_AD = 'CCU_CD_AD'
    CCU_CD_LCU = 'CCU_CD_LCU'
    CCU_CD_AD_LCU = 'CCU_CD_AD_LCU'
    LCU_L = 'LCU_L'
    LCU_R = 'LCU_R'


class Gear(BaseEnum):
    Park = 0
    Rvs = 1
    Neut = 2
    Drv = 3
    ManMode = 4
    Resd1 = 5
    Resd2 = 6
    Undefd = 7


class VehMtnSts(BaseEnum):
    Ukwn = 0
    StandStillVal1 = 1
    StandStillVal2 = 2
    StandStillVal3 = 3
    FwdVal1 = 4
    FwdVal2 = 5
    BackwVal1 = 6
    BackwVal2 = 7


class VehSpdQf(BaseEnum):
    UndefindDataAccur = 0
    TmpUndefdData = 1
    DataAccurNotWithinSpcn = 2
    AccurData = 3


class isOn(BaseEnum):
    Off = False
    On = True


class ViewPos(BaseEnum):
    RearRight = 0
    RearLeft = 1
    All = 2


class Direction(BaseEnum):
    Forward = 0
    Left = 1
    Up = 2
    Backward = 3
    Right = 4
    Down = 5


class MirrDirReq(BaseEnum):
    Idle = 0
    Up = 1
    Down = 2
    Left = 3
    Right = 4


class WinPos(BaseEnum):
    ukwn = 0
    close = 1
    percent_4 = 2
    percent_8 = 3
    percent_12 = 4
    percent_16 = 5
    percent_20 = 6
    percent_24 = 7
    percent_28 = 8
    percent_32 = 9
    percent_36 = 10
    percent_40 = 11
    percent_44 = 12
    percent_48 = 13
    percent_52 = 14
    percent_56 = 15
    percent_60 = 16
    percent_64 = 17
    percent_68 = 18
    percent_72 = 19
    percent_76 = 20
    percent_80 = 21
    percent_84 = 22
    percent_88 = 23
    percent_92 = 24
    percent_96 = 25
    percent_100 = 26
    percent_error = 255


class CenLockSts(BaseEnum):
    Unlock = 1
    TrUnlock = 2
    Lock = 3


class DoorOpenerSts(BaseEnum):
    Ukwn = 0
    FullClsd = 1
    MovgOut = 2
    MovgOutBrkg = 3
    StopDurgOpen = 4
    FullOpend = 5
    MovgIn = 6
    MovgInBrkg = 7
    StopDurgCls = 8
    HalfClsd = 9
    StopMinPntForCls = 0x0A

class DoorOpenerReq(BaseEnum):
    Idle = 0
    Open = 1
    Close = 2
    Stop = 3
    OpenMinang = 4


class DoorOpenerMoveSts(BaseEnum):
    Ukwn = 0
    FullClsd = 1
    MovgOut = 2
    MovgOutBrkg = 3
    StopDurgOpen = 4
    FullOpend = 5
    MovgIn = 6
    MovgInBrkg = 7
    StopDurgCls = 8
    HalfClsd = 9
    StopMinPntForCls = 0x0A

class AlrmSts(BaseEnum):
    Disarmd = 0
    Armd = 1
    Actv = 2


class IndcrSts(BaseEnum):
    Off = 0
    LeOn = 1
    RiOn = 2
    LeAndRiOn = 3


class SeatPos(BaseEnum):
    Drive = 0
    Pass = 1
    SecLeft = 2
    SecMid = 3
    SecRight = 4
    RearAll = 5


class AirWindMode(BaseEnum):
    Flr = 0
    Vent = 1
    Defrst = 2
    FlrDefrst = 3
    FlrVent = 4
    VentDefrst = 5
    FlrVentDefrst = 6
    Aut = 7


class SeatPresSts(BaseEnum):
    NoPres = 0
    Pres = 1


class OutSwitchPressSts(BaseEnum):
    NoPress = 0
    Press = 1


class LockTrigerSource(BaseEnum):
    NoTrigSrc = 0
    KeyRem = 1
    Keyls = 2
    IntrSwt = 3
    SpdAut = 4
    TmrAut = 5
    Slam = 6
    Telm = 7
    Crash = 8
    Apprch = 9
    OutsOth = 10
    InsOth = 11
    NFC = 12


class LockCmd(BaseEnum):
    UnLock = 0
    Lock = 1
    AllDoorCloseAndLock = 2
    LockCompleteArm = 3


class LockSource(BaseEnum):
    RKE = 0
    Telm = 1
    HMI = 2
    NFC = 3
    Apprch = 4
    KV_PEPS = 5
    Crash = 6
    SpdAut = 7
    TmrAut = 8
    OutsOth = 9
    InsOth = 10
    APA = 11


class SysDefenSts(BaseEnum):
    DisArmd = 0
    Armd = 1
    Actv = 2


class AlmSrc(BaseEnum):
    NoTrigSource = 0
    BackupBattSensor = 1
    InclinationSensor = 2
    IntrusionScannerSensor = 3
    Hood = 4
    Tailgate = 5
    DriDoor = 6
    PassDoor = 7
    ReleDoor = 8
    ReriDoor = 9
    Vehlmobinivld = 10


class SysFault(BaseEnum):
    NoFailr = False
    Failr = True


class WiperMode(BaseEnum):
    Off = 0
    SingleWipe = 1
    IntLow = 2
    IntHigh = 3
    Low = 4
    High = 5
    Auto = 6
    Error = 7


class WiperPos(BaseEnum):
    Front = 0
    Rear = 1
    All = 2


class WipgSpdInfo(BaseEnum):
    Off = 0
    IntlLo = 1
    IntlHi = 2
    WipgSpd4045 = 3
    WipgSpd4650 = 4
    WipgSpd5155 = 5
    WipgSpd5660 = 6
    WiprErr = 7


class WashReq(BaseEnum):
    Not_Valid_1 = 0
    Off = 1
    On = 2
    Not_Valid_2 = 3


class RainSensorAct(BaseEnum):
    Off = 0
    On = 1


class MaintainPosReq(BaseEnum):
    Off = 0
    On = 1


class DCChrgnHndlSts(BaseEnum):
    # 充电枪状态
    Disconnected = 0
    ConnectedWithoutPower = 1
    PowerAvailableButNotActivated = 2
    ConnectedWithPower = 3
    Init = 4
    Fault = 5


class BattSnsrHwFltRaw(BaseEnum):
    # 电池硬件故状态
    DevErrSts2_NoFlt = 0
    DevErrSts2_Flt = 1


class DcDcActvd(BaseEnum):
    # 电池激活状态
    NoConversionToLVSide = 0
    ConversionToLVSide = 1


class LVPwrSplyErrSts(BaseEnum):
    # 低压电池供电错误状态
    SysOk = 0
    UhiDurgDrvg = 1
    UloDurgdrvg = 2
    BattRlyFlt = 3
    BattSnsrComFlt = 4
    BattSnsrHwFlt = 5
    FltComDcDc = 6
    FltElecDcDc = 7
    FltDcDc = 8
    SupCptrHwFlt = 9
    AltFltMecl = 10
    AltFltElec = 11
    AltFltT = 12
    AltFltCom = 13
    SpprtBattFltChrgn = 14
    LoSOC = 15


class EngSt1WdStsEngSt1WdSts(BaseEnum):
    # 发动机运行状态
    EngSt1_Ini = 0
    EngSt1_Awake = 1
    EngSt1_Rdy = 2
    EngSt1_PreStrtg = 3
    EngSt1_StrtgInProgs = 4
    EngSt1_RunngRunng = 5
    EngSt1_RunngStb = 6
    EngSt1_RunngStrtgInProgs = 7
    EngSt1_RunngRemStrtd = 8
    EngSt1_AftRun = 9


class BackgroundColor(BaseEnum):
    # 背景颜色
    GREEN = 0
    YELLOW = 1
    RED = 2


class BatteryLowTelltale(BaseEnum):
    # 电池低报警信息
    TELLTALE_OFF = 0
    TELLTALE_ON = 1
    TELLTALE_FLASH = 2


class ULoWarnULoWarn(BaseEnum):
    # 低压系统电压告警状态
    UOk = 0
    ULoTmp = 1
    ULoPrmnt = 2


class ValidityLevel(BaseEnum):
    kValid = 0  # 有效
    kSignalUnknownStatus = 1  # 信号值未定义
    kQualityFactor2 = 2  # 信号的 qualityfactor = 2
    kE2ECounter = 3  # 信号E2E的计数不连续
    kSignalMissing = 4  # 信号超时或丢失
    kE2ECheckSum = 5  # E2E checksum校验失败
    kQualityFactor1 = 6  # 信号的 qualityfactor = 1
    kE2EGeneral = 7  # E2E错误（包括counter和checksum的双重错误或未知E2E错误）
    kQualityFactor0 = 8  # 信号的 qualityfactor = 0
    kFatal = 9  # 信号严重故障，不可信
    kReserved = 10  # 预留值，default值


class DCChrgnPort(BaseEnum):
    # DC充电口正负极
    Pos = 'Pos'
    Neg = 'Neg'


class TailWingPos(BaseEnum):
    # 电动尾翼位置状态
    Ukwn = 0
    P0 = 1
    P1 = 2
    P2 = 3
    P3 = 4
    Shifting = 5
    Reserved = 6
    Error = 7


class TailWindMode(BaseEnum):
    # 尾翼模式
    Off = 0
    On = 1
    Auto = 2
    NA = 3


class SetTailWingPos(BaseEnum):
    # 电动尾翼位置命令
    NoCmd = 0
    P0 = 1
    P1 = 2
    P2 = 3
    P3 = 4
    Reserved1 = 5
    Reserved2 = 6
    Reserved3 = 7


class TailGateMode(BaseEnum):
    Open = 0
    Close = 1
    Stop = 2
    OpenMinAngle = 4


class SetTailGatePos(BaseEnum):
    # 打开电动门请求
    Idle = 0
    Open = 1
    Close = 2
    Stop = 3
    CloseDelay = 4


class HeatLevel(BaseEnum):
    # 加热等级
    Off = 0
    Low = 1
    Mid = 2
    High = 3

class VentLevel(BaseEnum):
    # 加热等级
    Off = 0
    Low = 1
    Mid = 2
    High = 3

class AvlSts(BaseEnum):
    # 加热功能可用状态
    Non = 0
    On = 1
    Off = 2
    Error = 3
    Functionallimit = 4
    Energylimit = 5
    Resvd1 = 6
    Resvd2 = 7


class HvSysRelaySts(BaseEnum):
    # 设置高压继电器状态为
    Open = 0
    Close = 1
    KeepSts = 2
    OpenAndReqActvDcha = 3


class SeatId(BaseEnum):
    # 选择座椅
    FrontLeft = 0
    FrontRight = 1
    FrontMid = 2
    FrontRow = 3
    RearLeft = 4
    RearMiddle = 5
    RearRight = 6
    RearRow = 7
    ThirdLeft = 8
    ThirdMiddle = 9
    ThirdRight = 10
    ThirdRow = 11
    All = 12


class SeatsAlrm(BaseEnum):
    SeatFrontRow = 3
    SeatRearRow = 7
    SeatAll = 12

class BeltWarning(BaseEnum):
    # 安全带未系报警状态
    Normal = 0
    OccupiedAndFasten = 1
    Level1 = 2
    Level2Low = 3
    Level2High = 4
    Fault = 5
    
class BltFltSts(BaseEnum):
    # 安全带扣故障状态
    NoFault = 0
    Fault = 1
    Ukwn = 2


class BltLockSts(BaseEnum):
    # 安全带扣插入状态
    Unlock = 0
    Lock = 1
    Ukwn = 2


class SeatOccptSts(BaseEnum):
    # 座椅占位情况
    Empty = 0
    Fmale = 1
    OccptLrg = 2
    Ukwn = 3


class DriverSeatOccptSts(BaseEnum):
    # 座椅占位情况
    Undefd1 = 0
    OccptNotPrsnt = 1
    OccptPrsnt = 2
    Undefd2 = 3

class DiagActLineSts(BaseEnum):
    # 诊断激活线连接状态
    DisActive = 0
    Active = 1


class VentWorkStatus(BaseEnum):
    # 座椅通风工作状态
    kNone = 0
    On = 1
    Off = 2
    Error = 3
    FunctionLimit = 4
    EnergyLimit = 5
    Reserved1 = 6
    Reserved2 = 7


class BatteryThermalSts(BaseEnum):
    # 电池热管理当前工作状态
    kIdle = 0
    Cooling = 1
    Heating = 2
    Error = 3


class ThermalReqSts(BaseEnum):
    # 电池热管理目标指令
    Default = 0
    Heating = 1
    HeatFinished = 2
    RadiatorCooling = 3
    CompressorCooling = 4
    CoolingFinish = 5
    Inhibited = 6
    HeatingByEmotCoolt = 7
    Fault = 8


class TimeZone(BaseEnum):
    # 时区
    MIDDLE_ZONE = 0  #  中时区
    EAST_1 = 1  # 东一区
    EAST_2 = 2  # 东二区
    EAST_3 = 3  # 东三区
    EAST_4 = 4  # 东四区
    EAST_5 = 5  # 东五区
    EAST_6 = 6  # 东六区
    EAST_7 = 7  # 东七区
    EAST_8 = 8  # 东八区（默认值）
    EAST_9 = 9  # 东九区
    EAST_10 = 10  #  东十区
    EAST_11 = 11  #  东十一区
    EAST_12 = 12  #  东十二区
    WEST_12 = 13  #  西十二区
    WEST_11 = 14  #  西十一区
    WEST_10 = 15  #  西十区
    WEST_9 = 16  #  西九区
    WEST_8 = 17  #  西八区
    WEST_7 = 18  #  西七区
    WEST_6 = 19  #  西六区
    WEST_5 = 20  #  西五区
    WEST_4 = 21  #  西四区
    WEST_3 = 22  #  西三区
    WEST_2 = 23  #  西二区
    WEST_1 = 24  #  西一区
    EAST_3_30 = 25  # +03:30
    EAST_4_30 = 26  # +04:30
    EAST_5_30 = 27  # +05:30
    EAST_5_45 = 28  # +05:45
    EAST_6_30 = 29  # +06:30
    EAST_8_45 = 30  # +08:45
    EAST_9_30 = 31  # +09:30
    EAST_9_45 = 32  # +09:45
    EAST_10_30 = 33  # +10:30
    EAST_12_45 = 34  # +12:45
    EAST_13_45 = 35  # +13:45
    WEST_2_30 = 36  # -02:30
    WEST_3_30 = 37  # -03:30
    WEST_9_30 = 38  # -09:30


class TimeSyncSts(BaseEnum):
    Invalid = 0
    Default = 1
    RCT = 2
    NTP = 3
    GNSS = 4


class MASTER_REQUEST(BaseEnum):
    # FOTA Master服务的request
    GetStatus = 0
    GetTaskInfo = 1
    CancelFota = 2
    StartDownload = 3
    StopDownload = 4
    SuspendDownload = 5
    ResumeDownload = 6
    StartUpdate = 7
    GetConditionCheck = 8
    GetFunctionSts = 9
    StopUpdate = 10
    CheckTask = 20
    GetAppointment = 21
    CancelAppointment = 22
    SetAppointment = 23
    SetFirstCheckResult = 24


class UA_REQUEST(BaseEnum):
    # Update Agent服务的request
    GetStatus = 0
    SuspendDownload = 1
    ResumeDownload = 2
    CancelDownload = 3
    PreUpdate = 4
    StartUpdate = 5
    CancelUpdate = 6
    Rollback = 7
    Activate = 8
    FinishUpdate = 9
    Rescue = 10
    StartDownload = 20


class UA_EVENT(BaseEnum):
    # Update Agent服务event的字段
    Status = 0
    DownloadStatus = 1
    PreUpdateStatus = 2
    UpdateStatus = 3
    ErrorCode = 4
    DownloadFileSize = 5
    DownloadTotalFileSize = 6
    DownloadSpeed = 7
    Progress = 8
    UpdateFileSize = 9
    UpdateTotalFileSize = 10    


class MASTER_EVENT(BaseEnum):
    # FOTA Master服务event的字段
    Status = 0
    TaskId = 1
    ErrorCode = 2
    SerialNumber = 3
    TaskType = 4

class DOMAIN(BaseEnum):
    # 四大域控
    BGM = 0
    TCAM = 1
    CDC = 2
    ACU = 3


class VSP(BaseEnum):
    # VSP云端常规操作
    Repub = 0
    Cancel = 1
    Reset = 2
    UnFreeze = 3


class BlockName(BaseEnum):
    # RVS相关的数据块
    VehicleMode = 10102
    VehicleBody = 10103
    CabinStatus = 10104
    GISAndTravel = 10105
    DrivingStatus = 10106
    EicCharging = 10107
    BLEEicCharging = 10207
    WTIService = 10701
    WTIAutoDriveService = 10702
    BusStatus = 10109
    DeviceInfo = 10110
    EOLData = 10111
    Light = 10112
    APA = 19001


class VSP_PUBLIC_ACCOUNT():
    # VSP公共账号
    Name = 'bGl1Lnlhbmc='
    Password = __import__("os").environ.get('XAT_CREDENTIAL_____CONSTANTS_COMMON_PY_PASSWORD', "")
    # Name = 'cmVueXVlLmRhaQ=='
    # Password = 'eloxMjMxMjMxMjM='

class FOTAMasteSts(BaseEnum):
    IDLE = 0
    QUERY = 1
    NEW_TASK = 2
    DOWNLOADING = 3
    ACTIVE = 4
    UPDATE = 5
    ROLLBACK = 6
    FAILED_NOT_DRIVING = 7
    FAILED_DRIVING = 8
    SUCCESSFUL = 9
    REACH_APPOINTMENT = 10
    REMOTE_UPDATE = 11
    FACTORY_TASK = 20
    FACTORY_UPDATE = 21
    FACTORY_SUCCESSFUL = 22
    FACTORY_FAILED = 23
    RESCUE = 30


class LogLevel(BaseEnum):
    '''
    日志等级
    '''
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


class UA_Sts(BaseEnum):
    # UA 状态
    IDLE = 0
    DOWNLOAD = 1
    READY_TO_INSTALL = 2
    INSTALLING = 3
    UPDATE_FINISH = 4
    ROLLING_BACK = 5
    SYSTEM_ACTIVE = 6
    ERROR = 7
    ACTIVATING = 8
    UPDATE_FAILED = 9


UA_Status_Event = {
    "status": 0,
    "downloadStatus": {
        "downloadFileSize": 0,
        "totalFileSize": 0,
        "downloadSpeed": 0,
        "status": 255
    },
    "preUpdateStatus": {
        "progress": 0,
        "status": 255
    },
    "updateStatus": {
        "updateFileSize": 0,
        "totalFileSize": 0,
        "status": 255
    },
    "errorCode": 0
}


class ClimateZone(BaseEnum):
    AllZone = 0
    FirstRow = 1
    SecondRow = 2
    FirstRowLeft = 3
    FirstRowRight = 4
    SecondRowLeft = 5
    SecondRowMiddle = 6
    SecondRowRight = 7
    FirstRowLeftLeft = 8
    FirstRowLeftRight = 9
    FirstRowRightLeft = 10
    FirstRowRightRight = 11
    SecondRowLeftLeft = 12
    SecondRowLeftRight = 13
    SecondRowRightLeft = 14
    SecondRowRightRight = 15


class WindSpeed(BaseEnum):
    kOff = 0
    kLvlMan1 = 1
    kLvlMan2 = 2
    kLvlMan3 = 3
    kLvlMan4 = 4
    kLvlMan5 = 5
    kLvlMan6 = 6
    kLvlMan7 = 7
    kLvlMan8 = 8
    kLvlMan9 = 9
    kLvlAutoMinusMinus = 10
    kLvlAutoMinus = 11
    kLvlAutoNormal = 12
    kLvlAutoPlus = 13
    kLvlAutoPlusPlus = 14


class CycleMode(BaseEnum):
    Auto = 0
    AutoWithAirQuality = 1
    InternalCirculation = 2
    ExternalCirculation = 3


class CoolgReq(BaseEnum):
    Off = 0
    Auto = 1


class ExteriorLightMode(BaseEnum):
    Off = 0
    Auto = 1
    Position = 2
    LowHeam = 3


class ExtrLtgSts(BaseEnum):
    Off = 0
    On = 1
    Err = 2
    Resd = 3
    Auto = 4


class HighBeamSts(BaseEnum):
    Off = 0
    On = 1
    Err = 2

class AutoHighBeamSts(BaseEnum):
    Off = 0
    On = 1
    AHBC = 2
    AHBC_Temporarily_Off = 3
    Error = 4


class LowBeamClientId(BaseEnum):
    Reserve = 0
    GameMode = 1
    SteerWheelBut = 2
    Voice = 3
    ANP = 4
    AVP = 5
    AHBC = 6
    NoFunc = 255


class RemClimateSts(BaseEnum):
    Off = 0
    On = 1
    SignalMissing = 251
    SignalCounterFault = 252
    SignalChecksumFault = 253
    SignalE2EFault = 254
    Invalid = 255


class ChargingSts(BaseEnum):
    Default = 0
    NoCharging = 1
    ACCharging = 2
    ACChargingEnd = 3
    ChargingCmpl = 4
    Heating = 5
    Booking = 6
    NoDischarging = 7
    Discharging = 8
    DischargingEnd = 9
    DischargingCmpl = 10
    Chargingfault = 11
    DischargingFault = 12
    ACChrgnFltChrgrSide = 14
    DCCharging = 15
    DCChrgnFltVehSide = 18
    DCChrgnFltChrgrSideTempFlt = 19
    DCChrgnFltChrgrSideConFlt = 20
    DCChrgnFltChrgrSideHwFlt = 21
    DCChrgnFltChrgrSideEmgyFlt = 22
    DCChrgnFltChrgrSideComFlt = 23
    SuperCharging = 24
    ACChargingSuspend = 25
    DCChargingEnd = 26
    ACChrgnFltVehSide = 27
    Boostcharging = 28
    BoostchargingFlt = 29
    WirelessCharging = 30


class PluggerSts(BaseEnum):
    Disconnected = 0
    ConnectedWithoutPower = 1
    PowerAvailableButNotActivated = 2
    ConnectedWithPower = 3
    Init = 4
    Fault = 5
    Default = 6
    NotCompleteConnnected = 7
    DischargeConnectWithoutPowerInCar = 8
    DischargeConnectWithoutPowerOutCa = 9
    DischargeConnectwithPowerInCar = 10
    DischargeConnectwithPowerOutCar = 11


class BookChargeSts(BaseEnum):
    Default = 1
    On = 1
    Off = 2
    Reserve = 3


class HVActiveSts(BaseEnum):
    Open = 0
    Close = 1
    Keep = 2
    Open_And_Req_Act_Dcha = 3


class RemClimateSts(BaseEnum):
    Off = 0
    On = 1
    SignalMissing = 251
    SignalCounterFault = 252
    SignalChecksumFault = 253
    SignalE2EFault = 254
    Invalid = 255


class ChargingSts(BaseEnum):
    Default = 0
    NoCharging = 1
    ACCharging = 2
    ACChargingEnd = 3
    ChargingCmpl = 4
    Heating = 5
    Booking = 6
    NoDischarging = 7
    Discharging = 8
    DischargingEnd = 9
    DischargingCmpl = 10
    Chargingfault = 11
    DischargingFault = 12
    ACChrgnFltChrgrSide = 14
    DCCharging = 15
    DCChrgnFltVehSide = 18
    DCChrgnFltChrgrSideTempFlt = 19
    DCChrgnFltChrgrSideConFlt = 20
    DCChrgnFltChrgrSideHwFlt = 21
    DCChrgnFltChrgrSideEmgyFlt = 22
    DCChrgnFltChrgrSideComFlt = 23
    SuperCharging = 24
    ACChargingSuspend = 25
    DCChargingEnd = 26
    ACChrgnFltVehSide = 27
    Boostcharging = 28
    BoostchargingFlt = 29
    WirelessCharging = 30

class BookChargeSts(BaseEnum):
    Default = 1
    On = 1
    Off = 2
    Reserve = 3


class HVActiveSts(BaseEnum):
    Open = 0
    Close = 1
    Keep = 2
    Open_And_Req_Act_Dcha = 3
    Auto = 1


class SESSION:
    EMPTY = 0
    DEFAULT = 1
    PROGRAMMING = 2
    EXTENDED = 3


class TA:
    BGM_SOC = 0x1001
    BGM_MCU = 0x1002
    TCAM = 0x1011
    FUNCTION = 0x1FFF


class UnLock:
    L0 = 0
    L1 = 1
    L3 = 3
    L5 = 5
    L7 = 7
    L11 = 11


class Check_Method:
    response = 0
    read = 1
    reset = 2
    kl30 = 3


class RadarSts(BaseEnum):
    Not_Init = 0
    Init = 1
    Standby = 2
    Active = 3
    Failure = 4
    SensorBlockage = 5
    Reserved1 = 6
    Reserved2 = 7
    Reserved3 = 8
    Reserved4 = 9


class EpbSts(BaseEnum):
    Resd0 = 0
    Resd1 = 1
    Resd2 = 2
    AllAppld = 3
    Resd4 = 4
    AllInTran = 5
    BrkgDynByActr = 6
    Resd7 = 7
    Resd8 = 8
    ActrAllReld = 9
    BrkgDynDegraded = 10
    Resd11 = 11
    BrkgDyn = 12
    Resd13 = 13
    Resd14 = 14
    Err = 15


class TroubleLightSts(BaseEnum):
    LampOff = 0
    Unknown = 1
    LampFlash = 2
    LampOn = 3


class AirbagLampReqSts(BaseEnum):
    LampOff = 0
    Unknown = 1
    LampFlash = 2
    LampOn = 3


class AirbagWarningSts(BaseEnum):
    NotVld1 = 0
    Off = 1
    On = 2
    NotVld2 = 3


class PedestProtectFltSts(BaseEnum):
    NotVld1 = 0
    Off = 1
    On = 2
    NotVld2 = 3


class PedestProtectImpctSts(BaseEnum):
    Off = 0
    On = 1


class LightType(BaseEnum):
    LightBrake = 0
    LightEyebrow = 1
    LightHazard = 2
    LightDaytime = 3
    LightFog = 4
    LightHighBeam = 5
    LightLowBeam = 6
    LightOutLine = 7
    LightReverse = 8
    LightHeadLamp = 9
    LightSteer = 10
    LightPosition = 11
    LightWelcome = 12
    LightPixel = 13
    LightDidrl = 14
    LightLicense = 15
    LightSteerMirror = 16
    LightDoorAlarm = 17
    LightCorner = 18
    LightPuddle = 19
    LightBlind = 21
    LightReading = 22
    LightBackground = 23
    LightFoot = 24
    LightSmartAmbient = 25
    LightCourtesy = 26
    LightTrunk = 27
    LightArmRestBox = 28
    LightRoof = 29
    LightSide = 30
    LightGlove = 31
    LightOvertake = 32
    LightSteerWheel = 33
    LightGeneralAmbient = 35
    LightAFS = 36
    LightAHL = 37
    LightPositionPattern = 38
    kAILamp = 39
    LightSystem = 100


class LightZone(BaseEnum):
    LightZoneAllOrSingle = 0
    LightZoneFrontLeft = 1
    LightZoneFrontRight = 2
    LightZoneRearLeft = 3
    LightZoneRearRight = 4
    ZoneMiddleRear = 5
    LightZoneThreeRowLeft = 6
    LightZoneThreeRowRight = 7
    LightZoneMiddleThreeRow = 8
    LightZoneFront = 9
    LightZoneRear = 10
    LightZoneThreeRow = 11
    LightZoneLeft = 12
    LightZoneRight = 13
    LightZoneRing = 14
    LightIpLeft = 15
    LightIpRight = 16
    LightTweeterLeft = 17
    LightTweeterRight = 18
    LightConsoleLeft = 19
    LightConsoleRight = 20
    leftY1Sts = 21
    leftY2Sts = 22
    leftY3Sts = 23
    leftY4Sts = 24
    rightY1Sts = 25
    rightY2Sts = 26
    rightY3Sts = 27
    rightY4Sts = 28


class LightMode(BaseEnum):
    NA = 255
    Off = 0
    On = 1
    Auto = 2
    Flash = 3
    AdasStatus1 = 4
    AdasStatus2 = 5
    AdasStatus3 = 6
    AdasStatus4 = 7
    AdasStatus5 = 8
    AdasStatus6 = 9
    AdasStatus7 = 10
    AdasStatus8 = 11
    AdasStatus9 = 12
    AdasStatus10 = 13
    AdasStatus11 = 14


class ReadLampZone(BaseEnum):
    FrontLeft = 1
    FrontRight = 2
    RearLeft = 3
    RearRight = 4


class ReadLampSts(BaseEnum):
    Unknow = 0
    AllOff = 1
    Courtesy = 2
    Manual = 3
    Polite = 4
    ForceOn = 5
    ForceOff = 6


class PixelType(BaseEnum):
    RgbBmp = 0
    ByteCustomized = 1


# class TirePosition(BaseEnum):
#     FrontLeft = 0
#     FrontRight = 1
#     RearRight = 2
#     RearLeft = 3


class SysWarnFlg(BaseEnum):
    SysWarnFlg = 0
    PWarnFlg = 1
    TWarnFlg = 2
    MsgOldFlg = 3
    FastLoseWarnFlg = 4
    BattLoSt = 5


class TireAlarmSts(BaseEnum):
    Normal = 0
    LowPressureWarning = 1
    HighPressureWarning = 2
    Reserve = 3


class TirePos(BaseEnum):
    FrontLeft = 1
    FrontRight = 2
    RearRight = 3
    RearLeft = 4
    All = 5


class BattMaintReqSts(BaseEnum):
    Start = 0
    Finish = 1


class ClimateCycleReq(BaseEnum):
    Aut = 0  # 自动
    AutWithAirQly = 1  # 自动＋空气净化
    RecircFull = 2  # 内循环
    OscircFull = 3  # 外循环


class SeatVenPos(BaseEnum):
    Front = 0
    Rear = 1
    All = 2


class SeatVenSpeed(BaseEnum):
    Off = 0
    LvlMan1 = 1
    LvlMan2 = 2
    LvlMan3 = 3
    LvlMan4 = 4
    LvlMan5 = 5
    LvlMan6 = 6
    LvlMan7 = 7
    LvlMan8 = 8
    LvlMan9 = 9
    LvlAutMinusMinus = 10
    LvlAutMinus = 11
    LvlAutNorm = 12
    LvlAutPlus = 13
    LvlAutPlusPlus = 14
    Reserved = 15


class StalkId(BaseEnum):
    StalkRight = 0
    StalkLeft = 1
    All = 2


class PressType(BaseEnum):
    kNone = 0
    LightPress = 1
    FullPress = 2
    Error = 3
    E2eCheckError = 4


class LinChannel(BaseEnum):
    LIN1 = 1
    LIN2 = 2
    LIN3 = 3
    LIN4 = 4
    LIN5 = 5
    LIN6 = 6


class BusSendSts(BaseEnum):
    Sleep = 0
    Awakeup = 1


class UnlockStep(BaseEnum):
    seed = 0
    key = 1


class RemoteClimateStatus(BaseEnum):
    Off = 0
    On = 1
    Invalid = 255


class ClimateZoneId(BaseEnum):
    AllZone = 0
    FirstRow = 1
    SecondRow = 2
    FirstRowLeft = 3
    FirstRowRight = 4
    SecondRowLeft = 5
    SecondRowMiddle = 6
    SecondRowRight = 7
    FirstRowLeftLeft = 8
    FirstRowLeftRight = 9
    FirstRowRightLeft = 10
    FirstRowRightRight = 11
    SecondRowLeftLeft = 12
    SecondRowLeftRight = 13
    SecondRowRightLeft = 14
    SecondRowRightRight = 15


class WindMode(BaseEnum):
    WindFoot = 0
    WindFace = 1
    WindDefrst = 2
    WindFootDefrst = 3
    WindFootFace = 4
    WindFaceDefrst = 5
    WindFootFaceDefrst = 6
    WindAuto = 7


class CoolingHeatingStatus(BaseEnum):
    kNone = 0
    Cooling = 1
    Heating = 2
    CoolingAndHeating = 3
    Invalid = 4


class FaultId(BaseEnum):
    OK = 0
    FaultOutletError = 1
    FaultExternalTempSensorError = 2
    FaultInternalTempSensorError = 3
    FaultOutletEnergyLimit = 4
    FaultAQSSensorError = 5
    FaultCoolantLow = 6
    FaultBatteryLow = 7
    FaultCoolantLowAndBatteryLow = 8
    FaultTemperatureLow = 9
    FaultTemperatureHigh = 10

    FaultClimateError = 11
    FaultHighVoltageError = 12
    FaultActivationLimited = 13


class TriggerSourceId(BaseEnum):
    NoTriggerSource = 0
    RemoteKey = 1
    KeyLessPassive = 2
    InteriorSwitches = 3
    SpeedLocking = 4
    Relocking = 5
    SlamLocking = 6
    Telematices = 7
    CrashUnlock = 8
    Approach = 9
    OutsideOthers = 10
    InsideOthers = 11
    NFC = 12


class LockStatus(BaseEnum):
    Undef = 0
    Unlocked = 1
    FourDoorLockedTailUnlocked = 2
    AllLocked = 3


class ShieldWindowId(BaseEnum):
    ShieldWindowAll = 0
    ShieldWindowFront = 1
    ShieldWindowRear = 2


class HeatStatus(BaseEnum):
    HeatStatusOff = 0
    HeatStatusOn = 1
    HeatStatusAutoOn = 2
    HeatFault = 3


class ViewId(BaseEnum):
    RearViewRight = 0
    RearViewLeft = 1
    RearViewAll = 2


class HeatVentWorkStatus(BaseEnum):
    kNone = 0
    On = 1
    Off = 2
    Error = 3
    FunctionLimit = 4
    EnergyLimit = 5
    Reserved1 = 6
    Reserved2 = 7


class SteerHeatAvailiable(BaseEnum):
    kNone = 0
    On = 1
    Off = 2
    Error = 3
    Funcational_Limit = 4
    Energy_Limit = 5


class PedalId(BaseEnum):
    PedalAcc = 0
    PedalBraker = 1
    PedalAll = 2


class PressedStatus(BaseEnum):
    PedalReleased = 0
    PedalPressed = 1
    PedalNA = 2


class AirWindMode(BaseEnum):
    Foot = 0
    Face = 1
    Defrst = 2
    FootDefrst = 3
    FootFace = 4
    FaceDefrst = 5
    FootFaceDefrst = 6
    Auto = 7


class AirVentReqPos(BaseEnum):
    DrvrLeft = 0
    DrvrRight = 1
    PassLeft = 2
    PassRight = 3
    SecRow = 4
    All = 5


class AirVentReqSts(BaseEnum):
    Off = 0
    On = 1


class KeyConfigType(BaseEnum):
    AutoLockOnLeave = 0
    AutoLockOnApproach = 1
    LightOnApproache = 2
    DoorAutoOpenOnUnlock = 3
    WindowAutoCloseOnLock = 4
    SetPEKeySearchDedicateZone = 5


class HornStatus(BaseEnum):
    On = 0
    Off = 1
    NA = 2


class HeatVentiLvl(BaseEnum):
    Off = 0
    Level1 = 1
    Level2 = 2
    Level3 = 3


class MassType(BaseEnum):
    Type1 = 0
    Type2 = 1
    Type3 = 2
    Type4 = 3
    Type5 = 4
    Type6 = 5
    Type7 = 6
    Type8 = 7


class MassIntensity(BaseEnum):
    Low = 0
    Normal = 1
    High = 2
    Off = 3


class SeatPart(BaseEnum):
    Seat = 0
    SeatBack = 1
    SeatLegrest = 2
    SeatLumbar = 3


class AdjustDirection(BaseEnum):
    Forward = 0
    Left = 1
    Up = 2
    Backward = 3
    Right = 4
    Down = 5


class HeatVentiSts(BaseEnum):
    None_ = 0
    On = 1
    Off = 2
    Error = 3
    Functionallimit = 4
    Energylimit = 5
    Resvd1 = 6
    Resvd2 = 7


class CnvnReq(BaseEnum):
    NotReqd = 0
    Chrgn = 1
    Resd1 = 2
    Resd2 = 3
    Resd3 = 4
    Resd4 = 5
    Resd5 = 6
    Resd6 = 7


class CnvnAllwd(BaseEnum):
    NotOk = 0
    OK = 1


class IPMLoUWakeUpReq(BaseEnum):
    NotReqd = 0
    Chrgn = 1
    NotChrgn = 2
    Invalid = 3


class LockCmd(BaseEnum):
    UnLock = 0
    Lock = 1
    AllDoorCloseAndLock = 2
    LockCompleteArm = 3


class LockReqSource(BaseEnum):
    Ble_Rke = 0
    Talematics = 1
    Hmi = 2
    APA = 3

class FindKeyType(BaseEnum):
    NoReq = 0
    OutsideKey = 1
    InsideKey = 2
    OutsideAndInsideKey = 3

class LockSource(BaseEnum):
    RKE = 0
    Telm = 1
    HMI = 2
    NFC = 3
    Apprch = 4
    KV_PEPS = 5
    Crash = 6
    SpdAut = 7
    TmrAut = 8
    OutsOth = 9
    InsOth = 10
    APA = 11

class ThermalRequestType(BaseEnum):
    kNoRequest = 0
    kCoolingRequest = 1
    kHeatingRequest = 2
    kCoolingAndHeatingRequest = 3
    kPostHeating = 4
    kBookHeating = 5
    
class LockSts(BaseEnum):
    Undef = 0
    Unlocked = 1
    FourDoorLockedTailUnlocked = 2
    AllLocked = 3


class TailGateCmd(BaseEnum):
    Open = 0
    Close = 1
    Stop = 2


class TailGatePos(BaseEnum):
    pos20 = 20
    pos50 = 50
    pos80 = 80


class TailGateSts(BaseEnum):
    kOpened = 0
    kClosing = 1
    kClosed = 2
    kOpening = 3
    kHover = 4
    kNA = 5
    kClosingBreak = 6
    kOpeningBreak = 7
    kHalfClosed = 8
    kInvalid = 65535


class CarLocalTraceReq(BaseEnum):
    kNoReq = 0  # 无请求
    kHornReq = 1  # 喇叭请求
    kLiReq = 2  # 灯光请求
    kHornLiReq = 3  # 喇叭和灯光同时请求


class CarLocalTraceActiveStatus(BaseEnum):
    kIdle = 0  # 未寻(Default)
    kSuccess = 1  # 寻车成功
    kFail = 2  # 寻车失败
    kInvalid = 3  # 无效


class TurnLampMode(BaseEnum):
    kStop = 0  # 转向灯关闭
    kLeft = 1  # 左转向灯开启
    kRight = 2  # 右转向灯开启
    kHazard = 3  # 危险报警灯开启
    Release = 255 #释放独占需求


class DoorId(BaseEnum):
    kDoorFrontLeft = 0
    kDoorFrontRight = 1
    kDoorRearLeft = 2
    kDoorRearRight = 3
    kDoorAll = 4


class DoorIsOpen(BaseEnum):
    FALSE = 0
    TRUE = 1


class DoorStatus(BaseEnum):
    kOpened = 0  # 全开
    kClosing = 1  # 关闭中
    kClosed = 2  # 全关
    kLocked = 3  # 未使用
    kUnlocked = 4  # 未使用
    kOpening = 5  # 开启中
    kHover = 6  # 悬停
    kNA = 7  # 未知
    kClosingBreak = 8  # 关闭过程中减速
    kOpeningBreak = 9  # 开启过程中减速
    kHalfClosed = 10  # 半锁状态(门锁卡在一半且门开度很小)
    kInvalid = 65535  # (Default)


class WindowId(BaseEnum):
    kWindowFrontLeft = 0
    kWindowFrontRight = 1
    kWindowRearLeft = 2
    kWindowRearRight = 3
    kWindowAll = 4
    PdmWindowPass= 4
    RldmWindowRele=5
    RrdmWindowReRi=6

class WindowPos(BaseEnum):
    windowpos0 = 0
    windowpos4 = 4
    windowpos8 = 8
    windowpos12 = 12
    windowpos16 = 16
    windowpos20 = 20
    windowpos24 = 24
    windowpos28 = 28
    windowpos32 = 32


class ChargeLidSts(BaseEnum):
    kOpened = 0  # 口盖运动行程在6%~100%均表示打开
    kClosing = 1  # 仅预留
    kClosed = 2  # 口盖运动行程在0%~5%均表示关闭
    kLocked = 3  # 仅预留
    kUnlocked = 4  # 仅预留
    kOpening = 5  # 仅预留
    kHover = 6  # 仅预留
    kNA = 7


class MirrStsTyp(BaseEnum):
    Undefd = 0
    Unfold = 1
    Fold = 2
    MovgToUnfold = 3
    MovgToFold = 4


class FoldHmiReq(BaseEnum):
    NotPsd = 0
    Psd = 1

class AutoFoldReq(BaseEnum):
    Idle = 0
    FoldIn = 1
    FoldOut = 2

class MASTER_NotifyAppointTime_EVENT(BaseEnum):
    # FOTA Master服务NotifyAppointTime event的字段
    TaskId = 0
    Type = 1
    AppointmentTime = 2


class FragChannel(BaseEnum):
    NoReq = 0
    Channel1 = 1
    Channel2 = 2
    Channel3 = 3
    Channel4 = 4
    Channel5 = 5


class FragLevel(BaseEnum):
    LevelOff = 0
    Level1 = 1
    Level2 = 2
    Level3 = 3


class ActiveStatus(BaseEnum):
    Active = 0
    Level1 = 1
    Invalid = 2


class DoorSide(BaseEnum):
    Inside = 0
    Outside = 1


class SwitchSts(BaseEnum):
    Unknow = 0
    Pressed = 1
    NotPressed = 2


class DoorOpenSource(BaseEnum):
    NoTrigSrc = 0
    KeyRem = 1
    HMI = 2
    Telm = 3
    OutdSwt = 4
    InsdSwt = 5


class DoorOpenSts(BaseEnum):
    Open = 0
    Close = 1
    Stop = 2


class PM25Sts(BaseEnum):
    Initial = 0
    Collecting = 1
    Complete = 2
    Error = 3


class PM25Level(BaseEnum):
    Level1 = 0
    Level2 = 1
    Level3 = 2
    Level4 = 3
    Level5 = 4
    Level6 = 5
    Reserved = 6
    Invalid = 7


class MirrrDefrstrSts(BaseEnum):
    Off = 0
    Limited = 1
    NotAvailable = 2
    TmrOff = 1
    AutoCdn = 2


class SeatAdjustType(BaseEnum):
    Height = 0
    Len = 1
    Back = 2
    Legrest = 3
    Lumbar = 4


class SeatUpDownAdj(BaseEnum):
    Idle = 0
    Up = 1
    Down = 2


class SeatForwBackAdj(BaseEnum):
    Idle = 0
    Forward = 1
    Backward = 2


class FOTA_Skip_Debug():
    CDC_UA = 'cdc_ua'
    ACU_UA = 'acu_ua'
    update_precondition_check = 'update_precondition_check'
    baseline = 'baseline:6100000200 DZ'
    bridge_baseline = 'baseline:6100000200CCC'
    upload_version_from_debug_file = 'upload_version_from_debug_file'
    ecm3_down_hv = 'ecm3_down_hv'
    before_group_1081 = 'before_group_1081'
    before_group_hv_ctl = 'before_group_hv_ctl'
    fota_mode_requeset_ecm3 = 'fota_mode_requeset_ecm3'
    fota_mode_requeset_acu = 'fota_mode_requeset_acu'
    fota_mode_requeset_cdc = 'fota_mode_requeset_cdc'
    car_mode_normal = 'car_mode_normal'
    version_collect = 'version_collect'
    wait_hmi = 'wait_hmi'
    start_download = 'start_download'
    time_check = 'time_check'
    cdc_acu_doip_check = 'cdc_acu_doip_check'
    factory_ecu_ver_collection = 'factory_ecu_ver_collection'


class MsgSendContrl(BaseEnum):
    Start = 0
    Stop = 1
    Pause = 2


class SteerAsscLvl(BaseEnum):
    Ukwn = 0
    Lvl1 = 1
    Lvl2 = 2
    Lvl3 = 3
    Lvl4 = 4
    Resd5 = 5
    Resd6 = 6
    Resd7 = 7


class OutletSide(BaseEnum):
    Left = 0
    Right = 1


class GeneralPos(BaseEnum):
    Front = 0
    Rear = 1
    Left = 2
    Right = 3
    All = 4
    Mid = 5


class LampSts(BaseEnum):
    Off = 0
    On = 1
    Error = 2
    Reserve = 3


class LockSysStsPrmt(BaseEnum):
    Idle = 0
    NFC_PSD = 1
    ANTI_LOCK_KEY_FORGET = 2
    NO_KEY_PRESENT = 3
    CLOSE_DOOR_AUDIO = 4
    ANTI_RELOCK = 5
    AUTO_RELOCK = 6


class Network_Mode(BaseEnum):
    Fourth_Generation = 0
    Fifth_Generation = 1


class SA_sts(BaseEnum):
    On = 1  # (5G网络打开)
    Off = 2  # (LTE网络)


class Cell_band(BaseEnum):
    SA = 21
    LTE = 2


class ApnSts(BaseEnum):
    available = 0
    unavailable = 1


class BlueType(BaseEnum):
    NoKeyConnected = 0
    NFC_Card = 1
    BLE_Key = 2
    BLE_UWB_KeyFob = 3
    Temp_BLE_Key = 4
    ICCE_BLE_Key = 5
    ICCE_NFC_Key = 6
    CCC_NFC_BLE_UWB_Key = 7
    CCC_NFC_Key = 8
    CCC_NFC_BLE_Key = 9


class ConnSts(BaseEnum):
    Disconnect = 0
    Connect = 1


class ChrgLidOperType(BaseEnum):
    Open = 0
    Close = 1


class ChrgLidSts(BaseEnum):
    Opened = 0
    Closing = 1
    Closed = 2
    Locked = 3
    Unlocked = 4
    Opening = 5
    Hover = 6
    NA = 7

class HvBattThermReq(BaseEnum):
    Idle = 0
    Cooling = 1
    Heating = 2
    Erro = 3


class ChrgLidOpenCloseSts(BaseEnum):
    Ukwn = 0
    Open = 1
    Close = 2

class ChrgLidConnectSts(BaseEnum):
    Disconnected = 0
    ConnectedWithoutPower = 1
    PowerAvailableButNotActivated = 2
    ConnectedWithPower = 3
    Init = 4
    Fault = 5
    
class ChrgLidReq(BaseEnum):
    Idle = 127
    Open = 0
    Close = 100

class ChrgLidSts(BaseEnum):
    Ukwn = 127
    Open = 0
    Close = 100


class ChrdLidFaultType(BaseEnum):
    ElecErr = 0
    TempHigh = 1
    VoltHigh = 2    
    VoltLow = 3
    All = 4

class OccupySts(BaseEnum):
    NotOccupied = 0
    Occupied = 1
    Invalid = 2


class SeatOccupySts:
    def __init__(self,sensor_sts:OccupySts = OccupySts.NotOccupied,sts:OccupySts = OccupySts.NotOccupied):
        self.sensor_sts = sensor_sts
        self.sts= sts


class XcallConstants(BaseEnum):
    ON = 1
    OFF = 0


class eCallSts(BaseEnum):
    kIDLE = 0                # 已取消/default
    kDIALING = 1             # 正在拨号
    kRINGING = 2             # 正在响铃
    kVOICE_CONVERSATIO = 3   # 通话已接通状态
    kINCOMING_CALL = 4       # 来电未接通状态（reserved）
    kHANG_UP = 5             # 已挂断
    kWAIT_FOR_CONFIRM = 6    # 倒计时等待确认中（reserved)
    kCALL_FAILURE = 7        # 呼叫失败：由于业务或网络繁忙等导致未接通


class eCallReqSource(BaseEnum):
    kCDC = 0                 # CDC
    kACU = 1                 # ACU


class eCallOperCmd(BaseEnum):
    kNO_REQUEST = 0          # 无请求
    kSTART_ECALL = 1         # 开始eCall
    kCANCEL_ECALL = 2        # 取消eCall
    kPICK_UP_ECALL = 3       # 接听eCall
    kHANG_UP_ECALL = 4       # 挂断eCall
    kCONFIRM_ECALL = 5       # 确认拨打eCall

class bCallOperCmd(BaseEnum):
    kNO_REQUEST = 0          # 无请求
    kSTART_BCALL = 1         # 开始bCall
    kCANCEL_BCALL = 2        # 取消bCall
    kHANG_UP_BCALL = 3       # 挂断bCall

class eCallFunSts(BaseEnum):
    kREADY = 0               # 无故障
    kECALL_ERROR_MINOR = 1   # 轻微故障
    kECALL_ERROR_SEVERE = 2  # 严重故障


class eCallType(BaseEnum):
    kIDLE = 0                # 默认状态
    kACTIVE = 1              # 主动通话
    kPASSIVE = 2             # 被动通话
    kINCOMING = 3            # 电话回拨

 
class FacQlyDoorSts(BaseEnum):
    Uknow = 0
    Open = 1
    Close = 2

class UA_ErrorCode(BaseEnum):
    None_0x00_0x00 = 0
    FotaStateError_0x02_0x06 = 518
    Insufficient_Resources_0x02_0x07 = 519
    PayLoadError_0x02_0x24 = 548
    DL_HTTPS_TimeoutError_0x02_0x08 = 520
    DL_TLS_Error_0x02_0x09 = 521
    DL_File_Change_0x02_0x0A = 522
    DNS_Error_0x02_0x0B = 523
    FileSecurityCheck_Error_0x02_0x22 = 546
    Service_Unavailable_0x02_0x0C = 524
    Not_Found_0x02_0x0D = 525
    General_Error_0x02_0x21 = 545
    File_Size_Error_0x02_0x25 = 549
    FotaStateError_0x03_0x0C = 780
    PackageMissing_0x03_0x0D = 781
    VBFFormat_Error_0x03_0x0E = 782
    Decryption_Error_0x03_0x0F = 783
    VBF_Signature_verification_Error_0x03_0x10 = 784
    Insufficient_Resourcesr_0x03_0x12 = 786
    Software_Call_failed_0x03_0x13 = 787
    Software_Incompatibility_0x03_0x14 = 788
    Differential_Baseline_Error_0x03_0x15 = 789
    UpdateError_0x03_0x16 = 790
    CallFunctionTimeOut_0x03_0x2C = 812
    IntegratedFailed_0x03_0x17 = 791
    RollBackError_0x03_0x18 = 792
    Permission_Error_0x03_0x19 = 793
    CancelError_0x03_0x1A = 794
    Reset_Condition_Error_0x03_0x1B = 795
    Reset_Error_0x03_0x1C = 796
    DeletePackage_Error_0x03_0x05 = 773
    ChangState_Error_0x03_0x06 = 774
    CanNotCancel_0x03_0x07 = 775
    VBFVersionError_0x03_0x11 = 785
    IntsallSocFailed_0x09_0x07 = 2311
    
class MASTER_ConditionCheckResults_EVENT(BaseEnum):
    # FOTA Master服务ConditionCheckResults event的字段
    CheckConditionType = 0
    Results = 1
    
class FOTA_ConditionCheck_Type(BaseEnum):
    Immediate_Update = 0
    Scheduled_Update = 1
    Factory_Update = 2

class FOTA_ConditionCheck_Code(BaseEnum):
    CR_SUCCESSFUL = 0
    CR_HV_ERROR = 1
    CR_NOT_GEAR_P = 2
    CR_LV_ERROR = 3
    CR_HT_ERROR = 4
    CR_SPEED_ERROR = 5
    CR_SOH_ERROR = 6
    CR_VMM_ERROR = 7
    CR_VOLTAGE_ERROR = 8
    CR_DIAGNOSTIC_ERROR = 9
    CR_CHARGING_ERROR = 10
    CR_APA_ENABLE_ERROR = 11
    CR_AVP_ENABLE_ERROR = 12
    CR_ECALL_ERROR = 13
    CR_BCALL_ERROR = 14
    CR_CHECK_CONDITION_TIMEOUT_ERROR = 15
    CR_HWPN_ERROR = 16
    CR_PET_MODE_ERROR = 17
    CR_MNTN_MODE_ERROR = 18
    CR_PARKING_COMFORT_MODE_ERROR = 19
    CR_DOIP_NODE_ERROR = 20
    CR_NETWORK_ERROR = 21
    CR_DISCHARGING_ERROR = 22

class BusName(BaseEnum):
    bodycan = 'bodycan'
    propulsioncan = 'propulsioncan'
    chassiscan1 = 'chassiscan1'
    chassiscan2 = 'chassiscan2'
    passivesafetycan = __import__("os").environ.get('XAT_CREDENTIAL_____CONSTANTS_COMMON_PY_PASSIVESAFETYCAN', "")
    diagnosticcan = 'diagnosticcan'
    infocanfd = 'infocanfd'
    bodyexposedcanfd = 'infocanfd'
    adcanfd = 'infocanfd'
    connectivitycanfd = 'connectivitycanfd'
    bodyalmcanfd1 = 'bodyalmcanfd1'
    bodyalmcanfd2 = 'bodyalmcanfd2'
    cem_lin1 = 'cem_lin1'
    cem_lin2 = 'cem_lin2'
    cem_lin3 = 'cem_lin3'
    cem_lin4 = 'cem_lin4'
    cem_lin5 = 'cem_lin5'
    cem_lin6 = 'cem_lin6'
    backbonefr= 'backbonefr'


class NMSts(BaseEnum):
    no_valid = 0
    valid = 1


class NMMsgId(BaseEnum):
    x501 = 0x501
    x502 = 0x502
    x503 = 0x503
    x509 = 0x509
    x528 = 0x528
    x52A = 0x52A
    x533 = 0x533


class BGMPNC(BaseEnum):
    PNC16 = 'PNC16_BGM'
    PNC17 = 'PNC17_BGM'
    PNC18 = 'PNC18_BGM'
    PNC19 = 'PNC19_BGM'
    PNC20 = 'PNC20_BGM'
    PNC21 = 'PNC21_BGM'
    PNC22 = 'PNC22_BGM'
    PNC23 = 'PNC23_BGM'
    PNC24 = 'PNC24_BGM'
    PNC25 = 'PNC25_BGM'
    PNC26 = 'PNC26_BGM'
    PNC27 = 'PNC27_BGM'
    PNC28 = 'PNC28_BGM'
    PNC29 = 'PNC29_BGM'
    PNC30 = 'PNC30_BGM'
    PNC31 = 'PNC31_BGM'
    PNC32 = 'PNC32_BGM'
    PNC33 = 'PNC33_BGM'
    PNC34 = 'PNC34_BGM'
    PNC35 = 'PNC35_BGM'
    PNC36 = 'PNC36_BGM'
    PNC37 = 'PNC37_BGM'
    PNC38 = 'PNC38_BGM'
    PNC39 = 'PNC39_BGM'
    PNC40 = 'PNC40_BGM'
    PNC41 = 'PNC41_BGM'
    PNC42 = 'PNC42_BGM'


class TCAMPNC(BaseEnum):
    PNC16 = 'PNC16_TCAM'
    PNC17 = 'PNC17_TCAM'
    PNC18 = 'PNC18_TCAM'
    PNC19 = 'PNC19_TCAM'
    PNC20 = 'PNC20_TCAM'
    PNC21 = 'PNC21_TCAM'
    PNC22 = 'PNC22_TCAM'
    PNC23 = 'PNC23_TCAM'
    PNC24 = 'PNC24_TCAM'
    PNC25 = 'PNC25_TCAM'
    PNC26 = 'PNC26_TCAM'
    PNC27 = 'PNC27_TCAM'
    PNC28 = 'PNC28_TCAM'
    PNC29 = 'PNC29_TCAM'
    PNC30 = 'PNC30_TCAM'
    PNC31 = 'PNC31_TCAM'
    PNC32 = 'PNC32_TCAM'
    PNC33 = 'PNC33_TCAM'
    PNC34 = 'PNC34_TCAM'
    PNC35 = 'PNC35_TCAM'
    PNC36 = 'PNC36_TCAM'
    PNC37 = 'PNC37_TCAM'
    PNC38 = 'PNC38_TCAM'
    PNC39 = 'PNC39_TCAM'
    PNC40 = 'PNC40_TCAM'
    PNC41 = 'PNC41_TCAM'
    PNC42 = 'PNC42_TCAM'


class FrameType(BaseEnum):
    quick = 0
    slow = 1


class LampPos(BaseEnum):
    FrontLeft = 0
    FrontRight = 1
    RearLeft = 2
    RearMid = 3
    RearRight = 4
    All = 5

class PosnLampSts(BaseEnum):
    Off = 0
    On = 1
    Error = 2
    Resd = 3

class VehType(BaseEnum):
    Old = 0
    New = 1

class RotateDirec(BaseEnum):
    Left = 0
    Right = 1
    All = 2

class SteerWhlTouchSwt(BaseEnum):
    NotAvailble = 0
    ShortPress = 1
    LongPress = 2
    Error = 3
    


key_id0 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
key_id1 = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]
key_id2 = [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F]
key_id3 = [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x2F]
key_id4 = [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x3F]
key_id5 = [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x4F]
key_id6 = [0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x5F]

class Location(Enum):
    """寻钥匙区域"""
    Idle = 0
    ALL = auto()
    AllExt = auto()
    DrvrExt = auto()
    PassExt = auto()
    TrExt = auto()
    AllInt = auto()
    DrvrInt = auto()
    PassInt = auto()
    ResvInt = auto()
    ResvIntSimple = auto()

class KeyType(Enum):
    """钥匙类型"""
    NoKeyConnected = 0
    NFC_Card = auto()
    BLE_Key = auto()
    BLE_UWB_KeyFob = auto()
    Temp_BLE_Key = auto()
    ICCE_BLE_Key = auto()
    ICCE_NFC_Key = auto()
    CCC_NFC_BLE_UWB_Key = auto()
    CCC_NFC_Key = auto()
    CCC_NFC_BLE_Key = auto()

class InternalExternalStatus(Enum):
    """钥匙所在区域"""
    SearchSts_Idle = 1
    ExternalSearchSts_FrntFound = auto()
    ExternalSearchSts_LeftFnd = auto()
    ExternalSearchSts_RightFnd = auto()
    ExternalSearchSts_RearFnd = auto()
    ExternalSearchSts_Found = auto()
    Reserved = auto()
    InternalSearchSts_Found = auto() # 8
    SearchSts_NotFound = auto()
    ExternalSearchSts_LeftFnd_RearFnd = auto()
    ExternalSearchSts_RightFnd_RearFnd = auto()

class KeyInfo:
    def __init__(self, key_type: Union[KeyType, int], key_id: list, key_status: Union[InternalExternalStatus, int]) -> None:
        self.keyType = key_type if isinstance(key_type, int) else key_type.value
        self.keyID = key_id
        self.key_status = key_status if isinstance(key_status, int) else key_status.value

    def format_key_info(self):
        """将该钥匙信息格式化为列表形式返回"""
        return [self.keyType] + self.keyID + [self.key_status]

class KeyType(Enum):
    """钥匙类型"""
    NoKeyConnected = 0
    NFC_Card = auto()
    BLE_Key = auto()
    BLE_UWB_KeyFob = auto()
    Temp_BLE_Key = auto()
    ICCE_BLE_Key = auto()
    ICCE_NFC_Key = auto()
    CCC_NFC_BLE_UWB_Key = auto()
    CCC_NFC_Key = auto()
    CCC_NFC_BLE_Key = auto()

class InternalExternalStatus(Enum):
    """钥匙所在区域"""
    SearchSts_Idle = 1
    ExternalSearchSts_FrntFound = auto()
    ExternalSearchSts_LeftFnd = auto()
    ExternalSearchSts_RightFnd = auto()
    ExternalSearchSts_RearFnd = auto()
    ExternalSearchSts_Found = auto()
    Reserved = auto()
    InternalSearchSts_Found = auto() # 8
    SearchSts_NotFound = auto()
    ExternalSearchSts_LeftFnd_RearFnd = auto()
    ExternalSearchSts_RightFnd_RearFnd = auto()


class MASTER_DownloadProcess_EVENT(BaseEnum):
    # FOTA Master服务DownloadProcess event的字段
    taskId = 0
    state = 1
    progress = 2
    downloadSpeed = 3
    leftTime = 4
    errorCode = 5
    
class VSP_Status(BaseEnum):
    # VSP 平台FOTA Status
    Pushing = 14
    Push_Success = 15
    Push_Failed = 16
    Downloading = 4
    Download_Success = 5
    Upgrading = 8
    Upgrade_Failed = 10
    FOTA_Cancelled = 20
    FOTA_Success = 18
    FOTA_Failed = 19


class YesOrNo(BaseEnum):
    No = 0
    Yes = 1

class ValueQf(BaseEnum):
    UndefindDataAccur = 0
    TmpUndefdData = 1
    DataAccurNotWithinSpcn = 2
    AccurData = 3

class ReqSts(BaseEnum):
    NotReqd = 0
    Reqd = 1


class EmgyBrkLiReq(BaseEnum):
    NotInProgs = 0
    InProgs = 1
    InProgsAtSpdLo = 2

class BrkPedlSnsrSt(BaseEnum):
    NoInfo1 = 0
    NotPsd = 1
    Psd = 2
    NoInfo2 = 3
    
class MASTER_UpdateProcess_EVENT(BaseEnum):
    # FOTA Master服务UpdateProcess event的字段
    taskId = 0
    state = 1
    progress = 2
    leftTime = 3
    errorCode = 4
    
class Master_UpdateStatusEnum(BaseEnum):
    # FOTA Master服务UpdateStatusEnum值
    UPDATE_RUNNING = 0
    UPDATE_COMPLETE = 1
    UPDATE_FAILED = 2
    UPDATE_FAILED_NOT_DRIVING = 3
    PRE_UPDATE = 4
    
class Master_DownloadStatusEnum(BaseEnum):
    # FOTA Master服务DownloadStatusEnum值
    DOWNLOAD_RUNNING = 0
    DOWNLOAD_COMPLETE = 1
    DOWNLOAD_FAILED = 2


class DoorRelsReq(BaseEnum):
    Invld = 0
    On = 1
    Off = 2
    Invld2 = 3


class GeneralSts(BaseEnum):
    Enable = 0
    Disable = 1
    OutRangeValue = 2


class BleVehicleBody(BaseEnum):
    TailGate = 0
    Bonnet = 1
    CentralLock = 2
    TailWing = 3
    Tire = 4
    Doors = 5
    Wins = 6
    OuterRearView = 7

class BleEicCharg(BaseEnum):
    Charging = 0
    BatteryInfo = 1

class BleCharging(BaseEnum):
    LidSts = 0
    PluggerSts = 1
    ChargSpeed= 2
    RemainChargTime = 3
    ChargeTargetSoc = 4
    ChargPower = 5
    ChargEgyThisTime = 6
    IncMilThisTime = 7
    RecentChargeStartTime = 8
    RecentChargEndTime = 9
    MaxCurrent = 10
    ActualCurrent = 11
    Type = 12
    ChargTargetMil = 13

class BleBatteryInfo(BaseEnum):
    Current = 0
    CalSoc = 1
    CurrSoc= 2
class CheckType(BaseEnum):
    IN_TIME = 1 
    IN_ALL = 2 
    IS_COMPLETE = 3 

class V2T_API(BaseEnum):
    OTA = 'ota' 
    FOD = 'V2TCcpForwarder' 
    RemoteRescue = 'rescue'

class V2T_Interaction_Type(BaseEnum):
    Type_10 = 1 # vehicle => tsp, Task detection interface
    Type_20 = 2 # tsp => vehicle, Task detection response interface 
    Type_30 = 3 # vehicle => tsp, Vehicle receives the task response interface
    Type_40 = 4 # vehicle => tsp, Task detection interface
    Type_50 = 5 # tsp => vehicle, Delivering task information interface 
    Type_60 = 6 # vehicle => tsp, Status reporting interface
    Type_70 = 7 # tsp => vehicle, Cancel task interface
    Type_80 = 8 # tsp => vehicle, APP trigger update interface


class BMSWakeUpSetType(BaseEnum):
    ChrgnCurrThd = 0
    ChrgnCurrEna = 1
    DisChrgnCurrThd = 2
    DisChrgnCurrEna = 3
    SocEna = 4
    SocThd = 5
    VolThd = 6
    VolEna = 7
    TiChrgnAtSleepThd = 8


class WTI_Func(BaseEnum):
    HighVolBattLow	 = 0
    SteeringSysWarning	 = 1
    SuspensionFailed	 = 2
    LowBattWarning1	 = 3
    LowBattWarning2	 = 4
    LightLevelingMotor	 = 5
    LBFailure	 = 6
    HBFailure	 = 7
    OvertakeLightFailure	 = 8
    ReverseLightFailure	 = 9
    POFailure	 = 10
    RearFogFailure	 = 11
    LeftTIFailure	 = 12
    RightTIFailure	 = 13
    DriverSeatBeltWarning	 = 14
    PassengerSeatBeltWarning	 = 15
    SecRowLeftSeatBeltWarning	 = 16
    SecRowMidSeatBeltWarning	 = 17
    SecRowRightSeatBeltWarning	 = 18
    AirbagFailure	 = 19
    TireFLPressureLow	 = 20
    TireFRPressureLow	 = 21
    TireRLPressureLow	 = 22
    TireRRPressureLow	 = 23
    TireFLPressureHigh	 = 24
    TireFRPressureHigh	 = 25
    TireRLPressureHigh	 = 26
    TireRRPressureHigh	 = 27
    TireFLTempHigh	 = 28
    TireFRTempHigh	 = 29
    TireRLTempHigh	 = 30
    TireRRTempHigh	 = 31
    TireFLPressureFastLost	 = 32
    TireFRPressureFastLost	 = 33
    TireRLPressureFastLost	 = 34
    TireRRPressureFastLost	 = 35
    TireFLSensorBattLow	 = 36
    TireFRSensorBattLow	 = 37
    TireRLSensorBattLow	 = 38
    TireRRSensorBattLow	 = 39
    TirePressureSysFailureFL	 = 40
    TirePressureSysFailureFR	 = 41
    TirePressureSysFailureRL	 = 42
    TirePressureSysFailureRR	 = 43
    ChargingGunTemp	 = 44
    ThermalOutOfControl	 = 45
    PowerSysFailure	 = 46
    HighVolInterLock_0	 = 47
    HighVolInterLock_1	 = 179
    HighVolInterLock_2	 = 180
    HighVolInterLock_3	 = 181
    HighVolIsolation	 = 48
    ChargeLidOpenSts	 = 49
    ChargeLidInfo	 = 50
    ChargeLidFault	 = 51
    EnergyRegenLimit_1	 = 52
    EnergyRegenLimit_2	 = 182
    ShiftGear	 = 53
    GearFailure	 = 54
    BrakingFluid	 = 55
    EPBWarning1	 = 56
    EPBWarning2	 = 57
    EPBWarningChime	 = 58
    EPBFailure	 = 59
    EBDWaring	 = 60
    AutoholdWarning	 = 61
    NoKey	 = 62
    Starting	 = 63
    NotParked	 = 64
    AntiTheft	 = 65
    Coolant	 = 66
    DoorHood	 = 67
    DoorDrv	 = 68
    DoorPass	 = 69
    DoorRearLeft	 = 70
    DoorRearRight	 = 71
    DoorTail	 = 72
    PedestrianProtectFailure	 = 73
    PedestrianProtectEnabled	 = 74
    WiperWashingLiquid	 = 75
    WiperSysFailure	 = 76
    WiperExitRepairPosition	 = 77
    WiperSensorFailure	 = 78
    DrvWindowFailure	 = 79
    PassWindowFailure	 = 80
    RearLeWindowFailure	 = 81
    RearRiWindowFailure	 = 82
    DModelShowsTailPosition	 = 83
    CarTailWarning	 = 84
    WirelessChargingRemind	 = 85
    SteerWheelHeatWarning	 = 86
    DriverSeatHeatWarning	 = 87
    PassengerSeatHeatWarning	 = 88
    DriverSeatWindWarning	 = 89
    PassengerSeatWindWarning	 = 90
    DriverElectricDoorWarning	 = 91
    PassengerElectricDoorWarning	 = 92
    SecLeftElectricDoorWarning	 = 93
    SecRightElectricDoorWarning	 = 94
    NoPowerOutput	 = 95
    HighBeamOperationFailReminder	 = 96
    TailGateUnlockWarning	 = 97
    UnlockReminder	 = 98
    LockFailedReminder	 = 99
    CannotUnLockReminder	 = 100
    CloseDoorReminder	 = 101
    NoKeyPresent	 = 102
    KeyDisconnectedReminder	 = 103
    PEBLEKeyLegacyReminder	 = 104
    PEUWBKeyLegacyOnDriverReminder	 = 105
    PEUWBKeyLegacyOnPassReminder	 = 106
    PEUWBKeyLegacyOnReLeReminder	 = 107
    PEUWBKeyLegacyOnReRiReminder	 = 108
    PEUWBKeyLegacyOnTrunkReminder	 = 109
    NFCBLEKeyLegacyReminder	 = 110
    NFCUWBKeyLegacyOnDriverReminder	 = 111
    NFCUWBKeyLegacyOnPassReminder	 = 112
    NFCUWBKeyLegacyOnReLeReminder	 = 113
    NFCUWBKeyLegacyOnReRiReminder	 = 114
    NFCUWBKeyLegacyOnTrunkReminder	 = 115
    ETCFaultReminder	 = 116
    ETCRemoveReminder	 = 117
    TireFLPressureLowLevel2	 = 118
    TireFRPressureLowLevel2	 = 119
    TireRLPressureLowLevel2	 = 120
    TireRRPressureLowLevel2	 = 121
    TouchShiftActivated	 = 122
    WPCWarn	 = 123
    BNCMWarn	 = 124
    NKRWarn	 = 125
    BKAWarn	 = 126
    EntityKeyBattLow	 = 127
    DriverRadarWarning	 = 128
    PassengerRadarWarning	 = 129
    LeftRearRadarWarning	 = 130
    RightRearRadarWarning	 = 131
    ChargingFailedWarning	 = 132
    DrvWindowMotorOverheating	 = 133
    PassWindowMotorOverheating	 = 134
    ReleWindowMotorOverheating	 = 135
    ReRiWindowMotorOverheating	 = 136
    DrvrMirrorFoldError	 = 137
    PassMirrorFoldError	 = 138
    DrvrMirrorAdjError	 = 139
    PassMirrorAdjError	 = 140
    FrontVentAdjError	 = 141
    RearVentAdjError	 = 142
    CirculationMotorError	 = 143
    FrontModeMotorError	 = 144
    PM25SystemError	 = 145
    AQSSystemError	 = 146
    ClimateSystemError	 = 147
    FragSystemError	 = 148
    RemoteAuthStart	 = 149
    LowBattWarning3	 = 150
    EPedalFunIndcn	 = 151
    IPMBattFaultWarn	 = 152
    CoolantDriveSys	 = 153
    CoolantHighVolBatt	 = 154
    ETCAuthenticationFailed	 = 155
    DoorIceBreakReminder	 = 156
    PEKeyLegacyReminder	 = 157
    NFCKeyLegacyReminder	 = 158
    PleaseManualCloseDueToCloseDoorFail	 = 159
    OpenCloseDoorReminderDueToLargeSlope	 = 160
    DoorAntiPlayAndThermalProtectionReminder	 = 161
    AirGrilleAbnormal	 = 162
    WiperSwitchUsePrompt	 = 163
    RearFogAndLowBeamOff	 = 164
    LaunchModePrompt_1	 = 165
    LaunchModePrompt_2	 = 182
    ReLeSeatHeatWarning	 = 166
    ReRiSeatHeatWarning	 = 167
    ReLeSeatVentWarning	 = 168
    ReRiSeatVentWarning	 = 169
    VehicleBaselineInconsistent	 = 170
    HVBatteryThermalSts	 = 171
    DrvWirelessChargingRemind	 = 172
    PassWirelessChargingRemind	 = 173
    PressBrakeAndAccPedalDeeplyToActiveLaunchMode	 = 174
    TiChrgnAtSleepThd = 8
    PowerSysFailed = 175
    HighVoltBattFailed_1 = 176
    HighVoltBattFailed_2 = 177
    BatteryTempLow = 178
    EPBWork_1 = 183
    EPBWork_2 = 184
    BrakingSysFailedYellow = 185
    BrakingSysFailedRed_1 = 186
    BrakingSysFailedRed_2 = 187
    HDCGrey = 188
    ABSFailed = 189
    ESCFailed = 190
    ESCOff_1 = 191
    ESCOff_2 = 192
    SteeringSysFailedYellow = 193
    SuspensionFailed_1 = 194
    SuspensionFailed_2 = 195
    AutoholdActiveGreen = 196
    AutoholStandbyGrey = 197
    ChargingGunConnectSts = 198
    
class DTCFault(BaseEnum):
    AWMSensorFail_A = "A02D7C"
    AWMSensorFail_B = "A02D7D"
    HeartBeatFail = "F00000"
    CommunicationFail_CEM_and_RSLM = "D34587"
    NoSignalFromWMM= "D35387"
    ActvReSplrHallSnsrFltHallOutpFlt="A07D11"
    ActvReSplrUFltLoVoltDetdFlt ="A02D16"
    ActvReSplrUFltHiVoltDetdFlt = "A02D17"
    CalStsAWM = "A02E51"
    ActvReSplrIntFltActrFlt3 = "A07E13"
    ActvReSplrIntFltActrFlt5 = "A02E4C"
    ActvReSplrIntFltActrFlt2 = "A02E11"
    ActvReSplrIntFltActrFlt1 = "A02E12"
    ActvReSplrIntFltActrFlt4 = "A02E19"
    Pauselin6 = "D31687"
    RainSensorFault = "D34549"
    RainSensorCalibrationFault = "D34546"
    BMSCommunicationFault = "A1DB87"
    BMSHardwareFault = "A1DB96"
    IPMBattSocSts = "D12487"
    RSLMCommunicationFault = "D34587"
    Rainerror = "D34549"
    Raincalibrationerror = "D34546"
    WiperError = "AD3896"
    WiperVoltage = "AD3816"
    WiperOverVoltage = "AD3817"
    WiperOverload = "AD3819"
    RelHumSnsrErr = "970149"
    NoresponseBMS = "D31787"
    WMMresponseLIN = "D30183"
    SolarSnsrErr = "90BE96"
    Switch_Right = "D35182"
    Switch_Left = "D13082"
    ALM1Fault_LED = "A04010"
    ALM1Fault_Vlt = "A0401C"
    ALM1Fault_Tmp = "A0404B"
    ALM2Fault_LED = "A04110"
    ALM2Fault_Vlt = "A0411C"
    ALM2Fault_Tmp = "A0414B"
    ALM3Fault_LED = "A04210"
    ALM3Fault_Vlt = "A0421C"
    ALM3Fault_Tmp = "A0424B"
    ALM4Fault_LED = "A04310"
    ALM4Fault_Vlt = "A0431C"
    ALM4Fault_Tmp = "A0434B"
    ALM5Fault_LED = "A04410"
    ALM5Fault_Vlt = "A0441C"
    ALM5Fault_Tmp = "A0444B"
    ALM6Fault_LED = "A04510"
    ALM6Fault_Vlt = "A0451C"
    ALM6Fault_Tmp = "A0454B"
    ALM7Fault_LED = "A04610"
    ALM7Fault_Vlt = "A0461C"
    ALM7Fault_Tmp = "A0464B"
    ALM8Fault_LED = "A04710"
    ALM8Fault_Vlt = "A0471C"
    ALM8Fault_Tmp = "A0474B"
    ALM9Fault_LED = "A06610"
    ALM9Fault_Vlt = "A0661C"
    ALM9Fault_Tmp = "A0664B"
    ALM10Fault_LED = "A06710"
    ALM10Fault_Vlt = "A0671C"
    ALM10Fault_Tmp = "A0674B"
    OHCLossLin = "D30787"
    DSGLVolHigh = "A03417"
    DSGLVolLow = "A03416"
    DSGLTempHigh = "A0344B"
    DSGLLedFail = "A03414"
    PSGLVolHigh = "A03517"
    PSGLVolLow = "A03516"
    PSGLTempHigh = "A0354B"
    PSGLLedFail = "A03514"
    OHCRLiBtnReadingLe = "A07271"
    OHCRLiBtnReadingRi = "A07371"
    OHCLiBtnReadingLe = "A07071"
    OHCLiBtnReadingRi = "A07171"
    ALM1missLin = "D30E87"
    ALM2missLin = "D30F87"
    ALM3missLin = "D31087"
    ALM4missLin = "D31187"
    ALM5missLin = "D31287"
    ALM6missLin = "D31387"
    ALM7missLin = "D31487"
    ALM8missLin = "D31587"
    ALM9missLin = "D31887"
    ALM10missLin = "D31987"

    
class DTCSts(BaseEnum):
    CurrentFailed = 0b00000001
    FailedThisOperCycle = 0b00000010
    Pending = 0b00000100
    Confirm = 0b00001000
    NotCompletedSinceLastClear = 0b00010000
    FailedSinceLastClear = 0b00100000
    NotCompletedThisOperCycle = 0b01000000
    WarningIndicatorReq = 0b10000000
    WithHistoryWithoutCurrent = 0b00001000
    FullWithCurrentFailed = 0b00100111
    FullWithHistory = 0b00100110
    Trc_dissatisfaction = 0b01010000

class BattSnsrType(BaseEnum):
    NAWC=3
    AWC=0
    Reserved01=1
    Reserved02=2

class BMSWakeUpTrgSrc(BaseEnum):
    NotReqd=0
    LoSOC=1
    LoVoltage=2
    ChrgnCurrent=3
    DisChrgnCurrent=4
    Reserved1=5
    Reserved2=6
    Reserved3=7

class SocSts(BaseEnum):
    Larger15Per=0
    LessOrEqual15Per=1
    LessOrEqual10Per=2
    Invalid=3


class GeneralFltSts(BaseEnum):
    NotVld1 = 0
    Off = 1
    On = 2
    NotVld2 = 3

class WiperFaultType(BaseEnum):
    Ok = 0
    WashWaterLow = 1
    RainSensorError = 2
    LightRawSensorError = 3
    SystemError = 4
    SwitchError = 5
    NA = 6

class UpType(BaseEnum):
    Gear = 0
    GeatAuto = 1
    GearCdc = 2
    SetUsageModeUp = 3
    SetUsageModeWithoutKey = 4
    
class ParkLockSts(BaseEnum):
    ParkNotEngd = 0
    ParkEngd = 1
    NotInUse = 2
    Undefd = 3
    
class FirstCheck_ErrorCode(BaseEnum):
    FirstCheck_HVSOCLow_0x04_0x20 = "0420"
    FirstCheck_NotInPark_0x04_0x21 = "0421"
    FirstCheck_VehicleSpeed_0x04_0x22 = "0422"
    UserChoosePause_0x04_0x23 = "0423"
    FirstCheck_NoJIDUCharger_0x04_0x25 = "0425"

class WinShortDropReq(BaseEnum):
    Idle = 0
    Close = 1
    Open = 2

class UA_Skip_Debug():
    Need_Skip_Download = 'need_skip_download'
    Allow_Same_Version_Flash = 'allow_same_version_flash'

class Motorola(BaseEnum):
    idle = 0
    Warning = 1
    NoWarning = 2
    Reserved = 3
class KeepPowerFlag(BaseEnum):
    open = 0
    close_service = 1
    close_hvsoc = 2
    close_gear = 3
    close_carmode = 4
    close_fota = 5
    close_other = 6
    
class RelaySts(BaseEnum):
    Off = 0
    On = 1
    Open = 2


class RainCloseWinReq(BaseEnum):
    NoRequest = 0
    Open = 1
    CloseWinAndSunroof = 2
    Close = 3
    Stop = 4


class HighBeamCmd(BaseEnum):
    Off = 0
    Flash = 1
    On = 2
    Release = 255


class ChdLockSts(BaseEnum):
    Invld1 = 0
    On = 1
    Off = 2
    Invld2 = 3
    
class DrvrDesDir(BaseEnum):
    Undefd = 0
    Fwd = 1
    Rvs = 2
    Neut = 3
    Resd0 = 4
    Resd1 = 5
    Resd2 = 6
    Resd3 = 7

class SteerWhlTouchSwtPos(BaseEnum):
    Left1 = 0
    Left2 = 1
    Left3 = 2
    Right1 = 3
    Right2 = 4
    Right3 = 5
    All = 6


class SteerWhlTouchSwtSts(BaseEnum):
    NotAvailble = 0
    ShortPress = 1
    LongPress = 2
    Error = 3

class ClimateMode(BaseEnum):
    kOFF=0
    kManual=1
    kAuto=2
    kPM25 = 3
    kCockpitClean = 4
    kDefrost=5


class ULoWarnULoWarn(BaseEnum):
     Uon = 0
     ULoTmp = 1
     ULoPrmnt = 2
    

class CllsnThreat1(BaseEnum):
    ukwn = 0
    threatlo = 1
    threatmed = 2
    threathi = 3
    
class UA_DownloadStatus(BaseEnum):
    DOWNLOAD_RUNNING = 0
    DOWNLOAD_COMPLETE = 1
    DOWNLOAD_FIRST_FAILED = 2
    DOWNLOAD_FINAL_FAILED = 3
    DOWNLOAD_DEFAULT = 255
    
class UA_PreUpdatedStatus(BaseEnum):
    WAIT_PREUPDATE_CMD = 0
    PREUPDATE_RUNNING = 1
    PREUPDATE_COMPLETE = 2
    PREUPDATE_FAILED = 3
    PREUPDATE_DEFAULT = 255
    
class UA_UpdatedStatus(BaseEnum):
    UPDATE_RUNNING = 0
    UPDATE_FIRST_FAILED = 1
    UPDATE_FAILED_TWICE = 2
    UPDATE_COMPLETE = 3
    ROLLBACK_RUNNING = 4
    ROLLBACK_FAILED = 5
    ROLLBACK_COMPLETE = 6
    UPDATE_REBOOT_ACTIVE_FAILED = 7
    UPDATE_REBOOT_ACTIVE_SUCCESS = 8
    ROLLBACK_REBOOT_ACTIVE_FAILED = 9
    ROLLBACK_REBOOT_ACTIVE_SUCCESS = 10
    UPDATE_DEFAULT = 255
class Wakeup_Reasons(BaseEnum):    
    NO_WAKEUP = 0
    WAKEUP_BY_POWERON=1
    WAKEUP_BY_RTC=2
    WAKEUP_BY_BODYCAN =3
    WAKEUP_BY_BODYEXPCANCANFD =4
    WAKEUP_BY_CONNCANFD=5
    WAKEUP_BY_PASSIVESAFETYCAN=6
    WAKEUP_BY_PROPULSIONCAN=7
    WAKEUP_BY_CLASSICCAN1=8
    WAKEUP_BY_CLASSICCAN2=9
    WAKEUP_BY_INFOCAN=10
    WAKEUP_BY_DIAGCAN=11
    WAKEUP_BY_ADCAN=12
    WAKEUP_BY_ALM1=13
    WAKEUP_BY_ALM2=14
    WAKEUP_BY_FLEXRAY=15
    WAKEUP_BY_LIN1=16
    WAKEUP_BY_LIN2=17
    WAKEUP_BY_LIN3=18
    WAKEUP_BY_LIN4=19
    WAKEUP_BY_LIN5=20
    WAKEUP_BY_LIN6=21
    WAKEUP_BY_ACTIVATION_LINE=22
    WAKEUP_BY_HOOD1=23
    WAKEUP_BY_HOOD2=24
    WAKEUP_BY_FLDOOR_SW=25
    WAKEUP_BY_FRDOOR_SW=26
    WAKEUP_BY_RLDOOR_SW=27
    WAKEUP_BY_RRDOOR_SW=28
    WAKEUP_BY_FLDOOR_LOCK_SW=29
    WAKEUP_BY_FRDOOR_LOCK_SW=30
    WAKEUP_BY_RLDOOR_LOCK_SW=31
    WAKEUP_BY_RRDOOR_LOCK_SW=32
    WAKEUP_BY_TAILGATE_LOCK_SW=33
    WAKEUP_BY_BRAKE=34
    WAKEUP_BY_IG1=35
    WAKEUP_BY_KL15_2=36
    WAKEUP_BY_TRUNK=37
    WAKEUP_BY_CHARGELID=38
    WAKEUP_BY_HAZARD=39
    WAKEUP_BY_HORN=40
    
class VehicleModelCcp(BaseEnum):
    Mars1 = {950:0x01}
    Venus = {950:0x02}

class StrtMsgToModMngt(BaseEnum):
    NoInhb = 0
    PwrUpDly = 1
    AltvStrt = 2
    inhbremstrt = 3
    diremstrt = 4
    SelnOfParkOrNeut = 5
    Resd1 = 6
    Resd2 = 7

class StrtMsgToDrvrg(BaseEnum):
    NoMsg = 0
    Msg1 = 1
    Msg2 = 2
    Msg3 = 3
    Msg4 = 4
    Msg5 = 5
    Msg6 = 6
    Msg7 = 7
    Msg8 = 8
    Msg9 = 9
    Msg10 = 10
    Msg11 = 11

class StrtInProgs(BaseEnum):
    StrtStsOff = 0
    StrtStsImminent = 1
    StrtStsStrtng = 2
    StrtStsRunng = 3

class TrsmParkLockd(BaseEnum):
    ParkNotEngd = 0
    ParkEngd = 1
    NotInUse = 2
    Undefd = 3

class VehNotParkInfoWarn(BaseEnum):
    NoTxt = 0
    ShifttoP = 1
    OutofP = 2

class Locksts(BaseEnum):
    Ukwn = 0
    Unlckd = 1
    Lockd = 2
    SafeLockd = 3

class Unlockfailtohmi(BaseEnum):
    SafeInvld1 = 0
    SafeOn = 1
    SafeOff = 2
    SafeInvld2 = 2

class crashsts(BaseEnum):
    NoCrash = 0
    Crash = 1
    
class RainSensorFaultType(BaseEnum):
    SensorFault = 0
    CalibrationFault = 1
    All = 2


class WpcModule(BaseEnum):
    OverTemperatureProtected = 0
    Standby = 1 
    Charging = 2 
    FOD = 3
    VoltageProtected = 4
    OverPowerProtected = 5
    Transmittingcoildisable = 6
    OFF = 7
    ChargingCompleted = 8
    DeactivatedbyUser = 9
    InternalFailure = 10
    NFCFailure = 11
    Resvd4 = 12
    Resvd5 = 13
    Resvd6 = 14
    Invalid = 15


class WipgAutFrntMod(BaseEnum):
    Off = 0
    ImdtMod = 1 
    IntlMod = 2 
    ContnsMod = 3

class RainLeve(BaseEnum):
    Level0 = 0
    Level1 = 1
    Level2 = 2
    Level3 = 3
    Level4 = 4 
    Level5 = 5
    Level6 = 6
    Level7 = 7 
    Level8 = 8
    Level9 = 9
    Level10 = 10 
    Level11 = 11
    Level12 = 12
    Level13 = 13
    Level14 = 14
    Level15 = 15
 
class CmdType(BaseEnum):
    # 远程诊断指令类型
    SessionOpen = "session_open"
    SessionClose = "session_close"
    SendDiagCmd_3E = "SendDiagCmd_3E"
    SendDiagCmd_19 = "SendDiagCmd_19"
    SendDiagCmd_14 = "SendDiagCmd_14"
    SendDiagCmd_10_11 = "SendDiagCmd_10&11"
    SendDiagCmd_22_P0_DID = "SendDiagCmd_22_P0_DID"
    SendDiagCmd_22_P1_DID = "SendDiagCmd_22_P1_DID"
    SendDiagCmd_22_P2_DID = "SendDiagCmd_22_P2_DID"
    SendDiagCmd_cali = "SendDiagCmd_cali"

class CheckRemoteDiagRes(BaseEnum):
    #用于区分不同远程诊断指令执行结果的检测
    CheckRemoteDiagRes_3E = "CheckRemoteDiagRes_3E"
    CheckRemoteDiagRes_19 = "CheckRemoteDiagRes_19"
    CheckRemoteDiagRes_14 = "CheckRemoteDiagRes_14"
    CheckRemoteDiagRes_10_11 = "CheckRemoteDiagRes_10&11"
    CheckRemoteDiagRes_22_P0_DID = "CheckRemoteDiagRes_22_P0_DID"
    CheckRemoteDiagRes_22_P1_DID = "CheckRemoteDiagRes_22_P1_DID"
    CheckRemoteDiagRes_22_P2_DID = "CheckRemoteDiagRes_22_P2_DID"

class RescueType(BaseEnum):
    # 远程救援指令类型，1. 200:维持不可开车 2. 210:取消维持不可开车 3. 220:四域重启
    OpenInhibit = 200
    CloseInhibit = 210
    ResetDomain = 220

class WiperAutoMode(BaseEnum):
    NA = 0
    Off = 1
    Single = 2
    Interval = 3
    Continuous = 4

class CarModDisp1(BaseEnum):
    CarModDisp1_NoDisp = 0
    CarModDisp1_Facy = 1
    CarModDisp1_FacyStop = 2
    CarModDisp1_Trnsp = 3
    CarModDisp1_TrnspStop = 4
    CarModDisp1_Dyno = 5
    CarModDisp1_Norm = 6
    CarModDisp1_Crash = 7

class Keyprsntsts(BaseEnum):
    KeyPrsntStsIdle = 0
    KeyPrsntStsInProgs = 1
    KeyPrsntStsNotPrsnt = 2
    KeyPrsntStsPrsnt = 3
    
class LockWarn(BaseEnum):
    Idle = 0
    LockFailByNFC = 1
    LockFailByKeyForget = 2
    NoKey = 3
    DoorClose = 4
    ReLockFail = 5
    keLockOk = 6
    NotSetAopproachLockHmi = 7
    CloseFailByApproach = 8
    CloseFailByNfcPe = 9
    LockWithNfcButKeyForget = 10
    UnlockFailWithHighSpeed = 11
    CloseDoorFail = 12

class DoorRemind(BaseEnum):
    NoRequest = 0
    CloseDoorInside = 1
    CloseDoorOutside = 2

class UsagemodeSize(BaseEnum):
    Abandon_0h = 3
    Abandon_10h = 5
    Abandon_20h = 7
    Abandon_80h = 9
    Abandon_500h = 11
    Inactive_1min = 13
    Inactive_10h = 15
    Inactive_20h = 17
    Inactive_80h = 19
    Convenience_10s = 21
    Convenience_10min = 23
    Convenience_20min = 25
    Convenience_40min = 27
    Active_10s = 29
    Active_10min = 31
    Active_20min = 33
    Active_40min = 35
    Driving_0min =37
    Driving_10min =39
    Driving_30min =41
    Driving_90min =43

class UsagemodeValue(BaseEnum):
    Abandon = 3
    Inactive = 6
    Convenience = 12
    Active = 18
    Driving = 24
    
class BLEKeyPrsntZone(BaseEnum):
    Zone0=0
    Zone1=1
    Zone2=2
    Zone3=3
    Zone4=4
    Zone5=5
    Zone6=6
    Zone7=7
    Zone8=8
    Zone9=9
    Zone10=10
    Zone11=11
    Zone12=12
    Zone13=13
    Zone14=14
    Zone15=15

class BLEKeyPrsntSts(BaseEnum):
    NotValid = 0
    Valid = 1


class RemHvStrtActvReq(BaseEnum):
    NoReq = 0
    On = 1
    Off = 2

class Ccp_Skip_Debug():
    skip_check_seat = "skip_check_seat"
    skip_gear_p = "skip_gear_p"
    skip_acu = "skip_acu"
    skip_cdc = "skip_cdc"
    skip_arb_token = __import__("os").environ.get('XAT_CREDENTIAL_____CONSTANTS_COMMON_PY_SKIP_ARB_TOKEN', "")
    skip_usage_mode_down = "skip_usage_mode_down"
    skip_usage_mode_up = "kip_usage_mode_up"
    skip_pre_check_usage_mode = "skip_pre_check_usage_mode"
    skip_net_work = "skip_net_work"
    debug_ccp_report_time = "ebug_ccp_report_time"
    skip_verify = "skip_verify"


class DigitalKeyType(BaseEnum):
    """钥匙类型"""
    NoKeyConnected = 0
    NFC_Card = 1
    BLE_Key = 2
    BLE_UWB_KeyFob = 3
    Temp_BLE_Key = 4
    ICCE_BLE_Key = 5
    ICCE_NFC_Key = 6
    CCC_NFC_BLE_UWB_Key = 7
    CCC_NFC_Key = 8
    CCC_NFC_BLE_Key = 9


class DigitalKeyIdTrigger(BaseEnum):
    Invalid = 0
    ApproachLight = 1
    ApproachSecon = 2
    Unlock = 3
class MoveSts(BaseEnum):
    Opened = 0
    Closing = 1
    Closed = 2
    Opening = 3
    Hover = 4
    NA = 5
    ClosingBreak = 6
    OpeningBreak = 7
    HalfClosed = 8
    Invalid = 65535
    
class CCPMasteSts(BaseEnum):
    # CCP Master状态机状态
    IDLE = 0
    PRE_ACTIVE = 1
    ACTIVING = 2
    FAIL = 3
    FAIL_IMPACT_DRIVING = 4
    SUCCESS = 5
    
class CCPMasterSts_Field(BaseEnum):
    # CCP Master StatusStruct 中的字段
    TaskInfo = 0
    State = 1
    ErrorCode = 2
    
class CCPMasterConditionCheckResult_Field(BaseEnum):
    # CCP Master ConditionCheckResult 中的字段
    TaskInfo = 0
    ConditionCheckVecs = 1
    
class TaskInfo_Field(BaseEnum):
    # CCP Master TaskInfo 中的字段
    TaskId = 0
    ModifyBy = 1
    ModifyExt = 2
    
class CheckResultEnum(BaseEnum):
    # CCP Master 条件检查的结果
    CR_SUCCESSFUL = 0
    CR_SPEED_ERROR = 1
    CR_NOT_GEAR_P = 2
    CR_AVP_DISABLE = 3
    CR_APA_DISABLE = 4
    CR_NOT_TOKEN = 5
    CR_CHECKING = 32
    
class VehicleType(BaseEnum):
    # （CCP#951==0x01代表 Mars  CCP#951==0x02代表 Venus)
    Mars = 0x01
    Venus = 0x02

class VehicleMca(BaseEnum):
    # (CCP#962==0x00代表MCA 400v CCP#962==0x02代表MCA 800v)
    Mca_400v = 0x00
    Mca_800v = 0x02


class DoorLockCmd(BaseEnum):
    Off = 0
    Unlck = 1
    Lock = 2
    Safe = 3
    UnlckByCrash0 = 12
    UnlckByCrash1 = 4
    UnlckByCrash2 = 8
    UnlckByCrash3 = 14
    UnlckByCrash4 = 13

class DoorTrigerSource(BaseEnum):
    NoTrigSrc = 0
    KeyRem = 1
    HMI = 2
    Telm = 3
    OutdSwt = 4
    InsdSwt = 5

class TailgateTrigerSource(BaseEnum):
    TrNoTrigSrc = 0
    TrKeyRem = 1
    TrSwtIntr = 2
    TrByFootOper = 3
    TrHndlOutd = 4
    TrShutFace = 5
    TrHMI = 6
    TrByAppch = 7

class DoorMoveSts(BaseEnum):
    Ukwn = 0
    FullClsd = 1
    MovgOut = 2
    MovgOutBrkg = 3
    StopDurgOpen = 4
    FullOpend = 5
    MovgIn = 6
    MovgInBrkg = 7
    StopDurgCls = 8
    HalfClsd = 9
    StopMinPntForCls = 10

class DoorMoveStatus(BaseEnum):
    Opened = 0
    Closing = 1
    Closed = 2
    Locked = 3
    Unlocked = 4
    Opening = 5
    Hover = 6
    NA = 7
    ClosingBreak = 8
    OpeningBreak = 9
    HalfClosed = 10
    kInvalid = 65535

class TriggerType(BaseEnum):
    enable  = 0
    disable = 1

class UnlockSts(BaseEnum):
    kDefault = 0  #   /** 默认 */
    kFail = 1  # /** 成功 */
    kSuccess = 2  #  /** 失败 */
    
class HeatWorkSts(BaseEnum):
    HeatOff = 0
    HeatOn = 1
    Invalid = 255

class HeatSts(BaseEnum):
    Off = 0
    On = 1
    Limited = 2
    NotAvailable = 3
    TimeoutOff = 4
    AutoHeatOn = 5
    Invalid = 255

class ViewFoldStatus(BaseEnum):
    StatusNa = 0
    StatusUnfolded = 1
    StatusFolded = 2
    StatusUnfolding = 3
    StatusFolding = 4

class SideDoor(BaseEnum):
    FrntLeftDoorSts  = 0
    FrntRightDoorSts = 1
    RearLeftDoorSts = 2
    RearRightDoorSts = 3
    All = 4

class LockReminder(BaseEnum):
    Idle  = 0
    NFCLockFail = 1
    PELockFailByKeyForget = 2
    NoKeyPresent = 3
    DoorCloseAudio = 4
    ReLockFail = 5
    ReLockOk = 6
    WalkAwayAudio = 7

class PowerOutLetReq(BaseEnum):
    NoReq = 0
    On = 1
    Off  = 2   

class RelayType(BaseEnum):
    KL151 = 0
    KL152 = 1
    KL153  = 2   
    climate  = 3   
    batterysaver  = 4  
    poweroutlet  = 5   
    crashrelay  = 6   
    poweroutproxy  = 6 

class LockStsPrmt(BaseEnum):
    Idle  = 0
    NFC_PSD = 1
    ANTI_LOCK_KEY_FORGET = 2
    NO_KEY_PRESENT = 3
    CLOSE_DOOR_AUDIO = 4
    ANTI_RELOCK = 5
    AUTO_RELOCK = 6
    WalkAwayAudio = 7

class UsgModDeactvnQly(BaseEnum):
    InvalidValue = 0
    QlyNotOkLowConfidence = 1
    QlyOkHighConfidence = 2
    InvalidValue2 = 3
    
class OutdBriSts(BaseEnum):
    Ukwn = 0
    Night = 1
    Day = 2
    Invld = 3    

class BtnStsSngTyp(BaseEnum):
    Idle = 0
    BtnPsd = 1

class TwliBriRaw(BaseEnum):
    Night = 0
    Day = 1
    
class foldStatusValidity(BaseEnum):
    Valid = 0
    SignalMissing = 4

class AsySftyHWLReq(BaseEnum):
    NoRequest = 0
    TurnOn = 1
    TurnOff = 2
    Reserved = 3 
    
class AutWinWipgCmd(BaseEnum):
    WipgSpd0Rpm = 0
    WipgSpd40Rpm = 1 
    WipgSpd43Rpm = 2 
    WipgSpd46Rpm = 3 
    WipgSpd50Rpm = 4  
    WipgSpd54Rpm= 5  
    WipgSpd57Rpm = 6 
    WipgSpd60Rpm = 7 
    
class RainSnsrStsToHMI(BaseEnum):
    Off = 0
    On = 1 

class WiprActvFromWMM(BaseEnum):
    on = 1
    Off = 0 
    
class WiprActv(BaseEnum):
    on = 1
    Off = 0  
    
class WiprMotErrSafe(BaseEnum):
    NotVld1 = 0
    Off = 1 
    On = 2 
    NotVld2 = 3 
    
class WiprInWipgArFromWMM(BaseEnum):
    on = 1
    Off = 0  
    
class WiprInWipgAr(BaseEnum):
    on = 1
    Off = 0

class DisplayLeftTime(BaseEnum):
    kUnknown = 0
    kCharging = 1
    kCalulating = 2
    kWithin15Min = 3
    kWithin30Min = 4
    kWithin1Hour = 5
    kWithin2Hour = 6
    kWithin3Hour = 7
    kWithin4Hour = 8
    kWithin5Hour = 9
    kWithin6Hour = 10
    kWithin7Hour = 11
    kWithin8Hour = 12
    kWithin9Hour = 13
    kWithin10Hour = 14
    kWithin11Hour = 15
    kWithin12Hour = 16
    kWithin13Hour = 17
    kWithin14Hour = 18
    kWithin15Hour = 19
    kWithin16Hour = 20
    kWithin17Hour = 21
    kWithin18Hour = 22
    kWithin19Hour = 23
    kWithin20Hour = 24
    kWithin21Hour = 25
    kWithin22Hour = 26
    kWithin23Hour = 27
    kWithin24Hour = 28
    k24HourPlus = 29

class MirrFoldCmdTyp(BaseEnum):
    Idle = 0
    FoldIn = 1
    FoldOut = 2
    

class GeneralInVehiclePos(BaseEnum):
    FrontLeft = 0
    FrontRight = 1
    RearLeft = 2
    RearRight = 3

class DkAlertType(BaseEnum):
    OverFlow = 1
    OutOrder = 2
    PacketTimeout = 3
    ACKTimeout = 4
    EncrptErr = 5
    InputError = 6
    
class FotaFailType(BaseEnum):
    ExitFotaModeFail = 0
    FlashDomianEcuFail = 1
    FlashHvEcuFail = 2
    FlashLvEcuFail = 3
    
class FotaTaskType(BaseEnum):
    Normal = 0
    Rescue = 1
    Bridge = 2
    

class DoorfFultSts(BaseEnum):
    OK = 0
    FaultChildLock = 1
    FaultDoorLock = 2
    FaultNA = 3
    FaultDoorLocation = 4
    FaultApsStuck = 5
    FaultShorttoBatOrAPSOpencircuit = 6
    FaultAPSOpenCircuit = 7
    FaultExternalSWStuck = 8
    FaultInternalSWStuck = 9
    FaultVoltageUORO = 10
    FaultPlayProtectionActive = 11
    FaultInternalError = 12
    FaultNoPositionKnown = 13
    FaultE2E = 14
    FaultMismatchSafetyParameter = 15
    ThermalProtection = 16
    RollAngleAbnormal = 17
    RoadInclinationAbnormal = 18
    HallSensorsError = 19

class CheckInterfaceType(BaseEnum):
    Get  = 0
    CheckNotify = 1
    All = 2

class PetModeSts(BaseEnum):
    kOFF = 0
    kON = 1
    kRUN = 2
    kUnExpect = 255

class SourceId(BaseEnum):
    Idle = 0
    HMI = 1
    Remote = 2

class Carmode_subtype(BaseEnum):
    Normal = 0
    Factory_Paused = 1
    Factory_Driving = 2
    Transport_Driving = 3
    Transport = 8
    Factory = 16
    Crash_1 = 24
    Crash_2 = 25
    Dyno_2 = 40
    Dyno_4 = 41

class ImobSts(BaseEnum):
    ImobUndefd = 0
    ImobImobn = 1
    ImobMtn = 2
    ImobNoMtn = 3
class RemoteAuthSts(BaseEnum):
    kDefault = 0            # /**默认状态，默认值 */
    kReady2R = 1            # /**自动授权条件判断 */
    kUnlockWait = 2         # /**等待解锁状态 */
    kReadyEntry = 3         # /**远程授权成功，倒计时 */
    kEntry = 4              # /**进入远程授权模式 */
    kReady2L = 5            # /**授权启动取消,进入本地模式 */

class Settings(BaseEnum):
    Set = 0
    CancelSet = 1

class TailGateOpenerSts(BaseEnum):
    Ukwn = 0
    FullClsd = 1
    MovgUp = 2
    MovgUpBrkg = 3
    StopDurgOpen = 4
    FullOpend = 5
    MovgDown = 6
    MovgDownBrkg = 7
    StopDurgCls = 8
    HalfClsd = 9
    StopMinPntForCls = 10
    Incalid = 65535

class FOTA_TaskType(BaseEnum):
    Rescue = 1
    Bridge = 2

class InfoCanFOTAStatus(BaseEnum):#infocan fotastatus 状态信号值
    Idle = 0
    Query = 1
    Downloading = 2
    Active = 3
    Update = 4
    Rollback = 5
    UpdateFailNotDriving = 6    

class KeySlot(BaseEnum):
    FirstKey = 0
    SecondKey = 1
    TheThirdKey = 2
    TheFourthKey = 3
    All = 4

class KeyConnectType(BaseEnum):
    NoKeyConnected = 0
    NfcCard = 1
    BleKey = 2
    BleUwbKey = 3
    TempBleKey = 4
    IcceBleKey = 5
    ICCENfcKey = 6
    CccNfcBleUwbKey = 7
    CCCNfcKey = 8
    CccNfcBleKey = 9

class ConnectionStatus(BaseEnum):
    Disconnect = 0
    Connect = 1

class ActionType(BaseEnum):
    PrivatetLockSts = 0
    GloveBoxReq = 1

class SetType(BaseEnum):
    Open = 0
    Lock = 2
    Unlock = 3

class GloveBoxStatus(BaseEnum):
    Off = 0
    On = 1
    
class FindZone(BaseEnum):
    ZoneAllOutSide = 0
    ZoneAllWithConnectedOutSide = 1
    ZoneDriverOutSide = 2
    ZonePassengerOutSide = 3
    ZoneTailGateOutSide = 4
    ZoneAllInSide = 5
    ZoneDriverInSide = 6
    ZonePassengerInSide = 7
    ZoneRearInSide = 8
    ZoneRearInSideSimple = 9
    ZoneNa = 10
    
class KeyZone(BaseEnum):
    KeyLocnIdle = 0
    KeyLocnAll = 1
    KeyLocnAllExt = 2
    KeyLocnDrvrExt = 3
    KeyLocnPassExt = 4
    KeyLocnTrExt = 5
    KeyLocnAllInt = 6
    KeyLocnDrvrInt = 7
    KeyLocnPassInt = 8
    KeyLocnResvInt = 9
    KeyLocnResvIntSimple = 10

class MainState(BaseEnum):
    Idle = 0
    Triggering = 1
    ConditionCheck = 2
    Arbitration = 3
    Reseting = 4
    Rebooting = 5

class Notification(BaseEnum):
    Idle = 0
    NotInPark = 1
    Updating = 2
    ShutDownFail = 3
    RestartTriggered = 4
    ArbitrationFail = 5
    
class TeleState(BaseEnum):
    Idle = 0
    Reseting = 1
    Success = 2
    Fail = 3

class AutoState(BaseEnum):
    Idle = 0
    Reseting = 1
    Success = 2
    Fail = 3
    
class CdcState(BaseEnum):
    Idle = 0
    Reseting = 1
    Success = 2
    Fail = 3

class BncmState(BaseEnum):
    Idle = 0
    Reseting = 1
    Success = 2
    Fail = 3

class StsForUsrFb(BaseEnum):
    Undefd = 0
    Opend = 1
    Clsd = 2
    Lockd = 3
    safe = 4

class LockState(BaseEnum):
    UnLock = 0
    Lock = 1  
    SafeLock = 2  

class VehicleUpgradeStatus(BaseEnum):
    #VSP FOTA 升级状态
    Downloading = 4 #下载中，可重置，不可解除
    DownloadSuccess = 5 #下载成功，可重置，不可解除
    Upgrading = 8 #升级中，可重置，不可解除
    UpgradeFail = 10 #升级失败，实际不存在该状态
    Pushing = 14 #推送中，实际不存在该状态
    PushSuccess = 15 #推送成功，可重置，不可解除
    PushFail = 16 #推送失败，不可重置，不可解除
    FOTASuccess = 18 #FOTA成功，不可重置，不可解除
    FOTAFailCanNotDriving = 19 #FOTA失败-不可开车，不可重置，可解除
    FOTACancel = 20 #FOTA取消，不可重置，不可解除
    FOTAFailCanDriving = 21 #FOTA失败-可开车，不可重置，不可解除
    AlreadyLatestVersion = 22 #已是最新版本，不可重置，不可解除

class VehicleInsideOutside(BaseEnum):
    VehicleInSide = 0
    VehicleOutSide = 1

class Side(BaseEnum):
    Left = 0
    Right = 1
    All = 2

class OnOffSafe1(BaseEnum):
    OnOffSafeInvld1 = 0
    OnOffSafeOn = 1
    OnOffSafeOff = 2   
    OnOffSafeInvld2 = 3

class BrkSysCap(BaseEnum):
    NotInitialized = 0
    Full = 1  
    TestPending = 2  
    Fault = 3

class ReqSts2(BaseEnum):
    Default = 0
    NotReqd = 1
    Reqd = 2
    Reserved = 3

class set_usagemode_type(BaseEnum):
    service = 0
    open_fl_door = 1
    open_fr_door = 2
    open_rl_door = 3
    open_rr_door = 4
    occupy_drvr_seat = 5
    hit_brake = 6
    app_set_convenience = 7

class SourceType(BaseEnum):
    kVoicd = 0
    kScreen = 1
    kRemote = 2

class calibration_status(BaseEnum):
    kIdle = 0
    kStartRunning = 1
    kAuthorization = 2
    kCheckPreconditionFailed = 3
    kCalibrationRunning = 4
    kCalibrationSuccess = 5
    kCalibrationFailed = 6

class calibration_error_code(BaseEnum):
    kSuccess = 0
    kFOTARunning = 1
    kHighPriorityRunning = 2
    kAuthorizedFailed = 3
    kCheckPreconditionFailed = 4
    kRoutineFailed = 5
    kUserCancelRoutine = 6
    kRoutingTimeout = 7
    kAuthorizedTimeout = 8
    kCheckPreconditionTimeout = 9

class Inact(BaseEnum):
    Inactive = 0
    Active = 1

class calibration_req(BaseEnum):
    kOff = 0
    KOn = 1

class CalibrationFunctionID(BaseEnum):
    ChrgLid = 0
    DriverSeat = 1
    PassengerSeat = 2
    ClimateVent = 3
    ALM = 4
    InvalidValue = 255


class CalibrationFunctionID(BaseEnum):
    ChrgLid = 0
    DriverSeat = 1
    PassengerSeat = 2
    ClimateVent = 3
    ALM = 4
    InvalidValue = 255


class Authorization_req(BaseEnum):
    kAuthorize = 0
    kCancelAuthorize = 1

class retry_req(BaseEnum):
    kCancel = 0
    kRetry = 1

class OnBdChrgrHndlSts(BaseEnum):
    Disconnected = 0
    ConnectedWithoutPower = 1
    PowerAvailableButNotActivated = 2
    ConnectedWithPower = 3
    DischargeConnectwithoutpowerincar = 4
    DischargeConnectwithoutpoweroutcar = 5
    DischargeConnectwithpowerincar = 6
    DischargeConnectwithpoweroutcar = 7
    Init = 8
    Fault = 9
    NotCompleteConnnected = 10
    Reserved0 = 11
    Reserved1 = 12
    Reserved2 = 13

class ChrgHndlStrtEna(BaseEnum):
    PwrUpNotEna = 0
    PwrUpEna = 1

class PsdNotPsd2(BaseEnum):
    NoInfo1 = 0
    NotPsd = 1
    Psd = 2
    NoInfo2 = 3

class NotifyBookInfoListEVENT(BaseEnum):
    bookType = 0
    repeatType = 1
    weekDay = 2
    startTime = 3
    stopTime = 4



#o_fan.liu edit
class RemSteerWhlHeatgLvlReqLevel(BaseEnum):
    # 加热等级
    Off = 0
    Low = 1
    Mid = 2
    High = 3


#o_fan.liu edit   
class DesPwr(BaseEnum):
    # 预计功率
    Off_power = 0
    Low_power = 30
    Mid_power = 50
    High_power = 90


class AlmSts(BaseEnum):
    Fault = 1
    Normal = 0


class AlmNum(BaseEnum):
    ALM1 = 1
    ALM2 = 2
    ALM3 = 3
    ALM4 = 4
    ALM5 = 5
    ALM6 = 6
    ALM7 = 7
    ALM8 = 8
    ALM9 = 9
    ALM10 = 10

class LatPosition(BaseEnum):
    Undefined = 0
    FullyClosed = 1
    SecondaryPosition = 2
    FullyOpen = 3

class ShortDropSts(BaseEnum):
    Idle = 0
    WindowDown = 1
    WindowClosed = 2
    NotUsed = 3

class ClimateSpcl(BaseEnum):
    # 远程空调设定温度模式
    Normal = 0
    Lo = 1
    Hi = 2

class RangeType(BaseEnum):
    RoadIncln = 0
    RollAgGlb = 1
    
class ChildLockReq(BaseEnum):
    UnLock = 0
    Lock = 1

class LockgCenReq2(BaseEnum):
    Idle = 0
    UnLock = 1
    Lock = 2

class OnOff(BaseEnum):
    "开关0/1状态，适用于所有仅0和1的枚举"
    Off = 0
    On = 1

class BgmApp(BaseEnum):
    s2s_service = 0
    em2 = auto()
    jetlogd = auto()
    service_monitor = auto()

class VehicleMode(BaseEnum):
    CarMode = 0
    UsageMode = 1
    
class Flgsts(BaseEnum):
    Flg1_Rst = 0
    Flg1_Set = 1

class LcmaIndcn(BaseEnum):
    NoLcmaWarn = 0
    LcmaWarnLvl1 = 1
    NotUsed = 2
    LcmaWarnLvl2 = 3

class DoorOpenResistCmd(BaseEnum):
    Idle = 0
    AddResist = 1
    SubtResist = 2
    Resd = 3

class ResistMode(BaseEnum):
    CloseDoor = 0
    DoorOpenWarning = 1

class ActTq(BaseEnum):
    NominalTorque = 0
    reserved0 = 1
    LowTorque = 2
    Tqreserved13 = 3
    
class SequenceAction(BaseEnum):
    kSequenceStart = 0
    kSequenceStop = 1
    kSequencePause = 2
    
class StaticLightingModeEn(BaseEnum):
    ENABLE = 0 
    ACTIVATED = 1
    DISABLE = 2

class ExtrLtgStsStaticLtgShow(BaseEnum):
    DevSts4_Off = 0 
    DevSts4_On = 1
    DevSts4_Err = 2
    DevSts4_Resd = 3


    
    
class DeviceType(BaseEnum):
    # 设备类型
    kACCM = 0
    kHVCH = 1
    kBCFV = 2
    kBCTV = 3
    kECTV = 4
    kBEXV = 5
    kCEXV = 6
    kEEXV = 7
    kREXV = 8
    kEMotorPump = 9
    kHvBatteryPump = 10
    kHeaterPump = 11
    kCoolingFan = 12
    kSOV1 = 13
    kSOV2 = 14
    kSOV3 = 15
    kAll = 255
    
    
class ThermalFaultSts(BaseEnum):
    # 热管理系统部件故障状态
    kNormal = 0
    kFault = 1
    kUnknown = 2
    

class RemoteBatteryHeatingSts(BaseEnum):
    # 远程电池加热状态
    kOff = 0
    kReady = 1
    kOn = 2
    kError = 3
    
class RemoteBatteryHeatingModeSts(BaseEnum):
    # 远程电池加热模式
    kIdle = 0
    kLowTemperatureSelfHeat = 1
    kBookHeat = 2
    kRealTimeHeat = 3  
    
class HeatingEnergySource(BaseEnum):
    # 加热取电能量源
    kNone = 0
    kCharger = 1
    kHVBattery = 2
    
    
class ACDCType(BaseEnum):
    # 充放电设备类型
    kDefault  = 0
    kDC = 1
    kAC = 2
    kACDC = 3
    kUnknown = 255
    

class EngActvnMod1(BaseEnum):
    WakeupFunctionNOTActiveANDExternalRequestNOTPresent = 0
    WakeupFunctionNOTActiveANDExternalRequestPresent = 1
    WakeupFunctionActiveANDExternalRequestNOTPresent = 2
    WakeupFunctionActiveANDExternalRequestPresent = 3
    
class DoorActionTriggerId(BaseEnum):
    NoTriggerSource = 0
    RemoteKey = 1
    HMI = 2
    Telematices = 3
    OutsideSwitch = 4
    InsideSwitch = 5
    Unknown = 255

class DoorAction(BaseEnum):
    Idle = 0
    Open = 1
    Close = 2
    Stop = 3
    OpenMinAngle = 4
    Invalid = 255

class Zone(BaseEnum):
    Zone0 = 0
    Zone1 = 1
    Zone2 = 2
    Zone3 = 3
    Zone4 = 4 
    Zone5 = 5
    Zone6 = 6
    Zone7 = 7
    Zone8 = 8
    Zone9 = 9
    Zone10 = 10

class Validity(BaseEnum):
    NotValid = 0
    Valid = 1

class NoYesCrit1(BaseEnum):
    NotVld1 = 0
    No = 1
    Yes = 2
    NotVld2 = 3
    
    
class DisAdjMov(BaseEnum):  #o_fan.liu
    # DisAdjMov取值
    NotInhb = 0
    Inhb = 1


class ALMZoneId(BaseEnum):
    """
    普通氛围灯灯带编号
    """
    FrontLeft = 1
    FrontRight = 2
    RearLeft = 3
    RearRight = 4
    TweeterLeft = 17
    TweeterRight = 18
    CCLeft = 19
    CCRight = 20
    CCMiddleRight = 29
    CCMiddleLeft = 30
    CCUnder = 31

class tyres(BaseEnum):
    kTyreFrintLeft = 0
    kTyreFrintRight = 1
    kTyreRearLeft = 2
    kTyreRearRight = 3
    kTyreAll = 4
class OutDoorSwitchLightMode(BaseEnum):
    kModeOff = 0
    kOnStatic = 1
    kOnDynamic = 2

class Flg1(BaseEnum):
    Rst = 0
    Set = 1

class RemPrkgSts(BaseEnum):
    PrkgAssiSysRemPrkgSts_OFF = 0
    PrkgAssiSysRemPrkgSts_Remoteparkinstandby = 1
    PrkgAssiSysRemPrkgSts_Remoteparkoutstandby = 2
    PrkgAssiSysRemPrkgSts_Searching = 3
    PrkgAssiSysRemPrkgSts_Remoteparkinpreactive = 4
    PrkgAssiSysRemPrkgSts_Remoteparkactive = 5
    PrkgAssiSysRemPrkgSts_Parkprocessactive  = 6
    PrkgAssiSysRemPrkgSts_Suspend = 7
    PrkgAssiSysRemPrkgSts_Abort = 8
    PrkgAssiSysRemPrkgSts_Remoteparkprocesscompleted = 9
    PrkgAssiSysRemPrkgSts_Remoteparkoutprocscompleted = 10
    PrkgAssiSysRemPrkgSts_Remoteparkcompleted = 11
    PrkgAssiSysRemPrkgSts_Quit = 12
    PrkgAssiSysRemPrkgSts_Failure  = 13
    PrkgAssiSysRemPrkgSts_Cancel = 14

class PtActvnReq1(BaseEnum):
    NoPtActvnReq = 0
    PtActvnReq = 1
    PtActvnReqRem = 2
    PtActvnNotDriving = 3

class DisChargingState(BaseEnum):
    Default = 0
    NoDischarging = 1
    DCDischarging = 2
    DischargingEnd = 3
    DischargingCmpl = 4
    DischargingFault = 5
    ACCharging = 6

class CommandType(BaseEnum):
    kDefault = 0
    kOn = 1
    kOff = 2
    DischargingEnd = 3
    DischargingCmpl = 4
    DischargingFault = 5
    ACCharging = 6

class DischargeSourceId(BaseEnum):
    kDefault = 0
    kVoiceControl = 1 # //语音控制
    kScreenControl = 2 # , //屏幕控制
    kRemoteControl = 3 #, //远程控制
    kBlueTooth = 4 # , //蓝牙控制
    kFota = 5 # Fota控制


class KeySettingItem(BaseEnum):
    Off = 0
    OnWithoutAnyDoorClose = 1
    OnWithDriverDoorClose = 2
    OnWithAllDoorClose = 3
    OnWithAllDoorAndTailgateClose = 4 
    Reserved1 = 5
    Reserved2 = 6
    Reserved3 = 7

class KeySettingType(BaseEnum):
    WalkAay = 0
    Approch = 1
    All = 3

class EnableDisable(BaseEnum):
    Enable = 0
    Disable = 1
    
class LockgCenReq2(BaseEnum):
    Idle = 0
    UnLock = 1
    Lock = 2

class StaticLightingModeEn(BaseEnum):
    ENABLE = 0 
    ACTIVATED = 1
    DISABLE = 2

class ExtrLtgStsStaticLtgShow(BaseEnum):
    DevSts4_Off = 0 
    DevSts4_On = 1
    DevSts4_Err = 2
    DevSts4_Resd = 3

class ChrgSoftSwCtrlSt(BaseEnum):
    OnOffNoReq_NoReq = 0 
    OnOffNoReq_On = 1
    OnOffNoReq_Off = 2

class SequenceAction(BaseEnum):
    kSequenceStart = 0
    kSequenceStop = 1
    kSequencePause = 2

class CommandType(BaseEnum):
    kDefault = 0
    kOn = 1
    kOff = 2
class HV_SourceId(BaseEnum):
    kDefault = 0
    kVoiceControl = 1
    kScreenControl = 2
    kRemoteControl = 3
    kBlueTooth = 4
    kFota = 5

class ACBookChargingReqSts(BaseEnum):
    kDefault = 0
    kBookActive = 1
    kBookDeactive = 2
    kBookOff = 3

class ACBookChargingWorkSts(BaseEnum):
    kBookStsDefault = 0
    kBookStsOff = 1
    kBookStsWait = 2
    kBookStsStandby = 3
    kBookStsCharging = 4
    kBookStsFailed = 5
    kBookStsCanceled = 6
    kBookStsFinish = 7

class DisplayBookChargingType(BaseEnum):
    kNoDisplay = 0
    kAC = 1
    kDC = 2

class BookChargeSetResponse(BaseEnum):
    Default = 0
    Success = 1
    Cancelled = 2
    Fail = 3

class TargetUsageMode(BaseEnum):
    OFF = 0
    INACTIVE = 1
    DRIVING = 2


class WPCZoneId(BaseEnum):
    FrontLeft = 0
    FrontRight = 1
    FrontRow = 2
    All = 12


class WPCZoneNum(BaseEnum):
    Single = 0
    Double = 1


class WPCIsForgotten(BaseEnum):
    NotForgotten = 0
    Forgotten = 1
    Invalid = 255


class WPCCtrlSts(BaseEnum):
    Enable = 0  # 功能开启
    Shutdown_By_Switch = 2  # 用户设置无线充电功能关闭
    Disable_By_NFC = 3  # NFC导致功能关闭
    Invalid = 255  # 默认/无效值


class WPCCtrlRes(BaseEnum):
    enabled = 0
    disabledbyPEPS = 1
    shutdownbySwitchOrCAN = 2
    disabledbyNFC = 3


class WPCChargingSts(BaseEnum):
    Standby = 0  # 待机状态
    Charging = 1  # 充电中
    ChargingComplete = 2  # 充电完成
    ModuleOFF = 3  # 模块关闭
    Fault = 4  # 模块故障
    Invalid = 255  # 无效值(默认)


class WPCModuleSts(BaseEnum):
    OverTemperatureProtected = 0
    Standby = 1
    Charging = 2
    FOD = 3
    VoltageProtected = 4
    OverPowerProtected = 5
    OFF = 7
    InternalFailure = 10
    NFCCardFailure = 12
    Resvd5 = 13
    Resvd6 = 14
    Invalid = 15


class isForgotten(BaseEnum):
    NotForgotten = 0
    Forgotten = 1


class WPCFailureSts(BaseEnum):
    NoFailure = 0
    OverTemperature = 1
    RFOD = 2
    VoltageProtected = 3
    OverPowerProtected = 4
    InternalFailure = 5
    SmartPhoneNoResponseOrUnknown = 6
    OFOD = 7
    NFCCardProtect = 8
    Reserved2 = 9
    Reserved3 = 10
    Reserved4 = 11
    Reserved5 = 12
    Reserved6 = 13
    Reserved7 = 14
    Invalid = 15


class WPCFaultsId(BaseEnum):
    Ok = 0  # 正常
    OverTemperature = 1  # 过温保护
    RFOD = 2  # 检测到异物(通过感抗检测)
    VoltageProtected = 3  # 过压保护
    OverPowerProtected = 4  # 过功率保护
    InternalError = 5  # 内部故障
    OFOD = 7  # 检测到异物(通过功率检测)
    NFCCardProtect = 8  # NFC卡过热保护
    WPCFailureSignalInvalid = 9  # WPCFailureSts信号值无效
    Invalid = 255  # 默认值/无效值

class JIDUChgrFlg(BaseEnum):
    UnknownJiduCharger = 0 #/** 是否集度桩未知 */
    JiduCharger = 1 #/** @brief 集度桩 */
    NotJiduCharger = 2 #/** 非集度桩 */
    PrivateCharger = 3 #/** 私桩 */
    PublicCharger = 4 #/** 公桩 */
    FastCharger = 5 #/** 快充桩 */
    SlowCharger = 6 #/** 慢充桩 */
    UnknownPriPublicCharger = 7 #/** 公私桩未知 */
    ACCharger = 8 #/** 交流桩 */

class HvacTIfQf(BaseEnum):
    SnsrDataNotOk = 0
    SnsrDataOk = 1

class BGM_HWPN(BaseEnum):
    A_8893802862 = '8893802862  A' 
    B_8895036214 = '8895036214  B'
    C_8895036214 = '8895036214  C'
    D_8895036214 = '8895036214  D'
    E_8895036214 = '8895036214  E'
    F_8895036214 = '8895036214  F'
    G_8895036214 = '8895036214  G'
    H_8895036214 = '8895036214  H'
    XH_8895036214 = '8895036214 XH'
    L_8895036214 = '8895036214  L'
    A_2500000095 = '2500000095  A'
    B_2500000095 = '2500000095  B'

class TCAM_HWPN(BaseEnum):
    A_8895036217 = '8895036217  A' 
    A_8893810192 = '8893810192  A'
    B_8895036217 = '8895036217  B'
    C_8895036217 = '8895036217  C'
    D_8895036217 = '8895036217  D'

class StrtReq(BaseEnum):
    NotReqd = 0
    Reqd = 1
    RemReqd = 2
    

class TurnPressGear(BaseEnum):
    NotAvailble = 0 #无状态
    DownPress1stGear = 1 #下拨一档
    DownPress2stGear = 2 #下拨二档
    UpPress1stGear = 3 #上拨一档
    UpPress2stGear = 4 #上拨二档
    Error  = 5 #错误

class HighPressGear(BaseEnum):
    NotAvailble = 0 #无状态
    PressInsd = 1 #内拨
    PressOutd = 2 #外拨
    Error = 3 #错误

class LockSts2(BaseEnum):
    LockStsUkwn = 0 
    Unlckd = 1 
    Lockd = 2 
    SafeLockd = 3 

class Remote_Rescue_DriveSts(BaseEnum):
    kNormal = 0
    kInhibit = 1
    kUnknown = 255

class DoorCode(BaseEnum):
    driver_door_control = 33
    passenger_door_control = 34
    rear_left_door_control = 35
    rear_right_door_control = 36
    All_door = 37

class BookChargingCommandType(BaseEnum):
    kCancel = 0
    kCreate  = 1
    kModify = 2

class RepeatType(BaseEnum):
    kDefault = 0
    kOnce  = 1
    kDaily = 2

class ControlCommandType(BaseEnum):
    kDefault = 0
    kOn = 1
    kOff = 2
class WindowSwitchStatus(BaseEnum):
    kUnknown = 0 #未知
    kIdle = 1 #无请求
    kUpManual = 2 #手动上升
    kUpAuto = 3 #自动上升
    kDownManual = 4 #手动下降
    kDownAuto = 5 #自动下降

class RcwReq(BaseEnum):
    Yes = 0
    No = 1
    
class TweeterZoneId(BaseEnum):
    AllZone = 0
    LeftZone = 1
    RightZone = 2
    
class TweeterCommand(BaseEnum):
    STOP = 0
    UP = 1
    DOWN =2 
    Reserved =3 
    
class TweeterSts(BaseEnum):
    stop = 0
    UP = 1
    DOWN =2 
    Reserved =3


class FootLightSts(BaseEnum):
    On = 1
    Off = 0
    Fault = 2
    


class PulseHeatingSts(BaseEnum):
    # 脉冲加热状态
    kIdle = 0
    kInit = 1
    kHeating = 2
    kHeatFinish = 3
    kError = 4
    kInhibit = 5
    kReserved = 6
    kDefault = 255

class OnOff1(BaseEnum):
    Off = 0  
    On = 1


class DoorSts(BaseEnum):
    Drv = 1
    Pass = 2
    RiRe = 3
    LeRe = 4
    Close = 5

class SteerWheelButtonType(BaseEnum):
    SteerWhlTouchSwtLe2SteerWhlTouchSwt2 = 'SteerWhlTouchSwtLe2SteerWhlTouchSwt2'
    SteerWhlTouchSwtLe3 = 'SteerWhlTouchSwtLe3'
    SteerWhlScButtonMidLe1SteerWhlTouchSwt1 = 'SteerWhlScButtonMidLe1SteerWhlTouchSwt1'
    SteerWhlScButtonMidLe2SteerWhlTouchSwt2 = 'SteerWhlScButtonMidLe2SteerWhlTouchSwt2'

class SteerWheelButtonSts(BaseEnum):
    kSimpleNone = 0
    kSimplePress = 1
    kSimpleLongPress = 2

class WindowsButtonType(BaseEnum):
    WinSwtReqFrntLe = 0  # 主驾驶车窗开关
    WinSwtReqFrntRi = 1  # 主驾侧副驾车窗开关
    WinSwtReqReLe = 2  # 主驾侧左后车窗开关
    WinSwtReqReRi = 3  # 主驾侧右后车窗开关
    WinSwtStsAtPass = 4  # 副驾侧车窗开关
    WinSwtStsAtRele = 5  # 左后侧车窗开关
    WinSwtStsAtReRi = 6  # 右后侧车窗开关

class WindowsButtonSts(BaseEnum):
    kIdle = 0
    kUpManual = 1
    kUpAuto = 2
    kDownManual = 3
    kDownAuto = 4
    kUnknown = 5
