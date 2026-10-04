#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_EntryService.py
@Time         :2023/04/30 19:07:31
@Author       :qingxia.ai@jiduauto.com
@Description  :
"""
import allure
import pytest
from threading import Thread
from time import sleep
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.sdk.digital_key.digital_key_class import *
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.interface.bgm.bgm_ssh import *
from xat_ecu.legacy.sdk.sdk_tools import *
from collections import Counter
Times=1


@allure.feature("SOA服务接口")
@allure.story("BGM应用/EntryService")
@pytest.mark.aqx
class TestEntryService(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("EntryService", "client"),
                                     ("CentralLockService", "client"),
                                     ("KeyService", "client"),
                                     ("AVPService", "server"),
                                     ("ChassisService", "client"),
                                     ("RPAAPAService", "server"),
                                     ("HornService", "client"),
                                     ("DoorService", "client"),
                                     ("PedalService", "client"),
                                     ("BonnetService", "client"),
                                     ("TailGateService", "client"),
                                     ("CTDService", "client"),
                                     ("SeatService", "client")
                                     ])
        self.partner.method_default_timeout = 0.1
        self.io.hood_door1_close()
        self.io.hood_door2_close()
        #抓取tcpdump
        self.bgm_tcpdump = BGM_SSH()
        self.bgm_tcpdump.init_bgm_tcpdump()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
        self.ipdu.rx_flag_reset_all()
        self.ipdu.reset_check_results()
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')        
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropComFr10, 'TrsmParkLockdTrsmParkLockd', 1)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr24, 'GearLvrIndcn', 0)        
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4, 142: 0x83})
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]})
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]}) # 开启离车关四门配置
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.sd_tester.change_car_mode(0)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.io.io_obj.set_do_level("horn_switch", False) # 喇叭关闭
        self.partner.empty_all(2)
        self.dk.empty_dk_data_queue()

    def after_each_func(self, ecu):  
        self.flag=False
        self.ipdu.resume_all_bus_send()
        door=["Drvr", "Pass", "LeRe", "RiRe"]
        for i in range(4):
            self.set_door_fault(door[i])    
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 2) # 消除 童锁错误
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr02, 'ChdLockRightFailStsToHmi', 2) # 消除 童锁错误
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 'NoYes1_No')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 0)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 0) 
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReAntiPnch', 0) 
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReAntiPnch', 0) 
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyTyp', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo1KeyConnectSts', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo2KeyTyp', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo2KeyConnectSts', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19, 'DigKeyConnectInfo3KeyTyp', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19,'DigKeyConnectInfo3KeyConnectSts', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19, 'DigKeyConnectInfo4KeyTyp', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19,'DigKeyConnectInfo4KeyConnectSts', 0)
        sleep(2) 
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(3)  # 避免防玩
        super().after_each_func(ecu, start=False)

    # def set_nopeople_incar(self):
    #     self.io.drvr_door_open()
    #     self.io.driver_seat_notpresent()
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', 0)
    #     self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', 0)
    #     self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetVehicleInsidePersonSts", {},
    #                                         {"out":{"userInVehicleStatus":False}},timeout = 3.5)                                     
    #     self.io.drvr_door_close()
        
    def bgm_sleep_and_awake(self):
        pass  # todo

    def set_BrakeCloseDoorInhibit(self):
        while self.flag:
            self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": True}, timeout=2)
            sleep(1)
        
    def set_door_fault(self, door, fault=[0, 0, 0, 0, 0], sleep_time=0):          
        for i in range(5):
            if door == "Drvr": 
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, f'DtcInfDoorDrvrBoolean{i+1}', fault[i])
            elif door == "Pass":
                self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, f'DtcInfDoorPassBoolean{i+1}', fault[i])
            elif door == "LeRe":
                self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, f'DtcInfDoorLeReBoolean{i+1}', fault[i])
            elif door == "RiRe":
                self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, f'DtcInfDoorRiReBoolean{i+1}', fault[i])
        sleep(sleep_time) 
        
    def setPercPosn(self, posn=[0, 0, 0, 0]):
        '''设置当前车门位置'''
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPercPosn', posn[0])        
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassPercPosn', posn[1])
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeRePercPosn', posn[2])
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiRePercPosn', posn[3])

    def ck_EntrySystemAudioLightInfo(self, audio, light, timeout=2.0):
        """校验进入系统声光提醒信息"""
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo", {"info": {"audio": audio, "light": light}}, timeout)
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo", {"info": {"audio": 0, "light": 0}}, timeout)
        self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetEntrySystemAudioLightInfo", {}, {"out": {"audio": 0, "light": 0}})
 
    def ck_NotifyLockWarning(self, lock=None, Reminder=None, ck_horn=True, timeout=3.0):
        """校验进入系统的报警信息"""
        if ck_horn:
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 0})  # todo: 之后切换io输出校验
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 1})
        else:
            self.partner.ck_no_event("HornService_client", "Status")
        if lock is None and Reminder is None:
            self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout)
        else:
            self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", {"warnnings": {"lock": lock, "reminder": Reminder}}, timeout)
            if lock != 0 or Reminder != 0:
            # 通知完成后将提示请求置为IDLE     
                self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", {"warnnings": {"lock": 0, "reminder": 0}})
                self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetLockWarning", {}, {"out": {"lock": 0, "reminder": 0}})    

    def ck_horn(self, ck_horn=True, timeout=3.0):
        if ck_horn:
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 0})  # todo: 之后切换io输出校验
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 1})
        else:
            self.partner.ck_no_event("HornService_client", "Status")
                        
    def ck_pdu(self,file_path,save_name,data_list1,data_list2):
        # todo 停止抓包
        self.bgm_tcpdump.stop_bgm_tcpdump()
        # todo 拉取日志 单个日志 不打包
        file_path=self.bgm_tcpdump.scp_bgm_log_to_local(bgm_log_name=save_name)
        # todo 删除所有 pcap 文件
        self.bgm_tcpdump.delete_bgm_tcpdump_file(bgm_log_name='*.pcap')
        
        #停止和删除 也在aftercase中增加进去
        # 列表里面为元祖（pdu的id，数据长度，信号起始bit位，信号长度，信号值），可以 是多个元祖
        # data_list = [list1]
        ret, res_dict = check_pdu(data_list1, file_path)            
        
        # data_list 格式 为列表，列表里面为元祖（pdu的id，数据长度，信号起始bit未，信号长度），可以 是多个元祖
        # data_list = [list2]  
        res_dict=get_pdu_value_and_time(data_list2, file_path)
        if ret==False :
             assert False, f"对应信号不存在"
             
    def ck_LockActTriggerSource(self, src_id, timeout=1.0):
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockActTriggerSource", {"sourceId": src_id}, timeout)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockActTriggerSource", {},
                                              {"out": src_id})

    def ck_CentralLockStatusInfo(self, lock_sts, trigger_srcid, timeout=1):
        info1 = {"sts": lock_sts, "triggerId": trigger_srcid, "updateEve": True}
        info0 = {"sts": lock_sts, "triggerId": trigger_srcid, "updateEve": False}
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info1}, timeout)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info1})

        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "NotifyCentralLockSysInfo", {"info": info0}, timeout=1.5)
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetCentralLockSysInfo", {}, {"out": info0})
    
    @allure.title("闭锁状态告警_离车闭锁&&存在非主驾门未关_不触发lock=7") 
    @pytest.mark.full
    def test_caseid_1984597(self): # 140AV变更 见SOA-21267
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd() 
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout=3) # 确认不会触发场景1，lock=7
      
    @allure.title("闭锁状态告警_PE长按_主驾门防夹")
    @pytest.mark.smoke
    def test_caseid_1983916(self):  # V140
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.empty_all(1)
        self.dk.press_door_outswitch(1, 2.51)
        sleep(5.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 1) # 主驾门防夹
        self.ck_NotifyLockWarning(9, 0)      
        
    @allure.title("闭锁状态告警_PE长按_副驾门防夹")
    @pytest.mark.full    
    def test_caseid_1983917(self): 
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.empty_all(1)
        self.dk.press_door_outswitch(2, 2.51)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 1) # 副驾门防夹
        self.ck_NotifyLockWarning(9, 0)  
        
    @allure.title("闭锁状态告警_PE长按_副驾门防夹_触发两次防夹")
    @pytest.mark.full    
    def test_caseid_1987650(self): 
        self.dk.set_cenlock_sts(1)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.set_door_sts([1, 1, 0, 0, 0])
        self.dk.press_door_outswitch(2, 2.51)
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 1) # 副驾门防夹
        self.ck_NotifyLockWarning(9, 0)  
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 1) # 主驾门防夹
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout=4)
        self.partner.ck_no_event(HORN_SERVICE_CLIENT, "Status")
        
    @allure.title("闭锁状态告警_PE长按_左后门防夹")
    @pytest.mark.full
    def test_caseid_1983918(self):  # V140
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.empty_all(0.5)
        self.dk.press_door_outswitch(3, 2.51)
        sleep(5.5)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReAntiPnch', 1) # 左后门防夹
        self.ck_NotifyLockWarning(9, 0)    
        
    @allure.title("闭锁状态告警_PE长按_右后门防夹")
    @pytest.mark.full
    def test_caseid_1983919(self): 
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.empty_all(0.5)
        self.dk.press_door_outswitch(4, 2.51)
        sleep(5.5)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReAntiPnch', 1) # 右后门防夹
        self.ck_NotifyLockWarning(9, 0)    
        
    @allure.title("闭锁状态告警_PE长按_尾门防夹")
    @pytest.mark.sanity
    def test_caseid_1983920(self): 
        self.dk.set_cenlock_sts(1)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.empty_all(0.5)
        self.dk.press_door_outswitch(1, 2.51)
        sleep(5.5)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 1) # 尾门防夹
        self.ck_NotifyLockWarning(9, 0)   
        
    @allure.title("闭锁状态告警_PE长按_未发生防夹且五门关闭成功")
    @pytest.mark.full
    def test_caseid_1983921(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(1, 2.51)
        self.partner.empty_all(3)
        sleep(2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning")           

    @allure.title("闭锁状态告警_PE长按_计时时间内检测到尾门跳变至Opening")
    @pytest.mark.sanity
    def test_caseid_1983923(self): # 140BA
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.dk.press_door_outswitch(1, 2.51)       
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 2)
        self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT, "Status", {"sts":3})
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 1) # 尾门防夹
        self.ck_NotifyLockWarning(9, 0)  
        
    @allure.title("闭锁状态告警_PE长按_计时时间内检测到尾门跳变至OpeningBreak")
    @pytest.mark.full
    def test_caseid_1983924(self): # 140BA
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(1, 2.51)      
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 3)
        self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT, "Status", {"sts":7})
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 1) # 尾门防夹
        self.ck_NotifyLockWarning(9, 0)  
        
    @allure.title("闭锁状态告警_PE长按_计时时间内检测到电动门跳变至Opening")
    @pytest.mark.full
    def test_caseid_1983925(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(2, 2.51)      
        self.partner.empty_all(3)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorOpenerPassSts", 2) # 清空计时器
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 1) # 副驾门防夹
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout=2)     
        
    @allure.title("闭锁状态告警_PE长按_计时时间内检测到电动门跳变至OpeningBreak")
    @pytest.mark.full
    def test_caseid_1983927(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(4, 2.51) 
        self.partner.empty_all(3)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorOpenerRiReSts", 3) # 清空计时器
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReAntiPnch', 1) # 右后门防夹
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout=2)            
        
    @allure.title("闭锁状态告警_NFC长刷_尾门防夹")
    @pytest.mark.full
    def test_caseid_1983906(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected') 
        sleep(0.5)
        self.dk.send_nfc_cmd()
        sleep(2.1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected') 
        sleep(5.5)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 1) # 尾门防夹
        self.ck_NotifyLockWarning(9, 0)  
        
    @allure.title("闭锁状态告警_NFC长刷_主驾门防夹")
    @pytest.mark.sanity
    def test_caseid_1983907(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(0.5)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected') 
        sleep(0.5)
        self.dk.send_nfc_cmd()
        sleep(2.1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected') 
        sleep(5.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 1) # 主驾门防夹
        self.ck_NotifyLockWarning(9, 0)     
        
    @allure.title("闭锁状态告警_NFC长刷_副驾门防夹")
    @pytest.mark.full    
    def test_caseid_1983908(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        sleep(1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected') 
        sleep(0.5)
        self.dk.send_nfc_cmd()
        sleep(2.1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected') 
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 1) # 副驾门防夹
        self.ck_NotifyLockWarning(9, 0)   

    @allure.title("闭锁状态告警_NFC长刷_左后门防夹")
    @pytest.mark.smoke
    def test_caseid_1983909(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected') 
        sleep(0.5)
        self.dk.send_nfc_cmd()
        sleep(2.3)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected') 
        sleep(5.5)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReAntiPnch', 1) # 左后门防夹
        self.ck_NotifyLockWarning(9, 0)     
        
    @allure.title("闭锁状态告警_NFC长刷_右后门防夹")
    @pytest.mark.full
    def test_caseid_1983910(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected') 
        sleep(0.5)
        self.dk.send_nfc_cmd()
        sleep(2.1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected') 
        sleep(5.5)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReAntiPnch', 1) # 右后门防夹
        self.ck_NotifyLockWarning(9, 0)    
        
    @allure.title("闭锁状态告警_NFC长刷_未发生防夹且五门关闭成功")
    @pytest.mark.full
    def test_caseid_1983911(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected') 
        sleep(0.5)
        self.dk.send_nfc_cmd()
        sleep(2.1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected') 
        self.partner.empty_all(3)
        sleep(2)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning")
        
    @allure.title("闭锁状态告警_NFC长刷_计时时间内检测到尾门跳变至Opening")
    @pytest.mark.full
    def test_caseid_1983912(self): # 140BA
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected') 
        sleep(0.5)
        self.dk.send_nfc_cmd()
        sleep(2.1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected') 
        self.partner.empty_all(3)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 2) # 不清除计时
        self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT, "Status", {"sts":3})
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 1) # 尾门防夹
        self.ck_NotifyLockWarning(9, 0)    

    @allure.title("闭锁状态告警_NFC长刷_计时时间内检测到尾门跳变至OpeningBreak")
    @pytest.mark.full
    def test_caseid_1983913(self): # 140BA
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected') 
        sleep(0.5)
        self.dk.send_nfc_cmd()
        sleep(2.1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected') 
        self.partner.empty_all(3)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrOpenerSts', 3) # 不清除计时
        self.partner.ck_s2s_event(TAILGATE_SERVICE_CLIENT, "Status", {"sts":7})
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 1) # 尾门防夹
        self.ck_NotifyLockWarning(9, 0)   
        
    @allure.title("闭锁状态告警_NFC长刷_计时时间内检测到电动门跳变至Opening")
    @pytest.mark.sanity
    def test_caseid_1983914(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected') 
        sleep(0.5)
        self.dk.send_nfc_cmd()
        sleep(2.1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected') 
        self.partner.empty_all(3)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, "DoorOpenerDrvrSts", 2)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout=2)

    @allure.title("闭锁状态告警_NFC长刷_计时时间内检测到电动门跳变至OpeningBreak")
    @pytest.mark.full
    def test_caseid_1983915(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected') 
        sleep(0.5)
        self.dk.send_nfc_cmd()
        sleep(2.1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected') 
        self.partner.empty_all(3)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorOpenerLeReSts", 3)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReAntiPnch', 'Boolean_TRUE')
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout=2)

    @allure.title("闭锁状态告警_NFC长刷_主驾门7s后触发防夹")
    @pytest.mark.full
    def test_caseid_1980150(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected')
        sleep(0.5)
        self.dk.send_nfc_cmd()
        self.partner.empty_all(2.1)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected')
        sleep(7)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_NotifyLockWarning(ck_horn=False)       

    @allure.title("闭锁状态告警_PE长按_主驾门7s后触发防夹")
    @pytest.mark.full
    def test_caseid_1980151(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(1, 2.51)
        self.partner.empty_all(0.5)
        sleep(6.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_NotifyLockWarning(ck_horn=False)     

    @allure.title("闭锁状态告警_NFC短刷锁车_车内有有效钥匙")
    @allure.testcase('test_caseid_1959993')
    @pytest.mark.sanity
    def test_caseid_1959993(self): 
        # todo 开始抓包 　
        file_path, save_name = self.bgm_tcpdump.start_bgm_tcpdump() 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])  
        sleep(0.1)
        self.dk.send_nfc_cmd() 
        self.ck_NotifyLockWarning(10, 0, ck_horn=False,timeout=3)     
        # 检验TCP报文 # 列表里面为元祖（pdu的id，数据长度，信号起始bit位，信号长度，信号值），可以 是多个元祖
        data_list1 = [(15017, 1, 2, 3, 4),(15017, 1, 2, 3, 0)]
        data_list2 = [(15017, 1, 2, 3)]
        result1=self.ipdu.check_signal(self.ipdu.connectivitycanfd.BgmConnectivityFr15,
                        'ReminderWhileLock', timeout=1, do_print=True)
        logger.info(f"当前结果为：{result1}")
        sleep(5)
        self.ck_pdu(file_path,save_name,data_list1,data_list2)          

    @allure.title("闭锁状态告警_NFC长刷锁车_车内有有效钥匙")
    @pytest.mark.sanity
    def test_caseid_1959984(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected')
        sleep(0.1)
        self.dk.send_nfc_cmd()
        sleep(2.2)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected')
        self.ck_NotifyLockWarning(10, 0, ck_horn=False)

    @allure.title("闭锁状态告警_NFC短刷_主驾门开")
    @pytest.mark.sanity
    def test_caseid_1959985(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.dk.send_nfc_cmd()
        self.ck_NotifyLockWarning(1, 0, ck_horn=False)             

    @allure.title("闭锁状态告警_NFC短刷_副驾门开")
    @allure.testcase('test_caseid_1959986')
    @pytest.mark.full
    def test_caseid_1959986(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.dk.send_nfc_cmd()
        self.ck_NotifyLockWarning(1, 0, ck_horn=False)  
            
    @allure.title("闭锁状态告警_NFC短刷_左后门开")
    @allure.testcase('test_caseid_1959987')
    @pytest.mark.full
    def test_caseid_1959987(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.dk.send_nfc_cmd()
        self.ck_NotifyLockWarning(1, 0, ck_horn=False)   

    @allure.title("闭锁状态告警_NFC短刷_右后门开")
    @allure.testcase('test_caseid_1959988')
    @pytest.mark.full
    def test_caseid_1959988(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.dk.send_nfc_cmd()
        self.ck_NotifyLockWarning(1, 0, ck_horn=False) 
            
    @allure.title("闭锁状态告警_NFC短刷_尾门开")
    @allure.testcase('test_caseid_1959989')
    @pytest.mark.full
    def test_caseid_1959989(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.dk.send_nfc_cmd()
        self.ck_NotifyLockWarning(1, 0, ck_horn=False)       
 
    @allure.title("解锁失败告警_车内左前按钮解锁_lock=11")
    @pytest.mark.smoke
    def test_caseid_1959973(self): 
        self.dk.set_cenlock_sts(1)  
        self.partner.empty_all(1)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15") # 清空当前信号的值
        # ChassisService::VehicleMotionState 参数：0=未知无效值 1=静止 2=前进 3=后退  信号值：0=0，1/2/3=1，4/5=2，6/7=3
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 0)
        sleep(1)
        self.dk.press_door_inswitch(1, 0.5)
        self.ck_NotifyLockWarning(11, 0, ck_horn=False)

    @allure.title("解锁失败告警_车内右前按钮解锁_lock=11")
    @pytest.mark.full
    def test_caseid_1959975(self): 
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all(1)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 4)
        sleep(1)
        self.dk.press_door_inswitch(2, 0.5)
        self.ck_NotifyLockWarning(11, 0, ck_horn=False)        

    @allure.title("解锁失败告警_车内左后按钮解锁_lock=11")
    @pytest.mark.full
    def test_caseid_1959974(self):       
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 6)
        sleep(1)
        self.dk.press_door_inswitch(3, 0.5)
        self.ck_NotifyLockWarning(11, 0, ck_horn=False)

    @allure.title("解锁失败告警_车内右后按钮解锁_lock=11")
    @pytest.mark.sanity
    def test_caseid_1959976(self): 
        self.dk.set_cenlock_sts(3) 
        self.partner.empty_all(1)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 7)
        sleep(1)
        self.dk.press_door_inswitch(4, 0.5)
        self.ck_NotifyLockWarning(11, 0, ck_horn=False)
                
    @allure.title("关门提示_主驾门开&故障遍历_无车外提示")
    @pytest.mark.sanity
    def test_caseid_1980369(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([1, 0, 0, 0, 0])  
        for j in range(5):
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.set_door_fault("Drvr", door_fault, sleep_time=2)
            self.dk.send_rke_close_door_and_lock()
            self.ck_NotifyLockWarning(ck_horn=False)
            
    @allure.title("关门提示_副驾门开&故障遍历_无车外提示")
    @allure.testcase('test_caseid_1980370')
    @pytest.mark.full
    def test_caseid_1980370(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 1, 0, 0, 0]) 
        for j in range(5):
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.set_door_fault("Pass", door_fault, sleep_time=2)
            self.dk.send_rke_close_door_and_lock()
            self.ck_NotifyLockWarning(ck_horn=False)
            
    @allure.title("关门提示_左后门开&故障遍历_无车外提示")
    @allure.testcase('test_caseid_1980371')
    @pytest.mark.full
    def test_caseid_1980371(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 0, 1, 0, 0])  
        for j in range(5):
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.set_door_fault("LeRe", door_fault, sleep_time=2)
            self.dk.send_rke_close_door_and_lock()
            self.ck_NotifyLockWarning(ck_horn=False)
            
    @allure.title("关门提示_右后门开&故障遍历_无车外提示")
    @allure.testcase('test_caseid_1980372')
    @pytest.mark.full
    def test_caseid_1980372(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 0, 0, 1, 0])   
        for j in range(5):
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.set_door_fault("RiRe", door_fault, sleep_time=1)
            self.dk.send_rke_close_door_and_lock()
            self.ck_NotifyLockWarning(ck_horn=False)

    @allure.title("关门提示_主驾门开&其他门均有故障_车外提示")
    @allure.testcase('test_caseid_1980364')
    @pytest.mark.full
    def test_caseid_1980364(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([1, 0, 0, 0, 0])      
        door=["Pass", "LeRe", "RiRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1], sleep_time=1)  
        self.dk.send_rke_close_door_and_lock()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 4})
        self.ck_NotifyLockWarning(0, 2, ck_horn=False) 

    @allure.title("关门提示_副驾门开&其他门均有故障_车外提示")
    @allure.testcase('test_caseid_1980365')
    @pytest.mark.full
    def test_caseid_1980365(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 1, 0, 0, 0])      
        door=["Drvr", "LeRe", "RiRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1], sleep_time=1)  
        self.dk.send_rke_close_door_and_lock()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 4})
        self.ck_NotifyLockWarning(0, 2, ck_horn=False) 
        
    @allure.title("关门提示_左后门开&其他门均有故障_车外提示")
    @pytest.mark.sanity
    def test_caseid_1980366(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 0, 1, 0, 0])      
        door=["Drvr", "Pass", "RiRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1], sleep_time=1)  
        self.dk.send_rke_close_door_and_lock()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 4})
        self.ck_NotifyLockWarning(0, 2, ck_horn=False) 
        
    @allure.title("关门提示_右后门开&其他门均有故障_车外提示")
    @allure.testcase('test_caseid_1980367')
    @pytest.mark.full
    def test_caseid_1980367(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 0, 0, 1, 0])      
        door=["Drvr", "Pass", "LeRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1], sleep_time=1)  
        self.dk.send_rke_close_door_and_lock()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 4})
        self.ck_NotifyLockWarning(0, 2, ck_horn=False) 
        
    @allure.title("关门提示_尾门开&其他门有故障_车外提示")
    @pytest.mark.full
    def test_caseid_1980332(self):  
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 0, 0, 0, 1])      
        door=["Drvr", "Pass", "LeRe", "RiRe"]
        for i in range(4):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1], sleep_time=1)  
        self.dk.send_rke_close_door_and_lock()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 4})
        self.ck_NotifyLockWarning(0, 2, ck_horn=False) 
                            
    @allure.title("关门提示_四门闭锁但尾门解锁_尾门开_无车外提示")
    @allure.testcase('test_caseid_1980363') 
    @pytest.mark.full
    def test_caseid_1980363(self):  
        self.dk.set_cenlock_sts(2)  
        self.dk.set_door_sts([0, 0, 0, 0, 1])   
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [{"fault": 0, "faultMsg": "", "door": 4}]}) # 无故障
        self.dk.send_rke_close_door_and_lock()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 4})
        sleep(3)
        self.ck_NotifyLockWarning(ck_horn=False)       

    @allure.title("关门提示_挂挡自动关门_主驾门开&故障遍历_无车内提示")
    @pytest.mark.full
    def test_caseid_1980378(self): 
        self.dk.set_cenlock_sts(1) 
        self.dk.set_door_sts([1, 0, 0, 0, 0])   
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        for j in range(5):
            self.dk.set_chassis_service_gear('GearP') 
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.sd_tester.change_usage_mode(0xD)
            self.set_door_fault("Drvr", door_fault, sleep_time=1)
            self.dk.set_chassis_service_gear('GearR')
            self.ck_NotifyLockWarning(ck_horn=False)

    @allure.title("关门提示_挂挡自动关门_副驾门开&故障遍历_无车内提示")
    @pytest.mark.full
    def test_caseid_1980379(self): 
        self.dk.set_cenlock_sts(1) 
        self.dk.set_door_sts([0, 1, 0, 0, 0])   
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        for j in range(5):
            self.dk.set_chassis_service_gear('GearP') 
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.sd_tester.change_usage_mode(0xD)
            self.set_door_fault("Pass", door_fault, sleep_time=1)
            self.dk.set_chassis_service_gear('GearR')
            self.ck_NotifyLockWarning(ck_horn=False)

    @allure.title("关门提示_挂挡自动关门_左后门开&故障遍历_无车内提示")
    @pytest.mark.sanity
    def test_caseid_1980380(self): 
        self.dk.set_cenlock_sts(1) 
        self.sd_tester.change_usage_mode(0xD)
        self.dk.set_door_sts([0, 0, 1, 0, 0])   
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        for j in range(5):
            self.dk.set_chassis_service_gear('GearP') 
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.set_door_fault("LeRe", door_fault, sleep_time=1)
            self.dk.set_chassis_service_gear('GearD')
            self.ck_NotifyLockWarning(ck_horn=False)
            
    @allure.title("关门提示_挂挡自动关门_右后门开&故障遍历_无车内提示")
    @pytest.mark.full
    def test_caseid_1980381(self): 
        self.dk.set_cenlock_sts(1) 
        self.sd_tester.change_usage_mode(0xD)
        self.dk.set_door_sts([0, 0, 0, 1, 0])   
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        for j in range(5):
            self.dk.set_chassis_service_gear('GearP') 
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.set_door_fault("RiRe", door_fault, sleep_time=1)
            self.dk.set_chassis_service_gear('GearD')
            self.ck_NotifyLockWarning(ck_horn=False)
            
    @allure.title("关门提示_挂挡自动关门_主驾门开&其他门均有故障_车内提示")
    @pytest.mark.smoke
    def test_caseid_1980382(self): 
        self.dk.set_chassis_service_gear('GearP')
        self.dk.set_cenlock_sts(1) 
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        self.dk.set_door_sts([1, 0, 0, 0, 0])  
        door=["Pass", "LeRe", "RiRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1])
        sleep(0.5)
        self.dk.set_chassis_service_gear('GearR')
        self.ck_NotifyLockWarning(0, 1, ck_horn=False)   
        
    @allure.title("关门提示_挂挡自动关门_副驾门开&其他门均有故障_车内提示")
    @allure.testcase('test_caseid_1980383')
    @pytest.mark.full
    def test_caseid_1980383(self): 
        self.dk.set_chassis_service_gear('GearP')
        self.dk.set_cenlock_sts(1) 
        self.sd_tester.change_usage_mode(11)
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        self.dk.set_door_sts([0, 1, 0, 0, 0])  
        door=["Drvr", "LeRe", "RiRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1])  
        sleep(0.5)
        self.dk.set_chassis_service_gear('GearR')
        self.ck_NotifyLockWarning(0, 1, ck_horn=False)    
        
    @allure.title("关门提示_挂挡自动关门_左后门开&其他门均有故障_车内提示")
    @allure.testcase('test_caseid_1980384')
    @pytest.mark.full
    def test_caseid_1980384(self): 
        self.dk.set_chassis_service_gear('GearP')
        self.dk.set_cenlock_sts(1) 
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        self.dk.set_door_sts([0, 0, 1, 0, 0])      
        door=["Drvr", "Pass", "RiRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1]) 
        sleep(0.5)
        self.dk.set_chassis_service_gear('GearD')
        self.ck_NotifyLockWarning(0, 1, ck_horn=False)    
        
    @allure.title("关门提示_挂挡自动关门_右后门开&其他门均有故障_车内提示")
    @allure.testcase('test_caseid_1980385')
    @pytest.mark.full
    def test_caseid_1980385(self): 
        self.dk.set_chassis_service_gear('GearN')
        self.dk.set_cenlock_sts(1) 
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        self.dk.set_door_sts([0, 0, 0, 1, 0])      
        door=["Drvr", "Pass", "LeRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1])  
        sleep(0.5)
        self.dk.set_chassis_service_gear('GearD')
        self.ck_NotifyLockWarning(0, 1, ck_horn=False)           
        
    @allure.title("关门提示_挂挡自动关门取消_无车内提示")
    @pytest.mark.full
    def test_caseid_1980549(self): 
        self.dk.set_chassis_service_gear('GearN')
        self.dk.set_cenlock_sts(1) 
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, "CancelAutoCloseTrigger", {"trigger": 0})
        self.dk.set_door_sts([1, 1, 1, 1, 1])  
        sleep(1)
        self.dk.set_chassis_service_gear('GearD')
        self.ck_NotifyLockWarning(ck_horn=False)      
        
    @allure.title("关门提示_挂挡自动关门_尾门开&其他门均有故障_车内提示")
    @pytest.mark.full
    def test_caseid_1980386(self):  
        self.dk.set_chassis_service_gear('GearN') 
        self.sd_tester.change_usage_mode(0xD)     
        self.dk.set_cenlock_sts(1) 
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        self.dk.set_door_sts([0, 0, 0, 0, 1])      
        door=["Drvr", "Pass", "LeRe", "RiRe"]
        for i in range(4):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1])   
        self.dk.set_chassis_service_gear('GearD')
        self.ck_NotifyLockWarning(0, 1, ck_horn=False)   
        
    @allure.title("关门提示_挂挡自动关门_中控解锁&档位进入N档_无车内提示")
    @allure.testcase('test_caseid_1980387')
    @pytest.mark.full
    def test_caseid_1980387(self):   
        self.dk.set_chassis_service_gear('GearP') 
        self.sd_tester.change_usage_mode(0xD)     
        self.dk.set_cenlock_sts(1) 
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        self.dk.set_door_sts([1, 1, 1, 1, 1])    
        self.dk.set_chassis_service_gear('GearN')
        self.ck_NotifyLockWarning(ck_horn=False)
        
    @allure.title("关门提示_挂挡自动关门_四门闭锁但尾门解锁_无车内提示")
    @allure.testcase('test_caseid_1980388')
    @pytest.mark.full
    def test_caseid_1980388(self):   
        self.dk.set_chassis_service_gear('GearP') 
        self.dk.set_cenlock_sts(2) 
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        self.dk.set_door_sts([0, 0, 0, 0, 1])  
        self.sd_tester.change_usage_mode(11)  
        self.dk.set_chassis_service_gear('GearR')
        self.ck_NotifyLockWarning(ck_horn=False)  
                
    @allure.title("关门提示_挂挡自动关门_尾门未关&童锁故障_挂D档_车内提示")
    @pytest.mark.sanity
    def test_caseid_1959978(self):  # SOA-18708
        # todo 开始抓包   GearLvrIndcn|TrsmParkLockd|GetLockStatus|TrOpenerSts|AutoCloseTrigger|GetFaultInfo|NotifyLockWarning|GearCallback gear
        file_path, save_name = self.bgm_tcpdump.start_bgm_tcpdump()    
        self.dk.set_chassis_service_gear('GearP')     
        self.dk.set_cenlock_sts(1) #中控解锁
        self.sd_tester.change_usage_mode(0xD)
        self.partner.empty_all(1)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        self.dk.set_door_sts([0, 0, 0, 0, 1]) # 尾门未关 
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault", {"faults": [{"fault": 1, "faultMsg": "", "door": 2}]})   # 童锁错误
        self.dk.set_chassis_service_gear('GearD')
        self.ck_NotifyLockWarning(0, 1, ck_horn=False)
        # 检验TCP报文 # 列表里面为元祖（pdu的id，数据长度，信号起始bit位，信号长度，信号值），可以 是多个元祖
        data_list2 = [(15017, 1, 2, 3)]
        result1=self.ipdu.check_signal(self.ipdu.connectivitycanfd.BgmConnectivityFr15,
                        'ReminderWhileLock', timeout=1, do_print=True)
        logger.info(f"当前结果为：{result1}")
        sleep(5)
        self.ck_pdu(file_path,save_name,[],data_list2)  
   
    @allure.title("关门提示_挂挡自动关门_存在车门未关&童锁故障_挂R档_车内提示")
    @pytest.mark.sanity
    def test_caseid_1959977(self): 
        self.dk.set_cenlock_sts(1) #中控解锁
        self.sd_tester.change_usage_mode(0xD)
        self.partner.empty_all(1)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.partner.send_method_request("DoorService_client", 'SetAutoCloseTrigger', {"trigger": 0}) #打开D档自动关门
        self.dk.set_door_sts([1, 0, 1, 0, 0]) 
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 1)
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorFault", {"faults": [{"fault": 1, "faultMsg": "", "door": 2}]})   # 童锁错误
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [{"fault": 1, "faultMsg": "", "door": 2}]})
        self.dk.set_chassis_service_gear('GearR')
        self.ck_NotifyLockWarning(0, 1, ck_horn=False) 
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 2) # 消除 童锁错误
        sleep(2)

    @allure.title("关门提示_NFC长刷&存在车门未关&电动门无异常_车外提示")
    @pytest.mark.smoke
    def test_caseid_1939957(self):  
        self.dk.set_cenlock_sts(1) 
        self.partner.empty_all(1)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_Detected')
        sleep(0.1)
        self.dk.send_nfc_cmd()
        sleep(2.2)
        self.ipdu.set(self.ipdu.connectivitycanfd.NfcrConnFr02, 'NFCStatus', 'NFCSts_NotDetected')
        sleep(10)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 4})     
        self.ck_NotifyLockWarning(0, 2, ck_horn=False) 

    @allure.title("关门提示_PE长按闭锁&存在车门未关&电动门无异常_车外提示")
    @pytest.mark.sanity
    def test_caseid_1960057(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.dk.update_keyinfos(6, [KeyInfo(KeyType.BLE_Key, key_id1, 0x8)])
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(2, 2.51)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 4})     
        self.ck_NotifyLockWarning(0, 2, ck_horn=False)

    @allure.title("关门提示_RKE上锁&&存在车门未关&电动门无异常_车外提示")
    @pytest.mark.sanity
    def test_caseid_1960059(self): 
        self.dk.set_cenlock_sts(1) 
        self.partner.empty_all(1)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        self.dk.send_rke_close_door_and_lock()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 4})     
        self.ck_NotifyLockWarning(0, 2, ck_horn=False)   

    @allure.title("关门提示_远控上锁&&存在车门未关&电动门无异常_车外提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683306?projectId=46')
    @pytest.mark.full
    def test_caseid_1960060(self): 
        self.dk.set_cenlock_sts(1) 
        self.partner.empty_all(1)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 2, "source": 1}) #远程关门且闭锁 
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 4})     
        self.ck_NotifyLockWarning(0, 2, ck_horn=False)   

    @allure.title("车速自动关门_存在车门未关_车内提示_下发关门请求")
    @pytest.mark.sanity
    def test_caseid_1939961(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.sd_tester.change_usage_mode(0xD)
        self.dk.set_drvr_seat_present()
        self.dk.set_four_door_unlock()
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 'GenQf1_AccurData')
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 498)
        sleep(1.3)
        self.dk.ck_door_opener_cmd(1, 2) #校验关门指令
        self.dk.ck_door_opener_cmd(2, 2)
        self.dk.ck_door_opener_cmd(3, 2)
        self.dk.ck_door_opener_cmd(4, 2)
        self.dk.ck_door_opener_cmd(5, 2)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ck_NotifyLockWarning(0, 1, ck_horn=False)

    @allure.title("车速自动关门_存在车门未关_车内提示_不下发关门请求")
    @pytest.mark.full
    def test_caseid_1959992(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.sd_tester.change_usage_mode(0xD)
        self.dk.set_drvr_seat_present()
        self.dk.set_four_door_unlock()
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 'GenQf1_AccurData')
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 498)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        #监测re1   =1开门 =2关门
        sleep(1.3)
        self.ipdu.check(self.ipdu.bodycan.CemBodyFr02, 'TrOpenerReqTrOpenerReq', 0)              
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 0),
                                        (self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 0)])
        self.ipdu.check_multiple_signals([(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 0),
                                        (self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 0)])
        self.ck_NotifyLockWarning(0, 1, ck_horn=False)
        
    @allure.title("车速自动关门_存在车门未关_车速无效_无车内提示")
    @pytest.mark.full
    def test_caseid_1980546(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.sd_tester.change_usage_mode(0xD)
        self.dk.set_drvr_seat_present()
        self.dk.set_four_door_unlock()
        self.dk.set_door_opener_sts(5, 5, 5, 5, 5)
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 0) 
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 498) 
        sleep(1.3)
        self.dk.ck_door_opener_cmd(1, 0) #校验关门指令
        self.dk.ck_door_opener_cmd(2, 0)
        self.dk.ck_door_opener_cmd(3, 0)
        self.dk.ck_door_opener_cmd(4, 0)
        self.dk.ck_door_opener_cmd(5, 0)
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo")

    @allure.title("闭锁状态告警_PE长按&车外无有效钥匙")
    @pytest.mark.sanity
    def test_caseid_1959991(self): 
        self.dk.set_cenlock_sts(1)
        self.dk.reset_bncm_digital_keyinfo()
        self.dk.press_door_outswitch(1, 2.51)
        self.ck_NotifyLockWarning(3, 0, ck_horn=False)

    @allure.title("关门提醒-车门处于无法关门角度_通过设置的电动门开度百分比小于车门当前位置触发")
    @pytest.mark.sanity1
    def test_caseid_1989604(self):   
        self.dk.set_door_sts([1, 0, 0, 0, 0]) 
        self.setPercPosn([8, 0, 0, 0])
        self.partner.empty_all(0.5)
        for before_pos in [7, 8, 10]:
            for last_pos in [7, 8, 0]:
                self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPercPosn', before_pos) # 设置车门当前位置  
                self.partner.empty_all(1)
                self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 0, "pos": last_pos}]})
                self.partner.empty_all(2) # 3s计时器   
                logger.info(f"打印当前返回值:before_pos={before_pos},last_pos={last_pos}")  
                if before_pos <= 8 and last_pos < before_pos:
                    self.ck_NotifyLockWarning(12, 0, ck_horn=False)   
                else:
                    self.ck_NotifyLockWarning(ck_horn=False, timeout=2)      
                      
    @allure.title("关门提醒-车门处于无法关门角度_计时时间内相应车门故障遍历_超时后相应车门未关闭")
    @pytest.mark.sanity
    def test_caseid_1989605(self): # 若门产生11/16/17/18/19故障，则不会触发关门提醒
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        self.setPercPosn([0, 0, 8, 0]) # 后门多了儿童锁故障
        self.partner.empty_all(0.5)
        # 故障11/16/17/18/19
        for fault in range(5):
            door_fault=[0, 0, 0, 0, 0]
            door_fault[fault]=1
            self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 4, "pos": 1}]})
            sleep(1)
            self.set_door_fault("LeRe", door_fault, sleep_time=1)
            self.partner.empty_all()
            self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout=2)        
        # 儿童锁故障
        self.set_door_fault("LeRe", [0, 0, 0, 0, 0], sleep_time=1)
        self.partner.send_method_request(DOOR_SERVICE_CLIENT, 'SetPosition', {"doors": [{"id": 4, "pos": 1}]})
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 1)
        self.partner.empty_all(1)
        self.ck_NotifyLockWarning(12, 0, ck_horn=False)  
           
    @allure.title("关门提醒-车门处于无法关门角度_四门同时触发关门提醒")
    @pytest.mark.sanity
    def test_caseid_1943230(self):   #  四门都报 DoorDrvrPercPosn|PositionEvent|DoorActionRequestEvent|GetAntiPinch|GetFaultInfo|NotifyLockWarning
        self.dk.set_door_sts([1, 1, 1, 1, 0]) 
        self.setPercPosn([8, 8, 7, 6])
        self.partner.empty_all(1)
        self.partner.send_method_request('DoorService_client', 'SetPosition', {"doors": [{"id": 4, "pos": 0}]})
        self.partner.empty_all(2) # 3s计时器
        self.ck_NotifyLockWarning(12, 0, ck_horn=False)
        self.ck_NotifyLockWarning(12, 0, ck_horn=False)
        self.ck_NotifyLockWarning(12, 0, ck_horn=False)
        self.ck_NotifyLockWarning(12, 0, ck_horn=False)
    
    @allure.title("关门提醒-车门处于无法关门角度_计时时间内触发防夹_超时后车门未关仍执行关门提醒")
    @pytest.mark.full
    def test_caseid_1960006(self):    
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPercPosn', 1) 
        self.partner.empty_all(1)  
        self.partner.send_method_request('DoorService_client', 'SetPosition', {"doors": [{"id": 4, "pos": 0}]}) 
        sleep(0.5) 
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 1)
        self.partner.empty_all(2) # 3s计时器
        self.ck_NotifyLockWarning(12, 0, ck_horn=False)

    @allure.title("关门提醒-车门处于无法关门角度_计时结束时车门关门成功_不执行关门提醒")
    @pytest.mark.full
    def test_caseid_1943231(self):  
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassPercPosn', 8)
        self.partner.empty_all(1)
        self.partner.send_method_request('DoorService_client', 'SetPosition', {"doors": [{"id": 1, "pos": 0}]})
        self.partner.empty_all(1) # 3s计时器
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ck_NotifyLockWarning(ck_horn=False)

    @allure.title("关门提醒-车门处于无法关门角度_计时时间内发生异常又恢复_结束时车门未关闭_不执行关门提醒")
    @pytest.mark.full
    def test_caseid_1989608(self): # 门产生故障时，就会停止计时器 
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassPercPosn', 8)
        self.partner.empty_all(1)
        self.partner.send_method_request('DoorService_client', 'SetPosition', {"doors": [{"id": 1, "pos": 0}]})
        self.partner.empty_all(1) # 3s计时器
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DtcInfDoorPassBoolean2', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DtcInfDoorPassBoolean2', 0)
        self.ck_NotifyLockWarning(ck_horn=False)

    @allure.title("关门提醒-车门处于无法关门角度_计时开始前电动门故障_不执行关门提醒")
    @pytest.mark.full
    def test_caseid_1984671(self): # 进入计时器时也会get当前门的故障状态，若故障则停止计时，不上报关门提醒
        self.dk.set_door_sts([1, 1, 1, 1, 0])
        self.setPercPosn([8, 8, 8, 8])
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DtcInfDoorDrvrBoolean2', 1) # value(11) kFaultPlayProtectionActive
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DtcInfDoorPassBoolean3', 1) # value(17) kRollAngleAbnormal
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DtcInfDoorLeReBoolean4', 1) # value(18) kRoadInclinationAbnormal
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DtcInfDoorRiReBoolean5', 1) # value(19) kHallSensorsError
        self.partner.empty_all(1)
        self.partner.send_method_request('DoorService_client', 'SetPosition', {"doors": [{"id": 4, "pos": 1}]})
        self.partner.empty_all(2) # 3s计时器
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout=2)
        
    @allure.title("踩刹车自动关门功能禁用_isOn=True，重复触发&超时恢复")
    @pytest.mark.full
    def test_caseid_111446(self): 
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": False})   
        self.partner.empty_all(0.5)
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": True}) #设置踩刹车自动关门禁用-禁用
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT,"BrakeCloseDoorInhibitStatus",{"isOn": True}, 2.2)  #校验 notify
        self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetBrakeCloseDoorInhibitStatus", {}, {"out": True}) 
        sleep(1)
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": True}) # Timer时间内再次设置踩刹车自动关门禁用-禁用
        sleep(1.5)
        self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetBrakeCloseDoorInhibitStatus", {}, {"out": True})  
        sleep(1)
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT,"BrakeCloseDoorInhibitStatus",{"isOn": False},2.2)  #校验 notify
        self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetBrakeCloseDoorInhibitStatus", {}, {"out": False})  
        
    @allure.title("踩刹车自动关门功能禁用_isOn=True,重复触发&超时恢复_参数变化调用API")
    @pytest.mark.sanity
    def test_caseid_1980823(self):
        file_path, save_name = self.bgm_tcpdump.start_bgm_tcpdump()
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": False})   
        self.partner.empty_all(0.5)
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": True}) #设置踩刹车自动关门禁用-禁用
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT,"BrakeCloseDoorInhibitStatus",{"isOn": True}, 2.2)  #校验 notify
        self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetBrakeCloseDoorInhibitStatus", {}, {"out": True}) 
        sleep(1)
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": True}) # Timer时间内再次设置踩刹车自动关门禁用-禁用
        sleep(1.5)
        self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetBrakeCloseDoorInhibitStatus", {}, {"out": True})  
        sleep(1)
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT,"BrakeCloseDoorInhibitStatus",{"isOn": False}, 2.2)  #校验 notify
        self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetBrakeCloseDoorInhibitStatus", {}, {"out": False}) 
        sleep(5) 
        data_list = [(30013, 1, 0, 1)]
        data_list1 = [(30013, 1, 0, 1, 0), (30013, 1, 0, 1, 1)]
        self.ck_pdu(file_path,save_name,data_list1,data_list)
        
    @allure.title("踩刹车自动关门功能禁用_下电不记忆且服务启动触发上报&调用API")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1980824(self): 
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": True})
        sleep(1)
        self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetBrakeCloseDoorInhibitStatus", {}, {"out": True})
        self.restart_bgm_and_connect_service(ENTRY_SERVICE_CLIENT)
        sleep(5)
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "BrakeCloseDoorInhibitStatus", {"isOn": False})
        self.bgm_tcpdump.stop_bgm_tcpdump() #停止抓包
        file_path, save_name = self.bgm_tcpdump.start_bgm_tcpdump()
        sleep(10)
        data_list = [(30013, 1, 0, 1)]
        data_list1 = [(30013, 1, 0, 1, 0)]
        self.ck_pdu(file_path,save_name,data_list1,data_list)

    @allure.title("中控解闭锁成功触发声光提示_Approach解闭锁")
    @pytest.mark.sanity
    def test_caseid_105248(self):  
        self.dk.set_cenlock_sts(1)
        sleep(2)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        self.partner.empty_all()
        self.dk.send_walk_away_lock_cmd()
        self.ck_EntrySystemAudioLightInfo(2, 2)
        sleep(1)
        self.dk.send_approach_unlock_cmd()
        self.ck_EntrySystemAudioLightInfo(1, 1)
        
    @allure.title("中控解闭锁成功触发声光提示_蓝牙解闭锁")
    @pytest.mark.full
    def test_caseid_105254(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.send_rke_lock()
        self.ck_EntrySystemAudioLightInfo(2, 2)
        sleep(1)
        self.dk.send_rke_unlock()
        self.ck_EntrySystemAudioLightInfo(1, 1, timeout=5)

    @allure.title("中控解闭锁成功触发声光提示_中控锁状态从2变为1")
    @pytest.mark.full 
    def test_caseid_1980544(self): # grep "entry_service_imp|central_lock_service_imp"|grep -aiE "mLockStatu:|LockgCenStsLockSt|LockSuccessTriggerSource|EntrySystemAudioLightInfo"
        self.dk.set_cenlock_sts(2)
        self.partner.empty_all(1)
        self.dk.send_rke_unlock() # RKE：锁状态从2变1 无事件上报；从2变3，entry报6
        sleep(2)
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo")
        
    @allure.title("中控解闭锁成功触发声光提示_中控锁状态从3变为2")
    @pytest.mark.full 
    def test_caseid_1980545(self): 
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all(1)
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.press_door_outswitch(5, 0.5)
        self.dk.ck_cenlock_sts(2, timeout=2)
        sleep(2)
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo")
        
    @allure.title("中控解闭锁成功触发声光提示_PE解闭锁")
    @pytest.mark.smoke
    def test_caseid_1918651(self): 
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.empty_all()
        self.dk.press_door_outswitch(1, 2.51)
        self.ck_EntrySystemAudioLightInfo(2, 2)
        sleep(2)
        self.dk.press_door_outswitch(1, 1.1)
        self.ck_EntrySystemAudioLightInfo(1, 1)

    @allure.title("中控解闭锁成功触发声光提示_重上锁")
    @pytest.mark.full
    def test_caseid_105240(self): 
        logger.info("硬线J3-36接地(内部信号HoodSwt1")
        self.io.set_do_level("hood_ajar_2", True)
        sleep(1)
        logger.info("硬线J3-37接地(内部信号HoodSwt2)")
        self.io.set_do_level("hood_ajar_1", True)
        sleep(1)

        logger.info("Step:使硬线J3-36悬空")
        self.io.set_do_level("hood_ajar_2", False)

        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 1, "source": 0}) #蓝牙闭锁 
        sleep(1)
        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 0, "source": 0})  #蓝牙解锁
        sleep(1)
        self.partner.send_request_and_ck_resp(BOONET_SERVICE_CLIENT, 'GetStatus', {}, {"out": 1})  #获取前舱盖状态 1=关闭 0=打开
        self.partner.send_request_and_ck_resp(TAILGATE_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {}, {"out": {"value": False, "validity": 0}})  #尾门开关状态 false关 true打开
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatusValidity", {"doors": [4]},
                                                  {"out": [{"value":{"id":0,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":1,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":2,"isOpen":False},"isOpenValidity":0},
                                                           {"value":{"id":3,"isOpen":False},"isOpenValidity":0}]}) # DoorAll false关
        self.partner.empty_all()
        sleep(30)
        self.ck_EntrySystemAudioLightInfo(2, 2)  # 触发源为(1)kRemoteKey

    @allure.title("进入系统声光提醒信息_远控解闭锁_无需触发声光电提示")
    @allure.testcase('test_caseid_105247')
    @pytest.mark.full
    def test_caseid_105247(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 1, "source": 1})#远程闭锁 
        self.ck_EntrySystemAudioLightInfo(6, 6)
        sleep(1)
        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 0, "source": 1})#远程解锁
        self.ck_EntrySystemAudioLightInfo(5, 5)

    @allure.title("进入系统声光提醒信息_NFC解闭锁_无需触发声光电提示")
    @pytest.mark.sanity
    def test_caseid_1959520(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.dk.send_nfc_cmd()
        self.ck_EntrySystemAudioLightInfo(6, 6)
        sleep(1)
        self.dk.send_nfc_cmd()
        self.ck_EntrySystemAudioLightInfo(5, 5)

    @allure.title("进入系统声光提醒信息_外部其他方式解闭锁_无需触发声光电提示")
    @pytest.mark.sanity
    def test_caseid_1903587(self):  
        # 中控解锁
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        #外部其他方式上锁并设防
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3}) 
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockSuccessTriggerSource", {"sourceId": 10})
        self.partner.send_request_and_ck_resp(CENTRALLOCK_SERVICE_CLIENT, "GetLockSuccessTriggerSource", {},
                                              {"out": 10})
        self.ipdu.check(self.ipdu.bodycan.CEMBodyFr13, 'LockgCenStsTrigSrc', 10)
        self.ck_EntrySystemAudioLightInfo(6, 6)        #上锁       

    @allure.title("仅尾门开启_关闭尾门进入设防场景_原TrUnlock_RKE闭锁")
    @pytest.mark.smoke
    def test_caseid_105226(self): 
        self.dk.set_cenlock_sts(2)
        self.partner.empty_all(1)
        self.dk.send_rke_lock()
        self.ck_EntrySystemAudioLightInfo(6, 6)

    @allure.title("仅尾门开启_关闭尾门进入设防场景_原TrUnlock_PE长按闭锁")
    @pytest.mark.full
    def test_caseid_105239(self): 
        self.dk.set_cenlock_sts(2)
        self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.partner.empty_all(1)
        self.dk.press_door_outswitch(1, 2.51)  # todo: TrUnlock情况下，关闭尾门，此时无法长按闭锁，需求问题
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ck_EntrySystemAudioLightInfo(6, 6)

    @allure.title("仅尾门开启_关闭尾门进入设防场景_原TrUnlock_OutsideOthers闭锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683277?projectId=46')
    @pytest.mark.full
    def test_caseid_105235(self):
        self.dk.set_cenlock_sts(2)
        self.partner.empty_all(1)
        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 3, "source": 3})
        self.ck_EntrySystemAudioLightInfo(6, 6)      

    @allure.title("HAVP解闭锁成功_收到HAVP泊入完成_S2S无动作")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683297?projectId=46')
    @pytest.mark.full
    @pytest.mark.deleted_interface
    def test_caseid_105215(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_event_notify("AVPService_server", "NotifyAVPStatus", {"sts": {"havpSubSatus": 8}})
        sleep(3)
        self.dk.ck_cenlock_sts(1)
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo")

    @allure.title("HAVP解闭锁成功_收到HAVP泊出完成_原中控解锁_找到钥匙")
    @pytest.mark.sanity
    def test_caseid_105238(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_event_notify("AVPService_server", "NotifyAVPStatus", {"sts": {"havpSubSatus": 7}})
        sleep(3)
        try:
            self.dk.ck_search_key_req(2, 6)
        except Exception as e:
            pass
        else:
            assert False, "不应该有寻钥匙请求"
        self.dk.ck_cenlock_sts(1)
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo")

    @allure.title("APA解闭锁成功_收到APA泊入完成_PAStatus=3_S2S无动作")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683259?projectId=46')
    @pytest.mark.full
    @pytest.mark.deleted_interface
    def test_caseid_105253(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_event_notify("RPAAPAService_server", "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 3}})
        sleep(3)
        self.dk.ck_cenlock_sts(1)
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo")

    @allure.title("APA解闭锁成功_收到APA泊入完成_PAStatus=4_S2S无动作")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683249?projectId=46')
    @pytest.mark.full
    @pytest.mark.deleted_interface
    def test_caseid_105262(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_event_notify("RPAAPAService_server", "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 4}})
        sleep(3)
        self.dk.ck_cenlock_sts(1)
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo")

    @allure.title("APA解闭锁成功_收到APA泊出完成_paStatus=8_S2S无动作")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683291?projectId=46')
    @pytest.mark.full
    @pytest.mark.deleted_interface
    def test_caseid_105221(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_event_notify("RPAAPAService_server", "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 8}})
        sleep(3)
        try:
            self.dk.ck_search_key_req(2, 6)
        except Exception as e:
            pass
        else:
            assert False, "不应该有寻钥匙请求"
        self.dk.ck_cenlock_sts(1)
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo")

    @allure.title("APA解闭锁成功_收到APA泊出完成_paStatus=9_S2S无动作")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683255?projectId=46')
    @pytest.mark.full
    @pytest.mark.deleted_interface
    def test_caseid_105257(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_event_notify("RPAAPAService_server", "NotifyPARemoteStatus",
                                       {"paRemoteStatus": {"paStatus": 9}})
        sleep(3)
        try:
            self.dk.ck_search_key_req(2, 6)
        except Exception as e:
            pass
        else:
            assert False, "不应该有寻钥匙请求"
        self.dk.ck_cenlock_sts(1)
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo")

    # 闭锁状态告警 场景2
    @allure.title("闭锁状态告警_离车闭锁联动主驾门关_触发离车落锁请求后_8s内触发防夹_鸣笛")
    @pytest.mark.smoke
    def test_caseid_1989234(self): # SetConfigInfo|ApproachRequestInfoCallback info|DoorStsCallback : |horn_service|Entry: 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        self.partner.empty_all(7)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_horn()
        
    @allure.title("闭锁状态告警_离车闭锁联动主驾门关_触发离车落锁请求后_8s内触发两次防夹_第二次不鸣笛")
    @pytest.mark.full
    def test_caseid_1989235_1(self): # SetConfigInfo|ApproachRequestInfoCallback info|DoorStsCallback : |horn_service|Entry: 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.empty_all(6.5) # 防止触发场景3，【实车门会运动到正在开启中，故不存在NFC解锁开门触发防夹的场景】
        # 如果在台架上同时满足离车闭锁和场景3 的触发条件，会开启Timer1和Timer2
        # 在触发防夹后会鸣笛一次【停掉先满足触发的Timer】，然后时间内再触发一次防夹的话，会再鸣笛一次【此时才会停止另一个Timer】
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_horn() # 第一次触发防夹，鸣笛
        for i in range(2):
            self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', i)
            sleep(1)
        self.ck_horn(ck_horn=False) # 第二次触发防夹，不鸣笛       

    @allure.title("闭锁状态告警_离车闭锁联动主驾门关_触发离车落锁请求后_8s后触发防夹_无鸣笛")
    @pytest.mark.sanity
    def test_caseid_1989236(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        sleep(8)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_horn(ck_horn=False)
        
    @allure.title("闭锁状态告警_离车闭锁联动主驾门关_触发离车落锁请求后_8s内先关门再开门触发防夹_无鸣笛")
    @pytest.mark.sanity
    def test_caseid_1989237(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        self.dk.set_door_sts([0, 0, 0, 0, 0]) # 此时应停止8s计时器
        sleep(2)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_horn(ck_horn=False, timeout=5)

    @allure.title("闭锁状态告警_离车闭锁联动主驾门关_触发主驾门防夹后_再触发离车落锁请求_8s后无鸣笛")
    @pytest.mark.full
    def test_caseid_1989238(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 'Boolean_TRUE')
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        sleep(7)
        self.ck_horn(ck_horn=False, timeout=2)  
                
    @allure.title("闭锁状态告警_离车闭锁联动主驾门关_触发离车落锁请求后_8s内副驾门触发防夹_无鸣笛")
    @pytest.mark.full
    def test_caseid_1989239(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        self.dk.set_door_sts([1, 1, 0, 0, 0])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        sleep(7)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 'Boolean_TRUE')
        self.ck_horn(ck_horn=False, timeout=2)    
    
    # 闭锁状态告警 场景3
    @allure.title("闭锁状态告警_离车闭锁联动所有门关_触发离车落锁请求后_8s内触发主驾门防夹_鸣笛")
    @pytest.mark.smoke
    def test_caseid_1989243(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        sleep(7)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_horn() 

    @allure.title("闭锁状态告警_离车闭锁联动所有门关_触发离车落锁请求后_8s内触发左后门防夹_鸣笛")
    @pytest.mark.sanity
    def test_caseid_1989244(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        sleep(7)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReAntiPnch', 'Boolean_TRUE')
        self.ck_horn() 
        
    @allure.title("闭锁状态告警_离车闭锁联动所有门关_触发离车落锁请求后_8s内触发右后门防夹_鸣笛")
    @pytest.mark.full
    def test_caseid_1989245(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        sleep(7)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReAntiPnch', 'Boolean_TRUE') 
        self.ck_horn() 
        
    @allure.title("闭锁状态告警_离车闭锁联动所有门关_触发离车落锁请求后_8s内触发尾门防夹_鸣笛")
    @pytest.mark.full
    def test_caseid_1989246(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        sleep(7)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 'Boolean_TRUE') 
        self.ck_horn() 
        
    @allure.title("闭锁状态告警_离车闭锁联动所有门关_触发两次离车闭锁后_触发副驾门防夹_仅一次鸣笛")
    @pytest.mark.sanity
    def test_caseid_1989247(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        self.dk.set_door_sts([1, 1, 0, 0, 0])
        self.partner.empty_all(1)
        for _ in range(2):
            self.dk.send_walk_away_lock_cmd()
            self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
            sleep(3)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 'Boolean_TRUE') 
        self.ck_horn() 
        self.ck_horn(ck_horn=False)  
        
    @allure.title("闭锁状态告警_离车闭锁联动所有门关_触发离车落锁请求后_8s内触发两次防夹_第二次不鸣笛")
    @pytest.mark.sanity
    def test_caseid_1989248(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        self.dk.set_door_sts([1, 1, 0, 0, 0])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 'Boolean_TRUE') 
        self.ck_horn() 
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_horn(ck_horn=False)  

    @allure.title("闭锁状态告警_离车闭锁联动所有门关_触发离车落锁请求后_8s内先关门再开门触发防夹_无鸣笛")
    @pytest.mark.sanity
    def test_caseid_1989249(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        self.dk.set_door_sts([0, 0, 0, 0, 0]) # 此时应停止8s计时器
        sleep(2)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_horn(ck_horn=False, timeout=5)
        
    @allure.title("闭锁状态告警_离车闭锁联动所有门关_主驾门开触发离车落锁请求后_8s内副驾门开且触发防夹但主驾门关_鸣笛")
    @pytest.mark.full
    def test_caseid_1989250(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        self.dk.set_door_sts([1, 1, 0, 0, 0]) 
        sleep(2)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        sleep(2)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 'Boolean_TRUE') 
        self.ck_horn()      
        
    @allure.title("闭锁状态告警_离车闭锁联动所有门关_触发主驾门防夹后_再触发离车落锁请求_8s后无鸣笛")
    @pytest.mark.full
    def test_caseid_1989251(self): # todo 确认该场景 是否需要鸣笛
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 'Boolean_TRUE')
        self.partner.empty_all(1)
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(KEY_SERVICE_CLIENT, "DigitalKeyApproachRequestInfo",  {"approachRequestInfo": {"approachRequestSts": 3}}, timeout=3)
        sleep(7)
        self.ck_horn(ck_horn=False, timeout=2)  
                                                
    @allure.title("闭锁状态告警_离车闭锁&&存在车门未关_触发防夹")
    @pytest.mark.smoke
    def test_caseid_105252(self): # UpdateAntiPinchEvent|LockActTriggerSource|DoorDrvrSts|horn_service|ActvOfHorn
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.dk.send_walk_away_lock_cmd()
        self.partner.empty_all(7)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_horn()
        
    @allure.title("闭锁状态告警_离车闭锁&&存在车门未关_超时触发防夹")
    @pytest.mark.full
    def test_caseid_1980152(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.dk.send_walk_away_lock_cmd()
        self.partner.empty_all(7) # 离车闭锁5s后会下发关门，导致触发关门提示lock=12
        sleep(1.5)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        try:
            self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout=4)
        except Exception as e:
            logger.info(f"触发关门提示")
            self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", {"warnnings": {"lock": 12, "reminder": 0}})
            pass

    @allure.title("闭锁状态告警_离车闭锁&&存在车门未关_正常关闭")
    @pytest.mark.sanity
    def test_caseid_105256(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.dk.send_walk_away_lock_cmd()
        self.partner.empty_all(6)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ck_NotifyLockWarning(ck_horn=False)

    @allure.title("闭锁状态告警_离车闭锁&&存在车门未关_主驾门防夹")
    @pytest.mark.smoke
    def test_caseid_105249(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 0, 0, 0, 0])
        self.dk.send_walk_away_lock_cmd()
        self.partner.empty_all(7) # 离车闭锁联动关门，会立即触发关门提示，故先清除关门提示消息，来校验下面无notifylockwarning
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.ck_horn()

    @allure.title("闭锁状态告警_离车闭锁&&存在车门未关_副驾门防夹_触发两次离车闭锁")
    @pytest.mark.full
    def test_caseid_105242(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([0, 1, 0, 0, 0])
        self.dk.send_walk_away_lock_cmd()
        self.partner.empty_all(1.5)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 'Boolean_TRUE') 
        self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 0}) 
        self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 1})
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_no_event(HORN_SERVICE_CLIENT, "Status", timeout=8.5)
        
    @allure.title("闭锁状态告警_离车闭锁&&存在车门未关_副驾门防夹_触发两次防夹")
    @pytest.mark.sanity
    def test_caseid_1987649(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 1, 0, 0, 0])
        self.dk.send_walk_away_lock_cmd()
        self.partner.empty_all(1.5)
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassAntiPnch', 'Boolean_TRUE') 
        self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 0})  
        self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 1})
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrAntiPnch', 'Boolean_TRUE')
        self.partner.ck_no_event(HORN_SERVICE_CLIENT, "Status", timeout=3)

    @allure.title("闭锁状态告警_离车闭锁&&存在车门未关_左后门防夹")
    @pytest.mark.full
    def test_caseid_105230(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([0, 0, 1, 0, 0])
        sleep(0.5)
        self.dk.send_walk_away_lock_cmd()
        self.partner.empty_all(7.5)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeReAntiPnch', 'Boolean_TRUE')
        self.ck_horn()

    @allure.title("闭锁状态告警_离车闭锁&&存在车门未关_右后门防夹")
    @pytest.mark.full
    def test_caseid_105236(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([0, 0, 0, 1, 0])
        self.dk.send_walk_away_lock_cmd()
        self.partner.empty_all(7)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiReAntiPnch', 'Boolean_TRUE') 
        self.ck_horn()

    @allure.title("闭锁状态告警_离车闭锁&&存在车门未关_尾门防夹")
    @pytest.mark.sanity
    def test_caseid_105227(self): 
        self.dk.set_cenlock_sts(3)
        sleep(3)
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([0, 0, 0, 0, 1])
        self.dk.send_walk_away_lock_cmd()
        self.partner.empty_all(6.5)
        self.ipdu.set(self.ipdu.bodycan.PotBodyFr02, 'TrAntiPnch', 'Boolean_TRUE') 
        self.ck_horn()

    @allure.title("闭锁状态告警_离车闭锁&&五门未关_未触发防夹&五门关闭")
    @pytest.mark.full
    def test_caseid_1985274(self): 
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
        sleep(0.5)
        self.dk.set_door_sts([1, 1, 1, 1, 1])
        self.dk.send_walk_away_lock_cmd() # 无防夹不会触发该场景
        self.partner.empty_all(3)
        sleep(3)
        self.dk.set_door_sts([0, 0, 0, 0, 0])
        self.ck_NotifyLockWarning(ck_horn=False)

    @allure.title("踩刹车自动关门功能禁用_下电不记忆且服务启动触发上报")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_105246(self): 
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": True})
        sleep(1)
        self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetBrakeCloseDoorInhibitStatus", {}, {"out": True})
        self.restart_bgm_and_connect_service(ENTRY_SERVICE_CLIENT)
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "BrakeCloseDoorInhibitStatus", {"isOn": False})

    @allure.title("踩刹车自动关门_功能未禁用")
    @pytest.mark.smoke
    def test_caseid_1985634(self):   #  DoorOpenerDrvrReqDoorOpenerReq2
        # 当usgMod=0/1/2时， VehModMngtGlbSafe1EgyLvlElecMai =0 ；usgMod=11/13,不判断
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8) # SWSR：507156
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": False})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)  # 制动踏板位置
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)  # 制动踏板踩下无故障
        self.dk.set_cenlock_sts(1)  
        sleep(2)
        for i in range(12):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)     
            self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', i)  
            # 门运动状态 {0:7, 1:2, 2:5, 3:9, 4:6, 5:0, 6:1, 7:8, 8:6, 9:10, 10:6, other:65535}
            sleep(2) 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) 
            if i != 1:
                self.dk.ck_door_opener_cmd(1, 2)
            else :
                result=self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 2, do_assert=False)[0]
                assert not result

    @allure.title("踩刹车自动关门_功能禁用")
    @pytest.mark.full
    def test_caseid_1985635(self):   #  DoorOpenerDrvrReqDoorOpenerReq2
        # 当usgMod=0/1/2时， VehModMngtGlbSafe1EgyLvlElecMai =0 ；usgMod=11/13,不判断
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8) # SWSR：507156
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)  # 制动踏板位置
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)  # 制动踏板踩下无故障
        self.dk.set_cenlock_sts(1)  
        sleep(2)
        for i in range(12):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)     
            self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', i)  
            # 门运动状态 {0:7, 1:2, 2:5, 3:9, 4:6, 5:0, 6:1, 7:8, 8:6, 9:10, 10:6, other:65535}
            sleep(2) 
            self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": True})
            sleep(0.5)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) 
            result=self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 2, do_assert=False)[0]
            assert not result 

    @allure.title("踩刹车自动关门_非主驾门不下发关门请求")
    @pytest.mark.full
    def test_caseid_1985636(self): 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8) # SWSR：507156
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": False})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)  # 制动踏板位置
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)  # 制动踏板踩下无故障
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', 1)  
        self.dk.set_cenlock_sts(1)  
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)   
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, "DoorOpenerPassSts", random.choice(range(12)))
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, "DoorOpenerLeReSts", random.choice(range(12)))
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, "DoorOpenerRiReSts", random.choice(range(12)))
        sleep(2) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) 
        result_drvr=self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 2, do_assert=False)[0]
        result_pass=self.ipdu.check(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerPassReqDoorOpenerReq2', 2, do_assert=False)[0]
        result_lere=self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerLeReReqDoorOpenerReq2', 2, do_assert=False)[0]
        result_rere=self.ipdu.check(self.ipdu.bodycan.CemBodyFr79, 'DoorOpenerRiReReqDoorOpenerReq2', 2, do_assert=False)[0]
        assert result_drvr == result_pass == result_lere == result_rere == 0

    @allure.title("踩刹车自动关门_踏板被踩下后再次收到踏板被踩下的event不处理")
    @pytest.mark.full
    def test_caseid_1986111(self): # BrakePedalStatus
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8) # SWSR：507156
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": False})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)  # 制动踏板位置
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)  # 制动踏板踩下无故障
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', 0)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)  
        self.dk.set_cenlock_sts(1)  
        self.partner.empty_all(1)
        # # self.partner.ck_s2s_event(PEDAL_SERVICE_CLIENT, "BrakePedalStatus", {"status": {"value": 1, "validity": 0}})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)   
        # self.dk.ck_door_opener_cmd(1, 2) 
        self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest",{"pos": [{"id": 0, "action": 2}]})
        self.partner.empty_all(2)    
        # 门运动状态 {0:7, 1:2, 2:5, 3:9, 4:6, 5:0, 6:1, 7:8, 8:6, 9:10, 10:6, other:65535}
        self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        sleep(3)
        self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        sleep(2)
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "DoorActionRequest" )
        
    @allure.title("踩刹车自动关门_validity=7&sts从0至1_处理踩刹车自动关门")
    @pytest.mark.full
    def test_caseid_1986112(self): # BrakePedalStatus
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8) # SWSR：507156
        self.partner.send_method_request(ENTRY_SERVICE_CLIENT, "SetBrakeCloseDoorInhibit", {"isOn": False})
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)  # 制动踏板位置
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)  # 制动踏板踩下无故障
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', 0) 
        try: 
            self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
            sleep(2)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)  
            self.partner.empty_all(1) 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)   
            # self.dk.ck_door_opener_cmd(1, 2) 
            self.partner.ck_s2s_event(DOOR_SERVICE_CLIENT, "DoorActionRequest",{"pos": [{"id": 0, "action": 2}]})
            self.partner.empty_all(2)    
            # 门运动状态 {0:7, 1:2, 2:5, 3:9, 4:6, 5:0, 6:1, 7:8, 8:6, 9:10, 10:6, other:65535}  
        except Exception as error:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
            assert False, error
        else:
            self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')    
        self.partner.ck_no_event(DOOR_SERVICE_CLIENT, "DoorActionRequest" , timeout=3)  
        
    @allure.title("踩刹车自动关门_起线程模拟周期1s调用禁用接口_踩刹车不下发关门")
    @pytest.mark.full
    def test_caseid_1985651(self): 
        self.flag=True
        thread = threading.Thread(target=self.set_BrakeCloseDoorInhibit)
        thread.setDaemon(True) # 守护线程，case结束线程终止
        thread.start()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8) # SWSR：507156
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)  # 制动踏板位置
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)  # 制动踏板踩下无故障
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', 4)    
        self.dk.set_cenlock_sts(1)  
        sleep(2)        
        for _ in range(10):
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0) 
            sleep(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)  
            result=self.ipdu.check(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 2, do_assert=False)[0] 
            assert not result 

    @allure.title("踩刹车自动关门_重启后无bodycan信号")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1985652(self):  # DoorDrvrSts|DoorOpenerDrvrSts|DoorDrvrAntiPnch|BrkPedlPsdBrkPedlPsd
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1) 
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', 7) # sts
        sleep(2) 
        self.ipdu.pause_bus_send("bodycan") 
        sleep(2)
        self.bgm_power_off_and_on() # 无需等待服务连接
        self.dk.ck_door_opener_cmd(1, 2, timeout=7.1)  # 若能够收到event，拿到的是默认值65535

    @allure.title("踩刹车自动关门_重启后无DoorOpenerDrvrSts和DoorDrvrAntiPnch")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1985654(self): 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)  
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', 5) # sts
        sleep(2)
        self.ipdu.stop_send_pdu('bodycan', 0x217)
        sleep(2)
        self.bgm_power_off_and_on() # 无需等待服务连接
        self.dk.ck_door_opener_cmd(1, 2, timeout=7.1)

    @allure.title("踩刹车自动关门_重启后无DoorDrvrSts")
    @pytest.mark.full
    @pytest.mark.restart
    def test_caseid_1985655(self): 
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 8)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdQf', 3)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)  
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorOpenerDrvrSts', 7) # sts
        sleep(2)
        self.ipdu.stop_send_pdu('bodycan', 0x240)
        sleep(2)
        self.bgm_power_off_and_on() # 无需等待服务连接
        self.dk.ck_door_opener_cmd(1, 2, timeout=7.1)

    @allure.title("工厂模式下自动解锁_Normal切Factory")
    @pytest.mark.sanity
    @pytest.mark.restart
    def test_caseid_105233(self): 
        self.restart_bgm_and_connect_service(ENTRY_SERVICE_CLIENT)

        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 0, "source": 2}, timeout=1)
        sleep(1)
        self.dk.ck_cenlock_sts(1, timeout=2)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        sleep(1)
        self.dk.ck_cenlock_sts(3, timeout=2)
        self.sd_tester.change_car_mode(0x2)
        self.dk.ck_cenlock_sts(1, 3, timeout=10)

        self.sd_tester.change_car_mode(0)
        self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
        sleep(1)
        self.dk.ck_cenlock_sts(3, timeout=2)
        self.sd_tester.change_car_mode(0x2)
        sleep(2)
        self.dk.ck_cenlock_sts(3)

        self.restart_bgm_and_connect_service(ENTRY_SERVICE_CLIENT)  # 重启后上电即闭锁+工厂
        self.dk.ck_cenlock_sts(1, 3, timeout=10)

    @allure.title("重复解锁_原解锁_RKE解锁")
    @pytest.mark.full
    def test_caseid_1918654(self):
        self.dk.set_cenlock_sts(3)
        sleep(2)
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(2)
        self.dk.send_rke_unlock()
        self.ck_EntrySystemAudioLightInfo(1, 1)
        sleep(1)
        self.dk.send_rke_unlock()
        self.ck_EntrySystemAudioLightInfo(1, 1)
        
    @allure.title("重复闭锁_原闭锁_RKE闭锁")
    @pytest.mark.sanity
    def test_caseid_105223(self):
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(2)
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all(2)
        self.dk.send_rke_lock()
        self.ck_EntrySystemAudioLightInfo(2, 2, timeout=3)
        sleep(1)
        self.dk.send_rke_lock()
        self.ck_EntrySystemAudioLightInfo(2, 2)

    @allure.title("重复闭锁_原闭锁_远控闭锁")
    @pytest.mark.sanity
    def test_caseid_1918655(self):
        self.dk.set_cenlock_sts(1)
        self.dk.set_cenlock_sts(3)
        self.partner.empty_all(1.5)
        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 1, "source": 1})
        self.ck_EntrySystemAudioLightInfo(6, 6)
        sleep(1.5)
        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 1, "source": 1})
        self.ck_EntrySystemAudioLightInfo(6, 6)
        
    @allure.title("重复解锁_原解锁_远控解锁")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1683301?projectId=46')
    @pytest.mark.full
    def test_caseid_105211(self):
        self.dk.set_cenlock_sts(3)
        self.dk.set_cenlock_sts(1)
        self.partner.empty_all(1)
        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 0, "source": 1})
        self.ck_EntrySystemAudioLightInfo(5, 5)
        sleep(2)
        self.partner.send_method_request("CentralLockService_client", "SetDoorCloseLock", {"cmd": 0, "source": 1})
        self.ck_EntrySystemAudioLightInfo(5, 5)

    @allure.title("关门提示_主驾门开&其他门均有故障_离车关门落锁提示")
    @pytest.mark.sanity
    def test_caseid_1985275(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([1, 0, 0, 0, 0])      
        door=["Pass", "LeRe", "RiRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1], sleep_time=1)  
        self.dk.send_walk_away_lock_cmd()
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "CentralLockReminder", {"reminder": 7})
        self.ck_NotifyLockWarning(0, 3, ck_horn=False) 

    @allure.title("关门提示_副驾门开&其他门均有故障_离车关门落锁提示")
    @pytest.mark.smoke
    def test_caseid_1985276(self):
        self.dk.set_cenlock_sts(1)     
        self.dk.set_door_sts([0, 1, 0, 0, 0]) 
        door=["Drvr", "LeRe", "RiRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1], sleep_time=1)
        self.dk.send_walk_away_lock_cmd()
        self.ck_NotifyLockWarning(0, 3, ck_horn=False) 

    @allure.title("关门提示_左后门开&其他门均有故障_离车关门落锁提示")
    @pytest.mark.full
    def test_caseid_1985277(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 0, 1, 0, 0])      
        door=["Drvr", "Pass", "RiRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1], sleep_time=1)  
        self.dk.send_walk_away_lock_cmd()
        self.ck_NotifyLockWarning(0, 3, ck_horn=False) 
        
    @allure.title("关门提示_右后门开&其他门均有故障_离车关门落锁提示")
    @pytest.mark.full
    def test_caseid_1985278(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 0, 0, 1, 0])      
        door=["Drvr", "Pass", "LeRe"]
        for i in range(3):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1], sleep_time=1)  
        self.dk.send_walk_away_lock_cmd()
        self.ck_NotifyLockWarning(0, 3, ck_horn=False) 

    @allure.title("关门提示_尾门开&其他门有故障_离车关门落锁提示")
    @pytest.mark.full
    def test_caseid_1985279(self):  
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 0, 0, 0, 1])      
        door=["Drvr", "Pass", "LeRe", "RiRe"]
        for i in range(4):
            self.set_door_fault(door[i], [1, 1, 1, 1, 1], sleep_time=1)  
        self.dk.send_walk_away_lock_cmd()
        # self.ck_NotifyLockWarning(0, 3, ck_horn=False) 
        self.ck_NotifyLockWarning(ck_horn=False)  # 四门关闭，仅尾门打开，离车闭锁不触发reminder=7

    @allure.title("关门提示_四门闭锁但尾门解锁_尾门开_无离车关门落锁提示")
    @pytest.mark.sanity
    def test_caseid_1985280(self):  
        self.dk.set_cenlock_sts(2)  
        self.dk.set_door_sts([0, 0, 0, 0, 1])   
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetFaultInfo", {}, {"out": [{"fault": 0, "faultMsg": "", "door": 4}]}) # 无故障
        self.dk.send_walk_away_lock_cmd()
        sleep(3)
        self.ck_NotifyLockWarning(ck_horn=False)    
                
    @allure.title("关门提示_主驾门开&故障遍历_无离车关门落锁提示")
    @pytest.mark.full
    def test_caseid_1985281(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([1, 0, 0, 0, 0])  
        for j in range(5):
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.set_door_fault("Drvr", door_fault, sleep_time=2)
            self.dk.send_walk_away_lock_cmd()
            self.ck_NotifyLockWarning(ck_horn=False)
            
    @allure.title("关门提示_副驾门开&故障遍历_无离车关门落锁提示")
    @pytest.mark.full
    def test_caseid_1985282(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 1, 0, 0, 0]) 
        for j in range(5):
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.set_door_fault("Pass", door_fault, sleep_time=2)
            self.dk.send_walk_away_lock_cmd()
            self.ck_NotifyLockWarning(ck_horn=False)
            
    @allure.title("关门提示_左后门开&故障遍历_无离车关门落锁提示")
    @pytest.mark.full
    def test_caseid_1985283(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 0, 1, 0, 0])  
        for j in range(5):
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.set_door_fault("LeRe", door_fault, sleep_time=2)
            self.dk.send_walk_away_lock_cmd()
            self.ck_NotifyLockWarning(ck_horn=False)
            
    @allure.title("关门提示_右后门开&故障遍历_无离车关门落锁提示")
    @pytest.mark.full
    def test_caseid_1985284(self):
        self.dk.set_cenlock_sts(1)  
        self.dk.set_door_sts([0, 0, 0, 1, 0])   
        for j in range(5):
            door_fault=[0, 0, 0, 0, 0]
            door_fault[j]=1
            logger.info(f"打印当前循环值： door_fault={door_fault}")
            self.set_door_fault("RiRe", door_fault, sleep_time=1)
            self.dk.send_walk_away_lock_cmd()
            self.ck_NotifyLockWarning(ck_horn=False)

    @allure.title("关门提示_左后门开&童锁故障_离车关门落锁提示")
    @pytest.mark.sanity
    def test_caseid_1985290(self): # 偶现失败 SOA-24265
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        try:
            self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 3}]})
            self.dk.set_cenlock_sts(1)  
            self.dk.set_door_sts([0, 0, 1, 0, 0]) 
            self.ipdu.set(self.ipdu.bodycan.DdmBodyFr04, 'ChdPrtnLeftFailStsToHmi', 1) 
            self.partner.empty_all(2)
            self.dk.send_walk_away_lock_cmd() # 如果五门都开，只触发一次reminder=7的话，也只上报一次关门提示
            self.ck_NotifyLockWarning(0, 3, ck_horn=False) 
        except Exception as e:
            logger.info(f"error>>>{str(e)}")
            self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
            assert 0,str(e)
            pass
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal() 
        
    @allure.title("外锁下踩刹车解锁_当前kRemoteKey闭锁")
    @pytest.mark.sanity
    def test_caseid_1985656(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for type in range(10):
            logger.info(f"type=={type}")
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.dk.send_nfc_cmd()
            sleep(1)
            self.dk.set_cenlock_sts(1)
            sleep(1)
            self.partner.empty_all()
            self.dk.send_rke_lock()
            self.ck_CentralLockStatusInfo(3,1)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyTyp', type)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo1KeyConnectSts', 1)
            sleep(0.5)
            digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
            logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
            assert digitalKeyConnectedStatus[0]["type"] == type and digitalKeyConnectedStatus[0]["isConnected"] == True
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
            sleep(3)
            if type in [0,1,6,8]:
                self.dk.ck_cenlock_sts(3) 
            else:
                self.dk.ck_cenlock_sts(1) 
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [1,0,1,0,1,0,1,0,1,0,1,0]) 
        result = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert Counter(result).get(2) == 6
        
    @allure.title("外锁下踩刹车解锁_当前kKeyLessPassive闭锁")
    @pytest.mark.full
    def test_caseid_1985657(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for type in range(10):
            logger.info(f"type=={type}")
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.dk.send_nfc_cmd()
            sleep(1)
            self.dk.set_cenlock_sts(1)
            sleep(1)
            self.partner.empty_all()
            self.dk.update_keyinfos(2, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
            self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
            self.dk.press_door_outswitch(4, 2.2)
            self.ck_CentralLockStatusInfo(3,2)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo2KeyTyp', type)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo2KeyConnectSts', 1)
            sleep(0.5)
            digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
            logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
            assert digitalKeyConnectedStatus[1]["type"] == type and digitalKeyConnectedStatus[1]["isConnected"] == True
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
            sleep(2)
            if type in [0,1,6,8]:
                self.dk.ck_cenlock_sts(3) 
            else:
                self.dk.ck_cenlock_sts(1) 
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [1,0,1,0,1,0,1,0,1,0,1,0]) 
        result = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert Counter(result).get(2) == 6
     
    @allure.title("外锁下踩刹车解锁_当前kTelematices闭锁")
    @pytest.mark.full
    def test_caseid_1985658(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for type in range(10):
            logger.info(f"type=={type}")
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.dk.send_nfc_cmd()
            sleep(1)
            self.dk.set_cenlock_sts(1)
            sleep(1)
            self.partner.empty_all()
            self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 1})
            self.ck_CentralLockStatusInfo(3,7)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19, 'DigKeyConnectInfo3KeyTyp', type)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19,'DigKeyConnectInfo3KeyConnectSts', 1)
            sleep(0.5)
            digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
            logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
            assert digitalKeyConnectedStatus[2]["type"] == type and digitalKeyConnectedStatus[2]["isConnected"] == True
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
            sleep(2)
            if type in [0,1,6,8]:
                self.dk.ck_cenlock_sts(3) 
            else:
                self.dk.ck_cenlock_sts(1)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [1,0,1,0,1,0,1,0,1,0,1,0]) 
        result = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert Counter(result).get(2) == 6 
            
    @allure.title("外锁下踩刹车解锁_当前kApproach闭锁")
    @pytest.mark.full
    def test_caseid_1985659(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for type in range(10):
            logger.info(f"type=={type}")
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 0, "value": 2}]})
            self.dk.send_nfc_cmd()
            sleep(1)
            self.dk.set_cenlock_sts(1)
            sleep(1)
            self.partner.empty_all()
            self.dk.send_walk_away_lock_cmd()
            self.ck_CentralLockStatusInfo(3,9)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19, 'DigKeyConnectInfo4KeyTyp', type)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr19,'DigKeyConnectInfo4KeyConnectSts', 1)
            sleep(0.5)
            digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
            logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
            assert digitalKeyConnectedStatus[3]["type"] == type and digitalKeyConnectedStatus[3]["isConnected"] == True
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
            sleep(2)
            if type in [0,1,6,8]:
                self.dk.ck_cenlock_sts(3) 
            else:
                self.dk.ck_cenlock_sts(1)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [1,0,1,0,1,0,1,0,1,0,1,0])
        result = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert Counter(result).get(2) == 6 
           
    @allure.title("外锁下踩刹车解锁_当前kOutsideOthers闭锁")
    @pytest.mark.full
    def test_caseid_1985660(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for type in [2,3,4,5,7,9]:
            logger.info(f"type=={type}")
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.dk.send_nfc_cmd()
            sleep(1)
            self.dk.set_cenlock_sts(1)
            sleep(1)
            self.partner.empty_all()
            self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 3, "source": 3})
            self.ck_CentralLockStatusInfo(3,10)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyTyp', type)
            if type == 2:
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo1KeyConnectSts', 0)
            else:
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo1KeyConnectSts', 1)
            sleep(0.5)
            digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
            logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
            assert digitalKeyConnectedStatus[0]["type"] == type 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
            sleep(2)
            if type == 2:
                self.dk.ck_cenlock_sts(3) 
            else:
                self.dk.ck_cenlock_sts(1) 
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [1,0,1,0,1,0,1,0,1,0])
        result = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert Counter(result).get(2) == 5
    
    @allure.title("外锁下踩刹车解锁_当前nfc闭锁")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985661(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for type in [0,2,3,4,5,7,9]:
            logger.info(f"type=={type}")
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.dk.send_rke_unlock()
            sleep(1)
            self.partner.empty_all()
            self.dk.send_nfc_cmd()
            self.ck_CentralLockStatusInfo(3,12)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo2KeyTyp', type)
            if type == 0:
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo2KeyConnectSts', 0)
            else:
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo2KeyConnectSts', 1)
            sleep(0.5)
            digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
            logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
            assert digitalKeyConnectedStatus[1]["type"] == type 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
            sleep(2)
            if type == 0:
                self.dk.ck_cenlock_sts(3) 
            else:
                self.dk.ck_cenlock_sts(1) 
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [1,0,1,0,1,0,1,0,1,0,1,0])
        result = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert Counter(result).get(2) == 6
        
    @allure.title("非外锁下踩刹车不解锁_当前 kSpeedLocking闭锁")
    @pytest.mark.sanity
    def test_caseid_1985662(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for type in range(10):
            logger.info(f"type=={type}")
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.dk.send_nfc_cmd()
            sleep(1)
            self.dk.set_cenlock_sts(1)
            sleep(1)
            self.partner.empty_all()
            self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 2})
            self.ck_CentralLockStatusInfo(3,3)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyTyp', type)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo1KeyConnectSts', 1)
            sleep(0.5)
            digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
            logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
            assert digitalKeyConnectedStatus[0]["type"] == type 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
            sleep(2)
            self.dk.ck_cenlock_sts(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal() 
        # SetDoorCloseLock.source = 2,cmd = 1 发出pdu 
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0])
        self.bgm_eth_inter.ck_ordered_array("UsgModKeeperReq",[0])
        
        
    @allure.title("非外锁下踩刹车不解锁_当前kInteriorSwitches闭锁")
    @pytest.mark.full
    def test_caseid_1985663(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for type in range(10):
            logger.info(f"type=={type}")
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
            self.dk.set_door_opener_sts(1, 1, 1, 1, 1)
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.dk.send_nfc_cmd()
            sleep(1)
            self.dk.set_cenlock_sts(1)
            sleep(1)
            self.partner.empty_all()
            self.sd_tester.change_usage_mode(0xD)
            self.dk.set_drvr_seat_present()
            self.dk.set_four_door_unlock()
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtQf', 'GenQf1_AccurData')
            self.dk.set_door_opener_sts(1, 1)
            self.dk.set_door_opener_sts(2, 1)
            self.dk.set_door_opener_sts(3, 1)
            self.dk.set_door_opener_sts(4, 1)
            self.dk.set_door_opener_sts(5, 1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0x2C27)
            self.ck_CentralLockStatusInfo(3,4)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo2KeyTyp', type)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo2KeyConnectSts', 1)
            sleep(0.5)
            digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
            logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
            assert digitalKeyConnectedStatus[1]["type"] == type 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
            sleep(2)
            self.dk.ck_cenlock_sts(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal() 
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [])
        self.bgm_eth_inter.ck_ordered_array("UsgModKeeperReq",[0])
    
    @allure.title("外锁下踩刹车解锁_当前kRelocking闭锁")
    @pytest.mark.full
    def test_caseid_1985664(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for type in [0,2,3,4,5,7,9]:
            logger.info(f"type=={type}")
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            
            self.dk.set_cenlock_sts(1)
            self.partner.empty_all()
            sleep(0.5)
            self.partner.send_method_request(
                CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 0}
            )
            self.dk.ck_four_door_lock_cmd(2)
            self.ipdu.check(self.ipdu.backbonefr.CemBackBoneFr06, "LockgCenStsLockSt", 3)
            sleep(0.5)
            self.io.hood_door1_close()  # 接地
            self.io.hood_door2_open()  # 引擎盖open可能影响重锁功能(四门两盖需关闭)
            sleep(0.5)
            self.dk.send_rke_unlock()
            self.dk.ck_rke_resp(1, 0, "PreConditionOK", exec_type=2)
            self.dk.ck_four_door_lock_cmd(1)
            self.dk.set_four_door_unlock()
            self.dk.ck_cenlock_sts(0x1, 0x1)
            sleep(0.5)
            self.dk.ck_rke_resp(1, 0, "Success", exec_type=3)
            sleep(30)
            self.dk.ck_cenlock_sts(0x3, 0x5)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo2KeyTyp', type)
            if type == 0:
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo2KeyConnectSts', 0)
            else:
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo2KeyConnectSts', 1)
            sleep(0.5)
            digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
            logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
            assert digitalKeyConnectedStatus[1]["type"] == type 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
            sleep(2)
            if type == 0:
                self.dk.ck_cenlock_sts(3) 
            else:
                self.dk.ck_cenlock_sts(1)  
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [1,0,1,0,1,0,1,0,1,0,1,0])
        result = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert Counter(result).get(2) == 6 
        
    @allure.title("非外锁下踩刹车不解锁_当前kInsideOthers闭锁")
    @pytest.mark.full
    def test_caseid_1985665(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        for type in range(10):
            logger.info(f"type=={type}")
            
            self.sd_tester.change_usage_mode(1)
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
            self.dk.send_nfc_cmd()
            sleep(1)
            self.dk.set_cenlock_sts(1)
            sleep(1)
            self.partner.empty_all()
            self.partner.send_method_request(CENTRALLOCK_SERVICE_CLIENT, "SetDoorCloseLock", {"cmd": 1, "source": 3})
            self.ck_CentralLockStatusInfo(3,11)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyTyp', type)
            
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo1KeyConnectSts', 1)
            sleep(0.5)
            digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
            logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
            assert digitalKeyConnectedStatus[0]["type"] == type 
            self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
            sleep(2)
            self.dk.ck_cenlock_sts(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal() 
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [])   
        self.bgm_eth_inter.ck_ordered_array("UsgModKeeperReq",[0])
        
    @allure.title("外锁下踩刹车解锁_踏板被踩下后再次收到踏板被踩下的event不处理_Validity变化")
    @pytest.mark.sanity
    def test_caseid_1986161(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_rke_lock()
        self.ck_CentralLockStatusInfo(3,1)

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyTyp', 2)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo1KeyConnectSts', 1)
        sleep(0.5)
        digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
        logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
        assert digitalKeyConnectedStatus[0]["type"] == 2 and digitalKeyConnectedStatus[0]["isConnected"] == True
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        sleep(0.5)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 1})

        self.partner.empty_all(2) 
        self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        sleep(3)
        self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        sleep(2)
        self.partner.ck_no_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus")
        
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [1,0]) 
        result = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert Counter(result).get(2) == 1
        
    @allure.title("外锁下踩刹车解锁_validity=7&sts从0至1_处理踩刹车自动解锁")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1986163(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.change_usage_mode(1)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        self.dk.send_nfc_cmd()
        sleep(1)
        self.dk.set_cenlock_sts(1)
        sleep(1)
        self.partner.empty_all()
        self.dk.send_rke_lock()
        self.ck_CentralLockStatusInfo(3,1)

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18, 'DigKeyConnectInfo1KeyTyp', 2)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,'DigKeyConnectInfo1KeyConnectSts', 1)
        sleep(0.5)
        digitalKeyConnectedStatus = self.partner.send_request_and_return_resp(KEY_SERVICE_CLIENT, "GetDigitalKeyConnectedStatus", {})["out"]
        logger.info(f"digitalKeyConnectedStatus=={digitalKeyConnectedStatus}")
        assert digitalKeyConnectedStatus[0]["type"] == 2 and digitalKeyConnectedStatus[0]["isConnected"] == True
        sleep(2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 0)  
        self.partner.empty_all(1) 
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 1)
        self.partner.ck_s2s_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus", {"sts": 1})

        self.partner.empty_all(2)    
        self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd')
        sleep(2)
        self.partner.ck_no_event(CENTRALLOCK_SERVICE_CLIENT, "LockStatus")
        
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()    
        self.bgm_eth_inter.ck_signal_values("CenLockHmiReq", [1,0]) 
        result = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert Counter(result).get(2) == 1
        
######################################################################################################################################################## 
@allure.feature("SOA服务接口")
@allure.story("BGM应用/EntryService")         
class TestEntryServiceMockMcu(TestBase):            
    
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("EntryService", "client"),
                                     ("DoorService", "client"),
                                     ("TailGateService", "client")])
        self.partner.wait_for_service_reconnect(ENTRY_SERVICE_CLIENT) 

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
        
    @allure.title("关门提醒-车门处于无法关门角度_前置门开度条件检查_并通过DoorActionRequest.pos.action=Close触发关门提醒")
    @pytest.mark.sanity1
    def test_caseid_1989606(self):   
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1) # 硬线信号开 OpenCloseStatus
        self.partner.send_request_and_ck_resp(DOOR_SERVICE_CLIENT, "GetOpenCloseStatus", {"doors": [0]}, {"out": [{"id": 0, "isOpen": True}]}, timeout=5)     
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassPercPosn', 0)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiRePercPosn', 0)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeRePercPosn', 0)        
        for perposition in [7, 8, 9, 10]:
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', random.choice([0, 1, 3, 5]))
            self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPercPosn', perposition) # 设置车门当前位置
            sleep(1)
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 2)  # 事件触发 DoorActionRequest.action=Close
            self.partner.empty_all(2)
            if perposition <= 8:
                self.partner.ck_coming_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", {"warnnings": {"lock": 12, "reminder": 0}}, timeout=1.5)
                self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", {"warnnings": {"lock": 0, "reminder": 0}}) 
            else:
                self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout=2)
            
    @allure.title("关门提醒-车门处于无法关门角度_先触发DoorActionRequest.pos.action=Close_再满足前置门开度条件不执行关门提醒")
    @pytest.mark.full1
    def test_caseid_1989607(self):   
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr02, 'DoorDrvrSts', 1) # 硬线信号开 OpenCloseStatus        
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPercPosn', 10) # 设置车门当前位置    
        self.ipdu.set(self.ipdu.bodycan.PpodBodyFr01, 'DoorPassPercPosn', 0)
        self.ipdu.set(self.ipdu.bodycan.RpodBodyFr01, 'DoorRiRePercPosn', 0)
        self.ipdu.set(self.ipdu.bodycan.LpodBodyFr01, 'DoorLeRePercPosn', 0)         
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', random.choice([0, 1, 3, 5]))
        sleep(1)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr78, 'DoorOpenerDrvrReqDoorOpenerReq2', 2)  # 事件触发 DoorActionRequest.action=Close   
        self.partner.empty_all(1)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01, 'DoorDrvrPercPosn', 8) # 设置车门当前位置
        self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", timeout=4)                
        
######################################################################################################################################################## 
@allure.feature("SOA服务接口")
@allure.story("BGM应用/EntryService")  
@pytest.mark.aqx      
class TestEntryService_pressure(TestBase):

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass([("EntryService", "client"),
                                     ("CentralLockService", "client"),
                                     ("ChassisService", "client"),
                                     ("KeyService", "client"),
                                     ("AVPService", "server"),
                                     ("RPAAPAService", "server"),
                                     ("HornService", "client"),
                                     ("DoorService", "client"),
                                     ("PedalService", "client"),
                                     ("CTDService", "client"),
                                     ])
        self.partner.method_default_timeout = 0.1
        self.io.hood_door1_close()
        self.io.hood_door2_close()

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.ipdu.rx_flag_reset_all()
        self.ipdu.reset_check_results()
        self.sd_tester.change_car_mode(0)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')        
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        self.sd_tester.write_multi_ccp({94: 0x80, 98: 0x2, 97: 0x2, 10: 0x2, 481: 0x4, 578: 0x4, 142: 0x83})
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]})
        self.dk.set_pass_seat_notpresent()
        self.dk.set_secle_seat_notpresent()
        self.dk.set_secmid_seat_notpresent()
        self.dk.set_secri_seat_notpresent()
        self.dk.reset_bncm_digital_keyinfo()
        self.sd_tester.change_car_mode(0)
        self.dk.set_door_opener_sts(1, 1, 1, 1, 1)  # 设置bodycan上五个电动门均关闭
        self.io.init_bgm_HW()  # 用例开始前都先恢复5门关门状态，主驾无人，车门按钮未按下
        self.partner.empty_all()
        self.dk.empty_dk_data_queue()

    def after_each_func(self, ecu):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'BrkPedlPsdBrkPedlPsd', 'NoYes1_No')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr06, 'VehSpdLgtA', 0)
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(3)  # 避免防玩
        super().after_each_func(ecu, start=False)

    def bgm_sleep_and_awake(self):
        pass  # todo
    
    def ck_EntrySystemAudioLightInfo(self, audio, light, timeout=2.0):
        """校验进入系统声光提醒信息"""
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo", {"info": {"audio": audio, "light": light}}, timeout)
        self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "EntrySystemAudioLightInfo", {"info": {"audio": 0, "light": 0}}, timeout)
        self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetEntrySystemAudioLightInfo", {}, {"out": {"audio": 0, "light": 0}})
 
    def ck_NotifyLockWarning(self, lock=None, Reminder=None, ck_horn=True, timeout=2.0):
        """校验进入系统的报警信息"""
        if ck_horn:
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 0}, timeout=0.4)  # todo: 之后切换io输出校验
            self.partner.ck_s2s_event("HornService_client", "Status", {"sts": 1}, timeout=0.2)
        else:
            self.partner.ck_no_event("HornService_client", "Status")
        if lock is None and Reminder is None:
            self.partner.ck_no_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning")
        else:
            self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", {"warnnings": {"lock": lock, "reminder": Reminder}}, timeout)
            if lock != 0 or Reminder != 0:
            # 通知完成后将提示请求置为IDLE     
                self.partner.ck_s2s_event(ENTRY_SERVICE_CLIENT, "NotifyLockWarning", {"warnnings": {"lock": 0, "reminder": 0}})
                self.partner.send_request_and_ck_resp(ENTRY_SERVICE_CLIENT, "GetLockWarning", {}, {"out": {"lock": 0, "reminder": 0}})    
                                              
    @allure.title("压测_车辆非静止状态_解锁失败告警")
    @pytest.mark.full
    @pytest.mark.repeat(Times)
    def test_caseid_1980153(self):   
        self.dk.set_cenlock_sts(1)  
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr39, 'EpbLampReqEpbLampReq',0)
        self.ipdu.set(self.ipdu.backbonefr.BbmBackBoneFr04, 'EpbLampReqSecEpbLampReq',0)  
        self.partner.empty_all(1)
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}}) 
        self.ipdu.rx_flag_reset_msg("connectivitycanfd", "BgmConnectivityFr15") # 清空当前信号的值
        # ChassisService::VehicleMotionState 参数：0=未知无效值 1=静止 2=前进 3=后退  信号值：0=0，1/2/3=1，4/5=2，6/7=3
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 0)
        self.partner.empty_all(2)
        self.dk.press_door_inswitch(1, 1.5)
        self.ck_NotifyLockWarning(11, 0, ck_horn=False, timeout=3) 
        self.partner.send_request_and_ck_resp(CHASSIS_SERVICE_CLIENT,'getIndicatorLightReqStsValidity',{},{"out":{"value":1,"validity":0}}) 