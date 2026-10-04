"""
@File         :test_ShieldWindowService.py
@Time         :2023/04/30 19:07:31
@Author       :tao.cheng_ext@jiduauto.com
@Description : Test SOA for ShieldWindowService
"""

import pytest
import allure

from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import *


@allure.feature("SOA服务接口")
@allure.story("整车控制/ShieldWindowService")
class TestShieldWindowService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.nucapp, self.tc_config)
        self.partner = S2sBaseClass([("ShieldWindowService", "client")])
        self.partner.method_default_timeout = 0.1
        self.sd_tester.tester_present()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu, start=False)
        
    @pytest.mark.full
    @allure.title("设置挡风(前摄像头和后挡风)加热_校验TCP")
    def test_caseid_1984920(self):
        self.sd_tester.write_multi_ccp({182: 2, 13: 4})
        self.sd_tester.change_usage_mode(2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        for req in [0,1, 2]:
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 1, "status": req}})
            sleep(0.5)
        for req1 in [0,1,2]:
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 2, "status": req1}})
            sleep(0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("FrntCamDefrostReq", [0,1])
        self.bgm_eth_inter.ck_signal_values("HmiDefrstElecReqReElecReq", [0,1,2])
        self.bgm_eth_inter.ck_signal_values("HmiDefrstElecReqMirrElecReq", [0,1,2])
        self.bgm_eth_inter.ck_signal_values("HmiDefrstElecReqFrntElecReq", [0,0,0])
    
    @pytest.mark.sanity
    @allure.title("获取挡风(前摄像头和后挡风)_初始化 测试")
    def test_caseid_107050(self):
        with allure.step("BGM下电重启"):
            self.restart_bgm_and_connect_service(SHIELDWINDOW_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "GetHeat",{"windows":[1,2]},
                                             {"out":[{"id":1,"status":0},{"id":2,"status":0}]})

    @pytest.mark.full
    @allure.title("设置挡风(前摄像头和后挡风)_后挡风玻璃加热_切为inactive")
    def test_caseid_1960039(self):
        self.sd_tester.write_multi_ccp({182: 2, 13: 4})
        sleep(1)
        for X in [2,11,13]:
            self.sd_tester.change_usage_mode(X)
            self.partner.send_request_and_ck_resp(SHIELDWINDOW_SERVICE_CLIENT, "GetHeat", {"windows": [2]},
                                                {"out": [{"id": 2, "status": 0}]})
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 2, "status": 0}})
            self.partner.empty_all(0.5)
            self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 2, "status": 1}})        
            self.sd_tester.change_usage_mode(1)
            self.partner.send_request_and_ck_resp(SHIELDWINDOW_SERVICE_CLIENT, "GetHeat", {"windows": [2]},
                                                {"out": [{"id": 2, "status": 0}]})
        
    @pytest.mark.sanity
    @allure.title("获取和通知前挡风玻璃温度信息")
    def test_caseid_1983407(self):
        self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr02, 'CmptFrntWindT',0.0)
        self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr02, 'CmptFrntWindDewT', 0.0)
        self.partner.empty_all(0.5)
        for value in [-40.0,0.0,164.7]:
            logger.info(f"--发送两个信号值为{value}")
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr02, 'CmptFrntWindT',value)
            self.ipdu.set(self.ipdu.cem_lin1.RlsmCem_Lin1Fr02, 'CmptFrntWindDewT', value)
            sleep(0.5)
            self.partner.ck_s2s_event(SHIELDWINDOW_SERVICE_CLIENT,"FrontWindshieldTemperature", 
                                      {"info": {"frontWindshieldTemp": value,"frontWindshieldDewTemp": value}})
            self.partner.send_request_and_ck_resp(SHIELDWINDOW_SERVICE_CLIENT, "GetFrontWindshieldTemperature", {},
                                              {"out": {"frontWindshieldTemp": value,"frontWindshieldDewTemp": value}})

    @pytest.mark.full
    @pytest.mark.restart
    @allure.title("获取和通知前挡风玻璃温度信息_默认值")
    def test_caseid_1983409(self):
        self.restart_bgm_and_connect_service(SHIELDWINDOW_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(SHIELDWINDOW_SERVICE_CLIENT, "GetFrontWindshieldTemperature", {},
                                              {"out": {"frontWindshieldTemp": 255,"frontWindshieldDewTemp": 255}})
        
    @pytest.mark.full
    @allure.title("通知前摄像头和后挡风加热状态_默认值")
    def test_caseid_1984835(self):
        self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 1, "status": 0}})
        self.partner.send_method_request(SHIELDWINDOW_SERVICE_CLIENT, "SetHeat", {"heat": {"id": 2, "status": 0}})
        self.ipdu.pause_all_bus_send()
        self.nucapp.bgm_power_off()
        sleep(2)
        self.nucapp.bgm_power_on()
        sleep(4)
        self.ipdu.resume_all_bus_send()
        sleep(2)
        self.partner.ck_s2s_event(SHIELDWINDOW_SERVICE_CLIENT, "FrontCameraHeatStatus",
                                       {"sts": 0})
        self.partner.ck_s2s_event(SHIELDWINDOW_SERVICE_CLIENT, "RearShieldWindowHeatStatus",
                                       {"sts": 0})
            
