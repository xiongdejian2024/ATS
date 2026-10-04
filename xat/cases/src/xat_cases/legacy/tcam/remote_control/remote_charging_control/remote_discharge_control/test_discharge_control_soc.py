#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import random

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务/远程控制/远控放电")
@allure.story("远控设置放电SOC")
class TestDischargeSoc(TestABCBase):
    tar_soc = 20

    def before_class(self, ecu):
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server","SeatService_server", 
                         "HighVoltageService_server","VehicleTimeService_server",'HighVoltageAppService_server'])
        sleep(3)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])


    def before_each_func(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.tar_soc = random.randint(20,100)*10
        self.tar_soc = random.randint(20,100)*10
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.soa.notify_ChargingInfo(is_charging = True)

    def after_each_func(self, ecu):
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(15)
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.soa.notify_ChargingInfo(is_charging = True)
        time.sleep(1)

    def after_class(self, ecu):
        pass

    @allure.title("远程控制-RVC_远程设置放电SOC_服务不在线")
    @pytest.mark.smoke
    def test_caseid_1990172(self):
        self.soa.soa_partner.stop_single_partner("HighVoltageService_server")
        logger.info("高压服务已下线")
        time.sleep(10)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.soa_partner.start_single_partner(service="HighVoltageService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("HighVoltageService_server",timeout=30)

    @allure.title("远程控制-RVC_远程设置放电SOC_结束超时")
    @pytest.mark.smoke
    def test_caseid_1990173(self, ecu):
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_15s释放PNC")
    @pytest.mark.sanity
    def test_caseid_1990175(self, ecu):
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)
        time.sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=30)

    @allure.title("远程控制-RVC_远程设置放电SOC_driving")
    @allure.issue('https://jira.jiduauto.com/browse/SOA-29436?filter=-2')
    @pytest.mark.sanity
    def test_caseid_1990176(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.no_valid,timeout=30)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_active")
    @pytest.mark.full
    def test_caseid_1990177(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.no_valid,timeout=30)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_convience")
    @pytest.mark.sanity
    def test_caseid_1990178(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.no_valid,timeout=30)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_inactive")
    @pytest.mark.sanity
    def test_caseid_1990179(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_abandoned")
    @pytest.mark.smoke
    def test_caseid_1990180(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_维修模式与FOTA")
    @pytest.mark.full
    def test_caseid_1990181(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程设置放电SOC_transport与维修模式")
    @pytest.mark.full
    def test_caseid_1990182(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程设置放电SOC_transport与FOTA")
    @pytest.mark.full
    def test_caseid_1990183(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程设置放电SOC_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_caseid_1990184(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程设置放电SOC_SUCCESSFUL")
    @pytest.mark.full
    def test_caseid_1990185(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_FAILEDDRIVING")
    @pytest.mark.full
    def test_caseid_1990186(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_caseid_1990187(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_ACTIVE")
    @pytest.mark.full
    def test_caseid_1990188(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_DOWNLOADING")
    @pytest.mark.full
    def test_caseid_1990189(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_NEWTASK")
    @pytest.mark.full
    def test_caseid_1990190(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_QUERY")
    @pytest.mark.full
    def test_caseid_1990191(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_FOTA_ROLLBACK")
    @allure.issue('https://jira.jiduauto.com/browse/SOA-29436?filter=-2')
    @pytest.mark.sanity
    def test_caseid_1990192(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_FOTA_UPDATE")
    @pytest.mark.smoke
    def test_caseid_1990193(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_MntnMode_True")
    @pytest.mark.full
    def test_caseid_1990194(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_Carmode_factory")
    @pytest.mark.full
    def test_caseid_1990195(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_Carmode_transport")
    @pytest.mark.full
    def test_caseid_1990196(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_二次远程设置SOC")
    @pytest.mark.sanity
    def test_caseid_1990197(self, ecu):
        soc = random.randint(20,100)*10
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=soc)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_插枪中")
    @pytest.mark.full
    def test_caseid_1990198(self, ecu):
        self.soa.notify_ChargingInfo(isConnect = True)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_其他指令_充电口盖开")
    @pytest.mark.full
    def test_caseid_1990199(self, ecu):
        self.tsp.rvc_charge_Lidgate()
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_其他指令_设置充电目标SOC")
    @pytest.mark.full
    def test_caseid_1990200(self, ecu):
        self.tsp.rvc_charge_soc_settings()
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_其他指令_解锁")
    @pytest.mark.full
    def test_caseid_1990201(self, ecu):
        self.tsp.rvc_lock_control(1)
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_PNC置位")
    @pytest.mark.full
    def test_caseid_1990202(self, ecu):
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_收到其他值")
    @pytest.mark.full
    def test_caseid_1990203(self, ecu):
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        if self.tar_soc == 20.0:
            soc = self.tar_soc + 1
        elif self.tar_soc == 100.0:
            soc = self.tar_soc - 1
        else:
            soc = self.tar_soc - 2
        self.soa.notify_DischargingInfo(dischargeLimitSoc=soc)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_超时后收到其他值")
    @pytest.mark.full
    def test_caseid_1990204(self, ecu):
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        if self.tar_soc == 20.0:
            soc = self.tar_soc + 1
        elif self.tar_soc == 100.0:
            soc = self.tar_soc - 1
        else:
            soc = self.tar_soc - 2
        sleep(13)
        self.soa.notify_DischargingInfo(dischargeLimitSoc=soc)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程设置放电SOC_超时后收到目标值")
    @pytest.mark.full
    def test_caseid_1990205(self, ecu):
        execid = self.tsp.rvc_discharge_control_soc_settings(lowerLimit=self.tar_soc)
        self.soa.check_SetDischargeLimitSoc_req_and_feedback_resp(soc=self.tar_soc/10,timeout=20)  
        sleep(13)
        self.soa.notify_DischargingInfo(dischargeLimitSoc=self.tar_soc/10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"