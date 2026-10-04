# -*- coding: utf-8 -*-
"""
@File        : test_RtcAlarmService.py
@Author      : jingjing.wang
@Time        : 2023/06/20 15:00 PM
@Description : Test s2s interface about rtcalarm function
"""
import time
from time import sleep
import pytest
import datetime
import numpy as np
from xat_ecu.legacy.interface.bgm.bgm_ssh import command_send  # 获取BGM的utc时间
from xat_cases.legacy.soa.case_helper.test_base import TestBase
from xat_cases.legacy.bgm.s2s.case_helper.S2S_can_sim import *
from xat_ecu.legacy.ecu_sim.sd_tester import Sd_Tester
from xat_ecu.legacy.soa_partner.src.base_partner import *
from xat_ecu.legacy.soa_partner.src.partner_const import *


@allure.feature("SOA服务接口")
@allure.story("互联服务/RtcAlarmService")
@pytest.mark.tcam
@pytest.mark.wjj
class TestRtcAlarmService(TestBase):
    def before_class(self, ecu):
        super().before_class(self, ecu)
        # self.nucapp.bgm_power_off()
        # 启动partner operator
        self.partner = S2sBaseClass([("RtcAlarmService", "client")])
        self.partner.method_default_timeout = 0.1
        sleep(5)
        # 为了防止诊断反馈NRC22,需要发送FlexRay报文
        self.ipdu.set(self.ipdu.backbonefr.BcmVddmBackBoneFr00, 'VehMtnStVehMtnSt', 'VehMtnSt2_StandStillVal3')

    def before_each_func(self, ecu):
        super().before_each_func(ecu, start=False)
        bool_true = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT,"CancelServiceBookEvent",
                                                            {"serviceName":"aaa"})["out"]
        bool_true1 = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT,"CancelServiceBookEvent",
                                                            {"serviceName":"ccc"})["out"]
        bool_true2 = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT,"CancelServiceBookEvent",
                                                            {"serviceName":"eat4"})["out"]
        bool_true3 = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT,"CancelServiceBookEvent",
                                                            {"serviceName":"bbb"})["out"]
        bool_true4 = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT,"CancelServiceBookEvent",
                                                            {"serviceName":"HighVoltageAppService"})["out"]
        if bool_true == True:
            print("取消成功")
        if bool_true1 == True:
            print("取消成功")
        if bool_true2 == True:
            print("取消成功")
        if bool_true3 == True:
            print("取消成功")
        if bool_true4 == True:
            print("取消成功")

    def after_each_func(self, ecu):
        super().after_each_func(ecu, start=False)

    def after_class(self, ecu):
        self.partner.stop_operators()
        # self.nucapp.bgm_power_on()
        super().after_class(self, ecu)

    def getdatetime(self, minute=1):
        date = self.bgmcli.type_commands('date +"%Y-%m-%d %H:%M:%S"')  # 进入bgm执行命令
        print(date)
        date1 = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        delta_second = 60 * minute - date1.second
        date3 = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(
            seconds=delta_second) + datetime.timedelta(hours=8)
        print(date3)
        return int(date3.timestamp()), delta_second

    def datetime_time(self):
        date = self.bgmcli.type_commands('date +"%Y-%m-%d %H:%M:%S"')  # 进入bgm执行命令
        print(date)
        date1 = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        second = date1.second
        print(second)
        sleep(59 - second)
        date2 = self.bgmcli.type_commands('date +"%Y-%m-%d %H:%M:%S"')
        date3 = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(hours=8)
        print(date3)
        timestamp = date3.timestamp()
        print(timestamp)
        return int(timestamp)
        
    @allure.title("设置默认时间预约事件_默认值0")
    @pytest.mark.smoke
    def test_caseid_108955_1978126_108956_108880_108879_108870_108869(self):
        start_time, delta_second = self.getdatetime(2)
        timerHandler_config_ifo = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",  # 设置预约事件
                                                      {"bookEventInfo": {"serviceName": "eat4",  # 进程名
                                                                         "repeatType": 0,  # 预约事件类型
                                                                         "rtcTime": start_time,  # 当前时间+200s业务预约时间
                                                                         "timerFlag": "eatapple4",  # 任务名
                                                                         "bookInfo":  # 客户展示信息
                                                                             {"bookType": "11",  # 设置预约事件类型
                                                                              "repeatType": 0,  # 预约事件重复类型
                                                                              "startTime": start_time,
                                                                              # 业务预约时间开始时间
                                                                              "stopTime": start_time + 1000}}})[
                "out"]  # 结束时间
        if timerHandler_config_ifo == "":
            assert False
        else:
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetBookInfoList", {}, {  # 查询服务已预约的事件信息
                "out": [
                    {"bookType": "11", "repeatType": 0, "startTime": start_time, "stopTime": start_time + 1000}]})
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                  {"serviceName": "eat4"}, {
                                                      "out": [{"serviceName": "eat4",
                                                               "repeatType": 0,
                                                               "rtcTime": start_time,
                                                               "timerFlag": "eatapple4",
                                                               "bookInfo": {"bookType": "11",
                                                                            "repeatType": 0,
                                                                            "startTime": start_time,
                                                                            "stopTime": start_time + 1000}}]})

            self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyBookInfoList", {"bookInfoList": [  # 通知预约展示信息列表
                {"bookType": "11",
                 "repeatType": 0,
                 "startTime": start_time,
                 "stopTime": start_time + 1000}
            ]})
            sleep(delta_second - 18)
            print(time.time())
            self.partner.ck_no_event(RTCALARM_SERVICE_CLIENT, "NotifyPrepareTimeUpEventInfo", timeout=1)
            print(time.time())
            self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyPrepareTimeUpEventInfo",  # 预约的任务开始时间到时提前15s通知
                                      {"bookEvent": {"serviceName": "eat4",
                                                     "repeatType": 0,
                                                     "rtcTime": start_time,
                                                     "timerFlag": "eatapple4",
                                                     "weekDay": 0,
                                                     "bookInfo": {"bookType": "11",
                                                                  "repeatType": 0,
                                                                  "weekDay": 0,
                                                                  "startTime": start_time,
                                                                  "stopTime": start_time + 1000}
                                                     }}, timeout=5)
            print(time.time())
            sleep(13)
            self.partner.ck_no_event(RTCALARM_SERVICE_CLIENT, "NotifyPrepareTimeUpEventInfo", timeout=1)
            self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyTimeUpEventInfo",  # 预约的任务开始时间到时通知
                                      {"bookEvent": {"serviceName": "eat4",
                                                     "repeatType": 0,
                                                     "weekDay": 0,
                                                     "rtcTime": start_time,
                                                     "timerFlag": "eatapple4",
                                                     "bookInfo": {"bookType": "11",
                                                                  "repeatType": 0,
                                                                  "weekDay": 0,
                                                                  "startTime": start_time,
                                                                  "stopTime": start_time + 1000}
                                                     }}, timeout=3)
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetBookInfoList", {}, {  # 查询服务已预约的事件信息
                "out": []})

    @allure.title("设置默认时间预约事件_repeatType=3")
    @pytest.mark.full
    def test_caseid_1978147(self):
        today = datetime.datetime.today()
        _week_day = today.isoweekday()
        logger.info(f"今天是周{_week_day}")
        for k,w in {1:0b00000001, 2:0b00000010, 3:0b00000100, 4:0b00001000, 5:0b00010000, 6:0b00100000, 7:0b01000000}.items():
            if _week_day == k:
                start_time, delta_second = self.getdatetime(2)
                bookInfo={"bookType": "1",
                            "repeatType": 3,
                            "weekDay": w,
                            "startTime": start_time + 60,
                            "stopTime": start_time + 1000}
                timerHandler_config_ifo = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                                                    {"bookEventInfo": {"serviceName": "aaa",
                                                                                                    # 进程名
                                                                                                    "repeatType": 3,
                                                                                                    "weekDay": w,
                                                                                                    "rtcTime": start_time,
                                                                                                    "timerFlag": "bbb",
                                                                                                    "bookInfo":bookInfo}})[
                    "out"]                                                                                        
                if timerHandler_config_ifo == "":
                    assert False
                else:
                    self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetBookInfoList", {}, {
                        "out": [{"bookType": "1", "repeatType": 3, "weekDay": w, "startTime": start_time + 60,
                                "stopTime": start_time + 1000}]})
                    self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                        {"serviceName": "aaa"}, {
                                                            "out": [{"serviceName": "aaa",
                                                                    "repeatType": 3,
                                                                    "weekDay": w,
                                                                    "rtcTime": start_time,
                                                                    "timerFlag": "bbb",
                                                                    "bookInfo": bookInfo}]})

                    self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyBookInfoList", {"bookInfoList": [
                        bookInfo]})

                    sleep(delta_second - 18)
                    self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyPrepareTimeUpEventInfo",
                                            {"bookEvent": {"serviceName": "aaa",
                                                            "repeatType": 3,
                                                            "weekDay": w,
                                                            "rtcTime": start_time,
                                                            "timerFlag": "bbb",

                                                            "bookInfo": bookInfo}}, timeout=3)

                    sleep(13)
                    self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyTimeUpEventInfo",
                                            {"bookEvent": {"serviceName": "aaa",
                                                            "repeatType": 3,
                                                            "weekDay": w,
                                                            "rtcTime": start_time,
                                                            "timerFlag": "bbb",
                                                            "bookInfo": bookInfo}}, timeout=3)
                    bookInfo_exp={"bookType": "1",
                            "repeatType": 3,
                            "weekDay": w,
                            "startTime": start_time + 60 +604800,
                            "stopTime": start_time + 1000 +604800}
                    self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetBookInfoList", {}, {
                        "out": [bookInfo_exp]},timeout=2)
                    self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",
                                                        {"timerHandler": timerHandler_config_ifo},
                                                        {"out": True})
                    self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetBookInfoList", {}, {
                        "out": []},timeout=2)

    # @allure.title("设置默认时间预约事件_repeatType=3间隔1min预约")
    # @pytest.mark.full
    # def test_caseid_1978110(self):
    #     start_time1, delta_second1 = self.getdatetime(2)
    #     start_time2, delta_second2 = self.getdatetime(3)
    #     timerHandler_config_ifo = \
    #         self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
    #                                                   # 设置预约事件,设置第一个预约事件当前时间+200s
    #                                                   {"bookEventInfo": {"serviceName": "aaa",  # 任务名称
    #                                                                      "repeatType": 3,
    #                                                                      "weekDay": 0b00000010,
    #                                                                      "rtcTime": start_time1,
    #                                                                      # 当前时间+200s业务预约时间
    #                                                                      "timerFlag": "aaa4",  # 业务数据
    #                                                                      # RTC是否已到时/接口未使用
    #                                                                      "bookInfo":
    #                                                                          {"bookType": "3",  # 设置预约事件类型
    #                                                                           "repeatType": 3,  # 预约事件重复类型
    #                                                                           "weekDay": 0b00000010,
    #                                                                           "startTime": start_time1,
    #                                                                           # 业务预约时间开始时间
    #                                                                           "stopTime": start_time1}}})[
    #             "out"]  # 结束时间
    #     timerHandler = \
    #         self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
    #                                                   # 设置预约事件,设置第一个预约事件当前时间+200s
    #                                                   {"bookEventInfo": {"serviceName": "bbb",  # 任务名称
    #                                                                      "repeatType": 3,
    #                                                                      "weekDay": 0b00000010,
    #                                                                      "rtcTime": start_time2,
    #                                                                      # 当前时间+200s业务预约时间
    #                                                                      "timerFlag": "bbb4",  # 业务数据
    #                                                                      # RTC是否已到时/接口未使用
    #                                                                      "bookInfo":
    #                                                                          {"bookType": "3",  # 设置预约事件类型
    #                                                                           "repeatType": 3,  # 预约事件重复类型
    #                                                                           "weekDay": 0b00000010,
    #                                                                           "startTime": start_time2,
    #                                                                           # 业务预约时间开始时间
    #                                                                           "stopTime": start_time2}}})[
    #             "out"]  # 结束时间

    #     self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetBookInfoList", {}, {  # 查询服务已预约的事件信息
    #         "out": [
    #             {"bookType": "3", "repeatType": 3, "weekDay": 0b00000010, "startTime": start_time1,
    #              "stopTime": start_time1},
    #             {"bookType": "3", "repeatType": 3, "weekDay": 0b00000010, "startTime": start_time2,
    #              "stopTime": start_time2}]})
    #     self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
    #                                           {"serviceName": "aaa"}, {
    #                                               "out": [{"serviceName": "aaa", "repeatType": 3, "weekDay": 0b00000010,
    #                                                        "rtcTime": start_time1, "timerFlag": "aaa4",
    #                                                        "bookInfo": {"bookType": "3", "repeatType": 3,
    #                                                                     "weekDay": 0b00000010,
    #                                                                     "startTime": start_time1,
    #                                                                     "stopTime": start_time1}}]})
    #     self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
    #                                           {"serviceName": "bbb"}, {
    #                                               "out": [{"serviceName": "bbb", "repeatType": 3, "weekDay": 0b00000010,
    #                                                        "rtcTime": start_time2, "timerFlag": "bbb4",
    #                                                        "bookInfo": {"bookType": "3", "repeatType": 3,
    #                                                                     "weekDay": 0b00000010,
    #                                                                     "startTime": start_time2,
    #                                                                     "stopTime": start_time2}}]})
    #     self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyBookInfoList", {"bookInfoList": [  # 通知预约展示信息列表
    #         {"bookType": "3", "repeatType": 3, "weekDay": 0b00000010, "startTime": start_time1,
    #          "stopTime": start_time1},
    #         {"bookType": "3", "repeatType": 3, "weekDay": 0b00000010, "startTime": start_time2,
    #          "stopTime": start_time2}]})
    #     sleep(delta_second1 - 18)
    #     self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyPrepareTimeUpEventInfo",  # 预约的任务开始时间到时提前15s通知
    #                               {"bookEvent": {"serviceName": "aaa",
    #                                              "repeatType": 3,
    #                                              "weekDay": 0b00000010,
    #                                              "rtcTime": start_time1,
    #                                              "timerFlag": "aaa4",
    #                                              "bookInfo": {"bookType": "3",
    #                                                           "repeatType": 3,
    #                                                           "weekDay": 0b00000010,
    #                                                           "startTime": start_time1,
    #                                                           "stopTime": start_time1}}})
    #     sleep(delta_second1 - 1)
    #     self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyTimeUpEventInfo",  # 预约的任务开始时间到时通知
    #                               {"bookEvent": {"serviceName": "aaa",
    #                                              "repeatType": 3,
    #                                              "weekDay": 0b00000010,
    #                                              "rtcTime": start_time1,
    #                                              "timerFlag": "aaa4",
    #                                              "bookInfo": {"bookType": "3",
    #                                                           "repeatType": 3,
    #                                                           "weekDay": 0b00000010,
    #                                                           "startTime": start_time1,
    #                                                           "stopTime": start_time1}}})
    #     sleep(delta_second2 - 18)
    #     self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyPrepareTimeUpEventInfo",  # 预约的任务开始时间到时提前15s通知
    #                               {"bookEvent": {"serviceName": "bbb",
    #                                              "repeatType": 3,
    #                                              "weekDay": 0b00000010,
    #                                              "rtcTime": start_time2,
    #                                              "timerFlag": "bbb4",
    #                                              "bookInfo": {"bookType": "3",
    #                                                           "repeatType": 3,
    #                                                           "weekDay": 0b00000010,
    #                                                           "startTime": start_time2,
    #                                                           "stopTime": start_time2}}}, timeout=3)
    #     sleep(delta_second2 - 1)
    #     self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyTimeUpEventInfo",  # 预约的任务开始时间到时通知
    #                               {"bookEvent": {"serviceName": "bbb",
    #                                              "repeatType": 3,
    #                                              "weekDay": 0b00000010,
    #                                              "rtcTime": start_time2,
    #                                              "timerFlag": "bbb4",
    #                                              "bookInfo": {"bookType": "3",
    #                                                           "repeatType": 3,
    #                                                           "weekDay": 0b00000010,
    #                                                           "startTime": start_time2,
    #                                                           "stopTime": start_time2}
    #                                              }}, timeout=3)
    #     self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",  # 取消预约事件
    #                                           {"timerHandler": timerHandler_config_ifo},
    #                                           {"out": True})
    #     self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",  # 取消预约事件
    #                                           {"timerHandler": timerHandler},
    #                                           {"out": True})

    @allure.title("设置默认时间预约事件_repeatType=3_同进程名不同任务名同时间")
    @pytest.mark.full
    def test_caseid_1978034(self):
        today = datetime.datetime.today()
        _week_day = today.isoweekday()
        logger.info(f"今天是周{_week_day}")
        for k,w in {1:0b00001111, 2:0b00001111, 3:0b00001111, 4:0b00001111, 5:0b01110000, 6:0b01110000, 7:0b01110000}.items():
            if _week_day == k:
                start_time, delta_second = self.getdatetime(2)
                timerHandler_config_ifo = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                                                    {"bookEventInfo": {"serviceName": "aaa",
                                                                                                    # 任务名
                                                                                                    "repeatType": 3,
                                                                                                    "weekDay": w,
                                                                                                    "rtcTime": start_time,
                                                                                                    "timerFlag": "111",

                                                                                                    "bookInfo":
                                                                                                        {"bookType": "1",
                                                                                                            "repeatType": 3,
                                                                                                            "weekDay": w,
                                                                                                            "startTime": start_time + 60,
                                                                                                            "stopTime": start_time + 1000}}})[
                    "out"]
                if timerHandler_config_ifo == "":
                    assert False
                else:
                    timerHandler = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                                            {"bookEventInfo": {"serviceName": "aaa",
                                                                                                # 任务名
                                                                                                "repeatType": 3,
                                                                                                "weekDay": w,
                                                                                                "rtcTime": start_time,
                                                                                                "timerFlag": "222",

                                                                                                "bookInfo":
                                                                                                    {"bookType": "1",
                                                                                                    # 任务类型不同
                                                                                                    "repeatType": 3,
                                                                                                    "weekDay": w,
                                                                                                    "startTime": start_time + 60,
                                                                                                    "stopTime": start_time + 1000}}})[
                        "out"]
                if timerHandler == "":
                    assert False
                else:
                    self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetBookInfoList", {}, {
                        "out": [{"bookType": "1", "repeatType": 3, "weekDay": w, "startTime": start_time + 60,
                                "stopTime": start_time + 1000},
                                {"bookType": "1", "repeatType": 3, "weekDay": w, "startTime": start_time + 60,
                                "stopTime": start_time + 1000}]})
                    self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                        {"serviceName": "aaa"}, {
                                                            "out": [{"serviceName": "aaa",
                                                                    "repeatType": 3,
                                                                    "weekDay": w,
                                                                    "rtcTime": start_time,
                                                                    "timerFlag": "111",
                                                                    "bookInfo": {"bookType": "1",
                                                                                    "repeatType": 3,
                                                                                    "weekDay": w,
                                                                                    "startTime": start_time + 60,
                                                                                    "stopTime": start_time + 1000}},
                                                                    {"serviceName": "aaa",
                                                                    "repeatType": 3,
                                                                    "weekDay": w,
                                                                    "rtcTime": start_time,
                                                                    "timerFlag": "222",
                                                                    "bookInfo": {"bookType": "1",
                                                                                    "repeatType": 3,
                                                                                    "weekDay": w,
                                                                                    "startTime": start_time + 60,
                                                                                    "stopTime": start_time + 1000}}
                                                                    ]})

                    self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyBookInfoList", {"bookInfoList": [
                        {"bookType": "1", "repeatType": 3, "weekDay": w, "startTime": start_time + 60,
                        "stopTime": start_time + 1000},
                        {"bookType": "1", "repeatType": 3, "weekDay": w, "startTime": start_time + 60,
                        "stopTime": start_time + 1000}]})
                    sleep(delta_second - 18)
                    self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyPrepareTimeUpEventInfo",
                                            {"bookEvent": {"serviceName": "aaa",
                                                            "repeatType": 3,
                                                            "weekDay": w,
                                                            "rtcTime": start_time,
                                                            "timerFlag": "111",

                                                            "bookInfo": {"bookType": "1",
                                                                        "repeatType": 3,
                                                                        "weekDay": w,
                                                                        "startTime": start_time + 60,
                                                                        "stopTime": start_time + 1000}
                                                            }}, timeout=3)
                    self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyPrepareTimeUpEventInfo",
                                            {"bookEvent": {"serviceName": "aaa",
                                                            "repeatType": 3,
                                                            "weekDay": w,
                                                            "rtcTime": start_time,
                                                            "timerFlag": "222",

                                                            "bookInfo": {"bookType": "1",
                                                                        "repeatType": 3,
                                                                        "weekDay": w,
                                                                        "startTime": start_time + 60,
                                                                        "stopTime": start_time + 1000}
                                                            }}, timeout=3)

                    sleep(delta_second - 1)
                    self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyTimeUpEventInfo",
                                            {"bookEvent": {"serviceName": "aaa",
                                                            "repeatType": 3,
                                                            "weekDay": w,
                                                            "rtcTime": start_time,
                                                            "timerFlag": "111",

                                                            "bookInfo": {"bookType": "1",
                                                                        "repeatType": 3,
                                                                        "weekDay": w,
                                                                        "startTime": start_time + 60,
                                                                        "stopTime": start_time + 1000}
                                                            }}, timeout=3)
                    self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyTimeUpEventInfo",
                                            {"bookEvent": {"serviceName": "aaa",
                                                            "repeatType": 3,
                                                            "weekDay": w,
                                                            "rtcTime": start_time,
                                                            "timerFlag": "222",

                                                            "bookInfo": {"bookType": "1",
                                                                        "repeatType": 3,
                                                                        "weekDay": w,
                                                                        "startTime": start_time + 60,
                                                                        "stopTime": start_time + 1000}
                                                            }}, timeout=3)
                    self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",
                                                        {"timerHandler": timerHandler_config_ifo},
                                                        {"out": True})
                    self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",
                                                        {"timerHandler": timerHandler},
                                                        {"out": True})

    @allure.title("设置默认时间预约事件_非整分钟_设置不成功")
    @pytest.mark.sanity
    def test_caseid_1978045(self):
        start_time = time.time()
        timerHandler_config_ifo = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",  # 设置预约事件
                                                      {"bookEventInfo": {"serviceName": "aaa",  # 进程名
                                                                         "repeatType": 0,  # 预约事件类型
                                                                         "rtcTime": start_time + 61,
                                                                         "timerFlag": "111",  # 任务名
                                                                         # RTC是否已到时/接口未使用
                                                                         "bookInfo":  # 客户展示信息
                                                                             {"bookType": "1",  # 设置预约事件类型
                                                                              "repeatType": 0,  # 预约事件重复类型
                                                                              "startTime": start_time + 61,
                                                                              # 业务预约时间开始时间
                                                                              "stopTime": start_time + 1000}}})[
                "out"]  # 结束时间
        if timerHandler_config_ifo == "":
            assert True
        else:
            assert False

    @allure.title("设置周时间预约事件_repeatType=3_0b10000000_0b00000000_设置不成功")
    @pytest.mark.sanity
    def test_caseid_1979620(self):
        for i in [0b10000000, 0b00000000]:
            start_time, delta_second = self.getdatetime(2)
            timerHandler_config_ifo = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                                                {"bookEventInfo": {"serviceName": "aaa",
                                                                                                   # 任务名
                                                                                                   "repeatType": 3,
                                                                                                   "weekDay": i,
                                                                                                   "rtcTime": start_time,
                                                                                                   "timerFlag": "111",

                                                                                                   "bookInfo":
                                                                                                       {"bookType": "1",
                                                                                                        "repeatType": 3,
                                                                                                        "weekDay": i,
                                                                                                        "startTime": start_time + 60,
                                                                                                        "stopTime": start_time + 1000}}})[
                "out"]
            if timerHandler_config_ifo == "":
                assert True
            else:
                assert False

    @allure.title("设置默认时间预约事件_repeatType=1_0同一时间预约")
    @pytest.mark.full
    def test_caseid_1978142(self):
        start_time, delta_second = self.getdatetime(2)
        timerHandler_config_ifo = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",  # 设置预约事件
                                                      {"bookEventInfo": {"serviceName": "aaa",  # 进程名
                                                                         "repeatType": 0,  # 预约事件类型
                                                                         "weekDay": 0,
                                                                         "rtcTime": start_time,  # 当前时间+200s业务预约时间
                                                                         "timerFlag": "eatapple4",  # 任务名
                                                                         # RTC是否已到时/接口未使用
                                                                         "bookInfo":  # 客户展示信息
                                                                             {"bookType": "0",  # 设置预约事件类型
                                                                              "weekDay": 0,
                                                                              "repeatType": 0,  # 预约事件重复类型
                                                                              "startTime": start_time + 60,
                                                                              # 业务预约时间开始时间
                                                                              "stopTime": start_time + 1000}}})[
                "out"]  # 结束时间
        timerHandler = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",  # 设置预约事件
                                                                 {"bookEventInfo": {"serviceName": "bbb",  # 进程名
                                                                                    "repeatType": 1,  # 预约事件类型
                                                                                    "weekDay": 0,
                                                                                    "rtcTime": start_time,
                                                                                    # 当前时间+200s业务预约时间
                                                                                    "timerFlag": "eatapple4",  # 任务名
                                                                                    # RTC是否已到时/接口未使用
                                                                                    "bookInfo":  # 客户展示信息
                                                                                        {"bookType": "1",  # 设置预约事件类型
                                                                                         "weekDay": 0,
                                                                                         "repeatType": 1,  # 预约事件重复类型
                                                                                         "startTime": start_time + 60,
                                                                                         # 业务预约时间开始时间
                                                                                         "stopTime": start_time + 1000}}})[
            "out"]  # 结束时间
        if timerHandler_config_ifo == "":  # 判断预约事件是否成功
            assert False
        if timerHandler == "":
            assert False
        else:
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetBookInfoList", {}, {  # 查询服务已预约的事件信息
                "out": [
                    {"bookType": "0", "repeatType": 0, "startTime": start_time + 60, "stopTime": start_time + 1000},
                    {"bookType": "1", "repeatType": 1, "startTime": start_time + 60, "stopTime": start_time + 1000}]})
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                  {"serviceName": "aaa"}, {
                                                      "out": [{"serviceName": "aaa",  # 进程名
                                                               "repeatType": 0,  # 预约事件类型
                                                               "weekDay": 0,
                                                               "rtcTime": start_time,  # 当前时间+200s业务预约时间
                                                               "timerFlag": "eatapple4",  # 任务名
                                                               # RTC是否已到时/接口未使用
                                                               "bookInfo":  # 客户展示信息
                                                                   {"bookType": "0",  # 设置预约事件类型
                                                                    "weekDay": 0,
                                                                    "repeatType": 0,  # 预约事件重复类型
                                                                    "startTime": start_time + 60,
                                                                    # 业务预约时间开始时间
                                                                    "stopTime": start_time + 1000}}]})
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                  {"serviceName": "bbb"}, {
                                                        "out":[{"serviceName": "bbb",  # 进程名
                                                               "repeatType": 1,  # 预约事件类型
                                                               "weekDay": 0,
                                                               "rtcTime": start_time,
                                                               # 当前时间+200s业务预约时间
                                                               "timerFlag": "eatapple4",  # 任务名
                                                               # RTC是否已到时/接口未使用
                                                               "bookInfo":  # 客户展示信息
                                                                   {"bookType": "1",  # 设置预约事件类型
                                                                    "weekDay": 0,
                                                                    "repeatType": 1,  # 预约事件重复类型
                                                                    "startTime": start_time + 60,
                                                                    # 业务预约时间开始时间
                                                                    "stopTime": start_time + 1000}}]})

        self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyBookInfoList", {"bookInfoList": [
            {"bookType": "0", "repeatType": 0, "startTime": start_time + 60, "stopTime": start_time + 1000},
            {"bookType": "1", "repeatType": 1, "startTime": start_time + 60, "stopTime": start_time + 1000}]})
        sleep(delta_second - 18)
        self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyPrepareTimeUpEventInfo",
                                  {"bookEvent": {"serviceName": "aaa",  # 进程名
                                                 "repeatType": 0,  # 预约事件类型
                                                 "weekDay": 0,
                                                 "rtcTime": start_time,  # 当前时间+200s业务预约时间
                                                 "timerFlag": "eatapple4",  # 任务名
                                                 # RTC是否已到时/接口未使用
                                                 "bookInfo":  # 客户展示信息
                                                     {"bookType": "0",  # 设置预约事件类型
                                                      "weekDay": 0,
                                                      "repeatType": 0,  # 预约事件重复类型
                                                      "startTime": start_time + 60,
                                                      # 业务预约时间开始时间
                                                      "stopTime": start_time + 1000}}}, timeout=3)
        self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyPrepareTimeUpEventInfo",
                                  {"bookEvent": {"serviceName": "bbb",  # 进程名
                                                 "repeatType": 1,  # 预约事件类型
                                                 "weekDay": 0,
                                                 "rtcTime": start_time,
                                                 # 当前时间+200s业务预约时间
                                                 "timerFlag": "eatapple4",  # 任务名
                                                 # RTC是否已到时/接口未使用
                                                 "bookInfo":  # 客户展示信息
                                                     {"bookType": "1",  # 设置预约事件类型
                                                      "weekDay": 0,
                                                      "repeatType": 1,  # 预约事件重复类型
                                                      "startTime": start_time + 60,
                                                      # 业务预约时间开始时间
                                                      "stopTime": start_time + 1000}}}, timeout=3)

        sleep(delta_second - 1)
        self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyTimeUpEventInfo",
                                  {"bookEvent": {"serviceName": "aaa",  # 进程名
                                                 "repeatType": 0,  # 预约事件类型
                                                 "weekDay": 0,
                                                 "rtcTime": start_time,  # 当前时间+200s业务预约时间
                                                 "timerFlag": "eatapple4",  # 任务名
                                                 # RTC是否已到时/接口未使用
                                                 "bookInfo":  # 客户展示信息
                                                     {"bookType": "0",  # 设置预约事件类型
                                                      "weekDay": 0,
                                                      "repeatType": 0,  # 预约事件重复类型
                                                      "startTime": start_time + 60,
                                                      # 业务预约时间开始时间
                                                      "stopTime": start_time + 1000}}}, timeout=3)
        self.partner.ck_s2s_event(RTCALARM_SERVICE_CLIENT, "NotifyTimeUpEventInfo",
                                  {"bookEvent": {"serviceName": "bbb",  # 进程名
                                                 "repeatType": 1,  # 预约事件类型
                                                 "weekDay": 0,
                                                 "rtcTime": start_time,
                                                 # 当前时间+200s业务预约时间
                                                 "timerFlag": "eatapple4",  # 任务名
                                                 # RTC是否已到时/接口未使用
                                                 "bookInfo":  # 客户展示信息
                                                     {"bookType": "1",  # 设置预约事件类型
                                                      "weekDay": 0,
                                                      "repeatType": 1,  # 预约事件重复类型
                                                      "startTime": start_time + 60,
                                                      # 业务预约时间开始时间
                                                      "stopTime": start_time + 1000}
                                                 }}, timeout=3)
        self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                  {"serviceName": "bbb"}, {
                                                        "out":[{"serviceName": "bbb",  # 进程名
                                                               "repeatType": 1,  # 预约事件类型
                                                               "weekDay": 0,
                                                               "rtcTime": start_time + 86400,
                                                               # 当前时间+200s业务预约时间
                                                               "timerFlag": "eatapple4",  # 任务名
                                                               # RTC是否已到时/接口未使用
                                                               "bookInfo":  # 客户展示信息
                                                                   {"bookType": "1",  # 设置预约事件类型
                                                                    "weekDay": 0,
                                                                    "repeatType": 1,  # 预约事件重复类型
                                                                    "startTime": start_time + 60 + 86400,
                                                                    # 业务预约时间开始时间
                                                                    "stopTime": start_time + 1000 + 86400}}]})
        self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                  {"serviceName": "aaa"}, {
                                                        "out":[]})
        self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",
                                              {"timerHandler": timerHandler_config_ifo},
                                              {"out": True})
        self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",
                                              {"timerHandler": timerHandler},
                                              {"out": True})
        self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                  {"serviceName": "bbb"}, {
                                                        "out":[]})
        self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                  {"serviceName": "aaa"}, {
                                                        "out":[]})


    @allure.title("设置预约事件_repeatType=1且timerHandler!=timerHandler_config_ifo取消失败") 
    @pytest.mark.full
    def test_caseid_1979623(self):
        start_time, delta_second = self.getdatetime(2)
        timerHandler_config_ifo = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",  # 设置预约事件
                                                      {"bookEventInfo": {"serviceName": "aaa",  # 进程名
                                                                         "repeatType": 1,  # 预约事件类型
                                                                         "weekDay": 0,
                                                                         "rtcTime": start_time,  # 当前时间+200s业务预约时间
                                                                         "timerFlag": "eatapple4",  # 任务名
                                                                         # RTC是否已到时/接口未使用
                                                                         "bookInfo":  # 客户展示信息
                                                                             {"bookType": "0",  # 设置预约事件类型
                                                                              "weekDay": 0,
                                                                              "repeatType": 1,  # 预约事件重复类型
                                                                              "startTime": start_time + 60,
                                                                              # 业务预约时间开始时间
                                                                              "stopTime": start_time + 1000}}})[
                "out"]  # 结束时间
        if timerHandler_config_ifo == "":
            assert False
        else:
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",
                                                    {"timerHandler": " "},
                                                    {"out": True})#当前实现不管是已经取消了还是你要取消的不存在，都是返回true
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",
                                                    {"timerHandler": timerHandler_config_ifo},
                                                    {"out": True})

    @allure.title("设置预约事件_repeatType=1且bookinfo一致")  # todo 如何判断不获取weekday的值
    @pytest.mark.full
    def test_caseid_1979628(self):
        start_time, delta_second = self.getdatetime(2)
        timerHandler_config_ifo = \
            timerHandler_config_ifo = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                                            {"bookEventInfo": {"serviceName": "aaa",
                                                                                               # 任务名
                                                                                               "repeatType": 1,
                                                                                               "weekDay": 0,
                                                                                               "rtcTime": start_time,
                                                                                               "timerFlag": "111",

                                                                                               "bookInfo":
                                                                                                   {"bookType": "1",
                                                                                                    "repeatType": 1,
                                                                                                    "weekDay": 0,
                                                                                                    "startTime": start_time + 60,
                                                                                                    "stopTime": start_time + 1000}}})[
            "out"]
        if timerHandler_config_ifo == "":
            assert False
        else:
            timerHandler = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",
                                                                     {"bookEventInfo": {"serviceName": "bbb",
                                                                                               # 任务名
                                                                                               "repeatType": 1,
                                                                                               "weekDay": 0,
                                                                                               "rtcTime": start_time,
                                                                                               "timerFlag": "111",

                                                                                               "bookInfo":
                                                                                                   {"bookType": "1",
                                                                                                    "repeatType": 1,
                                                                                                    "weekDay": 0,
                                                                                                    "startTime": start_time + 60,
                                                                                                    "stopTime": start_time + 1000}}})[
                "out"]
        if timerHandler == "":
            assert False
        else:
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",
                                                    {"timerHandler": timerHandler},
                                                    {"out": True})
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",
                                                    {"timerHandler": timerHandler_config_ifo},
                                                    {"out": True})

