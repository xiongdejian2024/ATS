#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :tsp.py

@Time         :2023/10/31 10:00

@Author       :quan.sun@jiduauto.com

@Description  :云端能力模拟 抽象接口
"""
from abc import abstractmethod, ABCMeta

from typing import Union

from xat_ecu.api.constants.common import *


class AbcTsp(metaclass=ABCMeta):
    def trigger_vsp_fota(self, vsp_operation: VSP, task_id: int):
        """
        云端任务常规操作
        
        :param vsp_operation: 枚举类型 class VSP_OPERATION(BaseEnum): Repub = 0 Cancel = 1  Reset = 2
        :param task_id: 车辆taskid
        :returns: None
        :raises keyError: None
        """

    def rvs_event_check(self, block:BlockName, keys:list, target_value:str, index:int = 0, timeout:Union[int,float]=10):
        """
        Check RVS数据上报结果
        :param block: 功能块
            VehicleMode = 10102
            VehicleBody = 10103
            CabinStatus = 10104
            GISAndTravel = 10105
            DrivingStatus = 10106
            EicCharging = 10107
            WTIService = 10701
            WTIAutoDriveService = 10702
            BusStatus = 10109
            DeviceInfo = 10110
            EOLData = 10111
            Light = 10112
            APA = 19001
        :param keys:需要匹配的关键字，list
        :param target_value:期望得到的值
        :param index:参数位置
        :param timeout:最长查询时间，默认10s
        :returns: None
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def set_bench_config(self, vid, tel):
        """
        设置台架vid和tel

        :param vid: 台架vid, 字符串
        :param tel: 台架绑定的电话号码，字符串
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def get_token(self):
        """
        获取远控操作token

        :return: 返回token内容
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def cmd_to_pb(self, data):
        """
        将远控指令消息body加签名并转成protobuf序列化处理

        :param data: 远控指令消息body，字典类型
        :return: 序列化后的字节数组
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def send_rvc_cmd(self, pb_data):
        """
        通过TSP下发远控指令

        :param pb_data: 远控指令protobuf序列化字节数组
        :return: 
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_lock_control(self, op: int = 2):
        """
        通过TSP下远控解闭锁请求,op:1: 解锁, 2:闭锁, 3: 关门+闭锁

        :param op: 解闭锁操作类型，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_find_vehicle(self, op: int = 1):
        """
        通过TSP下远控寻车,op:(-1,关闭;1,鸣笛闪灯;2,仅闪灯)

        :param op: 寻车操作类型，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_window_control(self, win_fl: int = 100, win_fr: int = 100, win_rl: int = 100, win_rr: int = 100):
        """
        通过TSP下远控车窗请求, op:(-1,关闭;1,鸣笛闪灯;2,仅闪灯)

        :param win_fl: 左前车窗开度值，整形
        :param win_fr: 右前车窗开度值，整形
        :param win_rl: 左后车窗开度值，整形
        :param win_rr: 右后车窗开度值，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_tailgate_control(self, op: int = -1, position: int = 0):
        """
        通过TSP下远控尾门请求,op:动作(-1: 关, 1:开)

        :param op: 远控尾门操作类型，整形
        :param position:
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_charge_soc_settings(self, max_soc: int = 1000):
        """
        通过TSP下发充电设置请求，千分比(50.0%-100.0%,默认85.0%)如870为87%

        :param max_soc: 远控设置充电SOC上限，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:taiping.zong@jiduatuo.com
    def rvc_rear_view_control(self, op: int = 1):
        """
        op后视镜状态(1展开, -1折叠)
        
        Args:
            op (int, optional): 后视镜状态，1表示展开，-1表示折叠。默认为1。
        
        Returns:
            str: 执行ID
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_ac_control(self, op: int = 1, temp: int = 220):
        """
        通过TSP下发空调请求, op(1: 开，-1: 关), temp: 220 //int 温度(16~28, 默认 220)

        :param op: 远控设开启关闭开启空调操作类型，整形
        :param temp: 设置空调温度值，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:taiping.zong@jiduatuo.com
    def rvc_cold_down(self, op: int = 1):
        """
        通过TSP下发极速制冷请求, op(1: 开，-1: 关)

        :param op: 远控设开启关闭空调极速制冷操作类型，整形
        :return: exec_id,执行ID,字符串
        """
        pass

    # @Author:taiping.zong@jiduatuo.com
    def rvc_heat_up(self, op: int = 1):
        """
        通过TSP下发极速制热请求, op(1: 开，-1: 关)

        :param op: 远控设开启关闭空调极速制热操作类型，整形
        :return: exec_id,执行ID,字符串
        """
        pass

    def check_error_rvc_lock_control(self):
        """
        远控接闭锁请求,op:1: 解锁, 2:闭锁, 3: 关门+闭锁(单域tcam错误的vid环境检查使用)
        """

    def check_rvc_lock_control(self):
        """
        远控接闭锁请求,op:1: 解锁, 2:闭锁, 3: 关门+闭锁 (单域tcam环境检查使用)
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_driver_seat_heat(self, level: int = 2):
        """
        通过TSP下主驾加热,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)

        :param level: 远控下发主驾座椅加热等级，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_passenger_seat_heat(self, level: int = 2):
        """
        通过TSP下副驾加热,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)

        :param level: 远控下发副驾座椅加热等级，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    def rvc_rearleft_seat_heat(self, level: int = 2):
        """
        通过TSP下发左后座椅加热,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)

        :param level: 远控下发左后座椅加热等级，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_rearright_seat_heat(self, level: int = 2):
        """
        通过TSP下右后座椅加热,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)

        :param level: 远控下发右后座椅加热等级，整形
        :return: exec_id，执行ID，字符串
        """
        pass


    # @Author:taiping.zong@jiduatuo.com
    def rvc_driver_seat_vent(self, level: int = 2):
        """
        通过TSP下主驾座椅通风,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)

        :param level: 远控下发主驾座椅加热等级，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:taiping.zong@jiduatuo.com
    def rvc_passenger_seat_vent(self, level: int = 2):
        """
        通过TSP下副驾座椅通风,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)

        :param level: 远控下发主驾座椅加热等级，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:taiping.zong@jiduatuo.com
    def rvc_rear_left_seat_vent(self, level: int = 2):
        """
        通过TSP下左后座椅通风,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)

        :param level: 远控下发主驾座椅加热等级，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:taiping.zong@jiduatuo.com
    def rvc_rear_right_seat_vent(self, level: int = 2):
        """
        通过TSP下右后座椅通风,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)

        :param level: 远控下发主驾座椅加热等级，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_steering_wheel_heat(self, level: int = 2):
        """
        通过TSP下发方向盘加热等级(1档,2......)

        :param level: 远控下发方向盘加热等级，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_charge_operation(self, op: int = -1):
        """
        通过TSP下发充电开关(1: 开始，-1: 结束).  注: 当前只有-1生效

        :param op: 充电操作类型，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_charge_Lidgate(self, op: int = 1):
        """
        通过TSP下发充电口盖指令(1: 开，-1: 关)

        :param op: 充电口盖操作类型，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_defrost_control(self, op: int = 1):
        """
        通过TSP下发除霜开关(-1关,1开)

        :param op: 除霜操作类型，整形
        :return: exec_id，执行ID，字符串
        """
        pass
    
    @abstractmethod
    def rvc_maintainpower_control(self, op: int = 1):
        """
        通过TSP下发维持上电开关(-1关)
        当前只能远控关闭维持上电
        :param op: 维持上电操作类型，整形
        :return: exec_id，执行ID，字符串
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def log_search(self, keywords: str = "Success"):
        """
        远程控制执行过程中及执行结果上报到车云的执行状态

        :param keywords : keywords为校验车云结果的关键字,例如 Success,Sysbusy,StartOK.....
        :return:
        """
        pass

    # @Author:yulin.hu@jiduatuo.com 
    def rvc_taskCmd(self,fixed=False,appointment_hour=0,appointment_minute=30,appointWeekday="0000000", cyclesType=1,ac=1,temp=230,driver_level=1,passenger_level=1, RearLeft_level=-1, RearRight_level=-1, steering_level=1,DriverVent_level=-1,PassengerVent_level=-1,RearLeftVent_level=-1,RearRightVent_level=-1):
        """
        远程座舱预约,自动预约当前时间00分钟后的预约任务,时间可以根据需要调整
        :params  fixed bool:                根据 'true or false' 进行座舱预约上车时间计算
        :params  appointment_hour int:      预约上车时间, 设置预约时间为每天的指定时间
        :params  appointment_minute int:    预约上车时间, 默认当前时间后30分钟上车,例如预约空调、座椅加热立即执行,appointment_minute可以设置15分钟
        :params  appointWeekday int:       设置一周的周几执行, appointWeekday="1000000": 为每周一执行
        :params  ac   int:                  设置空调开关,默认1为开, -1为关
        :params  temp int:                  设置空调温度,例如设置23°C,就是230
        :params  driver_level int:          主驾加热挡位默认1,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  passenger_level int:       副驾加热挡位默认1,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  RearLeft_level int:        后左座椅加热挡位默认-1,level(ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  RearRight_level int:       后右座椅加热挡位默认-1,level(ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  steering_level int :       方向盘加热等级默认1,1档,2......
        :params  DriverVent_level int:      主驾通风挡位默认-1,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  PassengerVent_level int:   副驾通风挡位默认-1,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  RearLeftVent_level int:    后左驾通风挡位默认-1,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  RearRightVent_level int:   后右驾通风挡位默认-1,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :params  cyclesType int:            为预约循环设置,SctUnknown=0;//空挡
                                                SctOnce= 1;//一次 
                                                SctDaily= 2;//每日 
                                                SctWorkDay=3;//工作日 
                                                SctweekDay= 4; // 周一到周日可选                                
        """
        pass

    
    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod
    def log_appointment_search(self, keywords: str = "Success"):
        """
        远程座舱预约TCAM上报到车云的预约结果查询

        :param keywords: str  keywords为校验车云结果的关键字,例如:Success
        :return:
        """

    # @Author:yulin.hu@jiduatuo.com
    @abstractmethod    
    def log_SubscribeTaskResp_search(self, fuzz_match: str, detail: str, keywords: str ):
        """
        远程座舱预约执行过程中TCAM上报到车云的执行结果查询
        :params str : fuzz_match为校验车云结果的模糊词,例如：SubscribeTask|SubscribeTaskResp finsh、SubscribeTask|SubscribeTaskExecUpload finsh
        :params str : detail为校验车云结果的准确词，例如：code:1、cmdResp=execId
        :params str : keywords为校验车云结果的关键字,例如:CarModeFail、SOCLow、ChargingOngoing、ParkFail 、MntnMode、UsageModeFail
                                                   
        """
        pass   

    @abstractmethod
    def log_SubscribeTaskUpload_search(self, fuzz_match: str , detail: str, keywords: str):
        """
        远程座舱预约执行过程中TCAM上报预约任务查询
        :params fuzz_match : fuzz_match为校验预约任务的模糊词,例如：SubscribeTask|SubscribeTaskUpload finsh
        :params detail     : detail为校验预约任务的准确词，例如：taskDetail
        :params keywords   : keywords为校验预约任务的关键字,例如:useVehicleTime
           
        """
        pass
    
    @abstractmethod
    def cancel_cock_reserv_task(self, task_time: str, appointWeekday="0000000",cyclesType=1,temp=230,driver_level=1,passenger_level=1,steering_level=1):
        """
        取消远程座舱预约
        :param  task_time: int         座舱预约上车时间
        :param  ac:   int              设置空调开关,默认1为开，-1为关
        :param  temp: int              设置空调温度,例如设置23°C,就是230
        :param  driver_level: int      主驾加热挡位默认1,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :param  passenger_level: int   副驾加热默认1,level(ShNeutral:0空挡;ShClose:-1关;ShLevel1:1档;ShLevel2:2档;ShLevel3:3档)"
        :param  steering_level: int    方向盘加热等级默认1,1档,2......
        :param  cyclesType:  int       为预约循环设置,SctUnknown=0;//空挡、SctOnce= 1;//一次 、ctDaily= 2;//每日、SctWorkDay=3;//工作日、SctweekDay= 4; // 周一到周日可选
        :return:
        """
        pass

    @abstractmethod
    def get_rvc_appoint_taskID(self):
        """
        获取远控座舱预约任务ID

        :return: 当前预约任务的taskid
        """
        pass

    @abstractmethod
    def get_task_name(self, task_id: int):
        """
        获取当前taskid的VSP任务名

        :params task_id: 任务id
        :return: 当前taskid的VSP任务名
        """


    @abstractmethod
    def get_vsp_fota_status(self, task_id: int):
        """
        获取当前taskid的VSP Status
        :params task_id : 任务id
        :return: 当前taskid的VSP Status                                         
        """

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def rvc_remote_authorization(self, op: int = 1):
        """
        通过TSP下发远程授权启动指令
        :params op : 操作类型，int，1为开启远程授权启动
        :return:                                     
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def get_gb32960data_direct(self, vin: str, start_time: str, end_time: str, data_type: str, cycle_time: int = 10):
        """
        获取GB32960直连平台指定时间区间内数据上报情况
        :param vin: 车辆编码，字符串类型，固定17位，大写字母和数字组成
        :param start_time: 查询开始时间，字符串类型，格式为 2024-01-16 11:00:00
        :param end_time: 查询结束时间，字符串类型，格式为 2024-01-16 11:00:00
        :param data_type: 查询上报类型，字符串，中文字符，取值范围["实时信息上报", "补发信息上报"]
        :param cycle_time: 上报周期，整形，单位s
        """
        pass

    # @Author:Liangliang.chen
    @abstractmethod
    def check_gb_data_cycle(self, gb_data_list:list, start_time, end_time, data_type: str, cycle_time: int = 10):
        """
        :param gb_data_list: 查询到的国标数据列表
        :param start_time: 查询开始时间，格式为 2024-01-16 11:00:00 | time.time()
        :param end_time: 查询结束时间，格式为 2024-01-16 11:00:00 | time.time()
        :param data_type: 查询上报类型，字符串，中文字符，取值范围["实时信息上报", "补发信息上报"]
        :param cycle_time: 上报周期，整形，单位s
        
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def get_gb32960data_direct_alarm_level3(self, vin:str, alarm_trigger_time: int):
        """
        获取GB32960直连平台三级报警数据上报情况
        :param vin: 车辆编码，字符串类型，固定17位，大写字母和数字组成
        :param alarm_trigger_time: 三级报警触发时间，整型，秒级时间戳
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def get_gb32960data_forward(self, vin: str = "LSTEST6R9F2086644"):
        """
        获取GB32960转发平台数据上报情况
        :param vin: 车辆编码，字符串类型，固定17位，大写字母和数字组成
        :return:
        """
        pass

    @abstractmethod
    def trigger_update_by_real_app(self, vid: str = None, tel: str = None):
        """
        触发真实的APP下发 “立即升级” 指令
        
        :param vid: 车辆vid, 选填, 默认为bench config里的配置
        :param tel: 车主手机号, 选填, 默认为bench config里的配置
        :returns: 触发message
        :raises keyError: NA
        """
        
    @abstractmethod
    def get_userid(self, tel: str = None):
        """
        根据车主手机号 获取userid
        
        :param tel: 车主手机号, 选填, 默认为bench config里的配置
        :returns: userid
        :raises keyError: NA
        """
    
    @abstractmethod
    def mno_setAPNsts(self, APN4sts: int=1, iccid="89860808092390000036"):
        """
        仅限蜂窝测试实名使用，其他勿调用此接口
        通过MNO平台提供模拟APN4开关状态下发的接口，实现云端开关APN4，默认apn4状态为开
        :param APN4sts： APN4sts: int
                        0  关
                        1  开
        :param iccid:  tcam iccid   
        :return       
        """
        pass
    
    @abstractmethod
    def mno_log_search(self, search_time: int=20, fuzz_match="由调用网关成功更新状态为", detail= "lambda$mqttCallback", keywords: str = "车端处理成功"):
        """
        mno平台apn4状态查询
        :params serach_time : search_time为查询多少秒之前的云端结果 
        :params fuzz_match  : fuzz_match为校验预约任务的模糊词,例如："由调用网关成功更新状态为"
        :params detail      : detail为校验预约任务的准确词，例如："lambda$mqttCallback"
        :params keywords    : keywords为校验预约任务的关键字,例如:"车端处理成功"
           
        """
        pass

    @abstractmethod  
    def send_remote_diag_cmd(self, cmd_type: CmdType, session_time_out=300, check_intervel=3):
        """
        发送远程诊断指令
        :params cmd_type : 远程诊断指令类型 CmdType: str
                        SessionOpen  打开会话
                        SessionClose  关闭会话
                        SendDiagCmd  执行诊断命令
        :params session_time_out  : 会话超时时间，当且仅当cmd_type=SessionOpen时生效
        :params check_intervel  : 条件检测周期，当且仅当cmd_type=SessionOpen时生效
        :return       
        """
        pass

    @abstractmethod  
    def get_remote_diag_token(self):
        """
        获取远程诊断token并写入config/remote_diag_lua.yaml文件，该token用于远程诊断接口身份认证
        :return
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def get_rvs_data(self,block_id: str, rvs_db="jidulogapp-staging-vidb-report-data", retry_count=5):
        """
        根据查询条件查询rvs数据，数据类型列表，列表中的数据为字符串

        @param condition： 查询条件列表
        @param rvs_db: 查询数据库
        @param retry_count：查询失败最多重试次数
        """

    @abstractmethod
    def trigger_remote_rescue(self, rescue_type: RescueType):
        """
        下发远程救援指令
        :params cmd_type : 远程诊断指令类型 rescue_type: int
                        OpenInhibit  ——  200 维持不可开车，
                        CloseInhibit  ——  210 取消维持不可开车，
                        ResetDomain  ——  220 四域重启
        :return
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_rvs_data_update(self, block: BlockName, keys: list, target_value: str, index: int = 0,
                        timeout: Union[int, float] = 10):
        """
        Check RVS数据上报结果
        :param block: 功能块
            VehicleMode = 10102
            VehicleBody = 10103
            CabinStatus = 10104
            GISAndTravel = 10105
            DrivingStatus = 10106
            EicCharging = 10107
            WTIService = 10701
            WTIAutoDriveService = 10702
            BusStatus = 10109
            DeviceInfo = 10110
            EOLData = 10111
            Light = 10112
            APA = 19001
        :param keys:需要匹配的关键字，list
        :param target_value:期望得到的值
        :param index:参数位置
        :param timeout:最长查询时间，默认10s
        :returns: None
        """
    
    @abstractmethod
    def trigger_fod_task(self, FodConfig):
        """
        仅限staging环境FOD功能测试使用,其他勿调用此接口
        :param FodConfig 云端接口所需参数
 
        :return  云端接口调用返回信息     
        """
        pass
    

    def rvs_log_wakeup(self, vid: str = '', ecus: str = 'bgm'):
        """
        触发远程上报日志请求
        :param vid: 设备VID 默认
        :param ecus: bgm, tcam等
        :return:
        """
        pass    
    def check_rvs_data_update_new(self, block: BlockName, keys: list, target_value, timeout: Union[int, float] = 10):
        """
        Check RVS数据上报结果
        :param block: 功能块
            VehicleMode = 10102
            VehicleBody = 10103
            CabinStatus = 10104
            GISAndTravel = 10105
            DrivingStatus = 10106
            EicCharging = 10107
            WTIService = 10701
            WTIAutoDriveService = 10702
            BusStatus = 10109
            DeviceInfo = 10110
            EOLData = 10111
            Light = 10112
            APA = 19001
        :param keys:需要匹配的关键字，list
        :param target_value:期望得到的值
        :param timeout:最长查询时间，默认10s
        :returns: None
        """
        pass

    def get_rvs_data_new(self, block_id:str='10105',timeout: Union[int, float] = 5):
        """
        根据查询条件查询rvs数据，数据类型列表，列表中的数据为字符串
        @param block_id： 功能块
        """
        pass

    def log_search_result(self,vid:str=None,service_name:str = 'remote-vehicle-control', term_query_level:str='INFO',fuzzy_query: list = [],begin_time: int=0,end_time: int=None,size: int=10,interval_time:int =1, num:int=15):
        """
        基础查询,将查询的结果格式化后返回
        data = {
            "index": f"jidulogapp-staging-{service_name}-serverlog",
            "service_name": service_name,
            "term_query": {"level": term_query_level},
            "fuzzy_query": [f"vid:{vid}"] + fuzzy_query,
            "begin": int(begin_time),
            "end": int(end_time) if end_time else int(begin_time + num),
            "from": 0,
            "size": size
        }
        """
        pass

    def find_value(self, data, expression_list):
        """
        在给定数据中查找与表达式列表匹配的值。
        
        Args:
            data (dict): 包含需要搜索的数据的字典对象。
            expression_list (list): 包含多个表达式的列表，每个表达式都是一个字符串。
        
        Returns:
            list: 返回一个列表，包含与表达式列表中任意表达式匹配的所有值。
        
        """
        pass

    def log_search_remote_vehicle_control(self,keywords: str = "Success", execid:str="", begin_time: int = None, num: int = 25, exectype_num: int=1):
        """
        及时查询remote-vehicle-control服务的log日志
        查询开始时间为调用该方法时间，查询开始时间为调用时间 -1 秒
        结束时间为最大延迟时间。(默认为25s)
        :param execid: 查询指令id
        :param keywords: 查询的关键字
        :param begin_time: 查询开始时间
        :param end_time: 查询结束时间
        :param end_time: 间隔
        :param exectype_num: exectype=3的个数
        :return:
        """
        pass

    def check_async_log_search_result_from_remote_vehicle_control(self,keywords: str = "Success", execid:str="", begin_time: int = None, num: int = 25,flage: int = 0):
        """
        异步查询方法,用来实现多步查询
        :param keywords: 查询的关键字
        :param begin_time: 查询开始时间
        :param end_time: 查询结束时间
        :param flage: (0,1,2)  0: 第一次调用此方法，开始记录
                               1: 中间调用此异步方法
                               2: 最后一次调用此方法
        :return:
        """
        pass

    # @abstractmethod
    # def get_tcam_state_by_cloud(self, vid: str=None) -> str:
    #     """
    #     从赛博坦平台上获取TCAM的电源状态
    #     :param vid: 车辆唯一标识
    #     """
    #     pass


    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def get_tcam_power_status(self):
        """
        获取TCAM电源状态
        Args:
            无
        
        Returns:
            dict: 包含TCAM电源状态信息的字典
        """
        pass

    # @Author:lei.song@jiduatuo.com
    @abstractmethod
    def get_tcam_network_status(self):
        """
        获取TCAM网络状态        
        Args:
            无
        
        Returns:
            dict: 包含网络状态信息的字典
        
        """
        pass
    
    @abstractmethod
    def buried_point_data_query(self, dt: str=None, hour: str=None, signalname: str=None, httpheadervid: str=None, sigvalue: str=None, timeout: int=200, wait_interval: int=3):
        """
        查询https://dataworks.jiduprod.com/uddp/dataDev平台埋点数据
        
        Args:
            self (object): 类实例对象
            dt (str): 日期,格式为2024-05-22,不填则为当天日期
            hour (str): 小时格式为HH,不填则为当前小时
            signalname (str): 信号名称，必填
            httpheadervid (str): vid值,不填则为当前车辆vid
            sigvalue (Any): 信号值，根据信号类型而定,必填
            timeout (int, optional): 日志查询超时时间,默认200s
            wait_interval (int, optional): 查询间隔,单位为秒,默认为3秒。
        
        """
        pass

    # @Author:taiping.zong@jiduatuo.com
    @abstractmethod
    def cmd_to_ready(self, data):
        """
        一键备车内部接口, 发送到TSP端, 要求一键备车的下发的任务内容
        :param data: 一键备车的内容
                    data = {
                        "vid": self.vid,
                        "execId": exec_id,
                        "userConf":{
                        "switch":"true",
                        "selectedLoc": selectedLoc,
                        "temp": temp
                        }
        }
        """
        pass

    # @Author:taiping.zong@jiduatuo.com
    @abstractmethod
    def rvc_one_click_smart_cockpit_1(self, selectedLoc: list = [1,2,3,4,5], temp: int = 220):
        """
        一键备车内部接口, 写入对象
        :param selectedLoc: list类型, 1:主驾座椅、2:副驾座椅、3:后排左座椅、4:后排右座椅、5:方向盘加热、
        :param temp:空调目标温度需要*10
        """
        pass

    # @Author:taiping.zong@jiduatuo.com
    @abstractmethod
    def rvc_one_click_smart_cockpit_3(self, selectedLoc: list = [1,2,3,4,5,6], temp: int = 220, acAutoType: int = 2):
        """
        一键备车内部接口, 写入对象
        :param selectedLoc: list类型, 1:主驾座椅、2:副驾座椅、3:后排左座椅、4:后排右座椅、5:方向盘加热、6:电池加热、
        :param temp:空调目标温度需要*10
        :param acAutoType:自动空调类型,1:远控空调、2:自动空调
        """
        pass

    # @Author:taiping.zong@jiduatuo.com
    @abstractmethod
    def rvc_one_click_smart_cockpit_2(self, op: int = 1):
        """
        从TSP下发一键备车指令
        :param  op: 1:开启一键备车
        """
        pass
    
    @abstractmethod
    def create_vsp_task(self, vin,
                              target_soft_id, 
                              skip_ecu, 
                              task_name
                              ):
        """
        创建VSP任务, 一般是创建压测任务才会用
        :param vin: 车辆vin号
        :param target_soft_id: 软件包id
        :param skip_ecu: 需要跳过升级的ecu
        :param task_name: 任务名称
        """
        pass
    
    @abstractmethod
    def get_bgm_version_from_soft_detail(self, soft_id):
        """
        从整车软件中拿bgm版本
        :param soft_id: 软件包id
        :return bgm_bridge_version
        """
        pass
    
    @abstractmethod
    def get_softid_from_taskid(self, task_id):
        """
        从taskid中拿soft_id
        :param task_id: 任务id
        :return soft_id
        """
        pass
    
    @abstractmethod
    def get_domain_version_from_softid(self, soft_id, domain_name: DOMAIN):
        """
        从soft_id中拿指定域控的版本
        :param soft_id: 任务id
        :param 枚举类型 DOMAIN:
            class DOMAIN(BaseEnum):
                BGM = 0
                TCAM = 1
                CDC = 2
                ACU = 3
        :return domain version
        """
        pass
    
    @abstractmethod
    def back_vsp_to_Idle(self, vin: str = None):
        """
        令该vin的历史task id消费结束, 方便触发下次任务
        :param vin: 车辆vin
        
        :return 
        """
        pass

    @abstractmethod
    def get_signal_mining_data(self, table_name="ods.ods_data_jade_ee_signal_qa_staging_h", dt=None, hour=None, vid=None, 
                               limit=100000, timeout: int = 600, wait_interval: int = 3):
        """
        获取信号挖掘数据。
        
        Args:
            table_name (str, optional): 数据表名，默认为 "ods.ods_data_jade_ee_signal_qa_staging_h"。
            dt (str, optional): 日期，格式为 "YYYY-MM-DD"，默认为当前日期。
            hour (str, optional): 小时，格式为 "HH"，默认为当前小时。
            vid (str, optional): 台架vid，默认为类的vid属性。
            limit (int, optional): 查询数据条数限制，默认为 100000。
            timeout (int, optional): 查询超时时间（秒），默认为 600 秒。
            wait_interval (int, optional): 查询等待间隔（秒），默认为 3 秒。
        
        Returns:
            str: 下载的文件名，如果获取数据失败则返回 None。
        
        Raises:
            AssertionError: 当日志查询操作超时时抛出异常。
        """
        pass
    @abstractmethod
    def validate_signal_mining_data(self, vid: str = None, signame: str = None, sigvalue: str = None, message_id: str = None, 
                                    timestamp: float = None, csv_file: str = None):
        """
        验证信号挖掘数据是否匹配给定条件。
        
        Args:
            vid (str, optional): 台架vid. 默认为None.
            signame (str, optional): 信号名称. 默认为None.
            sigvalue (str, optional): 信号值. 默认为None.
            message_id (str, optional): 消息ID. 默认为None.
            timestamp (float, optional): 时间戳. 默认为None.
            csv_file (str): CSV文件名.
        
        Returns:
            bool: 如果在CSV文件中找到匹配项且时间戳相差在5秒内，则返回True，否则返回False.
        
        """
        pass
    
    @abstractmethod
    def check_task_existence(self, vin: str, soft_id: int):
        """
        检查当前vin是否存在以soft id为目标版本的任务存在
        :param soft_id: 软件id
        :param vin: 车辆vin
        :return: bool
        """
        pass
    
    @abstractmethod
    def get_vehicleSoftNumberAndVersion_from_softid(self, soft_id: int):
        """
        从softid中拿整车软件号, 例: 6100000200COG
        :param soft_id: 软件id
        :return: bool
        """
        pass
    
    @abstractmethod
    def get_target_version_from_softid(self, soft_id: int, ecu_name: str):
        """
        从softid中拿整车软件号、dis_baseline和ecu版本
        :param soft_id: 软件id
        :param ecu_name: ecu_name
        :return: tuple (target_baseline, target_dis_baseline, ecu_version)
        """
        pass
    
    @abstractmethod
    def is_task_consuming(self, task_id: int, vin: str):
        """
        判断当前任务是否正在消费
        :param task_id: 任务id
        :param vin: 车辆vin
        :return: bool
        """
        pass
    
    @abstractmethod
    def rvc_realtime_battery_heat(self, op: int = 1):
        """
        "远控电池包立即加热 (-1: 关, 1: 开)"
        :param op: (-1: 关, 1: 开)
        :return: execid
        """
        pass

    @abstractmethod
    def log_search_wti(self,wtiKey:str='ANP Risk Reminder',wtiFlag:str='1',num:int=25):
        """
        "查询WTI上传ES平台的接口"
        :param wtiKey: 
        :param wtiFlag: 
        :return: bool
        """
        pass

    @abstractmethod
    def log_search_battery(self, execid:str, keyword: str = "Success", num: int = 25):
        """
        "查询预约充电的结果"
        :param execid: 指令ID，下发任务时获取到的
        :param keyword: 指令执行结果关键字
        :param num: 查询超时次数
        :return: bool
        """
        pass

    @abstractmethod
    def get_subscribeId(self, execid:str, begin_time: str):
        """
        "查询预约指令对应的subscribeId"
        :param execid: 指令ID，下发任务时获取到的
        :param begin_time: 查询开始时间
        :return: subscribeId
        """
        pass
    @abstractmethod
    def uplaod_log_search_result(self,vid:str=None,index = 'jidulogapp-staging-*-serverlog', term_query_level:str='INFO',fuzzy_query: list = [],begin_time: int=0,end_time: int=0,size: int=10,interval_time:int =1, num:int=15, timeout:int=300):
        """
        上传日志搜索结果的函数
        
        Args:
            vid (str, optional): 默认为None.
            index (str, optional): 日志索引名称，默认为'jidulogapp-staging-*-serverlog'.
            term_query_level (str, optional): 日志级别，默认为'INFO'.
            fuzzy_query (list, optional): 模糊查询的关键词列表，默认为空列表.
            begin_time (int, optional): 查询开始时间，单位为秒，默认为0.
            end_time (int, optional): 查询结束时间，单位为秒，默认为0.
            size (int, optional): 返回结果的大小，默认为10.
            interval_time (int, optional): 查询的时间间隔，单位为秒，默认为1.
            num (int, optional): 查询的日志数量，默认为15.
        
        Returns:
            None
        
        """
        pass

    @abstractmethod
    def log_search_climate_control(self, execid:str, num: int = 25,**kwargs):
        """
        查询预约座舱的结果
        查询开始时间为调用该方法时间，查询开始时间为调用时间 -1 秒
        结束时间为最大延迟时间。(默认为25s)
        :param execid: 指令ID，下发任务时获取到的
        :param num: 查询超时次数
        :param **kwargs: 当前支持： ac_control : Success
                            steering_wheel_heat
                            driver_seat_heat
                            driver_seat_vent
                            passenger_seat_heat
                            passenger_seat_vent
                            rear_left_seat_vent
                            rear_left_seat_heat
                            rear_right_seat_vent
                            rear_right_seat_heat
        """
        
    @abstractmethod
    def check_appStatus(self, bin_name: str):
        """
        检查app提测状态
        
        :param bin_name: app名称
        :returns: appStatus, appId
        :raises keyError: NA
        """

    @abstractmethod
    def submit_app(self, app_name: str):
        """
        提测软件
        
        :param bin_name: app名称
        :returns: NA
        :raises keyError: NA
        """      

    @abstractmethod
    def __get_initial_softid(self):
        """
        根据任务列表的taskid，估计最新的softid
        丑陋方法，需要后续优化
        
        :returns: soft id
        :raises keyError: NA
        """
        
    @abstractmethod
    def get_domain_type_by_app_name(self, app_name: str):
        """
        根据app名称判断车型
        
        :param bin_name: app名称
        :returns: 车型
        :raises keyError: NA
        """
        
    @abstractmethod
    def get_softid_by_app_name(self, app_name: str):
        """
        根据app名称找到softid
        
        :param bin_name: app名称
        :returns: target_softid
        :raises keyError: NA
        """

    @abstractmethod
    def modify_download_net_type(self, task_id: int, download_net_type: int):
        """
        更改taskid的type50中的downloadType字段
        
        :param task_id: 任务id
        :param download_net_type: 下载类型
        :returns:NA
        :raises keyError: NA
        """