#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :buscomm.py

@Time         :2023/10/31 10:00

@Author       :quan.sun@jiduauto.com

@Description  :整车通信能力抽象接口
"""
from abc import abstractmethod, ABCMeta
from typing import Union, List, Tuple
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.api.constants.common import *


class AbcBusComm(metaclass=ABCMeta):

    @abstractmethod
    def set(self,
            bus_name: str,
            msg_name: str,
            signal_name: str,
            sig_value_name: Union[str, int, float],
            ub_flag: bool = True,
            cycle_time: Union[int, None] = None):
        """
        总线设置接口

        :param bus_name: 总线
        :param msg_name: 消息
        :param signal_name: 信号
        :param sig_value_name: 信号值  str -- "ON" "OFF"（信号值描述）    int -- 0,1 (原始值)      float -- 1.0, 2.0, 0.3 (物理值）
        :param ub_flag: ub标志位
        :param cycle_time: 周期
        :return:
        """

    @abstractmethod
    def check(self,
              bus_name: str,
              msg_name: str,
              signal_name: str,
              sig_value_name: Union[str, int],
              timeout: Union[float, int] = 5,
              do_assert: bool = True,
              check_time: int = 1,
              check_ub: Union[int, None] = None,
              ):
        """
        总线检查接口

        :param bus_name: 总线
        :param msg_name: 报文名
        :param signal_name: 信号
        :param sig_value_name: 信号值    str -- "ON" "OFF"（信号值描述）    int -- 0,1 (原始值)      float -- 1.0, 2.0, 0.3 (物理值）
        :param timeout: 超时时间
        :param do_assert: 是否自动assert判断标志
        :param check_time: 检查次数
        :param check_ub :    默认是None 不进行检查ub值, 如果是0,1,则检查ub值是否一直为该值
                    此参数针对需要检查信号的UB位，信号组请直接检查 XXX_UB
        :return:
        """

    @abstractmethod
    def check_sig_from_pdu(self,
              bus_name: str,
              msg_name: str,
              signal_name: str,
              sig_value_name: Union[str, int],
              pdu_data: list,
              do_assert: bool = True,
              ):
        """
        检查具体pdu中的信号值

        :param bus_name: 总线
        :param msg_name: 报文名
        :param signal_name: 信号
        :param sig_value_name: 信号值
        :param pdu_data: 需要check的 pdu 数据
        :param do_assert: 是否自动assert判断标志
        :return:
        """

    @abstractmethod
    def check_crc_from_pdu(self, msg_signals_obj, signal_name, pdu_data, do_assert):
        """
        根据pdu自动算出对应的crc，然后再pdu里的对应的crc进行比较

        :param msg_signals_obj : type
            self.dbc.bodycan.BCM_03            (= cls_signal_obj for each of this msg's signals)
        :param signal_name : str         信号或信号组都适配
            "DoorAjarFrntLeSts"             (= used to get the cls_signal_obj)
        :param pdu_data : list   需要check的pdu data
        :param do_assert : bool   是否直接进行assert判断
        :returns:   
            result : bool
                True if check succeeded
            actual_crc : int
                numeric value of signal
            expected_crc : int
                numeric value of signal

        """

    @abstractmethod
    def check_thread_start(
            self,
            bus_name: str,
            msg_name: str,
            signal_name: str,
            sig_value: Union[str, int],
            timeout: Union[float, int] = 5,
            do_assert=False,
            check_time=1,
    ):
        """
        # 同一报文内的多个信号同时检测,请不要用此接口，建议使用 check_multiple_signals_thread_start  接口 # 因为是线程,这个 do_assert 无效，目前固定是 False # 结果都需要通过 check_thread_stop 获取

        :param bus_name: 总线名
        :param msg_name: 消息名
        :param signal_name: 信号名
        :param sig_value: 信号值
        :param timeout: 超时时间
        :param do_assert: 是否抛异常
        :param check_time: 检查次数
        :return:
        """
        pass

    @abstractmethod
    def check_thread_stop(self, signal_name, timeout=30):
        """
        :param signal_name: 信号名
        :param timeout: 超时时间
        :return:
        """
        pass

    @abstractmethod
    def check_multiple_signals_thread_start(
            self,
            multiple_signals_info: List[Tuple[str, str, str, Union[str, int]]],
            timeout: Union[float, int] = 5,
            do_assert=False,
            check_time=1
    ) -> None:
        """
        异步检查最近收到的报文,multiple signals 都在一个报文内

        :param multiple_signals_info: bus_name:总线名,例如bodycan msg_name:消息名,例如BCM_03 signal_name:信号名,例如DoorAjarFrntLeSts sig_value_name:信号值,例如"v_Unlocked" or 123
        :param timeout: 检查超时时间
        :param do_assert: 是否出现异常
        :param check_time: 检查次数
        :return:
        """

    @abstractmethod
    def check_multiple_signals_thread_stop(self, message_name, timeout=30) -> bool:
        """
        异步停止多个信号检查，获取结果

        :param message_name: 报文名
        :param timeout: 超时时间，最好是check中timeout的2倍及以上
        :return:
        """
        pass

    @abstractmethod
    def check_signal_thread_start(
            self,
            bus_name: str,
            msg_name: str,
            signal_name: str,
            timeout: Union[float, int] = 5,
            do_print=False,
    ) -> None:
        """
        异步检查单个信号

        :param bus_name: 总线名
        :param msg_name: 消息名
        :param signal_name: 信号名
        :param timeout: 超时时间
        :param do_print: 是否打印报文
        :return:
        """
        pass

    @abstractmethod
    def check_signal_thread_stop(self, signal_name, timeout=30) -> bool:
        """
        异步停止单个信号检查

        :param signal_name: 需要与 check_signal_thread_start  保持一致
        :param timeout: 检查的超时时间，最好是check中timeout的2倍及以上
        :return:
        """
        pass

    @abstractmethod
    def set_vehspd_gear(self, vehspd: Union[int, float] = 0.0, gear: Union[Gear, None] = None):
        """
        设置车速和挡位

        :param vehspd: 设置的车速值
        :param gear: 设置的挡位值    枚举类型Gear class Gear(BaseEnum): Park = 0 Rvs = 1 Neut = 2 Drv = 3 ManMode = 4 Resd1 = 5 Resd2 = 6 Undefd = 7
        :returns: None
        """
        pass

    @abstractmethod
    def set_gear_pos(self, gear: Gear):
        """
        设置挡位

        :param gear: 设置的挡位值    枚举类型Gear class Gear(BaseEnum): Park = 0 Rvs = 1 Neut = 2 Drv = 3 ManMode = 4 Resd1 = 5 Resd2 = 6 Undefd = 7
        :returns: None
        """
        pass

    @abstractmethod
    def check_extr_mirr_adj_req(self, viewPos: ViewPos, req: MirrDirReq, timeout=3):
        """
        Check BGM发出的外后视镜请求

        :param viewPos: 指定要调节的外后视镜位置,包括:RearRight,RearLeft,All
        :param req: 期望接收到的请求值,包括:Idle,Up,Down,Left,Right
        :param timeout: 默认3
        :returns: None
        """
        pass

    @abstractmethod
    def set_windows_position(self, pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        """
        模拟反馈四个车窗当前的开度, 由DM BodyCan输入

        :param pos_drvr: 左前车窗开度, can信号值, 实际开度 4 * pos - 4
        :param pos_pass: 右前车窗开度,
        :param pos_lere: 左后车窗开度
        :param pos_rire: 右后车窗开度
        :return:
        """
        pass

    @abstractmethod
    def check_alrm_sts_req(self, alrm_sts: AlrmSts):
        """
        Check车辆告警上报状态

        :param alrm_sts: 告警上报状态 {'AlrmSt_Disarmd': 0, 'AlrmSt_Armd': 1, 'AlrmSt_Actv': 2}
        :return:
        """
        pass

    @abstractmethod
    def check_active_indicator_lamp_req(self, indcr_sts: IndcrSts):
        """
        Check BGM发出的闪灯请求

        :param indcr_sts: 闪灯请求  {'IndcrSts1_Off': 0, 'IndcrSts1_LeOn': 1, 'IndcrSts1_RiOn': 2, 'IndcrSts1_LeAndRiOn': 3}
        :return:
        """
        pass

    @abstractmethod
    def get_active_indicator_lamp_req_data(self, timeout=5):
        """
        获取闪灯请求信号的原始数据

        :param timeout: 获取信号的超时时间
        :return: 信号的原始数据
        """

    @abstractmethod
    def set_door_opener_sts(self, drv_opener: Union[DoorOpenerSts, None] = None,
                            pass_opener: Union[DoorOpenerSts, None] = None,
                            lere_opener: Union[DoorOpenerSts, None] = None,
                            rire_opener: Union[DoorOpenerSts, None] = None,
                            tr_opener: Union[DoorOpenerSts, None] = None):
        """
        设置五个门的开关状态 0x0 DoorOpenerSts_Ukwn 0x1 DoorOpenerSts_FullClsd 0x2 DoorOpenerSts_MovgOut 0x3 DoorOpenerSts_MovgOutBrkg 0x4 DoorOpenerSts_StopDurgOpen 0x5 DoorOpenerSts_FullOpend 0x6 DoorOpenerSts_MovgIn 0x7 DoorOpenerSts_MovgInBrkg 0x8 DoorOpenerSts_StopDurgCls 0x9 DoorOpenerSts_HalfClsd 0xA DoorOpenerSts_StopMinPntForCls

        :param drv_opener: 主驾门开关状态
        :param pass_opener: 副驾门开关状态
        :param lere_opener: 左后门开关状态
        :param rire_opener: 右后门开关状态
        :param tr_opener: 尾门开关状态
        :return:
        """
        pass

    @abstractmethod
    def set_five_door_opener_sts(self, door_opener: DoorOpenerSts):
        """
        同时设置五个门的开关状态
        :param door_opener: 门开关状态
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
        :return:
        """
        pass
    
    @abstractmethod
    def set_four_door_opener_sts(self, door_opener: DoorOpenerSts):
        """
        同时设置四个门的开关状态 
        :param door_opener: 门开关状态
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
        :return:
        """
        pass

    @abstractmethod
    def check_central_lock_sts(self, exp_sts: CenLockSts, exp_trigsrc: Union[None, LockTrigerSource] = None, timeout=1):
        """
        检测中控锁状态 0x0 LockStsUkwn - Lock Status Unknown 0x1 Unlckd - Unlocked 0x2 Lockd - Locked 0x3 SafeLockd - Safe Locked (Double Locked)

        :param exp_sts: 期望的锁状态
        :param exp_trigsrc: 期望的触发方式
        :return:
        """
        pass

    @abstractmethod
    def get_central_lock_sts(self, timeout=3):
        """
        获取中控锁状态

        :param timeout: 校验超时时间
        :return:
        """
        pass

    @abstractmethod
    def check_wipg_spd_info(self, wip_spd_info: WipgSpdInfo, timeout=2):
        """
        获取雨刮模式信息

        :param wip_spd_info: 雨刮模式信息
        :return:
        """
        pass

    @abstractmethod
    def check_wiper_wash_req(self, wash_req: WashReq, timeout=2):
        """
        获取雨刮清洗请求

        :param wash_req: 雨刮模式信息
        :return:
        """
        pass

    @abstractmethod
    def check_wiper_without_wash_req(self, timeout=5):
        """
        Check在条件不满足的情况下BGM不发送打开雨刮清洗请求

        :return:
        """
        pass

    @abstractmethod
    def check_wiper_rain_sensor_active_req(self, rain_sensor_act_req: RainSensorAct, timeout=5):
        """
        Check在条件满足的情况下BGM雨量传感器激活请求

        :param rain_sensor_act_req: 雨量传感器激活请求
        :return:
        """
        pass

    @abstractmethod
    def check_wiper_without_rain_sensor_active_req(self, timeout=5):
        """
        Check在条件不满足的情况下BGM不发送雨量传感器激活请求

        :return:
        """
        pass

    @abstractmethod
    def set_batterylow_mode(self, DCChrgnHndlSts: DCChrgnHndlSts, DispHvBattLvlOfChrg: int):
        """
        设置电量低报警信息

        :param DCChrgnHndlSts: 充电枪状态
        :param DispHvBattLvlOfChrg: 告警值，无告警（≥22） 一级告警(10~20) 二级告警（≤10）
        :return:
        """
        pass

    @abstractmethod
    def set_batter_sensor_hw_failure(self, BattSnsrHwFltRaw: BattSnsrHwFltRaw):
        """
        设置电量低报警信息

        :param BattSnsrHwFltRaw: 电池硬件故障状态
        :return:
        """
        pass

    @abstractmethod
    def set_dcdc_battary_act_sts(self, DcDcActvd: DcDcActvd):
        """
        设置高压电池激活状态

        :param DcDcActvd: 电池激活状态
        :return:
        """
        pass

    @abstractmethod
    def check_lv_power_supply_error_sts(self, LVPwrSplyErrSts: LVPwrSplyErrSts):
        """
        检测低压电池供电错误情况

        :param LVPwrSplyErrSts: 低压电池供电错误状态
        :return:
        """
        pass

    @abstractmethod
    def set_sys_safty_battery_current(self, BattSftySigSysSaftyBattI: float):
        """
        设置电池电流相关的系统安全状态

        :param BattSftySigSysSaftyBattI:
        :return:
        """
        pass

    @abstractmethod
    def set_sys_safty_battery_voltage(self, BattSftySigSysSaftyBattU: float):
        """
        设置电池电压相关的系统安全状态

        :param BattSftySigSysSaftyBattU:
        :return:
        """
        pass

    @abstractmethod
    def set_engine_sts(self, EngSt1WdStsEngSt1WdSts: EngSt1WdStsEngSt1WdSts):
        """
        设置发动机运行状态

        :param EngSt1WdStsEngSt1WdSts: 发动机运行状态
        :return:
        """
        pass

    @abstractmethod
    def check_low_sys_volt_warning(self, ULoWarnULoWarn: ULoWarnULoWarn):
        """
        检测低压系统电压告警

        :param ULoWarnULoWarn: 低压系统电压告警状态
        :return:
        """
        pass

    @abstractmethod
    def set_SOC_display_value(self, soc_value: int):
        """
        设置高压电池显示的SOC值

        :param soc_value: 显示SOC值
        :return:
        """
        pass

    @abstractmethod
    def set_HV_SOC_value(self, soc_value: int):
        """
        设置高压电池的SOC值

        :param soc_value: 显示SOC值
        :return:
        """
        pass

    @abstractmethod
    def set_DC_charge_port_tmp(self, port: DCChrgnPort, tmp):
        """
        设置DC充电口正负极温度

        :param port: 正负极
        :param tmp: 温度
        :return:
        """
        pass

    @abstractmethod
    def set_low_volt_power_supply(self):
        """
        设置低压补电开启

        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_wiper_maintain_ser_pos_req(self, maintain_ser_req: MaintainPosReq, timeout=5):
        """
        设置雨刮服务维修位置

        :param maintain_ser_req: 服务位置请求状态 Off = 0 On = 1
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_tailwing_pos(self, pos: TailWingPos):
        """
        设置电动尾翼位置

        :param pos: 电动尾翼位置
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_tailwing_pos_req(self, pos: SetTailWingPos):
        """
        BGM发出设置电动尾翼位置命令

        :param pos: BGM发出的电动尾翼位置请求 NoCmd = 0 P0 = 1 P1 = 2 P2 = 3 P3 = 4 Reserved1 = 5 Reserved2 = 6 Reserved3 = 7
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_vehicle_speed(self):
        """
        获取车速度信息

        :return: 车速值
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_tailgate_opener_req(self, req: SetTailGatePos):
        """
        BGM发出操作尾门的请求

        :param pos: BGM发出的电动尾翼位置请求 Idle = 0 Open= 1 Close = 2 Stop = 3 CloseDelay = 4
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_steerwheel_heat_req(self,avl_sts: AvlSts,  lev_sts: HeatLevel):
        """
        BGM发出的控制方向盘加热的状态

        :param lev_sts: 加热状态 Off = 0 Low = 1 Mid = 2 High = 3
        :param avl_sts: 功能可用状态 Non = 0 On = 1 Off = 2 Error = 3 Functionallimit = 4 Energylimit = 5 Resvd1 = 6 Resvd2 = 7
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_Hv_sys_relay_sts(self, sts: HvSysRelaySts):
        """
        #设置高压继电器状态为

        :param sts: 加热状态 Open = 0 Close = 1 KeepSts = 2 OpenAndReqActvDcha = 3
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_blt_sts(self, seat_id: SeatId, blt_flt_sts: BltFltSts, blt_lock_sts: BltLockSts):
        """
        #设置座椅安全带情况

        :param seat_id: 座椅位置 FrontLeft = 0 FrontRight  = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param blt_flt_sts: 安全带扣故障状态 NoFault = 0 Fault = 1
        :param blt_lock_sts: 安全带扣插入状态 Unlock = 0 Lock = 1
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_seat_occpt_sts(self, seat_id: SeatId, seat_sts: SeatOccptSts):
        """
        #设置座椅占位状态
        :param seat_id: 座椅位置 FrontLeft = 0 FrontRight  = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param seat_sts: 设置座椅状态 Empty = 0 Fmale = 1 OccptLrg = 2 Ukwn = 3
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_usage_mode_to_tcam(self, usage_mode: UsageMode):
        """"
        模拟BGM通过connectivitycanfd发送CarMode信号到TCAM

        :param usage_mode: /** 废弃 */ @value(0) ABANDONED, /** 未激活 */ @value(1) INACTIVE, /** 充电 */ @value(2) CONVENIENCE, /** 激活 */ @value(11) ACTIVE, /** 驾驶 */ @value(13) DRIVING
        :param do_assert: 若为True 则表示切换失败则会报错，否则返回切换后的模式
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_car_mode_to_tcam(self, car_mode: CarMode):
        """"
        模拟BGM通过connectivitycanfd发送UsageMode信号到TCAM

        :param car_mode: NORMAL = 0 TRANSPORT = 1 FACTORY = 2 CRASH = 3 DYNO = 5
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_night_mode(self,wait_time: Union[float, int] = 0):
        """
        设置当前为夜晚模式，适用于灯光测试
        @param wait_time: 等待时间
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_day_mode(self,wait_time: Union[float, int] = 0):
        """
        设置当前为白天模式，适用于灯光测试
        @param wait_time: 等待时间
        :return:
        """
        pass


    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_low_beam_sts(self):
        """
        设置当前为白天模式，适用于灯光测试

        :return:
        """
        pass

    @abstractmethod
    def set_vehspd(self, value=0):
        """
        设置车速

        :param value: 车速
        :return:
        """
        pass

    @abstractmethod
    def send_msg_by_id_func(self, bus_name, msg_id, data, **kwargs):
        """
        发送指定 id 的报文

        :param bus_name: 通道名称
        :param msg_id: msg id
        :param data: 发送数据内容，可以为列表（[0x10,0x01]），或者16进制字符传（1001）
        :return:
        """
        pass

    @abstractmethod
    def recv_msg_by_id_func(self, bus_name, msg_id, timeout=1, **kwargs):
        """
        在 当前通道接收指定id的报文，

        :param bus_name: 通道名称
        :param msg_id: id
        :param timeout: 接收超时时间
        :return:
        """
        pass

    @abstractmethod
    def recv_diag_request_msg(self, bus_name, request_id=0x712, response_id=0x612, bs=8, st=5, single_frame_len=None,
                              timeout=1):
        """
        接收 can的请求报文

        :param bus_name: 通道名字
        :param request_id:  请求id
        :param response_id: 响应id
        :param bs: block
        :param st: st_min
        :return:
        """
        pass

    @abstractmethod
    def send_diag_request_msg(self, bus_name: str, request_id=0x712, response_id=0x612, send_msg=[],
                              single_frame_len=None,
                              padding=0x00):
        """
        发送诊断请求

        :param bus_name: 通道名字
        :param request_id:  请求id
        :param response_id: 响应id
        :param bs: block
        :param st: st_min
        :return:
        """

    @abstractmethod
    def clear_all_bus_buffer(self):
        """
        清空所有 bus 通道缓存
        """
        self.ipdu.rx_flag_reset_all()

    @abstractmethod
    def clear_bus_buffer(self, bus_name):
        """
        清空 bus 通道缓存

        :param bus_name: str   通道名字
        :return:
        """
        self.ipdu.rx_flag_reset_bus(bus_name)

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_climate_ac_sts(self, sts: CoolgReq, timeout: Union[float, int] = 5):
        """
        check空调A/C状态

        :param sts: 空调A/C状态
        :param timeout: 监测信号的时间
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def recover_extral_light_to_defaul_sts(self):
        """
        恢复外灯设置为默认的无故障状态

        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_extral_light_button_to_defaul_sts(self):
        """
        设置灯相关按键无触发

        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_low_beam_act_sts(self, actn_sts: isOn, extr_light_sts: ExtrLtgSts):
        """
        检测近光灯相关状态

        :param actn_sts: 近光灯激活状态请求 Off = False On = True
        :param extr_light_sts: 外灯状态请求 Off = 0 On = 1 Err = 2 Resd = 3 Auto = 1
        :return:
        """
        pass

    @abstractmethod
    def clear_bus_id_buffer(self, bus_name, msgid: Union[str, int]):
        """
        清空总线上 某个id 报文的缓存

        :param bus_name:
        :param msgid:
        :return:
        """

    @abstractmethod
    def send_pdu(
            self, bus_name: str, msg_id: Union[str, int], data: Union[str, list], cycle_time=None
    ):
        """
        发送总线数据

        :param bus_name: 总线名称
        :param msg_id: 报文id
        :param data: 报文内容，16进制字符串('1001')，或者列表[0x10,0x01]
        :param cycle_time: 周期
        :return:
        """

    @abstractmethod
    def stop_send_pdu(self, bus_name: str, id: Union[str, int]):
        """
        # 针对的是 can bus,停止发送报文

        :param bus_name: 名字
        :param id: 报文id
        :return:
        """

    @abstractmethod
    def recv_pdu(self, bus_name, id: Union[str, int], timeout=5):
        """
        接收指定通道指定id的报文

        :param bus_name: 总线名称
        :param id: 报文id
        :param timeout: 接收超时时间
        :return: 返回一个元组 (id, time_stamp, length, data) 或者 None
        """

    @abstractmethod
    def pause_ecu_send(self, bus_name: str, ecu_name: str):
        """
        暂停 bus 发送数据

        :param bus_name: 通道名称
        :return:
        """

    @abstractmethod
    def pause_bus_send(self, bus_name: str):
        """
        暂停 bus 发送数据

        :param bus_name: 通道名称
        :return:
        """

    @abstractmethod
    def pause_all_bus_send(self):
        """
        暂停所有 通道发送数据

        :return:
        """

    @abstractmethod
    def resume_bus_send(self, bus_name: str):
        """
        继续发送 数据 #  can bus  需要做2s的等待以确保所有的报文都恢复 #  FR bus 需要做200ms 的等待以确保所有的报文都恢复

        :param bus_name:
        :return:
        """

    @abstractmethod
    def resume_all_bus_send(self):
        """
        继续发送 数据 # 目前只针对的是 can bus  ,  需要做2s的等待以确保所有的报文都恢复

        :return:
        """

    @abstractmethod
    def resume_send_pdu(self, bus_name: str, id: Union[str, int]):
        """
        继续发送

        :param bus_name:
        :param id:
        :return:
        """

    @abstractmethod
    def wakeup_lin1(self, **kwargs):
        """
        唤醒 lin 1  用车速唤醒，  维持原来的状态 要防止 fr 休眠，要先发送can 报文维持

        :param kwargs:
        :return:
        """

    @abstractmethod
    def recovery_wakeup_lin1_precondition(self, **kwargs):
        """
        恢复 唤醒 lin1  环境

        :param kwargs:
        :return:
        """

    @abstractmethod
    def wakeup_lin2(self, **kwargs):
        """
       非0 一直唤醒 在 usagemode=0 唤醒 lin 2  仿真发送FR::VDDM::VDDMBackBoneSignalIPdu29::DCChrgnHndlSts=2 要防止 fr 休眠，要先发送can 报文维持 sig_value_table = {'OnBdChrgrHndlSts_Disconnected': 0, 'OnBdChrgrHndlSts_ConnectedWithoutPower': 1, 'OnBdChrgrHndlSts_PowerAvailableButNotActivated': 2, 'OnBdChrgrHndlSts_ConnectedWithPower': 3, 'OnBdChrgrHndlSts_Init': 4, 'OnBdChrgrHndlSts_Fault': 5}

       :param kwargs:
       :return:
       """

    @abstractmethod
    def recovery_wakeup_lin2_precondition(self, **kwargs):
        """
        恢复 唤醒 lin2  环境

        :param kwargs:
        :return:
        """

    @abstractmethod
    def wakeup_lin3(self, partner, dk):
        """
        长时间唤醒 切模式 partner = S2sBaseClass([("VehicleModeService", "client")]) dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)

        :param kwargs:
        :return:
        """

    @abstractmethod
    def recovery_wakeup_lin3_precondition(self, partner, dk):
        """
        partner = S2sBaseClass([("VehicleModeService", "client")]) dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)

        :param partner:
        :param dk:
        :return:
        """
        pass

    @abstractmethod
    def wakeup_lin4(self, **kwargs):
        """
        唤醒 lin 4  用车速唤醒，  维持原来的状态 要防止 fr 休眠，要先发送can 报文维持

        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def recovery_wakeup_lin4_precondition(self, **kwargs):
        """
        恢复 lin4 唤醒

        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def wakeup_lin5(self, **kwargs):
        """
        唤醒 lin 5

        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def recovery_wakeup_lin5_precondition(self, **kwargs):
        """
        恢复 lin5 唤醒

        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def wakeup_lin6(self, **kwargs):
        """
        唤醒 lin 6

        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def recovery_wakeup_lin6_precondition(self, **kwargs):
        """
        恢复 lin6 唤醒

        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def wakeup_all_lin(self, partner, dk):
        """
        partner = S2sBaseClass([("VehicleModeService", "client")]) dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config) 唤醒所有lin 通道 lin1       车速唤醒  或者 driving lin2 非0 一直唤醒  driving  或者 在0 下 1、仿真发送FR::VDDM::VDDMBackBoneSignalIPdu29::DCChrgnHndlSts=2 lin3 非0 一直唤醒  driving 或者  必须切模式 lin4 非0 一直唤醒  driving  或者 车速唤醒  driving lin5 lin6 非0 一直唤醒  driving 或者 仿真低压LVEEM signal BattSnsrStsReq == 1 设置车速 和 切换模式 会唤醒所有通道

        :return:
        """
        pass

    @abstractmethod
    def recovery_wakeup_all_lin_precondition(self, partner, dk, **kwargs):
        """
        partner = S2sBaseClass([("VehicleModeService", "client")])
        dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        复位所有lin 通道

        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_door_warning_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        """
        功能: 设置四门破冰状态

        :param Drvr: 驾驶位故障状态，数据类型: bool
        :param Pass: 副驾驶故障状态，数据类型: bool
        :param LeRe: 左后故障状态，数据类型: bool
        :param RiRe: 右后故障状态，数据类型: bool
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_door_warning_sts(self, warn_sts: Union[bool, None] = None):
        """
        功能: 同时设置四门故障状态

        :param warn_sts: 驾驶位故障状态，数据类型: bool
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_door_active_ice_sts(self,
                                Drvr: Union[bool, None] = None,
                                Pass: Union[bool, None] = None,
                                LeRe: Union[bool, None] = None,
                                RiRe: Union[bool, None] = None
                                ):
        """
        功能: 设置四门破冰状态

        :param Drvr: 驾驶位破冰状态，数据类型: bool
        :param Pass: 副驾驶破冰状态，数据类型: bool
        :param LeRe: 左后破冰状态，数据类型: bool
        :param RiRe: 右后破冰状态，数据类型: bool
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_four_door_active_ice_sts(self, act_ice_sts: Union[bool, None] = None):
        """
        功能: 同时设置四门破冰状态

        :param warn_sts: 驾驶位破冰状态，数据类型: bool
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_door_radar_sts(self,
                           Drvr: Union[RadarSts, None] = None,
                           Pass: Union[RadarSts, None] = None,
                           LeRe: Union[RadarSts, None] = None,
                           RiRe: Union[RadarSts, None] = None
                           ):
        """
        功能: 设置四门雷达状态

        :param Drvr: 驾驶位雷达状态，数据类型: 枚举
        :param Pass: 副驾驶雷达状态，数据类型: 枚举
        :param LeRe: 左后雷达状态，数据类型: 枚举
        :param RiRe: 右后雷达状态，数据类型: 枚举
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_door_radar_sts(self, radar_sts: Union[RadarSts, None] = None):
        """
        功能: 同时设置四门雷达状态

        :param radar_sts: 驾驶位雷达状态，数据类型: 枚举
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_door_anti_pnch_sts(self,
                               Drvr: Union[bool, None] = None,
                               Pass: Union[bool, None] = None,
                               LeRe: Union[bool, None] = None,
                               RiRe: Union[bool, None] = None
                               ):
        """
        功能: 设置四门防夹状态

        :param Drvr: 驾驶位防夹状态，数据类型: bool
        :param Pass: 副驾驶防夹状态，数据类型: bool
        :param LeRe: 左后防夹状态，数据类型: bool
        :param RiRe: 右后防夹状态，数据类型: bool
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_four_door_anti_pnch_sts(self, anti_pnch_sts: Union[bool, None] = None):
        """
        功能: 同时设置四门防夹状态

        :param anti_pnch_sts: 驾驶位防夹状态，数据类型: bool
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_epb_sts(self, sts: EpbSts):
        """
        功能: 设置EPB状态

        :param sts: EPB状态，数据类型: 枚举 Resd0 = 0 Resd1 = 1 Resd2 = 2 AllAppld = 3 Resd4 = 4 AllInTran = 5 BrkgDynByActr = 6 Resd7 = 7 Resd8 = 8 ActrAllReld = 9 BrkgDynDegraded = 10 Resd11 = 11 BrkgDyn = 12 Resd13 = 13 Resd14 = 14 Err = 15
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_pedestrian_protection_fault_sts(self, sts: PedestProtectFltSts):
        """
        设置行人保护故障状态

        :param sts: 行人保护故障状态 NotVld1 = 0 Off = 1 On = 2 NotVld2 = 3
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_pedestrian_protection_warning_sts(self, sts: PedestProtectImpctSts):
        """
        设置行人保护报警状态

        :param sts: 行人保护报警状态 Off = 1 On = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_vehicle_crash_sts(self, roll_over_crash: Union[bool, None] = None, front_crash: Union[bool, None] = None,
                              rear_crash: Union[bool, None] = None, left_crash: Union[bool, None] = None,
                              right_crash: Union[bool, None] = None):
        """
        设置车辆碰撞状态

        :param roll_over_crash: 是否有翻滚 bool
        :param front_crash: 前碰撞 bool
        :param rear_crash: 后碰撞 bool
        :param left_crash: 左碰撞 bool
        :param right_crash: 右碰撞 bool
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_airbagsign_light_active_sts(self, sts: AirbagLampReqSts):
        """
        设置安全气囊指示灯激活状态

        :param sts: 安全气囊指示灯激活状态 LampOff = 0 Unknown = 1 LampFlash = 2 LampOn = 3
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_airbag_warning_sts(self, sts: AirbagWarningSts):
        """
        设置安全气囊提示状态

        :param sts: NotVld1 = 0 Off = 1 On = 2 NotVld2 = 3
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_intr_light_read_lamp_req(self, zone: ReadLampZone, sts: ReadLampSts):
        """
        Check BGM 发出阅读灯请求

        :param zone: 控制区域 FrontLeft = 1 FrontRight = 2 RearLeft = 3 RearRight = 4
        :param sts: 请求的状态 Unknow = 0 Welcome = 1 Courtesy = 2 Manual = 3 Polite = 4 ForceOn = 5 ForceOff = 6
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_alm_light_req(self, brightness: Union[int, None] = None, red: Union[int, None] = None,
                            green: Union[int, None] = None, blue: Union[int, None] = None):
        """
        Check氛围灯的颜色和亮度

        :param brightness: 亮度值，int
        :param red:   红色像素值 int
        :param green: 绿色像素值 int
        :param blue: 蓝色像素值 int
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def tire_sensor_ini(self, id1='11111111', id2='02628643', id3='026284F4', id4='22222222', pressure: int = 260):
        """
        初始化4个胎压的初始信息

        :param id1: 左前胎压ID
        :param id2: 右前胎压ID
        :param id3: 右后胎压ID
        :param id4: 左后胎压ID
        :param pressure: 初始的胎压值
        :return: tire_sensor_dic 初始化之后的4个胎压数据，字典
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_tpms_pressure(self, tire_sensor: dict, pos: TirePos = TirePos.All, pressure: Union[int, float] = 260,
                          time_wait: Union[float, int] = 0):
        """
        设置胎压数据

        :param tire_sensor: 输入的4个轮胎当前的字典数据
        :param pos: 要设置的轮胎位置 FrontLeft = 1 FrontRight = 2 RearRight = 3 RearLeft = 4 All = 5
        :param pressure: 设置的胎压值
        :param time_wait: 设置后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_tpms_factory(self, tire_sensor: dict, pos: TirePos = TirePos.All, factory: int = 0x02,
                         time_wait: Union[float, int] = 0):
        """
        设置Factory数据

        :param tire_sensor: 输入的4个轮胎
        :param pos: 要设置的轮胎位置 FrontLeft = 1 FrontRight = 2 RearRight = 3 RearLeft = 4 All = 5
        :param factory:
        :param time_wait: 设置后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_tpms_temperature(self, tire_sensor: dict, pos: TirePos = TirePos.All, temperature: Union[int, float] = 52,
                             time_wait: Union[float, int] = 0):
        """
        设置轮胎温度

        :param tire_sensor: 输入的4个轮胎
        :param pos: 要设置的轮胎位置 FrontLeft = 1 FrontRight = 2 RearRight = 3 RearLeft = 4 All = 5
        :param temperature: 设置的温度值
        :param time_wait: 设置后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_tire_flag(self, location: TirePos, flag: SysWarnFlg, status: TireAlarmSts):
        """
        检查指定轮胎的指定告警flag是否置位

        :param location: 车轮位置 FrontLeft = 1 FrontRight = 2 RearRight = 3 RearLeft = 4 All = 5
        :param flag: 系统胎压告警指示 SysWarnFlg = 0 PWarnFlg = 1 TWarnFlg = 2 MsgOldFlg = 3 FastLoseWarnFlg = 4 BattLoSt = 5
        :param status: 告警状态 Alarm = 0 NoAlarm = 1
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_four_tire_flag(self, flag: SysWarnFlg, status: TireAlarmSts):
        """
        检查4个轮胎的告警flag是否符合预期

        :param flag: 系统胎压告警指示 SysWarnFlg = 0 PWarnFlg = 1 TWarnFlg = 2 MsgOldFlg = 3 FastLoseWarnFlg = 4 BattLoSt = 5
        :param status: 告警状态 Alarm = 0 NoAlarm = 1
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def pause_bus_send_tpms(self):
        """
        测试TPMS,停止相关总线数据发送

        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def send_tpms_rf_data(self, rf_data, rolling_counter):
        """
        发送胎压数据

        :param rf_data: TPMS数据
        :param rolling_counter: 计数
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_vehspd_and_qf(self, vehspd: Union[int, float] = 0.0, veh_qf: VehSpdQf = VehSpdQf.AccurData):
        """
        设置车速和车速qf

        :param vehspd: 车速
        :param veh_qf: 车速qf
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_vehmtn(self, vehmtnst: VehMtnSts = VehMtnSts.StandStillVal3):
        """
        设置车辆静止状态

        :param vehmtnst: 车辆静止状态 Ukwn = 0 StandStillVal1 = 1 StandStillVal2 = 2 StandStillVal3 = 3 FwdVal1 = 4 FwdVal2 = 5 BackwVal1 = 6 BackwVal2 = 7
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_dtc_pre(self, **kwargs):
        """
        测试tpmsdtc都前置条件设置

        :param kwargs:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_climate_cycle_req(self, sts: ClimateCycleReq):
        """
        check BGM发出的循环模式请求

        :param sts: 循环模式请求
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def trigger_steer_wheel(self, time_interval: Union[int, float] = 0.5):
        """
        方向盘触发左转

        :param time_interval: 按键按下和松开的时间间隔
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_lin_bus_sts(self, lin_channel: LinChannel, sts: BusSendSts, msg_name: Union[str, None] = None,
                          signal_name: Union[str, None] = None, last_time: Union[float, int, None] = None):
        """
        检查Lin总线状态

        :param lin_channel: 要检测的Lin通道: LIN1 = 1 LIN2 = 2 LIN3 = 3 LIN4 = 4 LIN5 = 5 LIN6 = 6
        :param sts: 要检查的状态 Sleep = 0 Awakeup = 1
        :param msg_name: 要检测的消息名字 str,例如: "CemCem_Lin1Fr01"
        :param signal_name: 要检测的信号名字，str,例如: "IntrMirrCmdDrvrSide"
        :param last_time: 希望检查的信号的持续时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_climate_vent_req(self, pos: AirVentReqPos, sts: AirVentReqSts):
        """
        检查BGM 发出的出风口开关请求

        :param pos: 控制的位置 DrvrLeft = 0 DrvrRight = 1 PassLeft = 2 PassRight = 3 SecRow = 4 All = 5
        :param sts: 要检查的状态 Off = 0 On = 1
        """

    # # @Author:hui.zhao@jiduatuo.com
    # @abstractmethod
    # def check_door_opener_move_sts(self, door_pos: DoorPos, door_req: DoorOpenerMoveSts,
    #                                timeout: Union[float, int] = 1):
    #     """
    #     Check BGM 发出的电动门的运动状态请求

    #     :param door_pos: 门的位置
    #     :param door_req: 请求值 Ukwn = 0 FullClsd = 1 MovgOut = 2 MovgOutBrkg = 3 StopDurgOpen = 4 FullOpend = 5 MovgIn = 6 MovgInBrkg = 7 StopDurgCls = 8 HalfClsd = 9 StopMinPntForCls = 0x0A
    #     :param timeout:
    #     :return:
    #     """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_door_opener_req(self, drv_opener: Union[DoorPos, None] = None,
                              pass_opener: Union[DoorPos, None] = None,
                              lere_opener: Union[DoorPos, None] = None,
                              rire_opener: Union[DoorPos, None] = None,
                              tr_opener: Union[DoorPos, None] = None,
                              door_req: DoorOpenerReq = DoorOpenerReq.Idle,
                              trigger_src: Union[None, LockTrigerSource] = None,
                              timeout: Union[float, int] = 1
                              ):
        """
        Check BGM 发出的电动门的开关请求

        :param drv_opener:
        :param pass_opener:
        :param lere_opener:
        :param rire_opener:
        :param tr_opener:
        :param door_req: 请求值 Idle = 0 Open = 1 Close = 2 Stop = 3 OpenMinang = 4
        :param trigger_src: 触发源 NoTrigSrc = 0 KeyRem = 1 Keyls = 2 IntrSwt = 3 SpdAut = 4 TmrAut = 5 Slam = 6 Telm = 7 Crash = 8 Apprch = 9 OutsOth = 10 InsOth = 11 NFC = 12
        :param timeout:
        :return:
        """

    def check_four_door_opener_req(self, door_req: DoorOpenerReq, trigger_src: Union[None, LockTrigerSource] = None,
                                   timeout: Union[float, int] = 1):
        """
        同时Check 4门的开关请求

        :param door_req: Idle = 0 Open = 1 Close = 2 Stop = 3 OpenMinang = 4
        :param trigger_src: 触发源 NoTrigSrc = 0 KeyRem = 1 Keyls = 2 IntrSwt = 3 SpdAut = 4 TmrAut = 5 Slam = 6 Telm = 7 Crash = 8 Apprch = 9 OutsOth = 10 InsOth = 11 NFC = 12
        :param timeout:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_horn_active_req(self, req: isOn):
        """
        Check BGM 发出的喇叭激活请求

        :param req: Off = False On = True
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_seat_heat_sts(self, pos: SeatId, sts: HeatVentiSts):
        """
        模拟座椅节点返回座椅加热状态

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param sts: 座椅状态 None_ = 0 On = 1 Off = 2 Error = 3 Functionallimit = 4 Energylimit = 5 Resvd1 = 6 Resvd2 = 7
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_seat_venti_sts(self, pos: SeatId, sts: HeatVentiSts):
        """
        模拟座椅节点返回座椅通风状态

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param sts: 座椅状态 None_ = 0 On = 1 Off = 2 Error = 3 Functionallimit = 4 Energylimit = 5 Resvd1 = 6 Resvd2 = 7
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_seat_massg_sts(self, pos: SeatId, sts: isOn):
        """
        模拟座椅节点返回座椅按摩状态

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param sts: 座椅状态 Off = False On = True
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_seat_heat_level(self, pos: SeatId, level: HeatVentiLvl):
        """
        模拟座椅节点返回座椅加热等级

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_seat_venti_level(self, pos: SeatId, level: HeatVentiLvl):
        """
        模拟座椅节点返回座椅通风等级

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com    #o_fan.liu
    @abstractmethod
    def check_seat_heat_req(self, pos: SeatId, level: HeatVentiLvl, source:SourceId):
        """
        check BGM发出座椅加热请求

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :param level: 加热源    Idle = 0    HMI = 1    Remote = 2 
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com     #o_fan.liu
    @abstractmethod
    def check_seat_venti_req(self, pos: SeatId, level: HeatVentiLvl, source:SourceId):
        """
        check BGM发出座椅通风请求

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :param source: 加热源    Idle = 0    HMI = 1    Remote = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_seat_massg_req(self, pos: SeatId, is_on: bool, type: MassType, level: MassIntensity):  
        """
        check BGM发出座椅按摩请求

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param is_on: 按摩是否开启  Off = False On = True
        :param type: 按摩类型   Type1 = 0    Type2 = 1    Type3 = 2    Type4 = 3   Type5 = 4    Type6 = 5    Type7 = 6    Type8 = 7      
        :param level: 按摩强度 Low = 0 Normal = 1 High = 2 Off = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_seat_heat_level_sts(self, pos: SeatId, level: HeatVentiLvl):
        """
        check BGM 转发的座椅加热等级请求

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_seat_heat_available_sts(self, pos: SeatId, sts: HeatVentiSts):
        """
        check BGM 转发的座椅加热可用状态请求

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param sts: 加热状态 None_ = 0 On = 1 Off = 2 Error = 3 Functionallimit = 4 Energylimit = 5 Resvd1 = 6 Resvd2 = 7
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_seat_venti_available_sts(self, pos: SeatId, sts: HeatVentiSts):
        """
        check BGM 转发的座椅通风可用状态请求

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param sts: 通风状态 None_ = 0 On = 1 Off = 2 Error = 3 Functionallimit = 4 Energylimit = 5 Resvd1 = 6 Resvd2 = 7
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_seat_heat_massg_sts(self, pos: SeatId, sts: isOn):
        """
        check BGM 转发的座椅按摩状态请求

        :param pos: FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param sts: Off = False On = True
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_seat_direction_adjust_req(self, pos: SeatId, type: SeatAdjustType,
                                        req: Union[SeatUpDownAdj, SeatForwBackAdj]):
        """
        check BGM 转发的主驾座椅调节请求

        :param pos: 座椅位置
        :param type: 调节类型 Height = 0 Len = 1 Back = 2 Legrest = 3 Lumbar = 4
        :param req: SeatHeiAdj:上下调节 Idle = 0 Up = 1 Down = 2 或者 SeatLenAdj:前后调节 Idle = 0 Forward = 1 Backward = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_intelligent_charge_wakeup_counter(self, check_times: int = 4):
        """
        检查补电次数30S内最大补电次数

        :param check_times: check的次数
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_intelligent_charge_wakeup_sts(self, sts: IPMLoUWakeUpReq):
        """
        设置补电请求WakeUp请求

        :param sts: 请求状态 NotReqd = 0 Chrgn = 1 NotChrgn = 2 Invalid = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_low_volt_servse_sts(self, cnv_req: CnvnReq, charg_vol_req: Union[float, int, None] = None):
        """
        查询BGM智能补电状态和电压

        :param cnv_req: NotReqd = 0 Chrgn = 1 Resd1 = 2 Resd2 = 3 Resd3 = 4 Resd4 = 5 Resd5 = 6 Resd6 = 7
        :param charg_vol_req:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_battery_stop_intelligent_charge(self, time_wait: Union[float, int] = 3):
        """
        设置BattURaw停止补电

        :param time_wait: 执行操作之后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_intelligent_charge_allow_sts(self, sts: CnvnAllwd, time_wait: Union[float, int] = 0):
        """
        设置智能补电允许情况

        :param sts: NotOk = 0 OK = 1
        :param time_wait: 执行操作之后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_rear_view_fold_sts_req(self, req: FoldHmiReq):
        """
        Check BGM发出的后视镜展开折叠请求

        :param req: NotPsd = 0 Psd = 1
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_pass_seat_present(self):
        """
        设置副驾占位

        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_pass_seat_notpresent(self):
        """
        设置副驾未占位

        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_secle_seat_present(self):
        """
        设置后左占位

        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_secle_seat_notpresent(self):
        """
        设置后左未占位

        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_secmid_seat_present(self):
        """
        设置后中占位

        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_secmid_seat_notpresent(self):
        """
        设置后中未占位

        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_secri_seat_present(self):
        """
        设置后右占位

        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_secri_seat_notpresent(self):
        """
        设置后右未占位

        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_usage_mode_status(self, usage_mode: UsageMode, timeout=1):
        """
        Check 总线上的信号UsageMode值

        :param usage_mode: 期望获取Usagemode值
        :param timeout: 等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_car_mode_status(self, car_mode_main: CarMode, car_mode_sub: int, timeout=1):
        """
        检查总线上carmode主模式和子模式的状态

        :param car_mode_main:
        :param car_mode_sub:
        :param timeout:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def trigger_gear_by_auto(self, gear_status: bool = True):
        """
        触发自动挂挡

        :param gear_status:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def trigger_gear_by_cdc(self, gear_status: bool = True):
        """
        触发屏幕挂挡

        :param gear_status:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def trigger_gear_by_manual(self, gear_status: bool = True):
        """
        触发手动挂挡

        :param gear_status:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_four_door_and_tailgate_hood_sts(self, sts: Door,pos:DoorPos = DoorPos.All):
        """
        Check 四门两盖状态
        :param sts: 期望获取的门状态
            open = 1
            close = 2
        :param sts: check的位置
            Dirver = 0
            Pass = 1
            RearLeft = 2
            RearRight = 3
            Tailgate = 4
            All = 5
            Hood = 6
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_climate_fragrance_req(self, taste: FragChannel, level: FragLevel,
                                    ch1_ratio: Union[int, None] = 0, ch2_ratio: Union[int, None] = 0,
                                    ch3_ratio: Union[int, None] = 0,
                                    ch4_ratio: Union[int, None] = 0, ch5_ratio: Union[int, None] = 0):
        """
        Check BGM 发出的香氛信息

        :param taste: 香氛通道 NoReq = 0 Channel1 = 1 Channel2 = 2 Channel3 = 3 Channel4 = 4 Channel5 = 5
        :param level: 香氛等级 LevelOff  = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :param ch1_ratio: 通道1的香氛比例 int
        :param ch2_ratio: 通道2的香氛比例 int
        :param ch3_ratio: 通道3的香氛比例 int
        :param ch4_ratio: 通道4的香氛比例 int
        :param ch5_ratio: 通道5的香氛比例 int
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_door_open_angle_sts(self, door_pos: DoorId, angle: int, wait_time: Union[float, int] = 0):
        """
        设置门的kd

        :param door_pos: kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param angle:
        :param wait_time:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_door_trigger_source(self, door_pos: DoorId, trigger_source: DoorOpenSource):
        """
        check开门触发源

        :param door_pos: kDoorFrontLeft = 0 kDoorFrontRight = 1 kDoorRearLeft = 2 kDoorRearRight = 3 kDoorAll = 4
        :param trigger_source: 触发源 NoTrigSrc = 0 KeyRem = 1 HMI = 2 Telm = 3 OutdSwt = 4 InsdSwt = 5
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_climate_pm25_sts(self, int_pm25_sts: PM25Sts):
        """
        设置车辆PM2.5状态

        :param int_pm25_sts: PM2.5状态 Initial = 0 Collecting = 1 Complete = 2 Error = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_climate_pm25_value(self, int_pm25_val: int):
        """
        设置车辆PM2.5值

        :param int_pm25_val: PM2.5值 int
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_climate_pm25_level(self, int_pm25_level: PM25Level):
        """
        设置车辆PM2.5等级

        :param int_pm25_level: PM2.5等级 Level1 = 0 Level2 = 1 Level3 = 2 Level4 = 3 Level5 = 4 Level6 = 5 Reserved = 6 Invalid = 7
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_defrost_sts(self, defrost_sts: isOn):
        """
        设置车辆前挡除霜状态

        :param defrost_sts: Off = False On = True
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_outer_rearview_defrost_sts(self, mirr_def_sts: MirrrDefrstrSts):
        """
        设置车辆外后视镜除霜状态

        :param mirr_def_sts: Off = 0 Limited = 1 NotAvailable = 2 TmrOff = 1 AutoCdn = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_climate_temp_req(self, zone: ClimateZone, value: Union[float, int]):
        """
        Check BGM 发出的控制空调温度请求

        :param zone: AllZone = 0 FirstRow = 1 SecondRow = 2 FirstRowLeft = 3 FirstRowRight = 4 SecondRowLeft = 5 SecondRowMiddle = 6 SecondRowRight = 7 FirstRowLeftLeft = 8 FirstRowLeftRight = 9 FirstRowRightLeft = 10 FirstRowRightRight = 11 SecondRowLeftLeft = 12 SecondRowLeftRight = 13 SecondRowRightLeft = 14 SecondRowRightRight = 15
        :param value: 温度值
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_tailgate_opener_sts(self, sts: DoorOpenerSts, time_wait: Union[float, int] = 0):
        """
        设置尾门开关的状态

        :param sts: 尾门状态 Ukwn = 0 FullClsd = 1 MovgOut = 2 MovgOutBrkg = 3 StopDurgOpen = 4 FullOpend = 5 MovgIn = 6 MovgInBrkg = 7 StopDurgCls = 8 HalfClsd = 9 StopMinPntForCls = 0x0A
        :param time_wait:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_usage_mode_status(self):
        """
        获取BGM发出的UsageMode值

        :return: UsageMode int
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_charge_target_soc_value(self, value: Union[float, int], time_wait: Union[float, int] = 0):
        """
        设置目标充电SOC值

        :param value: 目标充电SOC值
        :param time_wait:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_driver_seat_btn_psd_sts(self, sts: bool, time_wait: Union[float, int] = 0):
        """
       仿真主驾座椅本地开关是否激活

       :param sts: bool
       :return:
       """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_driver_seat_ext_adj_allow_sts(self, sts: bool, time_wait: Union[float, int] = 0):
        """
       设置仿真主驾座椅是否可调

       :param sts: bool
       :return:
       """

    @abstractmethod
    def mock_bgm_send_ccp(self, ccp_raw_value, byte_index_to_change=None, change_to_value=None):
        """
        在connectivityCANFD上实现CCP报文发送（TCAM）:模拟BGM发送CCP报文，能够修改任意字节并发送

        :param ccp_raw_value: CCP的初始值，1558个字节
        :param byte_index_to_change: 需要修改CCP的字节序号列表
        :param change_to_value: 需要修改CCP的字节序号对应的值的列表
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_pass_seat_btn_psd_sts(self, sts: bool, time_wait: Union[float, int] = 0):
        """
        仿真副驾座椅本地开关是否激活

        :param sts: bool
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def centrl_lock_pre_msg_send_ctrl(self, sts: MsgSendContrl):
        """
        停止chassiscan1,chassiscan2,passivesafetycan 和部分connectivitycanfd 消息发送

        :param sts: 控制状态 Start = 0 Stop = 1 Pause = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_steer_strength_level_req(self, req: SteerAsscLvl):
        """
        Check BGM 发出的方向盘转动的扭矩等级

        :param req: 请求信号 Ukwn = 0 Lvl1 = 1 Lvl2 = 2 Lvl3 = 3 Lvl4 = 4 Resd5 = 5 Resd6 = 6 Resd7 = 7
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_rear_view_mode(self, pos: ViewPos, mode: MirrStsTyp):
        """
        模拟外后视镜展开折叠状态

        :param pos: 要设置的后视镜 RearRight = 0 RearLeft = 1 All = 2
        :param mode: 设置的目标位置 Undefd = 0 Unfold = 1 Fold = 2 MovgToUnfold = 3 MovgToFold = 4
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_rear_view_direction(self, pos: ViewPos, direction: MirrDirReq):
        """
        模拟外后视镜调节方向

        :param pos: 要设置的后视镜 RearRight = 0 RearLeft = 1 All = 2
        :param direction: 设置的目标位置 Idle = 0 Up = 1 Down = 2 Left = 3 Right = 4
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_climate_angle_req(self, drvr_LeX: int = 0, drvr_LeY: int = 0, pass_LeX: int = 0, pass_LeY: int = 0,
                                drvr_RiX: int = 0, drvr_RiY: int = 0,
                                pass_RiX: int = 0, pass_RiY: int = 0, sec_rowLeX: int = 0, sec_rowLeY: int = 0,
                                sec_rowRiX: int = 0, sec_rowRiY: int = 0):
        """
        Check出风口角度请求

        :param drvr_LeX:
        :param drvr_LeY:
        :param pass_LeX:
        :param pass_LeY:
        :param drvr_RiX:
        :param drvr_RiY:
        :param pass_RiX:
        :param pass_RiY:
        :param sec_rowLeX:
        :param sec_rowLeY:
        :param sec_rowRiX:
        :param sec_rowRiY:
        :return:
        """

    # # @Author:hui.zhao@jiduatuo.com
    # @abstractmethod
    # def check_door_lock_and_unlock_sts(self, drv_lock: Union[LockStatus, None] = None,
    #                                    pass_lock: Union[LockStatus, None] = None,
    #                                    lere_lock: Union[LockStatus, None] = None,
    #                                    rire_lock: Union[LockStatus, None] = None):
    #     """
    #     Check BGM发出的门的锁请求

    #     :param drv_lock: 主驾门锁状态设定值
    #     :param pass_lock: 副驾门锁状态设定值
    #     :param lere_lock: 左后门锁状态设定值
    #     :param rire_lock: 右后门锁状态设定值
    #     :return:
    #     """
    #     pass

    # # @Author:hui.zhao@jiduatuo.com
    # @abstractmethod
    # def set_four_doors_lock_and_unlock_sts(self, lock_sts: LockStatus):
    #     """
    #     同时Check BGM发出的四个门的锁请求

    #     :param lock_sts: 锁状态设定值
    #     :return:
    #     """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_lock_sys_sts(self, req: LockSysStsPrmt):
        """
        同时Check BGM发出的中控锁状态提醒

        :param req: 中控锁状态提醒值
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_central_lock_event_sts(self, evn_update_sts: bool, evn_trigsrc: Union[None, LockTrigerSource] = None):
        """
        同时Check BGM发出的锁动作事件上报

        :param evn_update_sts: 是否有事件上报
        :param evn_trigsrc: 锁操作的触发源
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_low_bean_fault_sts(self, pos: GeneralPos, fault_sts: LampSts):
        """
        设置HCM近光灯状态故障

        :param pos: 灯的位置 Front = 0 Rear = 1 Left = 2 Right = 3 All = 4
        :param fault_sts: 故障状态 Off = 0 On = 1 Error = 2 Reserve = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_high_bean_fault_sts(self, pos: GeneralPos, fault_sts: LampSts):
        """
        设置HCM远光灯状态故障

        :param pos: 灯的位置 Front = 0 Rear = 1 Left = 2 Right = 3 All = 4
        :param fault_sts: 故障状态 Off = 0 On = 1 Error = 2 Reserve = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_blue_id_type_sts(self, key_id: int, type: BlueType, con_sts: ConnSts):
        """
        设置蓝牙的Key_ID为: {key_id},设置蓝牙类型为{type.name},连接状态{con_sts.name}

        :param key_id: 蓝牙的Key_ID
        :param type: NoKeyConnected = 0 NFC_Card = 1 BLE_Key = 2 BLE_UWB_KeyFob = 3 Temp_BLE_Key = 4 ICCE_BLE_Key = 5 ICCE_NFC_Key = 6 CCC_NFC_BLE_UWB_Key = 7 CCC_NFC_Key = 8 CCC_NFC_BLE_Key = 9
        :param con_sts: Disconnect = 0 Connect = 1
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_chrglid_pos(self, sts: int):
        """
        仿真获取充电口盖位置百分比

        :param sts: 充电口盖位置百分比
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_chrgild_req(self, req: ChrgLidReq):
        """
        Check BGM 发出的控制充电口盖请求

        :param req: Idle = 127 Open = 0 Close = 100
        :return:
        """

    def check_chrgild_sts(self, sts: ChrgLidSts):
        """
        Check BGM 发出的充电口盖状态

        :param sts: Unknown = 0 Open = 1 Close = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_chrglid_fault(self, fault_type: ChrdLidFaultType, sts: bool = True, time_wait: Union[float, int] = 0):
        """
        设置充电口盖故障类型为{fault_type.name},故障状态为{sts}

        :param fault_type: ElecErr = 0 TempHigh = 1 VoltHigh = 2 VoltLow = 3 All = 4
        :param sts: bool
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_chrglid_fault_sts(self, sts: isOn):
        """
        Check BGM 发出的充电口盖故障状态

        :param sts: bool
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_door_open_mode_req(self, pos: DoorPos, mode: isOn):
        """
        Check BGM 发出的门的打开模式是

        :param pos: 门的位置 Dirver = 0 Pass = 1 RearLeft = 2 RearRight = 3 Tailgate = 4 All = 5
        :param mode: 模式 Off = False On = True
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_door_switch_light_sts(self, pos: DoorPos, req: LampSts):
        """
        Check BGM 发出的{pos.name}门按键指示灯状态是否为{sts.name}

        :param pos: 门的位置 Dirver = 0 Pass = 1 RearLeft = 2 RearRight = 3 Tailgate = 4 All = 5
        :param req: 等的状态 Off = 0 On = 1 Error = 2 Reserve = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_driver_door_QF_sts(self, sts: FacQlyDoorSts):
        """
        Check BGM 发出的驾驶门QF值

        :param sts: 门QF值 Uknow = 0 Open = 1 Close = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def press_door_inside_switch(self, pos: DoorPos = DoorPos.Dirver, time_interval: Union[int, float] = 3):
        """
        设置内开关按压状态

        :param pos: 门的位置 Dirver = 0 Pass = 1 RearLeft = 2 RearRight = 3 Tailgate = 4 All = 5
        :param time_interval: 按键按下和松开的时间间隔,默认3秒
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_steer_strength_level(self, level: SteerAsscLvl, time_wait: Union[int, float] = 0):
        """
        设置设置方向盘强度等级

        :param level: 强度等级 Ukwn = 0 Lvl1 = 1 Lvl2 = 2 Lvl3 = 3 Lvl4 = 4 Resd5 = 5 Resd6 = 6 Resd7 = 7
        :param time_wait: 执行操作之后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_dc_chrg_handle_sts(self, sts: DCChrgnHndlSts, time_wait: Union[int, float] = 0):
        """
        设置DC充电枪状态

        :param sts: 充电枪状态 Disconnected = 0 ConnectedWithoutPower = 1 PowerAvailableButNotActivated = 2 ConnectedWithPower = 3 Init = 4 Fault = 5
        :param time_wait: 执行操作之后的等待时间
        :return:
        """

    @abstractmethod
    def stop_listen_dk_bgm_response(self):
        """
        结束监视BGM和BNCM的报文交互
        """

    @abstractmethod
    def reset_bncm_digital_keyinfo(self):
        """
        重置钥匙信息, 当前任何区域无钥匙
        """

    @abstractmethod
    def update_keyinfos(self, location: Union[Location, int], keys: List[KeyInfo]):
        """
        配置不同寻钥匙区域, 返回的钥匙信息, 可以是多个钥匙

        :param location: 寻钥匙区域, int类型或者Location类型
        :param keys: 钥匙信息
        :return:
        """

    @abstractmethod
    def send_approach_light_cmd(self, key_type: int = 2, key_id=key_id1):
        """
        发送靠近迎宾指令

        :param key_type: 指令触发源钥匙类型, 默认蓝牙
        :param key_id: 数字钥匙keyid
        :return:
        """

    @abstractmethod
    def send_approach_unlock_cmd(self, key_type: int = 2, key_id=key_id1):
        """
        发送近车解锁指令

        :param key_type: 指令触发源钥匙类型, 默认蓝牙
        :param key_id: 数字钥匙keyid
        :return:
        """

    @abstractmethod
    def send_walk_away_lock_cmd(self, key_type: int = 2):
        """
        发送离车闭锁指令

        :param key_type: 指令触发源钥匙类型, 默认蓝牙
        :return:
        """

    @abstractmethod
    def press_door_outswitch(self):
        """
        按下四门或尾门外开关

        :return:
        """

    @abstractmethod
    def get_recent_signal_raw_value(self, msg_signals_obj: type, signal_name: str):
        """
        立马获取最近收到/发送的报文信号值，不等待，从来没有收到/发送过，返回默认信号值

        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def lin_send_pwm(self, lin_bus: LinChannel, run_time: int = 1000):
        """
        使用Lin总线发送PWM波

        :param lin_bus: 总线名称，仅支持lin总线
        :param run_time: 发送时间，单位微妙，RunTimeOfUs=0，代表一直输出PWM
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_lin_bus_awakeup_result(self, lin_bus: LinChannel, trig_start, trig_stop, exp_time_dif=0.5):
        """
        Check lin唤醒之后之后多久总线进入睡眠

        :param lin_bus: 总线名称，仅支持lin总线
        :param trig_start: 触发开始时间
        :param trig_stop: 触发结束时间
        :param exp_time_dif: 报文发送持续时间check误差
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_hv_batt_thermy_sts(self, sts: HvBattThermReq, time_wait: Union[int, float] = 0):
        """
        设置高压电池状态
        :param sts: 总线名称，高压电池状态
            Idle = 0
            Cooling = 1
            Heating = 2
            Erro = 3
        :param time_wait,执行等待时间
        :return:
        """

    # author:dejian.xiong@jiduauto.com
    @abstractmethod
    def check_PNC(self,
                  bus_name: BusName,
                  msg_id: NMMsgId,
                  pnc_name: Union[BGMPNC, TCAMPNC],
                  signal_value: NMSts,
                  timeout: Union[int, float] = 1,
                  check_time: int = 1):
        """
        检查超时时间内PNC的置位次数

        :param bus_name: 总线名
        :param msg_id: 消息id
        :param pnc_name: PNC名称
        :param signal_value: PNC信号值
        :param timeout: 超时时间
        :param check_time: 检查到PNC的置位次数
        :return:
        """
        pass

    # author:dejian.xiong@jiduauto.com
    @abstractmethod
    def check_PNC_thread_start(self,
                               bus_name: BusName,
                               msg_id: NMMsgId,
                               pnc_name: Union[BGMPNC, TCAMPNC],
                               signal_value: NMSts,
                               timeout: Union[int, float] = 1,
                               check_time: int = 1):
        """
        异步开始检查超时时间内PNC的置位次数

        :param bus_name: 总线名
        :param msg_id: 消息id
        :param pnc_name: PNC名称
        :param signal_value: PNC信号值
        :param timeout: 超时时间
        :param check_time: 检查到PNC的置位次数
        :return:
        """
        pass

    # author:dejian.xiong@jiduauto.com
    @abstractmethod
    def check_PNC_thread_stop(self,
                              bus_name: BusName,
                              msg_id: NMMsgId,
                              pnc_name: Union[BGMPNC, TCAMPNC],
                              timeout: Union[int, float] = 1):
        """
        异步结束检查超时时间内PNC的置位次数

        :param bus_name: 总线名
        :param msg_id: 消息id
        :param pnc_name: PNC名称
        :param timeout: 超时时间
        :return:
        """
        pass

    # author:dejian.xiong@jiduauto.com
    @abstractmethod
    def set_PNC(self,
                bus_name: BusName,
                msg_id: NMMsgId,
                pnc_name: Union[BGMPNC, TCAMPNC],
                signal_value: NMSts,
                frame_type: FrameType):
        """
        设置PNC的值

        :param bus_name: 总线名
        :param msg_id: 消息id
        :param pnc_name: PNC名称
        :param signal_value: 超时时间
        :param frame_type: 0表示快帧 1表示慢帧
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def telm_set_chrglid_sts(self, sts: ChrgLidOpenCloseSts, time_wait: Union[int, float] = 0):
        """
        APP设置充电口盖状态
        :param sts: 开关状态
            Ukwn = 0
            Open = 1
            Close = 2
        :param time_wait:执行操作之后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_pos_lamp_sts(self, pos: GeneralPos, sts: PosnLampSts, time_wait: Union[int, float] = 0):
        """
        设置位置灯状态
        :param front_rear:设置前后位置灯
            Front = 0
            Rear = 1
        :param pos:设置的灯的位置
            Left = 2
            Mid = 5
            Right = 3
            All = 4
        :param sts:设置状态
            Off = 0
            On = 1
            Error = 2
            Resd = 3
        :param time_wait:执行操作之后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_steerwheel_turn_lamp_sts(self, type: VehType, rotate_direc: RotateDirec, sts: SteerWhlTouchSwt):
        """
        设置方向盘转向灯开关状态
        :param type:车的类型，老款（CCP 629==0x4,OR 0x5）和新款（CCP629==0x6）
        :param rotate_direc:方向盘转动方向
            Left = 0
            Right = 1
            All = 2
        :param sts:方向盘状态
            NotAvailble = 0
            ShortPress = 1
            LongPress = 2
            Error = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_turn_lamp_act_req(self, sts: IndcrSts, act_sts: IndcrSts):
        """
        Check 转向灯请求
        :param sts:
            Off = 0
            LeOn = 1
            RiOn = 2
            LeAndRiOn = 3
        :param act_sts:
            Off = 0
            LeOn = 1
            RiOn = 2
            LeAndRiOn = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_turn_indcr_lamp_sts(self, pos: LampPos, sts: PosnLampSts, time_wait: Union[int, float] = 0):
        """
        设置HCM/RCM反馈转向灯状态
        :param pos:灯的位置
            FrontLeft = 0
            FrontRight = 1
            RearLeft = 2
            RearMid = 3
            RearRight = 4
            All = 5
        :param fault_sts:故障状态
            Off = 0
            On = 1
            Error = 2
            Resd = 3
        :param time_wait:执行之后的等待时间
        :return:
        """

    # @Author：hui.zhao @jiduatuo.com
    @abstractmethod
    def check_outside_turn_lamp_act_sts(self, pos: GeneralPos, act_sts_le: PosnLampSts, act_sts_ri: PosnLampSts,pos_sts: IndcrSts):
        """
        检查外部转向灯状态
        :param pos:灯的前后位置（只使用前、后）,枚举型：GeneralPos
            Front = 0
            Rear = 1
            Left = 2
            Right = 3
            All = 4
        :param act_sts_le:左转向灯激活状态,枚举型：PosnLampSts
            Off = 0
            On = 1
            Error = 2
            Resd = 3
        :param act_sts_ri:右转向灯激活状态,枚举型：PosnLampSts
            Off = 0
            On = 1
            Error = 2
            Resd = 3
        :param pos_sts:指示灯的状态,枚举型：IndcrSts
            Off = 0
            LeOn = 1
            RiOn = 2
            LeAndRiOn = 3
        :return:
        """

    @abstractmethod
    def trigger_call_sos_by_can(self):
        """
        模拟发送CAN信号CrashStsSafeSts=Crash,触发xcall
        :returns: 
        """
        pass
    
    @abstractmethod
    def set_hv_batt_thermy_sts(self,sts:HvBattThermReq,time_wait:Union[int,float] = 0):
        """
        设置高压电池状态

        :param sts: 总线名称，高压电池状态 Idle = 0 Cooling = 1 Heating = 2 Erro = 3
        :param time_wait：执行等待时间
        :return:
        """

    @abstractmethod
    def set_fota_download_wake_condition(self, display_hv_soc: Union[int, float], low_volt_soc: Union[int, float]):
        """
        设置常规OTA下载唤醒条件
        :param display_hv_soc: 大电池电量SOC
        :param low_volt_soc: 小电池电量SOC
        :return:
        """
        pass

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_signal_value_and_times(self,bus:str,msg:str,signal:str,value:Union[int,float],times:Union[int,str],timeout:Union[int,float] = 3):
        """
        Check 总线上发出的信号的值以及次数
        :param bus: 总线名字,str,例如:"cem_lin6"
        :param msg: 消息名字,str,例如:"BgmCem_Lin6Fr01"
        :param signal: 信号名字,str,例如:"ActvReSplrPosnCmd"
        :param value: 希望信号的值,int or float,例如:1
        :param msg: 信号发送次数,times, int or str 例如:3,如果检测有帧，但是不确定数量是可以输入字符串,例如"Not 0"
        :param timeout:检测时间，默认3秒
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_brake_pedal(self,safe:Union[None,YesOrNo] = YesOrNo.Yes,qf:Union[None,ValueQf] = ValueQf.AccurData,sts:Union[None,YesOrNo] = YesOrNo.Yes):
        """
        :param safe:刹车踏板安全校验
            No = 0
            Yes = 1
        设置刹车踏
        :param qf:刹车踏板QF值
            UndefindDataAccur = 0
            TmpUndefdData = 1
            DataAccurNotWithinSpcn = 2
            AccurData = 3
        :param sts:设置踩刹车状态
            No = 0
            Yes = 1
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_brake_req_light_on_sts(self,sts:ReqSts):
        """
        设置自动刹车灯请求状态
        :param sts:请求状态
            NotReqd = 0
            Reqd = 1
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_emergency_brake_req_light_on_sts(self,req:EmgyBrkLiReq):
        """
        设置紧急制动
        :param req:紧急制动状态
            NotInProgs = 0
            InProgs = 1
            InProgsAtSpdLo = 2
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_brake_light_act_sts(self,lamp_sts:isOn,mid_lamp_sts:isOn):
        """
        检查刹车灯开启状态
        :param lamp_sts:检测激活刹车灯状态,布尔型
            Off = False
            On = True
        :param mid_lamp_sts:检测激活中央刹车灯状态,布尔型
            Off = False
            On = True
        :return:
        """


    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_brake_light_sts(self,sts:ExtrLtgSts):
        """
        检车刹车灯状态
        :param sts:车灯状态
            Off = 0
            On = 1
            Err = 2
            Resd = 3
            Auto = 4
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_brake_lamp_fault_sts(self,pos:GeneralPos,sts:ExtrLtgSts):
        """
        设置刹车灯故障状态
        :param pos:灯位置
            Left = 2
            Right = 3
            Mid = 5
        :param sts:
            Off = 0
            On = 1
            Err = 2
            Resd = 3
            Auto = 4
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_brake_pedal_sensor_sts(self,sts:BrkPedlSnsrSt):
        """
        设置辅助踏板传感器
        :param sts:传感器状态
            NoInfo1 = 0
            NotPsd = 1
            Psd = 2
            NoInfo2 = 3
        :return:
        """
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_rear_fog_sts(self, actn_sts: isOn, extr_light_sts: ExtrLtgSts):
        """
        检查后雾灯开启状态
        :param actn_sts:开关状态
            Off = False
            On = True
        :param extr_light_sts:激活状态
            Off = 0
            On = 1
            Err = 2
            Resd = 3
            Auto = 4
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_rear_fog_fault_sts(self,pos:GeneralPos,sts:ExtrLtgSts):
        """
        设置后雾灯故障状态
        :param pos:位置
            Left = 2
            Right = 3
            All = 4
        :param sts:状态
            Off = 0
            On = 1
            Err = 2
            Resd = 3
            Auto = 4
        """
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_door_rels_req(self,Drv:Union[DoorRelsReq, None] = None, Pass:Union[DoorRelsReq, None] = None,
                            ReLe:Union[DoorRelsReq, None] = None,RiRe:Union[DoorRelsReq, None] = None,
                            Tr: Union[DoorRelsReq, None] = None):
        """
        check五门电释放请求状态
        :param Drv:主驾门
            Invld = 0
            On = 1
            Off = 2
            Invld2 = 3
        :param Pass:副驾门
            Invld = 0
            On = 1
            Off = 2
            Invld2 = 3
        :param ReLe:左后门
            Invld = 0
            On = 1
            Off = 2
            Invld2 = 3
        :param RiRe:右后门
            Invld = 0
            On = 1
            Off = 2
            Invld2 = 3
        :param Tr:尾门
            Invld = 0
            On = 1
            Off = 2
            Invld2 = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_ble_bus_siginal_veh_body(self,func_module:BleVehicleBody,sub_func:Union[TirePos,DoorId,WindowId,ViewPos,None],value:Union[int,float]):
        """
        模拟发送蓝牙VehicleBody功能相关得总线数据
        :param func_module:VehicleBody中得功能模块
            TailGate = 0
            Bonnet = 1
            CentralLock = 2
            TailWing = 3
            Tire = 4
            Doors = 5
            Wins = 6
            OuterRearView = 7
        :param sub_func:func_module中对应得子功能模块
        :param value:设置得信号值
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_ble_bus_siginal_charge(self,func_module:BleEicCharg,sub_func:Union[BleCharging,BleBatteryInfo],value:Union[int,float]):
        """
        模拟发送蓝牙EicCharging功能相关得总线数据
        :param func_module:EicCharging 中得功能模块
            Charging = 0
            BatteryInfo = 1
        :param sub_func:func_module中对应得子功能模块
        :param value:设置得信号值
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_singal(self,bus: str,msg: str,signal: str,value: Union[str, int, float],wait_time:Union[int,float] = 0):
        """
        总线信号设置接口
        :param bus: 总线名称,字符串，例如：bodycan or BodyCAN
        :param msg: 消息名称,字符串，例如：DdmBodyFr04
        :param signal: 信号名称,字符串，例如WinPosnStsAtDrvr
        :param value: 信号值 数据类型，整型，浮点型，字符串
        :param wait_time: 设置信号之后的等待时间(单位：秒)，整型，浮点型,默认0
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_singal(self,bus: str,msg: str,signal: str,value: Union[str, int, float],timeout:Union[int,float] = 5,do_assert = True,check_time = 1):
        """
        总线信号检测接口
        :param bus: 总线名称,字符串，例如：bodycan or BodyCAN
        :param msg: 消息名称,字符串，例如：DdmBodyFr04
        :param signal: 信号名称,字符串，例如WinPosnStsAtDrvr
        :param value: 信号值 数据类型，整型，浮点型，字符串
        :param timeout: 检测时间(单位：秒)，整型，浮点型，默认5s
        :param do_assert: 是否需要assert判断，bool，默认True
        :param check_time:检测信号的次数，默认1次
        :return:
        """

    def set_wti_signal(func:WTI_Func,value):
        """
        设置wti功能相关总线信号
        @param func:WTI功能 枚举：WTI_Func,功能太多不便展示
        @param value：设置的信号值
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_bms_related_signal(self,type:BMSWakeUpSetType,value:Union[GeneralSts,int,float]):
        """
        Check BMS相关信号
        @param type:BMS相关功能 枚举：
            ChrgnCurrThd = 0
            ChrgnCurrEna = 1
            DisChrgnCurrThd = 2
            DisChrgnCurrEna = 3
            SocEna = 4
            SocThd = 5
            VolThd = 6
            VolEna = 7
            TiChrgnAtSleepThd = 8
        @param value：Check的信号值
        :return:
        """

        
    @abstractmethod
    def get_all_can_channel_info(self):
        '''
        获取所有can通道 名字 索引号
        @return: 返回列表
        '''

    @abstractmethod
    def get_all_can_channel_index(self):
        '''
        获取所有can 通道的 索引
        @return:
        '''

    @abstractmethod
    def get_can_channel_index_by_name(self, bus_name: str):
        '''
        根据通道名字获取通道序号
        @param bus_name:
        @return:
        '''
    @abstractmethod
    def get_can_name_by_index(self, index: int):
        '''
        根据通道序号获取通道名字
        @param index:
        @return:
        '''

    @abstractmethod
    def recv_mul_can_channel_msg(self, can_chnanel_lis=[0, 4, 7, 9], msg_id=0x7ff, unexpect_msg=[0x02, 0x3e, 0x80],
                                 timeout=1, **kwargs):
        '''
        接收 多路 can，在某个id 段的报文
        @param can_chnanel_lis: can 通道对应的 索引
        @param msg_id: 可以为整数，或者一个元祖（min_id,max_id）
        @param unexpect_msg: 过滤的 报文内容 默认过滤 3e 80
        @param timeout:
        @return:
        '''

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_windows_position_req(self, pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        """
        Check BGM发出的窗户开度请求
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
        pass
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_windows_short_drop_req(self, pos_drvr: Union[WinShortDropReq, None] = None, pos_pass: Union[WinShortDropReq, None] = None,
                             pos_lere: Union[WinShortDropReq, None] = None, pos_rire: Union[WinShortDropReq, None] = None):
        """
        Check BGM发出的窗户短降请求
        :param pos_drvr: 左前短降请求，枚举型：
            Idle = 0
            Close = 1
            Open = 2
        :param pos_pass: 右前短降请求,
        :param pos_lere: 左后短降请求
        :param pos_rire: 右后短降请求
        :return:
        """
        pass
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_windows_without_short_drop_req(self, pos_drvr: Union[WinPos, None] = None, pos_pass: Union[WinPos, None] = None,
                             pos_lere: Union[WinPos, None] = None, pos_rire: Union[WinPos, None] = None):
        """
        Check BGM没有发出的窗户短降请求
        :param pos_drvr: 左前车窗开度，枚举型：
            Idle = 0
            Close = 1
            Open = 2
        :param pos_pass: 右前车窗开度,
        :param pos_lere: 左后车窗开度
        :param pos_rire: 右后车窗开度
        :return:
        """
        pass
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_5_door_lock_status(self, status:CenLockSts):
        """
        模拟反馈5门锁的状态
        :param status: 锁状态
            Unlock = 1
            TrUnlock = 2
            Lock = 3
        :return:
        """
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_pos_laom_act_sts(self,actn_sts: isOn,pos:GeneralPos, aextr_light_sts: ExtrLtgSts):
        """
        检查位置灯开启状态
        :param actn_sts:位置灯使能状态
            Off = False
            On = True
        :param pos:位置
            Front = 0
            Rear = 1
        :param aextr_light_sts:位置灯状态
            Off = 0
            On = 1
            Err = 2
            Resd = 3
        :return:
        """

    @abstractmethod
    def start_record_trace_log(self, file_name):
        """
        开始异步录制trace log
        @param file_name: 文件名称 一般是case_name
        @return:
        """
        pass

    @abstractmethod
    def stop_record_trace_log(self, is_record_status=True):
        """
        停止录制trace log
        @param is_record_status: 录制状态，如果为false时，不会作为allure附件
        @return:
        """
        pass

    @abstractmethod
    def check_bus_recv_message(self, bus_name, timeout=5):
        '''
        通常逻辑一般会搭配 resume_bus_send 使用,检查总线上是否有报文发出
        @param bus_name: 通道名称
        @param timeout: 超时时间默认5s
        @return: bool/None 检查总线上是否收到报文, 收到了返回 True, 超时没有收到返回 None
        '''

    @abstractmethod
    def check_ecu_not_recv_message(self, ecu_name, timeout=5):
        """
        检查超时时间内，对应的ecu节点是否没有收到报文

        @param ecu_name: ECU节点的名称
        @param timeout: 超时时间默认5s
        @return: True/False 检查超时时间内，对应的ecu节点是否没有收到报文, 收到了返回 False, 超时没有收到返回 True
        """

    # @Author:shulin.zheng@jiduatuo.com
    @abstractmethod
    def check_RTC_time(self,rtc_time):
        """
        查询RTC补电超时时间
        :param rtc_time:10~7200 分钟
        :param return:
        """ 

    # @Author:shulin.zheng@jiduatuo.com
    @abstractmethod
    def set_BMS_wukeup_mode(self,bms_type:BattSnsrType,wakeup_src:BMSWakeUpTrgSrc):
        """
        检查BMS智能补电
        :param bms_type:检查BMS补电方式
            NAWC=3
            AWC=0
            Reserved01=1
            Reserved02=2
        :param wakeup_src:触发BMS智能补电
            NotReqd=0
            LoSOC=1
            LoVoltage=2
            ChrgnCurrent=3
            DisChrgnCurrent=4
            Reserved1=5
            Reserved2=6
            Reserved3=7
        :return:
        """

    # @Author:shulin.zheng@jiduatuo.com
    @abstractmethod
    def set_BMS_stop_req(self,low_sts:SocSts,
                         low_soc:Union[float, int, None] = None,
                         low_soh:Union[float, int, None] = None
                         ):
        """
        设置BMS停止智能补电
        :param low_soc:设置BMS采集电池SOC
            0%~100%
        :param low_sts:设置BMS采集电池STS
            Larger15Per=0
            LessOrEqual15Per=1
            LessOrEqual10Per=2
            Invalid=3
        :param low_soh:设置BMS采集电池SOH
            0%~100%
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_cem_and_vmm_communication_error(self,fault_sts:GeneralFltSts):
        """
        Check CEM和VMM通信故障状态
        :param fault_sts:故障状态
            NotVld1 = 0
            Off = 1
            On = 2
            NotVld2 = 3
        :return:
        """
        
    # @Author:shulin.zheng@jiduatuo.com
    @abstractmethod
    def check_hv_volt_warning(self,LVChrgnFailWarn:Motorola):
        """
        检测低压补电失败告警状态
        :param LVChrgnFailWarn:失败告警状态
            idle = 0
            Warning = 1
            NoWarning = 2
            Reserved = 3
        :return:
        """
        
    # @Author:quan.sun@jiduatuo.com
    @abstractmethod
    def get_lin_scheduleTable(self, lin_bus:str):
        """
        获取lin的调度表信息
        
        :param lin_bus: lin bus 名    such as  "cem_lin1"
        :returns lin_scheduleTable_new: dict   such as {'Cem_Lin1_DiagResponseSchedule01': [(0, 'DiagResponse', 61, 8, 0.015)]}   
            (0, 'DiagResponse', 61, 8, 0.015) 解释：（lin调度表中的位置，lin msg 名字，msg id， length ，delay）
        """

    def check_lin_schedule_table(self, lin_bus, check_field=None, check_value=None, need_new_data=False):
        """
        获取lin的调度表信息

        :param lin_bus: lin bus 名    such as  "cem_lin1"
        :param check_field: 检查的字段，如:$.data.list[0].treeList[0].nodeList[1].conditionExpressionList[0].extras.rightValue
        :param check_value: 检查的字段的值，如：check_value=1
        :param need_new_data: 需要更新数据，为保证不频繁拿数据校验默认为False
        """
    
    @abstractmethod
    def set_tire_config_req(self):
        """
        触发胎压配置报文
        :return:
        """

    @abstractmethod
    def check_tire_config(self, id: list, config: list, is_id: bool, is_config: bool):
        """
        检查发送的胎压配置报文是否和预期一致
        @param id:预期的胎压配置报文的配置ID
        @param config:预期的胎压配置报文的配置
        @parm is_id:是否检查配置ID一致
        @parm is_config:是否检查配置一致
        :return:
        """

    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def check_relay_cmd(self, KL151: Union[RelaySts, None] = None,
                            KL152: Union[RelaySts, None] = None,
                            KL153: Union[RelaySts, None] = None,
                            climate: Union[RelaySts, None] = None,
                            batterysaver: Union[RelaySts, None] =None):
        """
        校验继电器使能状态 0x0 Off 0x1 On
        :param KL151: 请求KL15-2继电器闭合使能状态
            Off = 0
            On = 1
        :param KL152: 请求KL15-2继电器闭合使能状态
        :param KL153: 请求KL15-1继电器闭合使能状态
        :param climate: 请求鼓风机继电器闭合使能状态
        :param batterysaver: 请求节电继电器闭合使能状态
        :return:
        """
    
    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def set_lidar_req(self, Lidar: Union[RelaySts, None] = None):
        """
        设置雷达供电请求 0x0 Off 0x1 On
        :param Lidar:雷达电源上电请求
            Off = 0
            On = 1
        :return:
        """
        
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_drl_act_sts(self, actn_sts: isOn, extr_light_sts: ExtrLtgSts):
        """
        检测日行灯相关状态

        :param actn_sts: 日行灯激活状态请求 Off = False On = True
        :param extr_light_sts: 外灯状态请求 Off = 0 On = 1 Err = 2 Resd = 3 Auto = 1
        :return:
        """
        
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_high_beam_sts(self, hb_actn_sts:isOn, extr_light_sts: ExtrLtgSts,flash_light_sts:ExtrLtgSts):
        """
        检查远光灯开启状态
        :param actn_sts:位置灯使能状态
            Off = False
            On = True
        :param extr_light_sts:远光灯状态
            Off = 0
            On = 1
            Err = 2
            Resd = 3
        :param flash_light_sts:闪光灯状态
            Off = 0
            On = 1
            Err = 2
            Resd = 3
        :return:
        """
        
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_drl_fault_sts(self, pos: GeneralPos, fault_sts: LampSts):
        """
        设置HCM近光灯状态故障

        :param pos: 灯的位置 Front = 0 Rear = 1 Left = 2 Right = 3 All = 4
        :param fault_sts: 故障状态 Off = 0 On = 1 Error = 2 Reserve = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_pedal(self,sts:Union[None,YesOrNo] = YesOrNo.Yes):
        """
        :param sts:设置踩刹车状态
            No = 0
            Yes = 1
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_child_lock_sts(self,pos:GeneralPos,sts:ChdLockSts):
        """
        设置对应儿童锁状态
        :param pos:儿童锁位置
            Left = 2
            Right = 3
            All = 4
        :param sts:儿童锁状态
            Invld1 = 0
            On = 1
            Off = 2
            Invld2 = 3
        :return:
        """
        
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_reverse_lamp_act_sts(self, actn_sts: isOn, extr_light_sts: ExtrLtgSts):
        """
        检测倒车灯相关状态
        :param actn_sts: 倒车灯激活状态请求 Off = False On = True
        :param extr_light_sts: 外灯状态请求 Off = 0 On = 1 Err = 2 Resd = 3 Auto = 1
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_reverse_lamp_fault_sts(self, pos: GeneralPos, fault_sts: LampSts):
        """
        设置HCM倒车灯状态
        :param pos: 灯的位置 Front = 0 Rear = 1 Left = 2 Right = 3 All = 4
        :param fault_sts: 故障状态 Off = 0 On = 1 Error = 2 Reserve = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_drvrdes_sts(self, drvrdes: DrvrDesDir):
        """
        设置HCM近光灯状态故障
        :param drvrdes: 车辆挡位为  Undefd = 0 Fwd = 1 Rvs = 2 Neut = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_accr_pedl_press_act(self, act: isOn):
        """
        设置车辆挡位车辆加速踏板踩下
        :param act: 踩下激活状态
            Off = False
            On = True
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_accr_pedl_press_sts(self, sts: isOn):
        """
        设置车辆挡位车辆加速踏板踩下状态
        :param sts: 踩下状态
            Off = False
            On = True
        :return:
        """
         
    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def check_tailgate_without_opener_req(self, timeout=1):
        """
        Check在条件不满足的情况下BGM不发送尾门开关停动作请求

        :return:
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def check_tailgate_without_opener_rels(self, timeout=1):
        """
        在条件不满足的情况下BGM不发送尾门电释放请求

        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_steer_wheel_touch_switch_sts(self,pos:SteerWhlTouchSwtPos,sts:SteerWhlTouchSwtSts):
        """
        设置{pos.name}方向盘按键状态为:{sts.name}
        :param pos: 方向盘按键位置
            Left1 = 0
            Left2 = 1
            Left3 = 2
            Right1 = 3
            Right2 = 4
            Right3 = 5
        :param sts: 按键状态
            NotAvailble = 0
            ShortPress = 1
            LongPress = 2
            Error = 3
        :return:
        """

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_brake_light_act_cycle_sts(self):
        """
        查看刹车灯是否循环亮灭,包括激活刹车灯:ActnOfLedStopLampActnOfLedStopLamp和激活中央刹车灯:ActnOfLedStopLampMid)
        :param:
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_cllsnthreat(self, cllsnthreat: CllsnThreat1):
        """
        设置子系统的危险级别
        
        :param cllsnthreat:子系统的危险级别
            ukwn = 0
            threatlo = 1
            threatmed = 2
            threathi = 3
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_batturaw(self, BattURaw: int):
        """
        设置电池电压
        
        :param BattURaw:电池电压
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_battiraw(self, BattIRaw: int):
        """
        设置电池电流
        
        :param BattURaw:电池电流
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_fltelecdcdc(self, fltelecdcdc: BattSnsrHwFltRaw):
        """
        设置DCDC的电气故障指示
        
        :param fltelecdcdc:电气故障指示
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_flttdcdc(self, flttdcdc: BattSnsrHwFltRaw):
        """
        设置DCDC的温度故障指示
        
        :param flttdcdc:温度故障指示
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_pwrlvlelec(self, mai: int, subtype: int):
        """
        检查车辆的电功率水平
        
        :param mai:电功率主状态
        :param subtype:电功率子状态
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_battsoc_less_15(self):
        """
        设置battsoc的状态小于15
        
        :param:
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_hb_fail_flag_sts(self, hb_flag_sts: ExtrLtgSts):
        """
        检查远光灯开启状态
        :param hb_flag_sts:远光灯状态
            Off = 0
            On = 1
        :return:
        """
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_turn_indicate_lamp_req(self, sts: IndcrSts):
        """
        Check 转向指示灯状态
        :param sts:
            Off = 0
            LeOn = 1
            RiOn = 2
            LeAndRiOn = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def send_awakeup_msg(self,bus:str,id:int,payload:str,times:int,interval:int):
        """
        在总线{bus}上以时间间隔{interval}ms 循环发送{times}次 ID为：{id}，负载为{payload}的报文
        :param bus: 总线
        :param id: 消息ID
        :param payload: 消息负载
        :param times: 发送次数
        :param interval: 时间间隔
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_key_not_prsnt_msg_to_drvr(self, flag: bool):
        """
        检查车辆是否无钥匙启动的HMI状态
        
        :param flag: 是否
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_strt_msg_to_mod_mngt(self, StrtMsgToModMngt: StrtMsgToModMngt):
        """
        设置请求的启动的状态
        
        :param StrtMsgToModMngt:
            NoInhb = 0
            PwrUpDly = 1
            AltvStrt = 2
            inhbremstrt = 3
            diremstrt = 4
            SelnOfParkOrNeut = 5
            Resd1 = 6
            Resd2 = 7
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_strt_msg_to_drvrr(self, StrtMsgToDrvrg: StrtMsgToDrvrg):
        """
        检查启动相关的信息显示
        
        :param StrtMsgToDrvrg:
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
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_strtinprogs(self, StrtInProgs: StrtInProgs):
        """
        检查启动和关闭动力系统的消息
        
        :param StrtInProgs:
            StrtStsOff = 0
            StrtStsImminent = 1
            StrtStsStrtng = 2
            StrtStsRunng = 3
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_trsm_park_lockd(self, TrsmParkLockd: TrsmParkLockd):
        """
        设置驻车锁定状态
        
        :param TrsmParkLockd:
            ParkNotEngd = 0
            ParkEngd = 1
            NotInUse = 2
            Undefd = 3
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_veh_not_park_info_warn(self, VehNotParkInfoWarn: VehNotParkInfoWarn):
        """
        检查未驻车提示告警
        
        :param VehNotParkInfoWarn:
            NoTxt = 0
            ShifttoP = 1
            OutofP = 2
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_gearlvrillmnSts(self, GearLvrIllmnSts: isOn):
        """
        设置换挡器触摸状态
        
        :param GearLvrIllmnSts:
            Off = False
            On  = True
        :return:
        """
    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def set_door_lock_sts(self, drv_lock: Union[Locksts, None] = None, pass_lock: Union[Locksts, None] = None,
                          lere_lock: Union[Locksts, None] = None, rire_lock: Union[Locksts, None] = None):
        """
        设置四门锁状态
        :param drv_lock: 主驾门锁
        :param pass_lock: 副驾门锁
        :param lere_lock: 左后驾门锁
        :param rire_lock: 右后门锁
        :param CenLockSts: 上锁状态
            Ukwn = 0
            Unlock = 1
            lock = 2
            safeLock = 3
        :return:
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    def check_crashunllock_failrSts(self, unlockfail: Union[Unlockfailtohmi, None] = None):
        """
        获取总线Crash解锁失败状态
        :param Unlockfailtohmi: 上锁状态
            SafeInvld1 = 0
            SafeOn = 1
            SafeOff = 2
            SafeInvld2 = 2
        :return:
        """
        pass

    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_battcp_estimd(self, BattCpEstimdRaw: int):
        """
        设置估计电池容量
        
        :param BattCpEstimdRaw:Ah
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_egyavldelta(self, delta: int):
        """
        检查电池的可用余量
        
        :param delta:Ah
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_egyavlwarn(self, warn: int):
        """
        检查电池的发出告警前的可用能量
        
        :param warn:Ah
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_egylvlelec(self, mai: int, subtype: int):
        """
        检查车辆的能量水平
        
        :param mai:主能量水平
        :param subtype:主能量水平
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_battsocraw2_less_value(self, battsocraw2: int, wait_time: int=1000):
        """
        使规定时间内battsocraw2小于预期的值
        
        :param battsocraw2:预期的值
        :param wait_time:超时时间
        :return:
        """
        
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_battsocraw2_more_value(self, battsocraw2: int, wait_time: int=2000):
        """
        使规定时间内battsocraw2大于预期的值
        
        :param battsocraw2:预期的值
        :param wait_time:超时时间
        :return:
        """
        
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def wait_time_and_check_egylvlelec(self, mai_new: int, subtype_new: int, mai_old: int, subtype_old: int, time: int, ):
        """
        检查车辆能量水平指定时间内的变化状态
        
        :param mai_new:预期的主能量水平
        :param waitsubtype_new_time:预期的子能量水平
        :param mai_old:当前的主能量水平
        :param subtype_old:当前的子能量水平
        :param time:指定时间
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_crashsts_safests(self, CrashSts: crashsts):
        """
        设置crash状态信号
        
        :param CrashSts:
            NoCrash = 0
            Crash = 1
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_egylvlelec_drvinfo(self, info: int):
        """
        检查能量通知
        
        :param info:能量通知
        :return:
        """
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_rain_sensor_fault_sts(self,type:RainSensorFaultType,sts:bool):
        """
        设置雨量传感器系统故障状态
        :param :type 传感器故障类型
            SensorFault = 0
            CalibrationFault = 1
            All = 2
        :param :sts 传感器故障状态，bool
        :return:
         """
    # @Author:jianwen.wang@jiduatuo.com
    @abstractmethod
    def set_charging_sts(self, sts: ChargingSts ):
        """
         设置充电状态
        :param :充电状态
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
        :return:
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def send_ccp_to_tcam(self, ccp_byte_index: int = 566, ccp_value: int = 0x10):
        """
        在connectivityCANFD上实现CCP报文发送（TCAM）:模拟BGM发送CCP报文，能够修改任意字节并发送
        :param ccp_byte_index: 需要修改CCP的字节序号
        :param ccp_value: 需要修改CCP的字节序号对应的值
        """
        pass

    # @Author:xiangyue.li@jiduatuo.com
    @abstractmethod
    def set_wpcmodule_sts(self, sts: WpcModule ):
        """
         设置无线充电状态
        :param :无线充电状态
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
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_wiper_mode_req(self,req:WiperMode):
        """
        检查BGM发出控制雨刮的请求
        :req :雨刮请求
            Off = 0
            SingleWipe = 1
            IntLow = 2
            IntHigh = 3
            Low = 4
            High = 5
            Auto = 6
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_ahl_act_sts(self, actn_sts: isOn, extr_light_sts: ExtrLtgSts):
        """
        检查后雾灯开启状态
        :param actn_sts:开关状态
            Off = False
            On = True
        :param extr_light_sts:激活状态
            Off = 0
            On = 1
            Err = 2
            Resd = 3
            Auto = 4
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_ahl_fault_sts(self, pos: GeneralPos, fault_sts: LampSts):
        """
        设置HCM倒车灯状态
        :param pos: 灯的位置 Front = 0 Rear = 1 Left = 2 Right = 3 All = 4
        :param fault_sts: 故障状态 Off = 0 On = 1 Error = 2 Reserve = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_pib_sts(self, pib_sts: DiagActLineSts):
        """
        设置pib状态
        :param pib_sts:  pin状态 DisActive = 0 Active = 1
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_wiper_mode(self, mode: WipgAutFrntMod):
        """
        模拟反馈雨刮模式
        :param mode:  反馈的雨刮模式
            Off = 0
            ImdtMod = 1 
            IntlMod = 2 
            ContnsMod = 3
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_wiper_rain_level(self, level: int):
        """
        设置雨量大
        :param level:  雨量大,int
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_wiper_ambient_light_intensity(self,qf:Union[int,None]=None,value:Union[int,None]=None):
        """
        设置环境光强度
        :param qf:int
        :param value:int
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_solar_value(self,left_vlaue:Union[int,None]=None,right_value:Union[int,None]=None):
        """
        设置阳光强度
        :param left_vlaue:左边传感器检测强度，int
        :param right_value:右边传感器检测强度，int
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_pnc_valid_last_time(self,
                  bus_name: BusName,
                  msg_id: NMMsgId,
                  pnc_name: Union[BGMPNC, TCAMPNC],
                  last_time: Union[int,float]):
        """
        检查总线{bus_name}上PNC：{pnc_name.name}置位的持续时间是否为{last_time}(允许0.5秒的偏差)
        :param bus_name: 总线名
        :param msg_id: 消息id
        :param pnc_name: PNC名称
        :param last_time: 检测的持续时间
        :return:
        """


    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_turn_lamp_always_off(self,pos:GeneralPos,last_time:Union[float,int]):
        """
        Check {pos.name}转向灯是否处于关闭状态
        :param pnc_name: 转向灯位置
        :param last_time: 检测的持续时间
        :return:
        """


    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_keeperreq(self, usagemode:UsageMode):
        """
        检查模式维持请求
        
        :param usagemode:使用模式
            ABANDONED = 0
            INACTIVE = 1
            CONVENIENCE = 2
            ACTIVE = 11
            DRIVING = 13
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_keeperreq_act(self, usagemode:UsageMode):
        """
        检查模式请求仲裁
        
        :param usagemode:使用模式
            ABANDONED = 0
            INACTIVE = 1
            CONVENIENCE = 2
            ACTIVE = 11
            DRIVING = 13
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_carmode_dispd(self, carmoddisp1:CarModDisp1):
        """
        检查carmode展示信息
        
        :param carmoddisp1:使用模式
            CarModDisp1_NoDisp = 0
            CarModDisp1_Facy = 1
            CarModDisp1_FacyStop = 2
            CarModDisp1_Trnsp = 3
            CarModDisp1_TrnspStop = 4
            CarModDisp1_Dyno = 5
            CarModDisp1_Norm = 6
            CarModDisp1_Crash = 7
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_carmode_dispd_in_time(self,carmode:CarMode, subtype: int, carmoddisp1_old:CarModDisp1, carmoddisp1_new:CarModDisp1, time:int = 10, is_change:bool=True):
        """
        检查carmode在指定时间的信息显示和变化
        
        :param carmode:车辆模式
        :param subtype:车辆模式
        :param carmoddisp1_old:车辆模式当前显示
        :param carmoddisp1_old:车辆模式变化后显示
        :param time:多长时间内
        :param  is_change:是否发生变化
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_key_nfc_vmm_prsnt(self, keyprsnt: Keyprsntsts):
        """
        检查寻钥状态
        
        :param keyprsnt:寻钥状态
            KeyPrsntStsIdle = 0
            KeyPrsntStsInProgs = 1
            KeyPrsntStsNotPrsnt = 2
            KeyPrsntStsPrsnt = 3
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_key_nfc_vmm_prsnt_in_time(self, keyprsnt_old: Keyprsntsts, keyprsnt_new: Keyprsntsts, time:int = 10, is_change:bool=True):
        """
        检查寻钥状态在指定时间的信息显示和变化
        
        :param keyprsnt_old:寻钥状态当前
        :param keyprsnt_new:寻钥状态变化后
        :param time:多长时间内
        :param  is_change:是否发生变化
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_strt_msg_to_drvrr_in_time(self, StrtMsgToDrvrg_old: StrtMsgToDrvrg, StrtMsgToDrvrg_new: StrtMsgToDrvrg, time:int = 10, is_change:bool=True):
        """
        检查启动信息在指定时间的信息显示和变化
        
        :param StrtMsgToDrvrg_old:启动信息当前
        :param StrtMsgToDrvrg_new:启动信息变化后
        :param time:多长时间内
        :param  is_change:是否发生变化
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_key_not_prsnt_msg_to_drvr_in_time(self, flag_old: bool, flag_new: bool, time:int = 10, is_change:bool=True):
        """
        检查无钥匙状态在指定时间的信息显示和变化
        
        :param flag_old:无钥匙状态当前
        :param flag_new:无钥匙状态变化后
        :param time:多长时间内
        :param  is_change:是否发生变化
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_usage_mode_status_in_time(self, usagemode_old: UsageMode, usagemode_new: UsageMode, time:int = 10, is_change:bool=True):
        """
        检查usagemode在指定时间的信息显示和变化
        
        :param usagemode_old:使用模式当前
        :param usagemode_new:使用模式变化后
        :param time:多长时间内
        :param  is_change:是否发生变化
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_drvgcycoff_time(self, TiDrvgCycOff:int, wait_time: int = 0):
        """
        检查离开驾驶时间
        
        :param TiDrvgCycOff:离开驾驶时间
        :param wait_time:等待多长时间检查
        :return:
        """
    

    # @Author:xiangyue.li@jiduatuo.com
    @abstractmethod
    def check_auto_sts(self, sts: CoolgReq, cycle_sts: ClimateCycleReq, wind_pos: SeatPos, wind_mode: AirWindMode, speed_pos: SeatVenPos, speed: SeatVenSpeed):
        """
        检查AC、循环模式、吹风模式、风速
        :param sts: 制冷状态：
        :param cycle_sts: 循环模式：
        :param wind_pos: 吹风zone
        :param wind_mode: 吹风模式
        :param speed_pos: 风量zone
        :param speed: 风速
        :return:
        """

    @abstractmethod
    def recv_fr_msg_by_id(self, fr_id, send_address: list = [], recv_address: list = [], time_out=3):
        '''
        根据 id 接收 fr 数据 接收单帧报文
        @param fr_id: fr 的id
        @param send_address: 发送的逻辑地址
        @param recv_address: 接收的 逻辑地址
        @param time_out:
        @return:
        '''

    @abstractmethod
    def send_fr_msg_by_id(self, fr_id, data: list, **kwargs):
        '''
        发送 单帧 fr 报文
        @param fr_id: id
        @param data:  报文内容
        @param kwargs:
        @return:
        '''

    @abstractmethod
    def recv_fr_msg(self, fr_id_list=[88, 89, 90, 91, 92, 93, 94], fr_response_id=69, send_address=0x0e80,
                    recv_address=0x1601, time_out=20):
        '''
        接收 fr 报文
        @param fr_id_list: 接收id 列表
        @param fr_response_id: 响应id
        @param send_address: 发送的逻辑地址
        @param recv_address: 接收的逻辑地址
        @param time_out:
        @return:
        '''

    @abstractmethod
    def send_fr_msg(self, send_data, send_id=69, recv_id=88, send_address=0x1601, recv_address=0x0e80):
        '''
        发送 fr 报文，根据数据长度 自己判断是多帧还是单帧
        @param send_data: 发送的数据
        @param send_id: 请求id
        @param recv_id: 响应id
        @param send_address: 发送逻辑地址
        @param recv_address:接收逻辑地址
        @return:
        '''


    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_ble_key_prsnt_sts(self,zone:BLEKeyPrsntZone,sts:BLEKeyPrsntSts):
        """
        模拟设置蓝牙zone:{zone.name} 的钥匙在位状态为{sts.name}
        @param zone: 蓝牙区域
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
        @param sts: 蓝牙钥匙在位状态
            NotValid = 0
            Valid = 1
        @return:
        """

    
    def telm_set_hv_active_req(self, req: RemHvStrtActvReq, time_wait: Union[int, float] = 0):
        """
        APP远程设置充激活请求为{req.name}
        @param req: 充激活请求
            NoReq = 0
            On = 1
            Off = 2
        @param time_wait:等待时间
        @return:
        """
    
    # @Author:xiangyue.li@jiduatuo.com   #o_fan.liu
    @abstractmethod
    def check_steerwheel_direct_req(self, direct: AdjustDirection, sts: bool):
        '''
        @param direct: 方向盘调节方向  Forward = 0    Left = 1    Up = 2    Backward = 3    Right = 4    Down = 5
        @param sts: 方向盘调节请求
        @return:
        '''
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_door_switch_light_keep_sts(self, pos: DoorPos, req: LampSts,last_time:Union[int,float]):
        """
        Check BGM 发出的{pos.name}门按键指示灯状态是否一直为{sts.name}
        :param pos: 门的位置 Dirver = 0 Pass = 1 RearLeft = 2 RearRight = 3 Tailgate = 4 All = 5
        :param req: 等的状态 Off = 0 On = 1 Error = 2 Reserve = 3
        :return:
        """
        
    # @Author:xiangyue.li@jiduatuo.com
    @abstractmethod
    def check_tailgate_upper_req(self, req: isOn):
        '''
        @param req: 尾门上部位置请求
        @return:
        '''
        
    # @Author:xiangyue.li@jiduatuo.com
    @abstractmethod
    def set_tailgate_switch_sts(self, sts: FoldHmiReq):
        '''
        @param sts: 模拟尾门开关闭合状态
        @return:
        '''
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_hv_actv_for_vehmod_req(self, onoff: bool):
        """
        检查激活高压系统请求的状态
        
        :param onoff: 激活高压系统请求状态
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_hv_actv_for_vehmod_req_in_time(self, onoff_old: bool, onoff_new: bool, time:int = 10, is_change:bool=True):
        """
        检查激活高压系统请求状态在指定时间的信息显示和变化
        
        :param onoff_old: 历史激活高压系统请求状态
        :param onoff_new: 当前激活高压系统请求状态
        :param time: 多长时间内
        :param is_change: 是否变化
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_door_lock_req(self, door_pos: DoorPos, req: DoorLockCmd,timeout: Union[float, int] = 1):
        """
        Check BGM 发出的解闭锁请求
        @param :door_pos: 
            Dirver = 0
            Pass = 1
            RearLeft = 2
            RearRight = 3
            Tailgate = 4
            All = 5
            Hood = 6
        :param req: 控制请求
            Off = 0
            Unlck = 1
            Lock = 2
            Safe = 3
            UnlckByCrash0 = 12
            UnlckByCrash1 = 4
            UnlckByCrash2 = 8
            UnlckByCrash3 = 14
            UnlckByCrash4 = 13
        :param timeout: 超时时间
        @return:
        """
        
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_charge_target_soc_req(self, value:int):
        """
        Check BGM 发出的设置目标充电SOC值是否为{value}
        @param :value: 设置的目标SOC值
        @return:
        """
    def resume_ecu_send(self, bus_name: str, ecu_name: str):
        """
        继续 bus 发送数据
        :param bus_name: 通道名称
        :return:
        """
    # @Author:quan.sun@jiduatuo.com
    @abstractmethod
    def preheat_msg(self, bus_name: str, msg_name: str):
        '''
        预热msg发送, 让其 周期1ms 等待发送, 一般用在发送及时报文
        注意 预热至少要提前2s,只用在PCAN can bus

        @param bus_name: type: str    such as  "bodycan"
        @param msg_name: type: str
        '''

    # @Author:quan.sun@jiduatuo.com
    @abstractmethod
    def remove_preheating(self, bus_name: str, msg_name: str):
        '''
        移除 预热msg发送, 让其 恢复周期2s
        注意 只用在PCAN can bus

        @param bus_name: type: str    such as  "bodycan"
        @param msg_name: type: str
        '''

    @abstractmethod
    def get_dtc_snapshot_info(self, dtc:str):
        """
        执行诊断指令读取DTC
        @param dtc: 需要读取的快照信息
        :return: 返回诊断指令执行结果
        """

    @abstractmethod
    def check_tailwing_without_close_or_open_cmd(self,state,timeout=2):
        """
        检查一段时间内尾翼cmd信号不会发出
        @param state: 输入需要检查的值
        @param timeout:需要获取多长时间
        :return: 
        """

    # @Author:qian.feng@jiduatuo.com
    def check_relay_proxyreq(self, poweroutproxy: Union[PowerOutLetReq, None] = None):
        '''
        @param poweroutproxy: check 12v电源继电器proxy请求
            NoReq = 0
            On = 1
            Off  = 2   
        @return:
        '''
        
    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def check_relay_cmd(self, relaytype: Union[RelayType, None] = None,
                            relaysts: Union[RelaySts, None] = None,
                            OnOff: Union[OnOffSafe1, None] = None,
                            poweroutproxy: Union[PowerOutLetReq, None] = None,
                            time_wait: Union[float, int] = None):
        """
        校验继电器使能状态 0x0 Off 0x1 On
        :param relaytype: 继电器类型
            KL151 = 0
            KL152 = 1
            KL153  = 2   
            climate  = 3   
            batterysaver  = 4  
            poweroutlet  = 5   
            crashrelay  = 6   
        :param OnOff: Crash继电器状态
        :param relaysts: 继电器闭合状态
        :param poweroutproxy: 12v电源继电器状态
        :param time_wait: check时间，默认0
        :return:
        """

    # @Author:qian.feng@jiduatuo.com
    def check_Lock_and_unlock_remind(self, lockstsprmt: Union[LockStsPrmt, None] = None, timeout=2):  
        '''
        @param LockStsPrmt: check 2s内总线解闭锁动动作提醒状态
            Idle  = 0
            NFC_PSD = 1
            ANTI_LOCK_KEY_FORGET = 2
            NO_KEY_PRESENT = 3
            CLOSE_DOOR_AUDIO = 4
            ANTI_RELOCK = 5
            AUTO_RELOCK = 6
            WalkAwayAudio = 7
        @return:
        '''
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_usgmode_deactvn_qly(self, usgmoddeactvnqly: UsgModDeactvnQly):
        """
        检查停车时usagemode是否有效的状态值
        
        :param usgmoddeactvnqly: usagemode有效状态值
            InvalidValue = 0
            QlyNotOkLowConfidence = 1
            QlyOkHighConfidence = 2
            InvalidValue2 = 3
        :return:
        """
        
    # @Author:xiangyue.li@jiduatuo.com
    def check_alrm_notactived_req(self, timeout=3):  
        '''
        Check 防盗没有被激活  AlrmStsAlrmSt不为2
        @return:
        '''

    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def get_four_tire_pressure_and_temperature(self):
        """
        获取4轮胎压和胎温
        
        :param :
        :return tire_fl_P: 左前胎压
        :return tire_fl_T: 左前胎温
        :return tire_fr_P: 右前胎压
        :return tire_fr_T: 右前胎温
        :return tire_rl_P: 左后胎压
        :return tire_rl_T: 左后胎温
        :return tire_rr_P: 右后胎压
        :return tire_rr_T: 右后胎温
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_four_tire_pressure_and_temperature(self, tire_fl_P = 0, tire_fl_T = 0, tire_fr_P = 0, tire_fr_T = 0, tire_rl_P = 0, tire_rl_T = 0, tire_rr_P = 0, tire_rr_T = 0):
        """
        检查4轮胎压和胎温和预期的是否一致
        
        :param tire_fl_P: 左前胎压
        :param tire_fl_T: 左前胎温
        :param tire_fr_P: 右前胎压
        :param tire_fr_T: 右前胎温
        :param tire_rl_P: 左后胎压
        :param tire_rl_T: 左后胎温
        :param tire_rr_P: 右后胎压
        :param tire_rr_T: 右后胎温
        :return:
        """
    @abstractmethod
    def check_right_light_off(self):
        '''
        检查右转向灯灭
        '''

    @abstractmethod
    def check_left_light_off(self):
        '''
        检查左转向灯灭
        '''

    
    @abstractmethod
    def check_turn_right_error(self):
        """
        检查右转故障，右转向灯状态
        """
    

    @abstractmethod
    def set_turn_right_wheel(self,wheel="right_old"):
        """
        设置方向盘状态 
        @param wheel: 方向盘方向  默认为右转方向盘
        """

    @abstractmethod
    def check_wheel_light_on_and_light_off(self,direction,num=3):
        """
        检查转向灯亮灭情况
        """
        
    # @Author:xiangyue.li@jiduatuo.com
    def set_twilight_sensor_sts(self):  
        '''
        设置白天黑夜状态
        @return:
        '''

    @abstractmethod
    def four_domain_restart_send_signal(signal_name,sig_value_name,time_sleep):
        '''
        发送四域重启信号

        @param signal_name: 信号名 type: str
        @param sig_value_name: 信号值 type: int
        @param time_sleep: 发信号后的等待时间 默认值为0.01
        '''

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def wakeup_tcam_by_can(self):
        """
        通过CAN总线唤醒TCAM模块
        
        Args:
            无
        
        Returns:
            无
        
        """
        pass
    
    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def stop_wakeup_tcam_by_can(self):
        """
        通过CAN停止唤醒TCAM
        
        Args:
            无
        
        Returns:
            无
        
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_brake_pedal_function_safe(self,safe:Union[None,YesOrNo] = YesOrNo.Yes,qf:Union[None,ValueQf] = ValueQf.AccurData,sts:Union[None,YesOrNo] = YesOrNo.Yes, crc_sts:bool = True, ub_flag:bool = True):
        """
        控制刹车踏板状态及其CRC和UB
        
        :param safe: 刹车踏板状态安全信号
        :param qf: 刹车踏板状态质量信号
        :param sts: 刹车踏板状态
        :param crc_sts: crc状态
        :param ub_flag: UB状态
        :return:
        """

    # @Author:xiangyue.li@jiduatuo.com
    @abstractmethod
    def set_rearview_angle(self, left_horizon: Union[int, None] = None,
                            left_vertical: Union[int, None] = None,
                            right_horizon: Union[int, None] = None,
                            right_vertical: Union[int, None] = None):
        """
        设置后视镜目标角度
        
        :param left_horizon: 主驾水平角度
        :param left_vertical: 主驾垂直角度
        :param right_horizon: 副驾水平角度
        :param right_vertical: 副驾垂直角度
        :return:
        
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_aeb_brake_req(self,req:AsySftyHWLReq):
        """
        设置AEB紧急制动
        :param req:AEB紧急制动状态
            NoRequest = 0
            TurnOn = 1
            TurnOff = 2
            Reserved = 3
        :return:
        """

    def set_aeb_bkp_brake_req(self,req:AsySftyHWLReq):
        """
        设置AEB紧急制动
        :param req:AEB紧急制动状态
            NoRequest = 0
            TurnOn = 1
            TurnOff = 2
            Reserved = 3
        :return:
        """
    
    def set_bluetooth_key_connect_sts(self, key_num:int,type: BlueType, con_sts: ConnSts,key_zone:int=1,key_id: Union[list,None] = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
         0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]):
        """
        设置蓝牙钥匙连接状态
        :param key_num (int): 蓝牙钥匙编号
        :param type (BlueType): 蓝牙钥匙类型
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
        :param con_sts (ConnSts): 蓝牙钥匙连接状态
            Disconnect = 0
            Connect = 1
        :param key_zone (int, optional): 钥匙所在区域. Defaults to 1.
        :param key_id (Union[list, None], optional): 钥匙ID列表.
        :return:
        """
        
    # @Author:O_xue.li01@jiduatuo.com
    @abstractmethod
    def set_wiper_speed_signal(self, speed: AutWinWipgCmd):
        """
        模拟反送雨刮速度信号
        :param speed:  发送的雨刮速度信号
            WipgSpd0Rpm = 0
            WipgSpd40Rpm = 1 
            WipgSpd43Rpm = 2 
            WipgSpd46Rpm = 3 
            WipgSpd50Rpm = 4  
            WipgSpd54Rpm= 5  
            WipgSpd57Rpm = 6 
            WipgSpd60Rpm = 7
        :return:
        """ 
     
     # @Author:O_xue.li01@jiduatuo.com   
    @abstractmethod
    def check_wiper_rain_sensor(self, rain_sensor: RainSnsrStsToHMI, timeout=5):
        """
        Check在条件满足的情况下BGM雨量传感器激活请求

        :param rain_sensor_act_req: 雨量传感器激活请求
        :return:
        """
        pass 
    
    # @Author:O_xue.li01@jiduatuo.com  
    @abstractmethod
    def set_wiper_activation_signal(self, activa: WiprActvFromWMM):
        """
        模拟反送雨刮激活信号
        :param activation: 发送的雨刮激活信号 
            on = 1
            Off = 0
        :return:
        """  
        
     # @Author:O_xue.li01@jiduatuo.com   
    @abstractmethod
    def check_wiper_status_req(self, status_req: WiprActv):
        """
        Check在条件满足的情况下激活雨刮状态信息信号

        :param active_req: 雨刮状态激活请求
        :return:
        """  
        
    # @Author:O_xue.li01@jiduatuo.com  
    @abstractmethod
    def set_wiper_Motor_Error_signal(self, Motor_Error: WiprMotErrSafe, timeout=2):
        """
        模拟反送雨刮电机错误信号
        :param Motor_Error: 发送的雨刮电机错误请求 
            NotVld1 = 0
            Off = 1 
            On = 2 
            NotVld2 = 3
        :return:
        """  
        
    # @Author:O_xue.li01@jiduatuo.com  
    @abstractmethod
    def set_wiper_position_signal(self, wiper_position: WiprInWipgArFromWMM):
        """
        模拟发送雨刮位置信号
        :param wiper_position: 发送雨刮位置请求 
            on = 1
            Off = 0
        :return:
        """ 
        
    # @Author:O_xue.li01@jiduatuo.com   
    @abstractmethod
    def check_wiper_position_req(self, position_req: WiprInWipgAr):
        """
        Check在条件满足的情况下激活雨刮位置信号

        :param position_req: 雨刮位置信号请求
        :return:
        """     
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def check_keep_power_car_config(self, indcr_sts: IndcrSts, req: MirrFoldCmdTyp, pos: Union[WinPos, None] = None, timeout=1):
        """
        Check BGM 发出的窗户的开关请求、闪光灯状态、后视镜折叠请求

        :param indcr_sts: 闪光灯状态
        :param req: 后视镜折叠请求
        :param req: 窗户的开关请求
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_dcdc_battary_act_sts_on_can(self, DcDcActvd: DcDcActvd):
        """
        设置高压电池为状态

        :param DcDcActvd: 高压电池状态
        :return:
        """     
    
     # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_dispbattegyout(self, DispBattEgyOut: float):
        """
        设置显示输出电量

        :param DispBattEgyOut: 显示输出电量
        :return:
        """   
        
        
     

    # @Author:xiangyue.li@jiduatuo.com        
    def check_rear_view_autofold_req(self, req: AutoFoldReq):
        """
        Check BGM发出的后视镜自动折叠请求
        :param req: 后视镜自动折叠请求
            Idle = 0
            FoldIn = 1
            FoldOut = 2
        :return:
        """  
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def get_car_mode_status(self):
        """
        获取总线上的carmode状态

        :param:
        :return receive_result: 返回carmode状态值
        """  
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def wait_time_and_check_carmode(self, car_mode_main_new: CarMode, carmode_sub_new: int, car_mode_main_old: CarMode, carmode_sub_old: int, time: int=30):
        """
        等待一段时间并校验carmode的状态

        :param car_mode_main_new: carmode 主状态期望变化的值
        :param carmode_sub_new: carmode 子状态期望变化的值
        :param car_mode_main_old: carmode 主状态历史保持的值
        :param carmode_sub_old: carmode 子状态历史保持的值
        :param time: 等待的时间
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_driving_preconditions(self, engSt1WdStsEngSt1WdSts:EngSt1WdStsEngSt1WdSts = EngSt1WdStsEngSt1WdSts.EngSt1_Awake,  imobengsts1: ImobSts=ImobSts.ImobMtn, imobengsts2: ImobSts=ImobSts.ImobMtn, imobengsts3: ImobSts=ImobSts.ImobMtn):
        """
        设置驾驶前提条件

        :param engSt1WdStsEngSt1WdSts: 发送机状态
        :param imobengsts1: immo1 状态
        :param imobengsts2: immo2 状态
        :param imobengsts3: immo3 状态
        :return:
        """ 

    # @Author:o_liangliang.chen@external.jiduauto.com  
    @abstractmethod
    def clear_block_bytes(self):
        """
        清空block_bytes存储的数据
        """

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def get_block_bytes(self, blockid:BlockName, timeout: Union[int,float] = 5):
        """
        根据BlockID获取接收到的Block块数据

        :param blockid: BlockName
        :param timeout: 超时时间
        :return: 如果时间内存在对应Block数据则返回  list 如果没有则返回None
        """
    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def get_ble_bytes_thread_start(self):
        """
        启动获取蓝牙数据线程，建议放到测试类的before_class
        """

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def get_ble_bytes_thread_stop(self):
        """
        停止获取蓝牙数据线程，建议放到测试类的after_class
        """
    @abstractmethod   
    def get_designated_time_expected_message(self, channel, recv_id: [int, list, None] = None,
                                             filter_id: [int, list, None] = None, timeout=2):
        '''
        接收一段时间   指定通道的报文，返回接受的报文信息，每次接收前，要清空buffer
        @param channel: 通道，can lin fr
        @param recv_id: 接收指定的id，可以为单个id 或者一个列表包含多个id,默认为None 接收任意id（除去过滤对的id）报文
        @param filter_id: 过滤掉id，接收到该id的报文不算,可以为单个id 或者一个列表包含多个id，默认None 不过滤id
        @param timeout: 接收的一段时间，接收到报文（除去过滤的报文）就退出，接收不到就一直等到超时退出
        @return: [msg1，msg2 ....]/None
        '''

    @abstractmethod
    def get_current_expected_message(self, channel, recv_id: [int, list, None] = None,
                                     filter_id: [int, list, None] = None, timeout=2):
        '''
        接收 指定通道的报文，返回接受的报文信息，每次接收前，要清空buffer
        @param channel: 通道，can lin fr
        @param recv_id: 接收指定的id，可以为单个id 或者一个列表包含多个id,默认为None 接收任意id（除去过滤对的id）报文
        @param filter_id: 过滤掉id，接收到该id的报文不算,可以为单个id 或者一个列表包含多个id，默认None 不过滤id
        @param timeout: 接收的超时时间，接收到报文（除去过滤的报文）就退出，接收不到就一直等到超时退出
        @return: msg/None
        '''

    @abstractmethod
    def check_InfoCan_FOTAStatus(self, infocanfotastatus: InfoCanFOTAStatus):
        '''
        Check FOTA过程中InfoCan FOTAStatus状态
        @param InfoCanFOTAStatus: InfoCan FOTAStatus状态
            Idle = 0
            Query = 1
            Downloading = 2
            Active = 3
            Update = 4
            Rollback = 5
            UpdateFailNotDriving = 6
        @return: 
        '''   

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod       
    def set_keyconnected_and_keytype_sts(self, keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.NoKeyConnected, time_wait:  int=3):
        """
        仿真发送钥匙类型及连接状态

        :param keyslot: 第几把钥匙
        :param isconnect: 钥匙连接状态
        :param keyconnecttype: 钥匙类型
        :param time_wait: 等待时间
        :return:
        """ 
        
    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod       
    def check_glove_box_req_and_lock_sts(self, actiontype:ActionType, ison: GloveBoxStatus, time_wait:  int=1):
        """
        校验手套箱私锁及动作请求
        :param actiontype: 校验动作类型
        :param ison: 
            On::上锁 
            off::解锁
        :param time_wait: 等待时间
        :return:
        """ 
   
    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod    
    def check_glove_box_req(self, ison: Union[GloveBoxStatus, None] = None, timeout=2):  
        """
        校验2s内手套箱动作请求不置位
        :param ison: 
            On::使能手套箱开Req
            off::默认值
        :param timeout: 等待时间
        :return:
        """ 
        
    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod 
    def check_glove_box_private_lock_sts(self, ison: Union[GloveBoxStatus, None] = None, timeout=2):  
        """
        校验2s内手套箱私锁不状态不置位
        :param ison: 
            On::上锁 
            off::解锁
        :param timeout: 等待时间
        :return:
        """
        
    # @Author:xiangyue.li@jiduauto.com  
    @abstractmethod
    def check_keysearch_req(self, key_zone: KeyZone):
        '''
        Check 寻钥匙请求变化
        '''   
        
    # @Author:qian.feng@jiduatuo.com  
    def set_brake_pedal_sts(self, sts:Union[None,YesOrNo] = YesOrNo.Yes, time_wait:  int=2):
        '''
        设置刹车踏板踩下状态不含safe信号
        :param sts: 
            No = 0::未踩下状态
            Yes = 1::踩下状态
        :param time_wait: 等待时间
        :return:
        '''   

    # @Author:o_guojing.yang@jiduatuo.com
    @abstractmethod
    def check_seat_heat_climalvl(self, pos: SeatId, level: HeatVentiLvl):
        """
        check BGM 转发的座椅加热等级请求

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :return:
        """

    # @Author:o_guojing.yang@jiduatuo.com
    @abstractmethod
    def check_seat_venti_climalvl(self, pos: SeatId, level: HeatVentiLvl):
        """
        check BGM 转发的座椅通风等级请求

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 通风等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :return:
        """

    # @Author:o_guojing.yang@jiduatuo.com
    @abstractmethod
    def check_seat_venti_level_sts(self, pos: SeatId, level: HeatVentiLvl):
        """
        check BGM 转发的座椅通风等级请求

        :param pos: 座椅位置 FrontLeft = 0 FrontRight = 1 FrontMid = 2 FrontRow = 3 RearLeft = 4 RearMiddle = 5 RearRight = 6 RearRow = 7 ThirdLeft = 8 ThirdMiddle = 9 ThirdRight = 10 ThirdRow = 11 All = 12
        :param level: 加热等级 Off = 0 Level1 = 1 Level2 = 2 Level3 = 3
        :return:
        """

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod 
    def check_lock_status_for_user(self, sts: StsForUsrFb, time_wait:  int=2):
        """
        校验中央锁用户同步状态
        :param sts: 
            Undefd = 0::默认值
            Opend = 1::至少一个门处于Open状态
            Clsd = 2::四门及尾门处于关闭但未上锁状态
            Lockd = 3::上锁状态
            safe = 4::安全锁状态
        :param time_wait: 等待时间
        :return:
        """

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod 
    def set_door_lock_status(self, doorid:DoorId, lock_sts:Locksts, time_wait = 2):
        """
        设置四门锁上锁解锁状态
        :param doorid: 对应侧门
        :param lock_sts: 门锁状态
            Ukwn = 0
            Unlckd = 1
            Lockd = 2
            SafeLockd = 3
        :param time_wait: 等待时间
        :return:
        """

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod 
    def check_lock_unlock_event(self, event:bool,  time_wait = 1):
        """
        校验总线解闭锁event信号跳变
        :param event: bool 类型
            Flase = 0
            True = 1
        :param time_wait: 等待时间
        :return:
        """

    # @Author:lei.song@jiduatuo.com  
    @abstractmethod
    def send_signal_and_get_time(self, signal_info_set: list):
        """
        发送信号并记录发送时间。
        
        Args:
            signal_info_set (list): 包含多个信号信息的列表，每个信号信息是一个列表，
        
        Returns:
            list: 包含多个发送后的信号信息的列表，每个发送后的信号信息是一个列表，
                包含原始信号信息以及新增的发送时间（float，单位：秒），        
        """

    # @Author:guojing.yang@jiduatuo.com
    @abstractmethod
    def set_onbd_chrg_handle_sts(self, sts: DCChrgnHndlSts, time_wait: Union[int, float] = 0):
        """
        设置onbd充电枪状态

        :param sts: 充电枪状态 Disconnected = 0 ConnectedWithoutPower = 1 PowerAvailableButNotActivated = 2 ConnectedWithPower = 3 Init = 4 Fault = 5
        :param time_wait: 执行操作之后的等待时间
        :return:
        """

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod
    def set_engine_and_check_energy_level(self, EngSt1WdStsEngSt1WdSts:Union[EngSt1WdStsEngSt1WdSts, None] = None, mai:Union[int, None] = None):
        """
        设置发动机EngSt1WdStsEngSt1WdSts状态, check车身能量水平VehModMngtGlbSafe1EgyLvlElecMai状态
        :param EngSt1WdStsEngSt1WdSts: 发动机状态EngSt1WdStsEngSt1WdSts
        :mai : 车身能量水平::VehModMngtGlbSafe1EgyLvlElecMai
        :return:      
        """

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod
    def check_door_without_open_req(self, drv_opener: Union[DoorPos, None] = None, 
                                    pass_opener: Union[DoorPos, None] = None, 
                                    lere_opener: Union[DoorPos, None] = None, 
                                    rire_opener: Union[DoorPos, None] = None, 
                                    timeout:Union[int,float] = 2):

        """
        校验条件不满足的情况下BGM不发车门动作请求
        :param drv_opener: 主驾车门
        :param pass_opener: 副驾车门
        :param lere_opener: 左后车门
        :param rire_opener: 右后车门
        :param time_wait: 监测时间
        :return:      
        """

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod
    def check_door_open_pos_and_trigsrc(self, doorpos: Union[DoorPos, None] = None,
                              position: Union[int, None] = None,
                              door_trigsrc: Union[None, DoorTrigerSource] = None,
                              timeout: Union[float, int] = 0
                              ):
        """
        校验四门门开度及触发源
        :param doorpos: 对应侧门
        :param position: 门开角度
        :param door_trigsrc: 车门动作触发源
        :param timeout: 延迟时间默认0
        :return:      
        """

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod
    def set_child_lock_sts(self, side: Side, childlockstatus: OnOffSafe1, timeout: Union[float, int] = 0):
        """
        设置儿童锁上锁解锁状态
        :param side: 对应左侧 or 右侧
        :param childlockstatus: 儿童锁状态：
                OnOffSafeInvld1 = 0
                OnOffSafeOn = 1
                OnOffSafeOff = 2   
                OnOffSafeInvld2 = 3
        :param timeout: 延迟时间默认0
        :return:      
        """

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod    
    def set_door_perc_position(self, doorpos: Union[DoorPos, None] = None,
                              perc_position: Union[str, int] = None,
                              timeout: Union[float, int] = 0
                              ):
        """
        设置车门当前开度百分比
        :param doorpos: 对应侧门
        :param perc_position: 当前车门开度百分比
        :param timeout: 延迟时间默认0
        :return:      
        """
        
    @abstractmethod    
    def set_fota_JiDUCharging(self, isConnect: bool=False, isPrivate: bool=True):
        """
        设置充电桩状态, FOTA使用
        :param isConnect: 是否连接充电桩
        :param isPrivate: 是否是集度私桩
        :return:      
        """
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def check_ChrgLidManvgDCorAcDc_CalReq2 (self, Req2: Inact):
        """
        检查充电口盖标定请求状态

        :param Req2: 充电口盖标定请求状态
            Inactive = 0
            Active = 1
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_ChrgLidManvgDCorAcDc_CalRqrdFb(self, CalRqrdFb: bool):
        """
        设置充电口盖标定反馈状态

        :param CalRqrdFb: 充电口盖标定反馈状态
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_ChrgLidManvgDCorAcDc_CalActvSts2(self, ActvSts2: Inact):
        """
        设置充电口盖标定激活状态

        :param ActvSts2: 充电口盖标定激活状态
            Inactive = 0
            Active = 1
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_BrkSysSts_BrkSys_Capability(self, BrkSysCap: BrkSysCap):
        """
        设置博世平台的L3状态信号

        :param BrkSysCap: 博世平台的L3状态信号
            NotInitialized = 0
            Full = 1  
            TestPending = 2  
            Fault = 3
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def check_VMM_BrkgSys_SelfTestFlg(self, SelfTestFlg: bool):
        """
        检查自检标志状态

        :param SelfTestFlg: 自检标志状态
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def check_PrkgFctTestPndReq_From_VMM(self, ReqSts2: ReqSts2):
        """
        检查自检功能触发请求状态

        :param ReqSts2: 自检功能触发请求状态
            Default = 0
            NotReqd = 1
            Reqd = 2
            Reserved = 3
        :return:
        """ 


    #o_fan.liu edit
    @abstractmethod
    def check_steerwheel_DesPower_req(self, lev_sts: HeatLevel, DesPwr_sts: DesPwr):  #
        """
        BGM发出的预计功率信号

        :param lev_sts: 加热状态 Off = 0 Low = 1 Mid = 2 High = 3
        :param ower_sts: 预计功率大小 Off_power = 0   Low_power = 30  Mid_power = 50   High_power = 90
        :return:
        """
        pass

    #o_fan.liu edit
    def set_steerwheel_remHeat_sts(self, level: RemSteerWhlHeatgLvlReqLevel, time_wait: Union[float, int] = 0):
        """
        设置方向盘远程加热状态为

        :param level: 加热状态 Off = 0 Low = 1 Mid = 2 High = 3
        :return:
        """
        pass

    #o_fan.liu edit  
    def set_steerwheel_PwrAllwd(self, PwrAllwd_val: Union[int, float] = 90):    #LF
        """
        设置方向盘允许功率：

        :param PwrAllwd_val: 允许功率值
        :return:
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_OnBdChrgrHndlSts1(self, OnBdChrgrHndlSts: OnBdChrgrHndlSts):
        """
        设置交流充电枪状态

        :param OnBdChrgrHndlSts: 交流充电枪状态
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
        :return:
        """ 
        pass

    # @Author:guojing.yang@jiduatuo.com  
    @abstractmethod       
    def set_blekeyconnected_and_keytype_sts(self, keyslot=KeySlot.FirstKey, isconnect=ConnectionStatus.Connect, keyconnecttype=KeyConnectType.NoKeyConnected, zone=BLEKeyPrsntZone.Zone0, time_wait:  int=3):
        """
        仿真发送钥匙类型及连接状态

        :param keyslot: 第几把钥匙
        :param isconnect: 钥匙连接状态
        :param keyconnecttype: 钥匙类型
        :param zone: 钥匙位置信息
        :param time_wait: 等待时间
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def check_ChrgHndlStrtEna(self, ChrgHndlStrtEna: ChrgHndlStrtEna):
        """
        判断usagemode的充电请求

        :param ChrgHndlStrtEna: 充电请求状态
            PwrUpNotEna = 0
            PwrUpEna = 1
        :return:
        """ 
        
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_OnBdChrgrHndlSts1_function_safe(self, OnBdChrgrHndlSts:OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected,ub_flag:bool = True):
        """
        设置交流充电枪相关信号

        :param OnBdChrgrHndlSts: 交流充电枪状态
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
        :param ub_flag: ub位状态
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_dc_chrg_handle_sts_function_safe(self, sts:DCChrgnHndlSts = DCChrgnHndlSts.Disconnected, ub_flag:bool = True):
        """
        设置直流充电枪相关信号

        :param OnBdChrgrHndlSts: 直流充电枪状态
            Disconnected = 0
            ConnectedWithoutPower = 1
            PowerAvailableButNotActivated = 2
            ConnectedWithPower = 3
            Init = 4
            Fault = 5
        :param ub_flag: ub位状态
        :return:
        """

    @abstractmethod
    def set_alm_led_fault(self, AlmNum: int, value: AlmSts):
        """
        制造ALM的LED故障

        @param alm_num: 氛围灯编号1-10
        @param value: 1表示制造故障，0表示没有故障
        @return:
        """

    @abstractmethod
    def set_alm_vlt_fault(self, alm_num: AlmNum, value: AlmSts):
        """
        制造ALM的Vlt故障

        @param alm_num: 氛围灯编号1-10
        @param value: 1表示制造故障，0表示没有故障
        @return:
        """

    @abstractmethod
    def set_alm_tmp_fault(self, alm_num: AlmNum, value: AlmSts):
        """
        制造ALM的Tmp故障

        @param alm_num: 氛围灯编号1-10
        @param value: 1表示制造故障，0表示没有故障
        @return:
        """

    @abstractmethod
    def check_alm_flt(self, alm_num: AlmNum, sts: AlmSts):
        """
        校验ALM故障状态
        @param alm_num:
        @param sts:
        @return:
        """

    @abstractmethod
    def check_courtesy_light_req(self, sts: ReadLampSts):
        """
        校验迎宾灯状态

        @param sts: ReadLampSts
            Unknow = 0
            AllOff = 1
            Courtesy = 2
            Manual = 3
            Polite = 4（暂无）
            ForceOn = 5
            ForceOff = 6
        @return:
        """

    @abstractmethod
    def pause_OHC(self, wait_time):
        """
        暂停OHC接收所有LIN信号
        @param wait_time: 等待时间
        @return:
        """

    @abstractmethod
    def resume_OHC(self, wait_time):
        """
        恢复OHC接收所有LIN信号
        @param wait_time:  等待时间
        @return:
        """
    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod    
    def set_door_latch_posn(self, doorid: DoorId, latposn:LatPosition,  time_wait = 0):
        """
        设置车门锁舌位置
        :param doorid: 对应侧门
        :param latposn: 锁舌位置
            Undefined = 0
            FullyClosed = 1
            SecondaryPosition = 2
            FullyOpen = 3
        :param time_wait: 延迟时间默认0
        :return:      
        """
    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod    
    def set_windows_short_drop_sts(self, doorid: DoorId, shortdropsts:ShortDropSts,  time_wait = 0):
        """
        设置车窗短降位置
        :param doorid: 对应侧门
        :param shortdropsts: 车窗短降状态
            Idle = 0
            WindowDown = 1
            WindowClosed = 2
            NotUsed = 3
        :param time_wait: 延迟时间默认0
        :return:      
        """
    # @Author:guojing.yang@jiduatuo.com  
    @abstractmethod       
    def set_max_ClimaActv_sts(self, sts:isOn = isOn.Off):
        """
        设置空调开关
        :param ison: 
            On::开
            off::关
        :return:
        """ 
    
    # @Author:guojing.yang@jiduatuo.com  
    @abstractmethod       
    def check_telm_clima_req(self, sts:RemHvStrtActvReq):
        """
        校验远程空调请求
        :param RemHvStrtActvReq: 
            On::开
            off::关
        :return:
        """ 
    
    # @Author:guojing.yang@jiduatuo.com  
    @abstractmethod       
    def check_telm_clima_temp_range(self, sts:Union[float, int] = 16.0):
        """
        校验远程空调设定温度：16~28℃
        :return:
        """ 
    
    # @Author:guojing.yang@jiduatuo.com  
    @abstractmethod       
    def check_telm_clima_cmptmt_spcl(self, sts:ClimateSpcl):
        """
        校验远程空调设定温度模式
        :param ClimateSpcl: 
            Normal::0
            Lo::1
            Hi::2
        :return:
        """ 
    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod   
    def set_vehicle_rollover_and_inclination_angles(self, rangetype: RangeType, 
                                                    incln: Union[float, int] = None, 
                                                    roll: Union[float, int] = None, 
                                                    time_wait = 0):
        """
        设置车身翻转角度 或者车身倾斜角度
        :param rangetype: 设置类型：车身翻转角度 or 倾斜角度
        :param incln: 车身倾斜角度 int 类型
        :param roll: 车身翻转角度 int 类型
        :param time_wait: 延迟时间默认0
        :return:      
        """
        
    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod 
    def check_child_lock_unlock_req(self, childlockside: RotateDirec, lockreq: LockgCenReq2, time_wait: Union[float, int] = 0):
        """
        校验儿童锁上锁解锁请求
        :param childlockside: 需要校验的侧门儿童锁状态
        :param lockreq: 儿童锁请求状态
            Idle = 0
            UnLock = 1
            Lock = 2
        :param time_wait: 延迟时间默认0
        :return:      
        """
        
    @abstractmethod
    def check_WshrFldTankStsToHMI(self,expect_value,sleep_time:int):
        """
        检查WshrFldTankStsToHMI 信号值
        :param expect_value: 期望结果
        :param sleep_time: 等待时间

        """

    # @Author:guojing.yang@jiduatuo.com  
    @abstractmethod 
    def check_ApproachUnlockHmi(self,ConfigValue,time_wait: Union[float, int] = 0):
        """
        校验近车解锁开关设置项
        :param ConfigValue: 需要校验近车解锁开关设置项
        :param time_wait: 延迟时间默认0
        :return:      
        """

    # @Author:guojing.yang@jiduatuo.com  
    @abstractmethod 
    def check_ApproachUnlockHmi(self,AutoLockOnLeave,time_wait: Union[float, int] = 0):
        """
        校验离车落锁开关设置项
        :param ConfigValue: 需要校验离车落锁开关设置项
        :param time_wait: 延迟时间默认0
        :return:      
        """
    
    "*********************************************************以下为mock mcu专用接口，请不要插入写入*********************************************************************************"

    @abstractmethod
    def cdd_set_usage_mode(self, usage_mode: UsageMode):
        """
        模拟MCU设置使用模式
        @param usage_mode: UsageMode
            ABANDONED = 0
            INACTIVE = 1
            CONVENIENCE = 2
            ACTIVE = 11
            DRIVING = 13
        """
    
    @abstractmethod
    def cdd_set_car_mode(self, car_mode: CarMode):
        """
        模拟MCU设置车辆模式
        @param car_mode: CarMode
            NORMAL = 0
            TRANSPORT = 1
            FACTORY = 2
            CRASH = 3
            DYNO = 5
        """
    
    @abstractmethod
    def cdd_set_wiper_washer_fluid_low(self, sts: OnOff):
        """
        模拟MCU设置雨刮洗涤液位
        @param sts: OnOff
            Off = 0, 液位不低
            On = 1，液位低
        """
    
    @abstractmethod
    def cdd_set_rain_sensor_error(self, sts: OnOff):
        """
        模拟MCU设置雨量传感器故障
        @param sts: OnOff
            Off = 0, 无故障
            On = 1，有故障
        """
    
    def cdd_set_wiper_sys_fault(self, fault_sts: GeneralFltSts):
        """
        模拟MCU设置雨刮系统故障
        @param fault_sts: GeneralFltSts
            NotVld1 = 0，无效值
            Off = 1，无故障
            On = 2，有故障
            NotVld2 = 3，无效值
        """
    
    def cdd_set_wiper_position(self, WiprInPrkgPosnLo: Union[OnOff, None] = None, WiprInWipgAr: Union[OnOff, None] = None):
        """
        模拟MCU设置雨刮位置，S2S处理为WiperService::NotifyWiperPosition，通知雨刮位置
            0, 0  --  @value(1)   kWIPING_AREA 刮刷区
            0, 1  --  @value(1)   kWIPING_AREA 刮刷区
            1, 0  --  @value(0)   kPARKED 驻车区
            1, 1  --  last_value
            
        @param WiprInPrkgPosnLo: OnOff, 前挡风玻璃上雨刮操纵杆是否在驻车位置(即最低处)
            Off = 0, 在驻车位置以上(即非最低处)
            On = 1，在驻车位置(即最低处)
            
        @param WiprInWipgAr: OnOff，前挡风玻璃上雨刮器角度
            Off = 0, 角度0(即贴着风挡玻璃)
            On = 1，角度非0（即不贴着风挡玻璃，可能处于维修位置）
        """
    
    "*********************************************************以上为mock mcu专用接口，请不要插入写入*********************************************************************************"

    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_ChrgLidManvgDCorAcDcOverTrvlFb(self, Fb: bool):
        """
        设置充电口盖是否超行程
        :param Fb: bool
        :return:
        """

    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_ChrgLidManvgDCorAcDcBlkFb(self, Fb: bool):
        """
        设置充电口盖是否堵塞
        :param Fb: bool
        :return:
        """

    # @Author:shulin.zheng@jiduatuo.com
    @abstractmethod
    def check_door_tx(self, drv_tx: Union[Flgsts, None] = None, pass_tx: Union[Flgsts, None] = None,
                          lere_tx: Union[Flgsts, None] = None, rire_tx: Union[Flgsts, None] = None):
        """
        检查四门通讯状态
        :return:
        """
        
    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod 
    def set_fr_gear_pos(self, gear: Gear, time_wait: Union[float, int] = 0):
        """
        仿真发送FR挡位状态
        :param gear: 车辆挡位
        :param time_wait: 延迟时间默认0
        :return:      
        """
           
    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod 
    def set_door_open_warn_sts(self, side: Side, warn:LcmaIndcn,  time_wait = 0):
        """
        仿真发送侧门侧方开门预警信息
        :param side: 需要仿真的对应侧门
            Left = 0
            Right = 1
            All = 2
        :param warn: 需要仿真的告警状态
            NoLcmaWarn = 0
            LcmaWarnLvl1 = 1
            NotUsed = 2
            LcmaWarnLvl2 = 3
        :param time_wait: 延迟时间默认0
        :return:      
        """
        
    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod 
    def check_door_open_resistcmd_sts(self, resistcmd:DoorOpenResistCmd,  time_wait = 0):
        """
        校验总线车门阻力使能状态
        :param resistcmd: 车门有无阻力使能
            Idle = 0::默认值
            AddResist = 1::有阻力
            SubtResist = 2::撤销阻力
            Resd = 3::预留
        :param time_wait: 延迟时间默认0
        :return:      
        """

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod 
    def check_without_door_resist_cmd(self, timeout=1.5):
        """
        校验1.5s内在条件不满足的情况下BGM不发开门阻力使能
        :param timeout: 校验时间
        :return:      
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_ChrgLidManvgDCorAcDc_TqReq2(self, tqreq2: ActTq):
        """
        Check BGM 发出的控制充电口盖扭矩请求否堵塞
        :param tqreq2: 
            NominalTorque = 0
            reserved0 = 1
            LowTorque = 2
            Tqreserved13 = 3
        :return:
        """

    # @Author:guojing.yang@jiduatuo.com 
    @abstractmethod
    def set_RemClimaHvSts(self,sts:RemoteClimateStatus = RemoteClimateStatus.Invalid):
        """
        设置远程上高压
        @param sts: RemoteClimateStatus
            Off = 0
            On = 1
            Invalid = 255
        :return:
        """

    # @Author:guojing.yang@jiduatuo.com 
    @abstractmethod
    def check_TelmSteerWhlHeatgReqLvl(self, level:HeatLevel):
        """
        校验方向盘加热等级：
        @param level: HeatLevel
            Off = 0
            Low = 1
            Mid = 2
            High = 3
        :return:
        """
    
    # @Author:guojing.yang@jiduatuo.com 
    @abstractmethod
    def check_TelmDefrostReq(self, sts:OnOff):
        """
        校验远控除霜是否开启：
        @param sts: OnOff
            Off = 0
            On = 1
        :return:
        """

    # @Author:guojing.yang@jiduatuo.com 
    @abstractmethod
    def set_RemClimaDefrstSts(self, sts:OnOff):
        """
        设置远程除霜：
        @param sts: OnOff
            Off = 0
            On = 1
        :return:
        """
            
    # @Author:guojing.yang@jiduatuo.com 
    @abstractmethod
    def check_HmiDefrstMaxReq(self, sts:OnOff):
        """
        校验远控除霜是否开启：
        @param sts: OnOff
            Off = 0
            On = 1
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_PtInin(self, OnOff: isOn):
        """
        检查引脚设置状态
        :param OnOff: 
            Off = False
            On = True
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_EngActvnMod1WdReq(self, EngActvnMod1:EngActvnMod1):
        """
        检查wakeup信号
        :param EngActvnMod1: 
            WakeupFunctionNOTActiveANDExternalRequestNOTPresent = 0
            WakeupFunctionNOTActiveANDExternalRequestPresent = 1
            WakeupFunctionActiveANDExternalRequestNOTPresent = 2
            WakeupFunctionActiveANDExternalRequestPresent = 3
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_IgnRlyCmd(self, OnOff: isOn):
        """
        检查IGN继电器状态
        :param OnOff: 
            Off = False
            On = True
        :return:
        """

    # @Author:shulin.zheng@jiduauto.com
    @abstractmethod
    def check_AI_Inter_actionLamp_Sts(self, AIInteractionLampLeftY, AIInteractionLampRightY):
        """
        监测AI指示灯AIInteractionLampLeftY左指示 AIInteractionLampRightY右指示
        :AIInteractionLampLeftY: 左指示 数组
        :AIInteractionLampRightY: 右指示 数组
        """

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod     
    def set_bncm_key_key_zone(self, zone: Zone, valid: Validity, time_wait: Union[float, int] = 0):
        """
        仿真发送对应Zone区钥匙连接状态
        :param zone: 对应需要模拟的钥匙区域
        :param valid: 有效 or 无效
        :param time_wait: 等待时间, 默认0
        :return:
        """

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod   
    def set_tailgate_antiPnch_sts(self, sts: bool, time_wait: Union[float, int] = 0):
        """
        仿真发送尾门防夹状态
        :param sts: bool类型
        :param time_wait: 等待时间, 默认0
        :return:
        """
        
    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod   
    def check_driver_prsnt_sts(self, present: NoYesCrit1, time_wait: Union[float, int] = 0):
        """
        校验总线驾驶员在位状态
        :param present: 
            NotVld1 = 0
            No = 1
            Yes = 2
            NotVld2 = 3
        :param time_wait: 等待时间, 默认0
        :return:
        """

    @abstractmethod
    def check_front_left_alm(self, bright, r, g, b):
        """
        检验左前氛围灯状态
        @param bright: 亮度
        @param r: 颜色r
        @param g: 颜色g
        @param b: 颜色b
        @return:
        """
        pass

    @abstractmethod
    def check_front_right_alm(self, bright, r, g, b):
        """
        检验右前氛围灯状态
        @param bright: 亮度
        @param r: 颜色r
        @param g: 颜色r
        @param b: 颜色b
        @return:
        """

    @abstractmethod
    def check_rear_left_alm(self, bright, r, g, b):
        """
        检验左后氛围灯状态
        @param bright: 亮度
        @param r: 颜色r
        @param g: 颜色r
        @param b: 颜色b
        @return:
        """

    @abstractmethod
    def check_rear_right_alm(self, bright, r, g, b):
        """
        检验右后氛围灯状态
        @param bright: 亮度
        @param r: 颜色r
        @param g: 颜色r
        @param b: 颜色b
        @return:
        """

    @abstractmethod
    def check_cc_right_alm(self, bright, r, g, b):
        """
        检验中控右侧氛围灯状态
        @param bright: 亮度
        @param r: 颜色r
        @param g: 颜色r
        @param b: 颜色b
        @return:
        """

    @abstractmethod
    def check_cc_left_alm(self, bright, r, g, b):
        """
        检验中控左侧氛围灯状态
        @param bright: 亮度
        @param r: 颜色r
        @param g: 颜色r
        @param b: 颜色b
        @return:
        """

    @abstractmethod
    def check_cc_mid_right_alm(self, bright, r, g, b):
        """
        检验中控中间右侧氛围灯状态
        @param bright: 亮度
        @param r: 颜色r
        @param g: 颜色r
        @param b: 颜色b
        @return:
        """

    @abstractmethod
    def check_cc_mid_left_alm(self, bright, r, g, b):
        """
        检验中控中间左侧氛围灯状态
        @param bright: 亮度
        @param r: 颜色r
        @param g: 颜色r
        @param b: 颜色b
        @return:
        """

    @abstractmethod
    def check_twe_left_alm(self, bright, r, g, b):
        """
        检验左侧扬声器氛围灯状态
        @param bright: 亮度
        @param r: 颜色r
        @param g: 颜色r
        @param b: 颜色b
        @return:
        """

    @abstractmethod
    def check_twe_right_alm(self, bright, r, g, b):
        """
        检验右侧扬声器氛围灯状态
        @param bright: 亮度
        @param r: 颜色r
        @param g: 颜色r
        @param b: 颜色b
        @return:
        """

    @abstractmethod
    def check_cc_under_alm(self, bright, r, g, b):
        """
        检验中控下方氛围灯状态
        @param bright: 亮度
        @param r: 颜色r
        @param g: 颜色r
        @param b: 颜色b
        @return:
        """

    @abstractmethod
    def check_mul_alms(self, bright, r, g, b, zone_lst: List[ALMZoneId]):
        """
        检验普通氛围灯亮灭及颜色
        @param bright: 氛围灯亮度
        @param r: 颜色
        @param g: 颜色
        @param b: 颜色
        @param zone_lst: 氛围灯灯带列表
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

    @abstractmethod
    def check_goosenecklamp(self, sts: OnOff):
        """
        检验鹅颈灯状态
        """
        

    #o_fan.liu edit  
    def check_steerwheel_DisAdjMov_req(self, disAdjMov_req: DisAdjMov):
        """
        BGM发出的DisAdjMov信号

        :disAdjMov_req: DisAdjMov信号取值
        :return:
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def check_VehParkNotActvd(self, Flg1: Flg1):
        """
        检查车辆驻车未激活状态

        :param Flg1: 未激活状态
            Rst = 0
            Set = 1
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_epbsts_function_safe(self, sts:EpbSts = EpbSts.AllAppld, ub_flag:bool = True):
        """
        设置epb相关信号

        :param sts: epb状态
        :param ub_flag: ub位状态
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_trsmparklockd_function_safe(self, TrsmParkLockd:TrsmParkLockd = TrsmParkLockd.ParkEngd, ub_flag:bool = True):
        """
        设置驻车锁相关信号

        :param TrsmParkLockd: 驻车锁状态
        :param ub_flag: ub位状态
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def set_engine_sts_function_safe(self, EngSt1WdStsEngSt1WdSts:EngSt1WdStsEngSt1WdSts = EngSt1WdStsEngSt1WdSts.EngSt1_Ini, ub_flag:bool = True):
        """
        设置发动机状态相关信号

        :param EngSt1WdStsEngSt1WdSts: 发动机状态
        :param ub_flag: ub位状态
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def check_RemPrkgSts(self, RemPrkgSts: RemPrkgSts):
        """
        检查远程启动状态

        :param RemPrkgSts: 远程启动状态
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
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def check_PtActvnReq(self, PtActvnReq: PtActvnReq1):
        """
        检查启动请求状态

        :param PtActvnReq: 启动请求状态
            NoPtActvnReq = 0
            PtActvnReq = 1
            PtActvnReqRem = 2
            PtActvnNotDriving = 3
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def check_AudWarn(self, AudWarn: bool):
        """
        检查非P档离车音频告警

        :param AudWarn: bool 非P档离车音频告警
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def check_ProxyKeepLow(self, usage_mode: UsageMode):
        """
        检查请求保持的usagemode下限

        :param usage_mode: 使用模式
            ABANDONED = 0
            INACTIVE = 1
            CONVENIENCE = 2
            ACTIVE = 11
            DRIVING = 13
        :return:
        """ 
    
    # @Author:heng.wang@jiduatuo.com   
    @abstractmethod
    def check_StartInhibitReq(self, StartInhibitReq: isOn):
        """
        检查启动禁止请求

        :param StartInhibitReq: 启动机制请求
            Off = False
            On = True
        :return:
        """ 
        

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod     
    def check_walk_away_and_approch_settings(self, keysettingtype:KeySettingType, 
                                             walkaway: Union[KeySettingItem, int] = None, 
                                             approch: Union[EnableDisable, int] = None, 
                                             time_wait: Union[float, int] = 0):
        """
        校验接近离开设置项设置状态

        :param keysettingtype: 需要校验的设置类型：近车解锁 or 离车落锁
        :param walkaway: 离车落锁设置项
        :param approch: 近车解锁设置项
        :param time_wait: 等待时间默认0
        :return:
        """ 
        
    # @Author:shulin
    def set_battery_charger_handle_status(self, soc_value: Union[int, float], ChrgHndlStrtEna: ChrgHndlStrtEna, wait_time: int = 0):
        """
        设置高压电池SOC，并验证充电请求信号。

        :param soc_value: 高压电池的SOC值
        :param charger_handle_enable: 充电器处理启动使能标志
        :param wait_time: 设置后等待信号上报的时间，单位为秒
        """

    def set_BookCharge_SetResponse(self, BookChargeSetResponse: BookChargeSetResponse):
        """
        请求预约充电回馈状态 1 代表成功，2代表失败
        :BookChargeSetResponse: 充电回馈状态
        """


    def check_BookChrgnActvdReq_set_BookChrgnStsFb(self, BookChrgnActvdReq, BookChrgnStsFb):
        """
        监测充电请求发出，反馈充电相应 1 代表成功，2代表失败
        :BookChrgnActvdReq: 请求充电
        :BookChrgnStsFb:请求充电反馈
        """


    def check_AI_Inter_actionLamp_Sts(self, AIInteractionLampLeftY, AIInteractionLampRightY):
        """
        监测AI指示灯AIInteractionLampLeftY左指示 AIInteractionLampRightY右指示
        :AIInteractionLampLeftY: 左指示 数组
        :AIInteractionLampRightY: 右指示 数组
        """

    def set_WPCModuleSts(self, sts: WPCModuleSts):
        """
        设置主驾WPC状态
        @param sts: 充电状态值
        @return:
        """
        pass

    def set_WPCCtrlRes(self, res: WPCCtrlRes):
        """
        设置主驾功能反馈
        @param res: 反馈值
        @return:
        """
        pass

    def set_PhoneForgottenRmn(self, sts: OnOff):
        """
        设置主驾遗留
        @param sts: 遗留状态
        @return:
        """
        pass

    def set_WPCFailureSts(self, sts: WPCFailureSts):
        """
        设置主驾故障
        @param sts: 故障值
        @return:
        """
        pass

    def set_WPCModuleStsPass(self, sts: WPCModuleSts):
        """
        设置副驾充电状态值
        @param sts: 充电状态
        @return:
        """
        pass

    def set_WPCCtrlResPass(self, res: WPCCtrlRes):
        """
        设置副驾功能反馈
        @param res: 反馈值
        @return:
        """
        pass

    def set_PhoneForgottenRmnPass(self, sts: OnOff):
        """
        设置副驾遗留状态
        @param sts: 遗留状态
        @return:
        """
        pass

    def set_WPCFailureStsPass(self, sts: WPCFailureSts):
        """
        设置副驾故障
        @param sts: 故障值
        @return:
        """
        pass

    def check_wireless_charge_drv(self, sts: OnOff):
        """
        检测主驾充电是否开启
        @param sts: 充电状态
        @return:
        """
        pass

    def check_wireless_charge_pass(self, sts: OnOff):
        """
        检测副驾充电是否开启
        @param sts: 充电状态
        @return:
        """
        pass
    
    def check_DiagcComActv_sts(self, sts: OnOff,check_time = 1):
        '''检查诊断激活线状态 '''

    def set_wiper_lever_status(self,value=0):
        """
        设置雨刷拨杆状态位置
        @param value: 0为释放，1为短按，2为长按，3为故障
        """
        pass

    def check_single_wiper_status(self,value=0):
        """
        检查雨刮单刮信号值
        @param value: 0为没有单刮，1为执行了单刮
        """
        pass

    def check_wiper_wash_active_status(self,value=1):
        """
        检查雨刮洗涤激活状态信号
        @param value: 1为未激活，2为激活
        """
        pass

    def set_fota_Discharging(self, isDischarging: bool=False):
        """
        设置FOTA 放电前置条件
        @param isDischarging: 是否在放电状态
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_AmbTEstimd_and_qf(self, AmbTEstimd: Union[int, float] = 0.0, qf: HvacTIfQf =HvacTIfQf.SnsrDataOk):
        """
        设置环境温度和qf
        
        :param AmbTEstimd: 环境温度degC
        :param qf: 数据有效性
            SnsrDataNotOk = 0
            SnsrDataOk = 1
        :return:
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def check_DrvrStrtReq(self, StrtReq: StrtReq):
        """
        检查驾驶请求
        
        :param StrtReq: 驾驶请求状态
            NotReqd = 0
            Reqd = 1
            RemReqd = 2
        :return:
        """
        pass
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_can_lin_diag_req_and_send_resp(self,bus_name:BusName,req_id:int,resp_id:int,check_req_data:list=[],send_resp_data:list=[],check_len:Union[int,None] = None ):
        """
        Check CAN/LIN/Fr发送诊断请求，并发送响应
        :param bus_name:BusName 总线名称
            bodycan = 'bodycan'
            propulsioncan = 'propulsioncan'
            chassiscan1 = 'chassiscan1'
            chassiscan2 = 'chassiscan2'
            passivesafetycan = 'passivesafetycan'
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
        :param req_id: 请求总线消息ID
        :param resp_id: 响应总线消息ID
        :param check_req_data: 检查请求数据
        :param send_resp_data: 发送响应数据
        :param check_len: 检查发送的诊断请求长度，默认为None
        :return:
        """
   
    # @Author:mingyue.xing@jiduatuo.com
    @abstractmethod
    def set_hvbatt(self, value:int):
        """
        设置HvBattLimnIndcn的值模拟热失控状态
        @param :value: 设置HvBattLimnIndcn的值
        @return:
        """

    # @Author:mingyue.xing@jiduatuo.com
    @abstractmethod
    def check_afs_act(self, actn_sts: isOn):
        """
        检测自适应前照明系统相关状态

        @param actn_sts: 自适应前照明系统激活状态请求 Off = False On = True
        @return:
        """
        pass

    # @Author:mingyue.xing@jiduatuo.com
    @abstractmethod
    def set_trun_beam_pull_up_down(self,gear:TurnPressGear):
        """
        设置转向灯拨杆拨动状态

        @param gear: 转向灯拨杆拨动状态
            NotAvailble = 0 #无状态
            DownPress1stGear = 1 #下拨一档
            DownPress2stGear = 2 #下拨二档
            UpPress1stGear = 3 #上拨一档
            UpPress2stGear = 4 #上拨二档
            Error  = 5 #错误
        @return:
        """
        pass

    # @Author:mingyue.xing@jiduatuo.com
    @abstractmethod
    def set_high_beam_pull_in_out(self,gear:HighPressGear):
        """
        设置远光灯拨杆拨动状态

        @param gear: 远光灯拨杆拨动状态
            NotAvailble = 0 #无状态
            PressInsd = 1 #内拨
            PressOutd = 2 #外拨
            Error = 3 #错误
        @return:
        """
        pass

    # @Author:mingyue.xing@jiduatuo.com
    @abstractmethod
    def check_flash_lamp_always_on(self):
        """
        检查远光灯闪光常亮
        """
        pass

    # @Author:qian.feng@jiduatuo.com  
    @abstractmethod   
    def check_tailgate_lock_status(self,sterm_lock:LockSts2, time_wait: Union[float, int] = 0):
        """
        通过总线校验尾门锁状态
        @param sterm_lock: 尾门锁状态
            LockStsUkwn = 0  # 上电初期
            Unlckd = 1  # 解锁
            Lockd = 2  # 上锁
            SafeLockd = 3  # 安全锁状态

        """
        pass
    
    @abstractmethod
    def set_windows_stauts_signal(self,status:WindowSwitchStatus):
        """
        设置窗户状态
        kUnknown = 0 #未知
        kIdle = 1 #无请求
        kUpManual = 2 #手动上升
        kUpAuto = 3 #自动上升
        kDownManual = 4 #手动下降
        kDownAuto = 5 #自动下降
        """

    @abstractmethod
    def set_windows_pass_stauts_signal(self,status:WindowSwitchStatus):
        """
        设置副驾窗户状态
        status：
            kUnknown = 0 #未知
            kIdle = 1 #无请求
            kUpManual = 2 #手动上升
            kUpAuto = 3 #自动上升
            kDownManual = 4 #手动下降
            kDownAuto = 5 #自动下降
        """

    @abstractmethod
    def set_windows_ReLe_stauts_signal(self,status:WindowSwitchStatus):
        """
        设置左后窗户状态
        status：
            kUnknown = 0 #未知
            kIdle = 1 #无请求
            kUpManual = 2 #手动上升
            kUpAuto = 3 #自动上升
            kDownManual = 4 #手动下降
            kDownAuto = 5 #自动下降
        """

    @abstractmethod
    def set_windows_ReRi_stauts_signal(self,status:WindowSwitchStatus):
        """
        设置右后窗户状态
        status：
            kUnknown = 0 #未知
            kIdle = 1 #无请求
            kUpManual = 2 #手动上升
            kUpAuto = 3 #自动上升
            kDownManual = 4 #手动下降
            kDownAuto = 5 #自动下降
        """

    @abstractmethod
    def set_windows_PDM_pass_stauts_signal(self,status:WindowSwitchStatus):
        """
        设置PDM 副驾窗户状态
        status：
            kUnknown = 0 #未知
            kIdle = 1 #无请求
            kUpManual = 2 #手动上升
            kUpAuto = 3 #自动上升
            kDownManual = 4 #手动下降
            kDownAuto = 5 #自动下降
        """
    @abstractmethod
    def set_windows_RLDM_Rele_stauts_signal(self,status:WindowSwitchStatus):
        """
        设置RLDM 左后窗户状态
        status：
            kUnknown = 0 #未知
            kIdle = 1 #无请求
            kUpManual = 2 #手动上升
            kUpAuto = 3 #自动上升
            kDownManual = 4 #手动下降
            kDownAuto = 5 #自动下降
        """
    @abstractmethod
    def set_windows_RRDM_ReRi_stauts_signal(self,status:WindowSwitchStatus):
        """
        设置RRDM 右后窗户状态
        status：
            kUnknown = 0 #未知
            kIdle = 1 #无请求
            kUpManual = 2 #手动上升
            kUpAuto = 3 #自动上升
            kDownManual = 4 #手动下降
            kDownAuto = 5 #自动下降
        """

    # @Author:mingyue.xing@jiduatuo.com
    @abstractmethod
    def set_rcw_req(self,req:AsySftyHWLReq):
        """
        设置后碰撞预警(RCW)
        :param req:RcwReq后碰撞预警状态
            Yes = 0 #触发后碰撞预警
            No = 1 #退出后碰撞预警
        :return:
        """
        pass
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_signal_always_is(self,bus:str,msg:str,signal:str,value:Union[int,float],timeout = 3):
        """
        检查在指定时间内总线上对应信号发送的值是否一直是预期值
        :param str: 总线名称
            'bodycan'
            'propulsioncan'
            'chassiscan1'
            'chassiscan2'
            'passivesafetycan'
            'diagnosticcan'
            'infocanfd'
            'infocanfd'
            'infocanfd'
            'connectivitycanfd'
            'bodyalmcanfd1'
            'bodyalmcanfd2'
            'cem_lin1'
            'cem_lin2'
            'cem_lin3'
            'cem_lin4'
            'cem_lin5'
            'cem_lin6'
            'backbonefr'
        :param msg: 消息名称
        :param signal: 信号名称
        :param value: 预期值
        :param timeout: 超时时间
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_without_tailgate_action_req(self, timeout=3):
        """
        Check BGM 没有发出尾门控制请求
        :param timeout:
        :return:
        """

    # @Author:mingyue.xing@jiduatuo.com
    @abstractmethod
    def set_hzrdLiIndcn_req(self,req:YesOrNo):
        """
        设置HzrdLiIndcnReq请求激活HWL
        :param req:YesOrNo
            No = 0
            Yes = 1
        :return:
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def check_ignition_state(self, sts: OnOffSafe1, time_wait: Union[float, int] = 0):
        """
        通过总线校验点火继电器控制状态
        :param sts:继电器控制状态
            OnOffSafeInvld1 = 0
            OnOffSafeOn = 1
            OnOffSafeOff = 2   
            OnOffSafeInvld2 = 3
        :return:
        """
        pass
      
    # @Author:guojing.yang@jiduatuo.com
    @abstractmethod
    def set_door_warning_ThermalProtection_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        """
        功能: 设置四门热保护故障状态
        :param Drvr: 驾驶位故障状态，数据类型: bool
        :param Pass: 副驾驶故障状态，数据类型: bool
        :param LeRe: 左后故障状态，数据类型: bool
        :param RiRe: 右后故障状态，数据类型: bool
        :return:
        """
        pass

    # @Author:guojing.yang@jiduatuo.com
    @abstractmethod
    def set_door_warning_FaultPlayProtectionActive_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        """
        功能: 设置四门防玩激活故障状态
        :param Drvr: 驾驶位故障状态，数据类型: bool
        :param Pass: 副驾驶故障状态，数据类型: bool
        :param LeRe: 左后故障状态，数据类型: bool
        :param RiRe: 右后故障状态，数据类型: bool
        :return:
        """
        pass

    # @Author:guojing.yang@jiduatuo.com
    @abstractmethod
    def set_door_warning_RollAngleAbnormal_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        """
        功能: 设置四门车辆横摆角度不正常故障状态
        :param Drvr: 驾驶位故障状态，数据类型: bool
        :param Pass: 副驾驶故障状态，数据类型: bool
        :param LeRe: 左后故障状态，数据类型: bool
        :param RiRe: 右后故障状态，数据类型: bool
        :return:
        """
        pass

    # @Author:guojing.yang@jiduatuo.com
    @abstractmethod
    def set_door_warning_RoadInclinationAbnormal_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        """
        功能: 设置四门道路倾斜角度不正常故障状态
        :param Drvr: 驾驶位故障状态，数据类型: bool
        :param Pass: 副驾驶故障状态，数据类型: bool
        :param LeRe: 左后故障状态，数据类型: bool
        :param RiRe: 右后故障状态，数据类型: bool
        :return:
        """
        pass

    # @Author:guojing.yang@jiduatuo.com
    @abstractmethod
    def set_door_warning_HallSensorsError_sts(self,
                             Drvr: Union[bool, None] = None,
                             Pass: Union[bool, None] = None,
                             LeRe: Union[bool, None] = None,
                             RiRe: Union[bool, None] = None
                             ):
        """
        功能: 设置四门霍尔传感器故障状态
        :param Drvr: 驾驶位故障状态，数据类型: bool
        :param Pass: 副驾驶故障状态，数据类型: bool
        :param LeRe: 左后故障状态，数据类型: bool
        :param RiRe: 右后故障状态，数据类型: bool
        :return:
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def check_power_outlet_relay_proxy_req(self, proxy_req: PowerOutLetReq):
        """
        通过总线校验12V电源服务请求闭合状态
        :param proxy_req: 12v继电器请求状态
            NoReq = 0
            On = 1
            Off  = 2   
        :return:
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def check_battery_save_prxy_req(self, battery_save: OnOff1):
        """
        通过总线节电继电器请求闭合状态
        :param battery_save: 节电继电器请求状态
            off = 0
            On = 1  
        :return:
        """
        pass



# o_fan.liu
    @abstractmethod
    def set_tailgate_AntiPinch_sts(self, AntiPinch: bool):  
        """
        设置尾门防夹状态
        :param AntiPinch:设置尾门是否处于防夹
            False = 0 #处于防夹
            True = 1 #不处于防夹
        :return:
        """
        pass


    
    # o_fan.liu
    @abstractmethod
    def check_tailgate_Position(self, Position: int):  
        """
        检查尾门开度请求
        :param Position:检查尾门开度
    
        :return:
        """
        pass

    # o_fan.liu
    @abstractmethod
    def set_tailgate_TrOpenPosn(self, TrOpenPosn: int):  
        """
        设置尾门当前开度
        :param TrOpenPosn:当前尾门开度
         
        :return:
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def set_crash_proxy_req(self, crash_proxy: OnOff1):
        """
        通过总线设置Crash继电器Proxy闭合请求状态
        :param crash_proxy: Crash继电器请求状态

            Off = 0  
            On = 1
        :return:
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def set_clima_proxy_req(self, clima_proxy: OnOff1):
        """
        通过总线设置空调继电器请求闭合状态
        :param clima_proxy: 空调继电器请求状态
            off = 0
            On = 1  
        :return:
        """
        pass
    
    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def set_relay_control_proxy_req(self, proxy_req: OnOff1):
        """
        恢复继电器仿真请求，恢复默认值
        :param proxy_req: 继电器请求状态
            off = 0
            On = 1  
        :return:
        """
        pass