#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_chrglid_ctrl_abc.py
@Author      : xiangyue.li@jiduauto.com
@Time        : 2024/2/19 11:30
@Description: BGM车控车设充电口盖
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
from framework.automotive.utils.data_type import EcuInfo


@allure.feature("车控车设")
@allure.story("充电口盖")
class TestChrglidCtrlAbc(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client","DoorService_client", "TailGateService_client",
                         "ChargeLidService_client","KeyService_client","VehicleSetStatusService_client",
                         "GloveBoxService_client"])
        sleep(2)
    
    def before_each_func(self, ecu):
        self.mix.set_common_precontion(ccp={186: 0x2, 13: 0x4, 578: 0x04})
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.io.set_five_door_sts(Door.close)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.io.set_chrglid_open()
        pass

    def after_each_func(self, ecu):
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcBlkFb",0)
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.All,sts=False)
        self.bus_comm.set_chrglid_pos(127)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Ukwn)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.io.driver_seat_notpresent()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.soa.hmi_set_wash_mode(sts=isOn.Off)
        sleep(2)

    def after_class(self, ecu):
        self.sd_tester.write_ccp(ccp={13: 4})
        try:
            self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL)
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass


    @allure.title("通过HMI大屏控制打开充电口盖")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="打开充电口盖",
    )
    @pytest.mark.smoke
    @pytest.mark.verify
    def test_caseid_114693(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)


    @allure.title("503623_点击屏幕按钮关闭充电口盖")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="关闭充电口盖",
    )
    @pytest.mark.smoke
    def test_caseid_114692(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)


    @allure.title("503631_充电口盖电压过低故障")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="充电口盖电压过低故障",
    )
    @pytest.mark.smoke
    def test_caseid_1983413(self):
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.All,sts=False,time_wait=1)
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.VoltLow,sts=True)
        self.bus_comm.check_chrglid_fault_sts(sts=isOn.On)


    @allure.title("503631_充电口盖电压过高故障")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="充电口盖电压过高故障",
    )
    @pytest.mark.smoke
    def test_caseid_1983412(self):
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.All,sts=False,time_wait=1)
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.VoltHigh,sts=True)
        self.bus_comm.check_chrglid_fault_sts(sts=isOn.On)


    @allure.title("503631_充电口盖温度过高故障")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="充电口盖温度过高故障",
    )
    @pytest.mark.smoke
    def test_caseid_1983411(self):
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.All,sts=False,time_wait=1)
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.TempHigh,sts=True)
        self.bus_comm.check_chrglid_fault_sts(sts=isOn.On)



    @allure.title("503631_充电口盖执行器故障")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="充电口盖执行器故障",
    )
    @pytest.mark.smoke
    def test_caseid_114660(self):
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.All,sts=False,time_wait=1)
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.ElecErr,sts=True)
        self.bus_comm.check_chrglid_fault_sts(sts=isOn.On)



    @allure.title("503627_模式改变由Undefd到R,充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="模式改变由Undefd到R,充电口盖自动关闭",
    )
    @pytest.mark.smoke
    def test_caseid_114686(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_gear_pos(Gear.Undefd)
        # self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_gear_pos(Gear.Rvs)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)



    @allure.title("503627_模式改变由Undefd到D,充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="模式改变由Undefd到D,充电口盖自动关闭",
    )
    @pytest.mark.smoke
    def test_caseid_114685(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_gear_pos(Gear.Undefd)
        # self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_gear_pos(Gear.Drv)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)




    @allure.title("503627_模式改变由N到R,充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="模式改变由N到R,充电口盖自动关闭",
    )
    @pytest.mark.smoke
    def test_caseid_114683(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_gear_pos(Gear.Neut)
        # self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_gear_pos(Gear.Rvs)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)

    
    @allure.title("503627_模式改变由N到D,充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="模式改变由N到D,充电口盖自动关闭",
    )
    @pytest.mark.smoke
    @pytest.mark.gear_D
    def test_caseid_114682(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_gear_pos(Gear.Neut)
        # self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_gear_pos(Gear.Drv)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)



    @allure.title("503627_模式改变由P到R,充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="模式改变由P到R,充电口盖自动关闭",
    )
    @pytest.mark.smoke
    def test_caseid_114680(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_gear_pos(Gear.Park)
        # self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_gear_pos(Gear.Rvs)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)




    @allure.title("503627_模式改变由P到D,充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="模式改变由P到D,充电口盖自动关闭",
    )
    @pytest.mark.smoke
    def test_caseid_114679(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,car_mode=CarMode.NORMAL)
        self.bus_comm.set_gear_pos(Gear.Park)
        # self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_gear_pos(Gear.Drv)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)



    @allure.title("503628_拔枪充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="503628_拔枪充电口盖自动关闭",
    )
    @pytest.mark.smoke
    def test_caseid_114677(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.CONVENIENCE,car_mode=CarMode.NORMAL)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(2.9)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)

    
    @allure.title("503629_NFC闭锁,充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="503628_拔枪充电口盖自动关闭",
    )
    @pytest.mark.smoke
    def test_caseid_114669(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)

        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)

    @allure.title("诊断控制充电口盖打开")
    @pytest.mark.full
    def test_caseid_114662(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE
        )
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)#过5等级
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0x20, 0x30,0x00])
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)

    @allure.title("诊断控制充电口盖关闭")
    @pytest.mark.full
    def test_caseid_114661(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.CONVENIENCE
        )
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)#过5等级
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0x20, 0x30,0x01])
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)

    @allure.title("466169 后充电口盖状态_充电口盖开度6%-充电口盖状态Opend")
    @pytest.mark.sanity
    def test_caseid_1985261(self):
        self.sd_tester.write_ccp(ccp={13: 0x4})
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.set_chrglid_pos(6)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        
    @allure.title("466169 后充电口盖状态_充电口盖开度无效值126_充电口盖状态Ukwn")
    @pytest.mark.sanity
    def test_caseid_1985264(self):
        self.sd_tester.write_ccp(ccp={13: 0x4})
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.set_chrglid_pos(126)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Ukwn)
        
    @allure.title("466169 后充电口盖状态_充电口盖开度pos=0-充电口盖状态Clsd")
    @pytest.mark.sanity
    def test_caseid_1985267(self):
        self.sd_tester.write_ccp(ccp={13: 0x4})
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        
    @allure.title("466169 后充电口盖状态_充电口盖开度pos=4充电口盖状态Clsd")
    @pytest.mark.sanity
    def test_caseid_1985266(self):
        self.sd_tester.write_ccp(ccp={13: 0x4})
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.set_chrglid_pos(4)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        
    @allure.title("466169 后充电口盖状态_充电口盖开度pos=100-充电口盖状态Opend")
    @pytest.mark.sanity
    def test_caseid_1985262(self):
        self.sd_tester.write_ccp(ccp={13: 0x4})
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        
    @allure.title("466169 后充电口盖状态_充电口盖开度无效值101_充电口盖状态Ukwn")
    @pytest.mark.sanity
    def test_caseid_1985263(self):
        self.sd_tester.write_ccp(ccp={13: 0x4})
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.set_chrglid_pos(101)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Ukwn)
        
    @allure.title("503626 充电口盖开关动作请求_close")
    @pytest.mark.sanity
    @pytest.mark.test1121
    def test_caseid_1985273(self):
        self.sd_tester.write_ccp(ccp={578: 0x4})
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(.4)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        
    @allure.title("503626 充电口盖开关动作请求_open")
    @pytest.mark.sanity
    @pytest.mark.test1121
    def test_caseid_1985272(self):
        self.sd_tester.write_ccp(ccp={578: 0x4})
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        sleep(.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
       
        
    @allure.title("466169 后充电口盖状态_充电口盖开启角度信号不足0.1s-充电口盖状态Clsd")
    @pytest.mark.sanity
    def test_caseid_1985265(self):
        self.mix.set_common_precontion(ccp={13: 0x4})
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.set_ble_bus_siginal_charge(func_module=BleEicCharg.Charging,sub_func=BleCharging.PluggerSts,value=0)
        self.bus_comm.set_chrglid_pos(sts=6)
        sleep(0.05)
        self.bus_comm.set_chrglid_pos(sts=0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        
    # @allure.title("Lin电机故障提醒_PNC17置位3s")
    # @pytest.mark.smoke
    # def test_caseid_1985112(self):
    #     self.mix.set_common_precontion()
    #     self.bus_comm.set_singal("backbonefr","CemBackBoneFr19","ChrgLidRearFltSts",0)
    #     self.bus_comm.set_singal("backbonefr","CemBackBoneFr19","ChrgLidRearFltSts",1)
    #     self.bus_comm.check_pnc_valid_last_time(BusName.bodycan,NMMsgId.x501,BGMPNC.PNC17, 3.0)
        
    @allure.title("充电口盖故障_PNC17置位3s")
    @pytest.mark.smoke
    @pytest.mark.test1
    def test_caseid_1985111(self):
        self.mix.set_common_precontion()
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcBlkFb",0)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcBlkFb",1)
        self.bus_comm.check_pnc_valid_last_time(BusName.bodycan,NMMsgId.x501,BGMPNC.PNC17, 3.0)
    
    # @allure.title("466169 后充电口盖状态_充电口盖开启角度信号不足0.1s-充电口盖状态Clsd")
    # @pytest.mark.full
    # def test_caseid_1985268(self):
    #     self.mix.set_common_precontion(ccp={13: 0x4})
    #     # self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
    #     # self.bus_comm.set_ble_bus_siginal_charge(func_module=BleEicCharg.Charging,sub_func=BleCharging.PluggerSts,value=0)
    #     self.bus_comm.set_chrglid_pos(sts=0)
    #     self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
    #     self.bus_comm.set_chrglid_pos(sts=100)
    #     sleep(0.05)
    #     self.bus_comm.set_chrglid_pos(sts=0)
    #     self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
    @allure.title("503629_Apprch闭锁，充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="503628_拔枪充电口盖自动关闭",
    )
    @pytest.mark.full
    @pytest.mark.lock
    def test_caseid_114668(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(1)
        self.soa.hmi_set_key_config_info(key_type=KeyConfigType.AutoLockOnLeave, value=2)      
        self.bus_comm.check_singal("connectivitycanfd", "BgmConnectivityFr18", "WalkAwayLockHmi", 2)  
        self.bus_comm.send_walk_away_lock_cmd()
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Apprch, timeout=3)
        # sleep(1)  
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        
    
    @allure.title("503629_TmrAut闭锁,充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="503628_拔枪充电口盖自动关闭",
    )
    @pytest.mark.full
    @pytest.mark.lock
    def test_caseid_114666(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        self.io.set_hood_sts(HoodSts.Close)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockReqSource.Ble_Rke)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem, timeout=2)
        sleep(30)  
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.TmrAut, timeout=2)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503629_Keyls闭锁,充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="503628_拔枪充电口盖自动关闭",
    )
    @pytest.mark.full
    @pytest.mark.lock
    def test_caseid_114667(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(1)
        self.mix.push_door_outer_switch(pos=DoorPos.Dirver,time_interval=2.5)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Keyls)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503629_Telm闭锁，充电口盖自动关闭")
    @pytest.mark.lock
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="503628_拔枪充电口盖自动关闭",
    )
    @pytest.mark.full
    def test_caseid_114665(self):
        self.mix.set_common_precontion(ccp={94: 0x80})
        
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(1)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockReqSource.Talematics)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.Telm)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503629_KeyRem闭锁,充电口盖自动关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="503628_拔枪充电口盖自动关闭",
    )
    @pytest.mark.full
    def test_caseid_114664(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Unlock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.set_chrglid_pos(100)
        sleep(1)
        self.soa.hmi_set_door_close_lock(LockCmd.Lock, LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503630_交流充电_NFC闭锁，充电口盖自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990861(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503629_交流充电_充电口盖打开，120s内无插枪自动关闭")
    @pytest.mark.full
    def test_caseid_1990860(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(120)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    # @allure.title("503629_交流充电_Abandoned模式，充电口盖延时关闭")
    # @pytest.mark.sanity
    # def test_caseid_1990859(self):
    #     self.mix.set_common_precontion(
    #         car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED
    #     )
    #     self.sd_tester.write_ccp(ccp={973: 1})
    #     self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
    #     sleep(1)
    #     # self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
    #     self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
    #     self.bus_comm.set_chrglid_pos(100)
    #     sleep(115)
    #     # self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
    #     self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN2)
    #     # for i in range(15):
    #         # self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN2)
    #     #     self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    #     #     sleep(8)
    #     # self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
    #     sleep(5)
    #     self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503628_交流充电_拔枪充电口盖自动关闭")
    @pytest.mark.smoke
    def test_caseid_1990858(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        sleep(30)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流充电_模式改变由Undefd到R，充电口盖自动关闭")
    @pytest.mark.full
    def test_caseid_1990857(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Undefd)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流充电_模式改变由Undefd到D，充电口盖自动关闭")
    @pytest.mark.full
    def test_caseid_1990856(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Undefd)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流充电_模式改变由P到R，充电口盖自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990855(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流充电_模式改变由P到D，充电口盖自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990854(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流充电_模式改变由N到R，充电口盖自动关闭")
    @pytest.mark.full
    def test_caseid_1990853(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流充电_模式改变由N到D，充电口盖自动关闭")
    @pytest.mark.full
    def test_caseid_1990852(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503623_交流充电_点击屏幕按钮关闭充电口盖")
    @pytest.mark.sanity
    def test_caseid_1990850(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("503630_交流充电_插枪NFC闭锁，充电口盖不关闭")
    @pytest.mark.sanity
    def test_caseid_1990849(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        sleep(0.1)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("503629_交流充电_充电口盖打开，120s内插枪不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990848(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(60)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        sleep(60)
        self.mix.wait_time_in_chrgild_req(num=20, req=ChrgLidReq.Idle)
    
    @allure.title("503629_交流充电_Abandoned模式，120s内插枪充电口盖不触发延时关闭")
    @pytest.mark.full
    @pytest.mark.test1121
    def test_caseid_1990847(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        sleep(1)
        # self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(60)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        sleep(55)
        self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN2)
        sleep(5)
        # self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        # sleep(0.1)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("503628_交流充电_不拔枪充电口盖不自动关闭")
    @pytest.mark.smoke
    def test_caseid_1990846(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        sleep(3)
        sleep(0.1)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流充电_插枪_模式改变由Undefd到R，充电口盖不触发自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990845(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Undefd)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流充电_插枪_模式改变由Undefd到D，充电口盖不触发自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990844(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Undefd)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流充电_插枪_模式改变由P到R，充电口盖不触发自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990843(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流充电_插枪_模式改变由P到D，充电口盖不触发自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990842(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流充电_插枪_模式改变由N到R，充电口盖不触发自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990841(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流充电_插枪_模式改变由N到D，充电口盖不触发自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990840(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    
    @allure.title("503623_交流充电_插枪_点击屏幕按钮不触发关闭充电口盖")
    @pytest.mark.sanity
    def test_caseid_1990838(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503630_交流或直流充电_NFC闭锁，充电口盖自动关闭")
    @pytest.mark.full
    def test_caseid_1990837(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503629_交流或直流充电_充电口盖打开，120s内无插枪自动关闭")
    @pytest.mark.full
    def test_caseid_1990836(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(120)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    # @allure.title("503629_交流或直流充电_Abandoned模式，充电口盖延时关闭")
    # @pytest.mark.full
    # @pytest.mark.test1121
    # def test_caseid_1990835(self):
    #     self.mix.set_common_precontion(
    #         car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED
    #     )
    #     self.sd_tester.write_ccp(ccp={973: 2})
    #     self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
    #     self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
    #     self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
    #     self.bus_comm.set_chrglid_pos(100)
    #     sleep(115)
    #     self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN2)
    #     sleep(5)
    #     # self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
    #     self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503628_交流或直流充电_拔直流枪充电口盖自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990834(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(3)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503628_交流或直流充电_拔交流枪充电口盖自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990833(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        sleep(3)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流或直流充电_模式改变由Undefd到R，充电口盖自动关闭")
    @pytest.mark.full
    def test_caseid_1990832(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Undefd)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流或直流充电_模式改变由Undefd到D，充电口盖自动关闭")
    @pytest.mark.full
    def test_caseid_1990831(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Undefd)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流或直流充电_模式改变由P到R，充电口盖自动关闭")
    @pytest.mark.full
    def test_caseid_1990830(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流或直流充电_模式改变由P到D，充电口盖自动关闭")
    @pytest.mark.sanity
    def test_caseid_1990829(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流或直流充电_模式改变由N到R，充电口盖自动关闭")
    @pytest.mark.full
    def test_caseid_1990828(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503627_交流或直流充电_模式改变由N到D，充电口盖自动关闭")
    @pytest.mark.full
    def test_caseid_1990827(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    
    @allure.title("503623_交流或直流充电_点击屏幕按钮关闭充电口盖")
    @pytest.mark.full
    def test_caseid_1990825(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("503630_交流或直流充电_插交流枪_NFC闭锁，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990824(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503629_交流或直流充电_插交流枪_充电口盖打开，120s内插枪不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990823(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(60)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        sleep(60)
        self.mix.wait_time_in_chrgild_req(num=20, req=ChrgLidReq.Idle)
    
    @allure.title("503629_交流或直流充电_插交流枪_Abandoned模式，120s内插枪充电口盖不触发延时关闭")
    @pytest.mark.full
    @pytest.mark.test1121
    def test_caseid_1990822(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        # self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(60)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        sleep(55)
        self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN2)
        sleep(5)
        # self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("503628_交流或直流充电_插交流枪_不拔交流枪充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990821(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        sleep(3)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插交流枪_模式改变由Undefd到R，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990820(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Undefd)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插交流枪_模式改变由Undefd到D，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990819(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Undefd)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插交流枪_模式改变由P到R，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990818(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插交流枪_模式改变由P到D，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990817(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插交流枪_模式改变由N到R，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990816(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插交流枪_模式改变由N到D，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990815(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    
    @allure.title("503623_交流或直流充电_插交流枪_点击屏幕按钮不触发关闭充电口盖")
    @pytest.mark.full
    def test_caseid_1990813(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503630_交流或直流充电_插直流枪_NFC闭锁，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990812(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503629_交流或直流充电_插直流枪_充电口盖打开，120s内插枪不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990811(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(60)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        sleep(60)
        self.mix.wait_time_in_chrgild_req(num=20, req=ChrgLidReq.Idle)
    
    @allure.title("503629_交流或直流充电_插直流枪_充电口盖打开，120s内插枪不触发自动关闭")
    @pytest.mark.full
    @pytest.mark.test1121
    def test_caseid_1990810(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        # self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(60)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        sleep(55)
        self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN2)
        sleep(5)
        # self.mix.ctrl_lock(lock_type=LockCmd.Lock,ctrl_type=LockSource.NFC)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("503628_交流或直流充电_插直流枪_不拔直流枪充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990809(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        sleep(3)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插直流枪_模式改变由Undefd到R，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990808(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Undefd)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插直流枪_模式改变由Undefd到D，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990807(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Undefd)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插直流枪_模式改变由P到R，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990806(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插直流枪_模式改变由P到D，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990805(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插直流枪_模式改变由N到R，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990804(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("503627_交流或直流充电_插直流枪_模式改变由N到D，充电口盖不触发自动关闭")
    @pytest.mark.full
    def test_caseid_1990803(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        sleep(3)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        self.bus_comm.set_gear_pos(gear=Gear.Neut)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    
    @allure.title("503623_交流或直流充电_插直流枪_点击屏幕按钮不触发关闭充电口盖")
    @pytest.mark.full
    def test_caseid_1990801(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)
    
    @allure.title("705348_服务关闭充电口盖,DID打开")
    @pytest.mark.full
    def test_caseid_1987472(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)#过5等级
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0x20, 0x30,0x00])
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("705348_服务打开充电口盖,DID关闭")
    @pytest.mark.full
    def test_caseid_1987469(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L5)#过5等级
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0x20, 0x30,0x01])
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("503626 充电口盖开关动作请求_close")
    @pytest.mark.sanity
    def test_caseid_1985273(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("503626 充电口盖开关动作请求_open")
    @pytest.mark.sanity
    def test_caseid_1985272(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    # @allure.title("充电口盖DTC卡滞故障-A02F90")
    # @pytest.mark.full
    # def test_caseid_1982530(self):
    #     self.bus_comm.set_dtc_pre()
    #     sleep(1)
    #     self.mix.set_usage_mode(UsageMode.DRIVING)
    #     sleep(7)
    #     self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
    #     self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=True)
    #     sleep(1)
    #     result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
    #     self.sd_tester.check_dtc(result, [160,47,144], status1)
    #     self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=False)
    #     sleep(1)
    #     self.sd_tester.send_dtc_request_and_check_dtc_status([160,47,144], status2)
    
    # @allure.title("充电口盖DTC电路故障-A02F10")
    # @pytest.mark.full
    # def test_caseid_1982529(self):
    #     self.bus_comm.set_dtc_pre()
    #     sleep(1)
    #     self.mix.set_usage_mode(UsageMode.DRIVING)
    #     sleep(7)
    #     self.bus_comm.check_pwrlvlelec(mai=0, subtype=0)
    #     self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.ElecErr,sts=True)
    #     sleep(1)
    #     result, status1, status2 = self.sd_tester.send_dtc_request_and_return_check_status()
    #     self.sd_tester.check_dtc(result, [160,47,16], status1)
    #     self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.ElecErr,sts=False)
    #     sleep(1)
    #     self.sd_tester.send_dtc_request_and_check_dtc_status([160,47,16], status2)
    
    @allure.title("466169 后充电口盖状态_CCP不满足_充电口盖状态Close")
    @pytest.mark.sanity
    def test_caseid_114699(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.3)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.sd_tester.write_ccp(ccp={13: 1})
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        self.sd_tester.write_ccp(ccp={13: 4})
    
    @allure.title("503626_在打开期间收到新的请求，立刻发送请求")
    @pytest.mark.full
    def test_caseid_114698(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.DRIVING
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1)
        self.bus_comm.set_chrglid_pos(10)
        sleep(0.3)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        
    @allure.title("503623_点击屏幕按钮打开充电口盖1")
    @pytest.mark.full
    def test_caseid_114694(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("503628_拔枪后充电口盖取消发送关闭请求1")
    @pytest.mark.full
    def test_caseid_114676(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        sleep(0.5)
        self.mix.wait_time_in_chrgild_req(num=30, req=ChrgLidReq.Idle)
    
    @allure.title("503628_拔枪后充电口盖取消发送关闭请求2")
    @pytest.mark.full
    def test_caseid_114675(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_chrglid_pos(0)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        self.mix.wait_time_in_chrgild_req(num=30, req=ChrgLidReq.Idle)
    
    @allure.title("503629_充电口盖打开，120s内无插枪自动关闭")
    @pytest.mark.full
    def test_caseid_114674(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        sleep(120)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
    
    @allure.title("503629_充电口盖打开后，120s内切换为Close，取消发送关闭请求")
    @pytest.mark.full
    def test_caseid_114673(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        sleep(60)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        sleep(55)
        self.mix.wait_time_in_chrgild_req(num=50, req=ChrgLidReq.Idle)
    
    @allure.title("503632_充电口盖矩阵请求")
    @pytest.mark.full
    def test_caseid_114670(self):
        self.bus_comm.check_ChrgLidManvgDCorAcDc_TqReq2(tqreq2=ActTq.NominalTorque)
    
    @allure.title("503633_校准充电口盖")
    @pytest.mark.full
    def test_caseid_114663(self):
        self.bus_comm.check_ChrgLidManvgDCorAcDc_TqReq2(tqreq2=ActTq.NominalTorque)
        self.sd_tester.unlock_and_check(TA.BGM_MCU,SESSION.EXTENDED,UnLock.L0)
        self.sd_tester.send_request_and_recv_response([0x31, 0x01, 0x20, 0x31])
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Active)
        sleep(0.5)
        self.bus_comm.check_ChrgLidManvgDCorAcDc_CalReq2(Req2=Inact.Inactive)
    
    @allure.title("503631_充电口盖故障警告2")
    @pytest.mark.full
    def test_caseid_114659(self):
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.All,sts=True,time_wait=1)
        self.bus_comm.check_chrglid_fault_sts(sts=isOn.On)
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.All,sts=False,time_wait=1)
        self.bus_comm.check_chrglid_fault_sts(sts=isOn.Off)
    
    @allure.title("1995260_开关按钮打开充电口盖")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995260(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(2.0)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
    
    @allure.title("503622_车外硬线开关控制充电口盖_open to close")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995261(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        sleep(2.0)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503622_车外硬线开关控制充电口盖_打开（闭锁检测钥匙）")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995267(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        for value in  [2, 3, 4, 5, 6, 10, 11]:
            self.bus_comm.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, value)])
            sleep(2.0)
            self.io.set_chrglid_close()
            self.io.set_chrglid_open()           
            if self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open):
                logger.info("key_id1:{}".format(value))

    @allure.title("503622_车外硬线开关控制充电口盖_反向主驾占位打开失败")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995268(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(2.0)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        self.io.driver_seat_present()
        self.bus_comm.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x2)])
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)


    @allure.title("503622_车外硬线开关控制充电口盖_反向挡位D挡打开失败")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995269(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(2.0)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503622_车外硬线开关控制充电口盖_反向挡位R挡打开失败")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995270(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(2.0)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503622_车外硬线开关控制充电口盖_关闭反向_插交流枪")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995271(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        sleep(2.0)
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithoutPower)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503622_车外硬线开关控制充电口盖_关闭反向_插直流枪")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995272(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithoutPower)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        sleep(2.0)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503622_车外硬线开关控制充电口盖_ukwn to close")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995303(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(255)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Ukwn)
        sleep(2.0)
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.NFC)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503622_车外硬线开关控制充电口盖_挡位R挡500ms变为P档")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995304(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(2.0)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503622_车外硬线开关控制充电口盖_挡位D挡500ms变为P档")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995345(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(2.0)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503622_车外硬线开关控制充电口盖_关闭（禁用）")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995346(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        sleep(2.0)
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503622_车外硬线开关控制充电口盖_打开（禁用）")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995347(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(2.0)
        self.soa.hmi_set_wash_mode(sts=isOn.On)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)  

    @allure.title("503622_车外硬线开关控制充电口盖_open to close（超时关闭）")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995349(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(2.0)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        sleep(120)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)

    @allure.title("拔枪后充电口盖等待时间_开关请求")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995350(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(2.0)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithoutPower)
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)

    @allure.title("503622_车外硬线开关控制充电口盖_打开（车辆非静止）")
    @pytest.mark.full
    @pytest.mark.test1029
    def test_caseid_1995446(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(2.0)
        self.bus_comm.set_vehmtn(VehMtnSts.FwdVal1)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)
        
    @allure.title("503622_车外硬线开关控制充电口盖_锁车500ms变为解锁")
    @pytest.mark.full
    @pytest.mark.test1031
    def test_caseid_1995447(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(2.0)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Telm)
        self.io.set_chrglid_close()
        self.mix.ctrl_lock(lock_type=LockCmd.UnLock, ctrl_type=LockSource.Telm)
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)

    @allure.title("503622_车外硬线开关控制充电口盖_挡位D挡500ms超时变为P档")
    @pytest.mark.full
    @pytest.mark.test1102
    def test_caseid_1995448(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_gear_pos(gear=Gear.Drv)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        sleep(2.0)
        self.io.set_chrglid_close()
        self.bus_comm.check_ChrgLidDCorAcDctSwt_Req(1)
        self.io.set_chrglid_open()
        self.bus_comm.check_ChrgLidDCorAcDctSwt_Req(0)
        sleep(0.6)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_without_chrglid_req(req=127)

    @allure.title("503622_车外硬线开关控制充电口盖_挡位R挡500ms超时变为P档")
    @pytest.mark.full
    @pytest.mark.test1031
    def test_caseid_1995449(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        sleep(2.0)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.io.set_chrglid_close()
        self.bus_comm.check_ChrgLidDCorAcDctSwt_Req(1)
        self.io.set_chrglid_open()
        self.bus_comm.check_ChrgLidDCorAcDctSwt_Req(0)
        sleep(0.6)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        self.bus_comm.check_without_chrglid_req(req=127)

    @allure.title("503622_车外硬线开关控制充电口盖_打开（锁车内锁）")
    @pytest.mark.full
    @pytest.mark.test1031
    def test_caseid_1995450(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.HMI)
        sleep(2.0)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)

    @allure.title("503622_车外硬线开关控制充电口盖_打开（锁车外锁）")
    @pytest.mark.full
    @pytest.mark.test1102
    def test_caseid_1995451(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Telm)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(2.0)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)

    @allure.title("503622_车外硬线开关控制充电口盖_打开（尾门解锁）")
    @pytest.mark.full
    @pytest.mark.test1031
    def test_caseid_1995452(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        sleep(2.0)
        self.soa.hmi_set_tailgate_mode(TailGateMode.Open)
        self.io.set_door(Trunk=Door.open)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.TrUnlock, exp_trigsrc=LockTrigerSource.IntrSwt)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)

    @allure.title("503622_车外硬线开关控制充电口盖_打开（关闭状态小于2S）")
    @pytest.mark.full
    @pytest.mark.test1031
    def test_caseid_1995454(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_without_chrglid_req(req=127)

    @allure.title("503622_车外硬线开关控制充电口盖_打开（关闭状态大于2S）")
    @pytest.mark.full
    @pytest.mark.test1031
    def test_caseid_1995455(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        sleep(1)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(2)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)

    @allure.title("503622_车外硬线开关控制充电口盖_close插枪")
    @pytest.mark.full
    @pytest.mark.test1031
    def test_caseid_1995672(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithoutPower)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)

    @allure.title("503622_车外硬线开关控制充电口盖_close再次请求打开")
    @pytest.mark.full
    @pytest.mark.test1031
    def test_caseid_1995673(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503622_车外硬线开关控制充电口盖_close再次插枪")
    @pytest.mark.full
    @pytest.mark.test1031
    def test_caseid_1995674(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithoutPower)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)

    @allure.title("503622_车外硬线开关控制充电口盖_close服务请求打开")
    @pytest.mark.full
    @pytest.mark.test1031
    def test_caseid_1995675(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 0})
        self.sd_tester.write_ccp(ccp={578: 4})
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.io.set_chrglid_close()
        self.io.set_chrglid_open()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)  
#//////////////////////////////////2.2CR MPU还未合入///////////////////////////////////////////////
    @allure.title("设置拔枪充电口盖自动关闭时间_121s")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995212(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(30.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(30.0)
        sleep(0.2)
        self.soa.set_SetGunPullOutCharge_req(121.0,1)
        sleep(0.2)
        self.bus_comm.check_SetClsChargeLidTiSts_value(30.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False) 
        sleep(30.0)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("设置拔枪充电口盖自动关闭时间_120s")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995213(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(30.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(30.0)
        sleep(0.2)
        self.soa.set_SetGunPullOutCharge_req(120.0)
        sleep(0.2)
        self.bus_comm.check_SetClsChargeLidTiSts_value(120.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False) 
        sleep(120.0)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        self.soa.set_SetGunPullOutCharge_req(30.0)

    @allure.title("设置拔枪充电口盖自动关闭时间_10s")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995214(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(30.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(30.0)
        sleep(0.2)
        self.soa.set_SetGunPullOutCharge_req(10.0)
        sleep(0.2)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False) 
        sleep(10.0)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("设置拔枪充电口盖自动关闭时间_0s")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995215(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(30.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(30.0)
        sleep(0.2)
        self.soa.set_SetGunPullOutCharge_req(0.0)
        sleep(0.2)
        self.bus_comm.check_SetClsChargeLidTiSts_value(0.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False) 
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503629_Abandoned模式，充电口盖取消发送关闭请求")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_114671_114673(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN2)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_chrglid_pos(0)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        sleep(1.5)
        self.bus_comm.set_chrglid_pos(100)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=120)

    @allure.title("503629_Abandoned模式，充电口盖延时关闭")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_114672_114674(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.ABANDONED)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.lin_send_pwm(lin_bus=LinChannel.LIN2)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.5)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=120)

    @allure.title("拔枪后插枪充电口盖不关闭_拔交流枪插直流枪")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995199(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.5)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=5)
    
    @allure.title("拔枪后插枪充电口盖不关闭_拔交流枪插交流枪")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995200(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.5)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=5)

    @allure.title("拔枪后插枪充电口盖不关闭_拔直流枪插直流枪")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995201(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.5)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=5)

    @allure.title("拔枪后插枪充电口盖不关闭_拔直流枪插交流枪")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995202(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.5)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=5)

    @allure.title("拔枪后插枪重置充电口盖等待时间_拔交流枪插直流枪")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995203(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.5)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=5)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=3)

    @allure.title("拔枪后插枪重置充电口盖等待时间_拔交流枪插交流枪")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995204(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.5)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=5)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=3)

    @allure.title("拔枪后插枪重置充电口盖等待时间_拔指流枪插交流枪")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995205(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.5)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=5)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=3)
    
    @allure.title("拔枪后插枪重置充电口盖等待时间_拔直流枪插直流枪")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995206(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.5)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=5)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=3)

    @allure.title("SetClsChargeLidTiSts的存储_诊断重启")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995207(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.soa.set_SetGunPullOutCharge_req(10.0)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.sd_tester.reboot_bgm_by_diag_hardreset()
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=6)

    @allure.title("SetClsChargeLidTiSts的存储_上下电")
    @pytest.mark.full
    @pytest.mark.test1108
    def test_caseid_1995208(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.soa.set_SetGunPullOutCharge_req(10.0)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.io.bgm_power_off()
        self.io.bgm_power_on()
        sleep(30)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=6) 

    @allure.title("SetClsChargeLidTiSts的存储_休眠唤醒")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995209(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=True,isAConnect=False, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.soa.set_SetGunPullOutCharge_req(10.0)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.mix.network_sleep()
        self.mix.network_wakeup(wakeup_reason=Wakeup_Reasons.WAKEUP_BY_BODYCAN)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=6)

    @allure.title("拔枪后等待SetClsChargeLidTiSts后关充电口盖_拔交流枪")
    @pytest.mark.full
    @pytest.mark.test1107
    def test_caseid_1995210(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(5.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(5.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=6)

    @allure.title("拔枪后充电口盖等待时间_HMI请求")
    @pytest.mark.full
    @pytest.mark.test1108
    def test_caseid_1995273(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(10.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(1.0)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=10)

    @allure.title("拔枪后充电口盖等待时间_挡位变化")
    @pytest.mark.full
    @pytest.mark.test1108
    def test_caseid_1995274(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(10.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.set_gear_pos(gear=Gear.Rvs)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.set_gear_pos(gear=Gear.Park)
        sleep(1.0)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=10)
        #self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=10)

    @allure.title("拔枪后充电口盖等待时间_锁车请求")
    @pytest.mark.full
    @pytest.mark.test1108
    def test_caseid_1995276(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(10.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Telm)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(1.0)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=10)


    @allure.title("拔枪后充电口盖等待时间_重新设置时间减少")
    @pytest.mark.full
    @pytest.mark.test1115
    def test_caseid_1995277(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(10.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.soa.set_SetGunPullOutCharge_req(2.0)
        self.bus_comm.check_SetClsChargeLidTiSts_value(2.0)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=2)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=7)


    @allure.title("拔枪后充电口盖等待时间_重新设置时间增大")
    @pytest.mark.full
    @pytest.mark.test1115
    def test_caseid_1995278(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(10.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.soa.set_SetGunPullOutCharge_req(20.0)
        self.bus_comm.check_SetClsChargeLidTiSts_value(20.0)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=9)
        sleep(1.0)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=13)

    @allure.title("拔枪后充电口盖等待时间_重新设置时间下次生效")
    @pytest.mark.full
    @pytest.mark.test1115
    def test_caseid_1995280(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(10.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=3)
        self.soa.set_SetGunPullOutCharge_req(20.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(20.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.check_without_chrglid_req(req=127,timeout=12)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=10)

    @allure.title("拔枪后充电口盖等待时间_蓝牙请求")
    @pytest.mark.full
    @pytest.mark.test1108
    def test_caseid_1995445(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(10.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock,source=LockSource.RKE)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(1.0)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=10)

#///////////////////////////////////////////////////单域case/////////////////////////////////////////////////////////
@allure.feature("车控车设")
@allure.story("充电口盖控制")
@pytest.mark.test1101
class TestDoorOpenerCtrlAbc(TestABCBase):
    def change_bench_config(ecu:EcuInfo) -> EcuInfo:
        ecu.domain.single_bgm = True
        ecu.domain.two_domain = False
        ecu.tc_config["dut_ecu"] = ["BGM"]
        return ecu
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client","DoorService_client", "TailGateService_client",
                         "ChargeLidService_client","KeyService_client","VehicleSetStatusService_client",
                         "GloveBoxService_client"])
        sleep(2)

    def before_each_func(self, ecu):
        self.mix.set_common_precontion(ccp={186: 0x2, 13: 0x4, 578: 0x04})
        self.io.set_five_door_sts(Door.close)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL, vehmtnst=VehMtnSts.StandStillVal2)
        self.soa.hmi_set_door_close_lock(LockCmd.UnLock, LockSource.RKE)
        sleep(3)  # 防止开关触发热保护

    def after_each_func(self, ecu):
        sleep(2)

    def after_class(self, ecu):
        self.bus_comm.centrl_lock_pre_msg_send_ctrl(sts=MsgSendContrl.Start)
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    
    @allure.title("503624_APP控制充电口盖关闭")
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/1234?projectId=46",
        name="	503624_APP控制充电口盖关闭")
    @pytest.mark.smoke
    @pytest.mark.single_bgm
    def test_caseid_114689(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 0})
        # self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Ukwn)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        
    @allure.title("503624_交流充电_APP控制充电口盖关闭")
    @pytest.mark.sanity
    @pytest.mark.single_bgm
    def test_caseid_1990851(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Ukwn)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("拔枪后充电口盖等待时间_APP请求")
    @pytest.mark.full
    @pytest.mark.single_bgm
    @pytest.mark.test1108
    def test_caseid_1995275(self):
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE)
        self.sd_tester.write_ccp(ccp={973: 2})
        self.soa.set_SetGunPullOutCharge_req(10.0)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=True, isPrivate=False)
        self.bus_comm.check_SetClsChargeLidTiSts_value(10.0)
        self.bus_comm.set_JiDUCharging(isDConnect=False,isAConnect=False, isPrivate=False)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Ukwn)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close, timeout=10)

    @allure.title("503624_交流或直流充电_插直流枪_APP控制充电口盖关闭_充电枪链接状态_不触发关闭请求")
    @pytest.mark.full
    @pytest.mark.single_bgm
    @pytest.mark.test1121
    def test_caseid_1990802(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Close)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)

    @allure.title("503624_APP控制充电口盖开启_usagemode=Driving_不发open请求")
    @pytest.mark.smoke
    @pytest.mark.single_bgm
    @pytest.mark.test1121
    def test_caseid_114690(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal3,ccp={578: 0x4})
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        
    @allure.title("503624_APP控制充电口盖开启_非P OR N档_充电口盖open不发")
    @pytest.mark.sanity
    @pytest.mark.single_bgm
    @pytest.mark.test1121
    def test_caseid_1985286(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal3,ccp={578: 0x4})
        self.bus_comm.set_vehspd_gear(gear=Gear.Rvs)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        
    @allure.title("503624_APP控制充电口盖开启_P档&&车辆静止_充电口盖open")
    @pytest.mark.smoke
    @pytest.mark.single_bgm
    @pytest.mark.test1121
    def test_caseid_1985285(self):
        self.mix.set_common_precontion(vehmtnst=VehMtnSts.StandStillVal3,ccp={578: 0x4})
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        
    @allure.title("503624_APP控制充电口盖开启_N档&&车辆静止_充电口盖open")
    @pytest.mark.sanity
    @pytest.mark.single_bgm
    @pytest.mark.test1121
    def test_caseid_114691(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED, vehmtnst=VehMtnSts.StandStillVal3,ccp={578: 0x4})
        self.bus_comm.set_vehspd_gear(gear=Gear.Neut)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        
    @allure.title("503624_APP控制充电口盖开启_车辆非静止_充电口盖open请求不发")
    @pytest.mark.full
    @pytest.mark.single_bgm
    @pytest.mark.test1121
    def test_caseid_1985287(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING, vehmtnst=VehMtnSts.StandStillVal1,ccp={578: 0x4})
        self.bus_comm.set_vehspd_gear(gear=Gear.Park)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        
    @allure.title("503624_APP控制充电口盖关闭_车辆处于Drving模式_关闭请求忽略")
    @pytest.mark.sanity
    @pytest.mark.single_bgm
    @pytest.mark.test1121
    def test_caseid_1985288(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.DRIVING,ccp={13: 0x4})
        self.bus_comm.set_ble_bus_siginal_charge(func_module=BleEicCharg.Charging,sub_func=BleCharging.PluggerSts,value=0)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        
    @allure.title("503624_APP控制充电口盖关闭_充电枪链接状态_关闭请求忽略")
    @pytest.mark.sanity
    @pytest.mark.single_bgm
    @pytest.mark.test1121
    def test_caseid_1985289(self):
        self.mix.set_common_precontion(usage_mode=UsageMode.ABANDONED,ccp={13: 0x4})
        self.bus_comm.set_ble_bus_siginal_charge(func_module=BleEicCharg.Charging,sub_func=BleCharging.PluggerSts,value=0)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Open)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503624_交流充电_插枪_APP控制充电口盖关闭_充电枪链接状态_不触发关闭请求")
    @pytest.mark.sanity
    @pytest.mark.single_bgm
    @pytest.mark.test1121
    def test_caseid_1990839(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 1})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Close)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)

    @allure.title("503624_交流或直流充电_APP控制充电口盖关闭")
    @pytest.mark.full
    @pytest.mark.single_bgm
    @pytest.mark.test1121
    def test_caseid_1990826(self):
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcBlkFb",0)
        self.bus_comm.set_singal("cem_lin2","PrldCem_Lin2Fr02","ChrgLidManvgDCorAcDcBlkFb",1)
        self.bus_comm.set_chrglid_fault(fault_type=ChrdLidFaultType.ElecErr,sts=True)
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        sleep(0.5)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)

    @allure.title("503624_交流或直流充电_插交流枪_APP控制充电口盖关闭_充电枪链接状态_不触发关闭请求")
    @pytest.mark.full
    @pytest.mark.single_bgm
    @pytest.mark.test1121
    def test_caseid_1990814(self):
        self.mix.set_common_precontion(
            car_mode=CarMode.NORMAL, usage_mode=UsageMode.INACTIVE
        )
        self.sd_tester.write_ccp(ccp={973: 2})
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.ConnectedWithPower)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_chrglid_pos(100)
        sleep(0.2)
        self.bus_comm.telm_set_chrglid_sts(sts=ChrgLidOpenCloseSts.Close)
        self.mix.wait_time_in_chrgild_req(num=10, req=ChrgLidReq.Idle)