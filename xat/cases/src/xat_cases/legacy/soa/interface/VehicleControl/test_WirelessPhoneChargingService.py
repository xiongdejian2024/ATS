import os
import sys
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_cases.legacy.soa.case_helper.common_lib import *
from xat_ecu.legacy.interface.bgm.bgm_env.change_bgm_env import *
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *


@allure.feature("SOA服务接口")
@allure.story("整车控制/WirelessPhoneChargingService")
@pytest.mark.jishu
class TestWirelessPhoneChargingService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("WirelessPhoneChargingService", "client"),
                                     ("KeyService", "client")])
        self.partner.method_default_timeout = 0.1
        time.sleep(5)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all()

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)
        self.ipdu.resume_all_bus_send()
       
########################################################2.0新增
    @allure.title("设置无线充电功能开关_遍历全部开关")
    @pytest.mark.smoke
    def test_caseid_1984605(self):
        dic ={ 0 : False, 1 : True} 
        self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":2 ,"isOn": True}]})
        self.partner.empty_all(0.5)
        for num in [0, 1, 2, 12]:
            for sig, sts in dic.items():
                self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":num ,"isOn": sts}]})
                if num == 0:
                    self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', sig, timeout=0.5)
                elif num == 1:
                    self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', sig, timeout=0.5)
                else:
                    self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', sig, timeout=0.5)
                    self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', sig, timeout=0.5)
            sleep(0.5)
            
    @allure.title("设置无线充电功能开关_下行PDU周期校验")
    @pytest.mark.full
    def test_caseid_1984730(self):
        self.kill_s2s_and_reconnect_service(WIRELESScharging_CLIENT)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":1 ,"isOn": True}]})
        sleep(2)
        self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":12 ,"isOn": False}]})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmi", [0])  
        self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmiPass", [1, 0])
        self.bgm_eth_inter.ck_period_time("WirelschrgActvReqFromHmi", 0.5, 0.4, 2)
        sleep(1)
        self.kill_s2s_and_reconnect_service(WIRELESScharging_CLIENT)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":0 ,"isOn": False}]})
        sleep(2)
        self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":2 ,"isOn": True}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmi", [0 , 1])  
        self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmiPass", [1])
        self.bgm_eth_inter.ck_period_time("WirelschrgActvReqFromHmiPass", 0.5, 0.4, 1)
        
    # @allure.title("设置无线充电功能开关_服务启动无默认值")
    # @pytest.mark.full
    # def test_caseid_1984862(self):
    #     self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":12 ,"isOn": False}]})
    #     self.kill_bgm_process()
    #     self.bgm_eth_inter.start_bgm_tcpdump()
    #     sleep(10)
    #     self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
    #     self.bgm_eth_inter.ck_signal_values("WirelschrgActvReqFromHmi", [])  
    #     self.bgm_eth_inter.ck_signal_values("WirelschrgActvReqFromHmiPass", [])  
        
    @allure.title("通知/获取无线充电信息_mars1主驾无线充电面板")
    @pytest.mark.full
    def test_caseid_1984895(self):
        self.ipdu.stop_send_pdu('connectivitycanfd', 0x303)
        self.kill_s2s_and_reconnect_service(WIRELESScharging_CLIENT)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'PhoneForgottenRmn', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCCtrlRes', 2)        
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCModuleSts', 10)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCFailureSts', 4)    
        self.partner.ck_s2s_event(WIRELESScharging_CLIENT, "WirelessChargingInfo", {"info":[{"zone": 0, "isForgotten": 1, "ctrlSts": 2, "chargingSts":4, "faults":[{"faultId": 4,"faultMsg":""}]},
                                                                                             {"zone": 1, "isForgotten": 255, "ctrlSts": 255, "chargingSts":255, "faults":[{"faultId": 255,"faultMsg":""}]}]})
        self.partner.send_request_and_ck_resp(WIRELESScharging_CLIENT, "GetWirelessChargingInfo", {"zone":[12]},
                                                                                    {"out": [{"zone": 0, "isForgotten": 1, "ctrlSts": 2, "chargingSts":4, "faults":[{"faultId": 4,"faultMsg":""}]},
                                                                                             {"zone": 1, "isForgotten": 255, "ctrlSts": 255, "chargingSts":255, "faults":[{"faultId": 255,"faultMsg":""}]}]})
                       
    @allure.title("通知/获取无线充电信息_遍历主驾无线充电所有功能&venus")
    @pytest.mark.sanity
    def test_caseid_1984896(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'PhoneForgottenRmn', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCFailureSts', 5)
        self.partner.empty_all(1)
        dic1 ={0:0, 1:255, 2:2, 3:3}
        dic = {0 : [4, 0], 1 : [0, 1], 2 : [1, 2], 3 : [4, 3], 4 : [4, 4], 5 : [4, 5], 
               6 : [255, 6], 7 : [3, 7], 8 : [255, 8], 9 : [255, 9], 10 : [4, 9], 
               11 : [255, 9], 12 : [4, 9], 13 : [255, 9] , 14 : [255, 9], 15 : [255, 9]}
        temp = (-1,-1,-1,-1)
        for For in [0, 1]:
            self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'PhoneForgottenRmn', For)
            for Res, ctrl in dic1.items():
                self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCCtrlRes', Res)        
                for sig, flt, in dic.items():
                    logger.info(f"当前遗忘提醒.{For},当前控制反馈.{ctrl},当前状态信息.{flt[0]},当前故障.{flt[1]}")
                    self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCModuleSts', sig)
                    self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCFailureSts', sig)
                    if  temp !=(For, ctrl, flt[0], flt[1]):
                        self.partner.ck_s2s_event(WIRELESScharging_CLIENT, "WirelessChargingInfo", {"info":[{"zone": 0, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        self.partner.send_request_and_ck_resp(WIRELESScharging_CLIENT, "GetWirelessChargingInfo", {"zone":[0]},
                                        {"out": [{"zone": 0, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        temp=(For, ctrl, flt[0], flt[1])
                    else:
                        self.partner.ck_no_event(WIRELESScharging_CLIENT, "WirelessChargingInfo")
                        self.partner.send_request_and_ck_resp(WIRELESScharging_CLIENT, "GetWirelessChargingInfo", {"zone":[0]},
                                        {"out": [{"zone": 0, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        temp=(For, ctrl, flt[0], flt[1])
                    self.partner.empty_all(0.5)  
                       
    @allure.title("通知/获取无线充电信息_遍历主驾无线充电所有功能&Mars1")
    @pytest.mark.smoke
    def test_caseid_1984606(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'PhoneForgottenRmn', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCFailureSts', 5)
        self.partner.empty_all(1)
        dic1 ={0:0, 1:255, 2:2, 3:3}
        dic = {0 : [4, 0], 1 : [0, 1], 2 : [1,2], 3 : [4,3], 4 : [4,4], 5 : [4,5], 6 : [255,6], 
               7 : [3, 7], 8 : [255,8], 9 : [255,9], 10 : [4,9], 11 : [255,9],  12 : [4,9], 13 : [255,9] , 14 : [255,9], 15 : [255,9]}
        temp = (-1,-1,-1,-1)
        for For in [0, 1]:
            self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'PhoneForgottenRmn', For)
            for Res, ctrl in dic1.items():
                self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCCtrlRes', Res)        
                for sig, flt, in dic.items():
                    logger.info(f"当前遗忘提醒.{For},当前控制反馈.{ctrl},当前状态信息.{sig},当前故障.{flt[1]}")
                    self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCModuleSts', sig)
                    self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCFailureSts', sig)
                    if  temp !=(For, ctrl, flt[0], flt[1]):
                        self.partner.ck_s2s_event(WIRELESScharging_CLIENT, "WirelessChargingInfo", {"info":[{"zone": 0, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        self.partner.send_request_and_ck_resp(WIRELESScharging_CLIENT, "GetWirelessChargingInfo", {"zone":[0]},
                                        {"out": [{"zone": 0, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        temp=(For, ctrl, flt[0], flt[1])
                    else:
                        self.partner.ck_no_event(WIRELESScharging_CLIENT, "WirelessChargingInfo")
                        self.partner.send_request_and_ck_resp(WIRELESScharging_CLIENT, "GetWirelessChargingInfo", {"zone":[0]},
                                        {"out": [{"zone": 0, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        temp=(For, ctrl, flt[0], flt[1])
                    self.partner.empty_all(0.5)    
                    
    @allure.title("通知/获取无线充电信息_遍历副驾无线充电所有功能")
    @pytest.mark.sanity
    def test_caseid_1984607(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'PhoneForgottenRmnPass', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCFailureStsPass', 5)
        self.partner.empty_all(1)
        dic1 ={0:0, 1:255, 2:2, 3:3}
        dic = {0 : [4, 0], 1 : [0, 1], 2 : [1,2], 3 : [4,3], 4 : [4,4], 5 : [4,5], 6 : [255,6], 
               7 : [3, 7], 8 : [255,8], 9 : [255,9], 10 : [4,9], 11 : [255,9],  12 : [4,9], 13 : [255,9] , 14 : [255,9], 15 : [255,9]}
        temp = (-1,-1,-1,-1)
        for For in [0, 1]:
            self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'PhoneForgottenRmnPass', For)
            for Res, ctrl in dic1.items():
                self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCCtrlResPass', Res)         
                for sig, flt, in dic.items():
                    logger.info(f"当前遗忘提醒.{For},当前控制反馈.{ctrl},当前状态信息.{flt[0]},当前故障.{flt[1]}")
                    self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCModuleStsPass', sig)
                    self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCFailureStsPass', sig)
                    if  temp !=(For, ctrl, flt[0], flt[1]):
                        self.partner.ck_s2s_event(WIRELESScharging_CLIENT, "WirelessChargingInfo", {"info":[{"zone": 1, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        self.partner.send_request_and_ck_resp(WIRELESScharging_CLIENT, "GetWirelessChargingInfo", {"zone":[1]},
                                        {"out": [{"zone": 1, "isForgotten": For, "ctrlSts": ctrl, "chargingSts": flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        temp=(For, ctrl, flt[0], flt[1])
                    else:
                        self.partner.ck_no_event(WIRELESScharging_CLIENT, "WirelessChargingInfo")
                        self.partner.send_request_and_ck_resp(WIRELESScharging_CLIENT, "GetWirelessChargingInfo", {"zone":[1]},
                                        {"out": [{"zone": 1, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        temp=(For, ctrl, flt[0], flt[1])
                    self.partner.empty_all(0.5)                 
                        
    @allure.title("通知/获取无线充电信息_遍历前排所有区域无线充电所有功能")
    @pytest.mark.full
    def test_caseid_1984608(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'PhoneForgottenRmnPass', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCFailureStsPass', 5)
        self.partner.empty_all(1)
        dic1 ={0:0, 1:255, 2:2, 3:3}
        dic = {0 : [4, 0], 1 : [0, 1], 2 : [1,2], 3 : [4,3], 4 : [4,4], 5 : [4,5], 6 : [255,6], 
               7 : [3, 7], 8 : [255,8], 9 : [255,9], 10 : [4,9], 11 : [255,9],  12 : [4,9], 13 : [255,9] , 14 : [255,9], 15 : [255,9]}
        temp = (-1,-1,-1,-1)
        for For in [0, 1]:
            self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'PhoneForgottenRmnPass', For)
            self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'PhoneForgottenRmn', For)
            for Res, ctrl in dic1.items():
                self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCCtrlResPass', Res)  
                self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCCtrlRes', Res)        
                for sig, flt, in dic.items():
                    logger.info(f"当前遗忘提醒.{For},当前控制反馈.{ctrl},当前状态信息.{flt[0]},当前故障.{flt[1]}")
                    self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCModuleStsPass', sig)
                    self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCModuleSts', sig)
                    self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCFailureStsPass', sig)
                    self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCFailureSts', sig)
                    if  temp !=(For, ctrl, flt[0], flt[1]):
                        self.partner.ck_s2s_event(WIRELESScharging_CLIENT, "WirelessChargingInfo", {"info":[{"zone": 0, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]},{"zone": 1, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        self.partner.send_request_and_ck_resp(WIRELESScharging_CLIENT, "GetWirelessChargingInfo", {"zone":[2]},
                                        {"out": [{"zone": 0, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]},{"zone": 1, "isForgotten": For, "ctrlSts": ctrl, "chargingSts": flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        temp=(For, ctrl, flt[0], flt[1])
                    else:
                        self.partner.ck_no_event(WIRELESScharging_CLIENT, "WirelessChargingInfo")
                        self.partner.send_request_and_ck_resp(WIRELESScharging_CLIENT, "GetWirelessChargingInfo", {"zone":[2]},
                                        {"out": [{"zone": 0, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]},{"zone": 1, "isForgotten": For, "ctrlSts": ctrl, "chargingSts":flt[0], "faults":[{"faultId": flt[1], "faultMsg": ""}]}]})
                        temp=(For, ctrl, flt[0], flt[1])
                    self.partner.empty_all(0.5)
                        
    @allure.title("通知/获取无线充电信息_主驾默认值%副驾有效值停发总线恢复总线")
    @pytest.mark.full
    def test_caseid_1984609(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'PhoneForgottenRmnPass', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'PhoneForgottenRmn', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCCtrlResPass', 3)  
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCCtrlRes', 1)        
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCModuleStsPass', 12)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCModuleSts', 13)
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCFailureStsPass', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCFailureSts', 10)    
        self.partner.ck_s2s_event(WIRELESScharging_CLIENT, "WirelessChargingInfo", {"info":[{"zone": 0, "isForgotten": 1, "ctrlSts": 255, "chargingSts":255, "faults":[{"faultId": 9,"faultMsg":""}]},
                                                                                             {"zone": 1, "isForgotten": 1, "ctrlSts": 3, "chargingSts":4, "faults":[{"faultId": 0,"faultMsg":""}]}]})
        self.restart_bgm_and_connect_service(WIRELESScharging_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(WIRELESScharging_CLIENT, "GetWirelessChargingInfo", {"zone":[12]},
                                              {"out": [{"zone": 0, "isForgotten": 255, "ctrlSts": 255, "chargingSts":255, "faults":[{"faultId": 255,"faultMsg":""}]},
                                                       {"zone": 1, "isForgotten": 255, "ctrlSts": 255, "chargingSts":255, "faults":[{"faultId": 255,"faultMsg":""}]}]}, timeout=0.2)
        
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(WIRELESScharging_CLIENT, "WirelessChargingInfo", {"info":[{"zone": 0, "isForgotten": 1, "ctrlSts": 255, "chargingSts":255, "faults":[{"faultId": 9,"faultMsg":""}]},
                                                                                             {"zone": 1, "isForgotten": 1, "ctrlSts": 3, "chargingSts":4, "faults":[{"faultId": 0,"faultMsg":""}]}]})
        self.partner.send_request_and_ck_resp(WIRELESScharging_CLIENT, "GetWirelessChargingInfo", {"zone":[2]},
                                              {"out": [{"zone": 0, "isForgotten": 1, "ctrlSts": 255, "chargingSts":255, "faults":[{"faultId": 9,"faultMsg":""}]},
                                                                                             {"zone": 1, "isForgotten": 1, "ctrlSts": 3, "chargingSts":4, "faults":[{"faultId": 0,"faultMsg":""}]}]}, timeout=0.2)
        
    @allure.title("通知无线充电信息_所有区域无线充电启动场景")
    @pytest.mark.full
    def test_caseid_1984612(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'PhoneForgottenRmnPass', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'PhoneForgottenRmn', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCCtrlResPass', 3)  
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCCtrlRes', 3)        
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCModuleStsPass', 2)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCModuleSts', 2)
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCFailureStsPass', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCFailureSts', 0)  
        self.restart_bgm_and_connect_service(WIRELESScharging_CLIENT)
        self.partner.ck_s2s_event(WIRELESScharging_CLIENT, "WirelessChargingInfo", {"info":[{"zone": 0, "isForgotten": 1, "ctrlSts": 3, "chargingSts":1, "faults":[{"faultId": 0,"faultMsg":""}]},
                                                                                             {"zone": 1, "isForgotten": 1, "ctrlSts": 3, "chargingSts":1, "faults":[{"faultId": 0,"faultMsg":""}]}]})
     
    @allure.title("通知/获取无线充电信息_前排所有区域无线充电默认值重启校验event")
    @pytest.mark.full
    def test_caseid_1984731(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'PhoneForgottenRmnPass', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'PhoneForgottenRmn', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCCtrlResPass', 1)  
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCCtrlRes', 1)        
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCModuleStsPass', 13)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCModuleSts', 13)
        self.ipdu.set(self.ipdu.connectivitycanfd.Wpc3ConnFr01, 'WPCFailureStsPass', 10)
        self.ipdu.set(self.ipdu.connectivitycanfd.WpcConnFr02, 'WPCFailureSts', 10)  
        self.restart_bgm_and_connect_service(WIRELESScharging_CLIENT)
        self.partner.ck_s2s_event(WIRELESScharging_CLIENT, "WirelessChargingInfo", {"info":[{"zone": 0, "isForgotten": True, "ctrlSts": 255, "chargingSts":255, "faults":[{"faultId": 9,"faultMsg":""}] },
                                                                                             {"zone": 1, "isForgotten": True, "ctrlSts": 255, "chargingSts":255, "faults":[{"faultId": 9,"faultMsg":""}] }]})
    
    ########################################################200FU新增CR########################################################
    @allure.title("设置无线充电功能开关_服务启动后，开始周期发送记忆值&&请求参数isOn做持久化存储")
    @pytest.mark.sanity
    def test_caseid_1987973(self):
        # 全部前排初始值为True时：
        for num in [0, 1, 2, 12]:
            logger.info(f"num信号{num}")
            self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":2 ,"isOn": True}]}, timeout=1)
            self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":num ,"isOn": False}]}, timeout=1)
            sleep(2)
            self.kill_s2s_and_reconnect_service(WIRELESScharging_CLIENT)
            self.bgm_eth_inter.start_bgm_tcpdump()
            sleep(3)
            if num == 0:
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmi", [0])  
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmiPass", [1]) 
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', 0, timeout=1)
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', 1, timeout=1)
            elif num == 1:
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmi", [1])
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmiPass", [0])  
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', 1, timeout=1)
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', 0, timeout=1)
            else:
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmi", [0])  
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmiPass", [0])  
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', 0, timeout=1)
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', 0, timeout=1)
        # 全部前排初始值为False时：
        for num in [0, 1, 2, 12]:
            logger.info(f"num信号{num}")
            self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":2 ,"isOn": False}]}, timeout=1)
            self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":num ,"isOn": True}]}, timeout=1)
            sleep(2)
            self.kill_s2s_and_reconnect_service(WIRELESScharging_CLIENT)
            self.bgm_eth_inter.start_bgm_tcpdump()
            sleep(3)
            if num == 0:
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmi", [1])  
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmiPass", [0]) 
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', 1, timeout=1)
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', 0, timeout=1)
            elif num == 1:
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmi", [0])  
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmiPass", [1])  
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', 0, timeout=1)
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', 1, timeout=1)
            else:
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmi", [1])  
                self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmiPass", [1])  
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', 1, timeout=1)
                self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', 1, timeout=1)

    @allure.title("设置无线充电功能开关_首次上下线服务启动后获取默认值")
    @pytest.mark.sanity
    def test_caseid_1988005(self):
        self.del_s2s_db()
        self.restart_bgm_and_connect_service(WIRELESScharging_CLIENT)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmi', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'WirelschrgActvReqFromHmiPass', 1, timeout=0.5)
        self.partner.send_method_request(WIRELESScharging_CLIENT, "SetWirelessCharging", {"req":[{"zone":2 ,"isOn": False}]}, timeout=0.3)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmi", [0])  
        self.bgm_eth_inter.ck_ordered_array("WirelschrgActvReqFromHmiPass", [0])  
        self.bgm_eth_inter.ck_period_time("WirelschrgActvReqFromHmi", 0.5, 0.2, 3)
        self.bgm_eth_inter.ck_period_time("WirelschrgActvReqFromHmiPass", 0.5, 0.2, 3)