# @allure.title("设置每天时间预约事件_repeatType")
# @allure.testcase('https://jama.jiduauto.com/perspective.req#/items/1252331?projectId=46')
# @pytest.mark.full
# def test_caseid_11111111(self):
#     start_time = self.getdatetime()
#     timerHandler_config_ifo = \
#         self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",  # 设置预约事件
#                                                   {"bookEventInfo": {"serviceName": "eat4",  # 进程名
#                                                                      "repeatType": 1,  # 预约事件类型
#                                                                      "rtcTime": start_time + 60,  # 当前时间+200s业务预约时间
#                                                                      "timerFlag": "eatapple4",  # 任务名
#                                                                      # RTC是否已到时/接口未使用
#                                                                      "bookInfo":  # 客户展示信息
#                                                                          {"bookType": "1",  # 设置预约事件类型
#                                                                           "repeatType": 1,  # 预约事件重复类型
#                                                                           "startTime": start_time + 60,
#                                                                           # 业务预约时间开始时间
#                                                                           "stopTime": start_time + 1000}}})[
#             "out"]  # 结束时间
#     if timerHandler_config_ifo == "":
#         assert False
#     else:
#         data = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
#                                                          {"serviceName": "eat4"})
#         logger.info(timerHandler_config_ifo)  # 读取set接口返回的timerHandler
#         logger.info(data["out"])  # 读取get接口返回的out
#         for a in data["out"]:
#             logger.info(a["timerHandler"])  # 拿出timerHandler
#             if timerHandler_config_ifo == a["timerHandler"]:  # 当set的timerHandler==get的timerHandler
#                 assert True
#             else:
#                 assert False
#         sleep(65)
#         data1 = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
#                                                           {"serviceName": "eat4"})
#         for i in data1["out"]:  # 拿出事后get的out
#             print(i["rtcTime"], i["bookInfo"]["startTime"], i["bookInfo"]["stopTime"])
#             for a in data["out"]:  # 拿出事前get的out
#                 print(a["rtcTime"], a["bookInfo"]["startTime"], a["bookInfo"]["stopTime"])
#                 if i["rtcTime"] - a["rtcTime"] == 86400 and i["bookInfo"]["startTime"] - a["bookInfo"][
#                     "startTime"] == 86400 and i["bookInfo"]["stopTime"] - a["bookInfo"][
#                     "stopTime"] == 86400:  # 如果事后的rtcTime,startTime,stopTime各自相减事前的都等于86400s就说明已经到达第二次事件
#                     assert True
#                 else:
#                     assert False
#     self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",
#                                           {"timerHandler": timerHandler_config_ifo},
#                                           {"out": True})
#     data2 = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
#                                                       {"serviceName": "eat4"})
#     if not len(data2["out"]):  # 如果事件取消以后重新get,out为空说明取消成功
#         assert True
#     else:
#         assert False
#
    @allure.title("取消台架中的所有预约事件")
    @allure.testcase('https://jama.jiduauto.com/perspective.req#/items/1960043?projectId=46')
    @pytest.mark.full
    def test_caseid_10191721(self):
        data = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                        {"serviceName": "bbb4"})  # 填上serviceName进程名
        logger.info(data["out"])
        for i in data["out"]:
            logger.info(i["timerHandler"])
            print(i["timerHandler"])
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "CancelBookEvent",
                                                {"timerHandler": f"{i['timerHandler']}"},
                                                {"out": True})
        # self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
        #                                           {"serviceName": "aaa"})
    @allure.title("取消业务设置的所有预约事件_repeatType=0_1_3_取消不存在事件")
    @pytest.mark.sanity
    def test_caseid_1985563(self):
        start_time, delta_second = self.getdatetime(2)
        timerHandler_zone = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",  # 设置预约事件
                                                      {"bookEventInfo": {"serviceName": "aaa",  # 进程名
                                                                         "repeatType": 0,  # 预约事件类型
                                                                         "weekDay": 0,
                                                                         "rtcTime": start_time,  # 当前时间+200s业务预约时间
                                                                         "timerFlag": "zone",  # 任务名
                                                                         # RTC是否已到时/接口未使用
                                                                         "bookInfo":  # 客户展示信息
                                                                             {"bookType": "0",  # 设置预约事件类型
                                                                              "weekDay": 0,
                                                                              "repeatType": 0,  # 预约事件重复类型
                                                                              "startTime": start_time + 60,
                                                                              # 业务预约时间开始时间
                                                                              "stopTime": start_time + 1000}}})[
                "out"]  # 结束时间
        timerHandler_one = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",  # 设置预约事件
                                                                 {"bookEventInfo": {"serviceName": "aaa",  # 进程名
                                                                                    "repeatType": 1,  # 预约事件类型
                                                                                    "weekDay": 0,
                                                                                    "rtcTime": start_time,
                                                                                    # 当前时间+200s业务预约时间
                                                                                    "timerFlag": "one",  # 任务名
                                                                                    # RTC是否已到时/接口未使用
                                                                                    "bookInfo":  # 客户展示信息
                                                                                        {"bookType": "1",  # 设置预约事件类型
                                                                                         "weekDay": 0,
                                                                                         "repeatType": 1,  # 预约事件重复类型
                                                                                         "startTime": start_time + 60,
                                                                                         # 业务预约时间开始时间
                                                                                         "stopTime": start_time + 1000}}})[
            "out"]  # 结束时间                                                                                  
        timerHandler_two = self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",  # 设置预约事件
                                                                 {"bookEventInfo": {"serviceName": "aaa",  # 进程名
                                                                                    "repeatType": 3,  # 预约事件类型
                                                                                    "weekDay": 0b01111111,
                                                                                    "rtcTime": start_time,
                                                                                    # 当前时间+200s业务预约时间
                                                                                    "timerFlag": "two",  # 任务名
                                                                                    # RTC是否已到时/接口未使用
                                                                                    "bookInfo":  # 客户展示信息
                                                                                        {"bookType": "3",  # 设置预约事件类型
                                                                                         "weekDay": 0b01111111,
                                                                                         "repeatType": 3,  # 预约事件重复类型
                                                                                         "startTime": start_time + 60,
                                                                                         # 业务预约时间开始时间
                                                                                         "stopTime": start_time + 1000}}})[
            "out"]  # 结束时间
        timerHandler_ccc = \
            self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT, "SetBookEvent",  # 设置预约事件
                                                      {"bookEventInfo": {"serviceName": "ccc",  # 进程名
                                                                         "repeatType": 0,  # 预约事件类型
                                                                         "weekDay": 0,
                                                                         "rtcTime": start_time,  # 当前时间+200s业务预约时间
                                                                         "timerFlag": "jiaoyan",  # 任务名
                                                                         # RTC是否已到时/接口未使用
                                                                         "bookInfo":  # 客户展示信息
                                                                             {"bookType": "0",  # 设置预约事件类型
                                                                              "weekDay": 0,
                                                                              "repeatType": 0,  # 预约事件重复类型
                                                                              "startTime": start_time + 60,
                                                                              # 业务预约时间开始时间
                                                                              "stopTime": start_time + 1000}}})[
                "out"]  # 结束时间
        if timerHandler_zone == "":  # 判断预约事件是否成功
            assert False
        if timerHandler_one== "":
            assert False
        if timerHandler_two== "":
            assert False
        if timerHandler_ccc== "":
            assert False
        else:
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                  {"serviceName": "aaa"}, {
                                                      "out": [{"serviceName": "aaa",  # 进程名
                                                                         "repeatType": 0,  # 预约事件类型
                                                                         "weekDay": 0,
                                                                         "rtcTime": start_time,  # 当前时间+200s业务预约时间
                                                                         "timerFlag": "zone",  # 任务名
                                                                         # RTC是否已到时/接口未使用
                                                                         "bookInfo":  # 客户展示信息
                                                                             {"bookType": "0",  # 设置预约事件类型
                                                                              "weekDay": 0,
                                                                              "repeatType": 0,  # 预约事件重复类型
                                                                              "startTime": start_time + 60,
                                                                              # 业务预约时间开始时间
                                                                              "stopTime": start_time + 1000}},
                                                              {"serviceName": "aaa",  # 进程名
                                                                                    "repeatType": 1,  # 预约事件类型
                                                                                    "weekDay": 0,
                                                                                    "rtcTime": start_time,
                                                                                    # 当前时间+200s业务预约时间
                                                                                    "timerFlag": "one",  # 任务名
                                                                                    # RTC是否已到时/接口未使用
                                                                                    "bookInfo":  # 客户展示信息
                                                                                        {"bookType": "1",  # 设置预约事件类型
                                                                                         "weekDay": 0,
                                                                                         "repeatType": 1,  # 预约事件重复类型
                                                                                         "startTime": start_time + 60,
                                                                                         # 业务预约时间开始时间
                                                                                         "stopTime": start_time + 1000}},
                                                              {"serviceName": "aaa",  # 进程名
                                                                                    "repeatType": 3,  # 预约事件类型
                                                                                    "weekDay": 0b01111111,
                                                                                    "rtcTime": start_time,
                                                                                    # 当前时间+200s业务预约时间
                                                                                    "timerFlag": "two",  # 任务名
                                                                                    # RTC是否已到时/接口未使用
                                                                                    "bookInfo":  # 客户展示信息
                                                                                        {"bookType": "3",  # 设置预约事件类型
                                                                                         "weekDay": 0b01111111,
                                                                                         "repeatType": 3,  # 预约事件重复类型
                                                                                         "startTime": start_time + 60,
                                                                                         # 业务预约时间开始时间
                                                                                         "stopTime": start_time + 1000}}]})
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                  {"serviceName": "ccc"}, {
                                                      "out": [{"serviceName": "ccc",  # 进程名
                                                               "repeatType": 0,  # 预约事件类型
                                                               "weekDay": 0,
                                                               "rtcTime": start_time,  # 当前时间+200s业务预约时间
                                                               "timerFlag": "jiaoyan",  # 任务名
                                                               # RTC是否已到时/接口未使用
                                                               "bookInfo":  # 客户展示信息
                                                                   {"bookType": "0",  # 设置预约事件类型
                                                                    "weekDay": 0,
                                                                    "repeatType": 0,  # 预约事件重复类型
                                                                    "startTime": start_time + 60,
                                                                    # 业务预约时间开始时间
                                                                    "stopTime": start_time + 1000}}]})
            bool_true=self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT,"CancelServiceBookEvent",
                                                            {"serviceName":"aaa"})["out"]
            bool_false=self.partner.send_request_and_return_resp(RTCALARM_SERVICE_CLIENT,"CancelServiceBookEvent",
                                                            {"serviceName":"bbb"})["out"]
            if bool_true == "true":
                assert False
            if bool_false =="true":
                assert False
            self.partner.send_request_and_ck_resp(RTCALARM_SERVICE_CLIENT, "GetRtcEventInfoList",
                                                  {"serviceName": "ccc"}, {
                                                      "out": [{"serviceName": "ccc",  # 进程名
                                                               "repeatType": 0,  # 预约事件类型
                                                               "weekDay": 0,
                                                               "rtcTime": start_time,  # 当前时间+200s业务预约时间
                                                               "timerFlag": "jiaoyan",  # 任务名
                                                               # RTC是否已到时/接口未使用
                                                               "bookInfo":  # 客户展示信息
                                                                   {"bookType": "0",  # 设置预约事件类型
                                                                    "weekDay": 0,
                                                                    "repeatType": 0,  # 预约事件重复类型
                                                                    "startTime": start_time + 60,
                                                                    # 业务预约时间开始时间
                                                                    "stopTime": start_time + 1000}}]})