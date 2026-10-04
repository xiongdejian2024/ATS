#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_windows_memory.py
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
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=False)
        sleep(0.5)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
        sleep(1)

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
        
    def set_windows_rain_before(self,drvr_pos,pass_pos,lere_pos,rire_pos,usagmode=UsageMode.INACTIVE):
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
        self.bus_comm.set_windows_position(pos_drvr=drvr_pos,pos_pass=pass_pos,pos_lere=lere_pos,pos_rire=rire_pos)
        self.sd_tester.change_usage_mode(usage_mode=usagmode)
        
    @pytest.mark.smoke
    def test_caseid_1988031(self):
        """
        inactive下_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.smoke
    def test_caseid_1988032(self):
        """
        inactive下，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.smoke
    def test_caseid_1988035(self):
        """
        inactive下-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.smoke
    def test_caseid_1988036(self):
        """
        inactive下_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.smoke
    def test_caseid_1988037(self):
        """
        inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.smoke
    def test_caseid_1988038(self):
        """
        inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988040(self):
        """
        inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988041(self):
        """
        inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988042(self):
        """
        inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988043(self):
        """
        inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
    
    @pytest.mark.sanity
    def test_caseid_1988044(self):
        """
        inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988045(self):
        """
        inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.set_windows_rain_before(WinPos.percent_100,WinPos.percent_100,WinPos.percent_100,WinPos.percent_100)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988077(self):
        """
        convience to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988078(self):
        """
        convience to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988074(self):
        """
        convience to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988069(self):
        """
        convience to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988079(self):
        """
        convience to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988076(self):
        """
        convience to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988080(self):
        """
        convience to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988070(self):
        """
        convience to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988075(self):
        """
        convience to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988072(self):
        """
        convience to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
    
    @pytest.mark.sanity
    def test_caseid_1988071(self):
        """
        convience to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988073(self):
        """
        convience to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    #------------------------------------------------------------------------------------------------------------------
    @pytest.mark.sanity
    def test_caseid_1988414(self):
        """
        driving to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988412(self):
        """
        driving to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988405(self):
        """
        driving to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988407(self):
        """
        driving to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988404(self):
        """
        driving to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988413(self):
        """
        driving to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988408(self):
        """
        driving to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988411(self):
        """
        driving to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988410(self):
        """
        driving to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988409(self):
        """
        driving to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
    
    @pytest.mark.sanity
    def test_caseid_1988406(self):
        """
        driving to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988403(self):
        """
        driving to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    #==============================================================================================================================
    @pytest.mark.sanity
    def test_caseid_1988425(self):
        """
        active to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988416(self):
        """
        active to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988422(self):
        """
        active to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988418(self):
        """
        active to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988417(self):
        """
        active to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988420(self):
        """
        active to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988424(self):
        """
        active to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988427(self):
        """
        active to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988419(self):
        """
        active to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988423(self):
        """
        active to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
    
    @pytest.mark.sanity
    def test_caseid_1988426(self):
        """
        active to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988421(self):
        """
        active to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(1.5)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    @pytest.mark.sanity
    def test_caseid_1988428(self):
        """
        active to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor (默认四个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988434(self):
        """
        active to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988435(self):
        """
        active to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988439(self):
        """
        active to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988432(self):
        """
        active to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988429(self):
        """
        active to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988430(self):
        """
        active to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988433(self):
        """
        active to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988436(self):
        """
        active to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988438(self):
        """
        active to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
    
    @pytest.mark.sanity
    def test_caseid_1988437(self):
        """
        active to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988431(self):
        """
        active to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.ACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    @pytest.mark.sanity
    def test_caseid_1988446(self):
        """
        driving to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor (默认四个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988440(self):
        """
        driving to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988445(self):
        """
        driving to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988450(self):
        """
        driving to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988451(self):
        """
        driving to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988444(self):
        """
        driving to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988443(self):
        """
        driving to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988447(self):
        """
        driving to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988448(self):
        """
        driving to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988441(self):
        """
        driving to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
    
    @pytest.mark.sanity
    def test_caseid_1988442(self):
        """
        driving to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988449(self):
        """
        driving to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    @pytest.mark.sanity
    def test_caseid_1988452(self):
        """
        convience to inactive_车窗位置记忆，4个窗户全开—检查降雨检测使能信号状态EnaOfflineMonitor (默认四个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988462(self):
        """
        convience to inactive，车窗位置记忆，4个窗户全开，更新车窗UB位为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
        
    @pytest.mark.sanity
    def test_caseid_1988461(self):
        """
        convience to inactive-车窗位置记忆_4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988459(self):
        """
        convience to inactive_车窗位置记忆，更新车窗UB位为0，4个窗户状态为未知--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.ukwn,pos_pass=WinPos.ukwn,pos_lere=WinPos.ukwn,pos_rire=WinPos.ukwn)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(0,0,0,0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988454(self):
        """
        convience to inactive下车窗位置记忆_4个窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988453(self):
        """
        convience to inactive下_车窗位置记忆_更新车窗UB位为0，窗户状态为全关--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.close,pos_lere=WinPos.close,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,1,1,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        
    @pytest.mark.sanity
    def test_caseid_1988458(self):
        """
        convience to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988456(self):
        """
        convience to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988457(self):
        """
        convience to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988455(self):
        """
        convience to inactive下车窗位置记忆-主驾窗户为关闭，其余窗户全开，车窗UB为均为0--检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.close,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(1,26,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
    
    @pytest.mark.sanity
    def test_caseid_1988460(self):
        """
        convience to inactive下车窗位置记忆_副驾窗户为未知，其余窗户全开，车窗位置UB位均为0，检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.ukwn,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,0,26,26)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)
        
    @pytest.mark.sanity
    def test_caseid_1988463(self):
        """
        convience to inactive下车窗位置记忆-左后窗户为未知，右后窗户关闭，车窗UB位为0—检查降雨检测使能信号状态EnaOfflineMonitor（默认4个窗户全开）
        """
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
        self.bus_comm.set_rain_detect_sts(False)
        self.soa.hmi_set_rain_auto_close_window_sts(sts=True)
        self.soa.get_and_event_check_rain_auto_close_window_sts(sts=True)
        self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.ukwn,pos_rire=WinPos.close)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",0)
        sleep(0.5)
        self.set_windows_signal_ub_false(26,26,0,1)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehspd_gear(vehspd=3.0)
        sleep(1.5)
        self.bus_comm.check("cem_lin1","CemCem_Lin1Fr05", "EnaOfflineMonitor",1)


    # def test_caseid_ccc(self):
    #     self.io.set_five_door_sts(Door.close)
    #     self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
    #     self.soa.hmi_set_key_config_info(key_type=KeyConfigType.WindowAutoCloseOnLock,value=1)
    #     self.mix.ctrl_lock(lock_type=LockCmd.UnLock,ctrl_type=LockSource.NFC)
    #     self.bus_comm.set_windows_position(pos_drvr=WinPos.percent_100,pos_pass=WinPos.percent_100,pos_lere=WinPos.percent_100,pos_rire=WinPos.percent_100)
    #     self.mix.network_sleep()
    #     self.bus_comm.set_vehspd_gear(vehspd=3.0)  
    #     self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
    #     self.bus_comm.check_windows_position_req(pos_rire=WinPos.close)
