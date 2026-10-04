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

@allure.feature("互联服务/远程控制/远程充电口盖")
@allure.story("远程充电口盖")
class TestChargeLidCtrl(TestABCBase):
    def before_class(self, ecu):
        self.soa.update(["HighVoltageService_server","VehicleModeService_server", "FotaMasterService_server",
                    "VehicleSetStatusService_server", "ChassisService_server", 
                    "VehicleTimeService_server",  "SeatService_server", "ChargeLidService_server"])
        sleep(5)

    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.notify_ChargingInfo(isConnect=False)
        time.sleep(1)
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        
    def after_each_func(self, ecu):
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(10)
        self.io.tcam_kl15_up()
        self.bus_comm.resume_all_bus_send()
        time.sleep(1)

    def after_class(self, ecu):
        pass

    @allure.title("远程控制-RVC_远控控制充电口盖_开_ABANDONED")
    @pytest.mark.smoke
    def test_open_ChargeLid_ABANDONED_caseid_1980631(self):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        time.sleep(60)
        self.mix.tcam_network_sleep()
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.check_PNC_thread_start(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        execid = self.tsp.rvc_charge_Lidgate() 
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.check_ChargeLidService_Open_req(timeout=15)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,timeout=1)
        self.bus_comm.check_PNC_thread_stop(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,timeout=1)


    @allure.title("远程控制-RVC_远控控制充电口盖_开_INACTIVE")
    @pytest.mark.smoke
    def test_open_ChargeLid_INACTIVE_caseid_1980626(self):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_ Convenience")
    @pytest.mark.smoke
    def test_open_ChargeLid_caseid_1980625(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_ACTIVE")
    @pytest.mark.smoke
    def test_open_ChargeLid_caseid_1980624(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_ Driving和GearP")
    @pytest.mark.smoke
    def test_open_ChargeLid_caseid_1980622(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_关_ABANDONED")
    @pytest.mark.smoke
    def test_close_ChargeLid_caseid_1980576(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.io.tcam_kl15_down()
        self.bus_comm.pause_all_bus_send()
        time.sleep(60)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC17,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.resume_all_bus_send()
        self.soa.check_ChargeLidService_Close_req(timeout=15)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
                        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_INACTIVE")
    @pytest.mark.smoke
    def test_close_ChargeLid_caseid_1980575(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        execid = self.tsp.rvc_charge_Lidgate(-1)
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_关_ Convenience")
    @pytest.mark.smoke
    def test_close_ChargeLid_caseid_1980574(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_关_Active")
    @pytest.mark.smoke
    def test_close_ChargeLid_caseid_1980573(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_关_Driving和GearP")
    @pytest.mark.smoke
    def test_close_ChargeLid_caseid_1980571(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_FOTA为Query")
    @pytest.mark.sanity
    def test_open_ChargeLid_FOTA_Query_caseid_1980611(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_FOTA为NewTask")
    @pytest.mark.sanity
    def test_open_ChargeLid_FOTA_NewTask_caseid_1980610(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_open_ChargeLid_FOTA_Downloadingk_caseid_1980609(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_FOTA为Active")
    @pytest.mark.sanity
    def test_open_ChargeLid_FOTA_Active_caseid_1980608(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_open_ChargeLid_FOTA_UpdateFailedNotDriving_caseid_1980607(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)   
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开启二次远程控制充电口盖开")
    @pytest.mark.full
    def test_open_ChargeLid_two_open_caseid_1980635(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()
        execid2 = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid2),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_FOTA为Query")
    @pytest.mark.sanity
    def test_close_ChargeLid_FOTA_Query_caseid_1980560(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_FOTA为NewTask")
    @pytest.mark.sanity
    def test_close_ChargeLid_FOTA_NewTask_caseid_1980559(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_FOTA为Downloadingk")
    @pytest.mark.sanity
    def test_close_ChargeLid_FOTA_Downloadingk_caseid_1980558(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_FOTA为Active")
    @pytest.mark.sanity
    def test_close_ChargeLid_FOTA_Active_caseid_1980557(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_关_FOTA为UpdateFailedNotDriving")
    @pytest.mark.sanity
    def test_close_ChargeLid_FOTA_UpdateFailedNotDriving_caseid_1980556(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)   
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_关_Status==kClosing")
    @pytest.mark.sanity
    def test_close_ChargeLid_Status_kClosing_caseid_1980550(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosing)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_TRANSPORT")
    @pytest.mark.full
    def test_open_ChargeLid_CarMode_TRANSPORT_caseid_1980630(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_FACTORY")
    @pytest.mark.full
    def test_open_ChargeLid_CarMode_FACTORY_caseid_1980629(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控控制充电口盖_开_CRASH")
    @pytest.mark.full
    def test_open_ChargeLid_CarMode_CRASH_caseid_1980628(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控控制充电口盖_开_DYNO")
    @pytest.mark.full
    def test_open_ChargeLid_CarMode_DYNO_caseid_1980627(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控控制充电口盖_开_Driving")
    @pytest.mark.full
    def test_open_ChargeLid_UsageMode_DRIVING_caseid_1980623(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_Driving和GearR")
    @pytest.mark.full
    def test_open_ChargeLid_Gear_Rvs_UsageMode_DRIVING_caseid_1980621(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控控制充电口盖_开_Driving和GearN")
    @pytest.mark.full
    def test_open_ChargeLid_Gear_Neut_UsageMode_DRIVING_caseid_1980620(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_Driving和GearD")
    @pytest.mark.full
    def test_open_ChargeLid_Gear_Drv_UsageMode_DRIVING_caseid_1980619(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_Driving和GearM")
    @pytest.mark.full
    def test_open_ChargeLid_Gear_ManMode_UsageMode_DRIVING_caseid_1980618(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程控制-RVC_远控控制充电口盖_开_Convenience和GearR")
    @pytest.mark.sanity
    def test_open_ChargeLid_Gear_Rvs_UsageMode_CONVENIENCE_caseid_1980617(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_Active和GearR")
    @pytest.mark.full
    def test_open_ChargeLid_Gear_Rvs_UsageMode_Active_caseid_1980616(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_维修模式True")
    @pytest.mark.full
    def test_open_ChargeLid_mntnmode_True_caseid_1980615(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_open_ChargeLid_Gear_Rvs_UsageMode_Active_caseid_1980614(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远控控制充电口盖_开_FOTA为UPDATE")
    @pytest.mark.full
    def test_open_ChargeLid_FOTA_UPDATE_caseid_1980613(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_open_ChargeLid_FOTA_ROLLBACK_caseid_1980612(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
                                                                                 
    @allure.title("远程控制-RVC_远控控制充电口盖_开_充电枪StatusConnectedWithoutPower")
    @pytest.mark.full
    def test_open_ChargeLid_PluggerSts_ConnectedWithoutPower_caseid_1980606(self, ecu):
        self.soa.notify_ChargingInfo(plug_sts=PluggerSts.ConnectedWithoutPower,isConnect=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("PluggerConnected",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远控控制充电口盖_开_充电枪StatusPowerAvailableButNotActivated")
    @pytest.mark.full
    def test_open_ChargeLid_PluggerSts_PowerAvailableButNotActivated_caseid_1980605(self, ecu):
        self.soa.notify_ChargingInfo(plug_sts=PluggerSts.PowerAvailableButNotActivated,isConnect=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("PluggerConnected",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_充电枪StatusInit")
    @pytest.mark.full
    def test_open_ChargeLid_PluggerSts_ConnectedWithoutPower_caseid_1980604(self, ecu):
        self.soa.notify_ChargingInfo(plug_sts=PluggerSts.Init,isConnect=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("PluggerConnected",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"           
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_充电枪StatusFault")
    @pytest.mark.full
    def test_open_ChargeLid_PluggerSts_Fault_caseid_1980603(self, ecu):
        self.soa.notify_ChargingInfo(plug_sts=PluggerSts.Fault,isConnect=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        assert self.tsp.log_search_remote_vehicle_control("PluggerConnected",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"           

    @allure.title("远程控制-RVC_远控控制充电口盖_开_Status==kClosing")
    @pytest.mark.full
    def test_open_ChargeLid_Status_kClosing_caseid_1980601(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosing)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_Status==kUnlocked")
    @pytest.mark.sanity
    def test_open_ChargeLid_Status_kUnlocked_caseid_1980600(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kUnlocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_Status==kOpening")
    @pytest.mark.sanity
    def test_open_ChargeLid_Status_kOpening_caseid_1980599(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(10)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpening)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_Status==kHover")
    @pytest.mark.sanity
    def test_open_ChargeLid_Status_kHover_caseid_1980598(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(10)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

        
    @allure.title("远程控制-RVC_远控控制充电口盖_开_Status==kLocked")
    @pytest.mark.full
    def test_open_ChargeLid_ChargeLidSts_kLocked_caseid_1980597(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kLocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_Status==kClosing")
    @pytest.mark.full
    def test_open_ChargeLid_ChargeLidSts_kClosing_caseid_1980596(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosing)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_Status==kNA")
    @pytest.mark.full
    def test_open_ChargeLid_ChargeLidSts_kNA_caseid_1980595(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kNA)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远控控制充电口盖_开_Status==kClosed")
    @pytest.mark.full
    def test_open_ChargeLid_ChargeLidSts_kClosed_caseid_1980594(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程控制-RVC_远控控制充电口盖_开_超时和Status==kOpened")
    @pytest.mark.full
    def test_open_ChargeLid_ChargeLidSts_timeout_kOpened_caseid_1980593(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        time.sleep(11)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_超时和Status==kClosed")
    @pytest.mark.full
    def test_open_ChargeLid_ChargeLidSts_timeout_kClosed_caseid_1980592(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        time.sleep(11)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_开_超时和Status==kOpening")
    @pytest.mark.full
    def test_open_ChargeLid_ChargeLidSts_timeout_kOpening_caseid_1980591(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        time.sleep(11)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpening)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("RVC_远控控制充电口盖_开_超时和Status==kNA")
    @pytest.mark.full
    def test_open_ChargeLid_ChargeLidSts_timeout_kNA_caseid_1980590(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate()   
        self.soa.check_ChargeLidService_Open_req(timeout=10)
        time.sleep(11)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kNA)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控控制充电口盖_开启二次远程控制充电口盖关")
    @pytest.mark.full
    def test_open_ChargeLid_two_close_caseid_1980584(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(-1)   
        execid2 = self.tsp.rvc_charge_Lidgate(-1)   
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid2),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("远程控制-RVC_远控控制充电口盖_关_TRANSPORT")
    @pytest.mark.full
    def test_close_ChargeLid_CarMode_TRANSPORT_caseid_1980580(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_FACTORY")
    @pytest.mark.full
    def test_close_ChargeLid_CarMode_FACTORY_caseid_1980579(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控控制充电口盖_关_CRASH")
    @pytest.mark.full
    def test_close_ChargeLid_CarMode_CRASH_caseid_1980578(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控控制充电口盖_关_DYNO")
    @pytest.mark.full
    def test_close_ChargeLid_CarMode_DYNO_caseid_1980577(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控控制充电口盖_关_Driving")
    @pytest.mark.full
    def test_close_ChargeLid_UsageMode_DRIVING_caseid_1980572(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_Driving和GearR")
    @pytest.mark.full
    def test_close_ChargeLid_Gear_Rvs_UsageMode_DRIVING_caseid_1980570(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控控制充电口盖_关_Driving和GearN")
    @pytest.mark.full
    def test_close_ChargeLid_Gear_Neut_UsageMode_DRIVING_caseid_1980569(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_Driving和GearD")
    @pytest.mark.full
    def test_close_ChargeLid_Gear_Drv_UsageMode_DRIVING_caseid_1980568(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"       
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_Driving和GearM")
    @pytest.mark.full
    def test_close_ChargeLid_Gear_ManMode_UsageMode_DRIVING_caseid_1980567(self, ecu):
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"      

    @allure.title("远程控制-RVC_远控控制充电口盖_关_Convenience和GearR")
    @pytest.mark.sanity
    def test_close_ChargeLid_Gear_Rvs_UsageMode_Convenience_caseid_1980566(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_Active和GearR")
    @pytest.mark.sanity
    def test_close_ChargeLid_Gear_Rvs_UsageMode_Active_caseid_1980565(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_维修模式True")
    @pytest.mark.full
    def test_close_ChargeLid_mntnmode_True_caseid_1980564(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_维修模式True和FOTA为UPDATE")
    @pytest.mark.full
    def test_close_ChargeLid_Gear_Rvs_UsageMode_Active_caseid_1980563(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远控控制充电口盖_关_FOTA为UPDATE")
    @pytest.mark.full
    def test_close_ChargeLid_FOTA_UPDATE_caseid_1980562(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_FOTA为ROLLBACK")
    @pytest.mark.full
    def test_close_ChargeLid_FOTA_ROLLBACK_caseid_1980561(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
                                                                                 
    @allure.title("远程控制-RVC_远控控制充电口盖_关_充电枪StatusConnectedWithoutPower")
    @pytest.mark.full
    def test_close_ChargeLid_PluggerSts_ConnectedWithoutPower_caseid_1980555(self, ecu):
        self.soa.notify_ChargingInfo(plug_sts=PluggerSts.ConnectedWithoutPower,isConnect=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("PluggerConnected",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远控控制充电口盖_关_充电枪StatusPowerAvailableButNotActivated")
    @pytest.mark.full
    def test_close_ChargeLid_PluggerSts_PowerAvailableButNotActivated_caseid_1980554(self, ecu):
        self.soa.notify_ChargingInfo(plug_sts=PluggerSts.PowerAvailableButNotActivated,isConnect=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("PluggerConnected",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_充电枪StatusInit")
    @pytest.mark.full
    def test_close_ChargeLid_PluggerSts_ConnectedWithoutPower_caseid_1980553(self, ecu):
        self.soa.notify_ChargingInfo(plug_sts=PluggerSts.Init,isConnect=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("PluggerConnected",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"           
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_充电枪StatusFault")
    @pytest.mark.full
    def test_close_ChargeLid_PluggerSts_Fault_caseid_1980552(self, ecu):
        self.soa.notify_ChargingInfo(plug_sts=PluggerSts.Fault,isConnect=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        assert self.tsp.log_search_remote_vehicle_control("PluggerConnected",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"           
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_Status==kUnlocked")
    @pytest.mark.full
    def test_close_ChargeLid_ChargeLidSts_kUnlocked_caseid_1980548(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kUnlocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_关_Status==kOpening")
    @pytest.mark.full
    def test_close_ChargeLid_ChargeLidSts_kOpening_caseid_1980547(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpening)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_关_Status==kNA")
    @pytest.mark.full
    def test_close_ChargeLid_ChargeLidSts_kNA_caseid_1980545(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kNA)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远控控制充电口盖_关_Status==kOpened")
    @pytest.mark.full
    def test_close_ChargeLid_ChargeLidSts_kOpened_caseid_1980544(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"    

    @allure.title("远程控制-RVC_远控控制充电口盖_关_Status==kHover")
    @pytest.mark.full
    def test_close_ChargeLid_ChargeLidSts_kHover_caseid_1980546(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kHover)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_Status==kLocked")
    @pytest.mark.full
    def test_close_ChargeLid_Status_kLocked_caseid_1980549(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        time.sleep(1)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)   
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kLocked)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控控制充电口盖_关_超时和Status==kOpened")
    @pytest.mark.full
    def test_close_ChargeLid_ChargeLidSts_timeout_kOpened_caseid_1980542(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        time.sleep(11)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控控制充电口盖_关_超时和Status==kClosed")
    @pytest.mark.full
    def test_close_ChargeLid_ChargeLidSts_timeout_kClosed_caseid_1980543(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        time.sleep(11)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("RVC_远控控制充电口盖_关_超时和Status==kNA")
    @pytest.mark.full
    def test_close_ChargeLid_ChargeLidSts_timeout_kNA_caseid_1980541(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        time.sleep(0.5)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)  
        self.soa.check_ChargeLidService_Close_req(timeout=10)
        time.sleep(11)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kNA)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远控控制充电口盖_开_SOAFail")
    @pytest.mark.full
    def test_open_ChargeLid_SOAFail_caseid_1980602(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kClosed)
        self.soa.soa_partner.stop_single_partner("ChargeLidService_server")
        time.sleep(10)
        execid = self.tsp.rvc_charge_Lidgate()   
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        self.soa.soa_partner.start_single_partner(service="ChargeLidService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("ChargeLidService_server",timeout=30)    

    @allure.title("远程控制-RVC_远控控制充电口盖_关_SOAFail")
    @pytest.mark.full
    def test_close_ChargeLid_SOAFail_caseid_1980551(self, ecu):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.soa.soa_partner.stop_single_partner("ChargeLidService_server")
        time.sleep(10)
        execid = self.tsp.rvc_charge_Lidgate(op=-1)
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        self.soa.soa_partner.start_single_partner(service="ChargeLidService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("ChargeLidService_server",timeout=30)    

    @allure.title("远程控制-RVC_远控控制充电口盖_开_INACTIVE_检查休眠")
    @pytest.mark.sanity
    def test_open_ChargeLid_INACTIVE_hibernate_caseid_1980634(self):
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send()  
        sleep(180) # 避免其他case的指令未执行结束导致TCAM依旧保持唤醒
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_charge_Lidgate()
        self.soa.check_ChargeLidService_Open_req(timeout=15)
        self.soa.notify_ChargeLidService_status(chargelid_sts = ChargeLidSts.kOpened)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  
        time.sleep(180)  # todo: 具体时间不明 涉及VFC
        msg = self.bus_comm.check_bus_recv_message("connectivitycanfd")
        logger.info(f"检查休眠时connectivitycanfd上报文的结果是{msg}")
        assert msg == None, f"远控执行完成之后休眠检查失败"

                                                       
    @allure.title("远程控制-RVC_远控控制充电口盖_开_ABANDONED_TelmFctReq")
    @pytest.mark.full
    def test_open_ChargeLid_ABANDONED_wake_up_TelmFctReq_caseid_1980633(self, ecu):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send()  
        sleep(180) # 避免其他case的指令未执行结束导致TCAM依旧保持唤醒
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=10)
        execid = self.tsp.rvc_charge_Lidgate()
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",13)
        logger.info(f'监控到的数据： {result_ori_1}')
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==25, f"检查休眠唤醒后TelmFctReq发送失败"
        time.sleep(10)
        
    @allure.title("远程控制-RVC_远控控制充电口盖_关_ABANDONED_TelmFctReq")
    @pytest.mark.full
    def test_close_ChargeLid_ABANDONED_wake_up_TelmFctReq_caseid_1980632(self, ecu):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send()  
        sleep(180) # 避免其他case的指令未执行结束导致TCAM依旧保持唤醒
        self.mix.tcam_network_sleep()
        self.bus_comm.check_signal_thread_start("connectivitycanfd","TcamConnectivityFr35", "TelmFctReq", timeout=10)
        execid = self.tsp.rvc_charge_Lidgate(-1) 
        result_ori_1 = self.bus_comm.check_signal_thread_stop("TelmFctReq",13)
        logger.info(f'监控到的数据： {result_ori_1}')
        result_1 = check_signal_num(result_ori_1,1)
        frame_times = result_1[0]
        duration_time = result_1[1]
        logger.info(f"持续发送{frame_times}帧，持续时间为{duration_time}s")
        assert frame_times==25, f"检查休眠唤醒后TelmFctReq发送失败"
        time.sleep(10)
                                                                   
# pytest -vs -p no:warnings remote_control/remote_charging_control/test_chargelid.py

