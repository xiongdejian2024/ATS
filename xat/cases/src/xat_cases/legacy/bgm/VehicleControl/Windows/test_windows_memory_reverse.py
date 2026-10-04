#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_windows_memory_reverse.py
@Author      : daidi.liang@jiduauto.com
@Time        : 2024/06/07 11:30
@Description: BGM车控车设车窗记忆
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


@allure.feature("BGM车控车设/车窗功能")
@allure.story("雨天关窗")
@pytest.mark.run(order=1)
class TestWiperCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client","WindowService_client","KeyService_client","ResetSOAConfigService_client","WindowAppService_client","DoorService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.io.set_five_door_sts(Door.close)
        self.bus_comm.set_vehspd_gear(vehspd=0.0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)

    def after_each_func(self, ecu):
        sleep(3)

    def after_class(self, ecu):
        self.soa.stop_get_wiper_switch_sts()
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass

    
    def set_windows_signal_ub_false(self,drvr_pos,pass_pos,lere_pos,rire_pos):
        self.bus_comm.set("bodycan", "DdmBodyFr04", 'WinPosnStsAtDrvr',drvr_pos,ub_flag=False)
        self.bus_comm.set("bodycan", "PdmBodyFr01", 'WinPosnStsAtPass',pass_pos,ub_flag=False)
        self.bus_comm.set("bodycan", "RldmBodyFr01", 'WinPosnStsAtReLe',lere_pos,ub_flag=False)
        self.bus_comm.set("bodycan", "RrdmBodyFr01", 'WinPosnStsAtReRi',rire_pos,ub_flag=False)
        
    def set_windows_rain_before(self,windows_position,usagmode=UsageMode.INACTIVE):
        self.sd_tester.change_usage_mode(usage_mode=usagmode)
        self.bus_comm.set_windows_position(pos_drvr=windows_position,pos_pass=windows_position,pos_lere=windows_position,pos_rire=windows_position)
        if usagmode == UsageMode.INACTIVE:
            self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(True)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=False)
        
    def change_usgmode_inactive_check_EnaOff(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)

    @pytest.mark.full
    def test_caseid_1988165(self):
        """
        反向用例_inactive下_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.full
    def test_caseid_1988166(self):
        """
        反向用例_inactive下，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.full
    def test_caseid_1988161(self):
        """
        反向用例_inactive下-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.full
    def test_caseid_1988148(self):
        """
        反向用例_inactive下_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.full
    def test_caseid_1988167(self):
        """
        反向用例_inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.full
    def test_caseid_1988164(self):
        """
        反向用例_inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.full
    def test_caseid_1988168(self):
        """
        反向用例_inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.full
    def test_caseid_1988151(self):
        """
        反向用例_inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.full
    def test_caseid_1988162(self):
        """
        反向用例_inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.full
    def test_caseid_1988158(self):
        """
        反向用例_inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
    
    @pytest.mark.full
    def test_caseid_1988155(self):
        """
        反向用例_inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.full
    def test_caseid_1988160(self):
        """
        反向用例_inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    
    #==============================================================================================================================
    @pytest.mark.full
    def test_caseid_1988464(self):
        """
        反向用例_active to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
        
    @pytest.mark.full
    def test_caseid_1988477(self):
        """
        反向用例_active to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
        
    @pytest.mark.full
    def test_caseid_1988478(self):
        """
        反向用例_active to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988487(self):
        """
        反向用例_active to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988473(self):
        """
        反向用例_active to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988467(self):
        """
        反向用例_active to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988468(self):
        """
        反向用例_active to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988475(self):
        """
        反向用例_active to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988480(self):
        """
        反向用例_active to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988484(self):
        """
        反向用例_active to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
    
    @pytest.mark.full
    def test_caseid_1988481(self):
        """
        反向用例_active to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988469(self):
        """
        反向用例_active to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.change_usgmode_inactive_check_EnaOff()
        
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @pytest.mark.full
    def test_caseid_1988476(self):
        """
        反向用例_active to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor (默认四个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
        
    @pytest.mark.full
    def test_caseid_1988465(self):
        """
        反向用例_active to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
        
    @pytest.mark.full
    def test_caseid_1988474(self):
        """
        反向用例_active to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988485(self):
        """
        反向用例_active to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988486(self):
        """
        反向用例_active to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988472(self):
        """
        反向用例_active to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988471(self):
        """
        反向用例_active to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988479(self):
        """
        反向用例_active to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988482(self):
        """
        反向用例_active to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988466(self):
        """
        反向用例_active to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
    
    @pytest.mark.full
    def test_caseid_1988470(self):
        """
        反向用例_active to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988483(self):
        """
        反向用例_active to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.ACTIVE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988496(self):
        """
        反向用例_convience to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
        
    @pytest.mark.full
    def test_caseid_1988488(self):
        """
        反向用例_convience to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
        
    @pytest.mark.full
    def test_caseid_1988503(self):
        """
        反向用例_convience to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988493(self):
        """
        反向用例_convience to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988498(self):
        """
        反向用例_convience to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988489(self):
        """
        反向用例_convience to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988508(self):
        """
        反向用例_convience to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988501(self):
        """
        反向用例_convience to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988507(self):
        """
       反向用例_convience to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988510(self):
        """
        反向用例_convience to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
    
    @pytest.mark.full
    def test_caseid_1988505(self):
        """
        反向用例_convience to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor 
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988494(self):
        """
        反向用例_convience to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.change_usgmode_inactive_check_EnaOff()
        
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @pytest.mark.full
    def test_caseid_1988499(self):
        """
        反向用例_convience to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor (默认四个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
        
    @pytest.mark.full
    def test_caseid_1988511(self):
        """
        反向用例_convience to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988490(self):
        """
        反向用例_convience to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988506(self):
        """
        反向用例_convience to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988509(self):
        """
        反向用例_convience to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988495(self):
        """
        反向用例_convience to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988504(self):
        """
        反向用例_convience to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988492(self):
        """
        反向用例_convience to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开)
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988491(self):
        """
        反向用例_convience to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988500(self):
        """
        反向用例_convience to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
    
    @pytest.mark.full
    def test_caseid_1988502(self):
        """
        反向用例_convience to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988497(self):
        """
        反向用例_convience to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.CONVENIENCE)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.change_usgmode_inactive_check_EnaOff()
        
    #==============================================================================================================================
    @pytest.mark.full
    def test_caseid_1988530(self):
        """
        反向用例_driving to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
        
    @pytest.mark.full
    def test_caseid_1988531(self):
        """
        反向用例_driving to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
        
    @pytest.mark.full
    def test_caseid_1988523(self):
        """
        反向用例_driving to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988522(self):
        """
        反向用例_driving to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988516(self):
        """
        反向用例_driving to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988512(self):
        """
        反向用例_driving to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988526(self):
        """
        反向用例_driving to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988534(self):
        """
        反向用例_driving to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988528(self):
        """
       反向用例_driving to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988517(self):
        """
        反向用例_driving to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
    
    @pytest.mark.full
    def test_caseid_1988533(self):
        """
        反向用例_driving to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988535(self):
        """
        反向用例_driving to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.close,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.change_usgmode_inactive_check_EnaOff()
        
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @pytest.mark.full
    def test_caseid_1988521(self):
        """
        反向用例_driving to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor (默认四个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
        
    @pytest.mark.full
    def test_caseid_1988519(self):
        """
        反向用例_driving to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
        
    @pytest.mark.full
    def test_caseid_1988529(self):
        """
        反向用例_driving to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988527(self):
        """
        反向用例_driving to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988513(self):
        """
        反向用例_driving to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988532(self):
        """
        反向用例_driving to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988515(self):
        """
        反向用例_driving to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988524(self):
        """
        反向用例_driving to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开)
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988520(self):
        """
        反向用例_driving to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988518(self):
        """
        反向用例_driving to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.change_usgmode_inactive_check_EnaOff()
    
    @pytest.mark.full
    def test_caseid_1988525(self):
        """
        反向用例_driving to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.change_usgmode_inactive_check_EnaOff()
        
    @pytest.mark.full
    def test_caseid_1988514(self):
        """
        反向用例_driving to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.set_windows_rain_before(WinPos.percent_100,usagmode=UsageMode.DRIVING)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.change_usgmode_inactive_check_EnaOff()