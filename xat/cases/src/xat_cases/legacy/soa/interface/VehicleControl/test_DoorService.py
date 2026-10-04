# -*- coding: utf-8 -*-
"""
@File        : test_DoorService.py
@Author      : jishu.duan_ext
@Time        : 2023/05/23 18:00 PM
@Description : Test SOA for DoorService
"""

import pytest
import allure
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.common.data_type_handing import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.soa.case_helper.test_base import *
from xat_cases.legacy.soa.case_helper.utils import *


@allure.feature("SOA服务接口")
@allure.story("整车控制/DoorService")
@pytest.mark.jishu
class TestDoorService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("DoorService","client"),
                                     ("VehicleSetStatusService","client"),
                                     ("TailGateService", "client")])
        self.partner.method_default_timeout = 0.1
        sleep(1)
    
    def after_class(self, ecu):
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.set_nopeople_incar()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4})
        self.dk.reset_bncm_digital_keyinfo()
        self.ipdu.set_vehspd(0)
        sleep(0.5)
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)  
        self.io.init_bgm_HW()
        self.io.hood_door1_close()
        self.io.hood_door2_open()
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.partner.empty_all()
        self.set_Actv_sig_all(0)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftStsToHmi', 2)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'ChdLockRightStsToHmi', 2) 
    

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        self.sd_tester.stop_tester_present()
        if ecu.get("testresult") != "Pass":
            logger.error("case失败,需等待5s让环境恢复")
            sleep(5)
        else:
            logger.info("case成功,需等待3s让环境恢复")
            sleep(3)
        super().after_each_func(ecu)
        
    def set_Actv_sig_all(self, sigvalue):
        """
        遍历车门破冰四门信号
        @param sigvalue: 遍历车门破冰四门信号
        """
        dic = {"Drvr" : 7, "Pass" : 1 , "LeRe" : 2, "RiRe" : 2}
        for key, value in dic.items():
            if key == "Drvr" or key == "Pass":
                self.ipdu.set(eval(f"self.ipdu.bodycan.{key[0:1]}dmBodyFr0{value}"),f"IceBreakDoor{key}Actv", sigvalue )
            else:  
                self.ipdu.set(eval(f"self.ipdu.bodycan.R{key[0:1].lower()}dmBodyFr0{value}"),f"IceBreakDoor{key}Actv", sigvalue )
      
    def all_door_open_close(self,swith):
        """
        @param swith: 表示四门open=0 or close=1
        """
        for door in ["drvr","pass","lere","rire"]:
            if swith == 0:
                (eval(f"self.io.{door}_door_open() "))
            else:
                (eval(f"self.io.{door}_door_close() "))
        
    def set_door_fault(self, door: str, sig: int, signalvalue: int):
        """
        @param door: 表示门位置, All, Drvr, Pass, LeRe, RiRe
        """
        if door == "All" :
            for door in ["Drvr", "Pass", "LeRe", "RiRe"]:
                self.set_door_fault(door, sig, signalvalue)
        else:
            self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0:1]}podBodyFr01"), 
                               f"DtcInfDoor{door}Boolean{sig}", signalvalue)
    
    def set_door_fault_clear(self):
        """
        @param fault: 遍历恢复四门故障
        """
        for fault in range(4):
            self.set_door_fault("All", fault + 1, 0)
        self.partner.empty_all(1)
              
    @allure.title("通知/获取车门破冰功能激活状态_全部车门未激活&全部车门激活")
    @pytest.mark.full
    def test_caseid_1980562(self):
        self.set_Actv_sig_all(1)
        self.partner.empty_all(1)
        for sigvalue in range(2):
            logger.info(f"当前value.{sigvalue}")
            self.set_Actv_sig_all(sigvalue)
            sleep(0.5)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorIceBreakActiveStatus", {"sts": {"sts": sigvalue}})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetDoorIceBreakActiveStatus", {"doors": [4]},
                                                 {"out": [{"id": 0, "sts": sigvalue},
                                                         {"id": 1, "sts": sigvalue},
                                                         {"id": 2, "sts": sigvalue}, 
                                                         {"id": 3, "sts": sigvalue}]})
       
    @allure.title("通知/获取车门破冰功能激活状态_遍历四门破冰激活&未激活")
    @pytest.mark.sanity
    def test_caseid_1980564(self):
        self.set_Actv_sig_all(1)
        self.partner.empty_all(1)
        dic = {"Drvr" : [7, 0], "Pass" : [1, 1] , "LeRe" : [2, 2], "RiRe" : [2, 3]}
        for key, value in dic.items():
            for sigvalue in range(2):
                logger.info(f"当前value.{sigvalue}, 当前门.{key}, 当前value.{value}")
                if key in["Drvr", "Pass"]:
                    self.ipdu.set(eval(f"self.ipdu.bodycan.{key[0:1]}dmBodyFr0{value[0]}"), f"IceBreakDoor{key}Actv", sigvalue )
                else:  
                    self.ipdu.set(eval(f"self.ipdu.bodycan.R{key[0:1].lower()}dmBodyFr0{value[0]}"), f"IceBreakDoor{key}Actv", sigvalue )
                self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorIceBreakActiveStatus", {"sts": {"id":value[1], "sts": sigvalue}})
                logger.info(f"当前value.{value[1]}, 当前sig.{sigvalue}")
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorIceBreakActiveStatus", {"doors": [4]},
                                                {"out": [{"id":value[1], "sts": sigvalue}]})   
                         
    @allure.title("车门破冰功能激活状态_校验停发总线&恢复总线值")
    @pytest.mark.full
    def test_caseid_1980568(self):
        self.set_Actv_sig_all(1)
        self.partner.empty_all(1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False) 
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetDoorIceBreakActiveStatus", {"doors": [4]},
                                              {"out": [{"id": 0, "sts": 255}, 
                                                      {"id": 1, "sts": 255},
                                                      {"id": 2, "sts": 255},
                                                      {"id": 3, "sts": 255}]}, timeout=0.5)
        self.ipdu.resume_all_bus_send()
        sleep(2)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorIceBreakActiveStatus", {"sts": {"id":0, "sts": 1}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorIceBreakActiveStatus", {"sts": {"id":1, "sts": 1}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorIceBreakActiveStatus", {"sts": {"id":2, "sts": 1}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorIceBreakActiveStatus", {"sts": {"id":3, "sts": 1}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorIceBreakActiveStatus", {"doors": [4]},
                                              {"out": [{"id": 0, "sts": 1}, 
                                                      {"id": 1, "sts": 1},
                                                      {"id": 2, "sts": 1},
                                                      {"id": 3, "sts": 1}]})   
        
    @allure.title("通知车门破冰功能激活状态_校验bgm重启后event事件")
    @pytest.mark.sanity
    def test_caseid_1984244(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'IceBreakDoorDrvrActv', 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'IceBreakDoorPassActv', 1)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'IceBreakDoorLeReActv', 1)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'IceBreakDoorRiReActv', 1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT) 
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorIceBreakActiveStatus", {"sts": {"sts": 1}})
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'IceBreakDoorDrvrActv', 0)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'IceBreakDoorPassActv', 0)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'IceBreakDoorLeReActv', 0)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'IceBreakDoorRiReActv', 0)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT) 
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorIceBreakActiveStatus", {"sts": {"sts": 0}})    
      
    @allure.title("破冰场景下控制车门开启最小角度_遍历四门_总线信号校验")
    @pytest.mark.full
    def test_caseid_1980571(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(0.5)
        dic = {"Drvr" : [7, 0], "Pass" : [1, 1] , "LeRe" : [2, 2], "RiRe" : [2, 3]}
        for key, value in dic.items():
            logger.info(f"当前门.{key},当前value.{value}")
            if key in ["Drvr", "Pass"]:
                self.ipdu.set(eval(f"self.ipdu.bodycan.{key[0:1]}dmBodyFr0{value[0]}"), f"IceBreakDoor{key}Actv", 1 )
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, f"Door{key}TargPercReqFromHmi",5, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, f"Door{key}TargPercReqFromHmi",101, timeout=0.5)
                sleep(0.5)
            else :  
                self.ipdu.set(eval(f"self.ipdu.bodycan.R{key[0:1].lower()}dmBodyFr0{value[0]}"), f"IceBreakDoor{key}Actv", 1 )
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, f"Door{key}TargPercReqFromHmi",7, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, f"Door{key}TargPercReqFromHmi",101, timeout=0.5)
             
    @allure.title("破冰场景下控制车门开启最小角度_全部车门_下行pdu校验")
    @pytest.mark.full
    def test_caseid_1980572(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'IceBreakDoorDrvrActv', 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'IceBreakDoorPassActv', 1)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'IceBreakDoorLeReActv', 1)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'IceBreakDoorRiReActv', 1)
        sleep(1)
        self.dk.set_cenlock_sts(3)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'IceBreakDoorDrvrActv', 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'IceBreakDoorPassActv', 1)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'IceBreakDoorLeReActv', 1)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'IceBreakDoorRiReActv', 1)
        self.partner.empty_all(0.5)
        self.dk.set_cenlock_sts(2)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'IceBreakDoorDrvrActv', 1)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'IceBreakDoorPassActv', 1)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'IceBreakDoorLeReActv', 1)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'IceBreakDoorRiReActv', 1)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('DoorDrvrTargPercReqFromHmi', [5, 5, 5, 101])
        self.bgm_eth_inter.ck_signal_values('DoorPassTargPercReqFromHmi', [5, 5, 5, 101])
        self.bgm_eth_inter.ck_signal_values('DoorLeReTargPercReqFromHmi', [7, 7, 7, 101])
        self.bgm_eth_inter.ck_signal_values('DoorRiReTargPercReqFromHmi', [7, 7, 7, 101])
        
    @allure.title("破冰场景下控制车门开启最小角度_开门后锁动作_下行pdu校验")
    @pytest.mark.full
    def test_caseid_1987658(self):    
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr07, 'IceBreakDoorDrvrActv', 1)
        self.dk.set_cenlock_sts(1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.PdmBodyFr01, 'IceBreakDoorPassActv', 1)
        self.dk.set_cenlock_sts(3)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.RldmBodyFr02, 'IceBreakDoorLeReActv', 1)
        self.dk.set_cenlock_sts(1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.RrdmBodyFr02, 'IceBreakDoorRiReActv', 1)
        self.dk.set_cenlock_sts(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
        self.bgm_eth_inter.ck_signal_values('DoorDrvrTargPercReqFromHmi', [5, 5, 5, 101, 5, 5, 5, 101])
        self.bgm_eth_inter.ck_signal_values('DoorPassTargPercReqFromHmi', [5, 5, 5, 101, 5, 5, 5, 101])
        self.bgm_eth_inter.ck_signal_values('DoorLeReTargPercReqFromHmi', [7, 7, 7, 101])
        self.bgm_eth_inter.ck_signal_values('DoorRiReTargPercReqFromHmi', [7, 7, 7, 101])
      
    @allure.title("获取门最小角度状态提示 _遍历四车门未提示&提示")
    @pytest.mark.sanity
    def test_caseid_1980574(self):
        dic = {"Drvr" :  0, "Pass" : 1 , "LeRe" : 2, "RiRe" : 3}
        dic1 ={0 : False, 1 : True}
        for key, value in dic.items():
            self.ipdu.set(eval(f"self.ipdu.bodycan.{key[0:1]}podBodyFr01"), 
                                    f"Door{key}MInAngleFb", 1)
        self.partner.empty_all(1)
        for key, value in dic.items():
            for sig, bool1 in dic1.items():
                logger.info(f"当前信号值.{sig}, 当前门.{key},当前value.{value}")
                self.ipdu.set(eval(f"self.ipdu.bodycan.{key[0:1]}podBodyFr01"), 
                                    f"Door{key}MInAngleFb", sig)
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorMinAngleSts", {"doors": [value]},
                                                {"out": [{"id": value, "minAngleReminder": bool1}]})
                       
    @allure.title("获取门最小角度状态提示_all") #1.4新增
    @pytest.mark.full
    def test_caseid_1984298(self):
        dic = {0: False, 1: True}
        for sig, sts in dic.items():
            for key in ["Drvr", "Pass", "LeRe", "RiRe"]: 
                self.ipdu.set(eval(f"self.ipdu.bodycan.{key[0:1]}podBodyFr01"), f"Door{key}MInAngleFb", sig)
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorMinAngleSts", {"doors": [4]},
                                                        {"out": [{"id": 0, "minAngleReminder": sts}, 
                                                                 {"id": 1, "minAngleReminder": sts}, 
                                                                 {"id": 2, "minAngleReminder": sts}, 
                                                                 {"id": 3, "minAngleReminder": sts}]})
        self.partner.empty_all(1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False) 
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorMinAngleSts", {"doors": [4]},
                                                        {"out": [{"id": 0, "minAngleReminder": False}, 
                                                                 {"id": 1, "minAngleReminder": False}, 
                                                                 {"id": 2, "minAngleReminder": False}, 
                                                                 {"id": 3, "minAngleReminder": False}]})

    @allure.title("设置/取消 D档自动关门—业务功能校验")
    @pytest.mark.full
    def test_caseid_1981077(self):
        self.dk.set_door_sts([1, 1, 1, 1, 0])
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetAutoCloseTrigger", {"trigger": 0})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 3)
        self.sd_tester.change_usage_mode(13)  # 切usgmode为Drving模式
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 2)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 2)
        sleep(3)
        self.partner.empty_all(0.5)    
        self.sd_tester.change_usage_mode(11)
        self.dk.set_door_sts([1, 1, 1, 1, 0 ])
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "CancelAutoCloseTrigger", {"trigger": 0})
        sleep(0.1)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 0)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 0)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 0)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 0)
  
    @allure.title("设置D档自动关门_下行PDU校验")
    @pytest.mark.sanity
    def test_caseid_1980589(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetAutoCloseTrigger", {"trigger": 0})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SetPwrDoorClsInGearDR', [1])
                  
    @allure.title("取消D档自动关门_下行PDU校验")
    @pytest.mark.full
    def test_caseid_1980593(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "CancelAutoCloseTrigger", {"trigger": 0})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SetPwrDoorClsInGearDR', [0])
        
    @allure.title("取消D档自动关门_下电无记忆值报文发送调用再发")
    @pytest.mark.full
    def test_caseid_1984957(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "CancelAutoCloseTrigger", {"trigger": 0})
        sleep(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(3)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "CancelAutoCloseTrigger", {"trigger": 0}, timeout=1.5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
        self.bgm_eth_inter.ck_signal_values('SetPwrDoorClsInGearDR', [0])
               
    @allure.title("设置D档自动关门_启动后无下行PDU下发")
    @pytest.mark.full
    def test_caseid_1984958(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetAutoCloseTrigger", {"trigger": 0})
        sleep(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SetPwrDoorClsInGearDR', [])         
               
    @allure.title("通知/获取D档自动关门设置状态_下电记忆值")
    @pytest.mark.full
    def test_caseid_1980597(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetAutoCloseTrigger", {"trigger": 0})
        sleep(0.5)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "AutoCloseTrigger", {"triggers": [0]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoCloseTrigger", {},
                                              {"out": [0]})
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "AutoCloseTrigger", {"triggers": [0]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoCloseTrigger", {},
                                              {"out": [0]})
    
    @allure.title("通知/获取取消D档自动关门_下电记忆值")
    @pytest.mark.full
    def test_caseid_1984953(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "CancelAutoCloseTrigger", {"trigger": 0})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "AutoCloseTrigger", {"triggers": []})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoCloseTrigger", {},
                                              {"out": []})
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "AutoCloseTrigger", {"triggers": []})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoCloseTrigger", {},
                                              {"out": []})
        
    @allure.title("通知/获取D档自动关门设置状态_首次下线")
    @pytest.mark.full
    def test_caseid_1980599(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetAutoCloseTrigger", {"trigger": 0})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "AutoCloseTrigger", {"triggers": [0]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoCloseTrigger", {},
                                              {"out": [0]}, timeout=0.5)
        self.partner.empty_all(1)
        self.del_s2s_db()
        sleep(1)
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoCloseTrigger", {},
                                              {"out": []})
        
    @allure.title("获取门开关状态_遍历四门门开/门关")
    @pytest.mark.full
    def test_caseid_1980577(self):
        self.all_door_open_close(1)
        self.partner.empty_all(1)
        dic = {"drvr":0, "pass":1, "lere":2, "rire":3}
        for key, value in dic.items():
            for door_sts in ["open", "close"]:
                logger.info(f"当前门状态.{door_sts}, 当前门.{key}")
                if door_sts == "open":
                    (eval(f"self.io.{key}_door_open()"))
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatus", {"doors": [value]},
                                                                                                  {"out": [{"id": value, "isOpen": True}]})
                else:
                    (eval(f"self.io.{key}_door_close()"))
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatus", {"doors": [value]},
                                                                                                  {"out": [{"id": value, "isOpen": False}]})
     
    @allure.title("获取电动门运动状态_遍历四门所有运动状态")
    @pytest.mark.full
    def test_caseid_1980601(self):
        # 所有运动状态0:全开;1:关闭中;2:全关;3:未使用;4:未使用;5:开启中;6:悬停;7:未知;8:关闭中减速;9:开启中减速;10:半锁中;11:default
        dic = {"Drvr" :  0, "Pass" : 1 , "LeRe" : 2, "RiRe" : 3}
        for key, value in dic.items():
            self.ipdu.set(eval(f"self.ipdu.bodycan.{key[0:1]}podBodyFr01"), f"DoorOpener{key}Sts_0_{key[0:1]}podBodySignalIPdu01", 5)
        self.partner.empty_all(1)
        door_dic = {
                    0: 7, 1: 2, 2: 5, 3: 9, 4: 6, 5: 0, 6: 1, 7: 8, 8: 6, 9: 10, 10: 6, 
                    11: 65535, 12:  65535, 13: 65535, 14: 65535, 15: 65535
                       }
        for key, value in dic.items():
            for sigkey, sigvalue in door_dic.items():
                logger.info(f"当前信号.{sigkey},当前门.{key},当前参数.{sigvalue}")
                self.ipdu.set(eval(f"self.ipdu.bodycan.{key[0:1]}podBodyFr01"), f"DoorOpener{key}Sts", sigkey)
                if sigkey in [11, 12, 13, 14, 15]:
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetStatus", {"doors": [value]},
                                {"out": [{"id": value, "sts": 65535}]})
                else:
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetStatus", {"doors": [value]},
                                              {"out": [{"id": value, "sts": sigvalue}]}) 
                sleep(0.5)
    
    @allure.title("获取电动门防夹状态_遍历四门激活&未激活")
    @pytest.mark.full
    def test_caseid_1980602(self):
        dic = {"Drvr" :  0, "Pass" : 1 , "LeRe" : 2, "RiRe" : 3}
        for door_key, door_id in dic.items():
            self.ipdu.set(eval(f"self.ipdu.bodycan.{door_key[0:1]}podBodyFr01"), f"Door{door_key}AntiPnch", 1)
            self.partner.empty_all(0.5)      
        sig_dic = {0 : False, 1 : True}
        for door_key, door_id in dic.items(): 
            for sigkey, sigvalue in sig_dic.items():
                logger.info(f"当前信号.{sigkey},当前门.{door_key},当前参数.{sigvalue}")
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door_key[0:1]}podBodyFr01"), f"Door{door_key}AntiPnch", sigkey)#设置未激活
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAntiPinch", {"doors": [door_id]},
                                                {"out": [{"door": door_id, "isAntiPinch": sigvalue}]})
        sleep(1)
    
    @allure.title("设置电动门百分比_遍历四门_总线信号校验")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1980608(self):
        dic = {0 : [5664, "Drvr"], 1 : [5665, "Pass"], 2 : [5666, "LeRe"], 3 : [5667, "RiRe"]}
        for key_id, data_id in dic.items():  
            for pos1 in [0, 100, 90, 87, 23, 45, 99, 43]:
                logger.info(f"当前门.{data_id},当前信号.{pos1}")
                self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": key_id, "pos": pos1}]}) 
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, f"Door{data_id[1]}TargPercReqFromHmi", pos1)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, f"Door{data_id[1]}TargPercReqFromHmi", 101)
                sleep(1)           
                
    @allure.title("设置电动门百分比_校验报文发送打断逻辑v1.4")#待1.4修改
    @pytest.mark.full
    def test_caseid_1980609(self):   
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 0, "pos": 10}]})
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 0, "pos": 50}]})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("DoorDrvrTargPercReqFromHmi", [10, 50, 50, 50, 101])
        
    @allure.title("设置电动门百分比_服务上线后无需主动下发报文")#待1.4修改
    @pytest.mark.full
    def test_caseid_1984965(self):  
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 0, "pos": 10}]})
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("DoorDrvrTargPercReqFromHmi", [])
            
    @allure.title("获取电动门开度百分比_遍历四门")#等1.4修复
    @pytest.mark.full
    def test_caseid_1980611(self): 
        dic = {"Drvr": 0, "Pass": 1, "LeRe": 2, "RiRe": 3}
        for door, key_id in dic.items():
            for pos1 in [0, 100, 101, 127, 50, 20]:
                logger.info(f"当前门.{door},当前id.{key_id}, 当前值.{pos1}")
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0]}podBodyFr01"), f"Door{door}PercPosn", pos1)
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetPosition", {"doors": [key_id]},
                                                {"out": [{"id": key_id, "pos": pos1}]})

    @allure.title("获取门开启角度_遍历四门") ##待确认
    @pytest.mark.full
    def test_caseid_1980687(self):  
        door = {"Drvr": 0, "Pass": 1, "LeRe": 2, "RiRe": 3 }
        for agl in [0, 71, 85, 14, 30, 50, 10, 40]:
            for key, value in door.items():
                logger.info(f"当前key.{key},当前agl.{agl}")
                self.ipdu.set(eval(f"self.ipdu.bodycan.{key[0]}podBodyFr01"), f"Door{key}Posn_0_{key[0]}podBodySignalIPdu01", agl)
                if agl <=65:
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorAngle", {"doors": [value]},
                                                    {"out": [{"id": value, "angle": agl}]})  
                else:
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorAngle", {"doors": [value]},
                                                {"out": [{"id": value, "angle": 255}]}) 
        
    @allure.title("设置电动门最大开度百分比_校验报文打断逻辑")
    @pytest.mark.full
    def test_caseid_1980691(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPositionMax',{"doors": [{"id": 1, "pos": 10}]})
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPositionMax',{"doors": [{"id": 1, "pos": 50}]})
        sleep(0.1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPositionMax',{"doors": [{"id": 1, "pos": 50}]})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("DoorPassPercSetFromHmi", [10, 50, 50, 50, 101])
                
    @allure.title("设置电动门最大开度百分比_遍历四门_总线信号校验")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1980690(self):
        dic = {0 : "Drvr", 1 : "Pass", 2 : "LeRe", 3 : "RiRe"}
        for key_id, door in dic.items():  
            for pos1 in [0, 100, 90, 55, 48, 78, 10]:
                logger.info(f"当前门.{key_id},当前pos.{pos1},当前pdu.{door}")
                self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPositionMax', {"doors": [{"id": key_id, "pos": pos1}]})
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, f'Door{door}PercSetFromHmi', pos1, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr05, f'Door{door}PercSetFromHmi', 101, timeout=0.5)
                sleep(1)
                
    @allure.title("获取电动门最大开度百分比_遍历四门")
    @pytest.mark.full
    def test_caseid_1980692(self):
        dic = {"Drvr":0, "Pass":1, "LeRe":2, "RiRe":3}
        for pos1 in [0, 125, 127, 100, 50, 88]:
            for door, key_id in dic.items():
                logger.info(f"当前door.{door},当前keyid.{key_id},当前pos.{pos1}")
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0]}podBodyFr01"), f"TopPerc{door}HmiFeedBack", pos1)
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetPositionMax", {"doors": key_id}, 
                                                                {"out": [{"id": key_id, "pos": pos1}]}) 
                
    @allure.title("获取电动门最大开度百分比_全部车门_默认值")
    @pytest.mark.full
    def test_caseid_1980693(self):  
        for door in ["Drvr", "Pass", "LeRe", "RiRe"]:
            self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0]}podBodyFr01"), f"TopPerc{door}HmiFeedBack", 10)
        sleep(0.5)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetPositionMax", {"doors":[4]}, 
                                                                {"out": [{"id": 0, "pos": 10}, 
                                                                         {"id": 1, "pos": 10}, 
                                                                         {"id": 2, "pos": 10}, 
                                                                         {"id": 3, "pos": 10}]}, timeout=0.3)
        sleep(1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetPositionMax", {"doors":[4]}, 
                                                                {"out": [{"id": 0, "pos": 100}, 
                                                                         {"id": 1, "pos": 100}, 
                                                                         {"id": 2, "pos": 100}, 
                                                                         {"id": 3, "pos": 100}]}, timeout=0.3)
                           

    @allure.title("设置电动门操作力度_遍历全部力度_总线信号较验")
    @pytest.mark.full
    def test_caseid_1980695(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetStrengthLevel', {"doors": [{"id": 4, "level": 1}]})  
        #0=low; 1=medium; 2:high
        for streng in range(3):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetStrengthLevel', {"doors": [{"id": 4, "level": streng}]})
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPwrDoorFeel', streng, timeout=0.5)
        
    @allure.title("设置电动门操作力度_校验服务启动无下行PDU")#beta2
    @pytest.mark.full
    def test_caseid_1985575(self):  
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetStrengthLevel', {"doors": [{"id": 4, "level": 1}]})  
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SetPwrDoorFeel", [])
  
    @allure.title("通知/获取电动门操作力度_遍历全部力度")
    @pytest.mark.sanity
    def test_caseid_1980698(self):  
        for Strength in range(3):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetStrengthLevel', {"doors": [{"id": 4, "level": Strength}]})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "StrengthLevel", {"level": {"id": 4, "level": Strength}})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetStrengthLevel", {"doors": [4]},
                                                {"out":[{"id": 4, "level": Strength}]})
            self.partner.empty_all(0.1)
        
    @allure.title("通知/获取电动门操作力度_校验无记忆值重启默认值")#beta2
    @pytest.mark.full
    def test_caseid_1985504(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetStrengthLevel', {"doors": [{"id": 4, "level": 1}]})
        self.del_s2s_db()
        self.partner.empty_all(1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "StrengthLevel", {"level": {"id": 4, "level": 0}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetStrengthLevel", {"doors": [4]},
                                                {"out": [{"id": 4,"level": 0}]})
             
    @allure.title("通知/获取电动门操作力度_校验bgm重启后记忆值上报")#beta2
    @pytest.mark.full
    def test_caseid_1985503(self):
        for i in range(3):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetStrengthLevel', {"doors": [{"id": 4, "level": i}]}, timeout=0.2)
            self.partner.empty_all(1)
            self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "StrengthLevel", {"level": {"id": 4, "level": i}})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetStrengthLevel", {"doors": [4]},
                                                    {"out": [{"id": 4,"level": i}]}, timeout=0.2)
    
    @allure.title("设置开门速度_遍历全部速度_总线信号校验")
    @pytest.mark.smoke
    def test_caseid_1980700(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetOpenSpeed',{"doors": [{"id": 4, "level": 1}]})  
        for streng in range(3):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetOpenSpeed',{"doors": [{"id": 4, "level": streng}]})
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPwrDoorOpenSpd', streng, timeout=0.5)
        
    @allure.title("设置开门速度_校验服务启动无下行PDU")#beta
    @pytest.mark.full
    def test_caseid_1985576(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT,"SetOpenSpeed", {"doors": [{"id": 4, "level":1}]})
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SetPwrDoorOpenSpd", [])
            
    @allure.title("通知/获取开门速度_遍历全部速度")
    @pytest.mark.smoke
    def test_caseid_1980702(self):
        for Speed in range(3):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetOpenSpeed', {"doors": [{"id": 4, "level": Speed}]})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "OpenSpeed", {"info": {"id": 4, "level": Speed}})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenSpeed", {"doors": [4]},
                                                {"out":[{"id": 4, "level": Speed}]})
        
    @allure.title("设置关门速度_遍历全部速度_校验总线信号")
    @pytest.mark.full
    def test_caseid_1980707(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetCloseSpeed', {"doors": [{"id": 4, "level": 1}]})  
        #0=low; 1=medium; 2:high
        for streng in range(3):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetCloseSpeed', {"doors": [{"id": 4, "level": streng}]})
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPwrDoorClsSpd', streng, timeout=0.5)
        
    @allure.title("设置关门速度_校验服务启动无下行PDU")#beta2
    @pytest.mark.full
    def test_caseid_1985577(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SetPwrDoorClsSpd", [])
    
    @allure.title("通知/获取关门速度_遍历全部速度")
    @pytest.mark.sanity
    def test_caseid_1980705(self):
        for Speed in range(3):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetCloseSpeed', {"doors": [{"id": 4, "level": Speed}]})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "CloseSpeed", {"info": {"id": 4, "level": Speed}})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetCloseSpeed", {"doors": [4]},
                                                {"out":[{"id": 4, "level": Speed}]})
        
    @allure.title("通知/获取关门速度_无记忆值重启校验默认值")#beta2
    @pytest.mark.full
    def test_caseid_1985510(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetCloseSpeed', {"doors": [{"id": 4, "level": 2}]})
        self.del_s2s_db()
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_coming_event(DOOR_SERVICE_CLIENT, "CloseSpeed", {"info": {"id": 4, "level": 0}})  
        
    @allure.title("通知/获取关门速度_校验bgm重启记忆值上报")#beta2
    @pytest.mark.full
    def test_caseid_1985509(self):
        for i in range(3):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetCloseSpeed', {"doors": [{"id": 4, "level": i}]})
            self.partner.empty_all()
            self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "CloseSpeed", {"info": {"id": 4, "level": i}})  
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetCloseSpeed", {"doors": [4]}, {"out": [{"id": 4, "level": i}]}, timeout=0.2)
            self.partner.empty_all(0.5)
            
    @allure.title("通知/获取开门速度_无记忆值重启校验默认值")#beta2
    @pytest.mark.full
    def test_caseid_1985507(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetOpenSpeed', {"doors": [{"id": 4, "level": 2}]})
        sleep(1)
        self.del_s2s_db()
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_coming_event(DOOR_SERVICE_CLIENT, "CloseSpeed", {"info": {"id": 4, "level": 0}})  
        
    @allure.title("通知/获取开门速度_校验bgm重启后记忆值上报")#beta2
    @pytest.mark.full
    def test_caseid_1985506(self):
        for i in range(1):
            logger.info(f"当前循环.{i}")
            self.partner.send_method_request(DOOR_SERVICE_CLIENT,'SetOpenSpeed', {"doors": [{"id": 4, "level": i}]})
            self.partner.empty_all()
            self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "OpenSpeed", {"info": {"id": 4, "level": i}})  
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenSpeed", {"doors": [4]}, {"out": [{"id": 4, "level": i}]}, timeout=0.2)
            self.partner.empty_all(0.5)
            
    @allure.title("设置电动门风抖消除开关状态_总线信号校验")
    @pytest.mark.full
    def test_caseid_1981289(self):
        dic = {0 : False, 1 : True}
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetWindElimination", {"doors": [{"id": 4, "on": True}]})          
        for wind, value in dic.items():
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetWindElimination", {"doors": [{"id": 4, "on": value}]})
            self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPwrDoorWindCatch', wind, timeout=0.5)
                  
    @allure.title("设置电动门风抖消除开关状态_校验服务启动无下行PDU")#beta2
    @pytest.mark.full
    def test_caseid_1985580(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetWindElimination", {"doors": [{"id": 4, "on": True}]})      
        sleep(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(5)    
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SetPwrDoorWindCatch", [])
    
    @allure.title("通知/获取电动门风抖消除开关状态_遍历关闭开启")
    @pytest.mark.sanity
    def test_caseid_1980711(self):  
        for wind in [ False, True]:
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetWindElimination", {"doors": [{"id": 4, "on": wind}]})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "WindElimination", {"info": {"id": 4, "on": wind}})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetWindElimination", {"doors": [4]},
                                                                                             {"out": [{"id": 4, "on": wind}]})
                   
    @allure.title("通知/获取电动门风抖消除开关状态_上下电校验记忆值&校验首次下线")
    @pytest.mark.full
    def test_caseid_1980712(self):  
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetWindElimination", {"doors": [{"id": 4, "on": True}]})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "WindElimination", {"info": {"id": 4, "on": True}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetWindElimination", {"doors": [4]},
                                                                                             {"out": [{"id": 4, "on": True}]}, timeout=0.2)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetWindElimination", {"doors": [4]},
                                                                                             {"out": [{"id": 4, "on": True}]}, timeout=2)
        self.partner.empty_all(0.5)
        self.ipdu.resume_all_bus_send()
        sleep(10)
        self.del_s2s_db()
        self.kill_bgm_process()  
        self.partner.wait_for_service_reconnect(DOOR_SERVICE_CLIENT)
        sleep(2)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetWindElimination", {"doors": [4]},
                                                                                                {"out": [{"id": 4, "on": False}]}, timeout=2)
        
    @allure.title("设置电动门开启模式_遍历四门开启模式开关_总线信号校验")
    @pytest.mark.smoke
    def test_caseid_1980714(self):    
        dic = {0 : "Drvr", 1 : "Pass", 2 : "LeRe", 3 : "RiRe"}
        for key, value in dic.items():
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id": key, "mode": 1}]})
        for key, value in dic.items():
            for modevalue in range(2):
                logger.info(f"当前门.{key},当前值.{value}")
                self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id": key, "mode": modevalue}]})
                self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, f'Set{value}PwrDoorAutOperMode', modevalue)
        sleep(1)
               
    @allure.title("设置电动门开启模式_全部门开启模式开&关")
    @pytest.mark.sanity
    def test_caseid_1980718(self): 
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id":4 , "mode": 1}]})
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetDrvrPwrDoorAutOperMode', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPassPwrDoorAutOperMode', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetLeRePwrDoorAutOperMode', 1, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetRiRePwrDoorAutOperMode', 1, timeout=0.5)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id":4 , "mode": 0}]})
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetDrvrPwrDoorAutOperMode', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetPassPwrDoorAutOperMode', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetLeRePwrDoorAutOperMode', 0, timeout=0.5)
        self.ipdu.check(self.ipdu.bodycan.BgmBodyFr10, 'SetRiRePwrDoorAutOperMode', 0, timeout=0.5)
            
    @allure.title("设置电动门开启模式_校验服务启动无下行PDU&on")#beat2
    @pytest.mark.full
    def test_caseid_1985574(self): 
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id":4 , "mode": 1}]})
        sleep(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for sig in ["SetDrvrPwrDoorAutOperMode", "SetPassPwrDoorAutOperMode", "SetLeRePwrDoorAutOperMode", "SetRiRePwrDoorAutOperMode"]:
            self.bgm_eth_inter.ck_signal_values(sig, [])
        
    @allure.title("设置电动门开启模式_校验服务启动无下行PDU&off")#beat2
    @pytest.mark.full
    def test_caseid_1985573(self): 
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id":4 , "mode": 0}]})
        sleep(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        for sig in ["SetDrvrPwrDoorAutOperMode", "SetPassPwrDoorAutOperMode", "SetLeRePwrDoorAutOperMode", "SetRiRePwrDoorAutOperMode"]:
            self.bgm_eth_inter.ck_signal_values(sig, [])

              
       
    @allure.title("通知/获取电动门开启模式_遍历四门电动门开启/关闭模式")
    @pytest.mark.smoke
    def test_caseid_1980815(self): 
        for doorid in range(4):   
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id":doorid , "mode": 1}]})
            self.partner.empty_all(1)
        for doorid in range(4):
            for value in range(2):         
                self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id":doorid , "mode": value}]})
                self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorMode", {"info": {"id": doorid, "mode": value}})
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorMode", {"doors": [doorid]},
                                                                                        {"out": [{"id": doorid, "mode": value}]})
   
    @allure.title("通知/获取电动门开启模式_校验全部门下电默认值")
    @pytest.mark.full
    def test_caseid_1980816(self):     
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id":4 , "mode": 1}]}) 
        self.partner.empty_all(1)     
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id":4 , "mode": 0}]})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorMode", {"info": {"id": 0, "mode": 0}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorMode", {"info": {"id": 1, "mode": 0}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorMode", {"info": {"id": 2, "mode": 0}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorMode", {"info": {"id": 3, "mode": 0}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorMode", {"doors": [4]},
                                                                                {"out": [{"id": 0, "mode": 0}, 
                                                                                         {"id": 1, "mode": 0}, 
                                                                                         {"id": 2, "mode": 0}, 
                                                                                         {"id": 3, "mode": 0},]})  
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorMode",{"doors": [4]},
                                                                                     {"out": [{"id": 0, "mode": 0},
                                                                                              {"id": 1, "mode": 0},
                                                                                              {"id": 2, "mode": 0},                  
                                                                                              {"id": 3, "mode": 0},]})

    @allure.title("通知/获取电动门开启模式_首次下线校验记忆值")
    @pytest.mark.full
    def test_caseid_1984912(self):      
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorMode", {"doors": [{"id":4 , "mode": 0}]})
        sleep(3)
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorMode", {"info": {"mode": 0}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorMode", {"doors": [4]},
                                                                                {"out": [{"id": 0, "mode": 0}, 
                                                                                         {"id": 1, "mode": 0}, 
                                                                                         {"id": 2, "mode": 0}, 
                                                                                         {"id": 3, "mode": 0}]}, timeout=0.2) 
        sleep(3) 
        self.del_s2s_db()
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(3)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorMode", {"info": {"mode": 1}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorMode",{"doors": [4]},
                                                                                     {"out": [{"id": 0, "mode": 1},
                                                                                              {"id": 1, "mode": 1},
                                                                                              {"id": 2, "mode": 1},                  
                                                                                              {"id": 3, "mode": 1},]})
   
        
    @allure.title("关闭/开启/停止_遍历四门校验下行PDU")
    @pytest.mark.sanity
    def test_caseid_1981293(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        for value in ["Open", "Close", "Stop"]:
            for door_id in range(4):  
                self.partner.send_method_request(DOOR_SERVICE_CLIENT, value, {"doors": [door_id]}) 
                sleep(0.5)  
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_signal_trigger("DoorDrvrOpenHmiReqDoorOpenerReq1", idle_value = 0, trigger_values=[1, 2, 3])
        self.bgm_eth_inter.ck_period_signal_trigger("DoorPassOpenHmiReqDoorOpenerReq1", idle_value = 0, trigger_values=[1, 2, 3])
        self.bgm_eth_inter.ck_period_signal_trigger("DoorLeReOpenHmiReqDoorOpenerReq1", idle_value = 0, trigger_values=[1, 2, 3])
        self.bgm_eth_inter.ck_period_signal_trigger("DoorRiReOpenHmiReqDoorOpenerReq1", idle_value = 0, trigger_values=[1, 2, 3])
           
    @allure.title("开启_服务启动校验初始值")
    @pytest.mark.full
    def test_caseid_1981891(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Open", {"doors": [4]}) 
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(10)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("DoorDrvrOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_ordered_array("DoorPassOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_ordered_array("DoorLeReOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_ordered_array("DoorRiReOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_period_time("DoorDrvrOpenHmiReqDoorOpenerReq1", 0.2, deviation=0.4)
               
    @allure.title("关闭_服务启动校验初始值")
    @pytest.mark.full
    def test_caseid_1981890(self):
        # self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Close", {"doors": [4]}) 
        self.kill_bgm_process()
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(10)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("DoorDrvrOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_ordered_array("DoorPassOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_ordered_array("DoorLeReOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_ordered_array("DoorRiReOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_period_time("DoorDrvrOpenHmiReqDoorOpenerReq1", 0.2, deviation=0.4)
        
    @allure.title("停止_服务启动校验初始值")
    @pytest.mark.full
    def test_caseid_1981892(self): 
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Stop", {"doors": [4]}) 
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(10)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_ordered_array("DoorDrvrOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_ordered_array("DoorPassOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_ordered_array("DoorLeReOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_ordered_array("DoorRiReOpenHmiReqDoorOpenerReq1", [0])
        self.bgm_eth_inter.ck_period_time("DoorDrvrOpenHmiReqDoorOpenerReq1", 0.2, deviation=0.4)
    
    @allure.title("设置/取消P档自动解锁_校验下行PDU")
    @pytest.mark.sanity
    def test_caseid_1981294(self):
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(1)
        for value in ["CancelAutoUnlockTrigger", "SetAutoUnlockTrigger"]:
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, value,
                                            {"trigger": 0})
            sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SetAutLockInGearP", [0, 1])
       
    @allure.title("设置/取消P档自动解锁_上下线后无默认值发送") #beta2
    @pytest.mark.full
    def test_caseid_1985581(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "CancelAutoUnlockTrigger",{"trigger": 0})
        sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump()  
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SetAutLockInGearP", [])
        self.partner.empty_all(0.5)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetAutoUnlockTrigger",{"trigger": 0})
        sleep(1)
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SetAutLockInGearP", [])     

            
    @allure.title("设置P档自动解锁_校验中控锁锁状态")
    @pytest.mark.full
    def test_caseid_1981893(self):
        self.dk.set_cenlock_sts(3)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 3)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetAutoUnlockTrigger",
                                            {"trigger": 0})
        self.io.driver_seat_present()
        self.sd_tester.change_usage_mode(2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 0)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, 'LockgCenStsLockSt', 1)
        sleep(1)
        
    @allure.title("通知/获取P档自动解锁设置反馈状态_无记忆值重启校验默认值")#beta2
    @pytest.mark.full
    def test_caseid_1985526(self):   
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetAutoUnlockTrigger", {"trigger": 0})
        sleep(5)
        self.del_s2s_db()
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "AutoUnlockTrigger")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoUnlockTrigger", {}, {"out":[]})
        
    @allure.title("通知/获取P档自动解锁设置反馈状态_重启后校验设置P档记忆值")#beta2
    @pytest.mark.full
    def test_caseid_1985525(self):   
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetAutoUnlockTrigger", {"trigger": 0})
        sleep(5)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "AutoUnlockTrigger",{"triggers":[0]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoUnlockTrigger", {}, {"out":[0]})
        
    @allure.title("通知/获取P档自动解锁设置反馈状态_重启后校验取消设置P档记忆值")#beta2
    @pytest.mark.full
    def test_caseid_1985523(self):   
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "CancelAutoUnlockTrigger", {"trigger": 0})
        self.partner.empty_all(1)
        sleep(5)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "AutoUnlockTrigger",{"triggers": []})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoUnlockTrigger", {}, {"out":[]})
 
    @allure.title("通知/获取P档自动解锁设置反馈状态_取消设置P档解锁")#beta2
    @pytest.mark.sanity
    def test_caseid_1985522(self):   
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "CancelAutoUnlockTrigger", {"trigger": 0})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "AutoUnlockTrigger", {"triggers" : []})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoUnlockTrigger", {}, {"out":[]})
        
    @allure.title("通知/获取P档自动解锁设置反馈状态_设置P档解锁")#beta2
    @pytest.mark.full
    def test_caseid_1985521(self):   
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetAutoUnlockTrigger", {"trigger": 0})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "AutoUnlockTrigger",{"triggers":[0]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetAutoUnlockTrigger", {}, {"out":[0]})
            
    @allure.title("儿童锁上锁/解锁_总线信号校验")
    @pytest.mark.sanity
    def test_caseid_1981295(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "LockChildLock", {"doors": 2})
        self.partner.empty_all(1) 
        dic = { 1: "UnLockChildLock", 2: "LockChildLock"}
        dic1 = {2: "ChdLockReLeCtrlHmiReq", 3: "ChdLockReRiCtrlHmiReq"}
        for door_id, pdu_id in dic1.items():
            for lockkey, lockvalue in dic.items():
                self.partner.send_method_request(DOOR_SERVICE_CLIENT, lockvalue, {"doors": [door_id]})  
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr09, pdu_id, lockkey, timeout=0.5)
                self.ipdu.check(self.ipdu.bodycan.CemBodyFr09, pdu_id, 0, timeout=0.5)

    @allure.title("儿童锁上锁/解锁_下行PDU校验报文不可打断")#2.0
    @pytest.mark.full
    def test_caseid_1985255(self):
        self.bgm_eth_inter.start_bgm_tcpdump()  
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "UnLockChildLock", {"doors": [2]})
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "UnLockChildLock", {"doors": [2]})
        sleep(0.1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "LockChildLock", {"doors": [4]})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("ChdLockReLeCtrlHmiReq", [1, 1, 1, 0])
        self.bgm_eth_inter.ck_signal_values("ChdLockReRiCtrlHmiReq", [2, 2, 2, 0])
        self.bgm_eth_inter.ck_period_time("ChdLockReLeCtrlHmiReq", 0.05, deviation=0.4)
        self.bgm_eth_inter.start_bgm_tcpdump()  
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "LockChildLock", {"doors": [2]})
        sleep(0.1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "UnLockChildLock", {"doors": [4]})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("ChdLockReLeCtrlHmiReq", [2, 2, 2, 0])
        self.bgm_eth_inter.ck_signal_values("ChdLockReRiCtrlHmiReq", [1, 1, 1, 0])
        self.bgm_eth_inter.ck_period_time("ChdLockReRiCtrlHmiReq", 0.05, deviation=0.4)
        
    @allure.title("儿童锁上锁_下行PDU校验2.0")#2.0
    @pytest.mark.sanity
    def test_caseid_1985252(self):
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "LockChildLock", {"doors": [2]})
        sleep(0.3)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "LockChildLock", {"doors": [3]})
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "LockChildLock", {"doors": [3]})
        sleep(0.3)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "LockChildLock", {"doors": [4]})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("ChdLockReLeCtrlHmiReq", [2, 2, 2, 0, 2, 2, 2, 0])
        self.bgm_eth_inter.ck_signal_values("ChdLockReRiCtrlHmiReq", [2, 2, 2, 0, 2, 2, 2, 0])
        
    @allure.title("儿童锁上锁_校验服务下线上线后不发送报文")#2.0
    @pytest.mark.full
    def test_caseid_1985257(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "LockChildLock", {"doors": [4]})
        sleep(2)
        self.bgm_eth_inter.start_bgm_tcpdump()  
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("ChdLockReLeCtrlHmiReq", [])
        self.bgm_eth_inter.ck_signal_values("ChdLockReRiCtrlHmiReq", [])
        
    @allure.title("儿童锁解锁_下行PDU校验2.0")#2.0
    @pytest.mark.full
    def test_caseid_1985251(self):
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "UnLockChildLock", {"doors": [2]})
        sleep(0.3)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "UnLockChildLock", {"doors": [3]})
        sleep(0.3)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "UnLockChildLock", {"doors": [4]})
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("ChdLockReLeCtrlHmiReq", [1, 1, 1, 0, 1, 1, 1, 0])
        self.bgm_eth_inter.ck_signal_values("ChdLockReRiCtrlHmiReq", [1, 1, 1, 0, 1, 1, 1, 0])
        
    @allure.title("通知右后门儿童锁状态_校验bgm重启event上报")#v1.3
    @pytest.mark.full
    def test_caseid_1984514(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'ChdLockRightStsToHmi', 1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightChildLock", {"sts": 1})
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'ChdLockRightStsToHmi', 2)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightChildLock", {"sts": 2})
        
    @allure.title("通知左后门儿童锁状态_校验bgm重启event上报")#v1.3
    @pytest.mark.full
    def test_caseid_1984521(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftStsToHmi', 1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftChildLock", {"sts": 1})
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftStsToHmi', 2)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftChildLock", {"sts": 2})

    @allure.title("设置门雷达工作模式_总线信号校验")
    @pytest.mark.full
    def test_caseid_1981300(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorRadarWorkMode",
                                                          {"doors": 4, "mode": 2})      
        for modes in range(8):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorRadarWorkMode",
                                                          {"doors": 4, "mode": modes})
            self.ipdu.check(self.ipdu.connectivitycanfd.BgmConnectivityFr08, 'SetDRMMode', modes, timeout=0.5)
            
    @allure.title("设置门雷达工作模式_上下线后不主动发送报文")
    @pytest.mark.full
    def test_caseid_1984968(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetDoorRadarWorkMode",
                                                          {"doors": 4, "mode": 2})      
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_s2s_and_reconnect_service(DOOR_SERVICE_CLIENT)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values("SetDRMMode", [])
                       
    @allure.title("通知/获取门雷达工作模式_遍历四门信号0~8")
    @pytest.mark.sanity
    def test_caseid_1981307(self):
        dic = {0: "FL", 1: "FR", 2: "RL", 3: "RR"}
        last = ""
        for ids, sig in dic.items():
            self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{sig.lower()}ConnectivityFr06"), f"{sig}DRMWorkModeFB", 2)
        self.partner.empty_all(1)
        for ids, sig in dic.items():
            for Mode in range(9):
                logger.info(f"当前门.{ids},当前信号.{Mode}")
                self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{sig.lower()}ConnectivityFr06"), f"{sig}DRMWorkModeFB", Mode)
                if Mode in [0, 1, 2]:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorRadarWorkMode", {"info":
                                                                                    {"id": ids, "mode": Mode}})
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarWorkMode", {"doors": [ids]},
                                                {"out": [{"id": ids, "mode": Mode}]})
                    last = Mode
                else:
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarWorkMode", {"doors": [ids]},
                                                {"out": [{"id": ids, "mode": last}]})                    
  
    @allure.title("通知/获取门雷达工作模式_全部门上下电校验默认值")
    @pytest.mark.full
    def test_caseid_1981309(self):
        for sig in ["FL", "FR", "RL", "RR"]:
            self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{sig.lower()}ConnectivityFr06"), f"{sig}DRMWorkModeFB", 2)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorRadarWorkMode", {"info":
                                                                {"id": 0, "mode": 2}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarWorkMode", {"doors": [0, 1, 2, 3]},
                                                                {"out": [{"id": 0, "mode": 2}, 
                                                                        {"id": 1, "mode": 2}, 
                                                                        {"id": 2, "mode": 2}, 
                                                                        {"id": 3, "mode": 2}]})
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarWorkMode", {"doors": [0, 1, 2, 3]},
                                                                {"out": [{"id": 0, "mode": 0}, 
                                                                        {"id": 1, "mode": 0}, 
                                                                        {"id": 2, "mode": 0}, 
                                                                        {"id": 3, "mode": 0},]})
        self.ipdu.resume_all_bus_send()
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorRadarWorkMode", {"info":
                                                                {"id": 0, "mode": 2}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarWorkMode", {"doors": [0, 1, 2, 3]},
                                                                {"out": [{"id": 0, "mode": 2}, 
                                                                        {"id": 1, "mode": 2}, 
                                                                        {"id": 2, "mode": 2}, 
                                                                        {"id": 3, "mode": 2}]})
        
    @allure.title("获取门雷达工作模式 _all") #1.4新增
    @pytest.mark.sanity
    def test_caseid_1984295(self):
        for sig in ["FL", "FR", "RL", "RR"]:
            self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{sig.lower()}ConnectivityFr06"), f"{sig}DRMWorkModeFB", 2)
        self.partner.empty_all(1)
        for Mode in range(3):
            for sig in ["FL", "FR", "RL", "RR"]:
                logger.info(f"当前信号.{Mode}")
                self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{sig.lower()}ConnectivityFr06"), f"{sig}DRMWorkModeFB", Mode)
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarWorkMode", {"doors": [4]},
                                                {"out": [{"id": 0, "mode": Mode},
                                                         {"id": 0, "mode": Mode},
                                                         {"id": 0, "mode": Mode}, 
                                                         {"id": 3, "mode": Mode}]})       
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)             
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarWorkMode", {"doors": [4]},
                                                {"out": [{"id": 0, "mode": 0},
                                                         {"id": 0, "mode": 0},
                                                         {"id": 0, "mode": 0}, 
                                                         {"id": 3, "mode": 0}]})
          
    @allure.title("通知/获取门雷达状态_遍历四门信号0~8")
    @pytest.mark.sanity
    def test_caseid_1981310(self):
        last = ""
        dic ={"FL": [0, "Drvr"], "FR": [1, "Pass"], "RL": [2, "LeRe"], "RR": [3, "RiRe"]}    
        for key, door in dic.items():
            self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{key.lower()}ConnectivityFr07"),f'Radar{door[1]}Sts', 2)
        self.partner.empty_all(1)
        for key, door in dic.items():
            for sig in range(9):
                logger.info(f"当前门.{key},当前信号.{sig}")
                self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{key.lower()}ConnectivityFr07"),f'Radar{door[1]}Sts', sig)
                if sig in [0, 1, 2, 3, 4, 5]:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorRadarSts",
                                            {"radar": {"id": door[0], "radar": sig}})
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarSts", {"doors": [door[0]]},
                                                    {"out": [{"id": door[0], "radar": sig}]})
                    last = sig    
                else:
    
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarSts", {"doors": [door[0]]},
                                                    {"out": [{"id": door[0], "radar": last}]})
                    
    @allure.title("获取门雷达状态 _all") #1.4新增
    @pytest.mark.sanity
    def test_caseid_1984296(self):
        dic ={"FL": "Drvr", "FR": "Pass", "RL": "LeRe", "RR": "RiRe"}    
        for key, door in dic.items():
            self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{key.lower()}ConnectivityFr07"),f'Radar{door}Sts', 2)
        self.partner.empty_all(1)
        for sig in range(6):
            for key, door in dic.items():
                logger.info(f"当前门.{key},当前信号.{sig}")
                self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{key.lower()}ConnectivityFr07"),f'Radar{door}Sts', sig)
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarSts", {"doors": [4]},
                                                    {"out": [{"id": 0, "radar": sig}, 
                                                             {"id": 1, "radar": sig}, 
                                                             {"id": 2, "radar": sig}, 
                                                             {"id": 3, "radar": sig}]})
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT,pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarSts", {"doors": [4]},
                                                    {"out": [{"id": 0, "radar": 0}, 
                                                             {"id": 1, "radar": 0}, 
                                                             {"id": 2, "radar": 0}, 
                                                             {"id": 3, "radar": 0}]}, timeout=0.15)
                                
    @allure.title("通知/获取门雷达状态_全部门上下电校验默认值")
    @pytest.mark.full
    def test_caseid_1981311(self):
        dic ={"FL": "Drvr", "FR": "Pass", "RL": "LeRe", "RR": "RiRe"}    
        for key, door in dic.items():
            self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{key.lower()}ConnectivityFr07"),f'Radar{door}Sts', 2)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorRadarSts",
                                            {"radar": {"id": 0, "radar": 2}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarSts", {"doors": [0, 1, 2, 3]},
                                            {"out": [{"id": 0, "radar": 2},
                                            {"id": 1, "radar": 2},
                                            {"id": 2, "radar": 2},
                                            {"id": 3, "radar": 2}]})
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)   
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarSts", {"doors": [0, 1, 2, 3]},
                                                    {"out": [{"id":0, "radar": 0}, 
                                                             {"id":1, "radar": 0}, 
                                                             {"id":2, "radar": 0}, 
                                                             {"id":3, "radar": 0},]})
        self.ipdu.resume_all_bus_send()
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorRadarSts",
                                            {"radar": {"id": 0, "radar": 2}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorRadarSts", {"doors": [0, 1, 2, 3]},
                                                    {"out": [{"id":0, "radar": 2}, 
                                                             {"id":1, "radar": 2}, 
                                                             {"id":2, "radar": 2}, 
                                                             {"id":3, "radar": 2},]})
        
    @allure.title("通知/获取门按键开关状态_遍历四门内按键开关状态")
    @pytest.mark.sanity
    def test_caseid_1981314(self):
        self.dk.press_door_inswitch(3, timeout=1)
        for id in range(4):
            self.dk.press_door_inswitch(id+1, timeout=1)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"doors": id, "side": 0, "sts": 1})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": id, "side": 0},
                                                {"out": 1})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"doors": id, "side": 0, "sts": 2})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": id, "side": 0},
                                                {"out": 2})
            sleep(1)
            
    @allure.title("通知/获取门按键开关状态_遍历四门外按键开关状态_左前右前")
    @pytest.mark.full
    def test_caseid_1981320(self):
        for id in range(2):
            self.dk.press_door_outswitch(id+1, timeout=1)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"doors": id, "side": 1, "sts": 1})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"doors": id, "side": 1, "sts": 2})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": id, "side": 1},
                                                {"out": 2})
            sleep(5)

    @allure.title("通知/获取门按键开关状态_下电校验默认值")
    @pytest.mark.full
    def test_caseid_1981318(self):      
        self.dk.press_door_inswitch(1, timeout=1)    
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"doors": 0, "side": 0, "sts": 1})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 0, "side": 0},
                                                {"out": 1}) 
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"doors": 0, "side": 0, "sts": 2})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 0, "side": 0},
                                                {"out": 2})
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False) 
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 0, "side": 0},
                                                {"out": 0})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"doors": 0, "side": 0, "sts": 2})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 0, "side": 0},
                                                {"out": 2})
        sleep(10)

    @allure.title("通知门按键开关状态_校验bgm重启后event上报")
    @pytest.mark.full
    def test_caseid_1984522(self):    
        self.dk.press_door_outswitch(1, timeout=1)    
        self.dk.press_door_outswitch(2, timeout=1)
        self.dk.press_door_outswitch(3, timeout=1)
        self.dk.press_door_outswitch(4, timeout=1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"side": 1, "sts": 2})
        
    @allure.title("设置车门按键指示灯状态_下行PDU校验")
    @pytest.mark.full
    def test_caseid_1981322(self): 
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetOutDoorSwitchLightMode", {"doors": 4, "mode": 2})  
        for value in range(3):
            self.bgm_eth_inter.start_bgm_tcpdump()
            sleep(2)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetOutDoorSwitchLightMode", {"doors": 4, "mode": value})
            sleep(5)
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            self.bgm_eth_inter.ck_signal_values('OuterDoorSwLightReq', [value])
           
    @allure.title("通知/获取门故障_遍历四门放玩激活&热保护&车辆横摆角度不正常&道路倾斜角度不正常&霍尔传感器故障产生恢复")
    @pytest.mark.sanity
    def test_caseid_1981328(self):
        self.set_door_fault_clear()
        self.partner.empty_all()
        doors = {"Drvr": 0, "Pass": 1, "LeRe": 2, "RiRe": 3}
        fault = {1: 16, 2: 11, 3 : 17, 4: 18, 5: 19}
        for door, id in doors.items():
            for sigfl, vaulefl in fault.items():
                for sig in [1, 0]:
                    logger.info(f"当前门.{door},当前fault.{vaulefl},当前sig.{sig}")
                    self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0:1]}podBodyFr01"), f'DtcInfDoor{door}Boolean{sigfl}', sig)
                    if sig == 1:
                        sleep(0.5)
                        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault",
                                                {"faults": [{"fault": vaulefl, "faultMsg": "", "door": id}]})
                        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": vaulefl, "faultMsg": "", "door": id}]})
                    else:
                        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault",
                                                {"faults": [{"fault": 0, "faultMsg": "", "door": 4}]})
                        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 0, "faultMsg": "", "door": 4}]})
        
    @allure.title("通知/获取门故障_四门放玩激活&热保护&车辆横摆角度不正常&道路倾斜角度不正常&霍尔传感器故障全部产生单个恢复")
    @pytest.mark.full
    def test_caseid_1981329(self):
        for door in ["Drvr", "Pass", "LeRe", "RiRe"]:
            for sigfl in[1, 2, 3, 4, 5]:
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0:1]}podBodyFr01"), f'DtcInfDoor{door}Boolean{sigfl}', 0)
        self.partner.empty_all(1)
        for door in ["Drvr", "Pass", "LeRe", "RiRe"]:
            for sigfl in[1, 2, 3, 4, 5]:
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0:1]}podBodyFr01"), f'DtcInfDoor{door}Boolean{sigfl}', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault",
                                                {"faults": [{"fault": 16, "faultMsg": "", "door": 0},{"fault": 16, "faultMsg": "", "door": 1},{"fault": 16, "faultMsg": "", "door": 2},{"fault": 16, "faultMsg": "", "door": 3},
                                                            {"fault": 11, "faultMsg": "", "door": 0},{"fault": 11, "faultMsg": "", "door": 1},{"fault": 11, "faultMsg": "", "door": 2},{"fault": 11, "faultMsg": "", "door": 3},
                                                            {"fault": 17, "faultMsg": "", "door": 0},{"fault": 17, "faultMsg": "", "door": 1},{"fault": 17, "faultMsg": "", "door": 2},{"fault": 17, "faultMsg": "", "door": 3},
                                                            {"fault": 18, "faultMsg": "", "door": 0},{"fault": 18, "faultMsg": "", "door": 1},{"fault": 18, "faultMsg": "", "door": 2},{"fault": 18, "faultMsg": "", "door": 3},
                                                            {"fault": 19, "faultMsg": "", "door": 0},{"fault": 19, "faultMsg": "", "door": 1},{"fault": 19, "faultMsg": "", "door": 2},{"fault": 19, "faultMsg": "", "door": 3}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 16, "faultMsg": "", "door": 0},{"fault": 16, "faultMsg": "", "door": 1},{"fault": 16, "faultMsg": "", "door": 2},{"fault": 16, "faultMsg": "", "door": 3},
                                                            {"fault": 11, "faultMsg": "", "door": 0},{"fault": 11, "faultMsg": "", "door": 1},{"fault": 11, "faultMsg": "", "door": 2},{"fault": 11, "faultMsg": "", "door": 3},
                                                            {"fault": 17, "faultMsg": "", "door": 0},{"fault": 17, "faultMsg": "", "door": 1},{"fault": 17, "faultMsg": "", "door": 2},{"fault": 17, "faultMsg": "", "door": 3},
                                                            {"fault": 18, "faultMsg": "", "door": 0},{"fault": 18, "faultMsg": "", "door": 1},{"fault": 18, "faultMsg": "", "door": 2},{"fault": 18, "faultMsg": "", "door": 3},
                                                            {"fault": 19, "faultMsg": "", "door": 0},{"fault": 19, "faultMsg": "", "door": 1},{"fault": 19, "faultMsg": "", "door": 2},{"fault": 19, "faultMsg": "", "door": 3}]})
        for door in ["Drvr", "Pass", "LeRe", "RiRe"]:
            for sigfl in[1, 2, 3, 4, 5]:
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0:1]}podBodyFr01"), f'DtcInfDoor{door}Boolean{sigfl}', 0)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault",
                                               {"faults": [{"fault": 0, "faultMsg": "", "door": 4}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 0, "faultMsg": "", "door": 4}]})
    
    @allure.title("通知门故障_校验bgm重启后事件上报")
    @pytest.mark.full
    def test_caseid_1984524(self):
        for sigfl in [1, 2, 3, 4, 5]:
            for door in ["Drvr", "Pass", "LeRe", "RiRe"]:
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0:1]}podBodyFr01"), f'DtcInfDoor{door}Boolean{sigfl}', 1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)      
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault",   {"faults": [{"fault": 16, "faultMsg": "", "door": 0},{"fault": 16, "faultMsg": "", "door": 1},{"fault": 16, "faultMsg": "", "door": 2},{"fault": 16, "faultMsg": "", "door": 3},
                                                                                  {"fault": 11, "faultMsg": "", "door": 0},{"fault": 11, "faultMsg": "", "door": 1},{"fault": 11, "faultMsg": "", "door": 2},{"fault": 11, "faultMsg": "", "door": 3},
                                                                                  {"fault": 17, "faultMsg": "", "door": 0},{"fault": 17, "faultMsg": "", "door": 1},{"fault": 17, "faultMsg": "", "door": 2},{"fault": 17, "faultMsg": "", "door": 3},
                                                                                  {"fault": 18, "faultMsg": "", "door": 0},{"fault": 18, "faultMsg": "", "door": 1},{"fault": 18, "faultMsg": "", "door": 2},{"fault": 18, "faultMsg": "", "door": 3},
                                                                                  {"fault": 19, "faultMsg": "", "door": 0},{"fault": 19, "faultMsg": "", "door": 1},{"fault": 19, "faultMsg": "", "door": 2},{"fault": 19, "faultMsg": "", "door": 3}]})
        self.partner.empty_all(1)
        for door in ["Drvr", "Pass", "LeRe", "RiRe"]:
            for sigfl in [1, 2, 3, 4, 5]:
                self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0:1]}podBodyFr01"), f'DtcInfDoor{door}Boolean{sigfl}', 0)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault",
                                               {"faults": [{"fault": 0, "faultMsg": "", "door": 4}]})
                    
    @allure.title("通知/获取门故障_左后门童锁错误")
    @pytest.mark.sanity
    def test_caseid_1981332(self):  
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault",
                                        {"faults": [{"fault": 1, "faultMsg": "", "door": 2}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 1, "faultMsg": "", "door": 2}]})
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 0)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 1, "faultMsg": "", "door": 2}]})
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 2)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault",
                                        {"faults": [{"fault": 0, "faultMsg": "", "door": 4}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 0, "faultMsg": "", "door": 4}]})
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 3)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 0, "faultMsg": "", "door": 4}]})
  
    @allure.title("通知/获取门故障_右后门童锁错误")
    @pytest.mark.full
    def test_caseid_1981333(self):  
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr02, 'ChdLockRightFailStsToHmi', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault",
                                        {"faults": [{"fault": 1, "faultMsg": "", "door": 3}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 1, "faultMsg": "", "door": 3}]})
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr02, 'ChdLockRightFailStsToHmi', 0)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 1, "faultMsg": "", "door": 3}]})
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr02, 'ChdLockRightFailStsToHmi', 2)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault",
                                        {"faults": [{"fault": 0, "faultMsg": "", "door": 4}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 0, "faultMsg": "", "door": 4}]})
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr02, 'ChdLockRightFailStsToHmi', 3)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 0, "faultMsg": "", "door": 4}]})
        
    @allure.title("通知/获取门故障_左右后门儿童锁上下电校验默认值")
    @pytest.mark.full
    def test_caseid_1981334(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr02, 'ChdLockRightFailStsToHmi', 1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 0, "faultMsg": "", "door": 4}]})
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault",
                                                {"faults": [{"fault": 1, "faultMsg": "", "door": 2},
                                                            {"fault": 1, "faultMsg": "", "door": 3}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {},
                                                            {"out": [{"fault": 1, "faultMsg": "", "door": 2},
                                                                     {"fault": 1, "faultMsg": "", "door": 3}]})
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 2)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr02, 'ChdLockRightFailStsToHmi', 2)
        
    @allure.title("通知/获取电动门附近的障碍物信息_四门遍历无障碍物/有障碍物/检测障碍物时发生故障/障碍物信息未定义或计算中")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1981352(self):
        doors = {"Drvr": ["fl", 0], "Pass": ["fr", 1], "LeRe": ["rl", 2], "RiRe": ["rr", 3]}
        for door, sig in doors.items():
            for sigvalue in [0, 252, 170, 171, 251, 255, 90, 180, 254, 10, 190, 200]:
                value = sigvalue/2 
                logger.info(f"当前门.{door},当前信号.{sigvalue}")         
                self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{sig[0]}ConnectivityFr07"), f"Door{door}PosnToObstAngle1", sigvalue)
                if sigvalue == 252:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorObstacleInfo", {"info": [{"id": sig[1],"obstacleAngleSts": 0, "angle": value}]})
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorObstacleInfo", {"doors": [sig[1]]}, 
                                                                    {"out": [{"id":sig[1], "obstacleAngleSts":0, "angle": value}]})
                elif sigvalue<=170:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorObstacleInfo", {"info": [{"id": sig[1], "obstacleAngleSts": 1, "angle": value}]})
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorObstacleInfo", {"doors": [sig[1]]}, 
                                                                    {"out":[{"id":sig[1], "obstacleAngleSts":1, "angle": value}]})
                elif 171<=sigvalue<=251:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorObstacleInfo", {"info": [{"id": sig[1], "obstacleAngleSts": 2, "angle": value}]})
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetDoorObstacleInfo", {"doors": [sig[1]]}, 
                                                                    {"out": [{"id": sig[1], "obstacleAngleSts": 2, "angle": value}]})
                else:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorObstacleInfo", {"info": [{"id": sig[1], "obstacleAngleSts": 3, "angle": value}]})
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetDoorObstacleInfo", {"doors": [sig[1]]}, 
                                                                    {"out": [{"id": sig[1], "obstacleAngleSts": 3, "angle": value}]})               
            sleep(0.1)
    
    @allure.title("通知/获取电动门附近的障碍物信息_遍历无障碍物/有障碍物/检测障碍物时发生故障/障碍物信息未定义或计算中_四门")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.full
    def test_caseid_1981355(self):
        doors = {"Drvr": "fl", "Pass": "fr", "LeRe": "rl", "RiRe": "rr"}
        for door, sig in doors.items():      
            self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{sig}ConnectivityFr07"), f"Door{door}PosnToObstAngle1", 50)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT,"DoorObstacleInfo", {"info": [{"id": 0, "obstacleAngleSts": 1, "angle": 25}, 
                                                                                 {"id": 1, "obstacleAngleSts": 1, "angle": 25}, 
                                                                                 {"id": 2, "obstacleAngleSts": 1, "angle": 25}, 
                                                                                 {"id": 3, "obstacleAngleSts": 1, "angle": 25}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorObstacleInfo", {"doors": [4]}, 
                                                                                  {"out": [{"id": 0,"obstacleAngleSts": 1,"angle": 25}, 
                                                                                  {"id": 1, "obstacleAngleSts": 1, "angle": 25}, 
                                                                                  {"id": 2, "obstacleAngleSts": 1, "angle": 25}, 
                                                                                  {"id": 3, "obstacleAngleSts": 1, "angle": 25}]})        
        for door, sig in doors.items():      
            self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{sig}ConnectivityFr07"), f"Door{door}PosnToObstAngle1", 252)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorObstacleInfo", {"info": [{"id": 0, "obstacleAngleSts":0, "angle": 126}, 
                                                                                 {"id": 1, "obstacleAngleSts":0, "angle": 126}, 
                                                                                 {"id": 2, "obstacleAngleSts":0, "angle": 126}, 
                                                                                 {"id": 3, "obstacleAngleSts":0, "angle": 126}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorObstacleInfo", {"doors": [4]}, 
                                                                                {"out": [{"id":0, "obstacleAngleSts": 0, "angle": 126}, 
                                                                                {"id": 1, "obstacleAngleSts": 0, "angle": 126}, 
                                                                                {"id": 2, "obstacleAngleSts": 0, "angle": 126}, 
                                                                                {"id": 3, "obstacleAngleSts": 0, "angle": 126}]})
        for door, sig in doors.items():      
            self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{sig}ConnectivityFr07"), f"Door{door}PosnToObstAngle1", 250)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorObstacleInfo", {"info": [{"id": 0, "obstacleAngleSts": 2, "angle": 125}, 
                                                                                {"id": 1, "obstacleAngleSts": 2, "angle": 125}, 
                                                                                {"id": 2, "obstacleAngleSts": 2, "angle": 125}, 
                                                                                {"id": 3, "obstacleAngleSts": 2, "angle": 125}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorObstacleInfo", {"doors": [4]}, 
                                                                                {"out": [{"id":0, "obstacleAngleSts": 2, "angle": 125}, 
                                                                                {"id": 1, "obstacleAngleSts": 2, "angle": 125}, 
                                                                                {"id": 2, "obstacleAngleSts": 2, "angle": 125}, 
                                                                                {"id": 3, "obstacleAngleSts": 2, "angle": 125}]})
        for door, sig in doors.items():      
            self.ipdu.set(eval(f"self.ipdu.connectivitycanfd.Drm{sig}ConnectivityFr07"), f"Door{door}PosnToObstAngle1", 255)                   
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT,"DoorObstacleInfo", {"info":[{"id": 0, "obstacleAngleSts": 3,"angle": 127.5}, 
                                                                                            {"id": 1, "obstacleAngleSts": 3,"angle": 127.5}, 
                                                                                            {"id": 2, "obstacleAngleSts": 3,"angle": 127.5}, 
                                                                                            {"id": 3, "obstacleAngleSts": 3,"angle": 127.5}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorObstacleInfo",{"doors": [4]}, 
                                                                                    {"out":[{"id": 0, "obstacleAngleSts": 3, "angle": 127.5}, 
                                                                                            {"id": 1, "obstacleAngleSts": 3, "angle": 127.5}, 
                                                                                            {"id": 2, "obstacleAngleSts": 3, "angle": 127.5}, 
                                                                                            {"id": 3, "obstacleAngleSts": 3, "angle": 127.5}]})
        sleep(1)
        
    @allure.title("通知/获取门按键开关状态_遍历四门外按键开关状态_左后右后")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1987172(self):
        for id in [2, 3]:
            self.dk.press_door_outswitch(id+1, timeout=1)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"doors": id, "side": 1, "sts": 1})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"doors": id, "side": 1, "sts": 2})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": id, "side": 1},
                                                {"out": 2})
            sleep(5)

    @allure.title("通知/获取电动门附近的障碍物信息_四门不同值停发总线校验默认值")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.full    
    def test_caseid_1981356(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmflConnectivityFr07, 'DoorDrvrPosnToObstAngle1', 252)
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmfrConnectivityFr07, 'DoorPassPosnToObstAngle1', 251)
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmrlConnectivityFr07, 'DoorLeRePosnToObstAngle1', 170)
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmrrConnectivityFr07, 'DoorRiRePosnToObstAngle1', 254)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorObstacleInfo", {"info":[{"id": 0, "obstacleAngleSts": 0, "angle": 126}, 
                                                                                  {"id": 1, "obstacleAngleSts": 2, "angle": 125.5}, 
                                                                                  {"id": 2, "obstacleAngleSts": 1, "angle": 85}, 
                                                                                  {"id": 3, "obstacleAngleSts": 3, "angle": 127}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorObstacleInfo", {"doors": [4]},
                                                                          {"out": [{"id": 0, "obstacleAngleSts": 0, "angle": 126}, 
                                                                                  {"id": 1, "obstacleAngleSts": 2, "angle": 125.5}, 
                                                                                  {"id": 2, "obstacleAngleSts": 1, "angle": 85}, 
                                                                                  {"id": 3, "obstacleAngleSts": 3, "angle": 127}]})
        sleep(1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False) 
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorObstacleInfo", {"doors": [4]},
                                                                         {"out": [{"id": 0, "obstacleAngleSts": 255, "angle": 255}, 
                                                                                  {"id": 1, "obstacleAngleSts": 255, "angle": 255}, 
                                                                                  {"id": 2, "obstacleAngleSts": 255, "angle": 255}, 
                                                                                  {"id": 3, "obstacleAngleSts": 255, "angle": 255}]})
        self.ipdu.resume_all_bus_send()
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorObstacleInfo", {"info": [{"id": 0, "obstacleAngleSts": 0, "angle": 126}, 
                                                                                  {"id": 1, "obstacleAngleSts": 2, "angle": 125.5}, 
                                                                                  {"id": 2, "obstacleAngleSts": 1, "angle": 85}, 
                                                                                  {"id": 3, "obstacleAngleSts": 3, "angle": 127}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorObstacleInfo", {"doors":[4]},
                                                                          {"out": [{"id": 0, "obstacleAngleSts": 0, "angle": 126}, 
                                                                                  {"id": 1, "obstacleAngleSts": 2, "angle": 125.5}, 
                                                                                  {"id": 2, "obstacleAngleSts": 1, "angle": 85}, 
                                                                                  {"id": 3, "obstacleAngleSts": 3, "angle": 127}]})
       
    @allure.title("通知电动门附近的障碍物信息_校验bgm重启event事件上报")
    @pytest.mark.full    
    def test_caseid_1984525(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmflConnectivityFr07, 'DoorDrvrPosnToObstAngle1', 252)
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmfrConnectivityFr07, 'DoorPassPosnToObstAngle1', 251)
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmrlConnectivityFr07, 'DoorLeRePosnToObstAngle1', 170)
        self.ipdu.set(self.ipdu.connectivitycanfd.DrmrrConnectivityFr07, 'DoorRiRePosnToObstAngle1', 254)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorObstacleInfo", {"info":[{"id": 0, "obstacleAngleSts": 0, "angle": 126}, 
                                                                                  {"id": 1, "obstacleAngleSts": 2, "angle": 125.5}, 
                                                                                  {"id": 2, "obstacleAngleSts": 1, "angle": 85}, 
                                                                                  {"id": 3, "obstacleAngleSts": 3, "angle": 127}]})
       
    @allure.title("通知/获取门动作请求_遍历四门车门无请求") 
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1981363(self):
        for door in range(4):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": door, "pos": 50}]})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": door, "targetPosition": 50, "action": 0}]})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [door]},
                                                {"out":[{"id": door, "targetPosition": 50, "action": 0}]})
        
    @allure.title("通知/获取门动作请求_计时器逻辑") #v1.4新增计时器
    @pytest.mark.sanity
    def test_caseid_1984669(self):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 4, "pos": 50}]})
            self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 50, "action": 0},
                                                                                         {"id": 1, "targetPosition": 50, "action": 0},
                                                                                         {"id": 2, "targetPosition": 50, "action": 0},
                                                                                         {"id": 3, "targetPosition": 50, "action": 0}]}, 
                                      method_args={"doors": [4]},timeout=10)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 4, "pos": 100}]})
            self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 100, "action": 0},
                                                                                         {"id": 1, "targetPosition": 100, "action": 0},
                                                                                         {"id": 2, "targetPosition": 100, "action": 0},
                                                                                         {"id": 3, "targetPosition": 100, "action": 0}]},timeout=0.2)
            self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "DoorActionRequest",timeout=0.1)
            self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 101, "action": 0},
                                                                                         {"id": 1, "targetPosition": 101, "action": 0},
                                                                                         {"id": 2, "targetPosition": 101, "action": 0},
                                                                                         {"id": 3, "targetPosition": 101, "action": 0}]},
                                                                                        method_args={"doors": [4]},timeout=10)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 0, "pos": 0}]})
            self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 0, "action": 0},
                                                                                         {"id": 1, "targetPosition": 101, "action": 0},
                                                                                         {"id": 2, "targetPosition": 101, "action": 0},
                                                                                         {"id": 3, "targetPosition": 101, "action": 0}]},timeout=0.1)
            sleep(0.1)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 1, "pos": 50}]})
            self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 0, "action": 0},
                                                                                         {"id": 1, "targetPosition": 50, "action": 0},
                                                                                         {"id": 2, "targetPosition": 101, "action": 0},
                                                                                         {"id": 3, "targetPosition": 101, "action": 0}]},timeout=0.1)
            sleep(0.1)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 2, "pos": 70}]})
            self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 0, "action": 0},
                                                                                         {"id": 1, "targetPosition": 50, "action": 0},
                                                                                         {"id": 2, "targetPosition": 70, "action": 0},
                                                                                         {"id": 3, "targetPosition": 101, "action": 0}]},timeout=0.1)
            sleep(0.1)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 3, "pos": 100}]})
            self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 101, "action": 0},
                                                                                         {"id": 1, "targetPosition": 50, "action": 0},
                                                                                         {"id": 2, "targetPosition": 70, "action": 0},
                                                                                         {"id": 3, "targetPosition": 100, "action": 0}]},timeout=0.1)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 1, "targetPosition": 101, "action": 0}]})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 2, "targetPosition": 101, "action": 0}]})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 3, "targetPosition": 101, "action": 0}]})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [4]},
                                                {"out":[{"id": 0, "targetPosition": 101, "action": 0},
                                                        {"id": 1, "targetPosition": 101, "action": 0},
                                                        {"id": 2, "targetPosition": 101, "action": 0},
                                                        {"id": 3, "targetPosition": 101, "action": 0}]})
                    
    @allure.title("通知/获取门动作请求_遍历四门开") 
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.full
    def test_caseid_1981364(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(1)
        doors = {"drvr": 0, "pass": 1, "lere": 2, "rire": 3}
        for door, sts in doors.items():
            (eval(f"self.io.{door}_door_open()")) 
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, "EngSt1WdStsEngSt1WdSts", 8)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1EgyLvlElecMai", 0)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Open",
                                            {"doors": [sts]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": sts, "pos": 50}]})

            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest",{"pos": [{"id": sts, "targetPosition": 50, "action": 1}]})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [sts]},
                                                {"out": [{"id": sts, "targetPosition": 50, "action": 1}]})
            sleep(0.3)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest",{"pos": [{"id": sts, "targetPosition": 101, "action": 1}]})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [sts]},
                                                {"out": [{"id": sts, "targetPosition": 101, "action": 1}]})
        self.partner.empty_all(1)
        for door, sts in doors.items():
            (eval(f"self.io.{door}_door_open()")) 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, "EngSt1WdStsEngSt1WdSts", 8)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 4, "pos": 50}]})
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Open",
                                            {"doors": [4]})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 50, "action": 1},
                                                                                {"id": 1, "targetPosition": 50,"action": 1},
                                                                                {"id": 2, "targetPosition": 50, "action": 1},
                                                                                {"id": 3, "targetPosition": 50, "action": 1}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [4]},
                                                                            {"out": [{"id": 0, "targetPosition": 50, "action": 1},
                                                                                {"id": 1, "targetPosition": 50, "action": 1},
                                                                                {"id": 2, "targetPosition": 50, "action": 1},
                                                                                {"id": 3, "targetPosition": 50, "action": 1}]})
            
    @allure.title("通知/获取门动作请求_遍历四门停") 
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.full
    def test_caseid_1981366(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, "EngSt1WdStsEngSt1WdSts", 8)
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1EgyLvlElecMai", 0)
        doors = {"Drvr": 0, "Pass": 1, "LeRe": 2, "RiRe": 3}
        for door, sts in doors.items():
            logger.info(f"当前门.{door}")
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": sts, "pos": 100}]})
            self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0]}podBodyFr01"), f'DoorOpener{door}Sts', 6)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Stop", {"doors": [sts]})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT,"DoorActionRequest", {"pos": [{"id": sts, "targetPosition":100, "action": 3}]})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [sts]},
                                                {"out": [{"id": sts, "targetPosition": 100, "action": 3}]})  
            sleep(1)
        doors = {"Drvr": 0, "Pass": 1, "LeRe": 2, "RiRe": 3}
        for door, sts in doors.items():
            logger.info(f"当前门.{door}")
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": sts, "pos": 100}]})
            self.ipdu.set(eval(f"self.ipdu.bodycan.{door[0]}podBodyFr01"), f'DoorOpener{door}Sts', 6)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Stop", {"doors": [4]})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT,"DoorActionRequest", {"pos": [{"id": 0, "targetPosition":100, "action": 3},
                                                        {"id": 1, "targetPosition": 100, "action": 3},
                                                        {"id": 2, "targetPosition": 100, "action": 3},
                                                        {"id": 3, "targetPosition": 100, "action": 3}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetDoorActionRequest", {"doors": [4]},
                                                {"out":[{"id":0, "targetPosition": 100, "action": 3},
                                                        {"id":1, "targetPosition": 100, "action": 3},
                                                        {"id":2, "targetPosition": 100, "action": 3},
                                                        {"id":3, "targetPosition": 100, "action": 3}]})  
  
    @allure.title("通知/获取门动作请求_遍历四门关") 
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.full
    def test_caseid_1981365(self):
        self.dk.set_cenlock_sts(0x1)
        self.sd_tester.change_usage_mode(1)
        doors = {"drvr": 0, "pass": 1, "lere": 2, "rire": 3}
        for door, sts in doors.items():
            (eval(f"self.io.{door}_door_open()")) 
        sleep(2)
        self.partner.empty_all(1)
        for door, sts in doors.items():
            (eval(f"self.io.{door}_door_close()")) 
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, "EngSt1WdStsEngSt1WdSts", 8)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1EgyLvlElecMai", 0)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": sts, "pos": 100}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Close", {"doors": [sts]})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": sts, "targetPosition": 100, "action": 2}]})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest",{"doors": [sts]},
                                                {"out": [{"id": sts, "targetPosition": 100, "action": 2}]})     
            sleep(2)
                
    @allure.title("通知/获取门动作请求_遍历四门开到最小角度") 
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1981367(self):
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.sd_tester.change_usage_mode(2)
        self.sd_tester.tester_present()
        sleep(0.5)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": True})
        sleep(0.5)
        self.partner.send_request_and_ck_resp(VEHICLESETSTATUS_CLIENT, "GetWashModeSts", {}, {"out": True}) 
        self.dk.set_cenlock_sts(0x1)
        doors = {"drvr": 0, "pass": 1, "lere": 2, "rire": 3}
        for door, sts in doors.items():
            logger.info(f"当前门{door}")
            eval(f"self.io.{door}_door_open()")
            self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, "EngSt1WdStsEngSt1WdSts", 8)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr02, "VehModMngtGlbSafe1EgyLvlElecMai", 0)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": sts, "pos": 50}]})
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Open", {"doors": [sts]})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT,"DoorActionRequest",{"pos":[{"id":sts,"targetPosition":50,"action":4}]})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetDoorActionRequest",{"doors":[sts]},
                                                    {"out":[{"id":sts,"targetPosition":50,"action":4}]})
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetWashMode", {"isOn": False})

    @allure.title("通知/获取左后儿童锁状态_上锁/未上锁")#v1.4新增结构体拆分
    @pytest.mark.sanity
    def test_caseid_1983348(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftStsToHmi', 2)
        self.partner.empty_all(1)
        dic = {1: True, 0: "", 2: False, 3 : ""}
        last = ""
        for sts1, chdbool in dic.items():
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftStsToHmi', sts1)
            if sts1 in [1, 2]:
                self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftChildLock", {"sts": sts1 })
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetChildLock", {"doors": [2]},
                                              {"out": [{"id": 2, "isLocked": chdbool}]})
                last = chdbool
            else:
                self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "RearLeftChildLock")
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetChildLock", {"doors": [2]},
                                              {"out": [{"id": 2, "isLocked": last}]})         
                       
    @allure.title("通知/获取右后儿童锁状态_上锁/未上锁")#v1.4新增结构体拆分
    @pytest.mark.sanity
    def test_caseid_1983349(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'ChdLockRightStsToHmi', 2)
        self.partner.empty_all(1)
        dic = {1: True, 0: "", 2: False, 3 : ""}
        last = ""
        for sts1, chdbool in dic.items():
            logger.info(f"当前信号.{sts1},当前状态.{chdbool}")
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'ChdLockRightStsToHmi', sts1)
            if sts1 in [1, 2]:
                self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightChildLock", {"sts": sts1 })
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetChildLock", {"doors": [3]},
                                              {"out": [{"id": 3, "isLocked": chdbool}]})
                last = chdbool
            else:
                self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "RearRightChildLock")
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetChildLock", {"doors": [3]},
                                              {"out": [{"id": 3, "isLocked": last}]})            
   
    @allure.title("通知/获取儿童锁状态_右后门上锁后上下电校验默认值")#v1.4新增结构体拆分
    @pytest.mark.full
    def test_caseid_1983347(self):
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftStsToHmi', 2)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'ChdLockRightStsToHmi', 2)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftStsToHmi', 1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr01, 'ChdLockRightStsToHmi', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftChildLock", {"sts": 1 })
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightChildLock", {"sts": 1 })
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetChildLock", {"doors": [4]},
                                              {"out": [{"id": 2, "isLocked": True}, {"id": 3, "isLocked": True}]})
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetChildLock", {"doors": [4]},
                                              {"out": [{"id": 2, "isLocked": False}, {"id": 3, "isLocked": False}]})
        self.ipdu.resume_all_bus_send()
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftChildLock", {"sts": 1 })
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightChildLock", {"sts": 1 })
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetChildLock", {"doors": [4]},
                                              {"out": [{"id": 2, "isLocked": True}, {"id": 3, "isLocked": True}]})    
        
    @allure.title("通知/获取主驾驶电动门开关状态_主驾驶开/关&有效&遍历电动门运动状态&门防夹激活/未激活")
    @pytest.mark.smoke
    def test_caseid_1983436(self):
        self.io.drvr_door_open()
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorOpenerDrvrSts", 4)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrAntiPnch", 1)
        self.partner.empty_all(1)
        temp = (-1,-1,-1,-1)
        door_dic = {
                    0: 7, 1: 2, 2: 5, 3: 9, 4: 6, 5: 0, 6: 1, 7: 8, 8: 6, 9: 10, 10: 6, 
                    11: 65535, 12:  65535, 13: 65535, 14: 65535, 15: 65535
                       }
        sig_dic = {0 : False, 1 : True}
        for dr_sig, dr_sts in sig_dic.items():
            if dr_sig == 1:
                self.io.drvr_door_open()
            else:
                self.io.drvr_door_close()
            self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrAntiPnch", dr_sig)
            for sigkey, sigvalue in door_dic.items():
                logger.info(f"当前防夹状态.{dr_sts},当前运动状态.{sigkey},当前门开关.{dr_sig}")
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorOpenerDrvrSts", sigkey)
                if sigkey in [11, 12, 13, 14, 15]:
                    if temp !=(dr_sts,0,65535,dr_sts):
                        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": dr_sts, "isOpenValidity": 0}, "sts": 65535, "isAntiPinch": dr_sts}})
                        temp=(dr_sts,0,65535,dr_sts)
                    else:
                        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts")    
                else:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": dr_sts, "isOpenValidity": 0}, "sts": sigvalue, "isAntiPinch": dr_sts}})
                    temp=(dr_sts,0,sigvalue,dr_sts)
                self.partner.empty_all(1)
   
    @allure.title("通知主驾驶电动门开关状态_校验bgm重启后event上报")
    @pytest.mark.sanity
    def test_caseid_1984336(self):
        self.io.drvr_door_close()
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorOpenerDrvrSts", 4)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrAntiPnch", 1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 0}, "sts": 6, "isAntiPinch": True}})
        self.partner.empty_all(1)
        self.io.drvr_door_open()
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorOpenerDrvrSts", 4)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrAntiPnch", 0)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 0}, "sts": 6, "isAntiPinch": False}}) 
        self.io.drvr_door_open()
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorOpenerDrvrSts", 11)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrAntiPnch", 0)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 0}, "sts": 65535, "isAntiPinch": False}})   
 
    @allure.title("通知/获取副驾驶电动门开关状态_副驾驶开/关&有效&遍历电动门运动状态&门防夹激活/未激活")
    @pytest.mark.full
    def test_caseid_1983439(self):
        self.io.pass_door_open()
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorOpenerPassSts", 4)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassAntiPnch", 1)
        self.partner.empty_all(1)
        temp = (-1,-1,-1,-1)
        door_dic = {
                    0: 7, 1: 2, 2: 5, 3: 9, 4: 6, 5: 0, 6: 1, 7: 8, 8: 6, 9: 10, 10: 6, 
                    11: 65535, 12:  65535, 13: 65535, 14: 65535, 15: 65535
                       }
        sig_dic = {0 : False, 1 : True}
        for dr_sig, dr_sts in sig_dic.items():
            if dr_sig == 1:
                self.io.pass_door_open()
            else:
                self.io.pass_door_close()
            self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassAntiPnch", dr_sig)
            for sigkey, sigvalue in door_dic.items():
                logger.info(f"当前防夹状态.{dr_sts},当前运动状态.{sigkey},当前门开关.{dr_sig}")
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorOpenerPassSts", sigkey)
                if sigkey in [11, 12, 13, 14, 15]:
                    if temp !=(dr_sts,0,65535,dr_sts):
                       self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": dr_sts, "isOpenValidity": 0}, "sts": 65535, "isAntiPinch": dr_sts}})
                       temp=(dr_sts,0,65535,dr_sts)
                    else:
                        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts")                  
                else:
                   self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": dr_sts, "isOpenValidity": 0}, "sts": sigvalue, "isAntiPinch": dr_sts}})
                   temp=(dr_sts,0,sigvalue,dr_sts)
                self.partner.empty_all(0.5)
 
    @allure.title("通知副驾驶电动门开关状态_校验bgm重启后event上报")
    @pytest.mark.sanity
    def test_caseid_1984335(self):
        self.all_door_open_close(1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorOpenerPassSts", 4)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassAntiPnch", 1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 0}, "sts": 6, "isAntiPinch": True}})
        self.partner.empty_all(1)
        self.all_door_open_close(0)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorOpenerPassSts", 4)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassAntiPnch", 0)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 0}, "sts": 6, "isAntiPinch": False}})     
                 
    @allure.title("通知/获取左后电动门开关状态_左后门开/关&有效&遍历电动门运动状态&门防夹激活/未激活")
    @pytest.mark.sanity
    def test_caseid_1983440(self):
        self.io.lere_door_open()
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorOpenerLeReSts", 4)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeReAntiPnch", 1)
        self.partner.empty_all(1)
        door_dic = {
                    0: 7, 1: 2, 2: 5, 3: 9, 4: 6, 5: 0, 6: 1, 7: 8, 8: 6, 9: 10, 10: 6, 
                    11: 65535, 12:  65535, 13: 65535, 14: 65535, 15: 65535
                       }
        sig_dic = {0 : False, 1 : True}
        temp = (-1, -1, -1, -1)
        for dr_sig, dr_sts in sig_dic.items():
            if dr_sig == 1:
                self.io.lere_door_open()
            else:
                self.io.lere_door_close()
            self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeReAntiPnch", dr_sig)
            for sigkey, sigvalue in door_dic.items():
                logger.info(f"当前防夹状态.{dr_sts},当前运动状态.{sigkey},当前门开关.{dr_sig}")
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorOpenerLeReSts", sigkey)
                if sigkey in [11, 12, 13, 14, 15]:
                    if temp !=(dr_sts,0,65535,dr_sts):
                       self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": dr_sts, "isOpenValidity": 0}, "sts": 65535, "isAntiPinch": dr_sts}})
                       temp=(dr_sts,0,65535,dr_sts)
                    else:
                        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts")                
                else:
                   self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": dr_sts, "isOpenValidity": 0}, "sts": sigvalue, "isAntiPinch": dr_sts}})    
                   temp=(dr_sts,0,sigvalue,dr_sts)
                self.partner.empty_all(0.5)
      
    @allure.title("通知左后电动门开关状态_校验bgm重启后event上报")
    @pytest.mark.sanity
    def test_caseid_1984334(self):
        self.all_door_open_close(1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorOpenerLeReSts", 4)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeReAntiPnch", 1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 0}, "sts": 6, "isAntiPinch": True}})
        self.partner.empty_all(1)
        self.all_door_open_close(0)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorOpenerLeReSts", 4)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeReAntiPnch", 0)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 0}, "sts": 6, "isAntiPinch": False}})  
                 
    @allure.title("通知/获取右后电动门开关状态_右后门开/关&有效&遍历电动门运动状态&门防夹激活/未激活")
    @pytest.mark.sanity
    def test_caseid_1983441(self):
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorOpenerRiReSts", 4)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiReAntiPnch", 1)
        door_dic = {
                    0: 7, 1: 2, 2: 5, 3: 9, 4: 6, 5: 0, 6: 1, 7: 8, 8: 6, 9: 10, 10: 6, 
                    11: 65535, 12:  65535, 13: 65535, 14: 65535, 15: 65535
                    }
        sig_dic = {0 : False, 1 : True}
        temp = (-1,-1,-1,-1)
        for dr_sig, dr_sts in sig_dic.items():
            if dr_sig == 1:
                self.io.rire_door_open()
            else:
                self.io.rire_door_close()
            self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiReAntiPnch", dr_sig)
            for sigkey, sigvalue in door_dic.items():
                logger.info(f"当前防夹状态.{dr_sts},当前运动状态.{sigkey},当前门开关.{dr_sig}")  
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorOpenerRiReSts", sigkey)
                if sigkey in [11, 12, 13, 14, 15]:
                    if temp !=(dr_sts,0,65535,dr_sts):
                        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts", {"sts":{"openCloseSts":{"isOpen": dr_sts, "isOpenValidity": 0}, "sts": 65535, "isAntiPinch": dr_sts}})
                        temp=(dr_sts,0,65535,dr_sts)
                    else:
                        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts")
                else:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts", {"sts":{"openCloseSts":{"isOpen": dr_sts, "isOpenValidity": 0}, "sts": sigvalue, "isAntiPinch": dr_sts}})
                    temp=(dr_sts,0,sigvalue,dr_sts)
                    self.partner.empty_all(0.5)
            
    @allure.title("通知右后电动门开关状态_校验bgm重启后event上报")
    @pytest.mark.sanity
    def test_caseid_1984333(self):
        self.all_door_open_close(1)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorOpenerRiReSts", 4)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiReAntiPnch", 1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 0}, "sts": 6, "isAntiPinch": True}})
        self.partner.empty_all(1)
        self.all_door_open_close(0)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorOpenerRiReSts", 4)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiReAntiPnch", 0)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 0}, "sts": 6, "isAntiPinch": False}})  
                 
    @allure.title("通知主驾电动门位置信息_遍历主驾驶门实际开度&门实际角度&门最小角度提示&门设置的最大角度")
    @pytest.mark.sanity
    def test_caseid_1983457(self):  
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DoorDrvrMInAngleFb", 1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrPercPosn", 10)
        self.partner.empty_all(1)
        dic1 = {0 : False, 1 : True}
        temp = (-1, -1, -1, -1)
        for sig, sts in dic1.items():
            self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DoorDrvrMInAngleFb", sig)
            for pos1 in [0, 100, 101, 127, 50, 20]:
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrPercPosn", pos1)
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "TopPercDrvrHmiFeedBack", pos1) 
                for agl in [0, 71, 14, 30, 50, 10, 40, 85]:
                    logger.info(f"当前门开度.{pos1},当前门实际角度.{agl},当前门最小角度提示.{sig},当前门设置的最大开度.{pos1}")
                    self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPosn', agl) 
                    if agl >65:
                        if temp != (pos1, 255, sts, pos1):
                           self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorPosition", {"position":{"position": pos1, "angle": 255, "minAngleReminder": sts, "maxPosition": pos1}})    
                           temp=(pos1, 255, sts, pos1)
                        else:
                           self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorPosition")   
                    else:
                        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorPosition", {"position":{"position": pos1, "angle": agl, "minAngleReminder": sts, "maxPosition": pos1}})    
                        temp=(pos1, agl, sts, pos1)
                    self.partner.empty_all(0.5)
                     
    @allure.title("通知主驾电动门位置信息_校验bgm重启event上报")
    @pytest.mark.sanity
    def test_caseid_1984332(self):  
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DoorDrvrMInAngleFb", 0)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrPercPosn", 100)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "TopPercDrvrHmiFeedBack", 50) 
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPosn', 65) 
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorPosition", {"position":{"position": 100, "angle": 65, "minAngleReminder": False, "maxPosition": 50}})    
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DoorDrvrMInAngleFb", 1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrPercPosn", 100)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "TopPercDrvrHmiFeedBack", 50) 
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPosn', 65) 
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorPosition", {"position":{"position": 100, "angle": 65, "minAngleReminder": True, "maxPosition": 50}})    
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DoorDrvrMInAngleFb", 0)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrPercPosn", 120)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "TopPercDrvrHmiFeedBack", 110) 
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPosn', 71) 
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorPosition", {"position":{"position": 120, "angle": 255, "minAngleReminder": False, "maxPosition": 110}})        
                   
    @allure.title("通知副驾电动门位置信息_遍历副驾驶门实际开度&门实际角度&门最小角度提示&门设置的最大角度")
    @pytest.mark.sanity
    def test_caseid_1983459(self):  
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DoorPassMInAngleFb", 1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassPercPosn", 10)
        self.partner.empty_all(1)
        dic1 = {0 : False, 1 : True}
        temp = (-1, -1, -1, -1)
        for sig, sts in dic1.items():
            self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DoorPassMInAngleFb", sig)
            for pos1 in [0, 100, 101, 127, 50, 20]:
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassPercPosn", pos1)
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "TopPercPassHmiFeedBack", pos1) 
                for agl in [0, 71, 14, 30, 50, 10, 40, 85]:
                    logger.info(f"当前门开度.{pos1},当前门实际角度.{agl},当前门最小角度提示.{sig},当前门设置的最大开度.{pos1}")
                    self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassPosn', agl) 
                    if agl >65:
                        if temp != (pos1, 255, sts, pos1):
                           self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorPosition", {"position":{"position": pos1, "angle": 255, "minAngleReminder": sts, "maxPosition": pos1}})    
                           temp=(pos1, 255, sts, pos1)
                        else:
                           self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntRightDoorPosition")  
                    else:
                        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorPosition", {"position":{"position": pos1, "angle": agl, "minAngleReminder": sts, "maxPosition": pos1}})    
                        temp=(pos1, agl, sts, pos1)
                    self.partner.empty_all(0.5)
                    
    @allure.title("通知副驾电动门位置信息_校验bgm重启event上报")
    @pytest.mark.sanity
    def test_caseid_1984331(self):  
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DoorPassMInAngleFb", 0)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassPercPosn", 100)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "TopPercPassHmiFeedBack", 50) 
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassPosn', 65) 
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorPosition", {"position":{"position": 100, "angle": 65, "minAngleReminder": False, "maxPosition": 50}})    
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DoorPassMInAngleFb", 1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassPercPosn", 100)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "TopPercPassHmiFeedBack", 50) 
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassPosn', 65) 
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorPosition", {"position":{"position": 100, "angle": 65, "minAngleReminder": True, "maxPosition": 50}})
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01,"DoorPassMInAngleFb", 1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassPercPosn", 120)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "TopPercPassHmiFeedBack", 110) 
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassPosn', 71) 
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorPosition", {"position":{"position": 120, "angle": 255, "minAngleReminder": True, "maxPosition": 110}})            
                    
    @allure.title("通知左后电动门位置信息_遍历左后电动门实际开度&门实际角度&门最小角度提示&门设置的最大角度")
    @pytest.mark.sanity
    def test_caseid_1983460(self):  
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DoorLeReMInAngleFb", 1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeRePercPosn", 10)
        self.partner.empty_all(1)
        dic1 = {0 : False, 1 : True}
        temp = (-1, -1, -1, -1)
        for sig, sts in dic1.items():
            self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DoorLeReMInAngleFb", sig)
            for pos1 in [0, 100, 101, 127, 50, 20]:
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeRePercPosn", pos1)
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'TopPercLeReHmiFeedBack', pos1) 
                for agl in [0, 71, 14, 30, 50, 10, 40, 85]:
                    logger.info(f"当前门开度.{pos1},当前门实际角度.{agl},当前门最小角度提示.{sig},当前门设置的最大开度.{pos1}")
                    self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeRePosn', agl) 
                    if agl >65:
                        if temp != (pos1, 255, sts, pos1):
                           self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorPosition", {"position":{"position": pos1, "angle": 255, "minAngleReminder": sts, "maxPosition": pos1}})    
                           temp=(pos1, 255, sts, pos1)
                        else:
                           self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "RearLeftDoorPosition")  
                    else:
                        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorPosition", {"position":{"position": pos1, "angle": agl, "minAngleReminder": sts, "maxPosition": pos1}})    
                        temp=(pos1, agl, sts, pos1)
                    self.partner.empty_all(0.5)
 
    @allure.title("通知左后电动门位置信息_校验bgm重启event上报")
    @pytest.mark.sanity
    def test_caseid_1984330(self):  
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DoorLeReMInAngleFb", 0)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeRePercPosn", 100)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'TopPercLeReHmiFeedBack', 50) 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeRePosn', 65) 
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorPosition", {"position":{"position": 100, "angle": 65, "minAngleReminder": False, "maxPosition": 50}})    
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DoorLeReMInAngleFb", 1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeRePercPosn", 100)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'TopPercLeReHmiFeedBack', 50) 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeRePosn', 65) 
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorPosition", {"position":{"position": 100, "angle": 65, "minAngleReminder": True, "maxPosition": 50}})    
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01,"DoorLeReMInAngleFb", 1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeRePercPosn", 120)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'TopPercLeReHmiFeedBack', 110) 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeRePosn', 71) 
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorPosition", {"position":{"position": 120, "angle": 255, "minAngleReminder": True, "maxPosition": 110}})        
      
    @allure.title("通知右后电动门位置信息_遍历右后电动门实际开度&门实际角度&门最小角度提示&门设置的最大角度")
    @pytest.mark.full
    def test_caseid_1983461(self):  
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01,"DoorRiReMInAngleFb", 1)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiRePercPosn", 10)
        self.partner.empty_all(1)
        dic1 = {0 : False, 1 : True}
        temp = (-1, -1, -1, -1)
        for sig, sts in dic1.items():
            self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01,"DoorRiReMInAngleFb", sig)
            for pos1 in [0, 100, 101, 127, 50, 20]:
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiRePercPosn", pos1)
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'TopPercRiReHmiFeedBack', pos1) 
                for agl in [0, 71, 14, 30, 50, 10, 40, 85]:
                    logger.info(f"当前门开度.{pos1},当前门实际角度.{agl},当前门最小角度提示.{sig},当前门设置的最大开度.{pos1}")
                    self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiRePosn', agl) 
                    if agl >65:
                        if temp != (pos1, 255, sts, pos1):
                           self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorPosition", {"position":{"position": pos1, "angle": 255, "minAngleReminder": sts, "maxPosition": pos1}})    
                           temp=(pos1, 255, sts, pos1)
                        else:
                           self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "RearRightDoorPosition")  
                    else:
                        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorPosition", {"position":{"position": pos1, "angle": agl, "minAngleReminder": sts, "maxPosition": pos1}})    
                        temp=(pos1, agl, sts, pos1)
                    self.partner.empty_all(0.5)
                                         
    @allure.title("通知右后电动门位置信息_校验bgm重启event上报")
    @pytest.mark.sanity
    def test_caseid_1984329(self):  
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01,"DoorRiReMInAngleFb", 0)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiRePercPosn", 100)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'TopPercRiReHmiFeedBack', 50) 
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiRePosn', 65) 
        sleep(1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorPosition", {"position":{"position": 100, "angle": 65, "minAngleReminder": False, "maxPosition": 50}})    
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01,"DoorRiReMInAngleFb", 1)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiRePercPosn", 100)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'TopPercRiReHmiFeedBack', 50) 
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiRePosn', 65) 
        sleep(1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorPosition", {"position":{"position": 100, "angle": 65, "minAngleReminder": True, "maxPosition": 50}})      
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01,"DoorRiReMInAngleFb", 1)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiRePercPosn", 120)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'TopPercRiReHmiFeedBack', 110) 
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiRePosn', 71) 
        sleep(1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorPosition", {"position":{"position": 120, "angle": 255, "minAngleReminder": True, "maxPosition": 110}})       

@allure.feature("SOA服务接口")                                  
@allure.story("整车控制/DoorService")
@pytest.mark.mockmcu
class TestDoorServiceMockMcu(TestBase):

    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("DoorService", "client")])
        sleep(5)

    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
                
    def before_each_func(self, ecu):
        super().before_each_func(ecu) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 2)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 2)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 2)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 2)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 6)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', 6)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 6)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 6)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrPercPosn", 0) 
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassPercPosn", 0)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeRePercPosn", 0)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiRePercPosn", 0)    
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 0)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 0)  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 2)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 2)  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 2)  
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 2) 
        sleep(3)    
        self.partner.empty_all(0.5) 

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu)
        sleep(10)    
   
    @allure.title("通知/获取所有侧门的侧方开门保护状态_flag默认为1")
    @pytest.mark.smoke
    @pytest.mark.jishu2
    def test_caseid_1987879(self):  
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1) 
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)  
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)  
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",
                                  {"openProtectionSts":{"isActiveFL":True,"isActiveFR":True,"isActiveRL":True,"isActiveRR":True}})
   
    @allure.title("通知/获取门开关状态_带功能安全_信号值未定义")
    @pytest.mark.santy
    def test_caseid_1980827(self): 
        dic1= { "Drvr" : ["02", "em"], "Pass" : ["11", "EM"], "LeRe" : ["02", "em"], "RiRe" : ["11", "EM"]}
        for key, sig1 in dic1.items():
            for key, sig1 in dic1.items():
                sleep(0.5)
                self.ipdu.set(eval(f"self.ipdu.bodycan.C{sig1[1]}BodyFr{sig1[0]}"), f'Door{key}Sts', 3)
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetOpenCloseStatusValidity",{"doors": [4]},
                                                            {"out": [{"value": {"id": 0, "isOpen": False}, "isOpenValidity": 1},
                                                        {"value": {"id": 1, "isOpen": False}, "isOpenValidity": 1},
                                                        {"value": {"id": 2, "isOpen": False}, "isOpenValidity": 1},
                                                        {"value": {"id": 3, "isOpen": False}, "isOpenValidity": 1}]})
        
    @allure.title("通知/获取门按键开关状态_遍历四门遍历开关状态") #待1.4修改
    @pytest.mark.full
    def test_caseid_1982006(self):
        for sig in range(4):  
            logger.info(f"当前信号.{sig}")  
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr38, "DoorDrvrOpenReqInsdLogic", sig)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr38, "DoorPassOpenReqInsdLogic", sig)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr38, "DoorLeReOpenReqInsdLogic", sig)
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr38, "DoorRiReOpenReqInsdLogic", sig)
            if sig == 3:
                self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"doors": 3, "side": 0, "sts": 0})
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 0, "side": 0},
                                                {"out": 0})
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 1, "side": 0},
                                                {"out": 0})
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 2, "side": 0},
                                                {"out": 0})
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 3, "side": 0},
                                                {"out": 0})
            else:
                self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyDoorSwitchSts", {"doors": 3, "side": 0, "sts": sig})
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 0, "side": 0},
                                                {"out": sig})         
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 1, "side": 0},
                                                {"out": sig})
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 2, "side": 0},
                                                {"out": sig})
                self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorSwitchSts", {"doors": 3, "side": 0},
                                                {"out": sig})
                
    @allure.title("通知/获取门动作请求_主驾驶门无效")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.full
    def test_caseid_1984726(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 0, "pos": 100}]})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 7)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 101, "action": 255}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [0]},
                                              {"out": [{"id":0, "targetPosition": 101, "action": 255}]})

    @allure.title("通知/获取门动作请求_副驾驶门无效")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.full
    def test_caseid_1984727(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 1, "pos": 100}]})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 7)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos":[{"id": 1, "targetPosition": 101, "action": 255}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [1]},
                                              {"out": [{"id": 1, "targetPosition": 101, "action": 255}]})

    @allure.title("通知/获取门动作请求_左后门无效")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.full
    def test_caseid_1984728(self):
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 2, "pos": 100}]})
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 1)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 7)
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT,"DoorActionRequest", {"pos": [{"id": 2, "targetPosition": 101, "action": 255}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [2]},
                                              {"out": [{"id": 2, "targetPosition": 101, "action": 255}]})


    @allure.title("通知/获取门动作请求_右后门无效")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1754628?projectId=46')
    @pytest.mark.full
    def test_caseid_1984729(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2',1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 3, "pos": 100}]})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 7)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 3, "targetPosition": 101, "action": 255}]})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetDoorActionRequest",{"doors": [3]},
                                              {"out": [{"id": 3, "targetPosition": 101, "action": 255}]})
    
    @allure.title("获取门开关状态_带功能安全_有效&信号超时或丢失")
    @pytest.mark.full
    def test_caseid_1980826(self): 
        flag = True
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.pause_all_bus_send()
        logger.info(f"停发总线。。。。。。。。。。。。。。。")
        sleep(5)
        try:
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {"doors": [4]},
                                                            {"out": [{"value": {"id": 0, "isOpen": False}, "isOpenValidity": 4},
                                                                    {"value": {"id": 1, "isOpen": False}, "isOpenValidity": 4},
                                                                    {"value": {"id": 2, "isOpen": False}, "isOpenValidity": 4},
                                                                    {"value": {"id": 3, "isOpen": False}, "isOpenValidity": 4}]})   
        except:
            flag = False
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        assert flag  
        self.ipdu.resume_all_bus_send()
        sleep(1)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {"doors": [4]},
                                                          {"out": [{"value": {"id": 0, "isOpen": False}, "isOpenValidity": 0},
                                                                   {"value": {"id": 1, "isOpen": False}, "isOpenValidity": 0},
                                                                   {"value": {"id": 2, "isOpen": False}, "isOpenValidity": 0},
                                                                   {"value": {"id": 3, "isOpen": False}, "isOpenValidity": 0}]})
                
    @allure.title("通知/获取门动作请求_遍历信号0~8")
    @pytest.mark.smoke
    def test_caseid_1982009(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 2)
        self.partner.empty_all(0.5)
        dic ={0 : ["Drvr", 78], 1 : ["Pass", 79], 2 : ["LeRe", 78], 3 : ["RiRe", 79]}
        temp =(-1, -1, -1)
        for door_id, door_sig in dic.items():
            for sig in range(8):
                logger.info(f"当前门.{door_id},当前信号.{sig}")
                self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": door_id, "pos": 50}]})
                self.ipdu.set(eval(f"self.ipdu.bodycan.CemBodyFr{door_sig[1]}"), f'DoorOpener{door_sig[0]}ReqDoorOpenerReq2', sig)
                if sig > 4:
                    if  temp != (door_id, 50, 255):
                        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": door_id, "targetPosition": 50, "action": 255}]})
                        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [door_id]},
                                                                        {"out": [{"id": door_id, "targetPosition": 50, "action": 255}]})   
                        temp = (door_id, 50, 255)
                    else:
                        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [door_id]},
                                                                        {"out": [{"id": door_id, "targetPosition": 101, "action": 255}]})   
                else:       
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": door_id, "targetPosition": 50, "action": sig}]})
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [door_id]},
                                                                        {"out": [{"id": door_id, "targetPosition": 50, "action": sig}]})
                    temp = (door_id, 50, sig)
                self.partner.empty_all(1)
                
    @allure.title("通知/获取门动作请求_遍历请求源")
    @pytest.mark.smoke
    @pytest.mark.jishu2
    def test_caseid_1987668(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 2)
        self.partner.empty_all(0.5)
        dic ={0 : ["Drvr", 78], 1 : ["Pass", 79], 2 : ["LeRe", 78], 3 : ["RiRe", 79]}
        temp =(-1, -1, -1)
        for door_id, door_sig in dic.items():
            for sig in range(8):
                logger.info(f"当前门.{door_id},当前信号.{sig}")
                self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": door_id, "pos": 50}]})
                self.ipdu.set(eval(f"self.ipdu.bodycan.CemBodyFr{door_sig[1]}"), f'DoorOpener{door_sig[0]}ReqDoorOpenerReq2', 1)
                self.ipdu.set(eval(f"self.ipdu.bodycan.CemBodyFr{door_sig[1]}"), f'DoorOpener{door_sig[0]}ReqTrigSrc', sig)
                if sig > 5:
                    if  temp != (door_id, 50, 255):
                        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": door_id, "targetPosition": 50, "action": 1, "triggerId": 255}]})
                        temp = (door_id, 50, 255)       
                    else:
                        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [door_id]},
                                                              {"out": [{"id": door_id, "targetPosition": 50, "action": 1, "triggerId": 255}]})
                else:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": door_id, "targetPosition": 50, "action": 1, "triggerId": sig}]})
                    self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [door_id]},
                                                              {"out": [{"id": door_id, "targetPosition": 50, "action": 1, "triggerId": sig}]})
                    
                    temp = (door_id, 50, 1, sig)
                self.partner.empty_all(1)
                
    @allure.title("通知/获取门动作请求_停发单帧0x0B8总线校验event")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987671(self): 
        dic ={0 : ["Drvr", 78], 1 : ["Pass", 79], 2 : ["LeRe", 78], 3 : ["RiRe", 79]}
        for door_id, door_sig in dic.items():
            logger.info(f"当前门.{door_id}")
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": door_id, "pos": 50}]})
            self.ipdu.set(eval(f"self.ipdu.bodycan.CemBodyFr{door_sig[1]}"), f'DoorOpener{door_sig[0]}ReqDoorOpenerReq2', 1)
            self.ipdu.set(eval(f"self.ipdu.bodycan.CemBodyFr{door_sig[1]}"), f'DoorOpener{door_sig[0]}ReqTrigSrc', 5)
        self.ipdu.stop_send_pdu('bodycan', 0x0B8)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=False, resume_all_bus=False)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 1, "targetPosition": 255, "action": 255, "triggerId": 255},
                                                                                          {"id": 2, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 3, "targetPosition": 255, "action": 255, "triggerId": 255}]}, timeout=20)
        self.partner.empty_all(1)
        self.ipdu.resume_all_bus_send()       
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 1, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 2, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 3, "targetPosition": 255, "action": 1, "triggerId": 5}]},timeout=20)  
              
    @allure.title("通知/获取门动作请求_停发总线校验默认值")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987674(self): 
        dic ={0 : ["Drvr", 78], 1 : ["Pass", 79], 2 : ["LeRe", 78], 3 : ["RiRe", 79]}
        for door_id, door_sig in dic.items():
            logger.info(f"当前门.{door_id}")
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": door_id, "pos": 50}]})
            self.ipdu.set(eval(f"self.ipdu.bodycan.CemBodyFr{door_sig[1]}"), f'DoorOpener{door_sig[0]}ReqDoorOpenerReq2', 1)
            self.ipdu.set(eval(f"self.ipdu.bodycan.CemBodyFr{door_sig[1]}"), f'DoorOpener{door_sig[0]}ReqTrigSrc', 5)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, resume_all_bus=False)
        sleep(10)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetDoorActionRequest", {"doors": [4]}, 
                                                                                          {"out":[{"id": 0, "targetPosition": 255, "action": 255, "triggerId": 255},
                                                                                                  {"id": 1, "targetPosition": 255, "action": 255, "triggerId": 255},
                                                                                                  {"id": 2, "targetPosition": 255, "action": 255, "triggerId": 255},
                                                                                                  {"id": 3, "targetPosition": 255, "action": 255, "triggerId": 255}]})
        self.ipdu.resume_all_bus_send()      
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 1, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 2, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 3, "targetPosition": 255, "action": 1, "triggerId": 5}]})      
        
    @allure.title("通知/获取门动作请求_停发单帧0x0B4总线校验event")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987837(self): 
        dic ={0 : ["Drvr", 78], 1 : ["Pass", 79], 2 : ["LeRe", 78], 3 : ["RiRe", 79]}
        for door_id, door_sig in dic.items():
            logger.info(f"当前门.{door_id}")
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": door_id, "pos": 50}]})
            self.ipdu.set(eval(f"self.ipdu.bodycan.CemBodyFr{door_sig[1]}"), f'DoorOpener{door_sig[0]}ReqDoorOpenerReq2', 1)
            self.ipdu.set(eval(f"self.ipdu.bodycan.CemBodyFr{door_sig[1]}"), f'DoorOpener{door_sig[0]}ReqTrigSrc', 5)
        self.ipdu.stop_send_pdu('bodycan', 0x0B4)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT,pause_all_bus=False, resume_all_bus=False)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 255, "action": 255, "triggerId": 255},
                                                                                          {"id": 1, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 2, "targetPosition": 255, "action": 255, "triggerId": 255},
                                                                                          {"id": 3, "targetPosition": 255, "action": 1, "triggerId": 5}]},timeout=15)
        self.ipdu.resume_all_bus_send()       
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 1, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 2, "targetPosition": 255, "action": 1, "triggerId": 5},
                                                                                          {"id": 3, "targetPosition": 255, "action": 1, "triggerId": 5}]},timeout=10)          
                
    @allure.title("通知/获取门动作请求_不同门id不同值")
    @pytest.mark.full
    @pytest.mark.sanity
    def test_caseid_1987673(self):    
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 0, "pos": 50}]})
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 0)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 1)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 1, "pos": 100}]})
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 1)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', 2)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 2, "pos": 100}]})
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 4)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 4)
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 3, "pos": 100}]})
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 3)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 7)
            sleep(3)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 101, "action": 0, "triggerId": 1},
                                                                                          {"id": 1, "targetPosition": 101, "action": 1, "triggerId": 2},
                                                                                          {"id": 2, "targetPosition": 101, "action": 4, "triggerId": 4},
                                                                                          {"id": 3, "targetPosition": 101, "action": 3, "triggerId": 255}]})                                                   
            self.partner.empty_all(1)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 7)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 3)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 0)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', 3)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 0)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 3)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 7)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0, "targetPosition": 101, "action": 255, "triggerId": 3},
                                                                                          {"id": 1, "targetPosition": 101, "action": 0, "triggerId": 3},
                                                                                          {"id": 2, "targetPosition": 101, "action": 0, "triggerId": 3},
                                                                                          {"id": 3, "targetPosition": 101, "action": 1, "triggerId": 255}]})

    @allure.title("通知/获取所有侧门的侧方开门保护状态_门预警跳变2跳变0，计时器重新计时")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987835(self): 
        dic ={"Drvr": [78, "02", "Cem"], "Pass": [79, "11", "CEM"], "LeRe": [78, "02", "Cem"], "RiRe": [79, "11", "CEM"]}
        for door, door_sig in dic.items():
            logger.info(f"。。。。。。。。。。。。。。当前门: {door}")
            self.ipdu.set(eval(f"self.ipdu.bodycan.CemBodyFr{door_sig[0]}"), f'DoorOpener{door}ReqDoorOpenerReq2', 1)
            self.ipdu.set(eval(f"self.ipdu.bodycan.CemBodyFr{door_sig[0]}"), f'DoorOpener{door}ReqTrigSrc', 5) 
            self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
            self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)           
            self.ipdu.set(eval(f"self.ipdu.bodycan.{door_sig[2]}BodyFr{door_sig[1]}"), f'Door{door}Sts', 1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 1)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 0)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 0)
        sleep(2)
        self.partner.ck_coming_event_and_resp(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts", {"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_门激活保护后发送Close请求不关闭保护")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987767(self):     
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts", {"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        self.partner.empty_all(1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Close", {"doors": [0]})
        sleep(2)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                                  {"out":{"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}},timeout=5)
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_车外调用门开无激活保护")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987764(self):   
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 0, "pos":20}],"scene": 1})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', 4) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11,'DoorPassSts', 1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 3) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 1) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})    
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 2) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})    
             
    @allure.title("通知/获取所有侧门的侧方开门保护状态_车内调用电动门开度")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987711(self):   
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrPercPosn", 101) 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeRePercPosn", 101)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 0, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",
                                             {"openProtectionSts":{"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 1, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",
                                             {"openProtectionSts":{"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :False, "isActiveRR" :False}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :False, "isActiveRR" :False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 2, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",
                                             {"openProtectionSts":{"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :False}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :False}})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 3, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",
                                             {"openProtectionSts":{"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}})
        

    @allure.title("通知/获取所有侧门的侧方开门保护状态_触发预警后1s后内部开门")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987831(self):   
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 1, "pos":20}]},{"scene": 0})
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 2, "pos":20}]},{"scene": 0})
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",
                                             {"openProtectionSts":{"isActiveFL":False, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :False}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :False}})
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 2)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 2)
        sleep(2.5)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 1, "pos":20}]},{"scene": 0})
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 2, "pos":20}]},{"scene": 0})
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.empty_all(0.5)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})    
       
    @allure.title("通知/获取所有侧门的侧方开门保护状态_置主/副车内开门&左后/右后车外开门，触发预警")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987714(self):   
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 4) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})    
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', 0) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 4) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})    
            
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_校验打开阻力取消阻力下行数据")
    @pytest.mark.sanity
    @pytest.mark.jishu2
    def test_caseid_1987821(self): 
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 5) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('DoorOpenResistCmd', [1,  0]) 
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 0)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 0)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('DoorOpenResistCmd', [2, 0]) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_校验取消阻力打断逻辑_取消2s")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1988471(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1) 
        self.bgm_eth_inter.start_bgm_tcpdump()  
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 2)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3) 
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
        self.bgm_eth_inter.ck_signal_values('DoorOpenResistCmd', [2, 1, 0])   
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_电动开度请求小于真实开度百分比")
    @pytest.mark.sanity
    @pytest.mark.jishu2
    def test_caseid_1987712(self): 
        dic={"Drvr": "D", "Pass": "P", "LeRe": "L", "RiRe": "R"}
        for sts, sig in dic.items():
            self.ipdu.set(eval(f"self.ipdu.bodycan.{sig}podBodyFr01"), f"Door{sts}PercPosn", 90) 
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 4, "pos":20}],"scene": 1})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 0, "pos":20}],"scene": 0})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.partner.empty_all(0.5)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 1, "pos":20}],"scene": 0})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.partner.empty_all(0.5)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 2, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 3, "pos":100}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}})
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_左后保护激活后取消预警")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987708(self):     
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 0) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)  
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :False}})    
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 0)    
        sleep(1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts") 
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                    {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})    
         
    @allure.title("通知/获取所有侧门的侧方开门保护状态_左后保护激活后关门取消保护_取消2s")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1988477(self):     
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3) 
        sleep(0.5)  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)  
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :False}})    
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 2)  
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                    {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}, timeout=0.5)    
         
    
    @allure.title("通知/获取所有侧门的侧方开门保护状态_左后2s内取消预警恢复预警")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987701(self):     
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 0) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3) 
        sleep(0.5)  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)  
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :False}})    
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 0) 
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(2)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :False}}) 
            
    @allure.title("通知/获取所有侧门的侧方开门保护状态_左右预警取消时序不同校验阻力下行数据")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987824(self):   
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3) 
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3) 
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 0)
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=5)
        self.bgm_eth_inter.ck_signal_values('DoorOpenResistCmd', []) 
        sleep(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal(sleep_time=3)
        self.bgm_eth_inter.ck_signal_values('DoorOpenResistCmd', [2, 0]) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_左右两侧预警&门关取消门保护后再次开门_取消两秒")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1988457(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)   
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1) 
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})    
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 2) 
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1) 
        sleep(1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
             
           
    @allure.title("通知/获取所有侧门的侧方开门保护状态_四门驾驶门动作请求门最小角度&请求源为无请求")
    @pytest.mark.sanity
    @pytest.mark.jishu2
    def test_caseid_1987684(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 0) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3) 
        sleep(1)  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1) 
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', 0) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3) 
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :False, "isActiveRR" :False}}) 
     
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 0) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3) 
        sleep(1)  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1) 
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :False}}) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 0) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}}) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_四门触发门保护&关闭开启主/右后门&取消左侧预警")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987716(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}}) 
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 2)  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 2) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :True, "isActiveRL" :False, "isActiveRR" :True}}) 
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}}) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_四门激活保护_主/左后门开&右侧取消预警")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987834(self): 
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 0, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 2, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :False}}) 
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 0)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :False}}) 
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 1, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 3, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}}) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 0)
        sleep(2)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
     
    @allure.title("通知/获取所有侧门的侧方开门保护状态_四门激活保护&主/左后门关")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987832(self):   
        for sts in range(4):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": sts, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)    
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)  
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}})
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 2)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 2) 
        sleep(2)         
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :True, "isActiveRL" :False, "isActiveRR" :True}})
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_四门不同请求源激活门保护")
    @pytest.mark.smoke
    @pytest.mark.jishu2
    def test_caseid_1987709(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 1, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :False, "isActiveRR" :False}})
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 0) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :False}})
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Open", {"door":[3],"scene": 0})
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}}) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_四门Open,请求源为车内")
    @pytest.mark.sanity
    @pytest.mark.jishu2
    def test_caseid_1987685(self):  
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Open", {"door":[0],"scene": 0})
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        sleep(0.5)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Open", {"door":[1],"scene": 0})
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Open", {"door":[2],"scene": 0})
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :False}}) 
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "Open", {"door":[3],"scene": 0})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}}) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_右后门保护激活后关门取消保护")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987704(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                              {"isActiveFL":False,"isActiveFR":False,"isActiveRL":False,"isActiveRR":True}}) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 2)
        self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",
                                  {"openProtectionSts":{"isActiveFL":False,"isActiveFR":False,"isActiveRL":False,"isActiveRR":False}}) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_右后保护激活后取消预警")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987707(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :True}}) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 0)
        sleep(1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts") 
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_右后2s内取消预警恢复预警")
    @pytest.mark.sanity
    @pytest.mark.jishu2
    def test_caseid_1987703(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :True}}) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 0)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(2)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :True}}) 

    @allure.title("通知/获取所有侧门的侧方开门保护状态_取消门预警后再次预警门开激活保护")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987768(self): 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 2)
        sleep(2)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :False}})
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_副驾驶保护激活后取消预警")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987706(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :True, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 0)
        sleep(1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts") 
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_副驾驶保护激活后关门取消保护")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1988476(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        sleep(1)
        self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :True, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 2)
        self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}},timeout=2) 

    @allure.title("通知/获取所有侧门的侧方开门保护状态_副驾驶2s内取消预警恢复预警 ")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987702(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :True, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 0)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(2)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :True, "isActiveRL" :False, "isActiveRR" :False}}) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_主驾驶保护激活后取消预警")
    @pytest.mark.sanity
    @pytest.mark.jishu2
    def test_caseid_1987690(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 0)
        sleep(1)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts") 
        sleep(1)
        self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_主驾驶保护激活后关门取消保护_取消2s")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_19884751(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        sleep(1)
        self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts',2)
        self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        

    @allure.title("通知/获取所有侧门的侧方开门保护状态_主驾驶2s内取消预警恢复预警")
    @pytest.mark.sanity
    @pytest.mark.jishu2
    def test_caseid_1987693(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        sleep(1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 0)
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(2)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})     
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_主驾激活保护&左后车内开门")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987825(self):   
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3) 
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 2, "pos": 20}],"scene": 0})
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :False}}) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 2)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts") 
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},{"out":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :False}}) 
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_主副车外开门&左/右后车内开门，触发预警")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987827(self):       
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 4) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)   
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)  
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :False}})
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqTrigSrc', 4) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)   
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)  
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}})
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_主/左后门开未激活，右后门车内触发预警右侧激活保护")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987830(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 4) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)   
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)  
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)  
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)  
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :True}})
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_主/左后门开未激活，再次触发预警左侧激活保护")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987829(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 4) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)   
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1) 
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :True, "isActiveRR" :False}})
   
    @allure.title("通知/获取所有侧门的侧方开门保护状态_左侧预警右侧车内开门")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1988422(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 4) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 5) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 4) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        sleep(0.5)   
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts")
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetSideDoorOpenProtectionSts", {},
                                             {"out":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :True}})
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_一门激活保护，三门任意触发源激活")
    @pytest.mark.sanity
    @pytest.mark.jishu2
    def test_caseid_1987828(self):  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 4)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqTrigSrc', 5) 
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqTrigSrc', 4) 
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)  
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqTrigSrc', 4) 
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)  
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)  
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}})
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_关门和预警结合取消阻力")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1987836(self):  
        for sts in range(4):
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": sts, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)    
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1) 
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 2)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 2)    
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 2) 
        sleep(0.5)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT,"SideDoorOpenProtectionSts",
                                             {"openProtectionSts":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :True}}, timeout=1)    
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 1) 
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 1)
        sleep(2)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
        
    @allure.title("通知/获取所有侧门的侧方开门保护状态_四门保护激活后关门取消保护_取消2s")
    @pytest.mark.full
    @pytest.mark.jishu2
    def test_caseid_1988478(self):  
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "SetPosition", {"doors": [{"id": 4, "pos":20}],"scene": 0})
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnLeIndcn", 3)
        self.ipdu.set(self.ipdu.backbonefr.AsdmBackBoneFr04, "DoorOpenwarnRiIndcn", 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)    
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1) 
        sleep(0.5)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT,"SideDoorOpenProtectionSts",
                                             {"openProtectionSts":{"isActiveFL":True, "isActiveFR" :True, "isActiveRL" :True, "isActiveRR" :True}}, timeout=1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 2)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 2)    
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 2) 
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 2) 
        sleep(0.5)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT,"SideDoorOpenProtectionSts",
                                             {"openProtectionSts":{"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}}, timeout=1)    
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1) 
        self.partner.ck_no_event_and_ck_resp(DOOR_SERVICE_CLIENT, "SideDoorOpenProtectionSts",{"openProtectionSts":
                                                   {"isActiveFL":False, "isActiveFR" :False, "isActiveRL" :False, "isActiveRR" :False}})
           
        
    @allure.title("通知门动作请求_校验bgm重启event上报")
    @pytest.mark.full
    def test_caseid_1984539(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 7)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 3)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 7)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 0, "pos": 10}]}) 
        sleep(1)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0,"targetPosition": 255, "action": 3},
                                                                                     {"id": 1,"targetPosition": 255, "action": 255},
                                                                                     {"id": 2,"targetPosition": 255, "action": 3},
                                                                                     {"id": 3,"targetPosition": 255, "action": 255}]}, timeout=15)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 5) 
        sleep(0.5)
        self.partner.ck_event_and_resp(DOOR_SERVICE_CLIENT, "DoorActionRequest", {"pos": [{"id": 0,"targetPosition": 255, "action": 255},
                                                                                     {"id": 1,"targetPosition": 255, "action": 255},
                                                                                     {"id": 2,"targetPosition": 255, "action": 3},
                                                                                     {"id": 3,"targetPosition": 255, "action": 255}]},method_args={"doors": [4]})
 
    @allure.title("通知/获取主驾驶电动门开关状态_主驾驶信号值未定义&遍历电动门运动状态&门防夹激活/未激活")
    @pytest.mark.full
    def test_caseid_1983442(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorOpenerDrvrSts", 4)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrAntiPnch", 1)
        self.partner.empty_all(1)
        door_dic = {
                    0: 7, 1: 2, 2: 5, 3: 9, 4: 6, 5: 0, 6: 1, 7: 8, 8: 6, 9: 10, 10: 6, 
                    11: 65535, 12:  65535, 13: 65535, 14: 65535, 15: 65535
                       }
        sig_dic = {0 : False, 1 : True}
        temp = (-1,-1,-1,-1)
        for dr_sig, dr_sts in sig_dic.items():
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1)
            self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrAntiPnch", dr_sig)
            for sigkey, sigvalue in door_dic.items():
                logger.info(f"当前防夹状态.{dr_sts},当前运动状态.{sigkey},当前门开关.{dr_sig}")
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorOpenerDrvrSts", sigkey)
                if sigkey in [11, 12, 13, 14, 15]:
                    if temp !=(dr_sts,0,65535,dr_sts):
                       self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 0}, "sts": 65535, "isAntiPinch": dr_sts}})
                       temp=(dr_sts,0,65535,dr_sts)
                    else:
                       self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts") 
                else:
                   self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 0}, "sts": sigvalue, "isAntiPinch": dr_sts}})
                self.partner.empty_all(0.5)
         
    @allure.title("通知/获取副驾驶电动门开关状态_副驾驶信号值未定义&遍历电动门运动状态&门防夹激活/未激活") #v1.4修复
    @pytest.mark.full
    def test_caseid_1983443(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorOpenerPassSts", 4)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassAntiPnch", 1)
        self.partner.empty_all(1)
        door_dic = {
                    0: 7, 1: 2, 2: 5, 3: 9, 4: 6, 5: 0, 6: 1, 7: 8, 8: 6, 9: 10, 10: 6, 
                    11: 65535, 12:  65535, 13: 65535, 14: 65535, 15: 65535
                       }
        sig_dic = {0 : False, 1 : True}
        for dr_sig, dr_sts in sig_dic.items():
            self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 3)
            self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassAntiPnch", dr_sig)
            for sigkey, sigvalue in door_dic.items():
                logger.info(f"当前防夹状态.{dr_sts},当前运动状态.{sigvalue},当前门开关.{dr_sig}")
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorOpenerPassSts", sigkey)
                if sigkey in [11, 12, 13, 14, 15]:
                    if temp !=(dr_sts,0,65535,dr_sts):  
                       self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 1}, "sts": 65535, "isAntiPinch": dr_sts}})
                       temp=(dr_sts,0,65535,dr_sts)
                    else:
                        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts")                
                else:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 1}, "sts": sigvalue, "isAntiPinch": dr_sts}})
                    temp=(dr_sts,0,sigvalue,dr_sts)
                self.partner.empty_all(0.5)
                   
    @allure.title("通知/获取左后电动门开关状态_左后门信号值未定义&遍历电动门运动状态&门防夹激活/未激活")
    @pytest.mark.full
    def test_caseid_1983452(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 1)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorOpenerLeReSts", 4)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeReAntiPnch", 1)
        self.partner.empty_all(1)
        door_dic = {
                    0: 7, 1: 2, 2: 5, 3: 9, 4: 6, 5: 0, 6: 1, 7: 8, 8: 6, 9: 10, 10: 6, 
                    11: 65535, 12:  65535, 13: 65535, 14: 65535, 15: 65535
                       }
        sig_dic = {0 : False, 1 : True}
        for dr_sig, dr_sts in sig_dic.items():
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 3)
            self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeReAntiPnch", dr_sig)
            for sigkey, sigvalue in door_dic.items():
                logger.info(f"当前防夹状态.{dr_sts},当前运动状态.{sigkey},当前门开关.{dr_sig}")
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorOpenerLeReSts", sigkey)
                if sigkey in [11, 12, 13, 14, 15]:
                    if temp !=(dr_sts,0,65535,dr_sts):
                       self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 1}, "sts": 65535, "isAntiPinch": dr_sts}})
                       temp = (dr_sts,0,65535,dr_sts)
                    else:
                        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts")     
                else:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 1}, "sts": sigvalue, "isAntiPinch": dr_sts}})
                    temp=(dr_sts,0,sigvalue,dr_sts)
                self.partner.empty_all(0.5)
                
    @allure.title("通知/获取右后电动门开关状态_右后门信号值未定义&遍历电动门运动状态&门防夹激活/未激活")
    @pytest.mark.sanity
    def test_caseid_1983456(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 1)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 4)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiReAntiPnch", 1)
        self.partner.empty_all(1)
        door_dic = {
                    0: 7, 1: 2, 2: 5, 3: 9, 4: 6, 5: 0, 6: 1, 7: 8, 8: 6, 9: 10, 10: 6, 
                    11: 65535, 12:  65535, 13: 65535, 14: 65535, 15: 65535
                       }
        sig_dic = {0 : False, 1 : True}
        temp = (-1,-1,-1,-1)
        for dr_sig, dr_sts in sig_dic.items():
            self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 3)
            self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReAntiPnch', dr_sig)
            for sigkey, sigvalue in door_dic.items():
                logger.info(f"当前防夹状态.{dr_sts},当前运动状态.{sigkey},当前门开关.{dr_sig}")
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', sigkey)
                if sigkey in [11, 12, 13, 14, 15]:
                    if temp !=(dr_sts,0,65535,dr_sts):
                        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 1}, "sts": 65535, "isAntiPinch": dr_sts}})
                        temp=(dr_sts,0,65535,dr_sts)
                    else:
                        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts")    
                else:
                    self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts", {"sts":{"openCloseSts":{"isOpen": True, "isOpenValidity": 1}, "sts": sigvalue, "isAntiPinch": dr_sts}})
                    temp=(dr_sts,0,sigvalue,dr_sts)
                self.partner.empty_all(0.5)
  
    @allure.title("通知主驾驶电动门开关状态_主驾驶信号超时或丢失&遍历电动门运动状态&门防夹激活/未激活") #v1.4修复
    @pytest.mark.full
    def test_caseid_1983488(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 2)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorOpenerDrvrSts", 0)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorDrvrAntiPnch", 0)
        sleep(1)
        logger.info(f"开始停发总线*****************************")
        self.ipdu.pause_all_bus_send()
        sleep(1.5)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 4}, "sts": 7, "isAntiPinch": False}}, timeout= 20)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 0}, "sts": 7, "isAntiPinch": False}}, timeout= 20)
        
    @allure.title("通知副驾驶电动门开关状态_副驾驶信号超时或丢失&遍历电动门运动状态&门防夹激活/未激活") #v1.4修复
    @pytest.mark.sanity
    def test_caseid_1983489(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorPassSts', 2)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorOpenerPassSts", 0)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorPassAntiPnch", 0)
        sleep(1)
        logger.info(f"开始停发总线*****************************")
        self.ipdu.pause_all_bus_send()
        sleep(1.5)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 4}, "sts": 7, "isAntiPinch": False}}, timeout= 20)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "FrntRightDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 0}, "sts": 7, "isAntiPinch": False}}, timeout= 20)
    
    @allure.title("通知左后电动门开关状态_左后门信号超时或丢失&遍历电动门运动状态&门防夹激活/未激活") #v1.4修复
    @pytest.mark.full
    def test_caseid_1983490(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorLeReSts', 2)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorOpenerLeReSts", 0)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorLeReAntiPnch", 0)
        sleep(1)
        logger.info(f"开始停发总线*****************************")
        self.ipdu.pause_all_bus_send()
        sleep(1.5)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 4}, "sts": 7, "isAntiPinch": False}}, timeout= 20)
        self.ipdu.resume_all_bus_send()  
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearLeftDoorSts", {"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 0}, "sts": 7, "isAntiPinch": False}}, timeout= 20)
  
    @allure.title("通知右后电动门开关状态_右后门信号超时或丢失&遍历电动门运动状态&门防夹激活/未激活") #v1.4修复
    @pytest.mark.full
    def test_caseid_1983491(self):
        self.ipdu.set(self.ipdu.bodycan.CEMBodyFr11, 'DoorRiReSts', 2)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 0)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorRiReAntiPnch", 0)
        sleep(1)
        logger.info(f"开始停发总线*****************************")
        self.ipdu.pause_all_bus_send()
        sleep(1.5)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts",{"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 4}, "sts": 7, "isAntiPinch": False}}, timeout= 20)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "RearRightDoorSts",{"sts":{"openCloseSts":{"isOpen": False, "isOpenValidity": 0}, "sts": 7, "isAntiPinch": False}}, timeout= 20)    
        
    @allure.title("获取车门按键指示灯状态_all默认值")
    @pytest.mark.full
    def test_caseid_1984511(self):
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, pause_all_bus=True, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetOutDoorSwitchLightSts",{"doors": [4]},
                                                          {"out":[{"id":0, "sts": 0}, 
                                                                  {"id": 1, "sts": 0}, 
                                                                  {"id": 2, "sts": 0}, 
                                                                  {"id": 3, "sts": 0}]}, timeout=2.5)   
        
    @allure.title("通知/获取车门按键指示灯状态_遍历四门信号0-4")
    @pytest.mark.full
    def test_caseid_1987089(self):
        self.sd_tester.write_single_ccp(117, 2)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightPassSwLight', 2)
        self.partner.empty_all(1)
        for light in[3, 2, 0, 1]:
            sleep(0.5)
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightDrvrSwLight', light)
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightPassSwLight', light)
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightLeReSwLight', light)
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightRiReSwLight', light)
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 0, "sts": light}})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 1, "sts": light}})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 2, "sts": light}})
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 3, "sts": light}})
            self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetOutDoorSwitchLightSts",{"doors": [4]},
                                                          {"out":[{"id":0, "sts": light}, 
                                                                  {"id": 1, "sts": light}, 
                                                                  {"id": 2, "sts": light}, 
                                                                  {"id": 3, "sts": light}]}) 
            
    @allure.title("通知/获取车门按键指示灯状态_校验四门信号不同值")
    @pytest.mark.full
    def test_caseid_1987090(self):
        self.sd_tester.write_single_ccp(117, 2)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightPassSwLight', 2)
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightDrvrSwLight', 2)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightPassSwLight', 1)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightLeReSwLight', 3)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightRiReSwLight', 3)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 0, "sts": 2}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 1, "sts": 1}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 2, "sts": 3}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 3, "sts": 3}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetOutDoorSwitchLightSts",{"doors": [4]},
                                                        {"out":[{"id":0, "sts": 2}, 
                                                                {"id": 1, "sts": 1}, 
                                                                {"id": 2, "sts": 3}, 
                                                                {"id": 3, "sts": 3}]}) 
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightDrvrSwLight', 3)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightPassSwLight', 3)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightLeReSwLight', 0)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightRiReSwLight', 0)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 0, "sts": 3}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 1, "sts": 3}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 2, "sts": 0}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 3, "sts": 0}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetOutDoorSwitchLightSts",{"doors": [4]},
                                                        {"out":[{"id":0, "sts": 3}, 
                                                                {"id": 1, "sts": 3}, 
                                                                {"id": 2, "sts": 0}, 
                                                                {"id": 3, "sts": 0}]})
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightDrvrSwLight', 0)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightPassSwLight', 1)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightLeReSwLight', 2)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightRiReSwLight', 3)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 0, "sts": 0}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 1, "sts": 1}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 2, "sts": 2}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 3, "sts": 3}})
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetOutDoorSwitchLightSts",{"doors": [4]},
                                                        {"out":[{"id":0, "sts": 0}, 
                                                                {"id": 1, "sts": 1}, 
                                                                {"id": 2, "sts": 2}, 
                                                                {"id": 3, "sts": 3}]})  
        
    @allure.title("通知/获取车门按键指示灯状态_停总线恢复总线")
    @pytest.mark.full
    def test_caseid_1987094(self):
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightDrvrSwLight', 3)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightPassSwLight', 3)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightLeReSwLight', 3)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr22, 'StatusOfOuterDoorSwLightRiReSwLight', 0)
        self.restart_bgm_and_connect_service(DOOR_SERVICE_CLIENT, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT,"GetOutDoorSwitchLightSts",{"doors": [4]},
                                                        {"out":[{"id":0, "sts": 0}, 
                                                                {"id": 1, "sts": 0}, 
                                                                {"id": 2, "sts": 0}, 
                                                                {"id": 3, "sts": 0}]}, timeout=2)
        self.ipdu.resume_all_bus_send()
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 0, "sts": 3}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 1, "sts": 3}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 2, "sts": 3}})
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "NotifyOutDoorSwitchLightSts", {"info":{"id": 3, "sts": 0}})