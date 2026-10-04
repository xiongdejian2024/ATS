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


@allure.feature("互联服务/远程控制/远控结束充电")
@allure.story("远控结束充电")

class TestMaxSOC(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server","SeatService_server", 
                         "HighVoltageService_server","VehicleTimeService_server"])
        sleep(3)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])


    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        self.soa.set_tcam_rvc_common_preconditions()
        self.soa.notify_ChargingInfo(is_charging = True)

    def after_each_func(self, ecu):
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(10)
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.soa.notify_ChargingInfo(is_charging = True)
        time.sleep(1)

    def after_class(self, ecu):
        pass

    @allure.title("远程控制-RVC_远程设置SOC_二次远程设置SOC")
    @pytest.mark.full
    def test_max_soc_caseid_1982948(self, ecu):
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=80)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_transport")
    @pytest.mark.sanity
    def test_max_soc_caseid_1982947(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_factory")
    @pytest.mark.full
    def test_max_soc_caseid_1982946(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_维修模式")
    @pytest.mark.sanity
    def test_max_soc_caseid_1982945(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        

    @allure.title("远程控制-RVC_远程设置SOC_FOTAUPDATE")
    @pytest.mark.sanity
    def test_max_soc_caseid_1982944(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远程设置SOC_FOTAROLLBACK")
    @pytest.mark.sanity
    def test_max_soc_caseid_1982943(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_QUERY")
    @pytest.mark.full
    def test_max_soc_caseid_1982942(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=85)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_NEWTASK")
    @pytest.mark.full
    def test_max_soc_caseid_1982941(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=85)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_DOWNLOADING")
    @pytest.mark.full
    def test_max_soc_caseid_1982940(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=85)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_ACTIVE")
    @pytest.mark.full
    def test_max_soc_caseid_1982939(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=85)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_max_soc_caseid_1982938(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=85)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_FAILEDDRIVING")
    @pytest.mark.full
    def test_max_soc_caseid_1982937(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=85)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_SUCCESSFUL")
    @pytest.mark.full
    def test_max_soc_caseid_1982936(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=85)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_max_soc_caseid_1982935(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=85)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_transport与维修模式")
    @pytest.mark.full
    def test_max_soc_caseid_1982934(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_维修模式与FOTA")
    @pytest.mark.full
    def test_max_soc_caseid_1982933(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_abandoned")
    @pytest.mark.smoke
    def test_max_soc_caseid_1982932(self, ecu):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send()  
        sleep(180) # 避免其他case的指令未执行结束导致TCAM依旧保持唤醒
        execid = self.tsp.rvc_charge_soc_settings(max_soc=800)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.resume_all_bus_send()
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=80,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=80)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        time.sleep(180)

    @allure.title("远程控制-RVC_远程设置SOC_inactive")
    @pytest.mark.smoke
    def test_max_soc_caseid_1982931(self, ecu):
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=85)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_convience100%")
    @pytest.mark.full
    def test_max_soc_caseid_1982930(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=1000)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=100,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=100)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_convience50%")
    @pytest.mark.full
    def test_max_soc_caseid_1982929(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=500)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=50,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=50)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_convience80%")
    @pytest.mark.smoke
    def test_max_soc_caseid_1982928(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=800)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=80,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=80)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_active")
    @pytest.mark.full
    def test_max_soc_caseid_1982927(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=800)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=80,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=80)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_driving")
    @pytest.mark.full
    def test_max_soc_caseid_1982926(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=800)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=80,timeout=20)
        self.soa.notify_ChargingInfo(tar_soc=80)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_15s释放")
    @pytest.mark.full
    def test_max_soc_caseid_1982925(self, ecu):
        self.io.tcam_kl15_down()  
        self.bus_comm.pause_all_bus_send()  
        sleep(180) # 避免其他case的指令未执行结束导致TCAM依旧保持唤醒
        execid = self.tsp.rvc_charge_soc_settings(max_soc=800)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.resume_all_bus_send()
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=80,timeout=20)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        time.sleep(180)

    @allure.title("远程控制-RVC_远程设置SOC_结束超时")
    @pytest.mark.full
    def test_max_soc_caseid_1982924(self, ecu):
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        self.soa.check_SetChargeSoc_req_and_feedback_resp(soc=85,timeout=20)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置SOC_调用接口失败")
    @pytest.mark.full
    def test_max_soc_caseid_1982923(self, ecu):
        self.soa.soa_partner.stop_single_partner("HighVoltageService_server")
        logger.info("高压服务已下线")
        time.sleep(10)
        execid = self.tsp.rvc_charge_soc_settings(max_soc=850)
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.soa_partner.start_single_partner(service="HighVoltageService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("HighVoltageService_server",timeout=30)