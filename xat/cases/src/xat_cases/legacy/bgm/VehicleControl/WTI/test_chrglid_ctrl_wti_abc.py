#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_chrglid_ctrl_abc.py
@Author      : liqi.yin_ext@jiduauto.com
@Time        : 2023/12/7 11:30
@Description: BGM车控车设座椅
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
from xat_ecu.legacy.soa_partner.src.partner_const import *



@allure.feature("SOA服务接口")
@allure.story("WTI通知")
class TestWTIServiceChargeLid(TestABCBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        self.soa.update(["SeatService_client", "WTIService_client","ChargeLidService_client"])
        self.sd_tester.write_ccp(ccp={973: 0})
        sleep(2)
    def before_each_func(self, ecu):
            pass

    def after_each_func(self, ecu):
        self.bus_comm.set_chrglid_pos(126)
        self.bus_comm.set_ChrgLidManvgDCorAcDcOverTrvlFb(Fb=False)
        self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=False)
        self.bus_comm.set_door_opener_sts(tr_opener=DoorOpenerSts.FullClsd)

    def after_class(self, ecu):
        pass



    @allure.title("充电口盖异常提示ChrgLidManvgDCorAcDcBlkFb:1")                       #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339525?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1981041(self):
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcBlkFb", 0)
        sleep(1)
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcBlkFb", 1)

        self.soa.get_and_event_check_warning_info_list(name="Charge Lid Abnormal", info='1')
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcBlkFb", 0)
        # self.soa.get_warning_info_list(name="Charge Lid Abnormal", info=1)


    @allure.title("充电口盖无异常提示:ChrgLidManvgDCorAcDcOverTrvlFb:0")                 #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339524?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1981040(self):
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcOverTrvlFb", 1)
        sleep(1)
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcOverTrvlFb", 0)

        self.soa.get_and_event_check_warning_info_list(name="Charge Lid Abnormal", info='0')
        # self.soa.get_warning_info_list(name="Charge Lid Abnormal", info=1)


    @allure.title("充电口盖无异常提示:ChrgLidManvgDCorAcDcBlkFb:0")                         #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339522?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1981032(self):
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcBlkFb", 1)
        sleep(1)
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcBlkFb", 0)

        self.soa.get_and_event_check_warning_info_list(name="Charge Lid Abnormal", info='0')


    @allure.title("充电口盖异常提示:ChrgLidManvgDCorAcDcOverTrvlFb:1")                        #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339521?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1981031(self):
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcOverTrvlFb", 0)
        sleep(1)
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcOverTrvlFb", 1)

        self.soa.get_and_event_check_warning_info_list(name="Charge Lid Abnormal", info='1')
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcOverTrvlFb", 0)


    @allure.title("充电口盖警告显示:ChrgLidManvgDCorAcDcElecErrFb:1")                   #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339520?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1981021(self):
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcElecErrFb", 1)
        sleep(1)
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcElecErrFb", 0)
         
        self.soa.get_and_event_check_warning_info_list(name="Charge Lid", info='0')


    @allure.title("充电口盖故障:ChrgLidManvgDCorAcDcElecErrFb:1")                           #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339519?projectId=46"
    )
    @pytest.mark.smoke
    def test_caseid_1981019(self):
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcElecErrFb", 0)
        sleep(1)
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcElecErrFb", 1)
         
        self.soa.get_and_event_check_warning_info_list(name="Charge Lid", info='1')
        self.bus_comm.set("cem_lin2", "PrldCem_Lin2Fr02", "ChrgLidManvgDCorAcDcElecErrFb", 0)


    @allure.title("充电枪连接指示:DCChrgnHndlSts:1")                             #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339518?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981014(self):
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargingGunConnectSts,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ChargingGunConnectSts,sig_value=1,prom_name="Charging Gun Connected",prom_state="1")


    @allure.title("充电枪连接指示:DCChrgnHndlSts:5")                     #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339517?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981013(self):
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargingGunConnectSts,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ChargingGunConnectSts,sig_value=5,prom_name="Charging Gun Connected",prom_state="1")


    @allure.title("充电枪连接指示:DCChrgnHndlSts:2")                      #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339516?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981012(self):
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargingGunConnectSts,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ChargingGunConnectSts,sig_value=2,prom_name="Charging Gun Connected",prom_state="1")


    @allure.title("充电枪连接指示:DCChrgnHndlSts:4")                         #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339515?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981011(self):
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargingGunConnectSts,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ChargingGunConnectSts,sig_value=3,prom_name="Charging Gun Connected",prom_state="1")
        sleep(1)
        self.bus_comm.set_wti_signal(func = WTI_Func.ChargingGunConnectSts,value = 4)
        self.soa.get_warning_light_list(name="Charging Gun Connected", state="1")
        self.soa.empty_all()

    @allure.title("充电枪连接指示:DCChrgnHndlSts:0")                              #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339514?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981009(self):
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargingGunConnectSts,value=1)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ChargingGunConnectSts,sig_value=0,prom_name="Charging Gun Connected",prom_state="0")


    @allure.title("充电枪连接指示:DCChrgnHndlSts:3")                        #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339510?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1981003(self):
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Open)
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargingGunConnectSts,value=1)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_light_sts(func=WTI_Func.ChargingGunConnectSts,sig_value=3,prom_name="Charging Gun Connected",prom_state="1")


    @allure.title("充电口盖无状态显示:ChrgLidRearSts:0")                          #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339511?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1981004(self):
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargeLidOpenSts,value=1)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ChargeLidOpenSts,sig_value=127,prom_name="Charge Lid Status",prom_state="0")

    @allure.title("充电口盖显示开:ChrgLidRearSts:1")                             #pas
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339512?projectId=46"
    )
    @pytest.mark.sanity
    def test_caseid_1981005(self):
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargeLidOpenSts,value=2)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ChargeLidOpenSts,sig_value=100,prom_name="Charge Lid Status",prom_state="1")


    @allure.title("充电口盖显示关:ChrgLidRearSts:2")                        #pass
    @allure.testcase(
        "https://jama.jiduauto.com/perspective.req#/testCases/2339513?projectId=46"
    )
    @pytest.mark.full
    def test_caseid_1981006(self):
        self.bus_comm.set_wti_signal(func=WTI_Func.ChargeLidOpenSts,value=0)
        sleep(1)
        self.mix.wti_sig_set_and_get_and_event_check_warning_info_list(func=WTI_Func.ChargeLidOpenSts,sig_value=0,prom_name="Charge Lid Status",prom_state="2")
    
    @pytest.mark.sanity
    def test_caseid_1994550(self): 
        '''充电口盖关闭失败WTI产生'''
        hint = "ChargeLidCloseFailed"
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        time.sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=True)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
    
    @pytest.mark.sanity
    def test_caseid_1994549(self): 
        '''充电口盖关闭失败WTI恢复_充电口盖状态关闭'''
        hint = "ChargeLidCloseFailed"
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        time.sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=True)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0")
       
    @pytest.mark.full
    def test_caseid_1994548(self): 
        '''充电口盖关闭失败WTI恢复_充电口盖位置状态小于10%'''
        hint = "ChargeLidCloseFailed"
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        time.sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=True)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_chrglid_pos(10)
        time.sleep(0.3)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0") 
    
    @pytest.mark.full
    def test_caseid_1994547(self): 
        '''充电口盖关闭失败WTI恢复_充电口盖位置未知'''
        hint = "ChargeLidCloseFailed"
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        time.sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=True)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.bus_comm.set_chrglid_pos(126)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Ukwn)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="0") 
    
    @pytest.mark.full
    def test_caseid_1994546(self): 
        '''充电口盖关闭失败WTI初始值'''
        hint = "ChargeLidCloseFailed"
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        time.sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=True)
        self.soa.get_and_event_check_warning_info_list(name = hint, info="1")
        self.mix.restart_bgm_and_connect_service("WTIService_client")
        self.soa.get_warning_info_list(name = hint, info="0")
    
    @pytest.mark.full
    def test_caseid_1994545(self): 
        '''充电口盖关闭失败WTI异常状态无法产生_充电口盖状态为关闭'''
        hint = "ChargeLidCloseFailed"
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(0)
        time.sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=True)
        time.sleep(0.3)
        self.soa.get_warning_info_list(name = hint, info="0")
    
    @pytest.mark.full
    def test_caseid_1994544(self): 
        '''充电口盖关闭失败WTI异常状态无法产生_充电口盖状态小于10%'''
        hint = "ChargeLidCloseFailed"
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(10)
        time.sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=True)
        time.sleep(0.3)
        self.soa.get_warning_info_list(name = hint, info="0")
    
    @pytest.mark.full
    def test_caseid_1994543(self): 
        '''充电口盖关闭失败WTI异常状态无法产生_充电口盖状态未知'''
        hint = "ChargeLidCloseFailed"
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(126)
        time.sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=True)
        time.sleep(0.3)
        self.soa.get_warning_info_list(name = hint, info="0")
    
    @pytest.mark.full
    def test_caseid_1994542(self): 
        '''充电口盖关闭失败WTI异常状态无法产生_超时'''
        hint = "ChargeLidCloseFailed"
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        time.sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        time.sleep(1.6)
        self.bus_comm.set_ChrgLidManvgDCorAcDcBlkFb(Fb=True)
        time.sleep(0.3)
        self.soa.get_warning_info_list(name = hint, info="0")

    @pytest.mark.full
    def test_caseid_1994541(self): 
        '''充电口盖关闭失败WTI异常状态无法产生_WarnStatus不为1'''
        hint = "ChargeLidCloseFailed"
        self.bus_comm.set_OnBdChrgrHndlSts1(OnBdChrgrHndlSts = OnBdChrgrHndlSts.Disconnected)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected,time_wait = 1)
        self.bus_comm.set_chrglid_pos(100)
        time.sleep(1)
        self.soa.hmi_set_chrglid_sts(sts=ChrgLidOperType.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.set_ChrgLidManvgDCorAcDcOverTrvlFb(Fb=True)
        time.sleep(0.3)
        self.soa.get_warning_info_list(name = hint, info="0")
    
    
    
