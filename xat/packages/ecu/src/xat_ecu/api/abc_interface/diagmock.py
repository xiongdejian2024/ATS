#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :diagmock.py

@Time         :2023/10/31 10:00

@Author       :quan.sun@jiduauto.com

@Description  :整车 server ecu 诊断能力模拟抽象接口

"""
from abc import ABCMeta
from typing import Union, List, Tuple


class AbcDiagMock(metaclass=ABCMeta):
    def set_ecu_reply_mode(self, ecu_name, no_reply=False):
        """
        设置某个ECU诊断是否需要回复
        :param ecu_name: ecu名，类型str
        :param no_reply: 是否不回复，False：回复，True: 不回复
        """

    def send_candata(self, bus_name: str, ecu_name: str, res_ecu_canid: int, data: list):
        '''
        指用于tosun can
        :param bus_name: such as "bodycan"
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param res_ecu_canid: type:int  msg id  such as  0x623
        :param data: type:list   such as  [0x7F, 0x22, 0x78]   
        '''

    def update_0x22_data(self, ecu_name: str, did: str, data_info_update: Union[list, dict, str]):
        '''
        更新 0x22 服务相关数据
        single ecu of all_ecu,    data_info   is dict   
        read_data_by_identifier(SID=0x22) data positive response update
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param did: type:str  such as F1AA
        :data_info_update: one DID Positive/negative response      
            Positive response   type : list or str(str建议不用，需要了解的场景比较多)     such as [0x01]
            Negative response   type : dict   such as {"NRC": 0x22}
        '''
    
    def update_0x31_data(self, ecu_name: str, routine_control_data: dict):
        '''
        更新 0x31 服务相关数据
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param routine_control_data: routine control positive (include rid , routine_type , rsr)    /Negative data ,      type:dict 
                            such as  {"08BA": { 1 : [0x00] , 3 : [0x02]}}    {"08BA":{"NRC": 0x22}}
                            rid: "08BA" is  HV PowerDown 
                            routine_type:  are Fixed
                                        1  ---- "start routine request"
                                        2  ---- "stop rountine request"
                                        3  ---- "request rountine results"   
                            rsr: [0x00],[0x02],[0xA0,0x01] Specific ECU may have different implementation      
        '''

    def update_0x10_data(self, ecu_name: str, session_mode: dict):
        '''
        更新 0x10 切换会话服务相关数据 (只针对物理寻址Mock，功能寻址不需要回复)
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param session_mode: one DID Positive/negative response
            Positive response   type : int     such as {0x01: [0x01, 0x02, 0x03, 0x04], 0x02: [0x01, 0x02, 0x03, 0x04]}
            Negative response   type : dict   such as {"NRC": 0x22}
        '''

    def update_0x11_data(self, ecu_name: str, reset_type: Union[int, dict]):
        '''
        更新 0x11 ECU复位服务相关数据 (只针对物理寻址Mock，功能寻址不需要回复)
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param reset_type: one DID Positive/negative response
            Positive response   type : int     such as 0x01硬重启
            Negative response   type : dict   such as {"NRC": 0x22}
        '''

    def update_0x36_data(self, ecu_name: str, block_sequence_counter_nrc_config: Union[int, dict]):
        '''
        0x36 模拟数据传输 (只针对物理寻址Mock，功能寻址不需要回复)
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param block_sequence_counter_nrc_config: 第几个seq counter回复否定响应配置，如：
        {2: 0x78, 18: 0x11} 表示服务端收到第二个counter回复否定响应0x78，第18个counter回复0x11否定
        响应
        '''

    def update_0x37_data(self, ecu_name: str, data: dict):
        '''
        更新 0x37 请求结束刷写 ECU复位服务相关数据 (只针对物理寻址Mock，功能寻址不需要回复)
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param data: one DID Positive/negative response
            Negative response   type : dict   such as {"NRC": 0x22}
        '''

    def update_0x27_data(self, ecu_name: str, data_info: dict):
        '''
        更新 0x27 会话等级解锁 (只针对物理寻址Mock，功能寻址不需要回复)
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param data_info: one DID Positive/negative response
            Positive response   type : int     such as {0x01: [0x01, 0x02, 0x03], 0x02: []} 等级是0x01时
            回复种子：[0x01, 0x02, 0x03], 等级是0x02时直接回复67 02
            Negative response   type : dict   such as {"NRC": 0x22}
        '''

    def update_0x34_data(self, ecu_name: str, data: Union[list, dict]):
        '''
        更新 0x34 请求服务下载 (只针对物理寻址Mock，功能寻址不需要回复)
        :param ecu_name: if it is "can" , ecu_name such as "PLG" , "BCM_F"
                         if it is "lin" , ecu_name such as "SCU_D"
        :param data: one DID Positive/negative response
            Positive response   type : int     such as [0x20, 0x20, 0x20]
            Negative response   type : dict   such as {"NRC": 0x22}
        '''
