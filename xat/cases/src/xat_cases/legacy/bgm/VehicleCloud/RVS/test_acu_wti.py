import os
import sys
import pytest
from time import sleep
import threading
import math


sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))

import allure
import random
from time import sleep
from xat_ecu.legacy.common.data_type_handing import logger
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.driver.ssh_interface import command_send

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.legacy.tsp.rvs_client import RvsClient
from signal_value_mapping import *

ESS_SERVICE_SERVER = "ESSService_server"

@allure.feature("SOA服务接口")
@allure.story("WTI通知/WTIAutoDriveService")
@pytest.mark.zjb
# class TestWTIAutoDriveService(TestBase):
class TestRVS(TestABCBase):
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
                                     ("cdc_wtiservice_crossdomain","server")
                                     ])
        self.partner.method_default_timeout = 0.1
        # self.sd_tester.tester_present()
        # self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        # self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.AutoDriverStatus_response = False
        self.ANP_response = False
        sleep(1)
        self.vid = self.tb_config["vid"]
        self.rvs_client = RvsClient(vid=self.vid)
        logger.info("VID: {0}".format(self.vid))
        sleep(2)

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
        self.sd_tester.stop_tester_present()
        self.partner.stop_operators()
        super().after_class(self, ecu)

    def before_each_func(self, ecu):
        """每个测试用例前置步骤"""
        # super().before_each_func(ecu, start=False)
        self.partner.empty_all()
        logger.info(f"case开始运行***************************************************")

    def after_each_func(self, ecu):
        logger.info(f"case结束运行***************************************************")
        # super().after_each_func(ecu, start=False)

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

    @allure.title("1.7 ACU 小心碰撞  WTI-2383")
    @pytest.mark.sanity
    def test_caseid_1990905(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "CollisionRisk", {"riskInfo":{"decelerationRisk":0}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "CollisionRisk", {"riskInfo":{"decelerationRisk":1}})
        assert self.tsp.log_search_wti(wtiKey="ANP Risk Reminder",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "CollisionRisk", {"riskInfo":{"decelerationRisk":0}})
        assert self.tsp.log_search_wti(wtiKey="ANP Risk Reminder",wtiFlag=0)

    
    
    @allure.title("自动泊车退出，时间超五分钟 WTI-2345")
    @pytest.mark.full 
    def test_caseid_1990882(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type": 69, "lastHandleType": 2}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type": 69, "lastHandleType": 1}})
        assert self.tsp.log_search_wti(wtiKey="APA Working Status",wtiFlag=69)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type": 69, "lastHandleType": 2}})
        assert self.tsp.log_search_wti(wtiKey="APA Working Status",wtiFlag=0)
        
    
    # @allure.title("TTS 播报:我退出自动泊车了，因为暂停的时间超过了五分钟 WTI-2346")
    # def test_caseid_110112(self):
    #     self.sd_tester.change_usage_mode(1)       
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyConnectSts",1)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyPrsntZone",2)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte0",12)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte1",24)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte2",12)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte3",24)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte4",12)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte5",24)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte6",12)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte7",24)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte8",12)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte9",24)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte10",12)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte11",24)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte12",12)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte13",24)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte14",12)
    #     self.ipdu.set(self.ipdu.connectivitycanfd.BncmConnectivityFr18,"DigKeyConnectInfo1KeyIdByte15",24)
    #     self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
    #                                     {"reminder": {"type": 5, "lastHandleType": 2}})
    #     sleep(1)
    #     self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
    #                                     {"reminder": {"type": 5, "lastHandleType": 1}})
    #     # sleep(1)
    #     self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
    #                                     {"reminder": {"type": 5, "lastHandleType": 2}})
        
    
    @allure.title("车辆规划和控制ANP_PNC提醒: 注意通行方向,请手动转向,WTI-2341")
    @pytest.mark.full
    def test_caseid_1990880(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyPNCReminder",
                                       {"pncReminder": 0})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyPNCReminder",
                                       {"pncReminder": 114})
        assert self.tsp.log_search_wti(wtiKey="ANP PNC Remind",wtiFlag=114)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyPNCReminder",
                                       {"pncReminder": 0})
        assert self.tsp.log_search_wti(wtiKey="ANP PNC Remind",wtiFlag=0)

    
    @allure.title("ANP提醒: 车道太窄,无法开启车道保持,WTI-2323")
    @pytest.mark.full
    def test_caseid_1990879(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 148, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=148)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)
        

    
    @allure.title("ANP提醒: 车道太宽，无法开启车道保持,WTI-2324")
    @pytest.mark.full
    def test_caseid_1990877(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 150, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=150)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)
    
    

    @allure.title("跟车目标距离过近,无法开启PPA,WTI-2325")
    @pytest.mark.full
    def test_caseid_1990874(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 153, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=153)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)

    
    @allure.title("跟车目标过近,无法开启车道保持,WTI-2326")
    @pytest.mark.full
    def test_caseid_1990875(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 152, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=152)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)
        

    @allure.title("车道线不满足,无法开启PPA,WTI-2327")
    @pytest.mark.full
    def test_caseid_1990873(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 155, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=155)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)
        

    @allure.title("车道太窄,无法开启PPA,WTI-2328")
    @pytest.mark.full
    def test_caseid_1990878(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 149, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=149)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)
    

    @allure.title("车道太宽,无法开启PPA,WTI-2329")
    @pytest.mark.full
    def test_caseid_1990876(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 151, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=151)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)
        

    
    @allure.title("已切换到车道保持,WTI-2315")
    @pytest.mark.full
    def test_caseid_1990871(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 157, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=157)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)
        

    
    @allure.title("已切换到PPA,WTI-2316")
    @pytest.mark.full
    def test_caseid_1990872(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 156, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=156)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)
        

    
    @allure.title("雨太大,无法开启车道保持,WTI-2317")
    @pytest.mark.full
    def test_caseid_1990870(self):
        self.sd_tester.write_single_ccp(953, 2)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 142, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Remind",wtiFlag=142)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Remind",wtiFlag=0)
        

    
    @allure.title("车道纠偏中,无法开启车道保持,WTI-2320")
    @pytest.mark.full
    def test_caseid_1990869(self):
        self.sd_tester.write_single_ccp(953, 2)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 144, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Remind",wtiFlag=144)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Remind",wtiFlag=0)
        

    @allure.title("自动避险中,无法开启车道保持,WTI-2321")
    @pytest.mark.full
    def test_caseid_1990868(self):
        self.sd_tester.write_single_ccp(953, 2)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 146, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Remind",wtiFlag=146)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Remind",wtiFlag=0)
        

    @allure.title("握住方向盘后踩下刹车，以进入前进挡位,WTI-1474")
    @pytest.mark.full
    def test_caseid_1990867(self):
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":0}})
        sleep(1)
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":1}})
        assert self.tsp.log_search_wti(wtiKey="Auto Gear Remind",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":0}})
        assert self.tsp.log_search_wti(wtiKey="Auto Gear Remind",wtiFlag=0)
    
    
    @allure.title("握住方向盘后踩下刹车，以进入后退挡位,WTI-1475")
    @pytest.mark.full
    def test_caseid_1990866(self):
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":0}})
        sleep(1)
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":2}})
        assert self.tsp.log_search_wti(wtiKey="Auto Gear Remind",wtiFlag=2)
        sleep(1)
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":0}})
        assert self.tsp.log_search_wti(wtiKey="Auto Gear Remind",wtiFlag=0)
        
    
    @allure.title("自动驻车异常，请接管车辆,WTI-2309")
    @pytest.mark.full
    def test_caseid_1994624(self):
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":0}})
        sleep(1)
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":3}})
        assert self.tsp.log_search_wti(wtiKey="Auto Gear Remind",wtiFlag=3)
        sleep(1)
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":0}})
        assert self.tsp.log_search_wti(wtiKey="Auto Gear Remind",wtiFlag=0)
        

    @allure.title("车辆已进入D挡,WTI-2307")
    @pytest.mark.full
    def test_caseid_1994625(self):
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":0}})
        sleep(1)
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":4}})
        assert self.tsp.log_search_wti(wtiKey="Auto Gear Remind",wtiFlag=4)
        sleep(1)
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":0}})
        assert self.tsp.log_search_wti(wtiKey="Auto Gear Remind",wtiFlag=0)
        

    @allure.title("车辆已进入R挡,WTI-2308")
    @pytest.mark.full
    def test_caseid_1994626(self):
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":0}})
        sleep(1)
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":5}})
        assert self.tsp.log_search_wti(wtiKey="Auto Gear Remind",wtiFlag=5)
        sleep(1)
        self.partner.send_event_notify(AutoGearShift_SERVICE_SERVER, "NotifyAutoGearShiftSts",
                                       {"autoGearShiftSts": {"driverReminder":0}})
        assert self.tsp.log_search_wti(wtiKey="Auto Gear Remind",wtiFlag=0)
    
    
        
    @allure.title("左侧紧急车道保持功能激活,WTI-1824")
    @pytest.mark.full
    def test_caseid_1990865(self):
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"activeSts":0,"switchSts": 0}})
        sleep(1)
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"activeSts":1,"switchSts": 1}})
        assert self.tsp.log_search_wti(wtiKey="Emergency Lane Keeping Active Reminder",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"activeSts":0,"switchSts": 0}})
        assert self.tsp.log_search_wti(wtiKey="Emergency Lane Keeping Active Reminder",wtiFlag=0)
        

    @allure.title("右侧紧急车道保持功能激活,WTI-1826")
    @pytest.mark.full
    def test_caseid_1990864(self):
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":0,"switchSts": 0}})
        sleep(1)
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"activeSts":2,"switchSts": 1}})
        assert self.tsp.log_search_wti(wtiKey="Emergency Lane Keeping Active Reminder",wtiFlag=2)
        sleep(1)
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"activeSts":0,"switchSts": 0}})
        assert self.tsp.log_search_wti(wtiKey="Emergency Lane Keeping Active Reminder",wtiFlag=0)
        

    @allure.title("2.0 定位异常, 请注意路况,WTI-2400")
    @pytest.mark.sanity
    def test_caseid_1991834(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "LostLocationReminderInfo",
                                       {"reminderInfo": {"sdReminder": 0}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "LostLocationReminderInfo",
                                       {"reminderInfo": {"sdReminder": 1}})
        assert self.tsp.log_search_wti(wtiKey="Lost Location Reminder",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "LostLocationReminderInfo",
                                       {"reminderInfo": {"sdReminder": 0}})
        assert self.tsp.log_search_wti(wtiKey="Lost Location Reminder",wtiFlag=0)


    @allure.title("环境黑暗,最高限速100km/h, WTI-2194")
    @pytest.mark.full
    def test_caseid_1986495(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder",
                                       {"reminder":0})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder",
                                        {"reminder":1})
        assert self.tsp.log_search_wti(wtiKey="Dark Status Remind",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder",
                                       {"reminder":0})
        assert self.tsp.log_search_wti(wtiKey="Dark Status Remind",wtiFlag=0)
        
    
    
    @allure.title("车外光线环境恢复,限速100km/h已解除, WTI-2192")
    @pytest.mark.full
    def test_caseid_1986494(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder",
                                       {"reminder":0})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder",
                                        {"reminder":2})
        assert self.tsp.log_search_wti(wtiKey="Dark Status Remind",wtiFlag=2)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "DarkStsReminder",
                                       {"reminder":0})
        assert self.tsp.log_search_wti(wtiKey="Dark Status Remind",wtiFlag=0)
        

    
    @allure.title("因环境黑暗,最高限速100km/h, WTI-2193")
    @pytest.mark.full
    def test_caseid_109430(self):
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed",
                                       {"accSpeed": {"enableAdjustSpeedReason": 0}})
        sleep(1)
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed",
                                        {"accSpeed": {"enableAdjustSpeedReason": 6}})
        assert self.tsp.log_search_wti(wtiKey="ACC Speed Remind",wtiFlag=6)
        sleep(1)
        self.partner.send_event_notify(ACC_SERVICE_SERVER, "NotifyACCSpeed",
                                        {"accSpeed": {"enableAdjustSpeedReason": 0}})
        assert self.tsp.log_search_wti(wtiKey="ACC Speed Remind",wtiFlag=0)


    @allure.title("车道保持已启动,暗光下限速100km/h,WTI-2190")
    @pytest.mark.full
    def test_caseid_109433(self):
        self.sd_tester.write_single_ccp(953, 2)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 138, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=138)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)



    @allure.title("PPA已启动,暗光下限速100km/h,WTI-2191")
    @pytest.mark.full
    def test_caseid_1919374(self):
        self.sd_tester.write_single_ccp(953, 2)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 139, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=139)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)
        
    
    
    @allure.title("此车位可能地锁未降下，请注意泊车安全,WTI-2359")
    @pytest.mark.full
    def test_caseid_1994620(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                        {"reminder": {"type": 71, "lastHandleType": 2}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                        {"reminder": {"type": 71, "lastHandleType": 1}})
        assert self.tsp.log_search_wti(wtiKey="APA Working Status Cycle",wtiFlag=71)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderCycle",
                                        {"reminder": {"type": 71, "lastHandleType": 2}})
        assert self.tsp.log_search_wti(wtiKey="APA Working Status Cycle",wtiFlag=0)
        

    @allure.title("乘客需要系上安全带才能开启车道保持,WTI-2381")
    @pytest.mark.full
    def test_caseid_1994622(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 158, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP PStatus Reminder",wtiFlag=158)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP PStatus Reminder",wtiFlag=0)
        

    @allure.title("乘客需要系上安全带才能开启ASD,WTI-2382")
    @pytest.mark.full
    def test_caseid_1994623(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 159, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP PStatus Reminder",wtiFlag=159)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP PStatus Reminder",wtiFlag=0)
    
    
        
    
    @allure.title("前向摄像头温度过高,WTI-2360")
    @pytest.mark.full
    def test_caseid_1994627(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"wideAngleCamera": {"cameraTemperatureReminder": 0}
                                }})
        sleep(1)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"wideAngleCamera": {"cameraTemperatureReminder": 1}
                                }})
        assert self.tsp.log_search_wti(wtiKey="Front View Camera Over Temperature Reminder",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"wideAngleCamera": {"cameraTemperatureReminder": 0}
                                }})
        assert self.tsp.log_search_wti(wtiKey="Front View Camera Over Temperature Reminder",wtiFlag=0)
        

    @allure.title("侧向和后向摄像头温度过高,WTI-2363")
    @pytest.mark.full
    def test_caseid_1994628(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"rearCamera": {"cameraTemperatureReminder": 0}
                                }})
        sleep(1)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"rearCamera": {"cameraTemperatureReminder": 1}
                                }})
        assert self.tsp.log_search_wti(wtiKey="Side and Rear View Camera Over Temperature Reminder",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"rearCamera": {"cameraTemperatureReminder": 0}
                                }})
        assert self.tsp.log_search_wti(wtiKey="Side and Rear View Camera Over Temperature Reminder",wtiFlag=0)


    @allure.title("环视鱼眼摄像头摄像头温度过高,WTI-2364")
    @pytest.mark.full
    def test_caseid_1994629(self):
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"frontAVMCamera": {"cameraTemperatureReminder": 0}
                                }})
        sleep(1)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"frontAVMCamera": {"cameraTemperatureReminder": 1}
                                }})
        assert self.tsp.log_search_wti(wtiKey="AVM Camera Over Temperature Reminder",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify(ACUFaultInfo_SERVICE_SERVER, "CameraReminderInfo", 
                        {"info": {"frontAVMCamera": {"cameraTemperatureReminder": 0}
                                }})
        assert self.tsp.log_search_wti(wtiKey="AVM Camera Over Temperature Reminder",wtiFlag=0)
        


    @allure.title("前向和侧后向辅助安全功能受限提醒,WTI-2354")
    @pytest.mark.full
    def test_caseid_1994630(self):
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":0,"faultSts": 0}})
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", {"rcwStatus":{"functionStatus":0,"faultSts": 0}})
        sleep(1)
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":1,"faultSts": 1}})
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", {"rcwStatus":{"functionStatus":1,"faultSts": 1}})
        assert self.tsp.log_search_wti(wtiKey="Front And Side Back ADAS Limit Reminder",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":0,"faultSts": 0}})
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", {"rcwStatus":{"functionStatus":0,"faultSts": 0}})
        assert self.tsp.log_search_wti(wtiKey="Front And Side Back ADAS Limit Reminder",wtiFlag=0)



    @allure.title("前向辅助安全功能受限提醒,WTI-2355")
    @pytest.mark.full
    def test_caseid_1994631(self):
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":0,"faultSts": 0}})
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", {"rcwStatus":{"functionStatus":0,"faultSts": 0}})
        sleep(1)
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":1,"faultSts": 1}})
        assert self.tsp.log_search_wti(wtiKey="Front And Side Back ADAS Limit Reminder",wtiFlag=2)
        sleep(1)
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":0,"faultSts": 0}})
        assert self.tsp.log_search_wti(wtiKey="Front And Side Back ADAS Limit Reminder",wtiFlag=0)



    @allure.title("侧后向辅助安全功能受限提醒,WTI-2356")
    @pytest.mark.full
    def test_caseid_1994632(self):
        self.partner.send_event_notify(ELKSERVICE_SERVER, "ELKSts", {"sts":{"switchSts":0,"faultSts": 0}})
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", {"rcwStatus":{"functionStatus":0,"faultSts": 0}})
        sleep(1)
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", {"rcwStatus":{"functionStatus":1,"faultSts": 1}})
        assert self.tsp.log_search_wti(wtiKey="Front And Side Back ADAS Limit Reminder",wtiFlag=3)
        sleep(1)
        self.partner.send_event_notify(RCW_SERVICE_SERVER, "NotifyRCWStatus", {"rcwStatus":{"functionStatus":0,"faultSts": 0}})
        assert self.tsp.log_search_wti(wtiKey="Front And Side Back ADAS Limit Reminder",wtiFlag=0)



    # @allure.title("侧后向辅助安全功能受限提醒,WTI-2356")
    # def test_caseid_480110(self):
    #     self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts":{"anpStatus":0}})
    #     sleep(1)
    #     self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts":{"anpStatus":3}})
    #     sleep(1)
    #     self.partner.send_event_notify(MARSPILOTMARSDRIVER_SERVICE_SERVER, "NotifyAutoDriverStatus", {"sts":{"anpStatus":0}})


    @allure.title("夜间智驾安全提醒,WTI-2385")
    @pytest.mark.full
    def test_caseid_1994634(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NightDrivingSafetyReminder", {"reminder":0})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NightDrivingSafetyReminder", {"reminder":1})
        assert self.tsp.log_search_wti(wtiKey="Night Driving Safety Reminder",wtiFlag=1)
        sleep(2)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NightDrivingSafetyReminder", {"reminder":0})
        assert self.tsp.log_search_wti(wtiKey="Night Driving Safety Reminder",wtiFlag=0)


    @allure.title("当前电量过低,无法放电,WTI-2343")
    @pytest.mark.full
    def test_caseid_1994635(self):
        self.bus_comm.set_singal("chassiscan2","EcmChas2Fr09","DchaStopByTarDrvrIndcn",0)
        sleep(1)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04","DispHvBattLvlOfChrg",20.0)
        self.bus_comm.set_singal("chassiscan2","EcmChas2Fr09","DchaStopByTarDrvrIndcn",1)
        assert self.tsp.log_search_wti(wtiKey="Discharge Reminder",wtiFlag=1)
        sleep(1)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04","DispHvBattLvlOfChrg",100.0)
        self.bus_comm.set_singal("chassiscan2","EcmChas2Fr09","DchaStopByTarDrvrIndcn",0)
        assert self.tsp.log_search_wti(wtiKey="Discharge Reminder",wtiFlag=0)


    @allure.title("当前电量低于放电限值,请调整限值后重试,WTI-2350")
    @pytest.mark.full
    def test_caseid_1994636(self):
        self.bus_comm.set_singal("chassiscan2","EcmChas2Fr09","DchaStopByTarDrvrIndcn",0)
        sleep(1)
        self.bus_comm.set_singal("propulsioncan","EcmPropFr04","DispHvBattLvlOfChrg",100.0)
        self.bus_comm.set_singal("chassiscan2","EcmChas2Fr09","DchaStopByTarDrvrIndcn",1)
        assert self.tsp.log_search_wti(wtiKey="Discharge Reminder",wtiFlag=2)
        sleep(1)
        self.bus_comm.set_singal("chassiscan2","EcmChas2Fr09","DchaStopByTarDrvrIndcn",0)
        assert self.tsp.log_search_wti(wtiKey="Discharge Reminder",wtiFlag=0)



    @allure.title("WTI-2357,当前电量高于充电目标，请调整目标后重新插枪")
    @pytest.mark.full
    def test_caseid_1994672(self):
        self.bus_comm.set_SOC_display_value(80.0)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",60.0)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        assert self.tsp.log_search_wti(wtiKey="Charge Reminder",wtiFlag=1)
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_SOC_display_value(90.0)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",90.0)
        sleep(1)
        self.bus_comm.set_SOC_display_value(80.0)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",60.0)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        sleep(4)
        assert self.tsp.log_search_wti(wtiKey="Charge Reminder",wtiFlag=0)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        self.bus_comm.set_SOC_display_value(90.0)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",90.0)



    @allure.title("WTI-2358,已满充无需充电")
    @pytest.mark.full
    def test_caseid_1994673(self):
        self.bus_comm.set_SOC_display_value(100.0)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",100.0)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        assert self.tsp.log_search_wti(wtiKey="Charge Reminder",wtiFlag=2)
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_SOC_display_value(100.0)
        self.bus_comm.set_singal("chassiscan1","EcmChas1Fr13","BookChrgnTarValFb",100.0)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        sleep(4)
        assert self.tsp.log_search_wti(wtiKey="Charge Reminder",wtiFlag=0)
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)

    
    @allure.title("临近路口，无法开启车道保持,WTI-2377")
    @pytest.mark.full
    def test_caseid_1997134(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 160, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=160)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)


    @allure.title("关门请当心 ,WTI-2389")
    @pytest.mark.full
    def test_caseid_1997133(self):
        self.bus_comm.set_singal("connectivitycanfd","BncmConnectivityFr17", 'BLEKeyPrsntStsZone1', 1)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type":81, "lastHandleType":2}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 81, "lastHandleType": 1}})
        assert self.tsp.log_search_wti(wtiKey="APA TTS",wtiFlag=81)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                       {"reminder": {"type": 81, "lastHandleType": 2}})
        assert self.tsp.log_search_wti(wtiKey="APA TTS",wtiFlag=0)
    
    
    @allure.title("已偏离导航路线，请立即接管,WTI-2391")
    @pytest.mark.full
    def test_caseid_1997132(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyPNCReminder",
                                       {"pncReminder": 0})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyPNCReminder",
                                       {"pncReminder": 116})
        assert self.tsp.log_search_wti(wtiKey="ANP PNC Remind",wtiFlag=116)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyPNCReminder",
                                       {"pncReminder": 0})
        assert self.tsp.log_search_wti(wtiKey="ANP PNC Remind",wtiFlag=0)


    @allure.title("雪天环境受限\n立即接管,即将退出到手动驾驶,WTI-2365")
    @pytest.mark.full
    def test_caseid_1997131(self):
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyAffectADOperationReminder",
                                       {"reminder": 0})
        sleep(1)
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyAffectADOperationReminder",
                                       {"reminder": 4})
        assert self.tsp.log_search_wti(wtiKey="Take Over Remind",wtiFlag=4)
        sleep(1)
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyAffectADOperationReminder",
                                       {"reminder": 0})
        assert self.tsp.log_search_wti(wtiKey="Take Over Remind",wtiFlag=0)



    @allure.title("立即接管n\雪天环境受限,已退出到手动驾驶,WTI-2366")
    @pytest.mark.full
    def test_caseid_1997130(self):
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                        {"fault": 0})
        sleep(1)
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                       {"fault":10})
        assert self.tsp.log_search_wti(wtiKey="ANP Degraed Fault Remind",wtiFlag=10)
        sleep(1)
        self.partner.send_event_notify(ANPMRC_SERVICE_SERVER, "NotifyANPDegraedFault",
                                      {"fault":0})
        assert self.tsp.log_search_wti(wtiKey="ANP Degraed Fault Remind",wtiFlag=0)



    @allure.title("雪天环境受限，无法开启车道保持,WTI-2367")
    @pytest.mark.full
    def test_caseid_1997129(self):
        self.sd_tester.write_multi_ccp({953:2})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 163, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP SM Change Status Remind2",wtiFlag=163)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP SM Change Status Remind2",wtiFlag=0)
        self.sd_tester.write_multi_ccp({953:0})


    @allure.title("雪天环境受限,无法开启车道保持和ASD,WTI-2368")
    @pytest.mark.full
    def test_caseid_1997128(self):
        self.sd_tester.write_multi_ccp({953:5})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 163, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP SM Change Status Remind2",wtiFlag=164)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP SM Change Status Remind2",wtiFlag=0)
        self.sd_tester.write_multi_ccp({953:0})


    @allure.title("雾天能见度低，无法开启车道保持,WTI-2369")
    @pytest.mark.full
    def test_caseid_1997127(self):
        self.sd_tester.write_multi_ccp({953:2})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 165, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP SM Change Status Remind2",wtiFlag=165)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP SM Change Status Remind2",wtiFlag=0)
        self.sd_tester.write_multi_ccp({953:0})


    @allure.title("雾天能见度低,无法开启车道保持和ASD,WTI-2370")
    @pytest.mark.full
    def test_caseid_1997126(self):
        self.sd_tester.write_multi_ccp({953:5})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 165, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP SM Change Status Remind2",wtiFlag=166)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP SM Change Status Remind2",wtiFlag=0)
        self.sd_tester.write_multi_ccp({953:0})

    
    @allure.title("无法找到目标车道，请立即接管,WTI-2390")
    @pytest.mark.full
    def test_caseid_1997125(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyPNCReminder",
                                       {"pncReminder": 0})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyPNCReminder",
                                       {"pncReminder": 118})
        assert self.tsp.log_search_wti(wtiKey="ANP PNC Remind",wtiFlag=118)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyPNCReminder",
                                      {"pncReminder": 0})
        assert self.tsp.log_search_wti(wtiKey="ANP PNC Remind",wtiFlag=0)


    @allure.title("前方行驶区域过窄，停车等待，请手动接管,WTI-2401")
    @pytest.mark.full
    def test_caseid_1997124(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 167, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=167)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)


    @allure.title("导航路线变化，已退出到车道保持,WTI-2402")
    @pytest.mark.full
    def test_caseid_1997123(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 161, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=161)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)


    @allure.title("立即控制方向盘，已退出到自适应巡航\n导航路线改变,WTI-2403")
    @pytest.mark.full
    def test_caseid_1997122(self):
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 162, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=162)
        sleep(1)
        self.partner.send_event_notify(ANPWTI_SERVICE_SERVER, "NotifyANPStatus",
                                       {"anpStsReminder": {"anpStatusReminder": 0, "openSource": 2}})
        assert self.tsp.log_search_wti(wtiKey="ANP Status Open Source",wtiFlag=0)



    @allure.title("光线过暗，有刮蹭风险, WTI-2406")
    @pytest.mark.full 
    def test_caseid_1997121(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type": 41, "lastHandleType": 1,"sensorSts":5}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyReminder",wtiFlag=5)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyReminder",wtiFlag=0)


    @allure.title("新增车外tts提示:我开始了，光线过暗，帮我看着点, WTI-2407")
    @pytest.mark.full 
    def test_caseid_1997120(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type": 41, "lastHandleType": 1,"sensorSts":5}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyTts",wtiFlag=5)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyTts",wtiFlag=0)

    
    @allure.title("车头摄像头脏污，有刮蹭风险, WTI-2396")
    @pytest.mark.full 
    def test_caseid_1997119(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type": 41, "lastHandleType": 1,"sensorSts":1}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyReminder",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyReminder",wtiFlag=0)


    @allure.title("车尾摄像头脏污，有刮蹭风险, WTI-2397")
    @pytest.mark.full 
    def test_caseid_1997118(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type": 41, "lastHandleType": 1,"sensorSts":2}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyReminder",wtiFlag=2)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyReminder",wtiFlag=0)



    
    @allure.title("左后视镜摄像头脏污，有刮蹭风险, WTI-2398")
    @pytest.mark.full 
    def test_caseid_1997117(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type": 41, "lastHandleType": 1,"sensorSts":3}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyReminder",wtiFlag=3)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyReminder",wtiFlag=0)


    
    @allure.title("右后视镜摄像头脏污，有刮蹭风险, WTI-2399")
    @pytest.mark.full 
    def test_caseid_1997116(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type": 41, "lastHandleType": 1,"sensorSts":4}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyReminder",wtiFlag=4)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPAReminderEvent",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyReminder",wtiFlag=0)


    
    @allure.title("车外tts播报:我开始了，帮我看着点，车头摄像头有点脏，记得帮我擦一下, WTI-2408")
    @pytest.mark.full 
    def test_caseid_1997115(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type": 41, "lastHandleType": 1,"sensorSts":1}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyTts",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyTts",wtiFlag=0)


    @allure.title("车外tts播报:我开始了，帮我看着点，车尾摄像头有点脏，记得帮我擦一下, WTI-2409")
    @pytest.mark.full 
    def test_caseid_1997114(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type": 41, "lastHandleType": 1,"sensorSts":2}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyTts",wtiFlag=2)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyTts",wtiFlag=0)


    @allure.title("车外tts播报:我开始了，帮我看着点，左后视镜摄像头有点脏，记得帮我擦一下, WTI-2410")
    @pytest.mark.full 
    def test_caseid_1997113(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type": 41, "lastHandleType": 1,"sensorSts":3}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyTts",wtiFlag=3)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyTts",wtiFlag=0)


    @allure.title("车外tts播报:我开始了，帮我看着点，右后视镜摄像头有点脏，记得帮我擦一下, WTI-2411")
    @pytest.mark.full 
    def test_caseid_1997112(self):
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type": 41, "lastHandleType": 1,"sensorSts":4}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyTts",wtiFlag=4)
        sleep(1)
        self.partner.send_event_notify(RPAAPA_SERVICE_SERVER, "NotifyAPARemoteReminder",
                                        {"reminder": {"type":41, "lastHandleType":2,"sensorSts":0}})
        assert self.tsp.log_search_wti(wtiKey="CameraDirtyTts",wtiFlag=0)


    # @allure.title("红绿灯识别及提醒: 前车驾离，请起步,WTI-2422")
    # @pytest.mark.full 
    # def test_caseid_1997111(self):
    #     self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
    #                                     {"tlaFunctionStatus": {"startRemid":0}})
    #     sleep(1)
    #     self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
    #                                     {"tlaFunctionStatus": {"startRemid":1}})
    #     assert self.tsp.log_search_wti(wtiKey="Traffic Light Identification Remind",wtiFlag=5)
    #     sleep(1)
    #     self.partner.send_event_notify(TLA_SERVICE_SERVER, "NotifyTLAFunctionStatus",
    #                                     {"tlaFunctionStatus": {"startRemid":0}})
    #     assert self.tsp.log_search_wti(wtiKey="Traffic Light Identification Remind",wtiFlag=0)
    #     #当前3.0需求暂时不测试，此需求已回退到2.2AC版本



    # @allure.title("紧急转向辅助已激活,WTI-2379")
    # @pytest.mark.full 
    # def test_caseid_1997107(self):
    #     self.partner.send_event_notify(ESS_SERVICE_SERVER, "ESSInfo",
    #                                     {"essInfo": {"activeSts":0}})
    #     sleep(1)
    #     self.partner.send_event_notify(ESS_SERVICE_SERVER, "ESSInfo",
    #                                     {"essInfo": {"activeSts":1}})
    #     assert self.tsp.log_search_wti(wtiKey="ESSActiveReminder",wtiFlag=1)
    #     sleep(1)
    #     self.partner.send_event_notify(ESS_SERVICE_SERVER, "ESSInfo",
    #                                     {"essInfo": {"activeSts":0}})
    #     assert self.tsp.log_search_wti(wtiKey="ESSActiveReminder",wtiFlag=0)
    #     sleep(1)
    #     self.partner.send_event_notify(ESS_SERVICE_SERVER, "ESSInfo",
    #                                     {"essInfo": {"activeSts":2}})
    #     assert self.tsp.log_search_wti(wtiKey="ESSActiveReminder",wtiFlag=1)
    #     sleep(1)
    #     self.partner.send_event_notify(ESS_SERVICE_SERVER, "ESSInfo",
    #                                     {"essInfo": {"activeSts":0}})
    #     assert self.tsp.log_search_wti(wtiKey="ESSActiveReminder",wtiFlag=0)


    @allure.title("车速超过120km/h提醒(针对GSO),WTI-2412")
    @pytest.mark.full
    def test_caseid_1997108(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgVehSpdOver120",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgVehSpdOver120",'data':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgVehSpdOver120",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgVehSpdOver120",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgVehSpdOver120",wtiFlag=0)


    @allure.title("儿童座椅连接异常，请检查 MSO-WTI-1829")
    @pytest.mark.full
    def test_caseid_1999038(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgChildSeatConnectionFault",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgChildSeatConnectionFault",'data':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgChildSeatConnectionFault",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgChildSeatConnectionFault",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgChildSeatConnectionFault",wtiFlag=0)


    @allure.title("请系好儿童座椅安全带 MSO-WTI-2340")
    @pytest.mark.full
    def test_caseid_1999037(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgChildSeatbeltAlarm",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgChildSeatbeltAlarm",'data':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgChildSeatbeltAlarm",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgChildSeatbeltAlarm",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgChildSeatbeltAlarm",wtiFlag=0)


    @allure.title("请系好儿童座椅安全带 MSO-WTI-2221")
    @pytest.mark.full
    def test_caseid_1999036(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgChildSeatbeltAlarm",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgChildSeatbeltAlarm",'data':"2"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgChildSeatbeltAlarm",wtiFlag=2)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgChildSeatbeltAlarm",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgChildSeatbeltAlarm",wtiFlag=0)


    @allure.title("洗车模式开启，我要关门了,请当心 MSO-WTI-2314")
    @pytest.mark.full
    def test_caseid_1999035(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgDoorCloseWashModeReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgDoorCloseWashModeReminder",'data':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgDoorCloseWashModeReminder",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgDoorCloseWashModeReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgDoorCloseWashModeReminder",wtiFlag=0)


    @allure.title("系统故障，及时停车以退出赛道模式 MSO-WTI-2311")
    @pytest.mark.full
    def test_caseid_1999034(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHVRaceModeExitPromptStatus",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHVRaceModeExitPromptStatus",'data':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHVRaceModeExitPromptStatus",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHVRaceModeExitPromptStatus",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHVRaceModeExitPromptStatus",wtiFlag=0)


    
    @allure.title("系统故障，赛道模式即将退出 MSO-WTI-2312")
    @pytest.mark.full
    def test_caseid_1999033(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHVRaceModeExitPromptStatus",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHVRaceModeExitPromptStatus",'data':"2"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHVRaceModeExitPromptStatus",wtiFlag=2)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHVRaceModeExitPromptStatus",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHVRaceModeExitPromptStatus",wtiFlag=0)


    
    @allure.title("试驾模式超速提醒一级 MSO-WTI-2371")
    @pytest.mark.full
    def test_caseid_1999032(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgTestDriveOverSpeedReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgTestDriveOverSpeedReminder",'data':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgTestDriveOverSpeedReminder",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgTestDriveOverSpeedReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgTestDriveOverSpeedReminder",wtiFlag=0)


    @allure.title("试驾模式超速提醒二级 MSO-WTI-2374")
    @pytest.mark.full
    def test_caseid_1999031(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgTestDriveOverSpeedReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgTestDriveOverSpeedReminder",'data':"2"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgTestDriveOverSpeedReminder",wtiFlag=2)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgTestDriveOverSpeedReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgTestDriveOverSpeedReminder",wtiFlag=0)


    @allure.title("3D地图视野锁定提示  MSO-WTI-2404")
    @pytest.mark.full
    def test_caseid_1999028(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgMapLockReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgMapLockReminder",'data':"1"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgMapLockReminder",wtiFlag=1)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgMapLockReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgMapLockReminder",wtiFlag=0)


    @allure.title("3D地图视野解锁提示  MSO-WTI-2405")
    @pytest.mark.full
    def test_caseid_1999027(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgMapLockReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgMapLockReminder",'data':"2"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgMapLockReminder",wtiFlag=2)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgMapLockReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgMapLockReminder",wtiFlag=0)


    @allure.title("若要点选车位，请先深踩刹车 MSO-WTI-2275")
    @pytest.mark.full
    def test_caseid_1999026(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2275"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2275)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("暂不支持机械车位 MSO-WTI-2278")
    @pytest.mark.full
    def test_caseid_1999025(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2278"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2278)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)



    @allure.title("车位过窄，暂不支持 MSO-WTI-2279")
    @pytest.mark.full
    def test_caseid_1999024(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2279"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2279)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("通道过窄，暂不支持 MSO-WTI-2280")
    @pytest.mark.full
    def test_caseid_1999023(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2280"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2280)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("点击其他原因引起不可泊的车位 MSO-WTI-2281")
    @pytest.mark.full
    def test_caseid_1999022(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2281"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2281)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("坡度过大，暂不支持 MSO-WTI-2282")
    @pytest.mark.full
    def test_caseid_1999021(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2282"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2282)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("车位过远，可以开近点再试试 MSO-WTI-2283")
    @pytest.mark.full
    def test_caseid_1999020(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2283"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2283)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("车位上有锥桶，无法泊入 MSO-WTI-2284")
    @pytest.mark.full
    def test_caseid_1999019(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2284"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2284)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("车位上有车，无法泊入 MSO-WTI-2285")
    @pytest.mark.full
    def test_caseid_1999018(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2285"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2285)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("车位上有人，无法泊入 MSO-WTI-2286")
    @pytest.mark.full
    def test_caseid_1999017(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2286"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2286)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("地锁未降，无法泊入 MSO-WTI-2287")
    @pytest.mark.full
    def test_caseid_1999016(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2287"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2287)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("车位上有障碍物，无法泊入 MSO-WTI-2288")
    @pytest.mark.full
    def test_caseid_1999015(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2288"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2288)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)



    @allure.title("阻车器阻挡，无法泊入 MSO-WTI-2289")
    @pytest.mark.full
    def test_caseid_1999014(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2289"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2289)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("车头方向不正，无法泊入 MSO-WTI-2290")
    @pytest.mark.full
    def test_caseid_1999013(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2290"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2290)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("若要点选车位，请先深踩刹车 MSO-WTI-2291")
    @pytest.mark.full
    def test_caseid_1999012(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2291"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2291)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("若要点选车位，请先深踩刹车 MSO-WTI-2292")
    @pytest.mark.full
    def test_caseid_1999011(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2292"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2292)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)

    
    @allure.title("距离过短，无法选择车位 MSO-WTI-2339")
    @pytest.mark.full
    def test_caseid_1999010(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2339"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2339)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("退出全量车位搜索模式(APA&AVP) MSO-WTI-2344")
    @pytest.mark.full
    def test_caseid_1999009(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"2344"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=2344)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIAvpReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIAvpReminder",wtiFlag=0)


    @allure.title("光线过暗，无法开启自动泊车  MSO-WTI-2107")
    @pytest.mark.full
    def test_caseid_1999008(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2107"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2107)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("退出全量车位搜索模式(APA&AVP)  MSO-WTI-2344")
    @pytest.mark.full
    def test_caseid_1999007(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2344"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2344)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("若要点选车位，请先深踩刹车 MSO-WTI-2248")
    @pytest.mark.full
    def test_caseid_1999006(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2248"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2248)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("若要点选车位，请先深踩刹车 MSO-WTI-2249")
    @pytest.mark.full
    def test_caseid_1999005(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2249"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2249)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("通道过窄，暂不支持 MSO-WTI-2250")
    @pytest.mark.full
    def test_caseid_1999004(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2250"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2250)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)
    

    @allure.title("暂不支持机械车位 MSO-WTI-2251")
    @pytest.mark.full
    def test_caseid_1999003(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2251"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2251)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("车位过窄，暂不支持 MSO-WTI-2252")
    @pytest.mark.full
    def test_caseid_1999002(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2252"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2252)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("点击其他原因导致的不可泊车位  MSO-WTI-2253")
    @pytest.mark.full
    def test_caseid_1999001(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2253"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2253)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)

    
    @allure.title("坡度过大，暂不支持  MSO-WTI-2254")
    @pytest.mark.full
    def test_caseid_1999000(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2254"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2254)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("自动泊车辅助退出  MSO-WTI-2255")
    @pytest.mark.full
    def test_caseid_1998999(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2255"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2255)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("自动泊车未开启，请去车辆设置中打开  MSO-WTI-2265")
    @pytest.mark.full
    def test_caseid_1998998(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2265"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2265)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("车位上有锥桶，无法泊入  MSO-WTI-2266")
    @pytest.mark.full
    def test_caseid_1998997(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2266"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2266)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("车位上有人，无法泊入  MSO-WTI-2267")
    @pytest.mark.full
    def test_caseid_1998996(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2267"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2267)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("地锁未降，无法泊入  MSO-WTI-2268")
    @pytest.mark.full
    def test_caseid_1998995(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2268"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2268)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("车位上有车，无法泊入  MSO-WTI-2269")
    @pytest.mark.full
    def test_caseid_1998994(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2269"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2269)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("车位上有障碍物，无法泊入  MSO-WTI-2270")
    @pytest.mark.full
    def test_caseid_1998993(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2270"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2270)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("车位过远，可以开近点再试试  MSO-WTI-2271")
    @pytest.mark.full
    def test_caseid_1998992(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2271"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2271)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("阻车器阻挡，无法泊入  MSO-WTI-2272")
    @pytest.mark.full
    def test_caseid_1998991(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2272"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2272)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("车头方向不正，无法泊入  MSO-WTI-2273")
    @pytest.mark.full
    def test_caseid_1998990(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2273"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2273)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("车尾摄像头脏污，清理后再开启自动泊车  MSO-WTI-2392")
    @pytest.mark.full
    def test_caseid_1998989(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2392"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2392)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("车头摄像头脏污，清理后再开启自动泊车  MSO-WTI-2393")
    @pytest.mark.full
    def test_caseid_1998988(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2393"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2393)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("左后视镜摄像头脏污，清理后再开启自动泊车  MSO-WTI-2394")
    @pytest.mark.full
    def test_caseid_1998987(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2394"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2394)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)


    @allure.title("右后视镜摄像头脏污，清理后再开启自动泊车  MSO-WTI-2395")
    @pytest.mark.full
    def test_caseid_1998986(self):
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"2395"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=2395)
        sleep(1)
        self.partner.send_event_notify("cdc_wtiservice_crossdomain_server","WarningMsgStatus",
                                       {'values': [{'id': "CDCWTIMsgHavpWTIApaReminder",'data':"0"}]})
        assert self.tsp.log_search_wti(wtiKey="CDCWTIMsgHavpWTIApaReminder",wtiFlag=0)