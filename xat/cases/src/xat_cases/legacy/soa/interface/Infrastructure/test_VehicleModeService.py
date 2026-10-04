# -*- coding: utf-8 -*-
"""
@File        : test_VehicleModeService.py
@Author      : jingjing.wang
@Time        : 2023/05/10 15:00 PM
@Description : Test s2s interface about bonnet function
"""

import allure
import pytest
from time import sleep
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.soa_partner.src.partner_const import *
from xat_ecu.legacy.sdk.digital_key.digital_key_const import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.sdk.digital_key.digital_key_class import DigitalKey
from xat_cases.legacy.basetech.case_helper.diag_case_helper.DiagTestBase import SniffPacket
from copy import deepcopy
from datetime import datetime

default_ccp_list = DataTypeHanding.hexstr_to_inlist(
    "A3018006FD030101A302090304020102858B06010004050203000001048C800C0101010102010202010216010701010100030102028089020301010302736E03010101010101010302020202020A010103820201010102020103010201800202020201800000008182118003010103020102020302800102010102010104010101010101010203010103020101830201020201012902010402038002820103040128030A800104010201020203820402810101020101130301010101010205020101000302020304020202010101020001010101010101010180030A0101040607070A0A07070A0A00000400000201010101010280030301020000000202020102020200010102000000010300000100008100000000000000000000000000000080000000000000000000000100010100000200000080000000008403010100000000020100000000000000000002018001020101010101020103020180018002020101010101050380020601030110000002030100000000000000000000000000000000000000000000000000000002000000000001010301000000000200000000000000000000000000000000000000000000000000010201000000000085040102020201020202040301020201028004030101020201030101010202020101020101010101030000000180020201010202010202020102010302020101010101010101000103010201010502020204010101010301010402010201010101020101010101010100000000000001020301010109030101010202020101030104010401010101010201030105020001010101010101010101010101010101010101010101010202010101010102010101010201000001010401000000010100000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001030202080100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001010201020102020101020101010101010201010201010101010202010201010101020202020202010202010202010201010101020101010102010101000102010101000101010101020202010101020201010101010102020102010101010101010001010101010101020101010101020101010101010101010101010101010101010101020201020101010101010100000101010101010101020101010101010101010202000101010101010202020101010100000000000000000000000000000000000000000000000000000000000000000000020202020202020101010101010101020101010101010202020202010002020101020102020201020001")


USAGE_MODE_MAP = {
    0: "ABANDONED",
    1: "INACTIVE",
    2: "CONVENIENCE",
    11: "ACTIVE",
    13: "DRIVING",
}

CAR_MODE_MAP = {
    0: "NORMAL",
    1: "TRANSPORT",
    2: "FACTORY",
    3: "CRASH",
    5: "DYNO",
}


