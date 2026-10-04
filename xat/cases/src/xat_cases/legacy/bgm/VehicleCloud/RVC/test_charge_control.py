#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import threading
import pytest
import allure

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *
from xat_ecu.api.common import *

@allure.feature("远程控制/远控两域联调测试/远程充电口盖")
@allure.story("远程充电口盖")
class TestChargeControl(TestABCBase):
    def before_class(self, ecu):
        self.sd_tester.write_multi_ccp({578:0x4, 973:0}) 
        self.soa.update(["ChargeLidService_client","VehicleSetStatusService_client"])
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        
        sleep(5)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.bus_comm.set_chrglid_pos(0)
        # self.soa.set_tcam_rvc_common_preconditions()
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.mix.set_common_precontion(car_mode=CarMode.NORMAL)
        self.bus_comm.set_vehmtn(VehMtnSts.StandStillVal2)
        time.sleep(1)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        
    def after_each_func(self, ecu):
        pass

    def after_class(self, ecu):
        pass

    @allure.title("RVCChargeCover_Opened_success")
    @pytest.mark.smoke
    def test_caseid_1984907(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_charge_Lidgate()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)

    @allure.title("RVCChargeCover_Closed_abandoned")
    @pytest.mark.smoke
    def test_caseid_1984908(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.tsp.rvc_charge_Lidgate(-1)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)

    @allure.title("RVCChargeCover_Opened_Normal")
    @pytest.mark.smoke
    def test_caseid_1984909(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_charge_Lidgate()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)

    @allure.title("RVCChargeCover_Closed_success")
    @pytest.mark.smoke
    def test_caseid_1984906(self):
        self.sd_tester.change_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.tsp.rvc_charge_Lidgate(-1)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Close)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        self.bus_comm.set_chrglid_pos(0)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Close)

    @allure.title("远控直流电充电口盖开_Success_充电枪未连接")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1990915(self):
        self.tsp.rvc_charge_Lidgate()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)

    @allure.title("远控交流电充电口盖开_Success_充电枪未连接")
    @pytest.mark.smoke
    @pytest.mark.v210
    def test_caseid_1990913(self):
        self.sd_tester.write_multi_ccp({973:2})
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.Disconnected)
        sleep(1)
        self.tsp.rvc_charge_Lidgate()
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Open)
        self.bus_comm.check_chrgild_req(req=ChrgLidReq.Idle)
        self.bus_comm.set_chrglid_pos(100)
        self.bus_comm.check_chrgild_sts(sts=ChrgLidOpenCloseSts.Open)

    @allure.title("远控直流电充电口盖关_Fail_充电枪连接")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1990914(self):
        self.bus_comm.set_dc_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        assert self.tsp.log_search_remote_vehicle_control("PluggerConnected",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远控交流电充电口盖关_Fail_充电枪连接")
    @pytest.mark.sanity
    @pytest.mark.v210
    def test_caseid_1990912(self):
        self.sd_tester.write_multi_ccp({973:2}) 
        self.bus_comm.set_onbd_chrg_handle_sts(sts=DCChrgnHndlSts.ConnectedWithPower)
        sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        assert self.tsp.log_search_remote_vehicle_control("PluggerConnected",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
