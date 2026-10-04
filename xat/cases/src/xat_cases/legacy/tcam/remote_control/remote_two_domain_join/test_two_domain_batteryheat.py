#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import pytest
import allure
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("远程控制/远控两域联调测试/远控电池预加热")
@allure.story("远控电池预加热")
class TestRvcBattHeat(TestABCBase):
    def before_class(self, ecu):
        pass

    def before_each_func(self, ecu):
        self.bus_comm.set_singal("backbonefr","BcmVddmBackBoneFr00","VehMtnStVehMtnSt_0_BcmVddmBackBoneSignalIPdu00","VehMtnSt2_StandStillVal3")
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr18", "TrsmParkLockdTrsmParkLockd", 'TrsmParkLock1_ParkEngd')
        self.bus_comm.set_singal("backbonefr","VddmBackBoneFr03", "GearLvrIndcn_1_EcmPropSignalIPdu24",'GearLvrIndcn2_ParkIndcn')  
         
    def after_each_func(self, ecu):
        self.bus_comm.set_singal("propulsioncan","BecmPropFr09", "HvBattTMin", 300) 
        pass

    def after_class(self, ecu):
        pass


    @allure.title("远程控制-RVC_远控电池预加热B方案预约执行_abandoned")
    @pytest.mark.join_smoke
    def test_battery_heat_caseid_1980526(self):
        self.mix.network_sleep()
        with allure.step("下发远控电池预加热指令"): 
            appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd() 
        # 模拟电池最低温度
        self.bus_comm.set_singal("propulsioncan","BecmPropFr09", "HvBattTMin", -130)    
        time.sleep(0.1) 
        #表显soc
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04", "DispHvBattLvlOfChrg", 200) 
        time.sleep(0.1)
        #充电枪连接状态
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", "DCChrgnHndlSts", 0) 
        time.sleep(0.1)
        #模拟上高压
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01", "HvSysRlyStsHvSysRlySts","HvActvnSts_Clsd") 
        time.sleep(3) 
        #模拟电池热管理状态(需要跳变)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Default")
        time.sleep(2)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Heating")
        assert self.tsp.log_search_battery(execid=exec_id, keyword="Success"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"



    @allure.title("远程控制-RVC_远控电池预加热B方案预约执行_inactive")
    @pytest.mark.join_smoke
    def test_battery_heat_caseid_1980529(self):
        # 模拟电池最低温度
        self.bus_comm.set_singal("propulsioncan","BecmPropFr09", "HvBattTMin", -130)    
        time.sleep(0.1) 
        with allure.step("下发远控电池预加热指令"): 
            appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd() 
        #表显soc
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04", "DispHvBattLvlOfChrg", 200) 
        time.sleep(0.1)
        #充电枪连接状态
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", "DCChrgnHndlSts", 0) 
        time.sleep(0.1)
        #模拟上高压
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01", "HvSysRlyStsHvSysRlySts","HvActvnSts_Clsd") 
        time.sleep(3) 
        #模拟电池热管理状态(需要跳变)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Default")
        time.sleep(2)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Heating")
        assert self.tsp.log_search_battery(execid=exec_id, keyword="Success"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"


	
    @allure.title("远程控制-RVC_远控电池包立即加热_inactive")
    @pytest.mark.join_smoke
    def test_battery_heat_caseid_1990625(self):
        # 模拟电池最低温度
        self.bus_comm.set_singal("propulsioncan","BecmPropFr09", "HvBattTMin", 170)    
        time.sleep(0.1) 
        with allure.step("下发电池立即加热开启指令"): 
            execid = self.tsp.rvc_realtime_battery_heat()
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=60)  
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120) 
        #表显soc
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04", "DispHvBattLvlOfChrg", 200) 
        time.sleep(0.1)
        #充电枪连接状态
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", "DCChrgnHndlSts", 0) 
        time.sleep(0.1)
        #模拟上高压
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01", "HvSysRlyStsHvSysRlySts","HvActvnSts_Clsd") 
        time.sleep(3) 
        #模拟电池热管理状态(需要跳变)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Default")
        time.sleep(2)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Heating")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        time.sleep(10)
        with allure.step("下发电池立即加热关闭指令"): 
            execid01 = self.tsp.rvc_realtime_battery_heat(op=-1) 
        #模拟电池热管理状态
        time.sleep(1)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Inhibited")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid01),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远程控制-RVC_远控电池包立即加热_abandoned")
    @pytest.mark.join_smoke
    def test_battery_heat_caseid_1990626(self):
        #台架休眠
        self.mix.network_sleep()
        with allure.step("下发电池立即加热开启指令"): 
            execid = self.tsp.rvc_realtime_battery_heat() 
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=60)  
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509,pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=120) 
        # 模拟电池最低温度
        self.bus_comm.set_singal("propulsioncan","BecmPropFr09", "HvBattTMin", 170)    
        time.sleep(0.1) 
        #表显soc
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04", "DispHvBattLvlOfChrg", 200) 
        time.sleep(0.1)
        #充电枪连接状态
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", "DCChrgnHndlSts", 0) 
        time.sleep(0.1)
        #模拟上高压
        self.bus_comm.set_singal("propulsioncan","BecmPropFr01", "HvSysRlyStsHvSysRlySts","HvActvnSts_Clsd") 
        time.sleep(3) 
        #模拟电池热管理状态(需要跳变)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Default")
        time.sleep(2)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Heating")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        time.sleep(10)
        with allure.step("下发电池立即加热关闭指令"): 
            execid01 = self.tsp.rvc_realtime_battery_heat(op=-1) 
        #模拟电池热管理状态
        time.sleep(1)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Inhibited")
        assert self.tsp.log_search_remote_vehicle_control(execid=execid01),f"TCAM远程控制上报到车云的结果校验失败"



    @allure.title("远程控制-RVC_远控电池预加热A方案预约执行_inactive")
    @pytest.mark.join_smoke
    def test_battery_heat_caseid_1990687(self):
        #模拟私桩
        self.bus_comm.set_singal("connectivitycanfd","BncmBsrmConnectivityFr03", "ChrgrPileInfo", 1) 
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", "DCChrgnHndlSts", 3) 
        # 模拟电池最低温度
        self.bus_comm.set_singal("propulsioncan","BecmPropFr09", "HvBattTMin", 170)    
        time.sleep(1) 
        with allure.step("下发远控电池预加热指令"): 
            appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd() 
        #表显soc
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04", "DispHvBattLvlOfChrg", 200) 
        time.sleep(0.1)
        #充电枪连接状态
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", "DCChrgnHndlSts", 3) 
        time.sleep(0.1)
        #模拟电池热管理状态(需要跳变)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Default")
        time.sleep(2)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Heating")
        assert self.tsp.log_search_battery(execid=exec_id, keyword="Success"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"



    @allure.title("远程控制-RVC_远控电池预加热A方案预约执行_abandoned")
    @pytest.mark.join_smoke
    def test_battery_heat_caseid_1990688(self):
        #台架休眠
        self.mix.network_sleep()
        with allure.step("下发远控电池预加热指令"): 
            appointment_time, formattedUseVehicleTime,exec_id = self.tsp.rvc_taskCmd() 
        #模拟私桩
        self.bus_comm.set_singal("connectivitycanfd","BncmBsrmConnectivityFr03", "ChrgrPileInfo", 1) 
        time.sleep(0.1) 
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", "DCChrgnHndlSts", 3) 
        # 模拟电池最低温度
        self.bus_comm.set_singal("propulsioncan","BecmPropFr09", "HvBattTMin", 170)    
        time.sleep(1) 
        #表显soc
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04", "DispHvBattLvlOfChrg", 200) 
        time.sleep(0.1)
        #充电枪连接状态
        self.bus_comm.set_singal("propulsioncan","BecmPropFr15", "DCChrgnHndlSts", 3) 
        time.sleep(0.1)
        #模拟电池热管理状态(需要跳变)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Default")
        time.sleep(2)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr22", "HvBattThermReqFb", "HvBattThermReqFb_Heating")
        assert self.tsp.log_search_battery(execid=exec_id, keyword="Success"), f"TCAM远程电池预约执行结果上报到车云的结果校验失败"

