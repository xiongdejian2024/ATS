#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File         :test_wtiauto_wti_pressure.py
@Time         :2024/04/25 17:20:31
@Author       :gang.liu@jiduauto.com
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


@allure.feature("性能稳定性")
@allure.story("业务稳定性/启动场景压测-时间戳压测")
@pytest.mark.soa
class TestWTIAutoDriveService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("WTIService", "client"),
                                     ("WTIAutoDriveService", "client"),
                                     ("LightService", "client"),
                                     ("DoorService", "client"),
                                     ("AVPService", "server"),
                                     ("AutoHighBeamControlService","server"),
                                     ("CMSFService", "server")
                                     ])
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.AutoDriverStatus_response = False
        self.ANP_response = False

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
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
        
    def ck_s2s_event_timestamp(self, partner_key: str, interface_name: str, ck_info: dict, timeout=3, fuzz_match=True):
        """
        校验被测对象发送的resp内容
        :param partner_key: 类似KeyService_Server
        :param interface_name: 接口名
        :param ck_info: 校验事件内容
        :param timeout: 校验时间
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return: raw_data，event数据内容
        """
        st = time.time()
        logger.info(f"ck_s2s_event st:{st}")
        tmp_list = []
        while time.time() - st < timeout:
            try:
                event = self.partner.partner_infos[partner_key].event_queue.get(timeout=(st + timeout - time.time()))
            except queue.Empty:
                assert False, "超时未获取到期望event"
            else:
                if event['function'] == f"Update{interface_name}Event":
                    raw_data = eval(event['args'])
                    if (fuzz_match and ck_data(raw_data, ck_info)) or (not fuzz_match and raw_data == ck_info):
                        logger.info(f"校验{interface_name}::{ck_info}--True")
                        self.partner._put_items_to_queue(self.partner.partner_infos[partner_key].event_queue, 
                                                         sorted(tmp_list, key=return_timestamp))
                        return (event, raw_data)
                    else:
                        tmp_list.insert(0, event)
                else:
                    tmp_list.insert(0, event)
    
    def return_latest_event_wti(self, partner_key: str, interface_name: str):
        """
        返回指定接口最近的一次event消息
        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        """
        event = list(self.partner.partner_infos[partner_key].event_queue.queue)[-1]
        return eval(event['args'])
        
    @allure.title("WTIAuto时间戳压测")
    @pytest.mark.sanity
    @pytest.mark.repeat(3000)
    def test_caseid_1985358(self):
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                                       {"cmsfStatus": {"faultSts": 0}})
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyAVPReminderCycle",
                                       {"avpReminder": {"type": 0, "source": 0}})
        self.partner.empty_all(0.5)
        self.partner.send_event_notify(CMSF_SERVICE_SERVER, "NotifyCMSFStatus", 
                                       {"cmsfStatus": {"faultSts": 2}})
        self.partner.send_event_notify(AVP_SERVICE_SERVER, "NotifyAVPReminderCycle",
                                       {"avpReminder": {"type": 6, "source": 1}})
        sleep(1)
        #如果两个通知在一个报文中，则比较两个通知上报的时间是否相同，否则按partner收到的时间戳进行比较
        latestEvent = self.return_latest_event_wti(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList")
        logger.info(f"--latestEvent: {latestEvent}")
        if len(latestEvent['list']) > 1:
            firstWtiTimestamp = event1["list"][0]['sequenceTime']['timestamp']
            latestWtiTimestamp = event1["list"][len(latestEvent)-1]['sequenceTime']['timestamp']
            assert firstWtiTimestamp == latestWtiTimestamp
        else:
            data1,event1 = self.ck_s2s_event_timestamp(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", {"list":[{'name': 'FCW_AEB Failed Warning', 'info': '1'}]})
            event1_timestamp = event1["list"][0]['sequenceTime']['timestamp']
            data2,event2 = self.ck_s2s_event_timestamp(WTIAUTODRIVE_SERVICE_CLIENT, "WarningMsgList", {"list":[{'name': 'HAVP Cycle Warn Both', 'info': '1'}]})
            event2_timestamp = event2["list"][0]['sequenceTime']['timestamp']
            logger.info(f"--data1time: {data1['timestamp']}--event1_timestamp: {event1_timestamp}")
            logger.info(f"--data2time: {data2['timestamp']}--event2_timestamp: {event2_timestamp}")
            if data2['timestamp'] > data1['timestamp']:
                assert event2_timestamp > event1_timestamp
            else:
                assert event2_timestamp <= event1_timestamp
                
            
class TestWTIService(TestBase):
    def before_class(self, ecu):
        """测试用例的前处理"""
        super().before_class(self, ecu)
        self.partner = S2sBaseClass([("WTIService", "client"),
                                     ("WTIAutoDriveService", "client"),
                                     ("LightService", "client"),
                                     ("DoorService", "client"),
                                     ("AVPService", "server"),
                                     ("AutoHighBeamControlService","server"),
                                     ("CMSFService", "server")
                                     ])
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr18, 'TrsmParkLockdTrsmParkLockd', 'TrsmParkLock1_ParkEngd')
        self.ipdu.set(self.ipdu.backbonefr.VddmBackBoneFr03, 'GearLvrIndcn', 'GearLvrIndcn2_ParkIndcn')
        self.AutoDriverStatus_response = False
        self.ANP_response = False

    def after_class(self, ecu):
        """测试用例全部完成后的后处理"""
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
        
    def ck_s2s_event_timestamp(self, partner_key: str, interface_name: str, ck_info: dict, timeout=3, fuzz_match=True):
        """
        校验被测对象发送的resp内容
        :param partner_key: 类似KeyService_Server
        :param interface_name: 接口名
        :param ck_info: 校验事件内容
        :param timeout: 校验时间
        :param fuzz_match: 是否模糊匹配，模糊匹配对列表类的只需要列表内参数在event的列表中即可
        :return: raw_data，event数据内容
        """
        st = time.time()
        logger.info(f"ck_s2s_event st:{st}")
        tmp_list = []
        while time.time() - st < timeout:
            try:
                event = self.partner.partner_infos[partner_key].event_queue.get(timeout=(st + timeout - time.time()))
            except queue.Empty:
                assert False, "超时未获取到期望event"
            else:
                if event['function'] == f"Update{interface_name}Event":
                    raw_data = eval(event['args'])
                    if (fuzz_match and ck_data(raw_data, ck_info)) or (not fuzz_match and raw_data == ck_info):
                        logger.info(f"校验{interface_name}::{ck_info}--True")
                        self.partner._put_items_to_queue(self.partner.partner_infos[partner_key].event_queue, 
                                                         sorted(tmp_list, key=return_timestamp))
                        return (event, raw_data)
                    else:
                        tmp_list.insert(0, event)
                else:
                    tmp_list.insert(0, event)
    
    def return_latest_event_wti(self, partner_key: str, interface_name: str):
        """
        返回指定接口最近的一次event消息
        :param partner_key: 类似KeyService_Server
        :param interface_name:  接口名
        """
        event = list(self.partner.partner_infos[partner_key].event_queue.queue)[-1]
        return eval(event['args'])
                   
    @allure.title("WTI时间戳压测")
    @pytest.mark.sanity
    @pytest.mark.repeat(3000)
    def test_caseid_1985492(self):
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',0)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean1",0)
        self.partner.empty_all(0.5)
        self.ipdu.set(self.ipdu.bodycan.SmbBodyFr01, 'SeatVentAvlStsRowSecRi',3)
        self.ipdu.set(self.ipdu.bodycan.DpodBodyFr01,"DtcInfDoorDrvrBoolean1",1)
        sleep(2)
        latestEvent = self.return_latest_event_wti(WTI_SERVICE_CLIENT, "WarningMsgList")
        logger.info(f"--latestEvent: {latestEvent}")
        data1,event1 = self.ck_s2s_event_timestamp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list":[{'name': 'Rear Right Seat Vent Warning', 'info': '1'}]})
        data2,event2 = self.ck_s2s_event_timestamp(WTI_SERVICE_CLIENT, "WarningMsgList", {"list":[{'name': 'Door AntiPlay Reminder', 'info': '1'}]})
        if len(latestEvent['list']) > 1:
            firstWtiTimestamp = event1["list"][0]['sequenceTime']['timestamp']
            latestWtiTimestamp = event1["list"][len(latestEvent)-1]['sequenceTime']['timestamp']
            assert firstWtiTimestamp == latestWtiTimestamp
        else:
            event1_timestamp = event1["list"][0]['sequenceTime']['timestamp']
            event2_timestamp = event2["list"][0]['sequenceTime']['timestamp']
            logger.info(f"--data1time: {data1['timestamp']}--event1_timestamp: {event1_timestamp}")
            logger.info(f"--data2time: {data2['timestamp']}--event2_timestamp: {event2_timestamp}")
            if data2['timestamp'] > data1['timestamp']:
                assert event2_timestamp > event1_timestamp
            else:
                assert event2_timestamp <= event1_timestamp
        