@allure.feature("SOA服务接口")
@allure.story("架构基础/VehicleModeService")
@pytest.mark.wjj
@pytest.mark.vmm
class TestManyVehicleModeService(TestBase):
    '''vmm起多个服务端'''
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass(
            [("VehicleModeService", "client"), ("KeyService", "client"), ("VehicleModeService", "client_1"),
             ("VehicleModeService", "client_2"),("VehicleModeService", "client_3"),("VehicleModeService", "client_4")])
        self.partner.method_default_timeout = 0.1
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]})

    def before_each_func(self, ecu, **kwargs):
        super().before_each_func(ecu, start=False)
        self.set_nopeople_incar()
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

    def after_each_func(self, ecu):
        self.io.brake_up()
        # todo 停止抓包
        self.bgmcli.stop_bgm_tcpdump()
        self.nucapp.bgm_diag_line_up()  # 链接诊断激活线
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": False},timeout=2)
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(3)  # 避免防玩
        self.ipdu.resume_all_bus_send()
        sleep(1)
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

        
    @allure.title("设置使用模式上切/优先级")
    @pytest.mark.full
    def test_caseid_1981762(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.set_cenlock_sts(0x3)  # 闭锁
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 1})
        self.partner.send_method_request('VehicleModeService_client_1', 'SetUsageModeUp', {"mode": 2})
        self.partner.send_method_request('VehicleModeService_client_2', 'SetUsageModeUp', {"mode": 11})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02,'UsgModKeeperReq', 11, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="UsgModKeeperReq",idle_value=0,trigger_values=[11])

    @allure.title("设置使用模式下切/优先级2,1,11")
    @pytest.mark.full
    def test_caseid_1981776(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.set_cenlock_sts(0x3)  # 闭锁
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 2})
        self.partner.send_method_request('VehicleModeService_client_1', 'SetUsageModeDown', {"mode": 1})
        self.partner.send_method_request('VehicleModeService_client_2', 'SetUsageModeDown', {"mode": 11})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02,'UsgModDwnSwtReq', 1, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="UsgModDwnSwtReq",idle_value=0,trigger_values=[1])

    @allure.title("设置使用模式下切/优先级非0值不判断优先级")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1984869(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.set_cenlock_sts(0x3)  # 闭锁
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 1})
        self.partner.send_method_request('VehicleModeService_client_1', 'SetUsageModeDown', {"mode": 0})
        self.partner.send_method_request('VehicleModeService_client_2', 'SetUsageModeDown', {"mode": 2})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="UsgModDwnSwtReq",idle_value=0,trigger_values=[1])
        
    @allure.title("设置使用模式下切/优先级2,11,13")
    @pytest.mark.full
    def test_caseid_1984866(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.set_cenlock_sts(0x3)  # 闭锁
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 11})
        self.partner.send_method_request('VehicleModeService_client_1', 'SetUsageModeDown', {"mode": 2})
        self.partner.send_method_request('VehicleModeService_client_2', 'SetUsageModeDown', {"mode": 13})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="UsgModDwnSwtReq",idle_value=0,trigger_values=[2])
        
    @allure.title("设置使用模式下切/优先级11,13")
    @pytest.mark.full
    def test_caseid_1984867(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.set_cenlock_sts(0x3)  # 闭锁
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request('VehicleModeService_client_1', 'SetUsageModeDown', {"mode": 11})
        self.partner.send_method_request('VehicleModeService_client_2', 'SetUsageModeDown', {"mode": 13})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="UsgModDwnSwtReq",idle_value=0,trigger_values=[11])
        
    @allure.title("设置使用模式下切/优先级单个调用")
    @pytest.mark.full
    def test_caseid_1984868(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.set_cenlock_sts(0x3)  # 闭锁
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 0})
        self.partner.empty_all(0.3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 1})
        self.partner.empty_all(0.3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 2})
        self.partner.empty_all(0.3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 11})
        self.partner.empty_all(0.3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 13})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="UsgModDwnSwtReq",period=0.2)
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="UsgModDwnSwtReq",idle_value=0,trigger_values=[1, 2, 11, 13])
        
        
@pytest.mark.wjj
@pytest.mark.vmm
@allure.feature("SOA服务接口")
@allure.story("架构基础/VehicleModeService")
class TestVehicleModeService(TestBase):
    '''常规vmm'''
    def before_class(self, ecu):
        super().before_class(self, ecu)
        self.dk = DigitalKey(self.ipdu, self.busapp, self.io, self.tc_config)
        self.partner = S2sBaseClass(
            [("VehicleModeService", "client"), ("KeyService", "client"),("PedalService", "client"),("VehicleSetStatusService", "client")])
        self.partner.method_default_timeout = 0.1
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetConfigInfo", {"infos": [{"key": 5, "value": 0}]})
        self.tcpdump = SniffPacket(save_path = "/root/bgm_log")
        self.flag=True # 标志位

    def before_each_func(self, ecu, **kwargs):
        super().before_each_func(ecu, start=False)
        self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkNotEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
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
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.dk.set_chassis_service_gear("P")
        sleep(0.2) 
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0},timeout=0.3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 1},timeout=0.3)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        self.io.brake_up()
        self.bgmcli.stop_bgm_tcpdump()# 停止抓包
        self.bgm_eth_inter.bgm_ssh.scp_bgm_log_to_local(bgm_log_name=self.bgm_eth_inter.pcap_name, del_flag=True)#case失败抓包文件会保留
        self.nucapp.bgm_diag_line_up()  # 链接诊断激活线
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode",
                                         {"isOpen": False},timeout=2)
        if ecu.get("testresult") != "Pass":
            logger.info("case失败，需等待5s让环境恢复")
            sleep(5)
        else:
            sleep(3)  # 避免防玩
        self.ipdu.resume_all_bus_send()
        sleep(1)
        self.partner.empty_all(1)
        self.flag=False
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.dk.stop_listen_dk_bgm_response()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def ck_CarModeChanged_and_GetCarMode(self, CarMode):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "CarModeChanged", {"mode": CarMode})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarMode", {},
                                              {"out": CarMode},timeout=0.2)

    def ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(self, isOpen, isValid):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "NotifyExhibitionModeSts",
                                  {"sts": {"isOpen": isOpen, "isValid": isValid}})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetExhibitionModeSts", {},
                                              {"out": {"isOpen": isOpen, "isValid": isValid}})

    def ck_CarModeDisplayChanged_and_GetCarModeDisplay(self, mode):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "CarModeDisplayChanged", {"mode": mode})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeDisplay", {}, {"out": mode},timeout=0.5)

    def ck_NotifyStartInhibitStatus_and_GetStartInhibitStatus(self, isInhibit):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "NotifyStartInhibitStatus", {"isInhibit": isInhibit})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetStartInhibitStatus", {},
                                              {"out": isInhibit},timeout=0.5)

    def ck_ConvenienceModeDuration_and_GetConvenienceModeDuration(self, Duration):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "ConvenienceModeDuration", {"duration": Duration})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetConvenienceModeDuration", {},
                                              {"out": Duration},timeout=0.2)

    def ck_UsageModeChanged_and_GetUsageMode(self, mode):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "UsageModeChanged", {"mode": mode})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageMode", {}, {"out": mode})

    def ck_UsageModeChangedValidity_and_GetUsageModeValidity(self, value, validity):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "UsageModeChangedValidity",
                                  {"mode": {"value": value, "validity": validity}})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageModeValidity", {},
                                              {"out": {"value": value, "validity": validity}})

    def ck_lvRelaySts_and_getLVRelaySts(self, ck_dict,timeout=1):
        """校验指定lvRelaySts事件，并请求getLVRelaySts"""
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "lvRelaySts", {"sts": ck_dict})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "getLVRelaySts", {}, {"out": ck_dict})

    def ck_CarModeChangedValidity_and_GetCarModeValidity(self, value, validity):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "CarModeChangedValidity",
                                  {"mode": {"value": value, "validity": validity}})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeValidity", {},
                                             {"out": {"value": value, "validity": validity}})  
        
    def ck_usageModeRemind_and_getUsageModeRemind(self, isKeyNotInCar=False, sts=0, wordRemind=0, audioRemind=False,
                                                  powerSts=0):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "usageModeRemind", {
            "remind": {"isKeyNotInCar": isKeyNotInCar, "sts": sts, "wordRemind": wordRemind, "audioRemind": audioRemind,
                       "powerSts": powerSts}}, timeout=2)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "getUsageModeRemind", {}, {
            "out": {"isKeyNotInCar": isKeyNotInCar, "sts": sts, "wordRemind": wordRemind, "audioRemind": audioRemind,
                    "powerSts": powerSts}}, timeout=2)
        
    def ck_FastStartStsInfo_and_GetFastStartStsInfo(self, sts):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "FastStartStsInfo",
                                  {"info": {"sts": sts}})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetFastStartStsInfo", {},
                                              {"out": {"sts":sts}})
        
    def SetUsageModeUp(self):
        while self.flag:
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 13},timeout=0.2)
            sleep(0.5)
    
    def SetUp(self):
        while self.flag:
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 13})
            sleep(1.5)
    
    def SetUsageModeUp_before(self):     
        self.dk.set_cenlock_sts(0x3)  # 闭锁
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetFindKeyZone", {"zone": 0})#看有没有找到有效钥匙
        for SetUsageModeUp in [2, 11]:
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": SetUsageModeUp})
            sleep(0.2)
            self.ck_UsageModeChanged_and_GetUsageMode(SetUsageModeUp)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ck_UsageModeChanged_and_GetUsageMode(13)
        thread = threading.Thread(target=self.SetUsageModeUp,daemon=True)
        thread.start()
   
    @allure.title("设置/通知/获取CarMode_从Normal切换至Factory/CarMode显示信息/重启evnet")
    @pytest.mark.full
    def test_caseid_1984288(self):
        self.dk.set_cenlock_sts(1) 
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
        sleep(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 2})
        self.ck_CarModeChanged_and_GetCarMode(2)
        self.ck_CarModeDisplayChanged_and_GetCarModeDisplay(1)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="CarModChgReq",period=0.2)
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="CarModChgReq",idle_value=4,trigger_values=[0,2])
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        self.ck_CarModeChanged_and_GetCarMode(2)
        self.ck_CarModeDisplayChanged_and_GetCarModeDisplay(1) 
        
    @allure.title("设置/通知/获取CarMode_从Normal切换至1,2,0,5/CarMode(带功能安全需求参数)Validity4")
    @pytest.mark.full
    def test_caseid_109424(self):
        self.dk.set_cenlock_sts(1) 
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
        self.partner.empty_all(0.1)
        for carmode in [1,2,0,5]:
            self.partner.empty_all(0.2)
            logger.info({f'现在是{carmode}'})
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": carmode})
            self.ck_CarModeChangedValidity_and_GetCarModeValidity(carmode, 0)
            self.ipdu.pause_all_bus_send()
            sleep(2)
            self.ck_CarModeChangedValidity_and_GetCarModeValidity(carmode, 4)
            self.ipdu.resume_all_bus_send()
            self.ck_CarModeChangedValidity_and_GetCarModeValidity(carmode, 0)

    @allure.title("设置/通知/获取Car Mode_从Normal切换至Crash切不成功/CarMode显示信息")
    @pytest.mark.full
    def test_caseid_109423(self):
        self.dk.set_cenlock_sts(1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 1})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
        self.ck_CarModeChanged_and_GetCarMode(0)
        self.partner.empty_all(0.5)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 3})
        self.partner.ck_no_event(VEHICLEMODESERVICE_CLIENT, "CarModeChanged")
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarMode", {},{"out": 0})
        self.partner.ck_no_event(VEHICLEMODESERVICE_CLIENT, "CarModeDisplayChanged")
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeDisplay", {}, {"out": 6})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="CarModChgReq",period=0.2)
        self.bgm_eth_inter.ck_ordered_array(signal_name="CarModChgReq",ck_array=[4])


    @allure.title("设置/通知/获取Car Mode_从Normal切换至Dyno/CarMode显示信息/重启evnet")
    @pytest.mark.full
    def test_caseid_109422(self):
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
        self.partner.empty_all(0.2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 5})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02,'CarModChgReq', 5, timeout=0.5) 
        self.ck_CarModeChanged_and_GetCarMode(5)
        self.ck_CarModeDisplayChanged_and_GetCarModeDisplay(5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="CarModChgReq",period=0.2)
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="CarModChgReq",idle_value=4,trigger_values=[5])
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        self.ck_CarModeChanged_and_GetCarMode(5)
        self.ck_CarModeDisplayChanged_and_GetCarModeDisplay(5)

    @allure.title(
        "设置/通知/获取CarMode_从Normal切换至 Transport/CarMode显示信息/重启event")
    @pytest.mark.smoke
    def test_caseid_109421(self):
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
        self.dk.set_cenlock_sts(0x1)  # 解锁
        sleep(0.2)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 1})
        self.ck_CarModeChanged_and_GetCarMode(1)
        self.ck_CarModeDisplayChanged_and_GetCarModeDisplay(3)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="CarModChgReq",period=0.2,deviation=0.3)
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="CarModChgReq",idle_value=4,trigger_values=[1])
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        self.ck_CarModeChanged_and_GetCarMode(1)
        self.ck_CarModeDisplayChanged_and_GetCarModeDisplay(3)

    @allure.title(
        "通知/获取CarModeCrash/CarMode(带功能安全需求参数)Validity4/CarMode显示信息/下电记忆")
    @pytest.mark.full
    def test_caseid_1980559(self):
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetCarMode', {"mode": 0})
        sleep(0.5)
        self.sd_tester.change_car_mode(3)
        self.ck_CarModeChanged_and_GetCarMode(3)
        self.ck_CarModeDisplayChanged_and_GetCarModeDisplay(7)
        self.ipdu.pause_bus_send("backbonefr")
        sleep(2)
        self.ck_CarModeChangedValidity_and_GetCarModeValidity(3, 4)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarMode", {}, {"out": 4},timeout=0.5)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeDisplay", {}, {"out": 0},timeout=0.5)
        self.ipdu.resume_bus_send("backbonefr")
        self.ck_CarModeChangedValidity_and_GetCarModeValidity(3, 0)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarMode", {}, {"out": 3},timeout=0.5)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeDisplay", {}, {"out": 7},timeout=0.5)

    @allure.title("设置/通知/获取展车模式_开/重启event")
    @pytest.mark.smoke
    def test_caseid_109262(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(502, 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", {"isOpen": False})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", {"isOpen": True})
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(True, True)
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21,'SetExhibitionModeReq',1, timeout=0.5)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SetExhibitionModeReq', [2, 1, 0])
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(True, True)

    @allure.title("设置/通知/获取展车模式_关_下电记忆")
    @pytest.mark.full
    def test_caseid_109261(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.sd_tester.write_single_ccp(502, 2)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'EpbStsEpbSts', 3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", {"isOpen": True})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetExhibitionMode", {"isOpen": False})
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(False, True)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('SetExhibitionModeReq', [1, 2, 0])
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(False, True)

    @allure.title("设置/通知/获取禁止车辆启动_True")
    @pytest.mark.sanity
    def test_caseid_1886035(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetStartInhibit", {"isInhibit": False})
        sleep(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetStartInhibit", {"isInhibit": True})
        self.ck_NotifyStartInhibitStatus_and_GetStartInhibitStatus(True)#原本写的是1s但是校验了event和get后费时大概200s总共的时长为1200
        sleep(0.7)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetStartInhibit", {"isInhibit": True})
        sleep(0.1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetStartInhibit", {"isInhibit": True})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('StartInhibitReq', [0, 1, 1, 0])
        

    @allure.title("设置/通知/获取禁止车辆启动_False_重启event")
    @pytest.mark.full
    def test_caseid_1886036(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetStartInhibit", {"isInhibit": True})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18,'StartInhibitReq',1) 
        sleep(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetStartInhibit", {"isInhibit": False})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr18,'StartInhibitReq', 0, timeout=0.5) 
        self.ck_NotifyStartInhibitStatus_and_GetStartInhibitStatus(False)
        sleep(0.7)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetStartInhibit", {"isInhibit": False})
        sleep(0.1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetStartInhibit", {"isInhibit": True})
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('StartInhibitReq', [1, 0, 1, 0])
        self.partner.empty_all()
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        self.ck_NotifyStartInhibitStatus_and_GetStartInhibitStatus(False)

    @allure.title("设置BatterySaver继电器_True1")
    @pytest.mark.full
    def test_caseid_1982234(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": False})
        sleep(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": True})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('BattSaveRlyProxyReq', [0, 1, 0])

    @allure.title("设置BatterySaver继电器_True11")
    @pytest.mark.full
    def test_caseid_1982235(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": False})
        sleep(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": True})
        sleep(0.1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": True})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('BattSaveRlyProxyReq', [0, 1, 0])

    @allure.title("设置BatterySaver继电器_True01")
    @pytest.mark.full
    def test_caseid_1886044(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": True})
        sleep(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": False})
        sleep(0.1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": True})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('BattSaveRlyProxyReq', [1, 1, 0])
        
    @allure.title("设置BatterySaver继电器_True1101")
    @pytest.mark.full
    def test_caseid_1985702(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": True})
        sleep(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": True})
        sleep(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": False})
        sleep(0.3)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": True})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('BattSaveRlyProxyReq', [1, 1, 0, 1, 0])

    @allure.title("设置BatterySaver继电器_True10")
    @pytest.mark.sanity
    def test_caseid_1982236(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": False})
        sleep(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": True})
        sleep(0.1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": False})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('BattSaveRlyProxyReq', [0, 1, 0])

    @allure.title("设置BatterySaver继电器_False0")
    @pytest.mark.full
    def test_caseid_1959954(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        # 00000bc000000001,拉tcpdmp回00
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": True})
        sleep(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetBatterySaverConnect", {"isConnect": False})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('BattSaveRlyProxyReq', [1, 0, 0])

    @allure.title("设置使用模式无钥匙_1")
    @pytest.mark.full
    def test_caseid_1886039(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 1})
        self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdDevFr02,'PrkgAssiSysRemPrkgSts', 12, timeout=0.5) 
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('PrkgAssiSysRemPrkgSts', [0]+[12]*6+[0])

    @allure.title("设置使用模式无钥匙_2超时5.5s")
    @pytest.mark.full
    def test_caseid_1886037(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 0})
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 2})
        sleep(6)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('PrkgAssiSysRemPrkgSts', [0]+[5]*28+[0])

    @allure.title("设置使用模式无钥匙_2当前usagmode为13")
    @pytest.mark.full
    def test_caseid_1886038(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 0})
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(13)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 2})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('PrkgAssiSysRemPrkgSts', [0,0])
        self.sd_tester.change_usage_mode(1)

    @allure.title("设置驻车舒享模式时间_服务重启PrkgCmftModTiCtrl为0")
    @pytest.mark.full
    # 0000000700000001,拉tcpdmp回00
    def test_caseid_1984865(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.kill_bgm_process("s2s_service")
        logger.info("s2s_service已kill")
        sleep(10)#保证服务连上了
        self.ck_ConvenienceModeDuration_and_GetConvenienceModeDuration(0)
        sleep(5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('PrkgCmftModTiCtrl', [0])
        
    @allure.title("设置/通知/获取驻车舒享模式时间_usagmode2/11/13有效随后下切PrkgCmftModTiCtrl为0_重启event")
    @pytest.mark.smoke
    # 前提为2,200下发200跳到usg0下发0跳到1不下发,前提2,0下发0跳转usg0不下跳到1不下发,前提2,255下发255跳到0下发0跳到1不下发
    def test_caseid_1886043(self):
        self.dk.set_chassis_service_gear("P")  # 设置P档
        self.sd_tester.change_car_mode(0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)#条件改变从>=20到>20
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)#通知DCDC状态为true
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.bgm_eth_inter.start_bgm_tcpdump()
        for usagemode in [2, 11, 13]:
            logger.info(f'现在usagmode是{usagemode}')
            for Duration in [200, 0, 255]:
                self.sd_tester.change_usage_mode(usagemode)#usgmode切换
                logger.info(f'现在Duration是{Duration}')
                sleep(0.1)
                self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetConvenienceModeDuration",
                                                 {"duration": Duration})#有效值
                sleep(0.1)
                if Duration == 0:
                    self.partner.ck_no_event(VEHICLEMODESERVICE_CLIENT, "ConvenienceModeDuration")
                    self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetConvenienceModeDuration", {},
                                                          {"out": 0})
                else:
                    self.ck_ConvenienceModeDuration_and_GetConvenienceModeDuration(Duration)
                self.partner.empty_all()
                for usagemode01 in [0, 1]:
                    logger.info(f'现在usagmode切换是{usagemode01}')
                    self.sd_tester.change_usage_mode(usagemode01)
                    if usagemode01 == 1 or Duration == 0:
                        self.partner.ck_no_event(VEHICLEMODESERVICE_CLIENT, "ConvenienceModeDuration")
                        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetConvenienceModeDuration",
                                                              {},
                                                              {"out": 0})
                    else:
                        self.ck_ConvenienceModeDuration_and_GetConvenienceModeDuration(0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('PrkgCmftModTiCtrl', [200,0,0,255,0]*3)
        self.partner.empty_all()
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        self.ck_ConvenienceModeDuration_and_GetConvenienceModeDuration(0)


    @allure.title("设置驻车舒享模式时间_usagmode_0/1无效")
    @pytest.mark.sanity
    def test_caseid_1886042(self):
        self.dk.set_chassis_service_gear("P")  # 设置P档
        self.sd_tester.change_car_mode(0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)#通知DCDC状态为true
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        self.bgm_eth_inter.start_bgm_tcpdump()
        for usagemode01 in [0, 1]:
            logger.info(f'现在usagmode切换是{usagemode01}')
            for duration in [200, 0]:
                self.sd_tester.change_usage_mode(usagemode01)
                logger.info(f'现在duration是{duration}')
                self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetConvenienceModeDuration",
                                                 {"duration": duration})
                self.partner.ck_no_event(VEHICLEMODESERVICE_CLIENT, "ConvenienceModeDuration")
                self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetConvenienceModeDuration", {},
                                                      {"out": 0})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('PrkgCmftModTiCtrl', [0,0])

    @allure.title("设置/通知/获取驻车舒享模式时间_初始值")
    @pytest.mark.full
    def test_caseid_1886041(self):
        self.dk.set_chassis_service_gear("P")  # 设置P档
        self.sd_tester.change_car_mode(0)
        self.ipdu.set(self.ipdu.propulsioncan.BecmPropFr15, 'DCChrgnHndlSts', 3)
        self.ipdu.set(self.ipdu.propulsioncan.EcmPropFr04, 'DispHvBattLvlOfChrg', 21.0)
        self.ipdu.set(self.ipdu.propulsioncan.CddIgmPropFr01, 'DcDcActvd', 1)#通知DCDC状态为true
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 1})
        for usagemode in [2, 11, 13]:
            logger.info(f'现在usagmode是{usagemode}')
            self.sd_tester.change_usage_mode(usagemode)
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetConvenienceModeDuration", {"duration": 10})
            sleep(0.2)
            if usagemode == 2:
                self.ck_ConvenienceModeDuration_and_GetConvenienceModeDuration(10)
            else:
                self.partner.ck_no_event(VEHICLEMODESERVICE_CLIENT, "ConvenienceModeDuration")
                self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetConvenienceModeDuration", {},
                                                      {"out": 10})
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
        self.ck_ConvenienceModeDuration_and_GetConvenienceModeDuration(0)
        self.partner.send_method_request(VEHICLESETSTATUS_CLIENT, "SetParkingComfortMode", {"modeSts": 0})

    @allure.title("通知/获取CarMode（带功能安全需求参数）乱序时间戳")
    @pytest.mark.smoke
    def test_caseid_1886046(self):
        self.sd_tester.change_car_mode(0)
        self.partner.empty_all(0.5)
        self.sd_tester.change_car_mode(1)
        A = self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "CarModeChangedValidity",
                                      {"mode": {"value": 1, "validity": 0}})["mode"]["sequenceTime"]['timestamp']
        B = self.partner.send_request_and_return_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeValidity",{})["out"]["sequenceTime"][
            'timestamp']  # 观察"timestamp"时间戳event/get相同
        B1 = self.partner.send_request_and_return_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeValidity",{})["out"]["sequenceTime"][
            'id']
        logger.info(f"----{B}")
        if A == B:
            assert True
        else:
            assert False
        self.sd_tester.change_car_mode(2)
        sleep(1)
        C = self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "CarModeChangedValidity",
                                      {"mode": {"value": 2, "validity": 0}})["mode"]["sequenceTime"]['timestamp']
        if int(C) - int(A) > 0:
            assert True
        else:
            assert False
        self.partner.empty_all()
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        C1 = self.partner.send_request_and_return_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeValidity",{},timeout=2)["out"]["sequenceTime"]['id']
        logger.info(f"超时问题点")
        C2 = self.partner.send_request_and_return_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeValidity",{})["out"]["sequenceTime"]['timestamp']

        logger.info(f"比较----{C1}--{C2}--")
        if abs(C1 - B1) > 0:
            if C2 < B:
                assert True
        else:
            assert False
        self.sd_tester.change_car_mode(0)

    @allure.title("通知/获取使用模式状态（带功能安全需求参数）乱序时间戳")
    @pytest.mark.sanity
    def test_caseid_1886047(self):
        self.sd_tester.change_usage_mode(11)
        self.partner.empty_all(0.5)
        self.sd_tester.change_usage_mode(2)
        A = self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "UsageModeChangedValidity",
                                      {"mode": {"value": 2, "validity": 0}})["mode"]["sequenceTime"]['timestamp']
        logger.info(f"A的时间戳{A}")
        B = self.partner.send_request_and_return_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageModeValidity",
                                                      {})["out"]["sequenceTime"][
            'timestamp']  # 观察"timestamp"时间戳event/get相同
        B1 = self.partner.send_request_and_return_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageModeValidity",
                                                       {})["out"]["sequenceTime"][
            'id']  # 观察"timestamp"时间戳event/get相同

        logger.info(f"B的时间戳{B}")
        if A == B:
            assert True
        else:
            assert False
        self.sd_tester.change_usage_mode(11)
        sleep(1)
        C = self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "UsageModeChangedValidity",
                                      {"mode": {"value": 11, "validity": 0}})["mode"]["sequenceTime"]['timestamp']
        logger.info(f"C的时间戳{C}")

        if int(C) - int(A) > 0:
            assert True
        else:
            assert False
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        C1 = self.partner.send_request_and_return_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageModeValidity",
                                                       {},timeout=2)["out"]["sequenceTime"][
            'id']
        C2 = self.partner.send_request_and_return_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageModeValidity",
                                                       {})["out"]["sequenceTime"][
            'timestamp']

        logger.info(f"比较----{C1}--{C2}--")
        if abs(C1 - B1) > 0:
            logger.info(f"比较----{C1}--{B1}--")
            if C2 < B:
                assert True
        else:
            assert False
        self.sd_tester.change_usage_mode(0)

    @allure.title("设置使用模式上切/下切/获取/通知使用模式状态（带功能安全需求参数）")
    @pytest.mark.sanity
    def test_caseid_1981282(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.set_cenlock_sts(0x3)  # 闭锁
        sleep(2)
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 1})
        self.partner.empty_all(0.5)#确保能拿到一帧1
        for SetUsageModeUp in [2, 11]:
            logger.info(f'现在上切使用模式是{SetUsageModeUp}')
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": SetUsageModeUp})
            self.ck_UsageModeChanged_and_GetUsageMode(SetUsageModeUp)
            self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(SetUsageModeUp, 0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 13})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="UsgModKeeperReq",idle_value=0,trigger_values=[1,2,11,13])
        self.ck_UsageModeChanged_and_GetUsageMode(13)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.dk.set_chassis_service_gear("P")
        for SetUsageModeDown in [11, 2, 1]:
            logger.info(f'现在下切使用模式是{SetUsageModeDown}')
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": SetUsageModeDown})
            self.ck_UsageModeChanged_and_GetUsageMode(SetUsageModeDown)
            self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(SetUsageModeDown, 0)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="UsgModDwnSwtReq",idle_value=0,trigger_values=[11,2,1])

    @allure.title("设置使用模式上切/下切/获取/通知使用模式状态（带功能安全需求参数）4/重启event")
    @pytest.mark.full
    def test_caseid_1984526(self):
        self.sd_tester.change_usage_mode(0)
        for SetUsageModeUp in [1, 2, 11, 13]:
            logger.info(f'现在上切使用模式是{SetUsageModeUp}')
            self.sd_tester.change_usage_mode(SetUsageModeUp)
            self.ipdu.pause_all_bus_send()
            sleep(2)
            self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(SetUsageModeUp, 4)
            self.ipdu.resume_all_bus_send()
            self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(SetUsageModeUp, 0)
        self.partner.empty_all()
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(11, 0)#无发动机信号置位所以13重启以后变成11
        
    @allure.title("设置使用模式上切/防跑飞保持调用13_7min中调用下切2保持不打断")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985432(self):
        self.SetUsageModeUp_before()
        sleep(30)
        self.ipdu.set_vehspd(10.0)
        sleep(0.2)#确保车速生效
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode":2})
        logger.info({'调用一帧2'})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageMode", {}, {"out": 13})
        sleep(370)
        self.bgm_eth_inter.start_bgm_tcpdump()
        logger.info({"抓包时间"})
        sleep(30)
        self.flag=False
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="UsgModKeeperReq",period=0.2)
        ck_signal_values = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert 35 <= ck_signal_values.count(13) <= 45
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.dk.set_chassis_service_gear("P")

    @allure.title("设置使用模式上切/防跑飞保持调用13_设置车辆运动状态有效性为无效_7min后再次上切13不响应2s后响应")
    @pytest.mark.full
    def test_caseid_1985435(self):
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 1)  # 获取车辆运动状态
        self.SetUsageModeUp_before()
        sleep(30)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt')
        sleep(35)
        self.ipdu.restore_crc(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt')
        sleep(400)
        self.bgm_eth_inter.start_bgm_tcpdump()
        logger.info({"抓包时间"})
        sleep(30)
        self.flag=False
        sleep(2.4)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 13})
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="UsgModKeeperReq",period=0.2)
        ck_signal_values = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert 35 <= ck_signal_values.count(13) <= 45
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.dk.set_chassis_service_gear("P")
        
    @allure.title("设置使用模式上切/防跑飞保持调用13_每1.5s调用一次13,7min后不进入stop状态")
    @pytest.mark.full
    def test_caseid_1985477(self):
        self.dk.set_cenlock_sts(0x3)  # 闭锁
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        for SetUsageModeUp in [2, 11]:
            logger.info(f'现在上切使用模式是{SetUsageModeUp}')
            sleep(0.3)
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": SetUsageModeUp})
            self.ck_UsageModeChanged_and_GetUsageMode(SetUsageModeUp)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ck_UsageModeChanged_and_GetUsageMode(13)
        thread = threading.Thread(target=self.SetUp,daemon=True)
        thread.start()
        sleep(410)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(20)
        self.flag=False
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="UsgModKeeperReq",period=0.2)
        ck_signal_values = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert 10 <= ck_signal_values.count(13) <= 15
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.dk.set_chassis_service_gear("P")

    @allure.title("设置使用模式上切/防跑飞保持调用13_7min后下切0_usgmode0保持10s后退出stop再次可处理上切")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985433(self):
        self.SetUsageModeUp_before()
        sleep(422)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')#mcu查看P档的信号
        self.sd_tester.tester_present()
        self.sd_tester.change_usage_mode(0)
        self.ck_UsageModeChanged_and_GetUsageMode(0)
        sleep(11)
        self.sd_tester.stop_tester_present()
        self.flag=False
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        ck_signal_values = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert 4 <= ck_signal_values.count(13) <= 8
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.dk.set_chassis_service_gear("P")
        
    @allure.title("设置使用模式上切/防跑飞保持调用13_7min后VehicleMotionState!=1退出stop再次可处理上切")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985434(self):
        self.SetUsageModeUp_before()
        sleep(422)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="UsgModKeeperReq",idle_value=0,trigger_values=[])
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(10)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 4)  # 获取车辆运动状态
        sleep(0.2)
        self.flag=False
        logger.info(f'线程发送setup停止')
        sleep(0.3)#确保性能导致时间有一点延迟,停止0.3s后再调用
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 1)  # 获取车辆运动状态
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 13})
        logger.info(f'发了一帧新的mode13')
        sleep(2)#确保包可以抓到这一帧信号
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="UsgModKeeperReq",period=0.2)
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="UsgModKeeperReq",idle_value=0,trigger_values=[13])
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.dk.set_chassis_service_gear("P")
        
    @allure.title("设置使用模式上切/防跑飞保持调用13_7min后成功下切11,2,1维持10s_不退出stop")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985431(self):
        self.SetUsageModeUp_before()
        sleep(422)
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(1)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 11})
        logger.info(f'第一次断开11')
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "UsageModeChanged", {"mode": 11})
        sleep(12)  
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 2})
        logger.info(f'第二次断开2')
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "UsageModeChanged", {"mode": 2})
        sleep(23)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 1})
        logger.info(f'第三次断开1')
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "UsageModeChanged", {"mode": 1})
        sleep(35)
        self.flag=False
        logger.info(f'线程发送setup停止')
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="UsgModKeeperReq",period=0.2)
        self.bgm_eth_inter.ck_period_signal_trigger(signal_name="UsgModKeeperReq",idle_value=0,trigger_values=[])
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.dk.set_chassis_service_gear("P")
        
    @allure.title("设置使用模式上切/防跑飞7min内下切11,2,1计时器重新计时")
    @pytest.mark.full
    def test_caseid_1985429(self):
        self.SetUsageModeUp_before()
        sleep(5)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)#设置发动机状态为Ini
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 11})
        logger.info(f'第11')
        self.ck_UsageModeChanged_and_GetUsageMode(11)
        self.partner.empty_all(0.2)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ck_UsageModeChanged_and_GetUsageMode(13)
        sleep(10)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 2})
        logger.info(f'第2')
        self.ck_UsageModeChanged_and_GetUsageMode(2)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 2})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ck_UsageModeChanged_and_GetUsageMode(13)
        sleep(15)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 1})
        logger.info(f'第1')
        self.ck_UsageModeChanged_and_GetUsageMode(1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 2})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ck_UsageModeChanged_and_GetUsageMode(13)
        sleep(400)
        self.bgm_eth_inter.start_bgm_tcpdump()
        logger.info(f'抓包开始')
        sleep(30)
        self.flag=False
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        logger.info(f'抓包结束')
        self.bgm_eth_inter.ck_period_time(signal_name="UsgModKeeperReq",period=0.2, deviation= 0.3)
        ck_signal_values = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert 35 <= ck_signal_values.count(13) <= 45
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.dk.set_chassis_service_gear("P")
        
    @allure.title("复现bug_32249")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985381(self):
        # self.io.drvr_door_close()#门关
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatQf', 3)  # 制动踏板位置
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 0)#未踩下刹车
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.dk.set_cenlock_sts(0x3)  # 闭锁
        self.dk.update_keyinfos(1, [KeyInfo(KeyType.BLE_Key, key_id1, 0x5)])
        self.partner.send_method_request(KEY_SERVICE_CLIENT, "SetFindKeyZone", {"zone": 0})#看有没有找到有效钥匙
        self.dk.set_chassis_service_gear('P')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')#mcu查看P档的信号
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 11})
        self.ck_UsageModeChanged_and_GetUsageMode(11)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)
        self.ck_UsageModeChanged_and_GetUsageMode(13)
        sleep(2)
        for i in range(10):
            sleep(0.3)
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeUp', {"mode": 13})
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, 'SetUsageModeDown', {"mode": 1})
        self.ck_UsageModeChanged_and_GetUsageMode(1)
        sleep(0.2)#下切信号置位维持0.2ms
        self.dk.set_cenlock_sts(0x1)  # 解锁
        self.io.drvr_door_open()#门开
        # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 25600)#踩下刹车50%
        self.ck_UsageModeChanged_and_GetUsageMode(2)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageMode", {}, {"out": 2})
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.dk.set_chassis_service_gear("P")
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr08, 'BrkPedlrRatPerc', 0)#踩下刹车50%
        
    @allure.title("设置使用模式上切/防跑飞持续调用13_7min内切换VehicleMotionState!=1重新计时")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985430(self):
        self.SetUsageModeUp_before()
        sleep(10)
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 4)  # 获取车辆运动状态
        sleep(0.2)
        logger.info(f'standstill切换')
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 1)  # 获取车辆运动状态
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageMode", {}, {"out": 13})
        sleep(400)     
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(30)
        self.flag=False
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="UsgModKeeperReq",period=0.2)
        ck_signal_values = self.bgm_eth_inter.get_signal_values("UsgModKeeperReq")
        assert 38 <= ck_signal_values.count(13) <= 43
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 0)
        self.ipdu.set_vehspd(0)
        self.dk.set_chassis_service_gear("P")

    @allure.title("设置使用模式无钥匙_2/3s后usagmode为13")
    @pytest.mark.sanity
    def test_caseid_1979661(self):  
        self.sd_tester.tester_present()
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 0})
        self.partner.empty_all(0.2)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 2})
        sleep(3)
        # self.sd_tester.change_usage_mode(13)
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr00, 'EngSt1WdStsEngSt1WdSts', 5)#服务上13
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.sd_tester.stop_tester_present()
        self.bgm_eth_inter.ck_period_time(signal_name="PrkgAssiSysRemPrkgSts",period=0.2, deviation=0.3, permit_fail_times=3)
        ck_signal_values = self.bgm_eth_inter.get_signal_values("PrkgAssiSysRemPrkgSts")
        assert 10 <= ck_signal_values.count(5) <= 30
        
    @allure.title("设置使用模式无钥匙_2/5.5s内再次调用2计时器重新计时")
    @pytest.mark.full
    def test_caseid_1985372(self):  
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 0})
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.empty_all(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 2})#20个5
        sleep(4)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 2})#打断再发15个5
        sleep(3)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="PrkgAssiSysRemPrkgSts",period=0.2, deviation=0.3, permit_fail_times=3)
        ck_signal_values = self.bgm_eth_inter.get_signal_values("PrkgAssiSysRemPrkgSts")
        assert 33 <= ck_signal_values.count(5) <= 36

    @allure.title("获取/通知CarMode（带功能安全需求参数）Validity重启")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1980949(self):
        self.dk.set_cenlock_sts(0x1)  # 解锁
        self.sd_tester.change_car_mode(1)
        self.partner.empty_all(0.2)
        self.sd_tester.change_car_mode(0)
        self.ck_CarModeChangedValidity_and_GetCarModeValidity(0,0)
        self.ipdu.pause_all_bus_send()
        sleep(2)
        self.ck_CarModeChangedValidity_and_GetCarModeValidity(0,4)
        self.kill_bgm_process('s2s_service')
        logger.info({'进程'})
        sleep(3)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeValidity", {},
                                             {"out": {"value": 4, "validity": 0}},timeout=10)
        # self.ck_CarModeChangedValidity_and_GetCarModeValidity(4,4,timeout=10)#当前usgmode为0不检测超时所以4,4拿不到
        self.ipdu.resume_all_bus_send()
        self.sd_tester.change_car_mode(1)
        self.ck_CarModeChangedValidity_and_GetCarModeValidity(1,0)

    @allure.title("获取/通知使用模式状态（带功能安全需求参数）Validity重启")
    @pytest.mark.full
    def test_caseid_1981326(self):
        self.sd_tester.change_usage_mode(2)
        self.partner.empty_all(0.2)
        self.sd_tester.change_usage_mode(1)
        self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(1,0)
        self.ipdu.pause_all_bus_send()
        sleep(2)
        self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(1,4)
        self.kill_bgm_process('s2s_service')
        logger.info({'进程'})
        sleep(5)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageModeValidity", {},
                                             {"out": {"value": 0, "validity": 0}},timeout=5)
        # self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(0,4,timeout=10)#当前usgmode为0不检测超时所以4,4拿不到
        self.ipdu.resume_all_bus_send()
        self.sd_tester.change_usage_mode(1)
        self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(1,0)
        
    @allure.title("获取/通知使用模式用户提醒_重启event")
    @pytest.mark.full
    def test_caseid_1984556(self):
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        self.ck_usageModeRemind_and_getUsageModeRemind(False, 0, 0, False, 0)
        
    @allure.title("设置PowerOutlet继电器_usgmode遍历")
    @pytest.mark.smoke
    @pytest.mark.failed
    def test_caseid_1984620(self):
        self.sd_tester.tester_present()
        self.bgm_eth_inter.start_bgm_tcpdump()
        for usgmode in [0, 1, 2, 11, 13]:
            self.sd_tester.change_usage_mode(usgmode)
            logger.info(f"现在usgmode是{usgmode}")
            sleep(0.1)
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 0})
            logger.info(f"现在开始下发第一帧0")
            self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21,'RlyPwrCmdProxyReq',0, timeout=0.5)
            sleep(0.5)
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 1})
            sleep(0.2)
            if usgmode !=1 :
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21,'RlyPwrCmdProxyReq',0, timeout=0.5)
            else:
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21,'RlyPwrCmdProxyReq',1,timeout=1)#3秒信号会回0
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21,'RlyPwrCmdProxyReq',0,timeout=3)#3秒信号会回0
            sleep(3.5)
            self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 2})
            sleep(0.2)
            if usgmode !=1 :
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21,'RlyPwrCmdProxyReq',0, timeout=0.5)
            else:
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21,'RlyPwrCmdProxyReq',2,timeout=1)#3秒信号会回0
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21,'RlyPwrCmdProxyReq',0,timeout=3)#3秒信号会回0
            sleep(3.5)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('RlyPwrCmdProxyReq', [0, 0, 1, 1, 1, 1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0])
        self.sd_tester.stop_tester_present()
        
    @allure.title("设置PowerOutlet继电器_调用过程中切换usgmode")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1985236(self):
        self.sd_tester.tester_present()
        for req in [1, 2]:
            for usage_mode1 in [0, 2, 11, 13]:
                logger.info(f"现在usgmode是{usage_mode1}")
                self.bgm_eth_inter.start_bgm_tcpdump()
                self.sd_tester.change_usage_mode(1)
                self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": req})
                sleep(1.2)
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21,'RlyPwrCmdProxyReq',req, timeout=0.5)
                self.sd_tester.change_usage_mode(usage_mode1)
                sleep(0.2)
                self.ipdu.check(self.ipdu.infocanfd.BgmInfoCanFdFr21,'RlyPwrCmdProxyReq',0,timeout=1)
                self.sd_tester.change_usage_mode(2)
                sleep(1.2)
                self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
                self.bgm_eth_inter.ck_signal_values('RlyPwrCmdProxyReq', [req, req, req, 0])
        self.sd_tester.stop_tester_present()   
            
    @allure.title("设置PowerOutlet继电器_2多次调用")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1984778(self):
        self.sd_tester.tester_present()
        self.sd_tester.change_usage_mode(1) 
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 2})
        sleep(1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 2})
        sleep(1.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 2})
        sleep(2.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 2})
        sleep(4)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_period_time(signal_name="PrkgAssiSysRemPrkgSts",period=0.5, deviation=0.3, permit_fail_times=3)
        ck_signal_values = self.bgm_eth_inter.get_signal_values("RlyPwrCmdProxyReq")
        assert  1 <= ck_signal_values.count(0) <= 2
        assert 16 <= ck_signal_values.count(2) <= 19
        self.sd_tester.stop_tester_present() 
            
    @allure.title("设置PowerOutlet继电器_1,2超时3s可打断")
    @pytest.mark.full
    def test_caseid_1984776(self):
        self.sd_tester.tester_present()
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 1})
        sleep(4)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 0})
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 2})
        sleep(4)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 0})
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 1})
        sleep(4)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        ck_signal_values = self.bgm_eth_inter.get_signal_values("RlyPwrCmdProxyReq")
        assert ck_signal_values.count(0) == 5
        assert ck_signal_values.count(2) == 6
        assert ck_signal_values.count(1) == 12
        self.sd_tester.stop_tester_present() 
            
    @allure.title("设置PowerOutlet继电器_1多次调用")
    @pytest.mark.full
    def test_caseid_1984649(self):
        self.sd_tester.tester_present()
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 1})
        sleep(1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 1})
        sleep(1.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 1})
        sleep(2.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 1})
        sleep(4)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        ck_signal_values = self.bgm_eth_inter.get_signal_values("RlyPwrCmdProxyReq")
        assert 16 <=ck_signal_values.count(1) <= 18
        self.sd_tester.stop_tester_present() 

    @allure.title("设置PowerOutlet继电器_2打断")
    @pytest.mark.sanity
    def test_caseid_1984626(self):
        self.sd_tester.tester_present()
        self.sd_tester.change_usage_mode(1)
        self.bgm_eth_inter.start_bgm_tcpdump()
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 1})
        sleep(1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 0})
        sleep(0.7)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 2})
        sleep(0.5)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 0})
        sleep(1)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetPowerOutletConnect", {"req": 1})
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()
        self.bgm_eth_inter.ck_signal_values('RlyPwrCmdProxyReq', [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 0])
        self.sd_tester.stop_tester_present()

    @allure.title("获取_通知低压继电器_服务启动")
    @pytest.mark.full
    def test_caseid_1983212(self):
        self.sd_tester.change_usage_mode(0)
        self.partner.send_method_request(VEHICLEMODESERVICE_CLIENT, "SetUsageModeWithoutKey", {"mode": 1})
        self.ck_lvRelaySts_and_getLVRelaySts(
            {"kl15RlySts": 2, "battSaverRlySts": False, "pwrOutletRlySts": False, "kl15ExtRlySts": False,
             "kl15_3RlySts": False, "kl15RlyFbSts": False, "fuPmpRlyCmdSts": 2, "climRlyCmdSts": False})
        self.sd_tester.change_usage_mode(13)
        self.ck_lvRelaySts_and_getLVRelaySts(
            {"kl15RlySts": 1, "battSaverRlySts": True, "pwrOutletRlySts": True, "kl15ExtRlySts": True,
             "kl15_3RlySts": True, "kl15RlyFbSts": False, "fuPmpRlyCmdSts": 1, "climRlyCmdSts": True})
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        self.ck_lvRelaySts_and_getLVRelaySts(
            {"kl15RlySts": 1, "battSaverRlySts": True, "pwrOutletRlySts": True, "kl15ExtRlySts": True,
             "kl15_3RlySts": True, "kl15RlyFbSts": False, "fuPmpRlyCmdSts": 1, "climRlyCmdSts": True})
          
    @allure.title("获取_通知快速启动状态")
    @pytest.mark.smoke
    def test_caseid_1985528(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'UsgModChgReqFromBLE', 1)
        self.partner.empty_all(0.5)
        for sts in range(2):
            logger.info({f'现在是{sts}'})
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'UsgModChgReqFromBLE', sts)
            self.ck_FastStartStsInfo_and_GetFastStartStsInfo(sts)
            
    @allure.title("获取_通知快速启动状态_初始值")
    @pytest.mark.full
    def test_caseid_1985529(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'UsgModChgReqFromBLE', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'UsgModChgReqFromBLE', 1)
        self.ck_FastStartStsInfo_and_GetFastStartStsInfo(1)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT,resume_all_bus=False)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetFastStartStsInfo", {},
                                              {"out": {"sts":2}}) 
        self.ipdu.resume_all_bus_send()
        self.ck_FastStartStsInfo_and_GetFastStartStsInfo(1)        
            
