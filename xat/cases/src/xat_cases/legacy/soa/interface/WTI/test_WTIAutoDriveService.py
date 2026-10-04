#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_WTIAutoDriveService.py
@Time         :2023/05/18 17:20:31
@Author       :jiabin.zhu@jiduauto.com
@Description  :
"""
import allure
import pytest
import random
from time import sleep
from xat_ecu.legacy.common.data_type_handing import logger
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_cases.legacy.soa.case_helper.ANPMRC_server import ANPMRCService_Server

ELKSERVICE_SERVER = "ELKService_server"
ESS_SERVICE_SERVER = "ESSService_server"

@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIAutoDriveService")
@pytest.mark.zjb
class TestWTIAutoDriveService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("LCAService", "server"),
                                     ("WTIAutoDriveService", "client"),
                                     ("ANPWTIService", "server"),
                                     ("RPAAPAService", "server"),
                                     ("AVPService", "server"),
                                     ("BACUService", "server"),
                                     ("FCTAService", "server"),
                                     ("RCWService", "server"),
                                     ("AEBRService", "server"),
                                     ("RCTAService", "server"),
                                     ("DOWService", "server"),
                                     ("LKAService", "server"),
                                     ("TLAService", "server"),
                                     ("SensorSelfCleanService", "server"),
                                     ("ACUFaultInfoService", "server"),
                                     ("FrontBackupCamera", "server"),
                                     ("CMSFService", "server"),
                                     ("SASService", "server"),
                                     ("AutoHighBeamControlService", "server"),
                                     ("AEBService", "server"),
                                     ("FCWService", "server"),
                                     ("AutoGearShiftService", "server"),
                                     ("APIService", "server"),
                                     ("ANPMRCService", "server"),
                                     ("AutoTurnLampCtrlService", "server"),
                                     ("ACCService", "server"),
                                     ("ELKService", "server"),
                                     ("MarsPilotMarsDriverService", "server"),
                                     ("SeatService", "client"),
                                     ("ESSService","server")
                                     ])
        self.partner.method_default_timeout = 0.1
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        #lg
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 0}})
        self.AutoDriverStatus_response = False
        self.ANP_response = False
        sleep(1)
    
    #设置当前无前向和侧后向辅助安全功能受限提醒报警
    def setNoWTI_2354(self):
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 0}})
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":1,"faultSts": 0}})
        self.partner.send_event_notify(SAS_SERVICE_SERVER, "NotifyTrafficSignStatus",
                                      {"trafficSignStatus": {"functionSts":1,"faultSts": 0}})
        self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
                                      {"tlaFunctionStatus": {"switchSts": 6,"faultSts": 0}})
        self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                      {"allAHBCFunctionSts": {"switchSts": 1,"faultSts": 0}})
        self.partner.send_event_notify(AUTOTURNLAMPCTRL_SERVICE_SERVER, "AutoCtrlTurnLampSts",
                                     {"sts": {"switchSts":1,"faultSts": 0}})
        self.partner.send_event_notify(LKA_SERVICE_SERVER, "NotifyLKAFunctionStatus",
                                     {"lasFunctionStatus": {"switchSts":True,"faultSts": 0}})
        
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 0}})
        self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                     {"rctaFunctionStatus": {"functionStatus":1,"faultSts": 0}})
        self.partner.send_event_notify(LCA_SERVICE_SERVER, "NotifyLCAStatus",
                                     {"lcaStatus": {"switchSts":1,"faultSts": 0}})
        self.partner.send_event_notify(DOW_SERVICE_SERVER, "NotifyDOWStatus",
                                      {"dowStatus": {"functionStatus":1,"faultSts": 0}})
        sleep(0.5)
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": "Front And Side Back ADAS Limit Reminder", "info": 0}]})

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.partner.empty_all()
        logger.info(f"case开始运行***************************************************")

    def after_each_func(self, ecu):
        logger.info(f"case结束运行***************************************************")
        super().after_each_func(ecu, start=False)
    
    def seat_belt_status(self,A,B,C,D,E):
        """设置主驾 副驾 左后 后中 后右 1代表已系 0 代表未系"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSt1', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecLeBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSt1', D)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecMidBltLockSts', 0)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSt1', E)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,
                      'BltLockStAtRowSecRiBltLockSts', 0)
        sleep(1)
        
    def set_four_seat_occupt(self,A,B,C,D):
        """设置副驾 左后 后中 后右 1/2代表占位 0 代表未占位"""
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'PassSeatSts', A)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecLe', B)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecMid', C)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'SeatOccptAtRowSecRi', D)
        sleep(0.5)
        
    def ck_no_specific_event_and_GetWarningMsgList(self, hint, info, timeout=0.5):
        """校验无指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", hint, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def ck_and_get_warningmsglist(self, hint, info, timeout=1):
        """校验指定warningMsgList事件，并请求WarningMsgList获取结果"""
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": str(info)}]}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": [{"name": hint, "info": str(info)}]})

    def get_multiplewarningmsglist(self, hint, info, timeout=1):
        """校验指定warningMsgList事件，并请求WarningMsgList获取结果"""
        tmp = self.return_multiphint(hint,info)
        # self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
        #                           {"list": tmp}, timeout=timeout)
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                              {"out": tmp})    
    def return_multiphint(self, hint, info): 
        warning_info = []
        for i in range(len(hint)):
            info = {"name": hint[i], "info": info[i]}
            warning_info.append(info)
            return warning_info
    
    def ck_change_for_one_loop(self, hint, partner, interface, make_struct, origin_value, traversal_values, make_info,
                               jump_trigger=True):
        """校验信号跳变触发event， 一层循环"""
        self.partner.send_event_notify(partner, interface, make_struct(origin_value))
        self.partner.empty_all(0.5)
        last_info = origin_value
        for warning in list(traversal_values) + [0]:  # 添加个0测试产生到恢复
            self.partner.send_event_notify(partner, interface, make_struct(warning))
            new_info = make_info(warning)
            self.ck_warningmsg(hint, last_info, new_info, jump_trigger=jump_trigger)
            last_info = new_info

    def ck_change_for_two_loop(self, hint: str, partner: str, interface: str, origin_value: tuple,
                               traversal1_values, traversal2_values, make_struct, make_info, jump_trigger: bool):
        """
        发送智驾notify，校WTIAutoDrive的事件
        :param hint:   WTI提示信息
        :param partner:  智驾服务名
        :param interface: 智驾notify接口名
        :param origin_value: 默认信息
        :param traversal1_values:  外层循环遍历值，自动补0模拟恢复
        :param traversal2_values: 内存循环遍历值
        :param make_struct:  构造智驾notify接口结构体
        :param make_info:   返回当前notify参数匹配的info值
        :param jump_trigger:   是否检测info变化触发event
        :return:
        """
        self.partner.send_event_notify(partner, interface, make_struct(*origin_value))
        self.partner.empty_all(0.5)
        last_info = origin_value[0]
        for value1 in list(traversal1_values) + [0]:  # 添加个0测试产生到恢复
            for value2 in list(traversal2_values):
                logger.info(f"value1:{value1}, value2:{value2}")
                self.partner.send_event_notify(partner, interface, make_struct(value1, value2))
                new_info = make_info(value1, value2)
                self.ck_warningmsg(hint, last_info, new_info, jump_trigger=jump_trigger)
                last_info = new_info

    def ck_warningmsg(self, hint, last_info, new_info, jump_trigger=False):
        """校验事件型，非0每次上次上报，为0只在跳变为0触发一次"""
        if jump_trigger:  # 信号跳变
            if last_info != new_info:
                self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
        else:  # 不看信号跳变
            if new_info or last_info != new_info:
                self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
            else:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                
                               
    @allure.title("WarningMsgNode.name ANP_ANPStatusReminder&openSource（增加时间戳）")
    @pytest.mark.restart
    @pytest.mark.sanity
    def test_caseid_1918615(self):
        # timestamp为BGM上电后的单调时间，重启后恢复0，id是一个上电周期内相同，重启后不同
        # WTI和WTIAutoDrive中只要触发event和响应get，S2S都会重新赋id和timestamp，其他服务都是触发event的时候赋id和timestamp，调用get拿到的就是event时赋的值
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 14, "openSource": 2}})
        self.partner.empty_all(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 57, "openSource": 2}})
        event1 = self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", {})
        event1_timestamp = event1["list"][0]['sequenceTime']['timestamp']
        event1_id = event1["list"][0]['sequenceTime']['id']
        logger.info(f"--event1_id: {event1_id}--event1_timestamp: {event1_timestamp}")
        resp1 = self.partner.send_request_and_return_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {})["out"]
        for obj in resp1:
            name = obj["name"]
            if name == "ANP Status Open Source":
                resp1_timestamp = obj["sequenceTime"]["timestamp"]
                resp1_id = obj["sequenceTime"]["id"]
                logger.info(f"--resp1_id: {resp1_id}--resp1_timestamp: {resp1_timestamp}")
                break
        else:
            assert False, "not found"

        if resp1_timestamp < event1_timestamp:
            assert False
        if event1_id != resp1_id:
            assert False
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 14, "openSource": 2}})
        event2 = self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", {})
        event2_timestamp = event2[ "list"][0]['sequenceTime']['timestamp']
        event2_id = event2["list"][0]['sequenceTime']['id']
        logger.info(f"--event2_id: {event2_id}--event2_timestamp: {event2_timestamp}")
        if event2_timestamp < resp1_timestamp:
            assert False
        if event2_id != event1_id:
            assert False
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        self.partner.wait_for_service_reconnect(ANPWTI_SERVICE_SERVER)
        sleep(3)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 14, "openSource": 2}})
        event3 = self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", {})["list"][0]
        event3_timestamp = event3['sequenceTime']['timestamp']
        event3_id = event3['sequenceTime']['id']
        logger.info(f"--event3_id: {event3_id}--event3_timestamp: {event3_timestamp}")
        if event3_timestamp > event1_timestamp:
            assert False
        if event3_id == event2_id:
            assert False
        
    @allure.title("APA运行状态信息,事件型接口通知")
    @pytest.mark.smoke
    def test_caseid_1989253(self): 
        def return_struct(value1, value2):
            return {"reminder": {"type": value1, "lastHandleType": value2}}
        def return_info(value1, value2):
            if value2 in [0, 1, 4] and value1 in [2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 24, 
                                                  39, 40, 41, 44, 46, 48, 49, 52, 54, 55, 56, 57, 60, 62, 65, 69]:
                return value1
            else:
                return 0
        self.ck_change_for_two_loop("APA Working Status", RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                    (0, 0), range(70), range(5),
                                    return_struct, return_info, jump_trigger=False)
        
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                           {"reminder": {"type": 0, "lastHandleType": 0, "sensorSts":0}})
      
        for sensorSts in [0,1,2,3,4,5,6]:
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type": 41, "lastHandleType": 1, "sensorSts":sensorSts}})
            if sensorSts in [0,6]:
                self.partner.ck_wti_warning_and_resp("APA Working Status", 41, wti_auto=True)
            elif sensorSts == 1:
                self.partner.ck_wti_warning_and_resp("APA Working Status", 0, wti_auto=True)
            else:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", "APA Working Status")
          
    @allure.title("APA运行状态信息,周期性接口通知")
    @pytest.mark.full
    def test_caseid_1987867(self):
        def return_struct(value1, value2):
            return {"reminder": {"type": value1, "lastHandleType": value2}}

        def return_info(value1, value2):
            return value1 if value2 in [0, 1, 4] and (value1 == 47 or value1 == 71) else 0

        self.ck_change_for_two_loop("APA Working Status Cycle", RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                    (0, 0), [0, 7, 47, 71], range(5), return_struct, return_info, jump_trigger=True)

    @allure.title("APA TTS 播报_钥匙断连停止播报且不会触发播报")
    @pytest.mark.sanity
    def test_caseid_1959997(self):
        hint = "APA TTS"
        for zone in range(16):
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{zone}', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                      'BLEKeyPrsntStsZone1', 1)
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 4, "lastHandleType": 1}})
        self.partner.ck_wti_warning_and_resp(hint, 4, wti_auto=True)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                      'BLEKeyPrsntStsZone1', 0)
        self.partner.ck_wti_warning_and_resp(hint, 0, wti_auto=True)

        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 4, "lastHandleType": 1}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", hint)

    @allure.title("APA TTS 播报_任一蓝牙钥匙槽连接可使能播报")
    @pytest.mark.sanity
    def test_caseid_1960000(self):
        hint = "APA TTS"
        for zone in range(16):
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{zone}', 0)
        self.partner.empty_all(0.5)
        for zone in range(16):
            if zone > 1:
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                              f'BLEKeyPrsntStsZone{zone - 1}', 0)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{zone}', 1)
            logger.info(f"zone{zone}=1")
            sleep(0.2)
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                           {"reminder": {"type": 4, "lastHandleType": 1}})
            self.partner.ck_wti_warning_and_resp(hint, 4, wti_auto=True)
    
    @allure.title("APA TTS 播报_遍历所有type")
    @pytest.mark.sanity
    def test_caseid_1989252(self):   
        hint = "APA TTS"
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                      'BLEKeyPrsntStsZone1', 1)
        self.partner.empty_all(0.5)
        def return_struct(value1, value2):
            return {"reminder": {"type": value1, "lastHandleType": value2}}
        def return_info(value1, value2):
            if value2 in [0, 1, 4] and value1 in [0, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 16, 17, 18, 19, 20, 21, 25, 26, 
                                                  27, 28, 29, 30, 31, 32, 33, 34, 39, 40, 41, 43, 44, 45, 46, 47, 48, 49, 
                                                  50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 62, 65, 69, 70, 81]:
                return value1
            elif value2 in [0, 1, 4] and value1 in [72,73,74,75,76,77,78,79]:
                return 41
            else:
                return 0
        self.ck_change_for_two_loop(hint, RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                    (0, 0), range(82), range(5), return_struct, return_info, jump_trigger=False)
        
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                           {"reminder": {"type": 0, "lastHandleType": 0, "sensorSts":0}})
        for type in [41,72,73,74,75,76,77,78,79]:
            for sensorSts in [0,1,2,3,4,5,6]:
                self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                           {"reminder": {"type": type, "lastHandleType": 0, "sensorSts":sensorSts}})
                if sensorSts in [0,6]:
                    self.partner.ck_wti_warning_and_resp(hint, 41, wti_auto=True)
                elif sensorSts == 1:
                    self.partner.ck_wti_warning_and_resp(hint, 0, wti_auto=True)
                else:
                    self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", hint)
                    

    @allure.title("APA TTS 播报_组合判断type_source_任一变化触发上报")
    @pytest.mark.full
    def test_caseid_1979642(self):
        hint = "APA TTS"
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEKeyPrsntStsZone1', 1)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 4, "lastHandleType": 3}})
        self.partner.empty_all(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 4, "lastHandleType": 1}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": '4'}]})

        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 4, "lastHandleType": 0}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": '4'}]})

        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 4, "lastHandleType": 2}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": hint, "info": '0'}]})

        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 0, "lastHandleType": 2}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", hint)

    @allure.title("APA TTS 播报_先发送event_再满足蓝牙钥匙连接_不会触发上报")
    @pytest.mark.full
    def test_caseid_1979645(self):
        hint = "APA TTS"
        for zone in range(16):
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, f'BLEKeyPrsntStsZone{zone}', 0)
        sleep(0.5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 4, "lastHandleType": 2}})
        self.partner.empty_all(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 4, "lastHandleType": 1}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", hint)

        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17, 'BLEKeyPrsntStsZone1', 1)
        sleep(1)
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", hint)

    @allure.title("APA TTS 播报,不需要判断钥匙的检测区域")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727524?projectId=46')
    @pytest.mark.full
    def test_caseid_104921(self):
        for zone in range(16):
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{zone}', 0)
        sleep(0.5)

        def return_struct(value1, value2):
            return {"reminder": {"type": value1, "lastHandleType": value2}}

        def return_info(value1, value2):
            return 1 if value2 in [0, 1, 4] and value1 else 0

        self.ck_change_for_two_loop("APA TTS Not Care Key", RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                    (0, 0), [0, 53], range(5), return_struct, return_info, jump_trigger=False)
                                
    @allure.title("HAVP提示信息")
    @pytest.mark.smoke
    def test_caseid_1987190(self):  # DPMS-52843 V1.4新增WTI-2148和WTI-2149
        def return_struct(value1, value2):
            return {"avpReminder": {"type": value1, "source": value2}}

        def return_info(value1, value2):
            return value1 if value2 in [0, 1, 4, 5, 6] and value1 in [0, 7, 8, 19, 20, 21, 22, 23, 24, 25, 26,
                                                                      27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
                                                                      39, 40, 41, 42, 43, 44, 45, 46,
                                                                      48, 49, 50, 51, 52, 53, 55, 56,
                                                                      57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 
                                                                      74, 75, 76, 77, 78, 79, 80] else 0

        self.ck_change_for_two_loop("HAVP Warn", AVP_SERVICE_SERVER, "NotifyAVPReminderEvent",
                                    (0, 0), range(81), range(7), return_struct, return_info, jump_trigger=False)
   
    @allure.title("车辆规划和控制ANP_PNC提醒")
    @pytest.mark.smoke
    def test_caseid_1988915(self):
        def return_struct(value):
            return {"pncReminder": value}

        def return_info(value):
            return value if value in [38, 95, 114, 116 ,118] else 0

        self.ck_change_for_one_loop("ANP PNC Remind", ANPWTI_SERVICE_SERVER, "NotifyPNCReminder", return_struct,
                                    0, range(119), return_info, jump_trigger=False)

    @allure.title("车辆规划和控制ANP_LaneChange提醒1")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727551?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1979849(self):
        def return_struct(value1, value2):
            return {"anpLaneChangeReminder": {"reminder": value1, "openSource": value2}}

        def return_info(value1, value2):
            if value1 == 9:
                return 9
            else:
                return value1 if value2 == 2 else 0

        self.ck_change_for_two_loop("ANP Lane Change Remind1", ANPWTI_SERVICE_SERVER, "NotifyANPLaneChangeReminder",
                                    (0, 0),
                                    [0, 3, 4, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                                    range(3), return_struct, return_info, jump_trigger=False)

    @allure.title("车辆规划和控制ANP_LaneChange提醒2")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727495?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1979672(self):
        def return_struct(value):
            return {"anpLaneChangeReminder": {"reminder": value}}

        def return_info(value):
            if value == 6:
                return 1
            elif value in [28, 29]:
                return value
            else:
                return 0

        self.ck_change_for_one_loop("ANP Lane Change Remind2", ANPWTI_SERVICE_SERVER, "NotifyANPLaneChangeReminder",
                                    return_struct, 0, range(30), return_info, jump_trigger=False)

    @allure.title("车辆规划和控制ANP_LaneChange提醒3")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727470?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104973(self):
        def return_struct(value1, value2):
            return {"anpLaneChangeReminder": {"reminder": value1, "openSource": value2}}

        def return_info(value1, value2):
            return 1 if value1 == 20 and value2 == 2 else 0

        self.ck_change_for_two_loop("ANP Lane Change Remind3", ANPWTI_SERVICE_SERVER, "NotifyANPLaneChangeReminder",
                                    (0, 0),
                                    [0, 20],
                                    range(3), return_struct, return_info, jump_trigger=False)

    @allure.title("依赖NotifyANPStatus.ANPStatusReminder和NotifyANPStatus.openSource,且CCP#953=3/4/5") #需求更新待删除
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727531?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104914(self):
        for ccp in [2, 3, 4, 5]:
            self.sd_tester.write_single_ccp(953, ccp)
            logger.info(f"CCP953改为{ccp}")
            sleep(1)

            def return_struct(value1, value2):
                return {"anpStsReminder": {"anpStatusReminder": value1, "openSource": value2}}

            def return_info(value1, value2):
                return value1 if value2 == 2 and value1 and ccp in [3, 4, 5] else 0

            self.ck_change_for_two_loop("ANP Booked Remind", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                        (0, 0),
                                        [0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 13, 113, 115, 117],
                                        range(3), return_struct, return_info, jump_trigger=False)
            
    @allure.title("依赖NotifyANPStatus.ANPStatusReminder和NotifyANPStatus.openSource,且CCP#953=3/4/5")
    @pytest.mark.sanity
    def test_caseid_1985463(self):
        for ccp in [2, 3, 4, 5]:
            self.sd_tester.write_single_ccp(953, ccp)
            logger.info(f"CCP953改为{ccp}")
            sleep(1)

            def return_struct(value1, value2):
                return {"anpStsReminder": {"anpStatusReminder": value1, "openSource": value2}}

            def return_info(value1, value2):
                return value1 if value2 == 2 and value1 and ccp in [3, 4, 5] else 0
            
            def return_info1(value1, value2):
                return value1 if value1 and ccp in [3, 4, 5] else 0

            self.ck_change_for_two_loop("ANP Booked Remind", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                        (0, 0),
                                        [0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 13, 113, 115, 117, 142, 144, 146],
                                        range(3), return_struct, return_info, jump_trigger=False)
            self.ck_change_for_two_loop("ANP Booked Remind", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                        (0, 0),
                                        [140],
                                        range(3), return_struct, return_info1, jump_trigger=False)

    @allure.title("ANP_功能降级提示_SafetyBelt")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727522?projectId=46')
    @pytest.mark.smoke
    def test_caseid_104923(self):
        def return_struct(value):
            return {"driverDetection": {"safeBelt": value}}

        def return_info(value):
            return value

        self.ck_change_for_one_loop("ANP Degradation Safety Belt Remind", ANPWTI_SERVICE_SERVER,
                                    "NotifyDriverDetection",
                                    return_struct, 0, range(2), return_info, jump_trigger=False)

    @allure.title("ANP_功能降级提醒_driverOccupy")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727498?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104946(self):
        def return_struct(value):
            return {"driverDetection": {"driverOccupyWarning": value}}

        def return_info(value):
            return value

        self.ck_change_for_one_loop("ANP Degradation Driver Occupy Warning", ANPWTI_SERVICE_SERVER,
                                    "NotifyDriverDetection",
                                    return_struct, 0, range(2), return_info, jump_trigger=False)

    @allure.title("ANP_功能降级提醒")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727471?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104972(self):
        def return_struct(value1, value2):
            return {"driverDetection": {"handOff": value1, "mindsOff": value2}}

        def return_info(handOff, mindsOff):
            if handOff == 1 and mindsOff == 0:
                info = 1
            elif handOff == 2 and mindsOff == 0:
                info = 2
            elif handOff == 3 and mindsOff == 0:
                info = 3
            elif handOff == 4 and mindsOff == 0:
                info = 4
            elif handOff == 0 and mindsOff == 1:
                info = 5
            elif handOff == 0 and mindsOff == 2:
                info = 6
            elif handOff == 1 and mindsOff == 1:
                info = 7
            elif handOff == 3 and mindsOff == 1:
                info = 8
            elif (handOff == 3 and mindsOff == 2) or (handOff == 4 and mindsOff == 1) or \
                    (handOff == 4 and mindsOff == 2):
                info = 9
            elif (handOff == 1 and mindsOff == 2) or (handOff == 2 and mindsOff == 1) or \
                    (handOff == 2 and mindsOff == 2):
                info = 10
            else:
                info = 0
            return info

        self.ck_change_for_two_loop("ANP Degradation Warning", ANPWTI_SERVICE_SERVER, "NotifyDriverDetection",
                                    (0, 0), range(5), range(3), return_struct, return_info, jump_trigger=False)
    
    @allure.title("ANP_ANPStatusReminder")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1796996?projectId=46')
    @pytest.mark.sanity
    def test_caseid_1979657(self):
        def return_struct(value):
            return {"anpStsReminder": {"anpStatusReminder": value}}

        def return_info(value):
            if value in [101, 102]:
                res = 100
            elif value in [104, 105]:
                res = 103
            elif value in [107, 108]:
                res = 106
            else:
                res = value
            return res

        self.ck_change_for_one_loop("ANP PStatus Reminder", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                    return_struct, 0,
                                    [0, 0, 82, 82, 61, 62, 63, 64, 65, 66, 69, 83, 84, 86, 70, 71, 72, 73, 76, 90,
                                     93, 91, 77, 78, 79, 80, 81, 97, 68, 85, 75, 92, 98, 99, 100, 101, 102, 103, 104,
                                     105, 106, 107, 108, 120, 121, 122, 123, 124, 126, 127, 128, 129, 130, 131, 132,
                                     133, 134, 135, 136],
                                    return_info, jump_trigger=False)
        
    @allure.title("ANP_ANPStatusReminder")
    @pytest.mark.sanity
    def test_caseid_1987894(self):
        def return_struct(value1, value2):
            return {"anpStsReminder": {"anpStatusReminder": value1, "openSource": value2}}
        def return_info(value1,value2):
            if value2 == 2 and value1 != 0:
                info = value1
            else :
                info = 0
            return info
        self.ck_change_for_two_loop("ANP PStatus Reminder", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                    (0, 0), [158, 159, 0], range(3), return_struct, return_info, jump_trigger=False)
        
    @allure.title("ANP风险提醒")
    @pytest.mark.smoke
    def test_caseid_1987895(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "CollisionRisk",
                                       {"riskInfo": {"decelerationRisk":0}})
        sleep(0.5)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "CollisionRisk",
                                       {"riskInfo": {"decelerationRisk":0}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'ANP Risk Reminder')
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "CollisionRisk",
                                       {"riskInfo": {"decelerationRisk":1}})
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{'name': 'ANP Risk Reminder', 'info': '1'},
                                                        ]})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "CollisionRisk",
                                       {"riskInfo": {"decelerationRisk":1}})
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{'name': 'ANP Risk Reminder', 'info': '1'},
                                                        ]})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "CollisionRisk",
                                       {"riskInfo": {"decelerationRisk":0}})
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{'name': 'ANP Risk Reminder', 'info': '0'},
                                                        ]})

    @allure.title("夜间自动驾驶安全提醒")
    @pytest.mark.sanity
    def test_caseid_1987896(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NightDrivingSafetyReminder",
                                       {"reminder": 0})
        sleep(0.5)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NightDrivingSafetyReminder",
                                       {"reminder": 0})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Night Driving Safety Reminder')
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NightDrivingSafetyReminder",
                                       {"reminder": 1})
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{'name': 'Night Driving Safety Reminder', 'info': '1'},
                                                        ]})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NightDrivingSafetyReminder",
                                       {"reminder": 1})
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{'name': 'Night Driving Safety Reminder', 'info': '1'},
                                                        ]})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NightDrivingSafetyReminder",
                                       {"reminder": 0})
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{'name': 'Night Driving Safety Reminder', 'info': '0'},
                                                        ]})
        
    @allure.title("副驾自动驾驶安全带未系提醒_调用通知前安全带已系_通过安全带状态取消")
    @pytest.mark.smoke
    def test_caseid_1987897(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            self.partner.empty_all(0.5)
            #当前安全带已系
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', 1)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 1, "status": 0}]},timeout = 0.5)
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})

            self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
            #设置安全带解开
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', 0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 1, "status": 1}]},timeout = 0.5)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
            
            #设置安全带 均 系上
            self.seat_belt_status(1,1,1,1,1)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
        
    @allure.title("副驾自动驾驶安全带未系提醒_调用通知前安全带未系_通过安全带状态取消")
    @pytest.mark.full
    def test_caseid_1987916(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 0}})
            self.partner.empty_all(0.5)
            #当前安全带未系
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', 0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 1, "status": 1}]},timeout = 0.5)
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
            #设置安全带 均 系上
            self.seat_belt_status(1,1,1,1,1)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
            
    @allure.title("副驾自动驾驶安全带未系提醒_调用通知前安全带已系_通过通知状态取消")
    @pytest.mark.full
    def test_caseid_1987898(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            for j in [0,1,2,12,13,14]:
                self.partner.empty_all(0.5)
                #当前安全带已系
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', 1)
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                            {"out": [{"id": 1, "status": 0}]},timeout = 0.5)
                self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})

                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
                #设置安全带解开
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', 0)
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                            {"out": [{"id": 1, "status": 1}]},timeout = 0.5)
                self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
                
                self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": j}})
                self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
                
    @allure.title("副驾自动驾驶安全带未系提醒_触发条件不满足")
    @pytest.mark.full
    def test_caseid_1987899(self):
        #安全带无故障，座椅已占位，安全带未系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        self.partner.empty_all(0.5)
        #副驾座椅未占位 SeatOccupyStatusValidity.infos.value.status=0
        self.set_four_seat_occupt(0,1,1,1)
        self.seat_belt_status(1,0,1,1,1)  
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity",
                                                {"seats": [12]},{"out": [{"value": {"seatId": 1, "status": 0}},
                                                ]},timeout=3)
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 3}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        #副驾座椅占位
        self.set_four_seat_occupt(1,1,1,1)
        self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
        
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 0}})
        self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
        
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 12}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        
    @allure.title("二排左侧自动驾驶安全带未系提醒_调用通知前安全带已系_通过安全带状态取消")
    @pytest.mark.full
    def test_caseid_1987900(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 1)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 4, "status": 0}]},timeout = 0.5)
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})

            self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
            #设置安全带解开
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 4, "status": 1}]},timeout = 0.5)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
            #设置安全带 均 系上
            self.seat_belt_status(1,1,1,1,1)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
            
    @allure.title("二排左侧自动驾驶安全带未系提醒_调用通知前安全带未系_通过安全带状态取消")
    @pytest.mark.full
    def test_caseid_1987917(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 0}})
            self.partner.empty_all(0.5)
            #当前安全带未系
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSt1', 0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 4, "status": 1}]},timeout = 0.5)
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
            #设置安全带 均 系上
            self.seat_belt_status(1,1,1,1,1)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
        
    @allure.title("二排左侧自动驾驶安全带未系提醒_调用通知前安全带已系_通过通知状态取消")
    @pytest.mark.full
    def test_caseid_1987901(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            for j in [0,1,2,12,13,14]:
                self.partner.empty_all(0.5)
                #当前安全带已系
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 1)
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                            {"out": [{"id": 4, "status": 0}]},timeout = 0.5)
                self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})

                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
                #设置安全带解开
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSt1', 0)
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                            {"out": [{"id": 4, "status": 1}]},timeout = 0.5)
                self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
                
                self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": j}})
                self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
                
    @allure.title("二排左侧自动驾驶安全带未系提醒_触发条件不满足")
    @pytest.mark.full
    def test_caseid_1987902(self):
        #安全带无故障，座椅已占位，安全带未系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        self.partner.empty_all(0.5)
        #副驾座椅未占位 SeatOccupyStatusValidity.infos.value.status=0
        self.set_four_seat_occupt(1,0,1,1)
        self.seat_belt_status(1,1,0,1,1)  
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity",
                                                {"seats": [12]},{"out": [{"value": {"seatId": 4, "status": 0}},
                                                ]},timeout=3)
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 3}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        #座椅占位
        self.set_four_seat_occupt(1,1,1,1)
        self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
        
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 0}})
        self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
        
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 12}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
    
    @allure.title("二排中侧自动驾驶安全带未系提醒_调用通知前安全带已系_通过安全带状态取消")
    @pytest.mark.full
    def test_caseid_1987903(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            self.partner.empty_all(0.5)
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 1)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 5, "status": 0}]},timeout = 0.5)
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})

            self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
            #设置安全带解开
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 5, "status": 1}]},timeout = 0.5)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)  
            #设置安全带 均 系上
            self.seat_belt_status(1,1,1,1,1)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
    
    @allure.title("二排中侧自动驾驶安全带未系提醒_调用通知前安全带未系_通过安全带状态取消")
    @pytest.mark.full
    def test_caseid_1987918(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 0}})
            self.partner.empty_all(0.5)
            #当前安全带未系
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecMidBltLockSt1', 0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 5, "status": 1}]},timeout = 0.5)
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
            #设置安全带 均 系上
            self.seat_belt_status(1,1,1,1,1)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
            
    @allure.title("二排中侧自动驾驶安全带未系提醒_调用通知前安全带已系_通过通知状态取消")
    @pytest.mark.full
    def test_caseid_1987904(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            for j in [0,1,2,12,13,14]:
                self.partner.empty_all(0.5)
                #当前安全带已系
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 1)
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                            {"out": [{"id": 5, "status": 0}]},timeout = 0.5)
                self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})

                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
                #设置安全带解开
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSt1', 0)
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                            {"out": [{"id": 5, "status": 1}]},timeout = 0.5)
                self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
                
                self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": j}})
                self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
                
    @allure.title("二排中侧自动驾驶安全带未系提醒_触发条件不满足")
    @pytest.mark.full
    def test_caseid_1987905(self):
        #安全带无故障，座椅已占位，安全带未系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        self.partner.empty_all(0.5)
        #副驾座椅未占位 SeatOccupyStatusValidity.infos.value.status=0
        self.set_four_seat_occupt(1,1,0,1)
        self.seat_belt_status(1,1,1,0,1)  
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity",
                                                {"seats": [12]},{"out": [{"value": {"seatId": 5, "status": 0}},
                                                ]},timeout=3)
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 3}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        #座椅占位
        self.set_four_seat_occupt(1,1,1,1)
        self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
        
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 0}})
        self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
        
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 12}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        
    @allure.title("二排右侧自动驾驶安全带未系提醒_调用通知前安全带已系_通过安全带状态取消")
    @pytest.mark.full
    def test_caseid_1987906(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            self.partner.empty_all(0.5)
            #当前安全带已系
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 1)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 6, "status": 0}]},timeout = 0.5)
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})

            self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
            #设置安全带解开
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 6, "status": 1}]},timeout = 0.5)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)  
            #设置安全带 均 系上
            self.seat_belt_status(1,1,1,1,1)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
            
    @allure.title("二排右侧自动驾驶安全带未系提醒_调用通知前安全带未系_通过安全带状态取消")
    @pytest.mark.full
    def test_caseid_1987919(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 0}})
            self.partner.empty_all(0.5)
            #当前安全带未系
            self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecRiBltLockSt1', 0)
            self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                        {"out": [{"id": 6, "status": 1}]},timeout = 0.5)
            self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
            #设置安全带 均 系上
            self.seat_belt_status(1,1,1,1,1)
            self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
        
    @allure.title("二排右侧自动驾驶安全带未系提醒_调用通知前安全带已系_通过通知状态取消")
    @pytest.mark.full
    def test_caseid_1987907(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        for i in [3,4,5,6,7,8,9,10,11,15,16,17]:
            for j in [0,1,2,12,13,14]:
                self.partner.empty_all(0.5)
                #当前安全带已系
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 1)
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                            {"out": [{"id": 6, "status": 0}]},timeout = 0.5)
                self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": i}})

                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
                #设置安全带解开
                self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSt1', 0)
                self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                            {"out": [{"id": 6, "status": 1}]},timeout = 0.5)
                self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
                
                self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": j}})
                self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
                
    @allure.title("二排右侧自动驾驶安全带未系提醒_触发条件不满足")
    @pytest.mark.full
    def test_caseid_1987908(self):
        #安全带无故障，座椅已占位，安全带未系f
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        #副驾座椅未占位 SeatOccupyStatusValidity.infos.value.status=0
        self.set_four_seat_occupt(1,1,1,0)
        self.seat_belt_status(1,1,1,1,0)  
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetOccupiedValidity",
                                                {"seats": [12]},{"out": [{"value": {"seatId": 6, "status": 0}},
                                                ]},timeout=3)
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 3}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        #座椅占位
        self.set_four_seat_occupt(1,1,1,1)
        self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
        
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 0}})
        self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 0, timeout=2, wti_auto=True)
        
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 12}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        
    @allure.title("自动驾驶安全带未系提醒_取消条件不满足")
    @pytest.mark.full
    def test_caseid_1987909(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(0,1,1,1,1)  
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 3}})
        self.seat_belt_status(0,1,1,0,0)  
        self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
        
        #取消条件 anpStatus不满足
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 4}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        self.partner.empty_all(0.5)
        #取消条件 有占位的乘客均系上安全带不满足,不包括主驾
        self.seat_belt_status(0,1,1,0,1)    
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 4}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
    
    @allure.title("自动驾驶安全带未系提醒_存在安全带故障")
    @pytest.mark.full
    def test_caseid_1987910(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        self.partner.empty_all(0.5)
        #先发送通知，再设置故障
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 3}})
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatusValidity", {"seats": [12]},
                                            {"out": [{"value": {"id": 1, "status": 2}},
                                                    {"value": {"id": 4, "status": 2}},
                                                    {"value": {"id": 5, "status": 2}},
                                                    {"value": {"id": 6, "status": 2}}]},timeout = 0.5)
        
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        self.seat_belt_status(1,1,1,1,1)  
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 0}})
        #先造安全带故障，再发送通知
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecLeBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecMidBltLockSts', 1)
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtRowSecRiBltLockSts', 1)
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 3}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        self.seat_belt_status(1,1,1,1,1)  
        
    @allure.title("自动驾驶安全带未系提醒_仅ub位变化不会触发event")
    @pytest.mark.full
    def test_caseid_1987911(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  

        self.partner.empty_all(0.5)
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 3}})
        #设置安全带解开
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', 0)
        self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 0, ub_flag=False)
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04,'BltLockStAtPassBltLockSts', 0, ub_flag=True)
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        self.seat_belt_status(1,1,1,1,1)  
        
    @allure.title("自动驾驶安全带未系提醒_主驾状态满足无法触发报警")
    @pytest.mark.full
    def test_caseid_1987912(self):
        #安全带无故障，座椅已占位，安全带已系
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  

        self.partner.empty_all(0.5)
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 3}})
        #设置安全带解开
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr05, 'BltLockStAtDrvrBltLockSt1', 0)
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')

    @allure.title("自动驾驶安全带未系提醒_不同座椅条件满足不会重复上报")
    @pytest.mark.full
    def test_caseid_1987914(self):
        #安全带无故障，座椅已占位，安全带已系
        self.partner.empty_all(0.5)
        self.io.driver_seat_present()
        self.set_four_seat_occupt(1,1,1,1)
        self.seat_belt_status(1,1,1,1,1)  
        #当前安全带已系
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                    {"out": [{"id": 1, "status": 0}]},timeout = 0.5)
        self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts": {"anpStatus": 3}})

        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        #设置安全带解开
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtPassBltLockSt1', 0)
        self.partner.send_request_and_ck_resp(SEAT_SERVICE_CLIENT, "GetBeltStatus", {"seats": [12]},
                                    {"out": [{"id": 1, "status": 1}]},timeout = 0.5)
        self.partner.ck_wti_warning_and_resp("Auto Driving Belt Unfasten Reminder", 1, timeout=2, wti_auto=True)
        
        self.ipdu.set(self.ipdu.backbonefr.SrsBackBoneFr04, 'BltLockStAtRowSecLeBltLockSt1', 0)
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Auto Driving Belt Unfasten Reminder')
        
    @allure.title("ANP_AccelerateIntervention")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727564?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104883(self):
        def return_struct(value):
            return {"accelerateInterventionReminder": value}

        def return_info(value):
            return value if value < 5 else 0

        self.ck_change_for_one_loop("ANP Accelerate Intervention Remind", ANPWTI_SERVICE_SERVER,
                                    "NotifyAccelerateIntervention",
                                    return_struct, 0, range(8), return_info, jump_trigger=False)

    @allure.title("ANP提醒")  #需求更新待删除
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1796998?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104840(self):
        for ccp in [2, 3, 4, 5]:
            self.sd_tester.write_single_ccp(953, ccp)
            logger.info(f"CCP953改为{ccp}")
            sleep(1)

            def return_struct(value1, value2):
                return {"anpStsReminder": {"anpStatusReminder": value1, "openSource": value2}}

            def return_info(value1, value2):
                return value1 if value2 == 2 and ccp == 2 else 0

            self.ck_change_for_two_loop("ANP Remind", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                        (0, 0),
                                        [0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 13, 113, 115, 117],
                                        range(3), return_struct, return_info, jump_trigger=False)
            
    @allure.title("ANP提醒")
    @pytest.mark.sanity
    def test_caseid_1985464(self):
        for ccp in [2, 3, 4, 5]:
            self.sd_tester.write_single_ccp(953, ccp)
            logger.info(f"CCP953改为{ccp}")
            sleep(1)
            def return_struct(value1, value2):
                return {"anpStsReminder": {"anpStatusReminder": value1, "openSource": value2}}

            def return_info(value1, value2):
                return value1 if value2 == 2 and ccp == 2 else 0
            
            def return_info1(value1, value2):
                return value1 if  ccp == 2 else 0

            self.ck_change_for_two_loop("ANP Remind", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                        (0, 0),
                                        [0, 1, 2, 4, 5, 7, 8, 9, 10, 11, 12, 13, 113, 115, 117, 142, 144, 146],
                                        range(3), return_struct, return_info, jump_trigger=False)
            self.ck_change_for_two_loop("ANP Remind", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                        (0, 0),
                                        [140],
                                        range(3), return_struct, return_info1, jump_trigger=False)
        
    @allure.title("MsgANPDegraedFaultRemind依赖信号NotifyANPDegraedFault.ANPdegraedfault")
    @pytest.mark.sanity
    def test_caseid_1988779(self):
        def return_struct(value):
            return {"fault": value}

        def return_info(value):
            return 0 if value in [3, 7] else value

        self.ck_change_for_one_loop("ANP Degraed Fault Remind", ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                    return_struct, 0, range(11), return_info, jump_trigger=False)

    @allure.title("MsgANPMRCRemind依赖信号NotifysMRCSts.MRCStatus")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727541?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104905(self):
        def return_struct(value):
            return {"sts": value}

        def return_info(value):
            return value if value in [2, 4, 5] else 0

        self.ck_change_for_one_loop("ANP MRC Remind", ANPMRC_SERVICE_SERVER, "NotifyMRCSts",
                                    return_struct, 0, range(6), return_info, jump_trigger=False)

    @allure.title("前方左侧来车预警")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727473?projectId=46')
    @pytest.mark.smoke
    def test_caseid_104970(self):
        hint = "FCTA Left Warning"
        self.partner.send_event_notify(FCTA_SERVICE_SERVER, "NotifyFCTAFunctionStatus",
                                       {"fctaFunctionStatus": {"leftWarning": 0}})
        self.partner.empty_all(0.5)
        last_info = 0
        for warning in range(4):
            self.partner.send_event_notify(FCTA_SERVICE_SERVER, "NotifyFCTAFunctionStatus",
                                           {"fctaFunctionStatus": {"leftWarning": warning}})
            new_info = warning if warning in [1, 3] else 0
            self.ck_warningmsg(hint, last_info, new_info)
            last_info = new_info

    @allure.title("前方右侧来车预警")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727519?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104926(self):
        hint = "FCTA Right Warning"
        self.partner.send_event_notify(FCTA_SERVICE_SERVER, "NotifyFCTAFunctionStatus",
                                       {"fctaFunctionStatus": {"rightWarning": 0}})
        self.partner.empty_all(0.5)
        last_info = 0
        for warning in range(4):
            self.partner.send_event_notify(FCTA_SERVICE_SERVER, "NotifyFCTAFunctionStatus",
                                           {"fctaFunctionStatus": {"rightWarning": warning}})
            new_info = warning if warning in [1, 3] else 0
            self.ck_warningmsg(hint, last_info, new_info)
            last_info = new_info

    @allure.title("后向来车碰撞预警")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727497?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104947(self):
        def return_struct(value):
            return {"rcwStatus": {"warning": value}}

        def return_info(value):
            return 1 if value == 3 else 0

        self.ck_change_for_one_loop("RCW Warning", RCW_SERVICE_SERVER, "NotifyRCWStatus", return_struct,
                                    0, [0, 1, 3], return_info)

    @allure.title("AEBR,后向行人紧急制动预警")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727545?projectId=46')
    @pytest.mark.smoke
    def test_caseid_104901(self):
        def return_struct(value):
            return {"aebRStatus": {"activeSts": value}}

        def return_info(value):
            return value if value in [1, 3] else 0

        self.ck_change_for_one_loop("AEBR Warning", AEBR_SERVICE_SERVER, "NotifyAEBRStatus", return_struct,
                                    0, [0, 1, 3], return_info)

    @allure.title("RCTA,后侧来车预警及制动-leftWarning")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727547?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104899(self):
        def return_struct(value):
            return {"rctaFunctionStatus": {"leftWarning": value, "rightWarning": 0}}

        def return_info(value):
            return value

        self.ck_change_for_one_loop("RCTA Warning", RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus", return_struct,
                                    0, range(4), return_info)

    @allure.title("RCTA,后侧来车预警及制动-rightWarning")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727501?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104943(self):
        def return_struct(value):
            return {"rctaFunctionStatus": {"rightWarning": value, "leftWarning": 0}}

        def return_info(value):
            return value

        self.ck_change_for_one_loop("RCTA Warning", RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus", return_struct,
                                    0, range(4), return_info)

        self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                       {"rctaFunctionStatus": {"rightWarning": 1, "leftWarning": 2}})
        self.partner.ck_wti_warning_and_resp("RCTA Warning", 2, wti_auto=True)

        self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                       {"rctaFunctionStatus": {"rightWarning": 3, "leftWarning": 2}})
        self.partner.ck_wti_warning_and_resp("RCTA Warning", 3, wti_auto=True)

        self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                       {"rctaFunctionStatus": {"rightWarning": 1, "leftWarning": 1}})
        self.partner.ck_wti_warning_and_resp("RCTA Warning", 1, wti_auto=True)

    @allure.title("DOW,左侧开门预警")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727487?projectId=46')
    @pytest.mark.smoke
    def test_caseid_104957(self):
        def return_struct(value):
            return {"dowStatus": {"leftWarning": value}}

        def return_info(value):
            return 1 if value == 3 else 0

        self.ck_change_for_one_loop("DOW Left Warning", DOW_SERVICE_SERVER, "NotifyDOWStatus", return_struct,
                                    0, [0, 1, 3], return_info)

    @allure.title("DOW,右侧开门预警")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727526?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104919(self):
        def return_struct(value):
            return {"dowStatus": {"rightWarning": value}}

        def return_info(value):
            return 1 if value == 3 else 0

        self.ck_change_for_one_loop("DOW Right Warning", DOW_SERVICE_SERVER, "NotifyDOWStatus", return_struct,
                                    0, [0, 1, 3], return_info)

    @allure.title("LCA,左侧并线预警")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727482?projectId=46')
    @pytest.mark.smoke
    def test_caseid_104962(self):
        def return_struct(value):
            return {"lcaStatus": {"leftWarning": value}}

        def return_info(value):
            return 1 if value == 3 else 0

        self.ck_change_for_one_loop("LCA Left Warning", LCA_SERVICE_SERVER, "NotifyLCAStatus", return_struct,
                                    0, range(5), return_info)

    @allure.title("LCA,右侧并线预警")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727503?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104941(self):
        def return_struct(value):
            return {"lcaStatus": {"rightWarning": value}}

        def return_info(value):
            return 1 if value == 3 else 0

        self.ck_change_for_one_loop("LCA Right Warning", LCA_SERVICE_SERVER, "NotifyLCAStatus", return_struct,
                                    0, range(5), return_info)

    @allure.title("LDW,左侧压线预警")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727563?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104884(self):
        def return_struct(value):
            return {"lasFunctionStatus": {"activeSts": value}}

        def return_info(value):
            return 1 if value == 1 else 0

        self.ck_change_for_one_loop("LDW Left Warning", LKA_SERVICE_SERVER, "NotifyLKAFunctionStatus", return_struct,
                                    0, range(3), return_info)

    @allure.title("LDW,右侧压线预警")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727475?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104969(self):
        def return_struct(value):
            return {"lasFunctionStatus": {"activeSts": value}}

        def return_info(value):
            return 1 if value == 2 else 0

        self.ck_change_for_one_loop("LDW Right Warning", LKA_SERVICE_SERVER, "NotifyLKAFunctionStatus", return_struct,
                                    0, range(3), return_info)
    #回退
    # @allure.title("红绿灯识别及提醒")
    # @pytest.mark.smoke
    # def test_caseid_1989153(self):
    #     def return_struct(value1, value2):
    #         return {"tlaFunctionStatus": {"startRemid": value1, "runRedLightReminder": value2}}

    #     def return_info(value1, value2):
    #         if value2 == 1:
    #             return 1
    #         elif value1 == 2:
    #             return 2
    #         elif value1 == 1:
    #             return 5
    #         else:
    #             return 0

    #     self.ck_change_for_two_loop("Traffic Light Identification Remind", TLA_SERVICE_SERVER,
    #                                 "NotifyTLAFunctionStatus", (0, 0), range(5), [0, 1], return_struct, return_info,
    #                                 jump_trigger=True)
    
    @allure.title("红绿灯识别及提醒")
    @pytest.mark.smoke
    def test_caseid_1985830(self):
        def return_struct(value1, value2):
            return {"tlaFunctionStatus": {"startRemid": value1, "runRedLightReminder": value2}}

        def return_info(value1, value2):
            if value2 == 1:
                return 1
            elif value1 == 2 or value1 == 1:
                return 2
            else:
                return 0

        self.ck_change_for_two_loop("Traffic Light Identification Remind", TLA_SERVICE_SERVER,
                                    "NotifyTLAFunctionStatus", (0, 0), range(5), [0, 1], return_struct, return_info,
                                    jump_trigger=True)
        
    @allure.title("车外摄像头未标定提示-NotifyCameraSts")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727510?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104934(self):
        cameras = ["frontAVMCamera", "leftAVMCamera", "rightAVMCamera", "rearAVMCamera", "frontCamera",
                   "wideAngleCamera", "narrowAngleCamera", "rearCamera", "frontSideLeftCamera",
                   "frontSideRightCamera", "rearSideLeftCamera", "rearSideRightCamera"]
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {camera: {"isCalibrated": True} for camera in cameras}})

        self.partner.empty_all(0.5)
        last_info = 0
        for sts in [True, False]:
            self.partner.send_event_notify(FrontBackupCamera_SERVICE_SERVER, 'NotifyFrontCameraSts',
                                           {"frontCameraPrm": {"isCalibrated": sts}})
            for camera in cameras:
                for isCalibrated in [True, False, True]:
                    self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                                   {"cameraSts": {camera: {"isCalibrated": isCalibrated}}})
                    new_info = 1 if not isCalibrated else 0
                    self.ck_warningmsg('Camera Not Calibrated Warning', last_info, new_info, jump_trigger=True)
                    last_info = new_info

    @allure.title("毫米波雷达未标定提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727485?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104959(self):
        for radar in ["frontRadarSts", "rearLeftRadarSts", "rearRightRadarSts", "frontLeftRadarSts",
                      "frontRightRadarSts"]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                           {"radarFaultInfo": {radar: {"isCalibrated": False}}})
            self.partner.empty_all(0.5)
            for isCalibrated in [True, False]:
                self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                               {"radarFaultInfo": {radar: {"isCalibrated": isCalibrated}}})
                self.partner.ck_wti_warning_and_resp("Radar Not Calibrated Warning",
                                               1 if not isCalibrated else 0, wti_auto=True)

    @allure.title("智驾惯性测量单元未标定提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727469?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104974(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyIMUStatus",
                                       {"imuStatus": {"isCalibrationed": False}})
        self.partner.empty_all(0.5)

        for isCalibrationed in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyIMUStatus",
                                           {"imuStatus": {"isCalibrationed": isCalibrationed}})
            self.partner.ck_wti_warning_and_resp("AD IMU Cali Warning",
                                           1 if not isCalibrationed else 0, wti_auto=True)

        for isCalibrationed in [True, False]:
            self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBIMUStatus",
                                           {"status": {"isCalibrationed": isCalibrationed}})
            self.partner.ck_wti_warning_and_resp("AD IMU Cali Warning",
                                           1 if not isCalibrationed else 0, wti_auto=True)

    @allure.title("前向碰撞预警及制动FCW-AEB故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727558?projectId=46')
    @pytest.mark.smoke
    def test_caseid_104888(self):
        def return_struct(value):
            return {"cmsfStatus": {"faultSts": value}}

        def return_info(value):
            return 1 if value == 2 else 0

        self.ck_change_for_one_loop("FCW_AEB Failed Warning", CMSF_SERVICE_SERVER, "NotifyCMSFStatus", return_struct,
                                    0, range(3), return_info)

    @allure.title("前向碰撞预警及制动FCW-AEB受限提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727467?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104976(self):
        def return_struct(value):
            return {"cmsfStatus": {"faultSts": value}}

        def return_info(value):
            return 1 if value == 1 else 0

        self.ck_change_for_one_loop("FCW_AEB Restricted Warning", CMSF_SERVICE_SERVER, "NotifyCMSFStatus",
                                    return_struct,
                                    0, range(3), return_info)
        
    #2.1待验证    
    @allure.title("删除需求不应该被触发")
    @pytest.mark.sanity
    def test_caseid_1987948(self): 
        self.partner.send_event_notify(FCTA_SERVICE_SERVER, "NotifyFCTAFunctionStatus",
                                       {"fctaFunctionStatus": {"faultSts": 0}})
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                                       {"rcwStatus": {"faultSts": 0}})
        self.partner.send_event_notify(SAS_SERVICE_SERVER, "NotifyTrafficSignStatus",
                                      {"trafficSignStatus": {"faultSts": 0}})
        self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
                                      {"tlaFunctionStatus": {"faultSts": 0}})
        self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                      {"allAHBCFunctionSts": {"faultSts": 0}})
        self.partner.send_event_notify(DOW_SERVICE_SERVER, "NotifyDOWStatus",
                                      {"dowStatus": {"faultSts": 0}})
        self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                     {"rctaFunctionStatus": {"faultSts": 0}})
        self.partner.send_event_notify(AEBR_SERVICE_SERVER, "NotifyAEBRStatus",
                                     {"aebRStatus": {"faultSts": 0}})
        self.partner.send_event_notify(LCA_SERVICE_SERVER, "NotifyLCAStatus",
                                     {"lcaStatus": {"faultSts": 0}})
        self.partner.send_event_notify(LKA_SERVICE_SERVER, "NotifyLKAFunctionStatus",
                                     {"lasFunctionStatus": {"faultSts": 0}})
        self.partner.send_event_notify(AUTOTURNLAMPCTRL_SERVICE_SERVER, "AutoCtrlTurnLampSts",
                                     {"sts": {"faultSts": 0}})
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"faultSts": 0}})
        
        sleep(0.5)
        self.partner.send_event_notify(FCTA_SERVICE_SERVER, "NotifyFCTAFunctionStatus",
                                       {"fctaFunctionStatus": {"faultSts": 2}})
        self.partner.send_event_notify(FCTA_SERVICE_SERVER, "NotifyFCTAFunctionStatus",
                                       {"fctaFunctionStatus": {"faultSts": 1}})
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                                       {"rcwStatus": {"faultSts": 2}})
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                                       {"rcwStatus": {"faultSts": 1}})
        self.partner.send_event_notify(SAS_SERVICE_SERVER, "NotifyTrafficSignStatus",
                                      {"trafficSignStatus": {"faultSts": 2}})
        self.partner.send_event_notify(SAS_SERVICE_SERVER, "NotifyTrafficSignStatus",
                                      {"trafficSignStatus": {"faultSts": 1}})
        self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
                                      {"tlaFunctionStatus": {"faultSts": 2}})
        self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
                                      {"tlaFunctionStatus": {"faultSts": 1}})
        self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                      {"allAHBCFunctionSts": {"faultSts": 1}})
        self.partner.send_event_notify(DOW_SERVICE_SERVER, "NotifyDOWStatus",
                                      {"dowStatus": {"faultSts": 2}})
        self.partner.send_event_notify(DOW_SERVICE_SERVER, "NotifyDOWStatus",
                                      {"dowStatus": {"faultSts": 1}})
        self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                     {"rctaFunctionStatus": {"faultSts": 2}})
        self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                     {"rctaFunctionStatus": {"faultSts": 1}})
        self.partner.send_event_notify(AEBR_SERVICE_SERVER, "NotifyAEBRStatus",
                                     {"aebRStatus": {"faultSts": 2}})
        self.partner.send_event_notify(AEBR_SERVICE_SERVER, "NotifyAEBRStatus",
                                     {"aebRStatus": {"faultSts": 1}})
        self.partner.send_event_notify(LCA_SERVICE_SERVER, "NotifyLCAStatus",
                                     {"lcaStatus": {"faultSts": 2}})
        self.partner.send_event_notify(LCA_SERVICE_SERVER, "NotifyLCAStatus",
                                     {"lcaStatus": {"faultSts": 1}})
        self.partner.send_event_notify(LKA_SERVICE_SERVER, "NotifyLKAFunctionStatus",
                                     {"lasFunctionStatus": {"faultSts": 2}})
        self.partner.send_event_notify(LKA_SERVICE_SERVER, "NotifyLKAFunctionStatus",
                                     {"lasFunctionStatus": {"faultSts": 1}})
        self.partner.send_event_notify(AUTOTURNLAMPCTRL_SERVICE_SERVER, "AutoCtrlTurnLampSts",
                                     {"sts": {"faultSts": 2}})
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"faultSts": 2}})
        
        self.partner.ck_no_event(SEAT_SERVICE_CLIENT, "WarningMsgList")

    @allure.title("前视远距摄像头自清洁失败提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727580?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104867(self):
        hint = "Front View Camera Clean Failed Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                       {"cameraCleanSts": {"narrowAngleCamera": {"isDirty": False}}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                               {"occludedScenes": occludedScenes})
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                               {"cameraCleanSts": {"narrowAngleCamera": {"isDirty": sts}}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("前视广角摄像头自清洁失败提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727546?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104900(self):
        hint = "Wide Angle Camera Clean Failed Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                       {"cameraCleanSts": {"wideAngleCamera": {"isDirty": False}}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                            {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                               {"cameraCleanSts": {"wideAngleCamera": {"isDirty": sts}}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("其它摄像头被遮挡提示-frontAVMCamera")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727572?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104875(self):
        hint = "Front AVMCamera Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                       {"cameraCleanSts": {"frontAVMCamera": {"isDirty": False}}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                               {"cameraCleanSts": {"frontAVMCamera": {"isDirty": sts}}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("其它摄像头被遮挡提示-leftAVMCamera")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727537?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104908(self):
        hint = "Left AVMCamera Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                       {"cameraCleanSts": {"leftAVMCamera": {"isDirty": False}}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                               {"cameraCleanSts": {"leftAVMCamera": {"isDirty": sts}}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("其它摄像头被遮挡提示-rightAVMCamera")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727494?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104950(self):
        hint = "Right AVMCamera Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                       {"cameraCleanSts": {"rightAVMCamera": {"isDirty": False}}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                               {"cameraCleanSts": {"rightAVMCamera": {"isDirty": sts}}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("其它摄像头被遮挡提示-rearAVMCamera")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727529?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104916(self):
        hint = "Rear AVMCamera Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                       {"cameraCleanSts": {"rearAVMCamera": {"isDirty": False}}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                               {"cameraCleanSts": {"rearAVMCamera": {"isDirty": sts}}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("其它摄像头被遮挡提示-rearCamera")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727525?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104920(self):
        hint = "Rear Camera Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                       {"cameraCleanSts": {"rearCamera": {"isDirty": False}}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                               {"cameraCleanSts": {"rearCamera": {"isDirty": sts}}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("其它摄像头被遮挡提示-frontSideLeftCamera")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727565?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104882(self):
        hint = "Front Side Left Camera Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                       {"cameraCleanSts": {"frontSideLeftCamera": {"isDirty": False}}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                               {"cameraCleanSts": {"frontSideLeftCamera": {"isDirty": sts}}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("其它摄像头被遮挡提示-frontSideRightCamera")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727513?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104932(self):
        hint = "Front Side Right Camera Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                       {"cameraCleanSts": {"frontSideRightCamera": {"isDirty": False}}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                               {"cameraCleanSts": {"frontSideRightCamera": {"isDirty": sts}}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("其它摄像头被遮挡提示-rearSideLeftCamera")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727566?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104881(self):
        hint = "Rear Side Left Camera Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                       {"cameraCleanSts": {"rearSideLeftCamera": {"isDirty": False}}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                               {"cameraCleanSts": {"rearSideLeftCamera": {"isDirty": sts}}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("其它摄像头被遮挡提示-rearSideRightCamera")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727575?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104872(self):
        hint = "Rear Side Right Camera Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                       {"cameraCleanSts": {"rearSideRightCamera": {"isDirty": False}}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyCameraCleanSts",
                                               {"cameraCleanSts": {"rearSideRightCamera": {"isDirty": sts}}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("毫米波雷达被遮挡提示,Front")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727459?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104984(self):
        hint = "Front Radar Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyRadarCleanSts",
                                       {"radarCleanSts": {"isFrontRadarBlocked": False}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyRadarCleanSts",
                                               {"radarCleanSts": {"isFrontRadarBlocked": sts}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("毫米波雷达被遮挡提示,FrontLeft")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727472?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104971(self):
        hint = "Front Left Radar Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyRadarCleanSts",
                                       {"radarCleanSts": {"isFrontLeftRadarBlocked": False}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyRadarCleanSts",
                                               {"radarCleanSts": {"isFrontLeftRadarBlocked": sts}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("毫米波雷达被遮挡提示,FrontRight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727562?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104885(self):
        hint = "Front Right Radar Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyRadarCleanSts",
                                       {"radarCleanSts": {"isFrontRightRadarBlocked": False}})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyRadarCleanSts",
                                               {"radarCleanSts": {"isFrontRightRadarBlocked": sts}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("毫米波雷达被遮挡提示,RearLeft")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727465?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104978(self):
        hint = "Rear Left Radar Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyRadarCleanSts",
                                       {"radarCleanSts": {"isRearLeftRadarBlocked": False}})
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{'name': 'Rear Left Radar Blocked Remind', 'info': '0'},
                                                ]})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyRadarCleanSts",
                                               {"radarCleanSts": {"isRearLeftRadarBlocked": sts}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("毫米波雷达被遮挡提示,RearRight")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727464?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104979(self):
        hint = "Rear Right Radar Blocked Remind"
        self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyRadarCleanSts",
                                       {"radarCleanSts": {"isRearRightRadarBlocked": False}})
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{'name': 'Rear Right Radar Blocked Remind', 'info': '0'},
                                                ]})
        self.partner.empty_all(0.5)
        last_info = 0
        for occludedScenes in range(4):
            self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifySensorSelfCleanUsageScenario",
                                           {"occludedScenes": occludedScenes})
            for sts in [True, False]:
                new_info = 1 if sts else 0
                self.partner.send_event_notify(SensorSelfClean_SERVICE_SERVER, "NotifyRadarCleanSts",
                                               {"radarCleanSts": {"isRearRightRadarBlocked": sts}})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True, timeout=0.5)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("左侧摄像头故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727577?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104870(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"leftAVMCamera": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"leftAVMCamera": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Left AVM Camera Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("右侧摄像头故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727463?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104980(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"rightAVMCamera": {"isFault": False}}})
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{'name': 'Right AVM Camera Fault Warning', 'info': '0'},
                                                ]})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"rightAVMCamera": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Right AVM Camera Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("后方摄像头故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727532?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104913(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"rearAVMCamera": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"rearAVMCamera": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Rear AVM Camera Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("前方摄像头故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727539?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104917(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"frontAVMCamera": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"frontAVMCamera": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Front AVM Camera Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("120_deg摄像头故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727493?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104951(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"wideAngleCamera": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"wideAngleCamera": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Wide Angle Camera Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("30_deg摄像头故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727488?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104956(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"narrowAngleCamera": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"narrowAngleCamera": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Narrow Angle Camera Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("后视摄像头故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727462?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104981(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"rearCamera": {"isFault": False}}})
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{'name': 'Rear Camera Fault Warning', 'info': '0'},
                                                ]})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"rearCamera": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Rear Camera Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("前向左侧摄像头故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727515?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104930(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"frontSideLeftCamera": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"frontSideLeftCamera": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Front Left Camera Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("前向右侧摄像头故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727476?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104968(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"frontSideRightCamera": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"frontSideRightCamera": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Front Right Camera Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("后向左侧摄像头故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727549?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104897(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"rearSideLeftCamera": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"rearSideLeftCamera": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Rear Left Camera Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("后向右侧摄像头故障提示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727556?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104890(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                       {"cameraSts": {"rearSideRightCamera": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyCameraSts",
                                           {"cameraSts": {"rearSideRightCamera": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Rear Right Camera Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("前毫米波雷达故障显示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727514?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104931(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                       {"radarFaultInfo": {"frontRadarSts": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                           {"radarFaultInfo": {"frontRadarSts": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Front Radar Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("左前毫米波雷达故障显示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727518?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104927(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                       {"radarFaultInfo": {"frontLeftRadarSts": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                           {"radarFaultInfo": {"frontLeftRadarSts": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Front Left Radar Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("右前毫米波雷达故障显示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727568?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104879(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                       {"radarFaultInfo": {"frontRightRadarSts": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                           {"radarFaultInfo": {"frontRightRadarSts": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Front Right Radar Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("左后毫米波雷达故障显示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727508?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104936(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                       {"radarFaultInfo": {"rearLeftRadarSts": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                           {"radarFaultInfo": {"rearLeftRadarSts": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Rear Left Radar Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("右后毫米波雷达故障显示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727523?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104922(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                       {"radarFaultInfo": {"rearRightRadarSts": {"isFault": False}}})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyRadarFaultInfo",
                                           {"radarFaultInfo": {"rearRightRadarSts": {"isFault": isFault}}})
            self.partner.ck_wti_warning_and_resp("Rear Right Radar Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("脱手检测HOD故障显示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727505?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104939(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyHODFaultSts", {"isFault": False})
        self.partner.empty_all(0.5)
        for isFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyHODFaultSts", {"isFault": isFault})
            self.partner.ck_wti_warning_and_resp("HOD Fault Warning", 1 if isFault else 0, wti_auto=True)

    @allure.title("智驾系统故障显示")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727552?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104894(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyACUFault", {"isACUFault": False})
        self.partner.empty_all(0.5)
        for isACUFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyACUFault", {"isACUFault": isACUFault})
            self.partner.ck_wti_warning_and_resp("ACU Fault Warning", 1 if isACUFault else 0, wti_auto=True)

    @allure.title("BACU故障")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727499?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104945(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyBACUStsFromACU",
                                       {"isBACUFault": False})
        self.partner.empty_all(0.5)
        for isBACUFault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyBACUStsFromACU",
                                           {"isBACUFault": isBACUFault})
            self.partner.ck_wti_warning_and_resp("BACU Fault Warning", 1 if isBACUFault else 0, wti_auto=True)

    @allure.title("ACU通讯异常_NotifyACUNetworkClusterSts")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727559?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104887(self):
        hint = "ACU Network Warning"
        last_info = 0
        self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyCOMFaultBetweenBACUAndFLRSts",
                                       {"isCOMFaultBetweenBACUAndFLR": True})
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyACUNetworkClusterSts",
                                       {"networkClusterSts": [
                                           {"ecuSts": [
                                               {"ecuName": 0, "channel": 0,
                                                "netSts": 0}]}]})
        self.partner.ck_wti_warning_and_resp(hint, 0, wti_auto=True)
        for ecu_name in range(8):
            for netSts in [0, 1, 0]:
                new_info = netSts
                self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyACUNetworkClusterSts",
                                               {"networkClusterSts": [
                                                   {"ecuSts": [
                                                       {"ecuName": ecu_name, "channel": random.randint(0, 5),
                                                        "netSts": netSts}]}]})
                if new_info == last_info:
                    self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True)
                else:
                    self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                    last_info = new_info

    @allure.title("ACU通讯异常_NotifyCOMFaultBetweenBACUAndFLRSts")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727559?projectId=46')
    @pytest.mark.sanity
    def test_caseid_110861(self):
        hint = "ACU Network Warning"
        last_info = 0
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyACUNetworkClusterSts",
                                       {"networkClusterSts": [
                                           {"ecuSts": [
                                               {"ecuName": 1, "channel": 1,
                                                "netSts": 1}]}]})
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyCOMFaultBetweenBACUAndFLRSts",
                                       {"isCOMFaultBetweenBACUAndFLR": False})
        self.partner.ck_wti_warning_and_resp(hint, 0, wti_auto=True)
        for com_falut in [False, True, True, False]:
            new_info = 1 if com_falut else 0
            self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyCOMFaultBetweenBACUAndFLRSts",
                                           {"isCOMFaultBetweenBACUAndFLR": com_falut})
            if new_info == last_info:
                self.partner.ck_wti_no_warning_and_ck_resp(hint, new_info, wti_auto=True)
            else:
                self.partner.ck_wti_warning_and_resp(hint, new_info, wti_auto=True)
                last_info = new_info

    @allure.title("定位系统故障显示-NotifyIMUStatus")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727553?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104893(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyIMUStatus",
                                       {"imuStatus": {"isIMUFault": False}})
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyFusionGNSSFault",
                                       {"fusionGNSSFault": {"gnssFaultSts": 0}})
        self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBIMUStatus",
                                       {"status": {"isIMUFault": False}})
        self.partner.empty_all(0.5)
        for fault in [True, False]:
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyIMUStatus",
                                           {"imuStatus": {"isIMUFault": fault}})
            self.partner.ck_wti_warning_and_resp("IMU Fault Warning", 1 if fault else 0, wti_auto=True)

    @allure.title("定位系统故障显示-NotifyFusionGNSSFault")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727504?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104940(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyIMUStatus",
                                       {"imuStatus": {"isIMUFault": False}})
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyFusionGNSSFault",
                                       {"fusionGNSSFault": {"gnssFaultSts": 0}})
        self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBIMUStatus",
                                       {"status": {"isIMUFault": False}})
        self.partner.empty_all(0.5)

        def return_struct(value):
            return {"fusionGNSSFault": {"gnssFaultSts": value}}

        def return_info(value):
            return 1 if value & 1 or value & 4 else 0

        self.ck_change_for_one_loop("IMU Fault Warning", ACUFaultInfo_SERVICE_SERVER, "NotifyFusionGNSSFault",
                                    return_struct, 0, range(16), return_info)

    @allure.title("定位系统故障显示-NotifyBIMUStatus")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727520?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104925(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyIMUStatus",
                                       {"imuStatus": {"isIMUFault": False}})
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyFusionGNSSFault",
                                       {"fusionGNSSFault": {"gnssFaultSts": 0}})
        self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBIMUStatus",
                                       {"status": {"isIMUFault": False}})
        self.partner.empty_all(0.5)
        for isIMUFault in [True, False]:
            self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBIMUStatus",
                                           {"status": {"isIMUFault": isIMUFault}})
            self.partner.ck_wti_warning_and_resp("IMU Fault Warning", 1 if isIMUFault else 0, wti_auto=True)

        # 下面测试已经有一个置1，再另一个置1不会触发
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyIMUStatus",
                                       {"imuStatus": {"isIMUFault": True}})
        self.partner.ck_wti_warning_and_resp("IMU Fault Warning", 1, wti_auto=True)
        self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBIMUStatus",
                                       {"status": {"isIMUFault": True}})
        self.partner.ck_wti_no_warning_and_ck_resp("IMU Fault Warning", 1, wti_auto=True)

        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "NotifyIMUStatus",
                                       {"imuStatus": {"isIMUFault": False}})
        self.partner.ck_wti_warning_and_resp("IMU Fault Warning", 0, wti_auto=True)

    @allure.title("AEB警告信息")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727496?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104948(self):
        self.partner.send_event_notify(AEB_SERVICE_SERVER, "NotifyAEBStatus",
                                       {"aebStatus": {"functionActiveSts": 0}})
        self.partner.empty_all(0.5)
        for ActiveSts in [1, 0]:
            self.partner.send_event_notify(AEB_SERVICE_SERVER, "NotifyAEBStatus",
                                           {"aebStatus": {"functionActiveSts": ActiveSts}})
            self.partner.ck_wti_warning_and_resp("AEB Warning", 1 if ActiveSts else 0, wti_auto=True)

    @allure.title("FCW警告信息")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727490?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104954(self):
        def return_struct(value):
            return {"fcwStatus": {"warningSts": value}}

        def return_info(value):
            return value

        self.ck_change_for_one_loop("FCW Warning", FCW_SERVICE_SERVER, "NotifyFCWStatus",
                                    return_struct, 0, range(3), return_info)

    @allure.title("前向碰撞预警及制动故障")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727542?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104904(self):
        def return_struct(value):
            return {"cmsfStatus": {"faultSts": value}}

        def return_info(value):
            return 1 if value == 2 else 0

        self.ck_change_for_one_loop("CMSF Warning", CMSF_SERVICE_SERVER, "NotifyCMSFStatus",
                                    return_struct, 0, range(3), return_info)

    @allure.title("自动换挡提示")
    @pytest.mark.sanity
    def test_caseid_1989199(self):
        def return_struct(value):
            return {"autoGearShiftSts": {"driverReminder": value}}

        def return_info(value):
            if value in [1,2,3,4,5,14,15,16,17]:
                return value
            else:
                return 0

        self.ck_change_for_one_loop("Auto Gear Remind", AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                    return_struct, 0, range(18), return_info)
        
    @allure.title("自动换挡D/R互切提示")
    @pytest.mark.sanity
    def test_caseid_1989202(self):
        def return_struct(value1, value2):
           
            return {"autoGearShiftSts": {"driverReminder": value1,"targetGear":value2}}
        
        def return_info(value1, value2):
            if value1 in [6,7,8,9,10,11,12,13] and value2 in [2,3]:
                return 1
            else :
                return 0

        self.ck_change_for_two_loop("AutoGearShiftActive", AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                        (0, 0), range(18), range(4), return_struct, return_info, jump_trigger=True)
    
    #回退   
    # @allure.title("紧急转向辅助ESS激活提示")
    # @pytest.mark.smoke
    # def test_caseid_1989223(self):
    #     def return_struct(value):
    #         return {"essInfo": {"activeSts":value}}
        
    #     def return_info(value):
    #         if value in [1,2] :
    #             return 1
    #         else :
    #             return 0

    #     self.ck_change_for_one_loop("ESSActiveReminder", ESS_SERVICE_SERVER, "ESSInfo",
    #                                     return_struct, 0, range(3), return_info, jump_trigger=True)

    @allure.title("远光灯眩目提醒")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727477?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104967(self):
        self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                       {"allAHBCFunctionSts": {"glareTelltale": False}})
        self.partner.empty_all(0.5)
        for glareTelltale in [True, False]:
            self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                           {"allAHBCFunctionSts": {"glareTelltale": glareTelltale}})
            self.partner.ck_wti_warning_and_resp("High Beam Glare Remind", 1 if glareTelltale else 0, wti_auto=True)
 
    @allure.title("APA运行状态信息,系统故障-NotifyAPAReminderCycle")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727521?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104924(self):
        def return_struct(value1, value2):
            return {"reminder": {"type": value1, "lastHandleType": value2}}

        def return_info(value1, value2):
            return value1 if value1 == 1 and value2 in [0, 1, 4] else 0

        for reminder in [0, 1]:
            self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBACUWTI",
                                           {"reminder": {"APAReminder": reminder}})
            self.partner.empty_all(0.5)
            self.ck_change_for_two_loop("APA Working Status Both", RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                        (0, 0), [0, 1], range(5), return_struct, return_info, jump_trigger=False)

    @allure.title("APA运行状态信息,系统故障-NotifyBACUWTI")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727491?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104953(self):
        def return_struct(value):
            return {"reminder": {"APAReminder": value}}

        def return_info(value):
            return 1 if value == 1 else 0

        for reminder_type in [0, 1]:
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                           {"reminder": {"type": reminder_type, "lastHandleType": 0}})
            self.partner.empty_all(0.5)
            self.ck_change_for_one_loop("APA Working Status Both", BACU_SERVICE_SERVER, "NotifyBACUWTI", return_struct,
                                        0, range(8), return_info, jump_trigger=False)

    @allure.title("APA TTS 播报2_钥匙断连停止播报且不会触发播报")
    @pytest.mark.sanity
    def test_caseid_1960001(self):
        hint = "APA TTS Both"
        for zone in range(16):
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{zone}_0_BncmConnectivitySignalIPdu17', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                      'BLEKeyPrsntStsZone1', 1)
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 1, "lastHandleType": 1}})
        self.partner.ck_wti_warning_and_resp(hint, '1', wti_auto=True)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                      'BLEKeyPrsntStsZone1', 0)
        self.partner.ck_wti_warning_and_resp(hint, '0', wti_auto=True)

        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 1, "lastHandleType": 1}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", hint)

    @allure.title("APA TTS 播报2_任一蓝牙钥匙槽连接可使能播报")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727540?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104906(self):
        hint = "APA TTS Both"
        for zone in range(16):
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{zone}', 0)
        self.partner.empty_all(0.5)
        for zone in range(16):
            if zone > 1:
                self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                              f'BLEKeyPrsntStsZone{zone - 1}', 0)
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{zone}', 1)
            logger.info(f"zone{zone}=1")
            sleep(0.2)
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                           {"reminder": {"type": 1, "lastHandleType": 1}})
            self.partner.ck_wti_warning_and_resp(hint, '1', wti_auto=True)

    @allure.title("APA TTS 播报2_NotifyBACUWTI")
    @pytest.mark.sanity
    def test_caseid_104891(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                      f'BLEKeyPrsntStsZone1_0_BncmConnectivitySignalIPdu17', 1)
        sleep(0.1)
        for send_type in [0, 1]:
            self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                           {"reminder": {"type": send_type, "lastHandleType": 0}})
            self.partner.empty_all(0.5)

            def return_struct(value):
                return {"reminder": {"APAOutReminder": value}}

            def return_info(value):
                if value == 1:
                    return 1
                elif value == 2:
                    return 42
                else:
                    return 0

            self.ck_change_for_one_loop("APA TTS Both", BACU_SERVICE_SERVER, "NotifyBACUWTI", return_struct,
                                        0, [0, 1, 1, 2], return_info, jump_trigger=False)

    @allure.title("APA TTS 播报2_NotifyAPARemoteReminder")
    @pytest.mark.smoke
    def test_caseid_104896(self):
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                      f'BLEKeyPrsntStsZone1_0_BncmConnectivitySignalIPdu17', 1)
        sleep(0.1)
        for reminder in [0, 1]:
            self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBACUWTI",
                                           {"reminder": {"APAOutReminder": reminder}})
            self.partner.empty_all(0.5)

            def return_struct(value1, value2):
                return {"reminder": {"type": value1, "lastHandleType": value2}}

            def return_info(value1, value2):
                return value1 if value2 in [0, 1, 4] else 0

            self.ck_change_for_two_loop("APA TTS Both", RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        (0, 0),
                                        [1, 42, 0],
                                        range(5), return_struct, return_info, jump_trigger=False)

    @allure.title("HAVP提示信息,周期性接口通知2")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727512?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104933(self):
        for reminder in [0, 1]:
            self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBACUWTI",
                                           {"reminder": {"AVPReminder": reminder}})
            self.partner.empty_all(0.5)

            def return_struct(value1, value2):
                return {"avpReminder": {"type": value1, "source": value2}}

            def return_info(value1, value2):
                return 1 if value1 == 6 and value2 in [0, 1, 4] else 0

            self.ck_change_for_two_loop("HAVP Cycle Warn Both", AVP_SERVICE_SERVER, "NotifyAVPReminderCycle",
                                        (0, 0), [0, 6], range(5), return_struct, return_info, jump_trigger=False)

    @allure.title("HAVP提示信息,周期性接口通知2")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727509?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104935(self):
        for reminder_type in [0, 6]:
            self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyAVPReminderCycle",
                                           {"avpReminder": {"type": reminder_type, "source": 0}})
            self.partner.empty_all(0.5)

            def return_struct(value):
                return {"reminder": {"AVPReminder": value}}

            def return_info(value):
                return 1 if value == 1 else 0

            self.ck_change_for_one_loop("HAVP Cycle Warn Both", BACU_SERVICE_SERVER, "NotifyBACUWTI", return_struct,
                                        0, range(8), return_info, jump_trigger=False)

    @allure.title(
        "MsgANPDegraedFaultRemind依赖信号NotifyANPDegraedFault.ANPdegraedfault和BACUService::NotifyBACUWTI.ANPReminder")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727533?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104912(self):
        for reminder_type in [0, 3]:
            self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBACUWTI",
                                           {"reminder": {"ANPReminder": reminder_type}})
            self.partner.empty_all(0.5)

            def return_struct(value):
                return {"fault": value}

            def return_info(value):
                return 1 if value == 3 else 0

            self.ck_change_for_one_loop("ANP Degraed Fault Remind Both", ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                        return_struct, 0, range(6), return_info, jump_trigger=False)

    @allure.title(
        "MsgANPDegraedFaultRemind依赖信号NotifyANPDegraedFault.ANPdegraedfault和BACUService::NotifyBACUWTI.ANPReminder")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727557?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104889(self):
        for reminder_type in [0, 3]:
            self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                           {"fault": reminder_type})
            self.partner.empty_all(0.5)

            def return_struct(value):
                return {"reminder": {"ANPReminder": value}}

            def return_info(value):
                return 1 if value == 3 else 0

            self.ck_change_for_one_loop("ANP Degraed Fault Remind Both", BACU_SERVICE_SERVER, "NotifyBACUWTI",
                                        return_struct, 0, range(4), return_info, jump_trigger=False)

    @allure.title("驾驶员在位异常")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/testCases/1727460?projectId=46')
    @pytest.mark.sanity
    def test_caseid_104983(self):
        def return_struct(value):
            return {"driverDetection": {"occupyUnusual": value}}

        def return_info(value):
            return 1 if value else 0

        self.ck_change_for_one_loop("Driver Occupy Unusual Warning", ANPWTI_SERVICE_SERVER, "NotifyDriverDetection",
                                    return_struct, 0, [0, 0, 1, 1], return_info, jump_trigger=False)

    @allure.title("FCW的报警指示灯黄色")
    @pytest.mark.sanity
    def test_caseid_1959662(self):
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus",
                                       {"cmsfStatus": {"switchSts": True, "faultSts": 0}})
        self.partner.empty_all(0.5)
        last_state = '0'
        for switch in [False, True]:
            for faultSts in [0, 1, 2, 0]:
                curr_state = '1' if not switch or faultSts == 2 else '0'
                self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus",
                                               {"cmsfStatus": {"switchSts": switch, "faultSts": faultSts}})
                if last_state != curr_state:
                    self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "TelltaleList",
                                              {"list": [{"name": 'Yellow AEB and FCW', "state": curr_state}]},
                                              timeout=1)
                else:
                    self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "TelltaleList", "Yellow AEB and FCW")
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetTelltaleList", {},
                                                      {"out": [{"name": "Yellow AEB and FCW", "state": curr_state}]})
                last_state = curr_state

    @allure.title("FCW的报警指示灯红色")
    @pytest.mark.smoke
    def test_caseid_111456(self):
        self.partner.send_event_notify(AEB_SERVICE_SERVER, "NotifyAEBStatus", {"aebStatus": {"functionActiveSts": 0}})
        self.partner.send_event_notify(FCW_SERVICE_SERVER, "NotifyFCWStatus", {"fcwStatus": {"warningSts": 0}})
        self.partner.empty_all(0.5)
        last_state = '0'

        def func1(last_state, curr_state):
            if last_state != curr_state:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "TelltaleList",
                                          {"list": [{"name": 'Red AEB and FCW', "state": curr_state}]},
                                          timeout=1)
            else:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "TelltaleList", "Red AEB and FCW")
            self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetTelltaleList", {},
                                                  {"out": [{"name": "Red AEB and FCW", "state": curr_state}]})

        for functionActiveSts in [0, 1, 0]:
            for warningSts in [0, 1, 2, 0]:
                curr_state = '1' if functionActiveSts == 1 else '0'
                self.partner.send_event_notify(AEB_SERVICE_SERVER, "NotifyAEBStatus",
                                               {"aebStatus": {"functionActiveSts": functionActiveSts}})
                func1(last_state, curr_state)
                last_state = curr_state

                curr_state = '1' if warningSts in [1, 2] else '0'
                self.partner.send_event_notify(FCW_SERVICE_SERVER, "NotifyFCWStatus",
                                               {"fcwStatus": {"warningSts": warningSts}})

                func1(last_state, curr_state)
                last_state = curr_state

    @allure.title("辅助驾驶退出提醒")
    @pytest.mark.sanity
    def test_caseid_1988772(self):
        def return_struct(value):
            return {"reminder": value}

        def return_info(value):
           if value in [1,5] :
               return 1
           elif value == 4:
               return 4
           else:
               return 0

        self.ck_change_for_one_loop("Take Over Remind", ANPMRC_SERVICE_SERVER, "NotifyAffectADOperationReminder",
                                    return_struct, 0, [1, 1, 2, 3, 4, 5, 0], return_info, jump_trigger=True)
        
    @allure.title("辅助驾驶控灯中，请勿操控转向灯")
    @pytest.mark.sanity
    def test_caseid_1979674(self):
        def return_struct(value):
            return {"turnLampCtrlReminderSts": value}

        def return_info(value):
            return 1 if value == 1 else 0

        self.ck_change_for_one_loop("Turn Lamp Ctrl Remind", ANPWTI_SERVICE_SERVER, "TurnLampCtrlReminderSts",
                                    return_struct, 0, [0, 1, 1], return_info, jump_trigger=False)
    
    @allure.title("MsgANPObstacleRemind 依赖信号NotifyBarrierPerception.obstaclewarn")
    @pytest.mark.sanity
    def test_caseid_1983315(self):  # V1.4新增用例 http://172.18.128.183:8080/2023_12_21_22_58_53
        def return_struct(value):
            return {"barrierPerception": {"obstaclewarn": value}}

        def return_info(value):
            return 2 if value == 2 else 0

        self.ck_change_for_one_loop("ANP Obstacle Remind", ANPWTI_SERVICE_SERVER,
                                    "NotifyBarrierPerception",
                                    return_struct, 0, [0, 1, 2, 2, 0], return_info, jump_trigger=False)
    
    @allure.title("无法自动变道")
    @pytest.mark.sanity
    def test_caseid_1983316(self):  # V1.4新增用例
        def return_struct(value):
            return {"sts": {"anyCamera": value}}

        def return_info(value):
            return 1 if value else 0

        self.ck_change_for_one_loop("Lane Change Fault", ANPMRC_SERVICE_SERVER,
                                    "CameraNightOcclusionSts",
                                    return_struct, False, [False, True, True, False], return_info, jump_trigger=True)
    @allure.title("ACC巡航车速提醒")
    @pytest.mark.sanity
    def test_caseid_1984076(self):  # V1.4新增用例
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed", {"accSpeed":{"enableAdjustSpeedReason": 0}})
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed", {"accSpeed":{"enableAdjustSpeedReason": 0}})

        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'ACC Speed Remind')
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{'name': 'ACC Speed Remind', 'info': '0'},
                                                ]})
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed",{"accSpeed":{"enableAdjustSpeedReason": 6}})
        self.partner.ck_wti_warning_and_resp('ACC Speed Remind', 6,wti_auto=True)
        
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed",{"accSpeed":{"enableAdjustSpeedReason": 6}})
        self.partner.ck_wti_warning_and_resp('ACC Speed Remind', 6,wti_auto=True)
        
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed", {"accSpeed":{"enableAdjustSpeedReason": 0}})
        self.partner.ck_wti_warning_and_resp('ACC Speed Remind', 0,wti_auto=True)
        

    @allure.title("环境黑暗提示")
    @pytest.mark.sanity
    def test_caseid_1984081(self):  # V1.4新增用例
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder", {"reminder": 0})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder", {"reminder": 0})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Dark Status Remind')
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{'name': 'Dark Status Remind', 'info': '0'},
                                                        ]})
        
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder", {"reminder": 1})
        self.partner.ck_wti_warning_and_resp('Dark Status Remind', 1,wti_auto=True)
        
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder", {"reminder": 2})
        self.partner.ck_wti_warning_and_resp('Dark Status Remind', 2,wti_auto=True)
        
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder", {"reminder": 2})
        self.partner.ck_wti_warning_and_resp('Dark Status Remind', 2,wti_auto=True)
        
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder", {"reminder": 0})
        self.partner.ck_wti_warning_and_resp('Dark Status Remind', 0,wti_auto=True)
    
    #回退
    # @allure.title("紧急车道保持功能提醒_依赖ELKService.activeSts")
    # @pytest.mark.sanity
    # def test_caseid_1989197(self): 
    #     self.partner.empty_all(0.5)
    #     def return_struct(value1, value2):
    #         return {"sts":{"switchSts": value1, "activeSts": value2}}
        
    #     def return_info(value1, value2):
    #         return value2 if value1 in [1,2] and value2 in [1,2,0] else 0
        
    #     self.ck_change_for_two_loop("Emergency Lane Keeping Active Reminder", ELKSERVICE_SERVER, "ELKSts",
    #                                 (0, 0), [0,1,2], range(3), return_struct, return_info, jump_trigger=True)
        
    @allure.title("紧急车道保持功能提醒_依赖ELKService.activeSts")
    @pytest.mark.sanity
    def test_caseid_1985873(self): 
        self.partner.empty_all(0.5)
        def return_struct(value1, value2):
            return {"sts":{"switchSts": value1, "activeSts": value2}}
        
        def return_info(value1, value2):
            return value2 if value1 == 1 and value2 in [1,2,0] else 0
        
        self.ck_change_for_two_loop("Emergency Lane Keeping Active Reminder", ELKSERVICE_SERVER, "ELKSts",
                                    (0, 0), [0,1], range(3), return_struct, return_info, jump_trigger=True)
     
    @allure.title("ANP_ANPStatusReminder&openSource")
    @pytest.mark.sanity  
    def test_caseid_1988914(self): 
        def return_struct(value1, value2):
            return {"anpStsReminder": {"anpStatusReminder": value1, "openSource": value2}}
        def return_info(value1, value2):
            if value2 != 2:
                return 0
            elif value1 == 57:
                return 56
            else:
                return value1

        self.ck_change_for_two_loop("ANP Status Open Source", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                    (0, 0),
                                    [14, 0, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 41, 43, 44, 45, 46, 49, 50, 51,
                                     52, 53, 54, 55, 56, 57, 137, 138, 139, 148, 149, 150, 151, 152, 153, 155, 156, 157, 160,
                                     161, 162, 167],
                                    range(3), return_struct, return_info, jump_trigger=False)
    
    @allure.title("ANP_功能状态机变化提示_1.4New")
    @pytest.mark.sanity
    def test_caseid_1984083(self):
        def return_struct(value1, value2):
            return {"anpStsReminder": {"anpStatusReminder": value1, "openSource": value2}}

        def return_info(value1, value2):
            if value1 == 58 and value2 == 2:
                return 1
            elif value1 == 58 and value2 == 1:
                return 2
            elif value1 == 138 and value2 == 0:
                return 2
            elif value1 == 138 and value2 == 1:
                return 2
            elif value1 == 59 and value2 == 2:
                return 3
            elif value1 == 59 and value2 == 0:
                return 3
            elif value1 == 59 and value2 == 1:
                return 4
            elif value1 == 139 and value2 == 0:
                return 4
            elif value1 == 139 and value2 == 1:
                return 4
            else:
                return 0

        self.ck_change_for_two_loop("ANP SM Change Status Remind2", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                    (0, 0),
                                    [0, 58, 59, 138, 139],
                                    range(3), return_struct, return_info, jump_trigger=False)
        
    @allure.title("功能状态机变化提示_无法开启车道保持")
    @pytest.mark.sanity
    def test_caseid_1988773(self):
        def return_struct(value1, value2):
            return {"anpStsReminder": {"anpStatusReminder": value1, "openSource": value2}}

        def return_info1(value1, value2):
            if value1 in[163,165] and value2 == 2:
                return value1
            else:
                return 0
        def return_info2(value1, value2):
            if value1 in[163,165] and value2 == 2:
                return value1+1
            else:
                return 0
        self.sd_tester.write_single_ccp(953, 2)
        self.ck_change_for_two_loop("ANP SM Change Status Remind2", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                    (0, 0),
                                    [0, 163, 164, 165, 165 ,166, 0],
                                    range(3), return_struct, return_info1, jump_trigger=False)
        self.sd_tester.write_single_ccp(953, 5)
        self.ck_change_for_two_loop("ANP SM Change Status Remind2", ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                    (0, 0),
                                    [0, 163, 164, 165, 165, 166, 0],
                                    range(3), return_struct, return_info2, jump_trigger=False)
        
    @allure.title("ACU服务接口时效性判定")
    @pytest.mark.full
    def test_caseid_1984674(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type": 0, "lastHandleType": 0}})
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                        {"reminder": {"type": 0, "lastHandleType": 0}})
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyAVPReminderEvent",
                                       {"avpReminder": {"type": 0, "source": 0}})
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyAVPReminderCycle",
                                       {"avpReminder": {"type": 0, "source": 0}})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyAccelerateIntervention",
                                       {"accelerateInterventionReminder": 0})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyPNCReminder",
                                       {"pncReminder": 0})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 0}})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPLaneChangeReminder",
                                       {"anpLaneChangeReminder": {"reminder": 0, "openSource": 0}})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "TurnLampCtrlReminderSts",
                                       {"turnLampCtrlReminderSts": 0})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder", {"reminder": 0})
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault", {"fault": 0})
        self.partner.send_event_notify(BACU_SERVICE_SERVER, "NotifyBACUWTI", 
                                       {"reminder": {"type": 0, "lastHandleType": 0}})
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed", {"accSpeed":{"enableAdjustSpeedReason": 0}})
        #1.NotifyAPAReminderEvent
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type": 2, "lastHandleType": 1}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'APA Working Status', 'info': '2'}]})
        #2.NotifyAPAReminderCycle
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                        {"reminder": {"type": 47, "lastHandleType": 1}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'APA Working Status Cycle', 'info': '47'}]})
        #3.NotifyAPARemoteReminder
        hint = "APA TTS"
        for zone in range(16):
            self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                          f'BLEKeyPrsntStsZone{zone}', 0)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                      'BLEKeyPrsntStsZone1', 1)
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 4, "lastHandleType": 1}})
        self.partner.ck_wti_warning_and_resp(hint, 4, wti_auto=True)
        self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr17,
                      'BLEKeyPrsntStsZone1', 0)
        self.partner.ck_wti_warning_and_resp(hint, 0, wti_auto=True)
        #4.NotifyAVPReminderEvent
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyAVPReminderEvent",
                                       {"avpReminder": {"type": 7, "source": 1}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'HAVP Warn', 'info': '7'}]})
        #5.NotifyAVPReminderCycle
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyAVPReminderCycle",
                                       {"avpReminder": {"type": 6, "source": 1}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'HAVP Cycle Warn Both', 'info': '1'}]})
        #6.NotifyAccelerateIntervention
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyAccelerateIntervention",
                                       {"accelerateInterventionReminder": 1})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'ANP Accelerate Intervention Remind', 'info': '1'}]})
        #7.NotifyPNCReminder
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyPNCReminder",
                                       {"pncReminder": 38})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'ANP PNC Remind', 'info': '38'}]}) 
        #8.NotifyANPStatus
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 14, "openSource": 2}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'ANP Status Open Source', 'info': '14'}]})
        #9.NotifyANPLaneChangeReminder
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPLaneChangeReminder",
                                       {"anpLaneChangeReminder": {"reminder": 3, "openSource": 2}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'ANP Lane Change Remind1', 'info': '3'}]})
        #10.TurnLampCtrlReminderSts
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "TurnLampCtrlReminderSts",
                                       {"turnLampCtrlReminderSts": 1})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'Turn Lamp Ctrl Remind', 'info': '1'}]})
        #11.DarkStsReminder
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder", {"reminder": 1})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'Dark Status Remind', 'info': '1'}]})
        #12.NotifyANPDegraedFault
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault", {"fault": 2})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'ANP Degraed Fault Remind', 'info': '2'}]})
        #13.NotifyBACUWTI
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                           {"fault": 3})
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyBACUWTI", {"reminder": {"ANPReminder": 3}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                   {"list":[{'name': 'ANP Degraed Fault Remind Both', 'info': '1'}]})
        #14.NotifyACCSpeed
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed", {"accSpeed":{"enableAdjustSpeedReason": 6}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list":[{'name': 'ACC Speed Remind', 'info': '6'}]})
        self.partner.empty_all(0.5)
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'APA Working Status')
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'APA Working Status Cycle')
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'APA TTS')
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'HAVP Warn')
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'HAVP Cycle Warn Both') 
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'ANP Accelerate Intervention Remind') 
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'ANP PNC Remind') 
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'ANP Status Open Source') 
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'ANP Lane Change Remind1') 
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Turn Lamp Ctrl Remind') 
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Dark Status Remind') 
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'ANP Degraed Fault Remind') 
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'ANP Degraed Fault Remind Both') 
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'ACC Speed Remind') 
    
    @allure.title("超声波雷达故障提示_左前内侧超声波雷达故障")
    @pytest.mark.sanity  
    def test_caseid_1984660(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'InsdSnsrFltFrntShoLe', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'InsdSnsrFltFrntShoLe', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front Left Inside Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Left Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Left Inside Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Left Inside Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Left Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Left Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
                
    @allure.title("超声波雷达故障提示_右前内侧超声波雷达故障")
    @pytest.mark.full  
    def test_caseid_1984842(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'InsdSnsrFltFrntShoRi', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'InsdSnsrFltFrntShoRi', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front Right Inside Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Right Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Right Inside Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Right Inside Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Right Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Right Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
    
    @allure.title("超声波雷达故障提示_左后内侧超声波雷达故障")
    @pytest.mark.full  
    def test_caseid_1984843(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'InsdSnsrFltReShoLe', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'InsdSnsrFltReShoLe', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Rear Left Inside Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Left Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Left Inside Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Left Inside Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Left Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Left Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
                          
    @allure.title("超声波雷达故障提示_右后内侧超声波雷达故障")
    @pytest.mark.full  
    def test_caseid_1984844(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'InsdSnsrFltReShoRi', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'InsdSnsrFltReShoRi', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Rear Right Inside Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Right Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Right Inside Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Right Inside Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Right Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Right Inside Ultrasonic Radar Fault Remind", "info": "0"}]})
                  
    @allure.title("超声波雷达故障提示_左前外侧超声波雷达故障")
    @pytest.mark.full  
    def test_caseid_1984845(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'OutdSnsrFltFrntShoLe', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'OutdSnsrFltFrntShoLe', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front Left Outside Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Left Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Left Outside Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Left Outside Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Left Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Left Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
    
    @allure.title("超声波雷达故障提示_右前外侧超声波雷达故障")
    @pytest.mark.full 
    def test_caseid_1984846(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'OutdSnsrFltFrntShoRi', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'OutdSnsrFltFrntShoRi', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front Right Outside Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Right Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Right Outside Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Right Outside Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Right Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Right Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
                
    @allure.title("超声波雷达故障提示_左后外侧超声波雷达故障")
    @pytest.mark.full 
    def test_caseid_1984847(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'OutdSnsrFltReShoLe', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'OutdSnsrFltReShoLe', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Rear Left Outside Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Left Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Left Outside Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Left Outside Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Left Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Left Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
    
    @allure.title("超声波雷达故障提示_右后外侧超声波雷达故障")
    @pytest.mark.full  
    def test_caseid_1984848(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'OutdSnsrFltReShoRi', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'OutdSnsrFltReShoRi', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Rear Right Outside Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Right Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Right Outside Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Right Outside Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Right Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Right Outside Ultrasonic Radar Fault Remind", "info": "0"}]})
    
    @allure.title("超声波雷达故障提示_左前边超声波雷达故障")
    @pytest.mark.full  
    def test_caseid_1984849(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'SnsrFltFrntShoSideLe', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'SnsrFltFrntShoSideLe', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front Left Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Left Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Left Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Left Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Left Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Left Ultrasonic Radar Fault Remind", "info": "0"}]})
    
    @allure.title("超声波雷达故障提示_右前边超声波雷达故障")
    @pytest.mark.full  
    def test_caseid_1984850(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'SnsrFltFrntShoSideRi', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'SnsrFltFrntShoSideRi', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front Right Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Right Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Right Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Right Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Front Right Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front Right Ultrasonic Radar Fault Remind", "info": "0"}]})
                
    @allure.title("超声波雷达故障提示_/左后边超声波雷达故障")
    @pytest.mark.full  
    def test_caseid_1984851(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'SnsrFltReShoSideLe', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'SnsrFltReShoSideLe', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Rear Left Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Left Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Left Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Left Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Left Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Left Ultrasonic Radar Fault Remind", "info": "0"}]})
    
    @allure.title("超声波雷达故障提示_右后边超声波雷达故障")
    @pytest.mark.full  
    def test_caseid_1984852(self): 
        self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'SnsrFltReShoSideRi', 0)
        self.partner.empty_all(0.5)
        for i in range(4):
            self.ipdu.set(self.ipdu.adcanfd.AcuADCANFDFr03, 'SnsrFltReShoSideRi', i)
            if i == 0 or i == 3:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Rear Right Ultrasonic Radar Fault Remind')
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Right Ultrasonic Radar Fault Remind", "info": "0"}]})
            elif i == 1:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Right Ultrasonic Radar Fault Remind", "info": "1"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Right Ultrasonic Radar Fault Remind", "info": "1"}]})
            else:
                self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "Rear Right Ultrasonic Radar Fault Remind", "info": "0"}]})
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Rear Right Ultrasonic Radar Fault Remind", "info": "0"}]})                       
    
    @allure.title("危险场景提示")
    @pytest.mark.sanity
    def test_caseid_1985123(self):  
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DangerScenceReminder", {"reminder": 0})
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DangerScenceReminder", {"reminder": 0})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Dangerous Scence Reminder')
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DangerScenceReminder", {"reminder": 1})  
        self.partner.ck_wti_warning_and_resp('Dangerous Scence Reminder', 1,wti_auto=True)  
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DangerScenceReminder", {"reminder": 2})
        self.partner.ck_wti_warning_and_resp('Dangerous Scence Reminder', 2,wti_auto=True)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DangerScenceReminder", {"reminder": 2})
        self.partner.ck_wti_warning_and_resp('Dangerous Scence Reminder', 2,wti_auto=True)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DangerScenceReminder", {"reminder": 0})
        self.partner.ck_wti_warning_and_resp('Dangerous Scence Reminder', 0,wti_auto=True)
        
    @allure.title("正在绕行中无法变道")
    @pytest.mark.sanity
    def test_caseid_1985124(self):  
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyBarrierPerception", {"barrierPerception":{"avoidanceReminder": 0}})
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyBarrierPerception", {"barrierPerception":{"avoidanceReminder": 0}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'ANP Avoidance Reminder')
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{'name': 'ANP Avoidance Reminder', 'info': '0'},
                                                        ]})
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyBarrierPerception", {"barrierPerception":{"avoidanceReminder": 5}})
        self.partner.ck_wti_warning_and_resp('ANP Avoidance Reminder', 5,wti_auto=True)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyBarrierPerception", {"barrierPerception":{"avoidanceReminder": 5}})
        self.partner.ck_wti_warning_and_resp('ANP Avoidance Reminder', 5,wti_auto=True)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyBarrierPerception", {"barrierPerception":{"avoidanceReminder": 0}})
        self.partner.ck_wti_warning_and_resp('ANP Avoidance Reminder', 0,wti_auto=True)
        
    @allure.title("前摄像头过温提醒")
    @pytest.mark.sanity
    def test_caseid_1987250(self):  
        value1 = [1,1,0,0,0,255]
        value2 = [0,1,1,0,1,255]
        value3 = [0,1,0,0,0,255]
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"wideAngleCamera": {"cameraTemperatureReminder": 0},
                                "narrowAngleCamera": {"cameraTemperatureReminder": 0},
                                "frontCamera": {"cameraTemperatureReminder": 0},
                                }})
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"wideAngleCamera": {"cameraTemperatureReminder": 0},
                                "narrowAngleCamera": {"cameraTemperatureReminder": 0},
                                "frontCamera": {"cameraTemperatureReminder": 0},
                                }})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front View Camera Over Temperature Reminder')
        for i in range(6):
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"wideAngleCamera": {"cameraTemperatureReminder": value1[i]},
                                "narrowAngleCamera": {"cameraTemperatureReminder": value2[i]},
                                "frontCamera": {"cameraTemperatureReminder": value3[i]},
                                }})
            if i == 0 or i == 4:
                self.partner.ck_wti_warning_and_resp('Front View Camera Over Temperature Reminder', 1, wti_auto=True)
            elif i == 1 or i == 2:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front View Camera Over Temperature Reminder')
            else:
                self.partner.ck_wti_warning_and_resp('Front View Camera Over Temperature Reminder', 0, wti_auto=True)
    
    @allure.title("侧向和后向摄像头过温提醒")
    @pytest.mark.sanity
    def test_caseid_1987251(self):  
        value1 = [1,1,0,0,0,255,0,0,0,0,0,0]
        value2 = [0,1,1,0,1,255,0,0,0,0,0,0]
        value3 = [0,1,1,0,0,255,1,255,0,255,0,255]
        value4 = [0,1,1,0,0,255,0,255,1,255,0,255]
        value5 = [0,1,1,0,0,255,0,255,0,255,1,0]
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"rearCamera": {"cameraTemperatureReminder": 0},
                                "frontSideLeftCamera": {"cameraTemperatureReminder": 0},
                                "frontSideRightCamera": {"cameraTemperatureReminder": 0},
                                "rearSideLeftCamera": {"cameraTemperatureReminder": 0},
                                "rearSideRightCamera": {"cameraTemperatureReminder": 0},
                                }})
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"rearCamera": {"cameraTemperatureReminder": 0},
                                "frontSideLeftCamera": {"cameraTemperatureReminder": 0},
                                "frontSideRightCamera": {"cameraTemperatureReminder": 0},
                                "rearSideLeftCamera": {"cameraTemperatureReminder": 0},
                                "rearSideRightCamera": {"cameraTemperatureReminder": 0},
                                }})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Side and Rear View Camera Over Temperature Reminder')
        for i in range(12):
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"rearCamera": {"cameraTemperatureReminder": value1[i]},
                                "frontSideLeftCamera": {"cameraTemperatureReminder": value2[i]},
                                "frontSideRightCamera": {"cameraTemperatureReminder": value3[i]},
                                "rearSideLeftCamera": {"cameraTemperatureReminder": value4[i]},
                                "rearSideRightCamera": {"cameraTemperatureReminder": value5[i]},
                                }})
            if i == 0 or i == 4 or i == 6 or i == 8 or i == 10:
                self.partner.ck_wti_warning_and_resp('Side and Rear View Camera Over Temperature Reminder', 1, wti_auto=True)
            elif i == 1 or i == 2:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Side and Rear View Camera Over Temperature Reminder')
            else:
                self.partner.ck_wti_warning_and_resp('Side and Rear View Camera Over Temperature Reminder', 0, wti_auto=True) 
                
    @allure.title("环视(AVM)摄像头过温提醒")
    @pytest.mark.sanity
    def test_caseid_1987252(self):  
        value1 = [1,1,0,0,0,255,0,0,0,0]
        value2 = [0,1,1,0,1,255,0,0,0,0]
        value3 = [0,1,1,0,0,255,1,255,0,255,0]
        value4 = [0,1,1,0,0,255,0,0,1,255]
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"frontAVMCamera": {"cameraTemperatureReminder": 0},
                                "rearAVMCamera": {"cameraTemperatureReminder": 0},
                                "leftAVMCamera": {"cameraTemperatureReminder": 0},
                                "rightAVMCamera": {"cameraTemperatureReminder": 0},
                                }})
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"frontAVMCamera": {"cameraTemperatureReminder": 0},
                                "rearAVMCamera": {"cameraTemperatureReminder": 0},
                                "leftAVMCamera": {"cameraTemperatureReminder": 0},
                                "rightAVMCamera": {"cameraTemperatureReminder": 0},
                                }})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'AVM Camera Over Temperature Reminder')
        for i in range(10):
            self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"frontAVMCamera": {"cameraTemperatureReminder": value1[i]},
                                "rearAVMCamera": {"cameraTemperatureReminder": value2[i]},
                                "leftAVMCamera": {"cameraTemperatureReminder": value3[i]},
                                "rightAVMCamera": {"cameraTemperatureReminder": value4[i]},
                                }})
            if i == 0 or i == 4 or i == 6 or i == 8 :
                self.partner.ck_wti_warning_and_resp('AVM Camera Over Temperature Reminder', 1, wti_auto=True)
            elif i == 1 or i == 2:
                self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'AVM Camera Over Temperature Reminder')
            else:
                self.partner.ck_wti_warning_and_resp('AVM Camera Over Temperature Reminder', 0, wti_auto=True)  
                
    @allure.title("摄像头过温提示信息_参数不满足无过温通知")
    @pytest.mark.sanity
    def test_caseid_1987672(self):  
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"frontCamera": {"cameraTemperatureReminder": 0},
                                }})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'AVM Camera Over Temperature Reminder')
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front View Camera Over Temperature Reminder')
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Side and Rear View Camera Over Temperature Reminder')
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"frontCamera": {"cameraTemperatureReminder": 1},
                                }})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'AVM Camera Over Temperature Reminder')
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front View Camera Over Temperature Reminder')
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Side and Rear View Camera Over Temperature Reminder')   
    
    #2.1需求变化BSD_LCA Failed Warning无法触发
    @allure.title("依赖LCAService多个报警同时触发")
    @pytest.mark.full
    def test_caseid_1987878(self): 
        warnlist = ["LCA Left Warning", "LCA Right Warning", "BSD_LCA Failed Warning"]
        
        self.partner.send_event_notify(LCA_SERVICE_SERVER, "NotifyLCAStatus", 
                        {"lcaStatus": {"leftWarning": 0,"rightWarning": 0,"faultSts": 0}})
        sleep(2)
        self.partner.send_event_notify(LCA_SERVICE_SERVER, "NotifyLCAStatus", 
                        {"lcaStatus": {"leftWarning": 3,"rightWarning": 3,"faultSts": 2}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "LCA Left Warning", "info": str(1)},
                                            {"name": "LCA Right Warning", "info": str(1)},
                                           ]})
        self.get_multiplewarningmsglist(warnlist,["1","1","0"])
        
        self.partner.send_event_notify(LCA_SERVICE_SERVER, "NotifyLCAStatus", 
                        {"lcaStatus": {"leftWarning": 0,"rightWarning": 3,"faultSts": 2}})
        self.get_multiplewarningmsglist(warnlist,["0","1","0"])
    
        self.partner.send_event_notify(LCA_SERVICE_SERVER, "NotifyLCAStatus", 
                        {"lcaStatus": {"leftWarning": 0,"rightWarning": 0,"faultSts": 2}})
        self.get_multiplewarningmsglist(warnlist,["0","0","0"])
        
        self.partner.send_event_notify(LCA_SERVICE_SERVER, "NotifyLCAStatus", 
                        {"lcaStatus": {"leftWarning": 0,"rightWarning": 0,"faultSts": 0}})
        self.get_multiplewarningmsglist(warnlist,["0","0","0"])
    
    #2.1需求变化AEB_R Failed Warning、AEB_R Restricted Failed Warning无法触发  
    @allure.title("依赖AEBRService多个报警同时触发")
    @pytest.mark.full
    def test_caseid_1987883	(self): 
        warnlist = ["AEBR Warning", "AEB_R Failed Warning", "AEB_R Restricted Failed Warning"]
        
        self.partner.send_event_notify(AEBR_SERVICE_SERVER, "NotifyAEBRStatus", 
                        {"aebRStatus": {"activeSts": 0,"faultSts": 0}})
        sleep(2)
        self.partner.send_event_notify(AEBR_SERVICE_SERVER, "NotifyAEBRStatus", 
                        {"aebRStatus": {"activeSts": 3,"faultSts": 2}})
        self.partner.ck_s2s_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList",
                                  {"list": [{"name": "AEBR Warning", "info": str(3)},
                                            ]})
        self.get_multiplewarningmsglist(warnlist,["3","0","0"])
        
        self.partner.send_event_notify(AEBR_SERVICE_SERVER, "NotifyAEBRStatus", 
                        {"aebRStatus": {"activeSts": 0,"faultSts": 2}})
        self.get_multiplewarningmsglist(warnlist,["0","0","0"])
        
        self.partner.send_event_notify(AEBR_SERVICE_SERVER, "NotifyAEBRStatus", 
                        {"aebRStatus": {"activeSts": 0,"faultSts": 1}})
        self.get_multiplewarningmsglist(warnlist,["0","0","0"])
        
        self.partner.send_event_notify(AEBR_SERVICE_SERVER, "NotifyAEBRStatus", 
                        {"aebRStatus": {"activeSts": 0,"faultSts": 0}})
        self.get_multiplewarningmsglist(warnlist,["0","0","0"])
        
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件ag")
    @pytest.mark.sanity
    def test_caseid_1987776	(self): 
        def return_struct(value1, value2):
            return {"rcwStatus": {"functionStatus":value1,"faultSts": value2}}
        #当第一个条件满足时
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
         #当第一个条件满足时
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": sts,"faultSts": fsts}})
                if sts == 1 and fsts in [1,2]:
                    #[1,0], [1, 0, 2] 保证info变化上报
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件ah")
    @pytest.mark.full
    def test_caseid_1987777	(self): 
        def return_struct(value1, value2):
           return {"cmsfStatus": {"switchSts": value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 3
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 2
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                     {"rctaFunctionStatus": {"functionStatus":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", CMSF_SERVICE_SERVER,
                                    "NotifyCMSFStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", CMSF_SERVICE_SERVER,
                                    "NotifyCMSFStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件ai")
    @pytest.mark.full
    def test_caseid_1987778	(self): 
        def return_struct(value1, value2):
            return {"lcaStatus": {"switchSts":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
      
        self.setNoWTI_2354()    
        for sts in [0,1]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": sts,"faultSts": fsts}})
                if sts == 1 and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件aj")
    @pytest.mark.full
    def test_caseid_1987788	(self): 
        def return_struct(value1, value2):
            return {"dowStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0

        self.setNoWTI_2354()    
        for sts in [0,1]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": sts,"faultSts": fsts}})
                if sts == 1 and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    #回退                
    # @allure.title("前向和侧后向辅助安全功能受限提醒_条件bg")
    # @pytest.mark.full
    # def test_caseid_1987789	(self): 
    #     def return_struct(value1, value2):
    #         return {"rcwStatus": {"functionStatus":value1,"faultSts": value2}}
    #     def return_info1(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 1
    #         else:return 2
    #     def return_info2(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 3
    #         else:return 0
       
    #     self.setNoWTI_2354()    
    #     for sts in [0,1,2]:
    #         for fsts in [0,1,2]:
    #             logger.info(f"sts:{sts}, fsts:{fsts}")
    #             self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":sts,"faultSts": fsts}})
    #             #SOA-28941需求变更
    #             # if sts == 1 and fsts in [1,2]:
    #             if sts in [1,2] and fsts in [1,2]:
    #                 self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
    #                                 "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
    #                                 jump_trigger=True) 
    #             else:
    #                 self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
    #                                 "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
    #                                 jump_trigger=True)
                    
    # @allure.title("前向和侧后向辅助安全功能受限提醒_条件bh")
    # @pytest.mark.full
    # def test_caseid_1987790	(self): 
    #     def return_struct(value1, value2):
    #        return {"sts":{"switchSts":value1,"faultSts": value2}}
    #     def return_info1(value1, value2):
    #         #SOA-28941需求变更
    #         if value1 in [1,2] and value2 in [1,2]:return 1
    #         else:return 3
    #     def return_info2(value1, value2):
    #         if value1 in [1,2] and value2 in [1,2]:return 2
    #         else:return 0
       
    #     self.setNoWTI_2354()    
    #     for sts in [0,1,2]:
    #         for fsts in [0,1,2]:
    #             logger.info(f"sts:{sts}, fsts:{fsts}")
    #             self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
    #                                  {"rctaFunctionStatus": {"functionStatus":sts,"faultSts": fsts}})
    #             if sts in [1,2] and fsts in [1,2]:
    #                 self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", ELKSERVICE_SERVER,
    #                                 "ELKSts", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
    #                                 jump_trigger=True) 
    #             else:
    #                 self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", ELKSERVICE_SERVER,
    #                                 "ELKSts", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
    #                                 jump_trigger=True)
    
    # @allure.title("前向和侧后向辅助安全功能受限提醒_条件bi")
    # @pytest.mark.full
    # def test_caseid_1987791	(self): 
    #     def return_struct(value1, value2):
    #         return {"lcaStatus": {"switchSts":value1,"faultSts": value2}}
    #     def return_info1(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 1
    #         else:return 2
    #     def return_info2(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 3
    #         else:return 0
      
    #     self.setNoWTI_2354()    
    #     for sts in [0,1,2]:
    #         for fsts in [0,1,2]:
    #             logger.info(f"sts:{sts}, fsts:{fsts}")
    #             self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":sts,"faultSts": fsts}})
    #             if sts in [1,2] and fsts in [1,2]:
    #                 self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
    #                                 "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
    #                                 jump_trigger=True) 
    #             else:
    #                 self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
    #                                 "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
    #                                 jump_trigger=True)
                    
    # @allure.title("前向和侧后向辅助安全功能受限提醒_条件bj")
    # @pytest.mark.full
    # def test_caseid_1987792	(self): 
    #     def return_struct(value1, value2):
    #         return {"dowStatus": {"functionStatus":value1,"faultSts": value2}}
    #     def return_info1(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 1
    #         else:return 2
    #     def return_info2(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 3
    #         else:return 0

    #     self.setNoWTI_2354()    
    #     for sts in [0,1,2]:
    #         for fsts in [0,1,2]:
    #             logger.info(f"sts:{sts}, fsts:{fsts}")
    #             self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":sts,"faultSts": fsts}})
    #             if sts in [1,2] and fsts in [1,2]:
    #                 self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
    #                                 "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
    #                                 jump_trigger=True) 
    #             else:
    #                 self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
    #                                 "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
    #                                 jump_trigger=True)
    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件bg")
    @pytest.mark.full
    def test_caseid_1987789	(self): 
        def return_struct(value1, value2):
            return {"rcwStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":sts,"faultSts": fsts}})
                if sts == 1 and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件bh")
    @pytest.mark.full
    def test_caseid_1987790	(self): 
        def return_struct(value1, value2):
           return {"sts":{"switchSts":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 3
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 2
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                     {"rctaFunctionStatus": {"functionStatus":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", ELKSERVICE_SERVER,
                                    "ELKSts", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", ELKSERVICE_SERVER,
                                    "ELKSts", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件bi")
    @pytest.mark.full
    def test_caseid_1987791	(self): 
        def return_struct(value1, value2):
            return {"lcaStatus": {"switchSts":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
      
        self.setNoWTI_2354()    
        for sts in [0,1]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":sts,"faultSts": fsts}})
                if sts == 1 and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件bj")
    @pytest.mark.full
    def test_caseid_1987792	(self): 
        def return_struct(value1, value2):
            return {"dowStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0

        self.setNoWTI_2354()    
        for sts in [0,1]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":sts,"faultSts": fsts}})
                if sts == 1 and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件cg")
    @pytest.mark.full
    def test_caseid_1987793	(self): 
        def return_struct(value1, value2):
            return {"rcwStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(SAS_SERVICE_SERVER, "NotifyTrafficSignStatus",
                                      {"trafficSignStatus": {"functionSts":sts,"faultSts": fsts}})
                if sts == 1 and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件ch")
    @pytest.mark.full
    def test_caseid_1987794	(self): 
        def return_struct(value1, value2):
           return {"trafficSignStatus": {"functionSts":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 3
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 2
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                     {"rctaFunctionStatus": {"functionStatus":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", SAS_SERVICE_SERVER,
                                    "NotifyTrafficSignStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", SAS_SERVICE_SERVER,
                                    "NotifyTrafficSignStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件ci")
    @pytest.mark.full
    def test_caseid_1987795	(self): 
        def return_struct(value1, value2):
            return {"lcaStatus": {"switchSts":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
      
        self.setNoWTI_2354()    
        for sts in [0,1]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(SAS_SERVICE_SERVER, "NotifyTrafficSignStatus",
                                      {"trafficSignStatus": {"functionSts":sts,"faultSts": fsts}})
                if sts == 1 and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件cj")
    @pytest.mark.full
    def test_caseid_1987796	(self): 
        def return_struct(value1, value2):
            return {"dowStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0

        self.setNoWTI_2354()    
        for sts in [0,1]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(SAS_SERVICE_SERVER, "NotifyTrafficSignStatus",
                                      {"trafficSignStatus": {"functionSts":sts,"faultSts": fsts}})
                if sts == 1 and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    
    #回退               
    # @allure.title("前向和侧后向辅助安全功能受限提醒_条件dg")
    # @pytest.mark.full
    # def test_caseid_1987797	(self): 
    #     def return_struct(value1, value2):
    #         return {"rcwStatus": {"functionStatus":value1,"faultSts": value2}}
    #     def return_info1(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 1
    #         else:return 2
    #     def return_info2(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 3
    #         else:return 0
       
    #     self.setNoWTI_2354()    
    #     for sts in [0,6]:
    #         for redSts in [0,1]:
    #             for fsts in [0,1,2]:
    #                 logger.info(f"sts:{sts}, fsts:{fsts}")
    #                 self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
    #                                     {"tlaFunctionStatus": {"switchSts": sts,"faultSts": fsts, "redLightSwitchSts":redSts}})
    #                 if (sts == 6 and fsts in [1,2]) or (redSts == 1 and fsts in [1,2]):
    #                     self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
    #                                     "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
    #                                     jump_trigger=True) 
    #                 else:
    #                     self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
    #                                     "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
    #                                     jump_trigger=True)
                    
    # @allure.title("前向和侧后向辅助安全功能受限提醒_条件dh")
    # @pytest.mark.full
    # def test_caseid_1987799	(self): 
    #     def return_struct(value1, value2):
    #        return {"rctaFunctionStatus": {"functionStatus":value1,"faultSts": value2}}
    #     def return_info1(value1, value2):
    #         if value1 in [1,2] and value2 in [1,2]:return 1
    #         else:return 2
    #     def return_info2(value1, value2):
    #         if value1 in [1,2] and value2 in [1,2]:return 3
    #         else:return 0
       
    #     self.setNoWTI_2354()    
    #     for sts in [0,6]:
    #         for redSts in [0,1]:
    #             for fsts in [0,1,2]:
    #                 logger.info(f"sts:{sts}, fsts:{fsts}")
    #                 self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
    #                                     {"tlaFunctionStatus": {"switchSts": sts,"faultSts": fsts, "redLightSwitchSts":redSts}})
    #                 if (sts == 6 and fsts in [1,2]) or (redSts == 1 and fsts in [1,2]):
    #                     self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCTA_SERVICE_SERVER,
    #                                     "NotifyRCTAFunctionStatus", (0, 0),  [1,0,2], [1,0, 2], return_struct, return_info1,
    #                                     jump_trigger=True) 
    #                 else:
    #                     self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCTA_SERVICE_SERVER,
    #                                     "NotifyRCTAFunctionStatus", (0, 0),  [1,0,2], [1,0,2], return_struct, return_info2,
    #                                     jump_trigger=True) 
    
    # @allure.title("前向和侧后向辅助安全功能受限提醒_条件di")
    # @pytest.mark.full
    # def test_caseid_1987800	(self): 
    #     def return_struct(value1, value2):
    #         return {"lcaStatus": {"switchSts":value1,"faultSts": value2}}
    #     def return_info1(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 1
    #         else:return 2
    #     def return_info2(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 3
    #         else:return 0
      
    #     self.setNoWTI_2354()    
    #     for sts in [0,6]:
    #         for redSts in [0,1]:
    #             for fsts in [0,1,2]:
    #                 logger.info(f"sts:{sts}, fsts:{fsts}")
    #                 self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
    #                                     {"tlaFunctionStatus": {"switchSts": sts,"faultSts": fsts, "redLightSwitchSts":redSts}})
    #                 if (sts == 6 and fsts in [1,2]) or (redSts == 1 and fsts in [1,2]):
    #                     self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
    #                                     "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
    #                                     jump_trigger=True) 
    #                 else:
    #                     self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
    #                                     "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
    #                                     jump_trigger=True)
                    
    # @allure.title("前向和侧后向辅助安全功能受限提醒_条件dj")
    # @pytest.mark.full
    # def test_caseid_1987801	(self): 
    #     def return_struct(value1, value2):
    #         return {"dowStatus": {"functionStatus":value1,"faultSts": value2}}
    #     def return_info1(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 1
    #         else:return 2
    #     def return_info2(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 3
    #         else:return 0

    #     self.setNoWTI_2354()    
    #     for sts in [0,6]:
    #         for redSts in [0,1]:
    #             for fsts in [0,1,2]:
    #                 logger.info(f"sts:{sts}, fsts:{fsts}")
    #                 self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
    #                                     {"tlaFunctionStatus": {"switchSts": sts,"faultSts": fsts, "redLightSwitchSts":redSts}})
    #                 if (sts == 6 and fsts in [1,2]) or (redSts == 1 and fsts in [1,2]):
    #                     self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
    #                                     "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
    #                                     jump_trigger=True) 
    #                 else:
    #                     self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
    #                                     "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
    #                                     jump_trigger=True)
    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件dg")
    @pytest.mark.full
    def test_caseid_1987797	(self): 
        def return_struct(value1, value2):
            return {"rcwStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,6]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
                                      {"tlaFunctionStatus": {"switchSts": sts,"faultSts": fsts}})
                if sts == 6 and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件dh")
    @pytest.mark.full
    def test_caseid_1987799	(self): 
        def return_struct(value1, value2):
           return {"tlaFunctionStatus": {"switchSts": value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 6 and value2 in [1,2]:return 1
            else:return 3
        def return_info2(value1, value2):
            if value1 == 6 and value2 in [1,2]:return 2
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                     {"rctaFunctionStatus": {"functionStatus":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", TLA_SERVICE_SERVER,
                                    "NotifyTLAFunctionStatus", (0, 0),  [6,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", TLA_SERVICE_SERVER,
                                    "NotifyTLAFunctionStatus", (0, 0),  [6,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件di")
    @pytest.mark.full
    def test_caseid_1987800	(self): 
        def return_struct(value1, value2):
            return {"lcaStatus": {"switchSts":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
      
        self.setNoWTI_2354()    
        for sts in [0,6]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
                                      {"tlaFunctionStatus": {"switchSts": sts,"faultSts": fsts}})
                if sts == 6 and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件dj")
    @pytest.mark.full
    def test_caseid_1987801	(self): 
        def return_struct(value1, value2):
            return {"dowStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0

        self.setNoWTI_2354()    
        for sts in [0,6]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
                                      {"tlaFunctionStatus": {"switchSts": sts,"faultSts": fsts}})
                if sts == 6 and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
            
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件eg")
    @pytest.mark.full
    def test_caseid_1987802	(self): 
        def return_struct(value1, value2):
            return {"rcwStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1,2,3]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                      {"allAHBCFunctionSts": {"switchSts": sts,"faultSts": fsts}})
                if sts in [1,2,3] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件eh")
    @pytest.mark.full
    def test_caseid_1987803	(self): 
        def return_struct(value1, value2):
           return {"allAHBCFunctionSts": {"switchSts": value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 in [1,2,3] and value2 in [1,2]:return 1
            else:return 3
        def return_info2(value1, value2):
            if value1 in [1,2,3] and value2 in [1,2]:return 2
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                     {"rctaFunctionStatus": {"functionStatus":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", AUTOHIGHBEAMCONTROL_SERVICE_SERVER,
                                    "NotifyAHBCFunctionSts", (0, 0),  [1,0,2,3], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", AUTOHIGHBEAMCONTROL_SERVICE_SERVER,
                                    "NotifyAHBCFunctionSts", (0, 0),  [1,0,2,3], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件ei")
    @pytest.mark.full
    def test_caseid_1987804	(self): 
        def return_struct(value1, value2):
            return {"lcaStatus": {"switchSts":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
      
        self.setNoWTI_2354()    
        for sts in [0,1,2,3]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                      {"allAHBCFunctionSts": {"switchSts": sts,"faultSts": fsts}})
                if sts in [1,2,3] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件ej")
    @pytest.mark.full
    def test_caseid_1987805	(self): 
        def return_struct(value1, value2):
            return {"dowStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0

        self.setNoWTI_2354()    
        for sts in [0,1,2,3]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(AUTOHIGHBEAMCONTROL_SERVICE_SERVER, "NotifyAHBCFunctionSts",
                                      {"allAHBCFunctionSts": {"switchSts": sts,"faultSts": fsts}})
                if sts in [1,2,3] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件fg")
    @pytest.mark.full
    def test_caseid_1987807	(self): 
        def return_struct(value1, value2):
            return {"rcwStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(AUTOTURNLAMPCTRL_SERVICE_SERVER, "AutoCtrlTurnLampSts",
                                     {"sts": {"switchSts":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件fh")
    @pytest.mark.full
    def test_caseid_1987808	(self): 
        def return_struct(value1, value2):
           return  {"sts": {"switchSts":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 in [1,2] and value2 in [1,2]:return 1
            else:return 3
        def return_info2(value1, value2):
            if value1 in [1,2] and value2 in [1,2]:return 2
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                     {"rctaFunctionStatus": {"functionStatus":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", AUTOTURNLAMPCTRL_SERVICE_SERVER,
                                    "AutoCtrlTurnLampSts", (0, 0),  [1,0,2], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", AUTOTURNLAMPCTRL_SERVICE_SERVER,
                                    "AutoCtrlTurnLampSts", (0, 0),  [1,0,2], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件fi")
    @pytest.mark.full
    def test_caseid_1987809	(self): 
        def return_struct(value1, value2):
            return {"lcaStatus": {"switchSts":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
      
        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(AUTOTURNLAMPCTRL_SERVICE_SERVER, "AutoCtrlTurnLampSts",
                                     {"sts": {"switchSts":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件fj")
    @pytest.mark.full
    def test_caseid_1987810	(self): 
        def return_struct(value1, value2):
            return {"dowStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0

        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(AUTOTURNLAMPCTRL_SERVICE_SERVER, "AutoCtrlTurnLampSts",
                                     {"sts": {"switchSts":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件kg")
    @pytest.mark.full
    def test_caseid_1987968	(self): 
        def return_struct(value1, value2):
            return {"rcwStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(LKA_SERVICE_SERVER, "NotifyLKAFunctionStatus",
                                     {"lasFunctionStatus": {"switchSts":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", RCW_SERVICE_SERVER,
                                    "NotifyRCWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件kh")
    @pytest.mark.full
    def test_caseid_1987969	(self): 
        def return_struct(value1, value2):
           return  {"lasFunctionStatus": {"switchSts":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 in [1,2] and value2 in [1,2]:return 1
            else:return 3
        def return_info2(value1, value2):
            if value1 in [1,2] and value2 in [1,2]:return 2
            else:return 0
       
        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(RCTA_SERVICE_SERVER, "NotifyRCTAFunctionStatus",
                                     {"rctaFunctionStatus": {"functionStatus":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LKA_SERVICE_SERVER,
                                    "NotifyLKAFunctionStatus", (0, 0),  [1,0,2], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LKA_SERVICE_SERVER,
                                    "NotifyLKAFunctionStatus", (0, 0),  [1,0,2], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件ki")
    @pytest.mark.full
    def test_caseid_1987970	(self): 
        def return_struct(value1, value2):
            return {"lcaStatus": {"switchSts":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0
      
        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(LKA_SERVICE_SERVER, "NotifyLKAFunctionStatus",
                                     {"lasFunctionStatus": {"switchSts":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", LCA_SERVICE_SERVER,
                                    "NotifyLCAStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
                    
    @allure.title("前向和侧后向辅助安全功能受限提醒_条件kj")
    @pytest.mark.full
    def test_caseid_1987971	(self): 
        def return_struct(value1, value2):
            return {"dowStatus": {"functionStatus":value1,"faultSts": value2}}
        def return_info1(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 1
            else:return 2
        def return_info2(value1, value2):
            if value1 == 1 and value2 in [1,2]:return 3
            else:return 0

        self.setNoWTI_2354()    
        for sts in [0,1,2]:
            for fsts in [0,1,2]:
                logger.info(f"sts:{sts}, fsts:{fsts}")
                self.partner.send_event_notify(LKA_SERVICE_SERVER, "NotifyLKAFunctionStatus",
                                     {"lasFunctionStatus": {"switchSts":sts,"faultSts": fsts}})
                if sts in [1,2] and fsts in [1,2]:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info1,
                                    jump_trigger=True) 
                else:
                    self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", DOW_SERVICE_SERVER,
                                    "NotifyDOWStatus", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info2,
                                    jump_trigger=True)
    #回退                
    # @allure.title("前向和侧后向辅助安全功能受限提醒_条件l")
    # @pytest.mark.sanity
    # def test_caseid_1989225(self): 
    #     def return_struct(value1, value2):
    #         return {"ESSInfo": {"SwithSt":value1,"faultSts": value2}}
    #     def return_info(value1, value2):
    #         if value1 == 1 and value2 in [1,2]:return 1
    #         else:return 0

    #     self.setNoWTI_2354()    
      
    #     self.ck_change_for_two_loop("Front And Side Back ADAS Limit Reminder", ESS_SERVICE_SERVER,
    #                                 "ESSInfo", (0, 0),  [1,0], [1, 0, 2], return_struct, return_info,
    #                                 jump_trigger=True) 
                    
    @allure.title("前向辅助安全功能受限提醒")
    @pytest.mark.sanity
    def test_caseid_1987813	(self):
        self.setNoWTI_2354() 
        self.partner.empty_all(0.5)    
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 1}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 2, wti_auto=True)
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 2}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front And Side Back ADAS Limit Reminder')
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 0}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 0, wti_auto=True)
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 0,"faultSts": 2}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front And Side Back ADAS Limit Reminder')
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 2}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 2, wti_auto=True)
        
    @allure.title("侧后向辅助安全功能受限提醒")	
    @pytest.mark.sanity
    def test_caseid_1987815	(self):
        self.setNoWTI_2354()  
        self.partner.empty_all(0.5)       
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 1}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 3, wti_auto=True)
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 2}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front And Side Back ADAS Limit Reminder')
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 0}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 0, wti_auto=True)
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":0,"faultSts": 2}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front And Side Back ADAS Limit Reminder')
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 2}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 3, wti_auto=True)
        
    @allure.title("前向和侧后向辅助安全功能受限提醒_优先级与变化上报")
    @pytest.mark.sanity
    def test_caseid_1987816	(self):
        self.setNoWTI_2354()    
        self.partner.empty_all(0.5)     
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 1}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 2, wti_auto=True)
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 1}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 1, wti_auto=True)
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 0}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 2, wti_auto=True)
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 2}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 1, wti_auto=True)
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 0}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 3, wti_auto=True)
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 2}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 1, wti_auto=True)
        
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":1,"faultSts": 1}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front And Side Back ADAS Limit Reminder')
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 0}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front And Side Back ADAS Limit Reminder')
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":1,"faultSts": 0}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 3, wti_auto=True)
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 0}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 0, wti_auto=True)
        
    @allure.title("前向和侧后向辅助安全功能受限提醒_时效性测试")
    @pytest.mark.sanity
    def test_caseid_1987871	(self):
        self.setNoWTI_2354()    
        logger.info(f"断开服务端")
        self.partner.stop_single_partner(CMSF_SERVICE_SERVER)
        self.partner.stop_single_partner(RCW_SERVICE_SERVER)
        self.partner.empty_all(5)
        logger.info(f"连接服务端1")
        self.partner.start_single_partner("CMSFService", "server")
        sleep(0.3)
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 1}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front And Side Back ADAS Limit Reminder',timeout = 0.5)
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 2, wti_auto=True) 
        #启动其他服务的时候 不会再起timer
        self.partner.start_single_partner("RCWService", "server")
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 1}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 1, wti_auto=True, timeout = 0.5)
        
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 0}}) 
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 0}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 0, wti_auto=True, timeout = 0.5)
        
        self.partner.stop_single_partner(RCW_SERVICE_SERVER)
        self.partner.empty_all(5)
        self.partner.start_single_partner("RCWService", "server")
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", 
                            {"rcwStatus": {"functionStatus":1,"faultSts": 1}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front And Side Back ADAS Limit Reminder',timeout = 0.5)
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 3, wti_auto=True)
        
    @allure.title("前向和侧后向辅助安全功能受限提醒_时效性测试_ACU断连不影响故障")
    @pytest.mark.full
    def test_caseid_1987872	(self):
        self.partner.start_single_partner("CMSFService", "server")
        sleep(2)
        self.setNoWTI_2354()    
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 1}})
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 2, wti_auto=True) 
        self.partner.stop_single_partner(CMSF_SERVICE_SERVER)
        self.partner.empty_all(5)
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front And Side Back ADAS Limit Reminder')
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front And Side Back ADAS Limit Reminder", "info": "2"}]})
        self.partner.start_single_partner("CMSFService", "server")
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT,"WarningMsgList", 'Front And Side Back ADAS Limit Reminder')
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "Front And Side Back ADAS Limit Reminder", "info": "2"}]})
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                            {"cmsfStatus": {"switchSts": 1,"faultSts": 0}})    
        self.partner.ck_wti_warning_and_resp("Front And Side Back ADAS Limit Reminder", 0, wti_auto=True) 
        
    @allure.title("定位丢失提醒")
    @pytest.mark.sanity
    def test_caseid_1988405(self): 
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "LostLocationReminderInfo", {"reminderInfo":{"sdReminder" :0}})
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                                {"out": [{'name': 'Lost Location Reminder', 'info': '0'}]})
        
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "LostLocationReminderInfo", {"reminderInfo":{"sdReminder" :1}})
        self.partner.ck_wti_warning_and_resp('Lost Location Reminder', 1,wti_auto=True)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "LostLocationReminderInfo", {"reminderInfo":{"sdReminder" :1}})
        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'Lost Location Reminder')
        
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "LostLocationReminderInfo", {"reminderInfo":{"sdReminder" :0}})
        self.partner.ck_wti_warning_and_resp('Lost Location Reminder', 0,wti_auto=True)
        
    @allure.title("摄像头提醒")
    @pytest.mark.smoke
    def test_caseid_1988953(self):  
        for type in [41,42]:
            for lastHandleType in [0,1,2,3,4]:
                for sensorSts in [0,1,2,3,4,5,5,6]:
                    logger.info(f"type:{type}, lastHandleType:{lastHandleType}, sensorSts:{sensorSts}")
                    self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent", {
                        "reminder":{"type":type,"lastHandleType":lastHandleType,"sensorSts":sensorSts
                        }
                    })
                    if type == 41 and lastHandleType in [0,1,4] and sensorSts in [1,2,3,4,5]:
                        self.partner.ck_wti_warning_and_resp('CameraDirtyReminder', sensorSts, wti_auto=True)
                    elif type == 41 and lastHandleType in [0,1,4] and sensorSts == 6:
                        self.partner.ck_wti_warning_and_resp('CameraDirtyReminder', 0, wti_auto=True)
                    else:
                        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'CameraDirtyReminder')
                
    @allure.title("摄像头提醒TTS")
    @pytest.mark.sanity
    def test_caseid_1988954(self):  
        for type in [41,72,73,74,75,76,77,78,79,80]:
            for lastHandleType in [0,1,2,3,4]:
                for sensorSts in [0,1,2,3,4,5,5,6]:
                    logger.info(f"type:{type}, lastHandleType:{lastHandleType}, sensorSts:{sensorSts}")
                    self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder", {
                        "reminder":{"type":type,"lastHandleType":lastHandleType,"sensorSts":sensorSts
                        }
                    })
                    if type in [41,72,73,74,75,76,77,78,79] and lastHandleType in [0,1,4] and sensorSts in [1,2,3,4,5]:
                        self.partner.ck_wti_warning_and_resp('CameraDirtyTts', sensorSts, wti_auto=True)
                    elif type in [41,72,73,74,75,76,77,78,79] and lastHandleType in [0,1,4] and sensorSts == 6:
                        self.partner.ck_wti_warning_and_resp('CameraDirtyTts', 0, wti_auto=True)
                    else:
                        self.partner.ck_no_specific_event(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", 'CameraDirtyTts')              
        
               
@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIAutoDriveService")
@pytest.mark.zjb11
class TestWTIAutoDriveServiceSafety(TestBase):

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        super().after_class(self, ecu)

    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        sleep(1)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        super().before_each_func(ecu, start=False)
        self.partner = ANPMRCService_Server([("MarsPilotMarsDriverService", "server"),
                                            ("ANPMRCService", "server"),
                                            ("WTIAutoDriveService", "client")
                                            ])
        # 默认以0发送NotifyAutoDriverStatus。默认响应GetMRCSts和GetANPDegraedFault
        self.partner.empty_all()

    def after_each_func(self, ecu):
        self.partner.running = False
        self.partner.stop_operators()
        super().after_each_func(ecu, start=False)

    @allure.title("功能安全故障提示_服务连接30s内不检测ANPMRC功能安全故障")
    @pytest.mark.smoke
    def test_caseid_1983887(self):
        self.partner.ack_GetANPDegraedFault = False
        self.partner.ack_GetMRCSts = False
        self.partner.anpStatus = 8
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        sleep(10)
        self.partner.notify_flg = False
        self.partner.ck_wti_no_warning_and_ck_resp("FuncSafety Failure Remind", 0, wti_auto=True)
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "FuncSafety Failure Remind", "info": "0"}]})
        
    @allure.title("功能安全故障提示_服务连接30s内不检测MarsPilotMarsDriverService功能安全故障")
    @pytest.mark.smoke
    def test_caseid_1983889(self):
        self.partner.notify_flg = False
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        sleep(10)
        self.partner.ck_wti_no_warning_and_ck_resp("FuncSafety Failure Remind", 0, wti_auto=True)
    
    @allure.title("功能安全故障提示_BGM启动后3min后连上MarsPilotMarsDriverService_期间ANPMRC正常响应")
    @pytest.mark.smoke
    def test_caseid_1983890(self):
        self.partner.stop_single_partner(MARSPILOTMARSDRIVER_SERVICE_SERVER)
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        sleep(185)
        self.partner.ck_wti_no_warning_and_ck_resp("FuncSafety Failure Remind", 0, wti_auto=True)
        self.partner.start_single_partner("MarsPilotMarsDriverService", "server")
        self.partner.anpStatus = 8
        sleep(35)
        self.partner.notify_flg = False
        self.partner.ck_wti_no_warning_and_ck_resp("FuncSafety Failure Remind", 0, timeout=4, wti_auto=True)
        self.partner.ack_GetMRCSts = False
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 1, timeout=4, wti_auto=True)
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 0, timeout=5, wti_auto=True)
    
    @allure.title("功能安全故障提示_BGM启动后3min连不上ANPMRCService_MarsPilotMarsDriverService正常发送")
    @pytest.mark.smoke
    def test_caseid_1983895(self):  # Pass
        self.partner.stop_single_partner(ANPMRC_SERVICE_SERVER)
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        sleep(185)
        self.partner.ck_wti_no_warning_and_ck_resp("FuncSafety Failure Remind", 0, wti_auto=True)
        self.partner.anpStatus = 8
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 1, timeout=2, wti_auto=True)
        self.partner.ck_wti_no_warning_and_ck_resp("FuncSafety Failure Remind", 1, timeout=5, wti_auto=True)

        self.partner.anpStatus = 1
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 0, timeout=2, wti_auto=True)
    
    @allure.title("功能安全故障提示_BGM启动后3min连不上ANPMRCService和MarsPilotMarsDriverService")
    @pytest.mark.full
    def test_caseid_1983896(self):
        self.partner.stop_single_partner(ANPMRC_SERVICE_SERVER)
        self.partner.stop_single_partner(MARSPILOTMARSDRIVER_SERVICE_SERVER)
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        sleep(185)
        self.partner.ck_wti_no_warning_and_ck_resp("FuncSafety Failure Remind", 0, wti_auto=True)
        self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "FuncSafety Failure Remind", "info": "0"}]})
        
    @allure.title("功能安全故障提示_NotifyAutoDriverStatus无功能安全故障(ANPSts=8)_GetMRCSts堵塞_4s后恢复")  # N-Y-Y
    @pytest.mark.full
    def test_caseid_1983897(self):
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        self.partner.anpStatus = 8
        sleep(35)
        self.partner.ack_GetMRCSts = False
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 1, timeout=4, wti_auto=True)
        self.partner.ck_wti_no_warning_and_ck_resp("FuncSafety Failure Remind", 1, timeout=5, wti_auto=True)
        self.partner.ack_GetMRCSts = True
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 0, timeout=2, wti_auto=True)
    
    @allure.title("功能安全故障提示_NotifyAutoDriverStatus无功能安全故障(ANPSts=8)_GetANPDegraedFault堵塞_4s内恢复")  # N-Y-Y
    @pytest.mark.full
    def test_caseid_1983898(self):
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        self.partner.anpStatus = 8
        sleep(35)
        self.partner.ack_GetANPDegraedFault = False
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 1, timeout=4, wti_auto=True)
        self.partner.ack_GetANPDegraedFault = True
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 0, timeout=2, wti_auto=True)
    
    @allure.title("功能安全故障提示_遍历ANPStatus_仅8/9/10/11/15/16报故障")
    @pytest.mark.sanity
    def test_caseid_1983900(self):
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        self.partner.anpStatus = 8
        sleep(35)
        self.partner.ack_GetANPDegraedFault = False
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 1, timeout=4, wti_auto=True)
        for status in range(17):
            self.partner.anpStatus = status
            sleep(2)
            if status in [8, 9, 10, 11, 15, 16]:
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "FuncSafety Failure Remind", "info": "1"}]})
            else:
                self.partner.send_request_and_ck_resp(WTIAUTODRIVE_SERVICE_CLIENT, "GetWarningMsgList", {},
                                        {"out": [{"name": "FuncSafety Failure Remind", "info": "0"}]})
    
    @allure.title("功能安全故障提示_NotifyAutoDriverStatus有功能安全故障(ANPSts=8)_GetMRCSts堵塞_4s内恢复")  # N-Y-Y
    @pytest.mark.sanity
    def test_caseid_1983902(self):
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        self.partner.anpStatus = 8
        sleep(30)
        self.partner.notify_flg = False
        sleep(5)
        self.partner.ack_GetMRCSts = False
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 1, timeout=4, wti_auto=True)
        self.partner.ack_GetMRCSts = True#只是控制回不回
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 0, timeout=2, wti_auto=True)
    
    @allure.title("功能安全故障提示_NotifyAutoDriverStatus有功能安全故障(ANPSts=8)_GetANPDegraedFault堵塞_4s后恢复")  # N-Y-Y
    @pytest.mark.sanity
    def test_caseid_1983903(self):
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        self.partner.anpStatus = 8
        sleep(30)
        self.partner.notify_flg = False
        sleep(5)
        self.partner.ack_GetANPDegraedFault = False
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 1, timeout=4, wti_auto=True)
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 0, timeout=5, wti_auto=True)
        self.partner.ack_GetANPDegraedFault = True
        self.partner.ck_wti_no_warning_and_ck_resp("FuncSafety Failure Remind", 0, timeout=2, wti_auto=True)
    
    @allure.title("功能安全故障提示_NotifyAutoDriverStatus无功能安全故障(ANPSts=8)_GetANPDegraedFault和GetMRCSts均堵塞_单个恢复不会恢复")
    @pytest.mark.sanity
    def test_caseid_1983905(self):
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        self.partner.anpStatus = 8
        sleep(30)
        self.partner.ack_GetANPDegraedFault = False
        self.partner.ack_GetMRCSts = False
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 1, timeout=4.5, wti_auto=True)
        self.partner.ack_GetANPDegraedFault = True
        self.partner.ck_wti_no_warning_and_ck_resp("FuncSafety Failure Remind", 1, timeout=5, wti_auto=True)
        self.partner.ack_GetMRCSts = True
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 0, timeout=2, wti_auto=True)

    @allure.title("功能安全故障提示_MRCStatus=3时上报故障")
    @pytest.mark.sanity
    def test_caseid_1983926(self):
        self.restart_bgm_and_connect_service(WTIAUTODRIVE_SERVICE_CLIENT)
        sleep(5)
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyMRCSts", {"sts": 3})  # WTIAutoDrive针对这个看event，block看get
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 1, timeout=4, wti_auto=True)
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyMRCSts", {"sts": 2})
        self.partner.ck_wti_warning_and_resp("FuncSafety Failure Remind", 0, timeout=2, wti_auto=True)

    