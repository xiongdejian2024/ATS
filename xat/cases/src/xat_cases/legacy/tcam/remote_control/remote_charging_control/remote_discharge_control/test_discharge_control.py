#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import random

from xat_cases.legacy.abc_demo.case_helper.test_abc_base import TestABCBase
from xat_ecu.api.abc_interface import *


@allure.feature("互联服务/远程控制/远控放电")
@allure.story("远控放电")
class TestDischarge(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server","SeatService_server", 
                         "HighVoltageService_server","VehicleTimeService_server",'HighVoltageAppService_server'])

        sleep(3)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])


    def before_each_func(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_DischargingInfo(isDischarging=False)

    def after_each_func(self, ecu):
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(15)
            if "1990234" in ecu.testname or "1990297" in ecu.testname:
                self.soa.soa_partner.start_single_partner(service="HighVoltageAppService",role="server")
                self.soa.soa_partner.empty_all()
                self.soa.soa_partner.wait_for_service_reconnect("HighVoltageAppService_server",timeout=30)
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.soa.notify_ChargingInfo(is_charging = True)
        time.sleep(1)

    def after_class(self, ecu):
        pass


    @allure.title("远程控制-RVC_远程放电_开_CarMode_FACTORY")
    @pytest.mark.full
    def test_caseid_1990174(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_CarMode_TRANSPORT")
    @pytest.mark.sanity
    def test_caseid_1990207(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_CarMode_CRASH")
    @pytest.mark.full
    def test_caseid_1990208(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_CarMode_DYNO")
    @pytest.mark.full
    def test_caseid_1990209(self, ecu):
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_MntnMode_True")
    @pytest.mark.sanity
    def test_caseid_1990210(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_fota_UPDATE")
    @pytest.mark.sanity
    def test_caseid_1990211(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_fota_ROLLBACK")
    @pytest.mark.sanity
    def test_caseid_1990212(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_Gear_Rvs")
    @pytest.mark.full
    def test_caseid_1990213(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程放电_开_Gear_Neut")
    @pytest.mark.full
    def test_caseid_1990214(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程放电_开_Gear_Drv")
    @pytest.mark.smoke
    def test_caseid_1990215(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程放电_开_Gear_ManMode")
    @pytest.mark.full
    def test_caseid_1990216(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程放电_开_Gear_Resd1")
    @pytest.mark.full
    def test_caseid_1990217(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOn,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_Gear_Resd2")
    @pytest.mark.full
    def test_caseid_1990218(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Resd2)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程放电_开_Gear_Undefd")
    @pytest.mark.full
    def test_caseid_1990219(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Undefd)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程放电_开_UsageMode_DRIVING")
    @pytest.mark.smoke
    def test_caseid_1990220(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程放电_开_不相同指令_设置充电maxSOC")
    @pytest.mark.full
    def test_caseid_1990221(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        self.tsp.rvc_charge_soc_settings()
        execid = self.tsp.rvc_discharge_control(op=1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOn,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_车内有人")
    @pytest.mark.full
    def test_caseid_1990222(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        execid = self.tsp.rvc_discharge_control(op=1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOn,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_插枪")
    @pytest.mark.full
    def test_caseid_1990223(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        self.soa.notify_ChargingInfo(isConnect = True)
        execid = self.tsp.rvc_discharge_control(op=1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOn,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_相同指令")
    @pytest.mark.sanity
    def test_caseid_1990224(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        execid = self.tsp.rvc_discharge_control(op=1)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_相同指令_关")
    @pytest.mark.sanity
    def test_caseid_1990225(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        execid = self.tsp.rvc_discharge_control(op=1)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_不相同指令_充电口盖")
    @pytest.mark.full
    def test_caseid_1990226(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        self.tsp.rvc_charge_Lidgate()
        execid = self.tsp.rvc_discharge_control(op=1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOn,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_不相同指令_停止充电请求")
    @pytest.mark.full
    def test_caseid_1990227(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        self.tsp.rvc_charge_operation(-1)
        execid = self.tsp.rvc_discharge_control(op=1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOn,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_网络管理")
    @pytest.mark.smoke
    def test_caseid_1990228(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_discharge_control(op=1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOn,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=30)

    @allure.title("远程控制-RVC_远程放电_开_正向全流程")
    @pytest.mark.smoke
    def test_caseid_1990229(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_discharge_control(op=1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOn,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=True)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=30)

    @allure.title("远程控制-RVC_远程放电_开_超时后_放电成功")
    @pytest.mark.sanity
    def test_caseid_1990230(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOn,timeout=20)
        sleep(11)
        self.soa.notify_DischargingInfo(isDischarging=True)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_超时后_放电失败")
    @pytest.mark.sanity
    def test_caseid_1990231(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOn,timeout=20)
        sleep(11)
        self.soa.notify_DischargingInfo(isDischarging=False)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_超时后_无响应")
    @pytest.mark.full
    def test_caseid_1990232(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        execid = self.tsp.rvc_discharge_control(op=1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOn,timeout=20)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_网络唤醒失败")
    @pytest.mark.sanity
    def test_caseid_1990233(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_discharge_control(op=1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        assert self.tsp.log_search_remote_vehicle_control("NetwakeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_SOA服务调用失败")
    @pytest.mark.full
    def test_caseid_1990234(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        self.soa.soa_partner.stop_single_partner("HighVoltageAppService_server")
        logger.info("高压app服务已下线")
        execid = self.tsp.rvc_discharge_control(op=1)
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.soa_partner.start_single_partner(service="HighVoltageAppService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("HighVoltageAppService_server",timeout=30)



    @allure.title("远程控制-RVC_远程放电_关_CarMode_FACTORY")
    @pytest.mark.full
    def test_caseid_1990235(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_CarMode_TRANSPORT")
    @pytest.mark.sanity
    def test_caseid_1990236(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_CarMode_CRASH")
    @pytest.mark.full
    def test_caseid_1990237(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.soa.s2s_set_car_mode(car_mode=CarMode.CRASH)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_CarMode_DYNO")
    @pytest.mark.full
    def test_caseid_1990238(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_fota_UPDATE")
    @pytest.mark.sanity
    def test_caseid_1990239(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_MntnMode_True")
    @pytest.mark.sanity
    def test_caseid_1990240(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_fota_ROLLBACK")
    @pytest.mark.sanity
    def test_caseid_1990241(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_Gear_Rvs")
    @pytest.mark.full
    def test_caseid_1990242(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程放电_关_Gear_Neut")
    @pytest.mark.full
    def test_caseid_1990243(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Neut)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程放电_关_SOA服务调用失败")
    @pytest.mark.full
    def test_caseid_1990297(self, ecu):
        self.soa.soa_partner.stop_single_partner("HighVoltageAppService_server")
        logger.info("高压app服务已下线")
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_discharge_control(op=-1)
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.soa_partner.start_single_partner(service="HighVoltageAppService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("HighVoltageAppService_server",timeout=30)

    @allure.title("远程控制-RVC_远程放电_关_网络唤醒失败")
    @pytest.mark.sanity
    def test_caseid_1990298(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        assert self.tsp.log_search_remote_vehicle_control("NetwakeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_超时后_无响应")
    @pytest.mark.full
    def test_caseid_1990299(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOff,timeout=20)
        sleep(10)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_超时后_放电失败")
    @pytest.mark.sanity
    def test_caseid_1990300(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOff,timeout=20)
        sleep(11)
        self.soa.notify_DischargingInfo(isDischarging=False)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_超时后_放电成功")
    @pytest.mark.sanity
    def test_caseid_1990301(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOff,timeout=20)
        sleep(11)
        self.soa.notify_DischargingInfo(isDischarging=True)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_正向全流程")
    @pytest.mark.smoke
    def test_caseid_1990302(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.mix.tcam_network_sleep()            
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOff,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=False)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=30)

    @allure.title("远程控制-RVC_远程放电_关_网络管理")
    @pytest.mark.smoke
    def test_caseid_1990303(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.mix.tcam_network_sleep()
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC30,signal_value=NMSts.valid,timeout=30)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.INACTIVE)
        self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.valid,timeout=30)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOff,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        # self.bus_comm.check_PNC(bus_name=BusName.connectivitycanfd,msg_id=NMMsgId.x509, pnc_name=TCAMPNC.PNC26,signal_value=NMSts.no_valid,timeout=30)

    @allure.title("远程控制-RVC_远程放电_开_不相同指令_停止充电请求")
    @pytest.mark.full
    def test_caseid_1990304(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.tsp.rvc_charge_operation(-1)
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOff,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_开_不相同指令_充电口盖")
    @pytest.mark.full
    def test_caseid_1990305(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.tsp.rvc_charge_Lidgate()
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOff,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_相同指令_关")
    @pytest.mark.sanity
    def test_caseid_1990306(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        execid = self.tsp.rvc_discharge_control(op=-1)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("远程控制-RVC_远程放电_关_相同指令")
    @pytest.mark.sanity
    def test_caseid_1990307(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=False)
        execid = self.tsp.rvc_discharge_control(op=1)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("远程控制-RVC_远程放电_关_插枪")
    @pytest.mark.full
    def test_caseid_1990308(self, ecu):
        self.soa.notify_ChargingInfo(isConnect = True)
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOff,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_车内有人")
    @pytest.mark.full
    def test_caseid_1990309(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.soa.notify_VehicleInsidePersonSts(userInVehicleStatus=True)
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOff,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_不相同指令_设置充电maxSOC")
    @pytest.mark.full
    def test_caseid_1990310(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.tsp.rvc_charge_soc_settings()
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOff,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_UsageMode_DRIVING")
    @pytest.mark.smoke
    def test_caseid_1990311(self, ecu):
        self.soa.notify_DischargingInfo(isDischarging=True)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程放电_关_Gear_Undefd")
    @pytest.mark.full
    def test_caseid_1990312(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Undefd)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程放电_关_Gear_Resd2")
    @pytest.mark.full
    def test_caseid_1990313(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Resd2)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程放电_关_Gear_Resd1")
    @pytest.mark.full
    def test_caseid_1990314(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Resd1)
        self.soa.notify_DischargingInfo(isDischarging=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        self.soa.check_SetDischargingControl_req_and_feedback_resp(cmdtype=CommandType.kOff,timeout=20)
        self.soa.notify_DischargingInfo(isDischarging=False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程放电_关_Gear_ManMode")
    @pytest.mark.full
    def test_caseid_1990315(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.ManMode)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程放电_关_Gear_Drv")
    @pytest.mark.smoke
    def test_caseid_1990316(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Drv)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=-1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程放电_开_fota和挡位")
    @pytest.mark.full
    def test_caseid_1990317(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"     

    @allure.title("远程控制-RVC_远程放电_开_挡位和维修模式")
    @pytest.mark.full
    def test_caseid_1990318(self, ecu):
        self.soa.s2s_set_gear(gear=Gear.Drv)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"  

    @allure.title("远程控制-RVC_远程放电_开_维修模式和使用模式")
    @pytest.mark.full
    def test_caseid_1990319(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程放电_开_使用模式和车辆模式")
    @pytest.mark.full
    def test_caseid_1990320(self, ecu):
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程放电_开_Fota和车辆模式")
    @pytest.mark.full
    def test_caseid_1990321(self, ecu):
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程放电_开_维修模式和车辆模式")
    @pytest.mark.full
    def test_caseid_1990322(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.s2s_set_car_mode(car_mode=CarMode.DYNO)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程放电_开_维修模式和Fota")
    @pytest.mark.full
    def test_caseid_1990323(self, ecu):
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        time.sleep(0.5)
        execid = self.tsp.rvc_discharge_control(op=1)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 