@pytest.mark.wjj
@pytest.mark.vmm
@allure.feature("SOA服务接口")
@allure.story("架构基础/VehicleModeService")
class TestVehicleModeServiceSetup(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, udp_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("VehicleModeService", "client")])
        sleep(5)

    def after_class(self, ecu):
        try:
            self.partner.stop_operators()
        except Exception as e:
            logger.error(f"{str(e)}")
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.empty_all(1)

    def after_each_func(self, ecu):
        self.bgmcli.stop_bgm_tcpdump()# 停止抓包
        super().after_each_func(ecu)

    def ck_CarModeChangedValidity_and_GetCarModeValidity(self, value, validity, timeout=3):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "CarModeChangedValidity",
                                  {"mode": {"value": value, "validity": validity}})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeValidity", {},
                                              {"out": {"value": value, "validity": validity}})

    def ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(self, isOpen, isValid, timeout=3):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "NotifyExhibitionModeSts",
                                  {"sts": {"isOpen": isOpen, "isValid": isValid}})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetExhibitionModeSts", {},
                                              {"out": {"isOpen": isOpen, "isValid": isValid}})

    def set_usageModeRemind_signal(self, KeyNotPrsntMsgToDrvr=None, StrtMsgToDrvr=None, VehNotParkInfoWarn=None,
                                   AudWarn=None, StrtInProgs=None):
        if KeyNotPrsntMsgToDrvr is not None:
            logger.info(f"设置ButtonMidRi1--{KeyNotPrsntMsgToDrvr,StrtMsgToDrvr,VehNotParkInfoWarn,AudWarn,StrtInProgs}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr14, 'KeyNotPrsntMsgToDrvr', KeyNotPrsntMsgToDrvr)
        if StrtMsgToDrvr is not None:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr07, 'StrtMsgToDrvr', StrtMsgToDrvr)
        if VehNotParkInfoWarn is not None:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr19, 'VehNotParkInfoWarn', VehNotParkInfoWarn)
        if AudWarn is not None:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr25, 'AudWarn', AudWarn)
        if StrtInProgs is not None:
            self.ipdu.set(self.ipdu.bodycan.CemBodyFr63, 'StrtInProgs', StrtInProgs)
        sleep(1)

    def ck_usageModeRemind_and_getUsageModeRemind(self, isKeyNotInCar=False, sts=0, wordRemind=0, audioRemind=False,
                                                  powerSts=0):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "usageModeRemind", {
            "remind": {"isKeyNotInCar": isKeyNotInCar, "sts": sts, "wordRemind": wordRemind, "audioRemind": audioRemind,
                       "powerSts": powerSts}}, timeout=2)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "getUsageModeRemind", {}, {
            "out": {"isKeyNotInCar": isKeyNotInCar, "sts": sts, "wordRemind": wordRemind, "audioRemind": audioRemind,
                    "powerSts": powerSts}}, timeout=2)

    def ck_noevent_usageModeRemind_and_getUsageModeRemind(self, isKeyNotInCar, sts, wordRemind, audioRemind, powerSts):
        self.partner.ck_no_event(VEHICLEMODESERVICE_CLIENT, "usageModeRemind")
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "getUsageModeRemind", {}, {
            "out": {"isKeyNotInCar": isKeyNotInCar, "sts": sts, "wordRemind": wordRemind, "audioRemind": audioRemind,
                    "powerSts": powerSts}})

    def ck_CarModeDisplayChanged_and_GetCarModeDisplay(self, mode):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "CarModeDisplayChanged", {"mode": mode})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeDisplay", {}, {"out": mode})

    def ck_EnergylevelChanged_and_GetEnergyLevelSts(self, energyLevel, subEnergyLeve):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "EnergylevelChanged",
                                  {"energylevel": {"energyLevel": energyLevel, "subEnergyLevel": subEnergyLeve}})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetEnergyLevelSts", {},
                                              {"out": {"energyLevel": energyLevel, "subEnergyLevel": subEnergyLeve}})

    def ck_PowerlevelChanged_and_GetPowerlevel(self, powerLevel, subpowerLevel):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "PowerlevelChanged",
                                  {"powerlevel": {"powerLevel": powerLevel, "subpowerLevel": subpowerLevel}})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetPowerlevel", {},
                                              {"out": {"powerLevel": powerLevel, "subpowerLevel": subpowerLevel}})

    def ck_UsageModeChanged_and_GetUsageMode(self, mode):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "UsageModeChanged", {"mode": mode})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageMode", {}, {"out": mode})

    def ck_UsageModeChangedValidity_and_GetUsageModeValidity(self, value, validity):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "UsageModeChangedValidity",
                                  {"mode": {"value": value, "validity": validity}})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageModeValidity", {},
                                              {"out": {"value": value, "validity": validity}})

    def ck_ConvenienceModeDuration_and_GetConvenienceModeDuration(self, Duration, timeout=3):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "ConvenienceModeDuration", {"Duration": Duration})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetConvenienceModeDuration", {},
                                              {"out": Duration})

    def ck_lvRelaySts_and_getLVRelaySts(self, ck_dict):
        """校验指定lvRelaySts事件，并请求getLVRelaySts"""
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "lvRelaySts", {"sts": ck_dict})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "getLVRelaySts", {}, {"out": ck_dict})
    
    def ck_FastStartStsInfo_and_GetFastStartStsInfo(self, sts):
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "FastStartStsInfo",
                                  {"info": {"sts": sts}})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetFastStartStsInfo", {},
                                              {"out": sts})   
        
    @allure.title("通知/获取CarMode（带功能安全需求参数）初始值/重启evnet")
    @pytest.mark.full
    def test_caseid_1988587(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1CarModSts1',4)
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        sleep(10)
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "CarModeChangedValidity",
                                  {"mode": {"value": 4, "validity": 1}})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeValidity", {},
                                             {"out": {"value": 4, "validity": 1}})  
        
    @allure.title("通知/获取CarMode（不带功能安全需求参数）初始值/重启evnet")
    @pytest.mark.full
    def test_caseid_1988586(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02,'VehModMngtGlbSafe1CarModSts1',4)
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        sleep(10)
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "CarModeChanged", {"mode": 4})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarMode", {},
                                              {"out": 4})
        
    @allure.title("通知/获取CarMode显示信息_初始值/重启evnet")
    @pytest.mark.full
    def test_caseid_1988588(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr14, 'CarModDispdWdDispd', 0)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        sleep(10)
        self.ck_CarModeDisplayChanged_and_GetCarModeDisplay(0)
        
    @allure.title("获取_通知低压继电器IgnRlyFb")
    @pytest.mark.full
    def test_caseid_1960027(self):
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr04, 'IgnRlyFb', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr04, 'IgnRlyFb', 1)
        self.ck_lvRelaySts_and_getLVRelaySts({"kl15RlyFbSts": True})
        sleep(0.5)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr04, 'IgnRlyFb', 0)
        self.ck_lvRelaySts_and_getLVRelaySts({"kl15RlyFbSts": False})

    @allure.title("获取_通知低压继电器FuPmpRlyCmd")
    @pytest.mark.full
    def test_caseid_1960019(self):
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'FuPmpRlyCmd', 0)
        for i in range(1, 4):
            self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'FuPmpRlyCmd', i)
            logger.info(f"第{i}次")
            self.ck_lvRelaySts_and_getLVRelaySts({"fuPmpRlyCmdSts": i})
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'FuPmpRlyCmd', 0)
        self.ck_lvRelaySts_and_getLVRelaySts({"fuPmpRlyCmdSts": 0})

    @allure.title("获取_通知低压继电器ClimRlyCmd")
    @pytest.mark.full
    def test_caseid_1960018(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr04, 'ClimRlyCmd', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr04, 'ClimRlyCmd', 1)
        self.ck_lvRelaySts_and_getLVRelaySts({"climRlyCmdSts": True})
        sleep(0.5)
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr04, 'ClimRlyCmd', 0)
        self.ck_lvRelaySts_and_getLVRelaySts({"climRlyCmdSts": False})
        
    @allure.title("通知/获取低压继电器状态总线_默认值")
    @pytest.mark.full
    def test_caseid_1987171(self):
        self.ipdu.set(self.ipdu.bodycan.CemBodyFr04, 'ClimRlyCmd', 1)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdFr18, 'FuPmpRlyCmd', 1)
        self.ipdu.set(self.ipdu.infocanfd.BgmInfoCanFdDevFr04, 'IgnRlyFb', 1)
        self.ipdu.set(self.ipdu.connectivitycanfd.BgmConnectivityFr10,'RlyPwrDistbnCmd1WdPreBattSaveCmd', 1)
        self.ck_lvRelaySts_and_getLVRelaySts({"kl15RlyFbSts": True,"fuPmpRlyCmdSts": 1,"climRlyCmdSts": True,"BattSaverRlyPrewarn": True})
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
        sleep(10)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "getLVRelaySts", {}, {"out": {"kl15RlyFbSts": False,"fuPmpRlyCmdSts": 0,
                                                                                               "climRlyCmdSts": False,"BattSaverRlyPrewarn": False}},timeout=5)
        self.ipdu.resume_all_bus_send()
        self.ck_lvRelaySts_and_getLVRelaySts({"kl15RlyFbSts": True,"fuPmpRlyCmdSts": 1,"climRlyCmdSts": True,"BattSaverRlyPrewarn": True})
        
    @allure.title("通知/获取低压继电器状态BattSaverRlyPrewarn")
    @pytest.mark.sanity
    def test_caseid_1987178(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BgmConnectivityFr10,'RlyPwrDistbnCmd1WdPreBattSaveCmd', 0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.connectivitycanfd.BgmConnectivityFr10,'RlyPwrDistbnCmd1WdPreBattSaveCmd', 1)
        self.ck_lvRelaySts_and_getLVRelaySts({"BattSaverRlyPrewarn": True})
        self.ipdu.set(self.ipdu.connectivitycanfd.BgmConnectivityFr10,'RlyPwrDistbnCmd1WdPreBattSaveCmd', 0)
        self.ck_lvRelaySts_and_getLVRelaySts({"BattSaverRlyPrewarn": False})

    @allure.title("获取/通知使用模式状态（带功能安全需求参数）Validity7")
    @pytest.mark.full
    def test_caseid_1981335(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 0)
        self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(0, 0)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts')
        for E2E in [1, 2, 0, 11, 13]:
            logger.info(f"现在是{E2E}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', E2E)
            sleep(0.2)
            self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(E2E, 7)
        self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts')
        self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(13, 0)
        
    @allure.title("获取/通知使用模式状态（不带功能安全需求参数）_初始值/重启event")
    @pytest.mark.full
    def test_caseid_1988591(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 0)
        self.ck_UsageModeChanged_and_GetUsageMode(0)
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        sleep(10)
        self.ck_UsageModeChanged_and_GetUsageMode(0)
        
    @allure.title("获取/通知使用模式状态（带功能安全需求参数）_初始值/重启event")
    @pytest.mark.full
    def test_caseid_1988590(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 0)
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        sleep(10)
        self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(0, 0)

    @allure.title("获取/通知CarMode（带功能安全需求参数）Validity7")
    @pytest.mark.full
    def test_caseid_111505(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1')
        self.ck_CarModeChangedValidity_and_GetCarModeValidity(0, 7)
        for E2E in [1, 2, 3, 5]:
            logger.info(f"现在是{E2E}")
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', E2E)
            sleep(0.2)
            self.ck_CarModeChangedValidity_and_GetCarModeValidity(E2E, 7)
        self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1')
        self.ck_CarModeChangedValidity_and_GetCarModeValidity(5, 0)

    @allure.title("获取/通知CarMode（带功能安全需求参数）Validity优先级")
    @pytest.mark.full
    def test_caseid_1980948(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 1)
        self.ipdu.set_no_crc(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1')
        self.ck_CarModeChangedValidity_and_GetCarModeValidity(1, 7)
        self.ipdu.pause_all_bus_send()
        sleep(3)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeValidity", {},
                                              {"out": {"value": 1, "validity": 7}})
        self.ipdu.restore_crc(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1')
        self.ipdu.resume_all_bus_send()
        self.ck_CarModeChangedValidity_and_GetCarModeValidity(1, 0)
        
    @allure.title("获取/通知使用模式用户提醒_isKeyNotInCar_audioRemind/初始值")
    @pytest.mark.full
    def test_caseid_1980944(self):
        self.set_usageModeRemind_signal(KeyNotPrsntMsgToDrvr=0, StrtMsgToDrvr=0, VehNotParkInfoWarn=0,
                                   AudWarn=0, StrtInProgs=0)
        for isKeyNotInCar in [1, 0, 1]:
                self.set_usageModeRemind_signal(KeyNotPrsntMsgToDrvr=isKeyNotInCar)
                self.set_usageModeRemind_signal(AudWarn=isKeyNotInCar)
                sleep(0.3)
                self.ck_usageModeRemind_and_getUsageModeRemind(True if isKeyNotInCar else False, 0, 0, True if isKeyNotInCar else False, 0)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "getUsageModeRemind", {}, {
            "out": {"isKeyNotInCar": False, "sts": 0, "wordRemind": 0, "audioRemind": False,
                    "powerSts": 0}},timeout=5)
        self.ipdu.resume_all_bus_send()
        self.ck_usageModeRemind_and_getUsageModeRemind(True , 0, 0, True, 0)

    @allure.title("通知/获取展车模式状态/通讯故障")
    @pytest.mark.full
    def test_caseid_1980594(self):
        self.bgm_eth_inter.start_bgm_tcpdump()
        sleep(10)
        self.ipdu.set(self.ipdu.propulsioncan.BgmPropulsionFr01, 'ExhibitionModeStsExhibitionModeSts', 0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.BgmPropulsionFr01, 'ExhibitionModeStsExhibitionModeSts', 1)
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(True, True)
        self.ipdu.pause_all_bus_send()
        logger.info(f"停总线")
        sleep(1)
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "NotifyExhibitionModeSts",
                                  {"sts": {"isOpen": True, "isValid": False}}, timeout=1)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetExhibitionModeSts", {},
                                              {"out": {"isOpen": True, "isValid": False}})
        self.ipdu.resume_all_bus_send()
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(True, True)
        sleep(2)
        self.bgm_eth_inter.stop_tcpdump_and_parse_signal()

    @allure.title("通知/获取展车模式状态/E2E/无异常evnet")
    @pytest.mark.sanity
    def test_caseid_1983631(self):
        self.ipdu.set(self.ipdu.propulsioncan.BgmPropulsionFr01, 'ExhibitionModeStsExhibitionModeSts', 0)
        sleep(0.5)
        self.ipdu.set(self.ipdu.propulsioncan.BgmPropulsionFr01, 'ExhibitionModeStsExhibitionModeSts', 1)
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(True, True)
        self.ipdu.set_no_crc(self.ipdu.propulsioncan.BgmPropulsionFr01, 'ExhibitionModeStsExhibitionModeSts')
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(True, False)
        self.partner.empty_all()
        self.ipdu.set(self.ipdu.propulsioncan.BgmPropulsionFr01, 'ExhibitionModeStsExhibitionModeSts', 0)
        self.partner.ck_no_event(VEHICLEMODESERVICE_CLIENT, "NotifyExhibitionModeSts")
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetExhibitionModeSts", {},
                                              {"out": {"isOpen": True, "isValid": False}})
        self.ipdu.restore_crc(self.ipdu.propulsioncan.BgmPropulsionFr01, 'ExhibitionModeStsExhibitionModeSts')
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(False, True)

    @allure.title("通知/获取展车模式状态/默认值_重启event")
    @pytest.mark.full
    def test_caseid_1988589(self):
        self.ipdu.set(self.ipdu.propulsioncan.BgmPropulsionFr01, 'ExhibitionModeStsExhibitionModeSts', 0)
        self.ipdu.set_no_crc(self.ipdu.propulsioncan.BgmPropulsionFr01, 'ExhibitionModeStsExhibitionModeSts')
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(False, False)
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        sleep(10)
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(False, False)
        self.ipdu.restore_crc(self.ipdu.propulsioncan.BgmPropulsionFr01, 'ExhibitionModeStsExhibitionModeSts')
        self.ck_NotifyExhibitionModeSts_and_GetExhibitionModeSts(False, True)
        
    @allure.title("获取/通知使用模式用户提醒_sts")
    @pytest.mark.sanity
    @pytest.mark.failed
    def test_caseid_1980945(self):
        self.set_usageModeRemind_signal(StrtMsgToDrvr=0,KeyNotPrsntMsgToDrvr=0, VehNotParkInfoWarn=0,AudWarn=0, StrtInProgs=0)
        self.partner.empty_all()
        for sts in [1, 4, 7, 8, 0, 10]:
            logger.info(f"现在信号是{sts}")
            self.set_usageModeRemind_signal(StrtMsgToDrvr=sts)
            self.ck_usageModeRemind_and_getUsageModeRemind(sts=sts)
        for two in [2, 3, 5, 6, 9, 11, 12, 13, 14, 15]:
            logger.info(f"现在信号是{two}")
            self.set_usageModeRemind_signal(StrtMsgToDrvr=two)
            self.ck_noevent_usageModeRemind_and_getUsageModeRemind(False, 10, 0, False, 0)

    @allure.title("获取/通知使用模式用户提醒_wordRemind")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1980946(self):
        self.set_usageModeRemind_signal(StrtMsgToDrvr=0,KeyNotPrsntMsgToDrvr=0, VehNotParkInfoWarn=0,AudWarn=0, StrtInProgs=0)
        self.partner.empty_all()
        for wordRemind in [1, 2, 0, 1]:
            logger.info(f'现在是{wordRemind}')
            self.set_usageModeRemind_signal(VehNotParkInfoWarn=wordRemind)
            self.ck_usageModeRemind_and_getUsageModeRemind(wordRemind=wordRemind)
        self.set_usageModeRemind_signal(VehNotParkInfoWarn=3)
        self.ck_noevent_usageModeRemind_and_getUsageModeRemind(False, 0, 1, False, 0)
        self.set_usageModeRemind_signal(VehNotParkInfoWarn=0)

    @allure.title("获取/通知使用模式用户提醒_powerSts")
    @pytest.mark.sanity
    @pytest.mark.failed
    def test_caseid_1980947(self):
        self.set_usageModeRemind_signal(StrtMsgToDrvr=0,KeyNotPrsntMsgToDrvr=0, VehNotParkInfoWarn=0,AudWarn=0, StrtInProgs=0)
        self.partner.empty_all()
        for powerSts in [1, 2, 0, 3]:
            logger.info(f'现在是{powerSts}')
            self.set_usageModeRemind_signal(StrtInProgs=powerSts)
            self.ck_usageModeRemind_and_getUsageModeRemind(powerSts=powerSts)

    @allure.title("获取/通知使用模式用户提醒_初始值")
    @pytest.mark.full
    @pytest.mark.failed
    def test_caseid_1983388(self):
        self.set_usageModeRemind_signal(KeyNotPrsntMsgToDrvr=1, StrtMsgToDrvr=1, VehNotParkInfoWarn=1,
                                   AudWarn=1, StrtInProgs=1)
        sleep(0.5)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
        sleep(10)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "getUsageModeRemind", {}, {
            "out": {"isKeyNotInCar": False, "sts": 0, "wordRemind": 0, "audioRemind": False, "powerSts": 0}})
        self.ipdu.resume_all_bus_send()
        sleep(0.1)
        self.ck_usageModeRemind_and_getUsageModeRemind(True, 1, 1, True, 1)
        self.set_usageModeRemind_signal(KeyNotPrsntMsgToDrvr=0, StrtMsgToDrvr=0, VehNotParkInfoWarn=0,
                                   AudWarn=0, StrtInProgs=0)

    @allure.title("通知/获取CarMode显示信息/FacyStop13/TrnspStop13/初始值")
    @pytest.mark.smoke
    @pytest.mark.failed
    def test_caseid_1981090(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr14, 'CarModDispdWdDispd', 1)
        self.partner.empty_all(0.5)
        for mode in [2, 4]:
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr14, 'CarModDispdWdDispd', mode)
            self.ck_CarModeDisplayChanged_and_GetCarModeDisplay(mode)
            self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
            sleep(10)
            self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetCarModeDisplay", {}, {"out": 0})
            self.ipdu.resume_all_bus_send()
            self.ck_CarModeDisplayChanged_and_GetCarModeDisplay(mode)

    @allure.title("通知/获取车辆能量等级_energyLevel/初始值")
    @pytest.mark.full
    def test_caseid_1981091(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecMai', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecSubtyp', 1)
        self.partner.empty_all(0.5)
        for Mai in range(16):
            logger.info(f'现在是{Mai}')
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecMai', Mai)
            self.ck_EnergylevelChanged_and_GetEnergyLevelSts(Mai, 1)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetEnergyLevelSts", {},
                                              {"out": {"energyLevel": 0, "subEnergyLevel": 0}},timeout=5)
        self.ipdu.resume_all_bus_send()

    @allure.title("通知/获取车辆能量等级_subEnergyLevel/重启event")
    @pytest.mark.sanity
    def test_caseid_1981092(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecMai', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecSubtyp', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecSubtyp', 2)
        self.ck_EnergylevelChanged_and_GetEnergyLevelSts(1, 2)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        sleep(10)
        self.ck_EnergylevelChanged_and_GetEnergyLevelSts(1, 2)

    @allure.title("通知/获取车辆能量等级_subEnergyLevel/初始值")
    @pytest.mark.full
    def test_caseid_1983389(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecMai', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecSubtyp', 1)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetEnergyLevelSts", {},
                                              {"out": {"energyLevel": 0, "subEnergyLevel": 0}},timeout=5)
        self.ipdu.resume_all_bus_send()
        self.ck_EnergylevelChanged_and_GetEnergyLevelSts(1, 1)

    @allure.title("通知/获取车辆能量等级/初始值_重启event")
    @pytest.mark.full
    def test_caseid_1988836(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecMai', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1EgyLvlElecSubtyp', 0)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        sleep(10)
        self.ck_EnergylevelChanged_and_GetEnergyLevelSts(0, 0)

    @allure.title("通知/获取车辆功率等级_powerLevel/初始值")
    @pytest.mark.full
    def test_caseid_1981093(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecMai', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecSubtyp', 1)
        self.partner.empty_all(0.5)
        for powerLevel in range(16):
            logger.info(f'现在是{powerLevel}')
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecMai', powerLevel)
            self.ck_PowerlevelChanged_and_GetPowerlevel(powerLevel, 1)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetPowerlevel", {},
                                              {"out": {"powerLevel": 0, "subpowerLevel": 0}},timeout=5)
        self.ipdu.resume_all_bus_send()

    @allure.title("通知/获取车辆功率等级_subpowerLevel/初始值")
    @pytest.mark.sanity
    def test_caseid_1981094(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecMai', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecSubtyp', 1)
        self.partner.empty_all(0.5)
        for subpowerLevel in range(16):
            logger.info(f'现在是{subpowerLevel}')
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecSubtyp', subpowerLevel)
            self.ck_PowerlevelChanged_and_GetPowerlevel(1, subpowerLevel)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetPowerlevel", {},
                                              {"out": {"powerLevel": 0, "subpowerLevel": 0}},timeout=5)
        self.ipdu.resume_all_bus_send()
        self.ck_PowerlevelChanged_and_GetPowerlevel(1, 15)
        
    @allure.title("通知/获取车辆功率等级_重启event")
    @pytest.mark.full
    def test_caseid_1984531(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecMai', 1)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecSubtyp', 1)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecSubtyp', 2)
        self.ck_PowerlevelChanged_and_GetPowerlevel(1, 2)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        sleep(15)
        self.ck_PowerlevelChanged_and_GetPowerlevel(1, 2)

    @allure.title("通知/获取车辆功率等级/初始值_重启event")
    @pytest.mark.full
    def test_caseid_1988840(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecMai', 0)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1PwrLvlElecSubtyp', 0)
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT)
        sleep(10)
        self.ck_PowerlevelChanged_and_GetPowerlevel(0, 0)
        
    @allure.title("通知/获取通知使用模式状态（不带功能安全需求参数）/(带功能安全需求参数)/初始值/other")
    @pytest.mark.full
    def test_caseid_1981095(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', 1)
        self.partner.empty_all(0.5)
        for UsageMode in [0, 1]:
            logger.info(f'现在是UsageMode{UsageMode}')
            self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', UsageMode)
            self.ck_UsageModeChanged_and_GetUsageMode(UsageMode)
            self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(UsageMode, 0)
            for other in list(range(3, 11)) + [12, 14, 15]:
                logger.info(f'现在是other{other}')
                self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1UsgModSts', other)
                if other != 3:
                    self.partner.ck_no_event(VEHICLEMODESERVICE_CLIENT, "UsageModeChanged")
                    self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageMode", {}, {"out": UsageMode})
                    self.partner.ck_no_event(VEHICLEMODESERVICE_CLIENT, "UsageModeChangedValidity")
                    self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageModeValidity", {},
                                          {"out": {"value": UsageMode, "validity": 1}})
                else: 
                    self.ck_UsageModeChanged_and_GetUsageMode(UsageMode)   
                    self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(UsageMode, 1)  # 正常为1
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageMode", {}, {"out": 0},timeout=2)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "GetUsageModeValidity", {},
                                              {"out": {"value": 0, "validity": 0}},timeout=2)
        self.ipdu.resume_all_bus_send()
        self.ck_UsageModeChangedValidity_and_GetUsageModeValidity(0, 1)

    @allure.title("通知/获取CarMode（带功能安全需求参数）validity_1")
    @pytest.mark.full
    def test_caseid_111506(self):
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 1)
        sleep(0.5)
        self.ipdu.set(self.ipdu.backbonefr.CemBackBoneFr02, 'VehModMngtGlbSafe1CarModSts1', 4)
        self.ck_CarModeChangedValidity_and_GetCarModeValidity(1, 1)

