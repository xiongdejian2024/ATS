#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :mix.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :需要多个基础能力一起模拟的场景，提供对应抽象接口；
"""
from abc import ABCMeta, abstractmethod
from xat_ecu.api.constants.common import *
from typing import Union


class AbcMix(metaclass=ABCMeta):

    @abstractmethod
    def set_usage_mode(self, usage_mode: UsageMode, do_assert: bool = True):
        """
        设置车辆UsageMode
        :param usage_mode: 枚举类型UsageMode
            class UsageMode(BaseEnum):
                ABANDONED = 0
                INACTIVE = 1
                CONVENIENCE = 2
                ACTIVE = 11
                DRIVING = 13
        :param do_assert: 模式切换失败时是否上报异常，True为上报(默认值)，False为不上报(主要进行一些异常测试)
        :returns:
        """
        pass

    @abstractmethod
    def set_car_mode(self, car_mode: CarMode):
        """
        设置car_mode
        :param car_mode: 枚举类型CarMode
            class CarMode(BaseEnum):
                NORMAL = 0
                TRANSPORT = 1
                FACTORY = 2
                CRASH = 3
                DYNO = 5
        :returns:
        """
        pass

    @abstractmethod
    def set_common_precontion(self, usage_mode: Union[UsageMode, None] = UsageMode.INACTIVE,
                              car_mode: Union[CarMode, None] = CarMode.NORMAL, veh_spd: Union[float, int] = 0.0,
                              vehmtnst: Union[VehMtnSts, None] = None, doors_sts: Union[Door, None] = None,
                              cenlock_sts: Union[CenLockSts, None] = None, ccp: dict = {}):
        """
        功能:提供一个设置case的前提条件的接口,目前可以设置的包括usagemode,carmode,车速，车辆移动状态（vehmtnst），5门的状态（doors_sts），中控锁状态(cenlock_sts),CCP配置。
        @param usage_mode: Usagemode状态，默认值为1
        @param car_mode: Carmode,默认值为0
        @param veh_spd: 设置车速，默认值为0
        @param vehmtnst:车辆移动状态,默认没有使用，如果车速为0的时候默认vehmtnst=VehMtnSt2_StandStillVal3
        @param doors_sts:5门状态，默认没有设置，doors_sts = "close"表示5门关;doors_sts = "open"表示5门开
        @param cenlock_sts:中控锁状态，默认没有设置，cenlock_sts = "lock",表示中控锁处于上锁状态，cenlock_sts = "unlock",表示中控锁处于解锁状态
        @param ccp:设置CCP,默认没有设置ccp，ccp={98: 0x2, 97: 0x2}表示设置CCP 98 = 2;CCP 97 = 2
        :return:     
        """

    @abstractmethod
    def send_s2s_request_and_check(self, send_s2s_request_parameter: Union[tuple, list],
                                   check_signal_parameter: Union[tuple, list] = (),
                                   check_service_response: Union[tuple, list] = (),
                                   check_s2s_event_parameter: Union[tuple, list] = ()):
        """
        功能:检测通过服务来触发BGM相关的总线信号,服务状态，事件上报
        @param send_s2s_request_parameter_tuple:调用的S2S服务
        @param check_signal_parameter: 要检测的BGM发出的信号
        @param check_service_response 要获取的服务状态
        @param check_s2s_event_parameter 要检测测服务事件上报
        :return: 
        """

    @abstractmethod
    def check_signal_value_all_is(self, check_signal_parameter_tuple: tuple):
        """
        功能：检测信号的值是否一直为某个值。
        @param check_signal_parameter_tuple:参数类型为元组，要检测的信号以及值，例如：("backbonefr.CemBackBoneFr07",'WipgInfoWipgSpdInfo', 0,"timeout=5"),
            表示检测信号WipgInfoWipgSpdInfo再5秒钟内是否一直为0
        :return:
        """

    @abstractmethod
    def set_signal_value(self, set_signal_parameter: Union[tuple, list]):
        """
        功能：设置信号
        @param set_signal_parameter:参数类型为元组或者列表
        :return: 
        """

    @abstractmethod
    def check_signal_value(self, check_signal_parameter: Union[tuple, list]):
        """
        功能：检测信号值
        @param check_signal_parameter:参数类型为元组或者列表
        :return: 
        """

    @abstractmethod
    def set_signal_and_check(self, set_signal_parameter: Union[tuple, list],
                             check_signal_parameter: Union[tuple, list] = (),
                             check_service_response: Union[tuple, list] = (),
                             check_s2s_event_parameter: Union[tuple, list] = ()):
        """
        功能:检测通过模拟总线信号变化,来检测相应总线信号变化,服务状态，事件上报
        @param set_signal_parameter:模拟发送的总线信号，参数类型为元组或者列表。
        @param check_signal_parameter: 要检测的BGM信号,
        @param check_service_response 要获取的服务状态
        @param check_s2s_event_parameter 要检测测服务事件上报
        :return: 
        """

    @abstractmethod
    def send_s2s_service_request(self, send_s2s_request_parameter: Union[tuple, list]):
        """
        功能:发送s2s服务请求
        @param send_s2s_request_parameter:发送s2s服务请求参数。
        :return: 
        """
        pass

    @abstractmethod
    def check_s2s_event(self, check_s2s_event_parameter: Union[tuple, list]):
        """
        功能:check s2s 事件上报
        @param check_s2s_event_parameter 要检测测服务事件上报参数
        :return: 
        """
        pass

    @abstractmethod
    def send_s2s_request_and_check_response(self, send_s2s_req_and_check_resp: Union[tuple, list]):
        """
        功能:获取s2s服务状态
        @param send_s2s_req_and_check_resp:获取s2s服务状态的参数
        :return: 
        """
        pass

    @abstractmethod
    def set_get_battery_tem_sts(self, HvBattCellTInfo: int, sts: bool):
        """
        设置获取电池低温告警
        S2S在收到GetBatteryTemperatureLowState()调用时，返回bool。参数bool与信号
        HvBattCellTInfoHvBattTMin映射关系如下：
        信号HvBattCellTInfoHvBattTMin-40≤-10°C，bool=1；
        信号HvBattCellTInfoHvBattTMin-40≥0°C，   bool=0；
        -10°C<HvBattCellTInfoHvBattTMin-40<0°C,     bool保持Last value
        默认值：0
        :param HvBattCellTInfo:温度
        :param sts:告警状态
        :return:
        """
        pass

    @abstractmethod
    def set_get_hv_power_sts(self, err_sts: bool, ValidityLevel: ValidityLevel):
        """
        设置获取动力系统故障
        :param err_sts:故障状态
        :param ValidityLevel:功能安全通用信息安全等级
        :return:
        """
        pass

    @abstractmethod
    def set_get_hv_battery_Fault(self, err_sts: bool, ValidityLevel: ValidityLevel):
        """
        设置获取高压电池故障
        :param err_sts:故障状态
        :param ValidityLevel:功能安全通用信息安全等级
        :return:
        """
        pass

    @abstractmethod
    def ctrl_lock(self, lock_type: LockCmd, ctrl_type: LockSource):
        """
        控制整车的解锁和闭锁；
        :param lock_type:解锁和闭锁
        :param ctrl_type:控制锁的方式
        :return:
        """
        pass

    @abstractmethod
    def parse_excel_to_signal_routing_csv(self, excel_path, csv_path):
        """
        把 信号路由的excel 表处理成需要的csv 文件
        @param self:
        @param excel_path: 原表路径
        @param csv_path: 保存的csv 文件路径
        @return:  csv 文件路径
        """
        pass

    @abstractmethod
    def read_signal_routing_info(self, path=None, select_cond='cycle'):
        """
        读取信号路由的相关信息
        @param path: csv 文件路径
        @param select_cond: 根据条件筛选 ["cycle", "event", "ub", "crc", "counter"]
        @return: 返回列表,列表内容为字典字典的key为如下
        csv_header = [
            'SignalName',
            'Tx_BusChannel',
            'Tx_ECUName',
            'Tx_MessageName',
            'Tx_MessageID',
            'Tx_MessageCyclic',
            'EnableUB', 'crc','counter',
            'Rx_BusChannel',
            'Rx_ECUName',
            'Rx_MessageName',
            'Rx_MessageID',
            'Rx_MessageCyclic',
            "Len",
            "repeat",
        ]
        """
        pass

    @abstractmethod
    def get_signal_routing_communication_excel_path(self, excel_path):
        """
        获取信号路由通信矩阵的 路径
        返回 True ，CSV文件路径，原表的路径，表示 csv文件存在，无需解析
        返回 Flase ，CSV文件路径，原表的路径，表示 csv文件不存在，需要根据原表解析
        @param excel_path: 存放excel 表的路径
        @return: 返回 BOOL，path，path （True/False，CSV文件路径，原表的路径）
        """
        pass

    @abstractmethod
    def send_signal_route_and_check_result(self, item, set_ub_flag=True):
        """
        发送 信号，并校验接收信号，发送的信号有，最大值，最小值，以及中间的一个随机值
        带ub 位的 设置ub位为 True 可以路由
        带ub 位的 设置ub位为 False，不可以路由

        @param item:
        @param set_ub_flag: 设置ub位
        @return:
        """
        pass

    @abstractmethod
    def check_signal_route_items(self, excel_path=None, select_cond='cycle'):
        """
         遍历 data_list 里面的路由信号，发送的信号有，最大值，最小值，以及中间的一个随机值
        @param excel_path:  excel表 路径
        @param select_cond: 根据条件筛选 ["cycle", "event", "ub"]
        @return:
        """
        pass

    @abstractmethod
    def fota_back_to_idle(self):
        """
        根据当前FOTA Master状态, 发送对应request, 使FOTA Master Status回到Idle
        
        :returns: None
        :raises keyError: None
        """
        pass

    @abstractmethod
    def read_diag_route_excel(self, excel_path, sheet_name=None):
        """
        读取诊断路由的 excle表,
        如果传递 sheet_name 为None 则 读取所有的 sheet 表，返回一个字典,
        字典key 为sheet 名字value 为该sheet的 信息
        字典{
         sheet_name1 :[{}，{}],
         sheet_name1 :[{}，{}],
        }
        如果传递 sheet_name 为 具体的sheet 页，则返回一个列表，[{},{}]
        @param self:
        @param excel_path: 原表路径
        @param sheet_name: 读取的 sheet 名字 或者为None
        @return:
        """
        pass

    @abstractmethod
    def log_and_allure_step(self, log_string: str, level=LogLevel.INFO):
        """
        打印日志，并写allure 步骤
        @param log_string:
        @param level:
        @return:
        """
        pass

    @abstractmethod
    def diag_route_eth2can(self, data_info_list, send_length):
        """
        发送 以太到 can canfd 的诊断路由，并且can 回复响应
        @param data_info_list:
        @param send_length:
        @return:
        """
        pass


    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_and_check_low_beam(self, sts: isOn):
        """
        设置并且检查近光灯开关状态
        @param sts: 近光灯开关状态
        @return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_lb_off_and_night_mode_sped0(self):
        """
        设置：近光关 夜晚模式 车速零
        @param :
        @return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_intr_light_auto_and_in_night_mode(self):
        """
        设置：设置内灯为Auto模式,并且设置夜晚模式
        @param :
        @return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def init_boot_per(self):
        """
        设置初始化条件 保证bgm可以进入boot：使得车速为0，usagemode为abandoned carmode为normal
        @param :
        @return:
        """
        pass
    
    @abstractmethod
    def delete_vehicleInfo_json(self):
        """
        删除BGM vehicleInfo_json文件并重启等待10s
        @param :
        @return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_low_volt_servse_mode(
        self,
        sys_falt: Union[bool, None] = None,
        low_volt: Union[bool, None] = None,
        serv: Union[bool, None] = None,
        time_wait: Union[float, int] = 0,
    ):
        """
        设置智能补电允许情况:系统故障补电 低压补电 服务补电
        :param sys_falt:系统故障补电
        :param low_volt:低压补电
        :param serv:服务补电
        :param time_wait: 执行操作之后的等待时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_seats_present_sts(self,
                              drv_seat: Union[SeatPresSts, None] = None,
                              pass_seat: Union[SeatPresSts, None] = None,
                              sec_left: Union[SeatPresSts, None] = None,
                              sec_mid: Union[SeatPresSts, None] = None,
                              sec_right: Union[SeatPresSts, None] = None):
        """
        功能：5个座椅占位情况
        :param drv_seat: 驾驶位座椅占位情况
        :param pass_seat: 副驾驶座椅占位情况
        :param sec_left: 左后座椅占位情况
        :param sec_mid: 后中座椅占位情况
        :param sec_right: 右后座椅占位情况
        :return:
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_all_seats_present_sts(self, seat_pres_sts: SeatPresSts):
        """
        功能：同时设置所有的座椅占位情况
        :param seat_pres_sts: 占位情况
            NoPres = 0
            Pres = 1
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def s2s_change_car_mode_and_check_result(self, car_mode:CarMode, car_mode_sub:int):
        """
         功能：服务切换carmode并检查状态
        :param car_mode: 要设置的carmode
        :param car_mode_sub: 要设置的carmode子状态
        :return:
        """


    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def trigger_usage_mode_to_abandoned(self,wait_time:Union[int,float] = 180):
        '''
        进入 abandoned 模式
        @param wait_time:  关闭四门两盖以后，中控锁上锁后，最长等待时间
        @param do_assert: 为true   进入失败则会报错，为False 则不会报错，返回当前模式
        @param kwargs:
        @return:
        '''
        
    @abstractmethod
    def back_fota_to(self, fota_sts: FOTAMasteSts, taskid = 0):
        '''
        令FOTA 回到特定阶段
        
        :param 枚举类型 FOTAMasteSts:
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
                FACTORY_TASK = 20
                FACTORY_UPDATE = 21
                FACTORY_SUCCESSFUL = 22
                FACTORY_FAILED = 23
        :param taskid:FOTA 任务id
        :return:
        '''

    def set_factory_ota_condition(self, display_hv_soc:Union[int,float], low_volt_power:Union[int,float], local_diag_sts:DiagActLineSts):
        '''
        设置厂内OTA前置条件
        
        :param display_hv_soc: 显示的大电池值
        :param low_volt_power: 小电池电量
        :param local_diag_sts: 本地诊断连接状态
        :return:
        '''

    @abstractmethod
    def back_ua_to(self, domain_name: DOMAIN, ua_sts: UA_Sts, downlaod_req):
        """
        根据UA当前状态, 发送requset直至UA回到Idle

        :param 枚举类型 DOMAIN:
            class DOMAIN(BaseEnum):
                BGM = 0
                TCAM = 1
                CDC = 2
                ACU = 3
        :param 枚举类型 UA_Sts:
            class UA_Sts(BaseEnum):
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
        :param  downlaod_req: ua版本下载请求的json格式数据
        :returns:
        :raises keyError:
        """

    @abstractmethod
    def chk_tcam_ping(self, ping_time):
        """
        校验tcam两路网卡ping是否正常
        :param ping_time: ping 时长
        :returns:
        """
        pass

    @abstractmethod
    def chk_bgm_ping(self, ping_time):
        """
        校验bgm 联网是否正常
        :param ping_time: ping 时长
        :returns:
        """
        pass

    @abstractmethod
    def chk_bmg_ping_tcam(self, ping_time):
        """
        校验bgm 与tcam是否互通
        :param ping_time: ping 时长
        :returns:
        """
        pass

    # author:dejian.xiong@jiduauto.com
    @abstractmethod
    def network_sleep(self):
        """
        设置网络休眠
        """
        pass

    @abstractmethod
    def check_tcam_sleep(self,time_out: int = 180):
        """
        检查TCAM是否休眠
        """
        pass


    @abstractmethod
    def tcam_network_sleep(self):
        """
        执行TCAM的休眠动作。若自身业务依旧存在逻辑则无法休眠
        """
        pass


    @abstractmethod
    def check_ccp_data_resp(self, check_type:CheckType, bus_name, id: Union[str, int], data_index=0):
        """
        验证收到的ccp值是否符合需求

        :param 枚举类型 CheckType:
            class CheckType(BaseEnum):
                IN_TIME = 1 # 一个周期是否在9秒内
                IN_ALL = 2 # 30s有多少完整周期
                IS_COMPLETE = 3 # 一个周期是否完整
        :param bus_name: 总线名称
        :param bus_name: 报文id
        :param bus_name: block_id的起始位,默认值为0
        :returns:
        :raises keyError:
        """
    @abstractmethod
    def get_mcu_cpuload_save_data(self, path='/root/bgm_log/cpu_load',run_status='', **kwargs):
        '''
        读取mcu cpu load 保存在csv 文件
        @param path: 保存路径
        @param run_status: 运行状态
        @param kwargs:
        @return:
        '''
    
    @abstractmethod
    def service_change_usage_mode_and_check_result(self, usagemode:UsageMode):
        """
        @usagemode:期望切换的模式
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def wti_sig_set_and_get_and_event_check_warning_light_sts(self,func:WTI_Func,sig_value:Union[int,float], prom_name: str, prom_state: str):
        """
        设置WTI相关的信号之后通过服务获取告警灯相关状态和事件上报
        @param func:WTI功能 枚举：WTI_Func,功能太多不便展示
        @param sig_value：设置的信号值
        @param prom_name：check的提示字符串 
        @param prom_state：check 提示的状态
        @return:
        """

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def wti_sig_set_and_get_and_event_check_warning_info_list(self,func:WTI_Func,sig_value:Union[int,float], prom_name: str, prom_state: str):
        """
        设置WTI相关的信号之后通过服务获取告警信息和事件上报
        @param func:WTI功能 枚举：WTI_Func,功能太多不便展示
        @param sig_value：设置的信号值
        @param prom_name：check的提示字符串 
        @param prom_state：check 提示的状态
        @return:
        """
    @abstractmethod
    def diag_route_doip2can_func(self, data_info_list, send_length, **kwargs):
        """
        发送 以太到 can canfd 的诊断路由
        @param data_info_list:
        @param send_length:
        @return:
        """
    @abstractmethod
    def diag_route_eth2can_unrecv(self, data_info_list, send_length):
        """
        发送 以太到 can canfd 的诊断路由，并且can 回复响应
        @param data_info_list:
        @param send_length:
        @return:
        """
    
    @abstractmethod
    def SetConvenienceForAppAction_and_check_usagemode(self, time1: int , usagemode: UsageMode):
        """
        应用请求上切convenience并check预期的usagemode
        
        :param time1: 上切后超时下切的时间，单位为分钟
        :param usagemode： 发送请求后预期的模式
        :returns: 
        :raises keyError: 
        """
    
    @abstractmethod
    def wait_time_in_usagemde(self, num, usagemode: UsageMode):
        """ 
        保持在某个模式多少分钟
        
        :param num: 多少分钟
        :param usagemode:要保持的模式
        :returns: 
        :raises keyError: 
        """

    @abstractmethod
    def wait_time_exit_usagemde_a_to_b(self, num, usagemode1: UsageMode, usagemode2: UsageMode):
        """
        保持在某个模式多少分钟后退出到指定的模式
        
        :param num: 多少分钟
        :param usagemode1:时间内要保持的模式
        :param usagemode2:到达时间后要下切的模式
        :returns: 
        :raises keyError: 
        """

    @abstractmethod
    def creat_diag_route_doip2can_phy_invalid_data_item(self,data_info_list_phy):
        '''
        构造 以太到can的 物理寻址的，无效数据
        @return:
        '''

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def generate_dtc_fault(self,dtc_fault:DTCFault,last_time:Union[int,float] = 0):
        """
        制造DTC故障
        :param dtc_fault:DTC故障名字，枚举：DTCFault,太多没有全部展示
            AWMSensorFail_A = "A02D7C"
            AWMSensorFail_B = "A02D7D"
        :param last_time:制造DTC之后，等待的持续时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def remove_dtc_fault(self,dtc_fault:DTCFault,last_time:Union[int,float] = 0):
        """
        移除DTC故障
        :param dtc_fault:DTC故障名字，枚举：DTCFault,太多没有全部展示
            AWMSensorFail_A = "A02D7C"
            AWMSensorFail_B = "A02D7D"
        :param last_time:移除DTC之后，等待的持续时间
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_dtc_precontion(self):
        """
        设置DTC测试前提条件
        :return:
        """
    
    @abstractmethod
    def keep_lin_wake_up(self,usage_mode,channel,speed=0):
        """
        检查lin是否一直为唤醒状态
        """
    @abstractmethod
    def lin_sleep(self,usage_mode,channel,speed=0):
        """
        检查lin是否为休眠状态
        """

    @abstractmethod
    def pc_ping_BGM_and_vlan(self, count=10, err_count=3, condition="boot 下", dst_tar="tcam", ip='172.16.5.31'):
        '''

        @param count: 总共ping 几次
        @param err_count: 几次不通 报错
        @return:
      
       '''
    @abstractmethod
    def change_ip_and_id(self,ip,id,vlan):
        """
        修改vlan ip 及 mac id
        """
    @abstractmethod
    def ping_bgm_ip_and_vlan_ip(self,bgm_ip,other_ip):
        """
        检查是否能ping通BGM及其他IP
        """
    
    @abstractmethod
    def set_PtActvnReq(self, up_type:UpType):
        """
        触发PtActvnReq置位

        :param up_type :触发的类型 0 gear, 1 geatAuto, 2 gearCdc ,3 setusagemodeup = 13, 4 setusagemodewithoutkey = 2
        :returns: 
        :raises keyError: 
        """
    @abstractmethod
    def filter_vehicle_announcement_fun(self, pack):
        '''
        回调函数，过滤 车辆公告
        @param pack: 以太报文包
        @return:
        '''
    @abstractmethod
    def get_veh_ann_time_under_app_mode_send_func_1181(self,iface, max_time=30, do_assert=True):
        '''
        APPMode下_功能寻址_1181重启后车辆公告发出时长
         @param iface: OBD 口网卡名字
        @param max_time: 最长时间
        @param do_assert: 是否会报错，默认报错
        @return:
        '''

    @abstractmethod
    def get_veh_ann_time_under_app_mode_send_func_1082(self,iface, max_time=15, do_assert=True):
        '''
        APPMode下_功能寻址_1082重启后车辆公告发出时长
        @param iface: OBD 口网卡名字
        @param max_time: 最长时间
        @param do_assert: 是否会报错，默认报错
        @return:
        '''
    
    @abstractmethod
    def get_veh_ann_time_under_boot_mode_send_func_1181(self,iface, max_time=20, do_assert=True):
        '''
            BootMode下_功能寻址_1181重启后车辆公告发出时长
        @param iface: OBD 口网卡名字
        @param max_time: 最长时间
        @param do_assert:
        @return:
        '''
    
    @abstractmethod
    def set_precon_to_abandon(self):
        """
        满足进入abandon的条件
        
        :param：
        :returns: 
        :raises keyError: 
        """
       
    @abstractmethod
    def set_fota_RemoteUpdate_condition(self, usagemode:UsageMode, lock_cmd:LockCmd):
        """
        设置fota进入RemoteUpdate状态的条件

        :param 枚举类型 UsageMode:
            class UsageMode(BaseEnum):
                ABANDONED = 0
                INACTIVE = 1
                CONVENIENCE = 2
                ACTIVE = 11
                DRIVING = 13
        :param 枚举类型 LockCmd:
            class LockCmd(BaseEnum):
                UnLock = 0
                Lock = 1
                AllDoorCloseAndLock = 2
                LockCompleteArm = 3
        :returns:
        :raises keyError:
        """
        
    @abstractmethod
    def generate_fota_appointment_time(self, delay_seconds: int = 300):
        """
        返回一个未来的时间, 用于预约升级
        
        :param 枚举类型 delay_seconds:延迟多少秒
        :returns:
        :raises keyError:
        """

    @abstractmethod
    def return_when_reach_target_time(self, target_time: int, monitor_cycle: int = 1):
        """
        到达系统目标时间立即返回

        :param target_time: 目标时间, BCD格式
        :param monitor_cycle: 监控周期
        :returns:
        :raises keyError: 
        """
        
    @abstractmethod
    def check_fota_keep_awake(self, pnc29: bool, acu_keep_alive: bool, up_inactive: bool):
        """
        检查FOTA唤醒条件

        :param pnc29: 是否检查pnc 29
        :param acu_keep_alive: 是否检查acu keep alive
        :param up_inactive: 是否检查上切inactive
        :returns:
        :raises keyError: 
        """

    @abstractmethod
    def set_enter_boot_condition(self, usagemode: UsageMode, low_volt_power: Union[int, float], vehspd: Union[int, float]):
        """
        设置BGM MCU进boot条件
        注: usagemode 不等于 driving, 小电池电压 大于 9v, 车速 不等于 0

        :param usage_mode: 枚举类型UsageMode
            class UsageMode(BaseEnum):
                ABANDONED = 0
                INACTIVE = 1
                CONVENIENCE = 2
                ACTIVE = 11
                DRIVING = 13
        :param low_volt_power: 小电池电量
        :param vehspd: 车速
        :returns:
        :raises keyError: 
        """

    @abstractmethod
    def wait_appoint_until_excut_time(self, task_time):
        """
        设置远控座舱预约等待至用户上车前15min
        :param task_time:  远控座舱预约的上车时间 
        
        """
    
    @abstractmethod
    def wait_appoint_until_use_time(self, task_time):
        """
        设置远控座舱预约等待至用户上车时间
        :param task_time:  远控座舱预约的上车时间 
        
        """

    @abstractmethod
    def chk_rvc_cock_reserv_pnc(self):
        """
        检查远控座舱预约PNC报文置位状态

        """

    @abstractmethod
    def chk_rvc_cock_reserv_taskupload(self, task_time, message):
        """
        检查TCAM上报预约任务的上报协议是否正确
        需配合远控座舱预约任务下发接口一起使用
        :param task_time : 远控座舱预约的上车时间
        :param message   : TCAM上报到车云的远程座舱预约结果
        
        """
    
    @abstractmethod
    def chk_rvc_vent_reserv_taskupload(self, message, fields_to_check = ["ac_control"],expected_msg:str="Success", success=True):
        """
        检查TCAM上报预约任务的上报协议是否正确
        :param expected_msg      : 远控座舱预约通风的关键字
        :param message           : TCAM上报到车云的远程座舱预约结果
        :param fields_to_check   : 定义要校验的字段列表
        :param success           : 是否是结果正向检查，默认检查success
        
        """
    
    @abstractmethod
    def chk_rvc_vent_reserv_threads(self, ids: list=[str], timeout: int = 1800):
        """
        开始启动检查预约座椅通风关闭请求的线程
        :param ids       : 远控座舱预约通风的前后排座椅
        :param timeout   : 检查超时时间
        
        """
    
    @abstractmethod
    def chk_rvc_threads(self, target: callable, args: list):
        """
        开始启动检查远控服务请求的线程
        :param target     : 要执行的目标函数
        :param args       : 目标函数的参数
        
        """
    
    @abstractmethod
    def check_convenience_mode_duration(self, duration=255, do_assert=True, **kwargs):
        """
        检查驻车舒享模式是否和预期一致
        
        :param duration: 期待的驻车舒享的值
        :parm do_assert: 报错则返回模式不匹配，不报错则不返回
        :returns: 检查一致返回True,不一致返回False
        :raises keyError: 
        """
    
    @abstractmethod
    def set_keep_power_and_check_notify(self, flag:KeepPowerFlag):
        """
        控制维持上电模式并检查上报的notify通知
        
        :param flag: 控制的类型 
            0 open 
            1 close_服务
            2 close_hvsoc
            3 close_gear
            4 close_carmode
            5 close_fota
            6 close_other
        :returns: 
        :raises keyError: 
        """
    @abstractmethod
    def eth2can_send_response_recv_flow_frame(self, data_info_list, **kwargs):
        '''
        不发送请求，can 节点直接发送多帧响应，bgm 回复流控帧
        @param data_info_list: 
        @param kwargs: 
        @return: 
        '''

    @abstractmethod
    def make_can_communicate_err(self,bus_name,send_node_name,make_fault_msg,make_fault_before_expect_res,make_fault_after_expect_res):
        """
        制造can 某个节点故障
        @param bus_name: 通道名称
        @param send_node_name: 节点名称
        @param make_fault_msg: 制造故障信息
        @param make_fault_before_expect_res: 制造故障后的期望结果
        @param make_fault_after_expect_res: 制造故障清除后的期望结果
        """

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def get_request_and_send_response_to_tcam(self, check_req_list: list, func_param: dict, ignore_func:list):
        """
        通过SOA Partner监听TCAM发送的请求，并发送请求的响应，线程方式监听
        :param check_req_dict: 待监听的服务列表，实例化服务名(如HighVoltageService_server)
        :param func_param: 字典类型。指定请求的响应值。
        :param ignore_func: list 忽略的请求。如果接收到该请求则忽略 []
        :return:
        """
        pass

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def start_get_request_and_send_response_to_tcam_thread(self, check_req_list: list, func_param: dict = {}, ignore_func:list=[]):
        """
        通过SOA Partner监听TCAM发送的请求，并发送请求的响应，线程方式监听
        建议放到before_class中.
        :param check_req_dict: 待监听的服务列表，实例化服务名 示例：['HighVoltageService_server']
        :param func_param: 字典类型。指定请求的响应值。参数示例： {'GetVIN':{'vin':self.tb_config['vin']}} 可以为空。
        :param ignore_func: list 忽略的请求。如果接收到该请求则忽略 如: ['SetSpecificWindowPosition']
        :return:
        """
        pass
    
    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def stop_get_request_and_send_response_to_tcam_thread(self):
        """
        停止start_get_request_and_send_response_to_tcam_thread 线程
        一般放到after_class中
        """
        pass

    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def set_func_param(self, func_param:dict):
        """
        设置方法对应的参数
        """
        pass
    
    # @Author:o_liangliang.chen@external.jiduauto.com
    @abstractmethod
    def default_func_param(self,func_names:list):
        """
        将设置方法的参数清楚，使用方法响应的默认值
        """
        pass

    @abstractmethod
    def make_can_communicate_err(self,bus_name,send_node_name,make_fault_msg,make_fault_before_expect_res,make_fault_after_expect_res):
        """
        制造can 某个节点故障
        @param bus_name: 通道名称
        @param send_node_name: 节点名称
        @param make_fault_msg: 制造故障信息
        @param make_fault_before_expect_res: 制造故障后的期望结果
        @param make_fault_after_expect_res: 制造故障清除后的期望结果
        """


    @abstractmethod
    def set_enter_boot_condition(self, usagemode: UsageMode, low_volt_power: Union[int, float], vehspd: Union[int, float]):
        """
        设置BGM MCU进boot条件
        注: usagemode 不等于 driving, 小电池电压 大于 9v, 车速 不等于 0

        :param usage_mode: 枚举类型UsageMode
            class UsageMode(BaseEnum):
                ABANDONED = 0
                INACTIVE = 1
                CONVENIENCE = 2
                ACTIVE = 11
                DRIVING = 13
        :param low_volt_power: 小电池电量
        :param vehspd: 车速
        :returns:
        :raises keyError: 
        """

    @abstractmethod
    def filter_switch_port_fun(self, packet):
        '''
        回调函数，过滤 switch_port
        测试工具发送 start test 请求（31 01 DC05），SOC 收到请求后，以周期 1s 发送广播 UDP 消息（255.255.255.255， port: 7000）with payload
            0102030405060708090A
        @param pack: 以太报文包
        @return:
        '''

    @abstractmethod
    def bgm_soc_switch_port(self, iface='any', do_assert=True, ):
        '''
        测试工具发送 start test 请求（31 01 DC05），SOC 收到请求后，以周期 1s 发送广播 UDP 消息（255.255.255.255， port: 7000）with payload
        0102030405060708090A
        测试工具监控 5s(TBD)内所有 ports 是否收到了广播消息并 check payload
        收到后，测试工具发送 stop test 请求（31 02 DC05），SOC 收到请求后，停止发送 UDP 消息
        @param do_assert:
        @return:
        '''

    @abstractmethod
    def bgm_soc_check_mcu_mpu_comm_link_status(self, do_assert=True):
        '''
        如果收到 OK, 说明测试通过
        SOC 监控 MCU 发送的周期心跳请求，如果 1s 收不到就认为 link 有问题
        BGMIntEthPDU20020 MCU->SOC Cyclic-100ms 20020 1 HeartbeatMonitorUp
        BGMIntEthPDU20021 SOC->MCU Cyclic-100ms 20021 1 HeartbeatMonitorDown
        @param do_assert:
        @return:
        '''
    
    @abstractmethod
    def check_exhibition_mode(self, status: bool):
        """
        检查展车模式状态

        :param status: True 是展车模式， False 不是展车模式
        :returns: 
        :raises keyError: 
        """

    @abstractmethod
    def set_and_check_exhibition_mode(self, status: bool):
        """
        设置并检查展车模式状态

        :param status: True 展车模式， False 非展车模式
        :returns: 
        :raises keyError: 
        """
    
    @abstractmethod
    def set_tcam_bgm_to_wakeup(self):
        """
        使BGM & TCAM诊断激活线 上电

        """
        pass
    
    @abstractmethod
    def chk_tcam_reboot_or_not(self, time:int=15):
        """
        检查time周期内tcam是否重启,默认检查15min,time单位是1min
        """
        pass
    
    @abstractmethod
    def check_keywords_in_version_collect_results(self, taskid=None, expect_keywords: list=[], unexpect_keywords: list=[]):
        '''
        检查关键字是否出现在fota版本收集结果中

        :param taskid:FOTA 任务id
        :param expect_keywords: 期望出现的关键字
        :param unexpect_keywords: 不期望出现的关键字
        :return:
        :raises AssertionError
        '''

    @abstractmethod
    def check_factory_F154_results(self):
        '''
        检查厂内OTA升级结果与F154写入值是否匹配

        :return:
        :raises AssertionError
        '''

    @abstractmethod
    def check_remote_diag_results(self, remote_diag_res:CheckRemoteDiagRes):
        '''
        检查远程诊断执行结果

        :return:
        :raises AssertionError
        '''

    @abstractmethod   
    def get_bus_send_recv_info(self, ipdu, channel_name: str, **kwargs):
        '''
         根据通道获取当前通道的，发送节点和接收节点的数据
         @param ipdu:  对象 self.ipdu
         @param channel_name: 通道   bodycan 等等
         @param kwargs:
         @return: {}
        {
             "发送节点": {
                 "周期发送": {
                     "BGM": [ {"msg_name": msg_name,
                             "msg_id": msg_id,
                             "msg_type": msg_type,
                             "msg_tx_method": msg_tx_method,
                             "msg_cycle": msg_cycle,
                             "msg_length": msg_length,
                             "rx_nodes": rx_nodes,
                             "tx_node": tx_node,
                             "msg_base_cycle": msg_base_cycle,
                             "msg_repetition": msg_repetition}, {}],
                     "CCD": [{}, {}],
                 },
                 "非周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
             },
             "接收节点": {
                 "周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
                 "非周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
             },

         }
        '''

    @abstractmethod
    def check_app_busoff_channel_recv_msg(self,channel_name):
        """
        @param channel_name:  通道名称
        """

    @abstractmethod
    def check_boot_busoff_channel_recv_msg(self,channel_name):
        """
        @param channel_name:  通道名称
        """

    @abstractmethod
    def network_sleep_by_single_tcam(self):
        """
        单域TCAM休眠
        :return:
        """
			
    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def check_tcam_process_status(self, proecess_list: list, cmd: str = "ps -ef|grep -E 'usr|app|oem|mode=260'"):
        '''
        检查TCAM进程是否正常运行：
        :param proecess_list: 进程列表，要检查的进程集合，元素为字符串类型；
        :param cmd: 字符串类型，查询TCAM进程的指令
        '''
    
    @abstractmethod
    def set_strt_req(self, up_type:UpType):
        """
        触发start_req置位

        :param up_type :触发的类型 0 gear, 1 geatAuto, 2 gearCdc ,3 setusagemodeup = 13, 4 setusagemodewithoutkey = 2
        :returns: 
        :raises keyError: 
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def clear_pnc(self,pnc:BGMPNC):
        """
        清除PCN：{pnc.name}置位
        :param pnc: 要清除的PNC
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
        :return:
        """

    @abstractmethod
    def diag_route_can2can(self, data_info_list, send_length):
        """
        发送 以太到 can canfd 的诊断路由，并且can 回复响应
        @param data_info_list:列表 里面是字典格式元素包含每一条路由的信息
        @param send_length: 报文长度
        @return:
        """

    @abstractmethod
    def diag_route_can2can_unrecv(self, data_info_list, send_length, all_can=False,**kwargs):
        """
        发送 以太到 can canfd 的诊断路由，并且can 回复响应
        @param data_info_list:列表 里面是字典格式元素包含每一条路由的信息
        @param send_length:报文长度
        @return:
        """
        #

    @abstractmethod
    def creat_diag_route_can2can_phy_invalid_data_item(self, data_info_list_phy):
        '''
        构造无效数据
        @param data_info_list_phy:列表 里面是字典格式元素包含每一条路由的信息
        @return:
        '''

    @abstractmethod
    def diag_route_can2can_unsend_flow_frame(self, data_info_list, send_length):
        """
        发送多帧到下挂 ，下挂节点接收首帧，不回复流控帧，则收不到连续帧
        @param data_info_list:列表 里面是字典格式元素包含每一条路由的信息
        @param send_length:报文长度
        @return:
        """

    @abstractmethod
    def diag_route_eth2can_unsend_flow_frame(self, data_info_list, send_length):
        """
        发送多帧到下挂 ，下挂节点接收首帧，不回复流控帧，则收不到连续帧
        @param data_info_list:列表 里面是字典格式元素包含每一条路由的信息
        @param send_length:报文长度
        @return:
        """

    @abstractmethod
    def diag_route_can2can_func(self, data_info_list, send_length, **kwargs):
        """
        发送 can 到 can canfd 的诊断路由  功能寻址
        @param data_info_list:列表 里面是字典格式元素包含每一条路由的信息
        @param send_length:报文长度
        @return:
        """
      
    @abstractmethod
    def send_diag_route_eth2fr(self,data_info_list,send_length):
        '''
        发送诊断路由 以太到fr的
        @param data_info_list: 列表格式，里面是字典，包含每条信息的具体内容
        @param send_length: 发送数据长度
        @return:
        '''

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_digital_key_pre_condition(self):
        """
        设置数字钥匙测试的公共前提条件
        @param :
        @return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_turn_lamp_flash(self,pos:GeneralPos,sts:isOn,last_time:int):
        """
        Check外灯的双闪状态(相关的信号：IndcrDisp、ExtrLtgStsTurnIndrLe，ExtrLtgStsTurnIndrRi，ActvnOfIndcrIndcrOut)
        @param : pos 要check的灯的位置
            Left = 2
            Right = 3
            All = 4
        @param : sts check的状态
            Off = False
            On = True
        @param : last_time check的持续时间
        @return:
        """
    
    @abstractmethod
    def test_check_ping_tcam_success(self,bgm_wait_time:int,tcam_wait_time:int,expect_value:int):
        """
        bgm与tcam通讯正常
        @param bgm_wait_time: bgm断电上电后等待的时间
        @param tcam_wait_time: tcam断电后等待的时间
        @param expect_value: 期待出现的次数
        """
    @abstractmethod
    def test_check_ping_tcam_fail(self,bgm_wait_time,tcam_wait_time,expect_value,phy_reset_count):
        """
        bgm与tcam通讯异常
        @param bgm_wait_time: bgm断电上电后等待的时间
        @param tcam_wait_time: tcam断电后等待的时间
        @param expect_value: 期待出现的次数
        @param phy_reset_count: 复位的次数
        """
    @abstractmethod
    def write_vehicle_model_ccp(self, vehicle_model: VehicleType = VehicleType.Mars,
                                vehicle_mca: VehicleMca = VehicleMca.Mca_400v,
                                ccp_value: [list, str, None] = None, **kwargs):
        '''
          写入 车型
        @param vehicle_model: （CCP#951==0x01代表 Mars  CCP#951==0x02代表 Venus) 默认 Mars
        @param vehicle_mca:    (CCP#962==0x00代表MCA 400v CCP#962==0x02代表MCA 800v)  默认400v
        @param ccp_value: 传入的ccp 值 ，不传则采用默认的值
        @return:
        '''
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def exit_crash(self):
        """
        退出crash
        @param :
        @return:
        """
       
        
    @abstractmethod
    def back_ccp_status_to_Idle(self):
       """
       让ccp状态回idle
       
       :returns
       """
    
    @abstractmethod
    def set_keep_power_by_source_and_check_notify(self, flag:KeepPowerFlag, source: str = "PetMode"):
        """
        由某种模式控制维持上电模式并检查上报的notify通知
        
        :param flag: 控制的类型 
            0 open 
            1 close_服务
            2 close_hvsoc
            3 close_gear
            4 close_carmode
            5 close_fota
            6 close_other
        :param source: 某种模式,默认为宠物模式
        :returns: 
        :raises keyError: 
        """

    @abstractmethod
    def set_ccp(self,ccp_vlaue:dict):
        """
        修改ccp
        @param ccp_vlaue: ccp要修改得值
        """
        
    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def set_control_power_door_precondition(self, doorid:DoorPos, door_status: DoorStatus):
        """
        控制四门Ajar车门运动状态；
        :param doorid:对应侧门
        :param door_status:车门状态
        :return:
        """
        pass

    @abstractmethod
    def check_stop_light_flicker(self, num=3):
        '''
        Check 刹车灯闪烁
        @param num: 检测次数
        '''


    @abstractmethod
    def read_check_e2e_excel(self, excel_path, **kwargs):
        '''
        读取需要校验的e2e的信息表
        根据bgm的版本去匹配使用哪个版本的表

        @param excel_path: 表的路径
        @param kwargs:
        @return:
        '''
    @abstractmethod
    def check_e2e_func(self, data_list, **kwargs):
        '''
        校验e2e 是否正常
        @param data_list:
        @param kwargs:
        @return:
        '''

    @abstractmethod
    def set_open_close_door_precondition(self, doorid:DoorPos, door_status: DoorStatus):
        """
        设置控制电动门开启关闭及当前运动状态校验；
        :param door_status:对应侧门
        :param door_status:车门状态
        :return:
        """
        pass
    
    # @Author:longlong.zhu
    @abstractmethod
    def cycle_write_ccp(self,json_data,v1,v2,bus_name,id):
        """
        循环写入范围内的CCP值:
        :param v1:ccp_id取值范围的最小值 可以取到边界值
        :param v2:ccp_id取值范围的最大值 可以取到边界值
        :param bus_name:总线名称
        :param id:报文id
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def restart_bgm_and_connect_service(self, partner_name, pause_all_bus=True, resume_all_bus=True):
        """
        bgm重启并连接服务
        @param partner_name: 待连接的服务
        @param pause_all_bus: 是否在下电的时候停止总线
        @param resume_all_bus: 是否在上电之后恢复总线
        :return:
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_soc_and_wait_tme_check_keep_power_mode_time(self, soc_value: Union[int, float] = 0, wait_time: Union[int, float] = 0.1, displaytime:DisplayLeftTime=DisplayLeftTime.kUnknown):
        """
        设置指定的soc后等待一段时间校验维持上电模式的显示时间
        @param soc_value: 设置的soc
        @param wait_time: 设置等待的时间
        @param displaytime: 校验的显示时间
        :return:
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def times_set_soc_and_wait_tme_check_keep_power_mode_time(self, soc_sz = [], displaytimesz = []):
        """
        根据数组多次设置指定的soc后等待一段时间校验维持上电模式的显示时间
        @param soc_sz: 要输入的soc数组
        @param displaytimesz: 要校验的显示时间数组
        :return:
        """
        pass
        
    # @Author:liu.yang@jiduatuo.com
    @abstractmethod
    def set_fota_rescue_condition(self, gear: Union[Gear, None], hv_actice_sts: HVActiveSts, display_hv_soc: Union[int, float]):
        """ 
        FOTA Rescue condition:
            1.Gear=ParkIndcn (检查档位档位必须为P挡)
            2.HVActiveSts=Closed (检查当前是否处于上高压状态下)
            3.HVSOCInfo. displaySoc≥23 (检查当前表显大电池是否超过23%)
            
        :param gear: 档位
            class Gear(BaseEnum):
                Park = 0
                Rvs = 1
                Neut = 2
                Drv = 3
                ManMode = 4
                Resd1 = 5
                Resd2 = 6
                Undefd = 7
        :param hv_actice_sts:高压状态
            class HVActiveSts(BaseEnum):
                Open = 0
                Close = 1
                Keep = 2
                Open_And_Req_Act_Dcha = 3
                Auto = 1
        :param display_hv_soc:大电池电量
        :return:
        """

    # @Author:liu.yang@jiduatuo.com
    @abstractmethod
    def diag_not_change_car_mode(self, mode_type: int, do_assert=True, **kwargs):
        """
        检查前置条件不满足时诊断不能切换 carmode
        @param mode_type: 切换的 模式
                    0 : NORMAL
                    1 : TRANSPORT
                    2 : FACTORY
                    3 : CRASH
                    5 : DYNO
        @param do_assert: 若为True 则表示切换失败则会报错，否则返回切换后的模式
        @return:
        """
        
    # @Author:liu.yang@jiduatuo.com
    @abstractmethod
    def set_parkingComfortMode(self, parkingComfortMode: bool=None):
        """
        设置打开\关闭 维持上电模式
        
        @param parkingComfortMode: 是否维持上电模式
        @return:
        """

    # @Author:renyue.dai@jiduatuo.com
    @abstractmethod
    def set_normal_fota_update_condition_new(self, vehspd: Union[int, float], gear: Union[Gear, None], display_hv_soc: Union[int, float], thermaloutofcontrol: bool, 
                                             low_volt_soc: Union[int, float], is_jidu_charger: bool, local_diag_sts: DiagActLineSts, usage_mode: UsageMode, 
                                             is_hw_ver_match: bool, maintenance_mode_sts: bool, park_comfort_mode_sts: bool, pet_mode_sts: str):
        """
        设置FOTA升级前置条件
        
        :@param vehspd: 车速
        :@param gear: 挡位
        :@param display_hv_soc: 高压电池电量
        :@param thermaloutofcontrol: 是否热失控报警
        :@param low_volt_soc: 低压电池电量
        :@param is_jidu_charger: 是否集度充电桩
        :@param local_diag_sts: 是否接入诊断仪
        :@param usage_mode: usagemode值
        :@param is_hw_ver_match: 是否硬件匹配
        :@param maintenance_mode_sts: 维修模式状态
        :@param park_comfort_mode_sts: 维持上电模式状态
        :@param pet_mode_sts: 宠物模式状态
        
        :@return: None
        """
        pass

    @abstractmethod
    def set_wiper_test_before(self,usagemode,carmode,wash_func_sts,maintain_pos,wiper_mode):
        """
        @param usagemode: 使用模式
        @param carmode: 车辆模式
        @param wash_func_sts:雨刮洗涤
        @param maintain_pos:雨刮维修位置
        @param wiper_mode: 雨刮模式
        """
    @abstractmethod
    def check_wipe_safety_monitor_on_500385(self,wipe_mode):
        """
        @param wipe_mode: 雨刮模式
        """
        
    @abstractmethod
    def check_wipe_safety_monitor_off_500385(self,wipe_mode):
        """
        @param wipe_mode: 雨刮模式
        """

    @abstractmethod
    def check_fota_setStartInhibit(self, startInhibit: bool = False):
        """
        检查FOTA设置车辆静止信号

        :param startInhibit: 是否设置车辆静止信号
        :returns:
        :raises keyError: 
        """

    # @Author:xiangyue.li@jiduauto.com        
    @abstractmethod
    def set_rear_defrost_sts(self, sts: bool):
        """
        设置并且检测后除霜状态

        :param sts: 后除霜是否开启
        @return:
        """
        
    # @Author:xiangyue.li@jiduauto.com        
    @abstractmethod
    def set_and_check_findkey_sts(self, sts: bool):
        """
        寻钥匙请求

        :param sts: 寻钥匙请求是否发出
        @return:
        """

    @abstractmethod
    def check_remoteRescue_wakeup_and_Inhibit(self,
                              pnc29: bool = False, 
                              acu_keep_alive: bool = False,
                              up_inactive: bool = False,
                              hv_active: bool = False,
                              startInhibit: bool = False,
                              ):
        """
        remoteRescue手动救援开启或关闭时检测维持唤醒动作或停发唤醒动作
        :param sts:
        @return:
        """

    # @Author:qian.feng@jiduauto.com        
    @abstractmethod
    def set_seat_occpt_sts(self, occupysts: OccupySts,  time_wait = 0):
        """
        设置整车座椅占位状态

        :param occupysts: 占位状态
            NotOccupied = 0
            Occupied = 1
            Invalid = 2
        
        @return:
        """
        
    @abstractmethod
    def update_version_debug_bridge(self, task_id: int, domain_need_flushed_list: list = [{"SWPN": "", "name": "BGM"}, {"SWPN": "", "name": "CDC"}]):
        """
        更新version debug, 过桥FOTA专用

        :param task_id: 过桥taskid
        :param domain_need_flushed_list: version info

        @return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def set_usagemode_inactive_to_convenience(self, set_usagemode_type: set_usagemode_type, check_selftest_flag: bool = False, time1:int = 1, selftest_fail1_flg:bool = False, selftest_fail2_flg:bool = False):
        """
        触发usagemode从inactive上切到convenience
        @param set_usagemode_type: 上切的方式
            service = 0
            open_fl_door = 1
            open_fr_door = 2
            open_rl_door = 3
            open_rr_door = 4
            occupy_drvr_seat = 5
            hit_brake = 6
            app_set_convenience = 7
        @param check_selftest_flag: 是否做自检上切convenience相关的检查
        @param time1: 应用上切convenience的超时时间单位是30s
        @param selftest_fail1_flg: 是否做自检上切active相关的检查
        @param selftest_fail2_flg: 是否做自检下切convenience相关的检查
        @return:
        """
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def wait_time_in_chrgild_req(self, num: int, req: ChrgLidReq):
        """
        检查一定时间内的充电口盖控制请求
        @param num: 单位是0.1s
        @param req: 充电口控制请求
            Idle = 127
            Open = 0
            Close = 100
        @return:
        """

    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def vehicle_sleep(self):
        """
        检查一定时间内整车是否休眠
        """
    
    @abstractmethod
    def kill_s2s_and_reconnect_service(self, partner_key=None):
        """
        kill S2S进程，等待EM2拉起S2S并等待partner重新连接服务
        仅用于SIL环境测试
        @param partner_key: 需要重连的partner_key,如不填则不等待服务连接
        """
    
    @abstractmethod 
    def update_bgm_s2s_json(self, update_info: dict, partner_key=None):
        """
        更新本地s2s.json文件，并同步更新bgm的s2s.json并落盘
        仅用于SIL环境测试
        @param update_info: 更新的字段内容
        @param partner_key: 需要重连的partner_key,如不填则不等待服务连接
        """

    # @Author:qian.feng@jiduauto.com        
    @abstractmethod
    def set_and_get_wash_mode_sts(self, sts: isOn, time_wait = 0):
        """
        设置和校验洗车模式是否开启
        @param sts:洗车模式状态, On or Off
        @param time_wait: 等待时间默认0
        """
        pass
    
    # @Author:qian.feng@jiduauto.com        
    @abstractmethod
    def set_inside_open_door_flag(self, scene: VehicleInsideOutside,  time_wait = 0):
        """
        设置对应侧门发送开启请求及开门方式清除侧方开门flag
        @param scene:开门方式
            VehicleInSide = 0::车内方式
            VehicleOutSide = 1::车外方式
        @param time_wait: 等待时间默认0
        """
        pass

    # @Author:qian.feng@jiduauto.com        
    @abstractmethod
    def set_and_check_door_resist_cmd(self, resist: ResistMode, time_wait: Union[float, int] = 1):
        """
        通过关闭四门撤销开门阻力
        @param resist:撤销开门阻力方式 关门 or 清除侧方开门预警
        @param time_wait: 等待时间默认0
        """
        pass
    @abstractmethod
    def check_upload_log_to_cloud_consistency(self, ecu_name: str = 'bgm', duration: int = 1800):
        """
        检查云端和本地上传日志是否一致
        
        Args:
            ecu_name (str): ECU名称，默认为'bgm'
            duration (int): 日志检查时间范围，单位为秒，默认为3600秒
        
        Returns:
            None
        
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com
    @abstractmethod
    def exit_vehicle_inside_person(self):
        """
        退出车内有人状态
        @param :
        @return:
        """

    @abstractmethod
    def ck_rvc_DefrostHvRunTime(self, start_time:float, ck_time:int):
        """

        检查远控参数配置_RemElecDefrostHvRunTime配置有效性
        @param : start_time : 远控RemElecDefrost开始时间
                 ck_time    : 检查RemElecDefrostHvRunTime的运行时长
        @return:
        """
        pass

    @abstractmethod
    def write_did_and_check(self,ta:int,did:int,session=SESSION.EMPTY,unlock_level=UnLock.L0,write_data='',check_data='',check_length=0,check_range=[],check_in=[],check_method=Check_Method.reset,recover=True):   
        """
        写入值到对应的did

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param did: 要写入值的did
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED
        :param unlock_level: 要解锁的安全等级,sucn as UnLock.L0,UnLock.L1,UnLock.L3,UnLock.L5,UnLock.L7 或者0,1,3,5,7
        :param write_data: 要写入的值
        :param check_data: 预期的返回值，用于检查返回值是否与预期的一致
        :param check_length: 预期的返回值长度，用于检查返回值长度是否与预期的一致
        :param check_range: 预期的返回值范围，用于检查返回值是否在预期范围内
        :param check_in: 预期的返回值内容范围，用于检查返回值内容是否在预期范围内
        :param check_method: 当Check_Method是response时，检查当前诊断指令发送后的返回值是否与预期一致 ； 当Check_Method是method时，当前诊断指令发送后，再发送读取相关的did指令来确认返回值是否与预期一致 ;当Check_Method是method时，当前诊断指令发送后，1181重启再发送读取相关的did指令来确认返回值是否与预期一致
        :param recover: 是否需要恢复写入前的值
        :return: return_result:str
        """
        pass

    # @Author:qian.feng@jiduauto.com        
    @abstractmethod
    def set_lock_and_door_restore_default(self, anti_pinch: Union[bool, None] = None, 
                                          door_opener: Union[DoorOpenerSts, None] = None,
                                          engine: Union[EngSt1WdStsEngSt1WdSts, None] = None,
                                          door_sts: Union[Door, None] = None):
        """
        需要恢复的仿真信号
        :param anti_pinch: 防夹状态
        :param door_opener: 四门运动状态
        :param engine: 发动机状态
        :param door_sts: 四门Ajar状态
        :return: return_result:str
        """
        pass

    @abstractmethod
    def whether_auto_creat_task(self, ecu, vin):
        """
        是否自动创建任务
        
        :param ecu: ecu配置
        :param vin: vin号
        :returns: bool, taskid
        :raises keyError: NA
        """

    @abstractmethod
    def check_wiper_maintenance_mode_signal(self,status="deactive"):
        """
        检查雨刮维修模式设置后，信号状态
        
        :param status: "deactive"为维修未激活 or "active"为维修已激活
        """

    @abstractmethod
    def get_bus_send_recv_info(self, channel_name: str, **kwargs):
        '''
         根据通道获取当前通道的，发送节点和接收节点的数据
         @param channel_name: 通道   bodycan 等等
         @param kwargs:
         @return: {}
        {
             "发送节点": {
                 "周期发送": {
                     "BGM": [ {"msg_name": msg_name,
                             "msg_id": msg_id,
                             "msg_type": msg_type,
                             "msg_tx_method": msg_tx_method,
                             "msg_cycle": msg_cycle,
                             "msg_length": msg_length,
                             "rx_nodes": rx_nodes,
                             "tx_node": tx_node,
                             "msg_base_cycle": msg_base_cycle,
                             "msg_repetition": msg_repetition}, {}],
                     "CCD": [{}, {}],
                 },
                 "非周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
             },
             "接收节点": {
                 "周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
                 "非周期发送": {
                     "BGM": [{}, {}],
                     "CCD": [{}, {}],
                 },
             },

         }
        '''
        pass
        
    @abstractmethod
    def get_bus_send_msg_info(
        self,
        data_dic,
        send_nodes=None,
        send_type="cyclic",
    ):
        '''

        获取 当前bus通道， send_nodes 节点 send_type 发送数据；区分bgm 发送和 非bgm 发送

        @param data_dic: 根据bus 处理得到的数据  只是单个 bus
        @param send_nodes: 如果 send_nodes 为None 表示所有节点,除去bgm的 所有节点
        @param send_type:  cyclic  ，spontaneous
        @return: 非bgm 发送 列表，bgm发送的数据 列表
         [ {"msg_name": msg_name,
                "msg_id": msg_id,
                "msg_type": msg_type,
                "msg_tx_method": msg_tx_method,
                "msg_cycle": msg_cycle,
                "msg_length": msg_length,
                "rx_nodes": [BGM,.],
                "tx_node": tx_node,
                "msg_base_cycle": msg_base_cycle,
                "msg_repetition": msg_repetition
                    },
                    {
                    ....
                    }
                ]
            ，
         [{}，{}]
        '''
        pass
        
    @abstractmethod
    def parse_one_eth_packet(self, data_info_string, packet_index, time_string):
        '''
        解析 一条 eth 报文的数据
        UDP Payload格式： 总线编号+报文ID+ 毫秒时间戳 +报文长度 Data…总线编号 + 报文ID + 毫秒时间戳+ 报文长度+ Data… 结束符（0xFE）
        @param data_info_string: cdd打包的数据
        @param packet_index: UDP包的索引
        @param time_string: cdd打包全局时间
        @return:
        '''
        pass
        
    @abstractmethod
    def parse_pdu_msg(self, file_path, **kwargs):
        '''
        参考文档
        https://jama.jiduauto.com/perspective.req#/items/228479?projectId=46

        解析pud 的报文
        :param file_path: pcap 包路径
        :return:  packet_list ,packet_list
        data_list=[{所在pcap 包的行数(int),通道名字（str）,报文id（int），毫秒时间（int），报文长度（int），报文内容（str），
                     base_cycle（针对fr，can lin 为None）,repetition（针对fr，can lin 为None）}]
        packet_list=[{所在pcap 包的行数(int)，payload的 长度(int) ，结束符号(str),时间戳 （float）}]

        '''
        pass
        
    @abstractmethod
    def get_bus_msgid_info(self, channel_name: str, **kwargs):
        '''
        根据通道获取当前通道的，发送节点和接收节点的数据
        @param channel_name: 通道   bodycan 等等
        @param kwargs:
        @return: {}

        '''
        pass
    @abstractmethod
    def start_mock_cdc_wifi(self):
        """
        启动模拟的CDC WiFi。
        
        Args:
            无
        
        Returns:
            无
        
        """
        pass        
           
    @abstractmethod
    def stop_mock_cdc_wifi(self):
        """
        停止模拟CDC Wi-Fi。
        
        Args:
            无
        
        Returns:
            无
        
        """
        pass

    # @Author:qian.feng@jiduatuo.com
    @abstractmethod
    def restore_poweroutlet_relay_simulation_environment(self):
        '''
        12v电源继电器case结束后, 恢复诊断激活线连接状态, 关闭五门
        @return: 
        '''
        pass

    @abstractmethod
    def network_sleep_unlock(self):
        """
        不闭锁、开门休眠
        @return:
        """
        pass


    @abstractmethod
    def set_door_and_seat_status(self,motion_state,seat_status,door_status):
        '''
        设置门状态和座椅状态
        @param motion_state: 车辆运动状态
        @param seat_status:  座椅状态
        @param door_status:  门状态

        '''
        pass

    @abstractmethod
    def set_wiper_mode_and_get_wiper_mode(self,mode):
        '''
        设置雨刮模式，并获取雨刮模式
        @param motion_state: 雨刮模式
        pass
        '''

    @abstractmethod
    def check_wiper_maintanance_signal(self,status):
        '''
        检查雨刮维修激活或退出时，信号状态
        @param status: active 激活 or deactive 退出
        pass
        '''