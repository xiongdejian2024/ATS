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
        self.mix.network_wakeup()
        sleep(1)
            

    def after_class(self, ecu):
        pass


    @allure.title("远程控制-RVC_ReadyEntry状态_异常掉电复归_取消授权条件满足")
    @pytest.mark.long_time
    @pytest.mark.repeat(100)
    def test_authorization_caseid_1982810(self):
        execid = self.tsp.rvc_remote_authorization()
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('StartOK',flage=0,execid=execid)
        time.sleep(120)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('TimerAuthDelayFail',flage=1,execid=execid)
        self.tsp.check_async_log_search_result_from_remote_vehicle_control('AuthEscLockSuccess', flage=2,execid=execid)


    @allure.title("远程控制-RVC_远程授权_休眠唤醒压测100次")
    @pytest.mark.long_time
    @pytest.mark.repeat(100)
    def test_authorization_caseid_1982811(self):
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
