#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :io.py

@Time         :2023/10/31 10:00

@Author       :quan.sun@jiduauto.com

@Description  :io能力模拟抽象接口
"""
from abc import abstractmethod, ABCMeta
from typing import Union

from xat_ecu.api.constants.common import *


class AbcIo(metaclass=ABCMeta):
    @abstractmethod
    def io_reset_bgm(self, times: int=1):
        """
        BGM电源断电，经过times 秒后BGM上电
        
        :param times: int  重启中间等待时间（秒）
        :returns:
        :raises:
        """
        pass
        
    @abstractmethod
    def set_door(self,
                 Drvr: Union[Door, None] = None,
                 Pass: Union[Door, None] = None,
                 LeRe: Union[Door, None] = None,
                 RiRe: Union[Door, None] = None,
                 Trunk: Union[Door, None] = None):
        """
        设置门状态

        :param Drvr: 主驾门
        :param Pass: 副驾门
        :param LeRe: 左后门
        :param RiRe: 右后门
        :param Trunk: 尾门
        :return:
        """
        pass

    @abstractmethod
    def set_five_door_sts(self, sts: Door):
        """
        功能: 设置5门的io状态

        :param sts: 设置门的状态，open,close
        :return:
        """
        pass

    @abstractmethod
    def set_hood_sts(self, sts: HoodSts):
        """
        功能: 设置引擎盖的io状态

        :param sts: 设置门的状态，open,close
        :return:
        """
        pass
    
    def driver_seat_notpresent(self):
        """
        功能: 驾驶位乘客不在位

        :return:
        """
        pass

    def driver_seat_present(self):
        """
        功能: 驾驶位乘客在位

        :return:
        """
        pass

    @abstractmethod
    def trigger_door_outswitch_sts(self,
                                   Drvr: Union[OutSwitchPressSts, None] = None,
                                   Pass: Union[OutSwitchPressSts, None] = None,
                                   LeRe: Union[OutSwitchPressSts, None] = None,
                                   RiRe: Union[OutSwitchPressSts, None] = None,
                                   Trunk: Union[Door, None] = None):
        """
        触发门外开关的按压状态

        :param Drvr: 主驾门
        :param Pass: 副驾门
        :param LeRe: 左后门
        :param RiRe: 右后门
        :param Trunk: 尾门
        :return:
        """
        pass

    @abstractmethod
    def set_door(self,
                 Drvr: Union[Door, None] = None,
                 Pass: Union[Door, None] = None,
                 LeRe: Union[Door, None] = None,
                 RiRe: Union[Door, None] = None,
                 Trunk: Union[Door, None] = None):
        """
        设置门状态

        :param Drvr: 主驾门
        :param Pass: 副驾门
        :param LeRe: 左后门
        :param RiRe: 右后门
        :param Trunk: 尾门
        :return:
        """
        pass

    @abstractmethod
    def trigger_all_doors_outswitch(self, sts: OutSwitchPressSts):
        """
        同时设置所有门外开关的按压状态

        :param sts: 门外开关按压状态
        :return:
        """
        pass

    @abstractmethod
    def bgm_diag_active_line_ctrl(self,sts:DiagActLineSts):
        """
        控制BGM诊断激活线状态

        :param sts: 诊断激活线状态
        :return:
        """
        pass
    
    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_horn_switch_sts(self,sts:isOn):
        """
        继电器控制喇叭开关

        :param sts: Off = False On = True
        :return:
        """

    @abstractmethod
    def bgm_power_on(self):
        """
        BGM 上电
        """
        pass

    @abstractmethod
    def bgm_power_off(self):
        """
        BGM 下电
        """
        pass

    @abstractmethod
    def tcam_power_on(self):
        """
        TCAM 上电
        """
        pass

    @abstractmethod
    def tcam_power_off(self):
        """
        TCAM 下电
        """
        pass

    @abstractmethod
    def cdc_power_on(self):
        """
        CDC 上电

        """
        pass

    @abstractmethod
    def cdc_power_off(self):
        """
        CDC 下电
        """
        pass

    @abstractmethod
    def acu_power_on(self):
        """
        ACU 上电
        """
        pass

    @abstractmethod
    def acu_power_off(self):
        """
        ACU 下电
        """
        pass

    @abstractmethod
    def pcan_power_on(self):
        """
        PCAN 上电
        """
        pass

    @abstractmethod
    def pcan_power_off(self):
        """
        PCAN 下电
        """
        pass

    @abstractmethod
    def toomoss_power_on(self):
        """
        图莫斯 上电
        """
        pass

    @abstractmethod
    def toomoss_power_off(self):
        """
        图莫斯 下电
        """
        pass

    @abstractmethod
    def bgm_diag_line_up(self):
        """
        BGM诊断激活线 上电
        """
        pass

    @abstractmethod
    def bgm_diag_line_down(self):
        """
        BGM诊断激活线 下电
        """
        pass

    @abstractmethod
    def tcam_kl15_up(self):
        """
        TCAM诊断激活线 上电
        """
        pass

    @abstractmethod
    def tcam_kl15_down(self):
        """
        TCAM诊断激活线 下电
        """
        pass

    # @Author:hui.zhao@jiduatuo.com
    @abstractmethod
    def set_bgm_hardware_condition_to_default(self):
        """
        恢复BGM io控制的结点到默认状态: 5门关闭，座椅不占位，门外的开关没有被按，没有踩刹车

        :return:
        """

    @abstractmethod
    def partner_process_check(self):
        """
        检查上位机上是否有其它未关闭的soa_partner进程在运行，如果有，则杀死进程
        """
    
    @abstractmethod
    def hazard_light_open(self):
        """
        打开危险灯
        """
    
    @abstractmethod
    def hazard_light_close(self):
        """
        关闭危险灯
        """

    @abstractmethod
    def open_control_can_busoff(self,channel_name:str):
        """
        通过8路继电器控制can busoff
        :param channel_name: 通道名称
        """

    @abstractmethod
    def close_control_can_busoff(self,channel_name:str):
        """
        通过8路继电器控制关闭can busoff
        :param channel_name: 通道名称
        """

    @abstractmethod
    def brake_light_close(self):
        """
        释放刹车
        """
    
    @abstractmethod
    def brake_light_open(self):
        """
        踩下刹车
        """

    @abstractmethod
    def set_pwm(self, io_signal: str, freq: int, duty: int):
        '''
        设置 pwm 的占空比和频率
        :param io_signal io信号名称
        :param freq 频率
        :param duty 占空比
        :param kwargs:
        :return:
        '''

    @abstractmethod
    def get_pwm(self, io_signal: str):
        '''
        读取 pwm 波的 频率和占空比
        :param io_signal io信号名称
        :return:(频率，占空比)
        '''

    @abstractmethod
    def charge_lid_close(self):
        '''
        关闭充电口盖
        '''

    @abstractmethod
    def charge_lid_open(self):
        '''
        打开充电口盖
        '''