######################################################################################################################################################## 

@allure.feature("SOA服务接口")
@allure.story("整车控制/ShieldWindowService")
@pytest.mark.mock_tcp
class TestShieldWindowServiceMockMcu(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, tcp_down_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass(
            [("VehicleModeService", "client"),("ShieldWindowService", "client")])
        self.partner.wait_for_service_reconnect(SHIELDWINDOW_SERVICE_CLIENT)

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)
    
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)

    @allure.title("通知前摄像头和后挡风加热状态_遍历")
    @pytest.mark.sanity
    def test_caseid_1984834(self):
        def info(value):
            return 1 if value == 1 or value == 5 else 0
        self.bgm_eth_inter.set_signal("FrntCamDefrostSts", 1, send_pdu_immediately=True)#前挡风摄像头
        sleep(0.5)
        for sigin1 in range(2):
            logger.info(f"发送前挡风信号值{sigin1}")
            self.bgm_eth_inter.set_signal("FrntCamDefrostSts", sigin1, send_pdu_immediately=True)
            sleep(0.5)
            self.partner.ck_s2s_event(SHIELDWINDOW_SERVICE_CLIENT, "FrontCameraHeatStatus",
                                        {"sts": sigin1})
            self.partner.send_request_and_ck_resp(SHIELDWINDOW_SERVICE_CLIENT, "GetHeat", {"windows": [1]},
                                                        {"out": [{"id": 1, "status": sigin1}]})
        self.bgm_eth_inter.set_signal("FrntCamDefrostSts", 2, send_pdu_immediately=True)
        sleep(0.5)
        self.partner.ck_s2s_event(SHIELDWINDOW_SERVICE_CLIENT, "FrontCameraHeatStatus",
                                    {"sts": 3})
        self.partner.send_request_and_ck_resp(SHIELDWINDOW_SERVICE_CLIENT, "GetHeat", {"windows": [1]},
                                                    {"out": [{"id": 1, "status": 3}]})
        self.bgm_eth_inter.set_signal("HmiDefrstrElecStsRe", 1, send_pdu_immediately=True)#后挡风加热
        sleep(0.5)
        for sigin2 in [0,1,2,5,3,1,4,5]:
            logger.info(f"发送后挡风信号值{sigin2}")
            self.bgm_eth_inter.set_signal("HmiDefrstrElecStsRe", sigin2, send_pdu_immediately=True)#后挡风加热
            sleep(1)
            self.partner.ck_s2s_event(SHIELDWINDOW_SERVICE_CLIENT, "RearShieldWindowHeatStatus",
                                        {"sts": info(sigin2)})
            self.partner.send_request_and_ck_resp(SHIELDWINDOW_SERVICE_CLIENT, "GetHeat", {"windows": [2]},
                                                        {"out": [{"id": 2, "status": info(sigin2)}]})
        self.partner.send_request_and_ck_resp(SHIELDWINDOW_SERVICE_CLIENT, "GetHeat", {"windows": [1,2]},
                                                        {"out": [{"id": 1, "status": 3},{"id": 2, "status": 1}]})

    



