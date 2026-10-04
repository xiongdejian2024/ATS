# -*- coding: utf-8 -*-
"""
@File        : test_soa_heat.py
@Author      : gang.liugang@jiduatuo.com
@Time        : 2024/01/10 15:00 PM
@Description : Test SOA for ObtDiagService
"""

import os
import sys

from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_cases.legacy.soa.case_helper.parse_excel import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.sdk.sdk_tools import *
from xat_cases.legacy.soa.case_helper.utils import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *

current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.join(current_path.split("sat")[0], "sat"))
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.common.logger import logger

@allure.feature("SOA服务接口")
@allure.story("架构基础/ObtDiagService")
class TestObtDiagService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("ObtDiagService", "client"),
                                     ("PedalService","client"),
                                     ("SteerWheelService","client"),
                                     ])
        self.partner.method_default_timeout = 0.1

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkNotEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2})
        self.sd_tester.write_multi_ccp({10: 0x2, 481: 0x4, 578: 0x4})
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.ipdu.set_vehspd(0)
        sleep(0.5)
        self.sd_tester.change_car_mode(0)
        self.sd_tester.change_usage_mode(1)
        self.partner.empty_all(1)
        logger.info(f"case开始运行*******************************************************")

    def after_each_func(self, ecu):
        logger.info(f"case结束运行*******************************************************")
        self.ipdu.resume_all_bus_send()  # 信号恢复
        self.bgmcli.stop_bgm_tcpdump()
        self.bgmcli.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        if ecu.get("testresult") != "Pass":
            logger.error("case失败，需等待10s让环境恢复")
            sleep(10)
        else:
            logger.info("case成功，需等待3s让环境恢复")
            sleep(3)
        super().after_each_func(ecu, start=False)
 
    def after_class(self, ecu):
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)

    @allure.title("设置并通知毫米波标定结果_ECU进入扩展诊断模式失败_负反馈")
    @pytest.mark.sanity
    def test_caseid_1983930(self): 
        caliRadarList = [0,1,2,3,4]
        caliMethodList = [1,0]
        for i in range(len(caliRadarList)):
            for j in range(len(caliMethodList)):
                self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "SetRadarCaliMode",
                                            {"caliRadar":caliRadarList[i],"caliMethod":caliMethodList[j]})
                
                #timeout=8 是为了保证如果没有ACU仿真时，服务在6秒内启动
                self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyRadarCaliInfo",
                                            {"RadarCalSts":[{"RadarLocation":caliRadarList[i],"CalProgress":0,"CalErrorCode":66048}]},timeout=8)
            
    @allure.title("触发读取并通知安全带震动次数")
    #只需要收到通知即可，通知内容(VibNum,ErrorCode,NRC)无需确认
    @pytest.mark.smoke
    def test_caseid_1983929(self): 
        self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "ReadBeltVibInfo",
                                            {})
        self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyBeltVibInfo",
                                            {"info":{"VibNum":4294967295,"ErrorCode":1,"NRC":0}})   

    @allure.title("触发并通知EOL车窗雨刮标定_诊断仲裁_仲裁失败")
    #由于一次设置会发送两次通知，这两次通知会存在一个列表中，设置"source":inputSourceList[i]=1的时候，用来check
    #的其实是上一次 0 ，对应的第二次通知，所以需要修改，一次设置两次通知，且需要了解如何退出 4=WaitArb     // 诊断仲裁中状态
    @pytest.mark.sanity
    def test_caseid_1983931(self): 
        self.partner.empty_all(0.5)
        inputSourceList = [0,1]
        # self.nucapp.bgm_diag_line_down()
        for i in range(len(inputSourceList)):
            self.partner.send_request_and_ck_resp(OBTDIAG_SERVICE_CLIENT, "StartEOLCali",
                                            {"source":inputSourceList[i]}, {"out": True})
            #Device,Status,ErrorCode,NRC
            self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyEOLCaliInfo",
                                            {"info":{"Device":0,"Status":4,"ErrorCode":0,"NRC":0}})  
            self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyEOLCaliInfo",
                                            {"info":{"Device":1,"Status":4,"ErrorCode":0,"NRC":0}})  
            self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyEOLCaliInfo",
                                            {"info":{"Device":0,"Status":2,"ErrorCode":1,"NRC":0}})  
            self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "NotifyEOLCaliInfo",
                                            {"info":{"Device":1,"Status":2,"ErrorCode":1,"NRC":0}}) 
        # self.nucapp.bgm_diag_line_up()

    @allure.title("通知并获取整车重启状态")
    @pytest.mark.sanity
    def test_caseid_1983943(self): 
        self.partner.empty_all(0.5)
        #设置初始条件
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 2)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', 2)
        
        self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "RestartStatus",
                                            {"status":{"mainState":1,"notification":0,}})  
        self.partner.send_request_and_ck_resp(OBTDIAG_SERVICE_CLIENT, "GetRestartStatus", {},
                                            {"out": {"mainState":1,"notification":0,}})
        sleep(4.5) 
        self.partner.empty_all(0.5)  
        
    @allure.title("启动场景获取到总线信号后_通知整车重启状态_默认值")
    @pytest.mark.full
    def test_caseid_1984326(self):
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SwtrBodyFr01, 'SteerWhlScRightButtonRi', 0)
        self.ipdu.set(self.ipdu.bodycan.SwtlBodyFr02, 'SteerWhlScLeftButtonLeSteerWhlTouchSwt2', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.partner.empty_all(1)

        self.restart_bgm_and_connect_service(OBTDIAG_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)

        self.ipdu.resume_all_bus_send()
        sleep(0.5)
        self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "RestartStatus",
                                            {"status":{"mainState":0,"notification":0,}}) 
     
    @allure.title("设置整车域控重启")
    @pytest.mark.sanity
    def test_caseid_1985582(self):   
        self.partner.send_method_request(OBTDIAG_SERVICE_CLIENT, "SetRestart",  {"req": {"source": 1}})  
        self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "RestartStatus", {"status":{"mainState": 2}}) 
        # self.partner.ck_event_and_resp(OBTDIAG_SERVICE_CLIENT, "RestartStatus", {"status": {"mainState":2}})#因为是一瞬间的事情hetao说可以不用get     
        
    @allure.title("通知/获取智能标定结果信息")
    @pytest.mark.sanity
    def test_caseid_1988662(self): 
        self.nucapp.bgm_diag_line_down()
        sleep(1)
        SetResp = self.partner.send_request_and_return_resp(OBTDIAG_SERVICE_CLIENT, "SetIntelligentCalibrationFunctionCmd", 
                                                  {"cmd": {"req":1, "intelligentFunctionID":0, "sourceType":1, "isAllowedSkip":False}})["out"]
        if SetResp == 1:
                assert True
        else:
                assert False
        self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "IntelligentCalibrationStatusInfo",{"info":{"status":2}})
        SetResp1 = self.partner.send_request_and_return_resp(OBTDIAG_SERVICE_CLIENT, "SetIntelligentCalibrationAuthorizationCmd", 
                                                    {"cmd": {"req":1}})["out"]
        if SetResp1 == 1:
                assert True
        else:
                assert False
        self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "IntelligentCalibrationResultInfo",
                                              {"info":{"errorCode": 3,"intelligentFunctionID":0, "textID":255}}) 
        self.partner.send_request_and_ck_resp(OBTDIAG_SERVICE_CLIENT, "GetIntelligentCalibrationResultInfo", {},
                                              {"out": {"errorCode": 0,"intelligentFunctionID":255, "textID":255}})
        self.nucapp.bgm_diag_line_up()
    
    @allure.title("设置智能标定模式")
    @pytest.mark.smoke
    def test_caseid_1988658(self):   
        SetResp = self.partner.send_request_and_return_resp(OBTDIAG_SERVICE_CLIENT, "SetIntelligentCalibrationFunctionCmd", 
                                                  {"cmd": {"req":1, "intelligentFunctionID":0, "sourceType":2, "isAllowedSkip":True}})["out"]
        if SetResp == 1:
            assert True
        else:
            assert False

    @allure.title("触发重试智能标定")
    @pytest.mark.smoke
    def test_caseid_1988659(self):   
        for retryReq in range(2):
            SetResp = self.partner.send_request_and_return_resp(OBTDIAG_SERVICE_CLIENT, "SetIntelligentCalibrationFunctionRetryCmd", 
                                                    {"cmd": {"retryReq":retryReq}})["out"]
            if SetResp == 1:
                assert True
            else:
                assert False

    @allure.title("设置智能标定授权")
    @pytest.mark.smoke
    def test_caseid_1988660(self):   
        for req in range(2):
            SetResp = self.partner.send_request_and_return_resp(OBTDIAG_SERVICE_CLIENT, "SetIntelligentCalibrationAuthorizationCmd", 
                                                    {"cmd": {"req":req}})["out"]
            if SetResp == 1:
                assert True
            else:
                assert False

    @allure.title("通知/获取智能标定状态信息")
    @pytest.mark.sanity
    def test_caseid_1988661(self):
        SetResp = self.partner.send_request_and_return_resp(OBTDIAG_SERVICE_CLIENT, "SetIntelligentCalibrationFunctionCmd", 
                                                  {"cmd": {"req":1, "intelligentFunctionID":0, "sourceType":2, "isAllowedSkip":True}})["out"]
        if SetResp == 1:
                assert True
        else:
                assert False
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcCalRqrdFb', True)#设置充电口盖标定反馈状态
        self.ipdu.set(self.ipdu.cem_lin2.PrldCem_Lin2Fr02, 'ChrgLidManvgDCorAcDcCalActvSts2', 1)#设置充电口盖标定激活状态
        self.partner.ck_s2s_event(OBTDIAG_SERVICE_CLIENT, "IntelligentCalibrationStatusInfo",
                                              {"info":{"status":1,"intelligentFunctionID":0,"textID":255}})
        self.partner.send_request_and_ck_resp(OBTDIAG_SERVICE_CLIENT, "GetIntelligentCalibrationStatusInfo", {},
                                              {"out": {"status":1,"intelligentFunctionID":0,"textID":255}})

        
        