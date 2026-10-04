CALL_SERVICE = 'CallService'
CALL_SERVICE_CLIENT = 'CallService_client'


class TriggerMode:
    partner = 'partner'
    can = 'can'
    pwm = 'pwm'
    crash = 'crash'


class XcallConstants:
    ON = 1
    OFF = 0


class eCallSts:
    kIDLE = 0                # 已取消/default
    kDIALING = 1             # 正在拨号
    kRINGING = 2             # 正在响铃
    kVOICE_CONVERSATIO = 3   # 通话已接通状态
    kINCOMING_CALL = 4       # 来电未接通状态（reserved）
    kHANG_UP = 5             # 已挂断
    kWAIT_FOR_CONFIRM = 6    # 倒计时等待确认中（reserved
    kCALL_FAILURE = 7        # 呼叫失败：由于业务或网络繁忙等导致未接通


class eCallReqSource:
    kCDC = 0                 # CDC
    kACU = 1                 # ACU


class eCallOperationCmd:
    kNO_REQUEST = 0          # 无请求
    kSTART_ECALL = 1         # 开始eCall
    kCANCEL_ECALL = 2        # 取消eCall
    kPICK_UP_ECALL = 3       # 接听eCall
    kHANG_UP_ECALL = 4       # 挂断eCall
    kCONFIRM_ECALL = 5       # 确认拨打eCall


class eCallFunctionSts:
    kREADY = 0               # 无故障
    kECALL_ERROR_MINOR = 1   # 轻微故障
    kECALL_ERROR_SEVERE = 2  # 严重故障
    kIN_SELF_TEST = 3        # 自检中


class eCallType:
    kIDLE = 0                # 默认状态
    kACTIVE = 1              # 主动通话
    kPASSIVE = 2             # 被动通话
    kINCOMING = 3            # 电话回拨
