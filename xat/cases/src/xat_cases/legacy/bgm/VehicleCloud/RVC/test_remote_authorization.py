#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import time
import pytest
import allure
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), ".."))
sys.path.append(os.path.join(os.getcwd(), "../.."))
sys.path.append(os.path.join(os.getcwd(), "../../.."))
from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("远程控制/远控两域联调测试/远程启动")
@allure.story("远程启动")
class TestRemoteAuthorization(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["CentralLockService_client","VehicleModeService_client","VehicleSetStatusService_client","KeyService_client","DoorService_client","RemoteCtrlService_client"])
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,
                                       vehmtnst=VehMtnSts.StandStillVal2)
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        sleep(3)

    def before_each_func(self, ecu):
        pass

    def after_each_func(self, ecu):
        self.bus_comm.clear_all_bus_buffer()
        self.soa.set_maintenanceMode(maintenanceMode=False)
        self.mix.set_common_precontion(usage_mode=UsageMode.INACTIVE,
                                       vehmtnst=VehMtnSts.StandStillVal2)
        self.mix.set_all_seats_present_sts(seat_pres_sts=SeatPresSts.NoPres)
        self.io.set_five_door_sts(Door.close)
        sleep(3)

    def after_class(self, ecu):
        pass
    

    @allure.title("RVC_远控启动_ABANDONED")
    @pytest.mark.smoke
    def test_authorization_caseid_1991505(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.io.set_five_door_sts(Door.open)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("RVC_远控启动_INACTIVE")
    @pytest.mark.smoke
    def test_authorization_caseid_1991504(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.io.set_five_door_sts(Door.open)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("RVC_远控启动_CONVENIENCE")
    @pytest.mark.smoke
    def test_authorization_caseid_1991503(self, ecu):
        self.mix.set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_remote_authorization()
        self.io.set_five_door_sts(Door.open)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("RVC_取消远控启动_远控闭锁")
    @pytest.mark.smoke
    def test_authorization_caseid_1991502(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Telm)
        assert self.tsp.log_search_remote_vehicle_control("AuthEsc",execid=execid)

    @allure.title("RVC_取消远控启动_重上锁")
    @pytest.mark.sanity
    def test_authorization_caseid_1991500(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.Telm)
        assert self.tsp.log_search_remote_vehicle_control("AuthEsc",execid=execid)

    @allure.title("RVC_取消远控启动_NFC闭锁")
    @pytest.mark.sanity
    def test_authorization_caseid_1991499(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.mix.ctrl_lock(lock_type=LockCmd.Lock, ctrl_type=LockSource.NFC)
        assert self.tsp.log_search_remote_vehicle_control("AuthEsc",execid=execid)

    @allure.title("RVC_自动远程授权启动_门开")
    @pytest.mark.sanity
    def test_authorization_caseid_1991498(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.io.set_five_door_sts(Door.open)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("RVC_自动远程授权启动_主驾占座")
    @pytest.mark.smoke
    def test_authorization_caseid_1991497(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.io.driver_seat_present()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("RVC_自动远程授权启动_刹车踏板")
    @pytest.mark.sanity
    def test_authorization_caseid_1991496(self, ecu):
        execid = self.tsp.rvc_remote_authorization()
        self.bus_comm.set_brake_pedal_sts()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)

    @allure.title("RVC_取消远控启动_蓝牙闭锁")
    @pytest.mark.sanity
    def test_authorization_caseid_1991501(self, ecu):
        self.soa.hmi_set_door_close_lock(lock_cmd=LockCmd.Lock, source=LockSource.RKE)
        self.bus_comm.check_central_lock_sts(exp_sts=CenLockSts.Lock, exp_trigsrc=LockTrigerSource.KeyRem)
        execid = self.tsp.rvc_remote_authorization()
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid)