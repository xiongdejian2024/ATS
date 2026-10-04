#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :soa.py

@Time         :2023/10/31 10:00

@Author       :quan.sun@jiduauto.com

@Description  :soa通信能力模拟 抽象接口
"""
from abc import abstractmethod, ABCMeta
from typing import Union, List, Dict

from xat_ecu.api.constants.common import *

from xat_ecu.api.constants.common import eCallReqSource


class AbcSoa(metaclass=ABCMeta):
    @abstractmethod
    def ck_s2s_req(self, partner_key: str, interface_name: str, ck_info: dict, timeout=1):
        """
        校验被测对象发送的request内容

        :param partner_key: 类似KeyService_client
        :param interface_name: 请求接口名
        :param ck_info: 校验请求内容
        :param timeout: 默认超时1s，用于等待req事件触发
        :return:
        """
        pass

    def ck_s2s_req_v20(self, partner_key: str, interface_name_list: list, ck_info_list=None, timeout=1):
        """
        校验被测对象发送的request内容
        :param partner_key: 类似KeyService_client
        :param interface_name_list: 请求接口名列表
        :param ck_info_list: 校验请求内容列表，与接口名列表一一对应
        :param timeout: 默认超时1s，用于等待req事件触发
        :return:
        """
        pass

    @abstractmethod
    def chk_notify(self, partner_key: str, method_name: str, ck_info: dict, timeout=1, fuzz_match=True):
        """
        检查服务返回的response结果。

        :param partner_key:  类似KeyService_client
        :param method_name:   请求接口名
        :param ck_info:  校验返回值
        :param timeout:  超时时间
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return:
        """
        pass

    @abstractmethod
    def send_request_and_ck_failtype(self, partner_key: str, method_name: str, args: dict,
                                     failtype: Union[FailType, str], timeout=6, is_async=False):
        """
        发送request请求并校验FailType, 在服务未连接时调用，会一直等待服务连接后再发送，因此一定可用获得返回值

        :param partner_key:  类似KeyService_client
        :param method_name:   请求接口名
        :param args:   请求参数
        :param failtype:  返回tailtype，常用: 
        :param timeout:  超时时间
        :param is_async:
        :return:
        """
        pass

    @abstractmethod
    def send_request_and_ck_resp(self, partner_key: str, method_name: str, args: dict,
                                 ck_info: dict, timeout=1, cycle_time=0.2, is_async=False, fuzz_match=True):
        """
        发送request请求并校验结果， 超时时间内每100ms（默认值）调用一次并校验，获取到期望值退出, 在服务未连接时调用，会一直等待服务连接后再发送，因此一定可用获得返回值

        :param partner_key:  类似KeyService_client
        :param method_name:   请求接口名
        :param args:   请求参数
        :param ck_info:  校验返回值
        :param timeout:  超时时间
        :param cycle_time:  调用周期
        :param is_async:
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return:
        """
        pass

    @abstractmethod
    def send_request_and_return_resp(self, partner_key: str, method_name: str, args: dict,
                                     timeout=1, is_async=False):
        """
        发送请求并获取返回值

        :param partner_key: 类似KeyService_client
        :param method_name:   请求接口名
        :param args:   请求参数
        :param timeout:  超时时间
        :param is_async:
        :return: resp
        """
        pass

    @abstractmethod
    def wait_for_service_reconnect(self, partner_key: str, timeout=20):
        """
        服务上线连接后，partner会发出ServiceStatus事件，其中state=START，以此来判断服务连接上

        :param partner_key:  指定某个服务，partner作为client和server都可以
        :param timeout:  超时时间，20s服务没连接报错
        :return:
        """
        pass
    
    @abstractmethod
    def ck_event_and_resp(self, partner_key: str, event_name: str, event_info: dict,
                          method_name=None, method_args=None, resp_info=None,
                          timeout=3, fuzz_match=True):
        """
        校验历史event，并调用get获取结果
        :param partner_key: 类似KeyService_Server
        :param event_name: 待校验event接口名
        :param event_info: 待校验event的数据
        :param method_name: 请求的接口名，默认直接按event前面加Get调用调用
        :param method_args: 请求接口的入参，默认不传
        :param resp_info: 请求的预期响应结果
        :param timeout: 等待预期的event超时
        :param fuzz_match: 是否模糊匹配
        """

    @abstractmethod
    def ck_s2s_event(self, partner_key: str, interface_name: str, ck_info: dict, timeout=3, fuzz_match=True):
        """
        校验被测对象发送的resp内容

        :param partner_key: 类似KeyService_Server
        :param interface_name: 接口名
        :param ck_info: 校验事件内容
        :param timeout: 校验时间
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return raw_data: event数据内容
        """
        pass

    @abstractmethod
    def return_latest_event(self, partner_key: str, interface_name: str, pop_event: bool=False):
        """
        返回指定接口最近的一次event消息

        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        :param pop_event:  获取最新数据后是否弹出，默认弹出
        """
        pass

    @abstractmethod
    def ck_no_event(self, partner_key: str, interface_name: str, timeout=1):
        """
        校验指定时间内无指定event事件上报

        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        :param timeout: 校验时间
        :return:
        """
        pass

    @abstractmethod
    def ck_no_specific_event(self, partner_key: str, interface_name: str, hint: str, timeout=1):
        """
        校验指定时间内无指定服务的event事件上报，当前主要用于WTI，固定列表上报，只校验列表中无value=hint

        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        :param hint: 告警信息
        :param timeout: 校验时间
        :return:
        """
        pass

    @abstractmethod
    def ck_no_req(self, partner_key: str, interface_name: str, timeout=1):
        """
        校验指定时间内无指定method请求

        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        :param timeout: 校验时间
        :return:
        """
        pass

    @abstractmethod
    def register_event(self, partner_key: str, event_list: Union[None, List[Dict]] = None):
        """
        注册指定服务的指定event

        :param partner_key: 类似KeyService_Server
        :param event_list: 默认all，即全部event，否则给定event列表,[{"Status": 1}, {"DoorAngle": 2}], 键值对中值1: 注册后需要发送历史数据， 值2: 不需要发送历史数据
        :return:
        """
        pass

    @abstractmethod
    def unregister_event(self, partner_key: str, event_list: Union[None, List[Dict]] = None):
        """
        反注册指定服务的指定event

        :param partner_key: 类似KeyService_Server
        :param event_list: 默认all，即全部event，否则给定event列表
        :return:
        """
        pass

    @abstractmethod
    def send_method_request(self, partner_key: str, method_name: str, args: dict, is_async=False):
        """
        发送request请求

        :param partner_key: 类似KeyService_Server
        :param method_name:   请求接口名
        :param args:   请求参数
        :param is_async: 是否需要同步执行
        :return:
        """
        pass

    @abstractmethod
    def send_event_notify_thread_start(self, partner_key: str, event_name: str, args: dict, cycle_time: float = 1):
        """
        异步开始发送event事件

        :param partner_key: 类似KeyService_Server
        :param event_name: 请求接口名
        :param args: 请求参数
        :param cycle_time: 周期时间
        :return:
        """
        pass

    @abstractmethod
    def send_event_notify_thread_stop(self, partner_key):
        """
        停止发送event事件

        :param partner_key: 类似KeyService_Server
        :return:
        """
        pass

    @abstractmethod
    def send_event_notify_thread_update(self, partner_key: str, event_name: str, args: dict, cycle_time=None):
        """
        更新已发送的event事件

        :param partner_key: 类似KeyService_Server
        :param event_name: 请求接口名
        :param args: 请求参数
        :param cycle_time: 周期时间
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def send_response_to_req_start(self, partner_key: str, func):
        """
        开始调用注册函数，开始监测req，并且根据提取定义的函数会response

        :param partner_key: 类似KeyService_Server
        :param func: 需要注册的回调函数
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def send_response_to_req_stop(self, partner_key: str, func):
        """
        停止之前注册的回调函数，开始监测req，并且根据提取定义的函数会response

        :param partner_key: 类似KeyService_Server
        :param func: 需要注册的回调函数
        :return:
        """
        pass

    @abstractmethod
    def hmi_set_wash_mode(self, sts: isOn, time_wait: Union[float, int] = 0):
        """
        CDC设置洗车模式开关状态

        :param sts: 开关状态,Off表示关,On表示开
        :param time_wait: 执行操作之后的延时时间，默认是0
        :return:
        """
        pass

    @abstractmethod
    def hmi_set_start_adjust_viewmirror(self, viewPos: ViewPos, direction: Direction, time_wait: Union[float, int] = 0):
        """
        CDC开始调节后视镜操作

        :param viewPos:指定要调节的外后视镜位置,RearRight,RearLeft,All
        :param direction:指定调节的方向,Forward,Left,Up,Backward,Right,Down
        :param time_wait: 执行操作之后的延时时间，默认是0
        :return:
        """
        pass

    @abstractmethod
    def hmi_set_door_close_lock(self, lock_cmd: LockCmd, source: LockSource,
                                find_key_type: Union[FindKeyType, None] = None, time_wait: Union[float, int] = 0):
        """
        S2S服务设置整车上锁解锁

        :param lock_cmd: 整车上锁解锁UnLock = 0 Lock = 1 AllDoorCloseAndLock = 2 LockCompleteArm = 3`
        :param source: 指请求源 RKE = 0 Telm = 1 Hmi = 2 APA = 3
        :param find_key_type: 闭锁前找钥匙类型 NotReq = 0 OutsideKey = 1 InsideKey = 2 OutsideAndInsideKey = 3
        :param time_wait: 执行操作之后的延时时间，默认是0
        :return:
        """
        pass

    @abstractmethod
    def get_alrm_info(self, sys_fault: SysFault, sys_sts: SysDefenSts, alm_src: AlmSrc, timeout=5):
        """
        S2S获取车辆设防系统报警状态

        :param sys_fault:
        :param sys_sts:
        :param alm_src:
        :param timeout:
        :return:
        """
        pass

    @abstractmethod
    def start_get_wiper_switch_sts(self):
        """
        开始启动进程获取雨刮开关状态

        :return:
        """
        pass

    @abstractmethod
    def stop_get_wiper_switch_sts(self):
        """
        停止获取雨刮开关状态进程

        :return:
        """
        pass

    @abstractmethod
    def get_wiper_switch_sts(self):
        """
        获取雨刮开关状态进程

        :return:
        """
        pass

    @abstractmethod
    def hmi_set_wiper_mode(self, pos: WiperPos, mode: WiperMode):
        """
        S2S设置雨刮模式

        :param pos: 要设置的雨刮位置，Front,Rear,All
        :param mode: 雨刮模式
        :return:
        """
        pass

    @abstractmethod
    def hmi_set_wiper_wash_func(self, pos: WiperPos, sts: isOn):
        """
        S2S设置雨刮模式

        :param pos: 要设置的雨刮位置，Front,Rear,All
        :param sts: 雨刮洗涤开关
        :return:
        """
        pass

    @abstractmethod
    def hmi_set_wiper_maintaince_pos(self, sts: isOn):
        """
        S2S设置雨刮维修服务模式

        :param sts: 维修模式开关状态
        :return:
        """
        pass

    @abstractmethod
    def get_wiper_maintaince_pos(self, sts: isOn):
        """
        S2S获取雨刮维修服务模式

        :param sts: 维修模式开关状态
        :return:
        """
        pass

    @abstractmethod
    def event_check_wiper_maintaince_pos(self, sts: isOn):
        """
        S2S Check雨刮维修服务模式事件上报

        :param sts: 维修模式开关状态
        :return:
        """
        pass

    @abstractmethod
    def get_batterylow_mode(
            self,
            BatteryLowTelltale: BatteryLowTelltale,
            isFirstWarn: bool,
            isSecondWarn: bool
    ):
        """
        获取电量低报警信息

        :param BatteryLowTelltale:
        :param isFirstWarn:
        :param isSecondWarn:
        :return:
        """
        pass

    @abstractmethod
    def get_charging_info(self, isTempHigh: bool):
        """
        获取充电信息

        :param isTempHigh: True/False
        :return:
        """
        pass

    @abstractmethod
    def get_wiper_mode(self, pos: WiperPos, mode: WiperMode):
        """
        S2S获取雨刮模式

        :param pos: 要设置的雨刮位置，Front,Rear,All
        :param mode: 雨刮模式
        :return:
        """
        pass

    @abstractmethod
    def event_check_wiper_mode(self, pos: WiperPos, mode: WiperMode):
        """
        S2S Check雨刮模式改变事件上报

        :param pos: 要设置的雨刮位置，Front,Rear,All
        :param mode: 雨刮模式
        :return:
        """
        pass

    @abstractmethod
    def hmi_set_wiper_move_inhibit(self, sts: isOn):
        """
        S2S 设置雨刮移动禁用

        :param sts: 雨刮禁用开关状态
        :return:
        """
        pass

    @abstractmethod
    def get_wiper_inhibit_sts(self, pos: WiperPos, move_inhibit: isOn, wash_inhibit: isOn):
        """
        S2S服务获取雨刮禁用状态

        :param pos: 要设置的雨刮位置，Front,Rear,All
        :param move_inhibit: 雨刮活动禁用开关状态
        :param wash_inhibit: 雨刮清洗禁用开关状态
        :return:
        """
        pass

    @abstractmethod
    def event_check_wiper_inhibit_sts(self, pos: WiperPos, move_inhibit: isOn, wash_inhibit: isOn):
        """
        S2S查看雨刮禁用状态改变事件

        :param pos: 要设置的雨刮位置，Front,Rear,All
        :param move_inhibit: 雨刮活动禁用开关状态
        :param wash_inhibit: 雨刮清洗禁用开关状态
        :return:
        """
        pass

    @abstractmethod
    def hmi_set_wiper_wash_inhibit(self, pos: WiperPos, sts: isOn):
        """
        S2S服务设置雨刮洗涤禁用

        :param pos: 要设置的雨刮位置，Front,Rear,All
        :param sts: 雨刮洗涤禁用开关状态
        :return:
        """
        pass

    @abstractmethod
    def get_wiper_wash_sts(self, pos: WiperPos, sts: isOn):
        """
        S2S服务获取雨刮洗涤状态

        :param pos: 要设置的雨刮位置，Front,Rear,All
        :param sts: 雨刮洗涤禁用开关状态
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_wiper_wash_sts(self, pos: WiperPos, sts: isOn):
        """
        S2S查看雨刮洗涤状态改变事件

        :param pos: 要设置的雨刮位置，Front,Rear,All
        :param sts: 雨刮洗涤禁用开关状态
        :return:
        """
        pass

    @abstractmethod
    def get_battery_low_warn_info(self,
                                  BatteryLowTelltale: BatteryLowTelltale,
                                  isFirstWarn: bool,
                                  isSecondWarn: bool):
        """
        获取电量低报警信息

        :param BatteryLowTelltale:
        :param isFirstWarn:
        :param isSecondWarn:
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_tailwing_mode(self, mode: TailWindMode, time_wait: Union[float, int] = 0):
        """
        S2S设置尾翼开关模式

        :param mode: 尾翼模式状态 Off = 0 On = 1 Auto = 2 NA = 3
        :param time_wait: 执行操作之后的延时时间，默认是0
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_tailgate_mode(self, cmd: TailGateMode, time_wait: Union[float, int] = 0):
        """
        S2S设置尾门动作

        :param mode: 设置尾门动作 Open = 0 Close = 1 Stop = 3 OpenMinAngle = 4
        :param time_wait: 执行操作之后的延时时间，默认是0
        :return:
        """
        pass

   #o_fan.liu edit
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_steer_wheel_heat_level(self, level: HeatLevel, source:SourceId, time_wait: Union[float, int] = 0):
        """
        S2S设置方向盘加热等级

        :param level: 方向盘加热等级 Off = 0 Low = 1 Mid = 2 High = 3
        :param source: S2S获取方向盘加热等级事件上报 Idle = 0   HMI = 1   Remote = 2
        :param time_wait: 执行操作之后的延时时间，默认是0
        :return:
        """
        pass

  #o_fan.liu edit
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_steer_wheel_heat_level(self, level: HeatLevel, source:SourceId):
        """
        S2S获取方向盘加热等级

        :param level: 方向盘加热等级 Off = 0 Low = 1 Mid = 2 High = 3
        :param source: S2S获取方向盘加热等级事件上报 Idle = 0   HMI = 1   Remote = 2
        :return:
        """
        pass

  #o_fan.liu edit
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_steer_wheel_heat_level(self, level: HeatLevel, source:SourceId):
        """
        S2S获取方向盘加热等级事件上报

        :param level: S2S获取方向盘加热等级事件上报 Off = 0 Low = 1 Mid = 2 High = 3
        :param source: S2S获取方向盘加热等级事件上报 Idle = 0   HMI = 1   Remote = 2
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_belt_warning(self, seat_id: SeatId, warn_sts: BeltWarning, time_wait: Union[float, int] = 0):
        """
        S2S获取安全带提醒

        :param seat_id: 座椅id FrontLeft = 0 FrontRight  = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param warn_sts: 安全带未系报警状态 Normal = 0 OccupiedAndFasten = 1 Level1 = 2 Level2Low = 3 Level2High = 4 Fault = 5``
        :param time_wait: 执行操作之后的延时时间，默认是0
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_belt_warning(self, seat_id: SeatId, warn_sts: BeltWarning):
        """
        S2S安全带提醒事件上报

        :param seat_id: 座椅id FrontLeft = 0 FrontRight  = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param warn_sts:安全带未系报警状态	 Normal = 0 OccupiedAndFasten = 1 Level1 = 2 Level2Low = 3 Level2High = 4 Fault = 5``
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_warning_msg_List(self, name: str, info: str):
        """
        S2S获取警示信息列表

        :param name: 告警提示的名字
        :param info: 告警提示的信息
        :return:
        """
        pass

    @abstractmethod
    def s2s_set_usage_mode(self, usage_mode: UsageMode):
        """
        设置车辆UsageMode

        :param usage_mode: 枚举类型UsageMode
        :returns:
        """
        pass

    @abstractmethod
    def s2s_set_car_mode(self, car_mode: CarMode):
        """
        设置car_mode

        :param car_mode: 枚举类型CarMode
        :returns:
        """
        pass

    @abstractmethod
    def s2s_set_gear(self, gear: Gear):
        """
        挡位切换通过SOA 实现

        :param gear: 枚举类型Gear
        :returns:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def s2s_set_mntnmode(self, mntnmode: bool):
        """
        通知车辆维修模式

        :param mntnmode: bool
        :returns:
        """
        pass

    @abstractmethod
    def send_SetBookEvent_req(self, args_in=None):
        """
        通过SOA Partner发送SetBookEvent请求

        :param args_in: 类似KeyService_client
        :return: 无
        """
        pass

    @abstractmethod
    def check_GetHeat_req(self, timeout=1):
        """
        通过SOA Partner监听TCAM是否发出SteerWheelService:GetHeat请求。

        :return: 返回监听结果bool
        """
        pass

    @abstractmethod
    def response_to_GetHeat_req(self, heatlevel: HeatLevel):
        """
        通过SOA Partner发送SteerWheelService:GetHeat请求的响应

        :param heatlevel:  加热等级，枚举 Off = 0 Low = 1 Mid = 2 High = 3
        :return: 无
        """
        pass

    @abstractmethod
    def check_GetRemotePowerStatus_req(self, timeout=1):
        """
        通过SOA Partner监听TCAM是否发出ClimateControlService:GetRemotePowerStatus请求

        :return: 返回监听结果bool
        """
        pass

    @abstractmethod
    def check_NotifyTimeUpEventInfo_event(self, timeout=1):
        """
        通过SOA Partner监听RtcAlarmService:UpdateNotifyTimeUpEventInfoEvent事件是否发出

        :return:
        """
        pass

    @abstractmethod
    def response_to_GetRemotePowerStatus_req(self, rem_pow_sts: RemClimateSts):
        """
        通过SOA Partne发送ClimateControlService:GetRemotePowerStatus请求的响应

        :param rem_pow_sts: 远程空调状态 Off = 0 On = 1 SignalMissing = 251 SignalCounterFault = 252 SignalChecksumFault = 253 SignalE2EFault = 254 Invalid = 255
        :return: 无
        """
        pass

    @abstractmethod
    def check_GetDefrostSts_req(self, timeout=1):
        """
        通过SOA Partner监听TCAM是否发出ClimateControlService:GetDefrostSts请求

        :return: 返回监听结果bool
        """
        pass

    @abstractmethod
    def response_to_GetDefrostSts_req(self, defrostmax: bool, climatedefrost: bool):
        """
        通过SOA Partner发送ClimateControlService:GetDefrostSts请求的响应

        :param defrostmax: 类似KeyService_Server
        :param climatedefrost:
        :return: 返回监听结果bool
        """

        pass

    @abstractmethod
    def check_GetChargingInfo_req(self, timeout=1):
        """
        通过SOA Partner监听TCAM是否发出HighVoltageService:GetChargingInfo请求

        :return: 返回监听结果bool
        """
        pass

    @abstractmethod
    def response_to_GetChargingInfo_req(self, charg_sts: ChargingSts = ChargingSts.Default,
                                        plug_sts: PluggerSts = PluggerSts.Disconnected, tar_soc: float = 0.0,
                                        charg_complete_sts: bool = True,
                                        book_charg_sts: BookChargeSts = BookChargeSts.Default,
                                        is_charging_pre: bool = True):
        """
        :param charg_sts: 充电状态 Default = 0 NoCharging = 1 ACCharging = 2 ACChargingEnd = 3 ChargingCmpl = 4 Heating = 5  Booking = 6 NoDischarging = 7 Discharging = 8 DischargingEnd = 9 DischargingCmpl = 10 Chargingfault = 11 DischargingFault = 12 ACChrgnFltChrgrSide = 14 DCCharging = 15 DCChrgnFltVehSide = 18 DCChrgnFltChrgrSideTempFlt = 19 DCChrgnFltChrgrSideConFlt = 20 DCChrgnFltChrgrSideHwFlt = 21 DCChrgnFltChrgrSideEmgyFlt = 22 DCChrgnFltChrgrSideComFlt = 23 SuperCharging = 24 ACChargingSuspend = 25 DCChargingEnd = 26 ACChrgnFltVehSide = 27 Boostcharging = 28 BoostchargingFlt = 29 WirelessCharging = 30
        :param plug_sts: 充电枪状态  Disconnected = 0  ConnectedWithoutPower = 1  PowerAvailableButNotActivated = 2 ConnectedWithPower = 3 Init = 4 Fault = 5
        :param tar_soc: 充电目标SOC
        :param charg_complete_sts:
        :param book_charg_sts: 高压电池充电完成状态 Default = 1 On = 1 Off = 2 Reserve = 3
        :param is_charging_pre: 充电准备中
        :return:
        """
        pass

    @abstractmethod
    def check_SetOutput_req(self, timeout=1):
        """
        通过SOA Partner监听TCAM是否发出HighVoltageService:SetOutput请求

        :return: 返回监听结果bool
        """
        pass

    @abstractmethod
    def check_GethvActiveSts_req(self, timeout=1):
        """
        通过SOA Partner监听TCAM是否发出HighVoltageService:GethvActiveSts请求

        :return: 返回监听结果bool
        """
        pass

    @abstractmethod
    def response_to_GethvActiveSts_req(self, hv_act_sts: HVActiveSts):
        """
        通过SOA Partner发送HighVoltageService:GethvActiveSts请求的响应

        :param hv_act_sts: 高压激活状态 枚举值 Open = 0 Close = 1 Keep = 2 Open_And_Req_Act_Dcha = 3
        :return: 无
        """
        pass

    @abstractmethod
    def check_SetBatteryHeating_req(self, req_type: ThermalRequestType = ThermalRequestType.kNoRequest,
                                          on: bool = True, value: float = 28.0, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出HighVoltageService:SetBatteryHeating请求
        
        Args:
        :param req_type (ThermalRequestType, optional): 请求类型，默认为ThermalRequestType.kNoRequest.
        :param on (bool, optional): 是否开启电池加热，默认为True.
        :param value (float, optional): 电池加热目标温度值，默认为28.0.
        :param timeout (Union[float, int], optional): 超时时间，单位为秒，默认为1.
        :return: 无
        """

    @abstractmethod
    def check_GetSeatHeatVentStatus_req(self, seats: list = [12], timeout=1):
        """
        监听获取座椅通风加热状态请求

        通过SOA Partner监听TCAM是否发出SeatService:GetSeatHeatVentStatus请求
        :param seats: 要获取座椅加热通风状态的座椅ID，列表类型        
        :return: 返回监听结果bool
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def response_to_GetSeatHeatVentStatus_req(self, work_sts: VentWorkStatus = VentWorkStatus.kNone,
                                              pass_work_sts: VentWorkStatus = VentWorkStatus.kNone,
                                              dri_heat_level: HeatLevel = HeatLevel.Off,
                                              pass_heat_level: HeatLevel = HeatLevel.Off):
        """
        响应获取座椅通风加热状态请求 , 通过SOA Partne发送SeatService:GetSeatHeatVentStatus请求的响应

        :param work_sts: 主驾座椅加热状态，枚举值，取值范围:  kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param pass_work_sts: 副驾座椅加热状态，枚举值，取值范围:  kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param dri_heat_level: 主驾座椅加热等级，枚举值，取值范围:  Off = 0 Low = 1 Mid = 2 High = 3
        :param pass_heat_level: 副驾座椅加热等级，枚举值，取值范围:  Off = 0  Low = 1   Mid = 2 High = 3
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_GetBatteryTemperatureInfo_req(self, timeout=1):
        """
        监听获取高压电池温度信息请求 通过SOA Partne发送HighVoltageService:GetBatteryTemperatureInfo请求

        :return: 返回监听结果bool
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def response_to_GetBatteryTemperatureInfo_req(self, min_temp: Union[None, float] = 0,
                                                  max_temp: Union[None, float] = 0,
                                                  average_temp: Union[None, float] = 0):
        """
        响应获取高压电池温度信息请求 通过SOA Partne发送HighVoltageService:GetBatteryTemperatureInfo请求的响应

        :param min_temp: 高压电池最大温度
        :param max_temp: 高压电池最小温度
        :param average_temp: 高压电池平均温度
        :return: 
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def notify_BatteryHeatingInfo(self, current_sts: BatteryThermalSts, req_sts: ThermalReqSts,
                                  estimate_time: Union[None, int] = 0):
        """
        通知高压电池热管理状态信息 通过SOA Partne发送HighVoltageService:BatteryHeatingInfo通知

        :param current_sts: BECM反馈的电池热管理状态
        :param req_sts: 由ECM反馈的整车电池热管理状态
        :param estimate_time: 电池热管理运行时间
        :return: 
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_high_voltage_setoutput_request(self, check_time: float):
        """
        检查TCAM是否2s周期发送上高压请求，检查十次
        :param check_time: 需要持续检查的时间
        :return: 
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def notify_HVSOCInfo(self, realSoc: float = -1.0, calDTESOC: float = -1.0, displaySoc: float = -1):
        """
        发送高压电池SOC通知

        :param realSoc: 具体的SOC值
        :return: 
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def notify_VehicleTimeInfo(self, UTC_date: Union[int, None] = 0, UTC_time: Union[int, None] = 0,
                               time_zone: Union[TimeZone, None] = TimeZone.EAST_8,
                               sync_sts: Union[TimeSyncSts, None] = TimeSyncSts.Default,
                               poli_time_zone: Union[str, None] = " "):
        """
        通知车辆时间信息

        :param UTC_date: UTC日期
        :param UTC_time: UTC时间
        :param time_zone: 当前时区
        :param sync_sts: 时间同步标志位
        :param poli_time_zone: 政治时区
        :return: 
        """
        pass

    @abstractmethod
    def get_ua_status(self, domain_name: DOMAIN, ua_event_field: UA_EVENT):
        """
        返回域控 UA最新的Status event内容
        
        :param domain_name: 枚举类型 DOMAIN:  class DOMAIN(BaseEnum): BGM = 0  TCAM = 1 CDC = 2 ACU = 3
        :param ua_event_field: 枚举类型 UA_EVENT: class UA_EVENT(BaseEnum): Status = 0 DownloadStatus = 1 PreUpdateStatus = 2 UpdateStatus = 3 ErrorCode = 4 DownloadFileSize = 5 DownloadTotalFileSize = 6 DownloadSpeed = 7 Progress = 8 UpdateFileSize = 9 UpdateTotalFileSize = 10
        :returns Domain:  UA event status
        :raises keyError: None
        """
        pass

    @abstractmethod
    def get_fota_status(self, master_event_field: MASTER_EVENT, wait: bool=True):
        """
        返回BGM FOTA Master最新的Status event内容
        
        :param master_event_field: 枚举类型 MASTER_EVENT: class MASTER_EVENT(BaseEnum): Status = 0 TaskId = 1 ErrorCode = 2
        :returns status: FOTA Master event status
        :raises keyError: None
        """
        pass

    @abstractmethod
    def send_fota_request(self, master_request: MASTER_REQUEST, args={}, retry: bool=True):
        """
        作为FOTA Master Client端, 发起request请求
        
        :param master_request: 枚举类型 MASTER_REQUEST: class MASTER_REQUEST(BaseEnum): GetStatus = 0 GetTaskInfo = 1 CancelFota = 2 StartDownload = 3 StopDownload = 4 SuspendDownload = 5 ResumeDownload = 6 StartUpdate = 7 GetConditionCheck = 8 GetFunctionSts = 9 StopUpdate = 10 CheckTask = 20 GetAppointment = 21 CancelAppointment = 22 SetAppointment = 23
        :param retry: 发送StartDownload之后，UA状态不为DOWNLOAD时是否重试
        :returns: None
        :raises keyError: None
        """
        pass

    @abstractmethod
    def send_ua_request(self, domain_name: DOMAIN, ua_request: UA_REQUEST, args={}):
        """
        作为Domain UA Client端, 发起request请求:
        
        :param domain_name: 枚举类型 UA_REQUEST: class UA_REQUEST(BaseEnum): GetStatus = 0 SuspendDownload = 1 ResumeDownload = 2 CancelDownload = 3 PreUpdate = 4 StartUpdate = 5 CancelUpdate = 6 Rollback = 7 Activate = 8 FinishUpdate = 9 StartDownload = 20
        :param ua_request: 下载请求, 格式要求见 “https://jama.jiduauto.com/perspective.req#/items/160527?projectId=46”
        :returns: None
        :raises keyError: None
        """
        pass

    @abstractmethod
    def ua_back_to_idle(self, domain_name: DOMAIN):
        """
        根据Domain UA当前状态, 发送对应request, 让UA回到Idle

        :returns: None
        :raises keyError: None
        """
        pass

    @abstractmethod
    def notify_fota_status(self, state: FOTAMasteSts, errorCode: int = 0):
        """
        通知FOTAMaste状态

        :param state: 用于告知当前FOTA信息
        :param errorCode: 错误代码
        :returns: None
        :raises keyError: None
        """
        pass

    @abstractmethod
    def start_send_ua_event(self, domain_name: DOMAIN, event_args):
        """
        开始发送某域控UA的Status event 
                    
        :param domain_name: 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3
        :param event_args: event内容
        :returns: None
        :raises keyError: None
        """
        pass

    @abstractmethod
    def stop_send_ua_event(self, domain_name: DOMAIN):
        """
        停止发送某域控UA的Status event 
                    
        :param domain_name: 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3
        :returns: None
        :raises keyError: None
        """
        pass

    @abstractmethod
    def update_ua_event(self, domain_name: DOMAIN, event_args):
        """
        更新某域控发送的UA Status event 
                    
        :param domain_name: 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3
        :param event_args: event内容
        :returns: None
        :raises keyError: None
        """
        pass

    @abstractmethod
    def pack_ua_event_args(self, ua_sts: UA_Sts, errorCode=0):
        """
        打包符合UA Status event 格式定义的json字符串       
             
        :param ua_sts: 枚举类型 UA_Sts: class UA_Sts(BaseEnum): IDLE = 0 DOWNLOAD = 1 READY_TO_INSTALL = 2 INSTALLING = 3 UPDATE_FINISH = 4 ROLLING_BACK = 5 SYSTEM_ACTIVE = 6 ERROR = 7 ACTIVATING = 8 UPDATE_FAILED = 9
        :param errorCode: UA错误码
        :returns: UA Status json
        :raises keyError: None
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_climate_power_sts(self, zone: ClimateZone, sts: isOn, timeout: Union[float, int] = 0.5):
        """
        设置空调开关状态

        :param zone: 控制的空调区域 AllZone = 0 FirstRow =  1 SecondRow =  2 FirstRowLeft =  3 FirstRowRight =  4 SecondRowLeft =   5 SecondRowMiddle =   6 SecondRowRight = 7
        :param sts: 开关状态 Off = False On = True
        :returns: None
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_climate_ac_sts(self, sts: bool, timeout: Union[float, int] = 0.5):
        """
        设置A/C开或关模式

        :param sts 开关状态 bool
        :returns: None
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_climate_windspeed(self, zone: ClimateZone, speed: WindSpeed, timeout: Union[float, int] = 0.5):
        """
        设置A/C开或关模式

        :param zone: 控制的空调区域
        :param speed: 设置出风速度
        :returns: None
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_climate_auto_mode(self, zone: ClimateZone, sts: bool, timeout: Union[float, int] = 0.5):
        """
        设置空调自动模式开启关闭

        :param zone: 控制的空调区域
        :param sts: 自动模式开启关闭
        :returns: None
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_climate_cycle_mode(self, mode: CycleMode, timeout: Union[float, int] = 0.5):
        """
        S2S设置内外循环模式

        :param mode: 空调的循环模式 Auto, /* 自动 */ AutoWithAirQuality, /* 自动+空气净化 */ InternalCirculation, /* 内循环 */ ExternalCirculation /* 外循环 */
        :returns: None
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_climate_ac_sts(self, sts: bool, timeout: Union[float, int] = 0):
        """
        SOA获取A/C开或关模式

        :param sts: 开关状态 bool
        :returns: None
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_climate_ac_mode(self, sts: bool, timeout: Union[float, int] = 0):
        """
        SOA获取空调A/C状态

        :param sts: bool
        :param timeout:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_set_extilight_mode(self, target_mode: ExteriorLightMode):
        """
        获取当前的外灯模式，如果不是期望值就会调用服务设置为期望值

        :param target_mode: 期望的外灯模式 Off = 0 Auto = 1 Position = 2 LowHeam = 3
        :returns: None
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_low_beam_sts(self, mode: ExteriorLightMode):
        """
        通过事件上报和获取状态服务获取近光灯模式

        :param mode: 近光灯模式 Off = 0 Auto = 1 Position = 2 LowHeam = 3
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_high_beam_sts(self, sts: HighBeamSts, clientId: LowBeamClientId):
        """
        通过服务获取远光灯状态

        :param sts: 远光灯状态 Off = 0 On = 1 Err = 2
        :param clientId: 触发源 Reserve = 0 GameMode = 1 SteerWheelBut = 2 Voice = 3 ANP = 4 AVP = 5 AHBC = 6 NoFunc = 255
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_high_beam_sts(self, sts: Union[HighBeamSts,None], clientId: LowBeamClientId):
        """
        通过服务获取远光灯事件上报

        :param sts: 远光灯状态 Off = 0 On = 1 Err = 2
        :param clientId: 触发源 Reserve = 0 GameMode = 1 SteerWheelBut = 2 Voice = 3 ANP = 4 AVP = 5 AHBC = 6 NoFunc = 255
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_auto_high_beam_sts(self, auto_sts: AutoHighBeamSts):
        """
        通过服务获取自动远光灯事件上报

        :param auto_sts: 自动远光灯状态 Off = 0 On = 1 AHBC = 2 AHBC_Temporarily_Off = 3 Error = 4
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_high_beam_sts(self, auto_sts: AutoHighBeamSts, sts: HighBeamSts, clientId: LowBeamClientId):
        """
        通过事件上报和获取状态服务获取远光灯模式

        :param auto_sts: 自动远光灯状态 Off = 0 On = 1 AHBC = 2 AHBC_Tempora
        :param sts: 远光灯状态 Off = 0 On = 1 Err = 2
        :param clientId: 触发源 Reserve = 0 GameMode = 1 SteerWheelBut = 2 Voice = 3 ANP = 4 AVP = 5 AHBC = 6 NoFunc = 255
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_extilight_mode(self, mode: ExteriorLightMode):
        """
        获取当前的外灯模式

        :param mode: 期望的外灯模式 Off = 0 Auto = 1 Position = 2 LowHeam = 3
        :returns: None
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_extilight_mode(self, mode: ExteriorLightMode, time_wait: Union[float, int] = 0):
        """
        设置的外灯模式

        :param mode: 外灯模式 Off = 0 Auto = 1 Position = 2 LowHeam = 3
        :returns: None
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_extilight_mode(self, mode: ExteriorLightMode):
        """
        检测外灯模式事件上报

        :param mode: 期望的外灯模式 Off = 0 Auto = 1 Position = 2 LowHeam = 3
        :returns: None
        """
        pass

    @abstractmethod
    def send_response_to_req_start(self, partner_key: str, func):
        """
        开始回复client的requset调用, mock server端时使用

        :param partner_key: 类似KeyService_Server
        :param func: 函数名
        :return:
        """
        pass

    @abstractmethod
    def send_response_to_req_stop(self, partner_key: str, func):
        """
        停止回复client的requset调用, mock server端时使用

        :param partner_key: 类似KeyService_Server
        :param func: 函数名
        :return:
        """
        pass

    def check_GetSeatHeatVentStatus_req_and_feedback_resp(self, seats: list = [12],
                                                          work_sts: VentWorkStatus = VentWorkStatus.kNone,
                                                          pass_work_sts: VentWorkStatus = VentWorkStatus.kNone,
                                                          dri_heat_level: HeatLevel = HeatLevel.Off,
                                                          pass_heat_level: HeatLevel = HeatLevel.Off,
                                                          timeout: Union[float, int] = 0.5):
        """
        #获取SeatService_server:GetSeatHeatVentStatus请求,并且回复对应的响应

        :param seats: 要获取座椅加热通风状态的座椅ID，列表类型
        :param work_sts: 主驾座椅加热状态，枚举值，取值范围:  kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param pass_work_sts: 副驾座椅加热状态，枚举值，取值范围:  kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param dri_heat_level: 主驾座椅加热等级，枚举值，取值范围:  Off = 0 Low = 1 Mid = 2 High = 3
        :param pass_heat_level: 副驾座椅加热等级，枚举值，取值范围:  Off = 0 Low = 1 Mid = 2 High = 3
        :param timeout: 监听超时时间，浮点型或整形
        :return:
        """
        pass

    def check_steerwheel_GetHeat_req_and_feedback_resp(self, heatlevel: HeatLevel, timeout: Union[float, int] = 0.5):
        """
        获取SteerWheelService_server:GetHeat请求的响应,并且回复对应的响应"

        :param heatlevel:
        :param timeout:
        :return:
        """
        pass

    def check_climate_GetRemotePowerStatus_req_and_feedback_resp(self, rem_pow_sts: RemClimateSts,
                                                                 timeout: Union[float, int] = 0.5):
        """
        获取ClimateControlService:GetRemotePowerStatus请求,并且回复对应的响应"

        :param rem_pow_sts: 远程空调状态 Off = 0 On = 1 SignalMissing = 251 SignalCounterFault = 252 SignalChecksumFault = 253 SignalE2EFault = 254 Invalid = 255
        :param timeout:
        :return:
        """
        pass

    def check_GetDefrostSts_req_and_feedback_resp(self, defrostmax: bool, climatedefrost: bool,
                                                  timeout: Union[float, int] = 0.5):
        """
        获取ClimateControlService:GetDefrostSts请求,并且回复对应的响应

        :param defrostmax: bool
        :param climatedefrost: bool
        :param timeout:
        :return:
        """
        pass

    def check_GetBatteryTemperatureInfo_req_and_feedback_resp(self, min_temp: float = -50, max_temp: float = 80,
                                                              average_temp: float = 0,
                                                              timeout: Union[float, int] = 0.5):
        """
        获取HighVoltageService:GetBatteryTemperatureInfo请求,并且回复对应的响应

        :param min_temp: 高压电池最大温度
        :param max_temp: 高压电池最小温度
        :param average_temp: 高压电池平均温度
        :param timeout:
        :return:
        """
        pass

    def check_GetChargingInfo_req_and_feedback_resp(self, charg_sts: ChargingSts = ChargingSts.Default,
                                                    plug_sts: PluggerSts = PluggerSts.Disconnected,
                                                    tar_soc: float = 0.0,
                                                    charg_complete_sts: bool = True,
                                                    book_charg_sts: BookChargeSts = BookChargeSts.Default,
                                                    is_charging_pre: bool = True, timeout: Union[float, int] = 0.5):
        """
        获取HighVoltageService:GetChargingInfo请求,并且回复对应的响应

        :param charg_sts: 充电状态 Default = 0 NoCharging = 1 ACCharging = 2 ACChargingEnd = 3 ChargingCmpl = 4 Heating = 5 Booking = 6 NoDischarging = 7 Discharging = 8 DischargingEnd = 9 DischargingCmpl = 10 Chargingfault = 11 DischargingFault = 12 ACChrgnFltChrgrSide = 14 DCCharging = 15 DCChrgnFltVehSide = 18 DCChrgnFltChrgrSideTempFlt = 19 DCChrgnFltChrgrSideConFlt = 20 DCChrgnFltChrgrSideHwFlt = 21 DCChrgnFltChrgrSideEmgyFlt = 22 DCChrgnFltChrgrSideComFlt = 23 SuperCharging = 24 ACChargingSuspend = 25 DCChargingEnd = 26 ACChrgnFltVehSide = 27 Boostcharging = 28 BoostchargingFlt = 29 WirelessCharging = 30
        :param plug_sts: 充电枪状态 Disconnected = 0 ConnectedWithoutPower = 1 PowerAvailableButNotActivated = 2 ConnectedWithPower = 3 Init = 4 Fault = 5
        :param tar_soc: 充电目标SOC
        :param charg_complete_sts:
        :param book_charg_sts: 高压电池充电完成状态 Default = 1 On = 1 Off = 2 Reserve = 3
        :param is_charging_pre: 充电准备中
        :param timeout:
        :return:
        """

    def check_GethvActiveSts_req_and_feedback_resp(self, hv_act_sts: HVActiveSts, timeout: Union[float, int] = 0.5):
        """
        获取HighVoltageService:GethvActiveSts请求,并且回复对应的响应

        :param hv_act_sts: 高压激活状态 枚举值 Open = 0 Close = 1 Keep = 2 Open_And_Req_Act_Dcha = 3
        :param timeout:
        :return:
        """

    @abstractmethod
    def pack_ua_status_args(self, ua_sts: UA_Sts, errorCode=0):
        """
        打包符合UA Status 格式定义的json字符串与event区别点在于status不带event_name

        :param ua_sts: 枚举类型 : class UA_Sts(BaseEnum): IDLE = 0 DOWNLOAD = 1 READY_TO_INSTALL = 2 INSTALLING = 3 UPDATE_FINISH = 4 ROLLING_BACK = 5 SYSTEM_ACTIVE = 6 ERROR = 7 ACTIVATING = 8 UPDATE_FAILED = 9
        :param errorCode: UA错误码
        :returns: UA Status json
        :raises keyError: None
        """
        pass

    @abstractmethod
    def send_method_response(self, partner_key: str, method_name: str, args: dict):
        """
        发送method的response请求

        :param partner_key: 类似KeyService_Server
        :param method_name: 请求接口名
        :param args:   请求参数
        :return:
        """
        pass

    @abstractmethod
    def send_response_to_req_start(self, partner_key: str, func):
        """
        开始回复client的requset调用, mock server端时使用

        :param partner_key: 类似KeyService_Server
        :param func: 函数名
        :return:
        """
        pass

    @abstractmethod
    def start_send_ua_response(self, domain_name: DOMAIN):
        """
        开始回复client的requset调用, mock UA server端时使用

        :param domain_name: 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3
        :return:
        """
        pass

    @abstractmethod
    def stop_send_ua_response(self, domain_name: DOMAIN):
        """
        停止回复client的requset调用, mock UA server端时使用

        :param domain_name: 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3
        :return:
        """
        pass

    @abstractmethod
    def update_ua_response(self, domain_name: DOMAIN, get_status_args):
        """
        更新回复client的requset调用, mock UA server端时使用

        :param domain_name: 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3
        :param get_status_args: 更新后的UA回复内容
        :return:
        """
        pass

    @abstractmethod
    def change_ua_event_and_getstatus(self, domain_name: DOMAIN, ua_sts: UA_Sts, errorCode=0):
        """
        同时更新某UA的event事件和get_status回复

        :param domain_name: 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3
        :param ua_sts: 枚举类型 UA_Sts: class UA_Sts(BaseEnum): IDLE = 0 DOWNLOAD = 1 READY_TO_INSTALL = 2 INSTALLING = 3 UPDATE_FINISH = 4 ROLLING_BACK = 5 SYSTEM_ACTIVE = 6 ERROR = 7 ACTIVATING = 8 UPDATE_FAILED = 9
        :param errorCode: UA错误码
        :return:
        """
        pass

    @abstractmethod
    def on_ua_start_download(self, partner_key, msg):
        """
        mock的UA server端收到 StartDownload 请求时,执行该方法上层无直接调用场景

        :return:
        """
        pass

    @abstractmethod
    def on_ua_get_status(self, partner_key, msg):
        """
        mock的UA server端收到 GetStatus 请求时,执行该方法,上层无直接调用场景

        :return:
        """
        pass

    @abstractmethod
    def on_ua_suspend_download(self, partner_key, msg):
        """
        mock的UA server端收到 SuspendDownload 请求时,执行该方法,上层无直接调用场景

        :return:
        """
        pass

    @abstractmethod
    def on_ua_resume_download(self, partner_key, msg):
        """
        mock的UA server端收到 ResumeDownload 请求时,执行该方法,上层无直接调用场景

        :return:
        """
        pass

    @abstractmethod
    def on_ua_cancel_download(self, partner_key, msg):
        """
        mock的UA server端收到 CancelDownload 请求时,执行该方法,上层无直接调用场景

        :return:
        """
        pass

    @abstractmethod
    def on_ua_pre_update(self, partner_key, msg):
        """
        mock的UA server端收到 PreUpdate 请求时,执行该方法,上层无直接调用场景

        :return:
        """
        pass

    @abstractmethod
    def on_ua_start_update(self, partner_key, msg):
        """
        mock的UA server端收到 StartUpdate 请求时,执行该方法,上层无直接调用场景

        :return:
        """
        pass

    @abstractmethod
    def on_ua_cancel_update(self, partner_key, msg):
        """
        mock的UA server端收到 CancelUpdate 请求时,执行该方法,上层无直接调用场景

        :return:
        """
        pass

    @abstractmethod
    def on_ua_rollback(self, partner_key, msg):
        """
        mock的UA server端收到 Rollback 请求时,执行该方法,上层无直接调用场景

        :return:
        """
        pass

    @abstractmethod
    def on_ua_activate(self, partner_key, msg):
        """
        mock的UA server端收到 Activate 请求时,执行该方法,上层无直接调用场景

        :return:
        """
        pass

    @abstractmethod
    def on_ua_finishupdate(self, partner_key, msg):
        """
        mock的UA server端收到 FinishUpdate 请求时,执行该方法,上层无直接调用场景

        :return:
        """
        pass

    @abstractmethod
    def till_ua_event_to(self, domain_name: DOMAIN, ua_event_field: UA_EVENT, target_status=None, timeout=60):
        """
        持续监控UA状态, 直至它回到目标值

        :param domain_name:  枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3
        :param ua_event_field:  枚举类型 UA_EVENT: class UA_EVENT(BaseEnum): Status = 0 DownloadStatus = 1 PreUpdateStatus = 2 UpdateStatus = 3 ErrorCode = 4
        :returns:
        :raises keyError:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_warning_light_list(self, name: str, state: str):
        """
        获取告警灯通知

        :param name: 告警名字；数据类型: str
        :param state: 告警状态；数据类型: str
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_warning_light_list(self, name: str, state: str):
        """
        获取警示灯列表信息

        :param name: 告警名字；数据类型: str
        :param state: 告警状态；数据类型: str
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_warning_light_list(self, name: str, state: str):
        """
        获取警示灯列表信息和事件通知

        :param name: 告警名字；数据类型: str
        :param state: 告警状态；数据类型: str
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_warning_info_list(self, name: str, info: str):
        """
        获取告警信息事件上报

        :param name: 告警名字；数据类型: str
        :param info: 告警信息；数据类型: str
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_warning_info_list(self, name: str, info: str):
        """
        获取警示信息列表

        :param name: 告警名字；数据类型: str
        :param info: 告警信息；数据类型: str
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_warning_info_list(self, name: str, info: str):
        """
        获取警示信息列表以及事件上报

        :param name: 告警名字；数据类型: str
        :param info: 告警信息；数据类型: str
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_seatbelt_sign_warning_light_list(self, name: str = "Seat Belt", state: str = ""):
        """
        通知及获取安全带指示灯告警状态

        :param name: 告警名字；数据类型: str
        :param state: 告警状态；数据类型: str
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_airbag_sign_warning_light_list(self, name: str = "Airbag", state: str = ""):
        """
        通知及获取安全气囊指示灯状态

        :param name: 告警名字；数据类型: str
        :param state: 告警状态；数据类型: str
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_seatbelt_warning_sts_list(self, name: str = "Driver Seat Belt Warning", state: str = ""):
        """
        获取及通知安全带告警信息

        :param name: 告警名字；数据类型: str
        :param state: 告警状态；数据类型: str
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_airbag_trouble_light_warning_sts(self, trouble_light_sts: TroubleLightSts, is_fault: bool, is_valid: bool):
        """
        获取安全气囊系统报警信息

        :param trouble_light_sts: 故障灯状态，枚举 LampOff = 0 Unknown = 1 LampFlash = 2 LampOn = 3
        :param is_fault: 是否为故障，布尔
        :param is_valid: 是否有效，布尔
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_airbag_trouble_light_warning_sts(self, trouble_light_sts: TroubleLightSts, is_fault: bool,
                                                     is_valid: bool):
        """
        获取安全气囊系统报警信息事件上报

        :param trouble_light_sts: 故障灯状态，枚举 LampOff = 0 Unknown = 1 LampFlash = 2 LampOn = 3
        :param is_fault: 是否为故障，布尔
        :param is_valid: 是否有效，布尔
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_airbag_trouble_light_warning_sts(self, trouble_light_sts: TroubleLightSts, is_fault: bool,
                                                             is_valid: bool):
        """
        获取安全气囊系统报警信息以及事件上报

        :param trouble_light_sts: 故障灯状态，枚举 LampOff = 0 Unknown = 1 LampFlash = 2 LampOn = 3
        :param is_fault: 是否为故障，布尔
        :param is_valid: 是否有效，布尔
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_pedestrian_protection_warning_sts(self, is_sys_fault: bool, is_impact_warn: bool, is_valid: bool):
        """
        获取行人保护告警状态

        :param is_sys_fault: 表示是否为系统故障，布尔
        :param is_impact_warn: 表示是否为碰撞报警，布尔
        :param is_valid: 表示是否有效，布尔
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_pedestrian_protection_warning_sts(self, is_sys_fault: bool, is_impact_warn: bool, is_valid: bool):
        """
        获取行人保护告警状态事件上报

        :param is_sys_fault: 表示是否为系统故障，布尔
        :param is_impact_warn: 表示是否为碰撞报警，布尔
        :param is_valid: 表示是否有效，布尔
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_pedestrian_protection_warning_sts(self, is_sys_fault: bool, is_impact_warn: bool,
                                                              is_valid: bool):
        """
        获取行人保护告警状态以及事件上报

        :param is_sys_fault: 表示是否为系统故障，布尔
        :param is_impact_warn: 表示是否为碰撞报警，布尔
        :param is_valid: 表示是否有效，布尔
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_vehicle_collision_warning_sts(self, roll_over_crash: bool = False, front_crash: bool = False,
                                          rear_crash: bool = False, left_crash: bool = False,
                                          right_crash: bool = False):
        """
        获取车辆碰撞状态

        :param roll_over_crash: 是否为翻滚，布尔
        :param front_crash: 是否为前碰撞，布尔
        :param rear_crash: 是否为后碰撞，布尔
        :param left_crash: 是否为左碰撞，布尔
        :param right_crash: 是否为右碰撞，布尔
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_vehicle_collision_warning_sts(self, roll_over_crash: bool = False, front_crash: bool = False,
                                            rear_crash: bool = False, left_crash: bool = False,
                                            right_crash: bool = False):
        """
        通知车辆碰撞状态改变事件上报

        :param roll_over_crash: 是否为翻滚，布尔
        :param front_crash: 是否为前碰撞，布尔
        :param rear_crash: 是否为后碰撞，布尔
        :param left_crash: 是否为左碰撞，布尔
        :param right_crash: 是否为右碰撞，布尔
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_vehicle_collision_warning_sts(self, roll_over_crash: bool = False,
                                                          front_crash: bool = False, rear_crash: bool = False,
                                                          left_crash: bool = False, right_crash: bool = False):
        """
        获取车辆碰撞状态以及改变事件上报

        :param roll_over_crash: 是否为翻滚，布尔
        :param front_crash: 是否为前碰撞，布尔
        :param rear_crash: 是否为后碰撞，布尔
        :param left_crash: 是否为左碰撞，布尔
        :param right_crash: 是否为右碰撞，布尔
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_light_control(self, type: LightType, zone: LightZone, mode: LightMode, brightness: int = 0,
                          color: dict = {"R": 0, "G": 0, "B": 0}):
        """
        灯控制

        :param type: 车灯类型,类型定义: LightType LightBrake = 0 LightEyebrow = 1 LightHazard = 2 LightDaytime = 3 LightFog = 4 LightHighBeam = 5 LightLowBeam = 6 LightOutLine = 7 LightReverse = 8 LightHeadLamp = 9 LightSteer = 10 LightPosition = 11 LightWelcome = 12 LightPixel = 13 LightDidrl = 14 LightLicense = 15 LightSteerMirror = 16 LightDoorAlarm = 17 LightCorner = 18 LightPuddle = 19 LightBlind = 21 LightReading = 22 LightBackground = 23 LightFoot = 24 LightSmartAmbient = 25 LightCourtesy = 26 LightTrunk = 27 LightArmRestBox = 28 LightRoof = 29 LightSide = 30 LightGlove = 31 LightOvertake = 32 LightSteerWheel = 33 LightGeneralAmbient = 35 LightAFS = 36 LightAHL = 37 LightPositionPattern = 38 kAILamp = 39 LightSystem = 100
        :param zone: 灯区域, 类型定义: LightZoneId LightZoneAllOrSingle = 0 LightZoneFrontLeft = 1 LightZoneFrontRight = 2 LightZoneRearLeft = 3 LightZoneRearRight = 4 ZoneMiddleRear = 5 LightZoneThreeRowLeft = 6 LightZoneThreeRowRight = 7 LightZoneMiddleThreeRow = 8 LightZoneFront = 9 LightZoneRear = 10 LightZoneThreeRow = 11 LightZoneLeft = 12 LightZoneRight = 13 LightZoneRing = 14 LightIpLeft = 15 LightIpRight = 16 LightTweeterLeft = 17 LightTweeterRight = 18 LightConsoleLeft = 19 LightConsoleRight = 20 leftY1Sts = 21 leftY2Sts = 22 leftY3Sts = 23 leftY4Sts = 24 rightY1Sts = 25 rightY2Sts = 26 rightY3Sts = 27 rightY4Sts = 28
        :param mode: 车灯模式,类型定义: LightMode NA = 255 Off =0 On = 1 Auto = 2 Flash =3 AdasStatus1 =4 AdasStatus2 =5 AdasStatus3 =6 AdasStatus4 =7 AdasStatus5 =8 AdasStatus6 =9 AdasStatus7 = 10 AdasStatus8 = 11 AdasStatus9 = 12 AdasStatus10 =13 AdasStatus11 = 14
        :param brightness: 灯的颜色，如果不修改灯的颜色, 默认0
        :param color: 灯光颜色,字典，默认 {"R": 0, "G": 0, "B": 0}
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_intr_light_mode(self, mode: LightMode = LightMode.Auto):
        """
        设置内灯模式，默认为Auto模式

        :param mode: 车灯模式,类型定义: LightMode NA = 255 Off =0 On = 1 Auto = 2 Flash =3 AdasStatus1 =4 AdasStatus2 =5 AdasStatus3 =6 AdasStatus4 =7 AdasStatus5 =8 AdasStatus6 =9 AdasStatus7 = 10 AdasStatus8 = 11 AdasStatus9 = 12 AdasStatus10 =13 AdasStatus11 = 14
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_control_ai_and_alm_light(self, type: LightType, zone: LightZone, pixel_data: list = [0],
                                     pixel_type: PixelType = PixelType.RgbBmp, brightness: int = 0,
                                     color: dict = {"R": 0, "G": 0, "B": 0}):
        """
        AI灯和氛围灯的控制

        :param type: 车灯类型,类型定义: LightType LightBrake = 0 LightEyebrow = 1 LightHazard = 2 LightDaytime = 3 LightFog = 4 LightHighBeam = 5 LightLowBeam = 6 LightOutLine = 7 LightReverse = 8 LightHeadLamp = 9 LightSteer = 10 LightPosition = 11 LightWelcome = 12 LightPixel = 13 LightDidrl = 14 LightLicense = 15 LightSteerMirror = 16 LightDoorAlarm = 17 LightCorner = 18 LightPuddle = 19 LightBlind = 21 LightReading = 22 LightBackground = 23 LightFoot = 24 LightSmartAmbient = 25 LightCourtesy = 26 LightTrunk = 27 LightArmRestBox = 28 LightRoof = 29 LightSide = 30 LightGlove = 31 LightOvertake = 32 LightSteerWheel = 33 LightGeneralAmbient = 35 LightAFS = 36 LightAHL = 37 LightPositionPattern = 38 kAILamp = 39 LightSystem = 100
        :param zone: 灯区域, 类型定义: LightZoneId LightZoneAllOrSingle = 0 LightZoneFrontLeft = 1 LightZoneFrontRight = 2 LightZoneRearLeft = 3 LightZoneRearRight = 4 ZoneMiddleRear = 5 LightZoneThreeRowLeft = 6 LightZoneThreeRowRight = 7 LightZoneMiddleThreeRow = 8 LightZoneFront = 9 LightZoneRear = 10 LightZoneThreeRow = 11 LightZoneLeft = 12 LightZoneRight = 13 LightZoneRing = 14 LightIpLeft = 15 LightIpRight = 16 LightTweeterLeft = 17 LightTweeterRight = 18 LightConsoleLeft = 19 LightConsoleRight = 20 leftY1Sts = 21 leftY2Sts = 22 leftY3Sts = 23 leftY4Sts = 24 rightY1Sts = 25 rightY2Sts = 26 rightY3Sts = 27 rightY4Sts = 28
        :param pixel_data: 灯光秀数据,类型定义: list
        :param pixel_type: 灯光秀数据类型,类型定义: PixelData
        :param brightness: 灯的颜色，如果不修改灯的颜色, 默认0
        :param color: 灯光颜色,字典，默认 {"R": 0, "G": 0, "B": 0}
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_alm_color_brightness(self, brightness: int = 0, color: dict = {"R": 255, "G": 0, "B": 0}):
        """
        设置氛围灯的颜色和亮度

        :param brightness: 灯的颜色，如果不修改灯的颜色, 默认0
        :param color: 灯光颜色,字典，默认 {"R": 0, "G": 0, "B": 0}
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_SeatOccupyStatus(self, seatid: list = [0, 1, 4, 5, 6], rawsensorstatus: list = [0, 0, 0, 0, 0],
                                occupiedstatus: list = [0, 0, 0, 0, 0]):
        """
        发送车辆占位信息SeatService:SeatOccupyStatus

        :param seatid: 座椅id, list列表类型, 元素取值范围(整形0~12), MarsOne只有5座(前排主副, 后排左中右0,1,4,5,6)
        :param rawsensorstatus: 座椅占位传感器状态, 列表类型, 元素取值范围0、1、2
        :param occupiedstatus: 座椅占位信息, 列表类型, 元素取值范围0、1、2
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_getEquipmentInfo_req(self, timeout: Union[float, int]):
        """
        使用SOA Partner监听TCAM是否发出获取充电桩信息请求HighVoltageService:getEquipmentInfo

        :param timeout: 监听最长时间，整形或者浮点型
        :return: 返回监听结果bool
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_getEquipmentInfo_req(self, max_current: float, equipment_types: list, actual_current: float):
        """
        使用SOA Partner响应TCAM发出获取充电桩信息请求HighVoltageService:getEquipmentInfo

        :param max_current: 最大充电电流，浮点型
        :param equipment_types: 充电桩类型, list列表类型, 元素取值范围(整型0~7)
        :param actual_current: 实际充电电流，浮点型
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_getEquipmentInfo_req_and_feedback_resp(self, max_current: float, equipment_types: list,
                                                     actual_current: float, timeout: Union[float, int] = 0.5):
        """
        使用SOA Partner监听TCAN是否发出获取充电桩信息请求HighVoltageService:getEquipmentInfo, 并返回响应

        :param max_current: 最大充电电流，浮点型
        :param equipment_types: 充电桩类型, list列表类型, 元素取值范围(整型0~7)
        :param actual_current: 实际充电电流，浮点型
        :return: 返回监听结果bool
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetCharging_req(self, req: bool, timeout: Union[float, int]):
        """
        使用SOA Partner监听TCAN是否发出设置充电HighVoltageService:SetCharging

        :param req: 开启充电与否bool
        :param timeout: 最大监听时间整型或者浮点型
        :return: 返回监听结果bool
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def set_tcam_rvc_common_preconditions(self):
        """
        使用SOA Partner设置RVC相关的通用前置条件,CarMode/UsageMode/FotaStatus/Gear/MaintenanceMode/SeatOccupyStatus/HVSOCInfo/VehicleTimeInfo

        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_BattMaintReqSts(self, battmaintreqsts: BattMaintReqSts):
        """
        使用SOA Partner设置RVC相关的通用前置条件,CarMode/UsageMode/FotaStatus/Gear/MaintenanceMode/ SeatOccupyStatus/HVSOCInfo/VehicleTimeInfo

        :param battmaintreqsts: 温度维持状态,枚举值:  Start = 0 Finish = 1
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def start_battery_heating_success_plan_a(self, mintemp: float):
        """
        高压电池极低温自保护集度私桩场景正常开启电池加热功能正向流程, 使用SOA Partner模拟BGM与TCAM进行交互

        :param mintemp: 高压电池最低温度浮点型
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def start_battery_heating_success_plan_b_b1(self, mintemp: float):
        """
        高压电池极低温自保护非插枪场景正常开启电池加热功能正向流程, 使用SOA Partner模拟BGM与TCAM进行交互

        :param mintemp: 高压电池最低温度浮点型
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def start_battery_heating_success_plan_b_b2(self, mintemp: float):
        """
        高压电池极低温自保护非集度桩插枪场景正常开启电池加热功能正向流程, 使用SOA Partner模拟BGM与TCAM进行交互

        :param mintemp: 高压电池最低温度浮点型
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def start_battery_heating_success_plan_b_b3(self, mintemp: float):
        """
        高压电池极低温自保护集度公桩插枪场景正常开启电池加热功能正向流程, 使用SOA Partner模拟BGM与TCAM进行交互

        :param mintemp: 高压电池最低温度浮点型
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_climate_heat_status_and_get_mintemp_and_get_charginfo(self, mintemp: float,
                                                                    plug_sts: PluggerSts = PluggerSts.ConnectedWithoutPower,
                                                                    charg_sts: ChargingSts = ChargingSts.NoCharging):
        """
        通过SOA监听climate请求并返回响应, 监听获取最低温度请求并返回响应, 监听获取充电信息请求并返回响应

        :param mintemp: 高压电池最低温度浮点型
        :param plug_sts: 充电枪连接状态, 枚举型, 取值范围:  Disconnected = 0 ConnectedWithoutPower = 1 PowerAvailableButNotActivated = 2 ConnectedWithPower = 3 Init = 4 Fault = 5
        :param charg_sts: 充电状态, 枚举型, 取值范围: Default = 0 NoCharging = 1 ACCharging = 2 ACChargingEnd = 3 ChargingCmpl = 4 Heating = 5 Booking = 6 NoDischarging = 7 Discharging = 8 DischargingEnd = 9 DischargingCmpl = 10 Chargingfault = 11 DischargingFault = 12 ACChrgnFltChrgrSide = 14 DCCharging = 15 DCChrgnFltVehSide = 18 DCChrgnFltChrgrSideTempFlt = 19 DCChrgnFltChrgrSideConFlt = 20 DCChrgnFltChrgrSideHwFlt = 21 DCChrgnFltChrgrSideEmgyFlt = 22 DCChrgnFltChrgrSideComFlt = 23 SuperCharging = 24 ACChargingSuspend = 25 DCChargingEnd = 26 ACChrgnFltVehSide = 27 Boostcharging = 28 BoostchargingFlt = 29 WirelessCharging = 30
        :return:
            """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_climate_heat_status_and_get_mintemp(self, mintemp: float):
        """
        通过SOA监听climate请求并返回响应, 监听获取最低温度请求并返回响应, 监听获取充电信息请求并返回响应

        :param mintemp: 高压电池最低温度浮点型
        :return: 
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_steer_wheel_sts(self, stalk_id: StalkId, press_type: PressType, is_valid: bool):
        """
        通知转向开关状态

        :param stalk_id:  方向盘拨杆Id StalkRight = 0 StalkLeft = 1 All = 2
        :param press_type: 拨杆拨动类型 kNone = 0 LightPress = 1 FullPress = 2 Error = 3 E2eCheckError = 4
        :param is_valid: 转向开关状态 bool
        :return: 
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_climate_defrost_mode(self, mode: bool):
        """
        SOA设置打开/关闭强力除霜模式

        :param mode: 开关状态 bool
        :return: 
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetRemoteClimateSwitchToHV_req(self, isOn: bool = True, keep_time: int = 30,
                                             timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程上高压请求:ClimateControlService:SetRemoteClimateSwitchToHV

        :param isOn: 远程高压请求参数, 布尔型
        :param keep_time: 请求上高压时长, 单位min, 整形, 取值范围 0~59
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetRemoteClimateSwitchToHVDelay_req(self, extendtime: int = 30, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程延长上高压请求:ClimateControlService:SetRemoteClimateSwitchToHVDelay

        :param extendtime: 延长上高压时间, 整型, 取值范围0~59
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_RemoteClimateHVStatus(self, remote_climate_Status: RemoteClimateStatus):
        """
        通过SOA Partner发送远程上高压状态事件:ClimateControlService:RemoteClimateHVStatus

        :param remote_climate_Status: 远程空调状态, 枚举型 Off = 0 On = 1 Invalid = 255
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_RemoteOn_req(self, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程开启空调请求:ClimateControlService:RemoteOn

        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_RemoteOff_req(self, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程关闭空调请求:ClimateControlService:RemoteOff

        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetTemperature_req(self, zoneid: ClimateZoneId, temp: float, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程设置空调温度请求:ClimateControlService:SetTemperature

        :param zoneid: 空调区域ID, 枚举型，取值范围:  AllZone = 0 FirstRow = 1 SecondRow = 2 FirstRowLeft = 3 FirstRowRight = 4 SecondRowLeft = 5 SecondRowMiddle = 6 SecondRowRight = 7 FirstRowLeftLeft = 8 FirstRowLeftRight = 9 FirstRowRightLeft = 10 FirstRowRightRight = 11 SecondRowLeftLeft = 12 SecondRowLeftRight =13 SecondRowRightLeft = 14 SecondRowRightRight = 15
        :param temp: 目标温度, 浮点型
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    @abstractmethod
    def check_SetTemperature_and_remote_req(self, zoneid: ClimateZoneId, temp: float, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程设置空调温度请求:ClimateControlService:SetTemperature 与 RemoteOn

        :param zoneid: 空调区域ID, 枚举型，取值范围:  AllZone = 0 FirstRow = 1 SecondRow = 2 FirstRowLeft = 3 FirstRowRight = 4 SecondRowLeft = 5 SecondRowMiddle = 6 SecondRowRight = 7 FirstRowLeftLeft = 8 FirstRowLeftRight = 9 FirstRowRightLeft = 10 FirstRowRightRight = 11 SecondRowLeftLeft = 12 SecondRowLeftRight =13 SecondRowRightLeft = 14 SecondRowRightRight = 15
        :param temp: 目标温度, 浮点型
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetTemperatureAndOn_req(self, zoneid: ClimateZoneId, temp: float, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程设置空调温度并关联空调启动请求:ClimateControlService:SetTemperatureAndOn

        :param zoneid: 空调区域ID, 枚举型，取值范围:  AllZone = 0 FirstRow = 1 SecondRow = 2 FirstRowLeft = 3 FirstRowRight = 4 SecondRowLeft = 5 SecondRowMiddle = 6 SecondRowRight = 7 FirstRowLeftLeft = 8 FirstRowLeftRight = 9 FirstRowRightLeft = 10 FirstRowRightRight = 11 SecondRowLeftLeft = 12 SecondRowLeftRight =13 SecondRowRightLeft = 14 SecondRowRightRight = 15
        :param temp: 目标温度, 浮点型
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_Off_req(self, zoneid: ClimateZoneId, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程关闭本地空调请求:ClimateControlService:Off

        :param zoneid: 空调区域ID, 枚举型，取值范围: AllZone = 0 FirstRow = 1 SecondRow = 2 FirstRowLeft = 3 FirstRowRight = 4 SecondRowLeft = 5 SecondRowMiddle = 6 SecondRowRight = 7 FirstRowLeftLeft = 8 FirstRowLeftRight = 9 FirstRowRightLeft = 10 FirstRowRightRight = 11 SecondRowLeftLeft = 12 SecondRowLeftRight =13 SecondRowRightLeft = 14 SecondRowRightRight = 15
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_RemotePowerStatus(self, is_active: bool = True, start_resp: bool = True):
        """
        通过SOA Partner发送远程上高压状态事件:ClimateControlService:RemotePowerStatus

        :param is_active: 远程空调激活状态, 布尔型
        :param start_resp: 远程启动空调的反馈, 布尔型
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetClimateSystemStatus_req(self, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程关闭本地空调请求:ClimateControlService:GetClimateSystemStatus

        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetClimateSystemStatus(self, ac_status: bool, temp_dri: float = 0, temp_pass: float = 0,
                                           temp_sec: float = 0, temp_sec_left: float = 0,
                                           temp_sec_right: float = 0, wind_speed_firrow: WindSpeed = WindSpeed.kOff,
                                           wind_speed_secrow: WindSpeed = WindSpeed.kOff,
                                           airmodedri_windmode: WindMode = WindMode.WindAuto,
                                           airmodedri_auto: bool = True,
                                           airmodepass_windmode: WindMode = WindMode.WindAuto,
                                           airmodepass_auto: bool = True,
                                           airmodesecrow_windmode: WindMode = WindMode.WindAuto,
                                           airmodesecrow_auto: bool = True, ison: bool = True,
                                           first_row_power_status: bool = True, second_row_power_status: bool = True,
                                           cooling_heating_status: CoolingHeatingStatus = CoolingHeatingStatus.kNone):
        """
        通过SOA Partner模拟BGM返回响应:ClimateControlService:GetClimateSystemStatus

        :param ac_status: 空调状态, 布尔 
        :param temp_dri: 主驾设置温度, 浮点型
        :param temp_pass: 副驾驶设置温度, 浮点型
        :param temp_sec: 二排设置温度, 浮点型
        :param temp_sec_left: 二排左侧设置温度, 浮点型
        :param temp_sec_right: 二排右侧设置温度, 浮点型
        :param wind_speed_firrow: 主驾驶设置风量, 枚举型，取值范围:  WindFoot = 0 WindFace = 1 WindDefrst = 2 WindFootDefrst = 3 WindFootFace = 4 WindFaceDefrst = 5 WindFootFaceDefrst = 6 WindAuto = 7
        :param wind_speed_secrow: 二排设置风量, 枚举型
        :param airmodedri_windmode: 主驾驶设置吹风模式, 枚举型, 取值范围: WindFoot = 0 WindFace = 1 WindDefrst = 2 WindFootDefrst = 3 WindFootFace = 4 WindFaceDefrst = 5 WindFootFaceDefrst = 6 WindAuto = 7
        :param airmodedri_auto: 吹风模式是否为auto模式, 布尔型
        :param airmodepass_windmode: 副驾驶设置吹风模式, 枚举型
        :param airmodepass_auto: 吹风模式是否为auto模式, 布尔型
        :param airmodesecrow_windmode: 副驾驶设置吹风模式, 枚举型
        :param airmodesecrow_auto: 吹风模式是否为auto模式, 布尔型
        :param ison: 座舱清洁状态, 布尔型
        :param first_row_power_status: 前排电源开关状态, 布尔型
        :param second_row_power_status: 后排电源开关状态, 布尔型
        :param cooling_heating_status: 空调制冷制热状态, 枚举值, 取值范围:  kNone = 0 Cooling = 1 Heating = 2 CoolingAndHeating = 3 Invalid = 4
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_ClimateSystemStatus(self, ac_status: bool, temp_dri: float = 0, temp_pass: float = 0,
                                   temp_sec: float = 0, temp_sec_left: float = 0,
                                   temp_sec_right: float = 0, wind_speed_firrow: WindSpeed = WindSpeed.kOff,
                                   wind_speed_secrow: WindSpeed = WindSpeed.kOff,
                                   airmodedri_windmode: WindMode = WindMode.WindAuto, airmodedri_auto: bool = True,
                                   airmodepass_windmode: WindMode = WindMode.WindAuto,
                                   airmodepass_auto: bool = True, airmodesecrow_windmode: WindMode = WindMode.WindAuto,
                                   airmodesecrow_auto: bool = True, ison: bool = True,
                                   first_row_power_status: bool = True, second_row_power_status: bool = True,
                                   cooling_heating_status: CoolingHeatingStatus = CoolingHeatingStatus.kNone):
        """
        通过SOA Partner模拟BGM发送:ClimateControlService:GetClimateSystemStatus

        :param ac_status: 空调状态, 布尔 
        :param temp_dri: 主驾设置温度, 浮点型
        :param temp_pass: 副驾驶设置温度, 浮点型
        :param temp_sec: 二排设置温度, 浮点型
        :param temp_sec_left: 二排左侧设置温度, 浮点型
        :param temp_sec_right: 二排右侧设置温度, 浮点型
        :param wind_speed_firrow: 主驾驶设置风量, 枚举型，取值范围:  WindFoot = 0 WindFace = 1 WindDefrst = 2 WindFootDefrst = 3 WindFootFace = 4 WindFaceDefrst = 5 WindFootFaceDefrst = 6 WindAuto = 7
        :param wind_speed_secrow: 二排设置风量, 枚举型
        :param airmodedri_windmode: 主驾驶设置吹风模式, 枚举型, 取值范围: WindFoot = 0 WindFace = 1 WindDefrst = 2 WindFootDefrst = 3 WindFootFace = 4 WindFaceDefrst = 5 WindFootFaceDefrst = 6 WindAuto = 7
        :param airmodedri_auto: 吹风模式是否为auto模式, 布尔型
        :param airmodepass_windmode: 副驾驶设置吹风模式, 枚举型
        :param airmodepass_auto: 吹风模式是否为auto模式, 布尔型
        :param airmodesecrow_windmode: 副驾驶设置吹风模式, 枚举型
        :param airmodesecrow_auto: 吹风模式是否为auto模式, 布尔型
        :param ison: 座舱清洁状态, 布尔型
        :param first_row_power_status: 前排电源开关状态, 布尔型
        :param second_row_power_status: 后排电源开关状态, 布尔型
        :param cooling_heating_status: 空调制冷制热状态, 枚举值, 取值范围:  kNone = 0 Cooling = 1 Heating = 2 CoolingAndHeating = 3 Invalid = 4
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_ClimateFault(self, fault_id: FaultId = FaultId.OK, fault_msg: str = "OK"):
        """
        通过SOA Partner模拟BGM发送事件信息:ClimateControlService:ClimateFault.faults

        :param fault_id: 故障ID, 枚举值, 取值范围:  OK = 0 FaultOutletError = 1 FaultExternalTempSensorError = 2 FaultInternalTempSensorError = 3 FaultOutletEnergyLimit = 4 FaultAQSSensorError = 5 FaultCoolantLow = 6 FaultBatteryLow = 7 FaultCoolantLowAndBatteryLow = 8 FaultTemperatureLow = 9 FaultTemperatureHigh = 10 FaultClimateError = 11 FaultHighVoltageError = 12 FaultActivationLimited = 13
        :param fault_msg: 故障描述信息, 字符串
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_SetClimateTempMaintainSts(self, id: str = "SetClimateTempMaintainSts", data: str = "0"):
        """
        通过SOA Partner模拟CDC发送温度维持事件通知:InteractiveService:SetClimateTempMaintainSts

        :param id: 温度维持id, 字符串 "SetClimateTempMaintainSts"
        :param data: 温度维持data, 字符串, "0"表示OFF，"1"表示ON
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_LockActTriggerSource(self, trigger_source_id: TriggerSourceId.RemoteKey):
        """
        通过SOA Partner模拟BGM发送解闭锁动作触发源事件通知:CentralLockService:LockActTriggerSource.TriggerSourceId

        :param trigger_source_id: 中控锁触发原因, 枚举值, 取值范围: NoTriggerSource = 0 RemoteKey = 1 KeyLessPassive = 2 InteriorSwitches = 3 SpeedLocking = 4 Relocking = 5 SlamLocking = 6 Telematices = 7 CrashUnlock = 8 Approach = 9 OutsideOthers = 10 InsideOthers = 11 NFC = 12
        :param data: 温度维持data, 字符串
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_NotifyCentralLockSysInfo(self, sts: LockStatus = LockStatus.Undef,
                                     trigger_id: TriggerSourceId = TriggerSourceId.RemoteKey, update_eve: bool = False):
        """
        通过SOA Partner模拟BGM发送解闭锁动作触发源事件通知:CentralLockService:NotifyCentralLockSysInfo

        :param sts: 锁状态信息, 枚举值, 取值范围: Undef = 0 Unlocked = 1 FourDoorLockedTailUnlocked = 2 AllLocked = 3
        :param trigger_id: 中控锁触发原因, 枚举值, 取值范围: NoTriggerSource = 0 RemoteKey = 1 KeyLessPassive = 2 InteriorSwitches = 3 SpeedLocking = 4 Relocking = 5 SlamLocking = 6 Telematices = 7 CrashUnlock = 8 Approach = 9 OutsideOthers = 10 InsideOthers = 11 NFC = 12
        :param update_eve: 是否发生解闭锁事件, 布尔型
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_NotifyACDefrostSts(self, defrost_max: bool = False, climate_defrost: bool = False):
        """
        通过SOA Partner模拟BGM发送除霜状态事件通知:ClimateControlService:NotifyACDefrostSts

        :param defrost_max: 最大除霜状态, 布尔型
        :param climate_defrost: 除霜工作状态, 布尔型
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_ShieldWindowService_GetHeat_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner模拟BGM发送除霜状态事件通知:ShieldWindowService:GetHeat

        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_ShieldWindowService_GetHeat_req(self, id: ShieldWindowId = ShieldWindowId.ShieldWindowFront,
                                                    status: HeatStatus = HeatStatus.HeatStatusAutoOn):
        """
        通过SOA Partner发送ShieldWindowService:GetHeat请求的响应

        :param id: 挡风玻璃id, 枚举值, 取值范围: ShieldWindowAll = 0 ShieldWindowFront = 1 ShieldWindowRear = 2
        :param status: 加热状态, 枚举值, 取值范围: HeatStatusOff = 0 HeatStatusOn = 1 HeatStatusAutoOn = 2
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_ShieldWindowService_GetHeat_req_and_feedback_resp(self,
                                                                id: ShieldWindowId = ShieldWindowId.ShieldWindowFront,
                                                                status: HeatStatus = HeatStatus.HeatStatusAutoOn,
                                                                timeout: Union[float, int] = 1):
        """
        获取ShieldWindowService:GetHeat请求的响应,并且回复对应的响应

        :param id: 挡风玻璃id, 枚举值, 取值范围: ShieldWindowAll = 0 ShieldWindowFront = 1 ShieldWindowRear = 2
        :param status: 加热状态, 枚举值, 取值范围: HeatStatusOff = 0 HeatStatusOn = 1 HeatStatusAutoOn = 2
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_OuterRearViewService_GetHeat_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出OuterRearViewService:GetHeat请求

        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_OuterRearViewService_GetHeat_req(self, id: ViewId = ViewId.RearViewAll, ison: bool = True):
        """
        通过SOA Partner发送OuterRearViewService:GetHeat请求的响应

        :param id: 外后视镜id, 枚举值, 取值范围:  RearViewRight = 0 RearViewLeft = 1 RearViewAll = 2
        :param ison: 加热开启状态, 布尔型
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_OuterRearViewService_GetHeat_req_and_feedback_resp(self, id: ViewId = ViewId.RearViewAll,
                                                                 ison: bool = True, timeout: Union[float, int] = 1):
        """
        获取OuterRearViewService:GetHeat请求的响应,并且回复对应的响应

        :param id: 外后视镜id, 枚举值, 取值范围:  RearViewRight = 0 RearViewLeft = 1 RearViewAll = 2
        :param ison: 加热开启状态, 布尔型
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_ShieldWindowService_HeatStatus(self, heat_status: HeatStatus.HeatStatusAutoOn,
                                              id: ShieldWindowId = ShieldWindowId.ShieldWindowAll):
        """
        通过SOA Partner发送后窗加热状态事件:ShieldWindowService:HeatStatus

        :param id: 党风玻璃id, 枚举值, 取值范围:  ShieldWindowAll = 0 ShieldWindowFront = 1 ShieldWindowRear = 2
        :param heat_status: 加热状态, 枚举值, 取值范围: HeatStatusOff = 0 HeatStatusOn = 1 HeatStatusAutoOn = 2
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_OuterRearViewService_HeatStatus(self, id: ViewId = ViewId.RearViewAll, status: bool = False):
        """
        通过SOA Partner发送外后视镜加热状态事件:OuterRearViewService:HeatStatus

        :param id: 外后视镜id, 枚举值, 取值范围: RearViewRight = 0 RearViewLeft = 1 RearViewAll = 2
        :param status: 对应后视镜的电加热除霜状态, 布尔值
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_hvActiveSts(self, sts: HVActiveSts = HVActiveSts.Close):
        """
        通过SOA Partner发送高压继电器闭合状态事件:HighVoltageService:hvActiveSts

        :param sts: 高压继电器闭合状态, 枚举值, 取值范围: RearViewRight = 0 RearViewLeft = 1 RearViewAll = 2
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetFastDefrostMode_req(self, on: bool = True, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ClimateControlService:SetFastDefrostMode请求

        :param sts: 空调控制和状态, 布尔型
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_ShieldWindowService_SetHeat_req(self, id: ShieldWindowId = ShieldWindowId.ShieldWindowAll,
                                              heat_status: HeatStatus = HeatStatus.HeatStatusAutoOn,
                                              timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ShieldWindowService:SetHeat请求

        :param id: 挡风玻璃id, 枚举值, 取值范围: ShieldWindowAll = 0 ShieldWindowFront = 1 ShieldWindowRear = 2
        :param heat_status: 加热状态, 枚举值, 取值范围: HeatStatusOff = 0 HeatStatusOn = 1 HeatStatusAutoOn = 2
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SeatService_SetHeatingLevel_req(self, id: SeatId = SeatId.All, info: int = 1,
                                              source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出SeatService:SetHeatingLevel请求

        :param id: 座椅id, 枚举值, 取值范围: FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param info: 类型信息, 整形
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :param source: 请求来源, 枚举值, 取值范围: 0, 1, 2
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_SeatHeatVentStatus(self, id: SeatId = SeatId.FrontLeft, heat_level: int = 0, heat_time: int = 15,
                                  heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                  vent_level: int = 0, vent_time: int = 15,
                                  vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):
        """
        通过SOA Partner发送座椅加热通风状态事件:SeatService:SeatHeatVentStatus

        :param id: 座椅id, 枚举值, 取值范围: FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param heat_level: 座椅的加热等级, 整形
        :param heat_time: 座椅的加热时间, 整形, 单位min
        :param heat_work_sts: 加热通风状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param vent_level: 通风等级, 整形
        :param vent_time: 通风时间, 整形, 单位min
        :param vent_work_sts: 加热通风状态, 枚举值
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SteerWheelService_SetHeat_req(self, heat_level: HeatLevel = HeatLevel.Off,
                                            source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出SteerWheelService:SetHeat请求

        :param heat_level: 方向盘加热等级, 枚举值, 取值范围: Off = 0 Low = 1 Mid = 2 High = 3
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :param source: 请求来源, 枚举值, 取值范围: 0, 1, 2
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_SteerWheelService_Heat(self, heat_level: HeatLevel = HeatLevel.Off):
        """
        通过SOA Partner发送方向盘加热状态事件:SteerWheelService:Heat

        :param heat_level: 方向盘加热等级, 枚举值, 取值范围: Off = 0 Low = 1 Mid = 2 High = 3
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_SteerHeatAvailiable(self, availiable: SteerHeatAvailiable = SteerHeatAvailiable.On):
        """
        通过SOA Partner监听TCAM是否发出SteerWheelService:SetHeat请求

        :param availiable: 方向盘加热可用状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 Funcational_Limit = 4 Energy_Limit = 5
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetSteerHeatAvailiable_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出SteerWheelService:GetSteerHeatAvailiable请求

        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetSteerHeatAvailiable_req(self, availiable: SteerHeatAvailiable = SteerHeatAvailiable.On):
        """
        通过SOA Partner发送SteerWheelService:GetSteerHeatAvailiable请求的响应

        :param availiable: 方向盘加热可用状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 Funcational_Limit = 4 Energy_Limit = 5 :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetSteerHeatAvailiable_req_and_feedback_resp(self,
                                                           availiable: SteerHeatAvailiable = SteerHeatAvailiable.On,
                                                           timeout: Union[float, int] = 1):
        """
        获取SteerWheelService:GetSteerHeatAvailiable请求,并且回复对应的响应

        :param availiable: 方向盘加热可用状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 Funcational_Limit = 4 Energy_Limit = 5
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_PedalService_GetStatus_req(self, pedalid: PedalId = PedalId.PedalBraker, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出PedalService:GetStatus请求

        :param pedalid: 踏板id, 枚举值, 取值范围: PedalAcc = 0 PedalBraker = 1 PedalAll = 2
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_PedalService_GetStatus_req(self, pedalid: PedalId = PedalId.PedalBraker,
                                               sts: PressedStatus = PressedStatus.PedalNA):
        """
        通过SOA Partner发送PedalService:GetStatus请求的响应

        :param pedalid: 踏板id, 枚举值, 取值范围: PedalAcc = 0 PedalBraker = 1 PedalAll = 2
        :param sts: 踏板状态, 枚举值, 取值范围: PedalReleased = 0 PedalPressed = 1 PedalNA = 2
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_PedalService_GetStatus_req_and_feedback_resp(self, pedalid: PedalId = PedalId.PedalBraker,
                                                           sts: PressedStatus = PressedStatus.PedalNA,
                                                           timeout: Union[float, int] = 1):
        """
        获取PedalService:GetStatus请求,并且回复对应的响应

        :param pedalid: 踏板id, 枚举值, 取值范围: PedalAcc = 0 PedalBraker = 1 PedalAll = 2
        :param sts: 踏板状态, 枚举值, 取值范围: PedalReleased = 0 PedalPressed = 1 PedalNA = 2
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_NotifyRemoteAuthStartSts_event(self, is_valid: bool = True, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:NotifyRemoteAuthStartSts事件通知

        :param is_valid: 远程授权启动状态, 布尔型
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_reset_config_sts(self):
        """
        设置随车项恢复出厂设置

        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_climate_sys_sts(self, ac_sts: Union[bool, None] = None,
                            temp_dri: Union[float, int, None] = None, temp_pass: Union[float, int, None] = None,
                            temp_sec_row: Union[float, int, None] = None,
                            wind_spd_first_row: Union[WindSpeed, None] = None,
                            wind_spd_sec_row: Union[WindSpeed, None] = None,
                            air_mode_dri: Union[AirWindMode, None] = None, is_wind_mode_auto_dri: [bool, None] = None,
                            air_mode_pass: Union[AirWindMode, None] = None,
                            is_wind_mode_auto_pass: [bool, None] = None,
                            air_mode_sec_row: Union[AirWindMode, None] = None,
                            is_wind_mode_auto_sec_row: [bool, None] = None,
                            power_sts_first_row: [bool, None] = None, power_sts_sec_row: [bool, None] = None,
                            time_wait: Union[float, int, None] = 0, timeout: Union[float, int, None] = 1):
        """
        获取空调系统状态

        :param ac_sts:  A/C状态
        :param temp_dri: 驾驶位温度
        :param temp_pass: 副驾驶位温度
        :param temp_sec_row: 后排温度
        :param wind_spd_first_row: 第一排风速 kOff = 0 kLvlMan1 = 1 kLvlMan2 = 2 kLvlMan3 = 3 kLvlMan4 = 4 kLvlMan5 = 5 kLvlMan6 = 6 kLvlMan7 = 7 kLvlMan8 = 8 kLvlMan9 = 9 kLvlAutoMinusMinus = 10 kLvlAutoMinus = 11 kLvlAutoNormal = 12 kLvlAutoPlus = 13 kLvlAutoPlusPlus = 14
        :param wind_spd_sec_row: 第二排风速
        :param air_mode_dri: 驾驶位吹风模式 Foot = 0 Face = 1 Defrst = 2 FootDefrst = 3 FootFace = 4 FaceDefrst = 5 FootFaceDefrst = 6 Auto = 7
        :param is_wind_mode_auto_dri: 驾驶位是否位自动吹风模式 bool
        :param air_mode_pass: 副驾驶位吹风模式
        :param is_wind_mode_auto_pass: fu驾驶位是否位自动吹风模式 bool
        :param air_mode_sec_row: 第二排吹风模式
        :param is_wind_mode_auto_sec_row: 第二排是否位自动吹风模式 bool
        :param power_sts_first_row: 第一排空调开启状态 bool
        :param power_sts_sec_row: 第二排空调开启状态 bool
        :param time_wait: 发送操作之后的延时
        :param timeout: 等待响应的时间
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_climate_vent_sts(self, zone: ClimateZone, on: isOn):
        """
        设置电动出风口开启关闭状态为

        :param zone: 控制区域 AllZone = 0 FirstRow = 1 SecondRow = 2 FirstRowLeft = 3 FirstRowRight = 4 SecondRowLeft = 5 SecondRowMiddle = 6 SecondRowRight = 7 FirstRowLeftLeft = 8 FirstRowLeftRight = 9 FirstRowRightLeft = 10 FirstRowRightRight = 11 SecondRowLeftLeft = 12 SecondRowLeftRight = 13 SecondRowRightLeft = 14 SecondRowRightRight = 15
        :param on: 开关状态 Off = False On = True
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_climate_windmode_sts(self, zone: ClimateZone, mode: AirWindMode):
        """
        设置空调吹风模式

        :param zone: 控制区域 AllZone = 0 FirstRow = 1 SecondRow = 2 FirstRowLeft = 3 FirstRowRight = 4 SecondRowLeft = 5 SecondRowMiddle = 6 SecondRowRight = 7 FirstRowLeftLeft = 8 FirstRowLeftRight = 9 FirstRowRightLeft = 10 FirstRowRightRight = 11 SecondRowLeftLeft = 12 SecondRowLeftRight = 13 SecondRowRightLeft = 14 SecondRowRightRight = 15
        :param mode: 空调吹风模式 Foot = 0 Face = 1 Defrst = 2 FootDefrst = 3 FootFace = 4 FaceDefrst = 5 FootFaceDefrst = 6 Auto = 7
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_climate_temperature_sts(self, zone: ClimateZone, value: Union[float, int]):
        """
        设置空调温度（主/副/后排且联动空调开启)

        :param zone: AllZone = 0 FirstRow = 1 SecondRow = 2 FirstRowLeft = 3 FirstRowRight = 4 SecondRowLeft = 5 SecondRowMiddle = 6 SecondRowRight = 7 FirstRowLeftLeft = 8 FirstRowLeftRight = 9 FirstRowRightLeft = 10 FirstRowRightRight = 11 SecondRowLeftLeft = 12 SecondRowLeftRight = 13 SecondRowRightLeft = 14 SecondRowRightRight = 15
        :param value: 设置的温度值
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_climate_temperature(self, zone: ClimateZone, value: Union[float, int]):
        """
        设置空调温度

        :param zone: AllZone = 0 FirstRow = 1 SecondRow = 2 FirstRowLeft = 3 FirstRowRight = 4 SecondRowLeft = 5 SecondRowMiddle = 6 SecondRowRight = 7 FirstRowLeftLeft = 8 FirstRowLeftRight = 9 FirstRowRightLeft = 10 FirstRowRightRight = 11 SecondRowLeftLeft = 12 SecondRowLeftRight = 13 SecondRowRightLeft = 14 SecondRowRightRight = 15
        :param value: 设置的温度值
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_auto_close_door_by_drive_gear(self, time_wait: Union[float, int] = 0):
        """
        设置D档自动关门

        :param time_wait: 命令执行后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_key_config_info(self, key_type: KeyConfigType, value: int, time_wait: Union[float, int] = 0):
        """
        设置钥匙配置信息

        :param key_type: 配置类型:  AutoLockOnLeave = 0 //离车自动闭锁 AutoLockOnApproach = 1 //接近自动解锁 LightOnApproache = 2  //迎宾模式，平台能力暂无此配置 DoorAutoOpenOnUnlock = 3 //车外解锁，自动开启电动门 WindowAutoCloseOnLock = 4 //锁车自动关窗 SetPEKeySearchDedicateZone = 5  //设置PE解锁时对应寻钥匙的区域
        :param value: 设置的值 int
        :param time_wait: 命令执行后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_diag_connect_sts(self, con_sts: int, con_act: int):
        """
        SOA服务设置诊断连接状态

        :param con_sts:
        :param con_act:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_no_wti_event(self, s2s_interface_name: str):
        """
        检查对应的WTI 服务接口上报

        :param s2s_interface_name: 服务接口名字
        :return:
        """

    @abstractmethod
    def get_fota_NotifyAppointTime(self, master_notifyappointtime_event_field: MASTER_NotifyAppointTime_EVENT):
        """
        检查FOTA Master服务NotifyAppointTime event的内容
        
        :param master_notifyappointtime_event_field: 枚举类型 MASTER_NotifyAppointTime_EVENT: class MASTER_NotifyAppointTime_EVENT(BaseEnum): TaskId = 0 Type = 1 AppointmentTime = 2
        :return: FOTA Master NotifyAppointTime event的内容
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_horn_active_sts(self, sts: HornStatus):
        """
        获取喇叭的状态

        :param sts: 喇叭的状态
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_horn_sts(self, sts: HornStatus):
        """
        获取喇叭的状态改变通知

        :param sts: 喇叭的状态
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_horn_sts(self, on_time: Union[float, int], off_time: Union[float, int], times: int):
        """
        设置喇叭模式

        :param on_time: 喇叭On的持续时间,单位秒
        :param on_time: 喇叭Off的持续时间,单位秒
        :param on_time: 喇叭执行次数
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com   #o_fan.liu
    @abstractmethod
    def hmi_set_seat_heat_level(self, pos: SeatId, level: HeatVentiLvl, sourceId:SourceId): 
        """
        设置座椅加热等级

        :param pos: 设置座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :param sourceId: 加热源     Idle = 0    HMI = 1    Remote = 2
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_seat_vent_level(self, pos: SeatId, level: HeatVentiLvl, sourceId:SourceId):
        """
        设置座椅通风等级

        :param pos: 设置座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :param sourceId: 加热源     Idle = 0    HMI = 1    Remote = 2
        :return:
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def notify_DoorService_OpenCloseStatus(self, id: DoorId = DoorId.kDoorFrontLeft, isopen: bool = False):
        """
        通过SOA Partner发出四门的状态DoorService::OpenCloseStatus

        :param id: 四门 kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param isopen: 四门开关状态，布尔型
        :return: 
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def notify_DoorService_Status(self, id: DoorId = DoorId.kDoorFrontLeft, status: DoorStatus = DoorStatus.kClosed):
        """
        通过SOA Partner发出电动门的状态DoorService::Status

        :param id: 四门 kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param status: 四门运动状态 kOpened = 0 # 全开 kClosing = 1 # 关闭中 kClosed = 2 # 全关 kLocked = 3 # 未使用 kUnlocked = 4 # 未使用 kOpening = 5 # 开启中 kHover = 6  # 悬停 kNA = 7  # 未知 kClosingBreak = 8 # 关闭过程中减速 kOpeningBreak = 9 # 开启过程中减速 kHalfClosed = 10 # 半锁状态(门锁卡在一半且门开度很小) kInvalid = 65535 # (Default)
        :return: 
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def notify_LockStatus(self, lock_sts: LockSts):
        """
        通过SOA Partner发出解闭锁的状态CentralLockService::LockStatus.sts

        :param lock_sts: 整车锁状态 kUndef = 0 //Default kUnlocked = 1 //解锁 kFourDoorLockedTailUnlocked = 2 //四门上锁但尾门解锁 kAllLocked = 3 //四门上锁且尾门上锁
        :return: 
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def notify_TailGateService_Status(self, tailgate_sts: TailGateSts = TailGateSts.kClosed):
        """
        通过SOA Partner发出尾门的状态TailGateService::Status

        :param tailgate_sts: 尾门运动状态 kOpened = 0 kClosing = 1 kClosed = 2 kOpening = 3 kHover = 4 kNA = 5 kClosingBreak = 6 //关闭过程中减速 kOpeningBreak = 7 //开启过程中减速 kHalfClosed = 8 //半锁状态(门锁卡在一半且门开度很小) kInvalid = 65535 //(Default)
        :return: 
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_SetDoorCloseLock_req(self, cmd: LockCmd = LockCmd.Lock, source: LockReqSource = LockReqSource.Talematics,
                                   find_key_type: FindKeyType = FindKeyType.OutsideKey,
                                   timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出CentralLockService::SetDoorCloseLock请求

        :param cmd: 解闭锁指令，枚举型，取值范围: UnLock = 0 Lock = 1 AllDoorCloseAndLock = 2 LockCompleteArm = 3
        :param source: 解闭锁请求源，枚举型，取值范围: Ble_Rke = 0 Talematics = 1 Hmi = 2 APA = 3
        :param find_key_type: 寻钥匙类型，枚举型，取值范围: NotReq = 0 OutsideKey = 1 InsideKey = 2 OutsideAndInsideKey = 3
        :param timeout: 监听请求超时时间，浮点型或者整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def response_to_SetDoorCloseLock_req(self):
        """
        使用SOA Partner模拟CentralLockService::SetDoorCloseLock请求的响应

        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetDoorCloseLock_req_and_feedback_resp(self, lock_cmd: LockCmd,
                                                     source: LockReqSource = LockReqSource.Talematics,
                                                     find_key_type: Union[FindKeyType, None] = None,
                                                     timeout: Union[float, int] = 0.5):
        prompt_info = f"---------->获取CentralLockService::SetDoorCloseLock请求的响应,并且回复对应的响应"
        """
        通过SOA Partner监听TCAM是否发出CentralLockService::SetDoorCloseLock请求
        
        :param lock_cmd: 解闭锁指令，枚举型，取值范围: UnLock = 0 Lock = 1 AllDoorCloseAndLock = 2 LockCompleteArm = 3
        :param source: 解闭锁请求源，枚举型，取值范围: Ble_Rke = 0 Talematics = 1 Hmi = 2 APA = 3
        :param find_key_type: 寻钥匙类型，枚举型，取值范围: NotReq = 0 OutsideKey = 1 InsideKey = 2 OutsideAndInsideKey = 3
        :param timeout: 监听请求超时时间，浮点型或者整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_SetTailGate_req(self, cmd: TailGateCmd = TailGateCmd.Open, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出尾门TailGateService::SetTailGate请求

        :param cmd: 尾门开启关闭请求，枚举型，取值范围: Open = 0 Close = 1 Stop = 2
        :param timeout: 监听请求超时时间，浮点型或者整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def response_to_SetTailGate_req(self):
        """
        通过SOA Partner发送尾门TailGateService::SetTailGate.Cmd请求的响应

        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetTailGate_req_and_feedback_resp(self, cmd: TailGateCmd = TailGateCmd.Open,
                                                timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出尾门TailGateService::SetTailGate请求,并返回响应

        :param cmd: 尾门开启关闭请求，枚举型，取值范围: Open = 0 Close = 1 Stop = 2
        :param timeout: 监听请求超时时间，浮点型或者整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_TailGateService_SetPosition_req(self, pos: int, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出尾门TailGateService::SetPosition请求

        :param pos: 请求尾门开启位置，整形
        :param timeout: 监听请求超时时间，浮点型或者整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_TailGateService_OpenCloseStatus(self, isopen: bool = False):
        """
        通过SOA Partner发出尾门的状态事件通知TailGateService:OpenCloseStatus

        :param isopen: 尾门打开状态，布尔型
        :return:
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def response_to_TailGateService_SetPosition_req(self):
        """
        通过SOA Partner发送TailGateService::SetPosition请求的响应

        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_TailGateService_SetPosition_req_and_feedback_resp(self, pos: int, timeout: Union[float, int] = 1):
        """
        获取尾门翘起TailGateService::SetPosition请求,并且回复对应的响应

        :param pos: 请求尾门开启位置，整形
        :param timeout: 监听请求超时时间，浮点型或者整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def get_TailGate_GetStatus_sts(self, tailgate_sts: TailGateSts):
        """
        通过SOA Partner发送获取尾门状态TailGateService::GetStatus

        :param tailgate_sts: 尾门运动状态 kOpened = 0 kClosing = 1 kClosed = 2 kOpening = 3 kHover = 4 kNA = 5 kClosingBreak = 6 //关闭过程中减速 kOpeningBreak = 7 //开启过程中减速 kHalfClosed = 8 //半锁状态(门锁卡在一半且门开度很小) kInvalid = 65535 //(Default)
        :return: 返回监听结果bool
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_SetCarLocalTraceRequest_req(self, carloctr_req: CarLocalTraceReq = CarLocalTraceReq.kHornLiReq,
                                          timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出远程寻车KeyService::SetCarLocalTraceRequest请求

        :param carloctr_req: 寻车请求类型，枚举型，取值范围:  kNoReq = 0    # 无请求 kHornReq = 1  # 喇叭请求 kLiReq = 2     # 灯光请求 kHornLiReq = 3  # 喇叭和灯光同时请求
        :param timeout: 监听请求超时时间，浮点型或者整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def response_to_SetCarLocalTraceRequest_req(self):
        """
        通过SOA Partner发送寻车KeyService::SetCarLocalTraceRequest请求的响应

        :return:
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_SetCarLocalTraceRequest_req_and_feedback_resp(self,
                                                            carloctr_req: CarLocalTraceReq = CarLocalTraceReq.kHornLiReq,
                                                            timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出远程寻车KeyService::SetCarLocalTraceRequest请求,并返回响应

        :param carloctr_req: 寻车请求类型，枚举型，取值范围:  kNoReq = 0    # 无请求 kHornReq = 1  # 喇叭请求 kLiReq = 2     # 灯光请求 kHornLiReq = 3  # 喇叭和灯光同时请求
        :param timeout: 监听请求超时时间，浮点型或者整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def notify_NotifyCarLoctrActvnSts(self,
                                      cartrace_sts: CarLocalTraceActiveStatus = CarLocalTraceActiveStatus.kSuccess):
        """
        通过SOA Partner发出寻车功能执行状态KeyService::NotifyCarLoctrActvnSts.sts

        :param cartrace_sts: 远程寻车功能执行状态 kIdle = 0  // 未寻(Default) kSuccess = 1 // 寻车成功 kFail = 2  // 寻车失败 kInvalid =3 // 无效
        :return: 
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def notify_NotifyTurnLampStatus(self, priority: int, turnlamp_mode: TurnLampMode = TurnLampMode.kHazard):
        """
        通过SOA Partner发出转向灯的状态LightService::NotifyTurnLampStatus状态事件

        :param turnlamp_mode: 转向灯模式，枚举型，取值范围:  kStop = 0     //转向灯关闭 kLeft = 1      //左转向灯开启 kRight = 2    //右转向灯开启 kHazard = 3     //危险报警灯开启
        :param priority: 转向控制优先级标识，整形
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_SetSpecificWindowPosition_req(self, *position_info: dict, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出远程车窗WindowAppService::SetSpecificWindowPosition请求

        :param position_info: 车窗开度信息，类型为dict，{"id": WindowId, "position": int}
        :param timeout: 监听请求超时时间，浮点型或者整形
        :return: 返回监听结果，布尔型
        :return:
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def response_to_SetSpecificWindowPosition_req(self):
        """
        通过SOA Partner发送WindowAppService::SetSpecificWindowPosition请求的响应

        :return:
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_SetSpecificWindowPosition_req_and_feedback_resp(self, *position_info: dict,
                                                              timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出远程车窗WindowAppService::SetSpecificWindowPosition请求

        :param position_info: 车窗开度信息，类型为dict，{"id": WindowId, "position": int}
        :param timeout: 监听请求超时时间，浮点型或者整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def notify_WindowService_NotifyPosition_sts(self, win_id: WindowId, position: int):
        """
        通过SOA Partner发出车窗执行状态WindowService::NotifyPosition

        :param win_id: 车窗ID kWindowFrontLeft = 0 kWindowFrontRight = 1 kWindowRearLeft = 2 kWindowRearRight = 3 kWindowAll = 4
        :return:
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_ChargeLidService_Open_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出充电口盖开ChargeLidService::Open()请求

        :param timeout: 监听超时时间，整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def response_to_ChargeLidService_Open_req(self):
        """
        通过SOA Partner发送ChargeLidService:Open()请求的响应

        :return:
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_ChargeLidService_Open_req_and_feedback_resp(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出充电口盖开ChargeLidService::Open()请求

        :param timeout: 监听超时时间，整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_ChargeLidService_Close_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出充电口盖关ChargeLidService:Close()请求

        :param timeout: 监听超时时间，整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def response_to_ChargeLidService_Close_req(self):
        """
        通过SOA Partner发送充电口盖关ChargeLidService::Close()请求的响应

        :return:
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_ChargeLidService_Close_req_and_feedback_resp(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出充电口盖关ChargeLidService:Close()请求

        :param timeout: 监听超时时间，整形
        :return: 返回监听结果，布尔型
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def notify_ChargeLidService_status(self, chargelid_sts: ChargeLidSts):
        """
        通过SOA Partner发出充电口盖的状态ChargeLidService::Status

        :param chargelid_sts: 充电口盖的状态 kOpened = 0  # 口盖运动行程在6%~100%均表示打开 kClosing = 1 # 仅预留 kClosed = 2  # 口盖运动行程在0%~5%均表示关闭 kLocked = 3  # 仅预留 kUnlocked = 4  # 仅预留 kOpening = 5 # 仅预留 kHover = 6  # 仅预留 kNA = 7
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def send_Alldoor_OpenCloseStatus_close(self):
        """
        通过 DoorService_server:OpenCloseStatus 发送门开关状态为所有门关闭

        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def send_Alldoor_Status_close(self):
        """
        通过 DoorService_server:Status 发送电动门运动状态为关闭

        :return: 
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_seat_massg_level(self, pos: SeatId, is_on: bool, type: MassType, intensity: MassIntensity):
        """
        设置座椅按摩开关

        :param pos: 设置座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param is_on: True False
        :param type: Type1 = 0 Type2 = 1 Type3 = 2 Type4 = 3 Type5 = 4 Type6 = 5 Type7 = 6 Type8 = 7
        :param intensity: Low = 0 Normal = 1 High = 2 Off = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_seat_adjust_direction(self, pos: SeatId, part: SeatPart, direction: AdjustDirection):
        """
        调节座椅

        :param pos: FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param part: Seat = 0 SeatBack = 1 SeatLegrest = 2 SeatLumbar = 3
        :param direction: Forward = 0 Left = 1 Up = 2 Backward = 3 Right = 4 Down = 5
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_seat_massg_sts(self, pos: SeatId, is_on: bool, type: MassType, intensity: MassIntensity):
        """
        获取座椅按摩状态

        :param pos: 设置座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param is_on: True False
        :param type: Type1 = 0 Type2 = 1 Type3 = 2 Type4 = 3 Type5 = 4 Type6 = 5 Type7 = 6 Type8 = 7
        :param intensity: Low = 0 Normal = 1 High = 2 Off = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_seat_massg_sts(self, pos: SeatId, is_on: bool, type: MassType, intensity: MassIntensity):
        """
        Check 座椅按摩事件上报

        :param pos: 设置座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param is_on: True False
        :param type: Type1 = 0 Type2 = 1 Type3 = 2 Type4 = 3 Type5 = 4 Type6 = 5 Type7 = 6 Type8 = 7
        :param intensity: Low = 0 Normal = 1 High = 2 Off = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_seat_heat_level(self, pos: SeatId, level: HeatVentiLvl):
        """
        获取座椅加热等级

        :param pos: 设置座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_seat_venti_level(self, pos: SeatId, level: HeatVentiLvl):
        """
        获取座椅通风等级

        :param pos: 设置座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_seat_position_info(self, pos: SeatId, back_angle: Union[int, float], long_pos: Union[int, float],
                               vertical_pos: Union[int, float], legrest_vertical_pos: Union[int, float]):
        """
        获取座椅相关信息

        :param pos: 座椅位置
        :param back_angle: 座椅角度
        :param long_pos: 座椅前后位置
        :param vertical_pos: 座椅高度位置
        :param legrest_vertical_pos: 座椅腿托/坐垫高度位置
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_seat_position_info(self, pos: SeatId, back_angle: Union[int, float], long_pos: Union[int, float],
                                       vertical_pos: Union[int, float], legrest_vertical_pos: Union[int, float]):
        """
        check座椅相关信息通知

        :param pos: 座椅位置
        :param back_angle: 座椅角度
        :param long_pos: 座椅前后位置
        :param vertical_pos: 座椅高度位置
        :param legrest_vertical_pos: 座椅腿托/坐垫高度位置
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_rear_view_unfold(self, view_pos: ViewId, is_auto: bool):
        """
        通过 SteerWheelService_client::Unfold 展开后视镜状态

        :param view_pos: RearViewRight = 0 RearViewLeft = 1 RearViewAll = 2
        :param is_auto: boot
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_rear_view_fold(self, view_pos: ViewId, is_auto: bool):
        """
        通过 SteerWheelService_client::Fold 折叠后视镜状态

        :param view_pos: RearViewRight = 0 RearViewLeft = 1 RearViewAll = 2
        :param is_auto: boot
        :return:
        """

    @abstractmethod
    def get_fota_NotifyAppointTime(self, master_notifyappointtime_event_field: MASTER_NotifyAppointTime_EVENT):
        """
        检查FOTA Master服务NotifyAppointTime event的内容
        
        :param master_notifyappointtime_event_field: 枚举类型 MASTER_NotifyAppointTime_EVENT: class MASTER_NotifyAppointTime_EVENT(BaseEnum): TaskId = 0 Type = 1 AppointmentTime = 2
        :return: FOTA Master NotifyAppointTime event的内容
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_ChargingInfo(self, charg_sts: ChargingSts = ChargingSts.Default,
                            plug_sts: PluggerSts = PluggerSts.Disconnected, tar_soc: float = 0.0,
                            charg_complete_sts: bool = True, acdc_type: ACDCType = ACDCType.kDefault,
                            book_charg_sts: BookChargeSts = BookChargeSts.Default,
                            is_charging_pre: bool = True, is_charging: bool = True,isConnect:bool = True):
        """
        通过SOA Partner发送HighVoltageService:ChargingInfo事件通知

        :param charg_sts: 充电状态 Default = 0 NoCharging = 1 ACCharging = 2 ACChargingEnd = 3 ChargingCmpl = 4 Heating = 5 Booking = 6 NoDischarging = 7 Discharging = 8 DischargingEnd = 9 DischargingCmpl = 10 Chargingfault = 11 DischargingFault = 12 ACChrgnFltChrgrSide = 14 DCCharging = 15 DCChrgnFltVehSide = 18 DCChrgnFltChrgrSideTempFlt = 19 DCChrgnFltChrgrSideConFlt = 20 DCChrgnFltChrgrSideHwFlt = 21 DCChrgnFltChrgrSideEmgyFlt = 22 DCChrgnFltChrgrSideComFlt = 23 SuperCharging = 24 ACChargingSuspend = 25 DCChargingEnd = 26 ACChrgnFltVehSide = 27 Boostcharging = 28 BoostchargingFlt = 29 WirelessCharging = 30
        :param plug_sts: 充电枪状态 Disconnected = 0 ConnectedWithoutPower = 1 PowerAvailableButNotActivated = 2 ConnectedWithPower = 3 Init = 4 Fault = 5
        :param tar_soc: 充电目标SOC
        :param charg_complete_sts:
        :param book_charg_sts: 压电池充电完成状态 Default = 1 On = 1 Off = 2 Reserve = 3
        :param is_charging_pre: 充电准备中
        :param is_charging: 是否正在充电，布尔型
        :param acdc_type (ACDCType, optional): 充电桩类型. 默认为ACDCType.kDefault.
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetChargeSoc_req(self, soc: float = 80, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出设置充电SOC请求HighVoltageService:SetChargeSoc

        :param soc: 设置目标充电soc, 浮点型, 取值范围0~100, 精度0.1
        :param timeout: 监听超时时间，浮点型或者整形
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_SetChargeSoc_req(self):
        """
        通过SOA Partner发送设置充电SOC请求HighVoltageService:SetChargeSoc的响应

        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetChargeSoc_req_and_feedback_resp(self, soc: float = 80, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出设置充电SOC请求HighVoltageService:SetChargeSoc

        :param soc: 设置目标充电soc, 浮点型, 取值范围0~100, 精度0.1
        :param timeout: 监听超时时间，浮点型或者整形
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_fragrance_sts(self, channel: FragChannel, ratio: int, level: FragLevel,
                              wait_time: Union[float, int] = 0):
        """
        通过SOA ClimateControlService_client:SetFragranceType/SetFragranceLevel 设置香氛信息"

        :param channel: 设置的香氛通道（香氛类型）
        :param ratio: 设置的香氛比例
        :param level: 设置的香氛等级
        :param wait_time: 操作之后的等待时间
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_break_ice_active_sts(self, door_pos: DoorId, sts: ActiveStatus):
        """
        获取破冰激活状态

        :param door_pos: 门的位置 kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param sts: 破冰激活状态 Active  = 0 Level1 = 1 Invalid = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_break_ice_active_sts(self, door_pos: DoorId, sts: ActiveStatus):
        """
        获取破冰激活状态改变通知

        :param door_pos: 门的位置 kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param sts: 破冰激活状态 Active  = 0 Level1 = 1 Invalid = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_break_ice_active_sts(self, door_pos: DoorId, sts: ActiveStatus):
        """
        电动门:通知和获取破冰状态

        :param door_pos: 门的位置 kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param sts: 破冰激活状态 Active  = 0 Level1 = 1 Invalid = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def cancel_auto_close_door_by_gear_driving(self, time_wait: Union[float, int] = 0):
        """
        取消D档自动关门
        :param time_wait: 延时时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_auto_close_door_by_gear_driving(self, act_sts: isOn = isOn.Off):
        """
        通知挂挡自动关门

        :param act_sts: 取消的激活状态
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_auto_close_door_by_gear_driving(self, act_sts: isOn = isOn.Off):
        """
        获取挂挡自动关门

        :param act_sts: 取消的激活状态
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_auto_close_door_by_gear_driving(self, act_sts: isOn = isOn.Off):
        """
        通知和获取D档自动关门状态

        :param act_sts: 取消的激活状态
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_door_open_angle_sts(self, door_pos: DoorId, angle: int):
        """
        获取门开启角度

        :param door_pos: kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param angle: 开启的角度
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_door_open_angle_sts(self, door_pos: DoorId, angle: int):
        """
        获取门开启角度事件通知

        :param door_pos: kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param angle: 开启的角度
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_door_open_angle_sts(self, door_pos: DoorId, angle: int):
        """
        通知和获取门开启角度

        :param door_pos: kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param angle: 开启的角度
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_door_switch_sts(self, door_pos: DoorId, door_side: DoorSide, sts: SwitchSts):
        """
        获取门内外开关状态

        :param door_pos: kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param door_side: Inside = 0 Outside = 1
        :param sts: Unknow = 0 Pressed = 1 NotPressed = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_door_switch_sts(self, door_pos: DoorId, door_side: DoorSide, sts: SwitchSts):
        """
        获取门内外开关状态事件通知

        :param door_pos: kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param door_side: Inside = 0 Outside = 1
        :param sts: Unknow = 0 Pressed = 1 NotPressed = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_door_switch_sts(self, door_pos: DoorId, door_side: DoorSide, sts: SwitchSts):
        """
        通知及获取门按键状态

        :param door_pos:
        :param door_side:
        :param sts:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_door_opener_sts(self, door_pos: DoorId, sts: DoorOpenSts,  scene: VehicleInsideOutside= VehicleInsideOutside.VehicleInSide):
        """
        设置四门的动作请求开/关/停
        :param door_pos: kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param sts: 侧门动作请求状态 Open = 0 Close = 1 Stop = 2
        :param scene: 开门方式::Outside/inSide默认车内语音
        :return:
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetOpenCloseStatus_req(self, door_id: list = [0, 1, 2, 3], timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出请求DoorService:GetOpenCloseStatus

        :param door_id: 四门ID，列表类型
        :param timeout: 监听超时时间，浮点型或者整型
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetOpenCloseStatus_req(self,
                                           open_close_status: dict = {"0": False, "1": False, "2": False, "3": False}):
        """
        通过SOA Partner发送DoorService:GetOpenCloseStatus请求的响应

        :param open_close_status: 四门开关状态，字典类型
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetOpenCloseStatus_req_and_feedback_resp(self,
                                                       open_close_status: dict = {"0": False, "1": False, "2": False,
                                                                                  "3": False},
                                                       door_id: list = [0, 1, 2, 3], timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出请求DoorService:GetOpenCloseStatus，并返回响应"

        :param door_id: 四门ID，列表类型
        :param open_close_status: 四门开关状态，字典类型
        :param timeout: 监听超时时间，浮点型或者整型
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_TailGateService_GetStatus_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出请求TailGateService:GetStatus

        :param timeout: 监听超时时间，浮点型或者整型
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_TailGateService_GetStatus_req(self, status: TailGateSts = TailGateSts.kClosed):
        """
        通过SOA Partner发送TailGateService:GetStatus请求的响应

        :param status: 尾门状态，枚举型，取值范围:  kOpened = 0 kClosing = 1 kClosed = 2 kOpening = 3 kHover = 4 kNA = 5 kClosingBreak = 6 kOpeningBreak = 7 kHalfClosed = 8 kInvalid = 65535
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_TailGateService_GetStatus_req_and_feedback_resp(self, status: TailGateSts = TailGateSts.kClosed,
                                                              timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出请求TailGateService:GetStatus，并返回响应

        :param status: 尾门状态，枚举型，取值范围:  kOpened = 0 kClosing = 1 kClosed = 2 kOpening = 3 kHover = 4 kNA = 5 kClosingBreak = 6 kOpeningBreak = 7 kHalfClosed = 8 kInvalid = 65535
        :param timeout: 监听超时时间，浮点型或者整型
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetLockStatus_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出请求CentralLockService:GetLockStatus

        :param timeout: 监听超时时间，浮点型或者整型
        :return: 返回监听结果，布尔
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetLockStatus_req(self, lock_status: LockStatus = LockStatus.AllLocked):
        """
        通过SOA Partner发送CentralLockService:GetLockStatus请求的响应

        :param lock_status: 中控锁状态，枚举型，取值范围:  Undef = 0 Unlocked = 1 FourDoorLockedTailUnlocked = 2 AllLocked = 3
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetLockStatus_req_and_feedback_resp(self, lock_status: LockStatus = LockStatus.AllLocked,
                                                  timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出请求CentralLockService:GetLockStatus,并返回响应

        :param lock_status: 中控锁状态，枚举型，取值范围:  Undef = 0 Unlocked = 1 FourDoorLockedTailUnlocked = 2 AllLocked = 3
        :param timeout: 监听超时时间，浮点型或者整型
        :return: 返回监听结果，布尔
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetOccupied_req(self, seats: list = [12], timeout: Union[float, int] = 1):
        """
        过SOA Partner监听TCAM是否发出请求SeatService:GetOccupied

        :param seats: 要检查的座椅ID列表，列表类型
        :param timeout: 监听超时时间，浮点型或者整型
        :return: 返回监听结果，布尔
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetOccupied_req(self, resp_seats: list = [0, 1, 4, 5, 6],
                                    resp_rawsensorstatus: list = [0, 0, 0, 0, 0],
                                    resp_status: list = [0, 0, 0, 0, 0]):
        """
        通过SOA Partner发送SeatService:GetOccupied请求的响应

        :param seatid: 座椅id, list列表类型, 元素取值范围(整形0~12), MarsOne只有5座(前排主副, 后排左中右0,1,4,5,6)
        :param rawsensorstatus: 座椅占位传感器状态, 列表类型, 元素取值范围0、1、2
        :param occupiedstatus: 座椅占位信息, 列表类型, 元素取值范围0、1、2
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetOccupied_req_and_feedback_resp(self, seats: list = [12], resp_seats: list = [0, 1, 4, 5, 6],
                                                resp_rawsensorstatus: list = [0, 0, 0, 0, 0],
                                                resp_occupiedstatus: list = [0, 0, 0, 0, 0],
                                                timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出请求SeatService:GetOccupied,并返回响应

        :param seats: 要检查的座椅ID列表，列表类型
        :param timeout: 监听超时时间，浮点型或者整型
        :param seatid: 座椅id, list列表类型, 元素取值范围(整形0~12), MarsOne只有5座(前排主副, 后排左中右0,1,4,5,6)
        :param rawsensorstatus: 座椅占位传感器状态, 列表类型, 元素取值范围0、1、2
        :param occupiedstatus: 座椅占位信息, 列表类型, 元素取值范围0、1、2
        :return: 返回监听结果，布尔
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_BatteryTemperatureInfo(self, min_temp: float = -50, max_temp: float = 80,
                                      average_temp: float = 0):
        """
        通过SOA Partner发送HighVoltageService:BatteryTemperatureInfo事件通知

        :param min_temp: 电池最低温度，浮点型
        :param max_temp: 电池最高温度，浮点型
        :param average_temp: 电池平均温度，浮点型
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_key_config_info(self, key_type: KeyConfigType, value: int, time_wait: Union[float, int] = 0):
        """
        通过SOA Partner发送 KeyService_client:SetConfigInfo 设置钥匙配置信息

        :param key_type: 钥匙类型 AutoLockOnLeave = 0 AutoLockOnApproach = 1 LightOnApproache = 2 DoorAutoOpenOnUnlock = 3 WindowAutoCloseOnLock = 4 SetPEKeySearchDedicateZone = 5
        :param value: 设置的值
        :param time_wait: 执行操作之后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_diag_connect_sts(self, con_sts: int, con_act: int):
        """
        通过SOA Partner发送  InterCommService_client_BGM_InterCommService: SetDiagnosticConnectStatus 设置诊断连接状态和激活状态

        :param con_sts: 诊断连接状态 int
        :param con_act: 激活状态 int
        :return:
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_ChargingInfo_v13(self, charg_sts: ChargingSts = ChargingSts.Default,
                                plug_sts: PluggerSts = PluggerSts.Disconnected, tar_soc: float = 0.0,
                                charg_complete_sts: bool = True,
                                book_charg_sts: BookChargeSts = BookChargeSts.Default,
                                is_charging_pre: bool = True):
        """
        通过SOA Partner发送HighVoltageService:ChargingInfo事件通知

        :param charg_sts: 充电状态 Default = 0 NoCharging = 1 ACCharging = 2 ACChargingEnd = 3 ChargingCmpl = 4 Heating = 5 Booking = 6 NoDischarging = 7 Discharging = 8 DischargingEnd = 9 DischargingCmpl = 10 Chargingfault = 11 DischargingFault = 12 ACChrgnFltChrgrSide = 14 DCCharging = 15 DCChrgnFltVehSide = 18 DCChrgnFltChrgrSideTempFlt = 19 DCChrgnFltChrgrSideConFlt = 20 DCChrgnFltChrgrSideHwFlt = 21 DCChrgnFltChrgrSideEmgyFlt = 22 DCChrgnFltChrgrSideComFlt = 23 SuperCharging = 24 ACChargingSuspend = 25 DCChargingEnd = 26 ACChrgnFltVehSide = 27 Boostcharging = 28 BoostchargingFlt = 29 WirelessCharging = 30
        :param plug_sts: 充电枪状态 Disconnected = 0 ConnectedWithoutPower = 1 PowerAvailableButNotActivated = 2 ConnectedWithPower = 3 Init = 4 Fault = 5
        :param tar_soc: 充电目标SOC
        :param charg_complete_sts:
        :param book_charg_sts: 高压电池充电完成状态 Default = 1 On = 1 Off = 2 Reserve = 3
        :param is_charging_pre: 充电准备中
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_tailwing_mode(self, mode: TailWindMode):
        """
        获取并通知尾翼工作模式事件通知

        :param mode: 尾翼工作模式
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_tailwing_mode(self, mode: TailWindMode):
        """
        获取并通知尾翼工作模式

        :param mode: 尾翼工作模式
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_tailwing_mode(self, mode: TailWindMode):
        """
        获取并通知尾翼工作模式并且获取事件上报

        :param mode: 尾翼工作模式
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_climate_angle_sts(self, pos: ClimateZone, side: OutletSide, hori_ang: int, ver_ang: int):
        """
        通过SOA Partner发送 ClimateControlService_client:SetOutletAngle 设置空调{pos.name}区域电动出风口{side.name}出风水平角度{hori_ang},垂直角度为{ver_ang}

        :param pos: 空调区域位置
        :param side: 左右控制
        :param hori_ang: 出风水平角度
        :param ver_ang: 垂直角度
        :return:
        """

    @abstractmethod
    def check_event_period(self, partner_key: str, event_name: str, target_period: Union[float, int],
                           epsilon: float) -> bool:
        """
        检查某service的event事件发送周期
        
        :param partner_key: service 唯一 id
        :param event_name: event name
        :param target_period: 期望的周期
        :param epsilon: ±偏差值
        :returns: bool
        :raises keyError: None
        """

    @abstractmethod
    def check_ua_event_period(self, domain_name: DOMAIN, target_period: Union[float, int], epsilon: float):
        """
        检查某UA的Status event事件发送周期
        
        :param 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3
        :param target_period: 期望的周期
        :param epsilon: ±偏差值
        :returns: bool
        :raises keyError: None
        """

    @abstractmethod
    def send_SetNetResidentSts_req(self, is_5G: bool):
        """
        通过SOA Partner发送SetNetResidentSts请求

        :param is_5G: bool
        :return: 无
        """
        pass

    @abstractmethod
    def send_Get5GNetSts_req_and_ck_resp(self, sa_sts: SA_sts):
        """
        通过SOA Partner发送GetSwitch5GNet请求，并校验获取5G状态的结果

        :param sa_sts: 蜂窝网络5G状态 枚举 On = 1   (5G网络打开) Off = 2  (LTE网络)
        :return:
        """
        pass

    @abstractmethod
    def send_SetCellularNetSts_req(self, is_open: bool):
        """
        通过SOA Partner发送SetCellularNetSts请求

        :param is_open: bool
        :return: 无
        """
        pass

    @abstractmethod
    def send_GetNetSts_req_and_ck_resp(self, apnsts: ApnSts):
        """
        通过SOA Partner发送SetCellularNetSts请求，并校验获取apn4状态的结果

        :param is_open: APN4开关状态 枚举 available = 0 unavailable = 1
        :return: 无
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def remote_climate_open_susccess_when_inactive(self, temp: float = 22):
        """
        通过SOA Partner模拟远程空调在inactive模式正常开启成功

        :param temp: 请求开启温度值，浮点型
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def remote_climate_check_tcam_request(self, temp: float = 22):
        """
        通过SOA Partner检查TCAM是否发出远程开启空调请求

        :param temp: 请求开启温度值，浮点型
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def remote_lock_unlock_success_when_inactive(self, lock_status=LockStatus.Unlocked, lock_cmd=LockCmd.Lock,
                                                 source=LockReqSource.Talematics, find_key_type=FindKeyType.NoReq):
        """
        通过SOA Partner模拟BGM与TCAM交互成功解闭锁场景

        :param lock_status: 锁状态，枚举型，取值范围:  Undef = 0 Unlocked = 1 FourDoorLockedTailUnlocked = 2 AllLocked = 3
        :param lock_cmd: 解闭锁指令类型。枚举值，取值范围:  UnLock = 0 Lock = 1 AllDoorCloseAndLock = 2 LockCompleteArm = 3
        :param source: 解闭锁源类型，枚举值，取值范围:  Ble_Rke = 0 Talematics = 1 Hmi = 2 APA = 3
        :param find_key_type: 寻钥匙类型，枚举型，取值范围:  NoReq = 0 OutsideKey = 1 InsideKey = 2 OutsideAndInsideKey = 3
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_ClimateService_Off_req(self, zone_id: ClimateZoneId = ClimateZoneId.FirstRowLeft, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ClimateService:Off

        :param zone_id: 请求关闭空调区域，枚举型，取值范围:  AllZone = 0 FirstRow = 1 SecondRow = 2 FirstRowLeft = 3 FirstRowRight = 4 SecondRowLeft = 5 SecondRowMiddle = 6 SecondRowRight = 7 FirstRowLeftLeft = 8 FirstRowLeftRight = 9 FirstRowRightLeft = 10 FirstRowRightRight = 11 SecondRowLeftLeft = 12 SecondRowLeftRight =13 SecondRowRightLeft = 14 SecondRowRightRight = 15
        :param timeout: 监听超时时间，浮点型或者整型
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_ClimateService_Off_req(self):
        """
        通过SOA Partner发送ClimateService:Off的响应

        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_ClimateService_Off_req_and_feedback_resp(self, zone_id: ClimateZoneId = ClimateZoneId.FirstRowLeft, 
                                                       timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ClimateService:Off请求，并返回响应

        :param zone_id: 请求关闭空调区域，枚举型，取值范围:  AllZone = 0 FirstRow = 1 SecondRow = 2 FirstRowLeft = 3 FirstRowRight = 4 SecondRowLeft = 5 SecondRowMiddle = 6 SecondRowRight = 7 FirstRowLeftLeft = 8 FirstRowLeftRight = 9 FirstRowRightLeft = 10 FirstRowRightRight = 11 SecondRowLeftLeft = 12 SecondRowLeftRight =13 SecondRowRightLeft = 14 SecondRowRightRight = 15
        :param timeout: 监听超时时间，浮点型或者整型
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_chrglid_sts(self, sts: ChrgLidOperType, wait_time: Union[float, int] = 0):
        """
        设置充电口盖的状态

        :param sts: Open = 0 Close = 1
        :param wait_time:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_chrglid_sts(self, sts: ChrgLidSts):
        """
        获取电口盖的状态

        :param sts: Opened = 0 Closing = 1 Closed = 2 Locked = 3 Unlocked = 4 Opening = 5 Hover = 6 NA = 7
        :return:
        """
    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_SetRemoteClimateSwitchToHV_req(self):
        """
        通过SOA Partner发送远程上高压请求:ClimateControlService:SetRemoteClimateSwitchToHV的响应

        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetRemoteClimateSwitchToHV_req_feedback_resp(self, isOn: bool = True, keep_time: int = 30,
                                             timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程上高压请求:ClimateControlService:SetRemoteClimateSwitchToHV并返回响应

        :param isOn: 远程高压请求参数, 布尔型
        :param keep_time: 请求上高压时长, 单位min, 整形, 取值范围 0~59
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_SeatService_SetHeatingLevel_req(self):
        """
        通过SOA Partner发送SeatService:SetHeatingLevel请求的响应

        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SeatService_SetHeatingLevel_req_and_feedback_resp(self, id: SeatId = SeatId.All, info: int = 1,
                                              source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出SeatService:SetHeatingLevel请求并返回响应

        :param id: 远程请求座椅加热的座椅id，枚举型，取值范围:  # 选择座椅 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param info: 请求加热的等级，整形，取值范围0~3
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :param source: 请求来源, 枚举型，取值范围:  0, 1, 2
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def reponse_to_SteerWheelService_SetHeat_req(self, heat_level: HeatLevel = HeatLevel.Off,
                                            timeout: Union[float, int] = 1):
        """
        通过SOA Partner发送SteerWheelService:SetHeat请求的响应

        :param heat_level: 远程方向盘加热等级, 枚举型，取值范围:  Off = 0 Low = 1 Mid = 2 High = 3
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SteerWheelService_SetHeat_req_and_feedback_resp(self, heat_level: HeatLevel = HeatLevel.Off,
                                            source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出SteerWheelService:SetHeat请求并返回响应

        :param heat_level: 远程方向盘加热等级, 枚举型，取值范围:  Off = 0 Low = 1 Mid = 2 High = 3
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :param source: 请求来源, 枚举型，取值范围:  0, 1, 2
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_seat_heating_start_success(self, id: SeatId = SeatId.FrontLeft, heat_level: HeatLevel = HeatLevel.High,keep_time: int=30):
        """
        通过SOA Partner模拟座椅加热启动加热成功场景

        :param id: 请求加热的座椅ID，枚举型，取值范围:  FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param keep_time: 请求上高压时长, 单位min, 整形, 取值范围 0~59
        :param heat_level: 远程方向盘加热等级, 枚举型，取值范围:  Off = 0 Low = 1 Mid = 2 High = 3
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_steer_wheel_heating_success(self, heat_level: HeatLevel = HeatLevel.High,keep_time: int = 30):
        """
        通过SOA Partner模拟方向盘加热启动加热成功场景
        :param keep_time 请求上高压时长, 单位min, 整形, 取值范围 0~59
        :param heat_level: 远程方向盘加热等级, 枚举型，取值范围:  Off = 0 Low = 1 Mid = 2 High = 3
        :return: 
        """
        pass

   # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def remote_battery_heat_success_plan_a4(self, mintemp: float):
        """
        远程座舱预约电池预加热私桩插枪场景4正常开启电池加热功能正向流程, 使用SOA Partner模拟BGM与TCAM进行交互

        :param mintemp: 高压电池最低温度浮点型
        :return: 
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def remote_battery_heat_success_plan_b1(self, mintemp: float):
        """
        远程座舱预约电池预加热未插枪场景正常开启电池加热功能正向流程, 使用SOA Partner模拟BGM与TCAM进行交互

        :param mintemp: 高压电池最低温度浮点型
        :return: 
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def remote_battery_heat_success_plan_b2(self, mintemp: float):
        """
        远程座舱预约电池预加热非集度桩插枪场景正常开启电池加热功能正向流程, 使用SOA Partner模拟BGM与TCAM进行交互

        :param mintemp: 高压电池最低温度浮点型
        :return: 
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def remote_battery_heat_success_plan_b3(self, mintemp: float):
        """
        远程座舱预约电池预加热集度公桩插枪场景正常开启电池加热功能正向流程, 使用SOA Partner模拟BGM与TCAM进行交互

        :param mintemp: 高压电池最低温度浮点型
        :return: 
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_SetBatteryHeating_exit_req(self, type: ThermalRequestType = 5,on: bool = False, value: int = -40, timeout: Union[float, int] = 1):
        """
        预约电池加热过程中打断,使用SOA Partner监听TCAM发送HighVoltageService::SetBatteryHeating(ThermalRequestType type, bool on, float value) ==(kBookHeating,off,默认值-40)

        :param type: 加热请求类型
        :parm value: 加热目标温度
        :return: 
        """
        pass        
    
    @abstractmethod
    def trigger_call_sos_by_soa_partner(self, ReqSrc:eCallReqSource):
        """
        使用partner触发ECALL 开始呼叫

        :param ReqSrc: eCallReqSource kCDC = 0    # CDC触发ecall kACU = 1    # ACU触发ecall
        :returns: 
        """
        pass

    @abstractmethod
    def trigger_call_sos_notcheck_funsts_by_soa_partner(self, ReqSrc:eCallReqSource):
        """
        使用partner触发ECALL 开始呼叫不检查funsts状态

        :param ReqSrc: eCallReqSource kCDC = 0    # CDC触发ecall kACU = 1    # ACU触发ecall
        :returns: 
        """
        pass

    @abstractmethod
    def cancel_call_sos(self, ReqSrc: eCallReqSource):
        """
        使用partner取消ECALL 取消呼叫

        :param ReqSrc: eCallReqSource kCDC = 0    # CDC触发ecall kACU = 1    # ACU触发ecall
        :returns:
        """
        pass

    @abstractmethod
    def confirm_call_sos(self, opercmd = eCallOperCmd.kCONFIRM_ECALL, ReqSrc = eCallReqSource.kCDC):
        """
        确认呼叫SOS

        :return:
        """
        pass

    @abstractmethod
    def trigger_bcall_sos(self,opercmd = bCallOperCmd):
        """
        通过partner触发bcall
        :returns:
        """
        pass
    
    @abstractmethod
    def chk_xcall_notify(self,funsts= eCallFunSts.kREADY, type = eCallType.kPASSIVE, status = eCallSts.kIDLE):
        """
        partner检查xcall_mode状态
        :returns: 
        """
        pass

    @abstractmethod
    def chk_xcall_in_self_test_notify(self, funsts = eCallFunSts):
        """
        通过partner发出自检状态
        :returns: 
        """
        pass

    def hmi_set_tailgate_postion(self, pos: int, time_wait: Union[float, int] = 0):
        """
        设置尾门开启角度

        :param pos: 尾门开启角度
        :param time_wait: 执行操作之后的等待时间
        :return:
        """

    def hmi_set_door_postion(self, door_pos:DoorPos,pos:int, scene: VehicleInsideOutside= VehicleInsideOutside.VehicleInSide, time_wait: Union[float, int] = 0):
        """
        设置门开启角度

        :param door_pos: 设置的门的位置
        :param pos: 开启角度
        :param scene: 开门方式::VehicleInsideOutside/VehicleInSide/VehicleOutSide
        :param time_wait: 执行操作之后的等待时间默认0
        :return:
        """
    
    @abstractmethod
    def check_whether_ua_download(self, domain_name:DOMAIN):
        """
        检查某域控UA是否在下载
        
        :param domain_name: 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3
        :return: bool
        """
        pass
    
    @abstractmethod
    def hang_up_call_sos(self, opercmd = eCallOperCmd.kHANG_UP_ECALL, ReqSrc = eCallReqSource.kCDC,
                         funsts= eCallFunSts.kREADY, type = eCallType.kACTIVE, status = eCallSts.kHANG_UP):
        """
        挂断呼叫SOS

        :return:
        """
        pass

    @abstractmethod
    def hang_up_call_sos_not_check_funsts(self, opercmd = eCallOperCmd.kHANG_UP_ECALL, ReqSrc = eCallReqSource.kCDC,
                         type = eCallType.kACTIVE, status = eCallSts.kHANG_UP):
        """
        挂断呼叫SOS不检查funsts状态

        :return:
        """
        pass
    
    def get_fota_ConditionCheckResults(self, master_conditioncheckresult_field:MASTER_ConditionCheckResults_EVENT):
        """
        检查FOTA Master服务ConditionCheckResults event的内容
        
        :param master_conditioncheckresult_field: 枚举类型 MASTER_ConditionCheckResults_EVENT: class MASTER_ConditionCheckResults_EVENT(BaseEnum): CheckConditionType = 0 Results = 1
        :return: FOTA Master ConditionCheckResults event的内容
        """
        pass

    @abstractmethod
    def get_fota_UpdateErrorInfo(self):
        """
        检查FOTA Master服务UpdateErrorInfo event的内容
        
        :return: FOTA Master UpdateErrorInfo event的内容
        """
        pass

    @abstractmethod
    def till_fota_event_to(self, domain_name: DOMAIN, ua_event_field: UA_EVENT, target_status=None, timeout=60):
        """
        持续监控FOTA状态, 直至它回到目标值

        :param domain_name: 枚举类型 MASTER_EVENT: class MASTER_EVENT(BaseEnum): Status = 0 TaskId = 1 ErrorCode = 2
        :param target_status: 期望值
        :param timeout: 超时时间
        :returns:
        :raises keyError:
        """

    def event_check_hv_batt_thermy_sts(self, sts: HvBattThermReq, info: str = "HV Battery Thermal Status"):
        """
        Check高压电池告警事件提示是否为{info},状态是否为{sts.name}

        :param sts: 高压电池状态
        :param info: 提示信息
        :returns:
        """

    def get_hv_batt_thermy_sts(self, sts: HvBattThermReq, info: str = "HV Battery Thermal Status"):
        """
        获取高压电池告警提示是否为{info},状态是否为{sts.name}

        :param sts: 高压电池状态
        :param info: 提示信息
        :returns:
        """

    def event_check_and_get_hv_batt_thermy_sts(self, sts: HvBattThermReq, info: str = "HV Battery Thermal Status"):
        """
         获取高压电池告警上报以及状态信息

        :param sts: 高压电池状态
        :param info: 提示信息
        :returns:
        """

    def hmi_set_turn_lamp_mode_and_priority(self,mode:TurnLampMode,priority:int):
        """
        设置自动转向模式以及对应优先级
        :param mode:模式
            kStop = 0  # 转向灯关闭
            kLeft = 1  # 左转向灯开启
            kRight = 2  # 右转向灯开启
            kHazard = 3  # 危险报警灯开启
            Release = 255 #释放独占需求
        :param priority:优先级,int
        :return:
        """
    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_SetRemoteClimateSwitchToHVDelay_req(self):
        """
        通过SOA Partner发送远程延长上高压请求:ClimateControlService:SetRemoteClimateSwitchToHVDelay的响应
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SetRemoteClimateSwitchToHVDelay_req_and_feedback_resp(self, extendtime: int = 30,
                                                                    timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程延长上高压请求:ClimateControlService:SetRemoteClimateSwitchToHVDelay，并发送响应

        :param extendtime: 延长上高压时间, 整型, 取值范围0~59
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return:
        """
        pass

    @abstractmethod
    def get_fota_DownloadProcess(self, master_downloadprocess_event_field: MASTER_DownloadProcess_EVENT):
        """
        检查FOTA Master服务DownloadProcess event的内容
        
        :param 枚举类型 MASTER_DownloadProcess_EVENT:
            class MASTER_DownloadProcess_EVENT(BaseEnum):
                taskId = 0
                state = 1
                progress = 2
                downloadSpeed = 3
                leftTime = 4
                errorCode = 5
        :return: FOTA Master服务DownloadProcess event的内容
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_light_inhibit_sts(self,type:LightType,sts:bool):
        """
        获取车灯功能是否禁用的状态
        :param type: 车灯类型
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
        :param sts: 表示功能是否禁用, TRUE=功能禁用，FALSE=解除禁用
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def start_get_light_inhibit_sts(self,type:LightType = LightType.LightBrake ,sts:bool = False):
        """
        启动进程开始发送获取车灯功能是否禁用的状态请求
        :param type: 车灯类型
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
        :param sts: 表示功能是否禁用, TRUE=功能禁用，FALSE=解除禁用
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def stop_get_light_inhibit_sts(self):
        """
        停止发送获取车灯功能是否禁用的状态请求进程
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_extr_light_rear_fog_mode(self, mode: LightMode = LightMode.On):
        """
        设置后雾灯模式
        :param mode: 开关状态
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
        :return:
        """


    @abstractmethod
    def get_fota_UpdateProcess(self, master_updateprocess_event_field: MASTER_UpdateProcess_EVENT):
        """
        检查FOTA Master服务UpdateProcess event的内容
        
        :param 枚举类型 MASTER_UpdateProcess_EVENT:
            class MASTER_UpdateProcess_EVENT(BaseEnum):
                taskId = 0
                state = 1
                progress = 2
                leftTime = 3
                errorCode = 4
        :return: FOTA Master服务UpdateProcess event的内容
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_no_SetOutput_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM不会发出HighVoltageService:SetOutput请求        
        :param timeout: 监听超时时间，整形或浮点型
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_no_SetBatteryHeating_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM不会发出HighVoltageService:SetBatteryHeating请求        
        :param timeout: 监听超时时间，整形或浮点型
        :return: 
        """
        pass

    @abstractmethod
    def empty_all(self, wait_time=0):
        """
        清空partner所有缓存数据

        :return:
        """
        pass

    # @Author:liu.yang@jiduatuo.com
    @abstractmethod
    def call_vehicle_api(self, v2t_api: V2T_API, payload: dict):
        """
        通过调用V2TRoutingForwarder的CallVehicleApi请求, Mock 云端对车端进行业务交互
                
        :param v2t_api: 车端业务id V2T_API: class V2T_API(): OTA = 'ota' 
        :param payload: 请求体
        :return: 
        """
        pass
    
    # @Author:liu.yang@jiduatuo.com
    @abstractmethod
    def trigger_fota_type20(self, taskid: int):
        """
        触发v2t type 20接口, 触发OTA Master获取到任务id
                
        :param taskid: fota 任务id
        :return: 
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_window_full_close(self, win_pos:WindowId):
        """
        通过S2S设置窗户全关
        :param win_pos: 设置的窗户位置
            kWindowFrontLeft = 0
            kWindowFrontRight = 1
            kWindowRearLeft = 2
            kWindowRearRight = 3
            kWindowAll = 4
        :return: 
        """
   # @Author:taiping.zong@jiduatuo.com
    @abstractmethod
    def notify_LockSuccessTriggerSource(self, sourceid: TriggerSourceId = TriggerSourceId.RemoteKey):
        """
        通过SOA Partner模拟BGM发送解闭锁动作触发源事件通知:CentralLockService:LockSuccessTriggerSource.TriggerSourceId
        :param sourceid: 中控锁触发原因, 枚举值, 取值范围: NoTriggerSource = 0 RemoteKey = 1 KeyLessPassive = 2 InteriorSwitches = 3 SpeedLocking = 4 Relocking = 5 SlamLocking = 6 Telematices = 7 CrashUnlock = 8 Approach = 9 OutsideOthers = 10 InsideOthers = 11 NFC = 12
        :return: 
        """
        pass

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def check_GetPosition_req(self, timeout: Union[float, int] = 1):       
        """
        通过SOA Partner监听TCAM是否发出请求WindowService::GetPosition请求        
        :param timeout: 监听超时时间，整形或浮点型
        :return: 
        """
        pass
    
    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def response_to_GetPosition_req(self, *position_info: dict):
        """
        通过SOA Partner监听TCAM是否发出请求WindowService::GetPosition请求,并响应        
        :param position_info: 车窗开度信息,类型为dict,{"id": WindowId, "position": int}
        :return: 
        """
        pass

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_wiper_fault_sts(self,pos:WiperPos, fault_type: WiperFaultType, fault_msg:str = ""):
        """
        调用接口 GetFaultInfo 获取{pos.name}雨刮故障类型是否为{fault_type.name},提示信息是否为{fault_msg}      
        :param pos: 雨刮位置
            Front = 0
            Rear = 1
            All = 2
        :param pos: 故障类型
            Ok = 0
            WashWaterLow = 1
            RainSensorError = 2
            LightRawSensorError = 3
            SystemError = 4
            SwitchError = 5
            NA = 6
        :param fault_msg: 故障提示信息，字符串
        :return: 
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_wiper_fault_sts(self,pos:WiperPos, fault_type: WiperFaultType, fault_msg:str = "OK"):
        """
        调用接口 WiperFault 查看是否有雨刮故障事件上报，check事件信息：{pos.name}雨刮故障类型是否为{fault_type.name},提示信息是否为{fault_msg}  
        :param pos: 雨刮位置
            Front = 0
            Rear = 1
            All = 2
        :param pos: 故障类型
            Ok = 0
            WashWaterLow = 1
            RainSensorError = 2
            LightRawSensorError = 3
            SystemError = 4
            SwitchError = 5
            NA = 6
        :param fault_msg: 故障提示信息，字符串
        :return: 
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_wiper_fault_sts(self,pos:WiperPos, fault_type: WiperFaultType, fault_msg:str = ""):
        """
        获取雨刮故障状态并且Check雨刮故障状态上报事件     
        :param pos: 雨刮位置
            Front = 0
            Rear = 1
            All = 2
        :param pos: 故障类型
            Ok = 0
            WashWaterLow = 1
            RainSensorError = 2
            LightRawSensorError = 3
            SystemError = 4
            SwitchError = 5
            NA = 6
        :param fault_msg: 故障提示信息，字符串
        :return: 
        """

    # @Author:taiping.zong@jiduatuo.com
    @abstractmethod
    def notify_BrakePedalStatus(self, status: PressedStatus = PressedStatus.PedalReleased, validity: ValidityLevel = ValidityLevel.kValid):
        """
        通过SOA Partner发送制动踏板位置状态PedalService_server::BrakePedalStatus{status.value}"       
        :param status: 踏板位置状态,枚举值,取值范围:PedalReleased = 0 PedalPressed = 1 PedalNA = 2
        :param validity:信号置信度,枚举值,取值范围:kValid = 0 kSignalUnknownStatus = 1 kQualityFactor2 = 2 kE2ECounter = 3 kSignalMissing = 4 kE2ECheckSum = 5 kQualityFactor1 = 6 kE2EGeneral = 7 kQualityFactor0 = 8 kFatal = 9 kReserved = 10 
        :return: 
        """
        pass
    
    # @Author:liu.yang@jiduatuo.com
    @abstractmethod
    def trigger_fota_type90(self, taskid: int):
        """
        触发v2t type 90接口, 触发OTA Master获取到app 信息
                
        :param taskid: fota 任务id
        :return: 
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_rain_auto_close_window_sts(self,sts:bool):
        """
        设置雨天自动关窗
        :param sts: 自动关窗的状态 bool
        :return:  
        """
        
    @abstractmethod
    def wait_for_service_reconnect(self, partner_key: str, timeout=30):
        """
        服务上线连接后，partner会发出ServiceStatus事件，其中state=START，以此来判断服务连接上
        
        :param partner_key:  指定某个服务，partner作为client和server都可以
        :param timeout:  超时时间，30s服务没连接报错
        :return:
        """
        pass

    @abstractmethod
    def chek_hv_cli_seat_steer_driv_pseng_request(self):
        """
        Partner监听TCAM是否已发送上高压请求、空调开启请求、方向盘开启、主副驾开启请求
        
        """
        pass

    @abstractmethod
    def re_chek_hv_cli_seat_steer_driv_pseng_request(self):
        """
        使用SOA Partner监听TCAM是否已二次发送空调开启请求、方向盘开启、主副驾开启请求
        
        """
        pass

    @abstractmethod
    def check_no_hv_cli_seat_steer_driv_pseng_req(self, timeout: Union[float, int] ):
        """
        通过SOA Partner监听TCAM未发出上高压请求、空调开启请求、方向盘开启、主副驾开启请求
        
        """
        pass
    
    @abstractmethod
    def cock_reserv_hv_cli_seat_steer_driv_pseng_start_success(self):
        """
        通过SOA Partner模拟座舱预约座椅/方向盘/空调启动加热成功场景
        
        """
        pass
    
    @abstractmethod
    def chk_rvc_inacti_to_conve(self):
        """
        通过SOA Partner检测TCAM是否调用本地空调开启、主副座椅加热、方向盘加热请求
        
        """
        pass

    @abstractmethod
    def chk_hv_delay_cli_seat_steer_driv_pseng_req(self, ac:bool=False, temp:int=23, seat:bool=False,seat_level=HeatLevel.Low, steer:bool=False, steer_level=HeatLevel.Low):
        """
        使用SOA Partner监听TCAM是否已发送延长高压请求，空调开启或方向盘开启或主副驾开启请求，且请求参数正确
        
        :param  ac:     bool             是否为空调
        :param  temp:   int              设置空调温度,例如设置23°C,就是230
        :param  seat:   bool             是否为座椅
        :param  driver_level: int        主驾加热挡位默认1,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :param  passenger_level: int     副驾加热默认1,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :param  steer:   bool            是否为方向盘
        :param  steering_level: int      方向盘加热等级默认1,1档,2......
        :return:
        """
        pass

    @abstractmethod
    def set_ac_seat_steer_heating_start_success(self, heat_level: HeatLevel = HeatLevel.Low):
        """
        通过SOA Partner模拟开启空调、座椅加热、方向盘加热启动成功场景

        """
        pass

    @abstractmethod
    def chk_ac_seat_steer_driv_pseng_off_req(self, ac_off:bool=False, steer_off:bool=False, seat_off:bool=False, timeout: int=20):
        """
        使用SOA Partner监听TCAM是否已发送关闭空调、方向盘或主副驾请求，且请求参数正确
        
        """
        pass

    @abstractmethod
    def chk_no_ac_seat_steer_off_req(self, timeout:int= 20):
        """
        通过SOA Partner监听TCAM未发出关闭空调、方向盘、主副驾请求

        """
        pass
    
    @abstractmethod
    def set_convenience_duration(self, time):
        """
        通过SOA Partner 设置驻车舒享模式
        
        :param time: 是指的驻车舒享时间，单位是0.5h
        :returns: 
        :raises keyError: 
        """
    
    @abstractmethod
    def check_keep_power_mode(self, keep_power=True, exit_reason:KeepPowerFlag=KeepPowerFlag.open, do_assert=True,  **kwargs):
        """
        检查是否在维持上电模式以及原因是否正确
        
        :param keep_power: 检查维持上电模式的状态 
            True:在
            False:不在
        :param exit_reason: 检查维持上电模式的原因 
            0=kNormal  //正常状态，默认值 
            1=kUserReq  //用户请求关闭
            2=kHVSOC   //高压电池电量低于阈值 
            3=kGearNotP  //挡位非P挡
            4=kCarModeNotNormal //车辆模式不满足 
            5=kFOTAUpdate  //车辆开始FOTA升级
            6=kOther //其他原因退出
        :parm do_assert: 报错则返回模式不匹配，不报错则不返回
        :returns: 
        :raises keyError: 
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_not_rain_auto_close_window_req(self):
        """
        检测BGM没有发出雨天自动关窗的事件通知
        :parm do_assert: 报错则返回模式不匹配，不报错则不返回
        :returns: 
        """
        
    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_NotifyVIN(self, vin: str = "LSTEST6R9F2086644"):
        """
        通过SOA Partner模拟BGM发送CarConfigService:NotifyVIN事件        
        :param vin: 车辆编码，字符串类型，固定17位，大写字母和数字组成
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_NotifyHvBatteryCode(self, batt_code: str = "123456789012345678901234"):
        """
        通过SOA Partner模拟BGM发送HighVoltageService:NotifyHvBatteryCode事件        
        :param batt_code: 电池编码，字符串类型，固定24位，数字组成
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetBatteryCodeInfo_req(self, batt_code: str = "123456789012345678901234"):
        """
        通过SOA Partner模拟HighVoltageService_server:GetBatteryCodeInfo请求的响应       
        :param batt_code: 电池编码，字符串类型，固定24位，数字组成
        :return:
        """
        pass

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_rain_auto_close_window_sts(self,sts:bool):
        """
        调用接口 GetRainAutoCloseWindowStatus 获取雨天自动关窗状态
        :param sts: 自动关窗的状态 bool
        :return:  
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_rain_auto_close_window_sts(self,sts:bool):
        """
        调用接口获取雨天自动关窗事件通知上报
        :param sts: 自动关窗的状态 bool
        :return:  
        """

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_rain_auto_close_window_sts(self,sts:bool):
        """
        调用接口获取雨天自动关窗状态事件通知上报
        :param sts: 自动关窗的状态 bool
        :return:  
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_rain_auto_close_window_req(self,sts:RainCloseWinReq):
        """
        调用接口 GetRainWinAutoCloseReqSts 获取下雨自动关窗请求状态
        :param sts: 下雨自动关窗请求状态
            NoRequest = 0
            Open = 1
            CloseWinAndSunroof = 2
            Close = 3
            Stop = 4
        :return:  
        """

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_rain_auto_close_window_req(self,sts:RainCloseWinReq):
        """
        调用接口 NotifyRainWinAutoCloseReqSts 获取下雨自动关窗事件上报通知
        :param sts: 下雨自动关窗请求状态
            NoRequest = 0
            Open = 1
            CloseWinAndSunroof = 2
            Close = 3
            Stop = 4
        :return:  
        """

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_rain_auto_close_window_req(self,sts:RainCloseWinReq):
        """
        获取下雨自动关窗请求状态和对应通知上报
        :param sts: 下雨自动关窗请求状态
            NoRequest = 0
            Open = 1
            CloseWinAndSunroof = 2
            Close = 3
            Stop = 4
        :return:  
        """
    
    
    @abstractmethod
    def set_exhibition_mode(self, is_open: bool):
        """
        设置展车模式

        :param status: True 展车模式， False 非展车模式
        :returns: 
        :raises keyError: 
        """

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_high_beam_ctrl_cmd(self,cmd_value:HighBeamCmd,hbid_value:int):
        """
        调用接口 SetHighBeamControl 进行远光灯控制
        :param cmd_value: 光灯控制类型
            Off = 0
            Flash = 1
            On = 2
            Release = 255
        :param hbid_value: 客户端id,整型
        :return:  
        """

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_and_event_check_high_beam_ctrl_sts(self,cmd_value:HighBeamCmd,hbid_value:int,hbsts_prty:LowBeamClientId,sts:Union[HighBeamSts,None]=None):
        """
        调用接口 SetHighBeamControl 进行远光灯控制让后check对应事件上报
        :param cmd_value: 光灯控制类型
            Off = 0
            Flash = 1
            On = 2
            Release = 255
        :param hbid_value: 客户端id,整型
        :param hbsts_prty: 灯光优先级,整型
        :return:  
        """

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_windows_postion(self,pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        """
        调用服务WindowService_client GetPosition 获取窗户的位置信息
        :param pos_drvr: 左前车窗开度，枚举型：
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
        :param pos_pass: 右前车窗开度,
        :param pos_lere: 左后车窗开度
        :param pos_rire: 右后车窗开度
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_four_windows_postion(self,pos:WinPos):
        """
        调用服务WindowService_client GetPosition 同时获取四个窗户的位置
        :param pos_drvr: 期望四个车窗开度，枚举型：
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
        :return:
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetVIN_req(self, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出获取VIN请求:CarConfigService:GetVIN
        :param timeout: 监听请求超时时间，单位s，整形或浮点型
        :return: 
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetVIN_req(self, vin: str = "LSTEST6R9F2086644"):
        """
        通过SOA Partner发送获取VIN请求的响应:CarConfigService:GetVIN
        :param vin: 车辆编码，字符串类型，大写字母和数字组成，17位
        :return: 
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetVIN_req_and_feedback_resp(self, vin: str = "LSTEST6R9F2086644", timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出获取VIN请求:CarConfigService:GetVIN，并发送响应
        :param vin: 车辆编码，字符串类型，大写字母和数字组成，17位
        :param timeout: 监听请求超时时间，单位s，整形或浮点型
        :return: 
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_OutputState(self, on: bool = True):
        """
        通过SOA Partner模拟BGM发送HighVoltageService:OutputState事件通知
        :param on: 当前高压状态，布尔型
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetOutput_req(self, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出获取上高压状态请求:HighVoltageService:GetOutput
        :param timeout: 监听请求超时时间，单位s，整形或浮点型
        :return: 
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetOutput_req(self, on: bool = False):
        """
        通过SOA Partner发送获取上高压状态请求的响应:HighVoltageService:GetOutput
        :param on: 当前高压状态，布尔型
        :return: 
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetOutput_req_and_feedback_resp(self, on: bool = False, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出获取上高压状态的请求:HighVoltageService:GetOutput，并发送响应
        :param on: 当前高压状态，布尔型
        :param timeout: 监听请求超时时间，单位s，整形或浮点型
        :return: 
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_HVThermalOutOfControl(self, state: bool = False):
        """
        通过SOA Partner模拟BGM发送HighVoltageService:HVThermalOutOfControl事件通知
        :param state: 当前高压热失控状态，布尔型
        :return: 
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetHVThermalOutOfControl_req(self, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出获取高压热失控状态请求:HighVoltageService:GetHVThermalOutOfControl
        :param timeout: 监听请求超时时间，单位s，整形或浮点型
        :return: 
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetHVThermalOutOfControl_req(self, state: bool = False):
        """
        通过SOA Partner发送获取高压热失控状态请求的响应:HighVoltageService:GetHVThermalOutOfControl
        :param state: 当前高压热失控状态，布尔型
        :return: 
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetHVThermalOutOfControl_req_and_feedback_resp(self, state: bool = False, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出获取高压热失控状态的请求:HighVoltageService:GetHVThermalOutOfControl
        :param state: 当前高压热失控状态，布尔型
        :param timeout: 监听请求超时时间，单位s，整形或浮点型
        :return: 
        """

    @abstractmethod
    def pack_ua_event_args_with_error(self, 
                                    ua_sts: UA_Sts,
                                    ua_download_sts:UA_DownloadStatus = UA_DownloadStatus.DOWNLOAD_DEFAULT,
                                    ua_preupdate_sts:UA_PreUpdatedStatus = UA_PreUpdatedStatus.PREUPDATE_DEFAULT, 
                                    ua_update_sts:UA_UpdatedStatus = UA_UpdatedStatus.UPDATE_DEFAULT, 
                                    errorCode=0):
        """
        打包符合UA Status event 格式定义的json字符串, 带error  
             
        :param ua_sts: 枚举类型 UA_Sts: class UA_Sts(BaseEnum): IDLE = 0 DOWNLOAD = 1 READY_TO_INSTALL = 2 INSTALLING = 3 UPDATE_FINISH = 4 ROLLING_BACK = 5 SYSTEM_ACTIVE = 6 ERROR = 7 ACTIVATING = 8 UPDATE_FAILED = 9
        :param ua_download_sts: 枚举类型 UA_DownloadStatus:
            class UA_DownloadStatus(BaseEnum):
                DOWNLOAD_RUNNING = 0
                DOWNLOAD_COMPLETE = 1
                DOWNLOAD_FIRST_FAILED = 2
                DOWNLOAD_FINAL_FAILED = 3
                DOWNLOAD_DEFAULT = 255          
        :param ua_preupdate_sts: 枚举类型 UA_PreUpdatedStatus:
            class UA_PreUpdatedStatus(BaseEnum):
                WAIT_PREUPDATE_CMD = 0
                PREUPDATE_RUNNING = 1
                PREUPDATE_COMPLETE = 2
                PREUPDATE_FAILED = 3
                PREUPDATE_DEFAULT = 255      
        :param ua_update_sts: 枚举类型 UA_UpdatedStatus:
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
        :param errorCode: UA错误码
        :returns: UA Status json
        :raises keyError: None
        """
        pass
    
    @abstractmethod
    def pack_ua_status_args_with_error(self,
                                       ua_sts: UA_Sts,
                                       ua_download_sts:UA_DownloadStatus = UA_DownloadStatus.DOWNLOAD_DEFAULT,
                                       ua_preupdate_sts:UA_PreUpdatedStatus = UA_PreUpdatedStatus.PREUPDATE_DEFAULT, 
                                       ua_update_sts:UA_UpdatedStatus = UA_UpdatedStatus.UPDATE_DEFAULT, 
                                       errorCode = 0):
        """
        打包符合UA Status 格式定义的json字符串与event区别点在于status不带event_name, 带error  
             
        :param ua_sts: 枚举类型 UA_Sts: class UA_Sts(BaseEnum): IDLE = 0 DOWNLOAD = 1 READY_TO_INSTALL = 2 INSTALLING = 3 UPDATE_FINISH = 4 ROLLING_BACK = 5 SYSTEM_ACTIVE = 6 ERROR = 7 ACTIVATING = 8 UPDATE_FAILED = 9
        :param ua_download_sts: 枚举类型 UA_DownloadStatus:
            class UA_DownloadStatus(BaseEnum):
                DOWNLOAD_RUNNING = 0
                DOWNLOAD_COMPLETE = 1
                DOWNLOAD_FIRST_FAILED = 2
                DOWNLOAD_FINAL_FAILED = 3
                DOWNLOAD_DEFAULT = 255          
        :param ua_preupdate_sts: 枚举类型 UA_PreUpdatedStatus:
            class UA_PreUpdatedStatus(BaseEnum):
                WAIT_PREUPDATE_CMD = 0
                PREUPDATE_RUNNING = 1
                PREUPDATE_COMPLETE = 2
                PREUPDATE_FAILED = 3
                PREUPDATE_DEFAULT = 255      
        :param ua_update_sts: 枚举类型 UA_UpdatedStatus:
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
        :param errorCode: UA错误码
        :returns: UA Status json
        :raises keyError: None
        """
        pass
    
    @abstractmethod
    def change_ua_event_and_getstatus_with_error(self,
                                                 domain_name: DOMAIN,
                                                 ua_sts: UA_Sts,
                                                 ua_download_sts:UA_DownloadStatus = UA_DownloadStatus.DOWNLOAD_DEFAULT,
                                                 ua_preupdate_sts:UA_PreUpdatedStatus = UA_PreUpdatedStatus.PREUPDATE_DEFAULT, 
                                                 ua_update_sts:UA_UpdatedStatus = UA_UpdatedStatus.UPDATE_DEFAULT, 
                                                 errorCode=0):
        """
        同时更新某UA的event事件和get_status回复, 带error  
        
        :param domain_name: 枚举类型 DOMAIN: class DOMAIN(BaseEnum): BGM = 0 TCAM = 1 CDC = 2 ACU = 3    
        :param ua_sts: 枚举类型 UA_Sts: class UA_Sts(BaseEnum): IDLE = 0 DOWNLOAD = 1 READY_TO_INSTALL = 2 INSTALLING = 3 UPDATE_FINISH = 4 ROLLING_BACK = 5 SYSTEM_ACTIVE = 6 ERROR = 7 ACTIVATING = 8 UPDATE_FAILED = 9
        :param ua_download_sts: 枚举类型 UA_DownloadStatus:
            class UA_DownloadStatus(BaseEnum):
                DOWNLOAD_RUNNING = 0
                DOWNLOAD_COMPLETE = 1
                DOWNLOAD_FIRST_FAILED = 2
                DOWNLOAD_FINAL_FAILED = 3
                DOWNLOAD_DEFAULT = 255          
        :param ua_preupdate_sts: 枚举类型 UA_PreUpdatedStatus:
            class UA_PreUpdatedStatus(BaseEnum):
                WAIT_PREUPDATE_CMD = 0
                PREUPDATE_RUNNING = 1
                PREUPDATE_COMPLETE = 2
                PREUPDATE_FAILED = 3
                PREUPDATE_DEFAULT = 255      
        :param ua_update_sts: 枚举类型 UA_UpdatedStatus:
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
        :param errorCode: UA错误码
        :returns: UA Status json
        :raises keyError: None
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_maintain_mode(self, status: bool):
        """
        设置维修模式
        
        :param status:开关
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def notify_maintain_mode(self, status: bool):
        """
        检查维修模式状态notify通知
        
        :param status:开关
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_and_check_maintain_mode(self, status: bool):
        """
        设置并校验维修模式状态 
        :param status:开关
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_wiper_auto_mode(self, pos: WiperPos, mode: WipgAutFrntMod):
        """
        S2S获取和EventCheck雨刮自动模式状态
        :param pos:雨刮位置
            Front = 0
            Rear = 1
            All = 2
        :param mode:自动挡模式
            Off = 0
            ImdtMod = 1 
            IntlMod = 2 
            ContnsMod = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_wiper_single_mode(self, pos: WiperPos, sts: isOn):
        """
        S2S获取和EventCheck雨刮单挂模式状态
        :param pos:雨刮位置
            Front = 0
            Rear = 1
            All = 2
        :param sts:开关状态
            Off = False
            On = True
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_turn_lamp_mode_sts(self,mode:TurnLampMode,priority:int):
            """
        获取自动转向模式以及对应优先级
        :param mode:模式
            kStop = 0  # 转向灯关闭
            kLeft = 1  # 左转向灯开启
            kRight = 2  # 右转向灯开启
            kHazard = 3  # 危险报警灯开启
            Release = 255 #释放独占需求
        :param priority:优先级,int
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_wiper_return_pos(self, pos: WiperPos, sts: isOn):
        """
        获取/通知雨刮回位位置是否为{sts.value}
        :param pos:雨刮位置：
            Front = 0
            Rear = 1
            All = 2
        :param mode:状态
            Off = False
            On = True
        :return:
        """
        
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_rain_detected_pos(self, sts: bool):
        """
        获取/通知下雨事件是否为{sts}
        :param sts:bool
        :return:
        """


    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_rain_level(self, level:int):
        """
        获取/通知雨量值是否为{level}
        :param level:int
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_ambient_light_intensity(self,qf:int,value:int):
        """
        获取/通知环境光强度{value},QF={qf}
        :param qf:int
        :param value:int
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_day_and_night_sts(self,sts:bool):
        """
        获取/通知白天黑夜状态{sts}
        :param sts:bool
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_solar_value(self,value:int):
        """
        获取/通知阳光强度{value}
        :param value:int
        :return:
        """
    
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_and_event_check_wiper_switch_sts(self,sts:SteerWhlTouchSwtSts):
        """
        获取/通知雨刮开关状态是否为{sts.name}
        :param sts:方向盘按按压类型
            NotAvailble = 0
            ShortPress = 1
            LongPress = 2
            Error = 3
        :return:
        """
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_turn_lamp_mode_sts(self,mode:TurnLampMode,priority:int):
        """
        通过SOA Partner LightService_client::GetTurnLampStatus 获取转向灯模式，check模式是否为{mode.name},优先级是否为{priority}
        :param mode:模式
            kStop = 0  # 转向灯关闭
            kLeft = 1  # 左转向灯开启
            kRight = 2  # 右转向灯开启
            kHazard = 3  # 危险报警灯开启
            Release = 255 #释放独占需求
        :param priority:优先级,int
        :return:
        """
       
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_usagemode_up_and_down(self, up_usagemode: UsageMode, down_usagemode: UsageMode):
        """
        同时进行服务上切下切使用模式
        
        :param up_usagemode:上切的使用模式
            ABANDONED = 0
            INACTIVE = 1
            CONVENIENCE = 2
            ACTIVE = 11
            DRIVING = 13
        :param down_usagemode:上切的使用模式
            ABANDONED = 0
            INACTIVE = 1
            CONVENIENCE = 2
            ACTIVE = 11
            DRIVING = 13
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_carmode_by_serivice(self, carmod:CarMode):
        """
        调用服务切换carmode接口 
        :param carmod:要切换的carmode
        :return:
        """

  # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def notyfy_lock_warn_info(self, lock_warn: LockWarn, remind: DoorRemind, timeout=5):
        """
        通过SOA Partner通知期望的门锁告警信息:EntryService:NotifyLockWarning
        :param lock_warn: 门锁告警状态，枚举型：
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
        :param remind:门锁提醒类型，枚举型:
                NoRequest = 0
                CloseDoorInside = 1
                CloseDoorOutside = 2
        :return: 
        """
    
    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def get_lock_warn_info(self, lock_warn: LockWarn, remind: DoorRemind, timeout=5):
        """
        通过SOA Partner获取期望的门锁告警信息:EntryService:GetLockWarning
        :param lock_warn: 门锁告警状态，枚举型：
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
        :param remind:门提醒类型，枚举型:
                NoRequest = 0
                CloseDoorInside = 1
                CloseDoorOutside = 2
        :return: 
        """
    
    # @Author:xiangyue.li@jiduatuo.com
    def set_auto_sts(self, sts: bool, cycle_mode: CycleMode, wind_zone: ClimateZone, wind_mode: AirWindMode, speed_zone: ClimateZone, speed: WindSpeed):
        """
        通过SOA Partner设置AC、循环模式、吹风模式、风速
        :param sts: 制冷状态：
        :param cycle_mode:循环模式:
        :param wind_zone: 吹风区域：
        :param wind_mode:吹风模式:
        :param speed_zone: 风量区域：
        :param speed:风速:
        :return: 
        """    

    # @Author:qian.feng@jiduatuo.com
    def hmi_get_door_anti_pinch_sts(self, id: DoorId, isantipinch: bool = False):
        """
        通过SOA Partner获取对应侧门的故障信息:
        :param id: 侧门ID：              
        :param isantipinch: 防夹状态，布尔值：              
        :return: 
        """

    # @Author:qian.feng@jiduatuo.com
    def hmi_get_door_postion(self, doors:DoorPos, door_pos:DoorPos,pos:int, time_wait: Union[float, int] = 0):
        """
        通过SOA Partner获取对应侧门的故障信息:
        :param doors: 所有侧门ID：              
        :param door_pos: 对应侧门ID：              
        :param pos:门开角度:
        :return: 
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def ck_key_service_unlock_event(self, keyid: list, key_type: DigitalKeyType, trigger: DigitalKeyIdTrigger):
        """
        校验S2S_KeyService上报解锁事件
        :param keyid: 指示Key ID，占16个字节
        :param key_type: 钥匙类型
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
        :param trigger: 指示Key ID更新的事件类型
            Invalid = 0
            ApproachLight = 1
            ApproachSecon = 2
            Unlock = 3
        :return:
        """

        
    # @Author:xiangyue.li@jiduatuo.com
    def hmi_set_steer_wheel_adjust_direction(self, direct: AdjustDirection, time_wait: Union[float, int] = 0):
        """
        通过SOA Partner设置方向盘调节方向    Forward = 0    Left = 1    Up = 2    Backward = 3    Right = 4    Down = 5
        :param direct: 调节方向：
        :param time_wait: 等待时间：
        :return: 
        """

    # @Author:qian.feng@jiduatuo.com
    def hmi_event_check_tailgate_movests(self, status:MoveSts, time_wait: Union[float, int] = 1):
        """
        通过SOA Partner获取尾门运动状态:
        :param MoveSts: 尾门运动状态，枚举类型：              
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
        :return: 
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def hmi_set_car_location_req(self,req:CarLocalTraceReq,time_wait: Union[float, int] = 1):
        """
        通过SOA Partner KeyService_client::SetCarLocalTraceRequest 设置寻车请求
        :param req: 寻车请求类型，枚举类型：              
            kNoReq = 0  # 无请求
            kHornReq = 1  # 喇叭请求
            kLiReq = 2  # 灯光请求
            kHornLiReq = 3  # 喇叭和灯光同时请求
        :param time_wait执行之后等待时间
        :return: 
        """
    # @Author:liu.yang@jiduatuo.com
    def get_ccp_status(self, CcpMaster_field: CCPMasterSts_Field):
        """
        获取CCPMasterService的CCPStatus
        :param CcpMaster_field: 枚举类型 CCPMasterSts_Field:
            class CCPMasterSts_Field(BaseEnum):
                TaskInfo = 0
                State = 1
                ErrorCode = 2                
        :return: CCPStatus
        """
        
    # @Author:liu.yang@jiduatuo.com
    def get_ccp_status(self, CcpMasterConditionCheckResult_Field: CCPMasterConditionCheckResult_Field):
        """
        获取CCPMasterService的ConditionCheckResult
        :param CcpMasterConditionCheckResult_Field: 枚举类型 CCPMasterConditionCheckResult_Field:
            class CCPMasterConditionCheckResult_Field(BaseEnum):
                TaskInfo = 0
                ConditionCheckVecs = 1             
        :return: ConditionCheckResult
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_hv_off_sts(self, is_off:bool):
        """
        设置下高压请求 
        :param is_off: 下高压请求状态
        :return:
        """
        
    # @Author:liu.yang@jiduatuo.com
    def till_ccp_event_to(self, CcpMasterSts_Field: CCPMasterSts_Field, target_status=None, timeout=60):
        """
        获取CCPMasterService的ConditionCheckResult
        :param CcpMaster_field: 枚举类型 CCPMasterSts_Field:
            class CCPMasterSts_Field(BaseEnum):
                TaskInfo = 0
                State = 1
                ErrorCode = 2             
        :param target_status: 目标状态
        :param timeout: 超时时间
        :return
        """
   
    # @Author:liu.yang@jiduatuo.com
    def get_ccp_ActiveProgress(self):
        """
        获取CCPMasterService的ActiveProgress
        :return
        """

    # @Author:liu.yang@jiduatuo.com
    def till_ccp_ActiveProgress_to(self,target_status=None, timeout=60):
        """
        获取CCPMasterService的ActiveProgress           
        :param target_status: ActiveProgress value
        :param timeout: 超时时间
        :return
        """

    # @Author:qian.feng@jiduatuo.com
    def hmi_set_light_show_active(self, status: bool):
        """
        通过SOA Partner设置灯光秀激活/禁用:
        :param status:  灯光秀激活状态, 布尔        
        :return: 
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_keep_power_mode_by_source(self, keep_power=True, exit_reason:KeepPowerFlag=KeepPowerFlag.open, source:str="PetMode", do_assert=True,  **kwargs):
        """
        检查是否在维持上电模式以及原因是否正确
        
        :param keep_power: 检查维持上电模式的状态 
            True:在
            False:不在
        :param exit_reason: 检查维持上电模式的原因 
            0=kNormal  //正常状态，默认值 
            1=kUserReq  //用户请求关闭
            2=kHVSOC   //高压电池电量低于阈值 
            3=kGearNotP  //挡位非P挡
            4=kCarModeNotNormal //车辆模式不满足 
            5=kFOTAUpdate  //车辆开始FOTA升级
            6=kOther //其他原因退出
        :param source: 某种模式,默认为宠物模式
        :parm do_assert: 报错则返回模式不匹配，不报错则不返回
        :returns: 
        :raises keyError: 
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_keep_power_mode_by_source(self, modeSts: bool, source: str="PetMode"):
        """
        由某种模式控制设置维持上电模式 
        :param modeSts: 
            True:打开
            False:关闭
        :param source: 某种模式,默认为宠物模式
        :return:
        """

    # @Author:qian.feng@jiduatuo.com
    def notify_and_get_door_movests(self, doorid: DoorId, doormovests: DoorMoveStatus, time_wait: Union[float, int] = 1):
        """
        通过SOA Partner通知及获取四门运动状态:
        :param doorid:  四门ID 
        :param doormovests:  四门运动状态
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
        :return: 
        """
    
    @abstractmethod
    def check_SetParkingComfortModeOff_req(self):
        """
        通过SOA Partner监听TCAM是否发出VehicleSetStatusService:SetParkingComfortMode请求

        :return:
        """
        pass

    @abstractmethod
    def response_to_SetParkingComfortModeOff_req(self):
        """
        通过SOA Partner发送远程关闭维持上电请求:VehicleSetStatusService:SetParkingComfortMode的响应

        :return:
        """
        pass
    
    @abstractmethod
    def check_ParkingComfortModeOff_req_and_feedback_resp(self):
        """
        通过SOA Partner监听TCAM是否发出远程关闭维持上电请求:VehicleSetStatusService:SetParkingComfortMode,并返回响应

        :return:
        """
        pass
    
    @abstractmethod
    def check_GetParkingComfortModeSts_req(self, modeSts: int=0, reason: int=1):
        """
        通过SOA Partner监听TCAM是否发出VehicleSetStatusService:GetParkingComfortModeSts请求
        :param: modeSts:
                kOff  = 0     # 关闭
                kOn = 1       # 打开
        :param: reason:
                kNormal  = 0            # 正常状态，默认值
                kUserReq = 1            # 用户请求关闭
                kHVSOC = 2              # 高压电池电量低于阈值
                kGearNotP = 3           # 挡位非P挡
                kCarModeNotNormal  = 4  # 车辆模式不满足
                kFOTAUpdate = 5         # 车辆开始FOTA升级
                kOther = 6              # 其他原因退出

        :return:
        """
        pass
    
    @abstractmethod
    def response_to_GetParkingComfortModeSts_req(self, modeSts: int=0, reason: int=1):
        """
        通过SOA Partner发送获取维持上电状态请求:VehicleSetStatusService:GetParkingComfortModeSts的响应
        :param: modeSts:
                kOff  = 0     # 关闭
                kOn = 1       # 打开
        :param: reason:
                kNormal  = 0            # 正常状态，默认值
                kUserReq = 1            # 用户请求关闭
                kHVSOC = 2              # 高压电池电量低于阈值
                kGearNotP = 3           # 挡位非P挡
                kCarModeNotNormal  = 4  # 车辆模式不满足
                kFOTAUpdate = 5         # 车辆开始FOTA升级
                kOther = 6              # 其他原因退出

        :return:
        """
        pass
    
    @abstractmethod
    def check_GetParkingComfortModeSts_req_and_feedback_resp(self, modeSts:int=0, reason: int=1, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出远程关闭维持上电请求:VehicleSetStatusService:GetParkingComfortModeSts,并返回响应
        :param: modeSts:
                kOff  = 0     # 关闭
                kOn = 1       # 打开
        :param: reason:
                kNormal  = 0            # 正常状态，默认值
                kUserReq = 1            # 用户请求关闭
                kHVSOC = 2              # 高压电池电量低于阈值
                kGearNotP = 3           # 挡位非P挡
                kCarModeNotNormal  = 4  # 车辆模式不满足
                kFOTAUpdate = 5         # 车辆开始FOTA升级
                kOther = 6              # 其他原因退出

        :return:
        """
        pass
    
    @abstractmethod
    def notify_ParkingComfortModeSts(self, ParkingComfortModeSts: int = 0, exit_reason: int = 1):
        """
        通过SOA Partner发送维持上电模式状态的事件:VehicleSetStatusService::ParkingComfortModeSts
        :param: modeSts:
                kOff  = 0     # 关闭
                kOn = 1       # 打开
        :param: reason:
                kNormal  = 0            # 正常状态，默认值
                kUserReq = 1            # 用户请求关闭
                kHVSOC = 2              # 高压电池电量低于阈值
                kGearNotP = 3           # 挡位非P挡
                kCarModeNotNormal  = 4  # 车辆模式不满足
                kFOTAUpdate = 5         # 车辆开始FOTA升级
                kOther = 6              # 其他原因退出

        :return:
        """
        pass


    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_FrntLeftDoorSts(self, isopen: bool = False, validity: ValidityLevel = ValidityLevel.kValid, 
                               sts: DoorStatus = DoorStatus.kClosed, is_anti_pinchs: bool = False):
        """
        通过 DoorService_server:FrntLeftDoorSts 发送主驾门开关状态
        :param: isopen门状态，当前是否开启，布尔型True 开，False 关
        :param: validity门状态开启置信度，枚举型，取值范围：
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
        :param: sts门运动状态，枚举值，取值范围:
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
        :param: is_anti_pinchs门防夹状态，布尔型,True 触发防夹, False 未触发防夹
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_FrntRightDoorSts(self, isopen: bool = False, validity: ValidityLevel = ValidityLevel.kValid, 
                               sts: DoorStatus = DoorStatus.kClosed, is_anti_pinchs: bool = False):
        """
        通过 DoorService_server:FrntRightDoorSts 发送副驾门开关状态
        :param: isopen门状态，当前是否开启，布尔型True 开，False 关
        :param: validity门状态开启置信度，枚举型，取值范围：
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
        :param: sts门运动状态，枚举值，取值范围:
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
        :param: is_anti_pinchs门防夹状态，布尔型,True 触发防夹, False 未触发防夹
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_RearLeftDoorSts(self, isopen: bool = False, validity: ValidityLevel = ValidityLevel.kValid, 
                               sts: DoorStatus = DoorStatus.kClosed, is_anti_pinchs: bool = False):
        """
        通过 DoorService_server:RearLeftDoorSts 发送左后门开关状态
        :param: isopen门状态，当前是否开启，布尔型True 开，False 关
        :param: validity门状态开启置信度，枚举型，取值范围：
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
        :param: sts门运动状态，枚举值，取值范围:
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
        :param: is_anti_pinchs门防夹状态，布尔型,True 触发防夹, False 未触发防夹
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_RearRightDoorSts(self, isopen: bool = False, validity: ValidityLevel = ValidityLevel.kValid, 
                               sts: DoorStatus = DoorStatus.kClosed, is_anti_pinchs: bool = False):
        """
        通过 DoorService_server:RearRightDoorSts 发送右后门开关状态
        :param: isopen门状态，当前是否开启，布尔型True 开，False 关
        :param: validity门状态开启置信度，枚举型，取值范围：
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
        :param: sts门运动状态，枚举值，取值范围:
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
        :param: is_anti_pinchs门防夹状态，布尔型,True 触发防夹, False 未触发防夹
        """
        pass


    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_FrntLeftSeatHeatVentStatus(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):
        """
        通过SOA Partner发送主驾座椅加热通风状态事件:SeatService:FrntLeftSeatHeatVentStatus
        :param heat_level: 座椅的加热等级, 整形
        :param heat_time: 座椅的加热时间, 整形, 单位min
        :param heat_work_sts: 加热通风状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param vent_level: 通风等级, 整形
        :param vent_time: 通风时间, 整形, 单位min
        :param vent_work_sts: 加热通风状态, 枚举值
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_FrntRightSeatHeatVentStatus(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):
        """
        通过SOA Partner发送副驾座椅加热通风状态事件:SeatService:FrntRightSeatHeatVentStatus
        :param heat_level: 座椅的加热等级, 整形
        :param heat_time: 座椅的加热时间, 整形, 单位min
        :param heat_work_sts: 加热通风状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param vent_level: 通风等级, 整形
        :param vent_time: 通风时间, 整形, 单位min
        :param vent_work_sts: 加热通风状态, 枚举值
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_RearLeftSeatHeatVentStatus(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):
        """
        通过SOA Partner发送左后座椅加热通风状态事件:SeatService:RearLeftSeatHeatVentStatus
        :param heat_level: 座椅的加热等级, 整形
        :param heat_time: 座椅的加热时间, 整形, 单位min
        :param heat_work_sts: 加热通风状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param vent_level: 通风等级, 整形
        :param vent_time: 通风时间, 整形, 单位min
        :param vent_work_sts: 加热通风状态, 枚举值
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_RearRightSeatHeatVentStatus(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):
        """
        通过SOA Partner发送右后座椅加热通风状态事件:SeatService:RearLeftSeatHeatVentStatus
        :param heat_level: 座椅的加热等级, 整形
        :param heat_time: 座椅的加热时间, 整形, 单位min
        :param heat_work_sts: 加热通风状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param vent_level: 通风等级, 整形
        :param vent_time: 通风时间, 整形, 单位min
        :param vent_work_sts: 加热通风状态, 枚举值
        :return:
        """
        pass

    # @Author:linfeng.xu@jiduatuo.com
    @abstractmethod
    def check_climate_heat_status_and_get_charginfo_and_get_equipmentinfo_get_mintemp(self, mintemp: float,
                                                                    plug_sts: PluggerSts = PluggerSts.ConnectedWithoutPower,
                                                                    charg_sts: ChargingSts = ChargingSts.NoCharging):
        """
        通过SOA监听climate请求并返回响应, 监听获取充电信息请求并返回响应，监听获取充电桩信息并响应，监听获取电池最低温度并返回响应
        :param: mintemp: 高压电池最低温度浮点型
        :param: plug_sts: 充电枪状态  Disconnected = 0  ConnectedWithoutPower = 1  PowerAvailableButNotActivated = 2 ConnectedWithPower = 3 Init = 4 Fault = 5
        :param: charg_sts: 充电状态 Default = 0 NoCharging = 1 ACCharging = 2 ACChargingEnd = 3 ChargingCmpl = 4 Heating = 5 Booking = 6 NoDischarging = 7 Discharging = 8 DischargingEnd = 9 DischargingCmpl = 10 Chargingfault = 11 DischargingFault = 12 ACChrgnFltChrgrSide = 14 DCCharging = 15 DCChrgnFltVehSide = 18 DCChrgnFltChrgrSideTempFlt = 19 DCChrgnFltChrgrSideConFlt = 20 DCChrgnFltChrgrSideHwFlt = 21 DCChrgnFltChrgrSideEmgyFlt = 22 DCChrgnFltChrgrSideComFlt = 23 SuperCharging = 24 ACChargingSuspend = 25 DCChargingEnd = 26 ACChrgnFltVehSide = 27 Boostcharging = 28 BoostchargingFlt = 29 WirelessCharging = 30
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    def hmi_get_automatic_door_closing(self, triggertype:TriggerType, time_wait = 1):
        """
        通过SOA Partner获取D档自动关门设置项状态:
        :param TriggerType:  获取取消D档自动关门 or 设置D档自动关门
            enable  = 0 获取设置D档自动关门状态
            disable = 1 获取取消D档自动关门状态
        :param taime_wait:  延时时间         
        :return: 
        """

	# @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def send_Alldoor_close(self):
        """
        通过 DoorService_server:RearRightDoorSts 发送门开关状态为所有门关闭

        :return: 
        """
        pass

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def send_Alldoor_open(self):
        """
        通过 DoorService_server:RearRightDoorSts 发送门开关状态为所有门打开

        :return: 
        """
        pass

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def set_alldoor_sts(sts: DoorStatus=DoorStatus.kClosing):
        """
        通过 DoorService_server:RearRightDoorSts 发送门开关状态为所有门指定状态

        :return: 
        """
        pass

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def notify_WindowPosition_sts(self, positions: list = [100, 100,100, 100],):
        """
        通过SOA Partner发出车窗执行状态WindowService::WindwoPosition

        :param win_id: 车窗ID kWindowFrontLeft = 0 kWindowFrontRight = 1 kWindowRearLeft = 2 kWindowRearRight = 3 kWindowAll = 4
        :param position: 车窗位置
        :return:
        """
        pass

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def check_GetLockSuccessTriggerSource_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出CentralLockService:GetLockSuccessTriggerSource请求
        """
        pass

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def check_GetLockActTriggerSource_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出CentralLockService:GetLockActTriggerSource请求"
        """
        pass

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def check_GetLockSuccessTriggerSource_req_and_feedback_resp(self, trigger_source_id: TriggerSourceId = TriggerSourceId.Telematices, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出远程关闭维持上电请求:CentralLockService:GetLockSuccessTriggerSource,并返回响应
        """
        pass

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def check_GetLockActTriggerSource_req_and_feedback_resp(self, trigger_source_id: TriggerSourceId = TriggerSourceId.Telematices, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出远程关闭维持上电请求:CentralLockService:GetLockActTriggerSource,并返回响应
        """
        pass
    
    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def response_to_GetLockSuccessTriggerSource_req(self, trigger_source_id: TriggerSourceId = TriggerSourceId.Telematices):
        """
        通过SOA Partner发送CentralLockService:GetLockSuccessTriggerSource请求的响应
        """
        pass

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def response_to_GetLockActTriggerSource_req(self, trigger_source_id: TriggerSourceId = TriggerSourceId.Telematices):
        """
        通过SOA Partner发送CentralLockService:GetLockActTriggerSource响应
        """
        pass

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def check_NotifyRVCLockInfo_event(self, sts: UnlockSts=UnlockSts.kSuccess,uid: int = 0, seqId: str = '', timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:NotifyRVCLockInfo事件
        """
        pass
    
    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetOuterRearViewHeatStatus_req(self, id: ViewId = ViewId.RearViewAll, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出OuterRearViewService:GetOuterRearViewHeatStatus请求
        :param id: 后视镜ID, 整形，取值范围0~2
        :param timeout: 超时时间, 整形, 单位s
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetOuterRearViewHeatStatus_req(self, id: ViewId = ViewId.RearViewAll, heat_work_sts: HeatWorkSts = HeatWorkSts.HeatOn, \
                                                   heat_sts: HeatSts = HeatSts.On):
        """
        通过SOA Partner发送OuterRearViewService:GetOuterRearViewHeatStatus请求的响应
        :param id: 后视镜ID, 整形，取值范围0~2
        :param heat_work_sts: 加热工作状态，枚举型，取值范围：
            HeatOff = 0
            HeatOn = 1
            Invalid = 255
        :param heat_sts: 加热状态，枚举型，取值范围：
            Off = 0
            On = 1
            Limited = 2
            NotAvailable = 3
            TimeoutOff = 4
            AutoHeatOn = 5
            Invalid = 255
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetOuterRearViewHeatStatus_req_and_feedback_resp(self, id: ViewId = ViewId.RearViewAll, heat_work_sts: HeatWorkSts = HeatWorkSts.HeatOn, \
                                                                 heat_sts: HeatSts = HeatSts.On, timeout: Union[float, int] = 1):
        """
        获取OuterRearViewService:GetOuterRearViewHeatStatus请求的响应,并且回复对应的响应
        :param timeout: 超时时间, 整形, 单位s
        :param id: 后视镜ID, 整形，取值范围0~2
        :param heat_work_sts: 加热工作状态，枚举型，取值范围：
            HeatOff = 0
            HeatOn = 1
            Invalid = 255
        :param heat_sts: 加热状态，枚举型，取值范围：
            Off = 0
            On = 1
            Limited = 2
            NotAvailable = 3
            TimeoutOff = 4
            AutoHeatOn = 5
            Invalid = 255
        :return:
        """
        pass


    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_FrontCameraHeatStatus(self, heat_sts: HeatStatus = HeatStatus.HeatStatusOn):
        """
        通过SOA Partner发送前摄像头加热状态事件:ShieldWindowService::FrontCameraHeatStatus
        :param heat_sts: 前摄像头加热状态, 枚举型，取值范围：
            HeatStatusOff = 0
            HeatStatusOn = 1
            HeatStatusAutoOn = 2
            HeatFault = 3
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_RearShieldWindowHeatStatus(self, heat_sts: HeatStatus = HeatStatus.HeatStatusOn):
        """
        通过SOA Partner发送后挡风玻璃加热状态事件:ShieldWindowService::RearShieldWindowHeatStatus
        :param heat_sts: 后挡风玻璃加热状态, 枚举型，取值范围：
            HeatStatusOff = 0
            HeatStatusOn = 1
            HeatStatusAutoOn = 2
            HeatFault = 3
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_OuterRearViewHeatStatus(self, heat_work_sts: HeatWorkSts = HeatWorkSts.HeatOn, heat_sts: HeatSts = HeatSts.On):
        """
        通过SOA Partner发送外后视镜加热状态事件:OuterRearViewService:OuterRearViewHeatStatus
        :param heat_work_sts: 加热工作状态，枚举型，取值范围：
            HeatOff = 0
            HeatOn = 1
            Invalid = 255
        :param heat_sts: 加热状态，枚举型，取值范围：
            Off = 0
            On = 1
            Limited = 2
            NotAvailable = 3
            TimeoutOff = 4
            AutoHeatOn = 5
            Invalid = 255
        :return:
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    def check_envent_door_movement_and_antipinch_status(self, sidedoor: SideDoor, isopen: bool, doormovests: DoorMoveStatus, antipinch: bool, time_wait: Union[float, int] = 1):
        """
        通过SOA Partner获取当前车门通知运动状态, 车门开关状态, 防夹状态:
        :param SideDoor:  对应前后左右四个侧门
        :param isopen:  车门开关状态 bool
        :param doormovests:  车门运动状态
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
        :param antipinch:  当前侧门防夹状态 bool
        :param taime_wait:  延时时间         
        :return: 
        """

    # @Author:qian.feng@jiduatuo.com
    def check_envent_lock_reminder(self, lockreminder: LockReminder, time_wait = 1):
        """
        通过SOA Partner校验当前中央解闭锁动作提醒通知:
        :param lockreminder:  解闭锁动作提醒状态
            Idle  = 0
            NFCLockFail = 1
            PELockFailByKeyForget = 2
            NoKeyPresent = 3
            DoorCloseAudio = 4
            ReLockFail = 5
            ReLockOk = 6
            WalkAwayAudio = 7       
        :param taime_wait:  延时时间         
        :return: 
        """

    # @Author:qian.feng@jiduatuo.com
    def set_power_outlet_req(self, poweroutletreq: PowerOutLetReq, time_wait: Union[float, int] = 0):
        """
        通过SOA Partner设置12v电源继电器请求闭合/断开
        :param poweroutletreq: 12v电源闭合proxy请求：
            NoReq = 0
            On = 1
            Off = 2
        :param time_wait: 等待时间
        :return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    def notify_OuterRearViewFoldStatus(self, view_id: ViewId = ViewId.RearViewAll, value_left: ViewFoldStatus = ViewFoldStatus.StatusFolded, \
                                       validity_left: ValidityLevel = ValidityLevel.kValid, value_right: ViewFoldStatus = ViewFoldStatus.StatusFolded, \
                                        validity_right: ValidityLevel = ValidityLevel.kValid):
        """
        通过SOA Partner发送通知外后视镜折叠状态事件:OuterRearViewService:OuterRearViewFoldStatus
        
        Args:
            view_id: 左、右后视镜以及所有后视镜:
                kRearViewRight = 0
                kRearViewLeft = 1
                kRearViewAll = 2
            value_left (ViewFoldStatus, optional): 左侧后视镜的折叠状态，默认为 StatusFolded，取值范围：
                StatusNa = 0
                StatusUnfolded = 1
                StatusFolded = 2
                StatusUnfolding = 3
                StatusFolding = 4
            validity_left (ValidityLevel, optional): 左侧后视镜的折叠状态有效性，默认为 Valid，取值范围：
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
            value_right (ViewFoldStatus, optional): 右侧后视镜的折叠状态，默认为 StatusFolded，取值范围：
                StatusNa = 0
                StatusUnfolded = 1
                StatusFolded = 2
                StatusUnfolding = 3
                StatusFolding = 4
            validity_right (ValidityLevel, optional): 右侧后视镜的折叠状态有效性，默认为 kValid，取值范围：
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
        Returns:
            None
        
        """
        pass

    #@Author:lei.song@jiduatuo.com                                          
    def notify_ViewFault(self, *view_fault):
        """
        通过SOA Partner发送通知外后视镜故障状态事件:OuterRearViewService:ViewFault"
        
        Args:
            faultId:
                kOk = 0
                kFaultFold = 1  
                kFaultTilt = 2  
                kFaultNA = 3  
            faultMsg:
                ""
             ViewId:
                kRearViewRight = 0
                kRearViewLeft = 1
                kRearViewAll = 2
        Returns:
            None
        
        """
        pass
    
    # @Author:lei.song@jiduatuo.com
    def check_Unfold_req(self, id: ViewId = ViewId.RearViewAll, is_auto_unfold: bool = False, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出OuterRearViewService:Unfold请求
        
        Args:
            id (ViewId, optional): 需要监听的视图ID，枚举类型，默认为ViewId.RearViewAll，取值范围：
                RearViewRight = 0
                RearViewLeft = 1
                RearViewAll = 2
            is_auto_unfold (bool, optional): 是否自动展开，布尔型，默认为False
            timeout (Union[float, int], optional): 等待超时时间，整形或浮点型，默认为1秒
        
        Returns:
            None
        
        """
        pass


    # @Author:lei.song@jiduatuo.com
    def response_to_Unfold_req(self, result: int = 0):
        """
        通过SOA Partner发送OuterRearViewService:Unfold请求的响应
        
        Args:
        - result (int, optional): Unfold请求的执行结果，整形，默认为0，取值范围0~2
        
        Returns:
        - None
        
        """
        pass


    # @Author:lei.song@jiduatuo.com
    def check_Unfold_req_and_feedback_resp(self, id: ViewId = ViewId.RearViewAll, is_auto_unfold: bool = False, \
        timeout: Union[float, int] = 1, result: int = 0):
        """
        获取OuterRearViewService:Unfold请求的响应,并且回复对应的响应
        
        Args:
            id (ViewId, optional): 视图ID，枚举类型，默认为ViewId.RearViewAll，取值范围：
                RearViewRight = 0
                RearViewLeft = 1
                RearViewAll = 2
            is_auto_unfold (bool, optional): 是否自动展开，布尔型，默认为False
            timeout (Union[float, int], optional): 超时时间，整形或浮点型，默认为1秒
            result (int, optional): 响应结果，整形，默认为0，取值范围0~2
        
        Returns:
            None
        
        """
        pass


    # @Author:lei.song@jiduatuo.com
    def check_Fold_req(self, id: ViewId = ViewId.RearViewAll, is_auto_unfold: bool = False, timeout: Union[float, int] = 1):
        """
        检查TCAM是否发出OuterRearViewService:Fold请求
        
        Args:
            id (ViewId, optional): 需要折叠的视图ID，枚举型，默认为ViewId.RearViewAll，取值范围：
                RearViewRight = 0
                RearViewLeft = 1
                RearViewAll = 2
            is_auto_unfold (bool, optional): 是否自动展开，布尔型，默认为False
            timeout (Union[float, int], optional): 超时时间，整形或浮点型，默认为1秒
        
        Returns:
            None
        
        """
        pass


    # @Author:lei.song@jiduatuo.com
    def response_to_Fold_req(self, result: int = 0):
        """
        发送OuterRearViewService:Fold请求的响应
        
        Args:
            result (int, optional): 结果，默认为0
        
        Returns:
            None
        
        """
        pass

  
    # @Author:lei.song@jiduatuo.com
    def check_Fold_req_and_feedback_resp(self, id: ViewId = ViewId.RearViewAll, result: int = 0, \
                                         is_auto_unfold: bool = True, timeout: Union[float, int] = 1):
        """
        获取OuterRearViewService:Fold请求的响应，并且回复对应的响应
        
        Args:
            id (ViewId, optional): 视图ID，枚举类型，默认为ViewId.RearViewAll，取值范围：
                RearViewRight = 0
                RearViewLeft = 1
                RearViewAll = 2
            is_auto_unfold (bool, optional): 是否自动展开，布尔型，默认为False
            timeout (Union[float, int], optional): 超时时间，整形或浮点型，默认为1秒
            result (int, optional): 响应结果，整形，默认为0，取值范围0~2
        
        Returns:
            None
        """
        pass

    def notify_PetModeSts(self, sts: PetModeSts = PetModeSts.kOFF):
        """
        通过SOA Partner模拟宠物模式运行状态
        :param sts: kOFF = 0 kON = 1 kRUN = 2 kUnExpect = 255
        """
        pass 

    def check_SeatService_SetVentingLevel_req(self, id: SeatId = SeatId.All, info: HeatLevel = HeatLevel.Low,
                                              source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出SeatService:SetVentingLevel请求

        :param id: 座椅id, 枚举值, 取值范围: FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param info: 请求通风的等级，整形，取值范围0~3
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :param source: 请求源, 枚举值, 取值范围: 0, 1, 2
        :return:
        """
        pass

    def response_to_SeatService_SetVentingLevel_req(self):
        """
        通过SOA Partner发送SeatService:SetVentingLevel请求的响应

        :return: 
        """
        pass

    def check_SeatService_SetVentingLevel_req_and_feedback_resp(self, id: SeatId = SeatId.All, info: VentLevel = VentLevel.Low,
                                              source: SourceId = SourceId.Remote, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出SeatService:SetVentingLevel请求并返回响应

        :param id: 远程请求座椅通风的座椅id，枚举型，取值范围:  # 选择座椅 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param info: 请求通风的等级，整形，取值范围0~3
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :param source: 请求源, 枚举值, 取值范围: 0, 1, 2
        :return: 
        """
        pass

    def rvc_seat_venting_start_success(self, id: SeatId = SeatId.FrontLeft, vent_level: VentLevel = VentLevel.High, keep_time: int = 30):
        """
        通过SOA Partner模拟开启座椅通风启动成功场景
        :param keep_time 请求上高压时长, 单位min, 整形, 取值范围 0~59
        :param id: 远程请求座椅通风的座椅id，枚举型，取值范围:  # 选择座椅 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param vent_level: 请求通风的等级，整形，取值范围0~3
        """
        pass
    
    def get_viewmirror_angle(self, views:ViewPos,viewPos: ViewPos, hori_angle: Union[int, float], vert_angle: Union[int, float], time_wait: Union[float, int] = 3):
        """
        通过SOA Partner获取{viewPos}水平方向角度{hori_angle}垂直方向角度{vert_angle}
        :param: 后视镜位置{viewPos}，水平方向角度{hori_angle}，垂直方向角度{vert_angle}
        """
        pass

    def set_carloctr_req(self, req:CarLocalTraceReq):
        """
        通过SOA Partner监听TCAM是否发出远程寻车 KeyService_client:SetCarLocalTraceRequest请求

        :param req:
            kNoReq = 0
            kHornReq = 1
            kLiReq = 2
            kHornLiReq = 3
        :return:
        """
        pass
    
    def check_keep_power_mode_and_time(self, keep_power=True, exit_reason:KeepPowerFlag=KeepPowerFlag.open, displaytime:DisplayLeftTime=DisplayLeftTime.kUnknown, do_assert=True,  **kwargs):
        """
        检查是否在维持上电模式以及原因是否正确
        
        :param keep_power: 检查维持上电模式的状态 
            True:在
            False:不在
        :param exit_reason: 检查维持上电模式的原因 
            0=kNormal  //正常状态，默认值 
            1=kUserReq  //用户请求关闭
            2=kHVSOC   //高压电池电量低于阈值 
            3=kGearNotP  //挡位非P挡
            4=kCarModeNotNormal //车辆模式不满足 
            5=kFOTAUpdate  //车辆开始FOTA升级
            6=kOther //其他原因退出
        :param displaytime: 检查维持上电的显示时间
        :parm do_assert: 报错则返回模式不匹配，不报错则不返回
        :returns: 
        :raises keyError: 
        """
        pass


    # @Author:qian.feng@jiduatuo.com
    def get_and_check_envent_door_fault_sts(self, checkinterfacetype: CheckInterfaceType, doorid: DoorId, doorfaultsts: DoorfFultSts, time_wait = 1):
        """
        通过SOA Partner校验四门故障通知状态:
        :param CheckInterfaceType:  校验接口类型
            Get  = 0:获取故障
            CheckNotify = 1:故障通知
            All = 2:通知及获取
        :param doorid:  前后左右四门ID
        :param doorfaultsts:  车门故障状态   
        :param taime_wait:  延时时间               
        :return: 
        """
        
        
    @abstractmethod
    def check_no_GetHeat_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM不会发出SteerWheelService:GetHeat请求        
        :param timeout: 监听超时时间，整形或浮点型
        :return: 
        """
        pass
    
    
    @abstractmethod
    def check_no_GetRemotePowerStatus_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM不会发出ClimateControlService:GetRemotePowerStatus请求        
        :param timeout: 监听超时时间，整形或浮点型
        :return: 
        """
        pass
    
    
    @abstractmethod
    def check_no_GetDefrostSts_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM不会发出ClimateControlService:GetDefrostSts请求        
        :param timeout: 监听超时时间，整形或浮点型
        :return: 
        """
        pass
    
    
    @abstractmethod
    def check_no_GetChargingInfo_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM不会发出HighVoltageService:GetChargingInfo请求        
        :param timeout: 监听超时时间，整形或浮点型
        :return: 
        """
        pass
    
    
    @abstractmethod
    def check_no_GetBatteryTemperatureInfo_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM不会发出HighVoltageService:GetBatteryTemperatureInfo请求        
        :param timeout: 监听超时时间，整形或浮点型
        :return: 
        """
        pass


    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_NotifyConfigList(self, ccp_info = {566: 0x10}):
        """
        模拟BGM发送车辆配置字值改变通知
        :param ccp_info (dict, optional): 车辆配置信息字典，key为配置名称，value为配置值，默认为{566: 0x10}。
        :returns: None        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_ConfigDataNotify(self, config_data: str = "", app_name: str = "gb32960", file_name: str = "key_value_tab_config", \
                                publish_id: int = 0, action: int = 0, file_type: str = "Json", push_type: int = 1, \
                                    strategy: int = 3, domain_version: str = "2.0.0"):
        """
        发送远程配置数据通知
        :param config_data (str, optional): 配置数据内容. 默认为 "".
        :param app_name (str, optional): 应用名称. 默认为 "gb32960".
        :param file_name (str, optional): 配置文件名称. 默认为 "key_value_tab_config".
        :param publish_id (int, optional): 发布ID. 默认为 0.
        :param action (int, optional): 操作类型. 默认为 0.
        :param file_type (str, optional): 文件类型. 默认为 "Json".
        :param push_type (int, optional): 推送类型. 默认为 1.
        :param strategy (int, optional): 推送策略. 默认为 3.
        :param domain_version (str, optional): 域版本. 默认为 "2.0.0".
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetEcuAppsVersion_req(self, ecu: str = "TCAM", timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ConfigMasterService:GetEcuAppsVersion请求
        :param ecu: (str, optional): ECU名称，默认为"TCAM".
        :param timeout: (Union[float, int], optional): 超时时间，可以是浮点数或整数，默认为1秒.
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetEcuAppsVersion_req(self, app_name: str = "gb32960", publish_id: int = 0, \
                                        is_empty: bool = False, report_type: int = 4, status_type: int = 1025, \
                                        time_stamp: int = 0):
        """
        发送ConfigMasterService:GetEcuAppsVersion请求的响应
        :param app_name (str, optional): 应用名称. Defaults to "gb32960".
        :param publish_id (int, optional): 发布ID. Defaults to 0.
        :param is_empty (bool, optional): 是否为空. Defaults to False.
        :param report_type (int, optional): 报告类型. Defaults to 4.
        :param status_type (int, optional): 状态类型. Defaults to 1025.
        :param time_stamp (int, optional): 时间戳. Defaults to 0.
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetEcuAppsVersion_req_and_feedback_resp(self, app_name: str = "gb32960", publish_id: int = 0, \
                                        is_empty: bool = False, report_type: int = 4, status_type: int = 1025, \
                                        time_stamp: int = 0, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ConfigMasterService:GetEcuAppsVersion请求并返回响应
        :param app_name (str, optional): 应用名称，默认为"gb32960"。
        :param publish_id (int, optional): 发布ID，默认为0。
        :param is_empty (bool, optional): 是否为空，默认为False。
        :param report_type (int, optional): 报告类型，默认为4。
        :param status_type (int, optional): 状态类型，默认为1025。
        :param time_stamp (int, optional): 时间戳，默认为0。
        :param timeout (Union[float, int], optional): 超时时间，默认为1。
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetConfigMasterVersion_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ConfigMasterService:GetConfigMasterVersion请求
        :param timeout: (Union[float, int], optional): 请求超时时间，默认为1秒.
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetConfigMasterVersion_req(self, config_version: str = "Config2.0.12.1"):
        """
        响应通过SOA Partner发送的ConfigMasterService:GetConfigMasterVersion请求
        
        Args:
        :param config_version: (str, optional): 配置版本号，默认为"Config2.0.12.1"。
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetConfigMasterVersion_req_and_feedback_resp(self, config_version: str = "Config2.0.12.1", timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ConfigMasterService:GetConfigMasterVersion请求并返回响应
        :param config_version: (str, optional): 配置版本号. 默认为"Config2.0.12.1".
        :param timeout: (Union[float, int], optional): 请求超时时间. 默认为1.
        :param eturns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetAppConfig_req(self, app_name: str = "gb32960", timeout: Union[float, int] = 1):
        """
        监听TCAM是否通过SOA Partner向ConfigMasterService发出GetAppConfig请求
        
        Args:
        :param app_name: (str, optional): 应用名称，默认为"gb32960"。
        :param timeout: (Union[float, int], optional): 超时时间，单位为秒，默认为1秒。
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetAppConfig_req(self, config_data: str = "", app_name: str = "gb32960", file_name: str = "key_value_tab_config", \
                                    publish_id: int = 0, action: int = 0, file_type: str = "Json", push_type: int = 1, \
                                    strategy: int = 3, domain_version: str = "2.0.0"):
        """
        发送ConfigMasterService:GetAppConfig请求的响应
        :param config_data: (str, optional): 配置内容，默认为""。
        :param app_name: (str, optional): 应用名称，默认为"gb32960"。
        :param file_name: (str, optional): 配置文件名称，默认为"key_value_tab_config"。
        :param publish_id: (int, optional): 发布ID，默认为0。
        :param action: (int, optional): 操作类型，默认为0。
        :param file_type: (str, optional): 文件类型，默认为"Json"。
        :param push_type: (int, optional): 推送类型，默认为1。
        :param strategy: (int, optional): 策略类型，默认为3。
        :param domain_version: (str, optional): 域名版本，默认为"2.0.0"。
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetAppConfig_req_and_feedback_resp(self, config_data: str = "", app_name: str = "gb32960", file_name: str = "key_value_tab_config", \
                                                publish_id: int = 0, action: int = 0, file_type: str = "Json", push_type: int = 1, \
                                                strategy: int = 3, domain_version: str = "2.0.0", timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ConfigMasterService:GetAppConfig请求并返回响应
        :param config_data: (str, optional): 配置内容，默认为""。
        :param app_name: (str, optional): 应用名称，默认为"gb32960"。
        :param file_name: (str, optional): 配置文件名称，默认为"key_value_tab_config"。
        :param publish_id: (int, optional): 发布ID，默认为0。
        :param action: (int, optional): 操作类型，默认为0。
        :param file_type: (str, optional): 文件类型，默认为"Json"。
        :param push_type: (int, optional): 推送类型，默认为1。
        :param strategy: (int, optional): 策略类型，默认为3。
        :param domain_version: (str, optional): 域名版本，默认为"2.0.0"。
        :param timeout: (Union[float, int], optional): 超时时间，默认为1秒。
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SendConfigStatusToTsp_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ConfigMasterService:SendConfigStatusToTsp请求
        :param timeout: (Union[float, int], optional): 请求超时时间，默认为1秒。
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_SendConfigStatusToTsp_req(self, config_result: bool = True):
        """
        通过SOA Partner发送ConfigMasterService:SendConfigStatusToTsp请求的响应
        :param config_result: (bool, optional): 配置返回的结果，默认为True.
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_SendConfigStatusToTsp_req_and_feedback_resp(self, config_result: bool = True, timeout: Union[float, int] = 1):
        """
        监听TCAM是否发出ConfigMasterService:SendConfigStatusToTsp请求并返回响应
        :param config_result: (bool, optional): 配置的结果返回响应. Defaults to True.
        :param timeout: (Union[float, int], optional): 超时时间. Defaults to 1.
        :returns: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def send_config_data_and_feedback_result(self, config_data: str = "", app_name: str = "gb32960", file_name: str = "key_value_tab_config", \
                                publish_id: int = 0, action: int = 0, file_type: str = "Json", push_type: int = 1, \
                                    strategy: int = 3, domain_version: str = "2.0.0"):
        """
        发送配置数据并反馈结果。
        :param config_data: (str, optional): 配置数据。默认为空字符串。
        :param app_name: (str, optional): 应用名称。默认为"gb32960"。
        :param file_name: (str, optional): 文件名。默认为"key_value_tab_config"。
        :param publish_id: (int, optional): 发布ID。默认为0。
        :param action: (int, optional): 操作类型。默认为0。
        :param file_type: (str, optional): 文件类型。默认为"Json"。
        :param push_type: (int, optional): 推送类型。默认为1。
        :param strategy: (int, optional): 策略类型。默认为3。
        :param domain_version: (str, optional): 域名版本。默认为"2.0.0"。
        :returns: None
        """
        pass

    @abstractmethod
    def check_NotifyRemoteAuthStartModeSts_event(self, sts: RemoteAuthSts = RemoteAuthSts.kDefault, send_time:int=0xffffffff, timeout: Union[float, int] = 1):
        """
        监听TCAM是否发出RemoteAuthService:NotifyRemoteAuthStartModeSts事件
        :param sts: (RemoteAuthSts, optional): 远程认证状态。默认为RemoteAuthSts.kDefault。
        :param send_time: (int, optional): 发送时间。默认为0xffffffff。
        :param timeout: (Union[float, int], optional): 超时时间，单位为秒，默认为1秒。
        :returns: None
        """
        pass

    @abstractmethod
    def notify_VehicleInsidePersonSts(self, userInVehicleStatus: bool = False, userInVehicleStatusWithCam: bool = False):
        """
        发送RemoteAuthService:NotifyVehicleInsidePersonSts事件
        :param userInVehicleStatus: (bool, optional): 识别车内是否有人。默认为False。
        :param userInVehicleStatusWithCam: (bool, optional): 与相机相关的识别车内是否有人。默认为False。
        """
        pass

    def check_Play2_req(self, app: str = None,txt: str = None,param: str = None, timeout: Union[float, int] = 0.5):
        """
        监听TCAM是否发出Play2请求
        :param app: (str, optional): 应用名称。默认为None。
        :param txt: (str, optional): 文本内容。默认为None。
        :param param: (str, optional): 参数。默认为None。
        :param timeout: (Union[float, int], optional): 超时时间，单位为秒，默认为0.5秒。
        :returns: None
        """
        pass

     # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_windows_postion(self,pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        """
        调用服务WindowService_client WindowPosition Check窗户的位置改变的通知
        :param pos_drvr (Union[WinPos, None], optional): 主驾窗户位置信息. 默认为None.
        :param pos_pass (Union[WinPos, None], optional): 副驾窗户位置信息. 默认为None.
        :param pos_lere (Union[WinPos, None], optional): 左后窗户位置信息. 默认为None.
        :param pos_rire (Union[WinPos, None], optional): 右后窗户位置信息. 默认为None.
        :returns: None
        """
        pass
    def set_and_cancel_auto_lock_settings(self, settings: Settings, time_wait = 2):
        """
        通过SOAPartner 设置/取消P档自动解锁设置项
        :param settings: 设置模式：
            Set = 0::设置
            CancelSet = 1::取消设置
        :returns: None
        """
        pass
    
    
    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_GB32960Data(self, gb_data: dict = {}):
        """
        通过SOA Partner发送GB32960Service:GB32960Data事件。        
        :param gb_data: (dict, optional): GB32960数据的字典类型，默认为空字典。        
        :Returns: None
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def event_check_windows_postion(self,pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        """
        调用服务WindowService_client WindowPosition Check窗户的位置改变的通知
        :param pos_drvr (Union[WinPos, None], optional): 主驾窗户位置信息. 默认为None.
        :param pos_pass (Union[WinPos, None], optional): 副驾窗户位置信息. 默认为None.
        :param pos_lere (Union[WinPos, None], optional): 左后窗户位置信息. 默认为None.
        :param pos_rire (Union[WinPos, None], optional): 右后窗户位置信息. 默认为None.
        :returns: None
        """
        pass

    # @Author:o_guojing.yang@external.jiduauto.com
    @abstractmethod
    def event_check_NotifyCarLocalTraceActiveStatus(self,
                                      cartrace_sts: CarLocalTraceActiveStatus = CarLocalTraceActiveStatus.kSuccess):
        """
        通过SOA Partner检查寻车功能执行状态KeyService::NotifyCarLoctrActvnSts.sts

        :param cartrace_sts: 远程寻车功能执行状态 kIdle = 0  // 未寻(Default) kSuccess = 1 // 寻车成功 kFail = 2  // 寻车失败 kInvalid =3 // 无效
        :return: 
        """
        pass
    
    @abstractmethod
    def set_maintenanceMode(self, maintenanceMode: bool):
        """
        设置BGM维修模式状态       
        :param maintenanceMode: bool       
        :Returns: None
        """
        pass
    
    @abstractmethod
    def update_InteractiveService_response(self, get_return_args):
        """
        在开启InteractiveService Server端时使用, 用于更新InteractiveService Responese
        
        :param get_return_args: InteractiveService Responese数据       
        :Returns: None
        """
        pass
    
    @abstractmethod
    def stop_send_InteractiveService_response(self):
        """
        关闭InteractiveService Server端
          
        :Returns: None
        """
        pass
    
    @abstractmethod
    def start_send_InteractiveService_response(self):
        """
        开启InteractiveService Server端
          
        :Returns: None
        """
        pass
    
    @abstractmethod
    def on_setPetModeSts(self, partner_key, msg):
        """
        开启InteractiveService Server端
        
        :param partner_key:  指定某个服务，partner作为client和server都可以          
        :Returns: None
        """
        pass
    
    @abstractmethod
    def till_UpdateProcess_event_to(self, master_updateprocess_event_field: MASTER_UpdateProcess_EVENT, target_status=None, timeout=60):
        """
        持续监控FOTA UpdateProcess状态, 直至它回到目标值
        
        :param 枚举类型 MASTER_UpdateProcess_EVENT:
            class MASTER_UpdateProcess_EVENT(BaseEnum):
                taskId = 0
                state = 1
                progress = 2
                leftTime = 3
                errorCode = 4        
        :param target_status: 期望值
        :param timeout: 超时时间        
        :Returns: None
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def hmi_set_and_get_braking_close_the_door(self, isOn: bool, time_wait: Union[float, int] = 1):
        """
        调用SOAPartner设置和获取踩刹车关门设置项状态
        
        :param isOn:  bool
                False = 0:踩设车关门启用
                True = 0:踩设车关门启用
        :param time_wait:  等待时间
        :Returns: None
        """
        pass
    @abstractmethod
    def start_single_partner(self, service: str, role: str, instance: str = None, heartbeat: int = 600):
        """
        起单个服务
        :param service: 类似KeyService_client
        :param role: server
        :param instance:  用于区分不同的Server，比如GNSSService_HD表示ACU的server，GNSSService表示TCAM的server
        :param heartbeat:  通道阻塞检测的心跳
        :return:
        """

    @abstractmethod
    def stop_single_partner(self, partner_key):
        """
        停止某个特定服务
        :param partner_key: 类似KeyService_client
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetConfigList_req(self, name: int = 566, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出请求:CarConfigService:GetConfigList
        :param name: int类型，CCP字节序号
        :param timeout: 超时时间，单位为秒，默认为0.5秒
        :return: None
        """
        pass


    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetConfigList_req(self, ccp_value: int = 0x10):
        """
        通过SOA Partner发送CarConfigService:GetConfigList请求的响应
        :param ccp_value: int类型，CCP字节取值
        :return: None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetConfigList_req_and_feedback_resp(self, name: int = 566, ccp_value: int = 0x10, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出CarConfigService:GetConfigList请求，并发送响应
        :param name: int类型，CCP字节序号
        :param timeout: 超时时间，单位为秒，默认为0.5秒
        :param ccp_value: int类型，CCP字节取值
        :return: None
        """
        pass
        
    # @Author:renyue.dai@jiduatuo.com 
    @abstractmethod
    def update_InteractiveService_response(self, pet_mode_sts: str):
        """
        通过SOA发送InteractiveService获取宠物模式状态请求的响应
        
        :param pet_mode_sts: 是否进入宠物模式（0，1，255表示不在宠物模式）
        :return None
        """
        pass

    # @Author:taiping.zongi@jiduatuo.com
    def notify_NotifyAmbientTempRawData(self, temp: float = 9.0, tempunit: int = 0, is_valid: bool = True):
        """
        通过SOA Partner发送环境温度:ClimateControlService:NotifyAmbientTempRawData通知TCAM  
        :param temp: 温度值(-70~134.7，精度为0.1，)
        :param tempunit:单位为摄氏度
        :param is_valid:有效性
        :return None
        """
        pass
        
    def notify_Temperature(self, climatezoneId: ClimateZoneId = ClimateZoneId.AllZone, temp: float = 10.0, is_valid: bool = True):
        """
        通过SOA Partner发送舱内温度:ClimateControlService:Temperature通知TCAM
        :param climatezoneId:位置id
        :param temp: 温度值(-60~125, 精度为0.1)
        :param is_valid:有效性
        :return None
        """
        pass  

    def check_getAmbientTempRawData_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ClimateControlService:getAmbientTempRawData请求
        :param timeout: 超时时间，单位为秒，默认为0.5秒
        :return: None
        """
        pass

    def response_to_getAmbientTempRawData_req(self, temp: float = 9.0, tempunit: int = 0, is_valid: bool = True):
        """
        通过SOA Partner发送ClimateControlService:getAmbientTempRawData请求的响应
        :param temp: 温度值(-70~134.7，精度为0.1，)
        :param tempunit:单位为摄氏度
        :param is_valid:有效性
        :return None
        """
        pass

    def check_getAmbientTempRawData_req_and_feedback_resp(self, temp: float = 9.0, tempunit: int = 0, is_valid: bool = True, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ClimateControlService:getAmbientTempRawData请求并响应
        :param temp: 温度值(-70~134.7，精度为0.1，)
        :param tempunit:单位为摄氏度
        :param is_valid:有效性
        :param timeout: 超时时间，单位为秒，默认为0.5秒
        :return None
        """
        pass

    def check_GetCurrentTemperature_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ClimateControlService:GetCurrentTemperature请求
        :param timeout: 超时时间，单位为秒，默认为0.5秒
        :return: None
        """
        pass

    def response_to_GetCurrentTemperature_req(self, zone_id: ClimateZoneId = ClimateZoneId.AllZone, temp: float = 9.0, is_valid: bool = True):
        """
        通过SOA Partner发送ClimateControlService:GetCurrentTemperature请求的响应
        :param zone_id:位置id
        :param temp: 温度值(-60~125, 精度为0.1)
        :param is_valid:有效性
        :return None
        """
        pass

    def check_GetCurrentTemperature_req_and_feedback_resp(self, zone_id: ClimateZoneId = ClimateZoneId.AllZone, temp: float = 9.0, is_valid: bool = True, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出ClimateControlService:GetCurrentTemperature请求并响应
        :param zone_id:位置id
        :param temp: 温度值(-60~125, 精度为0.1)
        :param is_valid:有效性
        :param timeout: 超时时间，单位为秒，默认为0.5秒
        :return None
        """
        pass

    def check_Temperature_req_and_feedback_resp(self, s: int= 1, ambienttemp: float = 9.1, temp: float = 10.0, is_valid: bool = True):
        """
        通过SOA Partner监听TCAM是否发出ClimateControlService:getAmbientTempRawData、ClimateControlService:GetCurrentTemperature请求并响应
        :param s:通过SOA Partner监听TCAM发出信息的次数，int类型
        :param ambienttemp: 环境温度值(-70~134.7，精度为0.1，)
        :param temp: 舱内温度值(-60~125, 精度为0.1)
        :param is_valid:有效性
        :return None
        """
        pass
    
    # @Author:qian.feng@jiduatuo.com 
    @abstractmethod
    def hmi_set_glove_box_active_req(self, settype: SetType, time_wait: Union[float, int] = 2):
        """
        通过SOA Partner GloveBoxService_client设置手套箱开启    
        :param settype: 设置类型
        :param time_wait: 等待时间
        :return: None
        """
        pass

    # @Author:qian.feng@jiduatuo.com  
    def hmi_check_notify_key_connect_sts(self, keytype: KeyType, isconnect: bool, time_wait: Union[float, int] = 2):
        """
        通过SOA Partner KeyService_client校验钥匙连接类型及连接状态    
        :param keytype: 钥匙类型
        :param isconnect: 钥匙连接状态bool类型
            False = 0::无钥匙未连接
            True = 1::有钥匙连接
        :param time_wait: 等待时间
        :return: None
        """
        pass
        
        
    # @Author:xiangyue.li@jiduauto.com  
    @abstractmethod
    def set_findkey_req(self, findzone: FindZone):
        '''
        设置钥匙区域请求
        '''   

    # @Author:xiangyue.li@jiduauto.com  
    @abstractmethod
    def reset_soa_config(self):
        '''
        设置随车设置项初始化
        '''   
        
    # @Author:xiangyue.li@jiduauto.com  
    @abstractmethod
    def event_check_reset_vehicle_sts(self, state: MainState, notify: Notification, telestate:TeleState, autoState:AutoState, cockpitState:CdcState, digitalKeyState:BncmState):
        '''
        整车重启状态通知
        '''   

    # @Author:o_guojing.yang@jiduatuo.com
    @abstractmethod
    def set_and_frntleft_heat_sts(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):
        """
        通过SOA Partner发送主驾座椅加热通风状态事件:SeatService:FrntLeftSeatHeatVentStatus
        :param heat_level: 座椅的加热等级, 整形
        :param heat_time: 座椅的加热时间, 整形, 单位min
        :param heat_work_sts: 加热通风状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param vent_level: 通风等级, 整形
        :param vent_time: 通风时间, 整形, 单位min
        :param vent_work_sts: 加热通风状态, 枚举值
        :return:
        """
        pass

    # @Author:o_guojing.yang@jiduatuo.com
    @abstractmethod
    def set_and_frntringht_heat_sts(self, heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 15,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 15,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.Off):
        """
        通过SOA Partner发送副驾座椅加热通风状态事件:SeatService:FrntRightSeatHeatVentStatus
        :param heat_level: 座椅的加热等级, 整形
        :param heat_time: 座椅的加热时间, 整形, 单位min
        :param heat_work_sts: 加热通风状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param vent_level: 通风等级, 整形
        :param vent_time: 通风时间, 整形, 单位min
        :param vent_work_sts: 加热通风状态, 枚举值
        :return:
        """
        pass

    # @Author:o_guojing.yang@jiduatuo.com
    @abstractmethod
    def event_check_frntleft_heat_sts(heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 59,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 59,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone):
        """
        check 主驾座椅加热通风状态事件:SeatService:FrntLeftSeatHeatVentStatus
        :param heat_level: 座椅的加热等级, 整形
        :param heat_time: 座椅的加热时间, 整形, 单位min
        :param heat_work_sts: 加热通风状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param vent_level: 通风等级, 整形
        :param vent_time: 通风时间, 整形, 单位min
        :param vent_work_sts: 加热通风状态, 枚举值
        :return:
        """
        pass

    # @Author:o_guojing.yang@jiduatuo.com
    @abstractmethod
    def event_check_frntringht_heat_sts(heat_level: HeatLevel = HeatLevel.Off, heat_time: int = 59,
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone,
                                                vent_level: VentLevel = VentLevel.Off, vent_time: int = 59,
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone):
        """
        check 副驾座椅加热通风状态事件:SeatService:FrntRightSeatHeatVentStatus
        :param heat_level: 座椅的加热等级, 整形
        :param heat_time: 座椅的加热时间, 整形, 单位min
        :param heat_work_sts: 加热通风状态, 枚举值, 取值范围: kNone = 0 On = 1 Off = 2 Error = 3 FunctionLimit = 4 EnergyLimit = 5 Reserved1 = 6 Reserved2 = 7
        :param vent_level: 通风等级, 整形
        :param vent_time: 通风时间, 整形, 单位min
        :param vent_work_sts: 加热通风状态, 枚举值
        :return:
        """
        pass

    # @Author:o_guojing.yang@jiduatuo.com
    @abstractmethod
    def rvc_set_seat_vent_level(self, pos: SeatId, level: HeatVentiLvl, source:SourceId):
        """
        设置座椅通风等级

        :param pos: 设置座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :source : 请求源 Idle = 0 HMI = 1 Remote = 2
        :return:
        """
        pass

    # @Author:o_guojing.yang@jiduatuo.com
    @abstractmethod
    def rvc_set_seat_heat_level(self, pos: SeatId, level: HeatVentiLvl, source:SourceId):
        """
        设置座椅加热等级

        :param pos: 设置座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :source : 请求源 Idle = 0 HMI = 1 Remote = 2
        :return:
        """
        pass

    # @Author:qian.feng@jiduatuo.com  
    def check_envent_unlocking_action_sts(self, sourceid: LockTrigerSource, time_wait: Union[float, int] = 0):
        """
        通过SOA Partner LockActTriggerSource接口校验当前解闭锁动作触发源通知状态   
        :param sourceid: 对应解闭锁动作触发源
        :param time_wait: 等待时间默认为0
        :return: None
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_auto_calibration(self, req: calibration_req=calibration_req.KOn, ID: int=0, source:SourceType=SourceType.kScreen, isAlloweSkip:bool=False):
        """
        设置智能标定
        
        :param req: 设置标定状态 kOff = 0 KOn = 1
        :param ID: 智能标定的对象 目前 0 是充电口盖标定
        :param source: 请求源 语音kVoicd = 0 屏幕kScreen = 1 远程kRemote = 2
        :param isAlloweSkip: 是否允许跳过授权
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_Calibration_Authorization(self, req: Authorization_req=Authorization_req.kAuthorize):
        """
        设置智能标定授权
        
        :param req: 请求智能标定授权 用户授权kAuthorize = 0 取消用户授权kCancelAuthorize = 1
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_Calibration_Retry(self, req: retry_req=retry_req.kRetry):
        """
        触发重试智能标定
        
        :param req: 请求重试智能标定 取消重试kCancel = 0 请求重试kRetry = 1
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def event_check_Calibration_Status_Info(self,text_id: int=255, ID: int=0, status: calibration_status=calibration_status.kIdle):
        """
        获取标定状态事件上报
        
        :param text_id: 提示信息 目前只有21 充电口标定前置条件失败
        :param ID: 智能标定的对象 目前 0 是充电口盖标定
        :param status: 标定状态 
            kIdle = 0 
            kStartRunning = 1
            kAuthorization = 2
            kCheckPreconditionFailed = 3
            kCalibrationRunning = 4
            kCalibrationSuccess = 5
            kCalibrationFailed = 6
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def get_Calibration_Status_Info(self,text_id: int=255, ID: int=0, status: calibration_status=calibration_status.kIdle):
        """
        请求并校验标定状态
        
        :param text_id: 提示信息 目前只有21 充电口标定前置条件失败
        :param ID: 智能标定的对象 目前 0 是充电口盖标定
        :param status: 标定状态 
            kIdle = 0 
            kStartRunning = 1
            kAuthorization = 2
            kCheckPreconditionFailed = 3
            kCalibrationRunning = 4
            kCalibrationSuccess = 5
            kCalibrationFailed = 6
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def event_check_Calibration_Result_Info(self, ID: int=0, errorCode: calibration_error_code=calibration_error_code.kSuccess):
        """
        获取标定结果事件上报
        
        :param ID: 智能标定的对象 目前 0 是充电口盖标定
        :param errorCode: 标定结果 
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
        :return:
        """

    def get_fota_notifybookinfolist(self, master_NotifyBookInfoListEVENT_field: NotifyBookInfoListEVENT):        
        """
        通过SOA Partner监听RtcAlarmService_client::NotifyBookInfoList  
        :param master_NotifyBookInfoListEVENT_field: 事件通知参数
        :return: 指定参数对应的值
        """
        pass

    def send_cancel_service_book_event(self, service_name: str):
        """
        通过SOA Partner监听RtcAlarmService_client::CancelServiceBookEvent  
        :param service_name: 调用服务方
        :return: None
        """
        pass


    # @Author:guojing.yang@jiduatuo.com  
    def check_notify_key_connect_sts(self, keytype: KeyType, isconnect: bool, keyid: list, zone: BLEKeyPrsntZone, battwarbsts:bool = False, time_wait: Union[float, int] = 2):
        """
        通过SOA Partner KeyService_client校验钥匙连接类型及连接状态    
        :param keytype: 钥匙类型
        :param isconnect: 钥匙连接状态bool类型
            False = 0::无钥匙未连接
            True = 1::有钥匙连接
        :param keyid::钥匙ID
        :param zone::该钥匙槽定位的区域
        :param battwarbsts::当前钥匙电量是否有报警信息
        :param time_wait: 等待时间
        :return: None
        """
        pass

    # @Author:guojing.yang@jiduatuo.com  
    def check_central_lock_sts_info(self, lock_sts:LockStatus, trigger_srcid:TriggerSourceId, timeout=1):
        """
        通过SOA Partner CentralLockService_client校验中控锁系统状态    
        :param lock_sts: 锁状态
        :param trigger_srcid: 中控锁触发原因
        :param time_wait: 等待时间
        :return: None
        """
        pass
    
    @abstractmethod
    def check_no_GetSeatHeatVentStatus_req(self, timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM不会发出SeatService:GetSeatHeatVentStatus请求        
        :param timeout: 监听超时时间，整形或浮点型
        :return: 
        """
        pass

    # @Author:guojing.yang@jiduatuo.com  
    def check_Remote_Climate_Status(self, status: RemClimateSts):
        """
        通过SOA Partner ClimateControlService_client校验空调开启关闭状态 
        :param status: 空调开启关闭状态
        :return: None
        """
        pass

    # @Author:jianwen.wang@jiduatuo.com  
    def start_send_GetHVSOCInfo_response(self):
        """
        通过SOA Partner发送HighVoltageService_server:GetHVSOCInfo的响应
        :return:
        """

    # @Author:jianwen.wang@jiduatuo.com  
    def start_send_GetHVBatterySOH_response(self):
        """
        通过SOA Partner发送HighVoltageService_server:GetHVBatterySOH的响应
        :return:
        """

    # @Author:jianwen.wang@jiduatuo.com  
    def start_send_GetRange_response(self):
        """
        通过SOA Partner发送HighVoltageService_server:GetRange的响应
        :return:
        """

    
    # @Author:jianwen.wang@jiduatuo.com  
    def start_send_GetBatteryStatus_response(self):
        """
        通过SOA Partner发送LowVoltageService_server:GetBatteryStatus的响应
        :return:
        """

    # @Author:guojing.yangu@jiduatuo.com
    @abstractmethod
    def check_lock_status(self, lock_sts: LockSts):
        """
        通过SOA Partner发出解闭锁的状态CentralLockService::LockStatus.sts

        :param lock_sts: 整车锁状态 kUndef = 0 //Default kUnlocked = 1 //解锁 kFourDoorLockedTailUnlocked = 2 //四门上锁但尾门解锁 kAllLocked = 3 //四门上锁且尾门上锁
        :return: 
        """
        pass

    # @Author:taiping.zong@jiduatuo.com 
    def check_SetMaxCoolingCtrl_req(self, onOffCmd: bool = True, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出极速制冷开启请求:ClimateControlService:SetMaxCoolingCtrl    
        :param onOffCmd: 极速制冷开启关闭请求bool类型
        :return: None
        """

    # @Author:taiping.zong@jiduatuo.com 
    def check_SetMaxHeatingCtrl_req(self, onOffCmd: bool = True, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner监听TCAM是否发出极速制热开启请求:ClimateControlService:SetMaxHeatingCtrl  
        :param onOffCmd: 极速制热开启关闭请求bool类型
        :return: None
        """
        
    # @Author:taiping.zong@jiduatuo.com 
    def notify_MaxCoolingHeatingInfo(self, maxCoolingSts: bool = True, maxHeatingSts: bool = True):
        """
        通过SOA Partner发送ClimateControlService:MaxCoolingHeatingInfo 制冷状态为{maxCoolingSts}制热状态为{maxHeatingSts}  
        :param maxCoolingSts: 极速制热开启关闭状态bool类型，默认开启
        :param maxHeatingSts: 极速制热开启关闭状态bool类型，默认开启
        :return: None
        """

    @abstractmethod
    def get_internal_light_mode(self, mode: LightMode):
        """
        获取内灯模式

        @param mode: 内灯模式 Off=0 On=1 Auto=2
        @return:
        """
        pass
    
    # @Author:guojing.yang@jiduatuo.com 
    def set_Max_Cooling_Ctrl(self, onOffCmd: bool = True):
        """
        设置急速制冷开启/关闭  
        :param onOffCmd: 极速制冷开启关闭请求bool类型
            ture:打开，false:关闭
        :return
        """

    # @Author:guojing.yang@jiduatuo.com 
    def set_Max_Heating_Ctrl(self, onOffCmd: bool = True):
        """
        设置急速制热开启/关闭  
        :param onOffCmd: 极速制热开启关闭请求bool类型
            ture:打开，false:关闭
        :return
        """

    # @Author:guojing.yang@jiduatuo.com 
    def check_max_cooling_heating_info(self, maxCoolingSts: bool = True, maxHeatingSts: bool = True):
        """
        通过SOA Partner发送ClimateControlService:MaxCoolingHeatingInfo 校验制冷状态为{maxCoolingSts}制热状态为{maxHeatingSts}  
        :param maxCoolingSts: 极速制热开启关闭状态bool类型，默认开启
        :param maxHeatingSts: 极速制热开启关闭状态bool类型，默认开启
        :return: None
        """

  # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def set_child_lock_unlock_req(self, doorid: DoorId, childlockreq: ChildLockReq, time_wait: Union[float, int] = 0):
        """
        通过SOA Partner设置对应侧门儿童锁上锁解锁
        :param doorid: 需要设置的侧门ID
        :param childlockreq: 儿童锁上锁解锁请求
        :return: None
        """
        pass
    
    @abstractmethod
    def notify_ThermalSystemDeviceFaultInfo(self, device: DeviceType=DeviceType.kAll, faultSts:ThermalFaultSts=ThermalFaultSts.kNormal):
        """
        通过SOA Partner模拟BGM发送HighVoltageService:ThermalSystemDeviceFaultInfo事件通知
        :param device: 设备类型 枚举值
        :param faultSts: 故障状态 枚举值
        :return: 
        """
        pass
		

    @abstractmethod
    def check_NotifyRemoteBatteryHeatingInfo_event(self,modeSts:RemoteBatteryHeatingModeSts = RemoteBatteryHeatingModeSts.kIdle ,heatSts:RemoteBatteryHeatingSts = RemoteBatteryHeatingSts.kOff ,
                                                   source:HeatingEnergySource = HeatingEnergySource.kNone ,timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出 RemoteCtrlService_client:NotifyRemoteAuthStartSts事件通知

        :param modeSts: 远程电池加热模式 RemoteBatteryHeatingModeSts.kIdle
        :param heatSts: 远程电池加热状态 RemoteBatteryHeatingSts.kOff
        :param source: 加热取电能量源 RemoteBatteryHeatingSts.kNone
        :param timeout: 监听超时时间, 单位s, 浮点型或者整形
        :return:
        """
        pass


    def ck_event_and_resp(self, partner_key: str, event_name: str, event_info: dict,
                          method_name=None, method_args=None, resp_info=None,
                          timeout=3, fuzz_match=True):
        """
        校验历史event，并调用get获取结果
        :param partner_key: 类似KeyService_Server
        :param event_name: 待校验event接口名
        :param event_info: 待校验event的数据
        :param method_name: 请求的接口名，默认直接按event前面加Get调用调用
        :param method_args: 请求接口的入参，默认不传
        :param resp_info: 请求的预期响应结果
        :param timeout: 等待预期的event超时
        :param fuzz_match: 是否模糊匹配
        """

  # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def event_check_side_door_open_protection_sts(self, frontleft: Union[bool, int] = None,
                                                  frontrigiht: Union[bool, int] = None,
                                                  rearleft: Union[bool, int] = None,
                                                  rearright: Union[bool, int] = None,
                                                  time_wait: Union[float, int] = 0):
        """
        通过SOAPartner校验侧方开门预警
        :param frontleft: 左前车门
        :param frontrigiht: 右前车门
        :param rearleft: 左后车门
        :param rearright: 右后车门
        :param time_wait: 等待时间默认0
        """

  # @Author:shulin.zheng@jiduatuo.com       
    def check_Light_ShowActivate_Status(self, status: bool ):
        """
        检测BGM发送灯光秀激活/禁用事件:
        :param status:  灯光秀激活状态, 布尔        
        :return: 
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetSpeed_req(self, timeout=1):
        """
        通过SOA Partner监听TCAM是否发出ChassisService:GetSpeed请求。
        
        Args:
            timeout (int, optional): 监听超时时间，默认为1秒。
        
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def response_to_GetSpeed_req(self, speed: float = 0, is_valid: bool = True):
        """
        通过SOA Partner响应ChassisService:GetSpeed请求
        
        Args:
            speed (float, optional): 速度值. 默认为0.
            is_valid (bool, optional): 是否有效. 默认为True.
        
        Returns:
            None
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_GetSpeed_req_and_feedback_resp(self, speed: float = 0, is_valid: bool = True, timeout: Union[float, int] = 0.5):
        """
        Args:
            speed (float, optional): 返回的速度值. Defaults to 0.
            is_valid (bool, optional): 是否为有效速度值. Defaults to True.
            timeout (Union[float, int], optional): 超时时间. Defaults to 0.5.
        
        Returns:
            None
        
        Raises:
            无
        
        功能：
            发送ChassisService:GetSpeed请求并回复对应的响应
        
        调用方式：
            self.check_GetSpeed_req_and_feedback_resp(speed, is_valid, timeout)
        
        详细描述：
            该方法主要用于发送获取速度值的请求并返回相应的响应，参数包括速度值、是否为有效速度值以及超时时间。
            方法首先通过logger输出日志信息，然后调用check_GetSpeed_req方法发送请求，
            接着调用response_to_GetSpeed_req方法返回对应的响应。
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def notify_NotifyChargingEquipmentInformation(self, max_current: float = 3.8, actual_current: float = 4.0,
                                                  equipment_types: list = [3], charge_power: float = 300.0):
        """
        通过SOA Partner发送HighVoltageService:NotifyChargingEquipmentInformation事件通知
        
        Args:
            max_current (float, optional): 最大电流值，默认为3.8A。
            actual_current (float, optional): 实际电流值，默认为4.0A。
            equipment_types (list, optional): 充电设备类型列表，默认为[3]。
            charge_power (float, optional): 充电功率，默认为300.0W。
        
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_RemoteBatteryHeatingInfo(self, modests: RemoteBatteryHeatingModeSts = RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                              heatsts: RemoteBatteryHeatingSts = RemoteBatteryHeatingSts.kOff,
                                              source: HeatingEnergySource = HeatingEnergySource.kNone, timeout: Union[float, int] = 0.5):
        """
        通过SOA Partner检查TCAM是否发送RemoteCtrlService:RemoteBatteryHeatingInfo事件通知
        
        Args:
            modests (RemoteBatteryHeatingModeSts, optional): 电池加热模式状态，默认为RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat
            heatsts (RemoteBatteryHeatingSts, optional): 电池加热状态，默认为RemoteBatteryHeatingSts.kOff
            source (HeatingEnergySource, optional): 加热能量来源，默认为HeatingEnergySource.kNone
            timeout (Union[float, int], optional): 超时时间，默认为0.5
        
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def battery_protect_exect_planb(self, value: float = -28.0, source: HeatingEnergySource = HeatingEnergySource.kHVBattery,
                                          modests: RemoteBatteryHeatingModeSts = RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat,
                                          heatsts: RemoteBatteryHeatingSts = RemoteBatteryHeatingSts.kOn):
        """
        执行电池保护计划B
        
        Args:
            value (float, optional): 电池温度值，默认为-28.0.
            source (HeatingEnergySource, optional): 加热能量来源，默认为HeatingEnergySource.kHVBattery.
            modests (RemoteBatteryHeatingModeSts, optional): 电池加热模式状态，默认为RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat.
            heatsts (RemoteBatteryHeatingSts, optional): 电池加热状态，默认为RemoteBatteryHeatingSts.kOn.
        
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_no_SetCharging_req(self, timeout: Union[float, int]):
        """
        监听TCAM不会发出HighVoltageService_server:SetCharging请求
        
        Args:
            timeout (Union[float, int]): 监听超时时间
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_no_RemoteBatteryHeatingInfo(self, timeout: Union[float, int] = 0.5):
        """
        检查TCAM是否未发送RemoteCtrlService:RemoteBatteryHeatingInfo事件通知。
        
        Args:
            timeout (Union[float, int], optional): 超时时间，默认为0.5秒。
        
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    def battery_protect_exect_plana(self, min_temp: float = -31.0, acdc_type: ACDCType = ACDCType.kDC,
                                          plug_sts1: PluggerSts = PluggerSts.Disconnected,
                                          plug_sts2: PluggerSts = PluggerSts.ConnectedWithPower,
                                          value: float = -28.0, thermal_sts: ThermalReqSts = ThermalReqSts.Heating,
                                          modests: RemoteBatteryHeatingModeSts = RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat):
        """
        电池保护执行Plan A方案
        
        Args:
            min_temp (float, optional): 电池最低温度，默认为-31.0.
            acdc_type (ACDCType, optional): ACDC类型，默认为ACDCType.kDC.
            plug_sts1 (PluggerSts, optional): 插头状态1，默认为PluggerSts.Disconnected.
            plug_sts2 (PluggerSts, optional): 插头状态2，默认为PluggerSts.ConnectedWithPower.
            value (float, optional): 目标加热温度值，默认为-28.0.
            thermal_sts (ThermalReqSts, optional): 热请求状态，默认为ThermalReqSts.Heating.
            modests (RemoteBatteryHeatingModeSts, optional): 远程加热请求模式状态，默认为RemoteBatteryHeatingModeSts.kLowTemperatureSelfHeat.
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_NotifyACDefrostSts(self, defrost_max: bool = False, climate_defrost: bool = False):
        """
        check除霜状态事件通知:ClimateControlService:NotifyACDefrostSts

        :param defrost_max: 最大除霜状态, 布尔型
        :param climate_defrost: 除霜工作状态, 布尔型
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def battery_protect_exect_planB_by_stage_wait_HVActiveSts(self, min_temp: float = -31.0):
        """
        根据阶段等待HVActiveSts执行低温自保护PlanB方案
        
        Args:
            min_temp (float, optional): 最低温度阈值. 默认为-31.0.
        
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def battery_protect_exect_planB_by_stage_wait_ThermalReqSts(self, min_temp: float = -31.0, value: float = -28.0):
        """
        按照阶段等待ThermalReqSts执行低温保护方案B
        
        Args:
            min_temp (float, optional): 最低温度阈值，默认为-31.0摄氏度.
            value (float, optional): 加热请求值，默认为-28.0摄氏度.
        
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_battery_protect_planB_stoped_with_HVActiveSts_closed(self):
        """
        检查电池保护方案B是否已停止且高压系统已关闭。
        
        Args:
            无。
        
        Returns:
            无返回值，若执行过程中出现问题则会抛出异常。
        
        Raises:
            异常类型未定义，可能会根据实际执行情况抛出不同的异常。
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_battery_protect_planB_stoped_with_ThermalReqSts_heating(self):
        """
        检查电池保护方案B是否因ThermalReqSts.Heating停止
        
        Args:
            无
        
        Returns:
            无
        
        Raises:
            无
        
        该函数会执行以下操作：
        1. 调用 notify_BatteryHeatingInfo 函数，发送 ThermalReqSts.Heating 的请求状态。
        2. 调用 soa_partner 的 empty_all 函数，清空 soa_partner 中的数据。
        3. 调用 check_no_RemoteBatteryHeatingInfo 函数，检查在指定超时时间内是否没有收到 RemoteBatteryHeatingInfo 消息。
        4. 调用 check_no_SetOutput_req 函数，检查在指定超时时间内是否没有收到 SetOutput_req 消息。
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def battery_protect_exect_planA_DC_by_stage_SetCharging(self, min_temp: float = -31.0, value: float = -28.0):
        """
        执行PlanA DC充电阶段下的电池保护策略，设置充电信息
        
        Args:
            min_temp (float, optional): 最小温度值，默认为-31.0。
            value (float, optional): 加热请求值，默认为-28.0。
        
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def battery_protect_exect_planA_by_stage_wait_pluggerStatus(self, min_temp: float = -31.0, value: float = -28.0 , 
                                                                      acdc_type: ACDCType = ACDCType.kDC):
        """
        执行低温保护方案A根据阶段等待充电枪状态
        
        Args:
            min_temp (float, optional): 最低温度阈值，默认为-31.0.
            value (float, optional): 加热请求值，默认为-28.0.
            acdc_type (ACDCType, optional): 电源类型，默认为ACDCType.kDC.
        
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_battery_protect_planA_stoped_with_PluggerSts_ConnectedWithPower_and_ThermalReqSts_Heating(self, acdc_type: ACDCType = ACDCType.kDC):
        """
        检查执行方案A时加热停止
        
        Args:
            acdc_type (ACDCType, optional): 电源类型，默认为ACDCType.kDC，表示直流电源。
        
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_NotifyPrepareTimeUpEventInfo_event(self, service_name: str = "rvcsubscribe", timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出RtcAlarmService_client:NotifyPrepareTimeUpEventInfo事件
        
        Args:
            service_name (str, optional): 服务名称，默认为"rvcsubscribe"。
            timeout (Union[float, int], optional): 超时时间，默认为1秒。
        
        Returns:
            None
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_NotifyTimeUpEventInfo_event(self, service_name: str = "rvcsubscribe", timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出RtcAlarmService_client:NotifyTimeUpEventInfo事件
        
        Args:
            service_name (str, optional): 服务名称，默认为"rvcsubscribe"。
            timeout (Union[float, int], optional): 超时时间，单位为秒，支持浮点数和整数，默认为1。
        
        Returns:
            None
        
        """
        pass

  # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def get_and_check_door_action_req(self, checktype: CheckInterfaceType, doorid: DoorId, dooraction:DoorAction, triggerId:DoorActionTriggerId, time_wait: Union[float, int] = 0):
        """
        通过SOAPartner校验通知和获取对应车门动作请求和车门动作触发源为请求
        :param checktype: 需要校验的类型
            Get  = 0
            CheckNotify = 1
            All = 2
        :param doorid: 需要校验的对应侧门
        :param dooraction: 车门动作请求
            Idle = 0
            Open = 1
            Close = 2
            Stop = 3
            OpenMinAngle = 4
            Invalid = 255
        :param triggerId: 车门动作请求触发源
            NoTriggerSource = 0
            RemoteKey = 1
            HMI = 2
            Telematices = 3
            OutsideSwitch = 4
            InsideSwitch = 5
            Unknown = 255
        :return: 
        """
        pass

    @abstractmethod
    def ctrl_mul_alm_illuminate(self, bright, r, g, b, zoneid_lst: List[ALMZoneId]):
        """
        控制普通氛围灯亮灭及颜色

        @param b: 颜色b
        @param g: 颜色g
        @param r: 颜色r
        @param bright: 氛围灯亮度
        @param zoneid_lst: 氛围灯灯带列表
        1 - FrontLeft
        2 - FrontRight
        3 - RearLeft
        4 - RearRight
        17 - TweeterLeft
        18 - TweeterRight
        19 - CCLeft
        20 - CCRight
        29 - CCMiddleRight
        30 - CCMiddleLeft
        31 - CCUnder
        @return:
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def get_and_check_Pressure(self,tyres: tyres=tyres.kTyreFrintLeft, pressure: float=200):
        """
        请求指定位置的胎压
        
        :param tyres: 轮胎位置
            kTyreFrintLeft = 0
            kTyreFrintRight = 1
            kTyreRearLeft = 2
            kTyreRearRight = 3
            kTyreAll = 4
        :param pressure: 胎压
        :return:
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def get_and_check_Temperature(self,tyres: tyres=tyres.kTyreFrintLeft, temperature: int=64):
        """
        请求指定位置的胎温
        
        :param tyres: 轮胎位置
            kTyreFrintLeft = 0
            kTyreFrintRight = 1
            kTyreRearLeft = 2
            kTyreRearRight = 3
            kTyreAll = 4
        :param temperature: 胎温
        :return:
        """
        pass

    def get_and_set_outerdoorswlight_mode(self,target_doorid:DoorId,target_mode:OutDoorSwitchLightMode,target_sts:isOn):
        """
        通过SOAPartner获取当前的门板指示灯模式
        :param target_doorid: 门ID
            kDoorFrontLeft = 0
            kDoorFrontRight = 1
            kDoorRearLeft = 2
            kDoorRearRight = 3
            kDoorAll = 4
        :param target_mode: 门板指示灯模式
            kModeOff = 0
            kOnStatic = 1
            kOnDynamic = 2
        :param target_sts: 门板指示灯开关状态
            Off = False
            On = True
        :return: 
        """
        pass

    # @Author:shulin.zheng@jiduauto.com
    def response_to_GetBookChargingInfo_req(self,source: HV_SourceId,reqSts: ACBookChargingReqSts,workSts: ACBookChargingWorkSts,
                                            startTime: int,endTime: int,repeatType: CoolgReq,isToTargetSOCStop: bool):
        """
        通过SOA Partner发送预约充电预约信息。        
        :SourceId 请求源    (0)kDefault-默认调用方信息 (1)kVoiceControl-语音控制 (2)kScreenControl-屏幕控制 (3)kRemoteControl-远程控制 (4)kBlueTooth-蓝牙控制  (5)kFota-Fota控制。        
        :reqSts: 请求状态   Default(0)-kDefault,  预约开启本次有效(1)-kBookActive,  预约开启本次无效(2)-kBookDeactive,  预约关闭(3)-kBookOff。
        :workSts: 工作状态         
        :startTime: 预约开始时间 字符串标准时间
        :endTime: 预约结束时间 字符串标准时间
        :repeatType: 重复类型          
        """
        pass
    
    def event_to_BookChargingInfo(self,source: HV_SourceId,reqSts: ACBookChargingReqSts,workSts: ACBookChargingWorkSts,
                                            startTime: int,endTime: int,repeatType: CoolgReq,isToTargetSOCStop: bool):
        """
        检测SOA Partner发送预约充电预约信息。        
        :SourceId 请求源    (0)kDefault-默认调用方信息 (1)kVoiceControl-语音控制 (2)kScreenControl-屏幕控制 (3)kRemoteControl-远程控制 (4)kBlueTooth-蓝牙控制  (5)kFota-Fota控制。        
        :reqSts: 请求状态   Default(0)-kDefault,  预约开启本次有效(1)-kBookActive,  预约开启本次无效(2)-kBookDeactive,  预约关闭(3)-kBookOff。
        :workSts: 工作状态         
        :startTime: 预约开始时间 字符串标准时间
        :endTime: 预约结束时间 字符串标准时间
        :repeatType: 重复类型          
        """
        pass
    
    def response_to_GetDisplayBookChargingInfo_req(self,type: DisplayBookChargingType,startTime ,endTime ):
        """
        通过SOA Partner发送预约充电显示信息。        
        :type: 预约类型     不显示预约充电 -kNoDisplay, 交流充电预约 -(1) kAC, 直流充电预约-kDC
        :startTime: 预约开始时间 数组格式[年,月,日,时,分,秒]
        :endTime: 预约结束时间 数组格式[年,月,日,时,分,秒]
        """
        pass
     
    def check_Light_ShowActivate_Status(self, status: bool ):
        """
        检测BGM发送灯光秀激活/禁用事件:
        :param status:  灯光秀激活状态, 布尔        
        :return: 
        """
        pass

    def set_SetACBookCharging_req(self, type: CommandType,source: HV_SourceId,startTime,endTime,repeatType: CoolgReq,isToTargetSOCStop: bool):
        """
        通过SOA Partner发送预约充电显示信息。        
        :type: 预约类型     不显示预约充电 -kNoDisplay, 交流充电预约 -(1) kAC, 直流充电预约-kDC
        :source: 请求源    (0)kDefault-默认调用方信息 (1)kVoiceControl-语音控制 (2)kScreenControl-屏幕控制 (3)kRemoteControl
        :startTime: 预约开始时间 数组格式[年,月,日,时,分,秒]
        :endTime: 预约结束时间 数组格式[年,月,日,时,分,秒]
        :repeatType: 重复类型  
        :isToTargetSOCStop: 是否到目标SOC停止       
        """
        pass

    def response_to_GetBookChargingTime_req(self, type: DisplayBookChargingType,type1: HV_SourceId,startTime,endTime):
        """
        通过SOA Partner发送预约充电显示信息。        
        :type: 预约类型     不显示预约充电 -kNoDisplay, 交流充电预约 -(1) kAC, 直流充电预约-kDC
        :source: 请求源    (0)kDefault-默认调用方信息 (1)kVoiceControl-语音控制 (2)kScreenControl-屏幕控制 (3)kRemoteControl
        :startTime: 预约开始时间 数组格式[年,月,日,时,分,秒]
        :endTime: 预约结束时间 数组格式[年,月,日,时,分,秒]
        :repeatType: 重复类型  
        :isToTargetSOCStop: 是否到目标SOC停止       
        """
        pass
    
    def check_BookChargingTime(self, type: DisplayBookChargingType,startTime,endTime):
        """
        通过SOA Partner发送预约充电显示信息。        
        :type: 预约类型     不显示预约充电 -kNoDisplay, 交流充电预约 -(1) kAC, 直流充电预约-kDC
        :source: 请求源    (0)kDefault-默认调用方信息 (1)kVoiceControl-语音控制 (2)kScreenControl-屏幕控制 (3)kRemoteControl
        :startTime: 预约开始时间 数组格式[年,月,日,时,分,秒]
        :endTime: 预约结束时间 数组格式[年,月,日,时,分,秒]
        :repeatType: 重复类型  
        :isToTargetSOCStop: 是否到目标SOC停止       
        """
        pass

    def ctrl_wireless_charge(self, zone: WPCZoneId, sts: isOn):
        """
        控制无线充电功能打开/关闭
        @param zone: 无线充电区域
        @param sts: 无线充电打开/关闭状态
        @return:
        """

    def check_wireless_inform(self,
            isforgotten: WPCIsForgotten = WPCIsForgotten.NotForgotten,
            ctrlsts: WPCCtrlSts = WPCCtrlSts.Enable,
            chargingsts: WPCChargingSts = WPCChargingSts.Standby,
            faultid: WPCFaultsId = WPCFaultsId.Ok,
    ):
        """
        单无线充电区域通知
        @param isforgotten: 手机遗留通知
        @param ctrlsts: 功能反馈通知
        @param chargingsts: 充电状态通知
        @param faultid: 故障通知
        @return:
        """
        pass

    def check_two_wireless_inform(
            self,
            isforgotten: WPCIsForgotten,
            ctrlsts: WPCCtrlSts,
            chargingsts: WPCChargingSts,
            faultid: WPCFaultsId,
            isforgotten_pass: WPCIsForgotten,
            ctrlsts_pass: WPCCtrlSts,
            chargingsts_pass: WPCChargingSts,
            faultid_pass: WPCFaultsId,
    ):
        """
        双无线充电区域通知
        @param isforgotten: 主驾侧手机遗留通知
        @param ctrlsts: 主驾侧功能反馈通知
        @param chargingsts: 主驾侧充电状态通知
        @param faultid: 主驾侧故障通知
        @param isforgotten_pass: 副驾侧手机遗留通知
        @param ctrlsts_pass: 副驾侧功能反馈通知
        @param chargingsts_pass: 副驾侧充电状态通知
        @param faultid_pass: 副驾侧故障通知
        @return:
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_no_NotifyTimeUpEventInfo(self, timeout: Union[float, int]):
        """
        监听TCAM不会发出RtcAlarmService_server:NotifyTimeUpEventInfo事件
        
        Args:
            timeout (Union[float, int]): 监听超时时间
        
        Returns:
            None
        
        """
        pass

    @abstractmethod
    def trigger_fota_type70(self, taskid: int):
        """
        模拟云端取消
        
        :param taskid: 当前任务id
        :returns: NA
        :raises keyError: NA
        """

    @abstractmethod
    def check_DriveSts_event_period(self, target_period: Union[float, int], epsilon: float):
        """
        检查RemoteRescue的FOTARescueInfo event事件发送周期
        
        :param target_period: 期望的周期
        :param epsilon: ±偏差值
        :returns: bool
        :raises keyError: None
        """

    @abstractmethod
    def get_Remote_Rescue_DriveSts(self):
        """
        返回RemoteRescue的FOTARescueInfo event内容
        
        :returns FOTARescueInfo: Remote_Rescue_DriveSts
        :raises keyError: None
        """
        pass

    @abstractmethod
    def trigger_remote_rescue_inhibitControl(self):
        """
        触发v2t 下发维持不可开车指令接口, 触发车端设置车辆不可开车状态
                
        :return: 
        """
        pass
    
    @abstractmethod
    def hmi_set_window_full_open(self, win_pos:WindowId):
        """
        通过S2S设置窗户全关
        :param win_pos: 设置的窗户位置
            kWindowFrontLeft = 0
            kWindowFrontRight = 1
            kWindowRearLeft = 2
            kWindowRearRight = 3
            kWindowAll = 4
        :return: 
        """
        
    @abstractmethod
    def hmi_set_window_position(self, win_pos:WindowId, position: Union[WinPos, None] = None):
        """
        设置窗户位置
        
        :win_pos 窗户位置
        :position 窗户开度
        """
        
    @abstractmethod
    def hmi_set_window_full_open(self, win_pos:WindowId):
        """
        通过S2S设置窗户全关
        :param win_pos: 设置的窗户位置
            kWindowFrontLeft = 0
            kWindowFrontRight = 1
            kWindowRearLeft = 2
            kWindowRearRight = 3
            kWindowAll = 4
        :return: 
        """
        
    @abstractmethod
    def hmi_set_window_position(self, win_pos:WindowId, position: Union[WinPos, None] = None):
        """
        设置窗户位置
        
        :win_pos 窗户位置
        :position 窗户开度
        """
    @abstractmethod
    def check_window_status(self,zone:WindowId,switch_status:WindowSwitchStatus):
        """
        获取窗户开关状态
        zone:
            kWindowFrontLeft = 0  主驾
            kWindowFrontRight = 1 副驾
            kWindowRearLeft = 2   左后
            kWindowRearRight = 3  右后
            kWindowAll = 4  全部车窗

        switch_status:
            kUnknown = 0 #未知
            kIdle = 1 #无请求
            kUpManual = 2 #手动上升
            kUpAuto = 3 #自动上升
            kDownManual = 4 #手动下降
            kDownAuto = 5 #自动下降
        """
    @abstractmethod
    def check_window_event(self,event_status:WindowSwitchStatus):
        """
        获取窗户状态上报
        """
        
    @abstractmethod
    def hmi_set_window_full_open(self, win_pos:WindowId):
        """
        通过S2S设置窗户全关
        :param win_pos: 设置的窗户位置
            kWindowFrontLeft = 0
            kWindowFrontRight = 1
            kWindowRearLeft = 2
            kWindowRearRight = 3
            kWindowAll = 4
        :return: 
        """
        
        
    def get_gear_level(self, gear: Gear):
        """
        获取挡位通知
        :param gear: 挡位
            Park = 0
            Rvs = 1
            Neut = 2
            Drv = 3
            ManMode = 4
            Resd1 = 5
            Resd2 = 6
            Undefd = 7
        :return: 
        """

    @abstractmethod
    def notify_wifiStsChanged(self, type: str, hasAccessibility: str):
        """
        通知wifi状态, InteractiveService 
        
        :param type: 网络制式, 1:wifi  0:5g
        :param hasAccessibility: 是否可用        
        :returns NA
        :raises keyError: None
        """
        pass

    @abstractmethod
    def get_left_footlight_sts(self, sts: FootLightSts, timeout: int):
        """
        获取左照脚灯状态
        @param sts: 照脚灯状态
            On = 1
            Off = 0
        @param timeout:
        @return:
        """
        pass

    @abstractmethod
    def get_right_footlight_sts(self, sts: FootLightSts, timeout: int):
        """
        获取右照脚灯状态
        @param sts: 照脚灯状态
            On = 1
            Off = 0
        @param timeout:
        @return:
        """
        pass

    @abstractmethod
    def get_footlight_sts(self, sts: FootLightSts, timeout: int):
        """

        获取照脚灯状态
        @param sts: 照脚灯状态
            On = 1
            Off = 0
        @param timeout:
        @return:
        """
        pass

    @abstractmethod
    def check_left_footlight_inform(self, sts: FootLightSts, timeout: int):
        """
        通知左照脚灯状态
        @param sts: 照脚灯状态
            On = 1
            Off = 0
        @param timeout:
        @return:
        """
        pass

    @abstractmethod
    def check_right_footlight_inform(self, sts: FootLightSts, timeout: int):
        """
        通知右照脚灯状态
        @param sts: 照脚灯状态
            On = 1
            Off = 0
        @param timeout:
        @return:
        """
        pass

    @abstractmethod
    def set_footlight_sts(self, sts: OnOff):
        """
        控制照脚灯状态
        @param sts: 照脚灯状态
            On = 1
            Off = 0
        @return:
        """
        pass

    # @Author:guojing.yang@jiduatuo.com
    @abstractmethod
    def check_vehicle_inside_person_sts(self, userInVehicleStatus: bool = False, userInVehicleStatusWithCam: bool = False):
        """
        check车内有人状态事件
        :param userInVehicleStatus: (bool, optional): 识别车内是否有人。默认为False。
        :param userInVehicleStatusWithCam: (bool, optional): 与相机相关的识别车内是否有人。默认为False。
        """
        pass

    @abstractmethod
    def check_SetHvPulseHeating_req(self, on: bool = True,timeout: Union[float, int] = 1):
        """
        通过SOA Partner监听TCAM是否发出HighVoltageService:SetHvPulseHeating请求
        
        Args:
            on (bool, optional): 是否开启电池脉冲加热，默认为True.
            timeout (Union[float, int], optional): 超时时间，单位为秒，默认为1.
        
        Returns:
            None
        
        """
        pass

    @abstractmethod
    def notify_pulseHeatingInfo(self, pulseHeating_sts: PulseHeatingSts = PulseHeatingSts.kDefault,
                                  target_temperature: float=-41,):
        """
        通知脉冲加热状态信息 通过SOA Partne发送HighVoltageService:pulseHeatingInfo通知

        :param pulseHeating_sts: 脉冲加热状态
        :param target_temperature: 脉冲加热目标温度
        :return: 
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def set_batter_saver_connect(self, battersaver: bool):
        """
        通过SOAPartner设置节电继电器闭合或断开

        :param battersaver: bool类型 True:闭合False:断开
        :return: 
        """
        pass


#o_fan.liu           
    def event_check_frntleft_heat_sts2(self, heat_level: HeatLevel = HeatLevel.Off,                                                         ################o_fan.liu
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone,
                                                vent_level: VentLevel = VentLevel.Off, 
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone, source:SourceId=SourceId.Idle):
        """
        检查左前座椅的加热通风状态
        :param 
        heat_level: 加热等级
            Off = 0
            Low = 1
            Mid = 2
            High = 3
        heat_work_sts:加热工作状态
                kNone = 0
                On = 1
                Off = 2
                Error = 3
                FunctionLimit = 4
                EnergyLimit = 5
                Reserved1 = 6
                Reserved2 = 7
        vent_level:通风等级
            Off = 0
            Low = 1
            Mid = 2
            High = 3
        vent_work_sts:通风工作状态
                kNone = 0
                On = 1
                Off = 2
                Error = 3
                FunctionLimit = 4
                EnergyLimit = 5
                Reserved1 = 6
                Reserved2 = 7
        
            
        :return: 
        """             

    def event_check_frntright_heat_sts2(self, heat_level: HeatLevel = HeatLevel.Off,                                                         ################o_fan.liu
                                                heat_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone,
                                                vent_level: VentLevel = VentLevel.Off, 
                                                vent_work_sts: HeatVentWorkStatus = HeatVentWorkStatus.kNone, source:SourceId=SourceId.Idle):
        """
        检查右前座椅的加热通风状态
        :param 
        heat_level: 加热等级
            Off = 0
            Low = 1
            Mid = 2
            High = 3
        heat_work_sts:加热工作状态
                kNone = 0
                On = 1
                Off = 2
                Error = 3
                FunctionLimit = 4
                EnergyLimit = 5
                Reserved1 = 6
                Reserved2 = 7
        vent_level:通风等级
            Off = 0
            Low = 1
            Mid = 2
            High = 3
        vent_work_sts:通风工作状态
                kNone = 0
                On = 1
                Off = 2
                Error = 3
                FunctionLimit = 4
                EnergyLimit = 5
                Reserved1 = 6
                Reserved2 = 7
          
        :return: 
        """             
        
#o_fan.liu        
    @abstractmethod
    def get_tailgate_AntiPinch_sts(self, sts: bool):
        """
        获取尾门防夹通知

        :param sts: 尾门是否处于防夹
                False:不处于防夹
                True:处于防夹
        :return: 
        """
        pass
    
        
#o_fan.liu        
    @abstractmethod
    def event_check_tailgate_AntiPinch_sts(self, sts: bool):
        """
        校验尾门防夹通知

        :param sts: 尾门是否处于防夹
                False:不处于防夹
                True:处于防夹
        :return: 
        """
        pass
    
    @abstractmethod
    def stop_send_InteractiveService_response_gso(self):
        """
        注销InteractiveService服务回复(GSO)
        @param sts:
        @return:
        """
        pass

    @abstractmethod
    def start_send_InteractiveService_response_gso(self, isWifiConnectHotSpot: int):
        """
        启动InteractiveService服务回复(GSO)
        @param isWifiConnectHotSpot: 1是手机热点, 0是非手机热点
        @return:
        """
        pass

    @abstractmethod
    def update_InteractiveService_get_response(self, isWifiConnectHotSpot: int):
        """
        更新InteractiveService服务回复(GSO)
        @param isWifiConnectHotSpot: 1是手机热点, 0是非手机热点
        @return:
        """
        pass

    @abstractmethod
    def on_isWifiConnectHotSpot(self, partner_key, msg):
        """
        定义InteractiveService服务回复具体内容, 作为回调函数使用
        @param isWifiConnectHotSpot: 1是手机热点, 0是非手机热点
        @return:
        """
        pass

    @abstractmethod
    def notify_wifiStsChanged_NetWorkAccess(self, type: str, hasAccessibility: str):
        """
        EVENT wifiStsChanged, id="NetWorkAccess"
        @param type: 1是wifi, 0是5G
        @param hasAccessibility: true是连接, false是未连接
        @return:
        """
        pass