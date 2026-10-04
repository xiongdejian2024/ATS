#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import pytest
import allure
import random
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("TCAM性能稳定性/业务稳定性/远程控制/远程授权")
@allure.story("远程授权")
class TestRemoteAuthorization(TestABCBase):
    def before_class(self, ecu):
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])

    def before_each_func(self, ecu):
        # 自动授权条件不满足
        self.io.set_door(*[Door.close for _ in range(5)])
        self.bus_comm.set_seat_occpt_sts(SeatId.FrontLeft, SeatOccptSts.Empty)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        # 取消授权条件不满足
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.InsOth)

    
    def after_each_func(self, ecu):
        # 自动授权条件不满足
        self.io.set_door(*[Door.close for _ in range(5)])
        self.bus_comm.set_seat_occpt_sts(SeatId.FrontLeft, SeatOccptSts.Empty)
        self.bus_comm.set_brake_pedal(sts=YesOrNo.No)
        # 取消授权条件不满足
        self.mix.ctrl_lock(LockCmd.Lock, LockSource.NFC)
        self.mix.network_wakeup(Wakeup_Reasons.WAKEUP_BY_ACTIVATION_LINE)
        sleep(1)
            

    def after_class(self, ecu):
        pass


    @allure.title("远程控制-RVC_远程授权_abandoned两域联调")
    @pytest.mark.join_smoke
    def test_authorization_caseid_1982806(self):
        self.mix.network_sleep()
        execid = self.tsp.rvc_remote_authorization()
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('StartOK',flage=0,execid=execid)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC23,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC27,signal_value=NMSts.valid,timeout=30)
        sleep(1)
        self.io.set_door(Door.open,Door.close,Door.close,Door.close,Door.close)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control(flage=2,execid=execid)

    @allure.title("远程控制-RVC_远程授权_inactive两域联调")
    @pytest.mark.join_smoke
    def test_authorization_caseid_1982805(self):
        self.mix.set_usage_mode(UsageMode.INACTIVE)
        execid = self.tsp.rvc_remote_authorization()
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('StartOK',flage=0,execid=execid)
        sleep(1)
        self.io.set_door(Door.open,Door.close,Door.close,Door.close,Door.close)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control(flage=2,execid=execid)


    @allure.title("远程控制-RVC_远程授权_convience两域联调")
    @pytest.mark.join_smoke
    def test_authorization_caseid_1982804(self):
        self.mix.set_usage_mode(UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_remote_authorization()
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('StartOK',flage=0,execid=execid)
        sleep(1)
        self.io.set_door(Door.open,Door.close,Door.close,Door.close,Door.close)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control(flage=2,execid=execid)
        self.mix.set_usage_mode(UsageMode.INACTIVE)