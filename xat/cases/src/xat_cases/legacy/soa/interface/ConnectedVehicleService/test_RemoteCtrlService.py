#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_RemoteCtrlService.py
@Time         :2023/07/30 17:20:31
@Author       :jishu.duan_ext
@Description  :
"""
import allure
import pytest
import time
from time import sleep
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import *
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.api.abc_interface import *
from xat_ecu.api.interfaces.dp1.tsp import Tsp


REMOTECTRL_SERVICE_CLIENT = "RemoteCtrlService_client"
VEHICLESETSTATUS_CLIENT = "VehicleSetStatusService_client"

@allure.feature("SOA服务接口")
@allure.story("互联服务/RemoteCtrlService")
@pytest.mark.tcam
class TestRemoteCtrlService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.tsp = Tsp(**self.tc_config)  
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("CentralLockService", "client"),
                                     ("KeyService", "client"),
                                     ("RemoteCtrlService", "client"),
                                     ("VehicleSetStatusService", "client"),
                                     ("DoorService","client")
                                 ])
        self.partner.method_default_timeout = 0.1
        self.partner.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": False}
        )
        sleep(2)
        
    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
        self.sd_tester.change_car_mode(0, do_assert=1)
        sleep(0.5)
        self.sd_tester.change_usage_mode(1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', self.dk.last_sync_time_entity)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', self.dk.last_sync_time_ble)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.dk.set_chassis_service_gear("P")
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.io.init_bgm_HW()  
        self.io.hood_door1_close()
        self.io.hood_door2_open()
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send() 
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(30)  # 避免防玩
        super().after_each_func(ecu, start=False)
    
    def auto_no_accredit(self, accredit):
        """
        0=满足自动授权, 1=不满足自动授权，不满足取消自动授权, 2=取消自动授权
        """
        if accredit == 0:   
            self.io.drvr_door_open()
            self.io.driver_seat_present()
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        elif accredit == 1:
            self.io.init_bgm_HW()
            self.io.drvr_door_close()
            self.io.driver_seat_notpresent()
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.dk.set_cenlock_sts(1)
        elif accredit ==2:
            self.io.drvr_door_close()
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.io.init_bgm_HW() 
            self.dk.set_cenlock_sts(3)
        else:
            pass  
    
    def tcam_reset_wait_service(self, name):
        self.nucapp.tcam_power_off()
        sleep(50)
        self.nucapp.tcam_power_on()
        self.partner.wait_for_service_reconnect(name, timeout=300)
                    
    @allure.title("通知/获取远程解锁状态_default")
    @pytest.mark.full
    def test_caseid_1983166(self):
        self.tcam_reset_wait_service(REMOTECTRL_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRVCLockInfo", {}, {"out": {"sts": 0}})

    @allure.title("获取通知远控解锁状态_成功")
    @pytest.mark.smoke
    def test_caseid_1981477(self):
        self.dk.set_chassis_service_gear("P")
        time.sleep(0.5)
        self.dk.set_cenlock_sts(3)
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsLockSt_1_CEMBodySignalIPdu13', 3, timeout=3)
        sleep(1)
        self.tsp.rvc_lock_control(1)  # 1: 解锁, 2:闭锁, 3: 关门+闭锁
        logger.info("已发送解锁请求")
        self.partner.ck_s2s_event(REMOTECTRL_SERVICE_CLIENT, "NotifyRVCLockInfo", {"info":{"sts": 2}},timeout=10)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRVCLockInfo", {}, {"out": {"sts": 2}})     

    @allure.title("通知/获取远程解锁状态_False")
    @pytest.mark.sanity
    def test_caseid_1983167(self):
        self.sd_tester.change_usage_mode(13)
        self.dk.set_chassis_service_gear("D")
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn_1_EcmPropSignalIPdu24', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 0)
        time.sleep(0.5)
        self.tsp.rvc_lock_control(1)  
        logger.info("已发送解锁请求")
        self.partner.ck_s2s_event(REMOTECTRL_SERVICE_CLIENT, "NotifyRVCLockInfo", {"info": {"sts": 1}},timeout=10)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRVCLockInfo", {}, {"out": {"sts": 1}})

    @allure.title("通知/获取远程授权启动状态_kDefault")#beta2
    @pytest.mark.full
    def test_caseid_1985537(self):
        self.tcam_reset_wait_service(REMOTECTRL_SERVICE_CLIENT)
        sleep(20)
        self.partner.ck_s2s_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":0,"time": 0xFFFFFFFF}},timeout=10)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":0,"time": 0xFFFFFFFF}})
        
    @allure.title("通知/获取远程授权启动状态_UnlockWait进ReadyEntry进Ready2L")#beta2
    @pytest.mark.sanity
    @pytest.mark.failed
    def test_caseid_1985560(self):
        self.auto_no_accredit(2)
        self.partner.empty_all(0.5)
        self.tsp.rvc_remote_authorization()
        self.partner.ck_s2s_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":2,"time":0xFFFFFFFF}}, timeout=10)
        self.partner.ck_s2s_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":3,"time":120}}, timeout=5)
        sleep(110)
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":3,"time":9}}, timeout=3)
        sleep(10)
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":0,"time":0xFFFFFFFF}}, timeout=3)
      
    @allure.title("通知/获取远程授权启动状态_Entry")#beta2
    @pytest.mark.smoke
    def test_caseid_1985561(self):
        self.auto_no_accredit(0)
        self.tsp.rvc_remote_authorization()
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":4,"time":0xFFFFFFFF}}, timeout=3)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":4,"time":0xFFFFFFFF}})
        
    @allure.title("通知/获取远程授权启动状态_Entry切Ready2L")#beta2
    @pytest.mark.full
    def test_caseid_1985565(self):
        self.auto_no_accredit(0)
        self.tsp.rvc_remote_authorization()
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":4,"time":0xFFFFFFFF}}, timeout=3)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":4,"time": 0xFFFFFFFF}})
        self.partner.empty_all(1)
        self.auto_no_accredit(2)    
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":0,"time": 0xFFFFFFFF}}, timeout=3)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":0,"time": 0xFFFFFFFF}})    

    @allure.title("通知/获取远程授权启动状态_Entry下异常重启&取消授权条件成功")#beta2
    @pytest.mark.sanity
    def test_caseid_1985570(self):
        self.auto_no_accredit(0)
        self.tsp.rvc_remote_authorization()
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":4,"time": 0xFFFFFFFF}}, timeout=3)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":4,"time": 0xFFFFFFFF}})
        self.tcam_reset_wait_service(REMOTECTRL_SERVICE_CLIENT)
        self.auto_no_accredit(2)
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":0,"time": 0xFFFFFFFF}}, timeout=10)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":0,"time": 0xFFFFFFFF}})

    @allure.title("通知/获取远程授权启动状态_Entry下异常重启&不满足取消授权条件")#beta2
    @pytest.mark.full
    def test_caseid_1985569(self):
        self.auto_no_accredit(0)
        self.tsp.rvc_remote_authorization()
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":4,"time": 0xFFFFFFFF}}, timeout=3)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":4,"time": 0xFFFFFFFF}})
        self.partner.empty_all(1)
        self.tcam_reset_wait_service(REMOTECTRL_SERVICE_CLIENT)
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":4,"time": 0xFFFFFFFF}}, timeout=10)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":4,"time": 0xFFFFFFFF}})

    @allure.title("通知/获取远程授权启动状态_ReadyEntry下异常重启&自动授权条件成功")#beta2
    @pytest.mark.full
    def test_caseid_1985568(self):
        self.auto_no_accredit(2)
        self.tsp.rvc_remote_authorization()
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":3,"time":120}}, timeout=3)
        sleep(10)
        self.io.drvr_door_open()
        self.tcam_reset_wait_service(REMOTECTRL_SERVICE_CLIENT)
        self.auto_no_accredit(0)
        self.partner.ck_s2s_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":4,"time": 0xFFFFFFFF}}, timeout=3)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":4,"time": 0xFFFFFFFF}})

    @allure.title("通知/获取远程授权启动状态_ReadyEntry下异常重启&取消/自动授权条件失败")#beta2
    @pytest.mark.sanity
    def test_caseid_1985567(self):
        self.auto_no_accredit(2)
        self.tsp.rvc_remote_authorization()
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":3,"time":120}}, timeout=3)
        self.partner.empty_all(1)
        self.tcam_reset_wait_service(REMOTECTRL_SERVICE_CLIENT)
        self.auto_no_accredit(1)
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":0,"time": 0xFFFFFFFF}}, timeout=100)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":0,"time": 0xFFFFFFFF}})

    @allure.title("通知/获取远程授权启动状态_ReadyEntry下异常重启&取消授权条件判断成功")#beta2
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985566(self):
        self.auto_no_accredit(2)
        self.tsp.rvc_remote_authorization()
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":3,"time":120}},  timeout=3)
        self.partner.empty_all(1)
        self.tcam_reset_wait_service(REMOTECTRL_SERVICE_CLIENT)
        self.auto_no_accredit(2)
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":0,"time": 0xFFFFFFFF}}, timeout=3)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":0,"time": 0xFFFFFFFF}})
        
    @allure.title("通知/获取远程电池加热信息_默认值")#beta2
    @pytest.mark.smoke
    def test_caseid_1988561(self):
        self.tcam_reset_wait_service(REMOTECTRL_SERVICE_CLIENT)
        sleep(20)   
        self.partner.ck_event_and_resp(REMOTECTRL_SERVICE_CLIENT, "RemoteBatteryHeatingInfo", {"heatInfo":{"modeSts":0,"heatSts":0,"source":0}})   
        

@allure.feature("SOA服务接口")
@allure.story("互联服务/RemoteCtrlService")
@pytest.mark.jishu1
class TestRemoteCtrlServiceMock(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu, tcp_down_mcu_ip="172.16.5.21", enable_inter_service=True)
        self.tsp = Tsp(**self.tc_config)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("CentralLockService", "client"),
                                     ("KeyService", "client"),
                                     ("RemoteCtrlService", "client"),
                                     ("VehicleSetStatusService", "client"),
                                     ("DoorService","client")])
        self.partner.send_method_request(
            VEHICLESETSTATUS_CLIENT, "SetMaintenanceMode", {"isOn": False})
        sleep(2)
        
    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.sd_tester.change_car_mode(0, do_assert=1)
        sleep(0.5)
        self.sd_tester.change_usage_mode(1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'EntityKeyWhiteListVers', self.dk.last_sync_time_entity)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr20, 'BLESlotKeyWhiteListVers', self.dk.last_sync_time_ble)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.dk.set_chassis_service_gear("P")
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.io.init_bgm_HW()  
        self.io.hood_door1_close()
        self.io.hood_door2_open()
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send() 
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(30)  # 避免防玩
        super().after_each_func(ecu, start=False)
    
    def auto_no_accredit(self, accredit):
        """
        0=满足自动授权, 1=不满足自动授权，不满足取消自动授权, 2=取消自动授权
        """
        if accredit == 0:   
            self.io.init_bgm_HW() 
            self.dk.set_chassis_service_gear("P")
            self.io.drvr_door_open()
            self.io.driver_seat_present()
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        elif accredit == 1:
            self.io.init_bgm_HW() 
            self.dk.set_chassis_service_gear("P")
            self.io.drvr_door_open()
            self.io.driver_seat_present()
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.dk.set_cenlock_sts(1)
        elif accredit ==2:
            self.io.init_bgm_HW() 
            self.dk.set_chassis_service_gear("P")
            self.dk.set_cenlock_sts(3)
        else:
            pass  
    
    def tcam_reset_wait_service(self, name):
        self.nucapp.tcam_power_off()
        sleep(30)
        self.nucapp.tcam_power_on()
        sleep(180)
        
    @allure.title("通知/获取远程授权启动状态_UnlockWait")#beta2
    @pytest.mark.full
    def test_caseid_1985536(self):
        self.auto_no_accredit(2)
        self.tsp.rvc_remote_authorization()
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":2,"time":0xFFFFFFFF}}, timeout=3)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":2,"time":0xFFFFFFFF}})
        
    @allure.title("通知/获取远程授权启动状态_UnlockWait超时进入Ready2L")#beta2
    @pytest.mark.full
    def test_caseid_1985572(self):
        self.auto_no_accredit(2)
        self.tsp.rvc_remote_authorization()
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":2,"time": 0xFFFFFFFF}}, timeout=3)
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":2,"time": 0xFFFFFFFF}})
        sleep(10)
        self.partner.ck_coming_event(REMOTECTRL_SERVICE_CLIENT,"RemoteAuthStartModeSts", {"info":{"sts":0,"time":0xFFFFFFFF}}, timeout=3),
        self.partner.send_request_and_ck_resp(REMOTECTRL_SERVICE_CLIENT, "GetRemoteAuthStartModeSts", {},
                                                                                         {"out": {"sts":0,"time":0xFFFFFFFF}})
        