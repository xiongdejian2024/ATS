#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
@File         :sdtest.py

@Time         :2023/10/31 10:00

@Author       :quan.sun@jiduauto.com

@Description  :诊断仪能力模拟 抽象接口
"""
from abc import abstractmethod, ABCMeta
from typing import Union, List, Tuple
from xat_ecu.api.constants.common import *


class AbcSdTest(metaclass=ABCMeta):

    @abstractmethod
    def change_usage_mode(self, usage_mode:UsageMode, do_assert:bool = True):
        """
        设置usage_mode
        
        :param usage_mode: 模式类型
        :param do_assert: 模式切换失败时是否上报异常，True为上报(默认值)，False为不上报(主要进行一些异常测试)
        :return:
        """
        pass

    @abstractmethod
    def change_car_mode(self, car_mode:CarMode, do_assert:bool = True):
        """
        设置car_mode
        
        :param car_mode: 模式类型
        :param do_assert: 模式切换失败时是否上报异常，True为上报(默认值)，False为不上报(主要进行一些异常测试)
        :return:
        """
        pass

    @abstractmethod
    def write_ccp(self, ccp:dict):
        """
        设置车辆Car Configuration，可以同时设置一个或者多个CCP
        
        :param ccp: 要写入ccp的字典参数{94:0x80,98:0x2}   key值对应是ccp json中的字节序号
        :returns: result:bool , ccp_value:list
        """
        pass

    def read_bgm_mcu_version(self):
        """
        获取 BGM MCU app version
        
        :returns: str/None
        :raises keyError:
        """
        pass

    def read_bgm_boot_version(self):
        """
        获取 BGM MCU boot version
        
        :returns: str/None
        :raises keyError:
        """
        pass

    def read_bgm_switch_version(self):
        """
        获取 BGM switch version
        
        :returns: str/None
        :raises keyError:
        """
        pass

    def diag_cancel(self):
        """
        FOTA诊断取消, 给1001发 31 01 A1 02
        
        :returns: None
        :raises keyError: None
        """
        pass

    def enter_bgm_default_session(self):
        """
        进入 BGM SOC default session
        
        :returns:
        :raises keyError:AssertionError
        """
        pass

    def enter_bgm_programming_session(self):
        """
        进入 BGM SOC programming session
        
        :returns:
        :raises keyError: AssertionError
        """
        pass

    def enter_bgm_extended_session(self):
        """
        进入 BGM SOC extended session

        :returns:
        :raises keyError: AssertionError
        """
        pass

    # def send_data_and_check(self, ta:int, data:list, check_data:list, diagnostic_action:str="Diagnostic Action"):
    #     """
    #     诊断基础发送接收接口

    #     :param ta:int 逻辑地址  such as 0x1001，0x1002
    #     :param data:list 发送诊断数据
    #     :param check_data:list 期望回复的诊断数据
    #     :param diagnostic_action:str 该诊断行为描述，用于打印
    #     :returns:
    #     :raises keyError:AssertionError
    #     """
    #     pass

    @abstractmethod
    def update_serverdoipid(self, doipid, ecu="BGM"):
        """
        更新 逻辑地址
        
        :param doipid: 0x1001  0x1002
        :param ecu:
        :return:
        """
        pass

    @abstractmethod
    def send_request_and_recv_response(self, msg, msg1=None, recv=True, do_assert=True, ):
        """
        发送数据可以传递一个字符串，一个是列表，随机组合发送数据，是否接收返回值，根据recv 决定，是否直接报错 根据do_assert 决定

        :param msg: 发送的数据，可以是列表[0x10,0x01]，可以是16进制字符串1001/10 01，
        :param msg1: 发送的数据，可以是列表[0x10,0x01]，可以是16进制字符串1001/10 01，
        :param recv: 格式为字符串，列表 布尔 ；对接收的数据是否校验，True 只校验是否为正响应，传入具体的值，则会比较值是否相等
        :param do_assert:
        :return: True/False ，[]
        """
        pass

    @abstractmethod
    def send_data(self, data):
        """
        发送数据  列表里面需要是整型 或者发送数据内容，可以为列表（[0x10,0x01]），或者16进制字符传（1003）

        :param data: such as [0x10, 0x03] 或者  1003
        :return:
        """
        pass

    @abstractmethod
    def quit_boot(self, time_delay=10):
        """
        退出boot

        :param time_delay: 重启后延时时间，单位为秒
        :return:
        """
        pass

    @abstractmethod
    def enter_boot(self, time_delay=10):
        """
        退出 进入boot

        :param time_delay: 重启后延时时间，单位为秒
        :return:
        """
        pass

    @abstractmethod
    def return_udsdata_and_check_and_print_response_result(self):
        """
        发送诊断请求后，用来接收响应的

        :return: 返回一个列表 如 [0x71,0x01,0x02, 0x05,0x10,0x00,0x00,0x00,0x00,]
        """
        pass

    @abstractmethod
    def send_data_and_check(self, ta:int, data:str, check_data='', check_length=0, check_range=[],
                            diagnostic_action:str = "Diagnostic Action"):
        """
        发送诊断指令

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param data: 发送的诊断数据 可以是list,int,str类型
        :param check_data: 预期的返回值，用于检查返回值是否与预期的一致
        :param check_length: 预期的返回值长度，用于检查返回值长度是否与预期的一致
        :param check_range: 预期的返回值大小范围，用于检查返回值大小是否在预期范围内
        :param check_in: 预期的返回值内容范围，用于检查返回值内容是否在预期范围内
        :param diagnostic_action: 描述诊断指令行为
        :return: return_result:str
        """
        pass

    @abstractmethod
    def unlock_and_check(self,ta:int,session=SESSION.EMPTY,level=UnLock.L0,unlock_step=UnlockStep.key,constant=None,check_data='',check_length=0,check_range=[],check_in=[]):
        """
        解锁对应的安全等级

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED
        :param level: 要切换的安全等级 such as 0,1,3,5,7,11 或者 UnLock.L0,UnLock.L1,UnLock.L3,UnLock.L5,UnLock.L7,UnLock.L11
        :param unlock_step: 要执行的安全解锁步骤 such as 0,1或者 UnlockStep.seed,UnlockStep.key
        :param constant: 解锁使用的安全常数
        :param check_data: 预期的返回值，用于检查返回值是否与预期的一致
        :param check_length: 预期的返回值长度，用于检查返回值长度是否与预期的一致
        :param check_range: 预期的返回值大小范围，用于检查返回值大小是否在预期范围内
        :param check_in: 预期的返回值内容范围，用于检查返回值内容是否在预期范围内
        :return: return_result:str
        """
        pass

    @abstractmethod
    def session_ctrl_and_check(self, ta:int, session=SESSION.EMPTY, check_data='', check_length=0, check_range=[],
                               chech_in=[], check_method=Check_Method.read):
        """
        切换诊断会话并检查返回值

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED
        :param check_data: 预期的返回值，用于检查返回值是否与预期的一致
        :param check_length: 预期的返回值长度，用于检查返回值长度是否与预期的一致
        :param check_range: 预期的返回值大小范围，用于检查返回值大小是否在预期范围内
        :param check_in: 预期的返回值内容范围，用于检查返回值内容是否在预期范围内
        :param check_method: 当Check_Method是response时，检查当前诊断指令发送后的返回值是否与预期一致 ； 当Check_Method是method时，当前诊断指令发送后，再发送读取相关的did指令来确认返回值是否与预期一致
        :return: return_result:str
        """
        pass

    @abstractmethod
    def read_did_and_check(self, ta:int, did:int, session=SESSION.EMPTY, check_data='', check_length=0,
                           check_range=[], check_in=[]):
        """
        读取did并检查返回值

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param did: 要读取的did
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED
        :param check_data: 预期的返回值，用于检查返回值是否与预期的一致
        :param check_length: 预期的返回值长度，用于检查返回值长度是否与预期的一致
        :param check_range: 预期的返回值范围，用于检查返回值是否在预期范围内
        :param check_in: 预期的返回值内容范围，用于检查返回值内容是否在预期范围内
        :return: return_result:str
        """
        pass

    @abstractmethod
    def write_did_and_check(self, ta:int, did:int, session=SESSION.DEFAULT, unlock_level=UnLock.L0, write_data='',
                            check_data='', check_length=0, check_range=[], check_in=[], check_method=Check_Method.reset,
                            recover=True):
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

    @abstractmethod
    def io_ctrl_and_check(self, ta, did:int, io_type:int, session=SESSION.DEFAULT, unlock_level=UnLock.L0,
                          write_data='', check_data='', check_length=0, check_range=[], check_in=[],
                          check_method=Check_Method.read):
        """
        写入值到对应的Io control

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param did: 要写入值的did
        :param io_type: 要写入的IO Control的类型
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED
        :param unlock_level: 要解锁的安全等级,sucn as UnLock.L0,UnLock.L1,UnLock.L3,UnLock.L5,UnLock.L7 或者0,1,3,5,7
        :param write_data: 要写入的值
        :param check_data: 预期的返回值，用于检查返回值是否与预期的一致
        :param check_length: 预期的返回值长度，用于检查返回值长度是否与预期的一致
        :param check_range: 预期的返回值范围，用于检查返回值是否在预期范围内
        :param check_in: 预期的返回值内容范围，用于检查返回值内容是否在预期范围内
        :param check_method: 当Check_Method是response时，检查当前诊断指令发送后的返回值是否与预期一致 ； 当Check_Method是method时，当前诊断指令发送后，再发送读取相关的did指令来确认返回值是否与预期一致
        :return: return_result:str
        """
        pass

    @abstractmethod
    def routine_ctrl_and_check(self, ta, did:int, routine_type:int, session=SESSION.DEFAULT, unlock_level=UnLock.L0,
                               write_data='', check_data='', check_length=0, check_range=[], check_in=[]):
        """
        写入值到对应的io control

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param did: 要写入值的did
        :param routine_type: 要写入的Routine Control 的类型
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED 
        :param unlock_level: 要解锁的安全等级
        :param write_data: 要写入的值
        :param check_data: 预期的返回值，用于检查返回值是否与预期的一致
        :param check_length: 预期的返回值长度，用于检查返回值长度是否与预期的一致
        :param check_range: 预期的返回值范围，用于检查返回值是否在预期范围内
        :param check_in: 预期的返回值内容范围，用于检查返回值内容是否在预期范围内
        :return: return_result:str
        """
        pass

    @abstractmethod
    def close_fireware(self):
        """
        关闭BGM防火墙

        :return:
        """

    @abstractmethod
    def get_mcu_cpuload(self):
        """
        获取BGM的cpuload

        :return: return_result:str
        """

    @abstractmethod
    def get_ecu_core_assembly_part_number(self):
        """
        获取BGM的硬件号

        :return: return_result:str
        """

    @abstractmethod
    def get_ecu_delivery_assembly_part_number(self):
        """
        获取BGM的总成号
        :return:return_result:str
        """

    @abstractmethod
    def get_ecu_serial_number(self):
        """
        获取BGM的序列号

        :return: return_result:str
        """

    @abstractmethod
    def get_vehicle_identification_number(self):
        """
        获取BGM的VIN码

        :return: return_result:str
        """

    @abstractmethod
    def get_mcu_software_part_number(self):
        """
        获取BGM的MCU软件号

        :return: return_result:str
        """

    @abstractmethod
    def get_primary_bootloader_software_part_number(self):
        """
        获取BGM的PBL软件号

        :return: return_result:str
        """

    @abstractmethod
    def enter_mcu_boot(self, reconnect=True):
        """
        进入BGMM MUC boot

        :param reconnect: 是否重启BGM之后要重新连接
        :return: return_result:str
        """

    @abstractmethod
    def exit_muc_boot(self, reconnect=True):
        """
        退出BGM MCU boot

        :param reconnect: 是否重启BGM之后要重新连接
        :return: return_result:str
        """

    @abstractmethod
    def reset_0x1082(self,reconnect=True):
        """
        发送1082重启BGM

        :param reconnect: 是否重启BGM之后要重新连接
        :return:
        """

    @abstractmethod
    def reset_0x1181(self, reconnect=True, reboot_TA=TA.FUNCTION):
        """
        向指定TA发送1181重启指令

        :param reconnect: 是否重启BGM之后要重新连接
        :param reboot_TA: 想要重启的TA
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def change_usagemode_a_to_b(self, usage_mode_a:UsageMode, usage_mode_b:UsageMode,
                                wait_time:Union[int, float] = 1):
        """
        切换Usagemode

        :param usage_mode_a: 初始usagemode ABANDONED = 0 INACTIVE = 1 CONVENIENCE = 2 ACTIVE = 11 DRIVING = 13
        :param usage_mode_b: 切到的usagemode
        :param wait_time: 切换时间间隔
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def write_sensor_id(self, tpms_id:list, do_assert:bool = True, **kwargs):
        """
        写4轮传感器ID

        :param tpms_id: 胎压ID 列表
        :param do_assert: 是否需要assert判断 布尔
        :param kwargs: 可变参数
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_tpms_id(response:list, tpms_id:list, is_null:bool):
        """
        检查自定位后胎压ID是否和预期一致

        :param response: 诊断22 28 1f的响应
        :param tpms_id: 预期的胎压ID
        :param is_null: 是否判断为全0
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_dtc(response:list, DTC:list, status:hex):
        """
        校验DTC

        :param response: DTC的响应数据
        :param DTC: 需要校验的DTC
        :param status: 需要检测d
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def check_dtc_num(response:list):
        """
        获取DTC状态

        :param response: DTC的响应数据
        :return: status1, status2
        """

    @abstractmethod
    def control_dtc_setting_and_check(ta,setting_type:int,session=SESSION.EMPTY,unlock_level=UnLock.L0,check_data='',check_length=0,check_range=[],check_in=[]):
        """
        控制bgm dtc记录开关并检查返回值

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param setting_type: setting_type的类型
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED
        :param unlock_level: 要解锁的安全等级,sucn as UnLock.L0,UnLock.L1,UnLock.L3,UnLock.L5,UnLock.L7 或者0,1,3,5,7
        :param check_data: 预期的返回值，用于检查返回值是否与预期的一致
        :param check_length: 预期的返回值长度，用于检查返回值长度是否与预期的一致
        :param check_range: 预期的返回值范围，用于检查返回值是否在预期范围内
        :param check_in: 预期的返回值内容范围，用于检查返回值内容是否在预期范围内
        :return: return_result:str
        """
        pass
    
    @abstractmethod
    def clear_all_dtc_and_check(ta, session=SESSION.EMPTY, unlock_level=UnLock.L0, check_data='', check_length=0, check_range=[], check_in=[]):
        """
        清除dtc并检查返回值

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED
        :param unlock_level: 要解锁的安全等级,sucn as UnLock.L0,UnLock.L1,UnLock.L3,UnLock.L5,UnLock.L7 或者0,1,3,5,7,sunc as
        :param check_data: 预期的返回值，用于检查返回值是否与预期的一致
        :param check_length: 预期的返回值长度，用于检查返回值长度是否与预期的一致
        :param check_range: 预期的返回值范围，用于检查返回值是否在预期范围内
        :param check_in: 预期的返回值内容范围，用于检查返回值内容是否在预期范围内
        :return: return_result:str
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def send_dtc_request_and_return_check_status(self):
        """
        发送读DTC请求并返回需要校验的DTC状态

        :return: result,status1, status2
            result:190209的响应
            status1: DTC产生时检验的状态
            status2: DTC恢复时校验的状态
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def send_dtc_request_and_check_dtc_status(self, DTC: list, status):
        """
        获取DTC状态

        :param DTC: 要校验的DTC
        :param status: 校验的状态
        :return: 
        """
        
    @abstractmethod
    def communication_control_and_check(ta,control_did,control_type=None,session=SESSION.EMPTY,unlock_level=UnLock.L0,check_data='',check_length=0,check_range=[],check_in=[]):
        """
        #控制bgm 总线数据发送接收并检查返回值

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param control_did: control_did
        :param control_did: control_type的类型
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED
        :param unlock_level: 要解锁的安全等级,sucn as UnLock.L0,UnLock.L1,UnLock.L3,UnLock.L5,UnLock.L7 或者0,1,3,5,7
        :param check_data: 预期的返回值，用于检查返回值是否与预期的一致
        :param check_length: 预期的返回值长度，用于检查返回值长度是否与预期的一致
        :param check_range: 预期的返回值范围，用于检查返回值是否在预期范围内
        :param check_in: 预期的返回值内容范围，用于检查返回值内容是否在预期范围内
        :return: return_result:str
        """
        pass

    @abstractmethod
    def read_dtc_and_check(self,ta,sub_did=int,dtc_did:int=None,dtc_type=int,session=SESSION.EMPTY,check_data='',check_length=0,check_range=[],check_in=[]):
        """
        #控制bgm 总线数据发送接收并检查返回值

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param sub_did: sub_did:int
        :param dtc_did: dtc_did:int,默认值是None
        :param dtc_type: dtc_type:int
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED
        :param check_data: 预期的返回值，用于检查返回值是否与预期的一致
        :param check_length: 预期的返回值长度，用于检查返回值长度是否与预期的一致
        :param check_range: 预期的返回值范围，用于检查返回值是否在预期范围内
        :param check_in: 预期的返回值内容范围，用于检查返回值内容是否在预期范围内
        :return: return_result:str
        """
        pass
    
    @abstractmethod
    def wait_vehicle_announcement(before_time=0,reset_type=None,timeout=60):
        """
        #重启后等待并捕捉BGM的第一帧车辆公告的发出

        :param before_time: 发送重启指令的时间 为了计算出重启指令到车辆公告发出时间的时间间隔
        :param reset_type: 重启的类型
        :param timeout: 预期车辆公告发出时间最大范围
        :return: catch_time
        """
        pass
    
    @abstractmethod
    def hard_reset(ta,reconnect=True):
        """
        #硬重启

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param reconnect: 是否重启BGM之后要重新连接
        :return: return_result:str
        """
        pass
    
    @abstractmethod
    def soft_reset(ta, reconnect=True):
        """
        #软重启
        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param reconnect: 是否重启BGM之后要重新连接
        :return: return_result:str
        """
        pass
    
    @abstractmethod
    def caculate_key(self,ta,level,seed,constant=None):
        """
        #根据种子值和安全常数计算出对应的key值

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param level: 要计算的安全等级,sucn as UnLock.L0,UnLock.L1,UnLock.L3,UnLock.L5,UnLock.L7 或者0,1,3,5,7
        :param constant: 要使用计算key值的安全常数,such as 0xFFFFFFFF
        :return: calculatedKey:list
        """
        pass
    
    @abstractmethod
    def write_bncm_key(self,ta=TA.BGM_MCU,session=SESSION.EXTENDED,unlock_level=UnLock.L5,bncm_key=None):
        """
        #写入BNCM值

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED
        :param unlock_level: 要解锁的安全等级,sucn as UnLock.L0,UnLock.L1,UnLock.L3,UnLock.L5,UnLock.L7 或者0,1,3,5,7
        :param bncm_key: 要写入的BNCM值，such as '00112233445566778899aabbccddeeff'
        :return:
        """
        pass

    def get_and_check_tpms_id(self,tpms_id: list, is_null: bool):
        """获取并检查当前的胎压ID

        :param tpms_id:预期的胎压ID
        :param is_null:检查相同还是不同0:相同. 1:不同
        :return:
        """

    @abstractmethod
    def get_bgm_app_soft_version(self):
        """
        获取BGM 软件号，比如 6160110131 AF
        
        :returns: BGM 软件号
        :raises keyError: None
        """
        
    @abstractmethod
    def get_bgm_pbl_soft_version(self):
        """
        获取BGM PBL 软件号，比如 2960110130 AD
        
        :returns: BGM PBL 硬件号
        :raises keyError: None
        """
        
    @abstractmethod
    def get_bgm_hard_version(self):
        """
        获取BGM 硬件号，比如 8895036214 G
        
        :returns: BGM 硬件号
        :raises keyError: None
        """
        
    @abstractmethod
    def get_tcam_hard_version(self):
        """
        获取TCAM 硬件号，比如 8895036217 B
        
        :returns: TCAM 硬件号
        :raises keyError: None
        """
        
    @abstractmethod
    def get_tcam_soft_version(self):
        """
        获取TCAM 软件号，比如 6110110210 AP
        
        :returns: TCAM 软件号
        :raises keyError: None
        """

    @abstractmethod   
    def read_bgm_mpu_version(self):
        """
        读取 ecu 软件号
         返回 bgm mpu 和 boot 版本号
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod 
    def read_bms_did_value(self,did:[str,int],defaul_value:str,default_mode:bool = False):
        """
        获取BMS相关的DID的值
        :param did:BGM 相关DID,字符串或者十六进制数,0xBB01 or "BB01" or "0xBB01" or "bb01"
        :param defaul_value:期望获取的默认值，字符串，例如"10e0" 或者 "00"
        :param default_mode:是否需要进入默认模式再读取DID,bool,True表示需要，False表示不需要。
        :return:
        """


    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod 
    def write_bms_did_value(self,did:[str,int],write_data:str,check_resp:Union[str,None] = None,out_range_value:Union[list,str,None] = None,wait_time:Union[float,int] = 0):
        """
        写BMS相关的DID的值
        :param did:BMS 相关DID,字符串或者十六进制数,0xBB01 or "BB01" or "0xBB01" or "bb01"
        :param write_data:要写入的对应DID的值,字符串，例如"01" or "0808"
        :param check_resp:写入DID之后需要Check的响应，字符串，例如："6ebb01"，默认是None
        :param out_range_value:写入超过DID正常范围的值，字符串或者列表(可以写入多个)，例如"02",["02","03"]，默认是None
        :param wait_time:执行操作之后的等待时间，默认不等待
        :return:
        """


    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod 
    def reboot_bgm_by_diag_hardreset(self):
        """
        发送1181重启BGM
        :return:
        """

    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod 
    def recover_bms_did_to_default_value(self,did:[str,int],defaul_value:str):
        """
        将BMS相关的DID恢复到默认值
        :param did:BMS 相关DID,字符串或者十六进制数,0xBB01 or "BB01" or "0xBB01" or "bb01"
        :param defaul_value:要恢复的默认值，字符串，例如"00" or "8080"
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod 
    def write_did(self,ta:TA,did:[str,int],write_data:str,check_resp:Union[str,None] = None):
        """
        写入值到对应的did
        :param ta:要写入ECU的逻辑地址 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
            BGM_SOC = 0x1001
            BGM_MCU = 0x1002
            TCAM = 0x1011
            FUNCTION = 0x1FFF
        :param did:要写入值的did，字符串或者十六进制数,0xBB01 or "BB01" or "0xBB01" or "bb01"
        :param write_data:要写入的对应DID的值,字符串，例如"01" or "0808"
        :param check_resp:预期的诊断响应，字符串，例如"6ebb01" or "7f2e31",默认为None，表示不需要check诊断响应
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod 
    def read_did(self,ta:TA,did:[str,int],check_resp:Union[str,None] = None,return_result:Union[bool,None] = False):
        """
        读取对应DID的值
        :param ta:要读取ECU的逻辑地址 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
            BGM_SOC = 0x1001
            BGM_MCU = 0x1002
            TCAM = 0x1011
            FUNCTION = 0x1FFF
        :param did:要读取的did，字符串或者十六进制数,0xBB01 or "BB01" or "0xBB01" or "bb01"
        :param check_resp:预期的诊断响应，字符串，例如"6ebb01" or "7f2e31",默认为None，表示不需要check诊断响应
        :param return_result:是否需要返回诊断响应，bool，默认False,表示不需要返回值
        :return:
        """

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def dtc_read_and_check(self, dtc: DTCFault, dtc_sts: DTCSts, fault_sts: bool = True):
        """
        读取DTC并且根据要check的状态来判断检测结果
        :param dtc:DTC故障名字，枚举：DTCFault,太多没有全部展示
            AWMSensorFail_A = "A02D7C"
            AWMSensorFail_B = "A02D7D"
        :param dtc_sts:要检测的DTC状态位：枚举 DTCSts：
            CurrentFailed = 0b00000001
            FailedThisOperCycle = 0b00000010
            Pending = 0b00000100
            Confirm = 0b00001000
            NotCompletedSinceLastClear = 0b00010000
            FailedSinceLastClear = 0b00100000
            NotCompletedThisOperCycle = 0b01000000
            WarningIndicatorReq = 0b10000000
            WithHistoryWithoutCurrent = 0b00001001
        :param fault_sts:要检测故障的存在状态，bool，要检测故障存在就是True,检测不存在就是False
        :return:
        """

    @abstractmethod
    def stop_tester_present(self):
        """
        暂停3E80链接, 避免双tester问题

        :returns: 
        :raises:
        """

    @abstractmethod
    def check_mcu_whether_in_boot(self):
        """
        检查BGM MCU是否处于boot下

        :returns: bool
        :raises:
        """

    @abstractmethod
    def reset_bgm(self):
        """
        给BGM MCU发1181 reset, 并等待30s, 确保全部服务已启动并发出event

        :returns: 
        :raises:
        """    

    @abstractmethod
    def reset_bgm(self):
        """
        给TCAM 0x1011发1103 reset, 并等待180s, 确保全部服务已启动并发出event

        :returns: 
        :raises:
        """           

    @abstractmethod
    def read_ccp(self):
        '''
        读取ccp ，返回值去掉服务最后的校验位
        @return: 字符串，列表
        '''
    @abstractmethod
    def write_single_ccp(self, ccp_index: int, value: int):
        """
        序号从 1开始 不是0
       写入单个ccp数据，写入第几个字节
       :param ccp_index: ccp序号，如#10, index从1开始
       :param value: 写入值
       :return:
        """

    @abstractmethod
    def write_multi_ccp(self, ccp_dict: dict):
        """
        序号从 1开始 不是0
        写入多个ccp数据，如果读取的和写入的值相同，则不进行写入
        :param ccp_dict: 写入的ccp，如{10：2, 20: 3}
        :return:
        """
        
    @abstractmethod
    def check_ccp_value(self, ccp_dict: dict):
        '''
        校验 ccp 是否和读取的一样
        @param ccp_dict:
        @return: 返回 Flase 则存在不匹配的
        '''

   
    @abstractmethod
    def security_access_level(self, level: int = UnLock.L3):
        '''
        27 解锁
         L0 = 0
        L1 = 1
        L3 = 3
        L5 = 5
        L7 = 7
        L11 = 11
        @param level:
        @return:
        '''

    @abstractmethod
    def security_access(self, session: int, level: int, doipid=0x1001):
        '''
        进入指定会话并解锁
        @param session:
        @param level:
        @param doipid:
        @return:
        '''

    @abstractmethod
    def bgm_soc_send_data_and_check(self, send_data=[], expect_recv=[], do_assert=True):
        '''
        发送 数据 并校验预期结果
        @param send_data:
        @param expect_recv:
        @param do_assert:
        @return:
        '''

    @abstractmethod
    def bgm_soc_enter_ecu_eol_mode(self, do_assert=True):
        '''
        SOC enter ECU EOL mode
        @param do_assert:
        @return: 返回 接搜
        '''

    @abstractmethod
    def bgm_soc_quit_ecu_eol_mode(self, do_assert=True):
        '''
        SOC enter ECU EOL mode
        @param do_assert:
        @return:
        '''

    @abstractmethod
    def bgm_soc_ddr(self, do_assert=True):
        '''
        如果收到 Routine Status = completed 说明测试通过
        @param do_assert:
        @return:
        '''

    @abstractmethod
    def bgm_soc_emmc(self, do_assert=True):
        '''
        如果收到 Routine Status = completed 说明测试通过
        @param do_assert:
        @return:
        '''

    @abstractmethod
    def bgm_soc_emmc_checksum_verify(self, do_assert=True):
        '''
        如果收到 Routine Status = completed 说明测试通过
        @param do_assert:
        @return:
        '''

    @abstractmethod
    def bgm_soc_gpio(self, do_assert=True):
        '''
        MCU 收到控制请求后，控制 GPIO 状态
        通过 MPU 侧的 DID 获取 GPIO 状态
        上位机比较控制的状态跟读取的状态是否一致，一致就认为测试通过

        @param do_assert:
        @return:
        '''

    @abstractmethod
    def bgm_soc_check_secure_boot_status(self, do_assert=True):
        '''
        如果收到 OK, 说明测试通过
        @param do_assert:
        @return:
        '''

    @abstractmethod
    def write_ccp_and_check(self, ccp_info: [list, dict, str], restore=True, do_assert=True, **kwargs):
        '''
        写入ccp 并校验写入是否成功，最后恢复原来的ccp
        @param ccp_info:
         为list：列表为整数，不需要 2E F1 06 和最后的校验后
         为dict：写入的ccp，如{10：2, 20: 3}
                序号从 1开始 不是0
                写入多个ccp数据，如果读取的和写入的值相同，则不进行写入
         为 str ：16进制字符串，不需要 2E F1 06 和最后的校验后
        @param restore: 默认为True 会恢复原来的ccp 值
        @param do_assert:
        @param kwargs:
        @return: 返回 False 则是失败，True 则是成功
        '''

    @abstractmethod
    def write_ccp_value(self, ccp_data: [str, list], **kwargs):
        '''
        写入ccp  可以带cheksum  也可以不带，不带会自己生成
        @param ccp_data:
            为list：列表为整数，不需要 2E F1 06 和最后的校验后
            为 str ：16进制字符串，不需要 2E F1 06 和最后的校验后
        @param ccp_len:
        @return:
        '''
    
    @abstractmethod
    def quit_usage_mode(self, do_assert: bool = True):
        """
        退出诊断切换usagemode
        
        :param do_assert: 退出失败时是否上报异常，True为上报(默认值)，False为不上报(主要进行一些异常测试)
        :return:
        """
        pass
    
    @abstractmethod
    def send_usagemode_statistics_times_request_and_return_check_value(self, usagemode_size: UsagemodeSize, usagemode_size2: UsagemodeSize = 0, is_flag: bool = False):
        """
        发送读指定usagemode统计次数并返回指定的统计次数
        
        :param usagemode_size: 指定usagemode的起始位置
        :param usagemode_size2: 第二个指定usagemode的起始位置
        :param is_flag: 是否判断第二个指定usagemode的统计次数及返回
        :return: 返回指定usagemode的统计次数
        """
        pass
    
    @abstractmethod
    def return_usagmode_count(self,response: list, usagemode_size: UsagemodeSize, usagemode_size2: UsagemodeSize = 0, is_flag: bool = False):
        """
        根据指定的usagemode返回次数
        
        :param response: 诊断读取的响应
        :param usagemode_size: 指定usagemode的起始位置
        :param usagemode_size2: 第二个指定usagemode的起始位置
        :param is_flag: 是否判断第二个指定usagemode的统计次数及返回
        :return: 返回指定usagemode的统计次数
        """
        pass
    
    @abstractmethod
    def return_usagmode_time(self,response: list, usagemode_value: UsagemodeValue):
        """
        根据指定的usagemode返回时间
        
        :param response: 诊断读取的响应
        :param usagemode_value: 指定usagemode的起始位置
        :return: 返回指定usagemode的统计时间
        """
        pass

    @abstractmethod
    def compare_a_and_b(self, count_a: int, count_b: int, num: int, count_c: int =0, count_d: int =0, num_2:int =0, is_flag: bool = False):
        """
        比较前后增长是否符合预期
        
        :param count_a: 历史值
        :param count_b: 当前值
        :param num: 预期增长值
        :param count_c: 历史值2
        :param count_d: 当前值2
        :param num: 预期增长值2
        :param is_flag: 是否比较第二个值前后增长符合预期
        :return: 
        """
        pass
    
    @abstractmethod
    def send_usagemode_statistics_time_request_and_return_check_value(self, usagemode_value: UsagemodeValue):
        """
        发送读指定usagemode统计时间并返回指定的统计时间
        
        :param usagemode_value: 指定usagemode的起始位置
        :return: 返回指定usagemode的统计时间
        """
        pass
    
    
    @abstractmethod
    def get_vehicle_model(self, **kwargs):
        '''
        获取车型 配置
        @param kwargs:
        @return:
        '''

    @abstractmethod
    def set_ccp(self,ccp_type="mars",ccp_vlaue=None):
        """
        修改ccp
        @param ccp_type: 车型
        @param ccp_vlaue: ccp要修改得值
        """

    @abstractmethod
    def read_and_check_did_range_value(self,did:int,check_value_range:list):
        """
        读取指定did的值，并校验是否在指定的范围内
        @param did: 指定did,整型，例如：0xDD01或者0xdd01
        @param check_value_range: 校验的值范围
        @return:获取的DID的返回值
        """
    
    # @Author:heng.wang@jiduatuo.com 
    @abstractmethod
    def send_carmode_subtype_request_and_check_result_value(self, carmode_subtype:Carmode_subtype, do_assert:bool=True):
        """
        发送读carmode子模式的did并校验结果
        
        :param carmode_subtype: 校验的carmode子模式的值
        :param do_assert: 
        :return:
        """
    
    # @Author:heng.wang@jiduatuo.com 
    @abstractmethod
    def compare_list(self, list_a: list, list_b: list, is_equal:bool = True):
        """
        比较两个列表是否相同
        
        :param list_a: 比较列表a
        :param list_b: 比较列表b
        :param is_equal: 判断相同还是判断不同
        :return: 
        """
        pass
    
    # @Author:heng.wang@jiduatuo.com 
    @abstractmethod
    def generate_dd01_list(self, read_list:list):
        """
        生成DD01写入的值和校验的值
        
        :param read_list: 当前dd01读取的值
        :return write_list:   写入dd01的值
        :return check_list:   写入dd01的值后校验的值
        """
        pass

    @abstractmethod
    def read_f155(self):
        '''
        诊断读取DID F1 55 获取维持不可开车Flag置位信息
        @param kwargs:
        @return:
        '''
        pass
    
    @abstractmethod
    def write_bncm_key(self,ta=TA.BGM_MCU,session=SESSION.EXTENDED,unlock_level=UnLock.L5,bncm_key=None):
        """
        #写入BNCM值

        :param ta: 要发送的逻辑地址 such as 0x100,0x1002,0x1011, 或者 TA.BGM_SOC,TA.BGM_MCU,TA.TCAM
        :param session: 要切换的会话 such as 1,2,3 或者 SESSION.DEFAULT,SESSION.PROGRAMMING,SESSION.EXTENDED
        :param unlock_level: 要解锁的安全等级,sucn as UnLock.L0,UnLock.L1,UnLock.L3,UnLock.L5,UnLock.L7 或者0,1,3,5,7
        :param bncm_key: 要写入的BNCM值，such as '00112233445566778899aabbccddeeff'
        :return:
        """
        pass   

    @abstractmethod
    def get_bgm_soft_version(self):
        '''
        FOTA专用，其他功能慎用
        诊断读取DID F1 AE 获取BGM 软件号，处理后填充至version_debug.json中
        @param kwargs:
        @return:
        '''
        pass

    @abstractmethod
    def check_program_precondition(self,reverse_test_type = ""):
        '''
        刷写用例专用，其他功能慎用
        刷写step1:检查程序预置条件
        @param reverse_test_type：刷写反向用例类型,包括“上次刷写未进行复位”
        @return:
        '''
        pass

    @abstractmethod
    def enter_program_mode(self):
        '''
        刷写用例专用，其他功能慎用
        刷写step2:功能寻址请求进入program_session
        @return:
        '''
        pass

    @abstractmethod
    def confirm_program_mode(self,doipid):
        '''
        刷写用例专用，其他功能慎用
        刷写step3:物理寻址请求进入program_session
        @param doipid: doip报文逻辑地址
        @return:
        '''
        pass
    
    @abstractmethod
    def diagnostic_session_check(self,doipid):
        '''
        刷写用例专用，其他功能慎用
        刷写step4:诊断会话校验，检验是否进入program_session
        @param doipid: doip报文逻辑地址
        @return:
        '''
        pass

    @abstractmethod
    def infotainment_check(self,doipid):
        '''
        刷写用例专用，其他功能慎用
        刷写step5:信息校验，包括DID ED20,F1AA,F1AB,F18C,D01C
        @param doipid: doip报文逻辑地址
        @return:
        '''
        pass

    @abstractmethod
    def unlocK_for_download(self,doipid,ecu):
        '''
        刷写用例专用，其他功能慎用
        刷写step6:安全会话解锁L1
        @param doipid: doip报文逻辑地址
        @param ecu: 刷写目标ecu，必须传参，安全解锁依赖ecu更新安全常数 
        @return:
        '''
        pass

    @abstractmethod
    def erase_memory(self,doipid,file_path):
        '''
        刷写用例专用，其他功能慎用
        刷写step7:擦除内存
        @param doipid: doip报文逻辑地址
        @param file_path: 待刷文件路径，用于计算擦除地址段
        @return:
        '''
        pass

    @abstractmethod
    def request_download(self,doipid,file_path,compression_encryption_method=[0x00],reverse_test_type = "",**kwargs):
        '''
        刷写用例专用，其他功能慎用
        刷写step8:请求下载
        @param doipid: doip报文逻辑地址
        @param file_path: 待刷文件路径，用于计算请求下载的地址段
        @param compression_encryption_method：压缩算法，默认0x00
        @param reverse_test_type：刷写反向用例类型,包括“跳过erase_memory”，“跳过request_download”
        @return:
        '''
        pass

    @abstractmethod
    def transfer_data(self,doipid,file_path,usr_block_length=1000000000,reverse_test_type = ""):
        '''
        刷写用例专用，其他功能慎用
        刷写step9:数据传输
        @param doipid: doip报文逻辑地址
        @param file_path: 待刷文件路径，用于读取文件内容进行数据传输
        @param usr_block_length: 36服务最大传输长度，默认1000000000，实际依据控制器返回的数据进行传输
        @param reverse_test_type：刷写反向用例类型,包括“跳过request_download”，“跳过transfer_data”，"只传输一个数据块"，"重复传一帧数据"，"传包过程36的blockindex序号错误"，"重复传一段数据"，"跳过一段数据传输"，"错误的包"，"传输块大于最大允许的数据块长度"，"传包过程中异常掉电"
        @return:
        '''
        pass

    @abstractmethod
    def request_transfer_exit(self,doipid,reverse_test_type = ""):
        '''
        刷写用例专用，其他功能慎用
        刷写step10:请求退出数据传输
        @param doipid: doip报文逻辑地址
        @param reverse_test_type：刷写反向用例类型,包括"跳过transfer_data"，"跳过一段数据传输"
        @return:
        '''
        pass

    @abstractmethod
    def transfer_keyinfo(self,doipid,key_info,reverse_test_type = ""):
        '''
        刷写用例专用，其他功能慎用
        刷写step11:传输keyinfo
        @param doipid: doip报文逻辑地址
        @param key_info：待刷写keyinfo
        @param reverse_test_type：刷写反向用例类型,包括"跳过request_transfer_exit"，"keyinfo的长度错误","keyinfo的内容错误"
        @return:
        '''
        pass

    @abstractmethod
    def verify_software_integrity(self,doipid,reverse_test_type = "",verify_time=0):
        '''
        刷写用例专用，其他功能慎用
        刷写step12:软件一致性校验
        @param doipid: doip报文逻辑地址
        @param reverse_test_type：刷写反向用例类型,包括"keyinfo的内容错误","错误的包","安装过程中异常掉电"
        @param verify_time: 软件一致性校验时间，默认0
        @return:
        '''
        pass

    @abstractmethod
    def reset(self):
        '''
        刷写用例专用，其他功能慎用
        刷写step13:刷写完成后复位,功能寻址进行复位
        @return:
        '''
        pass

    @abstractmethod
    def read_version_or_check(self,doipip,check_data=None):
        '''
        读取 ecu 软件号，并根据参数判断是否需要校验
        @param doipid: doip报文逻辑地址，
        @param check_data: 默认为 None 不校验，则返回（True，版本号），否则返回（校验结果，版本号）
        @return:
        '''
        pass
    
    @abstractmethod
    def check_version(self,doipid,check_data=None):
        '''
        获取升级完后的版本，根据 check_data 来判断是否校验
        @param doipid: doip报文逻辑地址
        @param check_data: 默认为 None 不校验，则返回（True，版本号），否则返回（校验结果，版本号）
        @return:
        '''
        pass

    @abstractmethod
    def flashimage_download(self,file_url,offline=False):
        '''
        下载升级文件
        @param file_url: 文件下载地址
        @param offline: 是否离线下载，离线下载需要将文件放在指定文件路径
        @return:
        '''
        pass

    @abstractmethod
    def flash_single_standard_ecu(self,ecu,doipip, file_path,key_info,target_step=14,init_step=0,skip_step=[0],check_data=None,compression_encryption_method=0x00,offline_flashing=False,):
        '''
        标准刷写流程
        @param ecu: 刷写目标ecu
        @param doipip: doip报文逻辑地址
        @param file_path: 待刷文件路径
        @param key_info: 待刷写keyinfo
        @param target_step: 刷写目标步骤
        @param init_step: 刷写初始步骤
        @param skip_step: 刷写跳过步骤
        @param check_data: 待校验版本号，默认为 None 不校验
        @param compression_encryption_method: 压缩算法，默认0x00
        @param offline_flashing: 是否离线刷写
        @return:
        '''
        pass
        
    @abstractmethod
    def upgrade_ecu(self,ecu,doipip,keyinfo,file_url,standard=True, check_data=None, skip_step=[0], offline=False, save_packet=True,sniff_packet=False,save_path='.'):
        '''
        标准刷写流程，包括抓包，下载文件，刷写
        @param ecu: 刷写目标ecu
        @param doipip: doip报文逻辑地址
        @param keyinfo: 待刷写keyinfo
        @param file_url: 文件下载地址
        @param standard：是否是标准刷写，默认True
        @param check_data: 待校验版本号，默认为 None 不校验
        @param skip_step: 刷写跳过步骤
        @param offline: 是否离线下载，离线下载需要将文件放在指定文件路径
        @param save_packet: 是否保存抓包
        @param sniff_packet: 是否要保存tcpdump抓包数据
        @param save_path: 保存tcpdump抓包数据的路径
        @return:
        '''
        pass
    
    # @Author:heng.wang@jiduatuo.com 
    @abstractmethod
    def generate_tire_P_and_T(self,pressure: float, temperature: int):
        """
        生成标准胎压和胎温及校验值
        
        :param pressure: 胎压
        :param temperature: 胎温
        :return tire_P: 标准胎压
        :return tire_T: 标准胎温
        :return check_tire_p: 校验胎压
        :return check_tire_t: 校验胎温
        """
        pass
