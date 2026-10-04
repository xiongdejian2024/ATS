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
class TestStopOrStartCharge(TestABCBase):
    def before_class(self, ecu):
        self.soa.update([ "VehicleModeService_server", "FotaMasterService_server",
                         "VehicleSetStatusService_server", "ChassisService_server","SeatService_server", 
                         "HighVoltageService_server","VehicleTimeService_server",'HighVoltageAppService_server'])
        sleep(3)
        self.tsp.set_bench_config(self.tb_config["vid"], self.tb_config["tel"])


    def before_each_func(self, ecu):
        self.soa.empty_all()
        self.io.tcam_kl15_up()
        logger.info("检查时间同步状态： {0}".format(self.ssh.tcam_ssh.exec("date")))
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)
        

    def after_each_func(self, ecu):
        if ecu.testresult == 'Failure':
            logger.info('用例执行失败')
            sleep(10)
        if '1982887' in ecu.testname and ecu.testresult == 'Failure':
            self.soa.soa_partner.start_single_partner(service="HighVoltageAPPService",role="server")
            self.soa.soa_partner.empty_all()
            self.soa.soa_partner.wait_for_service_reconnect("HighVoltageAPPService_server",timeout=30)
        self.io.tcam_kl15_up()
        self.soa.set_tcam_rvc_common_preconditions()
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.INACTIVE)

        time.sleep(1)

    def after_class(self, ecu):
        pass

    @allure.title("远程控制-RVC_远控结束充电_二次结束充电")
    @pytest.mark.full
    def test_rvc_stop_charge_caseid_1982916(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_SeatOccupyStatus(rawsensorstatus=[1,1,1,1,1])
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_charge_operation(-1)
        # self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        execid = self.tsp.rvc_charge_operation(-1)
        # self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("SysBusy",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("远程控制-RVC_远程结束充电_StartOK")
    @pytest.mark.full
    def test_rvc_stop_charge_caseid_1982915(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("StartOK",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        sleep(10)

    @allure.title("远程控制-RVC_远程结束充电_transport")
    @pytest.mark.sanity
    def test_stop_charge_caseid_1982914(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_factory")
    @pytest.mark.full
    def test_stop_charge_caseid_1982913(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_car_mode(car_mode=CarMode.FACTORY)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_driving")
    @pytest.mark.sanity
    def test_stop_charge_caseid_1982912(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_维修模式")
    @pytest.mark.sanity
    def test_stop_charge_caseid_1982911(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程结束充电_N档")
    @pytest.mark.sanity
    def test_stop_charge_caseid_1982910(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"   

    @allure.title("远程控制-RVC_远程结束充电_D档")
    @pytest.mark.full
    def test_stop_charge_caseid_1982909(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_gear(gear=Gear.Drv)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程结束充电_R档")
    @pytest.mark.full
    def test_stop_charge_caseid_1982908(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_gear(gear=Gear.Rvs)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"        

    @allure.title("远程控制-RVC_远程结束充电_FOTAUPDATE")
    @pytest.mark.sanity
    def test_stop_charge_caseid_1982907(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远程结束充电_FOTAROLLBACK")
    @pytest.mark.full
    def test_stop_charge_caseid_1982906(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_fota_status(state=FOTAMasteSts.ROLLBACK)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_未充电")
    @pytest.mark.full
    def test_stop_charge_caseid_1982905(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = False)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控结束充电_QUERY")
    @pytest.mark.full
    def test_stop_charge_caseid_1982904(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_fota_status(state=FOTAMasteSts.QUERY)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_NEWTASK")
    @pytest.mark.full
    def test_stop_charge_caseid_1982903(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_fota_status(state=FOTAMasteSts.NEW_TASK)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_DOWNLOADING")
    @pytest.mark.full
    def test_stop_charge_caseid_1982902(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_fota_status(state=FOTAMasteSts.DOWNLOADING)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_ACTIVE")
    @pytest.mark.full
    def test_stop_charge_caseid_1982901(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_fota_status(state=FOTAMasteSts.ACTIVE)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_FAILEDNOTDRIVING")
    @pytest.mark.full
    def test_stop_charge_caseid_1982900(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_NOT_DRIVING)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_FAILEDDRIVING")
    @pytest.mark.full
    def test_stop_charge_caseid_1982899(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_fota_status(state=FOTAMasteSts.FAILED_DRIVING)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_SUCCESSFUL")
    @pytest.mark.full
    def test_stop_charge_caseid_1982898(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_fota_status(state=FOTAMasteSts.SUCCESSFUL)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_REACHAPPOINTMENT")
    @pytest.mark.full
    def test_stop_charge_caseid_1982897(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.notify_fota_status(state=FOTAMasteSts.REACH_APPOINTMENT)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_transport与driving")
    @pytest.mark.full
    def test_stop_charge_caseid_1982896(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_car_mode(car_mode=CarMode.TRANSPORT)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_driving与维修模式")
    @pytest.mark.full
    def test_stop_charge_caseid_1982895(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.DRIVING)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.DRIVING)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程结束充电_维修模式与N档")
    @pytest.mark.full
    def test_stop_charge_caseid_1982894(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_mntnmode(mntnmode=True)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远程结束充电_N档与FOTA")
    @pytest.mark.full
    def test_stop_charge_caseid_1982893(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_gear(gear=Gear.Neut)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_charge_operation(-1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败" 

    @allure.title("远程控制-RVC_远控结束充电_abandoned")
    @pytest.mark.full
    def test_stop_charge_caseid_1982892(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ABANDONED)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控结束充电_inactive")
    @pytest.mark.smoke
    def test_stop_charge_caseid_1982891(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控结束充电_convience")
    @pytest.mark.sanity
    def test_stop_charge_caseid_1982890(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.CONVENIENCE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.CONVENIENCE)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控结束充电_active")
    @pytest.mark.sanity
    def test_stop_charge_caseid_1982889(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.s2s_set_usage_mode(usage_mode=UsageMode.ACTIVE)
        self.bus_comm.set_usage_mode_to_tcam(usage_mode=UsageMode.ACTIVE)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        self.soa.notify_ChargingInfo(is_charging = False)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控结束充电_结束超时")
    @pytest.mark.full
    def test_stop_charge_caseid_1982888(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        execid = self.tsp.rvc_charge_operation(-1)
        self.soa.check_SetChargingControl_req(com_type=ControlCommandType.kOff,timeout=10)
        time.sleep(5)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远控结束充电_调用接口失败")
    @pytest.mark.full
    def test_stop_charge_caseid_1982887(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = True)
        self.soa.soa_partner.stop_single_partner("HighVoltageAppService_server")
        time.sleep(10)
        execid = self.tsp.rvc_charge_operation(-1)
        time.sleep(50)
        assert self.tsp.log_search_remote_vehicle_control("SOAFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        self.soa.soa_partner.start_single_partner(service="HighVoltageAppService",role="server")
        self.soa.soa_partner.empty_all()
        self.soa.soa_partner.wait_for_service_reconnect("HighVoltageAppService_server",timeout=30)    

    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_ACCharging")
    @pytest.mark.full
    def test_caseid_1990901(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.ACCharging)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"
        
    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_ACChargingEnd")
    @pytest.mark.full
    def test_caseid_1990951(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.ACChargingEnd)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_ChargingCmpl")
    @pytest.mark.full
    def test_caseid_1990950(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.ChargingCmpl)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_Heating")
    @pytest.mark.full
    def test_caseid_1990949(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Heating)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_NoDischarging")
    @pytest.mark.full
    def test_caseid_1990948(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.NoDischarging)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_Discharging")
    @pytest.mark.full
    def test_caseid_1990947(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Discharging)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_DischargingEnd")
    @pytest.mark.full
    def test_caseid_1990946(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.DischargingEnd)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_DischargingCmpl")
    @pytest.mark.full
    def test_caseid_1990945(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.DischargingCmpl)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_Chargingfault")
    @pytest.mark.full
    def test_caseid_1990944(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Chargingfault)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_DischargingFault")
    @pytest.mark.full
    def test_caseid_1990943(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.DischargingFault)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_ACChrgnFltChrgrSide")
    @pytest.mark.full
    def test_caseid_1990942(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.ACChrgnFltChrgrSide)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_DCCharging")
    @pytest.mark.full
    def test_caseid_1990941(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.DCCharging)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_DCChrgnFltVehSide")
    @pytest.mark.full
    def test_caseid_1990940(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.DCChrgnFltVehSide)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_DCChrgnFltChrgrSideTempFlt")
    @pytest.mark.full
    def test_caseid_1990939(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.DCChrgnFltChrgrSideTempFlt)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_DCChrgnFltChrgrSideConFlt")
    @pytest.mark.full
    def test_caseid_1990938(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.DCChrgnFltChrgrSideConFlt)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_DCChrgnFltChrgrSideHwFlt")
    @pytest.mark.full
    def test_caseid_1990937(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.DCChrgnFltChrgrSideHwFlt)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_DCChrgnFltChrgrSideEmgyFlt")
    @pytest.mark.full
    def test_caseid_1990936(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.DCChrgnFltChrgrSideEmgyFlt)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_DCChrgnFltChrgrSideComFlt")
    @pytest.mark.full
    def test_caseid_1990935(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.DCChrgnFltChrgrSideComFlt)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_SuperCharging")
    @pytest.mark.full
    def test_caseid_1990934(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.SuperCharging)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_ACChargingSuspend")
    @pytest.mark.full
    def test_caseid_1990933(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.ACChargingSuspend)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_DCChargingEnd")
    @pytest.mark.full
    def test_caseid_1990932(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.DCChargingEnd)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_ACChrgnFltVehSide")
    @pytest.mark.full
    def test_caseid_1990931(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.ACChrgnFltVehSide)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_Boostcharging")
    @pytest.mark.full
    def test_caseid_1990930(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Boostcharging)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_BoostchargingFlt")
    @pytest.mark.full
    def test_caseid_1990929(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.BoostchargingFlt)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_前提条件_充电中_WirelessCharging")
    @pytest.mark.full
    def test_caseid_1990928(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.WirelessCharging)
        sleep(1)
        execid = self.tsp.rvc_charge_operation(1)

        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程开始充电_前提条件优先级_充电中与OTA")
    @pytest.mark.full
    def test_caseid_1990902(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.ACChargingEnd)
        self.soa.notify_fota_status(state=FOTAMasteSts.UPDATE)
        execid = self.tsp.rvc_charge_operation(1)
        assert self.tsp.log_search_remote_vehicle_control("OTAOngoing",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程开始充电_前提条件优先级_充电中与挡位")
    @pytest.mark.full
    def test_caseid_1990903(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.ACChargingEnd)
        self.soa.s2s_set_gear(Gear.Drv)
        execid = self.tsp.rvc_charge_operation(1)
        assert self.tsp.log_search_remote_vehicle_control("ParkFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程开始充电_前提条件优先级_充电中与维修模式")
    @pytest.mark.full
    def test_caseid_1990904(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.ACChargingEnd)
        self.soa.s2s_set_mntnmode(True)
        execid = self.tsp.rvc_charge_operation(1)
        assert self.tsp.log_search_remote_vehicle_control("MntnMode",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程开始充电_前提条件优先级_充电中与使用模式")
    @pytest.mark.full
    def test_caseid_1990905(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.ACChargingEnd)
        self.soa.s2s_set_usage_mode(UsageMode.DRIVING)
        execid = self.tsp.rvc_charge_operation(1)
        assert self.tsp.log_search_remote_vehicle_control("UsageModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程开始充电_前提条件优先级_充电中与车辆模式")
    @pytest.mark.full
    def test_caseid_1990906(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.ACChargingEnd)
        self.soa.s2s_set_car_mode(CarMode.TRANSPORT)
        execid = self.tsp.rvc_charge_operation(1)
        assert self.tsp.log_search_remote_vehicle_control("CarModeFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程开始充电_未充电_不在预约中_NoDisplay")
    @pytest.mark.full
    def test_caseid_1990907(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default)
        self.soa.notify_DisplayBookChargingInfo(DisplayBookChargingType.kNoDisplay)
        execid = self.tsp.rvc_charge_operation(1)
        assert self.tsp.log_search_remote_vehicle_control("NoAcBookCharging",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程开始充电_未充电_不在预约中_kDC")
    @pytest.mark.full
    def test_caseid_1990908(self, ecu):
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default)
        self.soa.notify_DisplayBookChargingInfo(DisplayBookChargingType.kDC)
        execid = self.tsp.rvc_charge_operation(1)
        assert self.tsp.log_search_remote_vehicle_control("NoAcBookCharging",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程开始充电_未充电_在预约中_充电成功")
    @pytest.mark.smoke
    def test_caseid_1990909(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = False)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default)
        self.soa.notify_DisplayBookChargingInfo(DisplayBookChargingType.kAC)
        execid = self.tsp.rvc_charge_operation(1)
        self.soa.check_SetChargingControl_req_and_feedback_resp(ControlCommandType.kOn)
        self.soa.notify_ChargingInfo(is_charging = True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程开始充电_未充电_在预约中_超时后充电成功")
    @pytest.mark.full
    def test_caseid_1990910(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = False)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default)
        self.soa.notify_DisplayBookChargingInfo(DisplayBookChargingType.kAC)
        execid = self.tsp.rvc_charge_operation(1)
        self.soa.check_SetChargingControl_req_and_feedback_resp(ControlCommandType.kOn)
        sleep(11)
        self.soa.notify_ChargingInfo(is_charging = True)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程开始充电_未充电_在预约中_超时")
    @pytest.mark.full
    def test_caseid_1990911(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = False)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Default)
        self.soa.notify_DisplayBookChargingInfo(DisplayBookChargingType.kAC)
        execid = self.tsp.rvc_charge_operation(1)
        self.soa.check_SetChargingControl_req_and_feedback_resp(ControlCommandType.kOn)
        sleep(11)
        assert self.tsp.log_search_remote_vehicle_control("DelayFail",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"


    @allure.title("远程控制-RVC_远程开始充电_未充电_NoCharging_在预约中_充电成功")
    @pytest.mark.smoke
    def test_caseid_1990912(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = False)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.NoCharging)
        self.soa.notify_DisplayBookChargingInfo(DisplayBookChargingType.kAC)
        execid = self.tsp.rvc_charge_operation(1)
        self.soa.check_SetChargingControl_req_and_feedback_resp(ControlCommandType.kOn)
        self.soa.notify_ChargingInfo(is_charging = True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"

    @allure.title("远程控制-RVC_远程开始充电_未充电_NoCharging_在预约中_充电成功")
    @pytest.mark.smoke
    def test_caseid_1990913(self, ecu):
        self.soa.notify_ChargingInfo(is_charging = False)
        self.soa.notify_ChargingInfo(charg_sts=ChargingSts.Booking)
        self.soa.notify_DisplayBookChargingInfo(DisplayBookChargingType.kAC)
        execid = self.tsp.rvc_charge_operation(1)
        self.soa.check_SetChargingControl_req_and_feedback_resp(ControlCommandType.kOn)
        self.soa.notify_ChargingInfo(is_charging = True)
        assert self.tsp.log_search_remote_vehicle_control("Success",execid=execid),f"TCAM远程控制上报到车云的结果校验失败"