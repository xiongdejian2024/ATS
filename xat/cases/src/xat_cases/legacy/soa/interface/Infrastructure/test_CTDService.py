#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_EntryService.py
@Time         :2023/04/30 19:07:31
@Author       :qingxia.ai@jiduauto.com
@Description  :Test SOA for CTDService
"""
import allure
import pytest
from time import sleep
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *

@allure.feature("SOA服务接口")
@allure.story("架构基础/CTDService")
@pytest.mark.aqx
class TestCTDService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("CTDService", "client"),
                                     ("CentralLockService", "client"),
                                     ("DoorService", "client"),
                                     ("TailGateService", "client"),
                                     ("KeyService", "client"),
                                     ("BonnetService", "client")])
        self.partner.method_default_timeout = 0.1
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1) # MPU侧档位
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)  
        self.sd_tester.tester_present()
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4, 142: 0x83,  # 解闭锁相关
                                        64: 3,  # With Alarm Using Vehicle Horn 即siren，警报器
                                        543: 1,  # Without Battery Backed-Up Sounder 即BBS
                                        66: 1,  # Without inclination sensor 即IS倾斜传感器
                                        65: 1,  # Without Interior Motion Sensor 即内部运动传感器
                                        1: 0xA3,  # 适用配置了舒适泊车模式的车型，对应设防准备时间 30s
                                        69: 1,  # Re-trig次数，一个报警周期30s鸣笛停止10s
                                        70: 1,  # 无被动设防
                                        # 13: 4,  # 动力类型Battery electric vehicle，上切Active或Driving可解防
                                        })
        self.partner.empty_all(1)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        self.sd_tester.stop_tester_present()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 0)  #车速值 3=有效  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0) #车速值给了0 输入浮点数
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.io.init_bgm_HW()  # 用例开启始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)
        self.io.hood_door1_close()
        self.io.hood_door2_open()
        self.dk.set_cenlock_sts(0x1)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        self.ipdu.resume_all_bus_send()
        super().after_each_func(ecu, start=False)
        
    @allure.title("车辆设防系统报警状态_启动默认值")
    @pytest.mark.full
    @pytest.mark.restart 
    def test_caseid_1984563(self): 
        self.dk.set_cenlock_sts(0x1)
        sleep(1)
        self.restart_bgm_and_connect_service(CTD_SERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {},
                                              {"out":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}}, timeout=1)        
        self.ipdu.resume_all_bus_send()
        sleep(2)
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",
                                  {"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        
    @pytest.mark.full
    @allure.title("NFC闭锁设防后，30s内打开尾门_车辆解防")
    def test_caseid_1892928(self):
        self.io.trunk_door_close()
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 1)
        self.dk.set_cenlock_sts(0x1) 
        sleep(5)     
        # NFC刷卡闭锁 设防车辆  "sysSts":1,"almSrc":0
        self.dk.send_nfc_cmd()        
        sleep(2)
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {},{"out":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})        
        # 30s内开尾门，解除车辆设防
        self.io.trunk_door_open()
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, 
                                              {"out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}})     
        
    @pytest.mark.full
    @allure.title("设防临时禁用")
    def test_caseid_1919286(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for isDisable in [True,True, False, False]:
            self.partner.send_method_request(CTD_SERVICE_CLIENT,"setTheftDectSwitchSts",{"isDisable":isDisable}) # 设防临时禁用
            sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('PasAlrmDeactvnReq', [1, 1, 0, 0])
        
    @pytest.mark.full
    @allure.title("设防降级控制")
    def test_caseid_1919287(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for isOpenReduce in [True,True, False, False]:    
            self.partner.send_method_request(CTD_SERVICE_CLIENT,"setRedGuardLevSwitchSts",{"isOpenReduce":isOpenReduce}) 
            sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('AntithftRednReq', [1, 1, 0, 0])     
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防30s后解防_Normal+Abandoned+KeyRem闭锁设防+KeyRem解锁解防")
    def test_caseid_1919415(self):
        # 蓝牙闭锁
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_rke_lock() 
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 1},timeout=3) # 解闭锁动作成功触发源         
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(0)
        self.sd_tester.change_car_mode(0)           
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)                   
        sleep(32) # 在30s内 或者在30s外 蓝牙解锁 均解防        
        # 蓝牙解锁 解防
        self.dk.send_rke_unlock() 
        sleep(0.5)
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)      
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防30s后解防_Normal+Abandoned+NFC闭锁设防+Apprch解锁解防")
    def test_caseid_1919414(self):
        # NFC闭锁
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_nfc_cmd()
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 12},timeout=3) # 解闭锁动作成功触发源                      
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(0)
        self.sd_tester.change_car_mode(0)      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)                   
        sleep(32) # 在30s内 或者在30s外 蓝牙解锁 均解防        
        # Approach 靠近解锁和离车闭锁
        self.dk.send_approach_unlock_cmd()
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 9}) 
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)         
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防30s后解防_Normal+Abandoned+OutsOth闭锁设防+IntrSwt闭锁解防")
    def test_caseid_1919413(self):   
        # 外部其他方式闭锁
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {},{"out": 10})                              
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(0)
        self.sd_tester.change_car_mode(0)      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)             
        sleep(32) # 在30s内 或者在30s外 蓝牙解锁 均解防        
        # # 内部其他方式 解锁 也会解防
        # self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 3})
        # self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 11})         
        # 车内的按钮 闭锁
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 3}) 
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
        
    @pytest.mark.smoke
    @allure.title("车辆设防系统报警状态_设防30s后解防_Normal+Abandoned+Telm闭锁设防+上切Active解防")
    def test_caseid_1919412(self):
        # 远程闭锁
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 7},timeout=3)                              
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(0)
        self.sd_tester.change_car_mode(0)      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)           
        sleep(32) # 在30s内 或者在30s外 蓝牙解锁 均解防        
        # 上切Active 
        self.sd_tester.write_single_ccp(13, 4)
        self.sd_tester.change_usage_mode(11)        
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
        
    @pytest.mark.sanity
    @allure.title("车辆设防系统报警状态_设防30s内解防_Normal+Abandoned+TmrAut闭锁设防+左前门开解防")
    def test_caseid_1919411(self):
        # 重上锁
        logger.info("硬线J3-36接地(内部信号HoodSwt1")
        self.io.set_do_level("hood_ajar_2", True)
        sleep(1)
        logger.info("硬线J3-37接地(内部信号HoodSwt2")
        self.io.set_do_level("hood_ajar_1", True)
        sleep(1)
        logger.info("Step:使硬线J3-36悬空")
        self.io.set_do_level("hood_ajar_2", False)
        self.dk.set_cenlock_sts(1)
        self.dk.send_rke_lock()
        sleep(1)
        self.dk.send_rke_unlock()
        sleep(1)    
        # self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        # self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        # self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {}, {"out": {"value": False, "validity": 0}})  #尾门开关状态 false关 true打开
        # self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {"doors": [4]},
        #                                           {"out": [{"value":{"id":0,"isOpen":False},"isOpenValidity":0},
        #                                                    {"value":{"id":1,"isOpen":False},"isOpenValidity":0},
        #                                                    {"value":{"id":2,"isOpen":False},"isOpenValidity":0},
        #                                                    {"value":{"id":3,"isOpen":False},"isOpenValidity":0}]}) # DoorAll false关   
        self.partner.empty_all()
        sleep(35)    
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 5})                              
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(0)
        self.sd_tester.change_car_mode(0)      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)               
        sleep(5) # 在30s内 开门解防        
        # 左前门开 
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', 5)
        sleep(0.5)
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防30s内解防_Normal+Inactive+Keyls闭锁设防+Keyls解锁解防")
    def test_caseid_1919410(self):   
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)         
        # 车外的按钮 上锁
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)]) 
        self.dk.press_door_outswitch(4, 2.2) 
        info0 = {"sts": 3, "triggerId": 2, "updateEve": True}
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info0})
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)            
        sleep(5)         
        # 车外的按钮 解锁 
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 0.5)
        info0 = {"sts": 1, "triggerId": 2, "updateEve": True}
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info0})
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防30s内解防_Normal+Inactive+NFC闭锁设防+NFC解锁解防")
    def test_caseid_1919409(self):
        # NFC闭锁
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_nfc_cmd()
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 12},timeout=3) # 解闭锁动作成功触发源                              
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)             
        sleep(5) # 在30s内 或者在30s外 蓝牙解锁 均解防        
        # NFC 解锁 
        self.dk.send_nfc_cmd()
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 12},timeout=3) # 解闭锁动作成功触发源
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)   
        
    @pytest.mark.smoke
    @allure.title("车辆设防系统报警状态_设防30s内解防_Normal+Inactive+Telm闭锁设防+SpdAut闭锁解防")
    def test_caseid_1919408(self):
        # 远控 闭锁
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 7},timeout=3)                              
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)              
        sleep(5) # 在30s内 或者在30s外 蓝牙解锁 均解防        
        # 车速自动落锁  
        self.sd_tester.change_usage_mode(0xD)
        self.dk.set_drvr_seat_present()
        self.dk.set_four_door_unlock()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 'GenQf1_AccurData')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0x2C27)
        sleep(0.5)
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防30s内解防_Normal+Inactive+KeyRem闭锁设防+InsOth闭锁解防")
    def test_caseid_1919407(self):
        # 蓝牙 闭锁
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_rke_lock() 
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 1},timeout=3) # 解闭锁动作成功触发源                              
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)              
        sleep(5) # 在30s内 或者在30s外 蓝牙解锁 均解防        
        # 内部其他方式 闭锁 
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 11}) 
        sleep(0.5)
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
        
    @pytest.mark.smoke
    @allure.title("车辆设防系统报警状态_设防30s内解防_Normal+Inactive+Apprch闭锁设防+上切Driving解防")
    def test_caseid_1919406(self):
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_walk_away_lock_cmd() # Approach 离车闭锁
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 9})                               
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(0)      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)                
        sleep(5)         
        # 上切 Driving
        self.sd_tester.write_single_ccp(13, 4)
        self.sd_tester.change_usage_mode(13)
        sleep(0.5)
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
                
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防30s内解防_Dyno+Abandoned+TmrAut闭锁设防+前舱盖打开解防")
    def test_caseid_1919405(self):
        # 重上锁
        logger.info("硬线J3-36接地(内部信号HoodSwt1")
        self.io.set_do_level("hood_ajar_2", True)
        sleep(1)
        logger.info("硬线J3-37接地(内部信号HoodSwt2)")
        self.io.set_do_level("hood_ajar_1", True)
        sleep(1)
        logger.info("Step:使硬线J3-36悬空")
        self.io.set_do_level("hood_ajar_2", False)
        self.dk.set_cenlock_sts(1)
        self.dk.send_rke_lock()
        sleep(1)
        self.dk.send_rke_unlock()
        sleep(1)    
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {}, {"out": {"value": False, "validity": 0}})  #尾门开关状态 false关 true打开
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {"doors": [4]},
                                                  {"out": [{"value":{"id":0,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":1,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":2,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":3,"isOpen":False},"isOpenValidity":0}]}) # DoorAll false关   
        self.partner.empty_all()
        sleep(35)    
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 5})                              
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(5)      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)            
        sleep(5) # 30s内         
        # 前舱盖打开
        # 硬线接地
        self.io.hood_door1_open()
        self.io.hood_door2_open()
        # 确认总线收到backbonefr,HoodSts=1opened
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "HoodSts", "DoorSts2_Opend")
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防30s内解防_Dyno+Inactive+Telm闭锁设防+右前门打开解防")
    def test_caseid_1919404(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        # 远程闭锁
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 7},timeout=3)        
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(1)
        self.sd_tester.change_car_mode(5)      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)                     
        sleep(5) # 在30s内 开门解防        
        # 右前门开 
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorOpenerPassSts', 5)
        sleep(0.5)
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防30s内解防_Crash+Abandoned+NFC闭锁设防+Telm解锁解防")
    def test_caseid_1919403(self):  
        self.dk.set_cenlock_sts(1)
        # UsgMod CarMod
        self.sd_tester.change_car_mode(3) 
        self.sd_tester.change_usage_mode(0)
        self.partner.empty_all(10) 
        # NFC闭锁
        self.dk.send_nfc_cmd()
        sleep(1)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 12}) 
        # 设防 
        # self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)               
        sleep(5) # 在30s内或30s外        
        # 远程解锁
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 1})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 7},timeout=3)        
        # 解防 
        # self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
            "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)     
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防30s内解防_Crash+Abandoned+OutsOth闭锁设防+右后门打开解防")    
    def test_caseid_1919402(self):
        self.dk.set_cenlock_sts(1)
        # UsgMod CarMod
        self.sd_tester.change_car_mode(3) 
        self.sd_tester.change_usage_mode(0)  
        # self.dk.set_cenlock_sts(1)
        self.partner.empty_all(10)
        # 外部其他方式闭锁
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3})
        sleep(1)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {},{"out": 10},timeout=3)
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)                
        sleep(5) # 在30s内或30s外        
        # 右后门开 
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 1)
        sleep(0.5)        
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
 
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防30s内解防_Crash+Inactive+Apprch闭锁设防+尾门打开解防")
    def test_caseid_1919401(self):
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_walk_away_lock_cmd() # Approach 离车闭锁
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 9})         
        # UsgMod CarMod
        self.sd_tester.change_car_mode(3) 
        self.sd_tester.change_usage_mode(1)  
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)                 
        sleep(10) # 在30s内        
        # 30s内开尾门，解除车辆设防
        self.io.trunk_door_open()
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
        sleep(0.5)
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)    
        
    @pytest.mark.sanity
    @allure.title("车辆设防系统报警状态_设防并激活报警后解防_Normal+Abandoned+Keyls闭锁设防_前舱盖打开报警_KeyRem解锁解防")
    def test_caseid_1919400(self):
        # 车外的按钮 上锁
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)]) 
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 2.2) 
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 2},timeout=3)        
        # UsgMod CarMod
        self.sd_tester.change_car_mode(0) 
        self.sd_tester.change_usage_mode(0)  
        # 设防 
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)                      
        sleep(30.5)         
        # 前舱盖打开
        self.io.hood_door1_open()
        self.io.hood_door2_open()
        # 确认总线收到backbonefr,HoodSts=1opened
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "HoodSts", "DoorSts2_Opend")
        #触发防盗
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":2,"almSrc":4,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 2, "almSrc": 4, "senFault": False, "intrScanFault": False}},timeout=3)        
        sleep(2)
        # KeyRem解锁
        self.dk.send_rke_unlock() 
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 1},timeout=3) # 解闭锁动作成功触发源
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
        
    @pytest.mark.sanity
    @allure.title("车辆设防系统报警状态_设防并激活报警后解防_Normal+Abandoned+Apprch闭锁设防_左前门打开报警_IntrSwt解锁解防")
    def test_caseid_1978187(self): 
        # UsgMod CarMod
        self.sd_tester.change_car_mode(0) 
        self.sd_tester.change_usage_mode(0)        
        self.partner.send_method_request("KeyService_client", "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_walk_away_lock_cmd() # Approach 离车闭锁
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 9})      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)    
        sleep(30.5)          
        # 左前门开 
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', 5)
        sleep(0.5)
        #触发防盗
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":2,"almSrc":6,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 2, "almSrc": 6, "senFault": False, "intrScanFault": False}},timeout=3)                  
        sleep(5) 
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', 1)
        # 车内的按钮 闭锁
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        sleep(1)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 3})
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)           
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防并激活报警后解防_Normal+Inactive+TmrAut闭锁设防_右前门打开报警_上切Factory解防")
    def test_caseid_1919398(self):    
        # 重上锁
        logger.info("硬线J3-36接地(内部信号HoodSwt1")
        self.io.set_do_level("hood_ajar_2", True)
        sleep(1)
        logger.info("硬线J3-37接地(内部信号HoodSwt2)")
        self.io.set_do_level("hood_ajar_1", True)
        sleep(1)
        logger.info("Step:使硬线J3-36悬空")
        self.io.set_do_level("hood_ajar_2", False)
        self.dk.set_cenlock_sts(1)
        self.dk.send_rke_lock()
        sleep(1)
        self.dk.send_rke_unlock()
        sleep(1)    
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {}, {"out": {"value": False, "validity": 0}})  #尾门开关状态 false关 true打开
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {"doors": [4]},
                                                  {"out": [{"value":{"id":0,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":1,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":2,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":3,"isOpen":False},"isOpenValidity":0}]}) # DoorAll false关   
        self.partner.empty_all()
        sleep(30.5)     
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 5})      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, { "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)       
        sleep(35)        
        # 右前门开 
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorOpenerPassSts', 1)
        sleep(0.5)
        #触发防盗
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":2,"almSrc":7,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 2, "almSrc": 7, "senFault": False, "intrScanFault": False}},timeout=3)             
        # UsgMod CarMod
        # self.sd_tester.change_car_mode(2)  # alarm下不可以通过诊断切写 见SOA-9649
        # # 解防 
        # self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        # self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
        #         "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt',0)
        # self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmTrgSrc',0)         
          
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防并激活报警后解防_Normal+Inactive+OutsOth闭锁设防_左后门打开报警_上切Active解防")
    def test_caseid_1919397(self):  
        # 外部其他方式闭锁
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {},{"out": 10},timeout=3)     
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)     
        sleep(30.5)           
        # 右前门开 
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorOpenerLeReSts', 5)
        sleep(0.5)
        #触发防盗
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":2,"almSrc":8,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 2, "almSrc": 8, "senFault": False, "intrScanFault": False}},timeout=3)                
        sleep(5) 
        # UsgMod CarMod
        self.sd_tester.change_usage_mode(11) 
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)    
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防并激活报警后解防_Dyno+Abandoned+KeyRem闭锁设防_右后门打开报警_InsOth闭锁解防")
    def test_caseid_1919396(self): 
        # UsgMod CarMod
        self.sd_tester.change_car_mode(5) 
        self.sd_tester.change_usage_mode(0)        
        # 蓝牙闭锁
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_rke_lock() 
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 1},timeout=3) # 解闭锁动作成功触发源     
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)    
        sleep(30.5)    
        # 右后门开 
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 5)
        sleep(0.5)
        #触发防盗
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":2,"almSrc":9,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 2, "almSrc": 9, "senFault": False, "intrScanFault": False}},timeout=3)                
        sleep(5)     
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 1)
        # 内部其他方式 闭锁 
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 11})
        # 解防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":0,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 0, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)
        
    @pytest.mark.full
    @allure.title("车辆设防系统报警状态_设防并激活报警后解防_Dyno+Abandoned+Telm闭锁设防_尾门打开报警")
    def test_caseid_1919395(self): 
        # UsgMod CarMod
        self.sd_tester.change_car_mode(5) 
        self.sd_tester.change_usage_mode(0)       
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        # 远程闭锁
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 7},timeout=3)      
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)       
        sleep(30.5)    
        # 尾门开 
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 5)
        sleep(0.5)
        #触发防盗
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":2,"almSrc":5,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 2, "almSrc": 5, "senFault": False, "intrScanFault": False}},timeout=3)                            
        
    @pytest.mark.sanity
    @allure.title("车辆设防系统报警状态_设防并报警至报警周期结束_Dyno+Inactive+KeyRem闭锁设防_右后门打开报警_右后门关闭触发源保持不变")
    def test_caseid_1919394(self):
        # UsgMod CarMod
        self.sd_tester.change_car_mode(5) 
        self.sd_tester.change_usage_mode(1)        
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        # 蓝牙闭锁
        self.dk.send_rke_lock() 
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 1},timeout=3) # 解闭锁动作成功触发源     
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)      
        sleep(30)        
        # 右后门开 
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorOpenerRiReSts', 5)
        sleep(0.5)
        #触发防盗
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":2,"almSrc":9,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 2, "almSrc": 9, "senFault": False, "intrScanFault": False}},timeout=3)                 
        sleep(2)     
        # 仅改变门状态不会对触发源信号有影响    
        self.dk.set_door_sts([0, 0, 0, 0, 0]) 
        self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmTrgSrc',9)          
        # 报警周期结束后，触发源不会自动归-0，但是状态会进入设防状态
        sleep(285)
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":9,"senFault":False,"intrScanFault":False}},timeout=10)
        self.partner.empty_all()
        # 检测不会再次进入告警状态
        self.partner.ck_no_event(CTD_SERVICE_CLIENT,"alarmInfo",timeout=10)              
         
    @pytest.mark.sanity
    @allure.title("车辆设防系统报警状态_报警触发源改变_Dyno+Inactive+NFC闭锁设防_四门两盖按顺序打开")
    def test_caseid_1919393(self):
        # UsgMod CarMod
        self.sd_tester.change_car_mode(5) 
        self.sd_tester.change_usage_mode(1)        
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        # 蓝牙闭锁
        self.dk.send_nfc_cmd() 
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {}, {"out": 12},timeout=3) # 解闭锁动作成功触发源 
        # 设防 
        self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":1,"almSrc":0,"senFault":False,"intrScanFault":False}})
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
            "out": {"sysFault": False, "sysSts": 1, "almSrc": 0, "senFault": False, "intrScanFault": False}},timeout=3)          
        sleep(30.5)       
        list1=[0, 0, 0, 0, 0]
        almsrc=[6,7,8,9,5]
        for i in range(5):
            list1[i]=1
            self.dk.set_door_sts(list1)
            sleep(2)
            self.partner.ck_s2s_event(CTD_SERVICE_CLIENT,"alarmInfo",{"info":{"sysFault":False,"sysSts":2,"almSrc":almsrc[i],"senFault":False,"intrScanFault":False}})
            self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {}, {
                "out": {"sysFault": False, "sysSts": 2, "almSrc": almsrc[i], "senFault": False, "intrScanFault": False}},timeout=3)     
            sleep(35)  # 为了等待报警的30s结束
            self.partner.empty_all()

######################################################################################################################################################## 
@allure.feature("SOA服务接口")
@allure.story("架构基础/CTDService")
@pytest.mark.aqx   
class TestCTDServiceMockMcu(TestBase):            
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("CTDService", "client")])

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

    @pytest.mark.sanity
    @allure.title("车辆设防系统报警状态_MockMCU遍历信号值")
    def test_caseid_1919392(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt', 2) 
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmTrgSrc',4)  
        self.partner.send_request_and_ck_resp(CTD_SERVICE_CLIENT, "getAlarmInfo", {},  
                                              {"out":{"sysFault":False,"sysSts":2,"almSrc":4,"senFault":False,"intrScanFault":False}}, timeout=5)  
        self.partner.empty_all(1)
        last_sysSts, last_trgsrc=2, 4
        for sts in range(4):
            for trgsrc in range(16):
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmSt', sts) 
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr18, 'AlrmStsAlrmTrgSrc', trgsrc)  
                cur_sysSts=sts if sts in range(3) else 2
                cur_trgsrc=trgsrc if trgsrc in range(11) else 10
                sleep(2)
                if cur_sysSts != last_sysSts or cur_trgsrc != last_trgsrc:
                    self.partner.ck_event_and_resp(CTD_SERVICE_CLIENT, "alarmInfo", 
                                                   {"info": {"sysFault":False,"sysSts":cur_sysSts ,"almSrc":cur_trgsrc,"senFault":False,"intrScanFault":False}}, method_name="getAlarmInfo")
                else:
                    self.partner.ck_no_event_and_ck_resp(CTD_SERVICE_CLIENT, "alarmInfo", 
                                             {"out": {"sysFault":False,"sysSts":cur_sysSts ,"almSrc":cur_trgsrc,"senFault":False,"intrScanFault":False}}, method_name="getAlarmInfo", timeout=2)
                last_sysSts, last_trgsrc=cur_sysSts, cur_trgsrc