@allure.feature("SOA服务接口")
@allure.story("架构基础/VehicleModeService")
@pytest.mark.vmm
@pytest.mark.wjj
@pytest.mark.mock_tcp
class TestVehicleModeServiceMockTcp(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu, tcp_down_mcu_ip="172.16.5.21")
        self.partner = S2sBaseClass([("VehicleModeService", "client")])
        self.partner.wait_for_service_reconnect(VEHICLEMODESERVICE_CLIENT)
    
    def after_class(self, ecu):
        self.partner.stop_operators()
        super().after_class(self, ecu)
    
    def before_each_func(self, ecu):
        super().before_each_func(ecu)
        self.partner.empty_all()
        
    def after_each_func(self, ecu):
        self.bgmcli.stop_bgm_tcpdump()# 停止抓包
        super().after_each_func(ecu)
        
    def ck_lvRelaySts_and_getLVRelaySts(self, ck_dict):
        """校验指定lvRelaySts事件，并请求getLVRelaySts"""
        self.partner.ck_s2s_event(VEHICLEMODESERVICE_CLIENT, "lvRelaySts", {"sts": ck_dict})
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "getLVRelaySts", {}, {"out": ck_dict})
            
    @allure.title("通知/获取低压继电器状态kl15_3RlySts")
    @pytest.mark.full
    def test_caseid_1981478(self):
        for value in [1, 0, 1]:
            self.bgm_eth_inter.set_signal("IgnRly3Cmd", value, send_pdu_immediately=True)
            self.ck_lvRelaySts_and_getLVRelaySts({"kl15_3RlySts": True if value == 1 else False})
            
    @allure.title("通知/获取低压继电器状态battSaverRlySts")
    @pytest.mark.sanity
    def test_caseid_1981509(self):
        for value in [1, 0, 1]:
            self.bgm_eth_inter.set_signal("RlyPwrDistbnCmd1WdBattSaveCmd", value, send_pdu_immediately=True)
            self.ck_lvRelaySts_and_getLVRelaySts({"battSaverRlySts": True if value == 1 else False})
        
    @allure.title("通知/获取低压继电器状态pwrOutletRlySts")
    @pytest.mark.full
    def test_caseid_1981505(self):
        for value in [1, 0, 1]:
            self.bgm_eth_inter.set_signal("RlyPwrCmd", value, send_pdu_immediately=True)
            self.ck_lvRelaySts_and_getLVRelaySts({"pwrOutletRlySts": True if value == 1 else False})
            
    @allure.title("通知/获取低压继电器状态kl15RlySts")
    @pytest.mark.full
    def test_caseid_1892925(self):
        for value in [1, 2, 3, 0]:
            self.bgm_eth_inter.set_signal("IgnRlyCmdActr", value, send_pdu_immediately=True)
            self.ck_lvRelaySts_and_getLVRelaySts({"kl15RlySts": value})

    @allure.title("通知/获取低压继电器状态kl15ExtRlySts")
    @pytest.mark.smoke
    def test_caseid_1981496(self):       
        for value in [1, 0, 1]:
            self.bgm_eth_inter.set_signal("RlyPwrDistbnCmd1WdIgnRlyExtCmd", value, send_pdu_immediately=True)
            self.ck_lvRelaySts_and_getLVRelaySts({"kl15ExtRlySts": True if value == 1 else False})
        
    @allure.title("通知/获取低压继电器状态tcp_默认值")
    @pytest.mark.full
    def test_caseid_1981489(self):
        self.restart_bgm_and_connect_service(VEHICLEMODESERVICE_CLIENT, resume_all_bus=False)
        sleep(5)
        self.partner.send_request_and_ck_resp(VEHICLEMODESERVICE_CLIENT, "getLVRelaySts", {}, {"out": {"kl15RlySts":0,"battSaverRlySts": False, 
                                                                                                       "pwrOutletRlySts": False, "kl15ExtRlySts": False, "kl15_3RlySts": False}},timeout=5)