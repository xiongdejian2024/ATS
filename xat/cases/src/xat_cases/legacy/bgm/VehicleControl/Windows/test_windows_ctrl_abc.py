#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_Windows_ctrl_abc.py
@Author      : hui.zhao@jiduauto.com
@Time        : 2023/11/9 11:30
@Description: BGM车控车设车窗功能
"""

import os
import sys
import pytest
import allure
from time import sleep

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.constants.common import *


@allure.feature("车控车设")
@allure.story("后视镜功能")
@pytest.mark.run(order=1)
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client","WindowService_client","KeyService_client","ResetSOAConfigService_client","WindowAppService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_vehspd_gear(vehspd=0.0) 
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        sleep(0.5)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)

    def after_each_func(self, ecu):
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUnknown)
        sleep(3)

    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    
    def trigger_outside_switch(self,pos:DoorPos):
        if pos.name == "Dirver":
            self.mix.push_door_outer_switch(DoorPos.Dirver, 2)
            self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.Press)
            time.sleep(2)
            self.io.trigger_door_outswitch_sts(Drvr=OutSwitchPressSts.NoPress)
            self.bus_comm.check_door_opener_req(drv_opener=DoorOpenerReq.Idle, trigger_src=LockTrigerSource.NoTrigSrc)

    def trigger_auto_close_wins_by_rain(self):
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=0)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        sleep(0.5)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(1)
        self.bus_comm.wakeup_lin1()
        sleep(1)
        self.bus_comm.set_rain_detect_sts(False)
        sleep(1)
        self.bus_comm.set_rain_detect_sts(True)
        

    def trigger_walk_away_lock(self):
        self.sd_tester.write_ccp(ccp={94:0x80})
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave,value=2)
        sleep(1)
        self.bus_comm.dk.send_walk_away_lock_cmd()

    def set_windows_pre_condition(self,lock_sts:CenLockSts = CenLockSts.Unlock):
        self.mix.set_common_precontion()
        self.io.set_bgm_hardware_condition_to_default()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.bus_comm.set_five_door_opener_sts(door_opener=DoorOpenerSts.FullClsd)  # 设置bodycan上五个电动门均关闭
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)

    @pytest.mark.smoke
    def test_window_ctrl_caseid_118293(self):
        """
        HMI控制4窗户全关(CarMode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_window_full_close(win_pos=WindowId.kWindowAll)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)


    @pytest.mark.full
    def test_caseid_118127(self):
        """
        右后侧车窗开关状态变为kUnknown(状态未知)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        sleep(0.5)
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_event(zone=WindowId.RrdmWindowReRi,event_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.full
    def test_caseid_118128(self):
        """
        右后侧车窗开关状态变为kDownAuto(自动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_event(zone=WindowId.RrdmWindowReRi,event_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.full
    def test_caseid_118129(self):
        """
        右后侧车窗开关状态变为kDownManual(手动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_event(zone=WindowId.RrdmWindowReRi,event_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118130(self):
        """
        右后侧车窗开关状态变为kUpAuto(自动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_event(zone=WindowId.RrdmWindowReRi,event_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118131(self):
        """
        右后侧车窗开关状态变为kUpManual(手动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_event(zone=WindowId.RrdmWindowReRi,event_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118132(self):
        """
        右后侧车窗开关状态变为kIdle(无请求)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_event(zone=WindowId.RrdmWindowReRi,event_status=WindowSwitchStatus.kIdle)

    @pytest.mark.full
    def test_caseid_118133(self):
        """
        右后侧车窗开关状态为kUnknown(状态未知)时获取对应状态
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_status(zone=WindowId.RrdmWindowReRi,switch_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.full
    def test_caseid_118134(self):
        """
        右后侧车窗开关状态为kDownAuto(自动下降)时获取对应状态
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_status(zone=WindowId.RrdmWindowReRi,switch_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.full
    def test_caseid_118135(self):
        """
        右后侧车窗开关状态为kDownManual(手动下降)时获取对应状态
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_status(zone=WindowId.RrdmWindowReRi,switch_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118136(self):
        """
        右后侧车窗开关状态为kUpAuto(自动上升)时获取对应状态
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_status(zone=WindowId.RrdmWindowReRi,switch_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118137(self):
        """
        右后侧车窗开关状态为kUpManual(手动上升)时获取对应状态
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_status(zone=WindowId.RrdmWindowReRi,switch_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118138(self):
        """
        右后侧车窗开关状态为kIdle(无请求)时获取对应状态
        """
        self.bus_comm.set_windows_RRDM_ReRi_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_status(zone=WindowId.RrdmWindowReRi,switch_status=WindowSwitchStatus.kIdle)
 
    @pytest.mark.full
    def test_caseid_118139(self):
        """
        左后侧车窗开关状态变为kUnknown(状态未知)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        sleep(0.5)
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_event(zone=WindowId.RldmWindowRele,event_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.full
    def test_caseid_118140(self):
        """
        左后侧车窗开关状态变为kDownAuto(自动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_event(zone=WindowId.RldmWindowRele,event_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.full
    def test_caseid_118141(self):
        """
        左后侧车窗开关状态变为kDownManual(手动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_event(zone=WindowId.RldmWindowRele,event_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118142(self):
        """
        左后侧车窗开关状态变为kUpAuto(自动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_event(zone=WindowId.RldmWindowRele,event_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118143(self):
        """
        左后侧车窗开关状态变为kUpManual(手动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_event(zone=WindowId.RldmWindowRele,event_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118144(self):
        """
        左后侧车窗开关状态变为kIdle(无请求)时是否有对应状态上报
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_event(zone=WindowId.RldmWindowRele,event_status=WindowSwitchStatus.kIdle)

    @pytest.mark.full
    def test_caseid_118145(self):
        """
        左后侧车窗开关状态为kUnknown(状态未知)时获取对应状态
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_status(zone=WindowId.RldmWindowRele,switch_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.full
    def test_caseid_118146(self):
        """
        左后侧车窗开关状态为kDownAuto(自动下降)时获取对应状态
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_status(zone=WindowId.RldmWindowRele,switch_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.full
    def test_caseid_118147(self):
        """
        左后侧车窗开关状态为kDownManual(手动下降)时获取对应状态
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_status(zone=WindowId.RldmWindowRele,switch_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118148(self):
        """
        左后侧车窗开关状态为kUpAuto(自动上升)时获取对应状态
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_status(zone=WindowId.RldmWindowRele,switch_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118149(self):
        """
        左后侧车窗开关状态为kUpManual(手动上升)时获取对应状态
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_status(zone=WindowId.RldmWindowRele,switch_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118150(self):
        """
        左后侧车窗开关状态为kIdle(无请求)时获取对应状态
        """
        self.bus_comm.set_windows_RLDM_Rele_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_status(zone=WindowId.RldmWindowRele,switch_status=WindowSwitchStatus.kIdle)
        
    @pytest.mark.full
    def test_caseid_118151(self):
        """
        副驾侧车窗开关状态变为kUnknown(状态未知)时是否有对应状态上报
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        sleep(0.5)
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_event(zone=WindowId.PdmWindowPass,event_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.full
    def test_caseid_118152(self):
        """
        副驾侧车窗开关状态变为kDownAuto(自动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_event(zone=WindowId.PdmWindowPass,event_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.full
    def test_caseid_118153(self):
        """
        副驾侧车窗开关状态变为kDownManual(手动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_event(zone=WindowId.PdmWindowPass,event_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118154(self):
        """
        副驾侧车窗开关状态变为kUpAuto(自动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_event(zone=WindowId.PdmWindowPass,event_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118155(self):
        """
        副驾侧车窗开关状态变为kUpManual(手动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_event(zone=WindowId.PdmWindowPass,event_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118156(self):
        """
        副驾侧车窗开关状态变为kIdle(无请求)时是否有对应状态上报
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_event(zone=WindowId.PdmWindowPass,event_status=WindowSwitchStatus.kIdle)

    @pytest.mark.full
    def test_caseid_118157(self):
        """
        副驾侧车窗开关状态为kUnknown(状态未知)时获取对应状态
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_status(zone=WindowId.PdmWindowPass,switch_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.full
    def test_caseid_118158(self):
        """
        副驾侧车窗开关状态为kDownAuto(自动下降)时获取对应状态
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_status(zone=WindowId.PdmWindowPass,switch_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.full
    def test_caseid_118159(self):
        """
        副驾侧车窗开关状态为kDownManual(手动下降)时获取对应状态
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_status(zone=WindowId.PdmWindowPass,switch_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118160(self):
        """
        副驾侧车窗开关状态为kUpAuto(自动上升)时获取对应状态
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_status(zone=WindowId.PdmWindowPass,switch_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118161(self):
        """
        副驾侧车窗开关状态为kUpManual(手动上升)时获取对应状态
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_status(zone=WindowId.PdmWindowPass,switch_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118162(self):
        """
        副驾侧车窗开关状态为kIdle(无请求)时获取对应状态
        """
        self.bus_comm.set_windows_PDM_pass_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_status(zone=WindowId.PdmWindowPass,switch_status=WindowSwitchStatus.kIdle)

    @pytest.mark.full
    def test_caseid_118163(self):
        """
        主驾侧右后车窗开关状态变为kUnknown(状态未知)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        sleep(0.5)
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_event(zone=WindowId.kWindowRearRight,event_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.smoke
    def test_caseid_118164(self):
        """
        主驾侧右后车窗开关状态变为kDownAuto(自动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_event(zone=WindowId.kWindowRearRight,event_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.full
    def test_caseid_118165(self):
        """
        主驾侧右后车窗开关状态变为kDownManual(手动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_event(zone=WindowId.kWindowRearRight,event_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118166(self):
        """
        主驾侧右后车窗开关状态变为kUpAuto(自动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_event(zone=WindowId.kWindowRearRight,event_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118167(self):
        """
        主驾侧右后车窗开关状态变为kUpManual(手动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_event(zone=WindowId.kWindowRearRight,event_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118168(self):
        """
        主驾侧右后车窗开关状态变为kIdle(无请求)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_event(zone=WindowId.kWindowRearRight,event_status=WindowSwitchStatus.kIdle)

    @pytest.mark.full
    def test_caseid_118169(self):
        """
        主驾侧右后车窗开关状态为kUnknown(状态未知)时获取对应状态
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_status(zone=WindowId.kWindowRearRight,switch_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.smoke
    def test_caseid_118170(self):
        """
        主驾侧右后车窗开关状态为kDownAuto(自动下降)时获取对应状态
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_status(zone=WindowId.kWindowRearRight,switch_status=WindowSwitchStatus.kDownAuto)
    
    @pytest.mark.full
    def test_caseid_118171(self):
        """
        主驾侧右后车窗开关状态为kDownManual(手动下降)时获取对应状态
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_status(zone=WindowId.kWindowRearRight,switch_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118172(self):
        """
        主驾侧右后车窗开关状态为kUpAuto(自动上升)时获取对应状态
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_status(zone=WindowId.kWindowRearRight,switch_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118173(self):
        """
        主驾侧右后车窗开关状态为kUpManual(手动上升)时获取对应状态
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_status(zone=WindowId.kWindowRearRight,switch_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118174(self):
        """
        主驾侧右后车窗开关状态为kIdle(无请求)时获取对应状态
        """
        self.bus_comm.set_windows_ReRi_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_status(zone=WindowId.kWindowRearRight,switch_status=WindowSwitchStatus.kIdle)

    @pytest.mark.smoke
    def test_caseid_118175(self):
        """
        主驾侧左后车窗开关状态变为kUnknown(状态未知)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        sleep(0.5)
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_event(zone=WindowId.kWindowRearLeft,event_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.full
    def test_caseid_118176(self):
        """
        主驾侧左后车窗开关状态变为kDownAuto(自动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_event(zone=WindowId.kWindowRearLeft,event_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.smoke
    def test_caseid_118177(self):
        """
        主驾侧左后车窗开关状态变为kDownManual(手动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_event(zone=WindowId.kWindowRearLeft,event_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118178(self):
        """
        主驾侧左后车窗开关状态变为kUpAuto(自动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_event(zone=WindowId.kWindowRearLeft,event_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118179(self):
        """
        主驾侧左后车窗开关状态变为kUpManual(手动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_event(zone=WindowId.kWindowRearLeft,event_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118180(self):
        """
        主驾侧左后车窗开关状态变为kIdle(无请求)时是否有对应状态上报
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_event(zone=WindowId.kWindowRearLeft,event_status=WindowSwitchStatus.kIdle)

    @pytest.mark.full
    def test_caseid_118181(self):
        """
        主驾侧左后车窗开关状态为kUnknown(状态未知)时获取对应状态
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_status(zone=WindowId.kWindowRearLeft,switch_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.full
    def test_caseid_118182(self):
        """
        主驾侧左后车窗开关状态为kDownAuto(自动下降)时获取对应状态
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_status(zone=WindowId.kWindowRearLeft,switch_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.smoke
    def test_caseid_118183(self):
        """
        主驾侧左后车窗开关状态为kDownManual(手动下降)时获取对应状态
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_status(zone=WindowId.kWindowRearLeft,switch_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118184(self):
        """
        主驾侧左后车窗开关状态为kUpAuto(自动上升)时获取对应状态
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_status(zone=WindowId.kWindowRearLeft,switch_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118185(self):
        """
        主驾侧左后车窗开关状态为kUpManual(手动上升)时获取对应状态
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_status(zone=WindowId.kWindowRearLeft,switch_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118186(self):
        """
        主驾侧左后车窗开关状态为kIdle(无请求)时获取对应状态
        """
        self.bus_comm.set_windows_ReLe_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_status(zone=WindowId.kWindowRearLeft,switch_status=WindowSwitchStatus.kIdle)

    @pytest.mark.full
    def test_caseid_118187(self):
        """
        主驾侧副驾车窗开关状态变为kUnknown(状态未知)时是否有对应状态上报
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        sleep(0.5)
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_event(zone=WindowId.kWindowFrontRight,event_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.full
    def test_caseid_118188(self):
        """
        主驾侧副驾车窗开关状态变为kDownAuto(自动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_event(zone=WindowId.kWindowFrontRight,event_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.full
    def test_caseid_118189(self):
        """
        主驾侧副驾车窗开关状态变为kDownManual(手动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_event(zone=WindowId.kWindowFrontRight,event_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.smoke
    def test_caseid_118190(self):
        """
        主驾侧副驾车窗开关状态变为kUpAuto(自动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_event(zone=WindowId.kWindowFrontRight,event_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118191(self):
        """
        主驾侧副驾车窗开关状态变为kUpManual(手动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_event(zone=WindowId.kWindowFrontRight,event_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118192(self):
        """
        主驾侧副驾车窗开关状态变为kIdle(无请求)时是否有对应状态上报
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_event(zone=WindowId.kWindowFrontRight,event_status=WindowSwitchStatus.kIdle)

    @pytest.mark.full
    def test_caseid_118193(self):
        """
        主驾侧副驾车窗开关状态为kUnknown(状态未知)时获取对应状态
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_status(zone=WindowId.kWindowFrontRight,switch_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.full
    def test_caseid_118194(self):
        """
        主驾侧副驾车窗开关状态为kDownAuto(自动下降)时获取对应状态
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_status(zone=WindowId.kWindowFrontRight,switch_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.full
    def test_caseid_118195(self):
        """
        主驾侧副驾车窗开关状态为kDownManual(手动下降)时获取对应状态
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_status(zone=WindowId.kWindowFrontRight,switch_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.smoke
    def test_caseid_118196(self):
        """
        主驾侧副驾车窗开关状态为kUpAuto(自动上升)时获取对应状态
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_status(zone=WindowId.kWindowFrontRight,switch_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.full
    def test_caseid_118197(self):
        """
        主驾侧副驾车窗开关状态为kUpManual(手动上升)时获取对应状态
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_status(zone=WindowId.kWindowFrontRight,switch_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118198(self):
        """
        主驾侧副驾车窗开关状态为kIdle(无请求)时获取对应状态
        """
        self.bus_comm.set_windows_pass_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_status(zone=WindowId.kWindowFrontRight,switch_status=WindowSwitchStatus.kIdle)

    @pytest.mark.full
    def test_caseid_118199(self):
        """
        主驾驶车窗开关状态变为kUnknown(状态未知)时是否有对应状态上报
        """
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        sleep(0.5)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_event(zone=WindowId.kWindowFrontLeft,event_status=WindowSwitchStatus.kUnknown)

    
    @pytest.mark.full
    def test_caseid_118200(self):
        """
        主驾驶车窗开关状态变为kDownAuto(自动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_event(zone=WindowId.kWindowFrontLeft,event_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.full
    def test_caseid_118201(self):
        """
        主驾驶车窗开关状态变为kDownManual(手动下降)时是否有对应状态上报
        """
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_event(zone=WindowId.kWindowFrontLeft,event_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118202(self):
        """
        主驾驶车窗开关状态变为kUpAuto(自动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_event(zone=WindowId.kWindowFrontLeft,event_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.smoke
    def test_caseid_118203(self):
        """
        主驾驶车窗开关状态变为kUpManual(手动上升)时是否有对应状态上报
        """
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_event(zone=WindowId.kWindowFrontLeft,event_status=WindowSwitchStatus.kUpManual)
    
    @pytest.mark.full
    def test_caseid_118204(self):
        """
        主驾驶车窗开关状态变为kIdle(无请求)时是否有对应状态上报
        """
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_event(zone=WindowId.kWindowFrontLeft,event_status=WindowSwitchStatus.kIdle)

    @pytest.mark.full
    def test_caseid_118205(self):
        """
        主驾驶车窗开关状态为kUnknown(状态未知)时获取对应状态
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUnknown)
        self.soa.check_window_status(zone=WindowId.kWindowFrontLeft,switch_status=WindowSwitchStatus.kUnknown)

    @pytest.mark.full
    def test_caseid_118206(self):
        """
        主驾驶车窗开关状态为kDownAuto(自动下降)时获取对应状态
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kDownAuto)
        self.soa.check_window_status(zone=WindowId.kWindowFrontLeft,switch_status=WindowSwitchStatus.kDownAuto)

    @pytest.mark.full
    def test_caseid_118207(self):
        """
        主驾驶车窗开关状态为kDownManual(手动下降)时获取对应状态
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kDownManual)
        self.soa.check_window_status(zone=WindowId.kWindowFrontLeft,switch_status=WindowSwitchStatus.kDownManual)

    @pytest.mark.full
    def test_caseid_118208(self):
        """
        主驾驶车窗开关状态为kUpAuto(自动上升)时获取对应状态
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUpAuto)
        self.soa.check_window_status(zone=WindowId.kWindowFrontLeft,switch_status=WindowSwitchStatus.kUpAuto)

    @pytest.mark.smoke
    def test_caseid_118209(self):
        """
        主驾驶车窗开关状态为kUpManual(手动上升)时获取对应状态
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kUpManual)
        self.soa.check_window_status(zone=WindowId.kWindowFrontLeft,switch_status=WindowSwitchStatus.kUpManual)

    @pytest.mark.full
    def test_caseid_118210(self):
        """
        主驾驶车窗开关状态为kIdle(无请求)时获取对应状态
        """
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_windows_stauts_signal(status=WindowSwitchStatus.kIdle)
        self.soa.check_window_status(zone=WindowId.kWindowFrontLeft,switch_status=WindowSwitchStatus.kIdle)


    @pytest.mark.full
    def test_caseid_118212(self):
        """
        HMI控制4窗户全开(Car Mode=Normal、UsageMode=Driving)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_full_open(win_pos=WindowId.kWindowAll)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118213(self):
        """
        HMI控制4窗户全开(Car Mode=Normal、UsageMode=Active)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_full_open(win_pos=WindowId.kWindowAll)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118240(self):
        """
        HMI单独控制右后窗户打开100% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearRight,position=WinPos.percent_100)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118241(self):
        """
        HMI单独控制右后窗户打开80% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearRight,position=WinPos.percent_80)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_80)

    @pytest.mark.full
    def test_caseid_118242(self):
        """
        HMI单独控制右后窗户打开60% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearRight,position=WinPos.percent_60)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_60)

    @pytest.mark.full
    def test_caseid_118243(self):
        """
        HMI单独控制右后窗户打开40% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearRight,position=WinPos.percent_40)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_40)

    @pytest.mark.full
    def test_caseid_118244(self):
        """
        HMI单独控制右后窗户打开20% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearRight,position=WinPos.percent_20)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_20)

    @pytest.mark.full
    def test_caseid_118245(self):
        """
        HMI单独控制右后窗户打开4% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearRight,position=WinPos.percent_4)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_4)

    @pytest.mark.smoke
    def test_caseid_118246(self):
        """
        HMI单独控制左后窗户打开100% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearLeft,position=WinPos.percent_100)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_100)
    
    @pytest.mark.full
    def test_caseid_118247(self):
        """
        HMI单独控制左后窗户打开80% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearLeft,position=WinPos.percent_80)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_80)

    @pytest.mark.full
    def test_caseid_118248(self):
        """
        HMI单独控制左后窗户打开60% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearLeft,position=WinPos.percent_60)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_60)


    @pytest.mark.full
    def test_caseid_118249(self):
        """
        HMI单独控制左后窗户打开40% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearLeft,position=WinPos.percent_40)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_40)

    @pytest.mark.full
    def test_caseid_118250(self):
        """
        HMI单独控制左后窗户打开20% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearLeft,position=WinPos.percent_20)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_20)

    @pytest.mark.full
    def test_caseid_118251(self):
        """
        HMI单独控制左后窗户打开4% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowRearLeft,position=WinPos.percent_4)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_4)

    @pytest.mark.full
    def test_caseid_118252(self):
        """
        HMI单独控制副驾驶窗户打开100% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontRight,position=WinPos.percent_100)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118253(self):
        """
        HMI单独控制副驾驶窗户打开80% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontRight,position=WinPos.percent_80)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_80)

    @pytest.mark.full
    def test_caseid_118254(self):
        """
        HMI单独控制副驾驶窗户打开60% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontRight,position=WinPos.percent_60)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_60)

    @pytest.mark.full
    def test_caseid_118255(self):
        """
        HMI单独控制副驾驶窗户打开40% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontRight,position=WinPos.percent_40)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_40)

    @pytest.mark.full
    def test_caseid_118256(self):
        """
        HMI单独控制副驾驶窗户打开20% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontRight,position=WinPos.percent_20)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_20)

    @pytest.mark.smoke
    def test_caseid_118257(self):
        """
        HMI单独控制副驾驶窗户打开4% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontRight,position=WinPos.percent_4)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_4)

    @pytest.mark.full
    def test_caseid_118258(self):
        """
        HMI单独控制主驾驶窗户打开100% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontLeft,position=WinPos.percent_100)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118259(self):
        """
        HMI单独控制主驾驶窗户打开80% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontLeft,position=WinPos.percent_80)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_80)

    @pytest.mark.full
    def test_caseid_118260(self):
        """
        HMI单独控制主驾驶窗户打开60% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontLeft,position=WinPos.percent_60)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_60)

    @pytest.mark.full
    def test_caseid_118261(self):
        """
        HMI单独控制主驾驶窗户打开40% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontLeft,position=WinPos.percent_40)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_40)

    @pytest.mark.full
    def test_caseid_118262(self):
        """
        HMI单独控制主驾驶窗户打开20% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontLeft,position=WinPos.percent_20)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20)

    @pytest.mark.smoke
    def test_caseid_118263(self):
        """
        HMI单独控制主驾驶窗户打开4% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowFrontLeft,position=WinPos.percent_4)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_4)

    @pytest.mark.smoke
    def test_caseid_118264(self):
        """
        HMI控制4窗户打开100% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_100)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118265(self):
        """
        HMI控制4窗户打开96% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_96)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_96,pos_pass=WinPos.percent_96,pos_lere=WinPos.percent_96,pos_rire=WinPos.percent_96)

    @pytest.mark.full
    def test_caseid_118266(self):
        """
        HMI控制4窗户打开92% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_92)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_92,pos_pass=WinPos.percent_92,pos_lere=WinPos.percent_92,pos_rire=WinPos.percent_92)

    @pytest.mark.full
    def test_caseid_118267(self):
        """
        HMI控制4窗户打开88% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_88)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_88,pos_pass=WinPos.percent_88,pos_lere=WinPos.percent_88,pos_rire=WinPos.percent_88)

    @pytest.mark.full
    def test_caseid_118268(self):
        """
        HMI控制4窗户打开84% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_84)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_84,pos_pass=WinPos.percent_84,pos_lere=WinPos.percent_84,pos_rire=WinPos.percent_84)

    @pytest.mark.full
    def test_caseid_118269(self):
        """
        HMI控制4窗户打开80% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_80)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_80,pos_pass=WinPos.percent_80,pos_lere=WinPos.percent_80,pos_rire=WinPos.percent_80)

    @pytest.mark.full
    def test_caseid_118270(self):
        """
        HMI控制4窗户打开76% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_76)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_76,pos_pass=WinPos.percent_76,pos_lere=WinPos.percent_76,pos_rire=WinPos.percent_76)

    @pytest.mark.full
    def test_caseid_118271(self):
        """
        HMI控制4窗户打开72% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_72)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_72,pos_pass=WinPos.percent_72,pos_lere=WinPos.percent_72,pos_rire=WinPos.percent_72)

    @pytest.mark.full
    def test_caseid_118272(self):
        """
        HMI控制4窗户打开68% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_68)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_68,pos_pass=WinPos.percent_68,pos_lere=WinPos.percent_68,pos_rire=WinPos.percent_68)

    @pytest.mark.full
    def test_caseid_118273(self):
        """
        HMI控制4窗户打开64% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_64)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_64,pos_pass=WinPos.percent_64,pos_lere=WinPos.percent_64,pos_rire=WinPos.percent_64)

    @pytest.mark.full
    def test_caseid_118274(self):
        """
        HMI控制4窗户打开60% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_60)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_60,pos_pass=WinPos.percent_60,pos_lere=WinPos.percent_60,pos_rire=WinPos.percent_60)

    @pytest.mark.full
    def test_caseid_118275(self):
        """
        HMI控制4窗户打开56% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_56)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_56,pos_pass=WinPos.percent_56,pos_lere=WinPos.percent_56,pos_rire=WinPos.percent_56)

    @pytest.mark.full
    def test_caseid_118276(self):
        """
        HMI控制4窗户打开52% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_52)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_52,pos_pass=WinPos.percent_52,pos_lere=WinPos.percent_52,pos_rire=WinPos.percent_52)

    @pytest.mark.full
    def test_caseid_118277(self):
        """
        HMI控制4窗户打开52% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_48)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_48,pos_pass=WinPos.percent_48,pos_lere=WinPos.percent_48,pos_rire=WinPos.percent_48)

    @pytest.mark.full
    def test_caseid_118278(self):
        """
        HMI控制4窗户打开44% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_44)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_44,pos_pass=WinPos.percent_44,pos_lere=WinPos.percent_44,pos_rire=WinPos.percent_44)

    @pytest.mark.full
    def test_caseid_118279(self):
        """
        HMI控制4窗户打开40% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_40)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_40,pos_pass=WinPos.percent_40,pos_lere=WinPos.percent_40,pos_rire=WinPos.percent_40)

    @pytest.mark.full
    def test_caseid_118280(self):
        """
        HMI控制4窗户打开36% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_36)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_36,pos_pass=WinPos.percent_36,pos_lere=WinPos.percent_36,pos_rire=WinPos.percent_36)

    @pytest.mark.full
    def test_caseid_118281(self):
        """
        HMI控制4窗户打开32% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_32)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_32,pos_pass=WinPos.percent_32,pos_lere=WinPos.percent_32,pos_rire=WinPos.percent_32)

    @pytest.mark.full
    def test_caseid_118282(self):
        """
        HMI控制4窗户打开28% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_28)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_28,pos_pass=WinPos.percent_28,pos_lere=WinPos.percent_28,pos_rire=WinPos.percent_28)

    @pytest.mark.full
    def test_caseid_118283(self):
        """
        HMI控制4窗户打开24% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_24)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_24,pos_pass=WinPos.percent_24,pos_lere=WinPos.percent_24,pos_rire=WinPos.percent_24)

    @pytest.mark.full
    def test_caseid_118284(self):
        """
        HMI控制4窗户打开20% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_20)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_20,pos_pass=WinPos.percent_20,pos_lere=WinPos.percent_20,pos_rire=WinPos.percent_20)

    @pytest.mark.full
    def test_caseid_118285(self):
        """
        HMI控制4窗户打开16% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_16)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_16,pos_pass=WinPos.percent_16,pos_lere=WinPos.percent_16,pos_rire=WinPos.percent_16)

    @pytest.mark.full
    def test_caseid_118286(self):
        """
        HMI控制4窗户打开12% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_12)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_12,pos_pass=WinPos.percent_12,pos_lere=WinPos.percent_12,pos_rire=WinPos.percent_12)

    @pytest.mark.full
    def test_caseid_118287(self):
        """
        HMI控制4窗户打开8% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_8)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_8,pos_pass=WinPos.percent_8,pos_lere=WinPos.percent_8,pos_rire=WinPos.percent_8)

    @pytest.mark.smoke
    def test_caseid_118288(self):
        """
        HMI控制4窗户打开4% (Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_position(win_pos=WindowId.kWindowAll,position=WinPos.percent_4)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_4,pos_pass=WinPos.percent_4,pos_lere=WinPos.percent_4,pos_rire=WinPos.percent_4)

    @pytest.mark.full
    def test_caseid_118289(self):
        """
        HMI控制右后窗户全关(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_window_full_close(win_pos=WindowId.kWindowRearRight)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_118290(self):
        """
        HMI控制左后窗户全关(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_window_full_close(win_pos=WindowId.kWindowRearLeft)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.close)
    
    @pytest.mark.full
    def test_caseid_118291(self):
        """
        HMI控制副驾驶窗户全关(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_window_full_close(win_pos=WindowId.kWindowFrontRight)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.close)

    @pytest.mark.full
    def test_caseid_118292(self):
        """
        HMI控制驾驶位窗户全关(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_window_full_close(win_pos=WindowId.kWindowFrontLeft)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close)
    
    @pytest.mark.smoke
    def test_caseid_118293(self):
        """
        HMI控制4窗户全关(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.soa.hmi_set_window_full_close(win_pos=WindowId.kWindowAll)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)

    @pytest.mark.full
    def test_caseid_118294(self):
        """
        HMI控制右后窗户全开(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_full_open(win_pos=WindowId.kWindowRearRight)
        self.bus_comm.check_windows_position_req(pos_rire=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118295(self):
        """
        HMI控制左后窗户全开(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_full_open(win_pos=WindowId.kWindowRearLeft)
        self.bus_comm.check_windows_position_req(pos_lere=WinPos.percent_100)

    @pytest.mark.full
    def test_caseid_118296(self):
        """
        HMI控制副驾驶窗户全开(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_full_open(win_pos=WindowId.kWindowFrontRight)
        self.bus_comm.check_windows_position_req(pos_pass=WinPos.percent_100)
    
    @pytest.mark.full
    def test_caseid_118297(self):
        """
        HMI控制驾驶位窗户全开(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_full_open(win_pos=WindowId.kWindowFrontLeft)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100)

    @pytest.mark.smoke
    def test_caseid_118298(self):
        """
        HMI控制4窗户全开(Car Mode=Normal、UsageMode=Convenience)
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.soa.hmi_set_window_full_open(win_pos=WindowId.kWindowAll)
        self.bus_comm.check_windows_position_req(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)

    