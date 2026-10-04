#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :io.py
@Time         :2023/10/31 10:00
@Author       :quan.sun@jiduauto.com
@Description  :io能力模拟抽象接口
"""
from xat_ecu import reporting as allure
from xat_ecu.api import CommonIo

from time import sleep

from xat_ecu.api.constants.common import *
from xat_ecu.legacy.common.logger import logger
from xat_ecu.legacy.interface.nuc_app import partner_process_check
from xat_ecu.legacy.interface.nuc_app import jy_dam0800_operation


class Io(CommonIo):

    def io_reset_bgm(self, times: int = 1):
        self.bgm_power_off()
        sleep(times)
        self.bgm_power_on()

    def set_door(self,
                 Drvr: Union[Door, None] = None,
                 Pass: Union[Door, None] = None,
                 LeRe: Union[Door, None] = None,
                 RiRe: Union[Door, None] = None,
                 Trunk: Union[Door, None] = None):
        if Drvr is not None:
            with allure.step(f'设置主驾门为{Drvr.name}状态'):
                if Drvr.value == Drvr.open.value:
                    self.io.drvr_door_open()
                else:
                    self.io.drvr_door_close()
            logger.info(f'设置主驾门为{Drvr.name}状态成功')
        if Pass is not None:
            with allure.step(f'设置副驾门为{Pass.name}状态'):
                if Pass.value == Pass.open.value:
                    self.io.pass_door_open()
                else:
                    self.io.pass_door_close()
            logger.info(f'设置副驾门为{Pass.name}状态成功')
        if LeRe is not None:
            with allure.step(f'设置左后门为{LeRe.name}状态'):
                if LeRe.value == LeRe.open.value:
                    self.io.lere_door_open()
                else:
                    self.io.lere_door_close()
            logger.info(f'设置左后门为{LeRe.name}状态成功')
        if RiRe is not None:
            with allure.step(f'设置右后门为{RiRe.name}状态'):
                if RiRe.value == RiRe.open.value:
                    self.io.rire_door_open()
                else:
                    self.io.rire_door_close()
            logger.info(f'设置右后门为{RiRe.name}状态成功')
        if Trunk is not None:
            with allure.step(f'设置尾门为{Trunk.name}状态'):
                if Trunk.value == Trunk.open.value:
                    self.io.trunk_door_open()
                else:
                    self.io.trunk_door_close()
            logger.info(f'设置尾门为{Trunk.name}状态成功')

    def set_five_door_sts(self, sts: Door):
        logger.info(f'设置五门为{sts.name}状态')
        if sts.name == "open":
            self.set_door(Drvr=Door.open, Pass=Door.open, RiRe=Door.open, LeRe=Door.open, Trunk=Door.open)
        elif sts.name == "close":
            self.set_door(Drvr=Door.close, Pass=Door.close, RiRe=Door.close, LeRe=Door.close, Trunk=Door.close)

    
    def set_hood_sts(self, sts: HoodSts):
        logger.info(f'设置引擎盖为{sts.name}状态')
        if sts.name == "Open":
            self.io.hood_door1_open()
            self.io.hood_door2_open()
        elif sts.name == "Close":
            self.io.hood_door1_close()
            self.io.hood_door2_open()
    def set_wiper_washing_open(self):
        logger.info(f'雨刮洗涤低液位提醒开关设置为开状态')
        self.io.wiper_washing_low_open()

    def set_wiper_washing_close(self):
        logger.info(f'雨刮洗涤低液位提醒开关设置为关状态')
        self.io.wiper_washing_low_close()

    def driver_seat_notpresent(self):
        self.io.driver_seat_notpresent()
    
    def driver_seat_present(self):
        self.io.driver_seat_present()
    


    def trigger_door_outswitch_sts(self,
                                   Drvr: Union[OutSwitchPressSts, None] = None,
                                   Pass: Union[OutSwitchPressSts, None] = None,
                                   LeRe: Union[OutSwitchPressSts, None] = None,
                                   RiRe: Union[OutSwitchPressSts, None] = None,
                                   Trunk: Union[Door, None] = None):
        if Drvr is not None:
            with allure.step(f'设置主驾门外开关位{Drvr.name}状态'):
                if Drvr.value == OutSwitchPressSts.Press.value:
                    self.io.drvr_door_outswitch_pressed()
                else:
                    self.io.drvr_door_outswitch_unpressed()
            logger.info(f'设置主驾门外开关位{Drvr.name}状态成功')
        if Pass is not None:
            with allure.step(f'设置副驾门外开关位{Pass.name}状态'):
                if Pass.value == OutSwitchPressSts.Press.value:
                    self.io.pass_door_outswitch_pressed()
                else:
                    self.io.pass_door_outswitch_unpressed()
            logger.info(f'设置副驾门外开关位{Pass.name}状态成功')
        if LeRe is not None:
            with allure.step(f'设置左后门外开关位{LeRe.name}状态'):
                if LeRe.value == OutSwitchPressSts.Press.value:
                    self.io.lere_door_outswitch_pressed()
                else:
                    self.io.lere_door_outswitch_unpressed()
            logger.info(f'设置左后门外开关位{LeRe.name}状态成功')
        if RiRe is not None:
            with allure.step(f'设置右后门外开关位{RiRe.name}状态'):
                if RiRe.value == OutSwitchPressSts.Press.value:
                    self.io.rire_door_outswitch_pressed()
                else:
                    self.io.rire_door_outswitch_unpressed()
            logger.info(f'设置右后门外开关位{RiRe.name}状态成功')
        if Trunk is not None:
            with allure.step(f'设置尾门外开关位{Trunk.name}状态'):
                if Trunk.value == OutSwitchPressSts.Press.value:
                    self.io.trunk_door_outswitch_pressed()
                else:
                    self.io.trunk_door_outswitch_unpressed()
            logger.info(f'设置尾门外开关位{Trunk.name}状态成功')

    def trigger_all_doors_outswitch(self, sts: OutSwitchPressSts):
        logger.info(f'触发5门外开关按压状态为{sts}')
        if sts == OutSwitchPressSts.NoPress:
            self.io.drvr_door_outswitch_unpressed()
            self.io.pass_door_outswitch_unpressed()
            self.io.lere_door_outswitch_unpressed()
            self.io.rire_door_outswitch_unpressed()
            self.io.trunk_door_outswitch_unpressed()
        else:
            self.io.drvr_door_outswitch_pressed()
            self.io.pass_door_outswitch_pressed()
            self.io.lere_door_outswitch_pressed()
            self.io.rire_door_outswitch_pressed()
            self.io.trunk_door_outswitch_pressed()

    def bgm_diag_active_line_ctrl(self, sts: DiagActLineSts):
        with allure.step(f'设置BGM诊断激活线为{sts.name}状态'):
            logger.info(f'设置BGM诊断激活线为{sts.name}状态')
            if sts.name == "Active":
                self.io.bgm_diag_line_up()
            elif sts.name == "DisActive":
                self.io.bgm_diag_line_down()
    
    def set_horn_switch_sts(self,sts:isOn):
        with allure.step(f'继电器控制喇叭开关为{sts.name}状态'):
            logger.info(f'继电器控制喇叭开关为{sts.name}状态')
            if sts.name == "Off":
                self.io.horn_switch_open()
            elif sts.name == "On":
                self.io.horn_switch_close()

    def bgm_power_on(self):
        """
        BGM 上电
        """
        self.nuc_app.bgm_power_on()

    def bgm_power_off(self):
        """
        BGM 下电
        """
        self.nuc_app.bgm_power_off()

    def tcam_power_on(self):
        """
        TCAM 上电
        """
        self.nuc_app.tcam_power_on()

    def tcam_power_off(self):
        """
        TCAM 下电
        """
        self.nuc_app.tcam_power_off()

    def cdc_power_on(self):
        """
        CDC 上电
        """
        self.nuc_app.cdc_power_on()

    def cdc_power_off(self):
        """
        CDC 下电
        """
        self.nuc_app.cdc_power_off()

    def acu_power_on(self):
        """
        ACU 上电
        """
        self.nuc_app.acu_power_on()

    def acu_power_off(self):
        """
        ACU 下电
        """
        self.nuc_app.acu_power_off()

    def pcan_power_on(self):
        """
        PCAN 上电
        """
        self.nuc_app.pcan_power_on()

    def pcan_power_off(self):
        """
        PCAN 下电
        """
        self.nuc_app.pcan_power_off()

    def toomoss_power_on(self):
        """
        图莫斯 上电
        """
        self.nuc_app.toomoss_power_on()

    def toomoss_power_off(self):
        """
        图莫斯 下电
        """
        self.nuc_app.toomoss_power_off()

    def bgm_diag_line_up(self):
        """
        BGM诊断激活线 上电
        """
        self.nuc_app.bgm_diag_line_up()

    def bgm_diag_line_down(self):
        """
        BGM诊断激活线 下电
        """
        self.nuc_app.bgm_diag_line_down()

    def tcam_kl15_up(self):
        """
        TCAM诊断激活线 上电
        """
        self.nuc_app.tcam_kl15_up()

    def tcam_kl15_down(self):
        """
        TCAM诊断激活线 下电
        """
        self.nuc_app.tcam_kl15_down()
    
    def set_bgm_hardware_condition_to_default(self):
        with allure.step(f'-----------> 恢复BGM io控制的结点到默认状态：5门关闭，座椅不占位，门外的开关没有被按，没有踩刹车'):
            logger.info(f'----------->  恢复BGM io控制的结点到默认状态：5门关闭，座椅不占位，门外的开关没有被按，没有踩刹车')
            self.io.init_bgm_HW()

    def partner_process_check(self):
        partner_process_check()

    def hazard_light_open(self):
        """
        打开危险灯
        """
        self.io.hazard_light_open()
    
    def hazard_light_close(self):
        """
        关闭危险灯
        """
        self.io.hazard_light_close()

    def open_control_can_busoff(self,channel_name:str):
        """
        通过8路继电器控制can busoff
        """
        if self.nuc_app.power_control_type:
            if self.nuc_app.power_control_type == "jydam0800":
                jy_dam0800_operation(self.nuc_app.tb_cfg.get("jydam0800").get(channel_name),"open",self.nuc_app.jydam0800_port)
            else:
                self.nuc_app.usbrelay_cmd_open(channel_name)
        else:
            self.nuc_app.usbrelay_cmd_open(channel_name)


    def close_control_can_busoff(self,channel_name:str):
        """
        通过8路继电器控制关闭can busoff
        """
        if self.nuc_app.power_control_type:
            if self.nuc_app.power_control_type == "jydam0800":
                jy_dam0800_operation(self.nuc_app.tb_cfg.get("jydam0800").get(channel_name),"close",self.nuc_app.jydam0800_port)
            else:
                self.nuc_app.usbrelay_cmd_close(channel_name)
        else:
            self.nuc_app.usbrelay_cmd_close(channel_name)

    
    def brake_light_open(self):
        promt_info = f"释放刹车"
        with allure.step(promt_info):
            logger.info(promt_info)   
            self.io.brake_up()
    
    def brake_light_close(self):
        promt_info = f"踩下刹车"
        with allure.step(promt_info):
            logger.info(promt_info)  
            self.io.brake_down()

    def trunk_door_release_switch_unpressed(self):
        """
        J3-31 释放尾门解锁开关
        """
        self.io.trunk_door_outswitch_unpressed()    
        
    def trunk_door_release_switch_pressed(self):
        """
        J3-31 按下尾门解锁开关
        """
        self.io.trunk_door_outswitch_pressed()

    def set_pwm(self, io_signal: str, freq: int, duty: int):
        '''
        设置 pwm 的占空比和频率
        :param freq:
        :param duty:
        :param kwargs:
        :return:
        '''
        return self.io.set_pwm(io_signal, freq, duty)

    def get_pwm(self, io_signal: str):
        '''
        读取 pwm 波的 频率和占空比
            发送“read”字符串，读取设置的参数。
            设置成功返回：DOWN；
            设置失败返回：FALL。
        :return:
        '''
        return self.io.get_pwm(io_signal)

    def set_hood1_sts(self, sts1: HoodSts):
        logger.info(f'设置引擎盖J3-37状态为{sts1.name}状态')
        if sts1.name == "Open":
            self.io.hood_door1_open()
        elif sts1.name == "Close":
            self.io.hood_door1_close()

    def set_hood2_sts(self, sts2: HoodSts):
        logger.info(f'设置引擎盖J3-36状态为{sts2.name}状态')
        if sts2.name == "Open":
            self.io.hood_door2_open()
        elif sts2.name == "Close":
            self.io.hood_door2_close()

    def charge_lid_close(self):
        '''
        关闭充电口盖
        '''
        self.io.charge_lid_close()


    def charge_lid_open(self):
        '''
        打开充电口盖
        '''
        self.io.charge_lid_open()
        
    def set_chrglid_open(self):
        logger.info(f'充电口盖按键开关设置为开状态')
        self.io.charge_lid_open()

    def set_chrglid_close(self):
        logger.info(f'充电口盖按键开关设置为关状态')
        self.io.charge_lid_close()

    def dtc_relay_ch_switch(self, **kwargs):
        '''
        DTC测试台架继电器程控接口
        @param kwargs:
        @return:
        '''
        self.io.dtc_relay_ch_switch(**kwargs)
