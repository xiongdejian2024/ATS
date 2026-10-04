#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File        : test_tailwing_wti.py
@Author      : huajie.yang@jiduauto.com
@Time        : 2024/1/23 11:30
@Description: BGM车控车设尾翼WTI功能
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
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import *
from xat_cases.legacy.soa.case_helper.test_base import *

WTI_SERVICE_CLIENT = "WTIService_client"              
@allure.feature("车控车设")
@allure.story("尾翼WTI告警")
@pytest.mark.tailwing
class TestWTIServicePassiveSafety(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["WTIService_client","TailWingService_client"])
        self.sd_tester.write_ccp(ccp={211: 0x01, 564: 0x2})

    def before_each_func(self, ecu):
        self.bus_comm.set_vehspd_gear(vehspd=0.0)    
        #设置动力状态 0为静止状态 ，5为行驶状态
        self.bus_comm.set_engine_sts(EngSt1WdStsEngSt1WdSts=EngSt1WdStsEngSt1WdSts.EngSt1_Ini)
        #车辆静止 默认设置 3 （1，2，3都是静止）
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal3)
        sleep(.5)
          

    def after_each_func(self, ecu):       
        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltHiVoltDetdFlt', 0)
        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIceBreakFaild', 0)
        self.bus_comm.set('propulsioncan','EcmPropFr24', 'GearLvrIndcn_1_EcmPropSignalIPdu24', 0)
        #关闭尾门
        self.io.set_door(Trunk=Door.close)
        self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrMotBlk', 0)
        

    def after_class(self, ecu):
        try:
            self.mix.set_common_precontion(
                usage_mode=UsageMode.INACTIVE, car_mode=CarMode.NORMAL
            )
        except Exception as e:
            logger.info(f"----------> after_class Error{str(e)}")
            pass
    
    @pytest.mark.sanity
    def test_caseid_1981897(self):
        '''MSO-SVRIF-3256_电动尾翼系统故障报警信息'''  
        for i in [UsageMode.CONVENIENCE,UsageMode.ACTIVE,UsageMode.DRIVING]:
            self.mix.set_common_precontion(
                car_mode=CarMode.NORMAL, usage_mode=i
            )  
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltHiVoltDetdFlt', 1)
            self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)
            sleep(1)
            self.soa.ck_s2s_event("WTIService_client", "WarningMsgList",
                                                {'list': [{'name': 'Car Tail Failure', 'info': 7}]})
            self.soa.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},
                                                            {"out": [{'name': 'Car Tail Failure', 'info': 7}]}) 
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrUFltHiVoltDetdFlt', 0)
        
    @pytest.mark.sanity
    def test_caseid_1981894(self):
        '''MSO-SVRIF-3256_电动尾翼破冰报警信息'''    
        for i in [UsageMode.CONVENIENCE,UsageMode.ACTIVE,UsageMode.DRIVING]:
            self.mix.set_common_precontion(
                car_mode=CarMode.NORMAL, usage_mode=i
            )  
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIceBreakFaild', 1) 
            sleep(.5)
            self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)
            sleep(1)
            self.soa.ck_s2s_event("WTIService_client", "WarningMsgList",{'list': [{'name': 'Car Tail Failure', 'info': 4}]})         
            self.soa.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},{"out": [{'name': 'Car Tail Failure', 'info': 4}]})
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrIceBreakFaild', 0) 
                                                            

    @pytest.mark.sanity
    def test_caseid_1981896(self):
        '''MSO-SVRIF-3256_电动尾翼尾门未关闭报警信息'''
        for i in [UsageMode.CONVENIENCE,UsageMode.ACTIVE,UsageMode.DRIVING]:
            self.mix.set_common_precontion(
                car_mode=CarMode.NORMAL, usage_mode=i
            )  
            self.soa.hmi_set_tailwing_mode(mode=TailWindMode.Off)
            self.soa.get_tailwing_mode(mode=TailWindMode.Off)
            self.io.set_door(Trunk=Door.open)
            sleep(.5)
            self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)
            self.soa.get_tailwing_mode(mode=TailWindMode.On)
            sleep(1)
            self.soa.ck_s2s_event("WTIService_client", "WarningMsgList",{'list': [{'name': 'Car Tail Failure', 'info': 5}]})                      
            self.soa.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {}, {"out": [{'name': 'Car Tail Failure', 'info': 5}]})
            self.io.set_door(Trunk=Door.close)
                                                           
    @pytest.mark.sanity
    def test_caseid_1981895(self):
        '''MSO-SVRIF-3256_电动尾翼堵转报警信息'''
        for i in [UsageMode.CONVENIENCE,UsageMode.ACTIVE,UsageMode.DRIVING]:
            self.mix.set_common_precontion(
                car_mode=CarMode.NORMAL, usage_mode=i
            )  
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrMotBlk', 1)
            sleep(.5)
            self.soa.hmi_set_tailwing_mode(mode=TailWindMode.On)
            sleep(1)
            self.soa.ck_s2s_event("WTIService_client", "WarningMsgList",{'list': [{'name': 'Car Tail Failure', 'info': 3}]})
            self.soa.send_request_and_ck_resp("WTIService_client", "GetWarningMsgList", {},{"out": [{'name': 'Car Tail Failure', 'info': 3}]})
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01','ActvReSplrMotBlk', 0)
                                                            
    @pytest.mark.sanity
    def test_caseid_1981891(self):
        '''MSO-SVRIF-3255_3D车模显示尾翼收回
        '''
        for i in [UsageMode.CONVENIENCE,UsageMode.ACTIVE,UsageMode.DRIVING]:
            self.mix.set_common_precontion(
                car_mode=CarMode.NORMAL, usage_mode=i
            )  
            self.bus_comm.set_tailwing_pos(TailWingPos.Ukwn)
            sleep(.5)
            self.bus_comm.set_tailwing_pos(TailWingPos.P0)
            sleep(0.1)
            self.soa.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                    {"list": [{"name": "3D Model Shows Tail Position", "info": "1"}]})
            self.soa.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "3D Model Shows Tail Position", "info": "1"}]})
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01', 'ActvReSplrPosn', 0)
            sleep(0.1)
            self.soa.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                    {"list": [{"name": "3D Model Shows Tail Position", "info": "0"}]})
            self.soa.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "3D Model Shows Tail Position", "info": "0"}]})

    @pytest.mark.sanity
    def test_caseid_1981892(self):
        '''MSO-SVRIF-3255_3D车模显示尾翼收回
        '''
        for i in [UsageMode.CONVENIENCE,UsageMode.ACTIVE,UsageMode.DRIVING]:
            self.mix.set_common_precontion(
                car_mode=CarMode.NORMAL, usage_mode=i
            )  
            self.bus_comm.set_tailwing_pos(TailWingPos.Ukwn)
            sleep(.5)
            self.bus_comm.set_tailwing_pos(TailWingPos.P0)
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01', 'ActvReSplrPosn', 4)
            sleep(0.1)
            self.soa.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                    {"list": [{"name": "3D Model Shows Tail Position", "info": "4"}]})
            self.soa.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "3D Model Shows Tail Position", "info": "4"}]})
            self.bus_comm.set('cem_lin6','AwmCem_Lin6Fr01', 'ActvReSplrPosn', 0)
            sleep(0.1)
            self.soa.ck_s2s_event(WTI_SERVICE_CLIENT, "WarningMsgList",
                                    {"list": [{"name": "3D Model Shows Tail Position", "info": "0"}]})
            self.soa.send_request_and_ck_resp(WTI_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{"name": "3D Model Shows Tail Position", "info": "0"}]})
   